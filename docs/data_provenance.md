# Data provenance

Machine-readable records are in `data/metadata/source_manifest.csv`. Downloads are performed only from the official provider URLs recorded there; public raw downloads are ignored by Git and can be recreated by their scripts.

## Transformation chain

1. CSO SAPS CSV → energy-relevant Census counts and documented percentage features (`process_small_area_features.py`).
2. Tailte Éireann paged GeoJSON → official crosswalk, WGS84 centroids, source-area conversion, population/housing densities and an adjacency edge list (`build_small_area_spatial_features.py`).
3. Census + spatial table → 18,919-row public Small Area table, with 2024 county weather/BER/vacancy fields clearly labelled as county context (`build_spatial_model_features.py`).
4. UK NEED official CSV → harmonised transfer table after validity-flag filtering; actual electricity remains separate from weather-corrected gas (`process_uk_need_sample.py`).
5. `validate_research_datasets.py` reports counts, joins, ranges, dependencies, coordinates, missingness and target absence without silently dropping records.

The run date is not the statistical reference year. Reference years are columns in integrated outputs and are documented in `temporal_alignment.md`. Licences and provider attribution remain governed by the original official sources.
