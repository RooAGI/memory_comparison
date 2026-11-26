# Claude-Mem

## Identity and review pin

- **Ordinal:** 124
- **Catalog name and slug:** Claude-Mem (`claude-mem`)
- **Listed repository locator:** https://github.com/thedotmack/claude-mem (catalog status: explicit)
- **Canonical upstream repository:** https://github.com/thedotmack/claude-mem
- **Default branch:** `main`
- **Reviewed head:** [`11fdec893eb4ece18ff946758e75e82c92aff71b`](https://github.com/thedotmack/claude-mem/commit/11fdec893eb4ece18ff946758e75e82c92aff71b)
- **Head timestamp:** 2026-11-25T06:37:16Z (GitHub main Atom feed)
- **Reviewed:** 2026-11-25 08:07:02 UTC (2026-11-25 00:07:02 PST; America/Los_Angeles)
- **Review status:** Reviewed from current source and documentation
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [Atlas attribution entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/claude-mem.md), used only for catalog identity, listed locator, and attribution.

The project catalog identifies ordinal 124 as Claude-Mem, slug `claude-mem`, with an explicit repository locator. The Atlas entry is retained only as the catalog attribution source.[[catalog]][[atlas]] GitHub identifies `main` as the default branch; its official main page and commits feed show the same latest commit, and the feed gives the full head SHA and update timestamp recorded above.[[repo]][[head]] The README describes a local agent-memory plugin and worker that captures session activity, writes observations and summaries, then supplies selected context and searchable details to later sessions.[[readme]][[worker]]

## Summary

Claude-Mem is a local-first memory plugin and service for coding agents. Host hooks send activity to a worker; an observer turns activity into compact observations and session summaries, stored in SQLite. Session-start context and progressive search expose selected memories, with optional Chroma semantic search alongside SQLite keyword search.[[readme]][[worker]][[context]][[search]]

## Who and what

The README describes Claude-Mem as a persistent context system for multiple agent integrations and identifies Alex Newman as its author. This review concerns the repository implementation at the pinned SHA, not the hosted Cloud Sync service or its operational guarantees.[[readme]]

## Architecture and data model

The documented flow has agent-specific hooks pass tool activity to a local Bun-managed HTTP worker. The worker routes activity to observer providers and storage, and serves context, search, viewer, and MCP endpoints. Its local store is SQLite under `~/.claude-mem`; the README describes Chroma as an additional semantic-search layer over SQLite keyword search.[[readme]][[worker]]

Stored memory is organized into sessions, observations, and summaries, alongside prompts and raw tool-use records. Observations include a title/narrative fingerprint; the observation storage helper hashes the session ID, title, and narrative and has a second details hash for structured type, subtitle, facts, and concepts. File paths are indexed separately for reads and modifications. This supports deduplication and file-oriented retrieval, but a content hash is not a claim that duplicate or semantically equivalent memories are always merged.[[store]][[get]][[data]]

SQLite uses WAL, foreign keys, a busy timeout, and versioned schema migrations. The database code guards against opening a database whose schema is newer than the binary understands. These are storage and compatibility mechanisms visible in source, not measurements of throughput or durability under a workload.[[connection]]

## Write, update, delete, and retrieval

**Write and update.** The README says hooks forward activity while a separate observer creates observations and session summaries; live capture uses a bounded in-memory handoff, and documented quota or worker failures can skip current activity rather than preserve an inference backlog for later replay. The explicit `POST /api/memory/save` route validates text and optional title/project/metadata, applies project-exclusion checks, and writes a user-requested memory through `saveMemory`. The inspected routes do not establish a general user-facing correction or edit-history API for previously generated observations.[[readme]][[observer]][[memory]]

The observation helper computes stable hashes from session/title/narrative and a details fingerprint. This is deduplication identity support; I did not establish from the inspected paths that an existing observation is edited in place when new content arrives.[[store]]

**Delete.** The inspected memory route exposes an explicit save operation. The reviewed README and selected search/data routes do not establish a general hard-delete API or an end-to-end erasure contract for observations, derived summaries, Chroma copies, backups, or optional Cloud Sync. Do not treat hiding a row from context or removing a local record as proof that every derived or synchronized copy is erased.[[readme]][[memory]][[data]]

**Retrieval.** Session-start context selects recent observations and summaries for the active project scope, with mode/type/concept filters and optional reinforcement ranking. The project-key resolver supports project merges; platform source can also constrain the read. The context builder reads from SQLite and renders either agent or human context, with a separate read-worker path available.[[context]][[compiler]][[get]]

Search accepts text or filters. When Chroma is configured, the orchestrator uses semantic search and supplements empty result categories; filter-only search uses SQLite. The progressive memory search workflow first returns compact index rows, can show a timeline around an anchor, then fetches selected observation or summary details by ID. Detail fetch checks that the stored project still matches the project attached to the selected reference. This limits unnecessary full-record fetches but is not evidence of retrieval accuracy or a measured token reduction.[[search]][[progressive]][[readme]]

## Scope isolation

Project keys are applied in context and search reads; a one-hop project-merge mapping can include adopted rows. Search routes validate project arguments, and observation/file lookups can apply both project and platform-source filters. The README also says startup context defaults to the current harness unless the user opts to include all sources.[[compiler]][[get]][[search]][[readme]]

These are logical read filters in the reviewed paths. The review did not audit every integration, authorization boundary, Cloud Sync membership rule, or cross-project access path, and did not run an isolation workload. They do not establish tenant-grade isolation.

## Provenance and evidence

The project keeps observations tied to sessions and exposes observation IDs through its worker API and viewer. Tool-use records and file-read/file-modified references provide links back to captured activity; the explicit three-step search design lets an agent inspect an index, inspect nearby timeline context, and fetch only selected full observation details. The observation storage code explicitly treats tool-derived file evidence and agent/media metadata as provenance separate from the text fingerprint.[[readme]][[worker]][[progressive]][[store]][[get]]

These links provide inspectable lineage within the local record model. The reviewed paths do not establish that each generated claim is supported by source evidence, that every transformation has an immutable audit trail, or that records remain unmodified across export and sync.

## Efficiency and observability

Source-visible efficiency controls include compact search index rows, selected-ID detail fetches, per-request limits, SQLite indexes for file lookup, optional semantic candidate selection, configurable context budgets, and a bounded observer handoff. The README's approximate token sizes for index and detail rows describe the intended progressive workflow and explicitly are not a measured end-to-end saving.[[progressive]][[get]][[context]][[observer]][[readme]]

The worker exposes health, logs, and server-sent events for its viewer, and the code uses structured logs for database and search activity. The reviewed material does not establish production telemetry coverage or provide measured latency, tokens, cost, storage, or failure rates.[[worker]][[connection]][[search]]

## Metric-domain evidence

All rows below are **unmeasured**. This review inspected source and documentation only; Claude-Mem, its tests, and benchmarks were not run.[[metrics]][[result]]

## Limitations and unknowns

- The project supports local storage and optional Cloud Sync; the reviewed sources do not establish the privacy, retention, deletion, or backup behavior of every optional integration.[[readme]]
- The local observer lifecycle documentation describes bounded, live-only inference handoff and deliberate loss of some activity during outages. This can leave gaps in generated memories; original transcripts and saved observations remain separate records.[[observer]]
- The review did not verify the complete schema/data lifecycle, all plugin integrations, access-control boundaries, sync conflict handling, production deployment, or any service-level guarantee. The current commit is large and fast-moving, so later source revisions may change these behaviors.[[repo]][[head]]
- No quality, correction, deletion-leak, scope-isolation, latency, token, cost, or storage measurement was collected.[[metrics]][[result]]

## Benchmark status

**Benchmark not run.** This is a source-based review; no versioned measured result exists for this task. The project metric definitions are in [METRICS.md](../METRICS.md), and the task's review record is [claude-mem.json](../data/system-reviews/claude-mem.json).[[metrics]][[result]]

## Contact

The official pinned README was checked for a published contact email. It did not provide a contact email, so none is recorded.[[readme]]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed repository, and Atlas attribution.
- [Atlas attribution entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/claude-mem.md) — attribution only.
- [Official repository](https://github.com/thedotmack/claude-mem) — repository identity and default branch.
- [Verified current head](https://github.com/thedotmack/claude-mem/commit/11fdec893eb4ece18ff946758e75e82c92aff71b) — current commit SHA and commit page.
- [Official main commits feed](https://github.com/thedotmack/claude-mem/commits/main.atom) — full current head and feed timestamp.
- [Official README](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/README.md) — purpose, component overview, search workflow, storage, integrations, and author attribution.
- [Worker service README](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/src/services/worker/README.md) — local HTTP runtime and API overview.
- [SQLite connection](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/src/services/sqlite/connection.ts) — SQLite configuration, schema versioning, and safe-open checks.
- [Observation storage helpers](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/src/services/sqlite/observations/store.ts) — observation hashing and structured detail identity.
- [Observation lookup](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/src/services/sqlite/observations/get.ts) — project/platform filters and indexed file-path lookup.
- [Search orchestrator](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/src/services/worker/search/SearchOrchestrator.ts) — semantic search selection, SQLite filter-only search, and fallback behavior.
- [Progressive memory search](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/src/services/worker/ProgressiveMemorySearch.ts) — compact indexes, timeline reads, and selected detail fetches.
- [Context builder](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/src/services/context/ContextBuilder.ts) — project-scoped context construction and read paths.
- [Context observation compiler](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/src/services/context/ObservationCompiler.ts) — project selection, filtering, and recent observation selection.
- [Explicit memory save route](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/src/services/worker/http/routes/MemoryRoutes.ts) — validated manual memory write and project exclusion.
- [Data routes](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/src/services/worker/http/routes/DataRoutes.ts) — bounded selected-ID reads and import/export-related routes.
- [Observer lifecycle documentation](https://github.com/thedotmack/claude-mem/blob/11fdec893eb4ece18ff946758e75e82c92aff71b/docs/architecture/observer-lifecycle.md) — bounded live capture and failure handling.
- [Metric definitions](../METRICS.md) — project-owned benchmark definitions.
- [Review record](../data/system-reviews/claude-mem.json) — benchmark status and source evidence record.

**Verification boundary:** official GitHub source and documentation review only; no Claude-Mem runtime, tests, or benchmarks were run.
