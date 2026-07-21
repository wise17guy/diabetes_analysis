# Report Layout Specification

## Overview

This document describes the complete visual layout for each of the four  
Diabetes Analysis report pages.  Use it as a blueprint when building the  
`.pbix` file in Power BI Desktop.

**Canvas size:** 1280 × 720 px (16:9, default widescreen)  
**Theme:** Dark background (`#1A1A2E`) with teal/coral accent palette  
**Font:** Segoe UI throughout

---

## Colour Palette

| Token | Hex | Used For |
|---|---|---|
| Background | `#1A1A2E` | Canvas background |
| Panel | `#16213E` | Card / visual background |
| Accent 1 – Teal | `#0F3460` | High-risk indicators |
| Accent 2 – Coral | `#E94560` | Alert / high-risk markers |
| Accent 3 – Cyan | `#00B4D8` | Primary data series |
| Accent 4 – Lime | `#90E0EF` | Secondary data series |
| Text Primary | `#FFFFFF` | Titles, labels |
| Text Secondary | `#A0AEC0` | Subtitles, axis labels |
| Low Risk | `#48BB78` | Green |
| Medium Risk | `#ECC94B` | Amber |
| High Risk | `#E94560` | Coral/Red |

---

## Page 1: Executive Summary

**Purpose:** One-glance overview of the entire cohort — total patients, risk  
distribution, and key clinical averages.

**Navigation panel** (left, 40 px wide): vertical icon strip for page switching  
(use Buttons > Blank + Action: Page Navigation for each icon).

---

### Layout Grid (1240 × 680 px working area)

```
┌──────────────────────────────────────────────────────────────────┐
│  PAGE TITLE  "Diabetes Risk – Executive Summary"          [date] │
├────────┬────────┬────────┬────────┬────────┬────────────────────┤
│ KPI 1  │ KPI 2  │ KPI 3  │ KPI 4  │ KPI 5  │                    │
│ Total  │ High   │ Diab.  │ Avg    │ Avg    │  Risk Tier Donut   │
│ Pats   │ Risk % │ Range% │ Glucose│ BMI    │   (RiskCategory)   │
│        │        │        │        │        │                    │
├────────┴────────┴────────┴────────┴────────┤                    │
│                                            ├────────────────────┤
│   Clustered Bar — Patients by AgeGroup     │  Risk Score Gauge  │
│   with RiskCategory colour fill            │    (Avg Risk Score │
│   [sorted by AgeGroupSort]                 │     0–100)         │
│                                            │                    │
├────────────────────────────────────────────┴────────────────────┤
│  Stacked 100% Bar — GlucoseCategory distribution by AgeGroup   │
│  X: AgeGroup | Series: GlucoseCategory | Y: Count              │
├──────────────────────────────┬──────────────────────────────────┤
│   BMI Distribution (column   │   Slicer: AgeGroup              │
│   histogram by BMICategory)  │   Slicer: RiskCategory          │
│                              │   [both multi-select dropdown]  │
└──────────────────────────────┴──────────────────────────────────┘
```

---

### Visuals Detail

#### KPI Cards (5 cards, top row)

| # | Title | Measure | Format |
|---|---|---|---|
| 1 | Total Patients | `[Total Patients]` | `#,0` |
| 2 | High Risk | `[High Risk %]` | `0.0%` |
| 3 | Diabetic Range | `[Diabetic Range %]` | `0.0%` |
| 4 | Avg Glucose | `[Avg Glucose]` | `0.0 mg/dL` |
| 5 | Avg BMI | `[Avg BMI]` | `0.00` |

- Visual type: **Card** (new card visual)  
- Show sparkline: Yes (use RiskScore field as sparkline basis)  
- Conditional formatting on the KPI 2 card: Red background when `[High Risk %] > 0.40`

#### Risk Tier Donut (top-right)

