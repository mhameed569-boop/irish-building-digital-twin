# Irish Building Digital Twin

A research project for analysing residential energy performance,
vacancy, demographics, weather, and retrofit priorities in Ireland.

## Current Data Source

### CSO VAC14 - Local Authority Vacant Dwellings

Official source:

https://data.gov.ie/dataset/vac14-local-authority-vacant-dwelling-numbers

The dataset contains:

- Number of vacant dwellings
- Vacancy rate
- Local authority
- Quarter and year

## Project Structure

```text
scripts/
    download_cso_vacancy.py
    summarize_vacancy.py

data/
    raw/
        Downloaded data - not uploaded to GitHub
    processed/
        Non-sensitive analysis outputs
```

## How to Run

First, download the official CSO dataset:

```bash
python scripts/download_cso_vacancy.py
```

Then create the latest vacancy-rate summary:

```bash
python scripts/summarize_vacancy.py
```

The processed result is saved as:

```text
data/processed/latest_vacancy_rates.csv
```

## Data Protection

Raw and restricted datasets are not uploaded to GitHub.

The CSO COP BER and BER Energy Research Microdata Files must remain
inside the secure CSO Researcher Data Portal. Only non-confidential
code and approved aggregated results may be added to this repository.