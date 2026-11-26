# Core Memory

## Identity and review pin

- Catalog ordinal: 155
- System: Core Memory
- Slug: `core-memory`
- Listed repository: https://github.com/JohnnyFiv3r/Core-Memory
- Roster attribution: explicit repository locator; the pinned Atlas entry is recorded for curated identity/locator context only, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/core-memory.md)).
- Canonical upstream: https://github.com/JohnnyFiv3r/Core-Memory
- Default branch: `main`
- Reviewed full head: [79f6004653d8b162768c3fc67229c9672fade92e](https://github.com/JohnnyFiv3r/Core-Memory/commit/79f6004653d8b162768c3fc67229c9672fade92e)
- Review timestamp: 2026-11-25T09:20:38Z (UTC; 2026-11-25 01:20:38 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub’s repository page identifies `main` as the default branch. The official main-branch Atom feed reports head `79f6004653d8b162768c3fc67229c9672fade92e`, updated at 2026-11-23T06:03:15Z; the official commit page confirms that revision. ([repository](https://github.com/JohnnyFiv3r/Core-Memory), [main history](https://github.com/JohnnyFiv3r/Core-Memory/commits/main.atom), [head commit](https://github.com/JohnnyFiv3r/Core-Memory/commit/79f6004653d8b162768c3fc67229c9672fade92e))

## Summary

Core Memory is a self-hosted Rust memory engine whose durable record is a PostgreSQL schema. It stores source events verbatim, adds model-produced reads and judged relationships as separate records, and retrieves matching stored text with its current/disputed state and relationship context. It can run as a command, an HTTP service, or inside a host’s PostgreSQL database. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md), [architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md))

## Who and what

The official README names John Inniger and Chris Dedow as maintainers. It describes Core Memory 2 as a self-hosted engine, not a hosted memory service. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md))

## Architecture and data model

The Rust workspace separates contracts and deterministic chunking from the engine pipeline, PostgreSQL store, JSONL source reader, model transports, command/HTTP sidecar, and facade crate. PostgreSQL is the sole durable store. The `core_memory` schema includes workspaces and scopes, source events, chunks and chunk text, beads, read spans, tool outcomes, judge verdicts, arrows/edges, receipts, queues, checkpoints, and an erasure journal. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md), [architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md), [store contract](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/store.rs))

A source event is keyed by scope, source namespace, external ID, and revision. Its original bytes are deterministically divided into lossless chunks; messages/documents use chunk beads, tool calls use one bead for the whole call, and the judge can add textless group beads. Event and chunk IDs are keyed deterministic identifiers within a workspace. ([architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md), [engine](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/engine.rs), [store contract](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/store.rs))

## Write, update, delete, and retrieval

**Write.** Admission validates and chunks an event before storing the event, chunk text, facets, and beads in one transaction. Event identity is checked before chunking: a repeated identical event returns replay without another write; a conflicting identity is refused or handled as a new revision when the source profile allows editable records. Outcomes are typed (accepted, replay, identity conflict, checkpoint conflict, refused, or busy). ([engine](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/engine.rs), [architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md), [store contract](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/store.rs))

**Model reads and relationship updates.** Configured readers can label chunks and locate entities/actions/outcomes as byte ranges in the original chunk. A configured judge chooses candidate beads from time proximity, open disputes, and source-named links; its fixed-vocabulary arrows can express relations, replacement/withdrawal, or contradiction. Replacement/withdrawal becomes effective only after the configured second read agrees. A contradiction leaves both statements current and marks the dispute. These model calls are optional; without reader/judge configuration the original event storage and text recall still work. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md), [architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md), [engine](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/engine.rs))

**Delete/erasure.** Governance functions erase one event, a source key’s revisions, or a scope. Erasure deletes the event’s text and derived read data in one transaction, marks beads erased, and retains IDs as tombstones plus an erasure journal. Re-admission of an erased ID is refused. This is logical erasure: the architecture documentation says PostgreSQL table/index pages, WAL, and backups can retain bytes until operators rewrite/reindex data and expire backups. ([architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md), [README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md))

**Retrieval.** Recall uses PostgreSQL full-text search over stored chunk text and does not call a model. The store ranks text matches, filters results by authorized scopes, substitutes a successor for a replaced match, and can return disputed/current state plus arrows followed up to the request’s follow limit. Recall request construction rejects empty/control-bearing/oversize queries, invalid limits, and scopes outside the caller’s grants. This describes code behavior, not measured answer quality. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md), [recall request](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/recall.rs), [architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md))

## Scope isolation

