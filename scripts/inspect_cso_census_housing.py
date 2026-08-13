import json
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "cso_f2020_census_housing.json"
)


print("Reading CSO Census housing data...")

with INPUT_FILE.open(
    mode="r",
    encoding="utf-8-sig",
) as file:
    dataset = json.load(file)


dimension_ids = dataset["id"]
dimension_sizes = dataset["size"]

print(f"Dataset: {dataset.get('label', 'Unknown')}")
print(f"Dimensions: {dimension_ids}")
print(f"Dimension sizes: {dimension_sizes}")


for dimension_id in dimension_ids:
    dimension = dataset["dimension"][dimension_id]
    category = dimension["category"]

    index = category["index"]
    labels = category.get("label", {})

    if isinstance(index, dict):
        category_codes = [
            code
            for code, position in sorted(
                index.items(),
                key=lambda item: item[1],
            )
        ]
    else:
        category_codes = index

    print("\n" + "=" * 60)
    print(f"Dimension ID: {dimension_id}")
    print(
        "Dimension label:",
        dimension.get("label", dimension_id),
    )
    print(
        f"Number of categories: {len(category_codes)}"
    )
    print("First categories:")

    for code in category_codes[:20]:
        label = labels.get(code, code)
        print(f"  {code}: {label}")