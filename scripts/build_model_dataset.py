import csv
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]

PRIORITY_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "renovation_priority_by_county_2024.csv"
)

WEATHER_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "weather_by_county_2024.csv"
)

OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "model_dataset_county_2024.csv"
)


def read_csv(file_path):
    with file_path.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


print("Reading renovation priority data...")
priority_rows = read_csv(PRIORITY_FILE)

print("Reading weather data...")
weather_rows = read_csv(WEATHER_FILE)


weather_by_county = {
    row["County"].strip().upper(): row
    for row in weather_rows
}

combined_rows = []
missing_weather = []


for priority_row in priority_rows:
    county = priority_row["County"].strip()
    county_key = county.upper()

    weather_row = weather_by_county.get(county_key)

    if weather_row is None:
        missing_weather.append(county)
        continue

    rainfall_value = weather_row.get(
        "Annual Rainfall (mm)",
        weather_row.get("AnnualRainfall (mm)", ""),
    )

    combined_rows.append(
        {
            "Year": 2024,
            "County": county,
            "Vacancy Quarter": priority_row[
                "Vacancy Quarter"
            ],
            "Vacancy Rate (%)": priority_row[
                "Vacancy Rate (%)"
            ],
            "Poor BER (%)": priority_row[
                "Poor BER (%)"
            ],
            "Annual Mean Temperature (C)": weather_row[
                "Annual Mean Temperature (C)"
            ],
            "Annual Mean Minimum Temperature (C)": (
                weather_row[
                    "Annual Mean Minimum Temperature (C)"
                ]
            ),
            "Annual Mean Maximum Temperature (C)": (
                weather_row[
                    "Annual Mean Maximum Temperature (C)"
                ]
            ),
            "Annual Rainfall (mm)": rainfall_value,
            "Heating Degree Days (Base 15.5C)": weather_row[
                "Estimated Heating Degree Days (Base 15.5C)"
            ],
            "Vacancy Component (0-100)": priority_row[
                "Vacancy Component (0-100)"
            ],
            "BER Component (0-100)": priority_row[
                "BER Component (0-100)"
            ],
            "Renovation Priority Score": priority_row[
                "Renovation Priority Score"
            ],
            "Priority Rank": priority_row[
                "Priority Rank"
            ],
        }
    )


if missing_weather:
    print(
        "Counties missing weather data:",
        ", ".join(missing_weather),
    )


fieldnames = [
    "Year",
    "County",
    "Vacancy Quarter",
    "Vacancy Rate (%)",
    "Poor BER (%)",
    "Annual Mean Temperature (C)",
    "Annual Mean Minimum Temperature (C)",
    "Annual Mean Maximum Temperature (C)",
    "Annual Rainfall (mm)",
    "Heating Degree Days (Base 15.5C)",
    "Vacancy Component (0-100)",
    "BER Component (0-100)",
    "Renovation Priority Score",
    "Priority Rank",
]

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

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
    writer.writerows(combined_rows)


print(f"Counties combined: {len(combined_rows)}")
print(f"Model dataset created: {OUTPUT_FILE}")