package com.ashish.thread;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadLocalRandom;

/**
 * COMPREHENSIVE GUIDE TO COMPLETABLE FUTURE
 * <p>
 * Demonstrates:
 * 1. Chaining (Pipelines)
 * 2. Combining (A + B)
 * 3. Fast-Fail (AnyOf)
 * 4. Waiting for All (AllOf)
 * 5. Error Handling
 * </p>
 *
 * <pre>
 * <b>VISUALIZATION: The Async Pipeline</b>
 *
 *     (Start)           (Callback 1)          (Callback 2)
 *    supplyAsync  --->   thenApply    --->    thenAccept
 *  +-------------+    +-------------+       +-------------+
 *  | Fetch User  |    |  Get Email  |       |  Send Mail  |
 *  +------+------+    +------+------+       +------+------+
 *         |                  |                     |
 *         v                  v                     v
 *    [Thread-1]         [Thread-2]            [Thread-2]
 *                       (Async switch)
 * </pre>
 */
public class CompletableFutureDemo {

    public static void main(String[] args) {
        var exec = Executors.newFixedThreadPool(4);

        System.out.println("=== 1. CHAINING (Sync vs Async) ===");
        CompletableFuture.supplyAsync(() -> "Order-123", exec)
                .thenApplyAsync(order -> {
                    System.out.println("Enriching " + order + " on " + Thread.currentThread().getName());
                    return order + "-Enriched";
                }, exec)
                .thenAccept(finalOrder -> System.out.println("Saved " + finalOrder))
                .join();

        System.out.println("\n=== 2. COMBINING (Dependent Tasks) ===");
        // Task A: Fetch User
        CompletableFuture<String> userFuture = CompletableFuture.supplyAsync(() -> {
            sleep(500);
            return "Ashish";
        });

        // Task B: Fetch Preferences (Wait for A!)
        // thenCompose = "flatMap" (Returns a new Future)
        userFuture.thenCompose(user -> CompletableFuture.supplyAsync(() -> user + "'s Prefs"))
                .thenAccept(System.out::println)
                .join();

        System.out.println("\n=== 3. COMBINING (Independent Tasks) ===");
        // Task X: Get Price Amazon
        var priceA = CompletableFuture.supplyAsync(() -> 100);
        // Task Y: Get Price eBay
        var priceB = CompletableFuture.supplyAsync(() -> 95);

        // thenCombine = Run parallel, then join results
        priceA.thenCombine(priceB, (p1, p2) -> Math.min(p1, p2))
                .thenAccept(cheapest -> System.out.println("Cheapest: $" + cheapest))
                .join();

        System.out.println("\n=== 4. OR (The Fastest Wins) ===");
        var server1 = CompletableFuture.supplyAsync(() -> {
            sleep(2000);
            return "Server1";
        });
        var server2 = CompletableFuture.supplyAsync(() -> {
            sleep(500);
            return "Server2";
        }); // Faster

        CompletableFuture.anyOf(server1, server2)
                .thenAccept(winner -> System.out.println("Winner: " + winner))
                .join();

        System.out.println("\n=== 5. EXCEPTION HANDLING ===");
        CompletableFuture.supplyAsync(() -> {
            if (ThreadLocalRandom.current().nextBoolean())
                throw new RuntimeException("Boom!");
            return "Success";
        }).handle((res, ex) -> {
            if (ex != null)
                return "Recovered from: " + ex.getMessage();
            return res;
        }).thenAccept(System.out::println).join();

        exec.shutdown();
    }

    private static void sleep(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
        }
    }
}
