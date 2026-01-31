package com.ashish.thread;

import java.util.stream.LongStream;

/**
 * Demonstrates Parallel Streams and ForkJoinPool.
 */
public class ParallelStreamDemo {

    public static void main(String[] args) {
        long n = 10_000_000;

        // SEQUENTIAL
        long start = System.currentTimeMillis();
        long sumSeq = LongStream.rangeClosed(1, n)
                .map(ParallelStreamDemo::heavyCalc)
                .sum();
        long end = System.currentTimeMillis();
        System.out.println("Sequential Time: " + (end - start) + "ms");

        // PARALLEL
        start = System.currentTimeMillis();
        long sumPar = LongStream.rangeClosed(1, n)
                .parallel() // <--- The Magic
                .map(ParallelStreamDemo::heavyCalc)
                .sum();
        end = System.currentTimeMillis();
        System.out.println("Parallel Time:   " + (end - start) + "ms");
    }

    private static long heavyCalc(long i) {
        // Keep CPU busy with math
        return (long) Math.sqrt(i * i + 100);
    }
}
