# IoT Cloud-Based Temperature Monitoring System

CSDA306 (Internet of Things) assignment — simulates an IoT temperature sensor,
stores readings in Supabase, and visualizes them live in a Flask web dashboard.

## Overview

- **Part A** — `sensor/sensor_simulator.py` generates a random temperature
  reading (20–40°C) every 5 seconds and uploads it to a Supabase table.
- **Part B** — `webapp/app.py` (Flask) reads from the same table and serves
  a dashboard: a live line chart, a data table, the latest reading, and a
  CSV export — auto-refreshing every 5 seconds with no page reload.
- **Report** — `report/Temperature_Monitoring_Report.docx` documents the
  architecture, database schema, implementation, and challenges faced.

## Project structure
```
iot-temp-monitor/
├── supabase_setup.sql        # Run in Supabase SQL Editor first
├── .env.example               # Copy to .env, fill in Supabase credentials
├── sensor/
│   ├── sensor_simulator.py
│   └── requirements.txt
├── webapp/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   └── chart.umd.min.js   # Chart.js, bundled locally (no CDN dependency)
│   └── templates/
│       └── index.html
└── report/
    └── Temperature_Monitoring_Report.docx
```

## Setup

### 1. Supabase
1. Create a free project at [supabase.com](https://supabase.com).
2. In the **SQL Editor**, run the contents of `supabase_setup.sql`. This creates
   the `temperature_readings` table, enables Row Level Security, and grants the
   `anon` role insert/select access.
3. Go to **Project Settings → API** and copy the **Project URL** and **anon
   public key**.
4. Copy `.env.example` to `.env` in the project root and fill in those two values.

### 2. Part A — Sensor simulator
```
cd sensor
pip install -r requirements.txt
python sensor_simulator.py
```
Runs until stopped with `Ctrl+C`, uploading one reading every 5 seconds.

### 3. Part B — Web dashboard
```
cd webapp
pip install -r requirements.txt
python app.py
```
Open **http://127.0.0.1:5000**. Run the simulator (step 2) in a separate
terminal at the same time to see the dashboard update live.

## Features

- Random sensor simulation with cloud upload every 5 seconds
- Live line chart (Chart.js) and data table, auto-refreshing every 5 seconds
- Latest-reading display
- CSV export of all stored readings
- Chart.js bundled locally — no external CDN dependency at runtime

## Tech stack

Python, Flask, Supabase (Postgres + REST API), Chart.js, `requests`, `python-dotenv`.

## Author

Aldrin Aype Joseph — MSc Computer Science (Data Analytics), Semester 3