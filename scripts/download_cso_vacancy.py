from pathlib import Path
from urllib.request import urlopen


DATA_URL = (
    "https://ws.cso.ie/public/api.restful/"
    "PxStat.Data.Cube_API.ReadDataset/VAC14/CSV/1.0/en"
)

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_FOLDER / "data" / "raw" / "cso_vac14.csv"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

print("Downloading CSO vacancy data...")

with urlopen(DATA_URL, timeout=60) as response:
    OUTPUT_FILE.write_bytes(response.read())

print(f"Download completed: {OUTPUT_FILE}")