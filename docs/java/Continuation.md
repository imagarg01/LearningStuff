# Continuation in Java

> [!NOTE]
> **Internal API Warning**: `Continuation` is currently an internal API (`jdk.internal.vm.Continuation`) residing in the `java.base` module. It is **not exported** for public use and is intended primarily for JDK developers to implement constructs like Virtual Threads.

## Overview

A **Continuation** is a low-level primitive that represents a sequence of instructions that can be suspended and resumed. It is the fundamental mechanism that powers **Virtual Threads** (Project Loom).

Think of a Continuation as a "pausable runnable". Unlike a regular thread, which runs from start to finish (blocking the OS thread if it waits), a continuation can:

1. **Yield** (suspend) its execution at any point, saving its stack frame to memory (heap).
2. **Resume** execution later from exactly where it left off, restoring its stack frame.

## The Role in Virtual Threads

Virtual Threads are essentially **Continuations** scheduled by a `ForkJoinPool`.

When a Virtual Thread performs a blocking operation (like I/O or `Thread.sleep`):

1. The Virtual Thread calls `Continuation.yield()`.
2. The JVM copies the execution stack from the platform thread to the heap.
3. The underlying platform thread (carrier) is released to do other work.
4. When the operation completes, the scheduler calls `Continuation.run()`.
5. The JVM copies the stack back from the heap to a platform thread, and execution resumes.

This "mount/unmount" mechanism allows a few platform threads to handle millions of virtual threads.

## How it works (Conceptually)

The API revolves around the `Continuation` class and `ContinuationScope`.

```java
/*
 * CONCEPTUAL EXAMPLE (Internal API)
 * This code usually requires --add-exports java.base/jdk.internal.vm=ALL-UNNAMED
 */

import jdk.internal.vm.Continuation;
import jdk.internal.vm.ContinuationScope;

public class ContinuationDemo {
    public static void main(String[] args) {
        var scope = new ContinuationScope("demo");
        
        var continuation = new Continuation(scope, () -> {
            System.out.println("Start Phase 1");
            
            // Suspend execution here
            Continuation.yield(scope);
            
            System.out.println("Resume Phase 2");
        });

        System.out.println("Main: Starting continuation");
        continuation.run(); // Runs until yield()
        
        System.out.println("Main: Back in main after yield");
        
        continuation.run(); // Resumes after yield()
        System.out.println("Main: Finished");
    }
}
```

### Output

```text
Main: Starting continuation
Start Phase 1
Main: Back in main after yield
Resume Phase 2
Main: Finished
```

## Key Concepts

### 1. Stack Management

When a continuation yields:

- The JVM detects the boundary of the continuation.
- It copies the stack frames belonging to that continuation from the native thread stack to a `stack chunk` object on the Java heap.
- This is why Virtual Threads have a flexible stack size, unlike Platform Threads which have fixed 1MB (default) stacks.

### 2. Delimited Continuations (Scopes)

Java implements **Delimited Continuations**. This means a continuation has a start and an end, and it is "delimited" by a `ContinuationScope`.

- `yield(scope)` allows nested continuations to yield to a specific parent scope, ensuring control flows back to the correct handler.

### 3. Imperative Style

Continuations allow developers (and the JDK) to write imperative, sequential code that *looks* synchronous but behaves asynchronously. You don't need callbacks or `Future` chaining; the runtime handles the suspension.

## Why is it internal?

The Java team decided to keep `Continuation` internal to avoid locking in an API that might evolve. Currently, it is a building block for higher-level APIs like `java.lang.VirtualThread` and the upcoming **Structured Concurrency**. For 99% of Java developers, Virtual Threads are the correct API to use.

---

## Related Documentation

- **[VirtualThread.md](./VirtualThread.md)**: The user-facing API powered by continuations.
- **[StructuredConcurrency.md](./StructuredConcurrency.md)**: An endpoint for managing concurrent virtual threads.
