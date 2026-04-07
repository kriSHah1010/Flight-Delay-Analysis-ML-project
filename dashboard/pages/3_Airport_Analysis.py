import streamlit as st
import plotly.express as px
from data_loader import load_featured_data
from ui import inject_css, hero

inject_css()
hero(
    "🛫 Airport Analysis",
    "Find airports with the highest delay burden and see how delay risk differs across locations."
)

df = load_featured_data()

required_cols = ["ORIGIN", "ARR_DELAY", "delay_flag"]
missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

st.markdown("### Airport performance snapshot")

c1, c2, c3 = st.columns(3)
c1.metric("Airports in dataset", df["ORIGIN"].nunique())
c2.metric("Worst avg delay airport", df.groupby("ORIGIN")["ARR_DELAY"].mean().idxmax())
c3.metric("Highest delay probability", df.groupby("ORIGIN")["delay_flag"].mean().idxmax())

st.markdown("""
<div class="insight-box">
<b>Airport-level patterns often reflect congestion, turnaround pressure, and operational constraints.</b><br>
Sometimes smaller airports can also show high delays if they have fewer recovery options.
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Average Delay", "Delay Probability", "Volume vs Delay"])

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Top 10 Airports by Average Arrival Delay")

    top_airports = (
        df.groupby("ORIGIN")["ARR_DELAY"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_airports,
        x="ORIGIN",
        y="ARR_DELAY",
        color="ARR_DELAY",
        color_continuous_scale="Inferno",
        labels={"ORIGIN": "Airport", "ARR_DELAY": "Average Arrival Delay (minutes)"},
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Top 10 Airports by Delay Probability")

    airport_prob = (
        df.groupby("ORIGIN")["delay_flag"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        airport_prob,
        x="ORIGIN",
        y="delay_flag",
        color="delay_flag",
        color_continuous_scale="Magma",
        labels={"ORIGIN": "Airport", "delay_flag": "Delay Probability"},
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Traffic vs Delay")

    airport_volume = (
        df.groupby("ORIGIN")
        .agg(
            avg_arr_delay=("ARR_DELAY", "mean"),
            delay_prob=("delay_flag", "mean"),
            flights=("ORIGIN", "size"),
        )
        .reset_index()
    )

    airport_volume["avg_arr_delay_abs"] = airport_volume["avg_arr_delay"].abs()
    fig = px.scatter(
        airport_volume,
        x="flights",
        y="delay_prob",
        size="avg_arr_delay_abs",
        color="avg_arr_delay",
        hover_name="ORIGIN",
        color_continuous_scale="Turbo",
        labels={
            "flights": "Number of Flights",
            "delay_prob": "Delay Probability",
            "avg_arr_delay": "Average Arrival Delay",
        },
        title="Airport Volume vs Delay Risk",
    )
    fig.update_layout(height=550)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### Key Insight")
st.markdown("""
<div class="insight-box">
<b>Delay risk is not always highest at the busiest airports.</b><br>
Some airports show high average delay even with lower traffic, which suggests local operational bottlenecks or limited recovery capacity.
</div>
""", unsafe_allow_html=True)