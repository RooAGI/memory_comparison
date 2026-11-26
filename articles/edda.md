# Edda

## Identity and review pin

- Catalog ordinal: 208
- System: Edda
- Slug: `edda`
- Listed repository: https://github.com/fagemx/edda
- Roster attribution: explicit repository locator; the pinned Atlas entry is recorded only for curated identity/locator attribution, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/edda.md)).
- Canonical upstream: https://github.com/fagemx/edda
- Default branch: `main`
- Reviewed full head: [46bf30ec215546912a1833b3c3b808e53f9e0025](https://github.com/fagemx/edda/commit/46bf30ec215546912a1833b3c3b808e53f9e0025)
- Review timestamp: 2026-11-25T12:01:54Z (UTC; 2026-11-25 04:01:54 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

The official GitHub repository API identifies public, non-fork `fagemx/edda` and names `main` as its default branch. The GitHub `commits/main` API reports full head `46bf30ec215546912a1833b3c3b808e53f9e0025`; read-only `git ls-remote` and a shallow checkout independently matched it. ([repository metadata](https://api.github.com/repos/fagemx/edda), [head commit](https://api.github.com/repos/fagemx/edda/commits/main), [verified checkout](https://github.com/fagemx/edda/commit/46bf30ec215546912a1833b3c3b808e53f9e0025))

## Summary

Edda is a local-first system for coding-agent memory and multi-agent coordination. Its durable project ledger is a SQLite event store whose events are SHA-256 hash-chained; separate files hold live coordination state, blobs, and derived search/index data. The chain provides tamper evidence and replayable history, while its v1 format is unsigned and does not establish who authored an event or whether its claims are true. This assessment is based on pinned documentation and source; Edda, its tests, and benchmarks were not run. ([README](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/README.md), [event specification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/docs/reference/ledger-event-spec.md))

## Architecture and data model

The README describes three product layers: decisions, notes and session digests for memory; tasks, plans, claims and verdict gates for coordination; and an evolving control layer. The main durable ledger is `.edda/ledger.db`, with SQLite WAL. Rows carry event ID, producer timestamp, type, logical branch, parent hash, event hash, JSON payload, references, schema version, digests and taxonomy. Appends check the current global tail and validate the supplied hash/digest/taxonomy inside a SQLite transaction. The schema contains indexes on branch, event type and timestamp, with materialized decision and other projections. ([README](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/README.md), [SQLite schema](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/sqlite_store/schema.rs), [append and verification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/sqlite_store/events.rs))

A decision is represented as a `note` event with a structured decision payload (key, value, optional reason, scope, authority, tags and related fields). Notes, decisions, digests and task events share the event envelope. Branches label logical content, but the event specification says they do not fork the hash chain: events across branch switches and merges remain linked in one insertion-ordered chain. Live claims use a separate per-user coordination log, session heartbeats are snapshot files, conduct plans have their own state/log, and larger content may be stored in a local content-addressed blob directory. ([event specification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/docs/reference/ledger-event-spec.md), [path layout](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/paths.rs), [README](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/README.md))

## Write, update, delete, and retrieval

**Writes and corrections.** CLI and bridge paths append notes or decisions as new events. The decision bridge scrubs recognized secret patterns from values and reasons before persistence. When another decision uses the same key on the same branch, the previous decision projection is deactivated and the new event remains in history; the new decision can reference what it supersedes. Ratification is another append-only `decision_ratify` event rather than a mutation. The README explicitly describes ordinary ratification as a workflow convention today: `ratified_by` identity is not cryptographically enforced at that command path. ([decision bridge](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-cli/src/cmd_bridge/decide.rs), [event append/projection](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/sqlite_store/events.rs), [ratification command](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-cli/src/cmd_ratify/mod.rs), [event specification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/docs/reference/ledger-event-spec.md))

Ledger events are append-only; the reviewed source does not expose ordinary event deletion. Blob deletion is a separate lifecycle: retention/quota/purge operations may remove blob files and append tombstone records containing hash, time, reason, prior class, pin state and size. A tombstone is an audit record and the CLI exposes it for inspection; this review did not establish erasure from backups or every derived copy. ([blob/tombstone implementation](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/tombstone.rs), [blob commands](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-cli/src/cmd_blob.rs), [event specification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/docs/reference/ledger-event-spec.md))

**Retrieval.** `edda ask` recognizes exact decision keys, domains, keywords and overview queries. Keyword retrieval combines a semantic candidate path with lexical active-decision lookup, and can include related commits, notes, tasks and optionally transcript hits; branch, time, tags and village filters are available on relevant result paths. Separately, `edda search` queries a Tantivy index over ledger events and transcript turns, with project/session/type filters, title boosting, fuzzy ASCII matching, and exact or regex modes. The index is separately stored and must be built or rebuilt when missing or outdated. Session-start bridges also assemble and inject prior context. ([ask implementation](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ask/src/lib.rs), [Tantivy search](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-search-fts/src/search.rs), [search command](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-cli/src/cmd_search.rs), [README](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/README.md))

## Scope isolation

The default ledger path is `.edda/` beneath a repository root. Project identity and fleet registry support operations across multiple repositories, while branch filters scope decision queries. These are workspace and query boundaries; branches are not independent cryptographic chains. The ordinary local event format does not authenticate authors, and sharing a writable workspace gives processes able to modify its files the ability to append or tamper with local data. A distinct control-authority subsystem does validate registered actor/session, RBAC and a private sealed capability for specific controlled operations, but that narrower path should not be generalized to all notes, decisions or ratification. ([path layout](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/paths.rs), [ask implementation](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ask/src/lib.rs), [control authority threat model](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/control_authority.rs), [event specification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/docs/reference/ledger-event-spec.md))

## Provenance and evidence

The envelope has event IDs, timestamps, branch, parent hash, digest metadata and references to blobs, events, or provenance relations such as `based_on`, `supersedes` and `reviews`. Task receipts, review verdicts and control records add product-specific evidence. Hash verification recomputes the event hash and checks the chain in insertion order, making unauthorized edits detectable if the verifier has a trusted copy of the expected chain head. The v1 specification explicitly says the format is unsigned: successful verification does not prove author identity, payload truth, or that referenced external objects exist. The `digests` field is not a signature. ([event specification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/docs/reference/ledger-event-spec.md), [event types](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-core/src/types.rs), [chain verification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/sqlite_store/events.rs))

## Efficiency and observability

SQLite indexes support common branch/type/time lookups; Tantivy provides a separate full-text index; search caps result counts and reports when an index must be built or rebuilt. The code offers status, log, search, chain-verification, blob statistics and tombstone inspection surfaces, and tracing/logging appears in indexing and service paths. These are implementation and operator-visible mechanisms, not evidence of measured speed, scale, or reliability. A large workspace includes many Rust crates and independent state planes, so maintenance, compatibility and backup behavior across those stores are material operational questions. ([SQLite schema](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/sqlite_store/schema.rs), [search implementation](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-search-fts/src/search.rs), [search command](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-cli/src/cmd_search.rs), [blob commands](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-cli/src/cmd_blob.rs))

## Metric-domain evidence

All project benchmark outcomes are **unmeasured** for Edda. Source inspection shows mechanisms only. ([metric definitions](../METRICS.md), [project benchmark fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Exact/domain/keyword retrieval and empty results exist; no answerability cases were scored. |
| Correction accuracy and stale-value rate | Unmeasured | Same-key decisions supersede prior projections; no correction workload was run. |
| Deletion leakage | Unmeasured | Blob tombstone and cleanup paths exist; no post-delete probes or backup checks were made. |
| Scope isolation | Unmeasured | Repository workspaces, project filters and narrow control authority are source-visible; no leakage workload was run. |
| Evidence support and citation coverage | Unmeasured | Events can reference sources and receipts; no claim-level evidence workload was adjudicated. |
| Retrieval latency and write-to-recall delay | Unmeasured | SQLite/Tantivy paths exist; no timings or timed probes were collected. |
| Tokens and cost | Unmeasured | Optional LLM-assist and usage/telemetry components exist; no runtime token counts or costs were collected. |
| Storage efficiency | Unmeasured | SQLite, blobs and search-index stores are identifiable; no corpus-attributed storage measurement was made. |

## Limits and unknowns

This bounded review inspected the README, event specification, SQLite schema and event append/verification implementation, decision writer and ratification path, ask and Tantivy retrieval, path handling, blob tombstones and the control-authority threat model. It did not inspect every bridge, provider, migration, coordination protocol, export/import path or deployment configuration. ([README](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/README.md), [event specification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/docs/reference/ledger-event-spec.md), [event store](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/sqlite_store/events.rs), [ask](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ask/src/lib.rs), [blob handling](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/tombstone.rs))

The README and repository docs do not publish a contact email. The repository README and CONTRIBUTING guide were checked, as was the official website URL `https://edda.sh`; the managed browser returned `ERR_CONNECTION_CLOSED` for the website, so its page content could not be examined. No commit/profile metadata or third-party directory was used. ([checked README](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/README.md), [checked CONTRIBUTING guide](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/CONTRIBUTING.md))

## Benchmark status

**Benchmark not run.** No Edda runtime, benchmark workload or tests were run. Project evaluation files are specifications and execution-status records, not results for this system. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/edda.md)
- [Official repository metadata](https://api.github.com/repos/fagemx/edda)
- [Official main head API](https://api.github.com/repos/fagemx/edda/commits/main)
- [Reviewed full head](https://github.com/fagemx/edda/commit/46bf30ec215546912a1833b3c3b808e53f9e0025)
- [Pinned README](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/README.md)
- [Pinned event specification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/docs/reference/ledger-event-spec.md)
- [Pinned SQLite schema](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/sqlite_store/schema.rs)
- [Pinned append and chain verification](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/sqlite_store/events.rs)
- [Pinned decision writer](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-cli/src/cmd_bridge/decide.rs)
- [Pinned ratification path](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-cli/src/cmd_ratify/mod.rs)
- [Pinned decision query](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ask/src/lib.rs)
- [Pinned Tantivy search](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-search-fts/src/search.rs)
- [Pinned search command](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-cli/src/cmd_search.rs)
- [Pinned workspace paths](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/paths.rs)
- [Pinned tombstone handling](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/tombstone.rs)
- [Pinned control-authority threat model](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-ledger/src/control_authority.rs)
- [Pinned event types](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/crates/edda-core/src/types.rs)
- [Pinned CONTRIBUTING guide](https://github.com/fagemx/edda/blob/46bf30ec215546912a1833b3c3b808e53f9e0025/CONTRIBUTING.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
