"""Data loading and preprocessing utilities for the Diabetes Analysis Dashboard."""

import os
import pandas as pd
import numpy as np


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "diabetes.csv")


def load_data(filepath: str = DATA_PATH) -> pd.DataFrame:
    """Load and preprocess the diabetes dataset.

    Args:
        filepath: Path to the CSV file.

    Returns:
        Preprocessed DataFrame.
    """
    df = pd.read_csv(filepath)

    # Replace biologically impossible zeros with NaN for specific columns
    zero_cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    df[zero_cols] = df[zero_cols].replace(0, np.nan)

    # Impute missing values with the column median
    for col in zero_cols:
        df[col] = df[col].fillna(df[col].median())

    # Derive risk category based on Glucose and BMI thresholds
    df["RiskCategory"] = df.apply(_classify_risk, axis=1)

    # Derive BMI category
    df["BMICategory"] = df["BMI"].apply(_classify_bmi)

    # Derive age group
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 30, 45, 60, 120],
        labels=["21-30", "31-45", "46-60", "60+"],
    )

    return df


def _classify_risk(row: pd.Series) -> str:
    """Classify a patient into High, Medium, or Low diabetes risk.

    High risk:   Outcome==1 OR Glucose >= 140 OR BMI >= 35
    Medium risk: Glucose in [100, 140) OR BMI in [25, 35)
    Low risk:    all other cases
    """
    if row["Outcome"] == 1 or row["Glucose"] >= 140 or row["BMI"] >= 35:
        return "High"
    if row["Glucose"] >= 100 or row["BMI"] >= 25:
        return "Medium"
    return "Low"


def _classify_bmi(bmi: float) -> str:
    """Return WHO BMI category label."""
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25.0:
        return "Normal"
    if bmi < 30.0:
        return "Overweight"
    return "Obese"


def get_filtered_data(
    df: pd.DataFrame,
    age_range: tuple,
    bmi_categories: list,
    risk_categories: list,
    outcome: str = "All",
) -> pd.DataFrame:
    """Return a filtered subset of the DataFrame.

    Args:
        df: Full DataFrame returned by :func:`load_data`.
        age_range: Tuple of (min_age, max_age).
        bmi_categories: List of BMI category labels to include.
        risk_categories: List of risk category labels to include.
        outcome: ``"All"``, ``"Diabetic"``, or ``"Non-Diabetic"``.

    Returns:
        Filtered DataFrame.
    """
    mask = (df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])

    if bmi_categories:
        mask &= df["BMICategory"].isin(bmi_categories)

    if risk_categories:
        mask &= df["RiskCategory"].isin(risk_categories)

    if outcome == "Diabetic":
        mask &= df["Outcome"] == 1
    elif outcome == "Non-Diabetic":
        mask &= df["Outcome"] == 0

    return df[mask]
