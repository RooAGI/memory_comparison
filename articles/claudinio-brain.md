# Claudinio Brain source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 127 / Claudinio Brain / claudinio-brain  
**Listed repository locator:** [claudin-io/claudinio-brain](https://github.com/claudin-io/claudinio-brain) (explicit roster attribution)  
**Canonical upstream:** [claudin-io/claudinio-brain at reviewed commit](https://github.com/claudin-io/claudinio-brain/tree/6b6e57413aa38bb7cba24183c21bb41510d2d72c)  
**Default branch / current head:** main / [6b6e57413aa38bb7cba24183c21bb41510d2d72c](https://github.com/claudin-io/claudinio-brain/commit/6b6e57413aa38bb7cba24183c21bb41510d2d72c) [[revision]]  
**Review time:** 2026-11-25 08:13:43 UTC (2026-11-25 00:13:43 PST; America/Los_Angeles). The official repository page identifies main as the default branch and shows latest commit 6b6e574; the official commits feed provides the full SHA 6b6e57413aa38bb7cba24183c21bb41510d2d72c and feed timestamp 2026-09-01T10:04:19Z.[[repository]] [[head]]

## Identity and scope

The curated catalog places Claudinio Brain at ordinal 127 with slug claudinio-brain, an explicit repository locator, and the pinned Atlas attribution. Catalog and Atlas are used only for roster identity and attribution; the assessment below relies on official upstream documentation and source.[[catalog]] [[atlas]]

Claudinio Brain is a local-first agent memory CLI, Rust library, MCP server, and optional browser studio backed by one SQLite file per brain. Its core data model stores claims over valid-time and transaction-time timelines, while retrieval combines lexical, entity-name, semantic, graph, and kinship channels.[[readme]] [[schema]] [[recall]]

## Architecture and data model

The schema separates entities, aliases, predicate metadata, and facts. A fact connects a subject entity and predicate to a text, numeric, or entity object. If the object is an entity, the fact is also a graph edge; the design therefore gives relationships the same temporal model as other claims.[[schema]] [[readme]]

Facts record valid_from/valid_to for when a claim was true in the world and recorded_at/retracted_at/superseded_by for when the brain learned it or later rejected it. They may also carry confidence, reassert_count, scope, a source string, and an optional locator field described as JSON with file, line, URL, or SHA details. Predicate metadata distinguishes single-valued from multi-valued properties and literal values from relations.[[schema]] [[brain]]

One SQLite file holds metadata, facts, an FTS5 index and stored embeddings, with a sqlite-vec vector table as a derived index. FTS5 triggers update its index alongside fact mutations. The store requires a brain_id marker, enforces a schema version, and disables SQLite ATTACH so a connection remains inside one brain file.[[schema]] [[store]] [[security]]

## Write, update, delete, and retrieval

**Write.** The README documents remember, link, batch input, MCP tools, library calls, and lifecycle hooks. The writer normalizes entity identity and uses predicate metadata to resolve relational values to entities; text and numeric literals remain values. The documented batch path validates input before applying the batch.[[readme]] [[brain]] [[schema]]

**Update and correction.** A changed assertion on a single-valued predicate closes the previous fact's valid interval and records the replacement, keeping the older row and its recorded time. A repeated same-value assertion reinforces the existing claim. A correction at the same instant retracts the old claim as never true and records the replacement, leaving the disputed period unknown rather than inventing a valid value.[[readme]] [[brain]] [[schema]]

**Delete.** The documented user-facing removal path is retract: the claim is marked as never having been true and excluded from current, as-of, and history retrieval. This is a semantic correction/tombstoning behavior, not evidence of secure physical erasure from the SQLite file or its copies. The reviewed README and interfaces do not establish a full erasure workflow.[[readme]] [[recall]] [[schema]]

**Retrieval.** Exact get/history operations answer about a known subject and predicate; which provides a set-oriented predicate query; find searches record text; and recall handles natural-language questions. Recall fuses five ranked channels: FTS5 BM25 text, normalized entity or alias matches, semantic vectors, graph traversal, and kinship over shared properties. Results can expose which channels contributed, and explain output shows ranking contributions.[[readme]] [[recall]]

Temporal filtering happens before ranking. Graph traversal walks relation facts in either direction to a maximum depth of two, stops expansion through high-degree hubs, and caps the reached-entity set. These limits bound work, but can omit relevant nodes beyond the configured walk.[[recall]] [[graph]]

## Scope isolation

A fact may carry a scope, and retrieval offers optional include-scope and exclude-scope filters. The query defaults to no scope restriction, so omitting a filter can search across scopes inside the chosen brain. Each brain file is a separate store boundary, but the reviewed sources do not establish authenticated tenant or principal-level authorization.[[schema]] [[recall]] [[store]] [[security]]

## Provenance and evidence

The source and locator fields can retain an asserting party or reference location; temporal closure, retraction, and supersession links preserve some mutation lineage. Graph-derived results also retain the path that led the traversal to the result, and the documented why command inspects a fact's source and fate. These fields support traceability, but the schema does not require a source, quote, evidence span, or verification step for each stored claim.[[schema]] [[graph]] [[readme]]

## Efficiency and observability

The static embedding model is bundled with the binary and runs as a token-to-vector lookup, without transformer inference or a runtime model download. The source comments report about 7.7 MB of weights, 8,000 embeddings per second on one core, and lower MTEB retrieval quality than MiniLM. These are upstream statements rather than measurements reproduced here.[[embed]]

The retrieval implementation bounds graph depth and expansion. Explain output attributes channel contributions; stats, lint, repair, provenance lookup, and the local studio offer diagnostic views. The security policy says the project has no telemetry. No latency, throughput, cost, token, or storage measurement was collected for this review.[[graph]] [[recall]] [[readme]] [[security]]

## Metric-domain evidence

All quality and performance domains are unmeasured for this review except where the table records a source-visible implementation mechanism. These observations are not benchmark results.[[metrics]] [[fixture]] [[status]]

| Domain | Source evidence | Status |
|---|---|---|
| Answerable retrieval and abstention | Five ranked channels and explain output are source-visible; no labeled probes were run. | Unmeasured |
| Correction and stale values | Supersession, reassertion, and retraction have distinct write outcomes; no correction sequence was scored. | Unmeasured |
| Deletion leakage | Retraction filters claims from reads; no physical erasure or residual-copy probe was run. | Unmeasured |
| Scope isolation | Optional scope filters and a per-file brain boundary are visible; no multi-user isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Optional source and locator fields exist; no evidence adjudication was performed. | Unmeasured |
| Latency and write-to-recall delay | The embedder source reports throughput; no task timings were collected. | Unmeasured |
| Tokens, cost, and storage efficiency | The core uses local embeddings and SQLite; no resource usage was measured. | Unmeasured |
| Source-visible observability | Explain, channel attribution, stats, lint/repair, provenance inspection, and a local studio are visible. | Code observation |

## Limitations and unknowns

The README labels the project pre-1.0 and says the on-disk format is unstable with no migration path between schema versions. Static embeddings trade contextual expressiveness for a compact, deterministic local model. The two-hop graph walk and hub/reached caps can limit how far a recall query travels.[[readme]] [[embed]] [[graph]] [[store]]

Scope filters are caller-selected, and the official threat model says a person who can read a brain file can read its facts. The policy also treats stored content as untrusted input that may contain prompt injection. This review did not establish authenticated multi-tenant isolation, secure erasure across files/backups, or empirical retrieval behavior.[[recall]] [[security]] [[schema]]

The review covered the official README, schema, store, write, recall, graph, embedding, and security modules at the pinned head. It did not run the system or inspect every integration path; behavior beyond these sources remains unknown.

## Contact

The official pinned [SECURITY.md](https://github.com/claudin-io/claudinio-brain/blob/6b6e57413aa38bb7cba24183c21bb41510d2d72c/SECURITY.md) publishes security@claudin.io for private vulnerability reports. The exact source URL is stored in the review JSON. No commit/profile metadata or third-party directory was used.[[security]]

## Benchmark status

**Benchmark not run.** No Claudinio Brain runtime, tests, or benchmarks were executed. The project metrics, fixture, and status files are evaluation context only, not Claudinio Brain results.[[metrics]] [[fixture]] [[status]]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed locator, repository status, and Atlas attribution only.
- [Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/claudinio-brain.md) — identity and attribution only.
- [Official repository](https://github.com/claudin-io/claudinio-brain) — canonical repository and default branch.
- [Official commits feed](https://github.com/claudin-io/claudinio-brain/commits/main.atom) — full main head and feed timestamp.
- [Reviewed commit](https://github.com/claudin-io/claudinio-brain/commit/6b6e57413aa38bb7cba24183c21bb41510d2d72c)
- [README](https://github.com/claudin-io/claudinio-brain/blob/6b6e57413aa38bb7cba24183c21bb41510d2d72c/README.md)
- [SQLite schema](https://github.com/claudin-io/claudinio-brain/blob/6b6e57413aa38bb7cba24183c21bb41510d2d72c/src/store/schema.sql)
- [Store implementation](https://github.com/claudin-io/claudinio-brain/blob/6b6e57413aa38bb7cba24183c21bb41510d2d72c/src/store/mod.rs)
- [Bitemporal write implementation](https://github.com/claudin-io/claudinio-brain/blob/6b6e57413aa38bb7cba24183c21bb41510d2d72c/src/brain/mod.rs)
- [Recall implementation](https://github.com/claudin-io/claudinio-brain/blob/6b6e57413aa38bb7cba24183c21bb41510d2d72c/src/recall.rs)
- [Graph traversal implementation](https://github.com/claudin-io/claudinio-brain/blob/6b6e57413aa38bb7cba24183c21bb41510d2d72c/src/graph.rs)
- [Static embedder](https://github.com/claudin-io/claudinio-brain/blob/6b6e57413aa38bb7cba24183c21bb41510d2d72c/src/embed/mod.rs)
- [Security policy and contact](https://github.com/claudin-io/claudinio-brain/blob/6b6e57413aa38bb7cba24183c21bb41510d2d72c/SECURITY.md)
- [Project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) — evaluation plan/status only.

**Verification boundary:** Pinned upstream source and documentation review only; no system, tests, or benchmarks were run.
