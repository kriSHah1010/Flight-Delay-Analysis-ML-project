import pandas as pd
from pathlib import Path
import streamlit as st

@st.cache_data
def load_featured_data():
    # Project root = one level above the dashboard folder
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "processed" / "flights_featured.csv"

    df = pd.read_csv(data_path)
    df["FL_DATE"] = pd.to_datetime(df["FL_DATE"], errors="coerce")
    return df