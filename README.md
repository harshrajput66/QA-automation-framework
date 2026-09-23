# QA Automation Framework

An end-to-end QA automation project that validates data quality across an ETL pipeline using Python, Playwright, and pytest.

## What It Does

- Takes raw CSV sales data, loads it into a SQLite database via ETL
- Runs SQL and Pandas checks to catch data defects (nulls, duplicates, mismatches)
- Serves a Flask web dashboard for uploading data, running validation, and downloading reports
- Has 54 automated tests across three layers: Data, API, and UI

## Tools Used

- **Playwright** — UI browser automation with Page Object Model
- **pytest** — test framework for all three layers
- **requests** — API endpoint testing
- **Pandas / SQL** — data validation
- **Flask** — web app and REST API

## How to Run

```bash
# install dependencies
pip install -r requirements.txt
playwright install chromium

# run the CLI pipeline
python main.py

# start the web app (http://localhost:5000 — admin / admin123)
python app.py

# run all tests
pytest tests/ -v

# run by layer
pytest tests/data/ -v
pytest tests/api/ -v
pytest tests/ui/ -v
```
