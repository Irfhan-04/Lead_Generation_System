def normalize_titles(df):
    df["title"] = df["title"].str.lower()
    return df
