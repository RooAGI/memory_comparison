# BitterBot Desktop source review

## Identity and review pin

- **Curated ordinal:** 95
- **Listed name / slug:** BitterBot Desktop / `bitterbot-desktop`
- **Listed repository locator:** https://github.com/Bitterbot-AI/bitterbot-desktop
- **Canonical repository:** https://github.com/Bitterbot-AI/bitterbot-desktop
- **Default branch:** `main`
- **Reviewed head:** [`a0d01b11fae1a73c482f95d00ab4f8df251d737d`](https://github.com/Bitterbot-AI/bitterbot-desktop/commit/a0d01b11fae1a73c482f95d00ab4f8df251d737d)
- **Reviewed at:** 2026-11-25 00:04:35 UTC (2026-11-24 16:04:35 PST; America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The roster establishes the ordinal, listed name and locator, and attribution to [the pinned Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/bitterbot-desktop.md) for identity only. Atlas descriptions, marks, and layout were not assessment evidence. The official repository page identifies `main` and displays latest commit prefix `a0d01b1`; the official `main` Atom feed gives full head `a0d01b11fae1a73c482f95d00ab4f8df251d737d`, matching that prefix.[[roster](../data/memory-systems.json)][[repository](https://github.com/Bitterbot-AI/bitterbot-desktop)][[main history](https://github.com/Bitterbot-AI/bitterbot-desktop/commits/main.atom)][[reviewed head](https://github.com/Bitterbot-AI/bitterbot-desktop/commit/a0d01b11fae1a73c482f95d00ab4f8df251d737d)]

## Summary

Bitterbot Desktop is a local-first personal agent whose memory combines searchable conversation and file chunks, canonical facts, and a knowledge graph in SQLite. The observations here come from selected upstream source and documentation at the reviewed revision; the application was not run.[[README](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/README.md)][[architecture overview](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/docs/memory/architecture-overview.md)]

## Who and what

The official README describes an open-source personal agent designed for the owner's hardware, with memory and identity stored locally. It names Victor Michael Gil as a builder and community contributors. Bitterbot is an agent application with an integrated local memory subsystem, rather than a standalone hosted memory service. No additional maintainer identity is inferred.[[README](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/README.md)][[memory architecture](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/docs/memory/architecture-overview.md)]

## Architecture and data model

**Code observation.** The manager indexes source files and conversation sessions into chunk rows and embeddings. The SQLite schema includes files, chunks, an embedding cache, FTS5 tables when available, and a sqlite-vec vector table managed by the memory manager. Migrations add canonical facts, retrieval traces, audit logs, and graph and dream stores.[[schema](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/memory-schema.ts)][[manager](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/manager.ts)][[migrations](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/migrations.ts)]

A chunk can carry its source and path, line range, text hash, embedding model, lifecycle state, importance and access metadata, and evidence references. The canonical ledger is a separate keyed store with a value, trust source, scope, confidence, validity window, status, and evidence pointers. Graph relationships retain their own validity and supporting chunk IDs.[[schema](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/memory-schema.ts)][[canonical facts](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/canonical-facts.ts)][[knowledge graph](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/knowledge-graph.ts)]

The design combines similarity-gated archival chunks with exact-key facts that can enter the prompt independently of fuzzy retrieval. The documented architecture also describes dream-time consolidation and other retrieval lanes. Their presence in source does not show how often each contributes in a deployed run.[[architecture overview](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/docs/memory/architecture-overview.md)][[canonical facts](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/canonical-facts.ts)][[retrieval trace](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/retrieval-trace.ts)]

## Write, update, delete, and retrieval

**Write — code observation.** File and session indexing creates chunk records and index entries; the manager also maintains an embedding cache and pending-embedding backfill path. Canonical `memory_pin` writes reconcile by a closed set: add, strengthen a same-value fact, supersede a changed value, or reject. Source trust tiers put owner pins above agent pins and background extraction or research.[[manager](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/manager.ts)][[schema](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/memory-schema.ts)][[canonical facts](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/canonical-facts.ts)]

**Update and correction — code observation.** An owner edit plans a forget cascade and creates a replacement memory. Memories indexed from source files and frozen skills are read-only in these controls; transcript memories can be forgotten instead of edited. A changed canonical value closes the previous fact's validity interval and adds a successor, preserving history.[[owner controls](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/owner-controls.ts)][[forget cascade](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/forget-cascade.ts)][[canonical facts](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/canonical-facts.ts)]

**Delete and forgetting — code observation.** Owner forget applies a dependency-aware cascade, records suppressions so reindexing does not restore the same text, and writes an audit event that omits the memory text. Consolidation marks decayed chunks forgotten or merged chunks archived with a parent; a later retention purge removes the chunk and its vector and FTS rows. Canonical facts are normally retired or superseded as history rather than erased by reconciliation.[[owner controls](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/owner-controls.ts)][[forget cascade](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/forget-cascade.ts)][[consolidation](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/consolidation.ts)][[canonical facts](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/canonical-facts.ts)]

**Retrieval — code observation.** Search combines sqlite-vec vector candidates with FTS5/BM25 keyword results and hybrid fusion; the manager also coordinates graph and canonical-fact paths. The vector helper over-fetches a bounded candidate set before filtering by model and source. Without sqlite-vec, the fallback loads matching chunks and scores their stored embeddings in process. Active canonical facts may be rendered by key, separate from similarity-gated chunks.[[search helpers](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/manager-search.ts)][[manager](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/manager.ts)][[canonical facts](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/canonical-facts.ts)]

**Scope observation.** The documented primary deployment is a local database for one owner's agent. Canonical facts support `global`, `project:<name>`, and `person:<name>` scopes, with project facts gated by the active project. Guest access uses a separate sensitivity and path policy; the inspected code does not establish a general multi-tenant namespace or prove cross-user isolation.[[README](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/README.md)][[canonical facts](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/canonical-facts.ts)][[manager](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/manager.ts)][[owner controls](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/owner-controls.ts)]

**Provenance and evidence — code observation.** Chunks can hold typed evidence references; canonical facts retain evidence chunk IDs and an optional source reference; graph edges retain evidence chunk IDs. Owner and consolidation paths write selected audit events, while retrieval traces store layer counts rather than query text. Audit writes are spread among callers, so the log is not evidence of complete mutation coverage.[[schema](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/memory-schema.ts)][[canonical facts](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/canonical-facts.ts)][[knowledge graph](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/knowledge-graph.ts)][[owner controls](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/owner-controls.ts)][[retrieval trace](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/retrieval-trace.ts)]

**Source-visible efficiency and observability.** SQLite and local vector/keyword indexes avoid a retrieval network hop; the manager includes embedding caching and indexed lookups. The vector helper asks for at least 50 or four times the requested limit before applying its model/source filter. Consolidation caps pairwise merge candidates at 500 and yields periodically, with live chunk loading in batches of 50. Retrieval traces are best-effort and sampled at a default 5%; a contribution monitor can warn when a lane stays inactive while others are active. These are source observations, not measured latency or cost.[[architecture overview](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/docs/memory/architecture-overview.md)][[search helpers](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/manager-search.ts)][[consolidation](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/consolidation.ts)][[retrieval trace](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/retrieval-trace.ts)]

## Metric-domain evidence

The implementation supports the following source observations. The project-level metrics remain **unmeasured** for this review:

| Domain | Source observation | Measurement |
|---|---|---|
| Answerable recall and abstention | Vector/keyword search and exact-key canonical lookup exist. | No answerable or unanswerable probes run. |
| Correction accuracy and stale values | Canonical supersession retains validity history; owner edit replaces a selected chunk. | No correction adjudication run. |
| Deletion leakage | Forget cascades, suppressions, and delayed index purge are visible. | No post-delete retrieval probes run. |
| Scope isolation | Canonical scopes and project visibility checks exist in source. | No cross-scope or adversarial isolation probes run. |
| Evidence support and citation coverage | Chunk, fact, and graph evidence pointers exist. | No answer-level evidence adjudication run. |
| Retrieval latency and write-to-recall delay | Bounded search and batching plus sampled traces are implemented. | No runtime timings gathered. |
| Tokens and cost | Not established by this source inspection. | No token or provider-cost measurements gathered. |
| Storage efficiency | SQLite schema and index structure inspected. | No database or index size measured. |

See the project's [metric definitions](../METRICS.md), [benchmark status record](../results/initial-baselines-status.json), and [fixture/protocol](../fixtures/memory-benchmark-v1.json). Those define measurement work; they are not Bitterbot results.[[metric definitions](../METRICS.md)][[status record](../results/initial-baselines-status.json)][[fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded source review of selected files at one commit. It cannot establish runtime behavior across model providers, optional SQLite extensions, configuration choices, or deployments. The local owner-oriented store and guest sensitivity filtering do not establish tenant isolation. Lifecycle state and search-index membership are handled through separate paths; this review did not run deletion/retrieval sequences to assess leakage. Dream-cycle quality and wider skill-network behavior were outside the inspected slice.[[head](https://github.com/Bitterbot-AI/bitterbot-desktop/commit/a0d01b11fae1a73c482f95d00ab4f8df251d737d)][[manager](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/manager.ts)][[search helpers](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/manager-search.ts)][[consolidation](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/consolidation.ts)][[architecture overview](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/docs/memory/architecture-overview.md)]

## Benchmark status

**Benchmark not run.** This review did not execute Bitterbot, benchmarks, or tests. The project's metric definitions and fixture describe domains and protocol; its benchmark status record contains no measured result for this review.[[metric definitions](../METRICS.md)][[benchmark status](../results/initial-baselines-status.json)][[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Official repository and default branch](https://github.com/Bitterbot-AI/bitterbot-desktop)
- [Official main branch Atom feed and full head](https://github.com/Bitterbot-AI/bitterbot-desktop/commits/main.atom)
- [Reviewed full head commit](https://github.com/Bitterbot-AI/bitterbot-desktop/commit/a0d01b11fae1a73c482f95d00ab4f8df251d737d)
- [Official README](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/README.md)
- [Official SECURITY.md](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/SECURITY.md)
- [Memory architecture overview](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/docs/memory/architecture-overview.md)
- [How memory works](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/docs/memory/how-the-memory-works.md)
- [SQLite memory schema](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/memory-schema.ts)
- [Migrations](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/migrations.ts)
- [Memory manager](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/manager.ts)
- [Vector and keyword search](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/manager-search.ts)
- [Canonical facts](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/canonical-facts.ts)
- [Owner controls](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/owner-controls.ts)
- [Forget cascade](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/forget-cascade.ts)
- [Consolidation](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/consolidation.ts)
- [Retrieval trace](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/retrieval-trace.ts)
- [Knowledge graph](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/src/memory/knowledge-graph.ts)
- [Owner controls guide](https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/docs/memory/controls.md)
- [Curated identity and attribution](../data/memory-systems.json)
- [Atlas attribution entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/bitterbot-desktop.md)
- [Metric definitions](../METRICS.md)
- [Benchmark status record](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)

## Contact-list follow-up

The official pinned [README](<https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/README.md>) publishes `victor@bitterbot.net` as a maintainer contact. The official pinned [SECURITY.md](<https://github.com/Bitterbot-AI/bitterbot-desktop/blob/a0d01b11fae1a73c482f95d00ab4f8df251d737d/SECURITY.md>) separately publishes `security@bitterbot.net` for security issues. The JSON records the README maintainer address as `contact_email` with its exact pinned source URL.

**Verification boundary:** no Bitterbot runtime, benchmark, or tests were run.
