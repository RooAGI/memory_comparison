# Areev

## Identity and review pin

- **Curated ordinal:** 68 in `data/memory-systems.json`
- **Listed name / slug:** Areev / `areev`
- **Listed repository locator:** https://github.com/AreevAI/areev
- **Canonical repository:** https://github.com/AreevAI/areev
- **Default branch:** `main`
- **Reviewed head:** [`1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f`](https://github.com/AreevAI/areev/commit/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f)
- **Reviewed at:** 2026-11-24 21:29:19 UTC (13:29:19 PST, America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The roster’s [Atlas report](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/areev.md) is retained for identity, listed locator, and source attribution only. Its descriptions, marks, and layout are not assessment evidence.

## Summary

Areev is an embedded Rust memory engine and an implementation of the Open Memory Spec. It stores typed, immutable, content-addressed memory grains in per-memory database files. CAL provides structured and hybrid retrieval and assembles selected grains into a token-budgeted context. Areev Loop adds an optional, review-gated process for proposing and measuring memory changes. Findings here are source and documentation observations at the reviewed commit, not runtime measurements.

## Who and what

The official [README](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/README.md) presents Areev Core as an open-source engine for building focused AI products, with Rust, Python, Node.js, CLI, and MCP surfaces. The README says it is built and backed by MindGryd Software Private Limited. The repository describes local embedded storage as the default and PostgreSQL for server deployments. This is an engine and set of libraries and tools, rather than a hosted memory service.

## Architecture and data model

The [architecture guide](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/ARCHITECTURE.md) describes a grain as the atomic memory record: examples include a fact, event, state snapshot, or tool call. Grain identity is a SHA-256 address over a canonical serialized blob. A common envelope carries namespace, timestamps, provenance, supersession links, and optional content or embedding references. Typed fields add the semantics for each grain kind.

The store organizes each memory as a database file. Its indexes include dictionary-encoded subject/relation/object permutations, current entity heads, full-text and vector search structures, thread lookups, and an operation log with hybrid logical clocks and tombstones. Large content can live in a content-addressed blob sidecar. The [store implementation](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/crates/areev-store/src/lib.rs) exposes the embedded backend behind a synchronous store seam and also has a separately gated PostgreSQL backend.

## Write, update, delete, and retrieval

- **Write:** the documented surfaces include CAL `ADD`, language bindings, MCP, and CLI commands. A new grain is validated, serialized, and addressed by its contents. Tool executions are stored as data; the host, not the store, executes tools. The [grain guide](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/docs/grains.md) distinguishes durable facts from events, observations, state, plans, and other types.
- **Update:** grains are not edited in place. A correction is a new grain that supersedes an earlier grain, preserving history and allowing world-time and knowledge-time queries. Concurrent supersessions can leave multiple heads; the architecture describes deterministic provisional reads and explicit merge operations for resolving a fork.
- **Delete:** single-grain `FORGET` creates a tombstone. The [erasure guide](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/docs/erasure.md) documents subject- and age-based bulk erasure, exact namespace requirements, replication through ordinary tombstones, and audit behavior. Whole-memory deletion or cryptographic erasure is a separate file-level operation. On the embedded backend, physical remnants can remain in database pages or WAL until compaction; the documentation recommends crypto-erasure when whole-memory destruction is required.
- **Retrieval:** CAL supports structural filters, BM25 full text, vector search, reciprocal-rank fusion, bounded graph traversal, and temporal reads. `ASSEMBLE` can combine sources under priorities and per-source token budgets, then render formats such as SML, TOON, Markdown, or JSON. The README describes local recall as in-process without a server hop. These design and API descriptions do not establish answer quality or latency in this review.

## Scope isolation

Areev partitions memories into separate files, with namespaces providing finer query and authorization scopes. The architecture describes read-only mounts for composing sources and namespace checks in the store/CAL path. The [store code](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/crates/areev-store/src/lib.rs) uses exact-namespace and writable-namespace guards. These mechanisms are source-visible boundaries; this review did not run cross-tenant probes or establish the security of a particular host integration or deployment configuration.

## Provenance and evidence

The grain envelope and type-specific fields support source, actor, timestamps, content references, and supersession links. Reasoning grains can retain premises and conclusions; recommendation and audit records can carry evidence references and review decisions. Content addressing detects changes to serialized content, but the [security policy](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/SECURITY.md) explicitly says grain authenticity is not verified on import. Hash identity therefore does not by itself prove who created a grain or whether its claims are true.

## Source-visible efficiency and observability

**Code and documentation observations:** the intended recall path stays in-process; typed indexes support point and bounded graph reads; context assembly shares a token estimator and can progressively summarize or omit grains as budgets fill. Each memory file has its own writer queue, so the guide describes adding files as the scale-out boundary. Areev Loop can consume the operation log and a disposable recall-telemetry sidecar; the architecture describes buffered, non-blocking capture. The README says Areev collects no telemetry, which distinguishes local opt-in telemetry from telemetry sent to the project.

The architecture publishes source-level latency statements and the README reports separate retrieval and synthetic task experiments. I did not reproduce those claims. This review captured no latency, throughput, token, cost, storage, or write-to-recall measurements.

## Metric-domain evidence

Every project metric domain is **unmeasured** for this review. The project’s definitions are in [METRICS.md](../METRICS.md); the [execution-status record](../results/initial-baselines-status.json) is shared status, not an Areev result, and the [fixture](../fixtures/memory-benchmark-v1.json) is a planned workload.

| Domain | Source observation | Measurement status |
|---|---|---|
| Answerable recall and abstention | CAL exposes structured, lexical, vector, and fused retrieval paths. | Unmeasured |
| Correction accuracy and stale values | Supersession and two-axis temporal reads represent corrections and history. | Unmeasured |
| Deletion leakage | Tombstones and bulk erasure paths are documented; no post-delete probes were run. | Unmeasured |
| Scope isolation | Files, namespaces, and exact-scope guards are visible in code and docs. | Unmeasured |
| Evidence support and citation coverage | Grains can carry provenance and references; no claims or answers were adjudicated. | Unmeasured |
| Latency and write-to-recall delay | In-process retrieval and indexes are visible; no timings were collected. | Unmeasured |
| Tokens, cost, and storage | Budgeted context and local database/blob storage are described; no workload accounting was done. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of selected documentation and source at one verified commit. No Areev runtime, benchmark workload, or tests were run. The review cannot establish practical recall quality, abstention calibration, correction behavior across a workload, deletion completeness across backups or replicas, tenant isolation in a deployed host, or operational performance.

The security policy identifies concrete limits: the blob sidecar is plaintext even when the database is encrypted; imported grain authenticity is not verified; and the embedded engine’s encryption feature is described as experimental and defense in depth. Database-page remnants can remain until compaction. These limits should be evaluated against the chosen backend, host, and data-handling requirements.

## Contact-list follow-up

The official pinned [SECURITY.md](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/SECURITY.md) publishes **security@areev.ai** for private vulnerability reports. The official pinned [README](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/README.md) and [SUPPORT.md](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/SUPPORT.md) were also checked for a published contact email. The JSON records the security email and exact source URL.

## Benchmark status

**Benchmark not run.** No Areev runtime, tests, or benchmark workload were run for this review. Upstream README and architecture statements about separate experiments remain source-reported claims and are not results of this project’s benchmark. See the [project metric definitions](../METRICS.md), [shared execution-status record](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

- [Canonical repository](https://github.com/AreevAI/areev)
- [Current main commit feed](https://github.com/AreevAI/areev/commits/main.atom)
- [Verified main head](https://github.com/AreevAI/areev/commit/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f)
- [README](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/README.md)
- [Architecture guide](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/ARCHITECTURE.md)
- [Grain guide](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/docs/grains.md)
- [Erasure guide](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/docs/erasure.md)
- [Store implementation](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/crates/areev-store/src/lib.rs)
- [Memory tool adapter](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/crates/areev-store/src/memory_tool.rs)
- [Security policy](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/SECURITY.md)
- [Support policy](https://github.com/AreevAI/areev/blob/1911fb48a6ce05d9b4bb3c493ed3c9a42e585f2f/SUPPORT.md)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution-status record](../results/initial-baselines-status.json)
- [Planned benchmark fixture](../fixtures/memory-benchmark-v1.json)
