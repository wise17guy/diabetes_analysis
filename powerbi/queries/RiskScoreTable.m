// ============================================================
// Query Name : RiskScoreTable
// Purpose    : Produce a summary table of patient counts and
//              average clinical metrics grouped by RiskCategory.
//              Used as a helper for summary visuals and tooltips.
// Dependency : DiabetesData query must exist first.
// ============================================================

let
    // Reference the cleaned DiabetesData query (no data duplication)
    Source = DiabetesData,

    // Group by RiskCategory
    Grouped = Table.Group(
        Source,
        {"RiskCategory", "RiskCategorySort"},
        {
            {"PatientCount",     each Table.RowCount(_),                             Int64.Type},
            {"AvgAge",           each List.Average(List.Select([Age],           each _ <> null)), type number},
            {"AvgGlucose",       each List.Average(List.Select([Glucose],       each _ <> null)), type number},
            {"AvgBMI",           each List.Average(List.Select([BMI],           each _ <> null)), type number},
            {"AvgBloodPressure", each List.Average(List.Select([BloodPressure], each _ <> null)), type number},
            {"AvgDPF",           each List.Average(List.Select([DiabetesPedigreeFunction], each _ <> null)), type number},
            {"AvgRiskScore",     each List.Average(List.Select([RiskScore],     each _ <> null)), type number}
        }
    ),

    // Round averages for cleaner display
    RoundedAverages = Table.TransformColumns(
        Grouped,
        {
            {"AvgAge",           each Number.Round(_, 1), type number},
            {"AvgGlucose",       each Number.Round(_, 1), type number},
            {"AvgBMI",           each Number.Round(_, 2), type number},
            {"AvgBloodPressure", each Number.Round(_, 1), type number},
            {"AvgDPF",           each Number.Round(_, 3), type number},
            {"AvgRiskScore",     each Number.Round(_, 1), type number}
        }
    ),

    // Sort by risk level (Low → Medium → High)
    Sorted = Table.Sort(RoundedAverages, {{"RiskCategorySort", Order.Ascending}}),

    // Add % share column
    TotalPatients = List.Sum(Sorted[PatientCount]),
    AddPctShare = Table.AddColumn(
        Sorted,
        "PctShare",
        each Number.Round([PatientCount] / TotalPatients * 100, 1),
        type number
    )

in
    AddPctShare
