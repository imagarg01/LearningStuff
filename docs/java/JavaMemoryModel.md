# Java Memory Model (JMM)

The JMM defines how Java threads interact through memory (RAM). It solves two main problems:

1. **Visibility**: When does a write by Thread A become visible to Thread B?
2. **Ordering**: When is the compiler/CPU allowed to reorder instructions?

## 1. The Three Concepts

### A. Atomicity

An operation is atomic if it completes in a single step relative to other threads.

- `int i = 5;` (Atomic)
- `i++` (**NOT** Atomic: Read -> Modify -> Write)
- `long` and `double` writes are NOT guaranteed to be atomic on 32-bit systems (unless `volatile`).

### B. Visibility

CPU caches cause visibility issues. Thread A might write to its local cache, and Thread B checks main memory (seeing the old value).

**Solution**: `volatile` or `synchronized`.

### C. Ordering

Compilers and CPUs optimize code by reordering instructions that don't depend on each other. This is fine for single threads but breaks multithreading.

## 2. Happens-Before Relationship

This is the central guarantee of the JMM. If Action A *happens-before* Action B, then all changes made by A are visible to B.

**Key Happens-Before Rules:**

1. **Program Order**: Each action in a single thread happens-before every action later in that thread.
2. **Monitor Lock**: An unlock on a monitor happens-before every subsequent lock on that *same* monitor.
3. **Volatile Variable**: A write to a `volatile` field happens-before every subsequent read of that *same* field.
4. **Thread Start**: A call to `thread.start()` happens-before any action in the started thread.
5. **Thread Join**: All actions in a thread happen-before any other thread successfully returns from `thread.join()`.

## 3. The `final` Keyword Semantics

The JMM provides special guarantees for `final` fields.

- Once a constructor completes, the values assigned to `final` fields are guaranteed to be visible to other threads, even without synchronization.
- **Condition**: While constructing, you must not let the `this` reference escape (don't pass `this` to another thread inside the constructor).

## 4. Double-Checked Locking (The Right Way)

```java
// Singleton Pattern
class Singleton {
    // MUST be volatile to prevent reordering
    private static volatile Singleton instance;

    public static Singleton getInstance() {
        if (instance == null) {                 // 1. Check
            synchronized (Singleton.class) {
                if (instance == null) {         // 2. Check again
                    instance = new Singleton(); // 3. Create
                }
            }
        }
        return instance;
    }
}
```

Without `volatile`, the specialized Instruction Reordering could allow `instance` to point to a half-initialized object!
