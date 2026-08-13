import csv
import json
from pathlib import Path


TARGET_YEAR = "2024"

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_FOLDER / "data" / "raw" / "cso_eba02_ber.json"
OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "ber_by_county_2024.csv"
)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "BER data not found. Run download_cso_ber.py first."
    )

print("Reading CSO BER data...")

with INPUT_FILE.open(
    mode="r",
    encoding="utf-8-sig",
) as file:
    dataset = json.load(file)


def ordered_category_codes(dimension):
    category_index = dimension["category"]["index"]

    if isinstance(category_index, dict):
        return [
            code
            for code, position in sorted(
                category_index.items(),
                key=lambda item: item[1],
            )
        ]

    return category_index


dimension_ids = dataset["id"]
dimension_sizes = dataset["size"]
dimensions = dataset["dimension"]

codes = {
    dimension_id: ordered_category_codes(
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

if TARGET_YEAR not in positions["TLIST(A1)"]:
    raise ValueError(f"Year {TARGET_YEAR} is not available.")

ber_dimension = "C03440V04149"
dwelling_dimension = "C03151V03803"
fuel_dimension = "C03442V04151"
construction_dimension = "C03441V04150"
county_dimension = "C03444V04153"

ber_codes = [
    code
    for code in codes[ber_dimension]
    if code != "-"
]

county_codes = [
    code
    for code in codes[county_dimension]
    if labels[county_dimension].get(
        code,
        code,
    ).startswith("Co. ")
]

values = dataset["value"]


def get_dataset_value(flat_index):
    if isinstance(values, list):
        value = values[flat_index]
    else:
        value = values.get(str(flat_index))

    if value is None:
        return 0

    return int(value)


def calculate_flat_index(selected_positions):
    flat_index = 0

    for selected_position, dimension_size in zip(
        selected_positions,
        dimension_sizes,
    ):
        flat_index = (
            flat_index * dimension_size
            + selected_position
        )

    return flat_index


records = []

for county_code in county_codes:
    rating_counts = {}

    for ber_code in ber_codes:
        selected_positions = [
            0,
            positions["TLIST(A1)"][TARGET_YEAR],
            positions[ber_dimension][ber_code],
            positions[dwelling_dimension]["-"],
            positions[fuel_dimension]["-"],
            positions[construction_dimension]["-"],
            positions[county_dimension][county_code],
        ]

        flat_index = calculate_flat_index(
            selected_positions
        )

        rating_label = labels[ber_dimension].get(
            ber_code,
            ber_code,
        )

        rating_counts[rating_label] = get_dataset_value(
            flat_index
        )

    total_dwellings = sum(rating_counts.values())

    poor_ber_count = sum(
        count
        for rating, count in rating_counts.items()
        if rating in {"D", "E"} or rating.startswith("F")
    )

    weighted_score = sum(
        position * rating_counts[rating]
        for position, rating in enumerate(
            rating_counts,
            start=1,
        )
    )

    average_ber_score = (
        weighted_score / total_dwellings
        if total_dwellings
        else 0
    )

    poor_ber_percentage = (
        poor_ber_count / total_dwellings * 100
        if total_dwellings
        else 0
    )

    county_name = labels[county_dimension][
        county_code
    ].removeprefix("Co. ")

    record = {
        "Year": TARGET_YEAR,
        "County": county_name,
        "Total BER Dwellings": total_dwellings,
        "Poor BER Dwellings": poor_ber_count,
        "Poor BER (%)": round(
            poor_ber_percentage,
            2,
        ),
        "Average BER Category Score": round(
            average_ber_score,
            3,
        ),
    }

    record.update(rating_counts)
    records.append(record)

records.sort(
    key=lambda record: record["Poor BER (%)"],
    reverse=True,
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

fieldnames = [
    "Year",
    "County",
    "Total BER Dwellings",
    "Poor BER Dwellings",
    "Poor BER (%)",
    "Average BER Category Score",
]

fieldnames.extend(
    labels[ber_dimension].get(code, code)
    for code in ber_codes
)

with OUTPUT_FILE.open(
    mode="w",
    encoding="utf-8",
    newline="",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames,
    )
    writer.writeheader()
    writer.writerows(records)

print(f"Counties processed: {len(records)}")
print("\nCounties with highest poor-BER percentages:")

for record in records[:10]:
    print(
        f"{record['County']}: "
        f"{record['Poor BER (%)']}%"
    )

print(f"\nProcessed file created: {OUTPUT_FILE}")