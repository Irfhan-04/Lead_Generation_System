import pandas as pd

def load_leads(path: str) -> pd.DataFrame:
    return pd.read_csv(path)
