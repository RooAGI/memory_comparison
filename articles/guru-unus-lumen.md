# GURU source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 278 / GURU / guru-unus-lumen  
**Listed repository locator:** [GuruProduction/GURUbyUnusLumen](https://github.com/GuruProduction/GURUbyUnusLumen)  
**Canonical upstream:** [GuruProduction/GURUbyUnusLumen](https://github.com/GuruProduction/GURUbyUnusLumen)  
**Default branch / reviewed head:** main / [366208c8799d39cd5ec3921dd85a3d418e93810b](https://github.com/GuruProduction/GURUbyUnusLumen/commit/366208c8799d39cd5ec3921dd85a3d418e93810b)  
**Review time:** 2026-11-25 22:09:07 UTC (2026-11-25 14:09:07 PST; America/Los_Angeles).

## Identity and review pin

The curated roster lists GURU at ordinal 278, slug guru-unus-lumen, with the explicit locator https://github.com/GuruProduction/GURUbyUnusLumen. The Atlas record is retained only as roster attribution and locator context, not assessment evidence. The official repository page identifies main as the default branch. GitHub’s official main commit API reports full head SHA 366208c8799d39cd5ec3921dd85a3d418e93810b, with commit time 2026-11-21T10:43:08Z; the repository page shows the matching short hash 366208c. The review below is pinned to that commit.[[catalog]][[atlas]][[repo]][[head]]

## Summary

GURU is an Android agent app whose Cerebrum memory engine is a Rust workspace hosted in-process by the app. The current source describes layered buffer, episodic, and semantic memories, several retrieval indexes, graph structures, a mutation event store, and encrypted local persistence. These are source observations; no GURU runtime or benchmark was run.[[readme]][[architecture]][[state]]

## Who and what

The official README identifies GURU as an Android application built by Steven Newman / Unus Lumen. Cerebrum is integrated into the Android app through a JNI bridge; it is not presented as a standalone hosted memory service. Conversation history stays in a separate Room store, while the Cerebrum brain uses its own encrypted vault.[[readme]][[architecture]][[android]][[persistence]]

## Architecture and data model

The Cerebrum workspace is divided into crates for shared memory contracts, encrypted persistence, storage, decay, episodes, graph operations, embeddings, signatures, curation, event tracking, query, and protocol handling. Its core crate defines shared identifiers and data contracts; the storage crate exposes put/get/delete/prefix-scan and flush operations alongside in-memory WAL and snapshot helpers. CerebrumState aggregates engines and indices, including a context tree, graph store, lexical index, embeddings, signatures, dynamic wavelet matrix, episodic store, decay engine, event store, policy summaries, and hot caches.[[architecture]][[core]][[storage]][[state]]

The Android host keeps the brain in the app process. JNI calls reach the Rust host, which exchanges framed requests over an app-private Unix socket. The host marks mutating frames dirty and schedules a trailing save after the last mutation. The architecture guide describes Room conversation history as separate from Cerebrum memory.[[android]][[architecture]]

Persistence serializes subsystem state as tagged vault records. The crypto crate specifies an Argon2id-derived key and XChaCha20-Poly1305 record encryption, with the passphrase and derived key held in RAM during the host session. The Android bridge zeroizes the passphrase when the brain stops. This describes the implementation’s stated format and lifecycle; it is not a cryptographic audit.[[persistence]][[crypto]][[android]]

## Write, update, delete, and retrieval

**Write.** The request protocol has a CURATE operation. Its handler routes curation through multiple memory surfaces: context tree, lexical index, graph, event store, episode store, embeddings, signatures, policy summaries, and caches. This is a multi-index write path, so correctness depends on the subsystems staying aligned.[[handler]][[state]]

**Update and correction.** Curation and consolidation include mutation, duplicate-resolution, and memory promotion mechanisms. The code documents these flows, but no correction sequence was exercised here and the review does not establish that every surface retains a complete history of replaced values.[[handler]][[decay]][[readme]]

**Delete.** The handler has a shared retirement check for archived context-tree entries, allowing read surfaces to consistently hide retired memories. The README describes deletion as archiving rather than erasure. This does not establish physical removal from prior vault generations, backups, exports, or copies.[[handler]][[readme]][[persistence]]

**Retrieval.** The protocol provides separate query, retrieve, search, graph traversal, list, prefetch, and consolidation operations. The query engine classifies queries and routes retrieval across tiers; the state aggregates lexical, embedding, signature, graph, episodic, and hot-cache structures. The code structure documents available paths, not retrieval accuracy.[[handler]][[query]][[state]]

The episodic store can reconstruct an episode with its discovery context, valence, and related-episode IDs. It can search by source or trigger, and has a configurable capacity that evicts the oldest entry when the limit is reached.[[episodic]]

The README describes memories moving from buffer to episodic to semantic as they are recalled, with access strengthening, decay, and a daily consolidation pass. The Rust decay defaults instead specify a one-hour buffer half-life, a 30-day episodic half-life, and archival after a configured age and hibernation threshold. These are source defaults, not observed runtime behavior; the mismatch remains unresolved.[[readme]][[decay]]

## Scope isolation

GURU is documented as a local, owner-operated Android app with an in-process brain. The inspected aggregate state and request handlers do not show tenant or project authorization keys. That fits the single-owner product shape, but the code inspection does not establish isolation for multiple users or application clients; no cross-scope access test was run.[[readme]][[state]][[handler]]

## Provenance and evidence

The episodic model stores source, trigger, context, and related-episode identifiers. The aggregated state includes an event store described as an audit trail of memory mutations. These provide lineage and mutation-recording mechanisms, but the review did not establish that each derived claim remains linked to complete source evidence or that generated answers cite entailing records.[[episodic]][[state]][[handler]]

## Efficiency and observability

The design maintains specialized indexes and hot caches for retrieval. The Android bridge reports status, request counts, and the last error, and schedules encrypted persistence after mutations. The persistence layer rewrites a vault generation rather than appending repeated snapshots. No latency, write-to-recall, token, cost, storage, or interruption-recovery measurements were collected.[[state]][[android]][[persistence]]

The README says the memory vault is encrypted at rest and cloud backup is disabled. The security policy says prompts and recalled context are sent to the model endpoint selected by the user; therefore local storage does not mean recalled content stays on-device when a cloud model is configured. Neither claim was independently tested in a running device.[[readme]][[security]]

## Metric-domain evidence

The project [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define comparison protocol and status; they are not GURU results. All domains below remain unmeasured.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Query classification, tiered retrieval, and confidence routing exist in source. | Unmeasured |
| Correction and stale values | Curation, consolidation, and memory lifecycle mechanisms exist. | Unmeasured |
| Deletion leakage | Archived entries are hidden by a shared retirement predicate; physical erasure was not established. | Unmeasured |
| Scope isolation | Product is locally operated; no tenant isolation workload was run. | Unmeasured |
| Evidence support and citations | Episode provenance and mutation event structures exist; no answer evidence was adjudicated. | Unmeasured |
| Latency and write-to-recall delay | Host status and deferred persistence exist; no operation timings were collected. | Unmeasured |
| Tokens, cost, and storage | Local vault and configured model integration are documented; no token, charge, or storage comparison was made. | Unmeasured |

## Limits and unknowns

- The README’s seven-day decay description differs from the decay crate’s default half-lives and archival threshold. Runtime configuration and scheduling behavior were not exercised, so this cannot be resolved from this review.[[readme]][[decay]]
- The source supports archival and read filtering, but this review did not establish erasure from backups, old vault generations, exported data, or data already sent to an inference provider.[[handler]][[persistence]][[security]]
- The reviewed state is a single-owner in-process aggregate. Multi-tenant authorization and cross-user isolation were not demonstrated or tested.[[architecture]][[state]]
- The repository’s security policy says the project has not had a professional external security audit and identifies gaps in the broader trust chain. This source review was not a security audit.[[security]]
- The cited Rust source contains unit tests, but no tests, GURU runtime, benchmark fixture, or device workload was run. Retrieval quality, correction behavior, deletion leakage, scope behavior, crypto correctness, performance, and reliability remain unknown.[[metrics]][[fixture]][[status]]

## Benchmark status

**Benchmark not run.** No GURU runtime, tests, or benchmark fixture was executed. The project metric definitions, fixture, and shared status record describe protocol and execution status, not GURU benchmark results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and SECURITY.md publish steven@unuslumen.com. The structured record stores the address with the pinned README URL and records both checked official URLs. No commit/profile metadata, third-party directory, or inferred address was used.[[readme]][[security]]

## Sources

All upstream source links are pinned to the verified full SHA. The Atlas link is roster attribution only, not assessment evidence. See the structured [GURU review record](../data/system-reviews/guru-unus-lumen.json) and [curated roster](../data/memory-systems.json).

