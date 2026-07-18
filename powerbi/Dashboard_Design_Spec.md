# Power BI Dashboard Design Specification
## Diabetes Risk Analytics

---

## Overview

| Attribute | Value |
|-----------|-------|
| Data source | `diabetes_powerbi_ready.xlsx` → Sheet `Diabetes Data` |
| Number of pages | 4 |
| Canvas size | 1280 × 720 px (16:9) |
| Theme | Custom — primary `#C0392B` (red), secondary `#2980B9` (blue), accent `#27AE60` (green) |
| Cross-filter behavior | All visuals cross-filter each other within a page |

---

## Page 1 — Executive Summary

**Purpose:** High-level KPIs and population-level risk overview visible at a glance.

### Slicers (top bar, horizontal)
| Field | Type | Default |
|-------|------|---------|
| Age Group | Tile slicer | All |
| Risk Tier | Tile slicer | All |
| BMI Category | Dropdown slicer | All |

### KPI Cards (row of 4, below slicers)
| Card | Measure | Icon |
|------|---------|------|
| Total Patients | `Total Patients` | People |
| High Risk Patients | `High Risk Patients` | Warning |
| Avg Risk Score | `Avg Risk Score` | Gauge |
| % High Risk | `% High Risk` (format: %) | Alert |

### Visuals

| # | Visual Type | X / Category | Y / Value | Details |
|---|-------------|-------------|-----------|---------|
| 1 | **Donut chart** | Risk Tier | Count of patients | Colors: High=Red, Medium=Orange, Low=Green |
| 2 | **Clustered bar chart** | Age Group | Avg Risk Score | Sort descending; reference line at 50 |
| 3 | **Treemap** | BMI Category → Glucose Category | Count of patients | Hierarchical view of population |
| 4 | **Card (multi-row)** | — | Avg Glucose, Avg BMI, Avg BP, Avg Insulin | Benchmark comparison row |
| 5 | **Gauge** | — | Avg Risk Score | Min 0, Max 100; target at 50 |

---

## Page 2 — Risk Factor Deep-Dive

**Purpose:** Explore how each clinical variable correlates with risk.

### Slicers
| Field | Type |
|-------|------|
| Risk Tier | Tile slicer |
| Age Group | Tile slicer |
| Pregnancy Group | Dropdown |

### Visuals

| # | Visual Type | Details |
|---|-------------|---------|
| 1 | **Scatter chart** | X=Glucose, Y=BMI, Size=Risk Score, Color=Risk Tier, Tooltip=Risk Label |
| 2 | **Box & Whisker** (built-in or custom) | Glucose distribution by Risk Tier |
| 3 | **Clustered column chart** | Avg Glucose vs Avg BMI side-by-side by Age Group |
| 4 | **Line chart** | Risk Score trend across Age values (X=Age, Y=Avg Risk Score) |
| 5 | **100% Stacked bar** | Glucose Category breakdown by Age Group |
| 6 | **Card** | `% Diabetic Glucose Range` — large percentage format |

**Reference Lines (on scatter chart):**
- Vertical dashed line at Glucose = 126 (Diabetic threshold)
- Horizontal dashed line at BMI = 30 (Obese threshold)

---

## Page 3 — Population Health Analytics

**Purpose:** Demographic and multi-factor population analysis.

### Slicers
| Field | Type |
|-------|------|
| BMI Category | Checkbox list |
| BP Category | Checkbox list |
| Insulin Resistance | Toggle/Tile |

### Visuals

| # | Visual Type | Details |
|---|-------------|---------|
| 1 | **Stacked bar chart** | BMI Category by Risk Tier (count) |
| 2 | **Pie chart** | Glucose Category distribution |
| 3 | **Matrix / Heatmap** | Rows=Age Group, Cols=BMI Category, Values=Avg Risk Score; conditional formatting red-green |
| 4 | **Clustered bar** | Avg Insulin by Pregnancy Group |
| 5 | **Donut** | BP Category distribution |
| 6 | **KPI Card row** | `% Obese`, `% Insulin Resistance`, `% High BP`, `% Diabetic Glucose Range` |
| 7 | **Waterfall chart** | Show average Risk Score contribution by factor (use reference measures) |

---

## Page 4 — Patient-Level Explorer

**Purpose:** Drill down to individual patient records for clinical use.

### Slicers
| Field | Type |
|-------|------|
| Risk Tier | Tile slicer |
| Age Group | Dropdown |
| BMI Category | Dropdown |
| Risk Score (range) | Slider slicer (min/max on Risk Score) |

### Visuals

| # | Visual Type | Details |
|---|-------------|---------|
| 1 | **Table** | Patient ID, Age, Glucose, BMI, Blood Pressure, Insulin, Risk Score, Risk Tier — sortable; conditional formatting on Risk Score (red-yellow-green scale) |
| 2 | **Scatter chart** | X=Age, Y=Risk Score, Color=Risk Tier, Tooltip shows all clinical values |
| 3 | **Bar chart** | Top 20 highest Risk Score patients (sorted descending) |
| 4 | **Card** | Selected patient detail (use SELECTEDVALUE on Patient ID slicer) |
| 5 | **Radar / Spider chart** | Selected patient's normalised clinical profile vs population average (custom visual) |

**Export:** Enable "Export data" on the table visual for CSV download.

---

## Color Theme

```json
{
  "name": "Diabetes Risk Theme",
  "dataColors": [
    "#C0392B",
    "#E74C3C",
    "#E67E22",
    "#F39C12",
    "#27AE60",
    "#2980B9",
    "#8E44AD",
    "#16A085"
  ],
  "background": "#FFFFFF",
  "foreground": "#252423",
  "tableAccent": "#C0392B",
  "sentiment": {
    "bad": "#C0392B",
    "neutral": "#F39C12",
    "good": "#27AE60"
  }
}
```

Save the above as `diabetes_theme.json` and import via **View → Themes → Browse for themes**.

---

## Recommended Custom Visuals (from AppSource)

| Visual | Purpose |
|--------|---------|
| **Violin Plot** | Glucose / BMI distribution by Risk Tier |
| **Radar Chart** | Patient profile vs population average (Page 4) |
| **Chiclet Slicer** | Tile-style slicers with color coding |
| **Box and Whisker Chart** | Distribution spread per category |

---

## Navigation & UX

- Add a **navigation pane** (bookmark-based buttons): Executive Summary | Risk Factors | Population | Patient Explorer
- Add a **Reset Filters** button on every page (bookmark that clears all slicers)
- Enable **Sync slicers** for `Risk Tier` and `Age Group` across all pages
- Use **Tooltips** pages: create a 320×240 tooltip page showing a mini patient profile card
- Enable **Drill-through** from any Risk Tier visual → Page 4 filtered to that tier

---

## Data Refresh

- Data source: local Excel file `diabetes_powerbi_ready.xlsx`
- To schedule refresh via Power BI Service: publish the report and configure a gateway connection to the Excel file
