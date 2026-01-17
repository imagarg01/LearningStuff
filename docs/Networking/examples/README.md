# Network Protocol Examples

Working Python examples for each communication protocol.

## Examples

| Directory | Protocol | Description |
|-----------|----------|-------------|
| [rest_api/](rest_api/) | REST | FastAPI server with CRUD |
| [grpc_service/](grpc_service/) | gRPC | Protobuf-based RPC |
| [graphql_server/](graphql_server/) | GraphQL | Strawberry GraphQL |
| [rabbitmq/](rabbitmq/) | AMQP | RabbitMQ pub/sub |
| [kafka/](kafka/) | Kafka | Producer and consumer |
| [mqtt/](mqtt/) | MQTT | IoT messaging |

## Quick Start

Each example includes:

- `README.md` - Setup instructions
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - External services (if needed)

```bash
# General pattern
cd <example>/
pip install -r requirements.txt
docker-compose up -d  # if needed
python server.py      # or producer.py/publisher.py
python client.py      # or consumer.py/subscriber.py
```

## Prerequisites

- Python 3.10+
- Docker (for brokers)
- pip
