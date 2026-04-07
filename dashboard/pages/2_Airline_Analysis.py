import streamlit as st
import plotly.express as px
from data_loader import load_featured_data
from ui import inject_css, hero

inject_css()
hero(
    "✈️ Airline Analysis",
    "Compare airlines by average delay, delay probability, and performance consistency."
)

df = load_featured_data()

required_cols = ["AIRLINE", "ARR_DELAY", "delay_flag"]
missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

st.markdown("### Airline performance snapshot")

c1, c2, c3 = st.columns(3)
c1.metric("Airlines in dataset", df["AIRLINE"].nunique())
c2.metric("Worst avg delay airline", df.groupby("AIRLINE")["ARR_DELAY"].mean().idxmax())
c3.metric("Highest delay probability", df.groupby("AIRLINE")["delay_flag"].mean().idxmax())

st.markdown("""
<div class="insight-box">
<b>What to look for:</b><br>
Some airlines may have high average delay minutes, while others may have a high delay probability.
These two measures are related but not identical.
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Average Delay", "Delay Probability", "Consistency"])

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Average Arrival Delay by Airline")

    airline_delay = (
        df.groupby("AIRLINE")["ARR_DELAY"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        airline_delay,
        x="ARR_DELAY",
        y="AIRLINE",
        orientation="h",
        color="ARR_DELAY",
        color_continuous_scale="Plasma",
        labels={"ARR_DELAY": "Average Arrival Delay (minutes)", "AIRLINE": "Airline"},
    )
    fig.update_layout(height=600, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Delay Probability by Airline")

    airline_prob = (
        df.groupby("AIRLINE")["delay_flag"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        airline_prob,
        x="delay_flag",
        y="AIRLINE",
        orientation="h",
        color="delay_flag",
        color_continuous_scale="Viridis",
        labels={"delay_flag": "Delay Probability", "AIRLINE": "Airline"},
    )
    fig.update_layout(height=600, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Delay Variation by Airline")

    airline_stats = (
        df.groupby("AIRLINE")
        .agg(
            avg_arr_delay=("ARR_DELAY", "mean"),
            delay_prob=("delay_flag", "mean"),
            flights=("AIRLINE", "size"),
        )
        .reset_index()
    )

    fig = px.scatter(
        airline_stats,
        x="delay_prob",
        y="avg_arr_delay",
        size="flights",
        color="AIRLINE",
        hover_data=["flights"],
        labels={
            "delay_prob": "Delay Probability",
            "avg_arr_delay": "Average Arrival Delay",
        },
        title="Airline Delay Profile",
    )
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### Key Insight")
st.markdown("""
<div class="insight-box">
<b>Low-cost carriers often show higher delay risk.</b><br>
This may reflect tighter schedules, thinner buffers, and less recovery time when delays start to build.
</div>
""", unsafe_allow_html=True)