# Kafka Example

Apache Kafka producer and consumer.

## Setup

```bash
# Start Kafka
docker-compose up -d

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
# Terminal 1: Start consumer
python consumer.py

# Terminal 2: Send messages
python producer.py
```

## Notes

- Kafka uses Zookeeper for coordination (included in docker-compose)
- Topics are auto-created by default
