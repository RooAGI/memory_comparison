# CortexDB

## Identity and review pin

- Catalog ordinal: 163
- System: CortexDB
- Slug: `cortexdb`
- Listed repository: https://github.com/liliang-cn/cortexdb
- Roster attribution: explicit repository locator; the pinned Atlas report is used only for curated identity/locator context ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortexdb.md)).
- Canonical upstream: https://github.com/liliang-cn/cortexdb
- Default branch: `main`
- Reviewed full head: [0c6b7b98285a63125328dea95b8fe32f6d182d0d](https://github.com/liliang-cn/cortexdb/commit/0c6b7b98285a63125328dea95b8fe32f6d182d0d)
- Review timestamp: 2026-11-25T09:46:24Z (UTC; 2026-11-25 01:46:24 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

CortexDB is a Go memory and knowledge-graph library with MCP and gRPC interfaces. Its default storage is a SQLite database that combines scoped memories, knowledge documents and chunks, vectors, full-text indexes, and graph data. PostgreSQL is also supported. This review is pinned to the verified current `main` head; it is a source assessment, not a runtime or benchmark assessment. ([README](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/README.md), [architecture overview](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/docs/PROJECT_OVERVIEW.md))

## Who and what

The official project overview names Liang Li as creator and describes CortexDB as a pure-Go, single-file agent memory and knowledge graph library. The README presents both an embeddable Go API and service integrations for MCP/gRPC clients. ([project overview](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/docs/PROJECT_OVERVIEW.md), [README](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/README.md))

The official repository page identifies `main` as the default branch. Its main commit feed reports the current full head as `0c6b7b98285a63125328dea95b8fe32f6d182d0d`, updated at 2026-11-25T02:41:10Z. A fresh `git ls-remote --symref` and a shallow checkout independently matched that full SHA. ([repository](https://github.com/liliang-cn/cortexdb), [main commit feed](https://github.com/liliang-cn/cortexdb/commits/main.atom), [reviewed commit](https://github.com/liliang-cn/cortexdb/commit/0c6b7b98285a63125328dea95b8fe32f6d182d0d))

## Architecture and data model

The project overview describes a layered Go architecture: core storage/indexing and graph engines, a public `pkg/cortexdb` facade, memoryflow and graphflow workflow packages, and MCP/gRPC integration surfaces. SQLite is the default engine; the README documents PostgreSQL as another supported backend. ([architecture overview](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/docs/PROJECT_OVERVIEW.md), [README](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/README.md))

A memory record is stored as a message row with an ID, content, vector, bucket/session identifier, role, metadata, and creation time. Metadata can include scope, namespace, importance, expiry, writer/update information, evidence grade, and supersession markers. Knowledge records hold document text and metadata such as title, source URL, author, collection, chunk IDs, entities, and timestamps. Ingestion creates document/chunk and graph relationships for searchable source material. ([memory API](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_api.go), [knowledge types](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/knowledge_memory_types.go), [document ingestion](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/graphrag_tool_ingest.go))

The `KnowledgeMemory` facade composes memory search, knowledge search, graph facts and bounded context packing. Retrieval can use lexical indexes, an embedder-backed vector path, graph expansion or PPR; the project overview states that lexical retrieval remains available without an embedder. ([facade](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/brain.go), [memory search](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_api.go), [architecture overview](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/docs/PROJECT_OVERVIEW.md))

## Write, update, delete, and retrieval

**Memory writes and updates.** `SaveMemory` requires an ID and nonempty content, redacts recognized credential patterns, validates an optional evidence grade, resolves a global/user/session bucket and namespace, embeds content when configured, and upserts the row. Explicit `supersedes` IDs are marked as replaced. `UpdateMemory` updates content and metadata fields and refreshes the vector when content changes. ([memory API](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_api.go), [grade rules](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_grade.go))

**Memory correction and deletion.** A correction can be represented by saving a replacement with an explicit supersession relation: the prior row remains stored with replacement ID and time, while current recall filters it out; the replacement chain can be retrieved, including as-of history. `DeleteMemory` removes the message row and retracts its associated graph node. These are source-visible operations; this review did not execute them or verify erasure from backups or storage media. ([memory API](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_api.go), [supersession](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_supersession.go))

**Knowledge writes and deletion.** Knowledge records support partial updates, expiry and review decisions. Document ingestion stores source metadata and chunk identities; changing an ingested document retires trailing obsolete chunks. Document-graph deletion uses a transaction to remove document-specific edges and nodes, detach entities that have other source documents, and synchronize deleted graph node IDs after commit. ([knowledge API](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/knowledge_api.go), [knowledge types](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/knowledge_memory_types.go), [ingestion](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/graphrag_tool_ingest.go), [document graph deletion](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/graphrag_tool_delete_document.go))

**Retrieval.** Memory search resolves the requested bucket, retrieves lexical candidates and, when configured, vector candidates; entity hints can route through the graph. Shared facade recall can combine memory, knowledge and graph facts into a context pack. Search also applies expiry, supersession, as-of, review and minimum-grade filters. The lexical search tool applies collection filters and returns source chunks. ([memory API](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_api.go), [facade](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/brain.go), [search tool](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/graphrag_tool_search.go))

## Scope isolation

Memory scope is represented by global, user or session buckets and an optional namespace. Search resolves these values to a bucket before querying. A `CallerScope` attached by an authenticated server can restrict memory buckets and knowledge collections; without it, embedded library calls are not checked. The source also documents paths such as direct database listings, change feeds and chunk readers that are outside this facade-level guard and depend on the serving ports to refuse or constrain access. Effective isolation therefore depends on how a server wires caller identity and guards each exposed operation. No isolation workload was run. ([memory API](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_api.go), [caller scope](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_owner.go))

## Provenance and evidence

Memory records can carry grades `verified`, `self_consistent`, `asserted`, `held`, or `refused`; selected grades require a reason, and callers can set a minimum grade for retrieval. Knowledge records preserve source URL/author/metadata and chunk IDs. Relation provenance can expose the originating document and chunk IDs, whether a fact was inferred and by which rule, and optionally supporting chunk text; missing source chunks are reported instead of silently omitted. These mechanisms preserve provenance, but this review did not adjudicate generated claims against evidence. ([memory grade](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_grade.go), [knowledge types](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/knowledge_memory_types.go), [fact provenance](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/fact_provenance.go))

## Efficiency and observability

The implementation provides lexical and vector indexes, concurrent lexical/vector memory retrieval, bounded context packing, retrieval explain records with candidate scores and drop reasons, and explicit degraded-mode reasons when a retrieval arm fails. MCP calls carry request IDs and W3C trace context. An opt-in recall log stores queries and results with configurable retention and row limits; it is disabled unless requested. These source-visible mechanisms are not measured latency, cost, token, or storage outcomes. ([memory API](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_api.go), [facade](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/brain.go), [recall explain](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/recall_explain.go), [recall log](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/recall_log.go), [MCP tracing](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/mcp_call.go))

## Metric-domain evidence

All project benchmark domains are **unmeasured** for this review. The metric definitions, fixture and existing status record were read as project contract/status documents only; no fixture or benchmark was executed. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Search mechanisms were inspected; no answers were scored. |
| Correction accuracy and stale-value rate | Unmeasured | Update and explicit supersession mechanisms were inspected; no correction probes were run. |
| Deletion leakage | Unmeasured | Memory and document graph deletion code was inspected; no post-delete probes were run. |
| Scope isolation | Unmeasured | Bucket, collection and caller-scope code was inspected; no cross-scope workload was run. |
| Evidence support and citation coverage | Unmeasured | Grade and provenance paths were inspected; no claims were adjudicated. |
| Retrieval latency | Unmeasured | No latency samples were collected. |
| Write-to-recall delay | Unmeasured | No timed probes were run. |
| Tokens and cost | Unmeasured | No usage or charges were measured. |
| Storage efficiency | Unmeasured | No corpus storage size was measured. |

## Limits and unknowns

This bounded review inspected the official README and architecture overview, selected memory and knowledge APIs, document ingestion/deletion, caller-scope code, grade/provenance behavior, recall explanation/logging and trace middleware. It did not inspect every server adapter, storage migration, deployment configuration, embedder, or graph path. Source inspection cannot establish the deployed authorization configuration or runtime quality, isolation, deletion completeness, latency, cost or storage efficiency. ([README](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/README.md), [architecture overview](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/docs/PROJECT_OVERVIEW.md), [caller scope](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_owner.go), [project metric definitions](../METRICS.md))

The official README was checked for contact information; it publishes no contact email. No commit/profile metadata or third-party directory was used. ([README](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/README.md))

## Benchmark status

**Benchmark not run.** No CortexDB runtime, tests or benchmarks were run. Source observations and upstream documentation statements are separate from measured results. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortexdb.md)
- [Official repository](https://github.com/liliang-cn/cortexdb)
- [Official main commit feed](https://github.com/liliang-cn/cortexdb/commits/main.atom)
- [Reviewed head 0c6b7b98285a63125328dea95b8fe32f6d182d0d](https://github.com/liliang-cn/cortexdb/commit/0c6b7b98285a63125328dea95b8fe32f6d182d0d)
- [Pinned README](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/README.md)
- [Pinned architecture overview](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/docs/PROJECT_OVERVIEW.md)
- [Pinned memory API](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_api.go)
- [Pinned knowledge-memory facade](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/brain.go)
- [Pinned knowledge types](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/knowledge_memory_types.go)
- [Pinned knowledge API](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/knowledge_api.go)
- [Pinned document ingestion](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/graphrag_tool_ingest.go)
- [Pinned GraphRAG search tool](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/graphrag_tool_search.go)
- [Pinned document graph deletion](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/graphrag_tool_delete_document.go)
- [Pinned caller scope](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_owner.go)
- [Pinned evidence grade rules](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_grade.go)
- [Pinned supersession chain](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/memory_supersession.go)
- [Pinned fact provenance](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/fact_provenance.go)
- [Pinned recall explanation](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/recall_explain.go)
- [Pinned recall log](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/recall_log.go)
- [Pinned MCP trace middleware](https://github.com/liliang-cn/cortexdb/blob/0c6b7b98285a63125328dea95b8fe32f6d182d0d/pkg/cortexdb/mcp_call.go)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project result/status record](../results/initial-baselines-status.json)

---