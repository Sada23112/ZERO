# CODING_STANDARD.md — Coding Standards & Engineering Practices for Project ZERO

This document specifies the exact code formatting, error handling, logging, testing, and API design standards for Project ZERO.

---

## 1. Naming Conventions

- **Files & Folders**: Lowercase `kebab-case` (`model-router.ts`, `task-engine.ts`).
- **Interfaces & Types**: `PascalCase` (`InferenceRequest`, `CapabilityToken`).
- **Functions & Methods**: `camelCase` (`assembleContext()`, `executeTool()`).
- **Constants**: `UPPER_SNAKE_CASE` (`MAX_CONTEXT_TOKENS`, `DEFAULT_TIMEOUT_MS`).

---

## 2. Error Handling & Logging

- **No Swallowed Exceptions**: Never use empty `catch` blocks.
- **Result Monads / Explicit Errors**: Domain functions MUST return typed errors (`Result<T, E>`) or throw custom error classes extending `ZeroError`.
- **Structured Logging**: Use `pino` structured JSON logging. Log events with severity levels: `trace`, `debug`, `info`, `warn`, `error`, `fatal`.

```typescript
// Correct Error Handling Pattern
try {
  const result = await toolHost.executeTool(token, toolName, args);
  logger.info({ toolName, status: 'success' }, 'Tool execution completed');
  return result;
} catch (error) {
  logger.error({ toolName, err: error }, 'Tool execution failed');
  throw new ToolExecutionError(`Failed to execute ${toolName}`, { cause: error });
}
```

---

## 3. Testing Requirements

- **Unit Tests**: Co-located with source files using `.test.ts` extension (e.g. `model-router.test.ts`).
- **Integration Tests**: Stored in `tests/integration/`.
- **Coverage Standard**: Core utilities (memory indexers, security gatekeepers, token calculators) must achieve > 95% test coverage.

---

## 4. API & Dependency Injection

- **Dependency Injection**: Pass external dependencies (database instances, LLM clients, tool hosts) via constructor parameters or factory functions to enable clean unit testing.
- **Immutability**: Prefer `readonly` properties and immutable data structures where possible.
