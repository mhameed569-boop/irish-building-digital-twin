"""Assess public Small Area features for future spatial ML."""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "spatial_model_features_small_area.csv"
NEIGHBORS = ROOT / "data" / "processed" / "small_area_neighbors.csv"
OUTPUT = ROOT / "outputs" / "ml_readiness_report.md"


def numeric(value):
    try:
        float(value)
        return value.strip() != ""
    except (TypeError, ValueError):
        return False


def main():
    with DATA.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    columns = list(rows[0])
    identifiers = {c for c in columns if c.endswith("_id") or "guid" in c or "code" in c or c.endswith("_year") or c == "census_year"}
    categorical = []
    continuous = []
    missing = {}
    constant = []
    for column in columns:
        values = [row[column].strip() for row in rows]
        blanks = sum(not value for value in values)
        if blanks:
            missing[column] = blanks
        nonblank = [value for value in values if value]
        if len(set(nonblank)) <= 1:
            constant.append(column)
        elif nonblank and sum(numeric(value) for value in nonblank) / len(nonblank) > 0.95:
            continuous.append(column)
        else:
            categorical.append(column)
    predictors = [c for c in columns if c not in identifiers and c not in {"county_name", "county_model_name", "urban_area_name", "electoral_division_name", "nuts1_name", "nuts2_name", "nuts3_name", "vacancy_reference_quarter"}]
    neighbor_count = 0
    if NEIGHBORS.exists():
        with NEIGHBORS.open("r", encoding="utf-8-sig", newline="") as file:
            neighbor_count = sum(1 for _ in file) - 1

    exact_redundancies = [
        "census_year = census_reference_year",
        "weather_reference_year = ber_reference_year in the current snapshot",
        "counts and their derived percentage variables must not be entered together without feature selection",
        "county context repeats across Small Areas and must not be treated as fine-resolution measurements",
    ]
    missing_lines = "\n".join(f"- `{key}`: {value:,} missing" for key, value in sorted(missing.items())) or "- None"
    redundant_lines = "\n".join(f"- {item}" for item in exact_redundancies)
    report = f"""# Machine-learning readiness assessment

Generated from `{DATA.relative_to(ROOT)}`.

## Dataset profile

- Geographic resolution: Census 2022 Small Area
- Observations: {len(rows):,}
- Columns: {len(columns):,}
- Candidate predictors before formal feature selection: {len(predictors):,}
- Continuous/numeric-like columns: {len(continuous):,}
- Categorical columns: {len(categorical):,}
- Directed neighbour links: {neighbor_count:,}
- Actual metered-energy target: **NOT AVAILABLE IN THE PUBLIC DATASET**

## Missingness

{missing_lines}

Blank `urban_area_name` values are expected outside named urban areas. Three Small Areas have zero denominators for several percentages; they remain reported and were not silently removed.

## Redundancy and multicollinearity risks

{redundant_lines}

Constant/reference fields to exclude from model matrices: {', '.join(f'`{c}`' for c in constant)}.

## Readiness by method

| Method | Status | Reason |
|---|---|---|
| Random Forest | CONDITIONAL | Predictor matrix is adequate, but the authorised actual-energy target must first be joined and spatial leakage controlled. |
| XGBoost | CONDITIONAL | Same target requirement; encode categorical fields and use grouped/spatial validation. |
| MLP | NOT READY | No public target; scaling, encoding, feature reduction, and sufficient linked records are still required. |
| MGWR | CONDITIONAL | Coordinates, fine geography and neighbours exist; a continuous authorised target and multicollinearity screening are required. |
| Spatial holdout validation | READY FOR DESIGN | Official IDs, centroids and adjacency are available; define geographically separated folds after target linkage. |

## Decision

The repository is ready for **public-data feature engineering and unsupervised/exploratory spatial analysis**, but not for supervised prediction of actual residential consumption. Phase 1 supervised Spatial ML begins only after authorised COP-BER/BER Energy data are processed within the CSO Researcher Data Portal and an approved, linkable analysis table is available.
"""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(report, encoding="utf-8")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
