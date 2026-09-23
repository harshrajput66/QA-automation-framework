# End-to-End QA Automation Framework

A professional, multi-layered QA Automation Framework built with Python that validates data quality across an ETL pipeline — from raw CSV files through a SQLite database to a Flask web application — using **Playwright** (UI), **requests** (API), and **Pandas/SQL** (Data) testing.

## Architecture

```
CSV Data Source
       ↓
  ETL Pipeline (kaggle_loader.py)
       ↓
  SQLite Database
       ↓
  Validation Engine
  ├── SQL Checks (7 tests)
  └── Pandas Checks (6 tests)
       ↓
  Flask Web App (app.py)
  ├── REST API  ← tested by requests (22 tests)
  └── Web UI    ← tested by Playwright (19 tests)
```

## Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Core language |
| **pytest** | Test framework with markers & fixtures |
| **Playwright** | Browser-based UI automation |
| **requests** | REST API testing |
| **Pandas / NumPy** | Data validation & comparison |
| **SQLite** | Database layer |
| **Flask** | Web application & REST API |
| **Page Object Model** | UI test design pattern |

## Test Summary — 54 Automated Tests

| Layer | Tests | Tool |
|---|---|---|
| Data / Database | 13 | Pandas + SQL |
| API | 22 | requests + pytest |
| UI | 19 | Playwright + pytest |
| **Total** | **54** | **All passing ✅** |

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Run the Original CLI Pipeline
```bash
python main.py
```

### 3. Start the Web Application
```bash
python app.py
# Open http://localhost:5000
# Login: admin / admin123
```

### 4. Run All Tests
```bash
pytest tests/ -v
```

### 5. Run Tests by Layer
```bash
pytest tests/data/ -v          # Data/DB tests
pytest tests/api/ -v           # API tests
pytest tests/ui/ -v            # UI tests (headless)
```

### 6. Run UI Tests in Headed Mode (See the Browser)
```bash
set QA_HEADLESS=false
pytest tests/ui/ -v
```

## Project Structure

```
├── main.py                     # CLI entry point
├── app.py                      # Flask web application
├── pytest.ini                  # Test configuration
├── requirements.txt            # Dependencies
│
├── src/                        # Core business logic
│   ├── kaggle_loader.py        #   ETL: CSV → SQLite
│   ├── sql_validator.py        #   SQL quality checks
│   ├── pandas_reconciler.py    #   Pandas/NumPy checks
│   ├── excel_reporter.py       #   Excel report generator
│   ├── test_case_writer.py     #   Test case document
│   └── generate_sample_data.py #   Sample data generator
│
├── templates/                  # Flask HTML templates
│   ├── login.html
│   └── dashboard.html
│
└── tests/                      # Automated test suite
    ├── conftest.py             #   Root fixtures
    ├── utils/                  #   Shared config & helpers
    ├── data/                   #   Data validation tests (13)
    ├── api/                    #   API tests (22)
    └── ui/                     #   Playwright UI tests (19)
        └── pages/              #   Page Object Model
```

## Key Design Patterns

- **Page Object Model (POM):** UI locators and actions are encapsulated in `LoginPage` and `DashboardPage` classes, keeping test files clean and maintainable.
- **Reusable API Client:** The `APIClient` class manages HTTP sessions, cookies, and all endpoint interactions — tests focus purely on assertions.
- **pytest Fixtures:** Session-scoped fixtures start the Flask server once and share it across all API and UI tests. Data fixtures run ETL once per session.
- **Testing Pyramid:** Fast data tests at the base, API tests in the middle, UI tests at the top.

## License

This project is for educational and portfolio purposes.