- Visual: **Donut chart**  
- Legend: `DiabetesData[RiskCategory]`  
- Values: `[Total Patients]`  
- Inner label: `[Risk Score Gauge]` (Avg Risk Score as text)  
- Colour map: Low Risk → `#48BB78`, Medium → `#ECC94B`, High → `#E94560`

#### Risk Score Gauge

- Visual: **Gauge**  
- Value: `[Risk Score Gauge]`  
- Min: 0, Max: 100  
- Target value: 60 (threshold for High Risk)  
- Fill colour: Green below 30, Amber 30–60, Red above 60 (set via conditional formatting)

#### Clustered Bar — Patients by Age Group

- Visual: **Clustered bar chart**  
- Y axis: `DiabetesData[AgeGroup]` (sort by `AgeGroupSort`)  
- X axis: `[Total Patients]`  
- Series (legend): `DiabetesData[RiskCategory]`  
- Colour: per Risk Tier palette  
- Data labels: On  
- Tooltip: Add `[Avg Glucose]`, `[Avg BMI]`, `[Avg Risk Score]`

#### 100% Stacked Bar — Glucose Category by Age Group

- Visual: **100% stacked bar chart**  
- Y axis: `DiabetesData[AgeGroup]` (sort by `AgeGroupSort`)  
- X axis: `[% of Total Patients]`  
- Series: `DiabetesData[GlucoseCategory]` (sort by `GlucoseCategorySort`)  
- Colour: Normal → Cyan, Pre-Diabetic → Amber, Diabetic Range → Coral

#### BMI Histogram

- Visual: **Clustered column chart** (use BMICategory as X axis)  
- X axis: `DiabetesData[BMICategory]` (sort by `BMICategorySort`)  
- Y axis: `[Total Patients]`  
- Colour: per category (green → yellow → orange → red gradient)

#### Slicers

| Slicer | Field | Style |
|---|---|---|
| Age Group | `DiabetesData[AgeGroup]` | Dropdown, multi-select |
| Risk Category | `DiabetesData[RiskCategory]` | Tile (3 tiles) |

---

### Bookmarks (Page 1)

| Bookmark Name | State Captured |
|---|---|
| `BM_ExecAll` | All slicers cleared — full cohort view |
| `BM_ExecHighRisk` | RiskCategory slicer = "High Risk" only |
| `BM_ExecDiabeticRange` | GlucoseCategory = "Diabetic Range" |

Add a **Bookmark Navigator** button group (View > Bookmarks > Add) in the top-right  
corner, labelled "Quick Filters".

---

### Tooltips (Page 1)

- KPI cards: Enable default tooltip showing measure name + value.  
- Donut chart: Custom tooltip page (see **Tooltip Page T1** below).  
- Bar charts: Enable **drill-through** to Patient Analysis page (see Page 3 setup).

---

## Page 2: Risk Factors

**Purpose:** Explore which clinical variables drive the composite risk score —  
BMI, glucose, blood pressure, age, genetics, insulin, pregnancies.

---

### Layout Grid

```
┌──────────────────────────────────────────────────────────────────┐
│  PAGE TITLE  "Risk Factor Analysis"                              │
├──────────────────────────────────────────────┬───────────────────┤
│                                              │  Slicers:         │
│  Scatter Plot                                │  AgeGroup         │
│  X: Avg Glucose   Y: Avg BMI                 │  RiskCategory     │
│  Bubble size: [Avg Concurrent Risk Factors]  │  GlucoseCategory  │
│  Colour: RiskCategory                        │  BMICategory      │
│                                              │                   │
├──────────────────────────────────────────────┴───────────────────┤
│                                                                  │
│  Waterfall Chart — Avg Risk Point Contribution by Factor        │
│  Category: Factor names (Glucose, BMI, Age, BP, DPF, Preg.)    │
│  Values: [Risk From Glucose], [Risk From BMI], etc.             │
│                                                                  │
├─────────────────────────┬────────────────────────────────────────┤
│  Box-plot proxy         │  Correlation Matrix (Table visual)     │
│  (Column chart with     │  Rows: Factor  Cols: Avg Value         │
│   P25/P75 as error bars │  Conditional formatting: Heat map      │
│   for BMI and Glucose)  │  (darker = higher average)             │
│                         │                                        │
└─────────────────────────┴────────────────────────────────────────┘
```

