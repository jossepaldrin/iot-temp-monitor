"""
CSDA306 - Internet of Things
Part A: Cloud-Based Temperature Monitoring System - Sensor Simulator

Simulates an IoT temperature sensor by generating a random reading every
5 seconds and uploading it to a Supabase table via the REST API.
Runs until manually stopped (Ctrl+C).
"""

import os
import time
import random
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
TABLE_NAME = "temperature_readings"
READING_INTERVAL_SECONDS = 5
TEMP_MIN_C = 20.0
TEMP_MAX_C = 40.0

if not SUPABASE_URL or not SUPABASE_KEY:
    raise SystemExit(
        "Missing SUPABASE_URL or SUPABASE_KEY.\n"
        "Copy .env.example to .env and fill in your Supabase project details."
    )

ENDPOINT = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
}


def generate_reading():
    """Create one simulated temperature reading with the current timestamp."""
    temperature = round(random.uniform(TEMP_MIN_C, TEMP_MAX_C), 1)
    now = datetime.now()
    payload = {
        "temperature": temperature,
        "reading_date": now.strftime("%Y-%m-%d"),
        "reading_time": now.strftime("%H:%M:%S"),
    }
    return payload, now


def upload_reading(payload):
    """POST one reading to the Supabase table. Returns True on success."""
    try:
        response = requests.post(ENDPOINT, headers=HEADERS, json=payload, timeout=10)
        return response.status_code in (200, 201)
    except requests.RequestException as exc:
        print(f"  -> Network error while uploading: {exc}")
        return False


def main():
    print("Starting IoT temperature simulator.")
    print(f"Generating a reading every {READING_INTERVAL_SECONDS} seconds. Press Ctrl+C to stop.\n")
    try:
        while True:
            payload, now = generate_reading()
            success = upload_reading(payload)
            status = "Uploaded Successfully" if success else "Upload FAILED"
            timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Temperature: {payload['temperature']}°C | Time: {timestamp_str} | {status}")
            time.sleep(READING_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nSimulator stopped by user.")


if __name__ == "__main__":
    main()
