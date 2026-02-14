# LearningStuff 🚀

A comprehensive learning repository covering **Java concurrency**, **AI/ML**, **system design**, **cloud infrastructure**, **networking**, and more. This project contains extensive documentation, runnable code examples, and practical implementations.

---

## 🎯 Key Capabilities

### 1. **Java Concurrency & Modern Features** ⚡

**20+ Runnable Examples** covering:

- **Scoped Values** (JDK 21+) - Modern alternative to ThreadLocal
- **Virtual Threads** - Lightweight concurrency
- **Structured Concurrency** - Hierarchical task management
- **CompletableFuture** - Asynchronous programming
- **Blocking Queues** - Thread-safe data structures
- **Executor Services** - Thread pool management
- **Parallel Streams** - Data parallelism
- **Synchronization** - Thread coordination

**Quick Start:**

```bash
make help                    # See all available examples
make scoped-basic            # Run Scoped Values example
make virtual-threads         # Run Virtual Threads demo
make all-concurrency         # Run all concurrency examples
```

📖 **Documentation:** [`docs/java/`](docs/java/) - Comprehensive guides on Java concurrency, Virtual Threads, Structured Concurrency, and more

### 2. **AI & Machine Learning** 🤖

**Topics Covered:**

- **RAG (Retrieval-Augmented Generation)** - Advanced retrieval strategies, evaluation metrics
- **Context Graphs** - Knowledge graph construction for LLMs
- **Recursive Language Models (RLM)** - Advanced model architectures
- **BAML** - Structured LLM outputs

📖 **Documentation:** [`docs/AI/`](docs/AI/) - 159 files covering AI/ML concepts, implementations, and best practices

### 3. **System Design** 🏗️

**Topics Covered:**

- **OAuth2** - Authentication and authorization
- **Fintech Systems** - Payment processing, event streaming
- **Distributed Systems** - Scalability patterns
- **CQRS & Event Sourcing** - Architecture patterns

📖 **Documentation:** [`docs/system_design/`](docs/system_design/)

### 4. **Cloud & Infrastructure** ☁️

**Topics Covered:**

- **Infrastructure as Code (IAC)** - Terraform, CloudFormation
- **Kubernetes** - Container orchestration
- **Cloud Platforms** - AWS, GCP, Azure
- **Observability** - Monitoring, logging, tracing

📖 **Documentation:**

- [`docs/IAC/`](docs/IAC/) - 76 files on infrastructure automation
- [`docs/Cloud/`](docs/Cloud/) - 33 files on cloud platforms
- [`docs/Kubernetes/`](docs/Kubernetes/)
- [`docs/Observability/`](docs/Observability/)

### 5. **Networking** 🌐

**Topics Covered:**

- Network protocols and concepts
- Performance optimization
- Security best practices

📖 **Documentation:** [`docs/Networking/`](docs/Networking/) - 31 files

### 6. **Performance Engineering** 📊

**Runnable Examples:**

- **Flamegraph Analysis** - CPU profiling and visualization
- **JFR (Java Flight Recorder)** - Production profiling
- **Spring Boot Performance** - Application optimization

```bash
make flamegraph              # Run flamegraph example
```

---

## 📁 Repository Structure

```
LearningStuff/
├── docs/                    # Comprehensive documentation
│   ├── AI/                  # AI/ML topics (159 files)
│   ├── java/                # Java concurrency & features (29 files)
│   ├── system_design/       # System design patterns (15 files)
│   ├── IAC/                 # Infrastructure as Code (76 files)
│   ├── Cloud/               # Cloud platforms (33 files)
│   ├── Kubernetes/          # K8s documentation (6 files)
│   ├── Networking/          # Network concepts (31 files)
│   ├── Observability/       # Monitoring & logging (15 files)
│   ├── Finance/             # Financial concepts (51 files)
│   └── books/               # Reading lists and notes
│
├── src/main/java/           # Runnable Java examples
│   ├── com/ashish/thread/   # 18 concurrency examples
│   └── com/learning/performance/  # Performance examples
│
├── Makefile                 # Convenient targets for running examples
└── pom.xml                  # Maven build configuration
```

