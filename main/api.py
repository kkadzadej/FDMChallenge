from fastapi import FastAPI
import os
from constants import DATA_INPUT_FOLDER, GET_DATA_API_ENDPOINT, POST_RESULT_API_ENDPOINT
import pandas as pd
from main.main import MainApp

api = FastAPI()

@api.get("/")
def home():
    return "FDM Challenge API"

@api.get(POST_RESULT_API_ENDPOINT)
def post_september_results():
    main_app = MainApp()
    snapchef_grade_batches_for_september = main_app.run(from_api=False)

    return snapchef_grade_batches_for_september

@api.get(GET_DATA_API_ENDPOINT)
def get_data():
    files = [
        {
            "filename": f,
            "data": pd.read_csv(DATA_INPUT_FOLDER / f).to_dict(orient="records")
        }
        for f in os.listdir(DATA_INPUT_FOLDER)
        if f.endswith(".csv")
    ]
    return {"files": files}




