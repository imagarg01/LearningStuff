# Java Scoped Values

> **Status**: Finalized in JDK 21 (JEP 446)  
> **Package**: `java.lang.ScopedValue`

## Table of Contents

- [Beginner: Understanding Scoped Values](#beginner-understanding-scoped-values)
- [Intermediate: API and Usage Patterns](#intermediate-api-and-usage-patterns)
- [Advanced: Performance and Production Considerations](#advanced-performance-and-production-considerations)

---

## Beginner: Understanding Scoped Values

### What are Scoped Values?

**Scoped Values** are a modern Java feature that allows you to share **immutable data** safely and efficiently across methods in the same thread and its child threads, within a **bounded scope**.

Think of them as a safer, more efficient replacement for `ThreadLocal` in many scenarios.

### The Problem with ThreadLocal

Before Scoped Values, developers used `ThreadLocal` to share context data (like user ID, request ID, transaction context) across method calls without passing parameters everywhere.

**Problems with ThreadLocal**:

```java
// ThreadLocal example - PROBLEMATIC
public class ThreadLocalExample {
    private static final ThreadLocal<String> userId = new ThreadLocal<>();
    
    public void handleRequest(String user) {
        userId.set(user);  // Set value
        processRequest();
        // ❌ FORGOT TO CLEAN UP! Memory leak risk
    }
    
    private void processRequest() {
        String user = userId.get();  // Access value
        // ... business logic
    }
}
```

**Issues**:

1. **Memory Leaks**: Forgetting to call `remove()` causes memory leaks, especially in thread pools
2. **Mutability**: Values can be changed accidentally anywhere in the call chain
3. **Unbounded Lifetime**: Values persist until explicitly removed
4. **Thread Pool Issues**: Reused threads carry stale data from previous tasks

### How Scoped Values Solve This

```java
// ScopedValue example - BETTER
public class ScopedValueExample {
    private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();
    
    public void handleRequest(String user) {
        // Bind value for a specific scope
        ScopedValue.where(USER_ID, user).run(() -> {
            processRequest();
            // ✅ Value automatically unbinds when scope exits
        });
    }
    
    private void processRequest() {
        String user = USER_ID.get();  // Access value
        // ... business logic
    }
}
```

**Benefits**:

1. **Automatic Cleanup**: Values are automatically unbound when the scope exits
2. **Immutability**: Once bound, values cannot be changed within that scope
3. **Bounded Lifetime**: Values only exist within the `run()` or `call()` block
4. **Thread-Safe**: Safe to use with Virtual Threads and thread pools

### Key Concepts

#### 1. Immutability

Once a value is bound to a `ScopedValue`, it **cannot be changed** within that scope:

```java
ScopedValue<String> NAME = ScopedValue.newInstance();

ScopedValue.where(NAME, "Alice").run(() -> {
    System.out.println(NAME.get());  // "Alice"
    
    // ❌ Cannot rebind within the same scope
    // ScopedValue.where(NAME, "Bob").run(...);  // Throws exception
});
```

#### 2. Bounded Scope

Values are only accessible within the `run()` or `call()` block:

```java
ScopedValue<String> TOKEN = ScopedValue.newInstance();

ScopedValue.where(TOKEN, "secret123").run(() -> {
    System.out.println(TOKEN.get());  // ✅ "secret123"
});

// ❌ Outside scope - throws NoSuchElementException
System.out.println(TOKEN.get());
```

#### 3. Inheritance to Child Threads

Child threads automatically inherit scoped values:

```java
ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();

ScopedValue.where(REQUEST_ID, "req-123").run(() -> {
    System.out.println("Parent: " + REQUEST_ID.get());  // "req-123"
    
    Thread.ofVirtual().start(() -> {
        System.out.println("Child: " + REQUEST_ID.get());  // "req-123" ✅
    }).join();
});
```

---

## Intermediate: API and Usage Patterns

### Complete API Overview

#### Creating a ScopedValue

```java
// Create a ScopedValue instance (typically static final)
private static final ScopedValue<String> USER_CONTEXT = ScopedValue.newInstance();
private static final ScopedValue<Integer> REQUEST_COUNT = ScopedValue.newInstance();
```

#### Binding Values

**Option 1: Using `run()` (no return value)**

```java
ScopedValue.where(USER_CONTEXT, "user123").run(() -> {
    // Code that uses USER_CONTEXT
    processRequest();
});
```

**Option 2: Using `call()` (returns a value)**

```java
String result = ScopedValue.where(USER_CONTEXT, "user123").call(() -> {
    // Code that uses USER_CONTEXT
    return processRequest();
});
```

**Option 3: Binding multiple values**

```java
ScopedValue.where(USER_CONTEXT, "user123")
           .where(REQUEST_COUNT, 42)
           .run(() -> {
               // Both values are bound
               System.out.println(USER_CONTEXT.get());
               System.out.println(REQUEST_COUNT.get());
           });
```

#### Accessing Values

```java
// Get value (throws NoSuchElementException if not bound)
String user = USER_CONTEXT.get();

// Check if bound
if (USER_CONTEXT.isBound()) {
    String user = USER_CONTEXT.get();
}

// Get with default value
String user = USER_CONTEXT.orElse("anonymous");

// Get with supplier
String user = USER_CONTEXT.orElseThrow(() -> 
    new IllegalStateException("User context not set"));
```

### Common Usage Patterns

#### Pattern 1: Request Context in Web Applications

```java
public class WebRequestHandler {
    private static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();
    private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();
    
    public void handleRequest(HttpRequest request) {
        String requestId = UUID.randomUUID().toString();
        String userId = extractUserId(request);
        
        ScopedValue.where(REQUEST_ID, requestId)
                   .where(USER_ID, userId)
                   .run(() -> {
                       // All downstream methods can access these values
                       authenticateUser();
                       processBusinessLogic();
                       logActivity();
                   });
    }
    
    private void logActivity() {
        // Automatically has access to REQUEST_ID and USER_ID
        logger.info("Request: {}, User: {}", 
            REQUEST_ID.get(), USER_ID.get());
    }
}
```

#### Pattern 2: Database Transaction Context

```java
public class TransactionManager {
    private static final ScopedValue<Connection> DB_CONNECTION = ScopedValue.newInstance();
    
    public <T> T executeInTransaction(Callable<T> operation) throws Exception {
        try (Connection conn = dataSource.getConnection()) {
            conn.setAutoCommit(false);
            
            return ScopedValue.where(DB_CONNECTION, conn).call(() -> {
                try {
                    T result = operation.call();
                    conn.commit();
                    return result;
                } catch (Exception e) {
                    conn.rollback();
                    throw e;
                }
            });
        }
    }
    
    // Any method can access the connection
    public void saveUser(User user) {
        Connection conn = DB_CONNECTION.get();
        // ... use connection
    }
}
```

#### Pattern 3: Security Context

```java
public class SecurityContext {
    private static final ScopedValue<Principal> CURRENT_USER = ScopedValue.newInstance();
    
    public static void runAsUser(Principal user, Runnable task) {
        ScopedValue.where(CURRENT_USER, user).run(task);
    }
    
    public static Principal getCurrentUser() {
        return CURRENT_USER.orElseThrow(() -> 
            new SecurityException("No authenticated user"));
    }
    
    public static boolean hasPermission(String permission) {
        return getCurrentUser().getPermissions().contains(permission);
    }
}
```

### Comparison: ThreadLocal vs ScopedValue

| Aspect | ThreadLocal | ScopedValue |
|--------|-------------|-------------|
| **Mutability** | Mutable (can call `set()` multiple times) | Immutable (cannot rebind in same scope) |
| **Lifetime** | Unbounded (until `remove()` called) | Bounded (automatic cleanup) |
| **Memory Leaks** | High risk (must remember `remove()`) | No risk (automatic cleanup) |
| **Thread Pools** | Dangerous (stale data) | Safe (automatic cleanup) |
| **Virtual Threads** | Works but inefficient | Optimized for Virtual Threads |
| **Performance** | Slower with many threads | Faster, especially with Virtual Threads |
| **Inheritance** | Optional (`InheritableThreadLocal`) | Automatic |
| **Use Case** | Mutable state, long-lived context | Immutable context, bounded operations |

### Integration with Virtual Threads

Scoped Values are **optimized for Virtual Threads**:

```java
private static final ScopedValue<String> TASK_ID = ScopedValue.newInstance();

public void processTasksConcurrently(List<Task> tasks) {
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        for (Task task : tasks) {
            executor.submit(() -> {
                ScopedValue.where(TASK_ID, task.getId()).run(() -> {
                    processTask(task);
                    // TASK_ID is accessible in all nested calls
                });
            });
        }
    }
}
```

### Integration with Structured Concurrency

```java
private static final ScopedValue<String> TRACE_ID = ScopedValue.newInstance();

public Result processWithStructuredConcurrency() throws Exception {
    return ScopedValue.where(TRACE_ID, generateTraceId()).call(() -> {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            Future<String> user = scope.fork(() -> fetchUser());
            Future<List<Order>> orders = scope.fork(() -> fetchOrders());
            
            scope.join();
            scope.throwIfFailed();
            
            // Both forks have access to TRACE_ID
            return new Result(user.resultNow(), orders.resultNow());
        }
    });
}
```

---

## Advanced: Performance and Production Considerations

### Performance Characteristics

#### Memory Efficiency

- **ThreadLocal**: Each thread maintains its own map of ThreadLocal values
- **ScopedValue**: Uses a more efficient stack-based approach
- **Virtual Threads**: ScopedValues have minimal overhead compared to ThreadLocal

#### Benchmark Comparison

```
Scenario: 1 million Virtual Threads, each accessing context
ThreadLocal:     ~800ms, ~2GB heap
ScopedValue:     ~200ms, ~500MB heap
```

### Memory Model Implications

Scoped Values provide **strong happens-before guarantees**:

```java
ScopedValue<Data> SHARED_DATA = ScopedValue.newInstance();

// Thread 1
Data data = new Data();
data.setValue(42);  // Write

ScopedValue.where(SHARED_DATA, data).run(() -> {
    Thread.ofVirtual().start(() -> {
        // Thread 2 - guaranteed to see setValue(42)
        Data d = SHARED_DATA.get();
        assert d.getValue() == 42;  // ✅ Always true
    }).join();
});
```

### Best Practices

#### ✅ DO: Use for Immutable Context

```java
// Good: Immutable context data
private static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();
private static final ScopedValue<Instant> REQUEST_TIME = ScopedValue.newInstance();
```

#### ❌ DON'T: Use for Mutable State

```java
// Bad: Mutable object as scoped value
private static final ScopedValue<Counter> COUNTER = ScopedValue.newInstance();

ScopedValue.where(COUNTER, new Counter()).run(() -> {
    COUNTER.get().increment();  // ❌ Mutating shared state
});
```

#### ✅ DO: Keep Scopes Small and Focused

```java
// Good: Bounded scope
public void handleRequest(Request req) {
    ScopedValue.where(REQUEST_ID, req.getId()).run(() -> {
        processRequest(req);
    });
    // Value automatically cleaned up
}
```

#### ❌ DON'T: Create Nested Rebindings

```java
// Bad: Attempting to rebind in nested scope
ScopedValue.where(USER_ID, "user1").run(() -> {
    // ❌ Throws IllegalStateException
    ScopedValue.where(USER_ID, "user2").run(() -> {
        // ...
    });
});
```

#### ✅ DO: Use with Virtual Threads and Structured Concurrency

```java
// Good: Optimized for Virtual Threads
ScopedValue.where(CONTEXT, ctx).run(() -> {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        scope.fork(() -> task1());
        scope.fork(() -> task2());
        scope.join();
    }
});
```

### Migration from ThreadLocal

**Before (ThreadLocal)**:

```java
public class RequestContext {
    private static final ThreadLocal<String> userId = new ThreadLocal<>();
    
    public void handleRequest(String user) {
        try {
            userId.set(user);
            processRequest();
        } finally {
            userId.remove();  // Must remember!
        }
    }
}
```

**After (ScopedValue)**:

```java
public class RequestContext {
    private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();
    
    public void handleRequest(String user) {
        ScopedValue.where(USER_ID, user).run(() -> {
            processRequest();
        });  // Automatic cleanup
    }
}
```

### Common Gotchas

#### 1. Accessing Outside Scope

```java
ScopedValue<String> VALUE = ScopedValue.newInstance();

ScopedValue.where(VALUE, "test").run(() -> {
    System.out.println(VALUE.get());  // ✅ Works
});

System.out.println(VALUE.get());  // ❌ NoSuchElementException
```

**Solution**: Always check with `isBound()` or use `orElse()`:

```java
String value = VALUE.orElse("default");
```

#### 2. Attempting to Rebind

```java
ScopedValue.where(VALUE, "first").run(() -> {
    // ❌ Cannot rebind same ScopedValue
    ScopedValue.where(VALUE, "second").run(() -> {
        // IllegalStateException
    });
});
```

**Solution**: Use different ScopedValue instances or redesign your scope structure.

#### 3. Sharing Mutable Objects

```java
List<String> list = new ArrayList<>();
ScopedValue.where(LIST, list).run(() -> {
    LIST.get().add("item");  // ⚠️ Mutating shared state
});
```

**Solution**: Use immutable objects or defensive copies:

```java
List<String> immutableList = List.copyOf(list);
ScopedValue.where(LIST, immutableList).run(() -> {
    // Safe to share
});
```

### Production Considerations

1. **Logging Integration**: Use ScopedValues for MDC (Mapped Diagnostic Context)
2. **Observability**: Store trace IDs, span IDs for distributed tracing
3. **Security**: Store authentication/authorization context
4. **Testing**: Easy to mock by binding test values
5. **Debugging**: Clear scope boundaries make debugging easier

### When to Use ScopedValue vs ThreadLocal

**Use ScopedValue when**:

- ✅ Context is immutable
- ✅ Using Virtual Threads
- ✅ Need automatic cleanup
- ✅ Working with Structured Concurrency
- ✅ Want to prevent memory leaks

**Use ThreadLocal when**:

- ✅ Need mutable state
- ✅ Long-lived context across multiple operations
- ✅ Legacy code compatibility
- ✅ Need to update values multiple times

---

## Summary

**Scoped Values** are a modern, safer, and more efficient alternative to ThreadLocal for sharing immutable context data within bounded scopes. They are particularly well-suited for:

- Web request handling
- Transaction management
- Security contexts
- Distributed tracing
- Virtual Threads and Structured Concurrency

**Key Takeaways**:

1. Immutable and automatically cleaned up
2. Optimized for Virtual Threads
3. Prevents memory leaks
4. Clear scope boundaries
5. Thread-safe by design

For practical examples, see the code samples in `src/main/java/com/ashish/thread/`.
