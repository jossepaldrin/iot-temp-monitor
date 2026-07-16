# IoT Cloud-Based Temperature Monitoring System

CSDA306 (Internet of Things) assignment — simulates an IoT temperature sensor,
stores readings in Supabase, and visualizes them in a Flask web app.

## Project structure
```
iot-temp-monitor/
├── supabase_setup.sql   # Run this in Supabase SQL Editor first
├── .env.example         # Copy to .env and fill in your Supabase credentials
├── sensor/
│   ├── sensor_simulator.py
│   └── requirements.txt
└── webapp/              # (added in a later commit)
```

## Part A — Sensor simulator setup
1. Create a free project at https://supabase.com
2. In the Supabase dashboard, go to **SQL Editor** and run the contents of `supabase_setup.sql`.
3. Go to **Project Settings > API** and copy your **Project URL** and **anon public key**.
4. Copy `.env.example` to `.env` in the project root and fill in those two values.
5. Install dependencies and run:
   ```
   cd sensor
   pip install -r requirements.txt
   python sensor_simulator.py
   ```
6. Leave it running — it uploads one reading every 5 seconds until you press Ctrl+C.

More sections (Part B web app, report) will be added as the project develops.
