# Measuring Concurrency Performance

Concurrency is meant to make things faster, but incorrect usage can make them slower (due to context switching, cache contention, or locking).

**Rule #1**: Never guess. Always measure.

## 1. Micro-benchmarking with JMH

Writing a loop `start = System.nanoTime()` is usually wrong for micro-benchmarks (JVM Warmup, JIT compilation, Dead Code Elimination).

Use **JMH (Java Microbenchmark Harness)**, the official standard.

```java
@State(Scope.Thread)
@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.SECONDS)
public class MyBenchmark {

    @Benchmark
    public void testMethod() {
        // ... code to test ...
    }
}
```

- **Modes**:
  - `Throughput`: Ops/sec.
  - `AverageTime`: Latency per op.

## 2. Profiling with JFR (Java Flight Recorder)

JFR is a low-overhead profiling engine built into the JVM. It is the best way to see **why** threads are blocking.

### How to use

1. Start app with `-XX:StartFlightRecording` or use `jcmd`.
2. Open `.jfr` file in **JDK Mission Control (JMC)**.
3. Look at the "Threads" view.
    - **Green**: Running.
    - **Red/Brown**: Blocked on Lock? Waiting on I/O?

**Key Event**: `jdk.VirtualThreadPinned` (Crucial for Virtual Threads).

## 3. Key Metrics

- **Latency**: Time for one request. (Lower is better).
- **Throughput**: Requests per second. (Higher is better).

**Concurrency usually improves Throughput, but may degrade individual Latency** (due to queuing).

## 4. Common Performance Pitfalls

1. **Context Switching**: Too many platform threads (> CPU Cores) causes the OS to waste time switching threads instead of working.
    - *Fix*: Use Virtual Threads or Fixed Thread Pool size.
2. **False Sharing**: Multiple threads updating variables that sit on the same "Cache Line" (64 bytes).
    - *Fix*: Use `@Contended` (internal) or padding.
3. **Lock Contention**: Threads spending time waiting for locks.
    - *Fix*: Reduce critical section size, use ReadWriteLock, or Stripe locks (ConcurrentHashMap).
