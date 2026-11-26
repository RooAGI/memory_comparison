# HeurChain source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 293 / HeurChain / `heurchain`  
**Listed repository locator:** [peterjohannmedina/heurchain](https://github.com/peterjohannmedina/heurchain)  
**Canonical upstream:** [peterjohannmedina/heurchain](https://github.com/peterjohannmedina/heurchain)  
**Default branch / reviewed head:** master / [2da09e66626044661355540c320c8a4cb3d23b15](https://github.com/peterjohannmedina/heurchain/commit/2da09e66626044661355540c320c8a4cb3d23b15)  
**Review time:** 2026-11-25 22:56:38 UTC (2026-11-25 14:56:38 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists HeurChain at ordinal 293, slug `heurchain`, with the explicit locator `https://github.com/peterjohannmedina/heurchain`. The catalog’s pinned Atlas entry records roster attribution only; it is not assessment evidence. The official repository page identifies `master` as the default branch. The official `master.atom` commit feed reports current head `2da09e66626044661355540c320c8a4cb3d23b15`, updated 2026-11-23T03:42:31Z. This review is pinned to that full SHA. [[catalog]][[atlas]][[repo]][[head]]

## Summary

HeurChain is a self-hosted Go memory broker that stores tenant-scoped agent memories in Redis and combines BM25 keyword search with dense Qdrant search. It supports sessions, lifecycle consolidation, versioned correction, and explicit forget operations. This is a source review, not a runtime or performance evaluation. [[readme]][[records]][[recall]]

## Who and what

The official README describes this repository as the complete self-hosted edition: broker source, Docker Compose stack, systemd unit, and documentation. Agents connect over HTTP/JSON or MCP. It labels the broker line version 0.6.1-oss.1 and says it is frozen for new broker features, with fixes and documentation continuing. [[readme]]

## Architecture and data model

The README describes four local components. Redis is the source of truth for memory records, sessions, BM25 keyword indexes, and vault entries. An embedding service is required for writes. Qdrant stores dense vectors, while SQLite stores tenant records, API-key hashes, audit entries, and usage counts. Memory records include text, tags, agent/session identifiers, and timestamps; the lifecycle implementation also stores revisions, metadata, namespace, and change reason. [[readme]][[records]][[schema]]

The Go broker exposes HTTP endpoints and MCP tools. Requests carry a tenant ID and API key. The tenant scopes Redis key names and Qdrant collections; the key is checked against bcrypt hashes for that tenant in SQLite, with successful checks cached briefly in Redis. These are service-level tenant boundaries; this review did not test deployment configuration. [[readme]][[auth]][[schema]]

Corrections use optimistic revisions. An update preserves earlier content in a bounded history, increments the revision, and rejects a stale expected revision. The history is capped at 100 versions and 1 MiB. Checkpoint snapshots cannot be corrected. Get and list operations can surface active or archived records; list pagination explicitly does not provide a stable snapshot under concurrent writes. [[records]][[api]]

## Write, update, delete, and retrieval

**Write.** The broker authenticates the tenant, embeds the text, writes the record to Redis, then updates the BM25 and dense indexes. These steps are not one distributed transaction: an indexing error can leave the source write acknowledged with a retry indication. Qdrant is recommended but optional; without it, the README says storage continues and search falls back to keywords. The embedder is required for writes. [[readme]][[recall]][[api]]

**Update.** The correction API requires an expected revision and a short reason. It accepts changed text, metadata, tags, or namespace; changed text is embedded again before storing the next revision. A mismatched revision returns a conflict, and history remains bounded. [[api]][[records]]

**Delete / forget.** Explicit forget requires the expected revision and `confirm=true`. It removes active and archived copies, retained revision content, and BM25 state, then writes a non-expiring tombstone and deletes the Qdrant point. If dense-index cleanup fails, the response reports incomplete cleanup and asks for retry. The code checks tombstones on reads so residue from a stale restore or older writer is hidden. [[forget]][[records]]

The broker defines the forget boundary narrowly: the memory ID and revisions in broker storage and indexes. Backups, independently copied records, and context already returned to clients are outside that guarantee. [[forget]]

**Retrieval.** Search embeds the query and runs BM25 and dense retrieval concurrently, then fuses ranks. Tenant-level scoping, optional exact-agent and any-tag filters, and metadata eligibility checks are applied before and during result hydration. Tombstoned content is excluded. Search diagnostics can report embedding/cache timing, retrieval timing, candidate counts, backend status, and results returned. [[readme]][[recall]]

## Scope isolation

Every request must authenticate an API key for the supplied tenant. Redis keys include that tenant, and dense search uses tenant-specific Qdrant collections. The optional agent filter narrows results within the tenant; the inspected paths do not establish a separate credential boundary per agent. No cross-tenant test or deployed authorization review was performed here. [[auth]][[schema]][[recall]]

## Provenance and evidence

Memory text, tags, agent ID, timestamps, and change reason are stored with the record. The audit schema tracks tenant, actor key ID, action, resource ID, revision details, and agent ID; the update helper explicitly avoids writing memory content into audit telemetry. An agent-provenance endpoint aggregates observed request details and activity for a bounded recent window, which can help distinguish same-named agent instances but does not verify claims in memory. [[records]][[api]][[schema]][[provenance]]

The reviewed record and recall paths do not show source-document citations or independent validation of stored facts. Attribution and lifecycle metadata describe what the system recorded; they do not prove that a memory is true or that an answer is supported. [[records]][[recall]]

## Efficiency and observability

The broker runs lexical and dense retrieval in parallel and uses reciprocal-rank fusion. It bounds candidate processing, applies filters to avoid unrelated dense candidates consuming the search budget, and records per-search diagnostics. Query embedding cache hits and BM25/Qdrant backend status are visible in those diagnostics. [[recall]]

A background worker applies ACT-R-style activation decay and can move low-activation memories into an exportable vault that search does not query. The README says this promotion is dry-run by default; operators can configure live promotion. The README also reports LoCoMo development results: roughly 4,900–5,000 input tokens per question versus about 117,000 for full conversation, with reader scores from 4.8 percentage points below to 1.9 points above the full-history baseline. These figures are upstream-reported, not independently measured here. [[consolidation]][[readme]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for HeurChain in this review. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [baseline status record](../results/initial-baselines-status.json) describe project evaluation materials, not HeurChain results. [[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Hybrid retrieval and filters exist; answer quality and abstention were not scored. | Unmeasured |
| Correction and stale values | Revision-checked updates preserve bounded history; no correction workload was run. | Unmeasured |
| Deletion leakage | Forget removes broker copies and indexes and adds a tombstone; no deletion or recovery probe was run. | Unmeasured |
| Scope isolation | Tenant-bound keys and tenant-scoped stores are implemented; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | The inspected paths do not establish source-backed answer evidence; no claim adjudication was performed. | Unmeasured |
| Retrieval latency and write-to-recall delay | Diagnostics expose timing fields; no measurements were collected. | Unmeasured |
| Tokens, cost, and storage efficiency | README token figures are upstream-reported; no token, cost, or storage workload was measured here. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the current official README and selected broker implementation paths. HeurChain, its tests, and benchmarks were not run. The review does not establish real-world retrieval quality, agent behavior, deployment security, backup recovery, or durable consistency through every Redis/Qdrant failure mode. [[readme]][[records]][[recall]][[forget]]

The repository README reports benchmark results on 543 scored LoCoMo development questions. Those figures are upstream claims and are kept separate from this review’s unmeasured project benchmark status. Automatic recall qualification is documented for specific client builds and Windows; this review did not verify other client versions or platforms. [[readme]]

## Benchmark status

**Benchmark not run.** No HeurChain runtime, tests, or benchmarks were executed. No project result is claimed for retrieval, correction, deletion, scope isolation, evidence support, latency, token use, cost, or storage. The [project metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [baseline status record](../results/initial-baselines-status.json) are evaluation materials only. [[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email; none was present. The structured record stores `contact_email: null` and the exact checked README URL. No address was inferred from commit or profile metadata or taken from a third-party directory. [[readme]]

## Sources

All upstream source file links are pinned to the verified full SHA. The Atlas link documents curated roster attribution only and is excluded as assessment evidence. See the structured record [heurchain.json](../data/system-reviews/heurchain.json) and [curated roster](../data/memory-systems.json).
