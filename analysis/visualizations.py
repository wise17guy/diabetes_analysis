"""Reusable Plotly chart builders for the Diabetes Analysis Dashboard."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Colour palette ────────────────────────────────────────────────────────────
RISK_COLORS = {"High": "#E74C3C", "Medium": "#F39C12", "Low": "#2ECC71"}
BMI_COLORS = {
    "Underweight": "#3498DB",
    "Normal": "#2ECC71",
    "Overweight": "#F39C12",
    "Obese": "#E74C3C",
}
OUTCOME_COLORS = {0: "#2ECC71", 1: "#E74C3C"}

CHART_TEMPLATE = "plotly_dark"


# ── Risk segmentation ─────────────────────────────────────────────────────────

def risk_pie_chart(risk_df: pd.DataFrame) -> go.Figure:
    """Pie chart of High / Medium / Low risk distribution.

    Args:
        risk_df: DataFrame with columns [``RiskCategory``, ``Count``].

    Returns:
        Plotly Figure.
    """
    fig = px.pie(
        risk_df,
        names="RiskCategory",
        values="Count",
        color="RiskCategory",
        color_discrete_map=RISK_COLORS,
        hole=0.4,
        title="Diabetes Risk Segmentation",
        template=CHART_TEMPLATE,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def risk_bar_chart(risk_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of risk category counts.

    Args:
        risk_df: DataFrame with columns [``RiskCategory``, ``Count``].

    Returns:
        Plotly Figure.
    """
    order = ["High", "Medium", "Low"]
    risk_df = risk_df.set_index("RiskCategory").reindex(order).reset_index()
    colors = [RISK_COLORS.get(r, "#95A5A6") for r in risk_df["RiskCategory"]]

    fig = go.Figure(
        go.Bar(
            x=risk_df["Count"],
            y=risk_df["RiskCategory"],
            orientation="h",
            marker_color=colors,
            text=risk_df["Count"],
            textposition="auto",
        )
    )
    fig.update_layout(
        title="Patient Count by Risk Category",
        xaxis_title="Number of Patients",
        yaxis_title="Risk Category",
        template=CHART_TEMPLATE,
    )
    return fig


# ── Trends & Distributions ────────────────────────────────────────────────────

def glucose_age_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of Glucose vs Age coloured by Outcome.

    Args:
        df: Filtered patient DataFrame.

    Returns:
        Plotly Figure.
    """
    df = df.copy()
    df["DiabetesStatus"] = df["Outcome"].map({1: "Diabetic", 0: "Non-Diabetic"})
    fig = px.scatter(
        df,
        x="Age",
        y="Glucose",
        color="DiabetesStatus",
        color_discrete_map={"Diabetic": "#E74C3C", "Non-Diabetic": "#2ECC71"},
        hover_data=["BMI", "BloodPressure", "Insulin"],
        trendline="ols",
        title="Glucose vs Age by Diabetes Status",
        template=CHART_TEMPLATE,
    )
    fig.update_layout(xaxis_title="Age (years)", yaxis_title="Glucose (mg/dL)")
    return fig


def bmi_distribution_chart(bmi_df: pd.DataFrame) -> go.Figure:
    """Bar chart of BMI category distribution.

    Args:
        bmi_df: DataFrame with columns [``BMICategory``, ``Count``, ``Percentage``].

    Returns:
        Plotly Figure.
    """
    colors = [BMI_COLORS.get(c, "#95A5A6") for c in bmi_df["BMICategory"]]
    fig = go.Figure(
        go.Bar(
            x=bmi_df["BMICategory"],
            y=bmi_df["Count"],
            marker_color=colors,
            text=[f"{p}%" for p in bmi_df["Percentage"]],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="BMI Category Distribution",
        xaxis_title="BMI Category",
        yaxis_title="Number of Patients",
        template=CHART_TEMPLATE,
    )
    return fig


def blood_pressure_chart(bp_df: pd.DataFrame) -> go.Figure:
    """Bar chart of average Blood Pressure per Risk Category.

    Args:
        bp_df: DataFrame with columns [``RiskCategory``, ``AvgBP``].

    Returns:
        Plotly Figure.
    """
    colors = [RISK_COLORS.get(r, "#95A5A6") for r in bp_df["RiskCategory"]]
    fig = go.Figure(
        go.Bar(
            x=bp_df["RiskCategory"],
            y=bp_df["AvgBP"],
            marker_color=colors,
            text=bp_df["AvgBP"],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="Average Blood Pressure by Risk Category",
        xaxis_title="Risk Category",
        yaxis_title="Avg Blood Pressure (mmHg)",
        template=CHART_TEMPLATE,
    )
    return fig


def age_glucose_trend(age_glucose_df: pd.DataFrame) -> go.Figure:
    """Line chart of average Glucose per Age Group.

    Args:
        age_glucose_df: DataFrame with columns [``AgeGroup``, ``AvgGlucose``].

    Returns:
        Plotly Figure.
    """
    fig = px.line(
        age_glucose_df,
        x="AgeGroup",
        y="AvgGlucose",
        markers=True,
        title="Average Glucose Level by Age Group",
        template=CHART_TEMPLATE,
    )
    fig.update_traces(line_color="#3498DB", marker_color="#E74C3C", marker_size=10)
    fig.update_layout(xaxis_title="Age Group", yaxis_title="Avg Glucose (mg/dL)")
    return fig


# ── Correlation Analysis ──────────────────────────────────────────────────────

def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """Annotated heatmap of feature correlations.

    Args:
        df: Patient DataFrame.

    Returns:
        Plotly Figure.
    """
    cols = ["Glucose", "BMI", "BloodPressure", "Insulin", "Age", "Pregnancies", "Outcome"]
    corr = df[cols].corr().round(2)

    fig = go.Figure(
        go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            colorscale="RdBu",
            zmid=0,
            text=corr.values,
            texttemplate="%{text}",
            textfont={"size": 11},
            colorbar={"title": "Correlation"},
        )
    )
    fig.update_layout(
        title="Feature Correlation Heatmap",
        template=CHART_TEMPLATE,
    )
    return fig


def glucose_bmi_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of Glucose vs BMI coloured by Risk Category.

    Args:
        df: Filtered patient DataFrame.

    Returns:
        Plotly Figure.
    """
    fig = px.scatter(
        df,
        x="BMI",
        y="Glucose",
        color="RiskCategory",
        color_discrete_map=RISK_COLORS,
        size="Insulin",
        hover_data=["Age", "BloodPressure", "Outcome"],
        title="Glucose vs BMI (bubble size = Insulin level)",
        template=CHART_TEMPLATE,
    )
    fig.update_layout(xaxis_title="BMI", yaxis_title="Glucose (mg/dL)")
    return fig


