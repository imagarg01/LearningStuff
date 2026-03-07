# Makefile for Java Examples
# This Makefile provides convenient targets to compile and run all Java examples

.PHONY: help compile clean all-examples

# Default target - show help
help:
	@echo "Java Examples - Available targets:"
	@echo ""
	@echo "=== Compilation ==="
	@echo "  make compile              - Compile all Java source files"
	@echo "  make clean                - Clean compiled files"
	@echo ""
	@echo "=== Scoped Values Examples ==="
	@echo "  make scoped-basic         - BasicScopedValueExample"
	@echo "  make scoped-web           - WebRequestContextExample"
	@echo "  make scoped-comparison    - ThreadLocalVsScopedValue"
	@echo "  make scoped-advanced      - AdvancedPatternsExample"
	@echo ""
	@echo "=== Concurrency Examples ==="
	@echo "  make blocking-queue       - BlockingQueueDemo"
	@echo "  make advanced-queues      - AdvancedQueuesDemo"
	@echo "  make completable-future   - CompletableFutureDemo"
	@echo "  make concurrent-collections - ConcurrentCollectionsDemo"
	@echo "  make coordination         - CoordinationDemo"
	@echo "  make executor-service     - ExecutorServiceDemo"
	@echo "  make parallel-stream      - ParallelStreamDemo"
	@echo "  make synchronization      - SynchronizationDemo"
	@echo "  make thread-lifecycle     - ThreadLifecycleDemo"
	@echo ""
	@echo "=== Virtual Threads & Structured Concurrency ==="
	@echo "  make virtual-threads      - VirtualThreadsDemo"
	@echo "  make playing-vt           - PlayingWithVT"
	@echo "  make structured-concurrency - StructuredConcurrencyDemo"
	@echo "  make playing-sc           - PlayingWithSC"
	@echo "  make custom-sc-policy     - CustomStructuredPolicyExample"
	@echo ""
	@echo "=== Performance Examples ==="
	@echo "  make flamegraph           - FlamegraphExample"
	@echo "  make flamegraph-app       - FlamegraphSpringBootApp (Spring Boot)"
	@echo ""
	@echo "=== Run All ==="
	@echo "  make all-scoped           - Run all Scoped Values examples"
	@echo "  make all-concurrency      - Run all Concurrency examples"
	@echo "  make all-virtual-threads  - Run all Virtual Threads examples"
	@echo ""

# Compile all source files
compile:
	@echo "Compiling Java source files..."
	mvn clean compile

# Clean compiled files
clean:
	@echo "Cleaning compiled files..."
	mvn clean

# ============================================
# Scoped Values Examples
# ============================================

scoped-basic:
	@echo "Running BasicScopedValueExample..."
	@echo "===================================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.BasicScopedValueExample"

scoped-web:
	@echo "Running WebRequestContextExample..."
	@echo "====================================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.WebRequestContextExample"

scoped-comparison:
	@echo "Running ThreadLocalVsScopedValue..."
	@echo "====================================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.ThreadLocalVsScopedValue"

scoped-advanced:
	@echo "Running AdvancedPatternsExample..."
	@echo "===================================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.AdvancedPatternsExample"

all-scoped: scoped-basic scoped-web scoped-comparison scoped-advanced
	@echo ""
	@echo "✓ All Scoped Values examples completed!"

# ============================================
# Concurrency Examples
# ============================================

blocking-queue:
	@echo "Running BlockingQueueDemo..."
	@echo "============================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.BlockingQueueDemo"

advanced-queues:
	@echo "Running AdvancedQueuesDemo..."
	@echo "=============================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.AdvancedQueuesDemo"

completable-future:
	@echo "Running CompletableFutureDemo..."
	@echo "=================================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.CompletableFutureDemo"

concurrent-collections:
	@echo "Running ConcurrentCollectionsDemo..."
	@echo "======================================"
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.ConcurrentCollectionsDemo"

coordination:
	@echo "Running CoordinationDemo..."
	@echo "============================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.CoordinationDemo"

executor-service:
	@echo "Running ExecutorServiceDemo..."
	@echo "==============================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.ExecutorServiceDemo"

parallel-stream:
	@echo "Running ParallelStreamDemo..."
	@echo "=============================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.ParallelStreamDemo"

