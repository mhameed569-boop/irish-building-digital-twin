"""Validate public research datasets and report problems without dropping rows."""

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_FOLDER / "data" / "processed"
REPORT_TXT = PROJECT_FOLDER / "outputs" / "data_quality_report.txt"
REPORT_CSV = PROJECT_FOLDER / "outputs" / "data_quality_report.csv"

DATASETS = [
    ("county_final", PROCESSED / "final_model_dataset_county_2024.csv", "County", 26),
    (
        "small_area_census",
        PROCESSED / "census_demographic_features_small_area_2022.csv",
        "small_area_guid",
        18919,
    ),
    (
        "small_area_spatial",
        PROCESSED / "spatial_features_small_area.csv",
        "small_area_guid",
        18919,
    ),
    (
        "small_area_model",
        PROCESSED / "spatial_model_features_small_area.csv",
        "small_area_guid",
        18919,
    ),
]


def numeric(value):
    if value is None or value.strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def add(results, severity, dataset, check, status, details):
    results.append(
        {
            "severity": severity,
            "dataset": dataset,
            "check": check,
            "status": status,
            "details": details,
        }
    )


def validate_dataset(name, path, id_field, expected_rows, results):
    if not path.exists():
        add(results, "ERROR", name, "file_exists", "FAIL", str(path))
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    add(
        results,
        "ERROR" if len(rows) != expected_rows else "INFO",
        name,
        "expected_geographic_unit_count",
        "PASS" if len(rows) == expected_rows else "FAIL",
        f"expected={expected_rows}; observed={len(rows)}",
    )

    identifiers = [row.get(id_field, "") for row in rows]
    duplicate_count = sum(count - 1 for count in Counter(identifiers).values() if count > 1)
    add(
        results,
        "ERROR" if duplicate_count else "INFO",
        name,
        "duplicate_geographic_ids",
        "FAIL" if duplicate_count else "PASS",
        f"duplicates={duplicate_count}",
    )

    missing = {field: sum(row.get(field, "").strip() == "" for row in rows) for field in rows[0]}
    missing = {field: count for field, count in missing.items() if count}
    add(
        results,
        "WARNING" if missing else "INFO",
        name,
        "missing_values",
        "WARN" if missing else "PASS",
        "; ".join(f"{field}={count}" for field, count in missing.items()) or "none",
    )

    percentage_fields = [
        field
        for field in rows[0]
        if "pct" in field.lower() or "(%)" in field or "share (%)" in field.lower()
    ]
    invalid_percentages = 0
    for field in percentage_fields:
        invalid_percentages += sum(
            value is not None and not 0 <= value <= 100
            for value in (numeric(row[field]) for row in rows)
        )
    add(
        results,
        "ERROR" if invalid_percentages else "INFO",
        name,
        "percentage_range_0_100",
        "FAIL" if invalid_percentages else "PASS",
        f"invalid_values={invalid_percentages}",
    )

    count_fields = [
        field
        for field in rows[0]
        if any(word in field.lower() for word in ["population", "household", "dwelling", "housing stock"])
        and "pct" not in field.lower()
        and "density" not in field.lower()
    ]
    negative_counts = sum(
        value is not None and value < 0
        for field in count_fields
        for value in (numeric(row[field]) for row in rows)
    )
    add(
        results,
        "ERROR" if negative_counts else "INFO",
        name,
        "negative_counts",
        "FAIL" if negative_counts else "PASS",
        f"negative_values={negative_counts}",
    )

    signatures = defaultdict(list)
    for field in rows[0]:
        digest = hashlib.sha256("\x1f".join(row[field] for row in rows).encode("utf-8")).hexdigest()
        signatures[digest].append(field)
    duplicates = [fields for fields in signatures.values() if len(fields) > 1]
    add(
        results,
        "WARNING" if duplicates else "INFO",
        name,
        "exact_duplicate_variables",
        "WARN" if duplicates else "PASS",
        str(duplicates) if duplicates else "none",
    )

    near_zero = []
    for field in rows[0]:
        values = [row[field] for row in rows if row[field] != ""]
        if values and Counter(values).most_common(1)[0][1] / len(values) >= 0.99:
            near_zero.append(field)
    add(
        results,
        "WARNING" if near_zero else "INFO",
        name,
        "near_zero_variance",
        "WARN" if near_zero else "PASS",
        ", ".join(near_zero) or "none",
    )
    return rows


