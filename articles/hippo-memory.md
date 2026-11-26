# Hippo source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 298 / Hippo / hippo-memory  
**Listed repository locator:** [kitfunso/hippo-memory](https://github.com/kitfunso/hippo-memory)  
**Canonical upstream:** [kitfunso/hippo-memory](https://github.com/kitfunso/hippo-memory)  
**Default branch / reviewed head:** master / [8bf399e78b9c720b866c7299134ecd1d51a7c2d1](https://github.com/kitfunso/hippo-memory/commit/8bf399e78b9c720b866c7299134ecd1d51a7c2d1)  
**Review time:** 2026-11-25 23:07:55 UTC (2026-11-25 15:07:55 PST; America/Los_Angeles).

## Identity and review pin

The project catalog resolves position 298 to Hippo (hippo-memory) and lists the explicit locator https://github.com/kitfunso/hippo-memory. The catalog's pinned Agent Memory Atlas entry is preserved solely as roster attribution, not as evidence for this assessment. The official repository API identifies the canonical repository and default branch master; the official commits API reports current full head 8bf399e78b9c720b866c7299134ecd1d51a7c2d1. A fresh shallow checkout of master resolved to the same full SHA. This review is pinned to that checkout.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Hippo is a local-first memory system for coding agents. Its shared code supports CLI, API, MCP, hooks, and connector paths over a SQLite store. Entries carry lifecycle and provenance metadata; retrieval uses lexical search with optional vector embeddings, reranking, and graph stages. This article reports inspected implementation behavior; measured quality and performance are unreported here.[[readme]][[entry]][[remember]][[ranksearch]][[hybrid]]

## Who and what

The official README presents Hippo as a memory tool for coding agents, intended to keep information in a repository-local store and make it available across supported agents. It describes CLI commands, agent integrations, MCP access, and an optional team server with tenant-bound keys and roles. Those are upstream product descriptions; this review did not operate those surfaces.[[readme]]

The reviewed paths implement a memory-entry layer and associated retrieval and lifecycle APIs. The repository contains other features, including continuity records, connectors, graph processing, and operational surfaces, which are outside this memory-entry review.[[entry]][[remember]][[recall]]

## Architecture and data model

A memory entry has text and a typed kind and layer, tags, a confidence tier, strength and half-life values, timestamps, outcome counters, and supersession state. Additional fields can identify tenant, scope, owner, origin project, source session, source artifact, lead-in context, extraction source, and parent memories. These fields support lifecycle and provenance metadata, but do not themselves prove that a memory is correct or supported by a source passage.[[entry]]

The API write path checks project authorization and caller scope, screens content, and builds an entry before the store adapter writes it. SQLite persists entries and maintains FTS indexes and vector rows; mutation and recall paths can append tenant-scoped audit events. Agent-facing CLI, MCP, and HTTP surfaces call into shared API/store paths.[[remember]][[screen]][[entryrow]][[entrywrites]][[audit]][[audit-schema]]

Recall loads a bounded candidate pool from the tenant store, applying scope and project filters before the scoring window. The ranker can combine BM25 with vector cosine using a weighted blend or reciprocal-rank fusion; strength and recency affect ranking, and optional stages include graph expansion, MMR, reranking, and a result-token budget.[[ranksearch]][[pipeline]][[hybrid]][[fts]][[vectors]]

## Write, update, delete, and retrieval

**Write.** The remember API accepts content, kind, scope, owner, artifact reference, lead-in, tags, project identity, and caller-local metadata. The implementation vets secret-like material and screens shared-member or connector content for instruction-like patterns. When the store has review support, a flagged or connector-held write can be stored in quarantine with a review record; otherwise a detected member write receives a marker. The inspected checks do not establish that every unsafe input is detected.[[remember]][[screen]][[entry]]

**Update and correction.** The supersede API creates a successor and links the old memory to it; the SQLite write path commits the lifecycle change and audit event. Ordinary recall excludes superseded rows, while historical or as-of options can load them. This preserves a correction chain instead of replacing old text in place.[[promote]][[entrywrites]][[recall]][[ranksearch]]

**Delete and rejection.** Forget requires the caller to reach and have write rights to the row. It removes a non-raw row from the memory table, updates graph and FTS state, records the forget operation, and attempts post-commit mirror cleanup. Raw transcript rows are append-only through ordinary forget and are handled by a separate archive path. The rejection guard stores a tenant-scoped digest and reason without rejected content, then refuses future writes whose normalized text matches; semantic paraphrase matching is outside that guard. This review did not establish erasure from every backup or derivative copy.[[forget]][[entrywrites]][[entryrow]][[rejection]][[tombstone-schema]]

**Retrieval.** Recall applies tenant identity from the request context and passes caller scope and project-origin filters into candidate loading before the ranking window. Superseded rows are excluded by default. Search combines BM25 with optional vector similarity using either a weighted blend or reciprocal-rank fusion; strength and recency also shape scores. Optional stages include graph expansion, diversity reranking, configured rerankers, and a token budget. FTS5 and trigram indexes support lexical search; vectors are persisted as Float32 blobs.[[recall]][[ranksearch]][[hybrid]][[fts]][[vectors]][[pipeline]]

## Scope isolation

The memory model separates tenant ID, named scope, personal owner scope, and project origin. API recall defaults to restricted-scope denial, admits the authenticated caller's own personal scope, applies an explicitly requested API scope exactly, and filters by caller project while retaining user-global rows. Candidate SQL applies tenant, scope, and origin filters before its candidate limit.[[entry]][[scope]][[ranksearch]]

The CLI/operator path has distinct scope behavior: its named scope can add a scope to the default-visible pool because it has no API caller identity. sleepWholeStore explicitly processes the full store across tenants; source comments state that this operation is kept loopback-only. The correct boundary therefore depends on the intended surface and runtime configuration, and this review did not run isolation probes.[[scope]][[sleep]][[readme]]

## Provenance and evidence

Entries can retain a source label, artifact reference, source-session ID, lead-in, extracted-from pointer, parent IDs, tenant/project/scope labels, and a successor link. Recall audit rows retain actor, operation, target, and metadata; the query value is hashed rather than stored in recall audit metadata. Rejected-value tombstones store a digest and human reason, not rejected content.[[entry]][[remember]][[audit]][[finish]][[rejection]]

These fields can make origin and lifecycle easier to inspect, but the reviewed schema has no general citation-span contract tying each recalled claim to exact supporting text. Confidence tiers and observation counts are metadata, not independently verified evidence.[[entry]][[remember]]

## Efficiency and observability

The local SQLite store includes FTS5 and trigram indexes, plus stored vector embeddings. The ranker can use a lexical path, while vector and reranker configurations add their own work and dependencies. Candidate loading is bounded and filters tenant, scope, and project before scoring. The audit log and recall reporting paths expose operation and retrieval metadata; a failed FTS update warns and marks the index out of sync so it can be repaired.[[fts]][[vectors]][[ranksearch]][[hybrid]][[audit]][[finish]][[entryrow]]

No latency, write-to-recall delay, token, cost, or storage measurements were collected for this review.[[metrics]][[status]]

## Metric-domain evidence

All comparison domains are **unmeasured** for Hippo in this review. Source structure is not a benchmark result. The [project metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define evaluation work and shared status; they do not provide Hippo results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Status |
|---|---|---|
| Answerable retrieval and abstention | Ranked candidate retrieval inspected; no answerability or abstention workload scored. | Unmeasured |
| Correction accuracy and stale values | Successor links and default superseded-row exclusion inspected; no correction probes run. | Unmeasured |
| Deletion leakage | Forget and raw archive paths inspected; no post-delete leakage probes run. | Unmeasured |
| Scope isolation | Tenant, scope, and origin filters inspected; no cross-scope workload run. | Unmeasured |
| Evidence support and citation coverage | Provenance metadata inspected; no claim-to-passage adjudication run. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timings collected. | Unmeasured |
| Tokens, cost, and storage | SQLite/index/vector architecture inspected; no workload measurements collected. | Unmeasured |

## Limits and unknowns

This is a source review of the open upstream repository at the verified head. Hippo, its tests, and its benchmark workloads were not run. README statements about product capabilities or evaluations remain upstream statements, not reproduced findings. The paths reviewed here do not establish end-to-end privacy, every connector's retention behavior, complete erasure from backups, cross-surface authorization under deployment configuration, or measured recall quality. The homepage shows a different displayed version from the repository head; implementation claims here use the pinned source review.[[readme]][[website]][[head]][[forget]][[scope]]

## Benchmark status

**Benchmark not run.** No Hippo runtime, tests, or benchmark workload was executed. No retrieval, abstention, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) are protocol and status references, not Hippo results.[[metrics]][[fixture]][[status]]

## Contact

The official README pinned to the reviewed commit and the official project homepage were checked for a contact email. Neither publishes one; the structured record stores contact_email: null and the exact checked URLs. No commit/profile metadata, third-party directory, or inferred address was used.[[readme]][[website]]

## Sources

All upstream source-file citations are pinned to full SHA 8bf399e78b9c720b866c7299134ecd1d51a7c2d1. The Atlas entry is roster attribution only, not assessment evidence. See the structured review record [hippo-memory.json](../data/system-reviews/hippo-memory.json) and the [curated roster](../data/memory-systems.json).

---