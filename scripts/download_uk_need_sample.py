"""Download the public 50,000-row UK NEED 2025 transfer-learning sample."""

from pathlib import Path
from urllib.request import Request, urlopen


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
FILES = {
    "https://assets.publishing.service.gov.uk/media/685c01cec07c71e5a8709834/anon2025_50k.csv": (
        PROJECT_FOLDER / "data" / "raw" / "international" / "uk_need_2025_50k.csv"
    ),
    "https://assets.publishing.service.gov.uk/media/685c02aa0433072fce0e1025/NEED-2025-anonymised-dataset-metadata.ods": (
        PROJECT_FOLDER / "data" / "raw" / "international" / "uk_need_2025_metadata.ods"
    ),
}


def main():
    for url, output in FILES.items():
        output.parent.mkdir(parents=True, exist_ok=True)
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        print(f"Downloading {output.name}...")
        with urlopen(request, timeout=300) as response:
            data = response.read()
        output.write_bytes(data)
        print(f"Downloaded {len(data):,} bytes to {output}")


if __name__ == "__main__":
    main()