synchronization:
	@echo "Running SynchronizationDemo..."
	@echo "==============================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.SynchronizationDemo"

thread-lifecycle:
	@echo "Running ThreadLifecycleDemo..."
	@echo "==============================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.ThreadLifecycleDemo"

all-concurrency: blocking-queue advanced-queues completable-future concurrent-collections coordination executor-service parallel-stream synchronization thread-lifecycle
	@echo ""
	@echo "✓ All Concurrency examples completed!"

# ============================================
# Virtual Threads & Structured Concurrency
# ============================================

virtual-threads:
	@echo "Running VirtualThreadsDemo..."
	@echo "=============================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.VirtualThreadsDemo"

playing-vt:
	@echo "Running PlayingWithVT..."
	@echo "========================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.PlayingWithVT"

structured-concurrency:
	@echo "Running StructuredConcurrencyDemo..."
	@echo "======================================"
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.StructuredConcurrencyDemo"

playing-sc:
	@echo "Running PlayingWithSC..."
	@echo "========================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.PlayingWithSC"

custom-sc-policy:
	@echo "Running CustomStructuredPolicyExample..."
	@echo "=========================================="
	mvn exec:exec -Dexec.mainClass="com.ashish.thread.CustomStructuredPolicyExample"

all-virtual-threads: virtual-threads playing-vt structured-concurrency playing-sc custom-sc-policy
	@echo ""
	@echo "✓ All Virtual Threads & Structured Concurrency examples completed!"

# ============================================
# Performance Examples
# ============================================

flamegraph:
	@echo "Running FlamegraphExample..."
	@echo "============================="
	mvn exec:exec -Dexec.mainClass="com.learning.performance.FlamegraphExample"

flamegraph-app:
	@echo "Running FlamegraphSpringBootApp..."
	@echo "===================================="
	@echo "Note: This is a Spring Boot application. Use 'mvn spring-boot:run' instead."
	mvn spring-boot:run -Dstart-class=com.learning.performance.springboot.FlamegraphSpringBootApp

# ============================================
# Legacy aliases for backward compatibility
# ============================================

basic: scoped-basic
web-request: scoped-web
comparison: scoped-comparison
advanced: scoped-advanced
all-examples: all-scoped all-concurrency all-virtual-threads
	@echo ""
	@echo "✓✓✓ ALL EXAMPLES COMPLETED! ✓✓✓"

# ==============================================================================
# Observability Examples Project
# ==============================================================================

# Directory where the observability infrastructure lives
OBSERVABILITY_DIR=src/main/java/com/ashish/observability/infra
AGENT_JAR=opentelemetry-javaagent.jar

# 1. Download the OpenTelemetry Java Agent
obs-setup:
	@echo "⬇️ Downloading OpenTelemetry Java Agent..."
	@curl -L -O https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/latest/download/opentelemetry-javaagent.jar
	@echo "✅ Download complete."

# 2. Start the Observability Infrastructure (Grafana, Jaeger, Prometheus, Collector)
obs-infra-up:
	@echo "🐳 Starting Observability Infrastructure..."
	cd $$(OBSERVABILITY_DIR) && docker-compose up -d
	@echo "✅ Infrastructure running! Grafana: http://localhost:3000 | Jaeger: http://localhost:16686"

# 3. Stop the Observability Infrastructure
obs-infra-down:
	@echo "🛑 Stopping Observability Infrastructure..."
	cd $$(OBSERVABILITY_DIR) && docker-compose down

# 4. Run the Spring Boot App WITH the OpenTelemetry Agent attached
obs-run:
	@echo "🚀 Starting Spring Boot App with OpenTelemetry Agent..."
	@mvn spring-boot:run \
	  -Dstart-class=com.ashish.observability.ObservabilityApplication \
	  -Dspring-boot.run.jvmArguments="-javaagent:$(AGENT_JAR) -Dotel.service.name=observability-demo -Dotel.traces.exporter=otlp -Dotel.metrics.exporter=otlp -Dotel.logs.exporter=none -Dotel.exporter.otlp.endpoint=http://localhost:4317"

# 5. Run the K6 Load Test and Chaos Script
obs-load-test:
	@echo "🔥 Running K6 Load Test (Auto, Manual, and Chaos scenarios)..."
	k6 run src/main/java/com/ashish/observability/k6-script.js
