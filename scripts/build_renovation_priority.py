import csv
from collections import defaultdict
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]

VACANCY_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "cso_vac14.csv"
)

BER_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "ber_by_county_2024.csv"
)

OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "renovation_priority_by_county_2024.csv"
)


def local_authority_to_county(local_authority):
    special_cases = {
        "Cork City Council": "Cork",
        "Cork County Council": "Cork",
        "Dublin City Council": "Dublin",
        "Dún Laoghaire Rathdown County Council": "Dublin",
        "Fingal County Council": "Dublin",
        "South Dublin County Council": "Dublin",
        "Galway City Council": "Galway",
        "Galway County Council": "Galway",
        "Limerick City & County Council": "Limerick",
        "Waterford City & County Council": "Waterford",
    }

    if local_authority in special_cases:
        return special_cases[local_authority]

    return local_authority.removesuffix(
        " County Council"
    ).removesuffix(
        " City Council"
    )


if not VACANCY_FILE.exists():
    raise FileNotFoundError(
        "Vacancy data not found. "
        "Run download_cso_vacancy.py first."
    )

if not BER_FILE.exists():
    raise FileNotFoundError(
        "BER summary not found. Run summarize_ber.py first."
    )


with VACANCY_FILE.open(
    mode="r",
    encoding="utf-8-sig",
    newline="",
) as file:
    vacancy_rows = list(csv.DictReader(file))

latest_quarter = max(
    row["Quarter"] for row in vacancy_rows
)

authority_statistics = defaultdict(dict)

for row in vacancy_rows:
    if row["Quarter"] != latest_quarter:
        continue

    if not row["VALUE"]:
        continue

    authority = row["Local Authority"]
    statistic = row["Statistic Label"]

    authority_statistics[authority][statistic] = float(
        row["VALUE"]
    )


county_totals = defaultdict(
    lambda: {
        "vacant_dwellings": 0.0,
        "estimated_stock": 0.0,
    }
)

for authority, statistics in authority_statistics.items():
    vacant_dwellings = statistics.get(
        "Number of Vacant Dwellings"
    )

    vacancy_rate = statistics.get("Vacancy Rate")

    if (
        vacant_dwellings is None
        or vacancy_rate is None
        or vacancy_rate <= 0
    ):
        continue

    county = local_authority_to_county(authority)

    estimated_stock = (
        vacant_dwellings / (vacancy_rate / 100)
    )

    county_totals[county][
        "vacant_dwellings"
    ] += vacant_dwellings

    county_totals[county][
        "estimated_stock"
    ] += estimated_stock


vacancy_by_county = {}

for county, totals in county_totals.items():
    vacancy_rate = (
        totals["vacant_dwellings"]
        / totals["estimated_stock"]
        * 100
    )

    vacancy_by_county[county] = vacancy_rate


with BER_FILE.open(
    mode="r",
    encoding="utf-8-sig",
    newline="",
) as file:
    ber_rows = list(csv.DictReader(file))

poor_ber_by_county = {
    row["County"]: float(row["Poor BER (%)"])
    for row in ber_rows
}


matched_counties = sorted(
    set(vacancy_by_county)
    & set(poor_ber_by_county)
)

missing_vacancy = sorted(
    set(poor_ber_by_county)
    - set(vacancy_by_county)
)

missing_ber = sorted(
    set(vacancy_by_county)
    - set(poor_ber_by_county)
)

if missing_vacancy:
    print(
        "Counties missing vacancy data:",
        missing_vacancy,
    )

if missing_ber:
    print(
        "Counties missing BER data:",
        missing_ber,
    )


vacancy_values = [
    vacancy_by_county[county]
    for county in matched_counties
]

ber_values = [
    poor_ber_by_county[county]
    for county in matched_counties
]


def min_max_score(value, all_values):
    minimum = min(all_values)
    maximum = max(all_values)

    if maximum == minimum:
        return 0.0

    return (
        (value - minimum)
        / (maximum - minimum)
        * 100
    )


records = []

for county in matched_counties:
    vacancy_rate = vacancy_by_county[county]
    poor_ber_percentage = poor_ber_by_county[county]

    vacancy_score = min_max_score(
        vacancy_rate,
        vacancy_values,
    )

    ber_score = min_max_score(
        poor_ber_percentage,
        ber_values,
    )

    priority_score = (
        0.50 * vacancy_score
        + 0.50 * ber_score
    )

    records.append(
        {
            "County": county,
            "Vacancy Quarter": latest_quarter,
            "Vacancy Rate (%)": round(
                vacancy_rate,
                2,
            ),
            "Poor BER (%)": round(
                poor_ber_percentage,
                2,
            ),
            "Vacancy Component (0-100)": round(
                vacancy_score,
                2,
            ),
            "BER Component (0-100)": round(
                ber_score,
                2,
            ),
            "Renovation Priority Score": round(
                priority_score,
                2,
            ),
        }
    )


records.sort(
    key=lambda record: record[
        "Renovation Priority Score"
    ],
    reverse=True,
)

for rank, record in enumerate(records, start=1):
    record["Priority Rank"] = rank


OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

fieldnames = [
    "Priority Rank",
    "County",
    "Vacancy Quarter",
    "Vacancy Rate (%)",
    "Poor BER (%)",
    "Vacancy Component (0-100)",
    "BER Component (0-100)",
    "Renovation Priority Score",
]

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


print(f"Vacancy quarter: {latest_quarter}")
print(f"Matched counties: {len(matched_counties)}")
print("\nHighest renovation priorities:")

for record in records[:10]:
    print(
        f"{record['Priority Rank']}. "
        f"{record['County']}: "
        f"{record['Renovation Priority Score']}"
    )

print(f"\nOutput created: {OUTPUT_FILE}")