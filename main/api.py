from fastapi import FastAPI
import os
from constants import DATA_INPUT_FOLDER, GET_DATA_API_ENDPOINT
import pandas as pd


api = FastAPI()

@api.get(GET_DATA_API_ENDPOINT)
def get_csv_data():
    files = [
        {
            "filename": f,
            "data": pd.read_csv(DATA_INPUT_FOLDER / f).to_dict(orient="records")
        }
        for f in os.listdir(DATA_INPUT_FOLDER)
        if f.endswith(".csv")
    ]
    return {"files": files}




