package com.ashish.thread;

import java.time.Duration;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

/**
 * COMPREHENSIVE GUIDE TO VIRTUAL THREADS (Java 21+)
 * <p>
 * Demonstrates:
 * 1. Massive Scale (100k threads)
 * 2. Blocking (Sleep) without consuming OS threads.
 * 3. Platform vs Virtual comparison.
 * </p>
 *
 * <pre>
 * <b>VISUALIZATION: M:N Scheduling</b>
 *
 *   Virtual Threads (Millions)
 *   [VT] [VT] [VT] [VT] [VT] ...
 *     \    |    /    /
 *      \   |   /    /   (Mount/Unmount)
 *       v  v  v    v
 *   +------------------+
 *   | Carrier Threads  |  (ForkJoinPool)
 *   | [CT] [CT] [CT]   |  (Matches CPU Cores)
 *   +--------+---------+
 *            |
 *            v
 *        OS Kernal
 * </pre>
 */
public class VirtualThreadsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. PLATFORM THREADS (The Limit) ===");
        // Try creating 100,000 platform threads -> OutOfMemoryError
        // demoPlatformThreads(); // Uncomment to crash your JVM

        System.out.println("=== 2. VIRTUAL THREADS (The Scale) ===");
        demoVirtualThreads();

        System.out.println("\n=== 3. HOW IT WORKS (Carrier Threads) ===");
        demoCarrierIdentification();
    }

    private static void demoPlatformThreads() {
        try (var executor = Executors.newCachedThreadPool()) {
            IntStream.range(0, 100_000).forEach(i -> {
                executor.submit(() -> {
                    try {
                        Thread.sleep(Duration.ofSeconds(1));
                    } catch (Exception e) {
                    }
                });
            });
        }
    }

    private static void demoVirtualThreads() {
        long start = System.currentTimeMillis();

        // Try-with-resources auto-waits for all threads to finish
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {

            // Launch 100,000 tasks
            IntStream.range(0, 100_000).forEach(i -> {
                executor.submit(() -> {
                    // When this sleeps, the Virtual Thread unmounts.
                    // The Carrier Thread (OS Thread) goes to do other work.
                    // It does NOT block the OS thread.
                    try {
                        Thread.sleep(Duration.ofMillis(50));
                    } catch (InterruptedException e) {
                    }
                    return i;
                });
            });
        }

        long end = System.currentTimeMillis();
        // This finishes in ~500-1000ms on a laptop.
        // 100k platform threads would take minutes or crash.
        System.out.println("Executed 100,000 tasks in " + (end - start) + "ms");
    }

    private static void demoCarrierIdentification() {
        // Run a few virtual threads and print their string representation
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 3; i++) {
                executor.submit(() -> {
                    System.out.println("I am: " + Thread.currentThread());
                    // Output looks like: VirtualThread[#21]/runnable@ForkJoinPool-1-worker-1
                    // "ForkJoinPool-1-worker-1" is the CARRIER (OS) Tread.
                });
            }
        }
    }
}
