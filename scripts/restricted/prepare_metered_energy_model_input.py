"""Prepare authorised metered-energy data inside a secure environment only.

This template never downloads, uploads, or embeds credentials. Record-level input
must remain in the authorised CSO Researcher Data Portal. By default it writes
only a validation report; an aggregate CSV is produced only when explicitly
requested and must still pass the disclosure-control process.
"""

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


REQUIRED = {
    "geography_id",
    "reference_period",
    "electricity_kwh",
}
OPTIONAL_NUMERIC = {"gas_kwh", "floor_area_m2", "ber_primary_energy_kwh_m2_year"}


def number(value):
    if value is None or str(value).strip() == "":
        return None
    return float(value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--secure-input", required=True, type=Path)
    parser.add_argument("--validation-report", required=True, type=Path)
    parser.add_argument("--approved-aggregate-output", type=Path)
    parser.add_argument("--minimum-cell-count", type=int, default=10)
    args = parser.parse_args()

    if not args.secure_input.is_file():
        raise FileNotFoundError(args.secure_input)
    if args.minimum_cell_count < 10:
        raise ValueError("minimum-cell-count must be at least 10")

    counts = defaultdict(int)
    totals = defaultdict(lambda: [0.0, 0.0])
    problems = []
    rows_read = 0
    with args.secure_input.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        for line_number, row in enumerate(reader, 2):
            rows_read += 1
            try:
                electricity = number(row["electricity_kwh"])
                gas = number(row.get("gas_kwh"))
                for field in OPTIONAL_NUMERIC:
                    value = number(row.get(field))
                    if value is not None and value < 0:
                        problems.append(f"line {line_number}: negative {field}")
                if electricity is None or electricity < 0:
                    problems.append(f"line {line_number}: invalid electricity_kwh")
                    continue
                if gas is not None and gas < 0:
                    problems.append(f"line {line_number}: negative gas_kwh")
                    continue
                key = (row["geography_id"].strip(), row["reference_period"].strip())
                if not all(key):
                    problems.append(f"line {line_number}: blank aggregation key")
                    continue
                counts[key] += 1
                totals[key][0] += electricity
                totals[key][1] += gas or 0.0
            except ValueError as exc:
                problems.append(f"line {line_number}: {exc}")

    report = {
        "input": str(args.secure_input),
        "rows_read": rows_read,
        "candidate_aggregate_cells": len(counts),
        "validation_problem_count": len(problems),
        "first_100_problems": problems[:100],
        "warning": "Run and retain record-level files only inside the authorised secure environment.",
    }
    args.validation_report.parent.mkdir(parents=True, exist_ok=True)
    args.validation_report.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if args.approved_aggregate_output:
        args.approved_aggregate_output.parent.mkdir(parents=True, exist_ok=True)
        with args.approved_aggregate_output.open("w", encoding="utf-8", newline="") as file:
            fields = ["geography_id", "reference_period", "dwelling_count", "mean_electricity_kwh", "mean_gas_kwh"]
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for key in sorted(counts):
                count = counts[key]
                if count < args.minimum_cell_count:
                    continue
                writer.writerow({
                    "geography_id": key[0],
                    "reference_period": key[1],
                    "dwelling_count": count,
                    "mean_electricity_kwh": round(totals[key][0] / count, 2),
                    "mean_gas_kwh": round(totals[key][1] / count, 2),
                })
        print("Aggregate candidate created; CSO disclosure approval is still required.")
    print(f"Validation report: {args.validation_report}")


if __name__ == "__main__":
    main()
