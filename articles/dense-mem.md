# Dense-Mem — source review

**Review status:** Reviewed from selected documentation and source at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 187 — Dense-Mem / dense-mem  
**Listed repository:** [markhuangai/dense-mem](https://github.com/markhuangai/dense-mem)  
**Canonical upstream:** same repository; default branch `main`; reviewed head [d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a](https://github.com/markhuangai/dense-mem/commit/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a)  
**Review time:** 2026-11-25 10:57:27 UTC (2026-11-25 02:57:27 PST; America/Los_Angeles)

## Identity and scope

The curated catalog places Dense-Mem at ordinal 187 with slug `dense-mem`, an explicit repository locator, and a pinned Atlas attribution. Atlas is retained only for roster identity and locator context, not used as assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dense-mem.md)]

The official GitHub repository identifies `main` as its default branch. The official main commits feed reports current full head `d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a`, corroborated by a read-only `git ls-remote --symref` and a shallow checkout at the same SHA. The feed was updated at 2026-11-25T02:38:18Z; source links below pin the reviewed SHA.[[repository](https://github.com/markhuangai/dense-mem)] [[reviewed head](https://github.com/markhuangai/dense-mem/commit/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a)]

## Summary and architecture

Dense-Mem is a self-hosted HTTP MCP server using Streamable HTTP. AI clients connect through `/mcp`; the README describes a Remember, Recall, and Trace workflow.[[official README](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/README.md)] [[MCP server](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/mcp/server.go)]

PostgreSQL with pgvector is the durable authority. Redis is used for coordination in multi-instance deployments; the README says a single node can use process memory. Search documents and vector/text indexes are projections of canonical Evidence, and the contract exposes their lifecycle states.[[README](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/README.md)] [[domain contract](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/domain/contract.go)] [[Evidence schema](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/migrations/postgres/v2_4/2026071703_v2_ledger.sql)] [[Recall repository](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/recall/postgres/recall_repository.go)]

The current runtime contract is Evidence-only. Canonical records retain exact submitted content and hashes, occurrences, source revisions, authority, owner, space, and lifecycle. Topics and search projections aid discovery but are derived structures rather than canonical factual claims.[[domain contract](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/domain/contract.go)] [[ledger contract](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/contract/ledger.go)] [[Evidence schema](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/migrations/postgres/v2_4/2026071703_v2_ledger.sql)] [[occurrence schema](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/migrations/postgres/v2_6/20260903010001_evidence_occurrence_duplicates.sql)]

## Write, update, delete, and retrieval

**Write.** An AI client proposes Evidence through Remember. The service assesses the submission, applies policy and security checks, resolves duplicates, prepares embeddings, and commits via a request-owned persistence boundary. Provider calls and embedding execution remain separate from that commit contract; results support idempotency and replay.[[README](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/README.md)] [[Remember assessment](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/remember/service/submission_assessment_synchronous.go)] [[write contract](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/contract/write.go)] [[ledger contract](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/contract/ledger.go)]

**Update.** Source updates carry source keys, revision tokens, content hashes, and expected prior tokens. The PostgreSQL code binds a source to its memory space and rejects stale expectations. Superseded revisions remain in revision history; no update workload was run here.[[ledger contract](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/contract/ledger.go)] [[source revision implementation](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/postgres/source_revision_repository.go)] [[Evidence schema](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/migrations/postgres/v2_4/2026071703_v2_ledger.sql)]

**Delete and retraction.** The runtime contract exposes owner-scoped retraction with a reason and idempotency key. The PostgreSQL operation authorizes the actor, checks idempotent replay, records a lifecycle operation/event, and applies effects transactionally. Retraction affects active recall while preserving history. The repository also models queued private-memory erasure and retention purge as separate workflows; retraction should not be read as proof of physical removal from every backup or external copy.[[lifecycle contract](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/contract/lifecycle.go)] [[lifecycle implementation](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/postgres/evidence_lifecycle_repository.go)] [[Evidence schema](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/migrations/postgres/v2_4/2026071703_v2_ledger.sql)]

**Retrieval.** Recall reads full-text and vector candidates, fuses ranked branches, hydrates selected Evidence, and adds conflict context. Inputs support optional valid-time and known-time filters, known Evidence IDs, and topic IDs. Candidate overfetch is bounded; branch failures may be returned as explicit degradation. No recall workload was run.[[Recall pipeline](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/recall/retrieval.go)] [[PostgreSQL Recall](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/recall/postgres/recall_repository.go)]

## Scope isolation

Access is organized by authenticated team, owner profile, and memory space. The domain model distinguishes private and team-shared spaces with read/write permissions. Recall uses actor-authorized spaces and binds reads to a space ID and active generation; team-shared retrieval is constrained to the team's shared space.[[memory-space access model](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/domain/memory_space.go)] [[cross-space Recall](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/recall/recall_spaces.go)] [[Recall repository](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/recall/postgres/recall_repository.go)]

The README states that team-shared visibility does not grant permission to change another owner's Evidence. The source distinguishes read visibility from mutation authority. This review did not run cross-team or cross-space isolation probes, so leakage under workload is unmeasured.[[README](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/README.md)] [[memory-space access model](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/domain/memory_space.go)] [[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Provenance and evidence

Evidence preserves exact content and hashes, source type, authority, source reference/key and revision, occurrence identity, owner, and ingest identity. Authority labels include authoritative, primary, secondary, inferred, and unknown.[[Evidence types](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/domain/evidence.go)] [[ledger contract](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/contract/ledger.go)] [[occurrence schema](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/migrations/postgres/v2_6/20260903010001_evidence_occurrence_duplicates.sql)]

Remember assessment and source revision information are linked to writes; retractions carry reasons and preserve lifecycle history. The README describes Trace as the way to inspect provenance. Provenance supports lineage but does not prove that a source is truthful or guarantee citations in every downstream answer.[[README](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/README.md)] [[Remember assessment](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/remember/service/submission_assessment_synchronous.go)] [[source revision implementation](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/postgres/source_revision_repository.go)] [[lifecycle implementation](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/postgres/evidence_lifecycle_repository.go)]

## Efficiency and observability

The README says configured hosted model providers may receive Evidence and queries and suggests self-hosted providers when that traffic should remain within operator infrastructure. Embeddings and verifier-model configuration are required for semantic operations.[[README](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/README.md)] [[Remember assessment](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/remember/service/submission_assessment_synchronous.go)]

Recall has separate candidate, fusion, hydration, selection, and conflict stages with bounded candidate overfetch and result limits. Prometheus instrumentation includes HTTP and Recall request duration and result counts, Recall feedback, Remember acknowledgements, token counts, and estimated provider costs. These are observability hooks, not performance results from this review.[[Recall pipeline](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/recall/retrieval.go)] [[Prometheus metrics](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/observability/prometheus_metrics.go)]

## Metric-domain evidence

All metric domains remain unmeasured. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [existing result status](../results/initial-baselines-status.json).

- **Answerable retrieval, abstention, and write-to-recall delay — unmeasured.** No query corpus or timed workload was run.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)]
- **Correction accuracy and stale-value rate — unmeasured.** No correction probes were executed.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)]
- **Deletion leakage — unmeasured.** No post-retraction retrieval probes were run.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)]
- **Scope isolation leakage — unmeasured.** No cross-team or cross-space workload was run.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)]
- **Evidence support precision and citation coverage — unmeasured.** No generated answers were adjudicated.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)]
- **Retrieval latency, tokens, cost, and storage efficiency — unmeasured.** No resource or accounting workload was collected.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Limitations and unknowns

