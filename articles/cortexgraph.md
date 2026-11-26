# CortexGraph

## Identity and review pin

- Catalog ordinal: 165
- System: CortexGraph
- Slug: cortexgraph
- Listed repository: https://github.com/prefrontal-systems/cortexgraph
- Roster attribution: explicit repository locator; pinned Atlas entry is retained for identity/locator attribution only, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortexgraph.md)).
- Canonical upstream: https://github.com/prefrontal-systems/cortexgraph
- Default branch: main
- Reviewed full head: [81a2daa3436f0923650eda9d84579cab54710408](https://github.com/prefrontal-systems/cortexgraph/commit/81a2daa3436f0923650eda9d84579cab54710408)
- Review timestamp: 2026-11-25T09:53:45Z (UTC; 2026-11-25 01:53:45 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

The official repository identifies main as default. The main Atom feed and repository page show the reviewed head; a shallow checkout and git ls-remote independently returned the same SHA. ([repository](https://github.com/prefrontal-systems/cortexgraph), [main history](https://github.com/prefrontal-systems/cortexgraph/commits/main.atom), [head commit](https://github.com/prefrontal-systems/cortexgraph/commit/81a2daa3436f0923650eda9d84579cab54710408))

## Summary

CortexGraph is a local-first MCP memory system. It stores short-term records in JSONL by default or SQLite, scores memories with configurable decay and reinforcement, and can promote selected items to Markdown notes in an Obsidian-compatible vault. ([README](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/README.md), [architecture](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/docs/architecture.md))

## Who and what

The official README presents CortexGraph as a research proof of concept rather than a production service. It says the project was transferred to Prefrontal Systems and renamed from Mnemex. ([README](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/README.md))

## Architecture and data model

The Python package separates MCP tools, core algorithms, local storage, consolidation agents, preprocessing, activation, vault integration, and optional web and CLI surfaces. Short-term records use JSONL by default or SQLite; promoted long-term items become Markdown notes. ([README](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/README.md), [architecture](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/docs/architecture.md), [JSONL storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/jsonl_storage.py), [SQLite storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/sqlite_storage.py), [promotion tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/promote.py))

A Memory record contains an ID, content, metadata (tags, free-text source and context, and custom fields), timestamps, use count, strength, status, optional embedding, extracted entities, and review counters. Status values are active, promoted, or archived. Relations are typed directed links with strength, timestamp, and optional metadata. ([memory models](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/models.py))

The documented score combines use count, elapsed time since last use, configured decay, and strength. The code supports power-law, exponential, and two-component decay. This is a code observation, not measured retention. ([architecture](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/docs/architecture.md), [decay implementation](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/core/decay.py))

JSONL loads records into in-memory indexes and appends snapshots and deletion markers. The implementation warns that all memories are loaded into RAM. The documentation states a single-machine, single-user target and a scale target of 1,000–10,000 active memories. ([JSONL storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/jsonl_storage.py), [architecture](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/docs/architecture.md))

## Write, update, delete, and retrieval

**Write.** save_memory validates content and metadata, may extract entities and calculate importance, optionally creates an embedding, then saves a new UUID record. Source and context are caller-supplied text, not validated references to retained evidence. Embeddings are disabled by default in configuration. ([save tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/save.py), [memory model](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/models.py), [search tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/search.py))

**Update and correction.** touch_memory and observe_memory_usage update last-used time and use count; optional reinforcement raises strength up to its cap. Storage updates selected usage, review, status, and promotion fields. save_memory creates a new UUID; the inspected API defines no dedicated correction revision or stale-value reconciliation protocol. ([touch](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/touch.py), [observe](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/observe.py), [JSONL storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/jsonl_storage.py), [save tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/save.py))

**Delete and forgetting.** gc defaults to dry-run and selects active records below the forget threshold. When applied, it can archive or delete them. JSONL deletion removes the record from the in-memory index and appends a deletion marker; compaction can rewrite storage to discard markers. This is logical application deletion, not proof of secure physical erasure. No delete or post-delete probe was run. ([garbage collection](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/gc.py), [JSONL storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/jsonl_storage.py), [security policy](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/SECURITY.md))

**Retrieval.** search_memory filters by status, tags, and optional time window, ranks by decay and text overlap, optionally uses embedding similarity, and can blend relevant review-due records. It validates search bounds and returns memory records; source review establishes no answer-quality or abstention guarantee. ([search tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/search.py), [memory model](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/models.py), [architecture](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/docs/architecture.md))

## Scope isolation

Inspected memory records and search filters contain no user, project, tenant, or session principal. The official security policy explicitly says CortexGraph is single-user and does not provide multi-user isolation. Filesystem path containment does not establish logical tenant isolation. ([memory model](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/models.py), [search tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/search.py), [security policy](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/SECURITY.md))

## Provenance and evidence

Records can store free-text source and context, tags, entities, and custom metadata; relations accept arbitrary metadata. The inspected schema does not enforce source passage identifiers, a provenance chain, trust state, or a citation contract for generated answers. Caller metadata may describe provenance, but its evidentiary accuracy is not checked. ([memory model](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/models.py), [save tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/save.py), [relation tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/create_relation.py))

## Efficiency and observability

The JSONL backend builds in-memory indexes and exposes active counts, file bytes, line counts, and compaction potential. The performance collector retains up to 1,000 timing samples per operation and reports count, average, minimum, maximum, and total time in process. These are source-visible mechanisms; no measurements were collected here. ([JSONL storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/jsonl_storage.py), [performance instrumentation](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/performance.py))

## Metric-domain evidence

All project benchmark outcomes are **unmeasured** for CortexGraph. The fixture and shared status record describe a protocol and execution status, not results. ([metric definitions](../METRICS.md), [benchmark fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Search is implemented; no answerable or unanswerable probes were adjudicated. |
| Correction accuracy and stale-value rate | Unmeasured | Usage updates exist, but no explicit correction protocol was identified or evaluated. |
| Deletion leakage | Unmeasured | Garbage collection and JSONL deletion markers exist; no post-delete probes were run. |
| Scope isolation | Unmeasured | The project documents single-user operation without multi-user isolation; no probes were run. |
| Evidence support and citation coverage | Unmeasured | Free-text provenance fields exist; no claims or citations were scored. |
| Retrieval latency | Unmeasured | No retrieval timings were collected. |
| Write-to-recall delay | Unmeasured | No timed write-and-recall probes were run. |
| Tokens and cost | Unmeasured | No model usage or provider charges were collected. |
| Storage efficiency | Unmeasured | No benchmark corpus size or bytes-per-item measure was collected. |

The project exposes timing counters and storage statistics, but source-level instrumentation is not a benchmark result. ([performance instrumentation](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/performance.py), [JSONL storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/jsonl_storage.py), [metric definitions](../METRICS.md))

## Limits and unknowns

This bounded inspection covered the README and architecture document, record model, JSONL and SQLite storage, save/search/touch/observe/GC/promotion/relation tools, decay logic, performance collector, and security policy. It did not trace every MCP tool, database query, agent workflow, migration, web surface, or vault synchronization route. ([README](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/README.md), [architecture](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/docs/architecture.md), [JSONL storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/jsonl_storage.py), [SQLite storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/sqlite_storage.py))

The README labels the project a research proof of concept. The security policy states there is no encryption at rest, no multi-user isolation, and OS-level locking is not cluster-safe. No runtime, tests, or benchmarks were run, so operational correctness and measured behavior remain unknown. ([README](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/README.md), [security policy](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/SECURITY.md))

## Contact

No contact email is published in the official pinned README or SECURITY.md. The README directs general questions to repository channels, and the security policy directs vulnerability reports to GitHub private vulnerability reporting. No profile, commit metadata, or third-party directory was used. ([README](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/README.md), [security policy](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/SECURITY.md))

## Benchmark status

**Benchmark not run.** CortexGraph, its tests, and benchmark workloads were not run. The fixture is a workload specification only; the shared execution-status record contains no CortexGraph measurements. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortexgraph.md)
- [Official repository](https://github.com/prefrontal-systems/cortexgraph)
- [Official main commit feed](https://github.com/prefrontal-systems/cortexgraph/commits/main.atom)
- [Reviewed full head 81a2daa3436f0923650eda9d84579cab54710408](https://github.com/prefrontal-systems/cortexgraph/commit/81a2daa3436f0923650eda9d84579cab54710408)
- [Pinned README](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/README.md)
- [Pinned architecture documentation](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/docs/architecture.md)
- [Pinned memory model](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/models.py)
- [Pinned JSONL storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/jsonl_storage.py)
- [Pinned SQLite storage](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/storage/sqlite_storage.py)
- [Pinned save tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/save.py)
- [Pinned search tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/search.py)
- [Pinned touch tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/touch.py)
- [Pinned usage-observation tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/observe.py)
- [Pinned garbage collection tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/gc.py)
- [Pinned promotion tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/promote.py)
- [Pinned relation tool](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/tools/create_relation.py)
- [Pinned decay implementation](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/core/decay.py)
- [Pinned performance instrumentation](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/src/cortexgraph/performance.py)
- [Pinned security policy](https://github.com/prefrontal-systems/cortexgraph/blob/81a2daa3436f0923650eda9d84579cab54710408/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
