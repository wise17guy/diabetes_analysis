// ============================================================
// Query Name : DiabetesData
// Purpose    : Load, clean, and transform the raw diabetes
//              Excel dataset into an analysis-ready table.
// Source     : "diabetes new.xlsx"  (sheet: "diabetes new")
// ============================================================

let
    // ------------------------------------------------------------------
    // 1. LOAD SOURCE
    //    Adjust the file path to match where you placed the .xlsx file.
    //    In Power BI Desktop: Home > Transform Data > Data Source Settings
    //    to update the path after loading for the first time.
    // ------------------------------------------------------------------
    Source = Excel.Workbook(
        File.Contents("diabetes new.xlsx"),
        null,   // use first sheet
        true    // first row as headers
    ),
    RawSheet      = Source{[Item = "diabetes new", Kind = "Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(RawSheet, [PromoteAllScalars = true]),

    // ------------------------------------------------------------------
    // 2. RENAME COLUMNS  (normalise to clean, space-free names)
    // ------------------------------------------------------------------
    RenamedCols = Table.RenameColumns(
        PromotedHeaders,
        {
            {"Age",                       "Age"},
            {"Pregnancies",               "Pregnancies"},
            {"Glucose",                   "Glucose"},
            {"BloodPressure (mg/dL)",     "BloodPressure"},
            {"SkinThickness",             "SkinThickness"},
            {"Insulin",                   "Insulin"},
            {"BMI",                       "BMI"},
            {"DiabetesPedigreeFunction",  "DiabetesPedigreeFunction"}
        }
    ),

    // ------------------------------------------------------------------
    // 3. SET DATA TYPES
    // ------------------------------------------------------------------
    TypedTable = Table.TransformColumnTypes(
        RenamedCols,
        {
            {"Age",                      Int64.Type},
            {"Pregnancies",              Int64.Type},
            {"Glucose",                  Int64.Type},
            {"BloodPressure",            Int64.Type},
            {"SkinThickness",            Int64.Type},
            {"Insulin",                  Int64.Type},
            {"BMI",                      type number},
            {"DiabetesPedigreeFunction", type number}
        }
    ),

    // ------------------------------------------------------------------
    // 4. ADD SURROGATE KEY (PatientID)
    // ------------------------------------------------------------------
    AddPatientID = Table.AddIndexColumn(TypedTable, "PatientID", 1, 1, Int64.Type),

    // ------------------------------------------------------------------
    // 5. FIX DiabetesPedigreeFunction SCALING
    //    The source data stores ~84 % of DPF values multiplied by 1000
    //    (e.g. 0.627 → 627).  Values > 2.5 are normalised back to [0,1].
    //    Clinical DPF range is 0.078 – 2.42 (Pima dataset).
    // ------------------------------------------------------------------
    FixDPF = Table.TransformColumns(
        AddPatientID,
        {
            {
                "DiabetesPedigreeFunction",
                each if _ > 2.5 then _ / 1000 else _,
                type number
            }
        }
    ),

    // ------------------------------------------------------------------
    // 6. REPLACE CLINICALLY IMPOSSIBLE ZEROS WITH NULL
    //    Zero is physiologically impossible for Glucose, BloodPressure,
    //    SkinThickness, Insulin, and BMI — treat as missing data.
    // ------------------------------------------------------------------
    NullifyZeroGlucose = Table.ReplaceValue(
        FixDPF, 0, null, Replacer.ReplaceValue, {"Glucose"}
    ),
    NullifyZeroBP = Table.ReplaceValue(
        NullifyZeroGlucose, 0, null, Replacer.ReplaceValue, {"BloodPressure"}
    ),
    NullifyZeroSkin = Table.ReplaceValue(
        NullifyZeroBP, 0, null, Replacer.ReplaceValue, {"SkinThickness"}
    ),
    NullifyZeroInsulin = Table.ReplaceValue(
        NullifyZeroSkin, 0, null, Replacer.ReplaceValue, {"Insulin"}
    ),
    NullifyZeroBMI = Table.ReplaceValue(
        NullifyZeroInsulin, 0, null, Replacer.ReplaceValue, {"BMI"}
    ),

    // ------------------------------------------------------------------
    // 7. IMPUTE MISSING VALUES WITH COLUMN MEDIAN
    //    Computed from non-null rows; applied back to null cells.
    // ------------------------------------------------------------------
    // --- Glucose median
    GlucoseMedian = List.Median(
        List.Select(Table.Column(NullifyZeroBMI, "Glucose"), each _ <> null)
    ),
    ImputeGlucose = Table.TransformColumns(
        NullifyZeroBMI,
        {{"Glucose", each if _ = null then GlucoseMedian else _, type number}}
    ),

    // --- BloodPressure median
    BPMedian = List.Median(
        List.Select(Table.Column(ImputeGlucose, "BloodPressure"), each _ <> null)
    ),
    ImputeBP = Table.TransformColumns(
        ImputeGlucose,
        {{"BloodPressure", each if _ = null then BPMedian else _, type number}}
    ),

    // --- SkinThickness median
    SkinMedian = List.Median(
        List.Select(Table.Column(ImputeBP, "SkinThickness"), each _ <> null)
    ),
    ImputeSkin = Table.TransformColumns(
        ImputeBP,
        {{"SkinThickness", each if _ = null then SkinMedian else _, type number}}
    ),

    // --- Insulin median
    InsulinMedian = List.Median(
        List.Select(Table.Column(ImputeSkin, "Insulin"), each _ <> null)
    ),
    ImputeInsulin = Table.TransformColumns(
        ImputeSkin,
        {{"Insulin", each if _ = null then InsulinMedian else _, type number}}
    ),

    // --- BMI median
    BMIMedian = List.Median(
        List.Select(Table.Column(ImputeInsulin, "BMI"), each _ <> null)
    ),
    ImputeBMI = Table.TransformColumns(
        ImputeInsulin,
        {{"BMI", each if _ = null then BMIMedian else _, type number}}
    ),

    // ------------------------------------------------------------------
    // 8. DERIVED COLUMN — AgeGroup  (5 cohorts)
    // ------------------------------------------------------------------
    AddAgeGroup = Table.AddColumn(
        ImputeBMI,
        "AgeGroup",
        each
            if      [Age] < 30 then "Under 30"
            else if [Age] < 40 then "30–39"
            else if [Age] < 50 then "40–49"
            else if [Age] < 60 then "50–59"
            else                    "60+",
        type text
    ),

    // ------------------------------------------------------------------
    // 9. DERIVED COLUMN — AgeGroupSort  (numeric sort key for AgeGroup)
    // ------------------------------------------------------------------
    AddAgeGroupSort = Table.AddColumn(
        AddAgeGroup,
        "AgeGroupSort",
        each
            if      [Age] < 30 then 1
            else if [Age] < 40 then 2
            else if [Age] < 50 then 3
            else if [Age] < 60 then 4
            else                    5,
        Int64.Type
    ),

    // ------------------------------------------------------------------
    // 10. DERIVED COLUMN — GlucoseCategory
    //     ADA thresholds: Normal <100, Pre-Diabetic 100–125, Diabetic ≥126
    // ------------------------------------------------------------------
    AddGlucoseCategory = Table.AddColumn(
        AddAgeGroupSort,
        "GlucoseCategory",
        each
            if      [Glucose] < 100 then "Normal"
            else if [Glucose] < 126 then "Pre-Diabetic"
            else                         "Diabetic Range",
        type text
    ),

    // ------------------------------------------------------------------
    // 11. DERIVED COLUMN — GlucoseCategorySort
    // ------------------------------------------------------------------
    AddGlucoseCategorySort = Table.AddColumn(
        AddGlucoseCategory,
        "GlucoseCategorySort",
        each
            if      [Glucose] < 100 then 1
            else if [Glucose] < 126 then 2
            else                         3,
        Int64.Type
    ),

    // ------------------------------------------------------------------
    // 12. DERIVED COLUMN — BMICategory  (WHO classification)
    // ------------------------------------------------------------------
    AddBMICategory = Table.AddColumn(
        AddGlucoseCategorySort,
        "BMICategory",
        each
            if      [BMI] < 18.5 then "Underweight"
            else if [BMI] < 25.0 then "Normal Weight"
            else if [BMI] < 30.0 then "Overweight"
            else if [BMI] < 35.0 then "Obese I"
            else if [BMI] < 40.0 then "Obese II"
            else                       "Obese III",
        type text
    ),

    // ------------------------------------------------------------------
    // 13. DERIVED COLUMN — BMICategorySort
    // ------------------------------------------------------------------
    AddBMICategorySort = Table.AddColumn(
        AddBMICategory,
        "BMICategorySort",
        each
            if      [BMI] < 18.5 then 1
            else if [BMI] < 25.0 then 2
            else if [BMI] < 30.0 then 3
            else if [BMI] < 35.0 then 4
            else if [BMI] < 40.0 then 5
            else                       6,
        Int64.Type
    ),

    // ------------------------------------------------------------------
    // 14. DERIVED COLUMN — BloodPressureCategory  (JNC-8 thresholds)
    // ------------------------------------------------------------------
    AddBPCategory = Table.AddColumn(
        AddBMICategorySort,
        "BloodPressureCategory",
        each
            if      [BloodPressure] < 80  then "Normal"
            else if [BloodPressure] < 90  then "Elevated"
            else if [BloodPressure] < 100 then "Stage 1 HTN"
            else                               "Stage 2 HTN",
        type text
    ),

    // ------------------------------------------------------------------
    // 15. DERIVED COLUMN — InsulinCategory
    //     Fasting insulin reference: 16–166 pmol/L (2-hour test)
    // ------------------------------------------------------------------
    AddInsulinCategory = Table.AddColumn(
        AddBPCategory,
        "InsulinCategory",
        each
            if      [Insulin] = 0   then "Not Measured"
            else if [Insulin] < 16  then "Low"
            else if [Insulin] <= 166 then "Normal"
            else                         "High",
        type text
    ),

    // ------------------------------------------------------------------
    // 16. DERIVED COLUMN — RiskScore  (0–100 composite)
    //     Points system based on clinical risk thresholds:
    //       Glucose ≥ 126        → +30 pts
    //       Glucose 100–125      → +15 pts
    //       BMI ≥ 35             → +20 pts
    //       BMI 30–34.9          → +10 pts
    //       Age ≥ 50             → +15 pts
    //       Age 40–49            → +8  pts
    //       Pregnancies ≥ 6      → +10 pts
    //       BP ≥ 90              → +10 pts
    //       DPF ≥ 0.5            → +10 pts
    //       Insulin > 166        → +5  pts
    //     Maximum raw score = 110; capped & normalised to 100.
    // ------------------------------------------------------------------
    AddRawScore = Table.AddColumn(
        AddInsulinCategory,
        "_RawScore",
        each
            (if [Glucose] >= 126 then 30 else if [Glucose] >= 100 then 15 else 0)
          + (if [BMI]     >= 35  then 20 else if [BMI]     >= 30  then 10 else 0)
          + (if [Age]     >= 50  then 15 else if [Age]     >= 40  then 8  else 0)
          + (if [Pregnancies] >= 6 then 10 else 0)
          + (if [BloodPressure] >= 90 then 10 else 0)
          + (if [DiabetesPedigreeFunction] >= 0.5 then 10 else 0)
          + (if [Insulin] > 166 then 5 else 0),
        Int64.Type
    ),

    AddRiskScore = Table.AddColumn(
        AddRawScore,
        "RiskScore",
        each Number.Round(List.Min({[_RawScore] / 110 * 100, 100}), 1),
        type number
    ),

    // ------------------------------------------------------------------
    // 17. DERIVED COLUMN — RiskCategory
    // ------------------------------------------------------------------
    AddRiskCategory = Table.AddColumn(
        AddRiskScore,
        "RiskCategory",
        each
            if      [RiskScore] >= 60 then "High Risk"
            else if [RiskScore] >= 30 then "Medium Risk"
            else                           "Low Risk",
        type text
    ),

    // ------------------------------------------------------------------
    // 18. DERIVED COLUMN — RiskCategorySort
    // ------------------------------------------------------------------
    AddRiskCategorySort = Table.AddColumn(
        AddRiskCategory,
        "RiskCategorySort",
        each
            if      [RiskScore] >= 60 then 3
            else if [RiskScore] >= 30 then 2
            else                           1,
        Int64.Type
    ),

    // ------------------------------------------------------------------
    // 19. DERIVED COLUMN — PregnancyGroup
    // ------------------------------------------------------------------
    AddPregnancyGroup = Table.AddColumn(
        AddRiskCategorySort,
        "PregnancyGroup",
        each
            if      [Pregnancies] = 0 then "None"
            else if [Pregnancies] <= 3 then "1–3"
            else if [Pregnancies] <= 6 then "4–6"
            else                            "7+",
        type text
    ),

    // ------------------------------------------------------------------
    // 20. REMOVE HELPER COLUMN
    // ------------------------------------------------------------------
    RemoveHelper = Table.RemoveColumns(AddPregnancyGroup, {"_RawScore"}),

    // ------------------------------------------------------------------
    // 21. REORDER COLUMNS for readability in Power BI
    // ------------------------------------------------------------------
    ReorderedCols = Table.ReorderColumns(
        RemoveHelper,
        {
            "PatientID",
            "Age",         "AgeGroup",         "AgeGroupSort",
            "Pregnancies", "PregnancyGroup",
            "Glucose",     "GlucoseCategory",  "GlucoseCategorySort",
            "BloodPressure", "BloodPressureCategory",
            "SkinThickness",
            "Insulin",     "InsulinCategory",
            "BMI",         "BMICategory",       "BMICategorySort",
            "DiabetesPedigreeFunction",
            "RiskScore",   "RiskCategory",      "RiskCategorySort"
        }
    )

in
    ReorderedCols
