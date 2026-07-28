# Project ZERO — Personal Autonomous Intelligence Platform

> **Mission**: Project ZERO exists to continuously increase my ability to think, learn, design, invent, engineer, and create.

---

## 🏛️ Architecture Overview

Project ZERO is an autonomous AI companion and cognitive system built on a Python-first modular architecture.

```
ZERO/
├── docs/                 # Architectural specs, manifestos, ADRs, & research reports
├── core/                 # Engine lifecycle, execution orchestration, capability security
├── agents/               # Autonomous agent workflows & multi-agent capability roles
├── brain/                # Context window engineering, prompt composition, & synthesis
├── memory/               # Persistent SQLite episodic memory & vector key-value storage
├── planner/              # Multi-step goal decomposition & task graph execution
├── tools/                # Tool definitions (Filesystem, Terminal, Web search, MCP)
├── providers/            # Provider integration layer (Google Gemini API & fallback LLMs)
├── config/               # System configuration & environment loader (.env)
├── tests/                # Pytest automated test suite
├── scripts/              # Setup, diagnostic scripts, & CLI utilities
├── data/                 # Local persistent data storage (zero.db)
├── main.py               # Application entrypoint
├── requirements.txt      # Python dependencies
└── pyproject.toml        # Package manifest
```

---

## 📄 Documentation

All permanent architectural documentation and vision manifests are maintained in the [`docs/`](file:///d:/this%20is%20me/docs) directory:

- [`docs/AGENTS.md`](file:///d:/this%20is%20me/docs/AGENTS.md) — Constitution for AI agents working on ZERO.
- [`docs/MANIFESTO.md`](file:///d:/this%20is%20me/docs/MANIFESTO.md) — Identity, philosophy, and engineering values.
- [`docs/ARCHITECTURE.md`](file:///d:/this%20is%20me/docs/ARCHITECTURE.md) — Technical system design.
- [`docs/ROADMAP.md`](file:///d:/this%20is%20me/docs/ROADMAP.md) — Milestone execution plan.
- [`docs/DECISIONS.md`](file:///d:/this%20is%20me/docs/DECISIONS.md) — Architecture Decision Records (ADRs).
- [`docs/UX_RESEARCH_REPORT.md`](file:///d:/this%20is%20me/docs/UX_RESEARCH_REPORT.md) — Research study of developer tools and desktop UX.
