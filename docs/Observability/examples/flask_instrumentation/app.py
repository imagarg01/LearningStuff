from flask import Flask, jsonify
import time
import logging

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# 1. Setup Resource
resource = Resource.create({
    "service.name": "flask-example",
    "deployment.environment": "development"
})

# 2. Setup Tracing
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(trace_provider)

# 3. Setup Metrics
metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=5000)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# 4. Setup Application
app = Flask(__name__)

# 5. Enable Auto-Instrumentation for Flask
FlaskInstrumentor().instrument_app(app)

# 6. Get Tracer and Meter
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

request_counter = meter.create_counter("custom_requests_total", description="Total custom requests")

@app.route("/")
def home():
    with tracer.start_as_current_span("home-handler"):
        request_counter.add(1, {"route": "/"})
        return jsonify({"message": "Hello, OpenTelemetry!"})

@app.route("/process")
def process():
    with tracer.start_as_current_span("heavy-processing") as span:
        request_counter.add(1, {"route": "/process"})
        
        span.set_attribute("data.size", 1024)
        
        # Simulate work
        time.sleep(0.5)
        
        return jsonify({"status": "processed", "took": "500ms"})

@app.route("/error")
def error_endpoint():
    with tracer.start_as_current_span("error-handler") as span:
        try:
            raise ValueError("Something went wrong!")
        except ValueError as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask app on port 5000...")
    app.run(port=5000)
