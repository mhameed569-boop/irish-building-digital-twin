from pathlib import Path
from urllib.request import Request, urlopen


DATA_URL = (
    "https://clidata.met.ie/cli/grids/county/"
    "averages.csv"
)

PROJECT_FOLDER = Path(__file__).resolve().parents[1]

OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "met_eireann_county_weather.csv"
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

request = Request(
    DATA_URL,
    headers={
        "User-Agent": "Mozilla/5.0",
    },
)

print("Downloading Met Eireann county weather data...")

with urlopen(request, timeout=120) as response:
    weather_data = response.read()

OUTPUT_FILE.write_bytes(weather_data)

print(f"Downloaded {len(weather_data):,} bytes")
print(f"Download completed: {OUTPUT_FILE}")