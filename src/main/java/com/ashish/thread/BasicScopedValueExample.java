package com.ashish.thread;

import java.util.UUID;

/**
 * Basic demonstration of Java ScopedValue API.
 * 
 * This example shows:
 * 1. Creating a ScopedValue
 * 2. Binding and accessing values
 * 3. Scope boundaries
 * 4. Inheritance to child threads
 * 
 * @since Java 21
 */
public class BasicScopedValueExample {

    // Create ScopedValue instances (typically static final)
    private static final ScopedValue<String> USER_NAME = ScopedValue.newInstance();
    private static final ScopedValue<Integer> REQUEST_COUNT = ScopedValue.newInstance();

    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Basic ScopedValue Example ===\n");

        // Example 1: Basic binding and access
        example1_BasicBinding();

        // Example 2: Multiple values
        example2_MultipleValues();

        // Example 3: Scope boundaries
        example3_ScopeBoundaries();

        // Example 4: Inheritance to child threads
        example4_ChildThreadInheritance();

        // Example 5: Safe access patterns
        example5_SafeAccess();
    }

    /**
     * Example 1: Basic binding and accessing a ScopedValue
     */
    private static void example1_BasicBinding() {
        System.out.println("--- Example 1: Basic Binding ---");

        // Bind a value and execute code within that scope
        ScopedValue.where(USER_NAME, "Alice").run(() -> {
            // Within this scope, USER_NAME is bound to "Alice"
            String name = USER_NAME.get();
            System.out.println("User name: " + name);

            // Call other methods that can access the scoped value
            greetUser();
        });

        System.out.println();
    }

    private static void greetUser() {
        // This method can access USER_NAME without it being passed as a parameter
        System.out.println("Hello, " + USER_NAME.get() + "!");
    }

    /**
     * Example 2: Binding multiple ScopedValues
     */
    private static void example2_MultipleValues() {
        System.out.println("--- Example 2: Multiple Values ---");

        // Bind multiple values using method chaining
        ScopedValue.where(USER_NAME, "Bob")
                .where(REQUEST_COUNT, 42)
                .run(() -> {
                    System.out.println("User: " + USER_NAME.get());
                    System.out.println("Request count: " + REQUEST_COUNT.get());
                    processRequest();
                });

        System.out.println();
    }

    private static void processRequest() {
        // Both scoped values are accessible here
        System.out.println("Processing request #" + REQUEST_COUNT.get() +
                " for user " + USER_NAME.get());
    }

    /**
     * Example 3: Understanding scope boundaries
     */
    private static void example3_ScopeBoundaries() {
        System.out.println("--- Example 3: Scope Boundaries ---");

        // Check if value is bound before accessing
        System.out.println("Is USER_NAME bound? " + USER_NAME.isBound()); // false

        ScopedValue.where(USER_NAME, "Charlie").run(() -> {
            System.out.println("Inside scope - Is USER_NAME bound? " + USER_NAME.isBound()); // true
            System.out.println("Inside scope - Value: " + USER_NAME.get());
        });

        // Outside the scope, the value is no longer bound
        System.out.println("Outside scope - Is USER_NAME bound? " + USER_NAME.isBound()); // false

        // Attempting to access outside scope would throw NoSuchElementException
        // System.out.println(USER_NAME.get()); // ❌ Would throw exception

        System.out.println();
    }

    /**
     * Example 4: ScopedValues are inherited by child threads
     * Note: Using StructuredTaskScope ensures proper inheritance
     */
    private static void example4_ChildThreadInheritance() throws InterruptedException {
        System.out.println("--- Example 4: Child Thread Inheritance ---");

        ScopedValue.where(USER_NAME, "David").run(() -> {
            System.out.println("Parent thread - User: " + USER_NAME.get());

            // Using StructuredTaskScope for proper ScopedValue inheritance
            try (var scope = new java.util.concurrent.StructuredTaskScope<String>()) {
                var childTask = scope.fork(() -> {
                    // Child thread automatically inherits the scoped value
                    String user = USER_NAME.get();
                    System.out.println("Child thread - User: " + user);
                    System.out.println("Child thread - Same value inherited!");
                    return user;
                });

                scope.join();
                System.out.println("Child task completed successfully");
            } catch (Exception e) {
                System.err.println("Error in child thread: " + e.getMessage());
            }
        });

        System.out.println();
    }

    /**
     * Example 5: Safe access patterns
     */
    private static void example5_SafeAccess() {
        System.out.println("--- Example 5: Safe Access Patterns ---");

        // Pattern 1: Check if bound
        if (USER_NAME.isBound()) {
            System.out.println("User: " + USER_NAME.get());
        } else {
            System.out.println("No user context available");
        }

        // Pattern 2: Provide default value
        String user = USER_NAME.orElse("Anonymous");
        System.out.println("User (with default): " + user);

        // Pattern 3: Use orElseThrow for required values
        ScopedValue.where(USER_NAME, "Eve").run(() -> {
            String requiredUser = USER_NAME.orElseThrow(() -> new IllegalStateException("User context is required"));
            System.out.println("Required user: " + requiredUser);
        });

        System.out.println();
    }
}
