import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource

# 1. Setup the Tracer Provider
# This configures how traces are generated and where they are sent.
resource = Resource.create({
    "service.name": "basic-tracing-example",
    "service.version": "1.0.0"
})

provider = TracerProvider(resource=resource)

# We use the ConsoleSpanExporter to print traces to stdout for this example.
# In production, you would use OTLPSpanExporter to send to a Collector/Backend.
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Register the provider globally
trace.set_tracer_provider(provider)

# Get a tracer
tracer = trace.get_tracer(__name__)

def perform_subtask(task_id):
    # Create a child span
    with tracer.start_as_current_span(f"subtask-{task_id}") as span:
        span.set_attribute("task.id", task_id)
        span.add_event("Subtask started")
        
        # Simulate work
        time.sleep(0.1)
        
        span.add_event("Subtask finished")

def main():
    print("Starting basic tracing example...")
    
    # Start a root span
    with tracer.start_as_current_span("main-operation") as root_span:
        root_span.set_attribute("user.id", "123")
        root_span.set_attribute("priority", "high")
        
        print("Doing main work...")
        time.sleep(0.2)
        
        for i in range(3):
            perform_subtask(i)
            
    print("Trace completed. Check the console output above for span data.")

if __name__ == "__main__":
    main()
