package com.ashish.thread;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.StructuredTaskScope;
import java.util.function.Supplier;

/**
 * Demonstrates Structured Concurrency (Preview Feature).
 * Requires: --enable-preview --source 21
 */
public class StructuredConcurrencyDemo {

    public static void main(String[] args) {
        try {
            Response response = handleUserRequest();
            System.out.println(response);
        } catch (InterruptedException | ExecutionException e) {
            System.err.println("Request failed: " + e.getMessage());
        }
    }

    record Response(String user, String order) {
    }

    static Response handleUserRequest() throws InterruptedException, ExecutionException {

        // Scope allows us to fork concurrent subtasks
        // ShutdownOnFailure guarantees that if ONE fails, the other is Cancelled.
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {

            Supplier<String> userTask = scope.fork(() -> fetchUser());
            Supplier<String> orderTask = scope.fork(() -> fetchOrder());

            scope.join(); // Wait for both
            scope.throwIfFailed(); // Propagate errors

            return new Response(userTask.get(), orderTask.get());
        }
    }

    static String fetchUser() throws InterruptedException {
        Thread.sleep(100);
        return "Ashish";
    }

    static String fetchOrder() throws InterruptedException {
        Thread.sleep(200);
        return "Order #123";
    }
}
