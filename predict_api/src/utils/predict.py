import pandas as pd
from utils.feature_aggrigation import agg_feature
from utils.kline import Bybit
from utils.interfaces import Settings

settings = Settings()


def predict(symbol: str, interval: str):
    bybit = Bybit(settings.BYBIT_API_KEY, settings.BYBIT_SECRET_KEY, settings.API_BASE_URL)
    kline_df = bybit.kline_dataframe(symbol=symbol, interval=interval)
    if isinstance(kline_df, pd.DataFrame):
        features_df = agg_feature(kline_df)

        # [TODO]
        # - load buy model and sell model.
        # - calculate atr.
        # - predict dict of predict information
