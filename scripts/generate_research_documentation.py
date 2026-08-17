"""Generate dictionaries, provenance manifest, and collection status."""

import csv
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
DOCS = ROOT / "docs"
METADATA = ROOT / "data" / "metadata"
OUTPUTS = ROOT / "outputs"


def header(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return next(csv.reader(file))


def dimensions(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        columns = len(next(reader))
        rows = sum(1 for _ in reader)
    return rows, columns


def describe(name):
    exact = {
        "census_year": ("Census reference year", "year", "temporal identifier"),
        "small_area_guid": ("Stable official Small Area GUID", "identifier", "spatial identifier"),
        "small_area_code": ("Official published Small Area code", "identifier", "spatial identifier"),
        "small_area_geogid": ("Official Small Area geographic identifier", "identifier", "spatial identifier"),
        "county_model_name": ("Harmonised 26-county name for contextual joins", "category", "diagnostic"),
        "centroid_longitude": ("Polygon centroid longitude", "decimal degrees", "spatial identifier"),
        "centroid_latitude": ("Polygon centroid latitude", "decimal degrees", "spatial identifier"),
        "polygon_area_km2": ("Official polygon area converted to square kilometres", "km²", "predictor"),
        "average_household_size": ("Persons in private households divided by private households", "persons/household", "derived"),
        "county_renovation_priority_score": ("Preliminary 50/50 vacancy and poor-BER indicator", "0–100", "diagnostic"),
        "county_poor_ber_pct": ("Share of county BER records rated D, E or F-G", "%", "predictor"),
        "county_ber_sample_dwellings": ("County EBA02 sample denominator", "dwellings", "diagnostic"),
        "county_vacancy_rate_pct": ("County vacancy rate used by preliminary indicator", "%", "predictor"),
        "county_mean_temperature_c": ("County annual mean temperature", "°C", "predictor"),
        "county_annual_rainfall_mm": ("County annual rainfall sum", "mm", "predictor"),
        "county_heating_degree_days_base_15_5c": ("Estimated annual heating degree days, base 15.5°C", "degree-days", "predictor"),
    }
    if name in exact:
        return exact[name]
    label = name.replace("_", " ").capitalize()
    if name.endswith("_pct"):
        return (f"Derived percentage: {label[:-4]}", "%", "derived")
    if name.endswith("_density_per_km2"):
        return (label, "per km²", "derived")
    if name.endswith("_year") or "reference_year" in name:
        return (label, "year", "temporal identifier")
    if name.endswith("_quarter"):
        return (label, "quarter", "temporal identifier")
    if "guid" in name or name.endswith("_code") or name in {"nuts1_code", "nuts2_code", "nuts3_code"}:
        return (label, "identifier", "spatial identifier")
    if name.endswith("_name") or name.endswith("_class") or name.endswith("_flag"):
        return (label, "category", "exclude-from-model")
    return (label, "persons/households/dwellings as named", "predictor")


def source_for(column):
    if column.startswith("county_mean") or "rainfall" in column or "degree_days" in column:
        return "Met Éireann county averages", "2024", "County repeated as context"
    if "county_ber" in column or "poor_ber" in column:
        return "CSO EBA02", "2024", "County repeated as context"
    if "county_vacancy" in column or "priority" in column:
        return "CSO VAC14 / derived index", "2024Q4", "County repeated as context"
    spatial_tokens = ("small_area", "county_", "electoral_division", "local_electoral", "nuts", "urban_area", "centroid", "polygon_area", "density")
    if column.startswith(spatial_tokens):
        return "Tailte Éireann Small Area boundaries / CSO SAPS", "2022", "Small Area"
    return "CSO Census 2022 SAPS", "2022", "Small Area"


def write_census_dictionary(columns):
    lines = [
        "# Census Small Area feature dictionary",
        "",
        "Selected from the official CSO Census 2022 SAPS rather than retaining all 795 raw columns. The selection represents population/occupancy demand, vulnerability and fuel-poverty context, housing form/age, tenure, heating technology and retrofit propensity.",
        "",
        "| Variable | Meaning | Unit | Relevance / derivation |",
        "|---|---|---|---|",
    ]
    for column in columns:
        description, unit, role = describe(column)
        if column.endswith("_pct"):
            relevance = "Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero."
        elif column == "average_household_size":
            relevance = "Occupancy-intensity proxy; persons_in_private_households / private_households."
        elif "heating" in column or "heated" in column or "renewable" in column:
            relevance = "Heating technology/fuel and retrofit/decarbonisation relevance."
        elif any(token in column for token in ("employment", "unemployed", "education", "tenure", "rented", "owner")):
            relevance = "Socioeconomic/tenure proxy related to energy affordability and retrofit uptake."
        elif any(token in column for token in ("dwellings", "housing", "house_", "apartment", "holiday")):
            relevance = "Housing-stock form, occupancy, availability or construction-age context."
        else:
            relevance = f"Candidate {role} for residential energy-demand context."
        lines.append(f"| `{column}` | {description} | {unit} | {relevance} |")
    lines.extend([
        "", "## Modelling cautions", "",
        "Counts and their directly derived percentages are mathematically dependent; feature-selection pipelines must choose a non-redundant representation. Composition groups do not necessarily exhaust every Census category, so omitted categories are not zeros. Three Small Areas have zero denominators for some percentages and remain blank rather than being fabricated.",
    ])
    (DOCS / "census_feature_dictionary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_master_dictionary(columns):
    lines = [
        "# Master data dictionary — Small Area public feature table", "",
        "The modelling target is deliberately absent from the public table. Actual energy consumption will be supplied only inside the authorised secure environment.", "",
        "| Variable | Description | Unit | Source | Year | Geography | Raw/Derived | Formula | Model Role |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for column in columns:
        description, unit, role = describe(column)
        source, year, geography = source_for(column)
        derived = "Derived" if column.endswith("_pct") or "density" in column or column in {"average_household_size", "polygon_area_km2", "county_renovation_priority_score", "county_model_name"} else "Raw/aggregated source"
        if column.endswith("_pct"):
            formula = "relevant numerator / denominator × 100"
        elif "density" in column:
            formula = "count / polygon_area_km2"
        elif column == "average_household_size":
            formula = "persons_in_private_households / private_households"
        elif column == "county_renovation_priority_score":
            formula = "0.5 × vacancy min-max score + 0.5 × poor-BER min-max score"
        else:
            formula = "—"
        lines.append(f"| `{column}` | {description} | {unit} | {source} | {year} | {geography} | {derived} | {formula} | {role} |")
    lines.extend(["", "## Target placeholder (documentation only)", "", "`actual_energy_consumption`: target, kWh/dwelling/year or approved alternative; CSO COP BER / BER Energy RMF; restricted; **NOT AVAILABLE PUBLICLY and not represented by a fake numeric column**."])
    (DOCS / "master_data_dictionary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest():
    rows = [
        ["CSO", "VAC14", "https://data.cso.ie/table/VAC14", "2024Q4", "CSO reuse terms", "scripts/download_cso_vacancy.py", "data/raw/cso_vac14.csv", "data/processed/latest_vacancy_rates.csv", "API CSV; latest-quarter rates", "existing"],
        ["CSO", "EBA02", "https://data.cso.ie/table/EBA02", "2024", "CSO reuse terms", "scripts/download_cso_ber.py", "data/raw/cso_eba02_ber.json", "data/processed/ber_by_county_2024.csv", "PxStat JSON; county aggregation; poor BER=D/E/F-G", "existing"],
        ["Met Éireann", "County climate averages", "https://clidata.met.ie/cli/grids/county/averages.html", "2024", "CC BY 4.0", "scripts/download_met_eireann_weather.py", "data/raw/met_eireann_county_weather.csv", "data/processed/weather_by_county_2024.csv", "monthly-to-annual aggregation; HDD base 15.5°C", "existing"],
        ["CSO", "F2020", "https://data.cso.ie/table/F2020", "2022", "CSO reuse terms", "scripts/download_cso_census_housing.py", "data/raw/cso_f2020_census_housing.json", "data/processed/census_housing_by_county_2022.csv", "county aggregation and dwelling composition", "existing"],
        ["CSO", "Census 2022 SAPS Small Area", "https://www.cso.ie/en/census/census2022/census2022smallareapopulationstatistics/", "2022", "CSO reuse terms", "scripts/download_small_area_census.py", "data/raw/cso_saps_2022_small_area.csv", "data/processed/census_demographic_features_small_area_2022.csv", "selected energy-relevant counts and derived percentages", str(date.today())],
        ["Tailte Éireann", "SMALL_AREA_2022_Genralised_20m_view", "https://services-eu1.arcgis.com/BuS9rtTsYEV5C0xh/arcgis/rest/services/SMALL_AREA_2022_Genralised_20m_view/FeatureServer/0", "2022", "CC BY 4.0", "scripts/download_small_area_boundaries.py", "data/raw/ireland_small_areas_2022_generalised_20m.geojson", "data/processed/spatial_features_small_area.csv", "paged GeoJSON in WGS84; centroids, area, density, crosswalk, neighbours", str(date.today())],
        ["UK DESNZ", "NEED anonymised 2025 50k", "https://www.gov.uk/government/statistics/national-energy-efficiency-data-framework-need-anonymised-data-2025", "through 2023", "Open Government Licence", "scripts/download_uk_need_sample.py", "data/raw/international/anon2025_50k.csv", "data/interim/uk_need_transfer_features_2023.csv", "valid electricity records; gas kept only with valid flag", str(date.today())],
    ]
    path = METADATA / "source_manifest.csv"
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["provider", "dataset_id", "official_url", "reference_period", "licence", "script", "raw_file", "processed_output", "transformations", "download_or_audit_date"])
        writer.writerows(rows)


def write_provenance():
    text = """# Data provenance

Machine-readable records are in `data/metadata/source_manifest.csv`. Downloads are performed only from the official provider URLs recorded there; public raw downloads are ignored by Git and can be recreated by their scripts.

## Transformation chain

1. CSO SAPS CSV → energy-relevant Census counts and documented percentage features (`process_small_area_features.py`).
2. Tailte Éireann paged GeoJSON → official crosswalk, WGS84 centroids, source-area conversion, population/housing densities and an adjacency edge list (`build_small_area_spatial_features.py`).
3. Census + spatial table → 18,919-row public Small Area table, with 2024 county weather/BER/vacancy fields clearly labelled as county context (`build_spatial_model_features.py`).
4. UK NEED official CSV → harmonised transfer table after validity-flag filtering; actual electricity remains separate from weather-corrected gas (`process_uk_need_sample.py`).
5. `validate_research_datasets.py` reports counts, joins, ranges, dependencies, coordinates, missingness and target absence without silently dropping records.

The run date is not the statistical reference year. Reference years are columns in integrated outputs and are documented in `temporal_alignment.md`. Licences and provider attribution remain governed by the original official sources.
"""
    (DOCS / "data_provenance.md").write_text(text, encoding="utf-8")


def write_status():
    new_files = [
        ("CSO Census SAPS", PROCESSED / "census_demographic_features_small_area_2022.csv", "2022", "Small Area"),
        ("Tailte/CSO spatial features", PROCESSED / "spatial_features_small_area.csv", "2022", "Small Area"),
        ("Geography crosswalk", PROCESSED / "geography_crosswalk.csv", "2022", "Small Area"),
        ("Neighbour edge list", PROCESSED / "small_area_neighbors.csv", "2022", "Small Area pair"),
        ("Integrated public spatial features", PROCESSED / "spatial_model_features_small_area.csv", "2022/2024", "Small Area"),
        ("UK NEED transfer features", ROOT / "data" / "interim" / "uk_need_transfer_features_2023.csv", "through 2023", "Dwelling"),
    ]
    table = []
    for source, path, year, geography in new_files:
        rows, columns = dimensions(path)
        table.append(f"| {source} | {year} | {geography} | {rows:,} | {columns:,} | `{path.relative_to(ROOT)}` |")
    text = f"""# Research data collection status

## A. Completed before this task

The repository already had working pipelines for CSO VAC14 vacancy, CSO EBA02 aggregate BER, Met Éireann county weather, CSO F2020 Census housing, Tailte county boundaries, the unchanged preliminary Renovation Priority Index, county archetype features, figures and `final_model_dataset_county_2024.csv` (26 counties). These were preserved.

## B. Newly collected

| Source/dataset | Year | Geography | Observations | Variables | Output |
|---|---:|---|---:|---:|---|
{chr(10).join(table)}

Official SAPS glossary metadata is stored at `data/metadata/cso_saps_2022_glossary.xlsx`. Public processing now produces 18,919 Small Areas, 110,124 directed neighbour links and zero failed census/spatial/county-context joins.

## C. Remaining restricted data

The actual-energy dependent variable remains restricted. Apply for CSO **Census of Population BER Energy (COP BER), 2022** and/or **BER Energy RMFs 2016–2024** through the Researcher Data Portal. Record-level electricity/gas, BER and Census data must stay inside the secure environment. UK SERL is an additional restricted international candidate. See `docs/restricted_energy_data_plan.md`.

## D. Remaining research gaps

- No public Irish dwelling-level actual energy target; BER is theoretical and is not a substitute.
- Public BER, weather and vacancy context remain county-level when repeated onto Small Areas.
- Met Éireann 1 km temperature/rainfall aggregation is a useful future climate refinement; official fine-grid wind and solar products still require confirmation.
- Three Small Areas have legitimate zero denominators in several percentage fields; missingness must be handled explicitly.
- Target linkage, disclosure rules, spatial folds, feature selection and multicollinearity screening must be completed inside/after the authorised workflow.
- Satellite land-cover features are deferred until baseline ablation testing shows a need.

## E. Recommended next step

The foundation is sufficient to begin **exploratory public-data spatial analysis, spatial-weight design and an international NEED transfer-learning prototype**. It is **not yet sufficient to train Phase 1 supervised Spatial Machine Learning for actual Irish residential consumption**. The exact blocker is authorised access to COP BER/BER Energy actual electricity/gas data and a disclosure-approved, linkable target table. After access: validate the secure schema, define annual kWh targets, join authorised geography/time IDs, and construct leakage-safe spatial holdout folds before fitting Random Forest/XGBoost/MGWR baselines.
"""
    (OUTPUTS / "research_data_collection_status.md").write_text(text, encoding="utf-8")


def main():
    census_columns = header(PROCESSED / "census_demographic_features_small_area_2022.csv")
    model_columns = header(PROCESSED / "spatial_model_features_small_area.csv")
    DOCS.mkdir(exist_ok=True)
    METADATA.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(exist_ok=True)
    write_census_dictionary(census_columns)
    write_master_dictionary(model_columns)
    write_manifest()
    write_provenance()
    write_status()
    print("Generated dictionaries, provenance manifest, and collection status.")


if __name__ == "__main__":
    main()
