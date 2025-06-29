"""
A quick runpoint for the "app" to show the main results and the endpoint. More info in README.md.

Before running the code please run the below in bash or terminal to start a local server:
uvicorn main.api:api --reload
"""

import requests
from main.main import MainApp


if __name__ == "__main__":
    main_app = MainApp()
    scrapchef_inputs = main_app.run(from_api=False)
    response = requests.post("http://127.0.0.1:8000/september_batches/").json()
    print("kot")