---

## 🚀 Quick Start

### Prerequisites

- **Java 21+** (for modern features like Scoped Values, Virtual Threads)
- **Maven 3.6+**
- **Make** (optional, for convenient commands)

### Running Java Examples

**Using Makefile (Recommended):**

```bash
# See all available examples
make help

# Run specific examples
make scoped-basic            # Scoped Values basics
make virtual-threads         # Virtual Threads demo
make structured-concurrency  # Structured Concurrency
make completable-future      # CompletableFuture patterns

# Run all examples by category
make all-scoped              # All Scoped Values examples
make all-concurrency         # All concurrency examples
make all-virtual-threads     # All Virtual Threads examples
make all-examples            # Run ALL examples!
```

**Using Maven directly:**

```bash
# Compile
mvn clean compile

# Run specific example
mvn exec:exec -Dexec.mainClass="com.ashish.thread.VirtualThreadsDemo"
```

### Exploring Documentation

```bash
# Browse documentation
open docs/java/ScopedValue.md           # Scoped Values guide
open docs/java/VirtualThread.md         # Virtual Threads guide
open docs/AI/RAG/                       # RAG documentation
open docs/system_design/OAuth2/         # OAuth2 guide
```

---

## 📚 Featured Documentation

### Java Concurrency

- [**Scoped Values**](docs/java/ScopedValue.md) - Complete guide from beginner to advanced
- [**Virtual Threads**](docs/java/VirtualThread.md) - Lightweight concurrency in Java
- [**Structured Concurrency**](docs/java/StructuredConcurrency.md) - Hierarchical task management
- [**CompletableFuture**](docs/java/CompletableFuture.md) - Asynchronous programming patterns
- [**Blocking Queues**](docs/java/BlockingQueue.md) - Thread-safe queues

### AI/ML

- [**RAG Strategies**](docs/AI/RAG/) - Retrieval-Augmented Generation
- [**Context Graphs**](docs/AI/Context_Graph/) - Knowledge graphs for LLMs
- [**Recursive Language Models**](docs/AI/RLM/) - Advanced model architectures

### System Design

- [**OAuth2**](docs/system_design/OAuth2/) - Authentication patterns
- [**Fintech**](docs/system_design/Fintech/) - Payment systems, event streaming

---

## 🎓 Learning Path

### For Java Developers

1. Start with [Java Concurrency Decision Guide](docs/java/ConcurrencyDecisionGuide.md)
2. Explore [Virtual Threads](docs/java/VirtualThread.md)
3. Learn [Scoped Values](docs/java/ScopedValue.md)
4. Master [Structured Concurrency](docs/java/StructuredConcurrency.md)
5. Run examples: `make all-virtual-threads`

### For AI/ML Engineers

1. Explore [RAG documentation](docs/AI/RAG/)
2. Learn [Context Graphs](docs/AI/Context_Graph/)
3. Study [Recursive Language Models](docs/AI/RLM/)

### For System Designers

1. Review [System Design patterns](docs/system_design/)
2. Study [OAuth2 implementation](docs/system_design/OAuth2/)
3. Explore [Fintech architectures](docs/system_design/Fintech/)

---

## 🛠️ Development

### Build

```bash
mvn clean compile
```

### Run Tests

```bash
mvn test
```

### Clean

```bash
make clean
# or
mvn clean
```

---

## 📊 Project Stats

- **450+ Documentation Files**
- **26 Runnable Java Examples**
- **13 Major Topic Areas**
- **Java 21+ Modern Features**
- **Production-Ready Patterns**

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Add new examples
- Improve documentation
- Fix bugs
- Suggest new topics

---

## 📝 License

This is a personal learning repository. Feel free to use the code and documentation for your own learning purposes.

---

**Last Updated:** February 14, 2026
