"""Create Small Area crosswalk, geometry, density, and adjacency features."""

import csv
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
BOUNDARY_FILE = (
    PROJECT_FOLDER
    / "data"
    / "raw"
    / "ireland_small_areas_2022_generalised_20m.geojson"
)
CENSUS_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "census_demographic_features_small_area_2022.csv"
)
SPATIAL_FILE = (
    PROJECT_FOLDER / "data" / "processed" / "spatial_features_small_area.csv"
)
CROSSWALK_FILE = (
    PROJECT_FOLDER / "data" / "processed" / "geography_crosswalk.csv"
)
NEIGHBOUR_FILE = (
    PROJECT_FOLDER / "data" / "processed" / "small_area_neighbors.csv"
)


def exterior_rings(geometry):
    if geometry["type"] == "Polygon":
        polygons = [geometry["coordinates"]]
    elif geometry["type"] == "MultiPolygon":
        polygons = geometry["coordinates"]
    else:
        return []
    return [polygon[0] for polygon in polygons if polygon and polygon[0]]


def ring_centroid(ring):
    twice_area = 0.0
    centroid_x = 0.0
    centroid_y = 0.0
    for first, second in zip(ring, ring[1:]):
        x1, y1 = first[:2]
        x2, y2 = second[:2]
        cross = x1 * y2 - x2 * y1
        twice_area += cross
        centroid_x += (x1 + x2) * cross
        centroid_y += (y1 + y2) * cross
    if twice_area == 0:
        points = ring[:-1] or ring
        return 0.0, sum(p[0] for p in points) / len(points), sum(
            p[1] for p in points
        ) / len(points)
    return (
        abs(twice_area / 2),
        centroid_x / (3 * twice_area),
        centroid_y / (3 * twice_area),
    )


def geometry_centroid(geometry):
    pieces = [ring_centroid(ring) for ring in exterior_rings(geometry)]
    total_area = sum(piece[0] for piece in pieces)
    if total_area:
        return (
            sum(area * x for area, x, _ in pieces) / total_area,
            sum(area * y for area, _, y in pieces) / total_area,
        )
    points = [point for ring in exterior_rings(geometry) for point in ring]
    return (
        sum(point[0] for point in points) / len(points),
        sum(point[1] for point in points) / len(points),
    )


def main():
    with CENSUS_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        census = {row["small_area_guid"]: row for row in csv.DictReader(file)}
    with BOUNDARY_FILE.open("r", encoding="utf-8") as file:
        boundaries = json.load(file)

    crosswalk_rows = []
    spatial_rows = []
    vertex_owners = defaultdict(list)
    missing_census = []

    for feature in boundaries["features"]:
        properties = feature["properties"]
        guid = properties["SA_GUID_2022"]
        census_row = census.get(guid)
        if census_row is None:
            missing_census.append(guid)
            continue

        longitude, latitude = geometry_centroid(feature["geometry"])
        area_km2 = float(properties.get("Shape__Area") or 0) / 1_000_000
        population = float(census_row["population"] or 0)
        housing = float(census_row["total_housing_stock"] or 0)

        common = {
            "census_year": 2022,
            "small_area_guid": guid,
            "small_area_code": properties["SA_PUB2022"],
            "small_area_geogid": properties["SA_GEOGID_2022"],
            "county_code": properties["COUNTY_CODE"],
            "county_name": properties["COUNTY_ENGLISH"],
            "electoral_division_guid": properties["ED_GUID"],
            "electoral_division_code": properties["ED_ID_STR"],
            "electoral_division_name": properties["ED_ENGLISH"],
            "local_electoral_area_code": properties["CSO_LEA"],
            "nuts1_code": properties["SA_NUTS1"],
            "nuts1_name": properties["SA_NUTS1_NAME"],
            "nuts2_code": properties["SA_NUTS2"],
            "nuts2_name": properties["SA_NUTS2_NAME"],
            "nuts3_code": properties["SA_NUTS3"],
            "nuts3_name": properties["SA_NUTS3_NAME"],
            "urban_area_flag": properties["SA_URBAN_AREA_FLAG"],
            "urban_area_name": properties["SA_URBAN_AREA_NAME"],
        }
        crosswalk_rows.append(common)
        spatial_rows.append(
            {
                **common,
                "centroid_longitude": round(longitude, 7),
                "centroid_latitude": round(latitude, 7),
                "polygon_area_km2": round(area_km2, 6),
                "population_density_per_km2": round(population / area_km2, 4)
                if area_km2
                else "",
                "housing_density_per_km2": round(housing / area_km2, 4)
                if area_km2
                else "",
            }
        )

        vertices = {
            (round(point[0], 6), round(point[1], 6))
            for ring in exterior_rings(feature["geometry"])
            for point in ring
        }
        for vertex in vertices:
            vertex_owners[vertex].append(guid)

    neighbour_pairs = set()
    for owners in vertex_owners.values():
        if len(owners) > 1:
            for first, second in combinations(sorted(set(owners)), 2):
                neighbour_pairs.add((first, second))

    CROSSWALK_FILE.parent.mkdir(parents=True, exist_ok=True)
    for path, rows in [(CROSSWALK_FILE, crosswalk_rows), (SPATIAL_FILE, spatial_rows)]:
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    with NEIGHBOUR_FILE.open("w", encoding="utf-8-sig", newline="") as file:
        fieldnames = ["small_area_guid", "neighbor_small_area_guid", "weight"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for first, second in sorted(neighbour_pairs):
            writer.writerow(
                {
                    "small_area_guid": first,
                    "neighbor_small_area_guid": second,
                    "weight": 1,
                }
            )
            writer.writerow(
                {
                    "small_area_guid": second,
                    "neighbor_small_area_guid": first,
                    "weight": 1,
                }
            )

    print(f"Spatial features: {len(spatial_rows):,}")
    print(f"Directed neighbour links: {len(neighbour_pairs) * 2:,}")
    print(f"Missing Census joins: {len(missing_census):,}")
    print(f"Created: {SPATIAL_FILE}")
    print(f"Created: {CROSSWALK_FILE}")
    print(f"Created: {NEIGHBOUR_FILE}")


if __name__ == "__main__":
    main()
