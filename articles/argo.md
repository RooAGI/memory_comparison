# ARGO

## Identity and review pin

- **Curated position:** 69 in `data/memory-systems.json`
- **Listed name / slug:** ARGO / `argo`
- **Listed repository locator:** https://github.com/derekhu0002/Argo
- **Canonical repository:** https://github.com/derekhu0002/Argo
- **Default branch:** `main`
- **Reviewed head:** [`607a1c1dd0cd310fdfcb1ae8f060f01675142a7b`](https://github.com/derekhu0002/Argo/commit/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b)
- **Reviewed:** 2026-11-24 21:35:08 UTC (13:35:08 PST; America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The curated roster establishes the name, slug, listed locator, and Atlas attribution. I used the Atlas link only for those identity fields; its descriptions, marks, and layout are not assessment evidence. The official repository page identifies `main` as the default branch and displayed latest commit `607a1c1`; the official commit page confirms the full SHA above. Reviewed repository file links below pin to that SHA. [[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/derekhu0002/Argo)] [[reviewed commit](https://github.com/derekhu0002/Argo/commit/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b)] [[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/argo.md)]

## Summary

ARGO is a repository-centered software delivery framework that uses an ArchiMate knowledge graph as durable project context. A canonical JSON architecture document is validated and read through MCP; Neo4j and its vector indexes act as derived semantic projections for query and context assembly. This is a source review of the pinned revision, not an execution or benchmark assessment. [[README](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/README.md)] [[architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/OVERALL_ARCHITECTURE.md)] [[Neo4j projection](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/neo4j-system-architecture-store.js)]

## Who and what

The official repository account is `derekhu0002`; the README presents ARGO as an agent-loop framework spanning requirements, design, development, testing, and delivery archival, with human-in-the-loop and agent-led delivery modes. This review treats the repository as a framework with a project knowledge subsystem, not as a standalone memory database or hosted service. [[official repository](https://github.com/derekhu0002/Argo)] [[README](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/README.md)]

## Architecture and data model

**Canonical record.** The repository identifies `design/KG/SystemArchitecture.json` as the authoritative graph. Its schema requires a graph name and description plus non-empty arrays of Elements, ArchitectureRelationships, and Views. Elements use ArchiMate element types; relationships carry type and source/target IDs; Views contain metadata and included element/relationship IDs. Optional object fields include descriptions, attributes, test cases, and documents, but the schema does not require a general source URL or author field on every fact. [[top-level architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/OVERALL_ARCHITECTURE.md)] [[graph schema](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/schema/SystemArchitecture.schema.json)]

**Projection.** The Neo4j adapter maps graph objects to `ArchitectureGraph`, `Element`, `ArchitectureRelationship`, and `View` nodes, preserving raw object JSON and selected searchable properties. It keys records by a graph key derived from the architecture path, adds typed relationship and View-membership edges, and keeps local sync state with dirty/error timestamps and last verified counts. Neo4j remains subordinate projection state; canonical JSON remains authoritative. [[Neo4j graph store](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/neo4j-system-architecture-store.js)] [[graph-RAG architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/ARCHITECTURE.md)]

**Semantic index.** The reviewed retrieval contract separates Element, ArchitectureRelationship, and View channels, each with its own vector index and score threshold. Versioned semantic records and persistent readiness evidence bind provider/model metadata and index state back to canonical/content versions. The docs specify a Node.js Neo4j-driver path and external credential configuration; they do not make vector data canonical. [[semantic retrieval implementation](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/defaultSemanticRetrieval.js)] [[graph-RAG architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/ARCHITECTURE.md)]

## Write, update, delete, and retrieval

**Write and update.** The public architecture boundary exposes `applySystemArchitectureMutation` after schema and graph-semantic validation. Successful changes update the canonical JSON graph; the projection path can synchronize that document to Neo4j. The current production semantic lifecycle is documented to consume the exact touched object IDs and upsert changed vectors only after a successful canonical write. Preview/dry-run and failed validation are not supposed to cause vector writes. [[MCP and mutation boundary](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/systemarchitecture-mcp-server.js)] [[graph schema](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/schema/SystemArchitecture.schema.json)] [[graph-RAG architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/ARCHITECTURE.md)]

**Projection refresh and removal.** The general Neo4j sync implementation clears nodes for the graph key and rebuilds its graph, element, relationship, View, and membership records from canonical JSON; its verification compares expected and actual counts and IDs and records sync status. The separate production semantic projection contract says changed identities are upserted and removals become tombstones. These mechanisms do not establish erasure from backups, provider logs, or other copies. [[Neo4j graph store](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/neo4j-system-architecture-store.js)] [[sync entry point](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/syncSystemArchitectureToNeo4j.js)] [[graph-RAG architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/ARCHITECTURE.md)]

**Retrieval.** The MCP read boundary preserves an exact full canonical snapshot for no-query reads and the graph-tidy purpose. Ordinary semantic requests pass through persistent readiness checks before embedding and vector queries. The implementation defines independent Element, ArchitectureRelationship, and View thresholds (0.80, 0.78, and 0.76); the contract requires threshold-all results using expanding windows, followed by deterministic purpose-specific graph closure and structural completion. An unaligned index is automatically reconciled and the original ordinary query is retried once; if alignment still cannot be established, retrieval fails closed with no full-snapshot fallback. [[MCP query boundary](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/systemarchitecture-mcp-server.js)] [[semantic retrieval implementation](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/defaultSemanticRetrieval.js)] [[graph-RAG architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/ARCHITECTURE.md)]

## Scope isolation

The graph store uses a `graphKey` based on the repository-relative architecture path, and graph/object uniqueness constraints include that key. Query purposes are explicit categories such as intent-decision, implementation-design, coding-repair, audit, and graph-tidy. The inspected contracts say caller identity is not a scope selector; the public query fields are purpose, intent, subject, and optional anchors. This provides graph/path organization and policy-specific context selection, but the inspected surface does not establish per-user or per-agent authorization isolation. [[Neo4j graph store](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/neo4j-system-architecture-store.js)] [[MCP query boundary](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/systemarchitecture-mcp-server.js)] [[top-level architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/OVERALL_ARCHITECTURE.md)]

## Provenance and evidence

Canonical objects have stable IDs and relationships reference source/target IDs. Semantic records and readiness track canonical, content, and index versions plus channel/provider/model details. The graph-RAG contract also requires returned context to include the governing versions, selected policy and parameters, anchors, and ordered first-inclusion reasons for graph objects. These are useful structural provenance signals. The schema does not require a claim-level citation or source-document lineage for each stored fact, so the presence of an object or query inclusion reason alone does not validate the truth of its content. [[graph schema](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/schema/SystemArchitecture.schema.json)] [[Neo4j graph store](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/neo4j-system-architecture-store.js)] [[graph-RAG architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/ARCHITECTURE.md)]

## Source-visible efficiency and observability

**Code observations, not measurements.** A semantic request resolves external configuration, checks durable readiness, obtains an embedding, and queries three vector channels. Each channel uses a separate index and an expanding window so qualifying peers beyond the initial window can be returned; this can entail multiple query windows when results continue. The graph store’s full sync rebuilds a graph key’s projection, while the incremental semantic lifecycle is specified for affected records. The store records sync dirty/success/recovery times and verified counts; readiness exposes state and canonical/content/index versions, completed/missing/mismatched channels, and stable error categories. No source-derived throughput or latency number is reported here. [[semantic retrieval implementation](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/defaultSemanticRetrieval.js)] [[Neo4j graph store](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/neo4j-system-architecture-store.js)] [[graph-RAG architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/ARCHITECTURE.md)]

## Metric-domain evidence

All domains below are **unmeasured** in this review. Entries describe code-visible mechanisms or missing evidence only.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Channel thresholds and fail-closed alignment gates are source-visible; no answer-quality or abstention cases were run. | Unmeasured |
| Correction accuracy and stale values | Canonical mutation and projection lifecycle are visible, but no correction accuracy or stale-value probe was run. | Unmeasured |
| Deletion leakage | Canonical removals, graph-key rebuild, and semantic tombstones are documented; no post-delete or copy-leak probe was run. | Unmeasured |
| Scope isolation | A path-derived graph key and purpose policies are visible; no cross-project, user, or agent isolation probe was run. | Unmeasured |
| Evidence support and citation coverage | Query results can carry graph identity, version, policy, and inclusion provenance; no fact-level evidence adjudication was run. | Unmeasured |
| Retrieval latency and write-to-recall delay | External embedding, readiness checks, vector windows, graph closure, and projection updates are visible; no timings were collected. | Unmeasured |
| Tokens, cost, and storage | The system uses provider embeddings and persistent Neo4j state; no token, provider-cost, or corpus-attributed storage measurements were collected. | Unmeasured |

Project metric definitions, the versioned fixture, and execution status describe proposed reporting and planned cases; they are not ARGO measurements. [[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This bounded inspection establishes source and contract behavior at the reviewed commit, not successful deployment or runtime behavior. It does not verify Neo4j/provider configuration, index readiness on a live database, vector quality, scope isolation, deletion completeness, write-to-recall delay, latency, token use, provider cost, or storage efficiency. The architecture documentation contains implementation requirements and delivery gates; their presence in a contract is not evidence that a production environment has satisfied them. The local sync path’s wholesale graph-key rebuild is visible, but its failure/recovery behavior under interruption was not exercised. [[README](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/README.md)] [[graph-RAG architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/ARCHITECTURE.md)] [[Neo4j graph store](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/neo4j-system-architecture-store.js)]

## Contact-list follow-up

I checked the official pinned [README](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/README.md) for a published contact email; it publishes none. The corresponding official [SECURITY.md](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/SECURITY.md) path returned GitHub’s “File not found” page at this revision. The record stores a null email and both checked URLs.

## Benchmark status

**Benchmark not run.** I did not execute ARGO, run benchmarks, or add or run tests. Source-visible thresholds, planned cases, and architecture acceptance requirements are not measured outcomes. See the [project metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json). [[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Curated roster entry](../data/memory-systems.json) — ordinal, name, slug, listed locator, and Atlas attribution only.
- [Atlas attribution entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/argo.md) — attribution only; not assessment evidence.
- [Official repository](https://github.com/derekhu0002/Argo) — canonical repository, owner account, and default branch.
- [Reviewed full commit](https://github.com/derekhu0002/Argo/commit/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b) — full revision; the repository page showed this short SHA as the latest main commit.
- [README](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/README.md)
- [Overall architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/OVERALL_ARCHITECTURE.md)
- [Graph schema](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/schema/SystemArchitecture.schema.json)
- [MCP and mutation boundary](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/systemarchitecture-mcp-server.js)
- [Neo4j graph store](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/neo4j-system-architecture-store.js)
- [Neo4j sync entry point](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/syncSystemArchitectureToNeo4j.js)
- [Semantic retrieval implementation](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/defaultSemanticRetrieval.js)
- [Graph-RAG architecture contract](https://github.com/derekhu0002/Argo/blob/607a1c1dd0cd310fdfcb1ae8f060f01675142a7b/.argo/scripts/graph-rag/ARCHITECTURE.md)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only repository and source review; no ARGO runtime, benchmark workload, build, or tests.
