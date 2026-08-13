import csv
import json
from collections import defaultdict
from pathlib import Path


TARGET_YEAR = "2022"
STATISTIC_CODE = "F2020C01"

PROJECT_FOLDER = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "cso_f2020_census_housing.json"
)

OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "census_housing_by_county_2022.csv"
)


def ordered_category_codes(dimension):
    index = dimension["category"]["index"]

    if isinstance(index, dict):
        return [
            code
            for code, position in sorted(
                index.items(),
                key=lambda item: item[1],
            )
        ]

    return index


def county_name(administrative_area):
    dublin_areas = {
        "Dublin City",
        "Dún Laoghaire-Rathdown",
        "Fingal",
        "South Dublin",
    }

    if administrative_area in dublin_areas:
        return "Dublin"

    if administrative_area in {
        "Galway City",
        "Galway County",
    }:
        return "Galway"

    replacements = {
        "Cork City and Cork County": "Cork",
        "Limerick City and County": "Limerick",
        "Waterford City and County": "Waterford",
    }

    return replacements.get(
        administrative_area,
        administrative_area,
    )


print("Reading CSO Census housing data...")

with INPUT_FILE.open(
    mode="r",
    encoding="utf-8-sig",
) as file:
    dataset = json.load(file)


dimension_ids = dataset["id"]
dimension_sizes = dataset["size"]

category_codes = {
    dimension_id: ordered_category_codes(
        dataset["dimension"][dimension_id]
    )
    for dimension_id in dimension_ids
}

category_positions = {
    dimension_id: {
        code: position
        for position, code in enumerate(
            category_codes[dimension_id]
        )
    }
    for dimension_id in dimension_ids
}


multipliers = []

for dimension_index in range(len(dimension_sizes)):
    multiplier = 1

    for size in dimension_sizes[
        dimension_index + 1:
    ]:
        multiplier *= size

    multipliers.append(multiplier)


values = dataset["value"]


def get_value(category_selection):
    flat_index = 0

    for dimension_index, dimension_id in enumerate(
        dimension_ids
    ):
        code = category_selection[dimension_id]
        position = category_positions[
            dimension_id
        ][code]

        flat_index += (
            position
            * multipliers[dimension_index]
        )

    if isinstance(values, list):
        value = values[flat_index]
    else:
        value = values.get(str(flat_index))

    if value is None:
        return 0

    return float(value)


geography_dimension = dataset["dimension"][
    "C04104V04868"
]

geography_labels = geography_dimension[
    "category"
].get("label", {})


housing_status_codes = {
    "Total Housing Stock": "-",
    "Occupied Dwellings": "111",
    "Temporarily Absent Dwellings": "333",
    "Vacant Dwellings": "444",
    "Holiday Homes": "666",
}

dwelling_type_codes = {
    "Detached Houses": "12",
    "Semi-Detached Houses": "13",
    "Terraced Houses": "14",
    "Purpose-Built Apartments": "16",
    "Converted Apartments": "170",
}


county_totals = defaultdict(
    lambda: defaultdict(float)
)


for geography_code in category_codes[
    "C04104V04868"
]:
    if geography_code == "IE0":
        continue

    administrative_area = geography_labels[
        geography_code
    ]

    county = county_name(administrative_area)

    for output_column, status_code in (
        housing_status_codes.items()
    ):
        selection = {
            "STATISTIC": STATISTIC_CODE,
            "TLIST(A1)": TARGET_YEAR,
            "C04104V04868": geography_code,
            "C02010V02440": "-",
            "C02758V03328": status_code,
        }

        county_totals[county][output_column] += (
            get_value(selection)
        )

    for output_column, dwelling_code in (
        dwelling_type_codes.items()
    ):
        selection = {
            "STATISTIC": STATISTIC_CODE,
            "TLIST(A1)": TARGET_YEAR,
            "C04104V04868": geography_code,
            "C02010V02440": dwelling_code,
            "C02758V03328": "-",
        }

        county_totals[county][output_column] += (
            get_value(selection)
        )


processed_rows = []

for county in sorted(county_totals):
    totals = county_totals[county]

    total_housing_stock = totals[
        "Total Housing Stock"
    ]

    vacant_share = (
        totals["Vacant Dwellings"]
        / total_housing_stock
        * 100
        if total_housing_stock
        else 0
    )

    apartment_dwellings = (
        totals["Purpose-Built Apartments"]
        + totals["Converted Apartments"]
    )

    processed_rows.append(
        {
            "Census Year": int(TARGET_YEAR),
            "County": county,
            "Total Housing Stock": int(
                totals["Total Housing Stock"]
            ),
            "Occupied Dwellings": int(
                totals["Occupied Dwellings"]
            ),
            "Temporarily Absent Dwellings": int(
                totals["Temporarily Absent Dwellings"]
            ),
            "Vacant Dwellings": int(
                totals["Vacant Dwellings"]
            ),
            "Holiday Homes": int(
                totals["Holiday Homes"]
            ),
            "Vacant Share of Housing Stock (%)": round(
                vacant_share,
                2,
            ),
            "Detached Houses": int(
                totals["Detached Houses"]
            ),
            "Semi-Detached Houses": int(
                totals["Semi-Detached Houses"]
            ),
            "Terraced Houses": int(
                totals["Terraced Houses"]
            ),
            "Purpose-Built Apartments": int(
                totals["Purpose-Built Apartments"]
            ),
            "Converted Apartments": int(
                totals["Converted Apartments"]
            ),
            "Apartment Dwellings": int(
                apartment_dwellings
            ),
        }
    )


fieldnames = [
    "Census Year",
    "County",
    "Total Housing Stock",
    "Occupied Dwellings",
    "Temporarily Absent Dwellings",
    "Vacant Dwellings",
    "Holiday Homes",
    "Vacant Share of Housing Stock (%)",
    "Detached Houses",
    "Semi-Detached Houses",
    "Terraced Houses",
    "Purpose-Built Apartments",
    "Converted Apartments",
    "Apartment Dwellings",
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
    writer.writerows(processed_rows)


print(f"Counties processed: {len(processed_rows)}")
print(f"Processed file created: {OUTPUT_FILE}")