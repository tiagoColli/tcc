import pandas as pd


def normalize(df: pd.DataFrame, min: int, max: int, weights: dict = None):
    normalized_df = (df-df.min())/(df.max()-df.min())
    X_scaled = normalized_df * (max - min) + min

    if weights:
        for column, weight in weights.items():
            df[column] = df[column] * weight

    return X_scaled
