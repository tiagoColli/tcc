def normalize(df, min, max):
    normalized_df = (df-df.min())/(df.max()-df.min())
    X_scaled = normalized_df * (max - min) + min
    return X_scaled
