package com.learning.performance.springboot;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Service;
import org.springframework.stereotype.Component;

@Service
public class ProxyService {

    // Simulates a business method wrapped in AOP
    public String heavyProxyCall() {
        return "Processed by Proxy Forest";
    }
}

@Aspect
@Component
class ForestAspect {

    // Apply multiple layers of AOP to simulate deep stacks
    // In real life, this comes from Transactional, Security, Caching, etc.

    @Around("execution(* com.learning.performance.springboot.ProxyService.*(..))")
    public Object layer1(ProceedingJoinPoint joinPoint) throws Throwable {
        return joinPoint.proceed();
    }

    @Around("execution(* com.learning.performance.springboot.ProxyService.*(..))")
    public Object layer2(ProceedingJoinPoint joinPoint) throws Throwable {
        return joinPoint.proceed();
    }

    @Around("execution(* com.learning.performance.springboot.ProxyService.*(..))")
    public Object layer3(ProceedingJoinPoint joinPoint) throws Throwable {
        return joinPoint.proceed();
    }

    @Around("execution(* com.learning.performance.springboot.ProxyService.*(..))")
    public Object layer4(ProceedingJoinPoint joinPoint) throws Throwable {
        return joinPoint.proceed();
    }

    @Around("execution(* com.learning.performance.springboot.ProxyService.*(..))")
    public Object layer5(ProceedingJoinPoint joinPoint) throws Throwable {
        return joinPoint.proceed();
    }
}
