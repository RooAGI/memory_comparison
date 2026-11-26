# Chronotope (tempomem)

## Identity and review pin

- **System:** Chronotope
- **Curated position:** 116
- **Slug:** tempomem
- **Listed repository:** [wikieden/tempomem](https://github.com/wikieden/tempomem)
- **Canonical repository at review:** [wikieden/tempomem](https://github.com/wikieden/tempomem)
- **Default branch:** main
- **Reviewed head:** [92181fbbae7f5e66714aa5e91f61ba9558b1f1aa](https://github.com/wikieden/tempomem/commit/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa)
- **Reviewed:** 2026-11-25 07:48:04 UTC (2026-11-24 23:48:04 PST; America/Los_Angeles)
- **Review status:** Reviewed from current source and documentation
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/tempomem.md), used for catalog identity, listed repository and attribution only.

The local catalog places Chronotope at ordinal 116 with slug tempomem, listed repository https://github.com/wikieden/tempomem, and explicit roster attribution.[[catalog]] The official GitHub repository metadata confirms the canonical public repository and default branch main; the API reports current main head 92181fbbae7f5e66714aa5e91f61ba9558b1f1aa with commit timestamp 2026-07-03T02:13:33Z.[[repo]][[head]] A read-only git ls-remote check and shallow checkout independently resolved main to the same full SHA. This review was checked at the timestamp above.[[revision]]

## Summary

Chronotope is a pre-alpha Python library for persistent spatial memory. It stores detections as observations in a local SQLite scene graph, fuses them into object nodes, and supports geometric, temporal, label or optional embedding retrieval. This review reports source observations only; the system and benchmarks were not run.[[readme]][[schema]][[api]]

## Who and what

Chronotope is the repository's project name; tempomem is the package and repository name. It is a library, not a hosted memory service. The documented core expects caller-provided object detections and feature vectors. An RGB-D adapter protocol exists, but the official README says the ConceptGraphs adapter is still a work in progress.[[readme]][[frame]][[api]]

## Architecture and data model

The persistent unit is one SQLite .smem file. Tables store episodes, raw observations, aggregate scene nodes, typed edges, and many-to-many links from observations to nodes. A node contains a canonical label and label distribution, confidence, 3D centroid and bounding box, feature vector, observation count, timestamps, and optional parent region. Observations preserve timestamp, episode/session, label, confidence, 3D geometry, feature, optional mask and caller-defined auxiliary JSON.[[schema]][[persist]][[frame]]

On write, detections become observation rows and pending IDs. commit() fuses pending observations: it finds nearby candidates by a linear bounding-box overlap scan, combines geometry, box overlap, feature cosine and label compatibility, then merges into a matching object, rejects a low-confidence unmatched observation, or creates a node. Region hierarchy and inferred relations are represented separately.[[store_api]][[fusion]][[config]][[store_impl]][[relations]]

The optional [vec] extra enables sqlite-vec for node-feature semantic search. Feature blobs remain canonical and the vector table is rebuildable; without the extension, semantic search uses a linear cosine scan. Spatial retrieval scans nodes. Prompt serialization can include hierarchy and relation labels and cap output by a token budget, marking omitted content.[[schema]][[query_impl]][[serialize]][[readme]]

## Write, update, delete, and retrieval

**Writing.** add_detections() accepts detections with normalized feature vectors, open-vocabulary labels, confidence, center, bounding box, optional timestamp, episode/session, mask and aux fields. add_frame() runs a caller-provided RGB-D adapter before staging detections. Writes are fused at explicit commit(), unless a configured pending-observation threshold auto-flushes them.[[api]][[frame]][[store_api]][[config]]

**Update and history.** update() changes a node label, center or confidence in place. Renaming resets its label distribution to the new label. history() returns the observations still linked to that node; merge() ingests objects from another store through the fusion path.[[api]][[store_api]]

**Delete and maintenance.** forget() deletes the node and its observation links, incident edges and properties; children are reparented to avoid dangling region links. It does not delete the raw observation rows themselves. decay() lowers object confidence over time and prunes below a threshold. resplit() and consolidate() are caller-invoked maintenance methods, not background jobs.[[api]][[store_api]][[store_impl]]

**Retrieval.** query() first attempts simple relation-phrase and anchor-label matching. Temporal intent returns recent nodes. Spatial retrieval uses linear centroid distance or a keyword fallback; semantic retrieval uses an encoder plus optional sqlite-vec, or linear cosine; without an encoder, semantic search falls back to label substring matching. answer() serializes context and requires a caller-supplied verbalizer. The API accepts an episode on ingest but the reviewed query surface has no episode filter.[[api]][[query_spec]][[store_api]][[query_impl]][[schema]]

## Scope isolation

Episode/session labels organize ingest records, but the reviewed retrieval API does not filter by episode and the code does not show tenant or principal authorization. One local database file is the documented store boundary. Whether a deployment isolates multiple users or agents is unknown; no isolation workload was run.[[schema]][[api]][[store_api]][[readme]]

## Provenance and evidence

Node-to-observation links preserve a node's timestamps, episode IDs and spatial sightings; observation rows can also contain caller-defined aux JSON. The inspected schema does not require source documents, evidence excerpts, authors, trust state or validated citations. Retrieval does not establish support for factual statements. The available fields provide observation lineage rather than a verified evidence chain.[[schema]][[persist]][[frame]][[query_impl]]

## Efficiency and observability

The code exposes commit elapsed time and store statistics, including node/edge/observation counts and SQLite bytes. Optional sqlite-vec supports vector search; the built-in semantic fallback and spatial lookup scan nodes, while relation inference examines object pairs. Architecture documents describe structured fusion-decision logs, but this review did not verify every logging path. Published latency budgets are targets, not measurements.[[store_api]][[store_impl]][[query_impl]][[relations]][[architecture]][[query_spec]]

## Metric-domain evidence

Every quality and performance domain is **unmeasured in this review**. Source mechanisms, project metrics and benchmark plans are not Chronotope results.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Query mechanisms are implemented; no answerable or unanswerable probes were evaluated. | Unmeasured |
| Correction accuracy and stale values | In-place updates and observation history exist; no correction sequence was scored. | Unmeasured |
| Deletion leakage | Node deletion leaves observation rows; no post-delete retrieval or residual-store probe was run. | Unmeasured |
| Scope isolation | Ingest has episode labels; no access-control or cross-session leakage workload was assessed. | Unmeasured |
| Evidence support and citation coverage | Observation lineage and aux fields exist; no evidence adjudication was performed. | Unmeasured |
| Retrieval latency and write-to-recall delay | Commit timing and retrieval code exist; no workload timings were collected. | Unmeasured |
| Tokens, cost and storage | Serializer budget and store-byte counters exist; no token, cost or storage-efficiency measurements were collected. | Unmeasured |

The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) describe project evaluation criteria and status, not Chronotope measurements.[[metrics]][[fixture]][[status]]

## Limitations and unknowns

This is a bounded, read-only review of selected documentation, specifications and source modules at the pinned head. It does not establish runtime behavior, production stability, crash recovery, every adapter path, or deployed authorization behavior.[[readme]][[api]][[persist]]

The repository labels itself pre-alpha. The README marks the ConceptGraphs RGB-D integration as work in progress. The query API is limited to implemented relation phrases and keyword/embedding fallbacks; episode-scoped retrieval is not present in the inspected query interface. Linear spatial and fallback semantic scans may become costly as the store grows, and relation inference compares object pairs; no scale or latency result was measured.[[readme]][[query_spec]][[query_impl]][[relations]][[open_questions]]

Hard deletion removes a node and its associations but leaves its observation rows in the SQLite database. The reviewed sources do not establish a full purge, backup, or replica cleanup policy.[[store_api]][[store_impl]][[schema]]

## Benchmark status

**Benchmark not run.** I did not execute Chronotope, its tests, or a benchmark workload. No runtime quality, latency, token, cost, storage, correction, deletion, evidence, or scope-isolation result is claimed. The linked project metrics and fixture describe evaluation criteria and planned workload only.[[metrics]][[fixture]][[status]]

## Contact

No contact email was found in the pinned official [README](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/README.md), the official documentation page checked for project contact. The author metadata in package configuration was not used as contact evidence.[[readme]]

## Sources

- [Curated catalog](../data/memory-systems.json) — ordinal, slug, listed repository and roster attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/tempomem.md) — attribution only.
- [Official GitHub repository](https://github.com/wikieden/tempomem) — canonical repository and default branch.
- [GitHub API repository metadata](https://api.github.com/repos/wikieden/tempomem) — canonical name and default branch.
- [GitHub API current main head](https://api.github.com/repos/wikieden/tempomem/commits/main) — full current SHA and commit timestamp.
- [Reviewed head](https://github.com/wikieden/tempomem/commit/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa)
- [README](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/README.md) — product scope, implemented features and pre-alpha state.
- [Architecture](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/docs/en/02-ARCHITECTURE.md) — architecture and documented observability.
- [API specification](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/spec/API.md) — public API and planned features.
- [Schema specification](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/spec/SCHEMA.md) — object model and storage.
- [Fusion specification](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/spec/FUSION-ARBITER.md) — merge scoring and maintenance design.
- [Query specification](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/spec/QUERY-ROUTER.md) — query pathways and targets.
- [TempoMem API implementation](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/src/tempomem/__init__.py)
- [Detection model](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/src/tempomem/frame.py)
- [SQLite schema](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/src/tempomem/persist/schema.sql)
- [Store implementation](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/src/tempomem/store.py)
- [Query implementation](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/src/tempomem/query/__init__.py)
- [Relation inference](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/src/tempomem/relations.py)
- [Prompt serializer](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/src/tempomem/serialize.py)
- [Open questions](https://github.com/wikieden/tempomem/blob/92181fbbae7f5e66714aa5e91f61ba9558b1f1aa/docs/en/05-OPEN.md)
- [Project metrics](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) — project evaluation criteria/status, not system results.

**Verification boundary:** read-only source and documentation review; no Chronotope runtime, tests, or benchmarks.
