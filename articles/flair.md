# Flair source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 240 / Flair / `flair`  
**Listed repository locator:** [tpsdev-ai/flair](https://github.com/tpsdev-ai/flair)  
**Canonical upstream:** [tpsdev-ai/flair](https://github.com/tpsdev-ai/flair)  
**Default branch / reviewed head:** main / [5a9dd65a027adb6206c871018000393c9425065f](https://github.com/tpsdev-ai/flair/commit/5a9dd65a027adb6206c871018000393c9425065f)  
**Review time:** 2026-11-25 20:30:49 UTC (2026-11-25 12:30:49 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Flair at ordinal 240 with slug `flair` and explicit locator `https://github.com/tpsdev-ai/flair`. The pinned Atlas attribution is retained only as curated identity and locator context; Atlas descriptions and capability marks are not assessment evidence. GitHub identifies `tpsdev-ai/flair` as the canonical repository with default branch `main`; the official commits API and a fresh `git ls-remote` agree on full current head `5a9dd65a027adb6206c871018000393c9425065f`. A shallow checkout of `main` resolved to the same commit.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Flair is a self-hosted agent identity and memory service implemented as a native Harper application. It stores memories in Harper/RocksDB, creates embeddings in process, and combines vector and lexical retrieval. This review reports source and documentation observations only; it does not measure system behavior or performance.[[readme]][[schema]][[bm25]]

## Who and what

The current README presents Flair as an open-source, self-hosted identity and memory substrate for agents, with a CLI, Harper server, MCP integrations, client libraries, and framework bridges. This review focuses on its memory service and adjacent scope controls; it does not establish a full maintainer roster.[[readme]][[repo]]

Harper handles HTTP and persistence in one process. The repository says local embeddings do not require a separate vector database or embedding API.[[readme]]

## Architecture and data model

The Memory table stores an owner agent ID, text, visibility, durability, timestamps, optional temporal validity and supersession fields, archive state, provenance, and search/use counters. Its embedding column is indexed with HNSW. Relationships are separate temporal subject-predicate-object records.[[schema]][[api]]

The README documents in-process nomic-embed-text-v1.5 embeddings with 768 dimensions on CPU or supported GPU. Search combines HNSW vector candidates with a BM25 lexical candidate set using reciprocal rank fusion (RRF). The repository also defines vector-only and BM25-only retrieval modes.[[readme]][[bm25]]

The semantic endpoint applies scope, archive, and optional tag, subject, time, and score filters. It fetches more candidates than the requested result limit before selecting results and supports optional query-plan and per-leg candidate diagnostics.[[retrieval]][[scope]]

The MCP surface includes `memory_store`, `memory_search`, `memory_update`, `memory_get`, and `memory_delete`. Local stdio clients and the native OAuth `/mcp` endpoint are separate integration paths; the native route is off by default.[[readme]][[api]]

## Write, update, delete, and retrieval

**Write.** Authenticated agent writes are attributed to the caller and restricted to that agent's own rows. Writes are auto-embedded when the local embedding path is available. Server-controlled fields include provenance timestamps and a row-incarnation token. Durability defaults to `standard`; omitted visibility defaults to `private` for standard or ephemeral records and `shared` for permanent or persistent records.[[memory]][[schema]][[access]]

**Update and correction.** The memory update flow can edit a row in place or create a successor through `supersedes`. The schema also has `validFrom` and `validTo` for temporal validity. Maintenance archives expired standard memories and reaps expired ephemeral memories; these lifecycle labels do not promise backup or replica acknowledgements.[[api]][[schema]][[readme]]

**Delete and archive.** Owner or admin `DELETE /Memory/<id>` is the user-facing delete operation; deletion history can be appended for permanent-memory deletes. Basement/archive marks a row and can be reversed, retaining the row. Physical purge is a separate operator/internal operation with post-commit confirmation and is not authorized by agent keys, including admin-agent keys.[[api]][[archive]][[purge]]

**Retrieval.** The default mode combines BM25 and vector candidates with RRF. Search accepts optional filters and opt-in trust evidence or abstention. Semantic similarity is a ranking signal, not a calibrated probability that a memory answers the query correctly.[[bm25]][[retrieval]][[readme]]

**Scope isolation.** A verified non-admin reader can access its own memories at any visibility and other agents' non-private memories on that instance. `private` is owner-only; a missing visibility field is treated as non-private for legacy records. Writes remain owner-scoped. Admin and trusted in-process reads are broader, and federation provides an inter-instance boundary. Thus same-instance non-private memory is shared knowledge rather than per-agent read-isolated data.[[scope]][[access]][[memory]]

## Provenance and evidence

Local writes stamp server-derived agent identity and receipt time in the provenance record. Caller-supplied creation time, model, or client fields remain claims. Search can expose provenance and opt-in trust context; trust information is added for the reader and does not make authorization decisions. Source pointers and explicit usage signals provide additional traceability, but they do not prove a memory claim or entail a generated answer.[[schema]][[memory]][[retrieval]][[api]]

## Efficiency and observability

The implementation uses HNSW, a bounded BM25 candidate set with RRF fusion, scope-aware filtering, selected-field projections, and batched source-pointer joins. Search-hit counts go to a separate `MemoryHitStat` table rather than rewriting every memory hit; explicit use feedback is counted separately. Explain mode and optional per-leg results expose query and candidate diagnostics. These are implementation observations, not measured latency, throughput, or storage results.[[bm25]][[retrieval]][[hits]][[schema]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Flair. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe evaluation materials, not Flair results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Hybrid retrieval and opt-in abstention are present in source; no answers were scored. | Unmeasured |
| Correction and stale values | In-place/successor updates and temporal validity are represented; no correction sequence was probed. | Unmeasured |
| Deletion leakage | Delete, archive, and operator purge paths are documented; no post-delete retrieval workload was run. | Unmeasured |
| Scope isolation | Same-instance open-read policy and private-owner exception are documented; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Provenance and optional trust/source information are available; no answer claims were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Vector and lexical paths are present; this review collected no timings. | Unmeasured |
| Tokens, cost, and storage | No benchmark workload token, charge, or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This bounded review covers the current README, API/access-control documentation, Memory schema, centralized scope rule, selected CRUD/archive/purge code, retrieval, scoring, and hit tracking at the verified SHA. Flair, its tests, and benchmarks were not run.[[readme]][[api]][[access]][[schema]][[memory]][[scope]][[retrieval]][[archive]][[purge]][[bm25]][[scoring]][[hits]]

The docs describe a self-hosted service and state that agent signing keys do not encrypt memory data. Deployment security, backup/restore behavior, and production configuration were not exercised.[[readme]][[access]]

Same-instance non-private reads are intentionally available to every verified agent. Whether that policy fits an installation depends on its trust boundary and visibility choices; private visibility and federation do not make all same-instance reads tenant-isolated.[[scope]][[access]]

Source structure and project-published retrieval claims do not establish recall quality, abstention calibration, deletion leakage, scope safety under workload, concurrency outcomes, latency, cost, or storage efficiency. Those remain unverified here.[[readme]][[metrics]][[fixture]][[status]]

## Benchmark status

**Benchmark not run.** No Flair runtime, tests, or benchmarks were executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned [README](https://github.com/tpsdev-ai/flair/blob/5a9dd65a027adb6206c871018000393c9425065f/README.md), [SECURITY.md](https://github.com/tpsdev-ai/flair/blob/5a9dd65a027adb6206c871018000393c9425065f/SECURITY.md), and [CONTRIBUTING.md](https://github.com/tpsdev-ai/flair/blob/5a9dd65a027adb6206c871018000393c9425065f/CONTRIBUTING.md) were checked for a contact email; none was found.[[readme]][[security]][[contributing]] No contact was inferred from commit/profile metadata or a third-party directory.

## Sources

Repository code and documentation links are pinned to the verified full SHA. The Atlas attribution above is included only for curated identity and locator context. See the structured record [flair.json](../data/system-reviews/flair.json) and the [curated roster](../data/memory-systems.json).
