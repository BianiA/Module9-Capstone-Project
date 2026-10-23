# Capstone Project: Model Building & Deployment

## Overview
End-to-end synthetic customer purchase analytics pipeline following the supplied capstone brief. **All customer records are fabricated for educational purposes**, generated locally with a fixed random seed (42), not downloaded from Mockaroo. The assignment permits synthetic Mockaroo data or public APIs; confirm with your instructor whether locally generated synthetic data is acceptable before submission. No real people or sales are represented.

## Dataset
10,000 rows, columns: CustomerID, Name, Age, PurchaseAmount, Country, Date. One synthetic purchase per ID. Dates span 2025–2026. PurchaseAmount has no declared currency.

## Reproduce
Python 3.10+ required. From project folder:

```bash
pip install -r requirements.txt
python scripts/pipeline.py
```

Windows: double-click `scripts/run_pipeline.bat` after installing dependencies. This runs ingestion, storage, cleaning, enrichment, validation, SQLite loading, visualizations, and logging.

## Pipeline stages
1. Collection: `data/raw/dataset.csv` (locally generated synthetic source).
2. Storage: copy source to `data/cleaned/dataset_storage.csv`.
3. Cleaning: standardize names/types, remove nulls and duplicate IDs, filter invalid ages and purchase amounts.
4. Enrichment: age group, purchase category and year derived from raw fields. No external join is performed; enrichment is derived-feature integration only.
5. Validation: non-null, uniqueness, range and category assertions saved to `logs/validation.json`.
6. Loading: `data/cleaned/dataset_final.csv` and SQLite table `customer_purchases` in `capstone.db`.
7. Modeling: `diagrams/erd.md` with schema and limitations; see SQL queries in `sql/analytics.sql`.
8. Orchestration: weekly GitHub Actions schedule plus manual dispatch; workflow runs after repository is pushed and Actions is enabled.
9. Monitoring: `logs/pipeline.log` records start, errors, success, duration, and row counts.
10. Visualization: two PNG charts and age-group summary in `dashboards/`. These are Python charts, **not Power BI or Tableau dashboards**, so a separate Power BI/Tableau deliverable may be needed for full rubric credit.
11. Git: commit and push files to your own GitHub repository; submit repository URL in Canvas.

## Known limitations
Synthetic data; simplistic single-table schema; no true multi-table join; age-group label 'Teen' covers age 18 only; purchase amount units are unspecified. The repository includes automation configuration but an actual scheduled GitHub run must be verified after pushing. The course rubric specifically asks for Mockaroo/public API, a professional ERD, and Power BI/Tableau; these items may need enhancement.

## GitHub submission
Create a new repository on GitHub (e.g. `capstone-model-building`), upload the contents of this project folder, and commit. Copy its HTTPS URL into the Canvas assignment. Do not upload only the ZIP unless Canvas explicitly requests it.
