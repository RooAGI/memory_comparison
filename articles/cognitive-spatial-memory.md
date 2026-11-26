# Cognitive Spatial Memory — source review

**Review status:** Reviewed from official documentation and source at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 138 — Cognitive Spatial Memory / `cognitive-spatial-memory`  
**Listed repository:** [munch2u-a11y/Cognitive-Spatial-Memory](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory)  
**Canonical upstream:** same repository; default branch `main`; reviewed head [39df03a18d202a25f4c066d662109f85128886ef](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/commit/39df03a18d202a25f4c066d662109f85128886ef)  
**Review time:** 2026-11-25 08:37:24 UTC (2026-11-25 00:37:24 PST; America/Los_Angeles)

## Identity and scope

The catalog places Cognitive Spatial Memory at ordinal 138, slug `cognitive-spatial-memory`, with an explicit repository locator and pinned Atlas attribution. Atlas was used only to establish roster identity and locator, not as assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cognitive-spatial-memory.md)]

The public official repository page shows `main` as the default branch. Its official main commit feed reports full head `39df03a18d202a25f4c066d662109f85128886ef`, updated 2026-05-23T22:38:36Z, matching the catalog revision. The inspected README and project docs are linked at this SHA.[[repository](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory)] [[main commit feed](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/commits/main.atom)] [[reviewed head](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/commit/39df03a18d202a25f4c066d662109f85128886ef)]

## Architecture and data model

The project presents a Python memory library that maps text embeddings into a fixed eight-dimensional spatial manifold. The `SpatialMemory` entry point exposes `store()`, `query()`, and `get_context()`; a physics engine delegates to spatial mind and cognitive-space components. The repository README describes two spaces, one for beliefs and one for episodic memories, sharing a projection matrix.[[README](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/README.md)] [[entry-point audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part2_mind_engine_entry.md)]

The core stores points with an eight-dimensional position, type, confidence or importance, text, creation pulse, and last-access pulse. A seeded random orthogonal projection maps source embeddings to stable spatial coordinates; the documented default input is 384-dimensional. A KD-tree supplies nearby candidates, which are ranked by temperature × mass / distance². Beliefs and memories use different mass and cooling parameters. These are design descriptions, not evidence of retrieval quality.[[core-engine audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part1_core_engine.md)]

Beliefs are also persisted as categorized JSON files. Episodic storage is pluggable: the README names JSONL, SQLite, and ChromaDB backends, with JSONL as the default. The README says belief confidence can be recalculated and describes nightly attrition; the repository docs describe an optional lifecycle that can prune low-confidence beliefs. The exact scheduling and operational guarantees depend on integrating the surrounding lifecycle components.[[README](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/README.md)] [[peripheral-systems audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part3_peripheral_systems.md)]

## Write, update, delete, and retrieval

**Write.** `store()` persists an entry in the configured backend, then registers a point in the manifold; the entry point defaults to JSONL and also initializes a separate belief store. The basic API does not describe extraction, deduplication, or comparison with existing episodic items.[[entry-point source](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/spatial_memory/__init__.py)] [[README](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/README.md)]

**Update and delete.** I found no update/delete/forget operation for points in the documented `SpatialMemory` API. Its JSONL backend is described as append-only. The separate belief store supports confidence recalculation and pruning in its lifecycle, but the inspected sources do not establish a general user-directed correction, deletion, or purge guarantee across both persisted records and manifold state.[[README](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/README.md)] [[peripheral-systems audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part3_peripheral_systems.md)]

**Retrieval.** `query()` returns nearby points ranked by the system's gravity score, and `get_context()` formats a neighborhood for model injection. The preconscious interface described in the docs additionally extracts concepts, issues multiple gravity queries, avoids repeated selections, and adds scratchpad notes and spatial-state annotations. This is a described ranking and context assembly pipeline; no answer quality or abstention result was measured.[[README](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/README.md)] [[peripheral-systems audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part3_peripheral_systems.md)]

## Scope isolation

The reviewed data model and public API descriptions do not identify tenant, user, agent, or project keys on memory points or filtering controls in the basic query API. Consequently, the inspected material does not demonstrate isolation between callers or scopes; deployments would need an external partitioning boundary and independent verification.[[core-engine audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part1_core_engine.md)] [[README](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/README.md)]

## Provenance and evidence

Points contain their text and timing/type/weight information, but the reviewed descriptions do not show source-document identifiers, claim-level citations, trust states, or mutation audit records. Confidence or importance affects ranking mass; it is not a provenance or verification state. The belief lifecycle docs mention verification counts in confidence recalculation, but do not establish evidence-backed answers.[[core-engine audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part1_core_engine.md)] [[peripheral-systems audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part3_peripheral_systems.md)]

## Efficiency and observability

The docs describe a KD-tree rebuilt lazily after additions and a gravity grid with 512 anchors; the audit states potential computation scales with point count times anchor count. This suggests an explicit indexing and approximation strategy but provides no independently verified latency or scale result. The inspected README and audit docs do not describe production metrics or tracing for the memory API; one internal field tracks gravity-field computation time.[[core-engine audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part1_core_engine.md)]

## Metric-domain evidence

All project benchmark domains remain unmeasured. No runtime, tests, or benchmark were run for this review.

- **Recall and abstention — unmeasured.** The repository describes gravity ranking and context injection, but no adjudicated retrieval workload.[[README](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/README.md)]
- **Correction and stale retrieval — unmeasured.** The documented basic point API has no correction path; no stale-value probes were run.[[entry-point audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part2_mind_engine_entry.md)]
- **Deletion leakage — unmeasured.** No general deletion guarantee is established in the reviewed descriptions, and no post-delete probes were run.[[peripheral-systems audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part3_peripheral_systems.md)]
- **Scope isolation — unmeasured.** No multi-scope isolation workload was run.[[README](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/README.md)]
- **Evidence support and citation coverage — unmeasured.** No answer-level support audit was performed.[[core-engine audit](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/docs/audit_part1_core_engine.md)]
- **Latency, write-to-recall delay, tokens, cost, and storage efficiency — unmeasured.** No measurements were collected.[[metric definitions](../METRICS.md)]

## Limits and unknowns

This is a source-based assessment of the official README and three repository audit documents at the verified head. The audit documents are project-authored summaries; this review did not independently read every implementation path or verify each line-specific statement. Exact backend behavior, pulse scheduling, the relationship between belief pruning and in-memory points, persistence/reload consistency, and performance under realistic data remain unknown. No tests, system execution, or benchmark was performed.

## Contact

The official pinned README publishes `helix.agi.email@gmail.com` for commercial licensing questions. It is recorded as published contact, not as a technical support address.[[official README](https://github.com/munch2u-a11y/Cognitive-Spatial-Memory/blob/39df03a18d202a25f4c066d662109f85128886ef/README.md)]

## Benchmark status

Benchmark status is `not_run`. No runtime, tests, or benchmarks were run for this source review.[[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark status record](../results/initial-baselines-status.json)]
