import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from matplotlib.patches import Polygon


PROJECT_FOLDER = Path(__file__).resolve().parents[1]

GEOJSON_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "ireland_counties_2024.geojson"
)

PRIORITY_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "renovation_priority_by_county_2024.csv"
)

OUTPUT_FOLDER = PROJECT_FOLDER / "outputs" / "figures"
PNG_FILE = OUTPUT_FOLDER / "renovation_priority_map_2024.png"
SVG_FILE = OUTPUT_FOLDER / "renovation_priority_map_2024.svg"


if not GEOJSON_FILE.exists():
    raise FileNotFoundError(
        "County boundaries not found. "
        "Run download_county_boundaries.py first."
    )

if not PRIORITY_FILE.exists():
    raise FileNotFoundError(
        "Priority data not found. "
        "Run build_renovation_priority.py first."
    )


print("Reading renovation priority data...")

with PRIORITY_FILE.open(
    mode="r",
    encoding="utf-8-sig",
    newline="",
) as file:
    priority_rows = list(csv.DictReader(file))

priority_by_county = {
    row["County"].strip().upper(): float(
        row["Renovation Priority Score"]
    )
    for row in priority_rows
}

rank_by_county = {
    row["County"].strip().upper(): int(
        row["Priority Rank"]
    )
    for row in priority_rows
}


print("Reading county boundaries...")

with GEOJSON_FILE.open(
    mode="r",
    encoding="utf-8-sig",
) as file:
    geojson = json.load(file)


def polygon_area_and_centroid(coordinates):
    area_twice = 0.0
    centroid_x = 0.0
    centroid_y = 0.0

    for index in range(len(coordinates) - 1):
        x1, y1 = coordinates[index][:2]
        x2, y2 = coordinates[index + 1][:2]

        cross_product = x1 * y2 - x2 * y1

        area_twice += cross_product
        centroid_x += (x1 + x2) * cross_product
        centroid_y += (y1 + y2) * cross_product

    if area_twice == 0:
        points = coordinates[:-1] or coordinates

        average_x = sum(point[0] for point in points) / len(
            points
        )

        average_y = sum(point[1] for point in points) / len(
            points
        )

        return 0.0, average_x, average_y

    centroid_x /= 3 * area_twice
    centroid_y /= 3 * area_twice

    return abs(area_twice / 2), centroid_x, centroid_y


patches = []
patch_scores = []

centroid_totals = defaultdict(
    lambda: {
        "weighted_x": 0.0,
        "weighted_y": 0.0,
        "area": 0.0,
    }
)

mapped_counties = set()

for feature in geojson["features"]:
    properties = feature["properties"]
    geometry = feature.get("geometry")

    if not geometry:
        continue

    county = properties["ENG_NAME_VALUE"].strip().upper()
    score = priority_by_county.get(county)

    if score is None:
        continue

    geometry_type = geometry["type"]
    coordinates = geometry["coordinates"]

    if geometry_type == "Polygon":
        polygons = [coordinates]
    elif geometry_type == "MultiPolygon":
        polygons = coordinates
    else:
        continue

    for polygon_coordinates in polygons:
            if not polygon_coordinates:
                continue

            exterior_ring = polygon_coordinates[0]

            if len(exterior_ring) < 3:
                continue

            two_dimensional_ring = [
                [point[0], point[1]]
                for point in exterior_ring
            ]

            patches.append(
                Polygon(
                    two_dimensional_ring,
                    closed=True,
                )
            )

            patch_scores.append(score)
            mapped_counties.add(county)

            area, centroid_x, centroid_y = (
                polygon_area_and_centroid(exterior_ring)
            )

            centroid_totals[county][
                "weighted_x"
            ] += centroid_x * area

            centroid_totals[county][
                "weighted_y"
            ] += centroid_y * area

            centroid_totals[county]["area"] += area


missing_counties = sorted(
    set(priority_by_county) - mapped_counties
)

if missing_counties:
    print("Counties not matched:", missing_counties)


scores = list(priority_by_county.values())

normalizer = Normalize(
    vmin=min(scores),
    vmax=max(scores),
)

colour_map = plt.colormaps["RdYlGn_r"]

figure, axis = plt.subplots(figsize=(9, 11))

collection = PatchCollection(
    patches,
    cmap=colour_map,
    norm=normalizer,
    edgecolor="white",
    linewidth=0.35,
)

collection.set_array(patch_scores)
axis.add_collection(collection)

map_bounds = collection.get_datalim(axis.transData)

axis.set_xlim(
    map_bounds.xmin,
    map_bounds.xmax,
)

axis.set_ylim(
    map_bounds.ymin,
    map_bounds.ymax,
)

axis.set_aspect("equal")
axis.axis("off")

axis.set_title(
    "Renovation Priority Index by County",
    fontsize=17,
    pad=16,
)

axis.text(
    0.5,
    0.985,
    "Vacancy rate and poor BER performance, 2024",
    transform=axis.transAxes,
    ha="center",
    va="top",
    fontsize=10,
    color="#555555",
)


label_offsets = {
    "DUBLIN": (0.18, 0.00),
    "LOUTH": (0.12, 0.05),
    "MEATH": (0.06, 0.00),
    "KILDARE": (0.10, -0.02),
    "WICKLOW": (0.12, -0.02),
    "CARLOW": (0.08, -0.03),
    "KILKENNY": (0.04, -0.06),
    "WATERFORD": (0.00, -0.08),
    "LONGFORD": (0.00, 0.05),
    "LEITRIM": (0.00, 0.06),
    "SLIGO": (-0.02, 0.05),
}


for county, totals in centroid_totals.items():
    if totals["area"] == 0:
        continue

    x_position = (
        totals["weighted_x"] / totals["area"]
    )

    y_position = (
        totals["weighted_y"] / totals["area"]
    )

    offset_x, offset_y = label_offsets.get(
        county,
        (0.0, 0.0),
    )

    score = priority_by_county[county]
    rank = rank_by_county[county]

    if rank <= 10:
        label = (
            f"{county.title()}\n"
            f"{score:.1f}"
        )
        font_weight = "bold"
    else:
        label = county.title()
        font_weight = "normal"

    axis.text(
        x_position + offset_x,
        y_position + offset_y,
        label,
        ha="center",
        va="center",
        fontsize=6.5,
        fontweight=font_weight,
        color="#222222",
        bbox={
            "facecolor": "white",
            "edgecolor": "none",
            "alpha": 0.58,
            "pad": 0.8,
        },
    )


colour_bar = figure.colorbar(
    collection,
    ax=axis,
    orientation="horizontal",
    fraction=0.035,
    pad=0.025,
    aspect=35,
)

colour_bar.set_label(
    "Renovation Priority Score (higher = more urgent)",
    fontsize=10,
)

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)

figure.savefig(
    PNG_FILE,
    dpi=200,
    bbox_inches="tight",
)

figure.savefig(
    SVG_FILE,
    bbox_inches="tight",
)

plt.close(figure)

print(f"Boundary polygons plotted: {len(patches):,}")
print(f"Counties mapped: {len(mapped_counties)}")
print(f"PNG map created: {PNG_FILE}")
print(f"SVG map created: {SVG_FILE}")