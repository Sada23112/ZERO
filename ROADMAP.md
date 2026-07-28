# ROADMAP.md — Living Engineering Roadmap for Project ZERO

---

## Roadmap Overview

Project ZERO is developed across 11 vertical phases. Each phase delivers a usable product milestone.

```
Phase 0: Identity & Vision (DONE)
Phase 1: AI Companion MVP (Weeks 1-2)
Phase 2: Persistent Memory & Knowledge (Weeks 3-4)
Phase 3: Desktop & Browser Automation (Weeks 5-6)
Phase 4: Research Engine & Multi-Domain Engineering (Weeks 7-8)
Phase 5: Duplex Voice & Background Daemon (Weeks 9-10)
Phase 6: Autonomous Planning Engine (Weeks 11-12)
Phase 7: Dynamic Tool Generation & Verification (Weeks 13-14)
Phase 8: Weight-Less In-Context Learning Engine (Weeks 15-16)
Phase 9: Multi-Device P2P Synchronization (Weeks 17-18)
Phase 10: Rust Microkernel Extraction & System Hardening (Months 5-6)
```

---

## Detailed Phase Milestones & Acceptance Criteria

### Phase 0: Identity & Vision (COMPLETE)
- [x] Establish Project ZERO Manifesto, Constitution, and Architecture Specifications.
- [x] Commit `AGENTS.md`, `SKILLS.md`, `SECURITY.md`, and permanent documentation base.

### Phase 1: AI Companion MVP (Target: Day 14)
- [ ] Tauri Desktop System Tray App with floating overlay (`Alt+Space`).
- [ ] Gemini API Model Router integration.
- [ ] Local MCP filesystem (`read_file`, `write_file`, `edit_file`) and terminal tools.
- [ ] Local SQLite episodic chat storage (`zero.db`).
- **Completion Criterion**: User uses `Alt+Space` daily for workspace coding assistance.

### Phase 2: Persistent Memory & Knowledge Engine
- [ ] SQLite FTS5 + Qdrant vector store hybrid search integration.
- [ ] Automated project workspace indexing (README, git logs, code symbols).
- [ ] Personal preference and coding style persistence.
- **Completion Criterion**: ZERO retains user preferences and project structures across app restarts without re-prompting.

### Phase 3: Desktop Integration & Browser Automation
- [ ] Screen capture & accessibility tree grounding tool.
- [ ] Playwright headless browser control host.
- [ ] Clipboard context auto-injection on hotkey trigger.
- **Completion Criterion**: ZERO can inspect active UI errors, crawl web documentation, and test web apps autonomously.

### Phase 4: Research Engine & Multi-Domain Engineering
- [ ] Deep research multi-query generator and report synthesis engine.
- [ ] Multi-domain adapters: KiCad PCB schematics, OpenSCAD/STEP CAD models, ROS2 node architectures.
- **Completion Criterion**: ZERO generates cited research papers and parses hardware PCB/CAD files correctly.

### Phase 5: Duplex Voice & Background Daemon
- [ ] Real-time Whisper STT + Kokoro/ElevenLabs streaming TTS overlay.
- [ ] System background service (`zerod`) with cron and terminal build monitors.
- **Completion Criterion**: User can talk hands-free to ZERO and receive audio alerts when background jobs finish.

### Phase 6: Autonomous Planning Engine
- [ ] Directed Acyclic Task Graph (DAG) generator with pre/post-conditions.
- [ ] Observation assessor & dynamic plan replanner.
- **Completion Criterion**: ZERO executes multi-step plans autonomously, recovering automatically from tool errors.

### Phase 7: Dynamic Tool Generation & Verification
- [ ] Capability gap detector and TypeScript MCP tool synthesizer.
- [ ] Sandbox test runner verifying generated tools against synthetic unit tests.
- **Completion Criterion**: ZERO automatically generates, tests, and installs missing tools when encountering new file formats.

### Phase 8: Weight-Less In-Context Learning Engine
- [ ] Trajectory post-mortem failure miner and system rule generator.
- [ ] Reusable workflow macro generator.
- **Completion Criterion**: ZERO automatically stops making past errors and executes multi-step workflows as single-step macros.

### Phase 9: Multi-Device P2P Sync
- [ ] Android Flutter companion client app.
- [ ] Encrypted P2P CRDT memory synchronization (Automerge/Yjs).
- **Completion Criterion**: ZERO state synchronizes seamlessly across desktop and phone with end-to-end encryption.

### Phase 10: Rust Microkernel Extraction
- [ ] Extract microkernel IPC, scheduler, capability token security, and memory manager into Rust (`zero-kernel`).
- [ ] Enforce Ed25519 Capability Tokens for sandbox isolation.
- **Completion Criterion**: Idle RAM footprint drops below 50MB with microsecond IPC latency and production security hardening.
