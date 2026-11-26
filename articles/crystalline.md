# Crystalline

## Identity and review pin

- Catalog ordinal: 172
- System: Crystalline
- Slug: `crystalline`
- Listed repository: https://github.com/jordiboehme/crystalline
- Roster attribution: explicit repository locator; the pinned Atlas entry is retained for curated identity and locator context only, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/crystalline.md)).
- Canonical upstream: https://github.com/jordiboehme/crystalline
- Default branch: `main`
- Reviewed full head: [a3114b5965f67380d590090e7aecffb158c3ba8a](https://github.com/jordiboehme/crystalline/commit/a3114b5965f67380d590090e7aecffb158c3ba8a)
- Review timestamp: 2026-11-25T10:11:12Z (UTC; 2026-11-25 02:11:12 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

The official GitHub repository API identifies `jordiboehme/crystalline` as public, non-fork, and defaulting to `main`. Its official main Atom feed identifies full head `a3114b5965f67380d590090e7aecffb158c3ba8a`, updated at 2026-11-24T20:22:08Z; the commit page is recorded as the full-SHA head reference. ([repository metadata](https://api.github.com/repos/jordiboehme/crystalline), [main history](https://github.com/jordiboehme/crystalline/commits/main.atom), [head commit](https://github.com/jordiboehme/crystalline/commit/a3114b5965f67380d590090e7aecffb158c3ba8a))

## Summary

Crystalline is a local-first Rust system that stores agent knowledge as Markdown Engrams organized into Domains. Its search index is derived from the files and can be rebuilt. Agents use MCP and people can inspect or edit knowledge through the CLI and Fluid UI. This assessment is based on current source and documentation, not a runtime or benchmark evaluation. ([README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md), [architecture](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/docs/architecture.md))

## Architecture and data model

The repository divides responsibilities across a format/core crate, index, identity, engine, REST API, service daemon, and CLI. One daemon owns the database while other commands and MCP clients attach through local or network interfaces. File-backed Domains keep Markdown as the durable source and treat the search index as a disposable derived layer. Virtual Domains use database content as their source. ([architecture](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/docs/architecture.md), [README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md), [index contract](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/index/src/store.rs))

An Engram is a Markdown document with YAML frontmatter and a body. The core model includes a type, title, permalink, tags, free-form status, recorded date, validity window, generated write provenance, and description; it also parses observations, typed relations, wikilinks, and headings from the body. ([Engram model](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/core/src/engram.rs))

The product is local-first by default, with optional PostgreSQL, remote embeddings, connected servers, and GitHub team sharing. Each option changes deployment and data-flow boundaries, which this source review does not assess. ([README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md), [architecture](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/docs/architecture.md))

## Write, update, delete, and retrieval

**Writes and edits.** Agents and people can add or edit Engrams through MCP, the CLI, and Fluid. File-backed edits update the Markdown source and reindex it. Virtual-domain edits use compare-and-swap protections so an edit based on stale content is refused instead of silently replacing a concurrent write. ([README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md), [edit implementation](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/engine/src/engine/edit.rs))

**Lifecycle and deletion.** The model has recorded and valid-time dates and a free-form status; the README describes superseding stale knowledge rather than overwriting it, with older knowledge remaining addressable by date. A normal deletion removes the file and index rows, or the virtual-domain database rows. In review mode, deletion is represented by the actor's tombstone draft until it is reviewed. ([README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md), [Engram model](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/core/src/engram.rs), [index contract](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/index/src/store.rs), [delete implementation](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/engine/src/engine/delete.rs))

**Retrieval.** Search offers lexical, semantic, and hybrid modes, plus filters such as Domain, type, status, tags, temporal bounds, and metadata. The lexical Turso path uses a LIKE-based candidate prefilter and a weighted term score. Semantic or hybrid search falls back to text if the query/provider/active-model embedding prerequisites are not met. Typed relations and links support graph-neighborhood context retrieval. ([README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md), [engine search](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/engine/src/engine/search.rs), [Turso search](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/index/src/turso/search.rs))

## Scope isolation

Search applies caller visibility before querying. Domains a caller cannot see are removed from the query scope, and a named inaccessible Domain is treated as having no results. In review-mode Domains, the actor's own draft rows can be read while other actors' drafts are screened out. This is evidence of source-level filters, not a measured scope-isolation result. ([engine search](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/engine/src/engine/search.rs), [index contract](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/index/src/store.rs))

## Provenance and evidence

Engrams include generated write provenance and the README describes a verified trail. Review-mode drafts can keep agent changes separate until a proposal is merged. These mechanisms support authorship and change review; they do not independently establish the truth of a claim, and this review did not evaluate a provenance trail's accuracy. ([Engram model](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/core/src/engram.rs), [README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md), [architecture](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/docs/architecture.md))

## Efficiency and observability

The architecture keeps a single daemon and derived index. The lexical backend bounds candidate processing and pushes filters into SQL; semantic and hybrid paths depend on available embeddings. The README reports search in under half a second at ten thousand Engrams, but this is an upstream claim and was not reproduced. The README also says the default local setup has no developer telemetry or analytics; telemetry behavior in optional remote configurations was not assessed. ([architecture](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/docs/architecture.md), [Turso search](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/index/src/turso/search.rs), [README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md))

## Metric domains

All project benchmark metrics are **unmeasured** for Crystalline. The source establishes mechanisms only; no workload was executed. ([metric definitions](../METRICS.md), [project benchmark fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status record](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Multiple search modes and empty results exist; no cases were scored. |
| Correction accuracy and stale-value rate | Unmeasured | Guarded edits and retirement/supersession are available; no correction workload was run. |
| Deletion leakage | Unmeasured | Delete paths remove source or virtual records; no post-delete probes or backup checks were made. |
| Scope isolation leakage | Unmeasured | Visibility and per-actor draft filters are source-visible; no cross-scope workload was run. |
| Evidence support and citation coverage | Unmeasured | Provenance metadata exists; no claims were adjudicated for support. |
| Retrieval latency and write-to-recall delay | Unmeasured | The README states a latency claim; no timings were collected. |
| Tokens and cost | Unmeasured | No runtime token or billing measurements were collected. |
| Storage efficiency | Unmeasured | No corpus-attributed disk, index, or database size was measured. |

## Limits and unknowns

This bounded source review covered the README, architecture overview, Engram model, storage contract, search engine and Turso search implementation, and edit and deletion paths. It did not inspect every index backend, provider, API route, integration hook, or collaboration workflow. Source inspection cannot establish runtime correctness, retrieval quality, actual deployment configuration, access-control effectiveness, physical erasure from backups, latency, token cost, or storage efficiency. ([README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md), [architecture](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/docs/architecture.md), [Engram model](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/core/src/engram.rs), [search](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/engine/src/engine/search.rs), [Turso search](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/index/src/turso/search.rs), [edit](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/engine/src/engine/edit.rs), [delete](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/engine/src/engine/delete.rs))

The official pinned README publishes `jordi@boehme-lopez.de` as the contact email. No commit/profile metadata or third-party directory was used. ([checked official README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md))

## Benchmark status

**Benchmark not run.** Crystalline, its tests, and benchmark workloads were not run. Upstream README performance statements are not project benchmark results. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, identity/locator attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/crystalline.md)
- [Official GitHub repository metadata](https://api.github.com/repos/jordiboehme/crystalline)
- [Official main branch commit feed](https://github.com/jordiboehme/crystalline/commits/main.atom)
- [Reviewed full head a3114b5965f67380d590090e7aecffb158c3ba8a](https://github.com/jordiboehme/crystalline/commit/a3114b5965f67380d590090e7aecffb158c3ba8a)
- [Pinned README](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/README.md)
- [Pinned architecture overview](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/docs/architecture.md)
- [Pinned Engram model](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/core/src/engram.rs)
- [Pinned index storage contract](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/index/src/store.rs)
- [Pinned engine search and scope](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/engine/src/engine/search.rs)
- [Pinned Turso search implementation](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/index/src/turso/search.rs)
- [Pinned Engram edit implementation](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/engine/src/engine/edit.rs)
- [Pinned Engram deletion implementation](https://github.com/jordiboehme/crystalline/blob/a3114b5965f67380d590090e7aecffb158c3ba8a/crates/engine/src/engine/delete.rs)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
