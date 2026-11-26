# Aura

## Identity and review pin

- **System:** Aura
- **Curated position:** 76
- **Slug:** `aura`
- **Listed repository:** [youngbryan97/aura](https://github.com/youngbryan97/aura)
- **Default branch:** `main`
- **Reviewed head:** [`b391aed058f6f133e0308fbb63a99339f752cc8c`](https://github.com/youngbryan97/aura/commit/b391aed058f6f133e0308fbb63a99339f752cc8c)
- **Reviewed:** 2026-11-24 21:52:17 UTC (13:52:17 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/aura.md), used only for name, slug, listed repository, and attribution.

The curated roster places Aura at ordinal 76 with slug `aura` and listed locator `https://github.com/youngbryan97/aura`. A fresh read-only `git ls-remote --symref` identified `main` as the remote HEAD/default branch at `b391aed058f6f133e0308fbb63a99339f752cc8c`; a shallow checkout of that SHA matched. The official README describes Aura as an experimental local desktop assistant. All repository source links in this review pin to that full SHA.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/youngbryan97/aura)] [[official main feed](https://github.com/youngbryan97/aura/commits/main.atom)] [[reviewed head](https://github.com/youngbryan97/aura/commit/b391aed058f6f133e0308fbb63a99339f752cc8c)]

## Summary

Aura's memory system is a collection of local stores and retrieval paths rather than one database: working context, SQLite episodic records, semantic and vector memory, graph structures, user profiles, and procedural memory. Its code includes governed writes, provenance fields, several recall strategies, and retention paths. This article reports selected source behavior at the reviewed commit; it does not measure recall quality, privacy isolation, or deletion completeness.[[memory architecture](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/docs/MEMORY_ARCHITECTURE.md)] [[README](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/README.md)]

## Who and what

The public repository is maintained under GitHub account youngbryan97. Its README presents Aura as an experimental, local desktop assistant and cognitive architecture for Apple Silicon rather than a hosted memory service. The README points readers to a dedicated memory reference and describes separate runtime tiers and stores.[[repository](https://github.com/youngbryan97/aura)] [[README](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/README.md)]

## Architecture and data model

The memory guide describes working, episodic, semantic, and strategic/procedural tiers, with cold storage, snapshots, vector retrieval, and entity/knowledge graphs. It presents a broad design; this review inspected a selected subset and does not establish that every described module is active in every setup.[[memory architecture](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/docs/MEMORY_ARCHITECTURE.md)] [[README memory overview](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/README.md)]

The episodic implementation stores event-like records in SQLite. Its schema includes context, action, outcome, success, importance, emotional values, lessons and tags, decay/access fields, and source/session/exchange revision and supersession metadata. The vector layer stores text with metadata and embeddings; the documented SQLite vector fallback stores embeddings in binary blobs. These are distinct records and indexes, not one uniform memory schema.[[episodic store](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/episodic_memory.py)] [[vector memory](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/vector_memory.py)] [[SQLite vector store](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/sqlite_vector_store.py)]

## Write, update, delete, and retrieval

Episodic recording accepts context, action, outcome, success, importance, source, metadata, and an optional idempotency key. It calls the constitutional write gate; if that gate errors while the constitutional runtime is live, the write is deferred, but when the runtime is not live the inspected fallback can allow the write. The separate canonical gateway authorizes writes, uses an atomic schema-versioned file write, emits a MemoryWriteReceipt, and tries to restore the previous record if receipt emission fails. This source review does not establish that every memory family writes exclusively through that gateway.[[episodic write](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/episodic_memory.py)] [[write gateway](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/memory_write_gateway.py)]

Episodic recall can combine semantic vector candidates, keyword fallback when the vector set is short or the query requests exact wording, and hippocampal cue pattern completion. The merged candidates are ranked and the returned memories are registered as recalled. The semantic memory API exposes edit and delete; semantic deletion marks the entry deleted. Episodic hard deletion removes episode and cue rows and attempts matching vector deletion. Retention and consolidation also remove or compact some records. None of these selected paths establishes full erasure across every store, backup, export, or derived copy.[[episodic recall](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/episodic_recall.py)] [[vector memory](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/vector_memory.py)] [[semantic memory](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/brain/semantic_memory.py)] [[episodic storage](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/episodic_memory.py)] [[memory guide](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/docs/MEMORY_ARCHITECTURE.md)]

The facade searches multiple backends and filters returned records against principal context when both principal ID and surface are provided. In the inspected episodic route, candidate retrieval occurs before that facade-level check; the episodic database has source session/exchange fields but no tenant column, and the vector recall call filters by memory type. The README frames Aura as local and single-owner oriented. These observations do not prove a leak, but they leave cross-user isolation across all memory paths unverified.[[memory facade](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/memory_facade.py)] [[episodic recall](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/episodic_recall.py)] [[episodic schema](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/episodic_memory.py)] [[user profiles](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/user_profile.py)]

## Metric-domain evidence

These are code observations, not measurements. Benchmark status is not run.

| Domain | Source observation | Review measurement |
|---|---|---|
| Answerable retrieval and abstention | Episodic retrieval merges vector, keyword, and cue-based candidates, then ranks them. | Unmeasured |
| Correction and stale values | Semantic edit and episodic source revision/supersession fields are present. | Unmeasured |
| Deletion leakage | Semantic deletion marks entries; episodic deletion removes episodic/cue rows and attempts vector cleanup. | Unmeasured |
| Scope isolation | The facade applies principal visibility filtering after candidate retrieval on the inspected path; not all paths show the same boundary. | Unmeasured |
| Evidence and citations | Provenance helpers define source, confidence, contested, reviewed-time, and recall-use fields; episodes retain source references. | Unmeasured |
| Latency and write-to-recall delay | Episodic recall times retrieval stages and logs slow calls above a source-defined threshold. | Unmeasured |
| Tokens and cost | Model-backed embedding and fallback paths are visible; token and cost accounting was not measured. | Unmeasured |
| Persistent storage | SQLite episode and vector persistence are visible; storage growth was not measured. | Unmeasured |

The project’s [metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) describe evaluation and reporting, not results for Aura.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

Aura is a large repository with multiple memory stores and background paths. This bounded inspection does not audit every writer, reader, retention job, API, or integration. It cannot establish answer quality, calibrated confidence, correction accuracy, complete deletion, multi-user isolation, latency, token use, or storage efficiency. The memory documentation describes constraints and mechanisms, but those descriptions are not runtime evidence.[[README](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/README.md)] [[memory architecture](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/docs/MEMORY_ARCHITECTURE.md)] [[metrics](../METRICS.md)]

## Contact-list follow-up

I checked the official pinned [README](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/README.md), [SECURITY.md](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/SECURITY.md), and [LICENSE](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/LICENSE). The LICENSE publishes **bry.young124@gmail.com** for commercial licensing inquiries; the JSON record stores this address and the exact pinned source URL. No commit metadata or profile email was used.

## Benchmark status

**Benchmark not run.** No Aura runtime, benchmark workload, build, or tests were run for this review. Source structure, documentation, and upstream claims are not measurements from this review. The project’s metric definitions, fixture, and execution status are linked above.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution only.
- [Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/aura.md) — identity and locator attribution only.
- [Official repository](https://github.com/youngbryan97/aura) — repository identity.
- [Main branch feed](https://github.com/youngbryan97/aura/commits/main.atom) and [reviewed head](https://github.com/youngbryan97/aura/commit/b391aed058f6f133e0308fbb63a99339f752cc8c) — branch and revision pin.
- [README](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/README.md)
- [Memory architecture](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/docs/MEMORY_ARCHITECTURE.md)
- [Episodic memory store](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/episodic_memory.py)
- [Episodic recall](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/episodic_recall.py)
- [Vector memory](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/vector_memory.py) and [SQLite vector store](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/sqlite_vector_store.py)
- [Memory write gateway](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/memory_write_gateway.py) and [provenance envelope](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/provenance.py)
- [Memory facade](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/memory_facade.py) and [user profile store](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/memory/user_profile.py)
- [Semantic memory mutation API](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/core/brain/semantic_memory.py)
- [Security policy](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/SECURITY.md) and [license/contact](https://github.com/youngbryan97/aura/blob/b391aed058f6f133e0308fbb63a99339f752cc8c/LICENSE)
- [Project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json)

**Verification boundary:** pinned source inspection only; no Aura execution, benchmarks, builds, or tests.
