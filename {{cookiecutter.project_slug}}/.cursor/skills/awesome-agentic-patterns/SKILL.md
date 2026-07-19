---
name: awesome-agentic-patterns
description: >-
  Fetches the latest agentic AI patterns from nibzard/awesome-agentic-patterns
  and agentic-patterns.com when designing, building, or reviewing agentic
  applications. Use when implementing multi-agent systems, agent orchestration,
  memory/context strategies, tool routing, feedback loops, reliability/evals,
  agent security, or any agentic product architecture.
---

# Awesome Agentic Patterns

## Overview

[awesome-agentic-patterns](https://github.com/nibzard/awesome-agentic-patterns) is a curated catalogue of production agentic AI patterns. The catalogue changes frequently — **always fetch the latest** rather than relying on memorized or previously pasted content.

## When to Use

- Designing or building an agentic application
- Multi-agent orchestration, sub-agent spawning, planner/worker splits
- Agent memory, context packing, or progressive disclosure
- Tool routing, MCP/tool gateway design
- Agent reliability, evals, guardrails, or security
- Reviewing whether an agent architecture matches known patterns

## Process

1. **Always fetch fresh** — do not recommend patterns from memory alone.
2. **Primary index** — fetch [https://agentic-patterns.com/llms.txt](https://agentic-patterns.com/llms.txt) (LLM-optimized categories and selection guidance).
3. **Deep dive** — for selected patterns, fetch the matching file under [patterns/](https://github.com/nibzard/awesome-agentic-patterns/tree/main/patterns) or the corresponding page on [agentic-patterns.com](https://agentic-patterns.com).
4. **Optional discovery** — if the use case is ambiguous, use the site Decision Explorer / Pattern Packs.
5. **Apply** — map **1–3** relevant patterns to the current design; cite pattern names and source URLs.
6. **Compose** — combine with lifecycle skills (`spec-driven-development`, `api-and-interface-design`, `security-and-hardening`, etc.); this skill does not replace them.

## Categories (orientation only — confirm via live fetch)

- Context & Memory
- Feedback Loops
- Learning & Adaptation
- Orchestration & Control
- Reliability & Eval
- Security & Safety
- Tool Use & Environment
- UX & Collaboration

## Sources

| Priority | URL |
|----------|-----|
| 1 | https://agentic-patterns.com/llms.txt |
| 2 | https://github.com/nibzard/awesome-agentic-patterns |
| 3 | https://agentic-patterns.com |

## Verification

- [ ] Fetched `llms.txt` or GitHub in this session (not memory-only)
- [ ] Cited 1–3 named patterns with sources
- [ ] Combined with the appropriate lifecycle skills for implementation
