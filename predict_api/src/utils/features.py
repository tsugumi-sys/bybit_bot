import pandas as pd


def hilo(df: pd.DataFrame):
    return (df["high"] + df["low"]) / 2


def sma(df: pd.DataFrame, period: int = 10) -> pd.Series:
    return df["close"].rolling(period, min_periods=1).mean()


def ema(df: pd.DataFrame, period: int = 10) -> pd.Series:
    return df["close"].ewm(span=period, min_periods=1).mean()


def ema_ratio(df: pd.DataFrame, period: int = 10, shift: int = 1) -> pd.Series:
    return ema(df, period) / ema(df, period).shift(shift)


def high(df: pd.DataFrame, period: int) -> pd.Series:
    return df["close"].rolling(period).max()


def close_ratio(df: pd.DataFrame, period: int = 10) -> pd.Series:
    return df["close"] / df["close"].shift(period)


def std(df: pd.DataFrame, period: int = 10) -> pd.Series:
    return df["close"].rolling(period).std()
