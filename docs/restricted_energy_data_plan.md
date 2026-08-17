# Restricted actual-energy data plan

## Required datasets

### Census of Population BER Energy (COP BER), 2022

- Provider: Central Statistics Office Ireland (CSO).
- Access: researcher application and approved project through the CSO Researcher Data Portal; contact `environment@cso.ie` and consult the official RMF register.
- Purpose: strongest candidate for the dependent variable because it links occupied Census households, BER information, and quarterly metered electricity/gas.
- Likely linkage fields: protected household/building identifiers, BER match identifier, reference quarter/year and an authorised statistical geography. Exact fields must be confirmed from the current data dictionary inside the portal.
- Expected variables: quarterly electricity kWh, quarterly gas kWh, BER/building characteristics, Census household/demographic attributes and permitted geography.

### BER Energy Research Microdata Files, 2016–2024

- Provider: CSO, using BER and energy-provider data.
- Coverage: occupied BER-matched households; yearly files with quarterly electricity/gas. They do not provide the full Census linkage of COP BER.
- Role: longitudinal/robustness analysis and possible temporal transfer.

## Security and confidentiality

Record-level files remain inside the authorised portal. Do not copy them to a personal computer, cloud drive, GitHub, email, or this repository. No credentials or remote-upload logic belongs in code. All exported tables must pass CSO disclosure control. Small cells and identifiers must be suppressed according to the approved project rules; the template's default minimum of 10 is a conservative technical check, not a substitute for CSO approval.

## Secure workflow

1. Obtain researcher/project approval and the current CSO data dictionaries.
2. Work only in the secure project workspace.
3. Map the actual names to the template schema: `geography_id`, `reference_period`, `electricity_kwh`, optional `gas_kwh`, `floor_area_m2`, and `ber_primary_energy_kwh_m2_year`.
4. Validate using `scripts/restricted/prepare_metered_energy_model_input.py` with a user-supplied secure local path.
5. Create model-ready record-level inputs only inside the secure environment. Harmonise kWh period, missingness/validity flags, meter coverage, fuel and floor area; retain theoretical BER separately.
6. Join to public predictors using only authorised stable geography/time identifiers.
7. Request disclosure approval only for non-disclosive aggregates, coefficients, performance metrics and figures.

Example inside the secure environment:

```powershell
python scripts/restricted/prepare_metered_energy_model_input.py --secure-input D:\approved_project\metered.csv --validation-report D:\approved_project\validation.json
```

An aggregate candidate is optional via `--approved-aggregate-output`; creating it does **not** authorise removal from the portal.

## Dependent-variable definitions to agree before modelling

- Annual electricity kWh per dwelling, with meter-validity/coverage rules.
- Weather-corrected annual gas kWh where methodology supports it.
- Combined delivered metered kWh only when fuels and time coverage are comparable.
- Optional intensity (kWh/m²/year) only when trusted floor area is available.

BER primary energy or BER class is a predictor/diagnostic and must never be labelled actual consumption.
