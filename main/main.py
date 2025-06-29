import pandas as pd
import requests
from constants import GET_DATA_API_ENDPOINT
from setup_db_tables import DBTables

class MainApp:

    def write_files_to_db_tables(self, file_dfs: {}):
        """
        Method that creates the database tables them and writes the data to them
        """
        db_tables = DBTables()
        db_tables.create_tables()







    def get_files_from_api(self):
        response = requests.get(f"http://localhost:8000{GET_DATA_API_ENDPOINT}")
        files = response.json()["files"]
        dfs = {}
        for file in files:
            dfs[file["filename"]] = pd.DataFrame(file["data"])

        return dfs



if __name__ == "__main__":

    dfs = get_files_from_api()
    print("kot")