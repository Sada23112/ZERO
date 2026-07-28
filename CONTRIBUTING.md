# CONTRIBUTING.md — Contributor Guidelines for Project ZERO

This document outlines the workflow and quality guidelines for human developers and AI coding agents contributing to Project ZERO.

---

## 1. Code Contribution Workflow

1. **Read Core Docs**: Before modifying code, review `AGENTS.md`, `MANIFESTO.md`, and `SECURITY.md`.
2. **Create a Feature Branch**: Branch names should follow `feature/phaseX-feature-name` or `fix/issue-description`.
3. **Follow Coding Standards**: Strictly adhere to `CODING_STANDARD.md` (strict TypeScript typing, no implicit any, error handling).
4. **Run Verification Commands**:
   ```bash
   pnpm lint
   pnpm test
   pnpm build
   ```
5. **Submit Pull Request**: PRs must pass all automated CI checks and include clear descriptions of changes, testing evidence, and documentation updates.

---

## 2. Rules for AI Agents

- **No Hallucinated Imports**: Never introduce third-party npm dependencies without explicit justification.
- **Preserve Documentation**: Do not delete existing comments or TSdoc annotations.
- **Architectural Approval**: Any pull request that alters subsystem boundaries or API interfaces must update `DECISIONS.md`.
