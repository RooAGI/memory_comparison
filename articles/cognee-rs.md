# Cognee-RS — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 135 — Cognee-RS / `cognee-rs`  
**Listed repository:** [topoteretes/cognee-rs](https://github.com/topoteretes/cognee-rs)  
**Canonical upstream:** same repository; default branch `main`; reviewed head [a70bcab30059b674b98822a7bdff1570a69dfeb7](https://github.com/topoteretes/cognee-rs/commit/a70bcab30059b674b98822a7bdff1570a69dfeb7)  
**Review time:** 2026-11-25 08:32:09 UTC (2026-11-25 00:32:09 PST; America/Los_Angeles)

## Identity and scope

The catalog places Cognee-RS at ordinal 135, with slug `cognee-rs`, explicit listed repository locator, and a pinned Atlas attribution. The Atlas entry is retained only for curated identity and locator attribution, not as assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cognee-rs.md)]

The official repository page shows `main` as the default branch. GitHub’s official main commit feed reports full head `a70bcab30059b674b98822a7bdff1570a69dfeb7`, updated 2026-11-25T08:02:24Z. The reviewed documentation and code links below pin that commit.[[repository](https://github.com/topoteretes/cognee-rs)] [[main commit feed](https://github.com/topoteretes/cognee-rs/commits/main.atom)] [[reviewed head](https://github.com/topoteretes/cognee-rs/commit/a70bcab30059b674b98822a7bdff1570a69dfeb7)]

The README describes Cognee-RS as a Rust port of the Python Cognee library. It is a library and CLI with JavaScript/TypeScript, Python, C, and Java bindings. The HTTP server is referenced in documentation but is not part of this repository.[[README](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/README.md)] [[architecture](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/architecture.md)]

## Architecture and data model

Cognee-RS composes an add/ingest stage, cognify knowledge-graph construction, and search. The high-level memory API exposes `remember`, `recall`, `improve`, and `forget`. Cognify classifies and chunks documents, extracts entities and relationships, summarizes, then persists graph and vector data.[[architecture](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/architecture.md)] [[operations](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/operations.md)]

The system uses three complementary stores: relational storage for document tracking, datasets, sessions, and lineage; a graph store for entities and relationships; and vector storage for semantic search over chunks, entities, summaries, and edge facts. The documented defaults are SQLite, embedded Ladybug, and LanceDB. Other providers and backends are selectable by configuration and features.[[concepts](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/concepts.md)] [[README](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/README.md)]

A DataPoint is the shared record base: it includes identifiers, timestamps, version/type fields, metadata, dataset membership, and pipeline provenance such as source pipeline, task, node set, and source content hash. Cognify routes writes through a persistence layer that records ownership rows, graph and vector artifacts, and edge evidence, deduplicating shared writes across document groups.[[DataPoint model](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/models/src/data_point.rs)] [[persistence](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/cognify/src/persist.rs)] [[provenance IDs](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/database/src/provenance_ids.rs)]

## Write, update, delete, and retrieval

**Write.** `remember` adds input, runs cognify, then normally runs an improvement pass. Ingestion hashes and deduplicates sources. Cognify processes documents in bounded streams and writes each finished document group through one ordered writer. A separate deterministic code-repository route builds code graphs without LLM extraction.[[operations](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/operations.md)] [[architecture](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/architecture.md)] [[persistence](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/cognify/src/persist.rs)]

**Update and correction.** The documented update path replaces a document while retaining its data ID, removes its previous derived memory, re-adds the document and cognifies it again. Improve supports feedback-based enrichment and personalization. These operations describe mutation paths; they do not establish correction accuracy or rule out all stale derived results.[[operations](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/operations.md)]

**Delete.** Forget/delete offers whole-owner, dataset, or data-item targets and cascades through relational, graph, vector, and file storage; a dry-run preview is documented. Failed-run sweeps remove run-owned artifacts, while shared artifacts remain when another owner still claims them. This is source-visible behavior, not an end-to-end deletion guarantee.[[README](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/README.md)] [[operations](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/operations.md)] [[delete service](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/delete/src/lib.rs)] [[provenance IDs](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/database/src/provenance_ids.rs)]

**Retrieval.** Recall auto-routes among strategies when no type is specified. The default hybrid search combines vector candidates with one-hop graph-neighborhood expansion and an LLM completion. Recall can use graph and session scopes or return retrieved context without generated completion when no LLM is configured. Some modes have higher costs; documented batch triplet retrieval loads the whole graph or selected subgraph without a candidate limit.[[operations](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/operations.md)] [[recall scope](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/search/src/recall_scope.rs)]

## Scope isolation

Datasets provide the main organizational and ownership scope and can be tenant-scoped. Data and DataPoints carry dataset membership. Session memory is keyed by owner; configured bindings can use readable-dataset hooks to read another session owner’s entries. The docs describe node sets as partially implemented tagging and type/name subgraph selection, not a general query surface. These abstractions do not alone establish tenant isolation for every deployment; the host and selected API path matter.[[concepts](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/concepts.md)] [[operations](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/operations.md)] [[recall scope](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/search/src/recall_scope.rs)]

## Provenance and evidence

DataPoint provenance fields and relational ownership rows preserve which pipeline, task, dataset, and input item produced graph artifacts. Edges can also carry evidence. These mechanisms support lineage, deletion, and rollback, but do not guarantee answer-level citations or that a generated claim is supported by the recalled source.[[DataPoint model](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/models/src/data_point.rs)] [[persistence](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/cognify/src/persist.rs)] [[provenance IDs](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/database/src/provenance_ids.rs)]

## Efficiency and observability

The code and docs describe bounded concurrent extraction, per-document persistence, incremental cognify completion markers, and local embedded stores. OpenTelemetry tracing instruments pipeline stages when enabled and activated; structured logs are also available. The README’s boot and search timings are upstream-reported claims, not independently measured observations in this review.[[architecture](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/architecture.md)] [[operations](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/operations.md)] [[OpenTelemetry guide](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/observability/opentelemetry.md)] [[README](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/README.md)]

## Metric-domain evidence

All items here are source observations or unmeasured domains; no runtime results were collected.[[metric definitions](../METRICS.md)]

- **Answerable recall and abstention — unmeasured.** Retrieval modes and context-only fallback are documented, but no gold cases were run or adjudicated.[[operations](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/operations.md)]
- **Correction and staleness — unmeasured.** Update replaces and re-cognifies a data item, but no post-correction probes were run.[[operations](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/operations.md)]
- **Deletion leakage — unmeasured.** Cascading deletion is implemented, but no post-delete leak checks were performed.[[delete service](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/delete/src/lib.rs)]
- **Scope isolation — unmeasured.** Dataset and session scope appear in docs and source, but no cross-scope workload was executed.[[concepts](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/concepts.md)] [[recall scope](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/search/src/recall_scope.rs)]
- **Evidence support and citation coverage — unmeasured.** Provenance and edge evidence exist; no answer-level support audit was performed.[[persistence](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/crates/cognify/src/persist.rs)]
- **Retrieval latency — unmeasured.** README speed figures were not independently reproduced.[[README](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/README.md)]
- **Write-to-recall delay — unmeasured.** No timed write-then-recall workload was run.[[metric definitions](../METRICS.md)]
- **Tokens and cost — unmeasured.** No provider usage or cost accounting was performed.[[metric definitions](../METRICS.md)]
- **Storage efficiency — unmeasured.** No corpus-size measurement was collected.[[metric definitions](../METRICS.md)]

## Limits and unknowns

This review inspected the pinned README, architecture, concepts and operations guides, DataPoint model, cognify persistence, recall scope, deletion and provenance code, and observability guide. It does not cover every feature, provider, backend, language binding, or error path. The README states that cross-process locking for file-backed graph storage is out of scope; node-set querying is described as partial. Behavior under other configurations requires separate review.[[README](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/README.md)] [[concepts](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/concepts.md)] [[architecture](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/docs/architecture.md)]

No Cognee-RS runtime, tests, or benchmarks were run. Retrieval quality, abstention, correction accuracy, full deletion compliance, scope isolation, latency, write-to-recall delay, token/cost use, and storage efficiency remain unknown. The project fixture describes planned cases, not results.[[fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark status](../results/initial-baselines-status.json)] [[metric definitions](../METRICS.md)]

## Contact

The official pinned README and SECURITY.md were checked. SECURITY.md publishes `info@topoteretes.com` for private vulnerability reporting; that exact official source is recorded in the JSON review record.[[README](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/README.md)] [[security policy](https://github.com/topoteretes/cognee-rs/blob/a70bcab30059b674b98822a7bdff1570a69dfeb7/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No benchmark or tests were run for this assessment. See the [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).