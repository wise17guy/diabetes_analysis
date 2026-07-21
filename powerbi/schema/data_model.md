# Data Model Schema

## Overview

The Diabetes Analysis Power BI report uses **three tables** loaded via Power Query.  
The core analytical table is `DiabetesData`; the others support tooltips and future time-based slicing.

---

## Tables

### 1. DiabetesData  *(Fact / Main Table)*

Source: `diabetes new.xlsx` → sheet `diabetes new`  
Rows: 768 patients  
Loaded via: `powerbi/queries/DiabetesData.m`

| Column | Data Type | Source / Derivation | Notes |
|---|---|---|---|
| PatientID | Whole Number | Added index (1…768) | Surrogate key |
| Age | Whole Number | Source column | Range: 21–81 |
| AgeGroup | Text | Derived — see query | `Under 30 / 30–39 / 40–49 / 50–59 / 60+` |
| AgeGroupSort | Whole Number | Derived | Sort key for AgeGroup (1–5) |
| Pregnancies | Whole Number | Source column | Range: 0–17 |
| PregnancyGroup | Text | Derived | `None / 1–3 / 4–6 / 7+` |
| Glucose | Whole Number | Source; zeros → imputed with median | Range (after imputation): 44–199 |
| GlucoseCategory | Text | Derived — ADA thresholds | `Normal / Pre-Diabetic / Diabetic Range` |
| GlucoseCategorySort | Whole Number | Derived | Sort key for GlucoseCategory (1–3) |
| BloodPressure | Whole Number | Source `BloodPressure (mg/dL)`; zeros → imputed | Range: 24–122 |
| BloodPressureCategory | Text | Derived — JNC-8 | `Normal / Elevated / Stage 1 HTN / Stage 2 HTN` |
| SkinThickness | Whole Number | Source; zeros → imputed with median | mm |
| Insulin | Whole Number | Source; zeros → imputed with median | µIU/mL |
| InsulinCategory | Text | Derived | `Not Measured / Low / Normal / High` |
| BMI | Decimal Number | Source; zeros → imputed with median | kg/m² |
| BMICategory | Text | Derived — WHO | `Underweight / Normal Weight / Overweight / Obese I / II / III` |
| BMICategorySort | Whole Number | Derived | Sort key for BMICategory (1–6) |
| DiabetesPedigreeFunction | Decimal Number | Source; values >2.5 divided by 1000 | Range: 0.078–2.42 |
| RiskScore | Decimal Number | Derived composite (0–100) | See scoring logic below |
| RiskCategory | Text | Derived from RiskScore | `Low Risk / Medium Risk / High Risk` |
| RiskCategorySort | Whole Number | Derived | Sort key: 1=Low, 2=Med, 3=High |

**RiskScore Calculation**  
```
Points:
  Glucose ≥ 126         → +30
  Glucose 100–125       → +15
  BMI ≥ 35              → +20
  BMI 30–34.9           → +10
  Age ≥ 50              → +15
  Age 40–49             → +8
  Pregnancies ≥ 6       → +10
  BloodPressure ≥ 90    → +10
  DPF ≥ 0.5             → +10
  Insulin > 166         → +5
  ─────────────────────
  Max raw               = 110
  Normalised to 100     = (raw / 110) × 100

RiskCategory thresholds:
  High Risk   : RiskScore ≥ 60
  Medium Risk : RiskScore 30–59
  Low Risk    : RiskScore < 30
```

---

### 2. RiskScoreTable  *(Aggregate Summary)*

Loaded via: `powerbi/queries/RiskScoreTable.m`  
Rows: 3 (one per RiskCategory)  
Purpose: Pre-aggregated table for summary tooltips and the Executive Summary KPI grid.

