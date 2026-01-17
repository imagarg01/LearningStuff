package com.learning.performance.controller;

import com.learning.performance.service.PerformanceScenarioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/scenarios")
public class PerformanceController {

    @Autowired
    private PerformanceScenarioService scenarioService;

    @PostMapping("/stop")
    public String stop() {
        scenarioService.stopCurrentTask();
        return "Stopped all scenarios";
    }

    @PostMapping("/cpu/start")
    public String startCpu() {
        scenarioService.startCpuTask();
        return "Started CPU Scenario";
    }

    @PostMapping("/alloc/start")
    public String startAlloc() {
        scenarioService.startAllocTask();
        return "Started Allocation Scenario";
    }

    @PostMapping("/locks/start")
    public String startLocks() {
        scenarioService.startLockTask();
        return "Started Lock Contention Scenario";
    }

    @PostMapping("/io/start")
    public String startIo() {
        scenarioService.startFileIoTask();
        return "Started File I/O Scenario";
    }
}
