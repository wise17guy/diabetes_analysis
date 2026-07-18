# 🩺 Diabetes Risk Analysis Dashboard

An interactive, data-driven dashboard that provides meaningful insights into diabetes risk factors using Python, Streamlit, Plotly, and DAX (Power BI).

---

## 📋 Overview

This project delivers a practice dashboard covering:

| Feature | Description |
|---|---|
| **Key Metrics** | Total patients, Avg BMI, Glucose, Blood Pressure, Insulin |
| **Risk Segmentation** | High / Medium / Low risk categories with pie & bar charts |
| **Trends & Distribution** | Glucose vs Age scatter, BMI categories, Blood Pressure analysis |
| **Correlation Analysis** | Feature correlation heatmap and Glucose vs BMI bubble chart |
| **Gauge Charts** | Diabetes rate %, Average Glucose, Average BMI gauges |
| **Interactive Filters** | Age range, BMI category, Risk category, Diabetes status filters |
| **Predictive Insights** | Logistic regression feature importance and box-plot risk analysis |
| **Patient Drilldown** | Filterable data table for individual patient exploration |
| **DAX Reference** | Power BI DAX measures for reproducing the dashboard in Power BI |

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch the Streamlit dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

---

## 📁 Project Structure

```
diabetes_analysis/
├── app.py                          # Main Streamlit dashboard application
├── requirements.txt                # Python dependencies
├── data/
│   └── diabetes.csv                # Synthetic Pima Indians Diabetes Dataset (768 rows)
├── analysis/
│   ├── __init__.py
│   ├── data_loader.py              # Data loading, cleaning, and feature engineering
│   ├── metrics.py                  # KPI and statistical metric computation
│   └── visualizations.py          # Reusable Plotly chart builders
├── dax/
│   └── measures.md                 # Power BI DAX measures reference
└── notebooks/
    └── diabetes_analysis.ipynb     # Jupyter notebook for exploratory analysis
```

---

## 📊 Dataset

The project uses a synthetic dataset modelled on the **Pima Indians Diabetes Dataset**
with 768 patient records and the following features:

| Column | Description | Unit |
|---|---|---|
| `Pregnancies` | Number of pregnancies | count |
| `Glucose` | Plasma glucose concentration | mg/dL |
| `BloodPressure` | Diastolic blood pressure | mmHg |
| `SkinThickness` | Triceps skin fold thickness | mm |
| `Insulin` | 2-hour serum insulin | μU/mL |
| `BMI` | Body mass index | kg/m² |
| `DiabetesPedigreeFunction` | Diabetes pedigree score | — |
| `Age` | Patient age | years |
| `Outcome` | Diabetes diagnosis (1 = positive) | binary |

---

## 🔴 Risk Classification Logic

| Risk Level | Criteria |
|---|---|
| **High** | Outcome = 1 OR Glucose ≥ 140 OR BMI ≥ 35 |
| **Medium** | Glucose ∈ [100, 140) OR BMI ∈ [25, 35) |
| **Low** | All other cases |

---

## 🏋️ BMI Categories (WHO)

| Category | BMI Range |
|---|---|
| Underweight | < 18.5 |
| Normal | 18.5 – 24.9 |
| Overweight | 25.0 – 29.9 |
| Obese | ≥ 30.0 |

---

## 📐 Power BI / DAX

DAX measures for reproducing this dashboard in **Power BI** are documented in
[`dax/measures.md`](dax/measures.md). Measures cover:

- Key KPIs (Total Patients, Diabetes Rate, Avg Glucose, Avg BMI …)
- Risk & BMI category calculated columns
- Correlation approximation formula
- Predictive risk score
- Time intelligence (YTD, Month-over-Month)

---

## 🔬 Exploratory Analysis

Open the Jupyter notebook for a guided walkthrough:

```bash
jupyter notebook notebooks/diabetes_analysis.ipynb
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Core language |
| **Streamlit** | Interactive web dashboard |
| **Plotly** | Interactive charts and gauges |
| **Pandas / NumPy** | Data manipulation |
| **scikit-learn** | Logistic regression for feature importance |
| **Power BI / DAX** | Enterprise BI companion reference |
