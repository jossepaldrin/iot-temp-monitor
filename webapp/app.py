"""
CSDA306 - Internet of Things
Part B: Cloud-Based Temperature Monitoring System - Flask Web Application

Reads all temperature readings from the same Supabase table the sensor
simulator writes to, and serves a dashboard with a table, a live line
chart, the latest reading, and a CSV export.
"""

import csv
import io
import os

import requests
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
TABLE_NAME = "temperature_readings"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise SystemExit(
        "Missing SUPABASE_URL or SUPABASE_KEY.\n"
        "Make sure the .env file in the project root is filled in."
    )

ENDPOINT = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

app = Flask(__name__)


def fetch_readings():
    """Fetch all readings from Supabase, oldest first."""
    params = {
        "select": "id,temperature,reading_date,reading_time,created_at",
        "order": "created_at.asc",
    }
    response = requests.get(ENDPOINT, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/live-mqtt")
def live_mqtt():
    return render_template("mqtt_monitor.html")


@app.route("/api/readings")
def api_readings():
    """JSON endpoint the frontend polls every 5 seconds."""
    try:
        data = fetch_readings()
        return jsonify({"success": True, "readings": data})
    except requests.RequestException as exc:
        return jsonify({"success": False, "error": str(exc)}), 502


@app.route("/export")
def export_csv():
    """Bonus: export all readings as a downloadable CSV file."""
    try:
        data = fetch_readings()
    except requests.RequestException as exc:
        return jsonify({"success": False, "error": str(exc)}), 502

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "temperature_c", "reading_date", "reading_time", "created_at"])
    for row in data:
        writer.writerow([
            row.get("id"),
            row.get("temperature"),
            row.get("reading_date"),
            row.get("reading_time"),
            row.get("created_at"),
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=temperature_readings.csv"},
    )


if __name__ == "__main__":
    app.run(debug=True)