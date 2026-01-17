# RabbitMQ Example

AMQP messaging with pika.

## Setup

```bash
# Start RabbitMQ
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

## Management UI

- URL: <http://localhost:15672>
- Username: guest
- Password: guest
