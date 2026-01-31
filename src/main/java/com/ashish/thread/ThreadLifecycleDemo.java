package com.ashish.thread;

/**
 * Demonstrates the various states of a Java Thread.
 * <p>
 * States: NEW -> RUNNABLE -> (BLOCKED/WAITING/TIMED_WAITING) -> TERMINATED
 * </p>
 */
public class ThreadLifecycleDemo {

    public static void main(String[] args) throws InterruptedException {
        // 1. NEW
        Thread thread = new Thread(() -> {
            try {
                // 4. TIMED_WAITING
                Thread.sleep(1000);
                synchronized (ThreadLifecycleDemo.class) {
                    // 3. RUNNABLE (Running)
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });

        System.out.println("State after creation: " + thread.getState()); // NEW

        // 2. RUNNABLE
        thread.start();
        System.out.println("State after start: " + thread.getState()); // RUNNABLE

        // Wait for it to sleep
        Thread.sleep(100);
        System.out.println("State while sleeping: " + thread.getState()); // TIMED_WAITING

        thread.join();
        // 5. TERMINATED
        System.out.println("State after finish: " + thread.getState()); // TERMINATED
    }
}
