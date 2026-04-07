import streamlit as st
import plotly.express as px
from data_loader import load_featured_data
from ui import inject_css, hero

inject_css()
hero(
    "🔥 Delay Causes",
    "Understand whether delays come from carrier operations, weather, NAS, security, or late aircraft."
)

df = load_featured_data()

delay_cols = [
    "DELAY_DUE_CARRIER",
    "DELAY_DUE_WEATHER",
    "DELAY_DUE_NAS",
    "DELAY_DUE_SECURITY",
    "DELAY_DUE_LATE_AIRCRAFT",
]

missing_cols = [c for c in ["ARR_DELAY"] + delay_cols if c not in df.columns]

if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

st.markdown("### Delay cause snapshot")

c1, c2, c3 = st.columns(3)
c1.metric("Largest cause", df[delay_cols].mean().idxmax())
c2.metric("Smallest cause", df[delay_cols].mean().idxmin())
c3.metric("Avg total delay", f"{df['ARR_DELAY'].mean():.2f} min")

st.markdown("""
<div class="insight-box">
<b>Most delay minutes usually come from internal operations rather than security.</b><br>
Carrier and late-aircraft effects are often stronger than weather in many samples.
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Average Cause Minutes", "Cause Share", "Cause by Month"])

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Average Delay Contribution by Cause")

    cause_means = df[delay_cols].mean().sort_values(ascending=False).reset_index()
    cause_means.columns = ["cause", "minutes"]

    fig = px.bar(
        cause_means,
        x="cause",
        y="minutes",
        color="minutes",
        color_continuous_scale="Cividis",
        labels={"cause": "Cause", "minutes": "Average Delay Minutes"},
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Cause Share of Total Delay Minutes")

    totals = df[delay_cols].sum().reset_index()
    totals.columns = ["cause", "minutes"]

    fig = px.pie(
        totals,
        names="cause",
        values="minutes",
        hole=0.45,
        title="Total Delay Minute Share",
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(height=550)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Delay Causes by Month")

    if "month" in df.columns:
        monthly_causes = (
            df.groupby("month")[delay_cols]
            .mean()
            .reset_index()
        )

        fig = px.line(
            monthly_causes,
            x="month",
            y=delay_cols,
            markers=True,
            labels={"value": "Average Minutes", "month": "Month"},
            title="Monthly Delay Cause Trends",
        )
        fig.update_layout(height=550)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("The month column is missing from the dataset.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### Key Insight")
st.markdown("""
<div class="insight-box">
<b>Operational causes dominate.</b><br>
If carrier and late-aircraft delay are highest, the issue is likely network scheduling and recovery, not just external disruptions.
</div>
""", unsafe_allow_html=True)