package com.ashish.thread;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

/**
 * Demonstrates Producer-Consumer using BlockingQueue.
 *
 * <pre>
 * <b>Visual: Blocking Queue (Capacity 2)</b>
 *
 *   Producer TH            Queue [ ] [ ]              Consumer TH
 *
 *   1. put("A")  ----->   Queue [A] [ ]
 *   2. put("B")  ----->   Queue [A] [B]
 *   3. put("C")  ----->   BLOCKED (Wait) ...
 *                                      ----take()---> "A"
 *                         Queue [B] [ ]
 *       (Resumes)
 *   ... put("C") ----->   Queue [B] [C]
 * </pre>
 */
public class BlockingQueueDemo {

    public static void main(String[] args) {
        // Capacity of 2 items
        BlockingQueue<String> queue = new ArrayBlockingQueue<>(2);

        // Producer
        new Thread(() -> {
            try {
                for (int i = 1; i <= 5; i++) {
                    String msg = "Message " + i;
                    queue.put(msg); // Blocks if full
                    System.out.println("Produced: " + msg);
                    Thread.sleep(200);
                }
                queue.put("DONE");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }).start();

        // Consumer
        new Thread(() -> {
            try {
                while (true) {
                    Thread.sleep(1000); // Simulate slow processing
                    String msg = queue.take(); // Blocks if empty
                    if (msg.equals("DONE"))
                        break;
                    System.out.println("Consumed: " + msg);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }).start();
    }
}
