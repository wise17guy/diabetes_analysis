# Diabetes Analysis — Power BI Dashboard

A fully-specified **Microsoft Power BI** project that transforms the Pima Indians
Diabetes dataset into a four-page interactive report, complete with Power Query M
transformations, DAX measures, drill-through, bookmarks, slicers, and custom
tooltips.

> **No `.pbix` binary is stored in this repository.**  
> Power BI Desktop's `.pbix` format is a proprietary binary that cannot be
> generated programmatically. This repository contains all the source code and
> specifications needed to **assemble the `.pbix` in ~30–45 minutes** using the
> free Power BI Desktop application. Follow the step-by-step guide below.

---

## Table of Contents

1. [Repository Structure](#repository-structure)  
2. [Dataset](#dataset)  
3. [Prerequisites](#prerequisites)  
4. [Quick-Start — Build the .pbix](#quick-start--build-the-pbix)  
5. [Step 1 — Create a New Report](#step-1--create-a-new-report)  
6. [Step 2 — Load the Data (Power Query M)](#step-2--load-the-data-power-query-m)  
7. [Step 3 — Configure the Data Model](#step-3--configure-the-data-model)  
8. [Step 4 — Create DAX Measures](#step-4--create-dax-measures)  
9. [Step 5 — Build the Four Report Pages](#step-5--build-the-four-report-pages)  
10. [Step 6 — Add Slicers and Slicer Sync](#step-6--add-slicers-and-slicer-sync)  
11. [Step 7 — Configure Drill-Through](#step-7--configure-drill-through)  
12. [Step 8 — Add Bookmarks](#step-8--add-bookmarks)  
13. [Step 9 — Set Up Custom Tooltips](#step-9--set-up-custom-tooltips)  
14. [Step 10 — Apply Conditional Formatting](#step-10--apply-conditional-formatting)  
15. [Step 11 — Final Polish and Save](#step-11--final-polish-and-save)  
16. [Report Pages Overview](#report-pages-overview)  
17. [DAX Measures Reference](#dax-measures-reference)  
18. [Power Query Transformations](#power-query-transformations)  
19. [Troubleshooting](#troubleshooting)  

---

## Repository Structure

```
diabetes_analysis/
├── diabetes new.xlsx              ← Source dataset (768 patients, 8 variables)
├── README.md                      ← This file
└── powerbi/
    ├── queries/
    │   ├── DiabetesData.m         ← Main data load + all transformations
    │   ├── RiskScoreTable.m       ← Pre-aggregated risk summary table
    │   └── DateTable.m            ← Calendar dimension table
    ├── dax/
    │   └── measures.dax           ← All DAX measures (40+ measures, 4 sections)
    ├── schema/
    │   └── data_model.md          ← Table definitions, columns, relationships
    └── report/
        └── report_layout.md       ← Full page-by-page visual layout blueprint
```

---

## Dataset

**File:** `diabetes new.xlsx` — Sheet: `diabetes new`  
**Rows:** 768 patient records (Pima Indians Diabetes Study)  
**Columns:**

| Column | Description | Range |
|---|---|---|
| Age | Patient age (years) | 21–81 |
| Pregnancies | Number of pregnancies | 0–17 |
| Glucose | Plasma glucose concentration (mg/dL) | 0–199 |
| BloodPressure (mg/dL) | Diastolic blood pressure | 0–122 |
| SkinThickness | Triceps skinfold thickness (mm) | 0–99 |
| Insulin | 2-hour serum insulin (µIU/mL) | 0–846 |
| BMI | Body mass index (kg/m²) | 0–67.1 |
| DiabetesPedigreeFunction | Genetic diabetes risk score | 0.078–2.42 |

> **Data quality notes handled in Power Query:**  
> - Zeros in Glucose, BloodPressure, SkinThickness, Insulin, BMI are  
>   physiologically impossible and are treated as missing; they are  
>   imputed with the column median.  
> - ~84% of DiabetesPedigreeFunction values were stored ×1000 (e.g. 0.627  
>   stored as 627); the M query normalises these automatically.  
> - There is no `Outcome` column — a composite `RiskScore` (0–100) is  
>   derived from clinically validated thresholds.

---

## Prerequisites

| Requirement | Details |
|---|---|
| **Power BI Desktop** | Free download: [https://powerbi.microsoft.com/desktop](https://powerbi.microsoft.com/desktop) |
| **Operating System** | Windows 10 / 11 (Power BI Desktop is Windows-only) |
| **Version** | June 2024 or later (for new card visual + error bars) |
| **Source file** | `diabetes new.xlsx` placed in a known local path |

---

## Quick-Start — Build the .pbix

The full process takes ~30–45 minutes.  
Open each file in `powerbi/` alongside these instructions.

---

## Step 1 — Create a New Report

1. Open **Power BI Desktop**.  
2. Click **File → New**.  
3. Save immediately as `DiabetesAnalysis.pbix` in your preferred folder.

---

## Step 2 — Load the Data (Power Query M)

### 2a. Open Advanced Editor for DiabetesData

1. **Home → Transform Data** (opens Power Query Editor).  
2. In Power Query, click **Home → New Source → Blank Query**.  
3. Rename the query to `DiabetesData` (right-click → Rename).  
4. Click **View → Advanced Editor**.  
5. **Select all** the existing text and **delete it**.  
6. Open `powerbi/queries/DiabetesData.m` from this repository.  
7. **Copy the entire file contents** and paste into the Advanced Editor.  
8. Click **Done**.

> ⚠️ **Update the file path**  
> On line 19 of the M script, `File.Contents("diabetes new.xlsx")` uses a  
> relative path. If Power BI can't find the file, click  
> **Home → Data Source Settings → Change Source** and browse to the  
> absolute path of `diabetes new.xlsx`.

### 2b. Load RiskScoreTable

1. **New Source → Blank Query**, rename to `RiskScoreTable`.  
2. Advanced Editor → paste contents of `powerbi/queries/RiskScoreTable.m`.  
3. Click Done.

### 2c. Load DateTable

1. **New Source → Blank Query**, rename to `DateTable`.  
2. Advanced Editor → paste contents of `powerbi/queries/DateTable.m`.  
3. Click Done.

### 2d. Close and Apply

Click **Home → Close & Apply**. All three tables load into the data model.  
Expected row counts: `DiabetesData` = 768, `RiskScoreTable` = 3, `DateTable` = 11,323.

---

## Step 3 — Configure the Data Model

### 3a. Mark DateTable as a Date Table

1. Go to **Model view** (left sidebar icon).  
2. Right-click `DateTable` → **Mark as Date Table**.  
3. Set the date column to `Date`.

### 3b. Sort-by-Column Assignments

For proper axis ordering in visuals, apply these Sort By Column settings.  
In **Data view**, click the column, then **Column Tools → Sort by Column**:

| Table | Column | Sort By |
|---|---|---|
| DiabetesData | AgeGroup | AgeGroupSort |
| DiabetesData | GlucoseCategory | GlucoseCategorySort |
| DiabetesData | BMICategory | BMICategorySort |
| DiabetesData | RiskCategory | RiskCategorySort |
| DateTable | MonthName | MonthNum |
| DateTable | MonthShort | MonthNum |
| DateTable | DayOfWeekName | DayOfWeekNum |

### 3c. Add Calculated Columns

In **Data view**, select the `DiabetesData` table, then  
**Table Tools → New Column** for each:

**Risk Score Band** (for histogram buckets):
```dax
Risk Score Band =
VAR Band = FLOOR( DiabetesData[RiskScore], 10 )
RETURN FORMAT( Band, "0" ) & "–" & FORMAT( Band + 9, "0" )
```

**Risk Score Band Sort** (sort key for above):
```dax
Risk Score Band Sort =
FLOOR( DiabetesData[RiskScore], 10 )
```

After adding `Risk Score Band Sort`, go to **Column Tools → Sort by Column**  
and set `Risk Score Band` to sort by `Risk Score Band Sort`.

**Glucose × BMI** (scatter plot bubble size helper):
```dax
Glucose × BMI =
DiabetesData[Glucose] * DiabetesData[BMI]
```

### 3d. Create the Measures Table

1. **Modeling → New Table** and paste:
   ```dax
   _Measures = ROW( "Info", "All DAX measures stored here" )
   ```
2. This creates a blank table. All measures from Step 4 will live here.

---

## Step 4 — Create DAX Measures

All measures are documented in `powerbi/dax/measures.dax`.  
They are grouped into five sections with comments.

### How to Add Measures

1. In **Report view**, click the `_Measures` table in the Fields pane.  
2. **Modeling → New Measure**.  
3. In the formula bar, type (or paste) the measure expression.  
4. Press **Enter** or click the checkmark.

### Recommended Creation Order

Add measures in this order (some measures reference others):

**Section 0 — Base Measures** (create first):
- `Total Patients`
- `Total Patients (All)`
- `% of Total Patients`
- `Avg Age`, `Avg Glucose`, `Avg BMI`, `Avg Blood Pressure`
- `Avg Insulin`, `Avg DPF`, `Avg Pregnancies`, `Avg Skin Thickness`
- `Avg Risk Score`, `Max Risk Score`, `Min Risk Score`

**Section 1 — Executive Summary:**
- `High Risk Patients`, `Medium Risk Patients`, `Low Risk Patients`
- `High Risk %`, `Diabetic Range %`, `Pre-Diabetic %`, `Normal Glucose %`
- `Obese Patients %`, `Risk Score Gauge`, `Headline Summary`

**Section 2 — Risk Factors:**
- `Avg Risk Score (High)`, `Glucose Std Dev`, `BMI Std Dev`
- `High BP %`, `Elevated Insulin %`, `High DPF %`
- `Avg Concurrent Risk Factors`, `Glucose BMI Index`
- `Risk From Glucose`, `Risk From BMI`, `Risk From Age`
- `Risk From BP`, `Risk From Genetics`, `Risk From Pregnancies`

**Section 3 — Patient Analysis:**
- `Patients in Age Group`, `Avg BMI by Age Group`
- `BMI P25`, `BMI P75`, `Glucose P25`, `Glucose P75`
- `Max Pregnancies`, `High Pregnancy %`, `Age Range`
- `Median Glucose`, `Median BMI`, `Median Age`
- `Patient Profile Card`

**Section 4 — Predictive Insights:**
- `Predicted Diabetic Prob`, `Predicted Diabetic % Label`
- `Patients in Risk Band`
- `Cumulative Avg Risk Score by Age`, `Risk Score Trend`
- `Risk Tier High %`, `Risk Tier Medium %`, `Risk Tier Low %`
- `Top Risk Driver`, `Potential Risk Reduction`

---

## Step 5 — Build the Four Report Pages

Refer to `powerbi/report/report_layout.md` for the full visual specification  
(visual types, fields, axis assignments, formatting, colour maps).

### Rename the Pages

Right-click each tab at the bottom:
1. **Executive Summary**
2. **Risk Factors**
3. **Patient Analysis**
4. **Predictive Insights**

### Create Three Tooltip Pages (Hidden)

Add three more pages and rename them:
- `Tooltip - T1 Risk Tier Detail`
- `Tooltip - T2 Age Group Detail`
- `Tooltip - T3 Predictive Summary`

For each tooltip page:
- **View → Page Size → Type: Tooltip** (320 × 240 px)
- Right-click the tab → **Hide Page**
- In **Page information** (Format page panel), enable **Allow use as tooltip**

See `powerbi/report/report_layout.md` → "Tooltip Pages" section for the  
exact visual content of each tooltip page.

---

## Step 6 — Add Slicers and Slicer Sync

### Add Slicers on Each Page

Following the layout spec, add these slicers:

| Page | Slicer Field | Style |
|---|---|---|
| Executive Summary | `DiabetesData[AgeGroup]` | Dropdown |
| Executive Summary | `DiabetesData[RiskCategory]` | Tile |
| Risk Factors | `DiabetesData[AgeGroup]` | Dropdown |
| Risk Factors | `DiabetesData[RiskCategory]` | Tile |
| Risk Factors | `DiabetesData[GlucoseCategory]` | Dropdown |
| Risk Factors | `DiabetesData[BMICategory]` | Dropdown |
| Patient Analysis | `DiabetesData[AgeGroup]` | Dropdown |
| Patient Analysis | `DiabetesData[PregnancyGroup]` | Tile |
| Patient Analysis | `DiabetesData[BMICategory]` | Dropdown |
| Predictive Insights | `DiabetesData[AgeGroup]` | Dropdown |

### Sync AgeGroup Slicer Across All Pages

1. Click the **AgeGroup slicer** on Page 1.  
2. **View → Sync Slicers**.  
3. In the Sync Slicers panel, check **Sync** and **Visible** for all four pages.  
4. Repeat for the **RiskCategory** slicer (sync Pages 1 and 2).

---

## Step 7 — Configure Drill-Through

### Page 3 as Drill-Through Destination

1. Navigate to **Patient Analysis** page.  
2. Click on an empty area of the canvas.  
3. In the **Visualizations** pane, scroll down to find the **Drill through** well.  
4. Drag `DiabetesData[RiskCategory]` into the **Drill through** field well.  
5. Enable **Keep all filters**.

### Add a Back Button

1. **Insert → Buttons → Back**.  
2. Position in the top-left corner.  
3. Format: transparent background, white arrow.

### Test Drill-Through

1. Go to **Executive Summary** page.  
2. Right-click any bar in the Patients by Age Group chart.  
3. Select **Drill through → Patient Analysis**.

---

## Step 8 — Add Bookmarks

### Create Bookmarks

1. **View → Bookmarks → Add a Bookmark** for each state below.  
2. Name each bookmark exactly as shown.

| Page | Bookmark Name | Slicer State |
|---|---|---|
| Executive Summary | `BM_ExecAll` | All slicers cleared |
| Executive Summary | `BM_ExecHighRisk` | RiskCategory = "High Risk" |
| Executive Summary | `BM_ExecDiabeticRange` | GlucoseCategory = "Diabetic Range" |
| Risk Factors | `BM_RiskAll` | All slicers cleared |
| Risk Factors | `BM_RiskHighOnly` | RiskCategory = "High Risk" |
| Risk Factors | `BM_RiskObese` | BMICategory = Obese I/II/III |
| Patient Analysis | `BM_PatientAll` | All slicers cleared |
| Patient Analysis | `BM_PatientUnder30` | AgeGroup = "Under 30" |
| Predictive Insights | `BM_PredictAll` | All slicers cleared |
| Predictive Insights | `BM_PredictOlder` | AgeGroup = "50–59" + "60+" |

### Expose Bookmarks via Buttons

On each page, add a **"Quick Filters" button group**:
1. **Insert → Buttons → Blank** (one per bookmark).  
2. Set **Action → Type: Bookmark**, select the target bookmark.  
3. Label each button (e.g. "Show High Risk Only").  
4. Group the buttons: select all → **Format → Group**.

---

## Step 9 — Set Up Custom Tooltips

For each visual that should show a custom tooltip:

1. Click the visual.  
2. In **Visualizations → Format → General → Tooltips**:  
   - Type: **Report Page**  
   - Page: select the appropriate tooltip page (`T1`, `T2`, or `T3`)

| Visual | Tooltip Page |
|---|---|
| Executive Summary Donut | T1 — Risk Tier Detail |
| Patient Analysis Age Group chart | T2 — Age Group Detail |
| Predictive Insights Donut | T3 — Predictive Summary |

---

## Step 10 — Apply Conditional Formatting

### KPI Card — High Risk %
1. Click the **High Risk % card**.  
2. **Format → Callout value → Conditional formatting** (background colour):  
   - Rule: If value > 0.40 → background `#E94560` (coral)

### Patient Detail Table — Risk Score Column
1. Click the **Patient Detail table**.  
2. Select the `RiskScore` column → **Column formatting → Background colour**:  
   - Rules: < 30 → `#48BB78`, 30–59 → `#ECC94B`, ≥ 60 → `#E94560`

### Heatmap Matrix (Patient Analysis page)
1. Click the **Matrix visual**.  
2. **Values → Conditional formatting → Background colour** → Gradient:  
   - Min colour: white, Max colour: `#E94560`

### Risk Score Histogram (Predictive Insights page)
1. Click the **column chart**.  
2. **Columns → Conditional formatting → Background colour**:  
   - Based on field: `Risk Score Band Sort`  
   - Gradient: `#48BB78` (0) → `#ECC94B` (30) → `#E94560` (60+)

---

## Step 11 — Final Polish and Save

### Apply Theme

1. **View → Themes → Browse for themes**.  
2. Create a custom theme JSON or use the built-in **Dark** theme as a starting point.  
3. Core colours from the layout spec:
   - Background: `#1A1A2E`
   - Foreground: `#FFFFFF`
   - Data colours: `#00B4D8`, `#E94560`, `#48BB78`, `#ECC94B`, `#90E0EF`

### Add Page Navigation

For each page, add a vertical button strip on the left side:
1. **Insert → Buttons → Blank** (one per page).  
2. Action → Type: **Page Navigation** → Destination: target page.  
3. Add an icon (Home, Chart, People, Crystal Ball) via Format → Icon.  
4. Copy this button strip to all four pages.

### Final Checks

- [ ] All slicers work and cross-filter correctly  
- [ ] Drill-through works from Pages 1 & 2 to Page 3  
- [ ] Back button on Page 3 returns to the source page  
- [ ] All bookmarks restore the correct filter state  
- [ ] Tooltip pages appear on hover (not as regular report pages)  
- [ ] Sort-by-column is correct (AgeGroup, GlucoseCategory, etc.)  
- [ ] RiskScore histogram shows correct 10-pt bands in order  
- [ ] Conditional formatting thresholds apply correctly  

### Save

**File → Save** as `DiabetesAnalysis.pbix`.

---

## Report Pages Overview

### Page 1 — Executive Summary
High-level cohort KPIs: total patients, High Risk %, Diabetic Range %, average  
Glucose and BMI. Includes a Risk Tier donut chart, Risk Score gauge, and  
clustered bar chart of patients by Age Group coloured by Risk Category.

### Page 2 — Risk Factors
Deep-dive into which variables drive risk. Scatter plot of Glucose vs BMI  
(bubble size = concurrent risk factors), waterfall/column chart of risk  
contribution by factor, box-plot proxy for BMI/Glucose spread, and a  
correlation matrix heatmap.

### Page 3 — Patient Analysis
Demographic analysis and drill-through landing page. Stacked column chart by  
Age Group, line + column combo showing risk score trend, heatmap matrix  
(Age Group × BMI Category), and a sortable patient detail table with  
conditional formatting.

### Page 4 — Predictive Insights
Forward-looking analytics: risk score trend line by age cohort, predicted  
diabetic probability (logistic proxy), 100% stacked bar of risk tier  
distribution, risk score histogram, and an intervention simulation table  
showing how many High Risk patients could be reclassified with a 5-point  
BMI reduction.

---

## DAX Measures Reference

Full measure code is in `powerbi/dax/measures.dax`.  
Summary of the 40+ measures by section:

| Section | Measures |
|---|---|
| **Base** | Total Patients, % of Total, Avg Age/Glucose/BMI/BP/Insulin/DPF, Avg Risk Score |
| **Executive Summary** | High/Medium/Low Risk Patients & %, Diabetic Range %, Obese %, Risk Score Gauge |
| **Risk Factors** | High BP %, Elevated Insulin %, High DPF %, Avg Concurrent Risk Factors, Risk From [Factor] × 6 |
| **Patient Analysis** | Median Age/BMI/Glucose, BMI/Glucose P25/P75, High Pregnancy %, Patient Profile Card |
| **Predictive Insights** | Predicted Diabetic Prob, Top Risk Driver, Risk Tier %, Potential Risk Reduction, Cumulative Risk Score |

---

## Power Query Transformations

Full M code is in `powerbi/queries/DiabetesData.m`.  
Key transformation steps:

| Step | Action |
|---|---|
| Load | Read `diabetes new.xlsx` sheet `diabetes new` |
| Rename | Standardise column names (remove special chars and units) |
| Type | Cast all columns to correct data types |
| Surrogate Key | Add `PatientID` index (1–768) |
| Fix DPF | Divide DPF values > 2.5 by 1000 (normalise scaling error) |
| Null zeros | Replace impossible zeros in 5 clinical columns with `null` |
| Impute | Fill nulls with column median (non-destructive, preserves distribution) |
| AgeGroup | Bin ages into 5 cohorts: Under 30 / 30–39 / 40–49 / 50–59 / 60+ |
| GlucoseCategory | ADA thresholds: Normal / Pre-Diabetic / Diabetic Range |
| BMICategory | WHO classification: Underweight → Obese III (6 bands) |
| BPCategory | JNC-8 hypertension stages |
| InsulinCategory | Not Measured / Low / Normal / High |
| RiskScore | Composite 0–100 score (7 clinical factors, point-based) |
| RiskCategory | High / Medium / Low Risk from RiskScore |

---

## Troubleshooting

**"File not found" error when loading data**  
→ Open **Home → Transform Data**, click the `DiabetesData` query,  
→ **Home → Data Source Settings → Change Source**, browse to `diabetes new.xlsx`.

**AgeGroup sorts alphabetically instead of chronologically**  
→ In Data view, click `DiabetesData[AgeGroup]`  
→ **Column Tools → Sort by Column → AgeGroupSort**.  
Repeat for other categorical columns (see [Step 3b](#3b-sort-by-column-assignments)).

**RiskScoreTable shows formula errors**  
→ Ensure `DiabetesData` query loads successfully first.  
→ `RiskScoreTable` references `DiabetesData` by name — both must exist.

**Drill-through option missing from right-click menu**  
→ Confirm `DiabetesData[RiskCategory]` is in the **Drill through** well on Page 3.  
→ The field must be added to the Drill-through well, not the Filters well.

**Tooltip page appears as a regular page**  
→ Right-click the tooltip page tab → **Hide Page**.  
→ In **Format page → Page information**, enable "Allow use as tooltip".

**Predicted Diabetic Prob returns blank**  
→ The measure requires `[Avg Glucose]`, `[Avg BMI]`, and `[Avg Age]` to all  
  return numeric values. Confirm the base measures are created (Section 0).

---

*Dataset source: Pima Indians Diabetes Database (Smith et al., 1988),  
available via the UCI Machine Learning Repository.*
