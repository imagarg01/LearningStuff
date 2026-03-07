package com.ashish.observability.service;

import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.metrics.LongCounter;
import io.opentelemetry.api.metrics.Meter;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.StatusCode;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class OrderService {

    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);

    private final Tracer tracer;
    private final LongCounter ordersProcessedCounter;

    // We inject OpenTelemetry API here so we can create custom Spans and Metrics
    public OrderService(OpenTelemetry openTelemetry) {
        // 1. Get a Tracer for manual span creation
        this.tracer = openTelemetry.getTracer("com.ashish.observability.service.OrderService", "1.0.0");

        // 2. Get a Meter for manual metric creation
        Meter meter = openTelemetry.getMeter("com.ashish.observability.metrics");

        // 3. Create a custom business metric to track orders
        this.ordersProcessedCounter = meter
                .counterBuilder("business.orders.processed")
                .setDescription("Number of orders processed by the system")
                .setUnit("1")
                .build();
    }

    /**
     * ZERO-CODE APPROACH:
     * This method does not define any OpenTelemetry Spans directly.
     * However, because the OpenTelemetry Java Agent is running,
     * it will automatically capture the incoming HTTP request that led here.
     */
    public String processAutoOrder(String item) {
        logger.info("Processing auto order for item: {}", item);
        simulateDelay(100);
        return "Auto Order processed for " + item + " - ID: " + UUID.randomUUID().toString().substring(0, 8);
    }

    /**
     * MANUAL APPROACH:
     * Here we write custom code to explicitly create a deeper trace (Span),
     * add business tags (Attributes), handle specific errors, and increment a
     * business metric.
     */
    public String processManualOrder(String item, int quantity) {
        // Increment our custom metric
        ordersProcessedCounter.add(quantity);

        // Start a new manual span. It will automatically attach as a child
        // to the auto-instrumented HTTP request span!
        Span span = tracer.spanBuilder("process_manual_order").startSpan();

        // Make this span the "current" active span in the thread context
        try (Scope scope = span.makeCurrent()) {

            // Add custom business attributes that the Auto agent wouldn't know about
            span.setAttribute("order.item", item);
            span.setAttribute("order.quantity", quantity);
            span.setAttribute("business.tier", "premium");

            logger.info("Processing manual order logic for item: {}", item);

            // Simulate chaos error handling
            if ("error".equalsIgnoreCase(item)) {
                // Record the exact business exception in the trace
                throw new IllegalArgumentException("Invalid item name: 'error' triggers chaos scenario!");
            }

            simulateDelay(250);

            String id = UUID.randomUUID().toString().substring(0, 8);
            span.setAttribute("order.id", id);

            // Mark trace as successful
            span.setStatus(StatusCode.OK);
            return "Manual Order processed for " + item + " (x" + quantity + ") - ID: " + id;

        } catch (Exception e) {
            // Mark trace as failed and attach the exception
            span.setStatus(StatusCode.ERROR, e.getMessage());
            span.recordException(e);
            throw e;
        } finally {
            // ALWAYS end the span in a finally block
            span.end();
        }
    }

    private void simulateDelay(long millis) {
        try {
            Thread.sleep(millis + (long) (Math.random() * 50));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
