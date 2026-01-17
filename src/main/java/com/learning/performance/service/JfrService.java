package com.learning.performance.service;

import jdk.jfr.Recording;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Service
public class JfrService {

    private Recording recording;
    private static final DateTimeFormatter FILE_DATE_FMT = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss");

    public synchronized void startRecording() {
        if (recording != null) {
            stopRecording();
        }
        recording = new Recording();
        recording.setName("Manual-Web-Recording");
        recording.enable("jdk.CPULoad").withPeriod(java.time.Duration.ofMillis(100));
        recording.enable("jdk.JavaMonitorEnter").withThreshold(java.time.Duration.ofMillis(10));
        recording.start();
        System.out.println("JFR Recording started.");
    }

    public synchronized Path stopRecording() {
        if (recording == null) {
            throw new IllegalStateException("No recording running");
        }
        recording.stop();

        String filename = "recording_" + LocalDateTime.now().format(FILE_DATE_FMT) + ".jfr";
        Path path = Path.of(filename).toAbsolutePath();
        try {
            recording.dump(path);
            System.out.println("JFR Recording dumped to " + path);
        } catch (IOException e) {
            throw new RuntimeException("Failed to dump JFR", e);
        } finally {
            recording.close();
            recording = null;
        }
        return path;
    }
}
