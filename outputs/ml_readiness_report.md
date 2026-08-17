# Machine-learning readiness assessment

Generated from `data\processed\spatial_model_features_small_area.csv`.

## Dataset profile

- Geographic resolution: Census 2022 Small Area
- Observations: 18,919
- Columns: 97
- Candidate predictors before formal feature selection: 75
- Continuous/numeric-like columns: 76
- Categorical columns: 14
- Directed neighbour links: 110,124
- Actual metered-energy target: **NOT AVAILABLE IN THE PUBLIC DATASET**

## Missingness

- `apartment_or_bedsit_pct`: 3 missing
- `average_household_size`: 3 missing
- `built_2016_or_later_pct`: 3 missing
- `coal_or_peat_heating_pct`: 3 missing
- `electric_heating_pct`: 3 missing
- `gas_heating_pct`: 3 missing
- `holiday_homes_pct`: 3 missing
- `house_or_bungalow_pct`: 3 missing
- `low_education_pct`: 1 missing
- `no_central_heating_pct`: 3 missing
- `occupied_dwellings_pct`: 3 missing
- `oil_heating_pct`: 3 missing
- `one_parent_households_pct`: 3 missing
- `one_person_households_pct`: 3 missing
- `other_vacant_dwellings_pct`: 3 missing
- `owner_occupied_pct`: 3 missing
- `pre_2001_dwellings_pct`: 3 missing
- `private_rented_pct`: 3 missing
- `renewable_energy_pct`: 3 missing
- `social_rented_pct`: 3 missing
- `third_level_education_pct`: 1 missing
- `urban_area_name`: 5,734 missing

Blank `urban_area_name` values are expected outside named urban areas. Three Small Areas have zero denominators for several percentages; they remain reported and were not silently removed.

## Redundancy and multicollinearity risks

- census_year = census_reference_year
- weather_reference_year = ber_reference_year in the current snapshot
- counts and their derived percentage variables must not be entered together without feature selection
- county context repeats across Small Areas and must not be treated as fine-resolution measurements

Constant/reference fields to exclude from model matrices: `census_year`, `nuts1_code`, `nuts1_name`, `census_reference_year`, `weather_reference_year`, `ber_reference_year`, `vacancy_reference_quarter`.

## Readiness by method

| Method | Status | Reason |
|---|---|---|
| Random Forest | CONDITIONAL | Predictor matrix is adequate, but the authorised actual-energy target must first be joined and spatial leakage controlled. |
| XGBoost | CONDITIONAL | Same target requirement; encode categorical fields and use grouped/spatial validation. |
| MLP | NOT READY | No public target; scaling, encoding, feature reduction, and sufficient linked records are still required. |
| MGWR | CONDITIONAL | Coordinates, fine geography and neighbours exist; a continuous authorised target and multicollinearity screening are required. |
| Spatial holdout validation | READY FOR DESIGN | Official IDs, centroids and adjacency are available; define geographically separated folds after target linkage. |

## Decision

The repository is ready for **public-data feature engineering and unsupervised/exploratory spatial analysis**, but not for supervised prediction of actual residential consumption. Phase 1 supervised Spatial ML begins only after authorised COP-BER/BER Energy data are processed within the CSO Researcher Data Portal and an approved, linkable analysis table is available.
