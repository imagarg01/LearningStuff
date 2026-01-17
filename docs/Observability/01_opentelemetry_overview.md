# OpenTelemetry Overview

OpenTelemetry (OTel) is a vendor-neutral, open-source observability framework for instrumenting, generating, collecting, and exporting telemetry data.

---

## What is OpenTelemetry?

```mermaid
graph LR
    subgraph "OpenTelemetry"
        API[APIs]
        SDK[SDKs]
        I[Instrumentation]
        C[Collector]
    end
    
    App[Application] --> API
    API --> SDK
    SDK --> I
    I --> C
    C --> B1[Jaeger]
    C --> B2[Prometheus]
    C --> B3[Datadog]
```

OpenTelemetry provides:

| Component | Description |
|-----------|-------------|
| **APIs** | Language-specific interfaces for telemetry |
| **SDKs** | Implementations of the APIs |
| **Instrumentation** | Auto and manual instrumentation libraries |
| **Collector** | Vendor-agnostic data processing pipeline |
| **Semantic Conventions** | Standard attribute naming |

---

## History and Evolution

```mermaid
timeline
    title OpenTelemetry Evolution
    2010 : Dapper (Google)
    2012 : Zipkin (Twitter)
    2015 : OpenTracing started
    2017 : OpenCensus (Google)
    2019 : OpenTelemetry merger
    2021 : Tracing GA
    2023 : Metrics GA
    2024 : Logs GA
```

OpenTelemetry was formed by merging two projects:

| Project | Focus |
|---------|-------|
| **OpenTracing** | Vendor-neutral tracing API |
| **OpenCensus** | Metrics and tracing with exporters |

---

## Core Concepts

### Telemetry Signals

```mermaid
graph TB
    OTel[OpenTelemetry]
    
    OTel --> Traces
    OTel --> Metrics
    OTel --> Logs
    
    Traces --> S1["Distributed request tracking"]
    Metrics --> S2["Numeric measurements over time"]
    Logs --> S3["Timestamped event records"]
```

### Components Architecture

```mermaid
graph TB
    subgraph "Application"
        Code[Your Code]
        AL[Auto Libraries]
        ML[Manual Spans]
    end
    
    subgraph "OTel SDK"
        TP[TracerProvider]
        MP[MeterProvider]
        LP[LoggerProvider]
        Proc[Processors]
        Exp[Exporters]
    end
    
    subgraph "OTel Collector"
        R[Receivers]
        P[Processors]
        E[Exporters]
    end
    
    subgraph "Backends"
        J[Jaeger]
        Pr[Prometheus]
        L[Loki]
    end
    
    Code --> AL
    Code --> ML
    AL --> TP
    ML --> TP
    TP --> Proc
    MP --> Proc
    LP --> Proc
    Proc --> Exp
    Exp --> R
    R --> P
    P --> E
    E --> J
    E --> Pr
    E --> L
```

---

## Why OpenTelemetry?

### Problems it Solves

```mermaid
graph LR
    subgraph "Before OTel"
        V1[Vendor A SDK]
        V2[Vendor B SDK]
        V3[Vendor C SDK]
        App1[App] --> V1
        App1 --> V2
        App1 --> V3
    end
    
    subgraph "With OTel"
        OT[OpenTelemetry]
        App2[App] --> OT
        OT --> B1[Vendor A]
        OT --> B2[Vendor B]
        OT --> B3[Vendor C]
    end
```

### Key Benefits

| Benefit | Description |
|---------|-------------|
| **Vendor Neutrality** | Avoid lock-in to specific vendors |
| **Single Standard** | One SDK for all telemetry |
| **Cross-Language** | Consistent across languages |
| **Future-Proof** | CNCF incubating project |
| **Extensible** | Plugin architecture |

---

## Supported Languages

OpenTelemetry provides SDKs for many programming languages:

| Language | Status | Auto-Instrumentation |
|----------|--------|---------------------|
| **Java** | Stable | ✓ Agent available |
| **Python** | Stable | ✓ Available |
| **Go** | Stable | Partial |
| **JavaScript** | Stable | ✓ Available |
| **.NET** | Stable | ✓ Available |
| **C++** | Stable | Limited |
| **Rust** | Beta | Limited |
| **Ruby** | Beta | ✓ Available |
| **PHP** | Beta | ✓ Available |
| **Swift** | Alpha | Limited |
| **Erlang/Elixir** | Beta | Limited |

---

## OTel vs Alternatives

### Comparison with Other Tools

