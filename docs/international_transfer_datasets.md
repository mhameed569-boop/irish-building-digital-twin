# International transfer-learning datasets

| Rank | Dataset | Country/provider | Coverage and size | Energy target | Building/geography variables | Access/licence | Irish compatibility | Recommendation |
|---|---|---|---|---|---|---|---|---|
| HIGH | National Energy Efficiency Data-Framework (NEED) anonymised data 2025, 50k sample | UK DESNZ | 50,000 dwellings; annual series to 2023 | Metered electricity; weather-corrected gas, kWh | property type, age/floor bands, EPC, fuel, efficiency flags, region | Public CSV, Open Government Licence | Closest open match to Irish BER/building/energy variables; climate and definitions still require domain adaptation | INCLUDE for feature/representation pretraining and sensitivity tests |
| HIGH/RESTRICTED | Smart Energy Research Lab (SERL) Observatory, Study 8666 | UK SERL/UK Data Service | about 13,000 homes, longitudinal half-hourly | gas/electricity smart-meter readings | EPC, weather, dwelling and household attributes | SecureLab application | Excellent resolution, but separate authorisation and UK selection/domain shift | APPLY only if justified and resourced |
| MEDIUM | Smart-Grid Smart-City Customer Trial Data | Australia, Australian Government | trial customers, 2010–2014 | half-hour electricity | household/trial/demographic fields and geography | Public, CC BY 3.0 | Actual use is valuable; old period, Australian climate/grid and sample selection reduce direct transfer | DEFER until Irish/UK baseline |
| MEDIUM/LOW | Solar Home Electricity Data | Australia, Ausgrid | 300 half-hourly solar homes; larger monthly cohort, 2010–2013 | consumption and PV generation | limited household/geographic context | Public, CC BY 3.0 | Useful for PV/load-shape methods, weaker for national Irish archetypes | OPTIONAL specialised experiment |

## Reproducible public acquisition

`scripts/download_uk_need_sample.py` downloads the official NEED 50k CSV and official metadata ODS. `scripts/process_uk_need_sample.py` preserves only records with valid electricity flags and separates actual electricity from weather-corrected gas. Output is `data/interim/uk_need_transfer_features_2023.csv`; raw and interim large files are ignored by Git.

Official URLs:

- NEED publication: <https://www.gov.uk/government/statistics/national-energy-efficiency-data-framework-need-anonymised-data-2025>
- NEED 50k CSV: <https://assets.publishing.service.gov.uk/media/685c01cec07c71e5a8709834/anon2025_50k.csv>
- SERL catalogue: <https://datacatalogue.ukdataservice.ac.uk/studies/study?id=8666>
- Australian SGSC: <https://www.data.gov.au/data/dataset/smart-grid-smart-city-customer-trial-data>

Transfer learning must compare units, target construction, weather correction, stock distributions, reference period and selection bias. International data must not be silently pooled with Irish records.
