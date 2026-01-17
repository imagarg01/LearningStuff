"""
MQTT Publisher Example
Simulates IoT sensor publishing data.
"""

import paho.mqtt.client as mqtt
import json
import time
import random

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Publish online status (retained)
        client.publish("home/living-room/status", "online", qos=1, retain=True)
    else:
        print(f"Failed to connect, return code {rc}")

def main():
    client = mqtt.Client(client_id="sensor-living-room")
    client.on_connect = on_connect
    
    # Set Last Will and Testament
    client.will_set(
        topic="home/living-room/status",
        payload="offline",
        qos=1,
        retain=True
    )
    
    # Connect
    client.connect("localhost", 1883, keepalive=60)
    client.loop_start()
    
    try:
        while True:
            # Simulate sensor readings
            temperature = round(20 + random.uniform(-5, 5), 1)
            humidity = round(50 + random.uniform(-10, 10), 1)
            
            # Publish temperature
            payload = json.dumps({
                "value": temperature,
                "unit": "celsius",
                "timestamp": time.time()
            })
            client.publish(
                "home/living-room/temperature",
                payload,
                qos=1,
                retain=True
            )
            print(f"Published temperature: {temperature}°C")
            
            # Publish humidity
            payload = json.dumps({
                "value": humidity,
                "unit": "percent",
                "timestamp": time.time()
            })
            client.publish(
                "home/living-room/humidity",
                payload,
                qos=1,
                retain=True
            )
            print(f"Published humidity: {humidity}%")
            print()
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        client.publish("home/living-room/status", "offline", qos=1, retain=True)
        client.loop_stop()
        client.disconnect()

if __name__ == '__main__':
    main()
