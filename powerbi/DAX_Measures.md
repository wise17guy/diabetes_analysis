# DAX Measures — Diabetes Risk Analytics Dashboard

Paste each measure into the **Modeling → New Measure** dialog in Power BI Desktop.
All measures reference the table named **`Diabetes Data`**.

---

## 1. Core KPI Measures

```dax
-- Total Patients
Total Patients = COUNTROWS('Diabetes Data')

-- High Risk Patients
High Risk Patients =
CALCULATE(
    COUNTROWS('Diabetes Data'),
    'Diabetes Data'[Risk Tier] = "High"
)

-- Medium Risk Patients
Medium Risk Patients =
CALCULATE(
    COUNTROWS('Diabetes Data'),
    'Diabetes Data'[Risk Tier] = "Medium"
)

-- Low Risk Patients
Low Risk Patients =
CALCULATE(
    COUNTROWS('Diabetes Data'),
    'Diabetes Data'[Risk Tier] = "Low"
)

-- % High Risk
% High Risk =
DIVIDE([High Risk Patients], [Total Patients], 0)

-- Average Risk Score
Avg Risk Score =
AVERAGEX('Diabetes Data', 'Diabetes Data'[Risk Score])

-- Max Risk Score
Max Risk Score = MAX('Diabetes Data'[Risk Score])
```

---

## 2. Clinical Averages

```dax
Avg Glucose =
AVERAGE('Diabetes Data'[Glucose])

Avg BMI =
AVERAGE('Diabetes Data'[BMI])

Avg Blood Pressure =
AVERAGE('Diabetes Data'[BloodPressure (mg/dL)])

Avg Insulin =
AVERAGE('Diabetes Data'[Insulin])

Avg Age =
AVERAGE('Diabetes Data'[Age])

Avg DPF =
AVERAGE('Diabetes Data'[DiabetesPedigreeFunction])

Avg Pregnancies =
AVERAGE('Diabetes Data'[Pregnancies])
```

---

## 3. Risk-Stratified Clinical Averages

```dax
Avg Glucose (High Risk) =
CALCULATE(
    AVERAGE('Diabetes Data'[Glucose]),
    'Diabetes Data'[Risk Tier] = "High"
)

Avg BMI (High Risk) =
CALCULATE(
    AVERAGE('Diabetes Data'[BMI]),
    'Diabetes Data'[Risk Tier] = "High"
)

Avg Glucose (Low Risk) =
CALCULATE(
    AVERAGE('Diabetes Data'[Glucose]),
    'Diabetes Data'[Risk Tier] = "Low"
)

Avg BMI (Low Risk) =
CALCULATE(
    AVERAGE('Diabetes Data'[BMI]),
    'Diabetes Data'[Risk Tier] = "Low"
)
```

---

## 4. Prevalence & Distribution Measures

```dax
-- % Obese patients
% Obese =
DIVIDE(
    CALCULATE(COUNTROWS('Diabetes Data'), 'Diabetes Data'[BMI Category] = "Obese"),
    [Total Patients],
    0
)

-- % Diabetic Range Glucose
% Diabetic Glucose Range =
DIVIDE(
    CALCULATE(COUNTROWS('Diabetes Data'), 'Diabetes Data'[Glucose Category] = "Diabetic Range"),
    [Total Patients],
    0
)

-- % Pre-diabetic Glucose
% Pre-diabetic Glucose =
DIVIDE(
    CALCULATE(COUNTROWS('Diabetes Data'), 'Diabetes Data'[Glucose Category] = "Pre-diabetic"),
    [Total Percent],
    0
)

-- % with Insulin Resistance
% Insulin Resistance =
DIVIDE(
    CALCULATE(COUNTROWS('Diabetes Data'), 'Diabetes Data'[Insulin Resistance] = "Yes"),
    [Total Patients],
    0
)

-- % High Blood Pressure
% High BP =
DIVIDE(
    CALCULATE(COUNTROWS('Diabetes Data'), 'Diabetes Data'[BP Category] = "High"),
    [Total Patients],
    0
)
```

---

## 5. Dynamic Title Measure (for visuals)

```dax
-- Shows current filter context in chart titles
Selected Risk Tier =
IF(
    ISFILTERED('Diabetes Data'[Risk Tier]),
    SELECTEDVALUE('Diabetes Data'[Risk Tier], "Multiple Tiers"),
    "All Tiers"
)

Dynamic Chart Title =
"Risk Analytics — " & [Selected Risk Tier]
```

---

## 6. Benchmarking Measures (ADA / WHO reference lines)

```dax
-- ADA Normal Glucose Upper Limit
Glucose Normal Limit = 99

-- ADA Pre-diabetic Upper Limit
Glucose Pre-diabetic Limit = 125

-- WHO Normal BMI Upper Limit
BMI Normal Limit = 24.9

-- Normal Diastolic BP Upper Limit
BP Normal Limit = 79
```

---

## 7. Scatter Plot Helpers

```dax
-- Bubble size for scatter: normalised risk score (1–10 scale)
Bubble Size =
AVERAGEX(
    'Diabetes Data',
    DIVIDE('Diabetes Data'[Risk Score], 10)
)
```

---

## 8. Calculated Columns (add via Modeling → New Column)

```dax
-- Combined risk label for tooltips
Risk Label =
'Diabetes Data'[Patient ID]
    & " | Score: " & FORMAT('Diabetes Data'[Risk Score], "0.0")
    & " | " & 'Diabetes Data'[Risk Tier]
```
