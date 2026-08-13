from pathlib import Path
from urllib.request import Request, urlopen


DATA_URL = (
    "https://ws.cso.ie/public/api.restful/"
    "PxStat.Data.Cube_API.ReadDataset/EBA02/JSON-stat/2.0/en"
)

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_FOLDER / "data" / "raw" / "cso_eba02_ber.json"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

request = Request(
    DATA_URL,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    },
)

print("Downloading CSO domestic BER data as JSON...")

with urlopen(request, timeout=300) as response:
    data = response.read()

OUTPUT_FILE.write_bytes(data)

print(f"Downloaded {len(data):,} bytes")
print(f"Download completed: {OUTPUT_FILE}")