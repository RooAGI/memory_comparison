# Aura (chetto1983) source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 77 / Aura (chetto1983) / aura-chetto1983  
**Listed repository locator:** [chetto1983/Aura](https://github.com/chetto1983/Aura)  
**Current canonical repository:** [chetto1983/Aura](https://github.com/chetto1983/Aura)  
**Default branch / reviewed head:** master / ecc3d78c6cea6eeafb7396fd38859d8fda3eb483  
**Review time:** 2026-11-24 21:59:03 UTC (13:59:03 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists Aura (chetto1983) at ordinal 77, slug `aura-chetto1983`, with the repository locator above and an Atlas attribution source pinned at revision `19199a4fc249e89c0793be06f0b166b358089ba0`. The roster source is used only for identity and attribution; Atlas descriptions, marks, or layout are not assessment evidence. The official repository page and master commit feed identify the canonical repository, default branch, and current head used for this review. [curated roster](../data/memory-systems.json) [official repository](https://github.com/chetto1983/Aura) [master commit feed](https://github.com/chetto1983/Aura/commits/master.atom) [reviewed commit](https://github.com/chetto1983/Aura/commit/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483.patch)

## Summary

Aura is a self-hosted Go agent platform whose memory subsystem stores bitemporal facts as graph edges in ArcadeDB, alongside derived conversation recall. It combines named-entity traversal with hybrid lexical and vector retrieval, and exposes correction, forgetting, and provenance-aware writes. This review is pinned source inspection, not a runtime or performance assessment. [README.md](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/README.md) [memory.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory.go) [memory_recall.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_recall.go)

## Who and what

The official README presents Aura as a self-hosted, multi-user Go agent application with a web cockpit, CLI, Telegram channel, tools, and a Compose service stack. Memory is a subsystem of the application, exposed through its first-party authenticated ArcadeDB MCP interface, rather than a standalone memory library. [README.md](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/README.md) [Architecture]( https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/ARCHITECTURE.md )

## Architecture and data model

Aura connects its Go runtime to ArcadeDB for graph memory, PostgreSQL for authoritative conversations and identity data, and Garage for object storage. The README describes an ArcadeDB memory service and a separate ingestion service; this review focuses on the fact and conversation-recall implementation and MCP contract. [README.md](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/README.md) [Architecture]( https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/ARCHITECTURE.md ) [MCP tool schemas](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/arcadedb-mcp-live-tools.json)

A memory fact is a directed `FACT` edge between named `Entity` vertices. Edges hold statement, validity and record-time fields, a fact key, and one or more source maps. The schema adds a unique entity-name index and a Lucene English full-text index for fact statements. A separate 768-dimension cosine LSM vector index supports dense retrieval. [memory.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory.go) [memory_vector.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_vector.go)

The model uses two time axes: `valid_from/valid_to` describe when an assertion holds in the world; `created_at/expired_at` describe when the system recorded and closed it. Architecture documentation describes MENTIONS links to retained historical fact records and a derived conversation projection backed by PostgreSQL-authoritative turns. [memory.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory.go) [Architecture]( https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/ARCHITECTURE.md ) [memory_recall.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_recall.go)

## Write, update, delete, and retrieval

**Write.** The `memory_upsert_fact` MCP contract accepts a structured assertion with validity and provenance fields and optional supersession targeting. A host-side `AcceptedCapture` path also admits explicit facts or allowlisted durable artifacts. It validates identity, actor, source references, conversation and tool-call IDs, confidence, and idempotency before applying the capture through the memory-batch path. These are inspected write mechanisms, not evidence of extraction quality. [MCP tool schemas](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/arcadedb-mcp-live-tools.json) [memory_capture.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_capture.go) [memory.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory.go)

**Update and correction.** Corrections close the old fact's validity window and set its record expiry, retaining the old edge for historical `as_of` recall. A caller may identify one target by its exact `fact_key`; the legacy subject/predicate route refuses zero or multiple candidates rather than guessing. Exact replay may add support from another source to an existing fact. [memory_supersede.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_supersede.go) [memory.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory.go)

**Delete and retirement.** `memory_forget` can filter by source run, entity, or subject/predicate/object, and an empty filter is rejected. Source-specific forgetting removes that source's support if other sources remain; otherwise it hard-deletes the fact and can prune orphan entities. It also supports dry-run counts. This inspection did not establish whole-identity purge or erasure completeness across backups and derived stores. [forget.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/forget.go) [Architecture]( https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/ARCHITECTURE.md ) [MCP tool schemas](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/arcadedb-mcp-live-tools.json)

**Retrieval.** Unified recall includes semantic, recent, period, open, scroll, and reasoning modes. When given an entity, semantic recall walks its fact edges. Otherwise it fuses Lucene candidates with dense vector neighbors using reciprocal rank fusion, reranks them, applies a relevance floor, and uses lexical retrieval when embeddings are unavailable. Winning fact records are hydrated in a bounded follow-up query. Direct `FactsAbout` traverses both subject and object directions and can constrain predicate, validity time, and result count. [memory_recall.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_recall.go) [memory_vector.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_vector.go) [memory_facts_about.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_facts_about.go)

**Scope isolation.** A valid identity UUID maps to a separate ArcadeDB database and server user. Missing identity fails closed; per-identity credentials derive from a required server secret rather than using a shared account. The architecture also describes PostgreSQL row-level scope and identity-bound storage. This is source-visible design, not an isolation measurement across deployments. [tenant.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/tenant.go) [Architecture]( https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/ARCHITECTURE.md )

**Provenance and evidence.** Facts retain source run IDs, referenced memory IDs, writer role, and capture metadata including source kind and references, conversation/tool-call IDs, observed time, and confidence. The host supplies actor identity and role. These fields make supporting records inspectable, but do not establish that a source is true or that a generated response cites it correctly. [memory.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory.go) [memory_capture.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_capture.go) [memory_vector.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_vector.go)

**Source-visible efficiency and observability.** The code declares full-text and vector indexes, bounded candidate/result limits, exact-entity traversal, and bounded fact hydration. Recall returns backend elapsed time. The project architecture describes bounded memory context and runtime logs/metrics; graph diagnostics cap returned node details. These are code and documentation observations, not measurements from this review. [memory.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory.go) [memory_recall.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_recall.go) [memory_vector.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_vector.go) [Architecture]( https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/ARCHITECTURE.md )

The upstream source contains author-reported historical retrieval tuning and validation notes, including a concurrent deletion validation document. They were not reproduced here and are not results from this project's benchmark fixture or this review. [memory_vector.go](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_vector.go) [deletion validation note](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/memory-concurrent-delete-validation.md)

## Metric-domain evidence

Every project metric domain is **unmeasured** for this review. Retrieval and correction structures are code evidence only; no answerable recall, abstention, stale-value, deletion-leak, cross-identity, evidence-support, citation-coverage, latency, write-to-recall, token/cost, or storage measurement was collected. The project's definitions, fixture, and execution record describe the separate protocol and status, not Aura results. [METRICS.md](../METRICS.md) [benchmark execution status](../results/initial-baselines-status.json) [fixture](../fixtures/memory-benchmark-v1.json)

## Limits and unknowns

This bounded review inspected the official README and architecture, fact schema, recall and vector paths, direct fact lookup, accepted capture, superseding, forgetting, tenant mapping, MCP schemas, and security policy at the verified full SHA. Aura, its tests, and benchmarks were not run. Source inspection cannot establish answer quality, calibrated abstention, concurrent correctness, tenant isolation under all deployment settings, or complete deletion from backups and derived data. The MCP contracts and README describe behavior but are not runtime verification. [README.md](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/README.md) [Architecture]( https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/ARCHITECTURE.md ) [MCP schemas](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/arcadedb-mcp-live-tools.json) [Forget]( https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/forget.go )

## Contact-list follow-up

The official pinned SECURITY.md publishes **dvdmarchetto@gmail.com** for private vulnerability reports. The official pinned README and SECURITY.md were checked; no other official project or organization website was needed to verify this published contact. [SECURITY.md](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/SECURITY.md) [README.md](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/README.md)

## Benchmark status

**Benchmark not run.** No Aura execution, benchmark workload, or tests were run. Metric domains remain unmeasured. Project metric definitions, fixture, and execution-status record describe the separate evaluation protocol; fixture counts are planned probes, not measured observations. [METRICS.md](../METRICS.md) [execution status](../results/initial-baselines-status.json) [fixture](../fixtures/memory-benchmark-v1.json)

## Sources

- [Official repository](https://github.com/chetto1983/Aura)
- [Official master branch commit feed](https://github.com/chetto1983/Aura/commits/master.atom)
- [Reviewed full head commit](https://github.com/chetto1983/Aura/commit/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483.patch)
- [README.md](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/README.md)
- [Architecture documentation](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/ARCHITECTURE.md)
- [Memory fact schema](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory.go)
- [Unified recall](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_recall.go)
- [Hybrid retrieval](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_vector.go)
- [Direct fact retrieval](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_facts_about.go)
- [Accepted capture](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_capture.go)
- [Superseding](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/memory_supersede.go)
- [Forgetting](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/forget.go)
- [Tenant mapping](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/internal/arcadedb/tenant.go)
- [MCP tool schemas](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/arcadedb-mcp-live-tools.json)
- [Concurrent deletion validation note](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/docs/memory-concurrent-delete-validation.md)
- [Official security policy](https://github.com/chetto1983/Aura/blob/ecc3d78c6cea6eeafb7396fd38859d8fda3eb483/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and source attribution](../data/memory-systems.json)
- [Atlas attribution source, identity only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/aura-chetto1983.md)

**Verification boundary:** source observations only; no system, benchmark workload, or tests were run.
