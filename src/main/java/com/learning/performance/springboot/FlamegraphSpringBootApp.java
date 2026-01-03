package com.learning.performance.springboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.EnableAspectJAutoProxy;

@SpringBootApplication
@EnableAspectJAutoProxy // Enables AOP for our "Proxy Forest"
public class FlamegraphSpringBootApp {

    public static void main(String[] args) {
        System.out.println("Starting Flamegraph Spring Boot App...");
        System.out.println("PID: " + ProcessHandle.current().pid());
        SpringApplication.run(FlamegraphSpringBootApp.class, args);
    }
}
