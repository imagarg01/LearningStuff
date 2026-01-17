package com.learning.performance.service;

import org.springframework.stereotype.Service;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.regex.Pattern;

@Service
public class PerformanceScenarioService {

    private final ExecutorService executor = Executors.newCachedThreadPool();
    private final AtomicBoolean running = new AtomicBoolean(false);
    private Future<?> currentTask;

    // Regex compiled repeatedly to cause CPU load
    private static final String REGEX = "^([a-z0-9_\\.-]+)@([\\da-z\\.-]+)\\.([a-z\\.]{2,6})$";
    private static final Object LOCK = new Object();

    public synchronized void stopCurrentTask() {
        running.set(false);
        if (currentTask != null) {
            currentTask.cancel(true);
            currentTask = null;
        }
        System.out.println("Stopped current scenario.");
    }

    public synchronized void startCpuTask() {
        stopCurrentTask();
        running.set(true);
        currentTask = executor.submit(() -> loop(this::hotMethod));
        System.out.println("Started CPU Task");
    }

    public synchronized void startAllocTask() {
        stopCurrentTask();
        running.set(true);
        currentTask = executor.submit(() -> loop(this::allocateAndProcess));
        System.out.println("Started Alloc Task");
    }

    public synchronized void startLockTask() {
        stopCurrentTask();
        running.set(true);
        // Spawning multiple threads for lock contention
        currentTask = executor.submit(() -> {
            try (var lockExecutor = Executors.newFixedThreadPool(4)) {
                for (int i = 0; i < 4; i++) {
                    lockExecutor.submit(() -> loop(this::simulateLockContention));
                }
                // Keep the parent task alive until stopped
                while (running.get()) {
                    Thread.sleep(100);
                }
                lockExecutor.shutdownNow();
            } catch (Exception e) {
                // ignore
            }
        });
        System.out.println("Started Lock Task");
    }

    public synchronized void startFileIoTask() {
        stopCurrentTask();
        running.set(true);
        currentTask = executor.submit(() -> loop(this::simulateFileIO));
        System.out.println("Started File I/O Task");
    }

    private void loop(Runnable task) {
        while (running.get() && !Thread.currentThread().isInterrupted()) {
            task.run();
        }
    }

    // --- SCENARIO LOGIC (Copied & Adapted) ---

    private void hotMethod() {
        for (int i = 0; i < 1000; i++) {
            Pattern.matches(REGEX, "user.name@domain.com");
            Math.tan(Math.atan(Math.random())); // Math noise
        }
    }

    private void allocateAndProcess() {
        String[] array = new String[1000];
        for (int i = 0; i < array.length; i++) {
            array[i] = new String("Allocated String " + i + System.nanoTime());
        }
    }

    private void simulateLockContention() {
        synchronized (LOCK) {
            try {
                // Hold lock for a bit
                Thread.sleep(10);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    private void simulateFileIO() {
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
}
