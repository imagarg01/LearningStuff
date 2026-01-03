package com.learning.performance.springboot;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.regex.Pattern;

@RestController
@RequestMapping("/heavy")
public class ScenarioController {

    private final ProxyService proxyService;

    public ScenarioController(ProxyService proxyService) {
        this.proxyService = proxyService;
    }

    // SCENARIO 1: CPU HOG (The Jackson Tower / Regex)
    @GetMapping("/cpu")
    public String cpu() {
        for (int i = 0; i < 5000; i++) {
            Pattern.matches("^([a-z0-9_\\.-]+)@([\\da-z\\.-]+)\\.([a-z\\.]{2,6})$", "user.name@domain.com");
            Math.tan(Math.atan(Math.random()));
        }
        return "CPU Burned!";
    }

    // SCENARIO 2: ALLOCATION (The Logging Plateau)
    @GetMapping("/alloc")
    public String alloc() {
        String[] array = new String[5000];
        for (int i = 0; i < array.length; i++) {
            array[i] = new String("Allocated String " + i + System.nanoTime());
        }
        return "Memory Allocated!";
    }

    // SCENARIO 3: DB WAIT (Connection Pool Wait)
    @GetMapping("/db")
    public String db() throws InterruptedException {
        // Simulate waiting for a DB connection or slow query
        Thread.sleep(200);
        return "DB Query Finished (simulated)";
    }

    // SCENARIO 4: PROXY FOREST (Spring AOP)
    @GetMapping("/proxy")
    public String proxy() {
        return proxyService.heavyProxyCall();
    }
}
