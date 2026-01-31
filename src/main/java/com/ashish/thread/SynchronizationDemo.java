package com.ashish.thread;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.StampedLock;

/**
 * COMPREHENSIVE GUIDE TO LOCKING
 *
 * <pre>
 * <b>VISUALIZATION: Lock vs Condition</b>
 *
 *      Thread A                  Thread B
 *     +---------+               +---------+
 *     |  Lock   |               |         |
 *     |    |    |               |         |
 *     |  await()| --releases--> |  time   |
 *     |  (wait) | <---signal--- |  Lock   |
 *     |    |    |               | signal()|
 *     |  Resume |               | Unlock  |
 *     +----+----+               +----+----+
 *          |                         |
 *     +----v-------------------------v----+
 *     |         Shared Resource           |
 *     +-----------------------------------+
 * </pre>
 */
public class SynchronizationDemo {

    // 1. REENTRANT LOCK (The Monitor Killer)
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();

    // 2. STAMPED LOCK (The Performance King)
    private final StampedLock stampedLock = new StampedLock();
    private double x, y;

    public static void main(String[] args) throws InterruptedException {
        SynchronizationDemo demo = new SynchronizationDemo();

        // Demo 1: Try Lock (Non-blocking)
        new Thread(demo::demoTryLock).start();
        new Thread(demo::demoTryLock).start();

        Thread.sleep(1000);

        // Demo 2: Conditions (Wait/Notify)
        new Thread(() -> demo.produce()).start();
        new Thread(() -> demo.consume()).start();

        // Demo 3: Optimistic Locking
        new Thread(demo::calculateDistanceOptimistic).start();
    }

    // --- CASE 1: Avoiding Deadlocks with tryLock() ---
    /**
     * <pre>
     * <b>Visual: tryLock(100ms)</b>
     *
     *   Thread A             Thread B
     *      |                    |
     *    Lock()               lock.tryLock(100ms)
     *      | (Holds Lock)       |
     *      |                    |-- (Waiting...)
     *      |                    |
     *      | (Still holding)    |-- (Timeout!) -> Returns FALSE
     * </pre>
     */
    public void demoTryLock() {
        try {
            // Wait max 100ms. If locked, give up.
            if (lock.tryLock(100, TimeUnit.MILLISECONDS)) {
                try {
                    System.out.println(Thread.currentThread().getName() + " got the lock!");
                    Thread.sleep(500);
                } finally {
                    lock.unlock();
                }
            } else {
                System.out.println(Thread.currentThread().getName() + " could NOT get lock, doing something else...");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    // --- CASE 2: Producer/Consumer with Conditions ---
    private int buffer = 0;
    private boolean hasData = false;

    public void produce() {
        lock.lock();
        try {
            while (hasData) {
                notFull.await(); // Releases lock, waits for signal
            }
            buffer++;
            System.out.println("Produced: " + buffer);
            hasData = true;
            notEmpty.signal(); // Wake up consumer
        } catch (InterruptedException e) {
        } finally {
            lock.unlock();
        }
    }

    public void consume() {
        lock.lock();
        try {
            while (!hasData) {
                notEmpty.await();
            }
            System.out.println("Consumed: " + buffer);
            hasData = false;
            notFull.signal();
        } catch (InterruptedException e) {
        } finally {
            lock.unlock();
        }
    }

    // --- CASE 3: StampedLock Optimistic Read ---
    /**
     * <pre>
     * <b>Visual: Optimistic Lock</b>
     *
     *   Reader Thread            Writer Thread
     *         |                        |
     *   tryOptimisticRead()            |
     *   (returns stamp 100)            |
     *         |                        |
     *   ...Reads X, Y...             writeLock()
     *         |                        |
     *   validate(100) -> FALSE! <----- (Changes Stamp to 101)
     *         |                        |
     *   (Retry with full Lock)       unlock()
     * </pre>
     */
    public void calculateDistanceOptimistic() {
        long stamp = stampedLock.tryOptimisticRead(); // No lock taken!
        double currentX = x;
        double currentY = y;

        // Did someone write while I was reading?
        if (!stampedLock.validate(stamp)) {
            // Fallback to read lock
            stamp = stampedLock.readLock();
            try {
                currentX = x;
                currentY = y;
            } finally {
                stampedLock.unlockRead(stamp);
            }
        }
        System.out.println("Distance: " + Math.sqrt(currentX * currentX + currentY * currentY));
    }
}