| Aspect | OpenTelemetry | Prometheus | Jaeger |
|--------|---------------|------------|--------|
| **Scope** | Full observability | Metrics only | Traces only |
| **Collection** | Push & Pull | Pull | Push |
| **Vendor Lock** | None | None | None |
| **Standards** | OTLP | Prom format | OpenTracing |
| **Languages** | 11+ | 10+ | 10+ |

### Migration Path

```mermaid
graph LR
    subgraph "Existing"
        Prom[Prometheus Client]
        JClient[Jaeger Client]
        Zip[Zipkin]
    end
    
    subgraph "Migrate To"
        OTel[OpenTelemetry SDK]
    end
    
    Prom --> |Shim| OTel
    JClient --> |Shim| OTel
    Zip --> |Shim| OTel
```

---

## OpenTelemetry Protocol (OTLP)

The native protocol for transmitting telemetry data.

### Protocol Options

| Transport | Use Case |
|-----------|----------|
| **gRPC** | High throughput, streaming |
| **HTTP/protobuf** | Wide compatibility |
| **HTTP/JSON** | Debugging, simple setup |

### OTLP Message Structure

```protobuf
message TracesData {
  repeated ResourceSpans resource_spans = 1;
}

message ResourceSpans {
  Resource resource = 1;
  repeated ScopeSpans scope_spans = 2;
}

message ScopeSpans {
  InstrumentationScope scope = 1;
  repeated Span spans = 2;
}
```

### Export Example

```python
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

exporter = OTLPSpanExporter(
    endpoint="localhost:4317",
    insecure=True
)
```

---

## Getting Started

### Installation (Python)

```bash
# Core packages
pip install opentelemetry-api opentelemetry-sdk

# OTLP exporter
pip install opentelemetry-exporter-otlp

# Auto-instrumentation
pip install opentelemetry-instrumentation
```

### Basic Setup

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Set up the TracerProvider
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Get a tracer
tracer = trace.get_tracer(__name__)

# Create a span
with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("key", "value")
    # Your code here
```

---

## Environment Variables

Common configuration via environment variables:

| Variable | Description |
|----------|-------------|
| `OTEL_SERVICE_NAME` | Service name for all telemetry |
| `OTEL_RESOURCE_ATTRIBUTES` | Additional resource attributes |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP endpoint URL |
| `OTEL_TRACES_SAMPLER` | Sampling strategy |
| `OTEL_PROPAGATORS` | Context propagation format |

```bash
export OTEL_SERVICE_NAME="my-service"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
export OTEL_TRACES_SAMPLER="parentbased_traceidratio"
export OTEL_TRACES_SAMPLER_ARG="0.1"
```

---

## Semantic Conventions

Standard attribute names for common concepts:

### Service Attributes

```python
from opentelemetry.sdk.resources import Resource

resource = Resource.create({
    "service.name": "order-service",
    "service.version": "1.2.3",
    "service.namespace": "shop",
    "deployment.environment": "production"
})
```

### HTTP Attributes

| Attribute | Example |
|-----------|---------|
| `http.request.method` | GET |
| `http.route` | /users/:id |
| `http.response.status_code` | 200 |
| `url.path` | /users/123 |
| `server.address` | api.example.com |

### Database Attributes

| Attribute | Example |
|-----------|---------|
| `db.system` | postgresql |
| `db.operation.name` | SELECT |
| `db.query.text` | SELECT * FROM users |
| `db.namespace` | mydb |

---

## Architecture Patterns

### Direct Export

```mermaid
graph LR
    App[Application] --> |OTLP| Backend[Backend]
```

Simple but limited flexibility.

### Collector as Agent

```mermaid
graph LR
    App1[App 1] --> Agent1[Collector Agent]
    App2[App 2] --> Agent2[Collector Agent]
    Agent1 --> |OTLP| Backend
    Agent2 --> |OTLP| Backend
```

Per-host collectors for local processing.

### Collector as Gateway

```mermaid
graph LR
    App1[App 1] --> Gateway[Collector Gateway]
    App2[App 2] --> Gateway
    App3[App 3] --> Gateway
    Gateway --> B1[Backend 1]
    Gateway --> B2[Backend 2]
```

Centralized processing and routing.

### Full Pipeline

```mermaid
graph LR
    App1[App] --> Agent[Agent]
    Agent --> Gateway[Gateway]
    Gateway --> J[Jaeger]
    Gateway --> P[Prometheus]
    Gateway --> L[Loki]
```

Combines agent and gateway for maximum flexibility.

---

## Next Steps

- **[Traces](02_traces.md)** - Deep dive into distributed tracing
- **[Metrics](03_metrics.md)** - Understanding metrics collection
- **[Logs](04_logs.md)** - Structured logging with OTel
- **[Collector](05_collector.md)** - Setting up the OTel Collector