Every event belongs to a scope within a workspace. HTTP bearer tokens carry separate grants; recall refuses named scopes outside those grants and the store filters results by scope. PostgreSQL row security is enabled on every table, with no public grants. A workspace is also the unit for judging across scopes: a judge can compare memories from different scopes when each scope permits the destination, so a relation formed across scopes can affect currency/dispute interpretation. This is documented design behavior, not an isolation measurement. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md), [recall request](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/recall.rs), [architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md))

## Provenance and evidence

Stored event text remains the source of truth. Reader spans point into source chunk bytes, and records identify the reader/binding configuration; tool outcomes separately identify the model and compressor that produced them. Judge reads and verdicts retain bead IDs, scopes, rubric/binding revisions, and sequence numbers; edges use a fixed arrow directory. Recall results expose the event key/time basis and current/disputed state. These mechanisms provide origin and relationship history, but this review found no claim-level citation contract for arbitrary generated answers: recall returns matching stored text and provenance metadata for a host or caller to use. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md), [architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md), [store contract](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/store.rs))

## Efficiency and observability

Deterministic chunking, PostgreSQL full-text indexing, query limits, transactional sequence ordering, leased work queues, and separate processing lanes provide source-visible efficiency and operational controls. Reader workers are configurable up to 16; permits reserve per-binding daily token/call budgets before sending text. The architecture describes logs/status with work counts, retries, token usage, provider/cache usage, query timings, and problem codes; these are observability surfaces, not measurements made here. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md), [architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md), [store contract](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/store.rs))

## Metric-domain evidence

All project benchmark metrics are **unmeasured** for Core Memory. Source and documentation inspection does not establish measured quality, speed, token use, cost, or storage efficiency. ([metric definitions](../METRICS.md), [project result status](../results/initial-baselines-status.json), [fixture, not run](../fixtures/memory-benchmark-v1.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Lexical full-text recall and typed query refusals are implemented; no scored answer/abstention probes were run. |
| Correction accuracy and stale-value rate | Unmeasured | Replacement/withdrawal uses judged arrows and a second read; no correction workload was run. |
| Deletion leakage | Unmeasured | Transactional logical erasure and tombstones are implemented; no post-erasure probes or disk/backup checks were run. |
| Scope isolation | Unmeasured | Token grants, scope filters, and row security are documented; no cross-scope leakage workload was run. |
| Evidence support and citation coverage | Unmeasured | Source ranges and provenance metadata exist; no generated claims/citations were scored. |
| Retrieval latency | Unmeasured | No timing samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write/recall probes were run. |
| Tokens and cost | Unmeasured | No runtime token usage or charges were collected. |
| Storage efficiency | Unmeasured | No corpus-attributed physical or logical storage size was collected. |

The README reports its own adversarial evaluation counts. They are upstream-reported claims tied to that project's evaluation setup, not results from this project review and not independently verified here. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md))

## Limits and unknowns

This bounded review inspected the current README, architecture documentation, engine admission implementation, store contract, and recall request implementation. It did not inspect every PostgreSQL query, migration, model adapter, sidecar route, or host deployment configuration. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md), [architecture](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md), [engine](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/engine.rs), [recall request](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/recall.rs))

No system runtime, tests, or benchmarks were run. This review therefore does not establish runtime correctness, recall quality, abstention quality, deployed tenant isolation, complete physical erasure, latency, write-to-recall delay, token/cost totals, or storage efficiency. The code inspection also does not establish whether a particular host uses strict grants, configured models, or operator erasure procedures. ([metric definitions](../METRICS.md), [project result status](../results/initial-baselines-status.json))

## Contact

No contact email is published in the official pinned README. The README says bugs and feature requests should be filed as issues and otherwise invites contact with the maintainers directly. The checked official security-policy path returns GitHub “File not found.” No profile/commit metadata or third-party directory was used. ([README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md), [checked SECURITY.md path](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/SECURITY.md))

## Benchmark status

**Benchmark not run.** Core Memory, its tests, and benchmark workloads were not run. The project fixture is a workload specification only; the shared status record marks executions not run and contains no Core Memory measurements. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/core-memory.md)
- [Official repository](https://github.com/JohnnyFiv3r/Core-Memory)
- [Official main commit feed](https://github.com/JohnnyFiv3r/Core-Memory/commits/main.atom)
- [Reviewed full head 79f6004653d8b162768c3fc67229c9672fade92e](https://github.com/JohnnyFiv3r/Core-Memory/commit/79f6004653d8b162768c3fc67229c9672fade92e)
- [Pinned README](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/README.md)
- [Pinned architecture documentation](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/docs/architecture.md)
- [Pinned engine admission source](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/engine.rs)
- [Pinned store contract](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/store.rs)
- [Pinned recall request source](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/crates/core-memory-core/src/recall.rs)
- [Checked official security-policy path](https://github.com/JohnnyFiv3r/Core-Memory/blob/79f6004653d8b162768c3fc67229c9672fade92e/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
