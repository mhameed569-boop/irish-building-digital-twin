"""Download the official CSO Census 2022 SAPS Small Area CSV."""

from pathlib import Path
from urllib.request import Request, urlopen


DATA_URL = (
    "https://www.cso.ie/en/media/csoie/census/census2022/"
    "SAPS_2022_Small_Area_UR_171024.csv"
)
PROJECT_FOLDER = Path(__file__).resolve().parents[1]
OUTPUT_FILE = (
    PROJECT_FOLDER / "data" / "raw" / "cso_saps_2022_small_area.csv"
)


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    request = Request(DATA_URL, headers={"User-Agent": "Mozilla/5.0"})
    print("Downloading CSO Census 2022 Small Area SAPS data...")
    total = 0
    with urlopen(request, timeout=300) as response, OUTPUT_FILE.open("wb") as file:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            file.write(chunk)
            total += len(chunk)
    print(f"Downloaded {total:,} bytes")
    print(f"Download completed: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
