import os
import sys
from pathlib import Path
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    send_file,
)

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
CSV_PATH = DATA_DIR / "kaggle_sales_raw.csv"
DB_PATH = DATA_DIR / "target_dwh.db"
REPORT_PATH = PROJECT_ROOT / "QA_Test_Execution_Report.xlsx"
TEST_CASE_PATH = PROJECT_ROOT / "TestCases.xlsx"
UPLOAD_FOLDER = DATA_DIR

sys.path.insert(0, str(SRC_DIR))

from kaggle_loader import run_etl
from sql_validator import run_sql_checks
from pandas_reconciler import run_pandas_checks
from excel_reporter import generate_excel_report
from test_case_writer import generate_test_cases_excel
from generate_sample_data import create_sample_csv

app = Flask(__name__)
app.secret_key = "qa-framework-secret-key-2024"
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

app_state = {
    "validated": False,
    "sql_results": [],
    "pandas_results": [],
    "tables": None,
    "report_generated": False,
    "report_path": None,
}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            if request.is_json or request.path.startswith("/api/"):
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    return render_template("login.html", error=None)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=session.get("username", ""),
        state=app_state,
    )


@app.route("/api/login", methods=["POST"])
def api_login():
    if request.is_json:
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")

    if not username or not password:
        if request.is_json:
            return jsonify({"error": "Username and password are required"}), 400
        return render_template("login.html", error="Username and password are required")

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        session["logged_in"] = True
        session["username"] = username
        if request.is_json:
            return jsonify({"message": "Login successful", "username": username}), 200
        return redirect(url_for("dashboard"))

    if request.is_json:
        return jsonify({"error": "Invalid credentials"}), 401
    return render_template("login.html", error="Invalid credentials")


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    if request.is_json:
        return jsonify({"message": "Logged out successfully"}), 200
    return redirect(url_for("login_page"))


@app.route("/api/upload", methods=["POST"])
@login_required
def api_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files are supported"}), 400

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    save_path = CSV_PATH
    file.save(str(save_path))

    return jsonify({
        "message": "File uploaded successfully",
        "filename": file.filename,
        "path": str(save_path),
        "size": os.path.getsize(str(save_path)),
    }), 200


@app.route("/api/validate", methods=["POST"])
@login_required
def api_validate():
    if not CSV_PATH.exists():
        create_sample_csv(output_path=str(CSV_PATH), n_rows=1000)

    import pandas as pd
    try:
        row_count = len(pd.read_csv(str(CSV_PATH), encoding="latin-1"))
        if row_count < 25:
            create_sample_csv(output_path=str(CSV_PATH), n_rows=1000)
    except Exception:
        create_sample_csv(output_path=str(CSV_PATH), n_rows=1000)

    try:
        tables = run_etl(str(CSV_PATH), str(DB_PATH))
        sql_results = run_sql_checks(str(DB_PATH))
        pandas_results = run_pandas_checks(
            source=tables["fact_source"],
            target=tables["fact_target"],
        )

        app_state["validated"] = True
        app_state["tables"] = tables
        app_state["sql_results"] = sql_results
        app_state["pandas_results"] = pandas_results
        app_state["report_generated"] = False

        all_results = sql_results + pandas_results
        total = len(all_results)
        passed = sum(1 for r in all_results if r["Status"] == "PASS")
        failed = sum(1 for r in all_results if r["Status"] == "FAIL")

        return jsonify({
            "message": "Validation completed",
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "status": "completed",
        }), 200

    except Exception as e:
        return jsonify({"error": f"Validation failed: {str(e)}"}), 500


@app.route("/api/status", methods=["GET"])
@login_required
def api_status():
    return jsonify({
        "validated": app_state["validated"],
        "report_generated": app_state["report_generated"],
        "csv_exists": CSV_PATH.exists(),
        "db_exists": DB_PATH.exists(),
    }), 200


@app.route("/api/results", methods=["GET"])
@login_required
def api_results():
    if not app_state["validated"]:
        return jsonify({"error": "No validation has been run yet"}), 400

    sql_results = app_state["sql_results"]
    pandas_results = app_state["pandas_results"]

    clean_results = []
    for r in sql_results + pandas_results:
        clean_results.append({
            "test_id": r["Test ID"],
            "test_name": r["Test Name"],
            "expected": str(r["Expected"]),
            "result": str(r["Result"]),
            "status": r["Status"],
            "details": r["Details"],
        })

    total = len(clean_results)
    passed = sum(1 for r in clean_results if r["status"] == "PASS")
    failed = sum(1 for r in clean_results if r["status"] == "FAIL")

    return jsonify({
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "results": clean_results,
    }), 200


@app.route("/api/report", methods=["POST"])
@login_required
def api_report():
    if not app_state["validated"]:
        return jsonify({"error": "Run validation first"}), 400

    try:
        report_path = generate_excel_report(
            app_state["sql_results"],
            app_state["pandas_results"],
            output_path=str(REPORT_PATH),
        )
        test_case_path = generate_test_cases_excel(
            app_state["sql_results"],
            app_state["pandas_results"],
            output_path=str(TEST_CASE_PATH),
        )

        app_state["report_generated"] = True
        app_state["report_path"] = report_path

        return jsonify({
            "message": "Reports generated successfully",
            "report_path": report_path,
            "test_case_path": test_case_path,
        }), 200

    except Exception as e:
        return jsonify({"error": f"Report generation failed: {str(e)}"}), 500


@app.route("/api/report/download", methods=["GET"])
@login_required
def api_report_download():
    if not app_state["report_generated"]:
        return jsonify({"error": "No report has been generated yet"}), 400

    report_file = app_state["report_path"]
    if not report_file or not Path(report_file).exists():
        return jsonify({"error": "Report file not found"}), 404

    return send_file(
        report_file,
        as_attachment=True,
        download_name="QA_Test_Execution_Report.xlsx",
    )


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5000)
