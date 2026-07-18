# DAX Measures Reference — Diabetes Analysis Dashboard

This file documents the DAX measures used (or recommended) when recreating this
dashboard in **Power BI**. All measures assume the data is loaded into a table
named `DiabetesData`.

---

## 1. Key Metrics

### Total Patients
```dax
Total Patients = COUNTROWS(DiabetesData)
```

### Diabetic Patients
```dax
Diabetic Patients = CALCULATE(COUNTROWS(DiabetesData), DiabetesData[Outcome] = 1)
```

### Non-Diabetic Patients
```dax
Non-Diabetic Patients = CALCULATE(COUNTROWS(DiabetesData), DiabetesData[Outcome] = 0)
```

### Diabetes Rate (%)
```dax
Diabetes Rate % =
DIVIDE([Diabetic Patients], [Total Patients], 0) * 100
```

### Average BMI
```dax
Avg BMI = AVERAGE(DiabetesData[BMI])
```

### Average Glucose
```dax
Avg Glucose = AVERAGE(DiabetesData[Glucose])
```

### Average Blood Pressure
```dax
Avg Blood Pressure = AVERAGE(DiabetesData[BloodPressure])
```

### Average Insulin
```dax
Avg Insulin = AVERAGE(DiabetesData[Insulin])
```

### Average Age
```dax
Avg Age = AVERAGE(DiabetesData[Age])
```

---

## 2. Risk Segmentation

### Risk Category Column (Calculated Column)
```dax
RiskCategory =
IF(
    DiabetesData[Outcome] = 1 || DiabetesData[Glucose] >= 140 || DiabetesData[BMI] >= 35,
    "High",
    IF(
        DiabetesData[Glucose] >= 100 || DiabetesData[BMI] >= 25,
        "Medium",
        "Low"
    )
)
```

### High Risk Patients
```dax
High Risk Patients =
CALCULATE([Total Patients], DiabetesData[RiskCategory] = "High")
```

### Medium Risk Patients
```dax
Medium Risk Patients =
CALCULATE([Total Patients], DiabetesData[RiskCategory] = "Medium")
```

### Low Risk Patients
```dax
Low Risk Patients =
CALCULATE([Total Patients], DiabetesData[RiskCategory] = "Low")
```

### High Risk % (for Gauge)
```dax
High Risk % =
DIVIDE([High Risk Patients], [Total Patients], 0) * 100
```

---

## 3. BMI Distribution

### BMI Category Column (Calculated Column)
```dax
BMICategory =
SWITCH(
    TRUE(),
    DiabetesData[BMI] < 18.5,  "Underweight",
    DiabetesData[BMI] < 25,    "Normal",
    DiabetesData[BMI] < 30,    "Overweight",
    "Obese"
)
```

### Obese Patient Count
```dax
Obese Patients =
CALCULATE([Total Patients], DiabetesData[BMICategory] = "Obese")
```

---

## 4. Age Group Analysis

### Age Group Column (Calculated Column)
```dax
AgeGroup =
SWITCH(
    TRUE(),
    DiabetesData[Age] <= 30, "21-30",
    DiabetesData[Age] <= 45, "31-45",
    DiabetesData[Age] <= 60, "46-60",
    "60+"
)
```

### Avg Glucose by Age Group (used in trend charts)
```dax
Avg Glucose by Age Group =
CALCULATE(
    AVERAGE(DiabetesData[Glucose]),
    ALLEXCEPT(DiabetesData, DiabetesData[AgeGroup])
)
```

---

## 5. Correlation Insights

### Glucose-BMI Correlation (Pearson approximation)
Power BI does not have a native `CORR` function; use a Python visual or the
following approximation measure:

```dax
Glucose BMI Correlation =
VAR n      = [Total Patients]
VAR sumX   = SUMX(DiabetesData, DiabetesData[Glucose])
VAR sumY   = SUMX(DiabetesData, DiabetesData[BMI])
VAR sumXY  = SUMX(DiabetesData, DiabetesData[Glucose] * DiabetesData[BMI])
VAR sumX2  = SUMX(DiabetesData, DiabetesData[Glucose] ^ 2)
VAR sumY2  = SUMX(DiabetesData, DiabetesData[BMI] ^ 2)
RETURN
DIVIDE(
    n * sumXY - sumX * sumY,
    SQRT((n * sumX2 - sumX ^ 2) * (n * sumY2 - sumY ^ 2)),
    0
)
```

---

## 6. Predictive Risk Score

A simple additive risk score (0–100) to highlight high-risk patients:

```dax
Risk Score =
VAR glucoseFactor = MIN(DiabetesData[Glucose] / 200 * 40, 40)
VAR bmiFactor     = MIN((DiabetesData[BMI] - 18.5) / 40 * 30, 30)
VAR ageFactor     = MIN(DiabetesData[Age] / 80 * 20, 20)
VAR bpFactor      = MIN(DiabetesData[BloodPressure] / 120 * 10, 10)
RETURN
ROUND(glucoseFactor + bmiFactor + ageFactor + bpFactor, 0)
```

> **Tip:** Use this `Risk Score` as the value for a **Gauge visual** in Power BI to
> visualise individual patient risk.

---

## 7. Time Intelligence (if a date column is available)

```dax
YTD Diabetic Patients =
CALCULATE([Diabetic Patients], DATESYTD(DiabetesData[RecordDate]))

MoM Change % =
VAR currentMonth  = [Diabetic Patients]
VAR previousMonth = CALCULATE([Diabetic Patients], DATEADD(DiabetesData[RecordDate], -1, MONTH))
RETURN
DIVIDE(currentMonth - previousMonth, previousMonth, 0) * 100
```

---

*Generated as a Power BI companion reference for the Python Streamlit dashboard.*