| Column | Data Type | Description |
|---|---|---|
| RiskCategory | Text | `Low Risk / Medium Risk / High Risk` |
| RiskCategorySort | Whole Number | Sort key |
| PatientCount | Whole Number | Count per category |
| AvgAge | Decimal Number | |
| AvgGlucose | Decimal Number | |
| AvgBMI | Decimal Number | |
| AvgBloodPressure | Decimal Number | |
| AvgDPF | Decimal Number | |
| AvgRiskScore | Decimal Number | |
| PctShare | Decimal Number | % of total patients |

---

### 3. DateTable  *(Date Dimension)*

Loaded via: `powerbi/queries/DateTable.m`  
Rows: 11,323 (2000-01-01 → 2030-12-31)  
Purpose: Enables time-intelligence DAX functions; also used as a slicer if date data is added later.

| Column | Data Type | Description |
|---|---|---|
| Date | Date | Primary key |
| Year | Whole Number | |
| QuarterNum | Whole Number | 1–4 |
| Quarter | Text | `Q1`–`Q4` |
| YearQuarter | Text | e.g. `2024 Q3` |
| MonthNum | Whole Number | 1–12 |
| MonthName | Text | e.g. `January` |
| MonthShort | Text | e.g. `Jan` |
| YearMonth | Text | e.g. `2024-03` |
| WeekNum | Whole Number | ISO week number |
| DayOfWeekNum | Whole Number | 1=Mon … 7=Sun |
| DayOfWeekName | Text | |
| DayShort | Text | e.g. `Mon` |
| IsWeekend | True/False | |
| IsCurrentYear | True/False | |

---

## Relationships

```
DiabetesData ──── (no join) ──── DateTable
                 (standalone; no date FK in current dataset)

DiabetesData ──── (no join) ──── RiskScoreTable
                 (RiskScoreTable is pre-aggregated; used in
                  standalone visuals, not related to DiabetesData
                  to avoid double-counting)
```

> **Note:** Both `RiskScoreTable` and `DateTable` are **disconnected** tables.  
> They are used independently in specific visuals, not as dimensions in a star schema.  
> This is intentional — connecting `RiskScoreTable` to `DiabetesData` would create  
> circular aggregation issues since it was derived from `DiabetesData`.

---

## Calculated Columns

All heavy transformations are done in Power Query (M).  
The following **DAX calculated columns** should be added in Power BI Desktop  
after loading, for performance-critical scenarios:

### DiabetesData[Risk Score Band]
Groups `RiskScore` into 10-point histogram buckets.

```dax
Risk Score Band =
VAR Band = FLOOR( DiabetesData[RiskScore], 10 )
RETURN
    FORMAT( Band, "0" ) & "–" & FORMAT( Band + 9, "0" )
```

### DiabetesData[Risk Score Band Sort]
Sort key for `Risk Score Band`.

```dax
Risk Score Band Sort =
FLOOR( DiabetesData[RiskScore], 10 )
```

### DiabetesData[Glucose × BMI]
Product of Glucose and BMI — used as a compound risk indicator in scatter plots.

```dax
Glucose × BMI =
DiabetesData[Glucose] * DiabetesData[BMI]
```

---

## Sort-by-Column Assignments

Apply these in Power BI Desktop (Column Tools > Sort by Column):

| Column | Sort By Column |
|---|---|
| AgeGroup | AgeGroupSort |
| GlucoseCategory | GlucoseCategorySort |
| BMICategory | BMICategorySort |
| RiskCategory | RiskCategorySort |
| MonthName | MonthNum |
| MonthShort | MonthNum |
| DayOfWeekName | DayOfWeekNum |
| DayShort | DayOfWeekNum |
| Quarter | QuarterNum |

---

## Measures Table

All DAX measures in `powerbi/dax/measures.dax` should be placed in a  
dedicated **Measures Table** (blank calculated table):

```dax
-- In Power BI Desktop: Modeling > New Table
_Measures = ROW( "Info", "All DAX measures are stored here" )
```

Then move all measures into this table for clean organisation.
