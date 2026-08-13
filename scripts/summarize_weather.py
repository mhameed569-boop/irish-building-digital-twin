import calendar
import csv
from collections import defaultdict
from pathlib import Path


TARGET_YEAR = 2024
HEATING_BASE_TEMPERATURE = 15.5

PROJECT_FOLDER = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "met_eireann_county_weather.csv"
)

PRIORITY_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "renovation_priority_by_county_2024.csv"
)

OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "weather_by_county_2024.csv"
)


print("Reading Met Eireann weather data...")

with PRIORITY_FILE.open(
    mode="r",
    encoding="utf-8-sig",
    newline="",
) as file:
    priority_rows = list(csv.DictReader(file))

valid_counties = {
    row["County"].strip()
    for row in priority_rows
}


weather_by_county = defaultdict(
    lambda: defaultdict(dict)
)

with INPUT_FILE.open(
    mode="r",
    encoding="utf-8-sig",
    newline="",
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        year = int(row["year"])
        county = row["region"].strip()

        if year != TARGET_YEAR:
            continue

        if county not in valid_counties:
            continue

        month = int(row["month"])
        measurement = row["measurement_type"]
        value = float(row["value"])

        weather_by_county[county][measurement][month] = value


processed_rows = []

for county in sorted(weather_by_county):
    measurements = weather_by_county[county]

    mean_temperatures = measurements.get("meanTa", {})
    minimum_temperatures = measurements.get("minTa", {})
    maximum_temperatures = measurements.get("maxTa", {})
    rainfall = measurements.get("rain", {})

    available_months = sorted(mean_temperatures)

    if not available_months:
        continue

    total_days = sum(
        calendar.monthrange(TARGET_YEAR, month)[1]
        for month in available_months
    )

    annual_mean_temperature = sum(
        mean_temperatures[month]
        * calendar.monthrange(TARGET_YEAR, month)[1]
        for month in available_months
    ) / total_days

    annual_minimum_temperature = sum(
        minimum_temperatures[month]
        * calendar.monthrange(TARGET_YEAR, month)[1]
        for month in available_months
    ) / total_days

    annual_maximum_temperature = sum(
        maximum_temperatures[month]
        * calendar.monthrange(TARGET_YEAR, month)[1]
        for month in available_months
    ) / total_days

    annual_rainfall = sum(rainfall.values())

    heating_degree_days = sum(
        max(
            HEATING_BASE_TEMPERATURE
            - mean_temperatures[month],
            0,
        )
        * calendar.monthrange(TARGET_YEAR, month)[1]
        for month in available_months
    )

    processed_rows.append(
        {
            "Year": TARGET_YEAR,
            "County": county,
            "Months Available": len(available_months),
            "Annual Mean Temperature (C)": round(
                annual_mean_temperature,
                2,
            ),
            "Annual Mean Minimum Temperature (C)": round(
                annual_minimum_temperature,
                2,
            ),
            "Annual Mean Maximum Temperature (C)": round(
                annual_maximum_temperature,
                2,
            ),
            "Annual Rainfall (mm)": round(
                annual_rainfall,
                2,
            ),
            "Estimated Heating Degree Days (Base 15.5C)": round(
                heating_degree_days,
                2,
            ),
        }
    )


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

fieldnames = [
    "Year",
    "County",
    "Months Available",
    "Annual Mean Temperature (C)",
    "Annual Mean Minimum Temperature (C)",
    "Annual Mean Maximum Temperature (C)",
    "Annual Rainfall (mm)",
    "Estimated Heating Degree Days (Base 15.5C)",
]

with OUTPUT_FILE.open(
    mode="w",
    encoding="utf-8-sig",
    newline="",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames,
    )

    writer.writeheader()
    writer.writerows(processed_rows)


print(f"Counties processed: {len(processed_rows)}")
print(f"Processed file created: {OUTPUT_FILE}")