The service depends on configured model providers for embeddings and semantic Evidence assessment. Provider outages, malformed output, or configuration errors can impair those paths. Hosted provider traffic may include Evidence and queries.[[README](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/README.md)]

Evidence authority and revision metadata track origin and lifecycle; the selected source inspection does not establish factual accuracy or how reliably model assessment separates supported from unsupported content. Retraction, private-space erasure, and retention purge are distinct; this review does not establish physical removal from all backups, provider logs, or user-held exports.[[Evidence types](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/domain/evidence.go)] [[lifecycle implementation](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/postgres/evidence_lifecycle_repository.go)] [[README](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/README.md)]

This is a selected inspection of the README and key domain, write, lifecycle, search, scope, and metrics paths. Behavior in uninspected adapters, deployment setups, failure paths, and real model/provider combinations remains unknown. No Dense-Mem runtime, tests, or benchmarks were run.[[README](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/README.md)] [[Remember assessment](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/remember/service/submission_assessment_synchronous.go)] [[Recall pipeline](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/recall/retrieval.go)] [[lifecycle implementation](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/internal/knowledge/postgres/evidence_lifecycle_repository.go)]

## Contact

The official pinned README was checked for a contact email and publishes none. No commit/profile metadata or third-party directory was used.[[official README](https://github.com/markhuangai/dense-mem/blob/d60ff2b9bf2c9a259f57dbc69d2a055a7903e06a/README.md)]

## Benchmark status

**Benchmark not run.** No Dense-Mem runtime, test suite, or benchmarks were run for this review. Source observations and upstream descriptions are not measured results. See [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [result status](../results/initial-baselines-status.json).

---

