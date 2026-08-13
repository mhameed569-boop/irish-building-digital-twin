from pathlib import Path
from urllib.request import Request, urlopen


DATA_URL = (
    "https://data-osi.opendata.arcgis.com/api/download/v1/"
    "items/dc24df2a5ce84ee9a38d9afe8431ee9b/"
    "geojson?layers=1"
)

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "ireland_counties_2024.geojson"
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

request = Request(
    DATA_URL,
    headers={"User-Agent": "Mozilla/5.0"},
)

print("Downloading official county boundaries...")

with urlopen(request, timeout=300) as response:
    data = response.read()

OUTPUT_FILE.write_bytes(data)

print(f"Downloaded {len(data):,} bytes")
print(f"Download completed: {OUTPUT_FILE}")