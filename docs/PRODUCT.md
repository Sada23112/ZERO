# PRODUCT.md — Product Definition & UX Strategy for Project ZERO

---

## 1. Product Goals
Project ZERO is designed to be software that the user naturally keeps running every day on their computer.

- **Primary Goal**: Increase the user's daily engineering output, reasoning speed, and multi-domain problem-solving capability.
- **Form Factor**: Background system daemon + desktop floating overlay (`Alt+Space`) + duplex voice interface + mobile companion app.

---

## 2. Daily Workflow & User Experience (UX) Principles

1. **Zero-Friction Access**: Pressing `Alt+Space` instantly summons ZERO over any application, IDE, CAD tool, or terminal.
2. **Context Awareness**: ZERO automatically captures active workspace files, screen context, or selected text upon activation.
3. **Proactive Background Notifications**: The background daemon (`zerod`) notifies the user via desktop toast or audio when background builds, research crawls, or scheduled timers complete.

---

## 3. Product Scope: What ZERO Is vs. What ZERO Is Not

### Included Features (Phase 1–5 Scope)
- Global hotkey system overlay (`Alt+Space`).
- Persistent project memory & conversation history.
- Local MCP filesystem and terminal execution harness.
- Deep research web crawling & synthesis generator.
- Real-time streaming duplex voice chat.

### Excluded Non-Features (Do Not Implement Initially)
- Generic conversational chatbot widgets or social media plugins.
- Automatic cloud server auto-scaling or infrastructure provisioning.
- Public peer-to-peer open mesh networks.
- Custom model weight fine-tuning pipelines.

---

## 4. The Essentiality Filter

Before adding any feature, ask:
> **"If this feature disappeared tomorrow, would the user genuinely miss it during daily engineering work?"**
If the answer is NO, exclude the feature.

---

## 5. Success Metrics
- **Daily Active Usage**: Triggered > 10 times/day for real engineering work.
- **Context Accuracy**: > 95% precision on retrieving past project decisions and preferences.
- **Tool Reliability**: 0 crashes due to malformed tool call schemas.
