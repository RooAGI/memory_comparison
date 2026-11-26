# Chitta Field — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 115 — Chitta Field / `chitta-field`  
**Listed repository:** [genomewalker/chitta-field](https://github.com/genomewalker/chitta-field)  
**Canonical upstream:** [genomewalker/chitta-field](https://github.com/genomewalker/chitta-field); default branch `main`; reviewed head `5e8b30ed755aa62409ce413385f58edd04039131`  
**Review time:** 2026-11-25 07:49:10 UTC (2026-11-24 23:49:10 PST; America/Los_Angeles)

## Identity and scope

The curated catalog places Chitta Field at ordinal 115, slug `chitta-field`, and lists the repository above with `repository_status: explicit`. Its catalog attribution points to the pinned Agent Memory Atlas report; that attribution is retained for identity and locator context only. Atlas descriptions and capability marks were not assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/chitta-field.md)]

GitHub identifies the public repository and displays `main`; `git ls-remote --symref` resolved remote HEAD to `refs/heads/main`. A shallow checkout of that branch resolved to full SHA `5e8b30ed755aa62409ce413385f58edd04039131`, also returned by `git ls-remote`. The current main commit feed and full commit are linked below.[[repository](https://github.com/genomewalker/chitta-field)] [[main commit feed](https://github.com/genomewalker/chitta-field/commits/main.atom)] [[reviewed head](https://github.com/genomewalker/chitta-field/commit/5e8b30ed755aa62409ce413385f58edd04039131)]

This is a Rust library and C FFI backing store for the cc-soul daemon. The review covers the checked repository source and documentation, not a running deployment.[[README](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/README.md)]

## Architecture and data model

**Code and documentation observation.** The README describes an append-only operation log, in-memory indexes, and periodic binary snapshots. The indexed paths include semantic HNSW/LSH, BM25 keyword, cortical sparse, HDC, temporal, triplet, symbol/call-graph, and artifact indexes. A payload stores memory ID/version, kind, realm, content, embedding metadata, source session/tool, and artifact references; separate mutable state stores deletion, confidence, strength, decay, access history, status, and epistemic status.[[README](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/README.md)] [[payload](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/payload.rs)] [[state](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/state.rs)]

The log uses per-writer segments. Records carry CRCs and a SHA-256 previous-record chain; V3 segment headers include a vector-space identity. Snapshot families and sidecars are selected through a manifest. These are durability and recovery mechanisms visible in source, not independently tested here.[[log](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/log.rs)] [[snapshot](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/snapshot.rs)]

## Write, update, delete, and retrieval

**Write — code observation.** `put_memory` validates embedding dimensions, hashes kind/realm/content/embedding, checks exact duplicates, and can reinforce an existing same-realm near-duplicate when embeddings are available. A new memory is appended to the operation log before in-memory payload/state/index insertion. The API records source session and tool fields when supplied.[[store](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/store.rs)] [[operations](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/ops.rs)]

**Update — code observation.** The inspected `update_state` path appends a state-delta operation and then applies confidence, strength, decay, pin, or access changes. This review did not trace all payload-content replacement operations end to end.[[store](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/store.rs)] [[operations](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/ops.rs)]

**Delete — code observation.** `forget` is explicitly a soft delete: it appends and syncs a delete operation, marks state deleted, removes the item from active retrieval indexes and invalidates sourced triplets. The payload and deletion state remain represented in store/snapshot data; this path does not establish physical erasure from all WAL segments, snapshots, replicas, or backups.[[store](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/store.rs)] [[operations](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/ops.rs)]

**Retrieval — code observation.** Semantic recall searches the ANN index, can constrain candidates by realm, and scores results using memory state. The repository also exposes keyword, temporal, HDC, and other recall paths; its C FFI includes a semantic endpoint and a hybrid semantic/keyword fallback endpoint. The README documents additional sparse and graph retrieval lanes. No recall-quality or latency claim was measured for this review.[[recall](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/store/recall.rs)] [[FFI recall](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/ffi/recall.rs)] [[README](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/README.md)]

## Scope isolation

Memories carry a realm string. Semantic and some other retrieval APIs accept an optional realm filter; `None` permits unscoped retrieval. Realm filtering is an applicability boundary in the library API, not evidence of authenticated tenant isolation or authorization enforcement. No cross-scope probes or deployment authorization review were performed.[[payload](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/payload.rs)] [[recall](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/store/recall.rs)] [[README](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/README.md)]

## Provenance and evidence

Payloads can retain source session and source tool, and the payload type has a provenance field. In the inspected conversion from a put operation, that provenance field is initialized to the literal `human`; source session/tool are separate fields. Other stores expose evidence links for task protocols, but this review does not establish claim-level citations in ordinary recall results or verify the completeness/meaning of provenance across every write path.[[payload](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/payload.rs)] [[operations](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/ops.rs)] [[README](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/README.md)]

## Efficiency and observability

The source includes bounded candidate retrieval and multiple indexes; the README claims sub-millisecond cortical recall and documents HNSW, LSH, and product-quantized structures. Those are documentation/implementation claims, not measurements from this review. The WAL emits diagnostic messages for recovery and replay, while the locking document records operational incidents such as lock contention and slow filesystem calls. No system command, profile, benchmark, test, or telemetry session was run.[[README](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/README.md)] [[log](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/log.rs)] [[locking notes](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/docs/LOCKING.md)]

## Metric-domain evidence

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Multiple recall APIs and score fields exist. | Unmeasured |
| Correction and stale values | State/status and update operations exist; end-to-end correction quality was not checked. | Unmeasured |
| Deletion leakage | Soft-delete path marks state and removes active indexes. | Unmeasured |
| Scope isolation | Optional realm filters are visible in retrieval APIs. | Unmeasured |
| Evidence support and citations | Session/tool lineage fields exist; ordinary recall claim-level citation behavior was not established. | Unmeasured |
| Retrieval latency and write-to-recall delay | README describes performance goals; this review collected no timing samples. | Unmeasured |
| Tokens and cost | No token or provider-cost observations were collected. | Unmeasured |
| Storage efficiency | WAL, snapshots, and sidecars are implemented; no bytes-per-memory measurement was collected. | Unmeasured |

The project metric definitions and fixture specify future measurement domains; they are not Chitta Field results. The initial benchmark status record remains not run.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[status](../results/initial-baselines-status.json)]

## Contact

The official pinned repository README was checked for a published contact email and contains none. The record stores `contact_email: null` with the checked README URL.[[README](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/README.md)]

## Limits and unknowns

This source review cannot establish recall accuracy, abstention calibration, correction/staleness behavior, deletion completeness, cross-tenant security, recovery correctness under crashes, multi-writer convergence, live-provider behavior, or operational latency/cost/storage. The upstream THEORY document itself discusses non-commutative updates and snapshot-manifest conflict risks in the multi-writer model; those documented caveats reinforce that README claims about NFS-safe concurrent writes are not runtime guarantees from this review.[[theory](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/THEORY.md)] [[locking notes](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/docs/LOCKING.md)]

## Benchmark status

**Benchmark not run.** No Chitta Field system command, test, or workload was executed. The project metric definitions, fixture, and initial execution-status record are linked for protocol context only; none contains a measured Chitta Field result from this review.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[status](../results/initial-baselines-status.json)]

## Sources

- [Curated catalog entry and ordinal](../data/memory-systems.json)
- [Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/chitta-field.md)
- [Official repository and default branch](https://github.com/genomewalker/chitta-field)
- [Current main commit feed](https://github.com/genomewalker/chitta-field/commits/main.atom)
- [Reviewed full head](https://github.com/genomewalker/chitta-field/commit/5e8b30ed755aa62409ce413385f58edd04039131)
- [README.md](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/README.md)
- [src/payload.rs](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/payload.rs)
- [src/state.rs](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/state.rs)
- [src/ops.rs](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/ops.rs)
- [src/store.rs](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/store.rs)
- [src/store/recall.rs](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/store/recall.rs)
- [src/ffi/recall.rs](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/ffi/recall.rs)
- [src/log.rs](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/log.rs)
- [src/snapshot.rs](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/src/snapshot.rs)
- [THEORY.md](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/THEORY.md)
- [docs/LOCKING.md](https://github.com/genomewalker/chitta-field/blob/5e8b30ed755aa62409ce413385f58edd04039131/docs/LOCKING.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Initial benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** source and documentation were inspected read-only. No system, benchmark, or tests were run.
