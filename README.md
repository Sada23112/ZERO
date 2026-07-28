# Project ZERO

**Personal Autonomous Intelligence Platform & Lifelong Engineering Partner**

---

## Documentation

All architectural specifications, project manifestos, agent guidelines, and engineering handbooks are located in the [docs/](file:///d:/this%20is%20me/docs) directory:

- [docs/AGENTS.md](file:///d:/this%20is%20me/docs/AGENTS.md) — Primary AI developer guidelines & prime directive
- [docs/MANIFESTO.md](file:///d:/this%20is%20me/docs/MANIFESTO.md) — The Project ZERO constitution & core philosophy
- [docs/PRODUCT.md](file:///d:/this%20is%20me/docs/PRODUCT.md) — Product scope & essentiality filter
- [docs/ARCHITECTURE.md](file:///d:/this%20is%20me/docs/ARCHITECTURE.md) — High-level architecture & vertical slice strategy
- [docs/ROADMAP.md](file:///d:/this%20is%20me/docs/ROADMAP.md) — 10-phase living engineering roadmap
- [docs/DECISIONS.md](file:///d:/this%20is%20me/docs/DECISIONS.md) — Architecture Decision Records (ADRs)
- [docs/SECURITY.md](file:///d:/this%20is%20me/docs/SECURITY.md) — Capability tokens & security matrix
- [docs/SKILLS.md](file:///d:/this%20is%20me/docs/SKILLS.md) — Technical mastery handbook
- [docs/CODING_STANDARD.md](file:///d:/this%20is%20me/docs/CODING_STANDARD.md) — Coding standards & error handling

---

## Monorepo Layout

- `apps/desktop` — Desktop overlay app (Tauri/Electron + React + TypeScript)
- `packages/core` — Model router & task engine
- `packages/memory` — SQLite WAL & FTS memory engine
- `packages/security` — Capability permission gatekeeper
- `mcp-servers/` — Native MCP tool hosts (Filesystem & Terminal)
