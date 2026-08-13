import csv
import json
from pathlib import Path


TARGET_YEAR = "2024"

PROJECT_FOLDER = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "cso_eba02_ber.json"
)

OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "energy_archetype_features_by_county_2024.csv"
)


print("Reading CSO BER data...")

with INPUT_FILE.open(
    mode="r",
    encoding="utf-8-sig",
) as file:
    dataset = json.load(file)


def ordered_codes(dimension):
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


dimension_ids = dataset["id"]
dimension_sizes = dataset["size"]
dimensions = dataset["dimension"]

codes = {
    dimension_id: ordered_codes(
        dimensions[dimension_id]
    )
    for dimension_id in dimension_ids
}

positions = {
    dimension_id: {
        code: position
        for position, code in enumerate(
            codes[dimension_id]
        )
    }
    for dimension_id in dimension_ids
}

labels = {
    dimension_id: dimensions[dimension_id][
        "category"
    ].get("label", {})
    for dimension_id in dimension_ids
}

values = dataset["value"]


def dataset_value(selected_codes):
    selected_positions = [
        positions[dimension_id][
            selected_codes[dimension_id]
        ]
        for dimension_id in dimension_ids
    ]

    flat_index = 0

    for selected_position, dimension_size in zip(
        selected_positions,
        dimension_sizes,
    ):
        flat_index = (
            flat_index * dimension_size
            + selected_position
        )

    if isinstance(values, list):
        value = values[flat_index]
    else:
        value = values.get(str(flat_index))

    return int(value) if value is not None else 0


def percentage(count, total):
    if total == 0:
        return 0

    return round(count / total * 100, 2)


ber_dimension = "C03440V04149"
dwelling_dimension = "C03151V03803"
fuel_dimension = "C03442V04151"
construction_dimension = "C03441V04150"
county_dimension = "C03444V04153"


county_codes = [
    code
    for code in codes[county_dimension]
    if labels[county_dimension].get(
        code,
        code,
    ).startswith("Co. ")
]


fuel_groups = {
    "Mains Gas": ["01"],
    "LPG": ["02"],
    "Heating Oil": ["04"],
    "Electricity": ["05"],
    "Solid Fuel": ["11"],
}

dwelling_groups = {
    "Apartment": [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
    ],
    "Detached House": ["08"],
    "Semi-Detached House": ["09"],
    "Terraced House": ["10", "11"],
}

construction_groups = {
    "Pre-1978": ["01"],
    "1978-1999": ["02"],
    "2000-2009": ["03", "04"],
    "2010-2019": ["05", "14"],
    "2020-2024": ["15"],
}


records = []


for county_code in county_codes:
    base_selection = {
        "STATISTIC": "EBA02",
        "TLIST(A1)": TARGET_YEAR,
        ber_dimension: "-",
        dwelling_dimension: "-",
        fuel_dimension: "-",
        construction_dimension: "-",
        county_dimension: county_code,
    }

    total_dwellings = dataset_value(
        base_selection
    )

    fuel_counts = {}

    for group_name, group_codes in fuel_groups.items():
        fuel_counts[group_name] = sum(
            dataset_value(
                {
                    **base_selection,
                    fuel_dimension: code,
                }
            )
            for code in group_codes
        )

    dwelling_counts = {}

    for group_name, group_codes in (
        dwelling_groups.items()
    ):
        dwelling_counts[group_name] = sum(
            dataset_value(
                {
                    **base_selection,
                    dwelling_dimension: code,
                }
            )
            for code in group_codes
        )

    construction_counts = {}

    for group_name, group_codes in (
        construction_groups.items()
    ):
        construction_counts[group_name] = sum(
            dataset_value(
                {
                    **base_selection,
                    construction_dimension: code,
                }
            )
            for code in group_codes
        )

    pre_2000_count = (
        construction_counts["Pre-1978"]
        + construction_counts["1978-1999"]
    )

    dominant_fuel = max(
        fuel_counts,
        key=fuel_counts.get,
    )

    dominant_dwelling_type = max(
        dwelling_counts,
        key=dwelling_counts.get,
    )

    dominant_construction_period = max(
        construction_counts,
        key=construction_counts.get,
    )

    county = labels[county_dimension][
        county_code
    ].removeprefix("Co. ")

    record = {
        "Year": int(TARGET_YEAR),
        "County": county,
        "Total BER Dwellings": total_dwellings,
        "Dominant Heating Fuel": dominant_fuel,
        "Mains Gas (%)": percentage(
            fuel_counts["Mains Gas"],
            total_dwellings,
        ),
        "Heating Oil (%)": percentage(
            fuel_counts["Heating Oil"],
            total_dwellings,
        ),
        "Electricity (%)": percentage(
            fuel_counts["Electricity"],
            total_dwellings,
        ),
        "Solid Fuel (%)": percentage(
            fuel_counts["Solid Fuel"],
            total_dwellings,
        ),
        "LPG (%)": percentage(
            fuel_counts["LPG"],
            total_dwellings,
        ),
        "Dominant Dwelling Type": (
            dominant_dwelling_type
        ),
        "Apartment (%)": percentage(
            dwelling_counts["Apartment"],
            total_dwellings,
        ),
        "Detached House (%)": percentage(
            dwelling_counts["Detached House"],
            total_dwellings,
        ),
        "Semi-Detached House (%)": percentage(
            dwelling_counts["Semi-Detached House"],
            total_dwellings,
        ),
        "Terraced House (%)": percentage(
            dwelling_counts["Terraced House"],
            total_dwellings,
        ),
        "Dominant Construction Period": (
            dominant_construction_period
        ),
        "Pre-1978 (%)": percentage(
            construction_counts["Pre-1978"],
            total_dwellings,
        ),
        "1978-1999 (%)": percentage(
            construction_counts["1978-1999"],
            total_dwellings,
        ),
        "Pre-2000 (%)": percentage(
            pre_2000_count,
            total_dwellings,
        ),
        "2000-2009 (%)": percentage(
            construction_counts["2000-2009"],
            total_dwellings,
        ),
        "2010-2019 (%)": percentage(
            construction_counts["2010-2019"],
            total_dwellings,
        ),
        "2020-2024 (%)": percentage(
            construction_counts["2020-2024"],
            total_dwellings,
        ),
    }

    records.append(record)


records.sort(
    key=lambda record: record["County"]
)

fieldnames = list(records[0].keys())

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
    writer.writerows(records)


print(f"Counties processed: {len(records)}")
print(f"Processed file created: {OUTPUT_FILE}")