import streamlit as st
import plotly.express as px
from data_loader import load_featured_data
from ui import inject_css, hero

st.set_page_config(page_title="Flight Delay Dashboard", layout="wide")

inject_css()
hero(
    "✈️ Flight Delay Dashboard",
    "Explore delay patterns by time, airline, airport, route, and cause."
)

df = load_featured_data()

# Safety checks
required_cols = ["delay_flag", "ARR_DELAY", "DEP_DELAY", "month", "day_of_week", "AIRLINE", "ORIGIN", "route"]
missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

# Top KPI cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Flights", f"{len(df):,}")
c2.metric("Delay Rate", f"{df['delay_flag'].mean() * 100:.2f}%")
c3.metric("Avg Arrival Delay", f"{df['ARR_DELAY'].mean():.2f} min")
c4.metric("Avg Departure Delay", f"{df['DEP_DELAY'].mean():.2f} min")

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Quick Insights")

ins1, ins2, ins3 = st.columns(3)

with ins1:
    st.markdown(
        """
        <div class="insight-box">
        <b>Peak Delay Months</b><br>
        Delays are highest in summer months, especially June and July.
        </div>
        """,
        unsafe_allow_html=True,
    )

with ins2:
    st.markdown(
        """
        <div class="insight-box">
        <b>Operational Causes</b><br>
        Late aircraft and carrier issues drive most delay minutes.
        </div>
        """,
        unsafe_allow_html=True,
    )

with ins3:
    st.markdown(
        """
        <div class="insight-box">
        <b>System Propagation</b><br>
        Departure delays strongly carry into arrival delays.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Time Trends", "Airlines", "Airports", "Routes"])

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Delay Rate by Month")
    monthly_delay = df.groupby("month")["delay_flag"].mean().reset_index()
    fig = px.bar(
        monthly_delay,
        x="month",
        y="delay_flag",
        color="delay_flag",
        color_continuous_scale="Turbo",
        labels={"month": "Month", "delay_flag": "Delay Rate"},
        title="Delay Rate by Month",
    )
    fig.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Delay Rate by Day of Week")
    dow_delay = df.groupby("day_of_week")["delay_flag"].mean().reset_index()
    fig = px.line(
        dow_delay,
        x="day_of_week",
        y="delay_flag",
        markers=True,
        labels={"day_of_week": "Day of Week (0=Mon)", "delay_flag": "Delay Rate"},
        title="Delay Rate by Day of Week",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
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
        labels={"ARR_DELAY": "Avg Arrival Delay", "AIRLINE": "Airline"},
    )
    fig.update_layout(height=550, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

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
    fig.update_layout(height=550, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
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
        labels={"ORIGIN": "Airport", "ARR_DELAY": "Avg Arrival Delay"},
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

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

with tab4:
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
        labels={"route": "Route", "ARR_DELAY": "Avg Arrival Delay"},
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

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