# Temporal alignment

| Source | Reference period | Use |
|---|---|---|
| Census SAPS and housing | 2022 | demographic, housing, heating and tenure predictors |
| Small Area geography | Census 2022 boundaries | spatial identifiers, centroids, density and adjacency |
| VAC14 | 2024Q4 | county vacancy context and preliminary priority indicator |
| EBA02 | 2024 | county aggregated BER context |
| Met Éireann | calendar 2024 | county climate context and estimated HDD |
| UK NEED | annual consumption through 2023 | international transfer-learning feasibility |
| COP BER | 2022 when authorised | actual Irish energy target linked to Census |
| BER Energy RMFs | 2016–2024 when authorised | longitudinal actual energy analysis |

The public Small Area dataset is a mixed-year analytical snapshot; it does not imply that Census attributes were measured in 2024. Reference fields are retained explicitly. Census stock and household composition are assumed sufficiently stable for initial contextual analysis, but this assumption must be tested.

Future sensitivity analysis should: use COP BER 2022 with contemporaneous Census predictors; repeat using only variables expected to change slowly; compare 2022 and later climate normals/annual weather; test lagged versus contemporaneous vacancy/BER context; and use year/group fixed effects for multi-year RMFs. County-level 2024 values repeated across Small Areas are contextual covariates, not fine-resolution measurements.
