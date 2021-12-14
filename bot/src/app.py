# from typing import Optional
from fastapi import FastAPI
import os

from utils.requestor import get_request

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World, From Bot App."}


@app.get("/trade")
def trade():
    predict_api_endpoint = os.environ.get("PREDICT_API_ENDPOINT", "http://localhost:8000/")
    predict = get_request(predict_api_endpoint)
    return {"results": predict}
