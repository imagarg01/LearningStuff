package com.ashish.thread;

import java.math.BigInteger;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;



/**
 * Demonstrates various aspects of Virtual Threads in Java, including creation,
 * performance with I/O-bound vs CPU-bound operations, and comparison with platform threads.
 */
public class PlayingWithVT {

  enum ThreadType {
    VirtualThread,
    PlatformThread,
  }

  private static final int THREAD_POOL_SIZE = 12;
  private static final int TASK_LIMIT = 1000;
  private static final int FACTORIAL_INPUT = 100000;
  private static final int SLEEP_DURATION_SECONDS = 12;
  private static final int LARGE_VT_COUNT = 10_000;
  private static final int AWAIT_TIMEOUT_SECONDS = 60;
  private static final int LARGE_VT_SLEEP_SECONDS = 1;

  /**
   * Main method demonstrating CPU-intensive operations with platform threads.
   */
  public static void main(String[] args) throws InterruptedException {
    ExecutorService executorService = Executors.newFixedThreadPool(THREAD_POOL_SIZE);
    observeHowCPUIntensiveOperationWork(ThreadType.PlatformThread, executorService, TASK_LIMIT);

    System.out.println("Hello");
  }



  /**
   * Demonstrates how to create virtual threads using Thread.startVirtualThread().
   */
  static void waysToCreateVT() throws InterruptedException {
    // Via Thread.startVirtualThread
    Thread vt = Thread.startVirtualThread(() -> System.out.println("Hello"));
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
          } catch (InterruptedException e) {
            throw new RuntimeException(e);
          }
          System.out.println("Thread Name: " + Thread.currentThread().toString() + ": is virtual "
              + Thread.currentThread().isVirtual());
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

    long start = System.nanoTime();
    System.out.println("Starting Test at start with ==> " + type.name());
    Duration sleep = Duration.ofSeconds(SLEEP_DURATION_SECONDS);
    for (int i = 0; i < limit; i++) {
      executorService.submit(() -> {
        try {
          Thread.sleep(sleep);
        } catch (InterruptedException e) {
          Thread.currentThread().interrupt();
        }
        System.out.println("Thread Name: " + Thread.currentThread().toString() + ": is virtual "
            + Thread.currentThread().isVirtual());
      });
    }
    executorService.shutdown();
    try {
      if (!executorService.awaitTermination(AWAIT_TIMEOUT_SECONDS, java.util.concurrent.TimeUnit.SECONDS)) {
        executorService.shutdownNow();
      }
    } catch (InterruptedException e) {
      executorService.shutdownNow();
    }
    Duration demoElapsed = Duration.ofNanos(System.nanoTime() - start);
    System.out.println("INFO - test took " + demoElapsed.getSeconds() + " seconds");
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
    long start = System.nanoTime();
    System.out.println("Starting observeHowCPUIntensiveOperationWork Test at start with ==> " + type.name());

    for (int i = 0; i < limit; i++) {
      executorService.submit(() -> {
        // System.out.println("Before Thread Name: " + Thread.currentThread().toString()
        // + ": is virtual " + Thread.currentThread().isVirtual());
        BigInteger result = factorial(FACTORIAL_INPUT);
        // System.out.println("After Thread Name: " + Thread.currentThread().toString()
        // + ": is virtual " + Thread.currentThread().isVirtual());
      });
    }
    executorService.shutdown();
    try {
      if (!executorService.awaitTermination(AWAIT_TIMEOUT_SECONDS, java.util.concurrent.TimeUnit.SECONDS)) {
        executorService.shutdownNow();
      }
    } catch (InterruptedException e) {
      executorService.shutdownNow();
    }
    Duration demoElapsed = Duration.ofNanos(System.nanoTime() - start);
    System.out.println("INFO - observeHowCPUIntensiveOperationWork took " + demoElapsed.getSeconds() + " seconds");
  }

  /**
   * Computes the factorial of a number using BigInteger to handle large values.
   *
   * @param n the number to compute factorial for
   * @return the factorial result as BigInteger
   */
  private static BigInteger factorial(int n) {
    BigInteger result = BigInteger.ONE;
    for (int i = 2; i <= n; i++) {
      result = result.multiply(BigInteger.valueOf(i));
    }
    return result;
  }



}
