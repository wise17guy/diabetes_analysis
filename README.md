# Diabetes Risk Analytics — Power BI Dashboard

Interactive Power BI dashboard for diabetes risk analytics, built on the Pima Indians Diabetes dataset (768 patients, 8 clinical features).

---

## Repository Structure

```
diabetes_analysis/
├── diabetes new.xlsx                  # Raw dataset (original)
├── diabetes_powerbi_ready.xlsx        # Cleaned & enriched dataset (import this into Power BI)
└── powerbi/
    ├── Dashboard_Design_Spec.md       # Full 4-page dashboard layout & visual specifications
    ├── DAX_Measures.md                # All DAX measures and calculated columns
    └── diabetes_theme.json            # Custom Power BI color theme
```

---

## Dataset

| Feature | Description |
|---------|-------------|
| Age | Patient age (21–81) |
| Pregnancies | Number of pregnancies (0–17) |
| Glucose | Plasma glucose concentration (mg/dL) |
| BloodPressure (mmHg) | Diastolic blood pressure (column named 'mg/dL' in source but values are mmHg) |
| SkinThickness | Triceps skin fold thickness (mm) |
| Insulin | 2-Hour serum insulin (µIU/mL) |
| BMI | Body mass index |
| DiabetesPedigreeFunction | Genetic diabetes likelihood score |

`diabetes_powerbi_ready.xlsx` adds the following derived columns:

| Column | Description |
|--------|-------------|
| Patient ID | Unique identifier (P0001–P0768) |
| Age Group | 21–30 / 31–40 / 41–50 / 51–60 / 61+ |
| BMI Category | Underweight / Normal / Overweight / Obese (WHO) |
| Glucose Category | Normal / Pre-diabetic / Diabetic Range (ADA) |
| BP Category | Normal / Elevated / High |
| Pregnancy Group | None / Low / Moderate / High |
| Risk Score | Composite 0–100 weighted risk score |
| Risk Tier | Low / Medium / High (percentile-based) |
| Insulin Resistance | Yes / No (fasting insulin > 166 µIU/mL) |

---

## Quick Start

### 1. Open Power BI Desktop
Download free from [powerbi.microsoft.com](https://powerbi.microsoft.com/desktop/).

### 2. Import data
**Home → Get Data → Excel Workbook** → select `diabetes_powerbi_ready.xlsx` → load the `Diabetes Data` sheet.

### 3. Apply the theme
**View → Themes → Browse for themes** → select `powerbi/diabetes_theme.json`.

### 4. Add DAX measures
Open `powerbi/DAX_Measures.md` and paste each measure via **Modeling → New Measure**.

### 5. Build pages
Follow the 4-page layout in `powerbi/Dashboard_Design_Spec.md`:

| Page | Focus |
|------|-------|
| 1 — Executive Summary | KPI cards, risk donut, age-group bar, treemap |
| 2 — Risk Factor Deep-Dive | Scatter (Glucose vs BMI), distribution charts |
| 3 — Population Health | Heatmap matrix, stacked bars, prevalence KPIs |
| 4 — Patient Explorer | Sortable table, top-20 bar, individual radar chart |

### 6. Enable cross-filtering & drill-through
- Sync the **Risk Tier** and **Age Group** slicers across all pages
- Add a drill-through from any Risk Tier visual to **Page 4**
- Add bookmark-based navigation buttons for page switching

---

## Dashboard Pages at a Glance

```
Page 1 — Executive Summary
  [KPI Cards: Total | High Risk | Avg Score | % High Risk]
  [Donut: Risk Tier] [Bar: Avg Risk by Age Group] [Treemap: BMI × Glucose]

Page 2 — Risk Factor Deep-Dive
  [Scatter: Glucose vs BMI (colored by Risk Tier)]
  [Box plot: Glucose by Risk Tier] [100% Stacked: Glucose Cat by Age]

Page 3 — Population Health
  [Heatmap Matrix: Age Group × BMI Category → Avg Risk]
  [Stacked Bar: BMI Cat by Risk Tier] [KPI row: %Obese | %IR | %High BP]

Page 4 — Patient Explorer
  [Sortable Table with conditional formatting]
  [Scatter: Age vs Risk Score] [Top-20 Bar] [Radar: patient vs average]
```
