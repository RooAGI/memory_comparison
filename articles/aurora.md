# AURORA source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated position:** 79  
**Roster name / slug:** AURORA / `aurora`  
**Listed repository locator:** [hamr0/aurora](https://github.com/hamr0/aurora)  
**Default branch / reviewed head:** `main` / `750a39da51ed947aab851e9fd5c06a2587402e2b`  
**Review time:** 2026-11-24 22:05:57 UTC (14:05:57 PST; America/Los_Angeles). The official repository page identifies `main` as the default branch and shows latest commit `750a39d`; its commit page at the listed full SHA identifies that same commit. The repository is archived and read-only.

## Identity and review pin

The curated catalog at position 79 identifies this system as AURORA, slug `aurora`, and lists `https://github.com/hamr0/aurora`. The catalog’s pinned Atlas report is included only as identity and attribution; its descriptions, marks, and layout were not used as assessment evidence. ([project roster](../data/memory-systems.json); [catalog attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/aurora.md))

The official repository page shows the default branch as `main`, the current short head `750a39d`, and that the owner archived the repository on 2026-06-14. The official `main` Atom feed independently identifies the first commit as full SHA `750a39da51ed947aab851e9fd5c06a2587402e2b` (updated 2026-05-22T19:43:25Z), and its commit page matches. This review therefore describes the source at that archived head, not a live maintained service. ([repository page](https://github.com/hamr0/aurora); [reviewed commit](https://github.com/hamr0/aurora/commit/750a39da51ed947aab851e9fd5c06a2587402e2b))

## Summary

AURORA is a local code-aware memory and intelligence layer for coding assistants. The project README describes indexing source and Markdown, then searching indexed chunks with activation-based ranking and LSP-derived code context. Core package documentation and selected store code show a chunk store with activation and relationship data, backed by SQLite for persistent use and an in-memory implementation. This is a source review only; no runtime or benchmark was run. ([repository README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/README.md); [core package README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/README.md); [in-memory store](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/memory.py))

## Who and what

The inspected root README presents AURORA as a code memory and code-intelligence framework for AI coding assistants, with CLI and MCP/LSP-facing capabilities. It describes the system as running locally and storing memory in SQLite. The README also describes a broader orchestration layer; this review focuses on the code and document memory paths and the core store. The sources inspected do not establish a separate hosted memory service or a multi-tenant service boundary. ([repository README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/README.md); [core package README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/README.md))

## Architecture and data model

**Code observation.** The core package separates chunk types, storage, context management, activation, metrics, logging, and resilience. Its package guide demonstrates a `CodeChunk` with an ID, absolute file path, element type, symbol name, and line range; it is saved through the `Store` interface and retrieved by chunk ID. The in-memory implementation holds chunks, activation records, and relationships in separate Python containers. ([core package README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/README.md); [in-memory store](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/memory.py))

The project README says indexing parses Python, JavaScript/TypeScript, Go, and Java into code chunks, incorporates Git and LSP signals, and indexes Markdown documents for search. This is project documentation describing the product; the indexing pipeline itself was not inspected in this bounded source review. ([repository README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/README.md))

The documented persistent backend is SQLite, with the default database path `~/.aurora/memory.db`. The inspected SQLite store source describes per-thread pooled connections, deferred schema initialization, transaction support, rollback on errors, JSON serialization, and relationship traversal. WAL mode is enabled by default in its constructor. The in-memory store is documented as a lightweight alternative for tests and is explicitly not thread-safe. ([repository README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/README.md); [SQLite store](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/sqlite.py); [in-memory store](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/memory.py))

## Write, update, delete, and retrieval

**Write and update code observations.** The package guide uses `save_chunk` to persist a chunk and `get_chunk` to retrieve it by ID. In the in-memory implementation, saving validates the chunk and assigns it by ID; a new ID gets an initial activation record. The inspected method does not show a revision history or a distinct correction/supersession record. The SQLite backend implements the persistent store interface, but its full mutation behavior was not exhaustively traced here. ([core package README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/README.md); [in-memory store](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/memory.py); [SQLite store](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/sqlite.py))

The root README documents `aur mem index .` for indexing a project and `aur mem search` for querying it. It describes searches as activation-ranked and the product as combining relevance, recency/frequency, Git signals, and LSP enrichment. Separately, the official main commit feed records a February change making SQLite FTS5 the primary candidate gate and using FTS5 rank as the BM25 component of tri-hybrid scoring. This is an upstream change note, not a full trace of the final retrieval code; exact current filters, reindex replacement, stale-file cleanup, and deletion semantics remain unverified. ([repository README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/README.md))

The inspected in-memory store exposes reset and close operations that clear its in-memory chunks, activations, and relationships. The selected sources do not establish whether the user-facing indexer deletes individual records, removes stale indexed files, or provides a durable erasure path in SQLite. I therefore do not treat reset/close of the test store as a production deletion guarantee. ([in-memory store](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/memory.py); [SQLite store](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/sqlite.py))

## Metric-domain evidence

All benchmark domains below are unmeasured for this review. The repository README includes illustrative ranking output and approximate tool-speed statements; these are documentation examples, not measurements collected here. ([repository README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/README.md); [project metric definitions](../METRICS.md); [benchmark fixture](../fixtures/memory-benchmark-v1.json); [baseline execution status](../results/initial-baselines-status.json))

- **Answerable recall and abstention:** No adjudicated answerable or unanswerable retrieval probes were run. The inspected sources do not establish an abstention contract.
- **Correction and staleness:** No correction cases or stale-result probes were run. The selected store code does not establish versioned correction behavior.
- **Deletion:** No deletion leakage probes were run; durable deletion behavior was not verified in the selected code.
- **Scope isolation:** No cross-project isolation probes were run. Local project paths/database defaults suggest project-level placement, not an authorization guarantee.
- **Evidence and citations:** Code chunks are documented with file and line metadata, but evidence-support precision and citation coverage were not measured.
- **Latency and write-to-recall delay:** No timings were collected. README timing figures are presented as documentation claims, not this review’s results.
- **Tokens and cost:** No token or cost measurements were collected.
- **Storage efficiency:** No corpus-size or storage measurements were collected.

## Limits and unknowns

This is a bounded source review at the verified archived `main` head. It inspected the official README, core package guide, and selected in-memory and SQLite storage implementations. It did not inspect the full code/document indexing pipeline, complete retrieval stack, MCP handlers, or all store operations. Therefore, documented capabilities are distinguished from implementation details that remain unknown. ([repository README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/README.md); [core package README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/README.md); [SQLite store](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/sqlite.py))

The local SQLite path and project-oriented CLI do not prove operating-system access controls, authenticated principal boundaries, or isolation under shared-host deployment. Source-visible score explanations and configured storage behavior do not establish answer quality, privacy, or actual resource use. Runtime correctness, deletion guarantees, and performance remain untested.

The official README was checked for a published contact email. No email address was found there; the review JSON records `null` and the exact checked README URL. ([checked official README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/README.md))

## Benchmark status

**Benchmark not run.** No AURORA system execution or benchmark was performed. The project's metric definitions, fixture, and baseline-status record are linked for the review workflow only; they are not AURORA results. ([project metric definitions](../METRICS.md); [benchmark fixture](../fixtures/memory-benchmark-v1.json); [baseline execution status](../results/initial-baselines-status.json))

## Sources

- [Current upstream repository at reviewed commit](https://github.com/hamr0/aurora/tree/750a39da51ed947aab851e9fd5c06a2587402e2b)
- [Official main commit feed and full current head](https://github.com/hamr0/aurora/commits/main.atom)
- [FTS5 retrieval change record](https://github.com/hamr0/aurora/commit/d5b1695716e1be0af837fb682558cf5ee4970545)
- [Repository README](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/README.md)
- [Core package README — chunk and Store overview](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/README.md)
- [In-memory store — chunk, activation, relationship, and reset behavior](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/memory.py)
- [SQLite store — persistent backend](https://github.com/hamr0/aurora/blob/750a39da51ed947aab851e9fd5c06a2587402e2b/packages/core/src/aurora_core/store/sqlite.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project baseline execution status](../results/initial-baselines-status.json)
- [Catalog identity and listed locator attribution only](../data/memory-systems.json)
- [Catalog attribution source only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/aurora.md)