---

### Visuals Detail

#### Scatter Plot — Glucose vs BMI

- Visual: **Scatter chart**  
- X axis: `[Avg Glucose]`  
- Y axis: `[Avg BMI]`  
- Size: `[Avg Concurrent Risk Factors]`  
- Play axis: (none — no date column)  
- Legend: `DiabetesData[RiskCategory]`  
- Reference line: X = 126 (ADA diabetes threshold); Y = 30 (obese threshold)  
- Tooltip: Add `[Avg DPF]`, `[Avg Blood Pressure]`, `[Total Patients]`

#### Waterfall Chart — Risk Factor Contributions

- Visual: **Waterfall chart**  
- Category: Static labels — use a disconnected table or a matrix  
- Values: `[Risk From Glucose]`, `[Risk From BMI]`, `[Risk From Age]`,  
  `[Risk From BP]`, `[Risk From Genetics]`, `[Risk From Pregnancies]`  
- **Implementation tip:** Create a supporting DAX table:
  ```dax
  RiskFactors =
  DATATABLE(
      "Factor",    STRING,
      "SortOrder", INTEGER,
      {
          { "Glucose",      1 },
          { "BMI",          2 },
          { "Age",          3 },
          { "Blood Press.", 4 },
          { "Genetics",     5 },
          { "Pregnancies",  6 }
      }
  )
  ```
  Then use a Clustered Column chart with Factor on X axis and the corresponding  
  Risk From [X] measure on Y axis (waterfall chart in Power BI requires  
  a breakdown column, so a clustered column achieves the same waterfall effect).

#### Box-Plot Proxy — BMI and Glucose Spread

- Visual: **Error bar column chart** (or Line and Column Combo)  
- X axis: `DiabetesData[RiskCategory]`  
- Column values: `[Median BMI]` and `[Median Glucose]` (two series)  
- Error bars set via `[BMI P25]` / `[BMI P75]` for lower/upper bounds  
- Tooltip: `[BMI P25]`, `[BMI P75]`, `[Glucose P25]`, `[Glucose P75]`

#### Correlation Matrix (Table Visual)

- Visual: **Matrix**  
- Rows: `DiabetesData[RiskCategory]`  
- Columns: Measures  
- Values: `[Avg Glucose]`, `[Avg BMI]`, `[Avg Blood Pressure]`, `[Avg DPF]`,  
  `[Avg Pregnancies]`, `[Avg Insulin]`  
- Conditional formatting (background colour) applied to each value column:  
  gradient from white (low) to `#E94560` (high)

---

### Bookmarks (Page 2)

| Bookmark Name | State |
|---|---|
| `BM_RiskAll` | All slicers cleared |
| `BM_RiskHighOnly` | RiskCategory = "High Risk" |
| `BM_RiskGlucose` | GlucoseCategory = "Diabetic Range" |
| `BM_RiskObese` | BMICategory filter to Obese I/II/III |

---

### Drill-Through Setup (Page 2 as Source)

Clicking a **RiskCategory** in the scatter or waterfall chart drills through to  
**Page 3: Patient Analysis** (configured on Page 3 — see below).

---

## Page 3: Patient Analysis

**Purpose:** Patient-level exploration — demographic breakdowns, drill-through  
landing page, individual patient spotlight.

---

### Layout Grid