# ── Gauge & Summary Charts ────────────────────────────────────────────────────

def diabetes_rate_gauge(rate: float) -> go.Figure:
    """Gauge chart showing overall diabetes rate.

    Args:
        rate: Diabetes rate as a percentage (0-100).

    Returns:
        Plotly Figure.
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=rate,
            delta={"reference": 34.9, "valueformat": ".1f"},
            number={"suffix": "%"},
            title={"text": "Diabetes Rate (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#E74C3C"},
                "steps": [
                    {"range": [0, 25], "color": "#2ECC71"},
                    {"range": [25, 50], "color": "#F39C12"},
                    {"range": [50, 100], "color": "#E74C3C"},
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": rate,
                },
            },
        )
    )
    fig.update_layout(template=CHART_TEMPLATE, height=280)
    return fig


def avg_glucose_gauge(avg_glucose: float) -> go.Figure:
    """Gauge chart showing average glucose level.

    Args:
        avg_glucose: Mean glucose value.

    Returns:
        Plotly Figure.
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg_glucose,
            number={"suffix": " mg/dL"},
            title={"text": "Avg Glucose (mg/dL)"},
            gauge={
                "axis": {"range": [0, 200]},
                "bar": {"color": "#3498DB"},
                "steps": [
                    {"range": [0, 99], "color": "#2ECC71"},
                    {"range": [99, 125], "color": "#F39C12"},
                    {"range": [125, 200], "color": "#E74C3C"},
                ],
            },
        )
    )
    fig.update_layout(template=CHART_TEMPLATE, height=280)
    return fig


def avg_bmi_gauge(avg_bmi: float) -> go.Figure:
    """Gauge chart showing average BMI.

    Args:
        avg_bmi: Mean BMI value.

    Returns:
        Plotly Figure.
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg_bmi,
            number={"suffix": " kg/m²"},
            title={"text": "Avg BMI (kg/m²)"},
            gauge={
                "axis": {"range": [10, 60]},
                "bar": {"color": "#9B59B6"},
                "steps": [
                    {"range": [10, 18.5], "color": "#3498DB"},
                    {"range": [18.5, 25], "color": "#2ECC71"},
                    {"range": [25, 30], "color": "#F39C12"},
                    {"range": [30, 60], "color": "#E74C3C"},
                ],
            },
        )
    )
    fig.update_layout(template=CHART_TEMPLATE, height=280)
    return fig


# ── Predictive Insights ───────────────────────────────────────────────────────

def feature_importance_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart of feature importance from a simple logistic model.

    Uses standardised logistic regression coefficients as a proxy for
    feature importance, so no external ML library beyond scikit-learn is needed.

    Args:
        df: Full (unfiltered) patient DataFrame.

    Returns:
        Plotly Figure.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    features = ["Glucose", "BMI", "BloodPressure", "Insulin", "Age", "Pregnancies"]
    X = df[features].values
    y = df["Outcome"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_scaled, y)

    importance_df = pd.DataFrame(
        {"Feature": features, "Importance": abs(model.coef_[0])}
    ).sort_values("Importance", ascending=True)

    fig = go.Figure(
        go.Bar(
            x=importance_df["Importance"],
            y=importance_df["Feature"],
            orientation="h",
            marker_color="#3498DB",
            text=importance_df["Importance"].round(3),
            textposition="auto",
        )
    )
    fig.update_layout(
        title="Predictive Risk Factors (Logistic Regression Coefficients)",
        xaxis_title="Absolute Coefficient (importance)",
        yaxis_title="Feature",
        template=CHART_TEMPLATE,
    )
    return fig


def glucose_distribution_by_risk(df: pd.DataFrame) -> go.Figure:
    """Box plot of Glucose distribution per Risk Category.

    Args:
        df: Filtered patient DataFrame.

    Returns:
        Plotly Figure.
    """
    fig = px.box(
        df,
        x="RiskCategory",
        y="Glucose",
        color="RiskCategory",
        color_discrete_map=RISK_COLORS,
        category_orders={"RiskCategory": ["High", "Medium", "Low"]},
        title="Glucose Distribution by Risk Category",
        template=CHART_TEMPLATE,
    )
    fig.update_layout(xaxis_title="Risk Category", yaxis_title="Glucose (mg/dL)")
    return fig
