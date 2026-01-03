package com.learning.performance;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadLocalRandom;
import java.util.regex.Pattern;

/**
 * START HERE: Flamegraph Demonstration Application
 * 
 * This application is designed to simulate various common performance
 * anti-patterns
 * to help you learn how to read Flamegraphs.
 * 
 * Usage: java com.learning.performance.FlamegraphExample <scenario>
 * 
 * Scenarios:
 * cpu - High CPU usage (Regex usage)
 * alloc - High Memory Allocation (GC pressure)
 * stack - Deep Stack Traces (Recursion)
 * locks - Lock Contention (Threads fighting for locks)
 * file-io - File I/O Blocking (Off-CPU)
 * vt-ops - Virtual Threads (Efficient Blocking)
 * pt-scale - Platform Thread Scalability LIMIT (Inefficient)
 */
public class FlamegraphExample {

    // Regex compiled repeatedly to cause CPU load
    private static final String REGEX = "^([a-z0-9_\\.-]+)@([\\da-z\\.-]+)\\.([a-z\\.]{2,6})$";

    public static void main(String[] args) {
        String mode = args.length > 0 ? args[0] : "all";
        System.out.println("Starting FlamegraphExample in mode: " + mode);
        System.out.println("PID: " + ProcessHandle.current().pid());

        switch (mode.toLowerCase()) {
            case "cpu" -> runCpuTask();
            case "alloc" -> runAllocTask();
            case "stack" -> runStackTask();
            case "locks" -> runLockContentionTask();
            case "file-io" -> runFileIOTask();
            case "vt-ops" -> runVirtualThreadTask();
            case "pt-scale" -> runPlatformThreadScalabilityTask();
            case "all" -> runAllTasks(); // Chaos mode
            default -> {
                System.out.println("Unknown mode: " + mode);
                System.out.println("Available: cpu, alloc, stack, locks, file-io, vt-ops, pt-scale");
            }
        }
    }

    private static void runAllTasks() {
        try (var executor = Executors.newFixedThreadPool(6)) {
            executor.submit(() -> loop(FlamegraphExample::hotMethod));
            executor.submit(() -> loop(FlamegraphExample::allocateAndProcess));
            executor.submit(() -> loop(() -> recursiveMethod(0)));
            executor.submit(() -> loop(FlamegraphExample::simulateLockContention));
            executor.submit(() -> loop(FlamegraphExample::simulateFileIO));
        }
    }

    private static void loop(Runnable task) {
        while (true) {
            task.run();
        }
    }

    // ==========================================
    // SCENARIO 1: HIGH CPU (Regex)
    // ==========================================
    private static void runCpuTask() {
        System.out.println("Running CPU Task: Watch for wide towers in flamegraph.");
        loop(FlamegraphExample::hotMethod);
    }

    private static void hotMethod() {
        for (int i = 0; i < 1000; i++) {
            Pattern.matches(REGEX, "user.name@domain.com");
            Math.tan(Math.atan(Math.random())); // Math noise
        }
    }

    // ==========================================
    // SCENARIO 2: HIGH ALLOCATION (GC / Memory)
    // ==========================================
    private static void runAllocTask() {
        System.out.println("Running Alloc Task: Watch for GC threads and 'new' calls.");
        loop(FlamegraphExample::allocateAndProcess);
    }

    private static void allocateAndProcess() {
        String[] array = new String[1000];
        for (int i = 0; i < array.length; i++) {
            array[i] = new String("Allocated String " + i + System.nanoTime());
        }
    }

    // ==========================================
    // SCENARIO 3: DEEP STACKS (Recursion)
    // ==========================================
    private static void runStackTask() {
        System.out.println("Running Stack Task: Watch for tall towers.");
        loop(() -> recursiveMethod(0));
    }

    private static void recursiveMethod(int depth) {
        if (depth < 100) {
            recursiveMethod(depth + 1);
        } else {
            Math.random(); // Do something at bottom
        }
    }

    // ==========================================
    // SCENARIO 4: LOCK CONTENTION
    // ==========================================
    private static final Object LOCK = new Object();

    private static void runLockContentionTask() {
        System.out.println("Running Lock Contention: Use '-e lock' to see monitors.");
        // Spawn multiple threads fighting for one lock
        try (var executor = Executors.newFixedThreadPool(4)) {
            for (int i = 0; i < 4; i++) {
                executor.submit(() -> loop(FlamegraphExample::simulateLockContention));
            }
        }
    }

    private static void simulateLockContention() {
        synchronized (LOCK) {
            try {
                // Hold lock for a bit
                Thread.sleep(10);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    // ==========================================
    // SCENARIO 5: FILE I/O (Off-CPU)
    // ==========================================
    private static void runFileIOTask() {
        System.out.println("Running File I/O: Use '-e wall' to see blocking I/O.");
        loop(FlamegraphExample::simulateFileIO);
    }

    private static void simulateFileIO() {
        Path tmpFile = Path.of("temp-io-test.txt");
        try {
            String data = "Some data " + System.nanoTime() + "\n";
            Files.writeString(tmpFile, data, StandardOpenOption.CREATE, StandardOpenOption.APPEND);
            Files.readString(tmpFile);
            if (Files.size(tmpFile) > 100000) {
                Files.delete(tmpFile);
            }
        } catch (IOException e) {
            // ignore
        }
    }

    // ==========================================
    // SCENARIO 6: VIRTUAL THREADS (Efficient)
    // ==========================================
    private static void runVirtualThreadTask() {
        System.out.println("Running Virtual Threads: Spawning 100,000 threads.");
        System.out.println("Use '-e wall' to see them sleeping.");

        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 100_000; i++) {
                executor.submit(() -> {
                    try {
                        Thread.sleep(Duration.ofSeconds(10));
                    } catch (InterruptedException e) {
                        // ignore
                    }
                });
            }
        } // Close block waits for all to finish
        System.out.println("All 100,000 Virtual Threads completed.");
    }

    // ==========================================
    // SCENARIO 7: PLATFORM THREADS (Scalability Limit)
    // ==========================================
    private static void runPlatformThreadScalabilityTask() {
        System.out.println("Running Platform Threads: Spawning up to 5,000 threads.");
        // WARNING: This might crash or freeze your system if too high
        List<Thread> threads = new ArrayList<>();
        for (int i = 0; i < 5000; i++) {
            Thread t = new Thread(() -> {
                try {
                    Thread.sleep(Duration.ofSeconds(10));
                } catch (InterruptedException e) {
                    // ignore
                }
            });
            t.start();
            threads.add(t);
            if (i % 500 == 0)
                System.out.println("Spawned " + i + " platform threads...");
        }

        for (Thread t : threads) {
            try {
                t.join();
            } catch (InterruptedException e) {
                // ignore
            }
        }
        System.out.println("All Platform Threads completed.");
    }
}
