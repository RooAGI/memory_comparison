# CogniCore

## Identity and review pin

- **Catalog position:** 136, “CogniCore”; slug `cognicore`.
- **Listed repository:** [cognicore-dev/cognicore-env](https://github.com/cognicore-dev/cognicore-env); roster locator status is explicit. The pinned Atlas roster entry is recorded only for identity and locator attribution.
- **Canonical upstream:** public GitHub repository [cognicore-dev/cognicore-env](https://github.com/cognicore-dev/cognicore-env), default branch `main`. The official [main commits feed](https://github.com/cognicore-dev/cognicore-env/commits/main.atom) reports full head `44d06d2dde6ad1a637b169cb3133a291c572a019`, updated 2026-11-24T07:19:40Z. `git ls-remote` resolved remote HEAD and `refs/heads/main` to that SHA; a shallow checkout matched.
- **Reviewed:** 2026-11-25 08:38:19 UTC (2026-11-25 00:38:19 PST; America/Los_Angeles).
- **Status:** Reviewed from current pinned upstream source and documentation. Benchmark not run.

## Summary

CogniCore is a local-first session handoff and memory toolkit for Claude Code and Codex, with a SQLite memory SDK and MCP routes. Its hooks capture a project-scoped handoff, resume it within a token budget, and expose overflow details to search. This is a source review; no CogniCore runtime, tests, or benchmark workloads were run.[[Official README](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/README.md)] [[Reviewed commit](https://github.com/cognicore-dev/cognicore-env/commit/44d06d2dde6ad1a637b169cb3133a291c572a019)]

## Who and what

The official README presents CogniCore as local-first session memory for Claude Code and Codex. It documents automatic hook capture and resume, optional hosted sync, MCP tools, and a Python SDK. This review does not infer individual maintainer identity.[[README](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/README.md)]

The reviewed catalog position is 136, with “CogniCore,” slug `cognicore`, and the explicit listed repository locator. The pinned Atlas entry is retained only for roster attribution, not assessment evidence.[[Curated catalog](../data/memory-systems.json)] [[Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cognicore.md)]

## Architecture and data model

The primary handoff is a versioned JSON document (`cognicore.handoff/v1`) containing the goal, current state, completed work, decisions, open tasks, key facts, exact values, files, code, environment, and provenance. The default extraction uses rules without an LLM call, redacts detected secrets, deduplicates repeated statements, and selects content under a token budget.[[handoff implementation](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/handoff.py)] [[session capture](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/context_preservation.py)]

The local integration stores sessions, handoff JSON, and searchable memory rows in SQLite. A `MemoryEntry` carries text/category, scope and scope ID, session/sequence identifiers, confidence and lifecycle state, source component/agent/task fields, and supersession/invalidation links. SQLite maintains an FTS5 index with triggers for inserts, updates, and deletes; an embedding provider is optional.[[entry model](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/base.py)] [[SQLite backend](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/sqlite_backend.py)]

Hooks save at Stop, PreCompact, and SessionEnd and build a project brief at SessionStart. The Python SDK also exposes lower-level memory backends and structured experiences; the local MCP server provides memory tools including recall.[[hooks](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/hooks.py)] [[experience retrieval](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/experience/retrieval.py)] [[MCP server](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/mcp/server.py)]

## Write, update, delete, and retrieval

**Write.** The session save path builds a handoff from transcript content or an agent-supplied handoff, redacts detected secrets, derives a project key, stores searchable rows, and links exact statements already present rather than copying them. Identical content can return an existing session; repeated saves using a session key update that session.[[session save](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/context_preservation.py)] [[handoff extraction](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/handoff.py)]

**Update.** The SQLite backend exposes field updates for lifecycle, confidence, utility, source metadata, and supersession/invalidation fields. Session saves can update an existing session. The inspected generic entry API does not provide a content-correction history; the mutation fields do not establish that every writer preserves an audit trail.[[SQLite update](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/sqlite_backend.py)] [[entry model](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/base.py)] [[session save](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/context_preservation.py)]

**Delete.** SQLite hard-deletes a memory row by entry ID, and a database trigger removes the FTS entry. The inspected code does not establish end-to-end erasure from hosted sync, exports, backups, or every other store.[[SQLite delete](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/sqlite_backend.py)] [[session storage](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/context_preservation.py)]

**Retrieval.** SQLite search uses FTS5 prefix matching and a BM25 fallback. With an embedding provider, it evaluates a bounded candidate set and combines semantic similarity with normalized BM25. General search filters archived/deleted states and accepts category, scope, scope ID, and metadata filters. Experience retrieval also filters invalidated or incompatible records and can require verified states.[[SQLite search](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/sqlite_backend.py)] [[experience retrieval](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/experience/retrieval.py)]

The local MCP `cognicore_recall` tool accepts query, category, and top_k, but no project or scope argument. Its category-only fallback calls `get_by_category`, which does not apply the active/deleted state filter used by search. This finding applies to the inspected call path; other integrations may use different paths.[[MCP recall](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/mcp/server.py)] [[SQLite category and search methods](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/sqlite_backend.py)]

## Scope isolation

Session-start briefs derive a normalized project key from the repository root, or the starting folder outside a repository. SDK searches accept scope and scope ID filters. The local MCP recall tool does not pass these filters, so scope separation is caller-dependent across integrations; source review does not establish isolation for every path or deployment.[[project key and resume](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/context_preservation.py)] [[hook integration](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/hooks.py)] [[SQLite scope filters](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/sqlite_backend.py)] [[MCP recall](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/mcp/server.py)]

## Provenance and evidence

Entries can record creation reason, source component, source agent/task, session ID, sequence ID, confidence, and supersession or invalidation references. Handoff provenance records session metadata such as agent/client and timestamps. Structured experiences can retain verification evidence; the gate checks that each record has a command, zero exit code, and timestamp, but it does not execute commands or independently verify the supplied evidence.[[entry model](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/base.py)] [[handoff and session save](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/handoff.py)] [[verification gate](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/experience/verification.py)] [[hosted verification input](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/connectors/remote.py)]

## Efficiency and observability

The session saver batches rows and links duplicate statements; resume selects a bounded brief and leaves overflow searchable. SQLite uses FTS5 and can optionally use embeddings. The memory backend publishes store and search events to registered observers, while the local MCP server keeps in-process stored/recalled counters. These are source-level hooks, not measured latency or durable telemetry. The brief has a configurable token budget; the README documents a 700-token default. No latency, token, cost, or storage efficiency measurements were collected.[[session save and resume](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/context_preservation.py)] [[SQLite backend](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/sqlite_backend.py)] [[memory event bus](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/events.py)] [[MCP counters](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/mcp/server.py)] [[README](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/README.md)]

## Metric-domain evidence

- **Answerable recall and abstention:** retrieval paths are source-visible; quality and abstention were not measured.
- **Correction and stale values:** update and supersession fields are source-visible; no correction sequence was run.
- **Deletion leakage:** a local hard-delete path exists; no post-delete probes or residual-copy check were run.
- **Scope isolation:** hooks use a project key and SDK search accepts scope filters; local MCP recall has no scope argument. No isolation workload was run.
- **Evidence support and citation coverage:** source metadata and experience evidence exist; the verification gate validates supplied fields but does not execute the command. No claim-to-source adjudication was run.
- **Latency:** no latency workload was measured.
- **Write-to-recall delay:** no scheduled first-correct-recall measurement was collected.
- **Tokens and cost:** the handoff uses a token budget and its default extraction is rule-based; no token or provider cost was measured.
- **Storage efficiency:** SQLite rows, FTS index, sessions, and optional embeddings are visible in source; persistent bytes were not measured.

The project’s metric definitions are in [METRICS.md](../METRICS.md), the shared execution record is [initial-baselines-status.json](../results/initial-baselines-status.json), and the [benchmark fixture](../fixtures/memory-benchmark-v1.json) specifies a planned workload rather than a result.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Contact

The official [CogniCore website](https://www.cognicoree.tech/) publishes `contact@cognicoree.tech` in its organization metadata. The official pinned [README](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/README.md) was also checked; no contact email is published there.

## Limits and unknowns

Scope behavior depends on the caller. The hook-based session brief uses a project key, and SDK searches can apply scope filters, but local MCP recall does not accept a scope key; its category fallback also bypasses the state filter. The source review does not establish isolation across every integration or deployment.[[hooks](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/hooks.py)] [[SQLite search](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/sqlite_backend.py)] [[MCP recall](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/mcp/server.py)]

Experience verification checks metadata on evidence supplied by the agent and does not run the named command. A structurally valid record therefore does not establish that an independent test ran or that its output supports the experience.[[verification gate](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/experience/verification.py)] [[hosted verification input](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/connectors/remote.py)]

Hard deletion from local SQLite is not proof of deletion from hosted sync, other databases, backups, or storage remnants. Those paths and retention behavior were not fully audited. This review selected current README, handoff, hook, SQLite, experience, and MCP sources at the verified main head; it did not audit every adapter, hosted route, storage backend, or deployment configuration.[[SQLite backend](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/cognicore/memory/sqlite_backend.py)] [[README](https://github.com/cognicore-dev/cognicore-env/blob/44d06d2dde6ad1a637b169cb3133a291c572a019/README.md)] [[reviewed commit](https://github.com/cognicore-dev/cognicore-env/commit/44d06d2dde6ad1a637b169cb3133a291c572a019)]

## Benchmark status

**Benchmark not run.** No CogniCore runtime, tests, or benchmark workloads were executed. Source observations are not measured results. See [project metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and the [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs, URLs, and the roster attribution are recorded in [cognicore.json](../data/system-reviews/cognicore.json). The Atlas entry is included only for curated identity and locator attribution, not as assessment evidence.
