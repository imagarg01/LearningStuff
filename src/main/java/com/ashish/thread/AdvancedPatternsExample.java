package com.ashish.thread;

import java.time.Duration;
import java.util.concurrent.Callable;
import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.Executors;
import java.util.List;
import java.util.ArrayList;

/**
 * Advanced patterns and use cases for ScopedValue.
 * 
 * This example demonstrates:
 * 1. Multiple scoped values composition
 * 2. Nested scopes (different ScopedValues)
 * 3. Integration with Virtual Threads
 * 4. Integration with Structured Concurrency
 * 5. Error handling patterns
 * 6. Conditional scoping
 * 
 * @since Java 21
 */
public class AdvancedPatternsExample {

    // Multiple scoped values for different contexts
    private static final ScopedValue<String> TRACE_ID = ScopedValue.newInstance();
    private static final ScopedValue<String> SPAN_ID = ScopedValue.newInstance();
    private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();
    private static final ScopedValue<SecurityContext> SECURITY_CONTEXT = ScopedValue.newInstance();

    public static void main(String[] args) throws Exception {
        System.out.println("=== Advanced ScopedValue Patterns ===\n");

        // Example 1: Multiple scoped values
        example1_MultipleValues();

        // Example 2: Nested scopes (different values)
        example2_NestedScopes();

        // Example 3: Integration with Virtual Threads
        example3_VirtualThreads();

        // Example 4: Integration with Structured Concurrency
        example4_StructuredConcurrency();

        // Example 5: Error handling
        example5_ErrorHandling();

        // Example 6: Conditional scoping
        example6_ConditionalScoping();
    }

    /**
     * Example 1: Composing multiple scoped values
     */
    private static void example1_MultipleValues() {
        System.out.println("--- Example 1: Multiple Scoped Values ---");

        // Bind multiple values for distributed tracing
        ScopedValue.where(TRACE_ID, "trace-12345")
                .where(SPAN_ID, "span-001")
                .where(USER_ID, "user-alice")
                .run(() -> {
                    logWithContext("Processing request");

                    // All three values are accessible
                    performOperation();
                });

        System.out.println();
    }

    private static void logWithContext(String message) {
        System.out.printf("[Trace: %s] [Span: %s] [User: %s] %s%n",
                TRACE_ID.orElse("none"),
                SPAN_ID.orElse("none"),
                USER_ID.orElse("none"),
                message);
    }

    private static void performOperation() {
        logWithContext("Executing operation");
    }

    /**
     * Example 2: Nested scopes with different ScopedValues
     */
    private static void example2_NestedScopes() {
        System.out.println("--- Example 2: Nested Scopes ---");

        // Outer scope: Set trace context
        ScopedValue.where(TRACE_ID, "trace-67890").run(() -> {
            System.out.println("Outer scope - Trace: " + TRACE_ID.get());
            System.out.println("Outer scope - Span bound? " + SPAN_ID.isBound());

            // Inner scope: Add span context (different ScopedValue)
            ScopedValue.where(SPAN_ID, "span-002").run(() -> {
                System.out.println("Inner scope - Trace: " + TRACE_ID.get()); // Inherited
                System.out.println("Inner scope - Span: " + SPAN_ID.get()); // New binding

                // Both values are accessible in inner scope
                logWithContext("In nested scope");
            });

            // Back to outer scope - SPAN_ID no longer bound
            System.out.println("Back to outer - Span bound? " + SPAN_ID.isBound());
        });

        System.out.println();
    }

    /**
     * Example 3: Integration with Virtual Threads
     */
    private static void example3_VirtualThreads() throws InterruptedException {
        System.out.println("--- Example 3: Virtual Threads Integration ---");

        // Process multiple tasks concurrently with shared context
        ScopedValue.where(TRACE_ID, "trace-vt-001").run(() -> {
            try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {

                // Submit multiple tasks - all inherit TRACE_ID
                for (int i = 1; i <= 3; i++) {
                    final int taskNum = i;
                    executor.submit(() -> {
                        // Each task has its own SPAN_ID but shares TRACE_ID
                        ScopedValue.where(SPAN_ID, "span-" + taskNum).run(() -> {
                            logWithContext("Task " + taskNum + " executing");
                            simulateWork(50);
                            logWithContext("Task " + taskNum + " completed");
                        });
                    });
                }
            }
        });

        System.out.println();
    }

    /**
     * Example 4: Integration with Structured Concurrency
     */
    private static void example4_StructuredConcurrency() throws Exception {
        System.out.println("--- Example 4: Structured Concurrency Integration ---");

        // Use ScopedValue with Structured Concurrency
        String result = ScopedValue.where(TRACE_ID, "trace-sc-001")
                .where(USER_ID, "user-bob")
                .call(() -> fetchUserDataWithStructuredConcurrency());

        System.out.println("Result: " + result);
        System.out.println();
    }

