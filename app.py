"""Diabetes Risk Analysis – Interactive Streamlit Dashboard.

Run with:
    streamlit run app.py
"""

import streamlit as st

from analysis.data_loader import load_data, get_filtered_data
from analysis.metrics import (
    compute_key_metrics,
    compute_risk_distribution,
    compute_bmi_distribution,
    compute_age_glucose_stats,
    compute_bp_stats,
)
from analysis.visualizations import (
    risk_pie_chart,
    risk_bar_chart,
    glucose_age_scatter,
    bmi_distribution_chart,
    blood_pressure_chart,
    age_glucose_trend,
    correlation_heatmap,
    glucose_bmi_scatter,
    diabetes_rate_gauge,
    avg_glucose_gauge,
    avg_bmi_gauge,
    feature_importance_chart,
    glucose_distribution_by_risk,
)

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diabetes Risk Analysis Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load data (cached) ────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()


df_full = get_data()

# ── Sidebar – interactive filters ─────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/heart-with-pulse.png",
        width=60,
    )
    st.title("🩺 Dashboard Filters")
    st.markdown("---")

    age_range = st.slider(
        "Age Range",
        min_value=int(df_full["Age"].min()),
        max_value=int(df_full["Age"].max()),
        value=(int(df_full["Age"].min()), int(df_full["Age"].max())),
    )

    bmi_options = ["Underweight", "Normal", "Overweight", "Obese"]
    bmi_sel = st.multiselect("BMI Category", bmi_options, default=bmi_options)

    risk_options = ["High", "Medium", "Low"]
    risk_sel = st.multiselect("Risk Category", risk_options, default=risk_options)

    outcome_filter = st.radio(
        "Diabetes Status",
        ["All", "Diabetic", "Non-Diabetic"],
        horizontal=True,
    )

    st.markdown("---")
    st.caption("Data source: Synthetic Pima Indians Diabetes Dataset (768 patients)")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = get_filtered_data(df_full, age_range, bmi_sel, risk_sel, outcome_filter)

# ── Dashboard header ──────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;color:#E74C3C;'>🩺 Diabetes Risk Analysis Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:#BDC3C7;'>"
    "Interactive analytics for diabetes risk factors | Glucose · BMI · Blood Pressure · Insulin"
    "</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ── Section 1 – Key Metrics ───────────────────────────────────────────────────
st.subheader("📊 Key Metrics")

metrics = compute_key_metrics(df)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("👥 Total Patients", f"{metrics['total_patients']:,}")
col2.metric("⚠️ Diabetic", f"{metrics['diabetic_count']:,}", f"{metrics['diabetes_rate']}%")
col3.metric("⚖️ Avg BMI", f"{metrics['avg_bmi']}")
col4.metric("🩸 Avg Glucose", f"{metrics['avg_glucose']} mg/dL")
col5.metric("💉 Avg Insulin", f"{metrics['avg_insulin']} μU/mL")

col6, col7, col8, col9, col10 = st.columns(5)
col6.metric("🫀 Avg Blood Pressure", f"{metrics['avg_blood_pressure']} mmHg")
col7.metric("🕐 Avg Age", f"{metrics['avg_age']} yrs")
col8.metric("🔴 High Risk", f"{metrics['high_risk_count']:,}")
col9.metric("🟡 Medium Risk", f"{metrics['medium_risk_count']:,}")
col10.metric("🟢 Low Risk", f"{metrics['low_risk_count']:,}")

st.markdown("---")

# ── Section 2 – Gauge Charts ─────────────────────────────────────────────────
st.subheader("🎯 Health Gauge Summary")

g1, g2, g3 = st.columns(3)
with g1:
    st.plotly_chart(
        diabetes_rate_gauge(metrics["diabetes_rate"]),
        use_container_width=True,
    )
with g2:
    st.plotly_chart(
        avg_glucose_gauge(metrics["avg_glucose"]),
        use_container_width=True,
    )
with g3:
    st.plotly_chart(
        avg_bmi_gauge(metrics["avg_bmi"]),
        use_container_width=True,
    )

st.markdown("---")

# ── Section 3 – Risk Segmentation ────────────────────────────────────────────
st.subheader("🔴 Diabetes Risk Segmentation")

risk_df = compute_risk_distribution(df)

r1, r2 = st.columns(2)
with r1:
    st.plotly_chart(risk_pie_chart(risk_df), use_container_width=True)
with r2:
    st.plotly_chart(risk_bar_chart(risk_df), use_container_width=True)

st.markdown("---")

# ── Section 4 – Trends & Distribution ────────────────────────────────────────
st.subheader("📈 Trends & Distribution")

t1, t2 = st.columns(2)
with t1:
    st.plotly_chart(glucose_age_scatter(df), use_container_width=True)
with t2:
    age_glucose_df = compute_age_glucose_stats(df)
    st.plotly_chart(age_glucose_trend(age_glucose_df), use_container_width=True)

bmi_df = compute_bmi_distribution(df)
bp_df = compute_bp_stats(df)

t3, t4 = st.columns(2)
with t3:
    st.plotly_chart(bmi_distribution_chart(bmi_df), use_container_width=True)
with t4:
    st.plotly_chart(blood_pressure_chart(bp_df), use_container_width=True)

st.markdown("---")

# ── Section 5 – Correlation Analysis ─────────────────────────────────────────
st.subheader("🔗 Correlation Analysis")

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(correlation_heatmap(df), use_container_width=True)
with c2:
    st.plotly_chart(glucose_bmi_scatter(df), use_container_width=True)

st.markdown("---")

# ── Section 6 – Predictive Insights ──────────────────────────────────────────
st.subheader("🔮 Predictive Risk Insights")

p1, p2 = st.columns(2)
with p1:
    st.plotly_chart(feature_importance_chart(df_full), use_container_width=True)
with p2:
    st.plotly_chart(glucose_distribution_by_risk(df), use_container_width=True)

st.markdown("---")

# ── Section 7 – Drilldown Data Table ─────────────────────────────────────────
st.subheader("🔍 Patient Data Drilldown")

with st.expander("📋 View filtered patient records", expanded=False):
    display_cols = [
        "Age",
        "Glucose",
        "BMI",
        "BloodPressure",
        "Insulin",
        "Pregnancies",
        "DiabetesPedigreeFunction",
        "RiskCategory",
        "BMICategory",
        "AgeGroup",
        "Outcome",
    ]
    st.dataframe(
        df[display_cols]
        .rename(columns={"DiabetesPedigreeFunction": "DPF"})
        .reset_index(drop=True),
        use_container_width=True,
        height=400,
    )
    st.caption(f"Showing {len(df):,} of {len(df_full):,} patients based on current filters.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#95A5A6;font-size:12px;'>"
    "Diabetes Risk Analysis Dashboard · Built with Python, Streamlit & Plotly · "
    "DAX measures available in <code>dax/measures.md</code>"
    "</p>",
    unsafe_allow_html=True,
)
