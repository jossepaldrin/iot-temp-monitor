"""
CSDA306 - Internet of Things
MQTT Enhancement: Subscriber

Listens on the MQTT topic the publisher sends readings to, and is the
only piece of this pipeline that actually talks to Supabase. This plays
the role sensor_simulator.py used to play alone in Part A - the publisher
no longer needs any database credentials at all.
"""

import json
import os

import paho.mqtt.client as mqtt
import requests
from dotenv import load_dotenv

load_dotenv()

BROKER_HOST = "broker.hivemq.com"
BROKER_PORT = 1883
TOPIC = "csda306/aldrinaypejoseph/iot-temp-monitor/temperature"

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
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
}


def upload_reading(payload):
    try:
        response = requests.post(ENDPOINT, headers=HEADERS, json=payload, timeout=10)
        return response.status_code in (200, 201)
    except requests.RequestException as exc:
        print(f"  -> Network error while uploading: {exc}")
        return False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to broker. Subscribing to '{TOPIC}' ...")
        client.subscribe(TOPIC, qos=1)
    else:
        print(f"Connection failed with return code {rc}")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Received malformed message, skipping.")
        return

    success = upload_reading(payload)
    status = "Uploaded Successfully" if success else "Upload FAILED"
    print(
        f"Received: Temperature: {payload.get('temperature')}°C | "
        f"Time: {payload.get('reading_date')} {payload.get('reading_time')} | {status}"
    )


def main():
    client = mqtt.Client(client_id="iot-temp-subscriber")
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to broker {BROKER_HOST}:{BROKER_PORT} ...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    print("Listening for messages. Press Ctrl+C to stop.\n")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nSubscriber stopped by user.")
        client.disconnect()


if __name__ == "__main__":
    main()
