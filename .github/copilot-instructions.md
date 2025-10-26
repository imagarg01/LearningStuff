# AI Coding Agent Instructions for LearningStuff

This document guides AI agents on the essential patterns and practices for working with this codebase.

## Project Overview

LearningStuff is a learning-focused repository combining documentation and Java examples, particularly showcasing modern Java features and concurrent programming patterns.

## Key Technologies

- Java 21 (with preview features enabled)
- Maven for build management
- Structured Concurrency focus
- Apache Commons Lang (3.12.0, 2.4)

## Critical Patterns

### Java Code Structure
- Package naming: `com.ashish.{module}` (e.g., `com.ashish.thread`)
- Modern Java features heavily used:
  - Records for data classes (see `Weather` in `PlayingWithSC.java`)
  - Structured Concurrency with `StructuredTaskScope`
  - Pattern matching and var inference
  - Try-with-resources for resource management

### Exception Handling
```java
// Pattern: Wrap checked exceptions in RuntimeException with context
catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    throw new WeatherReadException("Failed to read weather data", e);
}
```

### Build and Run Commands
- Compile: `mvn compile` (includes --enable-preview)
- Full build: `mvn clean compile`
- Run example: `mvn exec:java -Dexec.mainClass="com.ashish.thread.PlayingWithSC"`

## Project Structure

- `/src/main/java/` - Java source code
  - `com.ashish.thread/` - Concurrency examples
- `/docs/` - Documentation by topic
  - Architecture, finance, Java concepts, etc.
- `/target/` - Compiled output (don't commit)

## Development Workflow

1. Enable preview features in your IDE for Java 21
2. Ensure Maven build includes `--enable-preview` flag
3. Follow existing patterns for:
   - Exception handling with proper context
   - Concurrency using StructuredTaskScope
   - Records for data classes
   - Descriptive naming in camelCase/PascalCase

## Documentation

Important context available in:
- `docs/java/` - Java-specific concepts
- `docs/SoftwareArch&Design/` - Architecture guidelines
- Individual module READMEs