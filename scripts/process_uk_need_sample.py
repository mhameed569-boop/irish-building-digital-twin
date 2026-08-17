"""Prepare a harmonised public UK NEED transfer-learning sample."""

import csv
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
INPUT_FILE = (
    PROJECT_FOLDER / "data" / "raw" / "international" / "uk_need_2025_50k.csv"
)
OUTPUT_FILE = (
    PROJECT_FOLDER / "data" / "interim" / "uk_need_transfer_features_2023.csv"
)

AGE_LABELS = {"1": "Before 1930", "2": "1930-1972", "3": "1973-1999", "4": "2000 or later"}
FLOOR_LABELS = {
    "1": "50 or less",
    "2": "51-100",
    "3": "101-150",
    "4": "151-200",
    "5": "Over 200",
}


def valid_consumption(row, value_field, flag_field):
    value = row[value_field].strip()
    return float(value) if row[flag_field] == "V" and value else None


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        for source in csv.DictReader(file):
            electricity = valid_consumption(source, "Econs2023", "ElecValFlag2023")
            gas = valid_consumption(source, "Gcons2023", "GasValFlag2023")
            if electricity is None:
                continue
            rows.append(
                {
                    "country": "United Kingdom",
                    "source_dataset": "DESNZ NEED anonymised data 2025 (50k sample)",
                    "energy_reference_year": 2023,
                    "property_type": source["PROP_TYPE"],
                    "construction_age_band": AGE_LABELS.get(
                        source["PROP_AGE_BAND"], source["PROP_AGE_BAND"]
                    ),
                    "floor_area_band_m2": FLOOR_LABELS.get(
                        source["FLOOR_AREA_BAND"], source["FLOOR_AREA_BAND"]
                    ),
                    "region_code": source["REGION"],
                    "energy_rating_band": source["EPC"],
                    "main_heating_fuel": (
                        "Gas" if source["MAIN_HEAT_FUEL"] == "1" else "Not gas"
                    ),
                    "photovoltaic_flag": source["PV_FLAG"],
                    "loft_insulation_flag": source["LI_FLAG"],
                    "cavity_wall_insulation_flag": source["CWI_FLAG"],
                    "actual_electricity_kwh": electricity,
                    "weather_corrected_gas_kwh": gas if gas is not None else "",
                    "combined_metered_energy_kwh": electricity + gas
                    if gas is not None
                    else "",
                    "electricity_validity_flag": source["ElecValFlag2023"],
                    "gas_validity_flag": source["GasValFlag2023"],
                }
            )

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Valid electricity observations: {len(rows):,}")
    print(f"Created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
