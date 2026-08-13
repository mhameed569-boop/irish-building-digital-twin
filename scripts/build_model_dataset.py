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

CENSUS_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "census_housing_by_county_2022.csv"
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

print("Reading Census housing data...")
census_rows = read_csv(CENSUS_FILE)


weather_by_county = {
    row["County"].strip().upper(): row
    for row in weather_rows
}

census_by_county = {
    row["County"].strip().upper(): row
    for row in census_rows
}


combined_rows = []
missing_data = []


for priority_row in priority_rows:
    county = priority_row["County"].strip()
    county_key = county.upper()

    weather_row = weather_by_county.get(county_key)
    census_row = census_by_county.get(county_key)

    if weather_row is None or census_row is None:
        missing_data.append(county)
        continue

    rainfall_value = weather_row.get(
        "Annual Rainfall (mm)",
        weather_row.get("AnnualRainfall (mm)", ""),
    )

    total_housing_stock = float(
        census_row["Total Housing Stock"]
    )

    apartment_dwellings = float(
        census_row["Apartment Dwellings"]
    )

    apartment_share = (
        apartment_dwellings
        / total_housing_stock
        * 100
        if total_housing_stock
        else 0
    )

    combined_rows.append(
        {
            "Analysis Year": 2024,
            "County": county,
            "Vacancy Quarter": priority_row[
                "Vacancy Quarter"
            ],
            "Census Year": census_row[
                "Census Year"
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
            "Total Housing Stock": census_row[
                "Total Housing Stock"
            ],
            "Occupied Dwellings": census_row[
                "Occupied Dwellings"
            ],
            "Census Vacant Dwellings": census_row[
                "Vacant Dwellings"
            ],
            "Holiday Homes": census_row[
                "Holiday Homes"
            ],
            "Census Vacant Share (%)": census_row[
                "Vacant Share of Housing Stock (%)"
            ],
            "Detached Houses": census_row[
                "Detached Houses"
            ],
            "Semi-Detached Houses": census_row[
                "Semi-Detached Houses"
            ],
            "Terraced Houses": census_row[
                "Terraced Houses"
            ],
            "Apartment Dwellings": census_row[
                "Apartment Dwellings"
            ],
            "Apartment Share (%)": round(
                apartment_share,
                2,
            ),
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


if missing_data:
    print(
        "Counties missing source data:",
        ", ".join(missing_data),
    )


fieldnames = [
    "Analysis Year",
    "County",
    "Vacancy Quarter",
    "Census Year",
    "Vacancy Rate (%)",
    "Poor BER (%)",
    "Annual Mean Temperature (C)",
    "Annual Mean Minimum Temperature (C)",
    "Annual Mean Maximum Temperature (C)",
    "Annual Rainfall (mm)",
    "Heating Degree Days (Base 15.5C)",
    "Total Housing Stock",
    "Occupied Dwellings",
    "Census Vacant Dwellings",
    "Holiday Homes",
    "Census Vacant Share (%)",
    "Detached Houses",
    "Semi-Detached Houses",
    "Terraced Houses",
    "Apartment Dwellings",
    "Apartment Share (%)",
    "Vacancy Component (0-100)",
    "BER Component (0-100)",
    "Renovation Priority Score",
    "Priority Rank",
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
    writer.writerows(combined_rows)


print(f"Counties combined: {len(combined_rows)}")
print(f"Model dataset updated: {OUTPUT_FILE}")