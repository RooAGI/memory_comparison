# ContextDB

## Identity and review pin

- **Catalog position:** 147, “contextdb”; slug `contextdb`.
- **Listed repository:** [context-graph-ai/contextdb](https://github.com/context-graph-ai/contextdb); roster locator status is explicit. The pinned Atlas roster entry is recorded only for identity and locator attribution, not as assessment evidence. [Curated roster](../data/memory-systems.json) · [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/contextdb.md)
- **Canonical upstream / default branch:** [context-graph-ai/contextdb](https://github.com/context-graph-ai/contextdb) / `dev`, as shown on the official repository page.
- **Reviewed head:** [df1cf70274d1e204c1b5f9b8f71f67be35609239](https://github.com/context-graph-ai/contextdb/commit/df1cf70274d1e204c1b5f9b8f71f67be35609239); the official [dev commits feed](https://github.com/context-graph-ai/contextdb/commits/dev.atom) reports this full SHA at 2026-11-25T04:08:55Z.
- **Reviewed:** 2026-11-25 09:00:35 UTC (2026-11-25 01:00:35 PST; America/Los_Angeles).
- **Status:** Reviewed from current source and official documentation at pinned GitHub pages. Benchmark not run.

## Summary

ContextDB is an embedded Rust database substrate for agentic-memory applications. It combines relational rows, bounded graph traversal, and exact vector search under transactional storage and policy constraints, while leaving the memory schema and agent-level selection logic to the application. This is a source review; no runtime or benchmark results were collected. [Official README](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/README.md) · [Capability index](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/capability-index.md)

## Architecture and data model

The repository describes a Rust workspace with relational storage as canonical data and graph adjacency and vector structures as secondary indexes. Its engine coordinates SQL parsing/planning, MVCC transactions, persistence, plugins, subscriptions, and optional peer synchronization. A single file is the documented local persistence unit. The database does not ship a prescribed memory schema. [README](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/README.md) · [Architecture](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/architecture.md) · [Engine source](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/crates/contextdb-engine/src/database.rs)

Graph queries use a bounded SQL/PGQ-style traversal with edge types and direction controls. Vector columns use cosine distance; the current docs state that this release provides exact search only, while indexed search is unavailable and the clustered index is switched off. It does not provide built-in embedding generation or agent memory selection. [Architecture](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/architecture.md) · [Capability index](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/capability-index.md)

## Write, update, delete, and retrieval

**Write.** Applications define tables and policy constraints, then issue SQL or use the Rust API. A transaction stages its changes and atomically publishes relational, graph, and vector state. The engine can enforce immutable fields, state-machine transitions, DAG constraints, foreign keys, retention, and state propagation. [README](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/README.md) · [Query language](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/query-language.md) · [Architecture](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/architecture.md)

**Update and correction.** UPDATE and upsert are available subject to table policy. IMMUTABLE columns cannot be changed. The query guide describes a correction pattern that inserts a replacement row and marks the old row superseded; HISTORY ALL preserves superseded versions by default, while HISTORY CURRENT ONLY allows maintenance to reclaim them. [Query language](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/query-language.md) · [Architecture](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/architecture.md)

**Delete and retention.** SQL DELETE and DROP TABLE are supported. RETAIN can expire rows, and maintenance reclaims eligible old versions and storage pages subject to MVCC readers. Logical deletion, version cleanup, and file compaction are separate; deleting or reclaiming a row does not promise secure forensic erasure, immediate file shrinkage, or removal from operator-held backups. The sync guide describes a separate all-or-nothing erasure boundary for governed fleet units. [Query language](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/query-language.md) · [Architecture](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/architecture.md) · [Sync guide](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/sync-two-machines.md)

**Retrieval.** SQL supports filtering, ordering, and bounded results; graph traversal and exact vector search are available for caller-defined records. Scoped handles can apply context, scope-label, and optional ACL restrictions. CLI reads use declared limits and refuse an over-budget result instead of silently truncating it; the embedded API has a separate uncapped execute contract. ContextDB does not itself decide what an agent should remember or return. [Query language](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/query-language.md) · [Capability index](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/capability-index.md) · [Architecture](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/architecture.md)

## Scope isolation

The capability index explicitly says the project is not a multi-tenant orchestration system. Context, scope, and ACL filtering are opt-in application-level declarations, and direct reads of a closed store rely on file permissions. The documented sync tenant ID groups clients and servers that replicate with each other; it is not an isolation boundary for separate tenants. Source documentation describes mechanisms, but does not establish the runtime configuration or isolation properties of any deployment. [Capability index](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/capability-index.md) · [Query language](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/query-language.md) · [Sync guide](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/sync-two-machines.md)

## Provenance and evidence

ContextDB does not supply a native claim-level truth, trust, or citation model. Applications can use immutable columns, state transitions, version history, event records, and sync custody manifests/receipts to preserve data and delivery state. Those mechanisms describe stored rows and transport custody; they do not verify that an extracted or generated claim is factually correct. [Query language](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/query-language.md) · [Sync guide](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/sync-two-machines.md) · [Capability index](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/capability-index.md)

## Efficiency and observability

The architecture documents MVCC readers, serialized writers, bounded resource accounting, cursor paging, maintenance, and memory and disk limits. The engine exposes commit subscriptions and plugin/query hooks; the documentation also describes tracing warnings for guarded contention. Vector search is exact-only in the reviewed release. These are source-visible design properties, not measured latency, throughput, cost, or storage efficiency. [Architecture](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/architecture.md) · [README](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/README.md) · [Capability index](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/capability-index.md)

## Metric domains

The project metric domains remain **unmeasured** in this review: answerable retrieval and abstention; correction accuracy and stale values; deletion leakage; scope isolation; evidence support and citation coverage; retrieval latency; write-to-recall delay; tokens; cost; and storage efficiency. [Metric definitions](../METRICS.md) · [Shared execution status](../results/initial-baselines-status.json) · [Planned fixture](../fixtures/memory-benchmark-v1.json)

## Contact

The official pinned [SECURITY.md](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/SECURITY.md) publishes `security@contextdb.tech` for vulnerability reports. The official pinned [README](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/README.md) and [SECURITY.md](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/SECURITY.md) were checked; no contact was inferred from commit or profile metadata.

## Limitations and unknowns

ContextDB is a database substrate, not an out-of-the-box agent memory manager. The SQL/PGQ graph surface is bounded, indexed vector search is unavailable in this release, and the stated design envelope is 10K–1M rows per database with sparse graphs and bounded traversal. Python and TypeScript bindings are listed as roadmap items; the repository excludes general multi-tenant orchestration. Physical erasure and exact deployment isolation require separate evaluation. [Capability index](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/capability-index.md) · [README](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/README.md) · [Query language](https://github.com/context-graph-ai/contextdb/blob/df1cf70274d1e204c1b5f9b8f71f67be35609239/docs/query-language.md)

This review covers selected official documentation and the engine database source at the verified current head. The source was read through SHA-pinned GitHub pages; the read-only worker command environment did not provide an upstream checkout. No ContextDB runtime, tests, or benchmarks were run.

## Benchmark status

**Benchmark not run.** No system runtime, tests, or benchmark workload was executed for this review. The project metric definitions, shared status record, and planned fixture are protocol references, not results. [Metric definitions](../METRICS.md) · [Shared execution status](../results/initial-baselines-status.json) · [Planned fixture](../fixtures/memory-benchmark-v1.json)

## Sources

Structured source IDs and pinned URLs are recorded in [contextdb.json](../data/system-reviews/contextdb.json). The [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/contextdb.md) supports identity and locator attribution only.