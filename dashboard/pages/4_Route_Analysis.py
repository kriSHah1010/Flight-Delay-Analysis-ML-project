import streamlit as st
import plotly.express as px
from data_loader import load_featured_data
from ui import inject_css, hero

inject_css()
hero(
    "🧭 Route Analysis",
    "Explore which origin-destination pairs suffer the most delay and how route-specific disruption behaves."
)

df = load_featured_data()

required_cols = ["route", "ARR_DELAY", "delay_flag"]
missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

st.markdown("### Route performance snapshot")

c1, c2, c3 = st.columns(3)
c1.metric("Routes in dataset", df["route"].nunique())
c2.metric("Worst avg delay route", df.groupby("route")["ARR_DELAY"].mean().idxmax())
c3.metric("Highest delay probability", df.groupby("route")["delay_flag"].mean().idxmax())

st.markdown("""
<div class="insight-box">
<b>Route analysis is where you see network effects.</b><br>
Some routes inherit delay from congested hubs, tight schedules, or weak recovery options.
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Average Delay", "Delay Probability", "Route Volume"])

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Worst Routes by Average Arrival Delay")

    route_delay = (
        df.groupby("route")["ARR_DELAY"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        route_delay,
        x="route",
        y="ARR_DELAY",
        color="ARR_DELAY",
        color_continuous_scale="Turbo",
        labels={"route": "Route", "ARR_DELAY": "Average Arrival Delay (minutes)"},
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Worst Routes by Delay Probability")

    route_prob = (
        df.groupby("route")["delay_flag"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        route_prob,
        x="route",
        y="delay_flag",
        color="delay_flag",
        color_continuous_scale="Viridis",
        labels={"route": "Route", "delay_flag": "Delay Probability"},
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Route Volume vs Delay Risk")

    route_stats = (
        df.groupby("route")
        .agg(
            avg_arr_delay=("ARR_DELAY", "mean"),
            delay_prob=("delay_flag", "mean"),
            flights=("route", "size"),
        )
        .reset_index()
    )

    fig = px.scatter(
        route_stats,
        x="flights",
        y="delay_prob",
        size="avg_arr_delay",
        color="avg_arr_delay",
        hover_name="route",
        color_continuous_scale="Plasma",
        labels={
            "flights": "Number of Flights",
            "delay_prob": "Delay Probability",
            "avg_arr_delay": "Average Arrival Delay",
        },
        title="Route Volume vs Delay Risk",
    )
    fig.update_layout(height=550)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### Key Insight")
st.markdown("""
<div class="insight-box">
<b>Some routes are consistently fragile.</b><br>
High-delay routes often connect busy hubs to smaller destinations, where disruptions are harder to absorb.
</div>
""", unsafe_allow_html=True)