# Java Multithreading & Concurrency: Mastery Path

To master Java Concurrency, a developer must traverse from the low-level foundations to high-level modern patterns.

## 1. Fundamentals (The "Old World")

Understanding threads is prerequisite to using thread pools.

- [x] **Threads & Lifecycle**: Rules of the generic OS thread. ([Thread.md](./Thread.md))
- [x] **Synchronization**: Locks, Monitors, and Critical Sections. ([Synchronization.md](./Synchronization.md))
- [ ] **Java Memory Model (JMM)**: Visibility, Reordering, and "Happens-Before". **(GAP)**

## 2. Classic abstraction (Java 5)

Moving from manual thread creation to management.

- [x] **Executor Service**: Thread Pools and Lifecycle. ([ExecutorService.md](./ExecutorService.md))
- [x] **Future**: The placeholder for async results. ([Future.md](./Future.md))
- [x] **Coordination**: Semaphores, Latches, Barriers. ([Synchronization.md](./Synchronization.md))
- [x] **Blocking Queues**: Producer-Consumer fundamentals. ([BlockingQueue.md](./BlockingQueue.md))
- [ ] **Concurrent Collections**: `ConcurrentHashMap`, `CopyOnWriteArrayList`. **(GAP)**

## 3. Asynchronous & Parallel (Java 8)

Non-blocking and data-parallel approaches.

- [x] **CompletableFuture**: Async pipelines and chaining. ([CompletableFuture.md](./CompletableFuture.md))
- [x] **Parallel Streams**: Data parallelism via Fork/Join. ([ParallelStream.md](./ParallelStream.md))

## 4. Modern Concurrency (Java 21+)

The revolution of lightweight threads.

- [x] **Virtual Threads**: Million-scale concurrency. ([VirtualThread.md](./VirtualThread.md))
- [x] **Structured Concurrency**: Treating related tasks as a single unit. ([StructuredConcurrency.md](./StructuredConcurrency.md))
- [x] **Scoped Values**: Thread-local data for virtual threads. (In [StructuredConcurrency.md](./StructuredConcurrency.md))

## 5. Advanced Concepts

- [x] **Performance Measurement**: JMH & JFR. ([ConcurrencyPerformance.md](./ConcurrencyPerformance.md))
- [ ] **Advanced Locking**: StampedLock (Optimistic Locking). **(GAP)**
