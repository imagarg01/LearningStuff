# MQTT Example

MQTT publisher and subscriber for IoT messaging.

## Setup

```bash
# Start Mosquitto broker
docker-compose up -d

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
# Terminal 1: Start subscriber
python subscriber.py

# Terminal 2: Publish messages
python publisher.py
```

## Topics

- `home/+/temperature` - Temperature readings
- `home/+/humidity` - Humidity readings
- `home/+/status` - Device status (retained)
