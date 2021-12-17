import pandas as pd
from utils.features import sma, ema, high, hilo


def agg_feature(df: pd.DataFrame) -> pd.DataFrame:
    feature_columns = []
    # hilo for visualization
    df["hilo"] = hilo(df)
    # input features
    df["sma10"] = sma(df, 10) / df["hilo"]
    df["sma45"] = sma(df, 45) / df["hilo"]
    feature_columns += [f"sma{i}" for i in [10, 45]]

    df["ewa45"] = ema(df, 45) / df["hilo"]
    feature_columns += [f"ewa{i}" for i in [45]]

    df["close_sma5_ratio"] = df["close"] / sma(df, 5)
    df["close_sma15_ratio"] = df["close"] / sma(df, 15)
    df["close_sma30_ratio"] = df["close"] / sma(df, 30)
    df["close_sma45_ratio"] = df["close"] / sma(df, 45)
    feature_columns += [f"close_sma{i}_ratio" for i in [5, 15, 30, 45]]

    df["sma45_sma15_ratio"] = sma(df, 45) / sma(df, 15)
    df["sma30_sma10_ratio"] = sma(df, 30) / sma(df, 10)
    df["sma5_sma45_ratio"] = sma(df, 5) / sma(df, 45)
    df["sma10_sma45_ratio"] = sma(df, 10) / sma(df, 45)
    feature_columns += [f"sma{i}_sma{j}_ratio" for i, j in zip([45, 30, 5, 10], [15, 10, 45, 45])]

    df["close_highest30_ratio"] = df["close"] / high(df, 30)
    df["close_highest45_ratio"] = df["close"] / high(df, 45)
    feature_columns += [f"close_highest{i}_ratio" for i in [30, 45]]

    df["close_10daysAgoHighest45_ratio"] = df["close"] / high(df, 45).shift(1 + 10)
    feature_columns += [f"close_{i}daysAgoHighest{j}_ratio" for i, j in zip([10], [45])]

    df["close_5daysAgoclose_ratio"] = df["close"] / df["close"].shift(5)
    df["close_10daysAgoclose_ratio"] = df["close"] / df["close"].shift(10)
    df["close_15daysAgoclose_ratio"] = df["close"] / df["close"].shift(15)
    df["close_20daysAgoclose_ratio"] = df["close"] / df["close"].shift(20)
    feature_columns += [f"close_{i}daysAgoclose_ratio" for i in [5, 10, 15, 20]]

    df = df.dropna()
    df = df[feature_columns]
    return df.loc[df.index[-1], :]
