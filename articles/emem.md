# eMEM

## Identity and review pin

- **Catalog position:** 216, “eMEM”; slug `emem`.
- **Listed repository:** [automatika-robotics/emem](https://github.com/automatika-robotics/emem); the roster marks the locator explicit. Atlas is used only for curated identity and locator attribution.
- **Canonical upstream:** [automatika-robotics/emem](https://github.com/automatika-robotics/emem), default branch `main`. Official GitHub repository metadata identifies `main`; the GitHub commit API and fresh `git ls-remote` agree on full current head `82e3da61cf710c4379e0cd7bf7a6a21710caaa96`. A shallow checkout resolved to the same SHA.
- **Reviewed:** 2026-11-25 19:05:02 UTC (2026-11-25 11:05:02 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) supplies the ordinal, slug, listed locator, and roster attribution. The pinned [Atlas record](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/emem.md) is cited for roster attribution only, not as assessment evidence.

## Summary

eMEM is an embedded Python memory library for embodied agents. It stores observations in a typed episode/gist/entity graph and combines SQLite, HNSW vector search, SQLite FTS5, and an in-memory spatial index. Its API supports spatiotemporal and semantic retrieval, but exposes no public memory edit or delete operation. This review makes no runtime or performance claims.

## Who and what

The official [README](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/README.md) describes eMEM as part of the EMOS ecosystem and as a Python library for embodied agents. It advertises ten read-only LLM tools; observations are written by the host perception pipeline. The README links EMOS documentation and a Discord, but publishes no contact email. The checked official email source is the pinned README; no commit or profile metadata or third-party directory was used.

## Architecture and data model

The `SpatioTemporalMemory` facade coordinates a `WorkingMemory` buffer, `MemoryStore`, `ConsolidationEngine`, and `MemoryTools`. Persistent structured records and graph edges live in SQLite (WAL mode); HNSW stores embeddings and ID mappings, FTS5 provides lexical search, and an R-tree-like spatial index is rebuilt in memory from SQLite on startup.[[facade](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/memory.py)] [[store](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/store.py)] [[spatial index](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/spatial.py)]

Observation records include text, coordinates, timestamp, perception layer, source type, confidence, optional episode, metadata, tier, and embedding state. Episodes group observations; gists summarize source observations with spatial/time extents; entities track named objects and locations. Typed edges connect observations, episodes, gists, and entities. This is provenance by identifiers and attribution fields, not a verifiable source citation chain.[[types](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/types.py)] [[store](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/store.py)]

## Write, update, delete, and retrieval

**Write.** `add` creates an observation with caller-supplied text, coordinates, optional timestamp, layer, source type, confidence, metadata, and optional embedding. Working memory batches writes by configured item count or elapsed interval, and assigns observations to an active episode. Embeddings are computed during store insertion when a non-null embedding provider is configured. The default embedding provider is null, so semantic embeddings require configuration or supplied vectors.[[facade](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/memory.py)] [[working memory](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/working_memory.py)] [[config](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/config.py)] [[embeddings](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/embeddings.py)]

**Update and delete.** The inspected public facade and tool definitions expose no observation edit or delete API. Ending an episode can create gists, promote raw observations to long-term, and run entity extraction. Archival changes tier, drops observation text, and removes searchable indexing for the raw record; it is retention/consolidation behavior, not an explicit user-directed deletion or erasure contract. Entity merges can update entity attributes. The README and source do not establish backup erasure or deletion guarantees.[[facade](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/memory.py)] [[consolidation](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/consolidation.py)] [[tools](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/tools.py)]

**Retrieval.** The store supports semantic search over vector candidates and, when hybrid retrieval is enabled, BM25 candidates from FTS5; reciprocal-rank fusion combines them. Filters include layer, time, spatial radius, and episode. Additional tools expose spatial, temporal, entity, gist, episode, current-context, concept-location, and body-state queries. These are source-level capabilities; no retrieval-quality or abstention workload was run.[[store](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/store.py)] [[tools](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/tools.py)]

**Scope isolation.** Each memory instance uses its configured database path. Layer, episode, time, and spatial parameters are query filters, not an authorization boundary. I found no tenant, user, project, or session isolation mechanism in the reviewed facade/store API. Applications requiring isolation must provide it outside this library; no boundary test or security claim was run.[[config](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/config.py)] [[store](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/store.py)]

**Provenance and evidence.** Observation fields preserve source type, timestamp, confidence, layer, optional episode, metadata, and IDs; gists retain IDs of source observations. The inspected model does not require quotations, source URLs, or citation validation, and confidence is not a truth guarantee. Whether a host supplies meaningful provenance is caller-dependent.[[types](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/types.py)] [[consolidation](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/consolidation.py)]

**Efficiency and observability.** Batch flushes and consolidation reduce per-observation storage/index work; SQLite indexes, HNSW, FTS5, and spatial indexing support multiple retrieval paths. The HNSW file is persisted on save/close rather than on each vector insertion, and the spatial index is reconstructed at startup. These implementation choices imply persistence and recovery questions that source inspection alone cannot quantify. No latency, write-to-recall delay, token, cost, throughput, or storage measurement was collected. The inspected public API does not establish operational telemetry or a durable mutation audit trail.[[working memory](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/working_memory.py)] [[store](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/emem/store.py)]

## Metric-domain evidence

- **Answerable retrieval and abstention:** semantic, lexical, spatial, and temporal retrieval paths exist; accuracy and abstention were not measured.
- **Correction and stale values:** no public edit/correction API was found; no correction workload was run.
- **Deletion leakage:** no explicit delete API was found; archival behavior is not evidence of deletion safety.
- **Scope isolation:** filters exist but are not a tenant/session authorization boundary; no isolation probes were run.
- **Evidence support and citations:** source metadata and gist source IDs are available; citation support is not enforced or measured.
- **Retrieval latency and write-to-recall delay:** not measured.
- **Tokens, cost, and storage efficiency:** not measured.

See the project's [metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and [benchmark fixture](../fixtures/memory-benchmark-v1.json). They define the comparison workload and do not report eMEM results.

## Contact

No contact email was found in the official pinned [README](https://github.com/automatika-robotics/emem/blob/82e3da61cf710c4379e0cd7bf7a6a21710caaa96/README.md). Exact checked URL is recorded in [emem.json](../data/system-reviews/emem.json).

## Limits and unknowns

This is a source review at one verified upstream SHA. I did not run eMEM, its tests, or benchmarks. Source inspection cannot establish retrieval accuracy, tenant safety, crash durability across SQLite/HNSW state, archive completeness, physical deletion, scaling, latency, or cost. The configured embedding/LLM providers, host ingestion behavior, and deployment boundary can change behavior and were not evaluated.

## Benchmark status

**Benchmark not run.** No eMEM runtime, tests, or benchmarks were run. See the [project metrics](../METRICS.md), [shared status](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and SHA-pinned upstream URLs are recorded in [emem.json](../data/system-reviews/emem.json). The [curated roster](../data/memory-systems.json) and [pinned Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/emem.md) support identity and locator context only.
