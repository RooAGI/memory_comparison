# Cognee

## Identity and review pin

- **Catalog position:** 134, “Cognee”; slug `cognee`.
- **Listed repository:** [topoteretes/cognee](https://github.com/topoteretes/cognee); roster locator status is explicit. The pinned Atlas roster entry is recorded only for catalog identity and locator attribution.
- **Canonical upstream:** public GitHub repository [topoteretes/cognee](https://github.com/topoteretes/cognee), default branch `main`. `git ls-remote --symref` resolved HEAD to `refs/heads/main`; the remote `HEAD`, `refs/heads/main`, and shallow checkout all matched full head `1961133d0c68b450fe8e71941a756371e94f7c04`. The official [pinned commit page](https://github.com/topoteretes/cognee/commit/1961133d0c68b450fe8e71941a756371e94f7c04) identifies the reviewed full SHA.
- **Reviewed:** 2026-11-25 08:29:35 UTC (2026-11-25 00:29:35 PST; America/Los_Angeles).
- **Status:** Reviewed from current pinned upstream source and documentation. Benchmark not run.

## Summary

Cognee stages source documents, transforms them into chunk, graph, and vector representations, and retrieves context through selectable search strategies. The code also includes session memory, dataset permissions, optional provenance tracking, and OpenTelemetry instrumentation. This is a source review; no runtime or benchmark results were collected.[[Official README](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/README.md)] [[Cognee commit](https://github.com/topoteretes/cognee/commit/1961133d0c68b450fe8e71941a756371e94f7c04)]

## Who and what

The official README describes Cognee as an open-source AI memory platform for persistent agent memory. The Python API exposes `add`/`cognify` and `remember`/`recall`/`forget`; the README also links CLI, REST, MCP, and agent integrations. This review does not infer individual maintainer identity.[[README](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/README.md)] [[add API](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/add/add.py)] [[cognify API](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/cognify/cognify.py)] [[remember API](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/remember/remember.py)]

## Architecture and data model

Ingestion stages source files and text as dataset-scoped data records. `cognify()` chunks documents, extracts entities and relationships, and writes graph and vector indexes. The public `DataPoint` abstraction supports structured graph objects; `DocumentChunk` stores text, chunk position, content hash, source document identity, and metadata; `Entity` specializes the graph data model.[[ingestion](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/add/add.py)] [[cognify](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/cognify/cognify.py)] [[DataPoint](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/infrastructure/engine/models/DataPoint.py)] [[DocumentChunk](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/chunking/models/DocumentChunk.py)] [[Entity](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/engine/models/Entity.py)]

The unified `remember()` path combines ingestion and graph construction with optional improvement and session bridging. Memory is represented across relational metadata, original and processed documents, graph nodes and edges, and vector indexes; the configured adapters determine concrete stores.[[remember](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/remember/remember.py)] [[README architecture](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/README.md)]

At query time, `recall()` can search session entries or route requests to graph, vector, chunk, summary, temporal, and code retrieval. Results may be retrieved context or generated completions; optional evidence references identify source segments or graph artifacts.[[recall](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/recall/recall.py)] [[search](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/search/search.py)] [[evidence references](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/search/models/EvidenceReference.py)]

## Write, update, delete, and retrieval

**Write.** `add()` stages data in a dataset and `cognify()` creates searchable chunks and graph structures. `remember()` combines these operations and can request improvement/session distillation. The ingestion code matches identical content by hash within a dataset; changed documents use `update()`.[[add](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/add/add.py)] [[cognify](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/cognify/cognify.py)] [[remember](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/remember/remember.py)]

**Update.** `update()` replaces one document while retaining its `data_id`. When prerequisites hold, it diffs changed chunks; otherwise it falls back to dropping and rebuilding that document’s memory. The implementation documents failed rebuild and retry behavior; no update sequence was run.[[update implementation](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/update/update.py)]

**Delete.** `forget()` supports deleting one data item, a dataset, all datasets the user may delete, memory-only removal, and optional history cleanup. Memory-only mode keeps raw files and data rows for later re-cognification. The source warns that storage engines can retain deleted bytes until compaction or vacuum, so the API does not establish byte-level erasure.[[forget implementation](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/forget/forget.py)]

**Retrieval.** `recall()` accepts dataset filters, top-k, search type, graph-node scope, and session ID; automatic routing can select a strategy. Completion results can include source locators when references are requested. Different retrievers return different shapes, such as passages, graph context, summaries, or generated answers.[[recall](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/recall/recall.py)] [[search](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/search/search.py)] [[EvidenceReference](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/search/models/EvidenceReference.py)]

## Scope isolation

Datasets are the unit of permissions and processing. When backend access control is active, authorized search resolves readable datasets before running retrieval and binds database context per dataset. The code says access control is on by default, but it can be disabled by configuration and requires supported graph/vector adapters. Source inspection cannot establish which configuration a particular deployment uses or prove its runtime isolation.[[access-control context](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/context_global_variables.py)] [[authorized search](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/search/methods/search.py)] [[ingestion dataset permissions](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/add/add.py)]

## Provenance and evidence

When `PROVENANCE_TRACKING` is enabled, a storage hook writes data-item content hash, dataset-qualified identity, source reference, actor, and pipeline activity to a relational hash-chained ledger. Tracking is off by default. The ledger records source-item lineage rather than proving extracted facts are correct; evidence references are optional locators for artifacts used in retrieval.[[tracking switch](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/provenance/tracking.py)] [[provenance writer](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/tasks/provenance/record_provenance.py)] [[ledger manager](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/provenance/manager.py)] [[ledger storage](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/provenance/storage.py)] [[entry schema](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/provenance/models/ProvenanceEntry.py)] [[retrieval evidence](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/search/models/EvidenceReference.py)]

## Efficiency and observability

The code includes batched ingestion and chunk indexing, incremental update paths, query routing, and batched provenance-chain transactions. OpenTelemetry instruments can record operation durations and counts for stored/retrieved/deleted items, result counts, bytes, vector searches, graph changes, and errors. Metrics are no-ops until a meter is configured. The cloud product-telemetry contract is a separate profile with filtered operation metadata. No efficiency measurements were collected.[[add](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/add/add.py)] [[cognify](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/cognify/cognify.py)] [[update](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/update/update.py)] [[provenance transactions](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/provenance/storage.py)] [[metrics](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/observability/metrics.py)] [[observability](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/observability/__init__.py)] [[cloud telemetry contract](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/docs/cloud-telemetry-contract.md)]

## Metric-domain evidence

- **Answerable recall and abstention:** retrieval and query routing are source-visible; answerability and abstention were not measured.
- **Correction and stale values:** stable-ID updates and incremental/full rebuild paths are source-visible; no correction or staleness workload was run.
- **Deletion leakage:** logical deletion modes are documented, including residual storage-engine bytes; no post-delete retrieval or residual-copy check was run.
- **Scope isolation:** dataset authorization is applied before search when enabled; no cross-dataset or cross-tenant workload was run.
- **Evidence and citations:** optional evidence references and provenance records exist; no claim-to-source adjudication was run.
- **Latency:** OpenTelemetry duration instruments exist; no latency workload was run.
- **Write-to-recall delay:** staging and indexing are separate or composable operations; no searchable-after-write timing was measured.
- **Tokens and cost:** local and provider-backed model paths are documented; no token or provider-cost results were collected.
- **Storage efficiency:** document, chunk, graph, vector, and optional ledger structures are source-visible; no storage comparison was measured.

Project metric definitions are in [METRICS.md](../METRICS.md); the shared execution record is [initial-baselines-status.json](../results/initial-baselines-status.json). The [benchmark fixture](../fixtures/memory-benchmark-v1.json) describes a planned workload and is not a result.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Contact

The official pinned [SECURITY.md](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/SECURITY.md) publishes `security@cognee.ai` for vulnerability reports. The structured record stores that address and its exact official source URL.

## Limits and unknowns

Deletion does not promise physical erasure from storage-engine files; memory-only mode intentionally preserves raw records. Access-control behavior depends on runtime configuration and adapter support. The optional provenance ledger tracks item lineage, not factual truth, and neither provenance nor retrieval locators establish claim correctness.[[forget](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/api/v1/forget/forget.py)] [[access control](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/context_global_variables.py)] [[provenance](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/tasks/provenance/record_provenance.py)] [[evidence schema](https://github.com/topoteretes/cognee/blob/1961133d0c68b450fe8e71941a756371e94f7c04/cognee/modules/search/models/EvidenceReference.py)]

This review covers selected current source and documentation at the verified `main` head. It did not audit every adapter, loader, integration, or deployment; did not run Cognee or its tests; and does not establish live retrieval quality, isolation, latency, token usage, cost, or storage behavior.[[repository](https://github.com/topoteretes/cognee)] [[reviewed commit](https://github.com/topoteretes/cognee/commit/1961133d0c68b450fe8e71941a756371e94f7c04)]

## Benchmark status

**Benchmark not run.** No Cognee runtime, tests, or benchmark workloads were executed. This source assessment is not a measured result. See [project metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and the [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and pinned URLs are recorded in [cognee.json](../data/system-reviews/cognee.json). The [pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cognee.md) is included only as curated identity/locator attribution, not as assessment evidence.
