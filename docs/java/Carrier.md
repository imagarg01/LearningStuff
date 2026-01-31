# Carrier Classes & Data Carriers

> **Note**: As of **JDK 24**, "Carrier Class" is **not** a language keyword or a specific Java feature you can use like `record` or `class`.
>
> It is a **concept** from the "Data-Oriented Programming" (DOP) roadmap and Project Amber discussions. It refers to a future evolution where normal classes could be treated as "Data Carriers" similar to records but with more flexibility.

However, the term "Carrier" appears in two distinct contexts in modern Java:

1. **Carrier Classes** (DOP Concept): A proposed flexible alternative to Records.
2. **Carrier Threads** (Virtual Thread Runtime): The native OS threads that run Virtual Threads.

---

## 1. Carrier Classes (The Concept)

### The Problem with Records

Records are **"Nominal Tuples"**. They are strict:

- **Immutable**: Fields are `final`.
- **Transparent**: The API (constructors/accessors) *must* match the state description exactly.
- **Final**: Cannot be extended.

Sometimes you want the *benefits* of records (Pattern Matching, Destructuring) but you need:

- Mutable state.
- Private state (not exposed in API).
- Validation that transforms data (API != Internal Representation).

### The "Carrier Class" Solution (Future)

A **Carrier Class** would be a normal `class` that publishes a **State Description**. This tells the compiler: *"Even though I am a complex class, you can treat me like a tuple of (x, y) for pattern matching."*

#### Conceptual Syntax (Not real Java code yet)

```java
// HYPOTHETICAL SYNTAX
carrier class Point {
    private int x, y;
    
    // State Description acts like a record header
    public state(int x, int y) {
        this.x = x;
        this.y = y;
    }
}
```

### Record vs. Carrier (Conceptual)

| Feature | `record` (Existing) | Carrier Class (Concept) |
| :--- | :--- | :--- |
| **Immutability** | Strictly Immutable | Flexible (Can be mutable) |
| **Encapsulation** | Transparent (API = Data) | Encapsulated (API != Data) |
| **Inheritance** | None (Final) | Normal Inheritance possible |
| **Pattern Matching**| Built-in (Component Match) | Custom (via Deconstructors) |

---

## 3. Pattern Matching Mechanics

### A. Records (The Status Quo)

Records have **"Transparent State"**. The compiler knows exactly how to deconstruct them because the constructor parameters matches the fields matches the accessors.

```java
// Definition
record Point(int x, int y) {}

// Matching (Java 21)
if (obj instanceof Point(int x, int y)) {
    // Compiler calls x() and y() accessors automatically
    System.out.println(x + y);
}
```

### B. Carrier Classes (The Future: Deconstructors)

Since a Carrier Class is encapsulated, the compiler *cannot* guess how to extract values. You might store `x` and `y` as a single `long`, or encrypt them.

To support Pattern Matching, Carrier Classes will likely introduce **Deconstructors** (The inverse of a Constructor).

#### Deconstruction Pattern (Hypothetical)

A deconstructor tells pattern matching how to "tear apart" the object.

```java
carrier class Point {
    private int x, y;
    
    // Constructor (Put data IN)
    public Point(int x, int y) { ... }
    
    // Matcher / Deconstructor (Get data OUT)
    // This allows: case Point(var a, var b)
    public matcher Point(int x, int y) {
        x = this.x;
        y = this.y;
    }
}
```

#### Why is this powerful?

It allows you to match logical views of data, not just physical fields.

```java
// Internal state: Cartesian (x, y)
carrier class Point {
    private double x, y;
    
    // Pattern 1: Match as Cartesian
    public matcher Point(double x, double y) {
        x = this.x;
        y = this.y;
    }
    
    // Pattern 2: Match as Polar Coordinates!
    // Allows: case Polar(var r, var theta)
    public matcher Polar(double r, double theta) {
        r = Math.sqrt(x*x + y*y);
        theta = Math.atan2(y, x);
    }
}

// Usage
switch (myPoint) {
    case Point(var x, var y) -> ...
    case Polar(var r, var theta) -> ...
}
```

## 4. Summary

- **Records**: Use them when your API **IS** your Data. Pattern matching is free.
- **Carrier Classes**: Use them when you need **Encapsulation** but still want Pattern Matching. You will explicitly write "Matchers" to bridge the gap.

> **Analogy**:
>
> - **Virtual Thread** = A single Uber Ride.
> - **Carrier Thread** = The Uber Driver/Car.
>
> The driver (Carrier) picks up a passenger (Virtual Thread), drives them for a while (CPU execution), and if the passenger needs to wait (block), the driver drops them off and picks up another passenger.

### Key Characteristics

1. **M:N Scheduling**: Millions of Virtual Threads are mapped to a few Carrier Threads (usually equal to CPU cores).
2. **Mount/Unmount**: When a Virtual Thread triggers a blocking I/O operation (e.g., `socket.read()`), existing Java APIs automagically **unmount** it from the Carrier. The Carrier is then free to do other work.
3. **ForkJoinPool**: The default scheduler for Carrier Threads.

```mermaid
graph TD
    subgraph "OS Kernel"
        CT1[Carrier Thread 1]
        CT2[Carrier Thread 2]
    end

    subgraph "JVM / Heap"
        VT1[Virtual Thread 1]
        VT2[Virtual Thread 2]
        VT3[Virtual Thread 3]
        VT4[Virtual Thread 4]
    end

    VT1 -.->|Mounts| CT1
    VT2 -.->|Mounts| CT2
    VT3 -.->|Waiting (Unmounted)| Heap[Heap Memory]
    VT4 -.->|Waiting (Unmounted)| Heap
```
