# Engram Provable

## Identity and review pin

- **Catalog position:** 227, “Engram Provable”; slug `engram-provable`.
- **Listed repository:** [Harshitk-cp/engram](https://github.com/Harshitk-cp/engram); the roster marks the locator explicit. The pinned Atlas entry is recorded only for roster attribution and locator context.
- **Canonical upstream:** [Harshitk-cp/engram](https://github.com/Harshitk-cp/engram), default branch `main`. The official GitHub repository page names `main`; `git ls-remote --symref` reported `HEAD -> refs/heads/main` at `4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37`. A shallow checkout of `main` resolved to the same full SHA.
- **Reviewed:** 2026-11-25 19:56:43 UTC (2026-11-25 11:56:43 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) establishes ordinal, name, slug, listed locator, and Atlas attribution. The pinned [Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/engram-provable.md) supports roster attribution only; it was not used as assessment evidence.

## Summary

Engram is a Go memory service for AI agents with HTTP and MCP interfaces, a React admin console, and PostgreSQL/pgvector storage. It models semantic beliefs alongside episodic, procedural, and working memory, with tenant and subject bindings, hybrid retrieval, confidence/freshness ranking, and a provenance quarantine and audit system. This is a source review; Engram, its tests, and benchmarks were not run.

## Who and what

The official [README](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/README.md) describes the project as memory infrastructure exposed through an HTTP API or MCP server and backed by PostgreSQL and pgvector. It documents a self-hosted server and managed service pathways. This review does not infer an individual maintainer identity from account or commit metadata.

## Architecture and data model

The Go service separates domain models, service logic, PostgreSQL stores, HTTP handlers, and middleware; the repository also includes an MCP server and React console. Semantic memory rows carry content, type, source/provenance, confidence, currency (freshness), optional event date, metadata, embedding model/provider, and tenant/agent plus private, anchor, session, canon, or quarantine binding. Separate stores support episodes, procedures, schemas, entities/graph relations, and working-memory activation. PostgreSQL migrations add pgvector HNSW indices for vector-backed records.[[README](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/README.md)] [[memory domain](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/domain/memory.go)] [[initial schema](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/migrations/001_init.up.sql)] [[vector indexes](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/migrations/008_hnsw_index.up.sql)]

## Write, update, delete, and retrieval

**Write and update.** The memory create path accepts typed content and optional source/provenance, confidence, event date, anchor/session identifiers, and a quarantine hint. Store defaults set provenance and confidence, while binding is computed server-side from scope IDs. Service logic can reinforce similar beliefs or record contradictions; an admin-scoped PATCH supports memory correction/review. The inspected API does not expose a general user-facing content-update route.[[create handler](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/api/handlers/memory.go)] [[admin handler](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/api/handlers/admin.go)] [[memory service](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/service/memory.go)] [[memory store](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/store/memory.go)] [[routes](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/api/router.go)]

**Delete, archive, and quarantine.** The ordinary memory DELETE path writes a content snapshot and hash to the mutation log before physically deleting the row in a transaction. Separate archive/restore paths toggle archived state. Subject purge/redaction paths are implemented separately and include derived-memory handling. Quarantine holds a row outside ordinary recall; admin-scoped release recomputes its binding, while reject records the decision and deletes it. Audit retention is not the same as retaining an active memory, and source inspection cannot establish behavior of external database backups.[[memory store](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/store/memory.go)] [[memory handler](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/api/handlers/memory.go)] [[admin service](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/service/admin.go)] [[router](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/api/router.go)]

**Retrieval.** The store supports vector recall and a hybrid path combining PostgreSQL full-text ranking with vector ranking through reciprocal-rank fusion. A separate service can blend vector and graph relevance; the score exposes vector and graph components, then applies confidence and currency (freshness). Recall filters tenant, agent, binding, anchor/session, archive state, and quarantine as applicable. These are code observations; retrieval quality, abstention, and ranking effectiveness were not measured.[[memory store](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/store/memory.go)] [[hybrid recall service](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/service/hybrid_recall.go)] [[recall handler](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/api/handlers/memory.go)]

## Scope isolation

Memory records carry both tenant and agent IDs. The create handler derives tenant identity from authenticated request context, resolves anchors/sessions within that tenant, and store reads/recall include tenant predicates. Private memories are the default; anchor and session bindings narrow subject/conversation context, canon is tenant-shared, and quarantine is excluded from recall. The inspected source relies on application-layer tenant predicates; it does not establish database row-level security or end-to-end isolation under a compromised service/database credential. No isolation workload was run.[[memory handler](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/api/handlers/memory.go)] [[auth middleware](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/api/middleware/auth.go)] [[memory store](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/store/memory.go)]

## Provenance and evidence

Memory fields represent source, provenance category, evidence type, confidence, and optional source-memory linkage. The quarantine workflow can hold untrusted writes outside recall until an admin decision. PostgreSQL triggers assign sequence numbers and SHA-256 row hashes in a per-tenant append-only mutation chain; verification checks links and the recorded chain head. The chain improves tamper detection and reviewability, but does not prove stored claims true. Routine decay entries are explicitly excluded from the sealed chain, and audit event capture should therefore not be interpreted as a complete history of every state change.[[memory domain](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/domain/memory.go)] [[audit store](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/store/learning.go)] [[audit handler](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/api/handlers/audit.go)] [[audit chain migration](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/migrations/019_audit_chain_complete.up.sql)] [[decay audit policy](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/migrations/029_audit_exclude_decay.up.sql)]

## Efficiency and observability

The code uses HNSW vector indexes and bounds the hybrid vector candidate set; embedding provider calls, full-text/vector ranking, and optional graph traversal add distinct work. Authenticated request middleware records coarse operation counts, server errors, and bucketed latency summaries (including p50/p95/p99) in a process-local registry that resets on restart. No latency, token, cost, storage-efficiency, or sustained-load measurements were collected for this review.[[HNSW migration](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/migrations/008_hnsw_index.up.sql)] [[memory store](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/store/memory.go)] [[observability middleware](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/api/middleware/observability.go)] [[observability registry](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/internal/observability/registry.go)]

## Metric-domain evidence

- **Answerable retrieval and abstention:** vector, full-text, and graph ranking paths are source-inspected; no answerability or abstention workload was run.
- **Correction and stale values:** reinforcement, contradiction, confidence, currency, and admin update paths are source-inspected; correction accuracy and stale-value rate are unmeasured.
- **Deletion leakage:** delete, archive, redaction, and subject purge paths are source-inspected; no post-delete probe or backup-erasure check was run.
- **Scope isolation:** tenant, agent, anchor, session, canon, and quarantine filters are source-inspected; no isolation workload was run.
- **Evidence support and citations:** provenance fields, quarantine, and audit history are source-inspected; answer support precision and citation coverage are unmeasured.
- **Retrieval latency and write-to-recall delay:** not measured.
- **Tokens, cost, and storage efficiency:** not measured.

See the project’s [metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and [planned benchmark fixture](../fixtures/memory-benchmark-v1.json). These comparison documents are not Engram measurements.

## Contact

No contact email was found in the official pinned [README](https://github.com/Harshitk-cp/engram/blob/4a3d20487a370d0cca6eaaf97861a6d5d0bcbe37/README.md). The exact checked URL is recorded in [engram-provable.json](../data/system-reviews/engram-provable.json); no commit/profile metadata or third-party directory was used.

## Limits and unknowns

This is a source review of the verified current `main` head. Engram, tests, and benchmarks were not run. The upstream README advertises LongMemEval scores, but this review did not reproduce or independently adjudicate those results. Source inspection does not establish retrieval accuracy, useful abstention, resistance to tenant-boundary failures, operational durability, secure erasure across backups, or production latency, costs, and scale. The official README and checked implementation were available; no separate repository `docs/` directory was present in the checkout.

## Benchmark status

**Benchmark not run.** No Engram runtime, tests, or benchmarks were run. See the [project metric definitions](../METRICS.md), [shared status](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and SHA-pinned upstream links are recorded in [engram-provable.json](../data/system-reviews/engram-provable.json). The [curated roster](../data/memory-systems.json) and pinned [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/engram-provable.md) support identity and locator context only.
