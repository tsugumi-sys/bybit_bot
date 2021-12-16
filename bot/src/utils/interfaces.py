from typing import TypedDict, List, Dict
from pydantic import BaseSettings


class MyPositionAmount(TypedDict):
    buy: float
    sell: float


class MyPositionLeverage(TypedDict):
    buy_leverage: float
    sell_leverage: float


class BYBIT_API_RETURN(TypedDict):
    ret_code: str
    ret_msg: str
    ext_code: str
    ext_info: str
    retult: List[Dict]


class Settings(BaseSettings):
    BYBIT_API_KEY: str
    BYBIT_SECRET_KEY: str
    API_BASE_URL: str
    API_NAME: str

    class Config:
        env_file = "../.env"
