# IoT Cloud-Based Temperature Monitoring System

CSDA306 (Internet of Things) assignment — simulates an IoT temperature sensor,
stores readings in Supabase, and visualizes them live in a Flask web dashboard.
Extended with an MQTT publish/subscribe layer as an enhancement.

## Overview

- **Part A** — `sensor/sensor_simulator.py` generates a random temperature
  reading (20–40°C) every 5 seconds and uploads it directly to Supabase.
- **Part B** — `webapp/app.py` (Flask) reads from Supabase and serves a
  dashboard: a live line chart, a data table, the latest reading, and a
  CSV export — auto-refreshing every 5 seconds with no page reload.
- **MQTT enhancement** — `mqtt/mqtt_publisher.py` and `mqtt/mqtt_subscriber.py`
  decouple sensor and database via a public MQTT broker (HiveMQ). A live
  browser-based monitor (`webapp/templates/mqtt_monitor.html`, at `/live-mqtt`)
  also subscribes directly over WebSocket to show raw pub/sub traffic in
  real time.
- **Report** — `report/Temperature_Monitoring_Report.docx` documents the
  architecture, database schema, implementation, and challenges faced.

## Project structure
```
iot-temp-monitor/
├── supabase_setup.sql        # Run in Supabase SQL Editor first
├── .env.example               # Copy to .env, fill in Supabase credentials
├── sensor/
│   ├── sensor_simulator.py    # Direct-to-Supabase version (no MQTT)
│   └── requirements.txt
├── mqtt/
│   ├── mqtt_publisher.py      # Publishes readings to a broker, no DB access
│   ├── mqtt_subscriber.py     # Subscribes, writes to Supabase
│   └── requirements.txt
├── webapp/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   ├── chart.umd.min.js   # Chart.js, bundled locally
│   │   └── mqtt.min.js        # mqtt.js, bundled locally (browser MQTT client)
│   └── templates/
│       ├── index.html         # Main dashboard (table + chart, from Supabase)
│       └── mqtt_monitor.html  # /live-mqtt - raw pub/sub feed, no DB involved
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

### 2. Part A — Sensor simulator (direct to Supabase)
```
cd sensor
pip install -r requirements.txt
python sensor_simulator.py
```

### 3. Part B — Web dashboard
```
cd webapp
pip install -r requirements.txt
python app.py
```
Open **http://127.0.0.1:5000**.

### 4. MQTT enhancement (optional layer)
```
cd mqtt
pip install -r requirements.txt
python mqtt_subscriber.py     # terminal 1 - start first
python mqtt_publisher.py      # terminal 2
```
Then visit **http://127.0.0.1:5000/live-mqtt** to watch messages arrive live,
straight from the broker to the browser.

## Two ways of getting data from sensor to dashboard

This project implements the same idea two different ways, to show the
trade-off between a simple direct connection and a decoupled, broker-based
one.

### Without MQTT — direct REST (`sensor/sensor_simulator.py`)

The simulator calls Supabase's REST API directly over HTTPS.

- **Coupling:** Tight — the sensor script must hold valid Supabase
  credentials and know its exact endpoint.
- **Who needs database access:** Every device generating data.
- **Moving parts:** 2 — simulator, database.
- **Latency:** Lowest possible — a single network hop.
- **Simplicity:** Very easy to write and reason about; no extra
  infrastructure.
- **Realism:** Convenient for a demo, but not how most real IoT deployments
  are built — devices rarely get direct database credentials.

### With MQTT — publish/subscribe (`mqtt/mqtt_publisher.py` + `mqtt_subscriber.py`)

The simulator (publisher) only talks to a broker; a separate subscriber is
the only piece that talks to Supabase.

- **Coupling:** Loose — publisher and subscriber never communicate
  directly and don't know about each other. The publisher holds no
  database credentials at all.
- **Who needs database access:** Only the subscriber (acting as a
  gateway).
- **Moving parts:** 4 — publisher, broker, subscriber, database.
- **Latency:** Slightly higher — two hops (publish to broker, deliver to
  subscriber) plus the subscriber's own write to Supabase.
- **Simplicity:** More moving parts to run and reason about, and a
  dependency on a broker being reachable.
- **Realism:** Much closer to real IoT architecture — many independent
  devices can publish to the same broker, and multiple subscribers (a
  database writer, a live dashboard, a logging service) can all listen to
  the same stream independently, none of them needing to know the others
  exist.
- **Bonus capability:** Because subscribing needs no database credentials,
  the browser itself can subscribe directly over WebSocket
  (`/live-mqtt`) and show live pub/sub traffic with zero backend
  involvement — something the direct-REST approach can't do.

## Features

- Random sensor simulation with cloud upload every 5 seconds
- Live line chart (Chart.js) and data table, auto-refreshing every 5 seconds
- Latest-reading display
- CSV export of all stored readings
- MQTT publish/subscribe pipeline via a public broker (HiveMQ)
- Live browser-based MQTT monitor over WebSocket, independent of the database
- Chart.js and mqtt.js both bundled locally — no external CDN dependency at runtime

## Tech stack

Python, Flask, Supabase (Postgres + REST API), MQTT (`paho-mqtt`, HiveMQ
public broker), Chart.js, `mqtt.js`, `requests`, `python-dotenv`.

## Author

Aldrin Aype Joseph — MSc Computer Science (Data Analytics), Semester 3