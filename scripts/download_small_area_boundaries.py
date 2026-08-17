"""Download official 2022 Small Area boundaries from Tailte Éireann."""

import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SERVICE_URL = (
    "https://services-eu1.arcgis.com/BuS9rtTsYEV5C0xh/arcgis/rest/services/"
    "SMALL_AREA_2022_Genralised_20m_view/FeatureServer/0/query"
)
PROJECT_FOLDER = Path(__file__).resolve().parents[1]
OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "ireland_small_areas_2022_generalised_20m.geojson"
)
PAGE_SIZE = 2000


def download_page(offset):
    parameters = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": "4326",
        "orderByFields": "OBJECTID",
        "resultOffset": offset,
        "resultRecordCount": PAGE_SIZE,
        "f": "geojson",
    }
    request = Request(
        f"{SERVICE_URL}?{urlencode(parameters)}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urlopen(request, timeout=300) as response:
        return json.load(response)


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    features = []
    offset = 0
    print("Downloading official 2022 Small Area boundaries...")
    while True:
        page = download_page(offset)
        page_features = page.get("features", [])
        features.extend(page_features)
        print(f"Downloaded boundary features: {len(features):,}")
        if len(page_features) < PAGE_SIZE:
            break
        offset += PAGE_SIZE

    collection = {
        "type": "FeatureCollection",
        "name": "CSO Small Areas 2022 Generalised 20m",
        "source": SERVICE_URL,
        "features": features,
    }
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(collection, file, ensure_ascii=False)
    print(f"Download completed: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
