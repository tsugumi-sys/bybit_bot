# from typing import Optional
from fastapi import FastAPI, HTTPException
import os

from fastapi.params import Query

from utils.request import request_predict_endpoint
from utils.trade import Trade
from utils.interfaces import Settings

app = FastAPI()

settings = Settings()
trader = Trade(settings.BYBIT_API_KEY, settings.BYBIT_SECRET_KEY, settings.API_BASE_URL)


@app.get("/")
def read_root():
    return {"Hello": "World, From Bot App."}


@app.get("/trade")
def trade(symbol: str = Query(..., description="The target pair name of Bybit USDT Perpetual.")):  # type: ignore
    if symbol not in trader.symbols_list():
        raise HTTPException(status_code=404, detail=f"Invalid symbol {symbol}")
    # predict_api_endpoint = os.environ.get("PREDICT_API_ENDPOINT", "http://localhost:8000/")
    # predict = request_predict_endpoint(predict_api_endpoint)
    predict = 1.0
    return {"results": predict}