    private static String fetchUserDataWithStructuredConcurrency() throws Exception {
        logWithContext("Starting structured concurrent fetch");

        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {

            // Fork multiple subtasks - all inherit scoped values
            var profileTask = scope.fork(() -> {
                logWithContext("Fetching user profile");
                simulateWork(100);
                return "Profile[name=Bob]";
            });

            var ordersTask = scope.fork(() -> {
                logWithContext("Fetching user orders");
                simulateWork(150);
                return "Orders[count=5]";
            });

            var preferencesTask = scope.fork(() -> {
                logWithContext("Fetching user preferences");
                simulateWork(80);
                return "Preferences[theme=dark]";
            });

            // Wait for all tasks to complete
            scope.join();
            scope.throwIfFailed();

            // Combine results
            String combined = String.format("%s, %s, %s",
                    profileTask.get(),
                    ordersTask.get(),
                    preferencesTask.get());

            logWithContext("All data fetched successfully");
            return combined;
        }
    }

    /**
     * Example 5: Error handling patterns
     */
    private static void example5_ErrorHandling() {
        System.out.println("--- Example 5: Error Handling ---");

        // Pattern 1: Safe access with orElse
        String traceId = TRACE_ID.orElse("no-trace");
        System.out.println("Safe access: " + traceId);

        // Pattern 2: Conditional execution
        if (TRACE_ID.isBound()) {
            System.out.println("Trace ID: " + TRACE_ID.get());
        } else {
            System.out.println("No trace context available");
        }

        // Pattern 3: Exception handling within scope
        try {
            ScopedValue.where(TRACE_ID, "trace-error-001").run(() -> {
                logWithContext("Starting risky operation");

                try {
                    riskyOperation();
                } catch (Exception e) {
                    // Error handling still has access to scoped values
                    logWithContext("Error occurred: " + e.getMessage());
                }

                logWithContext("Cleanup completed");
            });
        } catch (Exception e) {
            System.out.println("Outer exception handler");
        }

        // Pattern 4: Using call() with checked exceptions
        try {
            String result = ScopedValue.where(TRACE_ID, "trace-checked-001")
                    .call(() -> operationWithCheckedException());
            System.out.println("Result: " + result);
        } catch (Exception e) {
            System.out.println("Caught checked exception: " + e.getMessage());
        }

        System.out.println();
    }

    private static void riskyOperation() {
        if (Math.random() > 0.5) {
            throw new RuntimeException("Simulated error");
        }
    }

    private static String operationWithCheckedException() throws Exception {
        logWithContext("Executing operation with checked exception");
        return "Success";
    }

    /**
     * Example 6: Conditional scoping based on context
     */
    private static void example6_ConditionalScoping() {
        System.out.println("--- Example 6: Conditional Scoping ---");

        // Scenario: Only set security context for authenticated users
        processRequest("authenticated-user", true);
        processRequest("anonymous-user", false);

        System.out.println();
    }

    private static void processRequest(String userId, boolean isAuthenticated) {
        if (isAuthenticated) {
            // Set full security context for authenticated users
            SecurityContext securityContext = new SecurityContext(userId, List.of("READ", "WRITE"));

            ScopedValue.where(USER_ID, userId)
                    .where(SECURITY_CONTEXT, securityContext)
                    .run(() -> {
                        performSecureOperation();
                    });
        } else {
            // Limited context for anonymous users
            ScopedValue.where(USER_ID, userId).run(() -> {
                performLimitedOperation();
            });
        }
    }

    private static void performSecureOperation() {
        SecurityContext ctx = SECURITY_CONTEXT.get();
        System.out.printf("Secure operation for %s with permissions: %s%n",
                USER_ID.get(), ctx.permissions());
    }

    private static void performLimitedOperation() {
        System.out.printf("Limited operation for %s (no security context)%n",
                USER_ID.get());
    }

    // Helper methods
    private static void simulateWork(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    // Helper record for security context
    private record SecurityContext(String userId, List<String> permissions) {
    }
}

/**
 * KEY TAKEAWAYS:
 * 
 * 1. COMPOSITION: Multiple ScopedValues can be bound together for rich context
 * 
 * 2. NESTING: Different ScopedValues can be nested (but same one cannot be
 * rebound)
 * 
 * 3. VIRTUAL THREADS: ScopedValues are inherited automatically and efficiently
 * 
 * 4. STRUCTURED CONCURRENCY: Perfect integration - all forked tasks inherit
 * values
 * 
 * 5. ERROR HANDLING: Use isBound(), orElse(), and try-catch for robust code
 * 
 * 6. CONDITIONAL SCOPING: Set different contexts based on runtime conditions
 * 
 * BEST PRACTICES:
 * - Keep scoped values immutable
 * - Use records or immutable classes as values
 * - Combine with Virtual Threads and Structured Concurrency
 * - Always check isBound() when access is optional
 * - Use meaningful names for scoped values (TRACE_ID, USER_ID, etc.)
 */
