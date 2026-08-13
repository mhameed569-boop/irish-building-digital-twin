import csv
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_FOLDER / "data" / "raw" / "cso_vac14.csv"
OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "latest_vacancy_rates.csv"
)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "Raw data not found. Run download_cso_vacancy.py first."
    )

with INPUT_FILE.open(
    mode="r",
    encoding="utf-8-sig",
    newline="",
) as file:
    rows = list(csv.DictReader(file))

latest_quarter = max(row["Quarter"] for row in rows)

vacancy_rates = []

for row in rows:
    if (
        row["Quarter"] == latest_quarter
        and row["Statistic Label"] == "Vacancy Rate"
        and row["VALUE"]
    ):
        vacancy_rates.append(
            {
                "Quarter": row["Quarter"],
                "Local Authority": row["Local Authority"],
                "Vacancy Rate (%)": float(row["VALUE"]),
            }
        )

vacancy_rates.sort(
    key=lambda row: row["Vacancy Rate (%)"],
    reverse=True,
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open(
    mode="w",
    encoding="utf-8",
    newline="",
) as file:
    fieldnames = [
        "Quarter",
        "Local Authority",
        "Vacancy Rate (%)",
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(vacancy_rates)

print(f"Latest quarter: {latest_quarter}")
print(f"Number of areas: {len(vacancy_rates)}")
print("\nHighest vacancy rates:")

for row in vacancy_rates[:10]:
    print(
        f"{row['Local Authority']}: "
        f"{row['Vacancy Rate (%)']}%"
    )

print(f"\nProcessed file created: {OUTPUT_FILE}")