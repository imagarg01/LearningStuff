package com.ashish.thread;

import java.math.BigInteger;
import java.time.Duration;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;

/**
 * Demonstrates various aspects of Virtual Threads in Java, including creation,
 * performance with I/O-bound vs CPU-bound operations, and comparison with platform threads.
 */
public class PlayingWithVT {

    enum ThreadType {
        VIRTUAL_THREAD,
        PLATFORM_THREAD
    }

    private static final int THREAD_POOL_SIZE = 12;
    private static final int TASK_LIMIT = 1000;
    private static final int FACTORIAL_INPUT = 100_000;
    private static final int SLEEP_DURATION_SECONDS = 12;
    private static final int LARGE_VT_COUNT = 10_000;
    private static final int AWAIT_TIMEOUT_SECONDS = 60;
    private static final int LARGE_VT_SLEEP_SECONDS = 1;

    /**
     * Main method demonstrating CPU-intensive operations with platform threads.
     */
    public static void main(String[] args) throws InterruptedException {
        try (var executorService = Executors.newFixedThreadPool(THREAD_POOL_SIZE)) {
            observeHowCPUIntensiveOperationWork(ThreadType.PLATFORM_THREAD, executorService, TASK_LIMIT);
        }
        System.out.println("Demonstration completed");
    }



    /**
     * Demonstrates how to create virtual threads using Thread.startVirtualThread().
     */
    static void waysToCreateVT() throws InterruptedException {
        // Via Thread.startVirtualThread
        var vt = Thread.startVirtualThread(() -> System.out.println("Hello from Virtual Thread"));
        vt.join();
    }

    /**
     * Creates a large number of virtual threads to demonstrate scalability.
     * Each thread sleeps for a short duration to simulate I/O operations.
     */
    static void createLargeNumberOfVT() {
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            IntStream.range(0, LARGE_VT_COUNT).forEach(i -> {
                executor.submit(() -> {
                    try {
                        Thread.sleep(Duration.ofSeconds(LARGE_VT_SLEEP_SECONDS));
                        System.out.printf("Thread %s: is virtual %b%n", 
                            Thread.currentThread().getName(), 
                            Thread.currentThread().isVirtual());
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        throw new VirtualThreadException("Virtual thread was interrupted", e);
                    }
                });
            });
        }
    }

    /**
     * Observes the behavior of threads during sleep operations (I/O-bound simulation).
     * Measures the total time taken for all tasks to complete.
     *
     * @param type the type of thread (Virtual or Platform)
     * @param executorService the executor to submit tasks to
     * @param limit the number of tasks to submit
     */
    static void observeHowSleepBehave(ThreadType type, ExecutorService executorService, int limit) {
        var start = System.nanoTime();
        System.out.printf("Starting Sleep Test with %s%n", type.name());
        
        var sleep = Duration.ofSeconds(SLEEP_DURATION_SECONDS);
        for (int i = 0; i < limit; i++) {
            executorService.submit(() -> {
                try {
                    Thread.sleep(sleep);
                    System.out.printf("Thread %s: is virtual %b%n", 
                        Thread.currentThread().getName(), 
                        Thread.currentThread().isVirtual());
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    throw new VirtualThreadException("Thread was interrupted during sleep", e);
                }
            });
        }
        
        shutdownExecutorAndWait(executorService);
        
        var demoElapsed = Duration.ofNanos(System.nanoTime() - start);
        System.out.printf("INFO - Sleep test took %d seconds%n", demoElapsed.getSeconds());
    }

    /**
     * Observes the behavior of threads during CPU-intensive operations.
     * Each task computes a large factorial to simulate CPU-bound work.
     *
     * @param type the type of thread (Virtual or Platform)
     * @param executorService the executor to submit tasks to
     * @param limit the number of tasks to submit
     */
    static void observeHowCPUIntensiveOperationWork(ThreadType type, ExecutorService executorService, int limit) {
        var start = System.nanoTime();
        System.out.printf("Starting CPU Intensive Test with %s%n", type.name());

        for (int i = 0; i < limit; i++) {
            executorService.submit(() -> {
                var result = factorial(FACTORIAL_INPUT);
                // Optionally log thread information for debugging
                // System.out.printf("Thread %s computed factorial%n", Thread.currentThread().getName());
            });
        }
        
        shutdownExecutorAndWait(executorService);
        
        var demoElapsed = Duration.ofNanos(System.nanoTime() - start);
        System.out.printf("INFO - CPU intensive test took %d seconds%n", demoElapsed.getSeconds());
    }

    /**
     * Safely shuts down an executor service and waits for termination.
     *
     * @param executorService the executor service to shutdown
     */
    private static void shutdownExecutorAndWait(ExecutorService executorService) {
        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(AWAIT_TIMEOUT_SECONDS, TimeUnit.SECONDS)) {
                executorService.shutdownNow();
                if (!executorService.awaitTermination(10, TimeUnit.SECONDS)) {
                    System.err.println("Executor did not terminate gracefully");
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            executorService.shutdownNow();
        }
    }

    /**
     * Computes the factorial of a number using BigInteger to handle large values.
     *
     * @param n the number to compute factorial for
     * @return the factorial result as BigInteger
     */
    private static BigInteger factorial(int n) {
        var result = BigInteger.ONE;
        for (int i = 2; i <= n; i++) {
            result = result.multiply(BigInteger.valueOf(i));
        }
        return result;
    }

    /**
     * Custom exception for virtual thread related errors.
     */
    static class VirtualThreadException extends RuntimeException {
        public VirtualThreadException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}
