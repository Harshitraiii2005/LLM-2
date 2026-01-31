import pandas as pd

def fetch_data(data_path: str) -> pd.DataFrame:
    print("📥 Fetching data...")
    df = pd.read_csv(data_path)

    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    return df