```
┌──────────────────────────────────────────────────────────────────┐
│  PAGE TITLE  "Patient Analysis"   ← [Back] button (top-left)    │
├──────────────────────────────────┬───────────────────────────────┤
│                                  │  KPI Strip (4 cards):         │
│  Stacked Column Chart            │  Median Age | Median Glucose  │
│  X: AgeGroup                     │  Median BMI | Avg Risk Score  │
│  Y: Total Patients               │                               │
│  Series: RiskCategory            │  Slicer: AgeGroup             │
│                                  │  Slicer: PregnancyGroup       │
├──────────────────────────────────┤  Slicer: BMICategory          │
│  Line Chart                      │                               │
│  X: AgeGroup (sorted)            ├───────────────────────────────┤
│  Y: [Avg Risk Score]             │  Patient Detail Table         │
│  Secondary Y: [Avg Glucose]      │  Columns: PatientID, Age,     │
│                                  │  RiskCategory, Glucose,       │
│                                  │  BMI, RiskScore               │
│                                  │  (sorted by RiskScore DESC)   │
├──────────────────────────────────┴───────────────────────────────┤
│  Heatmap Matrix                                                  │
│  Rows: AgeGroup   Cols: BMICategory                              │
│  Values: [Total Patients]                                        │
│  Background: gradient green→red (conditional formatting)         │
└──────────────────────────────────────────────────────────────────┘
```

---

### Visuals Detail

#### Back Button

- Visual: **Button > Back**  
- Position: top-left corner (for drill-through return navigation)  
- Style: transparent background, white arrow icon

#### KPI Strip (4 mini cards)

| Measure | Label |
|---|---|
| `[Median Age]` | Median Age |
| `[Median Glucose]` | Median Glucose |
| `[Median BMI]` | Median BMI |
| `[Avg Risk Score]` | Avg Risk Score |

#### Stacked Column — Patients by Age Group

- Visual: **Stacked column chart**  
- X: `DiabetesData[AgeGroup]` (sorted by `AgeGroupSort`)  
- Y: `[Total Patients]`  
- Legend: `DiabetesData[RiskCategory]` (colour by risk tier)  
- Data labels: On  
- Tooltip: Custom tooltip page **T2** (Avg Glucose, Avg BMI, Avg Risk Score per AgeGroup)

#### Line + Column Combo — Age Group Trend

- Visual: **Line and stacked column chart**  
- Shared axis: `DiabetesData[AgeGroup]`  
- Column values: `[Total Patients]`  
- Line values: `[Avg Risk Score]`  
- Secondary Y axis: `[Avg Glucose]` (as a second line series)  
- Markers: On for both lines

#### Heatmap Matrix

- Visual: **Matrix**  
- Rows: `DiabetesData[AgeGroup]` (sorted by `AgeGroupSort`)  
- Columns: `DiabetesData[BMICategory]` (sorted by `BMICategorySort`)  
- Values: `[Total Patients]`  
- Background colour conditional formatting: white → red gradient based on patient count  
- Enable **Grand Totals** for rows and columns

#### Patient Detail Table

- Visual: **Table**  
- Columns: `PatientID`, `Age`, `RiskCategory`, `RiskScore`, `Glucose`, `BMI`,  
  `BloodPressure`, `DiabetesPedigreeFunction`  
- Sort: `RiskScore` descending by default  
- Conditional formatting on `RiskScore`: red ≥60, amber 30–59, green <30  
- Enable row-level conditional formatting on `GlucoseCategory`  
- **Drill-through target:** This table responds to drill-through from Pages 1 and 2  
  Add `DiabetesData[RiskCategory]` to the Drill-through well

---

### Drill-Through Configuration

On Page 3, add `DiabetesData[RiskCategory]` to the **Drill-through** field well.  
- Enable "Keep all filters"  
- This makes Page 3 the drill-through destination from Pages 1 and 2

Users right-click any `RiskCategory` value on Pages 1 or 2 → "Drill through → Patient Analysis"

---

### Bookmarks (Page 3)

| Bookmark Name | State |
|---|---|
| `BM_PatientAll` | All slicers reset |
| `BM_PatientUnder30` | AgeGroup = "Under 30" |
| `BM_PatientHighBMI` | BMICategory = Obese I/II/III |

