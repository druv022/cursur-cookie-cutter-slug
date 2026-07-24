---
name: graphify
description: Build and query a persistent knowledge graph of this codebase. Use for architecture questions, file relationships, data flow, cross-module connections, or when graphify-out/graph.json exists.
---

# graphify

Turn this project's code and docs into a queryable knowledge graph under `graphify-out/`.

## Install

```bash
./scripts/install-graphify.sh
```

Requires `uv` (preferred) or `pip`. Optional: set `GEMINI_API_KEY` or `GOOGLE_API_KEY` for semantic extraction on docs (`pip install 'graphifyy[gemini]'`).

## Build

**First time (full graph):**

```bash
make graph
# or: graphify extract .
```

In Cursor Agent chat you can also say **use graphify** or **/graphify** — the agent runs the full pipeline (AST + semantic extraction).

**After code changes (cheap AST-only refresh):**

```bash
make graph-update
# or: graphify update .
```

## Query

When `graphify-out/graph.json` exists, prefer graph traversal over reading the whole repo:

```bash
make graph-query QUERY="How does the main entry point work?"
graphify query "What calls main?"
graphify path "AuthModule" "Database"
graphify explain "main"
```

Open `graphify-out/graph.html` in a browser for the interactive view. Read `graphify-out/GRAPH_REPORT.md` for community labels and surprising connections.

## Outputs (gitignored)

| File | Purpose |
|------|---------|
| `graphify-out/graph.json` | Raw graph data |
| `graphify-out/graph.html` | Interactive visualization |
| `graphify-out/GRAPH_REPORT.md` | Audit report with communities |
| `graphify-out/cache/` | Extraction cache for `--update` |

## Agent workflow

1. If `graphify-out/graph.json` exists and the user asks about the codebase → run `graphify query "<question>"` first.
2. After editing `.py`, `.sh`, or other code in the session → run `graphify update .`.
3. If no graph exists and the user wants one → run `./scripts/install-graphify.sh` then `make graph` or the full `/graphify` pipeline.
4. Cite `source_file` / `source_location` from query results when stating facts.
