import pandas as pd
from pathlib import Path

def load_featured_data():
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "processed" / "flights_featured.csv"
    return pd.read_csv(data_path)