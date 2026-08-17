# Research data collection status

## A. Completed before this task

The repository already had working pipelines for CSO VAC14 vacancy, CSO EBA02 aggregate BER, Met Éireann county weather, CSO F2020 Census housing, Tailte county boundaries, the unchanged preliminary Renovation Priority Index, county archetype features, figures and `final_model_dataset_county_2024.csv` (26 counties). These were preserved.

## B. Newly collected

| Source/dataset | Year | Geography | Observations | Variables | Output |
|---|---:|---|---:|---:|---|
| CSO Census SAPS | 2022 | Small Area | 18,919 | 65 | `data\processed\census_demographic_features_small_area_2022.csv` |
| Tailte/CSO spatial features | 2022 | Small Area | 18,919 | 23 | `data\processed\spatial_features_small_area.csv` |
| Geography crosswalk | 2022 | Small Area | 18,919 | 18 | `data\processed\geography_crosswalk.csv` |
| Neighbour edge list | 2022 | Small Area pair | 110,124 | 3 | `data\processed\small_area_neighbors.csv` |
| Integrated public spatial features | 2022/2024 | Small Area | 18,919 | 97 | `data\processed\spatial_model_features_small_area.csv` |
| UK NEED transfer features | through 2023 | Dwelling | 45,459 | 17 | `data\interim\uk_need_transfer_features_2023.csv` |

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
