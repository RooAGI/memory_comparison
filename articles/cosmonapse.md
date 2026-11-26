# Cosmonapse

## Identity and review pin

- Catalog ordinal: 166
- System: Cosmonapse
- Slug: `cosmonapse`
- Listed repository: https://github.com/Cosmonapse/cosmonapse-core
- Roster attribution: the catalog marks the repository locator explicit; the pinned Atlas record is retained only for curated identity/locator attribution ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cosmonapse.md)).
- Canonical upstream: https://github.com/Cosmonapse/cosmonapse-core
- Default branch: `main`
- Reviewed full head: [bdb0be8e54190a4e41a34859d4c225571b5bc5b9](https://github.com/Cosmonapse/cosmonapse-core/commit/bdb0be8e54190a4e41a34859d4c225571b5bc5b9)
- Review timestamp: 2026-11-25T09:53:41Z (UTC; 2026-11-25 01:53:41 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

Cosmonapse is an event-driven runtime and Python SDK for distributed AI agents. Its optional Engram interface routes memory reads and writes as typed Signals over the same bus as task and tool events. The shipped Engram backends provide simple tagged, substring, or merge-key lookup over in-memory, SQLite, and PostgreSQL records; richer retrieval is left to custom backends. This is a source review only. ([README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/README.md), [Python SDK README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/README.md))

## Current upstream revision

The official repository page identifies `main` as the default branch. The official `main` Atom feed reports `bdb0be8e54190a4e41a34859d4c225571b5bc5b9` as its latest commit, updated 2026-11-19T15:40:22Z; the official commit page confirms that full SHA. ([repository](https://github.com/Cosmonapse/cosmonapse-core), [main commit feed](https://github.com/Cosmonapse/cosmonapse-core/commits/main.atom), [reviewed commit](https://github.com/Cosmonapse/cosmonapse-core/commit/bdb0be8e54190a4e41a34859d4c225571b5bc5b9))

## Architecture and data model

Cosmonapse models participants communicating through typed Signals on a Synapse message bus. Neurons are async functions hosted by Axons and connected by Dendrites; Effectors handle tools and side effects, while Receptors expose entry points such as CLI or HTTP. A centralized scheduler is not required. The README describes in-memory, local TCP, NATS, and Kafka transports. ([README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/README.md), [Python SDK README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/README.md))

Engram is a distinct, optional memory participant addressed by ID or kind. The host Dendrite services RECALL/IMPRINT requests and returns RECALLED/IMPRINTED responses. Requests carry the containing task's trace and parent lineage; the wire protocol leaves record schema and query semantics to each backend. ([Engram design](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/design/ENGRAM_DESIGN.md), [Signal envelope specification](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/design/ENVELOPE_SPEC.md), [Engram interface](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/base.py))

The SDK ships an in-memory backend for ephemeral use, a SQLite backend, and a PostgreSQL backend. Entries contain an ID, content, tags, version, creation/update times, and optional merge key and metadata. SQLite serializes content and metadata as JSON; PostgreSQL uses JSONB and a text-array tag field. Both SQL stores add a logical deletion timestamp and indexes for kind and merge key; PostgreSQL also indexes tags. ([Python SDK README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/README.md), [in-memory store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/memory.py), [SQLite store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/sqlite.py), [PostgreSQL store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/postgres.py))

## Write, update, delete, and retrieval

**Write and update.** The built-in stores support add, append, merge, and upsert operations. Add inserts a new ID; append records an item under a merge key; merge combines content and metadata and unions tags; upsert replaces a record found by merge key. Updates increment the record version and refresh its update time. The exact entry body is backend-defined. ([Engram design](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/design/ENGRAM_DESIGN.md), [in-memory store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/memory.py), [SQLite store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/sqlite.py), [PostgreSQL store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/postgres.py))

**Delete.** The in-memory backend removes an entry from its dictionaries. SQLite and PostgreSQL mark the row deleted with `deleted_at` and exclude it from normal recall; the reviewed code does not establish physical erasure from database pages, logs, or backups. ([in-memory store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/memory.py), [SQLite store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/sqlite.py), [PostgreSQL store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/postgres.py))

**Retrieval.** The default backends provide case-insensitive substring matching on content, exact tag or merge-key matches, optional all-tags and time-window filters, and a top-k limit (default 50). The SDK documentation directs vector-search or BM25 use cases to custom backends. ([in-memory store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/memory.py), [SQLite store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/sqlite.py), [PostgreSQL store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/postgres.py), [Python SDK README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/README.md))

## Scope isolation

The design accepts a `context_ref` that may describe trace, session, or project context and carries it with recall requests. The shipped entry schemas and query implementations do not partition or authorize records by that field. Applications must enforce access through their chosen backend and host wiring; the protocol field alone is not an isolation control. No isolation workload was run. ([Engram design](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/design/ENGRAM_DESIGN.md), [in-memory store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/memory.py), [SQLite store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/sqlite.py), [PostgreSQL store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/postgres.py))

## Provenance and evidence

Signal IDs, trace IDs, and parent IDs make each memory request and response traceable to its task and causal parent. Responses can include the responding Engram, hit IDs, scores, result version, and elapsed time. Entry payloads are otherwise opaque; source URLs, claim-level citations, trust grades, and human review are not required by the shipped schema. ([Signal envelope specification](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/design/ENVELOPE_SPEC.md), [Engram design](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/design/ENGRAM_DESIGN.md), [Engram interface](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/base.py))

## Efficiency and observability

Prism and passive Doppler consumers expose Signal streams and trace views. The SDK client correlates replies, supports deadlines and task cancellation, and allows optional acknowledgement for writes. SQLite dispatches blocking database calls through the default thread-pool executor. SQL indexes cover Engram kind and merge keys, with PostgreSQL GIN indexing for tags. These are source-visible controls, not measured performance. ([README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/README.md), [Python SDK README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/README.md), [Engram client](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/client.py), [SQLite store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/sqlite.py), [PostgreSQL store](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/postgres.py))

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Cosmonapse. The project metric definitions, fixture, and execution-status record are references only; no workload was run. ([metric definitions](../METRICS.md), [fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Built-in stores provide simple matches; no answer scoring was performed. |
| Correction accuracy and stale-value rate | Unmeasured | Merge/upsert and version changes exist; no correction probes were run. |
| Deletion leakage | Unmeasured | SQL delete is a logical mark; no post-delete probes were run. |
| Scope isolation | Unmeasured | A context reference is carried by the protocol; no authorization isolation was measured. |
| Evidence support and citation coverage | Unmeasured | Trace lineage exists; no claim support was scored. |
| Retrieval latency and write-to-recall delay | Unmeasured | No timed workload was run. |
| Tokens and cost | Unmeasured | No runtime usage or charges were measured. |
| Storage efficiency | Unmeasured | No corpus storage size was measured. |

## Limits and unknowns

This bounded review inspected the official README, SDK README, Engram design and envelope specification, and the current Engram interface, in-memory, SQLite, PostgreSQL, and client implementations. ENGRAM_DESIGN.md labels itself a draft. This review did not inspect every transport adapter, backend migration, deployment, custom Engram, or authorization integration. ([README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/README.md), [SDK README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/README.md), [Engram design](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/design/ENGRAM_DESIGN.md), [Engram sources](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/base.py))

The review cannot establish runtime correctness, retrieval quality, correction behavior, isolation in a deployment, physical deletion, latency, cost, or storage efficiency. No Cosmonapse runtime, tests, or benchmarks were run. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

## Contact

The official pinned README was checked for a published contact email and contains none. No commit/profile metadata or third-party directory was used. ([official README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/README.md))

## Benchmark status

**Benchmark not run.** Cosmonapse, its tests, and project benchmark workloads were not run. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cosmonapse.md)
- [Official repository](<https://github.com/Cosmonapse/cosmonapse-core>)
- [Official main commit feed](https://github.com/Cosmonapse/cosmonapse-core/commits/main.atom)
- [Reviewed full head bdb0be8e54190a4e41a34859d4c225571b5bc5b9](https://github.com/Cosmonapse/cosmonapse-core/commit/bdb0be8e54190a4e41a34859d4c225571b5bc5b9)
- [Pinned official README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/README.md)
- [Pinned Python SDK README](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/README.md)
- [Pinned Engram design draft](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/design/ENGRAM_DESIGN.md)
- [Pinned Signal envelope specification](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/design/ENVELOPE_SPEC.md)
- [Pinned Engram interface](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/base.py)
- [Pinned in-memory Engram](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/memory.py)
- [Pinned SQLite Engram](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/sqlite.py)
- [Pinned PostgreSQL Engram](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/postgres.py)
- [Pinned Engram client](https://github.com/Cosmonapse/cosmonapse-core/blob/bdb0be8e54190a4e41a34859d4c225571b5bc5b9/packages/python-sdk/cosmonapse/engram/client.py)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project execution status](../results/initial-baselines-status.json)
