# aios (rexleimo) source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 45 / aios (rexleimo) / rexleimo-aios  
**Listed repository locator:** [rexleimo/aios](https://github.com/rexleimo/aios)  
**Current canonical repository:** [rexleimo/aios](https://github.com/rexleimo/aios)  
**Default branch / reviewed head:** main / 79d99896bfa823249e54b008e56f93497f212367  
**Review time:** 2026-11-24 20:05:56 UTC (12:05:56 PST, America/Los_Angeles).

## Identity and scope

The curated roster identifies ordinal 45 as aios (rexleimo), slug rexleimo-aios, with the listed locator above. Its Atlas URL and revision are retained for attribution only; Atlas descriptions, marks and layout were not used as assessment evidence. The official repository page identifies main; the official main feed reports the full head 79d99896bfa823249e54b008e56f93497f212367. I checked out that exact SHA before inspecting source.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/rexleimo/aios)] [[main branch feed](https://github.com/rexleimo/aios/commits/main.atom)] [[reviewed head](https://github.com/rexleimo/aios/commit/79d99896bfa823249e54b008e56f93497f212367)]

## Summary

AIOS is a local-first control plane around existing coding clients. Its memory functionality has two parts: ContextDB stores project sessions and checkpoints for task continuity, while AIOS Memo stores durable scoped facts. The docs describe a pull model where agents search for context when needed. This is a source review, not a runtime quality or performance assessment.[[README](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/README.md)] [[ContextDB docs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/docs-site/contextdb.md)]

## Who and what

The official README describes AIOS as a local-first coding-agent control plane and identifies Rex as maintainer. ContextDB is a local project-memory component; AIOS Memo is a durable memo store. This article focuses on source-visible memory behavior.[[README](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/README.md)] [[ContextDB docs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/docs-site/contextdb.md)]

## Architecture and data model

ContextDB resolves to .aios/context-db under the project workspace by default, with an environment override and legacy location option. Each session has metadata, JSONL event and checkpoint files, state and continuity summaries. Workspace indexes and a SQLite sidecar support lookup; the sidecar contains FTS5 tables and project/session indexes and can be rebuilt from canonical files.[[paths.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/query/paths.ts)] [[core.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/store/core.ts)] [[schema.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/sqlite/tables/schema.ts)]

Session metadata includes agent, project, goal, tags, status and timestamps. Events hold role, kind, text, refs and optional turn metadata. Checkpoints hold status, summary, next actions, artifacts and optional verification, retry, elapsed-time and cost telemetry. AIOS Memo is separate: its default canonical store is append-only JSONL under .aios/memo/file/events.jsonl; split storage is optional. Memo records can include scope, provenance, refs, valid time, supersession links, entities and evidence references.[[core.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/store/core.ts)] [[ContextDB docs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/docs-site/contextdb.md)] [[events-write.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/events/events-write.mjs)]

The documented model is pull-based: project guidance locates the registry and an agent retrieves selected memos, checkpoints, events or context packs. Context packets can retain recent events, rank others against the goal and latest checkpoint, and apply an optional token budget. Documentation does not promise every client will read every source or stay under a fixed prompt size.[[ContextDB docs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/docs-site/contextdb.md)] [[core.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/store/core.ts)]

## Write, update, delete, and retrieval

**Writes and checkpoints.** Session creation writes metadata and initial state. Event append uses a per-session lock, deduplicates an identical last event within a 30-second window, appends JSONL, updates state and indexes, then best-effort updates SQLite. Checkpoint writes append a record and refresh summaries, continuity data and indexes. The SQLite sidecar is rebuildable.[[core.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/store/core.ts)] [[schema.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/sqlite/tables/schema.ts)]

Memo writes append events to JSONL or one-file-per-event split storage. Runtime authority determines claim status: an agent without shared-publish capability writing a shared memo is marked candidate. Corrections append a successor with supersedes links; the reader derives invalidation while preserving prior history. Candidate facts are excluded from ordinary recall by default.[[events-write.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/events/events-write.mjs)] [[provenance.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/govern/provenance.mjs)] [[temporal.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/govern/temporal.mjs)] [[query.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/views/query.mjs)]

**Deletion and retention.** I did not find a hard-delete operation in the inspected ContextDB session API or memo writer. The docs say a client clear leaves project files intact and removing the registry marker does not erase .aios data. Hygiene operations archive or rotate without deleting source rows; memo supersession hides old values from ordinary recall but preserves history. Erasure from backups, exports, Git history or provider context is unverified.[[core.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/store/core.ts)] [[ContextDB docs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/docs-site/contextdb.md)] [[temporal.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/govern/temporal.mjs)]

**Retrieval.** ContextDB search filters by project/session and other query fields through SQLite FTS5 BM25, with a LIKE fallback when FTS yields no rows. Session recall uses a bounded candidate set. Memo search uses token matching and BM25-style weighting, with optional entity/feedback boosts; a local embedder can widen lexical candidates. Ranking does not guarantee answerability or abstention.[[events.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/sqlite/tables/events.ts)] [[core.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/store/core.ts)] [[query.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/views/query.mjs)]

## Scope isolation

ContextDB can filter by project and session. Memo scopes include project-shared, agent-private and agent-ephemeral. Shared rows are visible across supported clients; private/ephemeral rows require a matching agent identity. Candidate inclusion is opt-in, and supersession checks scope and principal. These are source-visible filters and policy checks, not proof of isolation across every integration or filesystem boundary.[[events.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/sqlite/tables/events.ts)] [[query.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/views/query.mjs)] [[temporal.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/govern/temporal.mjs)] [[ContextDB docs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/docs-site/contextdb.md)]

## Provenance and evidence

Memo provenance can record producer/principal, agent, session/run/activation IDs, policy revision, source reference/hash and capabilities. Memos may carry refs and evidence references; ContextDB checkpoints can link artifacts and record verification, retries, elapsed time and cost. These fields support traceability but do not validate truth or citation support. The README describes run evidence as separate from agent claims.[[provenance.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/govern/provenance.mjs)] [[events-write.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/events/events-write.mjs)] [[core.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/store/core.ts)] [[README](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/README.md)]

## Source-visible efficiency and observability

The ContextDB sidecar indexes event/checkpoint text with FTS5 and maintains project/session indexes. Search has a bounded result limit and lexical fallback. Session writes persist canonical files first and treat SQLite as a best-effort rebuildable index. Memo reads use a bounded process-local parse cache keyed by file metadata, with hit/miss/eviction counters. Context packet construction tracks estimated token use and compression, truncation and drop counts when a budget applies. These are source observations, not runtime measurements.[[schema.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/sqlite/tables/schema.ts)] [[events.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/sqlite/tables/events.ts)] [[events-read.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/events/events-read.mjs)] [[core.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/store/core.ts)]

## Metric-domain evidence

All benchmark domains remain **unmeasured**. I did not run answerable/unsupported probes, correction or staleness cases, deletion checks, cross-scope probes, evidence adjudication, latency or write-to-recall timings, token/cost accounting, or storage measurements. Project metric definitions, fixture and execution status describe the separate protocol; they are not AIOS results.[[metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Contact-list follow-up

The official pinned README directs questions or feedback to GitHub issues and contains no published contact email. The structured record stores contact_email as null with that exact README URL. No profile address, commit metadata, third-party directory or inferred address was used.[[official README](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/README.md)]

## Limits and unknowns

This review covered the official README and ContextDB documentation, plus selected ContextDB session/search/schema and memo write/temporal/query/provenance/read-cache code at the verified SHA. It did not inspect every client adapter, MCP route, export, backup or provider path. No AIOS runtime, tests or benchmark workloads were run. Answer quality, complete deletion, all-path authorization and performance remain unknown; unknown means not established by this review.[[README](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/README.md)] [[ContextDB docs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/docs-site/contextdb.md)] [[core.ts](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/mcp-server/src/contextdb/store/core.ts)] [[query.mjs](https://github.com/rexleimo/aios/blob/79d99896bfa823249e54b008e56f93497f212367/scripts/lib/memory/memo/storage/views/query.mjs)]

## Benchmark status

**Benchmark not run.** No AIOS runtime, test suite or benchmark workload was run. Source and documentation observations are not measured outcomes. See the project metric definitions, execution-status record and fixture for the separate protocol.[[metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

The structured source IDs and pinned URLs are in [rexleimo-aios.json](../data/system-reviews/rexleimo-aios.json). The roster's Atlas locator is [the attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/rexleimo-aios.md); it was used only to identify the curated entry.
