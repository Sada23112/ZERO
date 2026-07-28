# PROJECT_STRUCTURE.md — Repository Layout & Module Boundaries

This document defines the monorepo directory layout for Project ZERO.

```
zero/
├── AGENTS.md                       # Primary AI developer instructions
├── MANIFESTO.md                    # Constitution & core philosophy
├── ARCHITECTURE.md                 # High-level architecture guide
├── ROADMAP.md                      # Living 10-phase engineering roadmap
├── DECISIONS.md                    # Architecture Decision Record (ADR) log
├── SECURITY.md                     # Security & permission specifications
├── CODING_STANDARD.md              # Detailed coding guidelines
├── pnpm-workspace.yaml             # Master TypeScript workspace configuration
├── package.json                    # Root scripts and workspace settings
├── apps/                           # End-User Applications
│   ├── desktop/                    # Tauri + React desktop system tray overlay
│   ├── mobile/                     # Android Flutter companion client (Phase 9)
│   └── cli/                        # Terminal CLI harness (`zero-cli`)
├── packages/                       # Shared Core TypeScript Libraries
│   ├── core/                       # Model Router, Task Engine & Execution Loop
│   ├── memory/                     # SQLite WAL, Qdrant Vector & Graph interfaces
│   ├── security/                   # Capability Tokens & Permission Gatekeeper
│   └── mcp-sdk/                    # MCP Client & Server host wrapper
├── mcp-servers/                    # Built-in Native Tool Servers
│   ├── filesystem/                 # Sandboxed workspace file tools
│   ├── terminal/                   # Sandboxed terminal command execution
│   ├── browser/                    # Playwright browser automation
│   └── desktop-automation/         # GUI screen grounding & mouse/keyboard
└── docs/                           # Extended technical specs & engineering reports
```

---

## Folder Ownership & Module Rules

- **`apps/desktop`**: Owns UI presentation and Tauri OS integration. Contains NO domain memory or LLM routing logic.
- **`packages/core`**: Owns model orchestration, task planning, and tool dispatching.
- **`packages/memory`**: Owns database schemas, vector indexing, and memory retrieval algorithms.
- **`packages/security`**: Owns capability token validation and permission prompts.
- **`mcp-servers/*`**: Standalone tool processes exposing JSON-RPC 2.0 endpoints over stdio.
