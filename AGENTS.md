# AGENTS.md - Coding Guidelines for LearningStuff Repository

## Build Commands
- **Compile**: `mvn compile` - Compile Java sources with Java 21 preview features
- **Clean**: `mvn clean` - Remove target directory
- **Full build**: `mvn clean compile` - Clean and compile
- **Run main class**: `mvn exec:java -Dexec.mainClass="com.ashish.thread.PlayingWithSC"`

## Code Style Guidelines

### Language & Framework
- **Java Version**: Java 21 with preview features enabled (`--enable-preview`)
- **Build Tool**: Maven
- **Package Structure**: `com.ashish.{module}` (e.g., `com.ashish.thread`)

### Naming Conventions
- **Classes**: PascalCase (e.g., `CustomStructuredPolicyExample`, `PlayingWithSC`)
- **Methods**: camelCase (e.g., `getPriceFromAirline1`, `readSunnyWeather`)
- **Variables**: camelCase with descriptive names (e.g., `weatherSubTask`, `arrayOfPrices`)
- **Constants**: UPPER_SNAKE_CASE (not observed in current codebase)
- **Packages**: lowercase with dots (e.g., `com.ashish.thread`)

### Code Patterns
- Use modern Java features: records, `var`, structured concurrency, try-with-resources
- Import organization: java.* packages first, then third-party libraries
- Exception handling: Wrap checked exceptions in `RuntimeException` when appropriate
- Use descriptive variable names and method names
- Prefer functional programming constructs where appropriate

### Dependencies
- Apache Commons Lang 3.12.0
- Apache Commons Lang 2.4

## Testing
No test framework currently configured. Add JUnit/Mockito to pom.xml for unit testing.

## File Structure
- `src/main/java/` - Source code
- `docs/` - Documentation and learning materials
- `pom.xml` - Maven configuration