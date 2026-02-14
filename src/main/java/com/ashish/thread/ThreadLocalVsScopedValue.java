package com.ashish.thread;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.Executors;

/**
 * Side-by-side comparison of ThreadLocal vs ScopedValue.
 * 
 * This example demonstrates:
 * 1. Memory leak risks with ThreadLocal
 * 2. Automatic cleanup with ScopedValue
 * 3. Immutability benefits
 * 4. Performance differences with Virtual Threads
 * 5. Code clarity improvements
 * 
 * @since Java 21
 */
public class ThreadLocalVsScopedValue {

    // ThreadLocal approach
    private static final ThreadLocal<String> THREAD_LOCAL_USER = new ThreadLocal<>();

    // ScopedValue approach
    private static final ScopedValue<String> SCOPED_VALUE_USER = ScopedValue.newInstance();

    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== ThreadLocal vs ScopedValue Comparison ===\n");

        // Example 1: Memory leak demonstration
        example1_MemoryLeakRisk();

        // Example 2: Automatic cleanup
        example2_AutomaticCleanup();

        // Example 3: Immutability
        example3_Immutability();

        // Example 4: Thread pool safety
        example4_ThreadPoolSafety();

        // Example 5: Performance with Virtual Threads
        example5_PerformanceComparison();
    }

    /**
     * Example 1: ThreadLocal memory leak risk
     */
    private static void example1_MemoryLeakRisk() {
        System.out.println("--- Example 1: Memory Leak Risk ---");

        // ThreadLocal: Easy to forget cleanup
        THREAD_LOCAL_USER.set("Alice");
        processWithThreadLocal();
        // ❌ FORGOT TO CALL remove()!
        // In a thread pool, this value persists and causes memory leaks

        System.out.println("ThreadLocal value still present: " +
                (THREAD_LOCAL_USER.get() != null));

        // Cleanup (should have been in finally block)
        THREAD_LOCAL_USER.remove();

        // ScopedValue: Automatic cleanup
        ScopedValue.where(SCOPED_VALUE_USER, "Bob").run(() -> {
            processWithScopedValue();
        });
        // ✅ Automatically cleaned up

        System.out.println("ScopedValue bound after scope: " +
                SCOPED_VALUE_USER.isBound());

        System.out.println();
    }

    private static void processWithThreadLocal() {
        System.out.println("ThreadLocal processing: " + THREAD_LOCAL_USER.get());
    }

    private static void processWithScopedValue() {
        System.out.println("ScopedValue processing: " + SCOPED_VALUE_USER.get());
    }

    /**
     * Example 2: Proper cleanup patterns
     */
    private static void example2_AutomaticCleanup() {
        System.out.println("--- Example 2: Automatic Cleanup ---");

        // ThreadLocal: Requires try-finally
        try {
            THREAD_LOCAL_USER.set("Charlie");
            System.out.println("ThreadLocal (in try): " + THREAD_LOCAL_USER.get());

            // Simulate exception
            if (Math.random() > -1) {
                // Even with exception, finally ensures cleanup
            }
        } finally {
            THREAD_LOCAL_USER.remove(); // Must remember!
            System.out.println("ThreadLocal cleaned up in finally");
        }

        // ScopedValue: Automatic cleanup even with exceptions
        try {
            ScopedValue.where(SCOPED_VALUE_USER, "Diana").run(() -> {
                System.out.println("ScopedValue (in scope): " + SCOPED_VALUE_USER.get());

                // Even if exception occurs, cleanup is automatic
                if (Math.random() > -1) {
                    // Automatic cleanup
                }
            });
        } catch (Exception e) {
            // Handle exception
        }
        System.out.println("ScopedValue automatically cleaned up: " +
                !SCOPED_VALUE_USER.isBound());

        System.out.println();
    }

    /**
     * Example 3: Immutability vs Mutability
     */
    private static void example3_Immutability() {
        System.out.println("--- Example 3: Immutability ---");

        // ThreadLocal: Can be mutated anywhere
        THREAD_LOCAL_USER.set("Eve");
        System.out.println("ThreadLocal initial: " + THREAD_LOCAL_USER.get());

        mutateThreadLocal();
        System.out.println("ThreadLocal after mutation: " + THREAD_LOCAL_USER.get());
        THREAD_LOCAL_USER.remove();

        // ScopedValue: Immutable within scope
        ScopedValue.where(SCOPED_VALUE_USER, "Frank").run(() -> {
            System.out.println("ScopedValue initial: " + SCOPED_VALUE_USER.get());

            // Cannot rebind within the same scope
            try {
                ScopedValue.where(SCOPED_VALUE_USER, "Grace").run(() -> {
                    // This would throw IllegalStateException
                });
            } catch (IllegalStateException e) {
                System.out.println("✓ Cannot rebind ScopedValue in same scope (immutable)");
            }

            System.out.println("ScopedValue remains: " + SCOPED_VALUE_USER.get());
        });

        System.out.println();
    }

    private static void mutateThreadLocal() {
        // ThreadLocal can be changed anywhere
        THREAD_LOCAL_USER.set("Eve_Modified");
    }

    /**
     * Example 4: Thread pool safety
     */
    private static void example4_ThreadPoolSafety() throws InterruptedException {
        System.out.println("--- Example 4: Thread Pool Safety ---");

        // Simulate thread pool with 2 threads
        try (var executor = Executors.newFixedThreadPool(2)) {

            // Task 1: Sets ThreadLocal but forgets to clean up
            executor.submit(() -> {
                THREAD_LOCAL_USER.set("Task1_User");
                System.out.println("Task 1: " + THREAD_LOCAL_USER.get());
                // ❌ Forgot to remove!
            });

            Thread.sleep(100);

            // Task 2: Might reuse the same thread and see stale data
            executor.submit(() -> {
                String user = THREAD_LOCAL_USER.get();
                if (user != null) {
                    System.out.println("⚠️  Task 2 sees stale ThreadLocal: " + user);
                } else {
                    System.out.println("Task 2: No ThreadLocal value");
                }
                THREAD_LOCAL_USER.remove();
            });

            Thread.sleep(100);

            // With ScopedValue: Always safe
            executor.submit(() -> {
                ScopedValue.where(SCOPED_VALUE_USER, "Task3_User").run(() -> {
                    System.out.println("Task 3: " + SCOPED_VALUE_USER.get());
                });
                // ✅ Automatically cleaned up
            });

            Thread.sleep(100);

            executor.submit(() -> {
                boolean bound = SCOPED_VALUE_USER.isBound();
                System.out.println("✓ Task 4: ScopedValue bound? " + bound + " (always clean)");
            });
        }

        System.out.println();
    }

    /**
     * Example 5: Performance comparison with Virtual Threads
     */
    private static void example5_PerformanceComparison() throws InterruptedException {
        System.out.println("--- Example 5: Performance Comparison ---");

        int numTasks = 10000;

        // Benchmark ThreadLocal
        long startThreadLocal = System.currentTimeMillis();
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < numTasks; i++) {
                executor.submit(() -> {
                    try {
                        THREAD_LOCAL_USER.set(UUID.randomUUID().toString());
                        String value = THREAD_LOCAL_USER.get();
                        // Simulate work
                    } finally {
                        THREAD_LOCAL_USER.remove();
                    }
                });
            }
        }
        long threadLocalTime = System.currentTimeMillis() - startThreadLocal;

        // Benchmark ScopedValue
        long startScopedValue = System.currentTimeMillis();
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < numTasks; i++) {
                executor.submit(() -> {
                    ScopedValue.where(SCOPED_VALUE_USER, UUID.randomUUID().toString())
                            .run(() -> {
                                String value = SCOPED_VALUE_USER.get();
                                // Simulate work
                            });
                });
            }
        }
        long scopedValueTime = System.currentTimeMillis() - startScopedValue;

        System.out.println("Performance with " + numTasks + " Virtual Threads:");
        System.out.println("  ThreadLocal:  " + threadLocalTime + "ms");
        System.out.println("  ScopedValue:  " + scopedValueTime + "ms");

        double improvement = ((double) (threadLocalTime - scopedValueTime) / threadLocalTime) * 100;
        System.out.printf("  ScopedValue is %.1f%% faster%n", improvement);

        System.out.println();
    }
}

/**
 * SUMMARY OF DIFFERENCES:
 * 
 * ┌─────────────────────┬────────────────────────┬────────────────────────┐
 * │ Aspect │ ThreadLocal │ ScopedValue │
 * ├─────────────────────┼────────────────────────┼────────────────────────┤
 * │ Cleanup │ Manual (remove()) │ Automatic │
 * │ Memory Leaks │ High risk │ No risk │
 * │ Mutability │ Mutable │ Immutable │
 * │ Thread Pool Safety │ Dangerous │ Safe │
 * │ Virtual Threads │ Works but slower │ Optimized │
 * │ Code Clarity │ Requires try-finally │ Clear scope boundaries │
 * │ Inheritance │ Optional │ Automatic │
 * └─────────────────────┴────────────────────────┴────────────────────────┘
 * 
 * RECOMMENDATION:
 * - Use ScopedValue for new code, especially with Virtual Threads
 * - Use ThreadLocal only for mutable state or legacy compatibility
 */
