package com.ashish.observability.controller;

import com.ashish.observability.service.OrderService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    /**
     * Zero-Code Endpoint
     * Try: curl -X POST http://localhost:8080/api/orders/auto?item=Laptop
     */
    @PostMapping("/auto")
    public ResponseEntity<Map<String, String>> createAutoOrder(@RequestParam(defaultValue = "Laptop") String item) {
        String result = orderService.processAutoOrder(item);
        return ResponseEntity.ok(Map.of("status", "success", "message", result, "type", "auto"));
    }

    /**
     * Manual Instrumentation Endpoint
     * Try: curl -X POST http://localhost:8080/api/orders/manual?item=Phone&qty=2
     * Chaos Try: curl -X POST "http://localhost:8080/api/orders/manual?item=error"
     */
    @PostMapping("/manual")
    public ResponseEntity<Map<String, String>> createManualOrder(
            @RequestParam(defaultValue = "Phone") String item,
            @RequestParam(defaultValue = "1") int qty) {

        try {
            String result = orderService.processManualOrder(item, qty);
            return ResponseEntity.ok(Map.of("status", "success", "message", result, "type", "manual"));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("status", "error", "message", e.getMessage()));
        }
    }
}
