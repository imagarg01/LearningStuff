package com.ashish.thread;

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * COMPREHENSIVE GUIDE TO EXECUTOR SERVICES
 * <p>
 * This class demonstrates the different types of Thread Pools, how to customize
 * them,
 * and when to use which.
 * </p>
 *
 * <pre>
 * <b>VISUALIZATION: How a Thread Pool Works</b>
 *
 *       Task Submission                    Executor Service
 *      ( main thread )                    ( The "Manager" )
 *     +----------------+             +--------------------------+
 *     | execute(Task1) | ---+------> |  [ Task Process Queue ]  |
 *     +----------------+    |        | [ T1 | T2 | T3 | T4 ... ]|
 *                           |        +-------------+------------+
 *     +----------------+    |                      |
 *     | execute(Task2) | ---+       +--------------v---------------+
 *     +----------------+            |      Thread Pool Workers     |
 *                                   | +------+  +------+  +------+ |
 *                                   | |  T1  |  |  T2  |  |  T3  | |
 *                                   | +------+  +------+  +------+ |
 *                                   +------------------------------+
 * </pre>
 */
public class ExecutorServiceDemo {

    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== 1. FIXED THREAD POOL ===");
        demoFixedThreadPool();

        System.out.println("\n=== 2. CACHED THREAD POOL ===");
        demoCachedThreadPool();

        System.out.println("\n=== 3. SCHEDULED THREAD POOL ===");
        demoScheduledThreadPool();

        System.out.println("\n=== 4. SINGLE THREAD EXECUTOR ===");
        demoSingleThreadExecutor();

        System.out.println("\n=== 5. CUSTOM THREAD POOL (The Power User way) ===");
        demoCustomThreadPool();
    }

    /**
     * WHEN TO USE:
     * - You have a known, stable load.
     * - You want to limit CPU usage (e.g., set size to CPU cores).
     * - Best for standard server applications.
     *
     * <pre>
     * <b>Visual: Fixed Pool (Size 2)</b>
     *
     *  Tasks: [T1] [T2] [T3]
     *           |    |    |
     * Pool:   +----+----+ |
     *         | Th1| Th2| | (Busy)
     *         +----+----+ |
     *                     |
     * Queue:  [ T3 ] <----+ (Waits)
     * </pre>
     */
    private static void demoFixedThreadPool() {
        // Reuse exactly 2 threads. If a 3rd task comes, it waits in a queue.
        try (ExecutorService executor = Executors.newFixedThreadPool(2)) {
            for (int i = 1; i <= 3; i++) {
                int id = i;
                executor.submit(() -> print("Fixed", id));
            }
        } // Auto-shutdown
    }

    /**
     * WHEN TO USE:
     * - You have unpredictable, short-lived tasks.
     * - You need high throughput and don't care about resource limits.
     * WARNING: Can crash your app (OOM) if tasks take too long, as it spawns
     * infinite threads!
     *
     * <pre>
     * <b>Visual: Cached Pool</b>
     *
     *  Tasks: [T1] [T2] [T3] ... [T100]
     *           |    |    |        |
     * Pool:   +--+ +--+ +--+ ... +--+
     *         |T1| |T2| |T3|     |Tn| (Grows infinitely)
     *         +--+ +--+ +--+     +--+
     * </pre>
     */
    private static void demoCachedThreadPool() {
        // Creates threads as needed. Reuses idle ones (60s life).
        try (ExecutorService executor = Executors.newCachedThreadPool()) {
            for (int i = 1; i <= 10; i++) {
                int id = i;
                // These might all run in parallel if the machine is fast enough
                executor.submit(() -> print("Cached", id));
            }
        }
    }

    /**
     * WHEN TO USE:
     * - You need to run tasks periodically (cron jobs, cleanup, heartbeats).
     * - Replaces the old java.util.Timer.
     *
     * <pre>
     * <b>Visual: Scheduled Pool</b>
     *
     * Time:  0ms    200ms   400ms   600ms
     *        |       |       |       |
     *        [Run]...[Run]...[Run]...[Run]
     * </pre>
     */
    private static void demoScheduledThreadPool() throws InterruptedException {
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);

        // Run once after delay
        scheduler.schedule(() -> System.out.println("[Scheduled] One-shot delayed task"),
                500, TimeUnit.MILLISECONDS);

        // Run continuously: Start at 0, repeat every 200ms
        // scheduleAtFixedRate: Strict frequency (overlap possible if task is slow)
        // scheduleWithFixedDelay: Wait for previous to finish + delay
        scheduler.scheduleAtFixedRate(() -> System.out.println("[Scheduled] Heartbeat..."),
                0, 200, TimeUnit.MILLISECONDS);

        Thread.sleep(1000); // Let it run for a bit
        scheduler.shutdown();
    }

    /**
     * WHEN TO USE:
     * - You need tasks to execute strictly sequentially (one after another).
     * - Great for Event Loops or managing a shared non-thread-safe resource.
     */
    private static void demoSingleThreadExecutor() {
        try (ExecutorService executor = Executors.newSingleThreadExecutor()) {
            // These will ALWAYS print in order 1, 2, 3
            executor.submit(() -> print("Single", 1));
            executor.submit(() -> print("Single", 2));
            executor.submit(() -> print("Single", 3));
        }
    }

    /**
     * THE PRO WAY:
     * - Executors.newFixed... are just wrappers around ThreadPoolExecutor.
     * - Use this when you need fine-grained control over Queue size, ThreadFactory,
     * or RejectionPolicy.
     */
    private static void demoCustomThreadPool() {
        int corePoolSize = 2; // Keep 2 threads alive
        int maxPoolSize = 4; // Go up to 4 if queue is full
        long keepAliveTime = 10; // Kill extra threads after 10s idle

        // Bounded Queue! (Crucial for stability)
        BlockingQueue<Runnable> queue = new ArrayBlockingQueue<>(2);

        // Custom Naming Factory
        ThreadFactory factory = r -> new Thread(r, "MyCustomPool-" + r.hashCode());

        // Rejection Policy: What if queue is full AND max threads are busy?
        // AbortPolicy (Default): Throw Exception
        // CallerRunsPolicy: Run in main thread (Slows down producer)
        RejectedExecutionHandler policy = new ThreadPoolExecutor.CallerRunsPolicy();

        ExecutorService executor = new ThreadPoolExecutor(
                corePoolSize, maxPoolSize, keepAliveTime, TimeUnit.SECONDS,
                queue, factory, policy);

        try {
            // Submit 10 tasks.
            // 2 run immediately (core)
            // 2 wait in queue
            // 2 spwan new threads (max)
            // Remaining 4 get rejected -> CallerRunsPolicy -> Main thread runs them!
            for (int i = 1; i <= 10; i++) {
                int id = i;
                executor.submit(() -> print("Custom", id));
            }
        } finally {
            executor.shutdown();
        }
    }

    private static void print(String type, int id) {
        System.out.println("[" + type + "] Task " + id + " on " + Thread.currentThread().getName());
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
        }
    }
}
