# Concurrency Decision Guide: Which tool to use?

Java provides many tools for concurrency. Choosing the wrong one can lead to poor performance or complex code.

## 1. Quick Decision Matrix

| Scenario | Recommended Tool | Why? |
| :--- | :--- | :--- |
| **High Concurrency I/O** (Rest APIs, DB calls) | **Virtual Threads** | Cheap blocking. Can handle millions of connections. |
| **Data Processing** (Large Lists, CPU heavy) | **ParallelStream** | simple `parallel()` call. Optimized for multi-core data crunching. |
| **Async Pipelines** (Chaining A -> B -> C) | **CompletableFuture** | Non-blocking chaining. Powerful error handling. |
| **Complex Subtask Groups** (Task A + Task B) | **Structured Concurrency** | Automatic cancellation, error propagation (See [StructuredConcurrency.md](./StructuredConcurrency.md)). |
| **Low-level coordination** (Building a cache) | **Locks / Semaphores** | precise control over shared state. |

## 2. Detailed Scenarios

### Scenario A: "I need to process 100,000 items in a list"

**Answer**: `ParallelStream`

- **Why**: The ForkJoinPool is designed to split data chunks and utilize all CPU cores.
- **Caveat**: Ensure the operation is CPU intensive. If it does DB calls, you will block the common pool.

### Scenario B: "I need to fetch data from 3 different APIs and combine them"

**Answer**: `Structured Concurrency` (or `CompletableFuture`)

- **Modern Way (Java 21+)**: Use `StructuredTaskScope`. It's cleaner and safer.
- **Classic Way (Java 8+)**: Use `CompletableFuture.allOf()`.

### Scenario C: "I need to limit access to a legacy rate-limited API"

**Answer**: `Semaphore` + `Virtual Threads`

- Use a Semaphore to limit the *concurrency* (e.g., 50 permits).
- Use Virtual Threads to handle the waiting (cheap blocking).

## 3. Trade-offs

| Tool | Pros | Cons |
| :--- | :--- | :--- |
| **Threads (Platform)** | Supported everywhere. | Expensive (1MB stack). Limited scale. |
| **Virtual Threads** | Massive scale. Standard blocking code style. | Pinning issues (native code). Not for CPU tasks. |
| **CompletableFuture** | Non-blocking. | "Callback Hell" if overused. Hard to debug. |
| **Parallel Stream** | One-line implementation. | Hard to control pool size. Hard to debug. |
| **[Future](./Future.md)** | Simple async handle. | Blocking `get()`. No callbacks. |
| **[BlockingQueue](./BlockingQueue.md)** | Thread-safe data transfer. | Blocking. Overhead if used for simple passing. |
