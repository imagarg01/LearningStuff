"""
MQTT Subscriber Example
Monitors IoT sensor data.
"""

import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to all home topics
    client.subscribe("home/#", qos=1)
    print("Subscribed to home/#")

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}")
    print(f"  QoS: {msg.qos}")
    print(f"  Retained: {msg.retain}")
    
    try:
        payload = json.loads(msg.payload.decode())
        print(f"  Payload: {payload}")
    except:
        print(f"  Payload (raw): {msg.payload.decode()}")
    print()

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed with QoS: {granted_qos}")

def main():
    client = mqtt.Client(client_id="home-monitor")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    
    client.connect("localhost", 1883, keepalive=60)
    
    print("Waiting for messages... Press CTRL+C to exit")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        client.disconnect()

if __name__ == '__main__':
    main()
