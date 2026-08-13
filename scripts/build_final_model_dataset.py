import csv
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]

BASE_MODEL_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "model_dataset_county_2024.csv"
)

ARCHETYPE_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "energy_archetype_features_by_county_2024.csv"
)

OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "final_model_dataset_county_2024.csv"
)


def read_csv(file_path):
    with file_path.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        fieldnames = reader.fieldnames

    return rows, fieldnames


print("Reading integrated county dataset...")

base_rows, base_fieldnames = read_csv(
    BASE_MODEL_FILE
)

print("Reading energy archetype features...")

archetype_rows, _ = read_csv(
    ARCHETYPE_FILE
)

archetype_by_county = {
    row["County"].strip().upper(): row
    for row in archetype_rows
}


additional_fieldnames = [
    "BER Sample Dwellings",
    "Dominant Heating Fuel",
    "Mains Gas (%)",
    "Heating Oil (%)",
    "Electricity (%)",
    "Solid Fuel (%)",
    "LPG (%)",
    "Dominant BER Dwelling Type",
    "BER Apartment (%)",
    "BER Detached House (%)",
    "BER Semi-Detached House (%)",
    "BER Terraced House (%)",
    "Dominant Construction Period",
    "Pre-1978 (%)",
    "1978-1999 (%)",
    "Pre-2000 (%)",
    "2000-2009 (%)",
    "2010-2019 (%)",
    "2020-2024 (%)",
]


final_rows = []
missing_counties = []


for base_row in base_rows:
    county = base_row["County"].strip()
    county_key = county.upper()

    archetype_row = archetype_by_county.get(
        county_key
    )

    if archetype_row is None:
        missing_counties.append(county)
        continue

    final_row = dict(base_row)

    final_row.update(
        {
            "BER Sample Dwellings": archetype_row[
                "Total BER Dwellings"
            ],
            "Dominant Heating Fuel": archetype_row[
                "Dominant Heating Fuel"
            ],
            "Mains Gas (%)": archetype_row[
                "Mains Gas (%)"
            ],
            "Heating Oil (%)": archetype_row[
                "Heating Oil (%)"
            ],
            "Electricity (%)": archetype_row[
                "Electricity (%)"
            ],
            "Solid Fuel (%)": archetype_row[
                "Solid Fuel (%)"
            ],
            "LPG (%)": archetype_row[
                "LPG (%)"
            ],
            "Dominant BER Dwelling Type": (
                archetype_row[
                    "Dominant Dwelling Type"
                ]
            ),
            "BER Apartment (%)": archetype_row[
                "Apartment (%)"
            ],
            "BER Detached House (%)": archetype_row[
                "Detached House (%)"
            ],
            "BER Semi-Detached House (%)": (
                archetype_row[
                    "Semi-Detached House (%)"
                ]
            ),
            "BER Terraced House (%)": archetype_row[
                "Terraced House (%)"
            ],
            "Dominant Construction Period": (
                archetype_row[
                    "Dominant Construction Period"
                ]
            ),
            "Pre-1978 (%)": archetype_row[
                "Pre-1978 (%)"
            ],
            "1978-1999 (%)": archetype_row[
                "1978-1999 (%)"
            ],
            "Pre-2000 (%)": archetype_row[
                "Pre-2000 (%)"
            ],
            "2000-2009 (%)": archetype_row[
                "2000-2009 (%)"
            ],
            "2010-2019 (%)": archetype_row[
                "2010-2019 (%)"
            ],
            "2020-2024 (%)": archetype_row[
                "2020-2024 (%)"
            ],
        }
    )

    final_rows.append(final_row)


if missing_counties:
    print(
        "Counties missing archetype data:",
        ", ".join(missing_counties),
    )


output_fieldnames = (
    base_fieldnames
    + additional_fieldnames
)


with OUTPUT_FILE.open(
    mode="w",
    encoding="utf-8-sig",
    newline="",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=output_fieldnames,
    )

    writer.writeheader()
    writer.writerows(final_rows)


print(f"Counties combined: {len(final_rows)}")
print(f"Final model dataset created: {OUTPUT_FILE}")