# AutoMem source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated position:** 84  
**Roster name / slug:** AutoMem / automem  
**Listed repository locator:** [verygoodplugins/automem](https://github.com/verygoodplugins/automem) (curated roster locator)  
**Current canonical repository:** [verygoodplugins/automem at reviewed commit](https://github.com/verygoodplugins/automem/tree/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2)  
**Default branch / reviewed head:** develop / `18569b4a1399c31dea3a8ec63c3082ab32f0dfb2`  
**Review time:** 2026-11-24 23:11:43 UTC (15:11:43 PST; America/Los_Angeles). GitHub repository metadata identified `develop` as the default branch; the official `commits/develop.atom` feed and latest commit page identified the full reviewed head.

## Identity and review pin

The curated roster places AutoMem at position 84 and lists the repository locator above. The roster and its pinned Atlas source are used only for the system name, slug, listed locator, and source attribution; Atlas descriptions and capability marks are not assessment evidence.[[curated roster](../data/memory-systems.json)]

## Summary

AutoMem is a self-hostable memory API for AI assistants that combines a FalkorDB graph as its canonical record with Qdrant vectors for semantic search. Its REST and MCP interfaces support storing and retrieving memories, with optional graph relations and background enrichment. This review describes the pinned source and documentation; it does not measure runtime quality or performance.

## Who and what

GitHub identifies the public repository owner as the `verygoodplugins` organization. The repository describes AutoMem as long-term memory for assistants and documents both a REST API and MCP integrations. It is a deployable service and integration stack, rather than only a client-side library.[[repository metadata](https://api.github.com/repos/verygoodplugins/automem)] [[README](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/README.md)] [[API reference](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/API.md)]

## Architecture and data model

**Source observation.** The README identifies FalkorDB as the graph store and canonical record, and Qdrant as the vector store containing embeddings. Graph nodes hold memories and typed edges connect them; the README lists semantic relationship types such as `RELATES_TO`, `LEADS_TO`, `CONTRADICTS`, and `DERIVED_FROM`. It also describes a degraded recall path when Qdrant is unavailable, while loss of the graph store makes the API unavailable.[[README](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/README.md)]

The documented memory API accepts content, tags, importance, type, confidence, timestamp, and metadata, with validity-window fields available on writes. A shared Qdrant payload builder carries content and its SHA-256 fingerprint, tags and tag prefixes, importance, timestamp, type, confidence, validity, archive state, update/access timestamps, metadata, and relevance score. The payload code shows how graph properties are copied into the vector index; it does not make the graph and vector writes one transaction.[[API reference](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/API.md)] [[memory API](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/automem/api/memory.py)] [[vector payload](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/automem/stores/vector_payload.py)]

## Write, update, delete, and retrieval

**Write and update — source observation.** The API documents single and batch memory creation, ID-based reads, partial `PATCH` updates, and deletion by ID or tag. A content-changing patch clears content-derived entity/enrichment metadata and queues enrichment again; metadata-only patches do not. The inspected memory route also records elapsed time and Qdrant write/queue status for batch writes. These are code paths, not measurements of successful operation under load.[[API reference](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/API.md)] [[memory API](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/automem/api/memory.py)]

**Delete — documented contract.** The API reference exposes `DELETE /memory/{id}` and `DELETE /memory/by-tag`. This review did not trace every deletion cleanup path across graph edges, vector points, derived indexes, and backups, so it cannot establish end-to-end erasure completeness. No tombstone or retained correction history is promised by the inspected API contract.[[API reference](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/API.md)]

**Retrieval — documented and source-visible behavior.** `GET /recall` combines semantic, keyword, metadata, tag, graph-relation, recency, and importance signals; the README describes a weighted score with ten signals, nine enabled by default. Tags are hard filters on several candidate paths. Current-state recall is the default: expired, future, archived, and superseded memories are suppressed, and replacement chains are followed with a bounded, cycle-safe traversal. History mode allows stale and future records. Relation/entity expansion can add connected memories; expansion may bypass tag scope unless requested to respect it. Optional `scope_fallback` can append unscoped vector results and marks them as outside the tag scope. These contracts do not establish recall accuracy.[[API reference](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/API.md)] [[recall implementation](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/automem/api/recall.py)] [[README](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/README.md)]

## Scope isolation and provenance

The API reference describes one configured API token for protected endpoints and does not describe token-to-user, project, or tenant mapping. Recall tags and exclusions are caller-selected filters; they are not authorization boundaries. In particular, the documented optional unscoped fallback deliberately reaches outside a tag filter, and graph expansion is not tag-constrained by default. Deployments needing tenant separation must supply and verify that boundary outside these retrieval filters; this review did not test a deployment’s external controls.[[API reference](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/API.md)] [[authentication helper](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/automem/api/auth_helpers.py)]

Memory IDs, timestamps, validity fields, metadata, and typed relations provide record-level context for updates and recall. Relations can represent derivation, contradiction, invalidation, or evolution, and current-state recall exposes relation/replacement provenance for suppressed items. The inspected API and payload contract do not establish source-document provenance for every memory or claim-level citations in generated assistant answers. Evidence support and citation coverage therefore remain unmeasured.[[API reference](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/API.md)] [[vector payload](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/automem/stores/vector_payload.py)]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for this system. “Code observation” describes visible implementation or instrumentation only; it is not a runtime result.

| Domain | Status | Evidence boundary |
|---|---|---|
| Answerable recall and abstention | Unmeasured | Hybrid candidate and ranking paths are documented; no adjudicated answerable or no-answer probes were run. |
| Correction accuracy and stale-value rate | Unmeasured | Patch and current/history state paths are visible; no post-correction probe set was run. |
| Deletion leakage | Unmeasured | Delete endpoints are documented; end-to-end deletion propagation and post-delete probes were not checked. |
| Scope isolation | Unmeasured | Tags filter retrieval, while expansion/fallback have explicit scope behavior; no cross-tenant isolation probes were run. |
| Evidence support and citation coverage | Unmeasured | IDs and relation provenance appear in records/responses; answer-level support was not evaluated. |
| Latency and write-to-recall delay | Unmeasured | Source emits elapsed-time fields and async work is queued; no latency distribution or acknowledgement-to-recall timing was collected. |
| Tokens, cost, and storage efficiency | Unmeasured | Embedding and optional enrichment paths are documented; no token, charge, or corpus-storage measurements were collected. |
| Source-visible observability | Code observation | API docs describe request/event logging, SSE operation events, enrichment status, and a health monitor for service availability and graph/vector count drift. These do not establish monitoring coverage or service-level outcomes. |

See the project’s [metric definitions](../METRICS.md), [benchmark status record](../results/initial-baselines-status.json), and [fixture](../fixtures/memory-benchmark-v1.json) for the protocol and project run status.[[project metrics](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[API reference](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/API.md)] [[health monitoring guide](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/HEALTH_MONITORING.md)]

## Limits and unknowns

This is a bounded review of the pinned README, API reference, memory and recall routes, payload helper, authentication helper, and health-monitoring guide. It did not execute the service or trace all worker, persistence, backup, and deletion paths. The docs describe cross-store graph/vector consistency work and limitations in temporal preference ranking; those are project documentation statements, not independent runtime findings. Current-state suppression and tag-scope controls should not be interpreted as measured guarantees. The review also cannot establish production latency, data recovery, access isolation beyond the inspected token/filter code, or correctness across all clients and deployment configurations.[[README](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/README.md)] [[API reference](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/API.md)] [[health monitoring guide](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/HEALTH_MONITORING.md)]

## Benchmark status

Project status for AutoMem: **Benchmark not run**. No AutoMem runtime, benchmark workload, or tests were run during this review. The repository’s own benchmark claims and historical runs are outside this review’s measured results. The [project status record](../results/initial-baselines-status.json) is not a result for AutoMem, and planned fixture counts are not measurements.[[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current upstream repository and default branch](https://api.github.com/repos/verygoodplugins/automem)
- [Current default-branch commits feed](https://github.com/verygoodplugins/automem/commits/develop.atom)
- [Reviewed commit](https://github.com/verygoodplugins/automem/commit/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2)
- [README at reviewed commit](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/README.md)
- [API reference at reviewed commit](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/API.md)
- [Memory routes at reviewed commit](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/automem/api/memory.py)
- [Recall routes at reviewed commit](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/automem/api/recall.py)
- [Vector payload helper at reviewed commit](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/automem/stores/vector_payload.py)
- [Authentication helper at reviewed commit](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/automem/api/auth_helpers.py)
- [Health monitoring guide at reviewed commit](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/docs/HEALTH_MONITORING.md)
- [Metric definitions](../METRICS.md)
- [Project benchmark status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and source attribution](../data/memory-systems.json)

## Contact-list follow-up

Checked the official pinned repository README for a published contact email; none is listed. The expected pinned `SECURITY.md` path returns File not found. The record stores a null contact and both exact checked URLs. No commit metadata or profile email was used.[[README](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/README.md)] [[checked SECURITY.md path](https://github.com/verygoodplugins/automem/blob/18569b4a1399c31dea3a8ec63c3082ab32f0dfb2/SECURITY.md)]

**Verification boundary:** the system, benchmarks, and tests were not run.
