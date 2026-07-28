# SECURITY.md — Security Architecture & Threat Model for Project ZERO

This document details the permission model, sandboxing strategy, threat vectors, and user consent gates for Project ZERO.

---

## 1. Capability-Based Permission Model

ZERO enforces capability-based security. No agent or tool possesses inherent ambient authority; every action requires a cryptographically validated Capability Token.

```json
{
  "token_id": "cap_88a91f",
  "issuer": "ZERO_SecurityManager",
  "subject_agent": "CoderService",
  "scope": {
    "filesystem": { "readwrite": ["/workspace/project/*"] },
    "tools": ["mcp_filesystem_*", "mcp_terminal_run_build"]
  },
  "expires_at": "2026-07-28T22:00:00Z",
  "signature_ed25519": "7f2a1b9..."
}
```

---

## 2. User Authorization Risk Level Matrix

| Level | Risk Tier | Scope | Approval Behavior |
| :--- | :--- | :--- | :--- |
| **Level 0** | **Low** | Read-only workspace files, local memory queries. | **Silent Auto-Approval**. |
| **Level 1** | **Medium** | Creating workspace files, running unit tests, git commits. | **Auto-Approved inside workspace**; logged to audit. |
| **Level 2** | **High** | Installing packages, external API calls outside LLMs. | **Transient Notification Toast** (10s cancel window). |
| **Level 3** | **Critical** | Deleting files, running `sudo`/admin commands, secret access. | **Mandatory Interactive User Consent Prompt**. |

---

## 3. Sandboxing & Runtime Isolation

1. **WASM / gVisor Sandboxing**: All user-generated code scripts and third-party dynamic tools MUST execute within **Wasmtime (WebAssembly)** or isolated gVisor containers with read-only root filesystems and loopback-only networks.
2. **Static AST Analysis**: Before dynamic scripts are evaluated, an AST scanner verifies the code contains no forbidden syscalls, raw socket generation, or environment variable dumps.
