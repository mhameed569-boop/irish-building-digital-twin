from pathlib import Path
from urllib.request import Request, urlopen


DATA_URL = (
    "https://ws.cso.ie/public/api.restful/"
    "PxStat.Data.Cube_API.ReadDataset/"
    "F2020/JSON-stat/2.0/en"
)

PROJECT_FOLDER = Path(__file__).resolve().parents[1]

OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "cso_f2020_census_housing.json"
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

request = Request(
    DATA_URL,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    },
)

print("Downloading CSO Census housing data...")

with urlopen(request, timeout=180) as response:
    census_data = response.read()

OUTPUT_FILE.write_bytes(census_data)

print(f"Downloaded {len(census_data):,} bytes")
print(f"Download completed: {OUTPUT_FILE}")