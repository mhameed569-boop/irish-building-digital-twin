# Census Small Area feature dictionary

Selected from the official CSO Census 2022 SAPS rather than retaining all 795 raw columns. The selection represents population/occupancy demand, vulnerability and fuel-poverty context, housing form/age, tenure, heating technology and retrofit propensity.

| Variable | Meaning | Unit | Relevance / derivation |
|---|---|---|---|
| `census_year` | Census reference year | year | Candidate temporal identifier for residential energy-demand context. |
| `small_area_guid` | Stable official Small Area GUID | identifier | Candidate spatial identifier for residential energy-demand context. |
| `small_area_code` | Official published Small Area code | identifier | Candidate spatial identifier for residential energy-demand context. |
| `urban_rural_code` | Urban rural code | identifier | Candidate spatial identifier for residential energy-demand context. |
| `urban_rural_class` | Urban rural class | category | Candidate exclude-from-model for residential energy-demand context. |
| `population` | Population | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `children_under_15` | Children under 15 | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `persons_65_plus` | Persons 65 plus | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `private_households` | Private households | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `persons_in_private_households` | Persons in private households | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `one_person_households` | One person households | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `one_parent_households` | One parent households | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `labour_status_population` | Labour status population | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `persons_at_work` | Persons at work | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `unemployed_persons` | Unemployed persons | persons/households/dwellings as named | Socioeconomic/tenure proxy related to energy affordability and retrofit uptake. |
| `retired_persons` | Retired persons | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `unable_to_work_persons` | Unable to work persons | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `education_population` | Education population | persons/households/dwellings as named | Socioeconomic/tenure proxy related to energy affordability and retrofit uptake. |
| `third_level_educated` | Third level educated | persons/households/dwellings as named | Candidate predictor for residential energy-demand context. |
| `low_education` | Low education | persons/households/dwellings as named | Socioeconomic/tenure proxy related to energy affordability and retrofit uptake. |
| `total_housing_stock` | Total housing stock | persons/households/dwellings as named | Housing-stock form, occupancy, availability or construction-age context. |
| `occupied_dwellings` | Occupied dwellings | persons/households/dwellings as named | Housing-stock form, occupancy, availability or construction-age context. |
| `temporarily_absent_dwellings` | Temporarily absent dwellings | persons/households/dwellings as named | Housing-stock form, occupancy, availability or construction-age context. |
| `holiday_homes` | Holiday homes | persons/households/dwellings as named | Housing-stock form, occupancy, availability or construction-age context. |
| `other_vacant_dwellings` | Other vacant dwellings | persons/households/dwellings as named | Housing-stock form, occupancy, availability or construction-age context. |
| `house_or_bungalow_households` | House or bungalow households | persons/households/dwellings as named | Housing-stock form, occupancy, availability or construction-age context. |
| `apartment_or_bedsit_households` | Apartment or bedsit households | persons/households/dwellings as named | Housing-stock form, occupancy, availability or construction-age context. |
| `pre_2001_dwellings` | Pre 2001 dwellings | persons/households/dwellings as named | Housing-stock form, occupancy, availability or construction-age context. |
| `built_2016_or_later_dwellings` | Built 2016 or later dwellings | persons/households/dwellings as named | Housing-stock form, occupancy, availability or construction-age context. |
| `owner_occupied_households` | Owner occupied households | persons/households/dwellings as named | Socioeconomic/tenure proxy related to energy affordability and retrofit uptake. |
| `private_rented_households` | Private rented households | persons/households/dwellings as named | Socioeconomic/tenure proxy related to energy affordability and retrofit uptake. |
| `social_rented_households` | Social rented households | persons/households/dwellings as named | Socioeconomic/tenure proxy related to energy affordability and retrofit uptake. |
| `oil_heated_households` | Oil heated households | persons/households/dwellings as named | Heating technology/fuel and retrofit/decarbonisation relevance. |
| `gas_heated_households` | Gas heated households | persons/households/dwellings as named | Heating technology/fuel and retrofit/decarbonisation relevance. |
| `electric_heated_households` | Electric heated households | persons/households/dwellings as named | Heating technology/fuel and retrofit/decarbonisation relevance. |
| `coal_or_peat_heated_households` | Coal or peat heated households | persons/households/dwellings as named | Heating technology/fuel and retrofit/decarbonisation relevance. |
| `no_central_heating_households` | No central heating households | persons/households/dwellings as named | Heating technology/fuel and retrofit/decarbonisation relevance. |
| `renewable_energy_households` | Renewable energy households | persons/households/dwellings as named | Heating technology/fuel and retrofit/decarbonisation relevance. |
| `average_household_size` | Persons in private households divided by private households | persons/household | Occupancy-intensity proxy; persons_in_private_households / private_households. |
| `children_under_15_pct` | Derived percentage: Children under 15 | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `persons_65_plus_pct` | Derived percentage: Persons 65 plus | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `one_person_households_pct` | Derived percentage: One person households | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `one_parent_households_pct` | Derived percentage: One parent households | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `employment_pct` | Derived percentage: Employment | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `unemployment_pct` | Derived percentage: Unemployment | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `retired_pct` | Derived percentage: Retired | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `unable_to_work_pct` | Derived percentage: Unable to work | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `third_level_education_pct` | Derived percentage: Third level education | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `low_education_pct` | Derived percentage: Low education | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `occupied_dwellings_pct` | Derived percentage: Occupied dwellings | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `other_vacant_dwellings_pct` | Derived percentage: Other vacant dwellings | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `holiday_homes_pct` | Derived percentage: Holiday homes | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `house_or_bungalow_pct` | Derived percentage: House or bungalow | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `apartment_or_bedsit_pct` | Derived percentage: Apartment or bedsit | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `pre_2001_dwellings_pct` | Derived percentage: Pre 2001 dwellings | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `built_2016_or_later_pct` | Derived percentage: Built 2016 or later | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `owner_occupied_pct` | Derived percentage: Owner occupied | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `private_rented_pct` | Derived percentage: Private rented | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `social_rented_pct` | Derived percentage: Social rented | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `oil_heating_pct` | Derived percentage: Oil heating | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `gas_heating_pct` | Derived percentage: Gas heating | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `electric_heating_pct` | Derived percentage: Electric heating | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `coal_or_peat_heating_pct` | Derived percentage: Coal or peat heating | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `no_central_heating_pct` | Derived percentage: No central heating | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |
| `renewable_energy_pct` | Derived percentage: Renewable energy | % | Derived as numerator / relevant population, household or housing denominator × 100; blank when denominator is zero. |

## Modelling cautions

Counts and their directly derived percentages are mathematically dependent; feature-selection pipelines must choose a non-redundant representation. Composition groups do not necessarily exhaust every Census category, so omitted categories are not zeros. Three Small Areas have zero denominators for some percentages and remain blank rather than being fabricated.
