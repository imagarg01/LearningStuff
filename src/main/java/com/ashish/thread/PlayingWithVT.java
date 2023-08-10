package com.ashish.thread;

import java.math.BigInteger;
import java.time.Duration;
import java.time.Instant;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

public class PlayingWithVT {

    enum ThreadType {
        VirtualThread,
        PlatformThread,
    }

    public static void main(String[] args) throws InterruptedException {
        //createLargeNumberOfVT();
//        waysToCreateVT();
//        observeHowSleepBehave(ThreadType.VirtualThread, executorService,1000000);
//
        ExecutorService executorService = Executors.newFixedThreadPool(12);
       // ExecutorService executorService = Executors.newVirtualThreadPerTaskExecutor();
        observerHowCPUIntensiveOperationWork(ThreadType.PlatformThread,executorService,1000);

    }

    static void waysToCreateVT() throws InterruptedException {

        //Via Thread.Builder interface
//        Thread.Builder builder = Thread.ofVirtual().name("MyThread");
//        Runnable task = () -> {
//            System.out.println("Running thread");
//        };
//        Thread t = builder.start(task);
//        System.out.println("Thread t name: " + t.getName());
//        t.join();

        //Via Thread.ofVirtual
//        Thread thread = Thread.ofVirtual().start(() -> System.out.println("Hello"));
//        thread.join();

        //Via Executors
//        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
//            IntStream.range(0, 10).forEach(i -> {
//                executor.submit(() -> {
//                    System.out.println("Thread Name: " + Thread.currentThread().toString());
//                });
//            });
//        }


        //Via Thread.startVirtualThread
        Thread vt =Thread.startVirtualThread(() -> System.out.println("Hello"));
        vt.join();
    }

    static void createLargeNumberOfVT() {

        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            IntStream.range(0, 10_000).forEach(i -> {
                executor.submit(() -> {
                    try {
                        Thread.sleep(Duration.ofSeconds(1));
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                    System.out.println("Thread Name: " + Thread.currentThread().toString() + ": is virtual " + Thread.currentThread().isVirtual());
                });
            });
        }
    }


    static void observeHowSleepBehave(ThreadType type, ExecutorService executorService, int limit){

        long start = System.nanoTime();
        System.out.println("Starting Test at start with ==> "+ type.name());
        try (executorService) {
            Duration sleep = Duration.ofSeconds( 12 );
            for ( int i = 0 ; i < limit ; i++ ) {
                executorService.submit(new Runnable() {
                            @Override
                            public void run ( )
                            {
                                try {Thread.sleep( sleep );} catch ( InterruptedException e ) {e.printStackTrace();}
                                System.out.println("Thread Name: " + Thread.currentThread().toString() + ": is virtual " + Thread.currentThread().isVirtual());
                            }});
            }
        }
        Duration demoElapsed = Duration.ofNanos(System.nanoTime() - start );
        System.out.println( "INFO - test took " + demoElapsed.getSeconds() + " seconds" );
    }

    static void observerHowCPUIntensiveOperationWork(ThreadType type, ExecutorService executorService, int limit) {
        long start = System.nanoTime();
        System.out.println("Starting observerHowCPUIntensiveOperationWork Test at start with ==> "+ type.name());

        try (executorService) {
            for ( int i = 0 ; i < limit ; i++ ) {
                executorService.submit(new Runnable() {
                    @Override
                    public void run ( ) {
                       // System.out.println("Before Thread Name: " + Thread.currentThread().toString() + ": is virtual " + Thread.currentThread().isVirtual());
                        BigInteger result = factorial(100000);
                       // System.out.println("After Thread Name: " + Thread.currentThread().toString() + ": is virtual " + Thread.currentThread().isVirtual());
                    }});
            }
        }
        Duration demoElapsed = Duration.ofNanos(System.nanoTime() - start );
        System.out.println( "INFO - observerHowCPUIntensiveOperationWork took " + demoElapsed.getSeconds() + " seconds" );
    }

    private static BigInteger factorial(int n) {
        BigInteger result = BigInteger.ONE;
        for (int i = 2; i <= n; i++) {
            result = result.multiply(BigInteger.valueOf(i));
        }
        return result;
    }

}
