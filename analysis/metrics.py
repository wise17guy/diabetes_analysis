"""Key metrics computation for the Diabetes Analysis Dashboard."""

import pandas as pd


def compute_key_metrics(df: pd.DataFrame) -> dict:
    """Return a dictionary of headline KPIs for the supplied DataFrame.

    Args:
        df: DataFrame (optionally pre-filtered) from :func:`data_loader.load_data`.

    Returns:
        Dictionary with the following keys:
            - total_patients (int)
            - diabetic_count (int)
            - non_diabetic_count (int)
            - diabetes_rate (float) – percentage
            - avg_bmi (float)
            - avg_glucose (float)
            - avg_blood_pressure (float)
            - avg_insulin (float)
            - avg_age (float)
            - high_risk_count (int)
            - medium_risk_count (int)
            - low_risk_count (int)
    """
    if df.empty:
        return {
            "total_patients": 0,
            "diabetic_count": 0,
            "non_diabetic_count": 0,
            "diabetes_rate": 0.0,
            "avg_bmi": 0.0,
            "avg_glucose": 0.0,
            "avg_blood_pressure": 0.0,
            "avg_insulin": 0.0,
            "avg_age": 0.0,
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0,
        }

    total = len(df)
    diabetic = int((df["Outcome"] == 1).sum())

    risk_counts = df["RiskCategory"].value_counts()

    return {
        "total_patients": total,
        "diabetic_count": diabetic,
        "non_diabetic_count": total - diabetic,
        "diabetes_rate": round(diabetic / total * 100, 1),
        "avg_bmi": round(df["BMI"].mean(), 1),
        "avg_glucose": round(df["Glucose"].mean(), 1),
        "avg_blood_pressure": round(df["BloodPressure"].mean(), 1),
        "avg_insulin": round(df["Insulin"].mean(), 1),
        "avg_age": round(df["Age"].mean(), 1),
        "high_risk_count": int(risk_counts.get("High", 0)),
        "medium_risk_count": int(risk_counts.get("Medium", 0)),
        "low_risk_count": int(risk_counts.get("Low", 0)),
    }


def compute_risk_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Return risk category counts and percentages.

    Args:
        df: Filtered DataFrame.

    Returns:
        DataFrame with columns [``RiskCategory``, ``Count``, ``Percentage``].
    """
    counts = df["RiskCategory"].value_counts().reset_index()
    counts.columns = ["RiskCategory", "Count"]
    counts["Percentage"] = (counts["Count"] / counts["Count"].sum() * 100).round(1)
    return counts


def compute_bmi_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Return BMI category counts.

    Args:
        df: Filtered DataFrame.

    Returns:
        DataFrame with columns [``BMICategory``, ``Count``, ``Percentage``].
    """
    order = ["Underweight", "Normal", "Overweight", "Obese"]
    counts = df["BMICategory"].value_counts().reindex(order, fill_value=0).reset_index()
    counts.columns = ["BMICategory", "Count"]
    counts["Percentage"] = (counts["Count"] / counts["Count"].sum() * 100).round(1)
    return counts


def compute_age_glucose_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return mean Glucose per AgeGroup for trend analysis.

    Args:
        df: Filtered DataFrame.

    Returns:
        DataFrame with columns [``AgeGroup``, ``AvgGlucose``].
    """
    return (
        df.groupby("AgeGroup", observed=True)["Glucose"]
        .mean()
        .round(1)
        .reset_index()
        .rename(columns={"Glucose": "AvgGlucose"})
    )


def compute_bp_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return mean BloodPressure per RiskCategory.

    Args:
        df: Filtered DataFrame.

    Returns:
        DataFrame with columns [``RiskCategory``, ``AvgBP``].
    """
    return (
        df.groupby("RiskCategory")["BloodPressure"]
        .mean()
        .round(1)
        .reset_index()
        .rename(columns={"BloodPressure": "AvgBP"})
    )
