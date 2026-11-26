# dsh-ai-memory

## Identity and review pin

- Catalog position: 196
- System name: `dsh-ai-memory`
- Slug: `dsh-ai-memory`
- Listed repository: https://github.com/zzjzzb/ai-memory
- Roster attribution: explicit repository locator; the pinned Atlas entry is retained for curated identity/locator context only, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-ai-memory.md)).
- Canonical upstream: https://github.com/zzjzzb/ai-memory
- Default branch: `main`
- Current full head: [9208281522612ebb349dff2e1b7e07a9c7683def](https://github.com/zzjzzb/ai-memory/commit/9208281522612ebb349dff2e1b7e07a9c7683def)
- Reviewed at: 2026-11-25T11:27:15Z (UTC)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

The official repository page identifies the public `zzjzzb/ai-memory` repository and `main` as its default branch. GitHub's official main Atom feed reports full head `9208281522612ebb349dff2e1b7e07a9c7683def`, updated at 2026-09-11T06:18:18Z. The official commit page and Git tree API confirm that revision. ([repository](https://github.com/zzjzzb/ai-memory), [main history](https://github.com/zzjzzb/ai-memory/commits/main.atom), [commit](https://github.com/zzjzzb/ai-memory/commit/9208281522612ebb349dff2e1b7e07a9c7683def), [tree](https://api.github.com/repos/zzjzzb/ai-memory/git/trees/9208281522612ebb349dff2e1b7e07a9c7683def?recursive=1))

## Summary

dsh-ai-memory is a local Rust and SQLite memory library for agent harnesses, with optional DeepSeek Harness integration. It stores project-scoped working, episodic, and profile notes; recalls them using recency, keyword, and vector scores; and can build a token-budgeted context pack. This is a source review, not a runtime or benchmark assessment. ([README](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/README.md), [architecture](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/docs/ARCHITECTURE.md))

## Who and what

The project describes itself as a memory layer below the agent harness: the host owns model calls and the tool loop, while this Rust library stores and recalls notes. The optional DeepSeek Harness plugin registers tools and a prompt prefetch section. This is a library and adapter, not a hosted service or complete LLM harness. ([README](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/README.md), [plugin](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/integrations/dsh-ai-memory/src/index.js))

## Architecture and data model

A SQLite database can hold multiple projects. Records have a project id, tier (`working`, `episodic`, or `profile`), text, optional JSON metadata, timestamps, access count, pin state, and an embedding. A per-project `MemoryPolicy` configures retention, promotion, and recall weights. ([types](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/types.rs), [policy](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/policy.rs), [SQLite store](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/sqlite.rs))

The `MemoryStore` interface supports project operations, writes, reads, pin/unpin, forget, recall, and consolidation. `ProjectHandle` binds operations to one project. The default SQLite backend uses an offline hash embedder and in-process cosine index; callers can inject alternatives, and sqlite-vec is optional. ([store contract](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/store.rs), [embedder](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/embedder.rs), [vector index](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/vector.rs))

## Write, update, delete, and retrieval

**Writes and updates.** Writes create rows, optionally with a tier; when omitted, a small heuristic can choose one. Batch writes are documented as one transaction. The inspected public contract has no update-in-place method, so correction must use forget-and-rewrite or a caller-managed convention. ([store contract](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/store.rs), [SQLite store](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/sqlite.rs), [tier policy](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/policy.rs))

**Deletion and maintenance.** Forget deletes by memory id within a project; project deletion is documented to cascade through memories and embeddings. Explicit consolidation applies TTL expiry and tier promotion. Expired unpinned rows are hidden from recall before consolidation; pins skip expiry. There is no background consolidator in the documented flow. ([store contract](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/store.rs), [policy](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/policy.rs), [usage guide](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/docs/USAGE.md))

**Retrieval.** Recall combines recency, keyword overlap, and vector similarity. The documented default bounds candidate scanning and prunes before vector scoring; the default vector path uses brute-force cosine. Budgeted packing ranks pinned rows first, then score and recency, and renders each result with its id, tier, score, and text. The default token estimator is `ceil(chars/4)`; callers can inject another estimator. ([policy](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/policy.rs), [SQLite store](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/sqlite.rs), [context pack](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/harness/context.rs), [usage guide](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/docs/USAGE.md))

**Compaction.** Explicit `compact_working` keeps pinned and newest working rows and folds bounded snippets from older rows into an episodic note. The default compactor is extractive and offline; folded working rows are then forgotten. ([compactor](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/harness/compact.rs), [usage guide](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/docs/USAGE.md))

## Scope isolation

Store methods take a project id, and `ProjectHandle` binds calls to a project. The SQLite operations are scoped by project id; the plugin uses a configured project id. This provides an application-level project boundary, but does not itself authenticate users or prove deployed isolation. ([store contract](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/store.rs), [SQLite store](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/sqlite.rs), [plugin](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/integrations/dsh-ai-memory/src/index.js))

## Provenance and evidence

Memory records can store optional metadata and expose operational fields such as IDs and timestamps. Context packs include id, tier, and score. The inspected tool/API surface does not require source URLs, claim-level evidence, trust state, or citations in generated answers, so provenance depends on caller-supplied metadata and workflow. ([types](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/types.rs), [context pack](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/harness/context.rs), [tools](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/integrations/dsh-ai-memory/src/tools.js))

## Efficiency and observability

The code applies SQLite WAL for file-backed stores, prepared statement caching, an embedding LRU, cache and busy-timeout defaults, bounded candidate scans, and a smaller candidate-prune set. Batch writes can use one transaction. The store exposes its applied pragmas for inspection. These are design/code observations, not measured latency, throughput, token, cost, or storage outcomes. ([SQLite store](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/sqlite.rs), [architecture](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/docs/ARCHITECTURE.md), [usage guide](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/docs/USAGE.md))

## Metric-domain evidence

All benchmark domains are **unmeasured** for this review. The repository’s benchmark examples and upstream performance statements were not reproduced or independently adjudicated. ([metric definitions](../METRICS.md), [fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Hybrid recall and empty results are available; no cases were scored. |
| Correction accuracy and stale-value rate | Unmeasured | The inspected contract has no update-in-place operation; no correction probes were run. |
| Deletion leakage | Unmeasured | Forget and project deletion exist; no post-delete probes or physical-storage checks were made. |
| Scope isolation | Unmeasured | Project-scoped handles and queries are source-visible; no cross-project workload was run. |
| Evidence support and citation coverage | Unmeasured | The context pack identifies memory rows but does not define claim-level citations; no answers were adjudicated. |
| Retrieval latency and write-to-recall delay | Unmeasured | No timings or write/recall probes were collected. |
| Tokens and cost | Unmeasured | A token estimator exists; no runtime usage or cost was recorded. |
| Storage efficiency | Unmeasured | SQLite storage is implemented; no corpus-attributed size was measured. |

## Limits and unknowns

This review inspected official SHA-pinned GitHub source and documentation pages, not a local upstream checkout. It did not inspect every helper, CLI route, optional sqlite-vec implementation, or every host integration detail. No runtime, tests, or benchmarks were run. Source inspection cannot establish deployed configuration, retrieval quality, correction outcomes, deletion completeness, effective access control, latency, costs, or storage efficiency. ([README](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/README.md), [SQLite store](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/sqlite.rs), [metric definitions](../METRICS.md))

The official pinned README and CONTRIBUTING.md were checked for a contact email; neither publishes one. No commit/profile metadata or third-party directories were used. ([README](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/README.md), [contributing guide](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/CONTRIBUTING.md))

## Benchmark status

**Benchmark not run.** dsh-ai-memory, its tests, and benchmark workloads were not run. Metric definitions and the project execution-status record are cited as contract/status context, not as system results. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and position](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-ai-memory.md)
- [Official repository](https://github.com/zzjzzb/ai-memory)
- [Official main branch feed](https://github.com/zzjzzb/ai-memory/commits/main.atom)
- [Reviewed full head](https://github.com/zzjzzb/ai-memory/commit/9208281522612ebb349dff2e1b7e07a9c7683def)
- [Pinned README](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/README.md)
- [Pinned contribution guide](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/CONTRIBUTING.md)
- [Pinned architecture guide](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/docs/ARCHITECTURE.md)
- [Pinned usage guide](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/docs/USAGE.md)
- [Pinned store contract](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/store.rs)
- [Pinned SQLite implementation](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/sqlite.rs)
- [Pinned project policy](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/policy.rs)
- [Pinned memory types](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/types.rs)
- [Pinned context pack](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/harness/context.rs)
- [Pinned working compactor](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/harness/compact.rs)
- [Pinned vector index](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/vector.rs)
- [Pinned embedder](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/src/embedder.rs)
- [Pinned DSH tool definitions](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/integrations/dsh-ai-memory/src/tools.js)
- [Pinned DSH plugin](https://github.com/zzjzzb/ai-memory/blob/9208281522612ebb349dff2e1b7e07a9c7683def/integrations/dsh-ai-memory/src/index.js)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project execution-status record](../results/initial-baselines-status.json)
