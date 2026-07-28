# AGENTS.md — Primary AI Developer Guidelines for Project ZERO

> **Mandatory Read**: Every AI coding agent and human contributor MUST read and follow this document before making changes to Project ZERO.

---

## 1. Project Overview & Vision

**Project ZERO** is a Personal Autonomous Intelligence Platform designed to serve as a lifelong engineering partner across software, electronics, robotics, embedded firmware, CAD, and academic research.

- **Mission**: ZERO exists to continuously increase the user's ability to think, learn, design, invent, engineer, and create.
- **Identity**: ZERO is not a chatbot or ephemeral assistant. It is a persistent cognitive operating system.

---

## 2. ZERO'S Prime Directive

1. **User Sovereignty & Empowerment**: ZERO exists to empower the user, not replace human intellect.
2. **Absolute Honesty & Transparency**: ZERO never fakes data, hides errors, or hallucinates tool outputs. If uncertain, ZERO states confidence bounds and shows evidence.
3. **Autonomy vs. Consent Balance**:
   - **Autonomous (Silent Auto-Approve)**: Isolated read-only workspace operations, local memory indexing, unit test execution.
   - **Interactive User Consent Required**: File deletions, network requests, terminal commands outside workspace, credential access, git pushes.
4. **Long-Term System Integrity**: Reject quick hacks. Every change must be modular, testable, and documented.

---

## 3. Core Development & Architecture Philosophy

1. **Working Software Before Microkernel**: Phase 1 through 9 are built as a high-velocity TypeScript + Tauri application. Rust microkernel extraction occurs in Phase 10 from proven code.
2. **Vertical Slice Development**: Each phase delivers daily product utility before extracting low-level abstractions.
3. **No Unnecessary Abstraction**: Do not introduce interfaces or layers until a second implementation actually requires them.
4. **Single Source of Truth**: State lives in explicit SQLite database tables and Qdrant vector indices, never in opaque global variables.

---

## 4. Module Boundaries & Dependency Rules

```
[Clients: Tauri Desktop / CLI / Mobile] 
          ↓ JSON-RPC / IPC
[User-Space Engines: Coder / Researcher / Voice / Learner]
          ↓ System Calls / Event Bus
[Core Runtime: Model Router / Security Manager / Memory Subsystem / Tool Harness]
          ↓ Data Adapters
[Storage & Hardware: SQLite / Qdrant / Local LLMs / OS APIs]
```

- **Rule 1**: Clients NEVER call storage engines directly. All calls route through the Core Runtime.
- **Rule 2**: User-space specialist engines are isolated modules communicating strictly via typed interfaces.
- **Rule 3**: Tools must be registered via the Model Context Protocol (MCP) interface.

---

## 5. Rules for Autonomous Changes vs. User Approval

### Autonomous Execution Permitted
- Reading workspace files and code symbol parsing.
- Executing unit tests inside local workspace.
- Querying local vector databases or memory caches.
- Drafting documentation and markdown specs.

### Mandatory User Approval Required
- Modifying files outside the active workspace.
- Executing `rm -rf`, `sudo`, or destructive terminal commands.
- Transmitting data to external network endpoints (outside configured cloud AI APIs).
- Accessing or decrypting environment secrets.

---

## 6. Definition of Done (DoD) Checklist

Before marking any task as complete, an AI agent must verify:
- [ ] Code builds without errors or warnings (`pnpm build`).
- [ ] Unit tests pass with clean exit codes (`pnpm test`).
- [ ] No hardcoded API keys or environment secrets in source code.
- [ ] All new functions and public types have clear TSdoc/Rustdoc comments.
- [ ] Architecture decisions updated in `DECISIONS.md` if design changed.
- [ ] Memory and security constraints enforced per `SECURITY.md`.
