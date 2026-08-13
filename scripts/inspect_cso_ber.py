import json
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_FOLDER / "data" / "raw" / "cso_eba02_ber.json"

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "BER data not found. Run download_cso_ber.py first."
    )

print("Reading BER metadata...")

with INPUT_FILE.open(
    mode="r",
    encoding="utf-8-sig",
) as file:
    dataset = json.load(file)

print(f"\nDataset: {dataset.get('label', 'Unknown')}")
print(f"Dimensions: {dataset['id']}")
print(f"Dimension sizes: {dataset['size']}")

for dimension_id in dataset["id"]:
    dimension = dataset["dimension"][dimension_id]
    category = dimension["category"]

    category_labels = category.get("label", {})
    category_index = category.get("index", {})

    if isinstance(category_index, dict):
        category_codes = sorted(
            category_index,
            key=category_index.get,
        )
    else:
        category_codes = category_index

    print("\n" + "=" * 60)
    print(f"Dimension ID: {dimension_id}")
    print(f"Dimension label: {dimension.get('label', dimension_id)}")
    print(f"Number of categories: {len(category_codes)}")
    print("First categories:")

    for code in category_codes[:10]:
        label = category_labels.get(code, code)
        print(f"  {code}: {label}")