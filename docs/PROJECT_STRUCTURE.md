# PROJECT_STRUCTURE.md — Repository Layout & Module Boundaries

This document defines the monorepo directory layout for Project ZERO.

```
zero/
├── docs/                           # Permanent Constitution & Technical Specs
│   ├── AGENTS.md                   # Primary AI developer instructions
│   ├── SKILLS.md                   # Technical mastery handbook
│   ├── MANIFESTO.md                # Constitution & core philosophy
│   ├── PRODUCT.md                  # Product definition & UX filter
│   ├── ARCHITECTURE.md             # High-level architecture guide
│   ├── ROADMAP.md                  # Living 10-phase engineering roadmap
│   ├── DECISIONS.md                # Architecture Decision Record (ADR) log
│   ├── CONTRIBUTING.md             # Contributor guidelines
│   ├── PROJECT_STRUCTURE.md        # Repository layout reference
│   ├── MEMORY_GUIDE.md             # Cognitive memory architecture
│   ├── SECURITY.md                 # Security & permission specifications
│   └── CODING_STANDARD.md          # Detailed coding guidelines
├── pnpm-workspace.yaml             # Master TypeScript workspace configuration
├── package.json                    # Root scripts and workspace settings
├── apps/                           # End-User Applications
│   ├── desktop/                    # Desktop overlay UI (Tauri/Electron)
│   ├── mobile/                     # Android Flutter companion client (Phase 9)
│   └── cli/                        # Terminal CLI harness (`zero-cli`)
├── packages/                       # Shared Core TypeScript Libraries
│   ├── core/                       # Model Router, Task Engine & Execution Loop
│   ├── memory/                     # SQLite WAL, Qdrant Vector & Graph interfaces
│   ├── security/                   # Capability Tokens & Permission Gatekeeper
│   └── mcp-sdk/                    # MCP Client & Server host wrapper
├── mcp-servers/                    # Built-in Native Tool Servers
│   ├── filesystem/                 # Sandboxed workspace file tools
│   └── terminal/                   # Sandboxed terminal command execution
└── tests/                          # Monorepo integration test suite
```

---

## Folder Ownership & Module Rules

- **`apps/desktop`**: Owns UI presentation and OS integration. Contains NO domain memory or LLM routing logic.
- **`packages/core`**: Owns model orchestration, task planning, and tool dispatching.
- **`packages/memory`**: Owns database schemas, vector indexing, and memory retrieval algorithms.
- **`packages/security`**: Owns capability token validation and permission prompts.
- **`mcp-servers/*`**: Standalone tool processes exposing JSON-RPC 2.0 endpoints over stdio.
