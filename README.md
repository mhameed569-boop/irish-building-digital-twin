# Irish Building Digital Twin

A reproducible research pipeline for analysing residential building
energy performance, vacancy, weather, housing characteristics, and
retrofit priorities across the 26 counties of Ireland.

## Research Purpose

The project combines official aggregated datasets to support:

- Identification of counties with high retrofit priority
- Analysis of residential vacancy and poor BER performance
- Discovery of county-level building energy archetypes
- Integration of climate, housing stock, construction period,
  dwelling type, and heating-fuel characteristics
- Development of future retrofit and decarbonisation models

## Data Sources

### 1. CSO VAC14 — Residential Vacancy

Official dataset:

https://data.cso.ie/table/VAC14

Variables used:

- Number of vacant dwellings
- Vacancy rate
- Local authority
- Quarter and year

Reference period used: 2024Q4.

### 2. CSO EBA02 — Domestic Building Energy Rating

Official dataset:

https://data.cso.ie/table/EBA02

Variables used:

- BER rating
- Dwelling type
- Main space-heating fuel
- Period of construction
- County

Reference year used: 2024.

Poor BER is defined in this project as ratings D, E, or F-G.

### 3. Met Éireann — County Climate Averages

Official dataset:

https://clidata.met.ie/cli/grids/county/averages.html

Variables used:

- Monthly mean temperature
- Monthly minimum temperature
- Monthly maximum temperature
- Monthly rainfall
- Estimated Heating Degree Days

Reference year used: 2024.

Heating Degree Days are estimated using a base temperature of 15.5°C.

### 4. CSO F2020 — Census Housing Stock

Official dataset:

https://data.cso.ie/table/F2020

Variables used:

- Total housing stock
- Occupied dwellings
- Vacant dwellings
- Holiday homes
- Detached houses
- Semi-detached houses
- Terraced houses
- Apartments

Reference year used: Census 2022.

### 5. Tailte Éireann — County Boundaries

Official county boundary GeoJSON is used to create the renovation
priority map.

The raw boundary file is downloaded automatically and is not stored
in the GitHub repository.

## Renovation Priority Index

The experimental Renovation Priority Score combines:

- 50% normalised vacancy-rate component
- 50% normalised poor-BER component

Both components are min-max normalised from 0 to 100.

A higher score indicates a county with a stronger combined signal of
residential vacancy and poor energy performance.

This is a research indicator and is not an official government index.

## Final Model Dataset

The main integrated output is:

```text
data/processed/final_model_dataset_county_2024.csv
```

It contains one row for each of Ireland's 26 counties and combines:

- Vacancy rate
- Poor BER percentage
- Renovation priority score and rank
- Temperature and rainfall
- Heating Degree Days
- Housing stock and occupancy
- Dwelling-type composition
- Heating-fuel composition
- Construction-period composition
- Dominant county energy archetype characteristics

The analysis combines 2024 vacancy, BER, and weather observations with
2022 Census housing characteristics. The reference years are retained
in the dataset and must be considered when interpreting results.

## Project Structure

```text
scripts/
    download_cso_vacancy.py
    summarize_vacancy.py
    download_cso_ber.py
    inspect_cso_ber.py
    summarize_ber.py
    build_renovation_priority.py
    plot_renovation_priority.py
    download_county_boundaries.py
    inspect_county_boundaries.py
    plot_renovation_priority_map.py
    download_met_eireann_weather.py
    summarize_weather.py
    download_cso_census_housing.py
    inspect_cso_census_housing.py
    summarize_census_housing.py
    build_model_dataset.py
    summarize_energy_archetypes.py
    build_final_model_dataset.py

data/
    raw/
        Downloaded source data — excluded from GitHub
    processed/
        Aggregated and reproducible research outputs

outputs/
    figures/
        Research charts and county maps
```

## How to Run

Run the scripts from the repository root in the following order.

### Download source data

```bash
python scripts/download_cso_vacancy.py
python scripts/download_cso_ber.py
python scripts/download_met_eireann_weather.py
python scripts/download_cso_census_housing.py
python scripts/download_county_boundaries.py
```

### Process the datasets

```bash
python scripts/summarize_vacancy.py
python scripts/summarize_ber.py
python scripts/summarize_weather.py
python scripts/summarize_census_housing.py
python scripts/summarize_energy_archetypes.py
```

### Build the integrated datasets

```bash
python scripts/build_renovation_priority.py
python scripts/build_model_dataset.py
python scripts/build_final_model_dataset.py
```

### Create the figures

```bash
python scripts/plot_renovation_priority.py
python scripts/plot_renovation_priority_map.py
```

## Main Outputs

```text
data/processed/latest_vacancy_rates.csv
data/processed/ber_by_county_2024.csv
data/processed/weather_by_county_2024.csv
data/processed/census_housing_by_county_2022.csv
data/processed/energy_archetype_features_by_county_2024.csv
data/processed/renovation_priority_by_county_2024.csv
data/processed/final_model_dataset_county_2024.csv

outputs/figures/renovation_priority_top10.png
outputs/figures/renovation_priority_map_2024.png
```

## Requirements

- Python 3
- Matplotlib

The data-processing scripts mainly use Python's standard library.
The map is generated without requiring GeoPandas.

## Data Protection

Raw datasets are excluded from GitHub through `.gitignore`.

Restricted CSO Research Microdata Files must never be uploaded to
GitHub. The CSO COP BER and BER Energy Research Microdata Files must
remain inside the secure CSO Researcher Data Portal.

Only non-confidential code and approved aggregated outputs may be
stored in this repository.

## Attribution

This project uses data from:

- Central Statistics Office Ireland
- Met Éireann
- Tailte Éireann

Users must review and follow the licence and attribution requirements
of each original data provider.