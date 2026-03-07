# Java Observability Examples: Zero-Code vs Manual

Welcome! This folder contains a fully working example demonstrating how to instrument a Spring Boot application using OpenTelemetry (OTel).

There are two primary endpoints in this project to help you understand the difference between letting the agent do everything ("Zero-Code") versus writing your own tracing logic ("Manual/With Code").

## Prerequisites

1. Docker and Docker Compose installed (for Grafana, Jaeger, Prometheus).
2. `k6` installed (`brew install k6`) for load testing.
3. Make sure you are in the ROOT of the `LearningStuff` repository.

## Step 1: Setup

First, download the OpenTelemetry Java Agent. This `.jar` file sits "around" our application and watches all the libraries we use (like Spring Web, JDBC, etc.).

```bash
make obs-setup
```

## Step 2: Start Infrastructure

Start the observability backend. This spins up:

- **OTel Collector**: The middleman that gathers our app's data.
- **Jaeger**: Where we view Distributed Traces (Port 16686).
- **Prometheus**: Where metrics are stored (Port 9090).
- **Grafana**: Where we view Dashboards (Port 3000).

```bash
make obs-infra-up
```

## Step 3: Run the Application

Now we run the Spring Boot app. **Crucially**, we attach the javaagent we downloaded in Step 1.

```bash
make obs-run
```

*If you look at the `Makefile`, you'll see we pass `-javaagent:opentelemetry-javaagent.jar` to the JVM!*

## Step 4: Generate Traffic & Chaos

Run the custom k6 script. This script acts as simulated users clicking around your app.

```bash
make obs-load-test
```

The script does 3 things:

1. Hits the `/api/orders/auto` endpoint (Zero-Code path).
2. Hits the `/api/orders/manual` endpoint (Manual path).
3. Hits the `/api/orders/manual?item=error` endpoint to simulate a **Chaos Exception**.

---

## Exploring the Results

### 1. View Dashboards in Grafana

Go to **<http://localhost:3000/d/a24ba8f8-b397-401d-bd21-1c39aa03a45c/java-observability-examples>**

Notice how the `business_orders_processed_total` chart is populated. This is a **custom metric** we created manually in `OrderService.java`.

### 2. View Traces in Jaeger

Go to **<http://localhost:16686>**

Search for traces from the `observability-demo` service.

- **The Auto Trace**: Click on a `POST /api/orders/auto` trace. Notice how OpenTelemetry captured the HTTP method, the URL, and the framework latency *without us writing a single line of tracing code*.
- **The Manual Trace**: Click on a `POST /api/orders/manual` trace. Notice it has a **child span** called `process_manual_order`. Look inside it! You will see custom tags like `order.item=Monitor`, `order.quantity=4`, and `business.tier=premium`.
- **The Chaos Trace**: Look for a trace marked in RED (Error). Dive into it. OpenTelemetry perfectly captured the Java Exception (`IllegalArgumentException: Invalid item name: 'error' triggers chaos scenario!`) and showed exactly which micro-operation failed.

## The Core Lesson

- **Zero-Code (Auto)** is amazing for getting basic HTTP/DB latency for free.
- **Manual (With Code)** is mandatory when you need to understand *business context* (e.g., tying a specific trace to a specific order ID or customer tier) or track specific business errors.
