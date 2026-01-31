# Concurrent Collections

Standard collections (`HashMap`, `ArrayList`) are **not** thread-safe. Using them in concurrent environments leads to race conditions or `ConcurrentModificationException`.

> **Run Code Example**: [`ConcurrentCollectionsDemo.java`](../../src/main/java/com/ashish/thread/ConcurrentCollectionsDemo.java)

Using `Collections.synchronizedMap()` is a blunt instrument—it locks the *entire* map for every read/write, killing performance.

## 1. ConcurrentHashMap

This is the gold standard for concurrent maps.

- **Non-blocking Reads**: Reads (`get`) never lock. They are extremely fast.
- **Micro-lock Writes**: Writes (`put`) lock only the specific "bucket" (node) where the collision happens, not the whole map.

```mermaid
graph TD
    subgraph "ConcurrentHashMap Structure"
        B1[Bucket 1]
        B2[Bucket 2: Locked by T1]
        B3[Bucket 3]
        B4[Bucket 4]
    end
    
    T1[Thread 1: put K1, V1] -->|Locks| B2
    T2[Thread 2: get K2] -->|Reads| B2
    T3[Thread 3: put K3, V3] -->|Locks| B4
    
    style B2 fill:#f99,stroke:#333
    style T2 stroke-dasharray: 5 5
```

### Key Methods

- `putIfAbsent(key, value)`: Atomic check-and-set.
- `compute(key, remappingFunction)`: Atomically compute a new value.

### When to use

Always, if you need a shared map in a multithreaded environment.

## 2. CopyOnWriteArrayList

A thread-safe variant of `ArrayList`.

- **Mechanism**: Every time you modify it (`add`, `set`, `remove`), it makes a fresh copy of the *entire* underlying array.
- **Reads**: Extremely fast. They read from the current "snapshot" array without locks.
- **Writes**: Expensive.

### Usage

- **Read-Heavy / Write-Rarely**: Event Listener lists, Configuration lists.
- **Avoid** if you write frequently (the copying cost is O(N)).

## 3. ConcurrentSkipListMap

A thread-safe sorted map (like `TreeMap`).

- Uses a **Skip List** algorithm (probabilistic data structure).
- Provides `O(log n)` time cost for most operations.
- Lock-free implementation (uses CAS).

## Summary Table

| Interface | Single Threaded | Thread Safe (Blocking) | Thread Safe (Concurrent/Fast) |
| :--- | :--- | :--- | :--- |
| **List** | `ArrayList` | `Collections.synchronizedList` | `CopyOnWriteArrayList` |
| **Map** | `HashMap` | `Collections.synchronizedMap` | `ConcurrentHashMap` |
| **SortedMap** | `TreeMap` | `Collections.synchronizedSortedMap` | `ConcurrentSkipListMap` |
