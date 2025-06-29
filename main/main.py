import pandas as pd
import requests
from constants import (GET_DATA_API_ENDPOINT,DATA_INPUT_FOLDER, DAILY_CHARGE_SCHEDULE,
                       PRODUCT_GROUP_MONTHLY, STEEL_GRADE_PRODUCTION, PRODUCT_GRADE_MAPPING)
import os
from setup_db_tables import DBTables
from setup_db import engine

class MainApp:

    def process_files(self, files: {}):
        """
        Method that uses the provided files to make hourly production schedule
        """
        production_history = files[PRODUCT_GROUP_MONTHLY]
        steel_grade_production = files[STEEL_GRADE_PRODUCTION]
        daily_charge_schedule_initial = files[DAILY_CHARGE_SCHEDULE]



    def get_grade_breakdown_for_september(self, production_history: pd.DataFrame, steel_grade_orders: pd.DataFrame):
        """
        The grade breakdown for the upcoming September order is not given and needs to be inferred from historic data
        and the charge schedule from the first day of September
        """
        for product_type, grades in PRODUCT_GRADE_MAPPING.items():





    def write_files_to_db_tables(self, files: {}):
        """
        Method that creates the database tables them and writes the data to them
        """

        db_tables = DBTables()
        db_tables.create_tables()

        for filename, file in files.items:
            file.to_sql(filename, con=engine, if_exists="replace", index=False)

    def read_files_from_disk(self):
        """
        Reads the files from /data/main instead of calling the API
        """
        files = [
            {
                "filename": f,
                "data": pd.read_csv(DATA_INPUT_FOLDER / f)
            }
            for f in os.listdir(DATA_INPUT_FOLDER)
            if f.endswith(".csv")
        ]
        return {"files": files}

    def get_files_from_api(self):
        """
        Reads the file from the API instead of the disk. Useful to test the API. Files given in README.md
        """
        response = requests.get(f"http://localhost:8000{GET_DATA_API_ENDPOINT}")
        files = response.json()["files"]
        dfs = {}
        for file in files:
            dfs[file["filename"]] = pd.DataFrame(file["data"])

        return dfs



if __name__ == "__main__":

    main_app = MainApp()
    dfs = get_files_from_api()
    print("kot")