---

### Tooltips (Page 3)

Custom tooltip page **T2** shows when hovering a bar in the Age Group stacked column:  
- Card: AgeGroup name  
- Gauge: Avg Risk Score  
- 3 mini KPIs: Avg Glucose, Avg BMI, Patient Count  

---

## Page 4: Predictive Insights

**Purpose:** Forward-looking analytics — risk trajectory, predicted diabetic  
probability, intervention simulation, and top risk driver identification.

---

### Layout Grid

```
┌──────────────────────────────────────────────────────────────────┐
│  PAGE TITLE  "Predictive Insights"                               │
├────────────────────────────────────────┬─────────────────────────┤
│                                        │  KPI Strip:             │
│  Line Chart — Risk Score Trend         │  Predicted Diabetic %   │
│  X: AgeGroup (sorted)                  │  Top Risk Driver (card) │
│  Y: [Cumulative Avg Risk Score]        │  High Risk %            │
│      [Risk Score Trend]                │  Potential Reduction    │
│  Two lines; shaded area between them   │                         │
│                                        │  Slicer: AgeGroup       │
├────────────────────────────────────────┴─────────────────────────┤
│                                                                  │
│  100% Stacked Bar — Risk Tier Distribution by Age Group          │
│  X: AgeGroup | Series: RiskCategory | Y: % of Total             │
│                                                                  │
├──────────────────────────────┬───────────────────────────────────┤
│  Donut — Risk Tier %         │  Histogram (column chart)         │
│  [Risk Tier High %]          │  X: Risk Score Band (10-pt bins)  │
│  [Risk Tier Medium %]        │  Y: [Total Patients]              │
│  [Risk Tier Low %]           │  Colour gradient: green→red       │
│  Centre label: Avg Risk Score│                                   │
├──────────────────────────────┴───────────────────────────────────┤
│  Intervention Simulation Table                                   │
│  Shows: RiskCategory | Count | PotentialReduction                │
│  Subtitle: "Patients who exit High Risk with −5 BMI points"     │
└──────────────────────────────────────────────────────────────────┘
```

---

### Visuals Detail

#### KPI Strip (top-right, 4 cards)

| Measure | Label | Format |
|---|---|---|
| `[Predicted Diabetic % Label]` | Predicted Diabetic Risk | text |
| `[Top Risk Driver]` | Top Risk Driver | text |
| `[High Risk %]` | High Risk % | `0.0%` |
| `[Potential Risk Reduction]` | Patients — Reducible | `#,0` |

- `[Predicted Diabetic % Label]` card: background changes to coral when value > 35%  
- `[Top Risk Driver]` card: displays the dynamic text measure

#### Line Chart — Risk Score Trend

- Visual: **Line chart**  
- X axis: `DiabetesData[AgeGroup]` (sorted by `AgeGroupSort`)  
- Lines:  
  - Line 1: `[Risk Score Trend]` (average per group — solid teal line)  
  - Line 2: `[Cumulative Avg Risk Score by Age]` (running average — dashed white line)  
- Enable **shaded area** below Line 1  
- Reference line: Y = 60 (High Risk threshold, dashed red)  
- Tooltip: `[Predicted Diabetic Prob]`, `[Total Patients]`, `[Avg Glucose]`

#### 100% Stacked Bar — Risk Distribution by Age

- Visual: **100% stacked bar chart**  
- Y axis: `DiabetesData[AgeGroup]` (sorted by `AgeGroupSort`)  
- X axis: `[% of Total Patients]`  
- Series: `DiabetesData[RiskCategory]` (sorted by `RiskCategorySort`)  
- Colour: per risk tier palette

#### Risk Tier Donut

- Visual: **Donut chart**  
- Values:  
  ```
  Legend: DiabetesData[RiskCategory]
  Values:  [Total Patients]
  ```
