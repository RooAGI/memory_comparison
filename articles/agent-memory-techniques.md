# Agent Memory Techniques source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster name / slug:** Agent Memory Techniques / agent-memory-techniques  
**Listed repository locator:** [NirDiamant/Agent_Memory_Techniques](https://github.com/NirDiamant/Agent_Memory_Techniques) (roster attribution)  
**Current canonical repository:** [NirDiamant/Agent_Memory_Techniques at reviewed commit](https://github.com/NirDiamant/Agent_Memory_Techniques/tree/f0b663472899e58568bf3e71b51ac4f2672dd669)  
**Default branch / reviewed head:** main / `f0b663472899e58568bf3e71b51ac4f2672dd669`  
**Review time:** 2026-11-24 18:25:28 UTC (10:25:28 PST; America/Los_Angeles). GitHub repository metadata and the `commits/main` API were checked at 18:20:09 UTC; the repository metadata named `main` as default branch and that ref resolved to the reviewed SHA.

## Identity and scope

The curated roster places Agent Memory Techniques at position 11 and lists the repository locator above with explicit attribution. The roster supplies identity and locator only; its Atlas descriptions and marks are not assessment evidence.[[curated roster](../data/memory-systems.json)]

This is an educational repository of Jupyter notebooks and helper material, not a single installable memory service. Its README says it contains 30 separate memory technique notebooks. The reviewed technique 30, “Production Memory Patterns,” presents deployment patterns in one notebook and says its Redis, Postgres/pgvector, and graph services are simulated in Python.[[repository README](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/README.md)] [[technique 30 README](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/README.md)] [[technique 30 notebook](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)]

## Architecture and data model

**Code observation.** The notebook defines a `MemoryRecord` with an ID, user ID, content, optional embedding, creation and last-access timestamps, access count, importance, tier, optional TTL, tags, a PII-redacted flag, token estimate, and optional compressed bytes. Its three tier classes are local in-memory examples: a hot cache with per-user ID sets, a warm dictionary-backed vector-store simulation, and a cold zlib archive. A separate `GraphEdge` stores source, relation, target, user ID, timestamp, and optional source memory ID; `GraphRelationshipStore` keeps edges in an in-process list and adjacency map.[[technique 30 notebook — MemoryRecord and tier classes](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)]

The README describes the larger walkthrough as PII scanning/redaction, fact and relationship extraction, embeddings, tiered memory, budget controls, cost tracking, and observability. It presents Redis, Postgres/pgvector, and external graph services as production replacements; those are design examples, not dependencies demonstrated by the inspected local classes.[[technique 30 README](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/README.md)] [[technique 30 notebook — tier implementation](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)]

## Write, update, delete, and retrieval

**Code observation.** The inspected hot and warm stores expose `put`; cold storage exposes `archive`. Warm `put` indexes records by ID and user, while hot `put` sets a default TTL and evicts the least recently accessed ID when that user reaches its configured capacity. The notebook’s inspected store APIs do not define a general correction-history or version-resolution contract; replacement through a store write should not be read as a tested correction guarantee.[[technique 30 notebook — HotTierCache.put and WarmTierStore.put](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)]

Warm retrieval takes a required `user_id`, skips missing or zero-length embeddings, computes cosine similarity over that user’s indexed records, sorts descending, and returns at most `k`. The hot tier offers ID lookup with TTL expiry checks and access touches; the cold tier decompresses an ID-addressed record. The README describes an orchestration path searching hot, warm, then cold and promoting records, but that end-to-end path was not traced through the whole notebook.[[technique 30 notebook — warm search and tier APIs](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)] [[technique 30 README — retrieval flow](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/README.md)]

The inspected hot, warm, cold, and graph classes include `delete_user` methods. Hot, warm, and cold remove records from their local stores and indexes; graph deletion filters its edge list by user and rebuilds adjacency. The README describes an audit log and cross-tier right-to-forget flow, but this bounded code inspection did not trace the audit implementation or a complete orchestrated deletion path. It therefore does not establish deletion propagation to external stores, backups, caches, or derived data.[[technique 30 notebook — delete_user methods](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)] [[technique 30 README — right-to-forget description](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/README.md)]

## Scope isolation and provenance

**Code observation.** Warm search and each tier’s user-record listing use per-user indexes; graph edges carry a user ID and deletion filters by it. The inspected graph `query(entity, relation)`, hot `get(record_id)`, and cold `retrieve(record_id)` methods do not take a user ID. That interface shape means those ID/entity lookup paths do not themselves enforce user isolation. This is a source-level observation, not a runtime isolation test.[[technique 30 notebook — scoped indexes and lookup methods](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)]

Records retain user ID and timestamps, and graph edges can point to a source memory ID. In the inspected record model I did not find a source citation or trust-state field; this does not establish whether later notebook orchestration adds provenance. The README describes PII redaction, fact extraction, and graph creation, but answer-claim citations and evidence support are not established by these structures.[[technique 30 notebook — MemoryRecord and GraphEdge](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)] [[technique 30 README — ingestion design](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/README.md)]

## Efficiency and observability

**Code observation.** Hot-cache state includes hit, miss, eviction, and expiration counters plus a derived hit-rate property. Cold storage tracks a byte-difference value when compressing content. Warm cosine search iterates that user’s indexed IDs and sorts candidates, so the visible example work grows with the indexed candidate set before truncating to `k`. The README discusses latency targets, metrics, alerts, cost controls, and sharding as design topics. These structures and descriptions are not measured latency, throughput, token use, cost, or storage results.[[technique 30 notebook — cache counters, search, and compression](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)] [[technique 30 README — observability and limits](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/README.md)]

## Project metric domains

All project benchmark domains remain **unmeasured** for this system. Source inspection does not establish answerable recall or abstention, correction accuracy or stale-value rate, deletion leakage, scope isolation, evidence support or citation coverage, retrieval latency, write-to-recall delay, token use, cost, or storage efficiency. See the project’s [metric definitions](../METRICS.md), [benchmark status record](../results/initial-baselines-status.json), and [fixture](../fixtures/memory-benchmark-v1.json) for the measurement protocol and current project status.[[project metrics](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This bounded, read-only review inspected the repository README, technique 30 README, and notebook model/store sections through the graph store. Later notebook cells, external-service integrations, and full orchestration were not traced end to end. The README itself identifies horizontal sharding and distributed deployment as additional infrastructure beyond the shown single-node patterns. The notebook models Redis and Postgres behavior in local Python structures; source code here does not demonstrate production persistence, concurrency, authorization, backup recovery, or reliability.[[repository README](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/README.md)] [[technique 30 README](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/README.md)] [[technique 30 notebook](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)]

The roster record is retained only for the curated name, ordinal, listed repository locator, and source attribution. It did not provide assessment findings.[[curated roster](../data/memory-systems.json)]

## Benchmark status

Project status: **Benchmark not run**. No system code, notebook, benchmark workload, or tests were executed for this review. The project status record is not a result for this system, and planned fixture counts are not measured denominators.[[benchmark status record](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current upstream repository at reviewed commit](https://github.com/NirDiamant/Agent_Memory_Techniques/tree/f0b663472899e58568bf3e71b51ac4f2672dd669)
- [Repository README](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/README.md)
- [Technique 30 README — Production Memory Patterns](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/README.md)
- [Technique 30 notebook — Production Memory Patterns](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/f0b663472899e58568bf3e71b51ac4f2672dd669/all_techniques/30_production_memory_patterns/production_memory_patterns.ipynb)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status record](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator attribution](../data/memory-systems.json)

**Verification boundary:** no Agent Memory Techniques notebook, system operation, benchmark, or test was run.