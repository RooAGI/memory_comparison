# Cortex (Hypermnesia)

## Identity and review pin

- Catalog ordinal: 159
- System: Cortex (Hypermnesia)
- Slug: `cortex-hypermnesia`
- Listed repository: https://github.com/cdeust/Cortex
- Roster attribution: the catalog marks the locator explicit and records the pinned Atlas entry for identity/locator context only. Atlas is not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortex-hypermnesia.md)).
- Canonical upstream: https://github.com/cdeust/Cortex
- Default branch: `main`
- Reviewed full head: [b9e9c36f24abfa779282ce8accba0695306a3e77](https://github.com/cdeust/Cortex/commit/b9e9c36f24abfa779282ce8accba0695306a3e77)
- Review timestamp: 2026-11-25T09:30:30Z (UTC; 2026-11-25 01:30:30 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub’s repository page identifies `main` as the default branch. Its official main-branch Atom feed reports the full head SHA above, updated at 2026-11-24T01:10:56Z; the repository page displays the matching short head `b9e9c36`. ([repository](https://github.com/cdeust/Cortex), [main history](https://github.com/cdeust/Cortex/commits/main.atom), [head commit](https://github.com/cdeust/Cortex/commit/b9e9c36f24abfa779282ce8accba0695306a3e77))

## Summary

Cortex is a local-first persistent memory MCP server for coding agents. It uses SQLite by default or PostgreSQL with pgvector, provides explicit memory tools to MCP hosts, and adds automatic capture and context hooks through its Claude Code and Codex plugins. Retrieval combines stored signals without an LLM in the retrieval loop. ([README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md), [MCP tool catalogue](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/mcp-tools.md))

## Who and what

The official README describes Cortex as the independent work of Clément Deust and presents it as open-source software that runs on the user’s machine by default, rather than as a hosted memory service. Its contact section publishes admin@ai-architect.tools. ([README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md))

## Architecture and data model

The Python project separates pure core logic, infrastructure, tool handlers, server and transport layers; lifecycle hooks also use core and infrastructure modules. The MCP tool catalogue exposes memory operations alongside profiling, consolidation, search, telemetry, and project wiki tools. ([architecture](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/architecture.md), [tool catalogue](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/mcp-tools.md))

The PostgreSQL schema stores memory content and embeddings with tags, source, domain, directory context, timestamps, heat/decay fields, confidence, access counters, capture origin, and related state. Supporting tables and modules cover entities, relationships, wiki pages, and other memory subsystems. SQLite provides the local default backend. ([PostgreSQL schema](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_schema.py), [README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md))

## Write, update, delete, and retrieval

**Write.** The `remember` handler accepts content, tags, directory, source, agent topic, global status, event time, and write class. It resolves origin/domain and delegates through configured gates and storage logic. Exact duplicates in the same write scope can be rejected with the existing memory ID; automatic capture shares that check. The README describes reference grading as a local structural check, not a truth assessment. ([remember handler](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/handlers/remember.py), [API reference](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/api-reference.md), [README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md))

**Correction and maintenance.** The API describes explicit `supersedes_id` writes as an atomic supersession path. Consolidation can supersede retained duplicate rows. The retrieved documentation describes decay-based consolidation, but this review did not trace every maintenance path or establish how each correction type behaves in every backend. ([API reference](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/api-reference.md), [tool catalogue](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/mcp-tools.md))

**Delete.** `forget` supports soft deletion by marking a memory stale and setting heat to zero; the handler notes that the row remains recoverable through SQL. Hard deletion calls the store erasure operation, reports deleted derived claims and artifacts, and can remove derived wiki pages after the transaction. The PostgreSQL erasure code notes that dead tuples remain until vacuum reclaims them. Thus logical removal is implemented, while immediate physical erasure from database storage is not established. ([forget handler](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/handlers/forget.py), [PostgreSQL erasure](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_store_erasure.py))

**Retrieval.** `recall` returns ranked memories, caps results, can add triggered/co-activated memories and related neighbors, annotates source attribution, and bounds the response payload. The PostgreSQL search implementation has vector and full-text paths; the README describes hybrid fusion across vector, full-text, trigram, heat, and recency signals, followed by cross-encoder reranking. The README also says SQLite fusion is in-process and unindexed, with no trigram signal, and cautions that it may be slower at very large scale. ([recall handler](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/handlers/recall.py), [PostgreSQL search](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_store_search.py), [README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md))

## Scope isolation

Memory writes carry directory and domain context, and search can apply project-directory ancestors within the query before ranking and limiting. The scope helper treats an omitted directory scope as no project restriction; when a project is supplied, it admits matching directories and explicitly global memories. This is useful project filtering, but the inspected paths do not establish mandatory tenant isolation for every tool or auxiliary store. ([remember handler](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/handlers/remember.py), [scope predicate](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_scope_clause.py), [PostgreSQL search](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_store_search.py))

## Provenance and evidence

Memory rows retain source, capture origin, and reference-related state. Recall exposes stored source attribution and a confabulation-risk annotation. The README states the provenance grade checks whether a reference resolves locally; a verified grade does not establish that the underlying claim is true. No general claim-level citation contract for arbitrary generated answers was established in this bounded review. ([PostgreSQL schema](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_schema.py), [recall handler](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/handlers/recall.py), [README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md))

## Efficiency and observability

The PostgreSQL path uses vector and full-text search structures and documents hybrid ranking and cross-encoder reranking; SQLite performs fusion in process without an index and is documented as less suited to very large stores. The tool catalogue lists target latency classes and a telemetry tool, while the README describes optional OTLP telemetry. These are code/documentation observations; no timings, resource use, or telemetry were collected in this review. ([PostgreSQL schema](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_schema.py), [PostgreSQL search](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_store_search.py), [tool catalogue](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/mcp-tools.md), [README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md))

## Metric-domain evidence

All project benchmark metrics are **unmeasured** for Cortex. Source inspection and upstream-reported evaluations are not results from this project. ([metric definitions](../METRICS.md), [project result status](../results/initial-baselines-status.json), [fixture, not run](../fixtures/memory-benchmark-v1.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Hybrid retrieval and a source-visible abstention gate exist; no answer or abstention workload was run. |
| Correction accuracy and stale-value rate | Unmeasured | Explicit supersession and consolidation paths are documented; no correction probes were adjudicated. |
| Deletion leakage | Unmeasured | Soft and hard deletion paths exist; no post-deletion recall or physical-storage checks were run. |
| Scope isolation | Unmeasured | Project-directory filtering and global-memory behavior are visible in code; no cross-project leakage workload was run. |
| Evidence support and citation coverage | Unmeasured | Reference resolvability and source attribution are implemented; no generated claims or citations were scored. |
| Retrieval latency | Unmeasured | No timing samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write/recall probes were run. |
| Tokens and cost | Unmeasured | No provider usage or charges were collected. |
| Storage efficiency | Unmeasured | No corpus-attributed logical or physical storage size was collected. |

The repository README reports retrieval evaluations and limits their interpretation to retrieval under the named setup; those upstream claims were not independently rerun and are not project benchmark results. ([README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md))

## Limits and unknowns

This bounded review inspected the README, architecture and API documentation, MCP catalogue, PostgreSQL schema, remember/recall/forget handlers, project-scope predicate, PostgreSQL search, and erasure implementation. It did not trace every store operation, backend-specific divergence, hook, model adapter, or auxiliary subsystem. ([architecture](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/architecture.md), [API reference](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/api-reference.md), [schema](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_schema.py))

No Cortex runtime, tests, or benchmarks were run. This review therefore does not establish runtime correctness, retrieval or abstention quality, scope isolation across every tool, complete physical erasure, latency, write-to-recall delay, token/cost totals, or storage efficiency. PostgreSQL’s hard deletion leaves physical reclamation to vacuum; the README describes SQLite’s search as unindexed and potentially slower at very large scale. ([forget handler](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/handlers/forget.py), [PostgreSQL erasure](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_store_erasure.py), [README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md), [metric definitions](../METRICS.md))

## Contact

The official pinned README publishes admin@ai-architect.tools in its contact section. This review used only official repository documentation for contact lookup; no commit/profile metadata or third-party directory was used. ([README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md))

## Benchmark status

**Benchmark not run.** Cortex, its tests, and benchmark workloads were not run. The project fixture is a workload specification only; the shared status record contains no Cortex measurements. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortex-hypermnesia.md)
- [Official repository](https://github.com/cdeust/Cortex)
- [Official main commit feed](https://github.com/cdeust/Cortex/commits/main.atom)
- [Reviewed full head b9e9c36f24abfa779282ce8accba0695306a3e77](https://github.com/cdeust/Cortex/commit/b9e9c36f24abfa779282ce8accba0695306a3e77)
- [Pinned README](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/README.md)
- [Pinned architecture documentation](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/architecture.md)
- [Pinned API reference](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/api-reference.md)
- [Pinned MCP tool catalogue](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/docs/mcp-tools.md)
- [Pinned PostgreSQL schema](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_schema.py)
- [Pinned remember handler](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/handlers/remember.py)
- [Pinned recall handler](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/handlers/recall.py)
- [Pinned forget handler](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/handlers/forget.py)
- [Pinned project scope predicate](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_scope_clause.py)
- [Pinned PostgreSQL search](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_store_search.py)
- [Pinned PostgreSQL erasure](https://github.com/cdeust/Cortex/blob/b9e9c36f24abfa779282ce8accba0695306a3e77/mcp_server/infrastructure/pg_store_erasure.py)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
