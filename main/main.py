import pandas as pd
import numpy as np
import requests
from sqlalchemy import inspect
from constants import (GET_DATA_API_ENDPOINT,DATA_INPUT_FOLDER, DAILY_CHARGE_SCHEDULE,
                       PRODUCT_GROUP_MONTHLY, STEEL_GRADE_PRODUCTION, PRODUCT_GRADE_MAPPING)
import os
from main.setup_db import DB

class MainApp:

    def run(self, from_api: bool = False):

        if not from_api:
            files = self.read_files_from_disk()
        else:
            files = self.read_files_from_api()

        db = DB()
        db.write_files_to_db_tables(files)

        production_history = files[STEEL_GRADE_PRODUCTION]
        steel_grade_orders = files[PRODUCT_GROUP_MONTHLY]

        snapchef_grade_breakdown = self.get_grade_batch_breakdown_for_september(production_history, steel_grade_orders)

        return snapchef_grade_breakdown

    def get_grade_batch_breakdown_for_september(self, production_history: pd.DataFrame, steel_grade_orders: pd.DataFrame):
        """
        The grade breakdown for the upcoming September order is not given and needs to be inferred from historic data
        and the charge schedule from the first day of September.

        The logic applied changes from product type to product type based on the historic data:

        Rebar
        For rebars it can be seen that as the total number of orders/batches produced changes the number of B500A and
        B500B grades remains roughly the same and what changes is the B500C. Thus, the best way to predict the breakdown
        for this product is by taking the 3 month average for B500A and B500B total production and subtracting it
        from the total rebars needed for Septemeber. This will give the total for B500C.

        MBQ
        For MBQ there is a change in production/orders after June where the only grades needed in July and August are 44W, 50W, A36.
        Since the orders in September are in the range of the orders in July/August, it would make sense that the grades needed
        are the same as those in July and August (so 44W, 50W and A36). It is assumed that the number of A36 batches remains
        the same in September (since it is the same in July and August), whereas the breakdown between the other two grades is found by using
        the average of the percentage that each grade has in the total production for each month.

        SBQ
        There are two ways to approach this, and number 1 below was implemented as it is the one that makes the least
        assumptions about the data:
        1.
        For SBQ the production/orders reduce from June to July and August, but the number of C40 batches remains the same.
        So for September we can assume that the number of C40 batches needed remains the same, the number of
        S235JR and S355J batches remains the same as in June, whereas the difference is covered by C35 grade steel
        which we know is needed from the production schedule for the 1st of September.

        2.
        The logic is similar to the one above however looking at the daily charge schedule it is clear that the
        plant operates with fixed shifts, and changing from one product type to the other requires time, and it is
        the next shift that picks the new product up. So when looking at 1/9/2024 (first day of Sept), there is a shift
        that starts at 4AM that makes only 1 batch of C35 and 1 batch of C40, and then there is a changeover in product
        type to B500B which is picked up by the next shift. This doesn't seem like the most efficient way of doing things
        (of course scheduling is impacted by many other things), so it might be that for September all that is needed is
        1 batch of C35 and 1 batch of C40. The rest are split up equally between S235JR and S355J.

        CHQ
        For CHQ it is harder to distinguish a clear pattern from the data, so we will assume that A53/A543 and A53/C591
        are both needed in equal amounts in September.
        """

        production_history = production_history.set_index("date") / 100
        production_history.reset_index(inplace=True)
        grade_batches = {}

        for product_type, grades in PRODUCT_GRADE_MAPPING.items():

            if product_type == "Rebar":
                grades_to_avg = ["B500A", "B500B"]
                grade_avg = 0
                for grade in grades_to_avg:
                    grade_avg = production_history[grade].mean()
                    grade_batches[grade] = np.round(grade_avg)
                grade_batches["B500C"] = np.round(self.get_order_total_for_product_and_month(steel_grade_orders, 9, product_type) -
                                                  sum([grade_batches["B500A"], grade_batches["B500B"]]))

            elif product_type == "MBQ":
                grade_44W_percentage_july = production_history[production_history["date"].dt.month == 7]["44W"].iloc[0] \
                                        / (self.get_order_total_for_product_and_month(steel_grade_orders, 7, product_type) - 2)
                grade_44W_percentage_august = production_history[production_history["date"].dt.month == 8]["44W"].iloc[0] \
                                        / (self.get_order_total_for_product_and_month(steel_grade_orders, 8, product_type) - 2)
                avg_grade_44W_perc = grade_44W_percentage_july + grade_44W_percentage_august / 2
                avg_grade_50W_perc = 1 - avg_grade_44W_perc

                grade_batches["A36"] = 2
                grade_batches["44W"] = np.round(avg_grade_44W_perc * (self.get_order_total_for_product_and_month(steel_grade_orders, 9, product_type) - 2))
                grade_batches["50W"] = np.round(avg_grade_50W_perc * (self.get_order_total_for_product_and_month(steel_grade_orders, 9, product_type) - 2))

            elif product_type == "SBQ":
                grades_to_consider = ["S235JR", "S355J", "C40"]
                for grade in grades_to_consider:
                    grade_batches[grade] = np.round(production_history[production_history["date"].dt.month == 6][grade].iloc[0])
                grade_batches["C35"] =np.round(self.get_order_total_for_product_and_month(steel_grade_orders, 9, product_type) \
                                       - sum([grade_batches["S235JR"], grade_batches["S355J"], grade_batches["C40"]]))

            elif product_type == "CHQ":
                grade_batches["A53/A543"] = np.round(self.get_order_total_for_product_and_month(steel_grade_orders, 9, product_type) * 0.5)
                grade_batches["A53/C591"] = np.round(self.get_order_total_for_product_and_month(steel_grade_orders, 9, product_type) * 0.5)

        return grade_batches

    @staticmethod
    def get_order_total_for_product_and_month(steel_grade_orders: pd.DataFrame, month: int, product_type: str):
        """
        Helper method that gets the total number of batches ordered for a given month and product type
        """
        month_row = steel_grade_orders[steel_grade_orders['date'].dt.month == month]
        month_value = month_row[product_type].iloc[0]

        return month_value


    def read_files_from_disk(self):
        """
        Reads the files from /data/main instead of calling the API
        """
        files = {}

        for f in os.listdir(DATA_INPUT_FOLDER):
            if f.endswith(".csv"):
                files[f.removesuffix(".csv")] = pd.read_csv(DATA_INPUT_FOLDER / f)

        self.convert_to_datetime(files.values())

        return files

    def read_files_from_api(self):
        """
        Tests that the API works by calling the get file endpoint of the API. To run this the following needs to be
        ran in the terminal:

        uvicorn main.api:api --reload
        """
        response = requests.get(f"http://localhost:8000{GET_DATA_API_ENDPOINT}")
        files = response.json()["files"]
        dfs = {}
        for file in files:
            filename = (file["filename"]).removesuffix(".csv")
            dfs[filename] = pd.DataFrame(file["data"])

        self.convert_to_datetime(dfs.values())

        return dfs

    @staticmethod
    def convert_to_datetime(dfs):
        """
        Helper method that converts the relevant df column to datetime
        """
        for df in dfs:
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            elif "Start time" in df.columns:
                df["Start time"] = pd.to_datetime(df["Start time"])

        return dfs