def main():
    results = []
    loaded = {}
    for name, path, id_field, expected_rows in DATASETS:
        loaded[name] = validate_dataset(name, path, id_field, expected_rows, results)

    county = loaded.get("county_final", [])
    apartment_errors = sum(
        abs(
            float(row["Apartment Dwellings"])
            - float(row["Purpose-Built Apartments"])
            - float(row["Converted Apartments"])
        )
        > 0.001
        for row in read_optional(PROCESSED / "census_housing_by_county_2022.csv")
    )
    dependency_errors = sum(
        abs(float(row["Pre-2000 (%)"]) - float(row["Pre-1978 (%)"]) - float(row["1978-1999 (%)"]))
        > 0.011
        for row in county
    )
    add(
        results,
        "ERROR" if apartment_errors else "INFO",
        "county_final",
        "apartment_count_dependency",
        "FAIL" if apartment_errors else "PASS",
        f"inconsistent_rows={apartment_errors}",
    )
    add(
        results,
        "WARNING",
        "county_final",
        "pre_2000_exact_dependency",
        "DOCUMENTED",
        f"inconsistent_rows={dependency_errors}; exclude one representation from regression",
    )

    small = loaded.get("small_area_census", [])
    total_errors = sum(
        abs(
            float(row["total_housing_stock"])
            - float(row["occupied_dwellings"])
            - float(row["temporarily_absent_dwellings"])
            - float(row["holiday_homes"])
            - float(row["other_vacant_dwellings"])
        )
        > 0.001
        for row in small
    )
    add(
        results,
        "ERROR" if total_errors else "INFO",
        "small_area_census",
        "housing_stock_component_total",
        "FAIL" if total_errors else "PASS",
        f"inconsistent_rows={total_errors}",
    )

    spatial = loaded.get("small_area_spatial", [])
    bad_coordinates = sum(
        not (-10.8 <= float(row["centroid_longitude"]) <= -5.3)
        or not (51.3 <= float(row["centroid_latitude"]) <= 55.5)
        for row in spatial
    )
    add(
        results,
        "ERROR" if bad_coordinates else "INFO",
        "small_area_spatial",
        "coordinate_validity_ireland",
        "FAIL" if bad_coordinates else "PASS",
        f"invalid_coordinates={bad_coordinates}",
    )

    expected_years = {
        "Analysis Year": {"2024"},
        "Census Year": {"2022"},
        "census_reference_year": {"2022"},
        "weather_reference_year": {"2024"},
        "ber_reference_year": {"2024"},
    }
    for name, rows in loaded.items():
        for field, expected in expected_years.items():
            if rows and field in rows[0]:
                observed = {row[field] for row in rows}
                add(
                    results,
                    "ERROR" if observed != expected else "INFO",
                    name,
                    f"expected_year_{field}",
                    "PASS" if observed == expected else "FAIL",
                    f"expected={sorted(expected)}; observed={sorted(observed)}",
                )

    add(
        results,
        "BLOCKER",
        "small_area_model",
        "actual_energy_consumption_target",
        "NOT_AVAILABLE_PUBLICLY",
        "Must be integrated inside the authorised CSO Researcher Data Portal; BER is not a substitute.",
    )

    REPORT_TXT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_CSV.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    with REPORT_TXT.open("w", encoding="utf-8") as file:
        file.write("Research data quality report\n")
        file.write("=" * 80 + "\n")
        for result in results:
            file.write(
                f"[{result['severity']}] {result['dataset']} :: {result['check']} :: "
                f"{result['status']}\n  {result['details']}\n"
            )
    print(f"Checks written: {len(results)}")
    print(f"Created: {REPORT_TXT}")
    print(f"Created: {REPORT_CSV}")


def read_optional(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


if __name__ == "__main__":
    main()
