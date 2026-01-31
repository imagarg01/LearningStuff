package com.ashish.thread;

import java.util.concurrent.*;

/**
 * COMPREHENSIVE GUIDE TO ADVANCED QUEUES
 * <p>
 * Demonstrates:
 * 1. SynchronousQueue (0 Capacity Handoff)
 * 2. DelayQueue (Time-released tasks)
 * 3. LinkedTransferQueue (Wait for Consumer)
 * 4. PriorityBlockingQueue (Ordering)
 * </p>
 */
public class AdvancedQueuesDemo {

    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== 1. SYNCHRONOUS QUEUE (The Handoff) ===");
        demoSynchronousQueue();

        System.out.println("\n=== 2. DELAY QUEUE (The Scheduler) ===");
        demoDelayQueue();

        System.out.println("\n=== 3. TRANSFER QUEUE (The Receipt) ===");
        demoTransferQueue();

        System.out.println("\n=== 4. PRIORITY QUEUE (The VIP) ===");
        demoPriorityQueue();
    }

    /**
     * Capacity = 0.
     * Put waits for Take. Take waits for Put.
     * Used in CachedThreadPool.
     * 
     * <pre>
     * <b>Visual: Synchronous Handoff</b>
     * 
     *    Producer                Consumer
     *       |                       |
     *    put("A") --(Waits)-->   take()
     *       |       (Meet)          |
     *       +-----> [ "A" ] ------->+
     *       |                       |
     *    (Resumes)               (Resumes)
     * </pre>
     */
    private static void demoSynchronousQueue() {
        var queue = new SynchronousQueue<String>();

        new Thread(() -> {
            try {
                System.out.println("Producer: Offering 'Data'...");
                queue.put("Data"); // Will BLOCK here until consumer arrives
                System.out.println("Producer: Handoff complete!");
            } catch (InterruptedException e) {
            }
        }).start();

        sleep(1000);
        new Thread(() -> {
            try {
                System.out.println("Consumer: Taking...");
                String msg = queue.take(); // Unblocks producer
                System.out.println("Consumer: Got " + msg);
            } catch (InterruptedException e) {
            }
        }).start();

        sleep(2000);
    }

    /**
     * Elements are kept until their delay expires.
     * 
     * <pre>
     * <b>Visual: DelayQueue</b>
     * 
     *    [Task C (5s)] [Task B (2s)] [Task A (Expired)]
     *         |             |              |
     *      (Hidden)      (Hidden)       (Ready!)
     *                                      |
     *                                   take()
     * </pre>
     */
    private static void demoDelayQueue() throws InterruptedException {
        var queue = new DelayQueue<DelayedTask>();
        queue.put(new DelayedTask("Fast Task", 100));
        queue.put(new DelayedTask("Slow Task", 1000));

        long start = System.currentTimeMillis();
        System.out.println("Taking tasks...");

        // This will block 100ms
        System.out.println("Got: " + queue.take().name + " @" + (System.currentTimeMillis() - start) + "ms");

        // This will block until 1000ms mark
        System.out.println("Got: " + queue.take().name + " @" + (System.currentTimeMillis() - start) + "ms");
    }

    /**
     * Producer waits for Consumer to explicitly RECEIVE the element.
     * (More robust than SynchronousQueue, allows buffering too)
     */
    private static void demoTransferQueue() {
        var queue = new LinkedTransferQueue<String>();

        new Thread(() -> {
            try {
                System.out.println("Producer: Transferring 'Message'...");
                queue.transfer("Message"); // BLOCKS until consumed
                System.out.println("Producer: Consumer received it.");
            } catch (InterruptedException e) {
            }
        }).start();

        sleep(500);
        new Thread(() -> {
            try {
                System.out.println("Consumer: Taking...");
                queue.take();
            } catch (InterruptedException e) {
            }
        }).start();

        sleep(1000);
    }

    private static void demoPriorityQueue() throws InterruptedException {
        var queue = new PriorityBlockingQueue<Integer>();

        queue.put(10);
        queue.put(1); // High priority!
        queue.put(5);

        System.out.println("Priority Take: " + queue.take()); // 1
        System.out.println("Priority Take: " + queue.take()); // 5
        System.out.println("Priority Take: " + queue.take()); // 10
    }

    static class DelayedTask implements Delayed {
        String name;
        long startTime;

        public DelayedTask(String name, long delayMs) {
            this.name = name;
            this.startTime = System.currentTimeMillis() + delayMs;
        }

        @Override
        public long getDelay(TimeUnit unit) {
            long diff = startTime - System.currentTimeMillis();
            return unit.convert(diff, TimeUnit.MILLISECONDS);
        }

        @Override
        public int compareTo(Delayed o) {
            if (this.startTime < ((DelayedTask) o).startTime)
                return -1;
            if (this.startTime > ((DelayedTask) o).startTime)
                return 1;
            return 0;
        }
    }

    private static void sleep(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
        }
    }
}
