"""Build the public Small Area feature table without fabricating a target."""

import csv
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_FOLDER / "data" / "processed"
CENSUS_FILE = PROCESSED / "census_demographic_features_small_area_2022.csv"
SPATIAL_FILE = PROCESSED / "spatial_features_small_area.csv"
WEATHER_FILE = PROCESSED / "weather_by_county_2024.csv"
BER_FILE = PROCESSED / "ber_by_county_2024.csv"
PRIORITY_FILE = PROCESSED / "renovation_priority_by_county_2024.csv"
OUTPUT_FILE = PROCESSED / "spatial_model_features_small_area.csv"


def read_rows(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def model_county(name):
    name = name.strip().upper()
    if name in {"DUBLIN CITY", "DUN LAOGHAIRE/RATHDOWN", "FINGAL", "SOUTH DUBLIN"}:
        return "DUBLIN"
    if name in {"GALWAY", "GALWAY CITY"}:
        return "GALWAY"
    if name in {"CORK", "CORK CITY"}:
        return "CORK"
    if name in {"LIMERICK", "LIMERICK CITY"}:
        return "LIMERICK"
    if name in {"WATERFORD", "WATERFORD CITY"}:
        return "WATERFORD"
    if name in {"NORTH TIPPERARY", "SOUTH TIPPERARY"}:
        return "TIPPERARY"
    return name


def keyed(rows, field="County"):
    return {row[field].strip().upper(): row for row in rows}


def main():
    census_rows = read_rows(CENSUS_FILE)
    spatial_rows = read_rows(SPATIAL_FILE)
    census_by_guid = {row["small_area_guid"]: row for row in census_rows}
    weather = keyed(read_rows(WEATHER_FILE))
    ber = keyed(read_rows(BER_FILE))
    priority = keyed(read_rows(PRIORITY_FILE))

    final_rows = []
    failed = []
    for spatial in spatial_rows:
        guid = spatial["small_area_guid"]
        census = census_by_guid.get(guid)
        county_key = model_county(spatial["county_name"])
        weather_row = weather.get(county_key)
        ber_row = ber.get(county_key)
        priority_row = priority.get(county_key)
        if not all([census, weather_row, ber_row, priority_row]):
            failed.append(guid)
            continue

        row = dict(spatial)
        for key, value in census.items():
            if key not in {
                "census_year",
                "small_area_guid",
                "small_area_code",
                "urban_rural_code",
                "urban_rural_class",
            }:
                row[key] = value
        row.update(
            {
                "urban_rural_code": census["urban_rural_code"],
                "urban_rural_class": census["urban_rural_class"],
                "county_model_name": county_key.title(),
                "census_reference_year": 2022,
                "weather_reference_year": weather_row["Year"],
                "ber_reference_year": ber_row["Year"],
                "vacancy_reference_quarter": priority_row["Vacancy Quarter"],
                "county_mean_temperature_c": weather_row[
                    "Annual Mean Temperature (C)"
                ],
                "county_annual_rainfall_mm": weather_row["Annual Rainfall (mm)"],
                "county_heating_degree_days_base_15_5c": weather_row[
                    "Estimated Heating Degree Days (Base 15.5C)"
                ],
                "county_poor_ber_pct": ber_row["Poor BER (%)"],
                "county_ber_sample_dwellings": ber_row["Total BER Dwellings"],
                "county_vacancy_rate_pct": priority_row["Vacancy Rate (%)"],
                "county_renovation_priority_score": priority_row[
                    "Renovation Priority Score"
                ],
            }
        )
        final_rows.append(row)

    if not final_rows:
        raise RuntimeError("No Small Area rows were integrated.")
    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(final_rows[0]))
        writer.writeheader()
        writer.writerows(final_rows)

    print(f"Small Area observations: {len(final_rows):,}")
    print(f"Failed joins: {len(failed):,}")
    print("Actual energy consumption target: NOT AVAILABLE PUBLICLY")
    print(f"Created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
