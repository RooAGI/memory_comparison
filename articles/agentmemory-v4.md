# agentmemory V4 source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 24 / agentmemory V4 / agentmemory-v4  
**Listed repository locator:** [jordanmccann/agentmemory](https://github.com/JordanMcCann/agentmemory)  
**Current canonical repository:** [JordanMcCann/agentmemory](https://github.com/JordanMcCann/agentmemory)  
**Default branch / reviewed head:** main / `3aa3b8389896f81dd813fdf9176ef3ca122d809e`  
**Review time:** 2026-11-24 19:04:35 UTC (11:04:35 PST; America/Los_Angeles).

## Identity and scope

The curated order places **agentmemory V4** at ordinal 24 with slug `agentmemory-v4` and listed repository locator `https://github.com/JordanMcCann/agentmemory`. The roster retains attribution to Agent Memory Atlas revision `19199a4fc249e89c0793be06f0b166b358089ba0`; that metadata is used only to identify and attribute the listed locator. Atlas descriptions, marks and layout were not used as assessment evidence.[[curated roster](../data/memory-systems.json)] [[Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agentmemory-v4.md)]

The official GitHub repository identifies the canonical public repository and default branch `main`. The branch history and commit page identify the reviewed head as `3aa3b8389896f81dd813fdf9176ef3ca122d809e`; the commit page shows it as the current root commit with no parents. Review time is 2026-11-24 19:04:35 UTC (11:04:35 PST; America/Los_Angeles).[[repository](<https://github.com/JordanMcCann/agentmemory>)] [[main history](<https://github.com/JordanMcCann/agentmemory/commits/main>)] [[reviewed head](<https://github.com/JordanMcCann/agentmemory/commit/3aa3b8389896f81dd813fdf9176ef3ca122d809e>)]

The README describes a Python memory library with a `MemoryStore` API and REST and MCP interfaces. It names Jordan McCann as the author. The observations below are limited to the README and selected code at the reviewed SHA; README statements and implementation details are identified separately.[[README](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/README.md>)]

## Architecture and data model

**Code observation.** `MemoryStore` is async-first and provides synchronous wrappers. Its component wiring includes storage, an embedding abstraction, ANN retrieval, a relationship graph, extraction, consolidation, validation, importance, calibration, feedback, and lineage. SQLite is the default backend; a backend can be injected, and the README documents PostgreSQL as an option.[[core.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/core.py?plain=1>)][[SQLite backend](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/storage/sqlite_backend.py?plain=1>)][[README](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/README.md>)]

**Code observation.** `MemoryNode` stores content, kind/tier, IDs, creation/access and event times, importance, confidence, embedding, metadata, provenance, namespace, parent and supersession links, tags, version, validity bounds, and media fields. `Namespace` has org, team, agent, and session dimensions. `Provenance` can store a source, session, turn, agent, tool call, document, parent role, and extraction method.[[models.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/models.py?plain=1>)]

**Documentation observation.** The README describes dense embeddings when the optional package is available, with a TF-IDF fallback, HNSW approximate nearest-neighbor retrieval, and optional cross-encoder reranking. It documents in-memory SQLite per case for its evaluation setup; that configuration is distinct from the default persistent SQLite deployment.[[README](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/README.md>)][[ANN index](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/ann_index.py?plain=1)]

## Write, update, delete, and retrieval

**Write — code and documentation observations.** The API exposes direct add, conversation ingestion, and document ingestion. The README describes extraction, classification, automatic graph construction, and optional streaming consolidation on write. REST also exposes update by node ID and delete by node ID; MCP provides add, conversation/document ingestion, delete, feedback and consolidation tools.[[README](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/README.md>)][[core.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/core.py?plain=1>)][[REST API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/server.py?plain=1>)][[MCP API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/mcp.py?plain=1>)]

**Update and consolidation — code observation.** Consolidation includes duplicate merging and supersession; retrieval excludes superseded records by default. The README additionally describes promotion between memory tiers, contradiction handling, confidence decay, and importance evolution. The selected inspection does not establish correction accuracy across all contradictory or corrected-fact cases.[[consolidation.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/consolidation.py?plain=1>)][[retrieval.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/retrieval.py?plain=1>)][[README](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/README.md>)]

**Delete — code observation.** The user deletion path selects records by source identifier, removes their edges and graph/ANN references, deletes nodes from storage, removes full-text references, redacts matching audit entries, and returns a deletion receipt. This inspected path does not establish removal from backups or external systems.[[gdpr.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/gdpr.py?plain=1>)][[SQLite backend](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/storage/sqlite_backend.py?plain=1>)]

**Retrieval — code observation.** Query scoring combines semantic similarity, BM25 lexical search, activation, graph spreading activation, importance/confidence, and temporal proximity. Query filters include kinds, tiers, tags, source, session, namespace, confidence and importance thresholds, supersession, validity, and time bounds. REST and MCP can build token-budgeted context; REST returns result scores and explanations. These interfaces do not establish retrieval quality or latency.[[retrieval.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/retrieval.py?plain=1>)][[graph.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/graph.py?plain=1>)][[REST API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/server.py?plain=1>)][[MCP API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/mcp.py?plain=1>)]

## Scope isolation, provenance, and evidence

Namespace dimensions are represented in the node model and retrieval can filter by a namespace. The inspected REST and MCP request shapes do not demonstrate authenticated tenant isolation. No cross-scope probes or deployment authorization review were performed.[[models.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/models.py?plain=1>)][[retrieval.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/retrieval.py?plain=1>)][[REST API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/server.py?plain=1>)][[MCP API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/mcp.py?plain=1>)]

Provenance fields, lineage, audit history, and deletion receipts provide source and lifecycle traceability. They do not establish that retrieved evidence entails a generated answer or that answers include claim-level citations.[[models.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/models.py?plain=1>)][[core.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/core.py?plain=1>)][[REST API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/server.py?plain=1>)][[MCP API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/mcp.py?plain=1>)]

## Source-visible efficiency and observability

**Code observation.** Retrieval uses HNSW candidate search with a configurable bound, a query cache, and bounded graph spreading. The SQLite backend uses WAL mode, a single-worker executor, and batch persistence methods. These are design observations, not measured performance or resource use.[[retrieval.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/retrieval.py?plain=1>)][[ANN index](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/ann_index.py?plain=1>)][[graph.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/graph.py?plain=1>)][[SQLite backend](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/storage/sqlite_backend.py?plain=1)]

The REST and MCP interfaces expose stats and health; REST additionally exposes history, calibration, drift and lineage endpoints. No runtime traces, latency distributions, provider charges, token totals, or storage measurements were collected.[[REST API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/server.py?plain=1>)][[MCP API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/mcp.py?plain=1>)]

## Project metric domains

Every project benchmark domain is **unmeasured** in this review. Code exposes retrieval and optional calibration mechanisms, but no answerable-recall, abstention, correction, stale-value, deletion-leak, scope-leak, citation-support, or citation-coverage probes were run. No retrieval latency, write-to-recall delay, token/cost total, or corpus storage measurement was collected. Project definitions and fixtures describe protocols, not system results.[[metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded inspection of the official README and selected source files at the verified upstream SHA. The system, tests, and benchmarks were not run. Production reliability, answer quality, tenant authorization, complete deletion beyond inspected stores and indexes, runtime performance, cost, and storage remain unverified.[[README](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/README.md>)][[core.py](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/core.py?plain=1>)][[REST API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/server.py?plain=1>)][[GDPR pipeline](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/gdpr.py?plain=1>)]

The upstream README includes a LongMemEval report. This review did not execute or independently reproduce it; it is not a result from this project's benchmark run. Project benchmark status remains `not_run`.[[README](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/README.md>)][[project status](../results/initial-baselines-status.json)]

## Contact-list follow-up

I checked the official repository README for a published contact email. It links to a personal profile but does not publish an email address. The JSON record stores `contact_email: null` and the exact pinned README URL that was checked.[[official README](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/README.md>)]

## Benchmark status

**Benchmark not run.** No agentmemory execution, project fixture run, benchmark, or tests were performed. Source and documentation observations are not measured results. The project metric definitions, fixture, and execution-status record remain separate protocol artifacts.[[metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Canonical public repository](<https://github.com/JordanMcCann/agentmemory>)
- [Reviewed main branch head](<https://github.com/JordanMcCann/agentmemory/commit/3aa3b8389896f81dd813fdf9176ef3ca122d809e>)
- [Official README](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/README.md>)
- [Memory data model](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/models.py?plain=1>)
- [MemoryStore](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/core.py?plain=1>)
- [Retrieval](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/retrieval.py?plain=1>)
- [REST API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/server.py?plain=1>)
- [MCP API](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/mcp.py?plain=1>)
- [SQLite backend](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/storage/sqlite_backend.py?plain=1>)
- [Relationship graph](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/graph.py?plain=1>)
- [Consolidation](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/consolidation.py?plain=1>)
- [User deletion pipeline](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/gdpr.py?plain=1>)
- [ANN index](<https://github.com/JordanMcCann/agentmemory/blob/3aa3b8389896f81dd813fdf9176ef3ca122d809e/agentmemory/ann_index.py?plain=1>)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated identity and source attribution](../data/memory-systems.json)

**Verification boundary:** no agentmemory system, tests, or benchmark workload was run.
