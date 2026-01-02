package com.ashish.thread;

import java.math.BigInteger;
import java.time.Duration;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;

/**
 * Demonstrates various aspects of Virtual Threads in Java, including creation,
 * performance with I/O-bound vs CPU-bound operations, and comparison with
 * platform threads.
 */
public class PlayingWithVT {

    enum ThreadType {
        VIRTUAL_THREAD,
        PLATFORM_THREAD
    }

    // Use available processors for platform thread pool sizing
    private static final int THREAD_POOL_SIZE = Runtime.getRuntime().availableProcessors();
    private static final int TASK_LIMIT = 500; // Reduced for quick demo
    private static final int FACTORIAL_INPUT = 50_000; // Reduced for quick demo
    private static final int SLEEP_DURATION_SECONDS = 2; // Reduced for quick demo
    private static final int LARGE_VT_COUNT = 10_000;
    private static final int AWAIT_TIMEOUT_SECONDS = 30;

    /**
     * Main method demonstrating various scenarios.
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== 1. Ways to Create Virtual Threads ===");
        waysToCreateVT();

        System.out.println("\n=== 2. I/O Bound Task (Sleep) - Platform vs Virtual ===");
        // Platform Threads
        try (var es = Executors.newFixedThreadPool(THREAD_POOL_SIZE)) {
            observeHowSleepBehave(ThreadType.PLATFORM_THREAD, es, 100);
        }
        // Virtual Threads
        try (var es = Executors.newVirtualThreadPerTaskExecutor()) {
            observeHowSleepBehave(ThreadType.VIRTUAL_THREAD, es, 100);
        }

        System.out.println("\n=== 3. Large Scale Virtual Threads (10k tasks) ===");
        createLargeNumberOfVT();

        System.out.println("\n=== 4. CPU Intensive Task - Platform vs Virtual ===");
        // Platform Threads
        try (var es = Executors.newFixedThreadPool(THREAD_POOL_SIZE)) {
            observeHowCPUIntensiveOperationWork(ThreadType.PLATFORM_THREAD, es, TASK_LIMIT);
        }
        // Virtual Threads
        try (var es = Executors.newVirtualThreadPerTaskExecutor()) {
            observeHowCPUIntensiveOperationWork(ThreadType.VIRTUAL_THREAD, es, TASK_LIMIT);
        }

        System.out.println("\nDemonstration completed.");
    }

    /**
     * Demonstrates how to create virtual threads using Thread.startVirtualThread().
     */
    static void waysToCreateVT() throws InterruptedException {
        // Via Thread.startVirtualThread
        var vt = Thread
                .startVirtualThread(() -> System.out.println("  Hello from Virtual Thread (startVirtualThread)"));
        vt.join();

        // Via Thread.ofVirtual()
        var vt2 = Thread.ofVirtual().name("vt-test")
                .start(() -> System.out.println("  Hello from Virtual Thread (ofVirtual)"));
        vt2.join();
    }

    /**
     * Creates a large number of virtual threads to demonstrate scalability.
     * Each thread sleeps for a short duration to simulate I/O operations.
     */
    static void createLargeNumberOfVT() {
        long start = System.nanoTime();
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            IntStream.range(0, LARGE_VT_COUNT).forEach(i -> {
                executor.submit(() -> {
                    try {
                        Thread.sleep(Duration.ofMillis(50)); // Short sleep
                        // prevent widespread console spam, only print every 1000th
                        if (i % 1000 == 0) {
                            // System.out.printf(" Processing %d%n", i);
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            });
        } // try-with-resources attempts to close() which waits for all tasks to complete
        Duration elapsed = Duration.ofNanos(System.nanoTime() - start);
        System.out.printf("INFO - Launched and completed %d virtual threads in %d ms%n", LARGE_VT_COUNT,
                elapsed.toMillis());
    }

    /**
     * Observes the behavior of threads during sleep operations (I/O-bound
     * simulation).
     * Measures the total time taken for all tasks to complete.
     */
    static void observeHowSleepBehave(ThreadType type, ExecutorService executorService, int limit) {
        var start = System.nanoTime();
        System.out.printf("Starting Sleep Test with %s (Tasks: %d, Sleep: %ds)%n", type.name(), limit,
                SLEEP_DURATION_SECONDS);

        var sleep = Duration.ofSeconds(SLEEP_DURATION_SECONDS);
        for (int i = 0; i < limit; i++) {
            executorService.submit(() -> {
                try {
                    Thread.sleep(sleep);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }

        // Use the passed executor but don't close it inside here if we want to measure
        // strictly execution time
        // including close() wait.
        // In the main method we use try-with-resources which auto-closes.
        // However, for this timing measurement, we need to wait for completion.
        // But since the caller controls the lifecycle via try-with-resources blocks in
        // main,
        // we can't easily measure *just* this block's completion unless we own the
        // executor
        // or await termination here without closing.
        // Given the structure, we'll rely on the caller's close() implicit wait,
        // OR we can't measure accurate time inside this method for the *completion* of
        // all tasks
        // unless we use a CountDownLatch or similar.
        // For simplicity reusing existing logic: The caller (main) handles the scope,
        // so we can't measure *wall clock time for all tasks* inside here easily
        // without blocking.
        // Let's change the pattern: The caller measures time? Or we use a Latch.

        // Actually, let's just submit tasks here. Time measurement in the loop is
        // meaningless for async.
        // We'll trust the main method structure or fix this method to wait.

        // NOTE: The previous implementation called
        // shutdownExecutorAndWait(executorService)
        // which closed the executor passed in. This is generally bad practice if the
        // executor
        // was shared, but here it's passed specifically for this test.
        // If we keep that pattern:
        shutdownExecutorAndWait(executorService);

        var demoElapsed = Duration.ofNanos(System.nanoTime() - start);
        System.out.printf("INFO - Sleep test took %d seconds%n", demoElapsed.getSeconds());
    }

    /**
     * Observes the behavior of threads during CPU-intensive operations.
     */
    static void observeHowCPUIntensiveOperationWork(ThreadType type, ExecutorService executorService, int limit) {
        var start = System.nanoTime();
        System.out.printf("Starting CPU Intensive Test with %s (Tasks: %d)%n", type.name(), limit);

        for (int i = 0; i < limit; i++) {
            executorService.submit(() -> {
                var result = factorial(FACTORIAL_INPUT);
            });
        }

        // Wait for completion
        shutdownExecutorAndWait(executorService);

        var demoElapsed = Duration.ofNanos(System.nanoTime() - start);
        System.out.printf("INFO - CPU intensive test took %d seconds%n", demoElapsed.getSeconds());
    }

    /**
     * Safely shuts down an executor service and waits for termination.
     */
    private static void shutdownExecutorAndWait(ExecutorService executorService) {
        if (executorService.isShutdown())
            return;
        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(AWAIT_TIMEOUT_SECONDS, TimeUnit.SECONDS)) {
                executorService.shutdownNow();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            executorService.shutdownNow();
        }
    }

    private static BigInteger factorial(int n) {
        var result = BigInteger.ONE;
        for (int i = 2; i <= n; i++) {
            result = result.multiply(BigInteger.valueOf(i));
        }
        return result;
    }
}
