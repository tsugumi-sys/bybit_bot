from datetime import datetime, timedelta
import pandas as pd
from pybit import HTTP
from pybit.exceptions import FailedRequestError, InvalidRequestError
from typing import List, Any, Union
import logging

logger = logging.getLogger(__name__)


class Bybit:
    def __init__(self, api_key: str, api_secret: str, base_url: str) -> None:
        if base_url not in ["https://api.bybit.com"]:
            raise ValueError(f"Invalid 'base_url' {base_url}. base_url should be in ['https://api.bybit.com']")

        self.session = HTTP(base_url, api_key=api_key, api_secret=api_secret)

    def symbols_list(self) -> List[str]:
        res: Any = self.session.query_symbol()
        symbols = [s["name"] for s in res["result"] if "name" in s]
        symbols = [s for s in symbols if "USDT" in s]
        return symbols

    def kline_dataframe(self, symbol: str, interval: str) -> Union[pd.DataFrame, str]:
        if symbol.upper() not in self.symbols_list():
            raise ValueError(f"Invalid symbol {symbol} for Bybit USDT Perpetual.")

        now = datetime.now()
        from_timestamp = str(int(datetime.timestamp(now - timedelta(days=2))))

        try:
            res = self.session.query_kline(symbol=symbol.upper(), interval=interval, from_time=from_timestamp)
            df = pd.DataFrame(res["result"])
            df = df.set_index("open_time")
            df = df.sort_index()

            target_cols = ["open", "high", "low", "close", "volume"]
            return df[target_cols]
        except FailedRequestError as e:
            err_msg = f"FailedRequestError: {e.message} (Bybit.{self.kline_dataframe.__name__})"
            logger.error(err_msg)
            return err_msg
        except InvalidRequestError as e:
            err_msg = f"InvalidRequestError: {e.message} (Bybit.{self.kline_dataframe.__name__})"
            logger.error(err_msg)
            return err_msg
