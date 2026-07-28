# DECISIONS.md — Architecture Decision Record (ADR) Log

This document records the major architectural decisions made for Project ZERO, including context, alternatives considered, justifications, and trade-offs.

---

## ADR-001: Project Name & Identity Pivot
- **Date**: 2026-07-28
- **Context**: The project was initially referred to academically as "AIOS".
- **Decision**: Formally adopt **Project ZERO** (or ZERO) as the permanent name and brand identity.
- **Justification**: ZERO reflects a clean slate, low-overhead microkernel philosophy, and personal autonomous intelligence platform identity.

---

## ADR-002: Vertical-Slice TypeScript Strategy over Premature Rust Microkernel
- **Date**: 2026-07-28
- **Context**: Designing a full Rust microkernel core in Phase 1 risks 3-6 months of low-level infrastructure development without delivering a usable daily product.
- **Decision**: Build Phases 1 through 9 as a high-velocity TypeScript + Tauri application. Extract stable core modules into a high-performance Rust microkernel in Phase 10.
- **Alternatives Considered**:
  1. *Rust Microkernel First*: Technically pure, but delays daily driver usability for months.
  2. *Pure Python Monolith*: Fast prototype, but poor desktop integration, high RAM usage, and weak typing.
- **Trade-Offs**: Requires refactoring stable TypeScript interfaces into Rust in Phase 10, but delivers immediate product value on Day 14.

---

## ADR-003: Model Router Default to Gemini 1.5/2.0 API with Provider Circuit Breakers
- **Date**: 2026-07-28
- **Context**: ZERO requires multi-modal processing (text, code, audio, screen images), ultra-large context windows, and low latency.
- **Decision**: Primary default LLM provider is Gemini (Gemini 1.5 Pro / Flash & Gemini 2.0). Implement automatic circuit breakers to fail over to Claude or local Ollama instances upon API rate-limit/error.
- **Justification**: Gemini offers premier context window capacity, native multi-modality, and cost efficiency.

---

## ADR-004: Model Context Protocol (MCP) Standard for Tool Host Subsystems
- **Date**: 2026-07-28
- **Context**: Tools must be extensible, decoupled from model backends, and reusable across environments.
- **Decision**: Adopt Anthropic's Model Context Protocol (MCP) JSON-RPC standard for all internal and third-party tools.
- **Justification**: Guarantees zero vendor lock-in, client-server decoupling, and instant compatibility with thousands of open-source MCP tools.

---

## ADR-005: Hybrid Memory Architecture (SQLite WAL + Qdrant Vector + KuzuDB Graph)
- **Date**: 2026-07-28
- **Context**: Opaque vector-only databases lack structured transactional history and deterministic full-text search.
- **Decision**: Implement a 4-tier memory architecture using SQLite (WAL mode + FTS5) for episodic logs, Qdrant/LanceDB for vector embeddings, and KuzuDB for entity relationships.
- **Justification**: Provides exact keyword search, dense semantic similarity, and property graph traversals without data corruption.
