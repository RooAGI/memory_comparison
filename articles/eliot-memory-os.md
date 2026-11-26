# ELIOT Memory OS source and design review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 213 / ELIOT Memory OS / `eliot-memory-os`  
**Listed repository locator:** [UnknownAlienHuman/eliot-memory-os](https://github.com/UnknownAlienHuman/eliot-memory-os)  
**Canonical upstream:** [UnknownAlienHuman/eliot-memory-os](https://github.com/UnknownAlienHuman/eliot-memory-os)  
**Default branch / reviewed head:** main / [1c19f33dbd8ca5278cea283ccecfaa073b9f8ac9](https://github.com/UnknownAlienHuman/eliot-memory-os/commit/1c19f33dbd8ca5278cea283ccecfaa073b9f8ac9)  
**Review time:** 2026-11-25 18:56:52 UTC (2026-11-25 10:56:52 PST; America/Los_Angeles).

## Identity and review pin

The catalog places ELIOT Memory OS at ordinal 213 with slug `eliot-memory-os`, an explicit locator, and a pinned Agent Memory Atlas roster attribution. The catalog and Atlas source were used only for identity, listed locator, and attribution; Atlas descriptions and capability marks were not assessment evidence. GitHub's official repository API identifies `main` as the default branch, and its commit API plus a shallow checkout independently resolve the current head to `1c19f33dbd8ca5278cea283ccecfaa073b9f8ac9`. The checkout's committer timestamp is 2026-11-05 19:14:43 UTC. The source review below is pinned to that head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

The current ELIOT Memory OS V3 material describes a local-first memory daemon and Store intended to preserve host observations, reconstruct addressed work, retrieve applicable context, and revise memory from outcomes. Upstream explicitly calls the V3 README a documentation baseline and says it is not a released runtime; V1/V2 source remains donor material. The findings below therefore describe documented V3 contracts, not verified V3 operation.[[readme]][[architecture]]

## Who and what

The official README describes ELIOT Memory OS as the core local-first Rust repository, with Eliot Search and Eliot Research maintained as optional providers in separate repositories. The reviewed material is a design/repository project, not a released V3 runtime. This review does not infer a maintainer identity from commit or profile metadata.[[readme]][[repo]]

## Architecture and data model

The V3 design assigns observation capture, memory revisions, retrieval, context, outcomes, and finite jobs to a Memory daemon, with a narrow host relay and a private SurrealDB Store. It selects six `SCHEMAFULL` tables (`stream`, `observation`, `memory`, `memory_history`, `link`, and `job`) plus immutable blobs, but the architecture document expressly says these are design selections rather than a running or qualified Store.[[architecture]][[implementation]][[store]]

The data model separates accepted source observations, interpreted memory claims, and revisions. Observations retain occurrence and source identities, exact accepted bytes or blob references, hashes, workspace/task or actor/session binding, capture limitations, disclosure, and attributed source relations. Memory revisions carry structured content, applicability/qualifiers, source grounds, and history; exact source opening is intended to resolve an exact observation or memory revision and verify its hashes.[[architecture]][[cognition]][[implementation]]

**Code observation — retained V1/V2 donor only.** The current tree defines `EpistemicStatus` and `LifecycleStatus` in `crates/eliot-types/src/memory.rs` and `CanonicalClaimCard` in `crates/eliot-store/src/canonical_observation_models.rs`. The older store has `recall_l0` code in `crates/eliot-store/src/canonical_store.rs`. Upstream labels these V1/V2 sources as donors, so these symbols do not prove V3 is implemented.[[legacy-code]][[legacy-model]][[legacy-recall]][[readme]]

## Write, update, delete, and retrieval

**Capture and write.** The contract stages an immutable capture command before Store send, then commits a bounded observation and its source relations in one transaction. Stable source event keys can make host redelivery idempotent; otherwise retries reuse the frozen command identity. Replay is designed to read back the original observation rather than minting a replacement. The docs state this path is still to be connected and qualified.[[implementation]][[registry]]

**Correction and update.** Notes and commitments are ordinary scoped memories linked to source observations. A direct correction must name the expected current revision, retain history, and publish the new revision, attributed cause, source grounds, and replacement together; exact retries return the original result and stale expected revisions conflict. This is a contract, not observed behavior at the reviewed head.[[cognition]][[implementation]]

**Delete, withdraw, and erase.** The design distinguishes withdrawal of guidance from erasure of content. Durable notices are intended to survive rollback and block stale replay or restore; erasure is monotonic and must be accompanied by verified cleanup of controlled current/history rows, blobs, spool entries, and derived packet/job copies. A committed notice is not itself proof of physical deletion. Delivered host transcripts and provider copies remain outside the deletion guarantee, and the documentation says the source implementation, Windows durability, and full cleanup inventory remain open.[[architecture]][[implementation]][[registry]]

**Retrieval.** The documented flow resolves the current work address first, then forms bounded candidate sets from direct handles, exact cues, lexical search, optional vectors, grounds/relations, and methods. Project/work scope applies before per-arm limits. A response is to disclose examined scope, unavailable arms, truncation, gaps, and exact source handles; a zero top-K result means no match in that examined retrieval, not proof that no relevant item exists. Selected content is intended to preserve negation, version, conditions, exceptions, and source/revision identity.[[architecture]][[cognition]]

## Scope isolation

The design binds work to project and workspace plus an actual task when supplied; otherwise it uses an actual actor/session pair. It rejects widening an empty or unavailable task lookup into a project-wide substitute. Retrieval applies project/work scope before candidate limits. These are documented design boundaries, not demonstrated authorization or cross-scope isolation: no runtime probes were run, and upstream states local OS access is not a hostile same-user sandbox.[[cognition]][[implementation]][[architecture]]

## Provenance and evidence

The design preserves accepted source before interpretation and keeps source, representation, and claim identities separate. It uses exact observation/revision handles, body and revision hashes, typed source relations, and grounds groups to track support. Similarity scores and model prose are not treated as truth or citation evidence; unknown or incomplete support is meant to remain qualified or cause abstention. These invariants have not been verified in a connected V3 runtime.[[architecture]][[cognition]][[implementation]]

## Efficiency and observability

The proposed retrieval path uses bounded candidate arms, byte-bounded records and packets, deterministic ordering, and a bounded lexical snapshot; optional vectors are additive. Exact token ceilings require a real host counter, and upstream docs explicitly distinguish configured limits from measured usage. Status and recovery are designed around durable readback of capture/replay, Store, notice, backup, and cleanup state. No latency, token, cost, storage, or throughput observations were collected for this review; the docs describe limits and owners, not measured efficiency.[[cognition]][[implementation]]

## Metric-domain evidence

All project evaluation domains are **unmeasured** for ELIOT Memory OS in this review. Source and design contracts do not establish result quality or operating guarantees. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the evaluation protocol and project status, not ELIOT results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Bounded retrieval arms, scope rules, source handles, and explicit gaps are specified; no answers were scored. | Unmeasured |
| Correction and stale values | Expected-revision updates and history are specified; no correction sequence was exercised. | Unmeasured |
| Deletion leakage | Notice and controlled-copy cleanup are specified; no erase or post-erase probe was run. | Unmeasured |
| Scope isolation | Project/work addressing and filtering are specified; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Grounds, source relations, and exact opens are specified; no response evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timings were collected. | Unmeasured |
| Tokens, cost, and storage | Limits are specified, but no workload or resource measurements were collected. | Unmeasured |

## Limits and unknowns

The repository states that the V3 design is not implemented behavior and that retained V1/V2 source is donor material. Selected legacy type and recall code remains in the tree, but it cannot establish V3 support. The Store guide describes an unmerged source candidate and says the schema/query package is not a working Store; the registry leaves Store connection, writer/readback, runtime qualification, and several cleanup and scenario paths open. This review did not run the system, its tests, or benchmarks, and did not treat donor V2 code as V3 evidence.[[readme]][[architecture]][[legacy-code]][[store]][[registry]]

The design itself identifies important boundaries: the Memory inference extension is not yet available; local OS permissions do not provide a hostile same-user sandbox or portable encrypted backups; prior host transcripts and provider copies cannot be recalled; and complete cleanup, Windows durability, deployed isolation, retrieval correctness, and actual performance remain unknown.[[architecture]][[implementation]][[registry]]

## Benchmark status

**Benchmark not run.** No ELIOT runtime, tests, or benchmark workload were executed. No quality, latency, token, cost, storage, deletion, correction, or isolation measurement is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json); these describe the evaluation protocol and status, not ELIOT results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and V3 documentation were checked for a published contact email. No address was found; the record stores `contact_email: null` and the exact checked URLs. No commit/profile metadata, third-party directory, or inferred address was used.[[readme]][[architecture]]

## Sources

Repository citations are pinned to the verified full SHA except the repository/API and current-head identity records. The Atlas link is retained only for roster attribution, not system assessment. See the structured record [eliot-memory-os.json](../data/system-reviews/eliot-memory-os.json) and [curated roster](../data/memory-systems.json).
