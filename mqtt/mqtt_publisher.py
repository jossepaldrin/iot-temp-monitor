"""
CSDA306 - Internet of Things
MQTT Enhancement: Publisher

Simulates an IoT temperature sensor, but instead of talking to Supabase
directly, it publishes each reading to an MQTT topic. It has no knowledge
of the database at all - that's the subscriber's job. This mirrors a real
IoT device that only needs to reach a broker, not the cloud database itself.
"""

import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER_HOST = "broker.hivemq.com"
BROKER_PORT = 1883
TOPIC = "csda306/aldrinaypejoseph/iot-temp-monitor/temperature"
PUBLISH_INTERVAL_SECONDS = 5
TEMP_MIN_C = 20.0
TEMP_MAX_C = 40.0


def generate_reading():
    temperature = round(random.uniform(TEMP_MIN_C, TEMP_MAX_C), 1)
    now = datetime.now()
    return {
        "temperature": temperature,
        "reading_date": now.strftime("%Y-%m-%d"),
        "reading_time": now.strftime("%H:%M:%S"),
    }, now


def main():
    client = mqtt.Client(client_id="iot-temp-publisher")
    print(f"Connecting to broker {BROKER_HOST}:{BROKER_PORT} ...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()
    print(f"Connected. Publishing to topic '{TOPIC}' every {PUBLISH_INTERVAL_SECONDS}s.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            payload, now = generate_reading()
            result = client.publish(TOPIC, json.dumps(payload), qos=1)
            result.wait_for_publish()
            timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Published: Temperature: {payload['temperature']}°C | Time: {timestamp_str}")
            time.sleep(PUBLISH_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nPublisher stopped by user.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
