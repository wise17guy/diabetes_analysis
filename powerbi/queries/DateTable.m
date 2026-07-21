// ============================================================
// Query Name : DateTable
// Purpose    : Standalone calendar / date dimension table.
//              Although this dataset has no date column, this
//              table enables time-intelligence DAX functions
//              and allows you to add a "Report Date" slicer if
//              the source is later enriched with timestamps.
//
//              Range: 2000-01-01 → 2030-12-31
// ============================================================

let
    // ------------------------------------------------------------------
    // 1. Generate a list of every date in the range
    // ------------------------------------------------------------------
    StartDate   = #date(2000, 1, 1),
    EndDate     = #date(2030, 12, 31),
    DayCount    = Duration.TotalDays(EndDate - StartDate) + 1,
    DateList    = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),

    // ------------------------------------------------------------------
    // 2. Convert list to a single-column table
    // ------------------------------------------------------------------
    DateTable   = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}),
    TypedDate   = Table.TransformColumnTypes(DateTable, {{"Date", type date}}),

    // ------------------------------------------------------------------
    // 3. Add calendar columns
    // ------------------------------------------------------------------
    AddYear = Table.AddColumn(
        TypedDate, "Year", each Date.Year([Date]), Int64.Type
    ),
    AddQuarterNum = Table.AddColumn(
        AddYear, "QuarterNum", each Date.QuarterOfYear([Date]), Int64.Type
    ),
    AddQuarterLabel = Table.AddColumn(
        AddQuarterNum, "Quarter",
        each "Q" & Text.From([QuarterNum]), type text
    ),
    AddYearQuarter = Table.AddColumn(
        AddQuarterLabel, "YearQuarter",
        each Text.From([Year]) & " Q" & Text.From([QuarterNum]), type text
    ),
    AddMonthNum = Table.AddColumn(
        AddYearQuarter, "MonthNum", each Date.Month([Date]), Int64.Type
    ),
    AddMonthName = Table.AddColumn(
        AddMonthNum, "MonthName",
        each Date.ToText([Date], "MMMM"), type text
    ),
    AddMonthShort = Table.AddColumn(
        AddMonthName, "MonthShort",
        each Date.ToText([Date], "MMM"), type text
    ),
    AddYearMonth = Table.AddColumn(
        AddMonthShort, "YearMonth",
        each Text.From([Year]) & "-" & Text.PadStart(Text.From([MonthNum]), 2, "0"), type text
    ),
    AddWeekNum = Table.AddColumn(
        AddYearMonth, "WeekNum", each Date.WeekOfYear([Date]), Int64.Type
    ),
    AddDayOfWeekNum = Table.AddColumn(
        AddWeekNum, "DayOfWeekNum", each Date.DayOfWeek([Date], Day.Monday) + 1, Int64.Type
    ),
    AddDayOfWeekName = Table.AddColumn(
        AddDayOfWeekNum, "DayOfWeekName",
        each Date.ToText([Date], "dddd"), type text
    ),
    AddDayShort = Table.AddColumn(
        AddDayOfWeekName, "DayShort",
        each Date.ToText([Date], "ddd"), type text
    ),
    AddIsWeekend = Table.AddColumn(
        AddDayShort, "IsWeekend",
        each [DayOfWeekNum] >= 6, type logical
    ),
    AddIsCurrentYear = Table.AddColumn(
        AddIsWeekend, "IsCurrentYear",
        each [Year] = Date.Year(DateTime.LocalNow()), type logical
    ),

    // ------------------------------------------------------------------
    // 4. Final column reorder
    // ------------------------------------------------------------------
    ReorderedCols = Table.ReorderColumns(
        AddIsCurrentYear,
        {
            "Date", "Year", "QuarterNum", "Quarter", "YearQuarter",
            "MonthNum", "MonthName", "MonthShort", "YearMonth",
            "WeekNum", "DayOfWeekNum", "DayOfWeekName", "DayShort",
            "IsWeekend", "IsCurrentYear"
        }
    )

in
    ReorderedCols
