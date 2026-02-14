# Recommended Papers & Resources

## Academic & Industry Papers

1. **"The Log: What every software engineer should know about real-time data's unifying abstraction"** (Jay Kreps, LinkedIn/Confluent)
    * *Concept*: The foundational concept of immutable logs (Kafka) as the backbone of distributed systems.
    * *Relevance*: Understanding why the Event Core is central to this design.

2. **"Sagas"** (Hector Garcia-Molina, Kenneth Salem)
    * *Concept*: Long-lived transactions in distributed systems (1987).
    * *Relevance*: The mathematical basis for handling distributed transactions without two-phase commit.

3. **"Kappa Architecture"** (Jay Kreps)
    * *Concept*: simplification of Lambda Architecture, treating everything as a stream.
    * *Relevance*: Moving towards a stream-first processing model for real-time analytics.

4. **"Harvest, Yield, and Scalable Tolerant Systems"** (Fox/Brewer)
    * *Concept*: CAP theorem trade-offs in high-volume systems.
    * *Relevance*: Understanding consistency vs. availability when designing the Read-Aside cache.

## Books

1. **"Designing Data-Intensive Applications"** by Martin Kleppmann
    * *Must Read*: Chapters on Stream Processing, Consistency, and Distributed Data.

2. **"Building Event-Driven Microservices"** by Adam Bellemare
    * *Focus*: Practical patterns for Kafka-based microservices.

3. **"Kafka: The Definitive Guide"** by Narkhede, Shapira, Palino
    * *Focus*: Deep dive into Kafka internals, tuning, and reliability.

## Technology Stack

### Core Infrastructure

* **Message Bus**: Apache Kafka / Redpanda (Low latency, high throughput)
* **Database (Transactional)**: PostgreSQL / Amazon Aurora
* **Database (Read/Cache)**: Redis / ScyllaDB (Low latency KV store)
* **Vector Database**: Pinecone / Milvus (For Agent memory)
* **Stream Processing**: Apache Flink / Kafka Streams

### Application Layer

* **Languages**: Go (High performance microservices), Python (AI Agents), Java (Enterprise logic)
* **API Gateway**: Kong / APISIX / Envoy
* **Protocol**: gRPC (Internal), GraphQL (BFF), Avro/Protobuf (Serialization)
