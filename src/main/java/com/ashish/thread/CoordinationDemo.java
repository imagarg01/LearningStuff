package com.ashish.thread;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Semaphore;

/**
 * Demonstrates Semaphore (limiting access) and CountDownLatch (waiting for
 * events).
 *
 * <pre>
 * <b>Visual: Semaphore (Permits=2)</b>
 *
 *   [T1] [T2] [T3]  --->  (Semaphore: 2)
 *
 *   1. T1 acquire() -> OK (Sem=1)
 *   2. T2 acquire() -> OK (Sem=0)
 *   3. T3 acquire() -> BLOCKED (Sem=0) ...
 *   ...
 *   T1 release()    -> (Sem=1) -> T3 wakes up & acquires
 * </pre>
 *
 * <pre>
 * <b>Visual: CountDownLatch (Count=3)</b>
 *  
 *   Main Thread       Service 1    Service 2    Service 3
 *       |                 |            |            |
 *    await()............. |            |            |
 *     (WAIT)           countDown()     |            |
 *       :                 |         countDown()     |
 *       :                 |            |         countDown()
 *    (RESUME!) <------------------------------------+
 *       |
 * </pre>
 */
public class CoordinationDemo {

    public static void main(String[] args) throws InterruptedException {
        // --- SEMAPHORE ---
        System.out.println("--- SEMAPHORE (Limit 2) ---");
        Semaphore semaphore = new Semaphore(2);

        Runnable task = () -> {
            try {
                semaphore.acquire();
                System.out.println(Thread.currentThread().getName() + " acquired permit.");
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                System.out.println(Thread.currentThread().getName() + " releasing.");
                semaphore.release();
            }
        };

        for (int i = 0; i < 4; i++)
            new Thread(task).start();

        Thread.sleep(3000);

        // --- COUNT DOWN LATCH ---
        System.out.println("\n--- COUNT DOWN LATCH ---");
        CountDownLatch latch = new CountDownLatch(3);

        for (int i = 1; i <= 3; i++) {
            new Thread(() -> {
                System.out.println("Service initialized.");
                latch.countDown();
            }).start();
        }

        System.out.println("Main: Waiting for services...");
        latch.await(); // Blocks until count is 0
        System.out.println("Main: All services ready!");
    }
}
