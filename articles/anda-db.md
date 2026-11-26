# Anda DB

## Identity and review pin

- **System:** Anda DB
- **Curated position:** 56
- **Slug:** `anda-db`
- **Listed repository:** [ldclabs/anda-db](https://github.com/ldclabs/anda-db)
- **Default branch:** `main`
- **Reviewed head:** [`e9c4959a24619fcf84b0e8afaf199dd19b44b09b`](https://github.com/ldclabs/anda-db/commit/e9c4959a24619fcf84b0e8afaf199dd19b44b09b)
- **Reviewed:** 2026-11-24 20:46:42 UTC (12:46:42 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/anda-db.md), used only to resolve this entry’s catalog identity, listed locator, and source attribution.

The curated roster places Anda DB at ordinal 56 with slug `anda-db` and listed locator `https://github.com/ldclabs/anda-db`. The Atlas entry is retained for attribution only; its descriptions, marks, and layout are not assessment evidence. GitHub’s official repository page identifies the canonical public repository and `main` as its default branch. Its latest commit prefix (`e9c4959`) matches the full head in the official main-branch feed. The review pins code and documentation citations to that full SHA.[[roster entry](../data/memory-systems.json)] [[official repository](https://github.com/ldclabs/anda-db)] [[official main feed](https://github.com/ldclabs/anda-db/commits/main.atom)] [[reviewed head](https://github.com/ldclabs/anda-db/commit/e9c4959a24619fcf84b0e8afaf199dd19b44b09b)]

## Summary

Anda DB is an embedded Rust document database and a workspace of storage, retrieval, and KIP components for building persistent agent memory. The Cognitive Nexus reference engine represents concepts, claims, evidence, and activity, with belief projected from assertions at read time. This review describes source-visible behavior at the pinned revision; it does not measure runtime quality or performance.

## Who and what

The repository identifies LDC Labs in its copyright/license text and presents Anda DB as a modular Rust workspace, rather than a single hosted memory service. It includes the embedded database, KIP SDK, Rust Cognitive Nexus reference engine, HTTP service crates, a shard proxy, Python binding, and an independent TypeScript KIP engine for Cloudflare Durable Objects. The Rust and TypeScript engines share a conformance fixture suite, according to the repository documentation.[[README](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/README.md)]

## Architecture and data model

**Code and documentation observations.** The storage layer uses schema-aware collections and B-Tree, BM25 full-text, and HNSW vector indexes. Its object-store abstraction supports local and cloud backends; optional wrappers add metadata/conditional updates and chunked AES-GCM encryption. The Cognitive Nexus stores distinct row kinds for Concepts, Propositions, Assertions, Evidence, and Activities, alongside Space, transaction, schema, control, and version-history collections.[[README](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/README.md)] [[Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)]

A Proposition is a truth-neutral subject/predicate/object tuple. An Assertion records an actor’s stance, mode, confidence, valid time, and supporting Evidence. Evidence can represent an observed message, tool result, or document passage; an Activity records process provenance. Current belief is computed from eligible Assertions under a named projection policy, rather than stored as another truth field. The projection source explicitly says evidence quality is not automatically evaluated.[[Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)] [[epistemic projection](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/projection/mod.rs)]

A MemorySpace is the ownership and policy boundary, not a topic label. Its row includes principals, policy/classification defaults, lifecycle status, schema environment version, and a monotonically increasing sequence. The sequence orders commits even when they share a timestamp. The transaction engine stages declarative mutations, assigns an element version once at commit, records a transaction, and provides atomic visibility under the Cognitive Nexus in-process write lock.[[Space store](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/store/space.rs)] [[transaction engine](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/tx.rs)] [[Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)]

## Write, update, delete, and retrieval

**Write and update.** KIP Mutation Language (KML) supports creation, upsert, proposition creation, Evidence/Assertion/Activity creation, field and lifecycle updates, retention changes, and merge operations. A mutation is planned before commit; multiple clauses form one declarative transition, so clause order is not update order. An element’s version advances once per transaction when its final state changes. A no-effect write does not emit a false change. Each committed row version is retained in the history log.[[Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)] [[transaction engine](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/tx.rs)] [[version history](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/store/history.rs)]

**Correction and world change.** The data model keeps old Assertions rather than rewriting claim history. A correction can supersede a prior Assertion; a world change closes its valid-time interval while preserving what was true earlier. Misrecording repair is a separate, protected operation. Competing actors’ assertions can coexist, and a projection can report contested, uncertain, rejected, or insufficient states. These are representational and source-level behaviors, not evidence of correction accuracy.[[Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)] [[epistemic projection](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/projection/mod.rs)]

**Delete and retention.** Archive and tombstone are lifecycle transitions; they keep records and make them unavailable to ordinary active-state matching by default. `PURGE` is the destructive path. The inspected purge code checks legal holds and authorization, defaults to denying referenced-element erasure, removes historical versions, and leaves an identity/audit stub with a content digest. This does not establish erasure from backups, external copies, or application-owned source data.[[Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)] [[purge implementation](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/governance/purge.rs)] [[version history](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/store/history.rs)]

**Retrieval.** KIP Query Language (KQL) matches graph patterns, traverses relationships, filters, projects, aggregates, pages, and supports text/vector search integrated with a query. The database combines BM25 and HNSW candidates with reciprocal-rank fusion and applies B-Tree filters. For belief questions the caller uses projection rather than treating a stored Proposition as true. `FOR TIME` asks what applied in the world then; `AS OF SEQ` asks what the Space contained at a prior commit.[[README](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/README.md)] [[Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)] [[version history](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/store/history.rs)]

## Scope isolation

Each Nexus query context is bound to one Space. The technical reference describes Space filtering on every element match and authorization as part of the query read path; callers need an authorized session for another Space. The repository also warns that a database must have one live writer and that sharded deployments must route each Space to exactly one process. These are source-visible boundaries; this review did not exercise server authentication, deployment policy, or cross-tenant isolation under load.[[Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)] [[Space store](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/store/space.rs)] [[README](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/README.md)]

## Provenance and evidence

Assertions link actor, stance, confidence, valid time, and evidence references; Evidence can identify source artifacts, and Activities can record inputs, outputs, and actors. Committed mutations carry receipts and change records, with a transaction journal and per-element version history. These affordances support inspection of how state changed. The projection documentation expressly limits the claim: evidence quality is not automatically evaluated, so stored references alone do not verify factual support.[[Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)] [[transaction engine](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/tx.rs)] [[epistemic projection](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/projection/mod.rs)]

## Source-visible efficiency and observability

**Code/documentation observations, not measurements.** The README describes B-Tree narrowing plus BM25 and HNSW retrieval with reciprocal-rank fusion, configurable collection/index setup, bounded caches, and object-store persistence. The Nexus reference sets a shared 100,000 intermediate candidate/work budget; exceeding it fails with a resource-exhaustion error, and a query limit does not bypass that budget. Historical reads are bounded as well. The project documents counters, transaction history, receipts, and structured service logs, but those facilities do not provide this review with latency or cost measurements.[[README](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/README.md)] [[Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)] [[transaction engine](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/tx.rs)]

## Metric-domain evidence

All domains below are **unmeasured for this review**. The table records only what the inspected design/code provides as a measurement target.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | KQL search and projection distinguish supported, contested, uncertain, and insufficient belief states. | Unmeasured; no answerable/unsupported probe set was run. |
| Correction and staleness | Assertions retain lifecycle and valid-time history; changes and versions are recorded. | Unmeasured; no correction or stale-value probes were run. |
| Deletion leakage | Purge covers current rows and the version log, with a digest stub; external copies are outside this boundary. | Unmeasured; no post-purge retrieval or copy audit was run. |
| Scope isolation | Session reads are Space-bound and authorization-aware in the engine. | Unmeasured; no cross-Space isolation probes were run. |
| Evidence support and citation coverage | Assertions and activities can link evidence and record provenance. | Unmeasured; no claim-to-source adjudication was run. |
| Latency and write-to-recall delay | Source includes indexed/vector/text retrieval and query work limits. | Unmeasured; no workload or timing was collected. |
| Tokens, cost, and storage | Persistence and model integrations are described by the workspace; no review-specific accounting was made. | Unmeasured. |

The project’s metric definitions, fixture, and initial execution status are linked for context. Their planned domains and case counts are not Anda DB measurements.[[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded inspection of selected source and documentation at the reviewed SHA. It does not establish runtime correctness, answer quality, authorization in a deployment, backend parity, crash recovery in practice, deletion completeness, or performance. The source and docs describe multiple engines, adapters, and service layers that were not all inspected. The engine documents a 100,000 query-work budget, a one-live-writer constraint per database, and capabilities that are explicitly refused when unsupported. Whether a specific application’s configuration provides its required privacy, durability, or retrieval quality remains unknown without integration testing.

## Contact-list follow-up

I checked the official pinned repository README and the official project website, [anda.ai](https://anda.ai/), for a published contact email. Neither page publishes one, so the JSON record stores `contact_email: null` and records both checked source URLs. No address was inferred.

## Benchmark status

**Benchmark not run.** No Anda DB system execution, benchmark workload, build, or tests were run for this review. Source structures, documentation statements, and repository-reported test/benchmark activity are not results from this review. See [metric definitions](../METRICS.md), the [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).

## Sources

- [Curated roster entry](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution only.
- [Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/anda-db.md) — identity/locator attribution only.
- [Official repository](https://github.com/ldclabs/anda-db) — canonical repository and default branch.
- [Official main commit feed](https://github.com/ldclabs/anda-db/commits/main.atom) — full current head.
- [Reviewed head](https://github.com/ldclabs/anda-db/commit/e9c4959a24619fcf84b0e8afaf199dd19b44b09b)
- [README](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/README.md)
- [Cognitive Nexus technical reference](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/docs/anda_cognitive_nexus.md)
- [Transaction engine](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/tx.rs)
- [Space store](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/store/space.rs)
- [Version history](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/store/history.rs)
- [Purge implementation](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/governance/purge.rs)
- [Epistemic projection](https://github.com/ldclabs/anda-db/blob/e9c4959a24619fcf84b0e8afaf199dd19b44b09b/rs/anda_cognitive_nexus/src/projection/mod.rs)
- [Official project website](https://anda.ai/) — checked for a published contact email.
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only source review; no system execution, benchmarks, build, or tests.
