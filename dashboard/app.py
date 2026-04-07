import streamlit as st
from data_loader import load_featured_data
from ui import inject_css, hero

st.set_page_config(page_title="Flight Delay Dashboard", layout="wide")

inject_css()
hero(
    "✈️ Flight Delay Analysis Dashboard",
    "A multi-page view of airline performance, airport congestion, routes, and delay causes."
)

st.title("✈️ Flight Delay Analysis Dashboard")
st.write("Use the pages on the left to explore the analysis.")

df = load_featured_data()

st.subheader("Quick Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Flights", f"{len(df):,}")
c2.metric("Delay Rate", f"{df['delay_flag'].mean() * 100:.2f}%")
c3.metric("Avg Arrival Delay", f"{df['ARR_DELAY'].mean():.2f} min")
c4.metric("Avg Departure Delay", f"{df['DEP_DELAY'].mean():.2f} min")

st.markdown("""
### Pages
- Overview
- Airline Analysis
- Airport Analysis
- Route Analysis
- Delay Causes
- ML Predictor
""")