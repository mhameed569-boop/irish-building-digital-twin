import json
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
INPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "ireland_counties_2024.geojson"
)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "County boundaries not found. "
        "Run download_county_boundaries.py first."
    )

print("Reading county boundary metadata...")

with INPUT_FILE.open(
    mode="r",
    encoding="utf-8-sig",
) as file:
    geojson = json.load(file)

features = geojson["features"]

print(f"Number of features: {len(features)}")
print(f"Geometry type: {features[0]['geometry']['type']}")
print("\nProperty fields:")

for field in features[0]["properties"]:
    print(f"  {field}")

print("\nFirst five records:")

for feature in features[:5]:
    print(feature["properties"])