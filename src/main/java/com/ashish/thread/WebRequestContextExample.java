package com.ashish.thread;

import java.time.Instant;
import java.util.UUID;
import java.util.concurrent.Executors;

/**
 * Realistic example of using ScopedValue for web request context.
 * 
 * This simulates a web application where request context (request ID, user ID,
 * timestamp)
 * needs to be available throughout the request processing pipeline without
 * passing
 * parameters through every method.
 * 
 * Demonstrates:
 * 1. Request context propagation across service layers
 * 2. Automatic availability in all methods within the request scope
 * 3. Thread safety with concurrent requests
 * 4. Integration with Virtual Threads
 * 
 * @since Java 21
 */
public class WebRequestContextExample {

    // Define scoped values for request context
    private static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();
    private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();
    private static final ScopedValue<Instant> REQUEST_TIME = ScopedValue.newInstance();

    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Web Request Context Example ===\n");

        // Simulate handling multiple concurrent requests
        simulateWebServer();
    }

    /**
     * Simulates a web server handling multiple concurrent requests
     */
    private static void simulateWebServer() throws InterruptedException {
        System.out.println("Starting web server simulation...\n");

        // Use Virtual Thread executor for handling requests
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {

            // Simulate 5 concurrent requests
            for (int i = 1; i <= 5; i++) {
                String userId = "user" + i;
                executor.submit(() -> handleRequest(userId));

                // Small delay to make output more readable
                Thread.sleep(100);
            }
        }

        System.out.println("\nAll requests processed!");
    }

    /**
     * Entry point for handling a web request.
     * This is where we establish the request context scope.
     */
    private static void handleRequest(String userId) {
        // Generate request-specific context
        String requestId = UUID.randomUUID().toString().substring(0, 8);
        Instant requestTime = Instant.now();

        // Bind all context values for this request scope
        ScopedValue.where(REQUEST_ID, requestId)
                .where(USER_ID, userId)
                .where(REQUEST_TIME, requestTime)
                .run(() -> {
                    // All code within this scope has access to the context
                    logRequestStart();
                    processRequest();
                    logRequestEnd();
                });
        // Context is automatically cleaned up when scope exits
    }

    /**
     * Simulates request processing through multiple layers
     */
    private static void processRequest() {
        // Authenticate user
        authenticateUser();

        // Process business logic
        executeBusinessLogic();

        // Save to database
        saveToDatabase();
    }

    /**
     * Authentication layer - has automatic access to USER_ID
     */
    private static void authenticateUser() {
        String userId = USER_ID.get();
        log("Authenticating user: " + userId);

        // Simulate authentication logic
        if (userId.equals("user3")) {
            log("⚠️  User requires additional verification");
        } else {
            log("✓ User authenticated successfully");
        }
    }

    /**
     * Business logic layer - has access to all context
     */
    private static void executeBusinessLogic() {
        log("Executing business logic");

        // Simulate some business operations
        fetchUserProfile();
        calculateRecommendations();

        log("✓ Business logic completed");
    }

    private static void fetchUserProfile() {
        String userId = USER_ID.get();
        log("  → Fetching profile for " + userId);
        // Simulate database call
        simulateDelay(50);
    }

    private static void calculateRecommendations() {
        log("  → Calculating recommendations");
        // Simulate computation
        simulateDelay(30);
    }

    /**
     * Data access layer - has access to context for logging
     */
    private static void saveToDatabase() {
        log("Saving data to database");

        // The database layer can log with full context
        String userId = USER_ID.get();
        log("  → Saving data for user: " + userId);

        simulateDelay(40);
        log("✓ Data saved successfully");
    }

    /**
     * Logging utility that automatically includes request context
     */
    private static void log(String message) {
        // Logging automatically has access to all context
        String requestId = REQUEST_ID.get();
        String userId = USER_ID.get();
        Instant requestTime = REQUEST_TIME.get();

        long elapsedMs = Instant.now().toEpochMilli() - requestTime.toEpochMilli();

        System.out.printf("[%s] [%s] [+%dms] %s%n",
                requestId, userId, elapsedMs, message);
    }

    private static void logRequestStart() {
        log("========== Request Started ==========");
    }

    private static void logRequestEnd() {
        log("========== Request Completed ==========");
    }

    private static void simulateDelay(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

/**
 * OUTPUT EXAMPLE:
 * 
 * === Web Request Context Example ===
 * 
 * Starting web server simulation...
 * 
 * [a1b2c3d4] [user1] [+0ms] ========== Request Started ==========
 * [a1b2c3d4] [user1] [+1ms] Authenticating user: user1
 * [a1b2c3d4] [user1] [+2ms] ✓ User authenticated successfully
 * [a1b2c3d4] [user1] [+2ms] Executing business logic
 * [a1b2c3d4] [user1] [+3ms] → Fetching profile for user1
 * [e5f6g7h8] [user2] [+0ms] ========== Request Started ==========
 * [e5f6g7h8] [user2] [+1ms] Authenticating user: user2
 * [a1b2c3d4] [user1] [+54ms] → Calculating recommendations
 * [e5f6g7h8] [user2] [+2ms] ✓ User authenticated successfully
 * ...
 * 
 * Notice how each request maintains its own context (REQUEST_ID, USER_ID)
 * even when processing concurrently!
 */
