# [Repository Name] - Repo Spec (agents.md)

> **Purpose:** This file grounds all AI Agents operating in this repository. It defines strict architectural boundaries, dependencies, and tribal knowledge to prevent hallucinations.

## 1. Architecture & Tech Stack
*   **Primary Language:** [e.g., Java 21, TypeScript 5.2]
*   **Core Frameworks:** [e.g., Spring Boot 3.2, React 18, Next.js 14]
*   **Architecture Pattern:** [e.g., Microservices, Monolith, Event-Driven, Hexagonal Architecture]

## 2. The Code Map (Directory Structure)
Agents must use this map to locate logic and place new files correctly.
*   `[path/to/domain]`: Contains pure business logic. No external dependencies.
*   `[path/to/infrastructure]`: Database adapters, third-party API clients.
*   `[path/to/api]`: Controllers, routes, and GraphQL resolvers.

## 3. External Boundaries & Integrations
Do not invent new databases or message queues. Use these explicitly:
*   **Primary Database:** [e.g., PostgreSQL for relational data. Schemas managed via Flyway.]
*   **Caching:** [e.g., Redis. Keys must be prefixed with `app:`]
*   **Message Broker:** [e.g., Kafka. Domain events publish to `domain.events` topic.]
*   **Downstream APIs:** [e.g., Auth service at `auth.internal.corp`.]

## 4. Testing Standards
All generated code must be accompanied by tests that pass the CI pipeline.
*   **Unit Tests:** [e.g., Use JUnit 5 & Mockito. Code coverage must be > 80%.]
*   **E2E Tests:** [e.g., Use Playwright. Run against the local Docker compose stack.]
*   **Mocking:** [e.g., Never hit real databases in unit tests. Use `TestContainers` for integration tests.]

## 5. Known Gotchas & Legacy Constraints (CRITICAL)
*   [Add known issue: e.g., "Do not use the standard `Date` object, always use `java.time.Instant` in UTC."]
*   [Add known issue: e.g., "The `legacy_users` table is read-only. Writes must go through `UserMigrationService`."]
