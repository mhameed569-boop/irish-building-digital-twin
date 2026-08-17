# Master data dictionary — Small Area public feature table

The modelling target is deliberately absent from the public table. Actual energy consumption will be supplied only inside the authorised secure environment.

| Variable | Description | Unit | Source | Year | Geography | Raw/Derived | Formula | Model Role |
|---|---|---|---|---|---|---|---|---|
| `census_year` | Census reference year | year | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | temporal identifier |
| `small_area_guid` | Stable official Small Area GUID | identifier | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `small_area_code` | Official published Small Area code | identifier | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `small_area_geogid` | Official Small Area geographic identifier | identifier | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `county_code` | County code | identifier | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `county_name` | County name | category | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | exclude-from-model |
| `electoral_division_guid` | Electoral division guid | identifier | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `electoral_division_code` | Electoral division code | identifier | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `electoral_division_name` | Electoral division name | category | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | exclude-from-model |
| `local_electoral_area_code` | Local electoral area code | identifier | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `nuts1_code` | Nuts1 code | identifier | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `nuts1_name` | Nuts1 name | category | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | exclude-from-model |
| `nuts2_code` | Nuts2 code | identifier | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `nuts2_name` | Nuts2 name | category | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | exclude-from-model |
| `nuts3_code` | Nuts3 code | identifier | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `nuts3_name` | Nuts3 name | category | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | exclude-from-model |
| `urban_area_flag` | Urban area flag | category | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | exclude-from-model |
| `urban_area_name` | Urban area name | category | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | exclude-from-model |
| `centroid_longitude` | Polygon centroid longitude | decimal degrees | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `centroid_latitude` | Polygon centroid latitude | decimal degrees | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `polygon_area_km2` | Official polygon area converted to square kilometres | km² | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Derived | — | predictor |
| `population_density_per_km2` | Population density per km2 | per km² | CSO Census 2022 SAPS | 2022 | Small Area | Derived | count / polygon_area_km2 | derived |
| `housing_density_per_km2` | Housing density per km2 | per km² | CSO Census 2022 SAPS | 2022 | Small Area | Derived | count / polygon_area_km2 | derived |
| `population` | Population | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `children_under_15` | Children under 15 | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `persons_65_plus` | Persons 65 plus | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `private_households` | Private households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `persons_in_private_households` | Persons in private households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `one_person_households` | One person households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `one_parent_households` | One parent households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `labour_status_population` | Labour status population | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `persons_at_work` | Persons at work | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `unemployed_persons` | Unemployed persons | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `retired_persons` | Retired persons | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `unable_to_work_persons` | Unable to work persons | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `education_population` | Education population | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `third_level_educated` | Third level educated | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `low_education` | Low education | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `total_housing_stock` | Total housing stock | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `occupied_dwellings` | Occupied dwellings | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `temporarily_absent_dwellings` | Temporarily absent dwellings | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `holiday_homes` | Holiday homes | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `other_vacant_dwellings` | Other vacant dwellings | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `house_or_bungalow_households` | House or bungalow households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `apartment_or_bedsit_households` | Apartment or bedsit households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `pre_2001_dwellings` | Pre 2001 dwellings | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `built_2016_or_later_dwellings` | Built 2016 or later dwellings | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `owner_occupied_households` | Owner occupied households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `private_rented_households` | Private rented households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `social_rented_households` | Social rented households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `oil_heated_households` | Oil heated households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `gas_heated_households` | Gas heated households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `electric_heated_households` | Electric heated households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `coal_or_peat_heated_households` | Coal or peat heated households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `no_central_heating_households` | No central heating households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `renewable_energy_households` | Renewable energy households | persons/households/dwellings as named | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | predictor |
| `average_household_size` | Persons in private households divided by private households | persons/household | CSO Census 2022 SAPS | 2022 | Small Area | Derived | persons_in_private_households / private_households | derived |
| `children_under_15_pct` | Derived percentage: Children under 15 | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `persons_65_plus_pct` | Derived percentage: Persons 65 plus | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `one_person_households_pct` | Derived percentage: One person households | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `one_parent_households_pct` | Derived percentage: One parent households | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `employment_pct` | Derived percentage: Employment | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `unemployment_pct` | Derived percentage: Unemployment | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `retired_pct` | Derived percentage: Retired | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `unable_to_work_pct` | Derived percentage: Unable to work | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `third_level_education_pct` | Derived percentage: Third level education | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `low_education_pct` | Derived percentage: Low education | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `occupied_dwellings_pct` | Derived percentage: Occupied dwellings | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `other_vacant_dwellings_pct` | Derived percentage: Other vacant dwellings | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `holiday_homes_pct` | Derived percentage: Holiday homes | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `house_or_bungalow_pct` | Derived percentage: House or bungalow | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `apartment_or_bedsit_pct` | Derived percentage: Apartment or bedsit | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `pre_2001_dwellings_pct` | Derived percentage: Pre 2001 dwellings | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `built_2016_or_later_pct` | Derived percentage: Built 2016 or later | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `owner_occupied_pct` | Derived percentage: Owner occupied | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `private_rented_pct` | Derived percentage: Private rented | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `social_rented_pct` | Derived percentage: Social rented | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `oil_heating_pct` | Derived percentage: Oil heating | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `gas_heating_pct` | Derived percentage: Gas heating | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `electric_heating_pct` | Derived percentage: Electric heating | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `coal_or_peat_heating_pct` | Derived percentage: Coal or peat heating | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `no_central_heating_pct` | Derived percentage: No central heating | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `renewable_energy_pct` | Derived percentage: Renewable energy | % | CSO Census 2022 SAPS | 2022 | Small Area | Derived | relevant numerator / denominator × 100 | derived |
| `urban_rural_code` | Urban rural code | identifier | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | spatial identifier |
| `urban_rural_class` | Urban rural class | category | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | exclude-from-model |
| `county_model_name` | Harmonised 26-county name for contextual joins | category | Tailte Éireann Small Area boundaries / CSO SAPS | 2022 | Small Area | Derived | — | diagnostic |
| `census_reference_year` | Census reference year | year | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | temporal identifier |
| `weather_reference_year` | Weather reference year | year | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | temporal identifier |
| `ber_reference_year` | Ber reference year | year | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | temporal identifier |
| `vacancy_reference_quarter` | Vacancy reference quarter | quarter | CSO Census 2022 SAPS | 2022 | Small Area | Raw/aggregated source | — | temporal identifier |
| `county_mean_temperature_c` | County annual mean temperature | °C | Met Éireann county averages | 2024 | County repeated as context | Raw/aggregated source | — | predictor |
| `county_annual_rainfall_mm` | County annual rainfall sum | mm | Met Éireann county averages | 2024 | County repeated as context | Raw/aggregated source | — | predictor |
| `county_heating_degree_days_base_15_5c` | Estimated annual heating degree days, base 15.5°C | degree-days | Met Éireann county averages | 2024 | County repeated as context | Raw/aggregated source | — | predictor |
| `county_poor_ber_pct` | Share of county BER records rated D, E or F-G | % | CSO EBA02 | 2024 | County repeated as context | Derived | relevant numerator / denominator × 100 | predictor |
| `county_ber_sample_dwellings` | County EBA02 sample denominator | dwellings | CSO EBA02 | 2024 | County repeated as context | Raw/aggregated source | — | diagnostic |
| `county_vacancy_rate_pct` | County vacancy rate used by preliminary indicator | % | CSO VAC14 / derived index | 2024Q4 | County repeated as context | Derived | relevant numerator / denominator × 100 | predictor |
| `county_renovation_priority_score` | Preliminary 50/50 vacancy and poor-BER indicator | 0–100 | CSO VAC14 / derived index | 2024Q4 | County repeated as context | Derived | 0.5 × vacancy min-max score + 0.5 × poor-BER min-max score | diagnostic |

## Target placeholder (documentation only)

`actual_energy_consumption`: target, kWh/dwelling/year or approved alternative; CSO COP BER / BER Energy RMF; restricted; **NOT AVAILABLE PUBLICLY and not represented by a fake numeric column**.
