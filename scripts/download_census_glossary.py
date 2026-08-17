"""Download the official CSO Census 2022 SAPS variable glossary."""

from pathlib import Path
from urllib.request import Request, urlopen


DATA_URL = (
    "https://www.cso.ie/en/media/csoie/census/census2022/"
    "Glossary_Saps_2022_REVISED_21102024.xlsx"
)
PROJECT_FOLDER = Path(__file__).resolve().parents[1]
OUTPUT_FILE = (
    PROJECT_FOLDER / "data" / "metadata" / "cso_saps_2022_glossary.xlsx"
)


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    request = Request(DATA_URL, headers={"User-Agent": "Mozilla/5.0"})
    print("Downloading CSO Census 2022 SAPS glossary...")
    with urlopen(request, timeout=120) as response:
        data = response.read()
    OUTPUT_FILE.write_bytes(data)
    print(f"Downloaded {len(data):,} bytes")
    print(f"Download completed: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