- Centre label: `[Risk Score Gauge]`  
- Tooltip: custom tooltip page **T3**

#### Risk Score Histogram

- Visual: **Clustered column chart**  
- X axis: `DiabetesData[Risk Score Band]` (sort by `Risk Score Band Sort`)  
- Y axis: `[Patients in Risk Band]`  
- Colour gradient conditional formatting on columns: green (0–10) → amber (30–50) → red (60–100)  
- Reference line: X = "60–69" band (High Risk boundary)

#### Intervention Simulation Table

- Visual: **Table**  
- Columns:  
  | Field / Measure | Label |
  |---|---|
  | `DiabetesData[RiskCategory]` | Risk Category |
  | `[Total Patients]` | Current Count |
  | `[Potential Risk Reduction]` | Reducible (−5 BMI) |
  | `[Predicted Diabetic Prob]` | Predicted Risk |
- Conditional formatting on `[Potential Risk Reduction]`: green bars  
- Subtitle text box below the table:  
  *"Reducible = High Risk patients who would exit that tier  
  if BMI was reduced by 5 points."*

---

### Bookmarks (Page 4)

| Bookmark Name | State |
|---|---|
| `BM_PredictAll` | All slicers cleared |
| `BM_PredictUnder40` | AgeGroup = "Under 30" + "30–39" |
| `BM_PredictOlder` | AgeGroup = "50–59" + "60+" |

---

## Tooltip Pages

Tooltip pages are **hidden report pages** (right-click tab → Hide Page).  
Set canvas to **Tooltip** size (320 × 240 px) via View > Page Size > Tooltip.

### Tooltip Page T1 — Risk Tier Detail

Used by: Executive Summary Donut chart  
Content:
- Title text box: `DiabetesData[RiskCategory]` (dynamic, set via slicer context)
- 3 KPI cards: Avg Glucose · Avg BMI · Patient Count
- Mini bar chart: Avg Risk Score vs RiskCategory

### Tooltip Page T2 — Age Group Detail

Used by: Patient Analysis Age Group stacked column  
Content:
- Title text box: "Age Group: " + AgeGroup value
- Gauge: Avg Risk Score (0–100)
- 3 mini KPI cards: Avg Glucose · Avg BMI · Patient Count

### Tooltip Page T3 — Predictive Summary

Used by: Predictive Insights Donut  
Content:
- Donut slice label: RiskCategory name
- Predicted Diabetic Prob measure (large card, formatted %)
- Top Risk Driver measure (text card)

---

## Navigation & Interactivity Summary

| Feature | Location | Implementation |
|---|---|---|
| Page navigation buttons | All pages, left panel | Blank button → Action: Page Navigation |
| Drill-through | Pages 1 & 2 → Page 3 | RiskCategory in Page 3 drill-through well |
| Back button | Page 3 (top-left) | Button type = Back |
| Bookmarks | All pages | View > Bookmarks; exposed via Button > Bookmark |
| Slicers | All pages | Dropdown (multi-select) or Tile |
| Slicer sync | All pages | View > Sync Slicers (AgeGroup synced across all pages) |
| Custom tooltips | Pages 1, 3, 4 | Hidden tooltip pages T1, T2, T3 |
| Cross-filter | All visuals | Default (click any visual filters others) |
| Conditional formatting | KPI cards, tables, matrices | Based on measure thresholds |

---

## Recommended Visual Import (AppSource)

The following certified Power BI visuals from AppSource enhance this report:

| Visual | Use |
|---|---|
| **Chiclet Slicer** | Tile-style slicer for RiskCategory with custom colours |
| **Enlighten Aquarium** | Eye-catching animated KPI for homepage |
| **Violin Plot** | BMI / Glucose distribution (replaces box-plot proxy) |
| **Charticulator** | Custom waterfall for risk factor contributions |

> These are optional. All layouts above work with built-in Power BI visuals.
