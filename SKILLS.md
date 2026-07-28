# SKILLS.md — Technical Mastery Handbook for Project ZERO

This document defines the technical competencies, pattern standards, and operational guidelines required when working on Project ZERO's codebase.

---

## 1. TypeScript & Structural Design
- **Strict Typing**: `noImplicitAny`, `strictNullChecks`, and `exactOptionalPropertyTypes` are enabled. Avoid using `any`; use `unknown` with explicit type guards.
- **Interface Segregation**: Prefer small, focused interfaces. Define interfaces at consumption sites rather than exporting huge monolithic types.
- **Async Safety**: Always handle promise rejections with explicit `try/catch` or result monads (`Result<T, E>`). Never swallow errors silently.

## 2. React & Tauri Desktop UI
- **Tauri Architecture**: The frontend communicates with the backend exclusively via typed IPC commands (`invoke('plugin:zero|command')`) or event streams.
- **State Management**: Keep UI state minimal. Render state derived from background events; avoid duplicating domain state in local component state.
- **Performance**: High-frequency overlay updates (e.g. streaming LLM responses or voice audio levels) must bypass heavy re-renders using refs or direct canvas updates.

## 3. Gemini API Integration & Model Routing
- **Streaming First**: All model completion calls must use streaming interfaces (`generateContentStream`) to provide immediate user feedback.
- **Structured Outputs**: Use JSON schemas (`responseSchema`) for tool arguments and step planning to guarantee syntactic validity.
- **Circuit Breaker Pattern**: If Gemini API returns 429 or 5xx, fail over gracefully to secondary providers (Claude / local Ollama) within < 200ms.

## 4. Model Context Protocol (MCP) & Tool Development
- **Decoupled Tools**: Tools must be implemented as standalone MCP servers communicating over stdio or SSE using JSON-RPC 2.0.
- **Schema Validation**: Validate input payloads using Zod or JSON Schema before passing them to execution handlers.
- **Idempotency**: Whenever possible, make tool actions idempotent (e.g. `write_file` replaces target content explicitly rather than blindly appending).

## 5. SQLite & Vector Memory Management
- **WAL Mode**: SQLite databases (`zero.db`) MUST be configured with `PRAGMA journal_mode=WAL;` and `PRAGMA synchronous=NORMAL;`.
- **Hybrid Retrieval**: Combine vector similarity search (Qdrant / LanceDB) with SQLite FTS5 BM25 keyword search using Reciprocal Rank Fusion (RRF).
- **Transactional Consistency**: All multi-turn memory updates must execute inside explicit database transactions.

## 6. Playwright Browser & Desktop Automation
- **Headless Execution**: Browser automation runs headless by default; toggle headful mode only for interactive user authorization sessions.
- **DOM & Visual Grounding**: Combine accessibility tree parsing (AXTree) with visual screenshot analysis for robust UI element locator strategies.

## 7. Dynamic Planning & Workflow Engineering
- **DAG Representation**: Plans are modeled as Directed Acyclic Task Graphs with explicit pre-conditions (`FileExists`) and post-conditions (`ExitCode == 0`).
- **Plan Repair**: Upon tool execution failure, trigger an observation assessor to mutate the active DAG rather than restarting the plan from scratch.

## 8. Testing, Refactoring & Debugging
- **Empirical Diagnostics**: Never hypothesis-fix an issue without inspecting the full un-truncated error traceback.
- **TDD for Core Utilities**: Memory indexers, token estimators, and capability validators MUST have 100% unit test coverage.
