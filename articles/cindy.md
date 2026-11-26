# Cindy

## Identity and review pin

- **System:** Cindy
- **Curated position:** 118
- **Slug:** cindy
- **Listed repository:** [makecindy/cindy](https://github.com/makecindy/cindy)
- **Canonical repository:** [makecindy/cindy](https://github.com/makecindy/cindy)
- **Default branch:** main
- **Reviewed head:** [6180b5d1f65b1e9f74329ddc9433f80304882f50](https://github.com/makecindy/cindy/commit/6180b5d1f65b1e9f74329ddc9433f80304882f50)
- **Reviewed:** 2026-11-25 07:56:04 UTC (2026-11-24 23:56:04 PST; America/Los_Angeles)
- **Review status:** Reviewed from current source and documentation
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cindy.md), used for identity, locator, and attribution only.

The local catalog places Cindy at ordinal 118 with slug cindy, lists https://github.com/makecindy/cindy, and marks its repository locator explicit. The Atlas source is retained only for attribution; its descriptions, capability marks, and conclusions were not used as assessment evidence.[[catalog]][[atlas]] The official GitHub repository page identifies the public repository and default branch main; its main commit feed reports full head 6180b5d1f65b1e9f74329ddc9433f80304882f50 at 2026-11-25 07:41:59 UTC. A fresh read-only git ls-remote and shallow checkout resolved main to the same SHA. This review was checked at the timestamp above.[[repo]][[main_feed]][[head]]

## Summary

Cindy is an open-source AI-agent client whose Maker Memory feature gives supported agents shared long-term notes scoped to a working directory. The inspected implementation stores Markdown shards and a derived SQLite FTS index locally, exposes MCP tools for retrieval and maintenance, and keeps buddy memory in separate scopes. This is a pinned source review, not a runtime or benchmark evaluation.[[readme]][[help]][[storage]][[tools]]

## Who and what

The repository contains desktop and mobile clients and shared packages; this review assesses its Maker Memory subsystem, not the whole agent product. The user guide distinguishes shared Maker Memory from Claude Code/Codex native memory and from each buddy’s separate memory. It says Maker Memory is stored locally and does not move to another computer.[[readme]][[help]]

The inspected code supports several agent harness integrations and a host-provided cindy_memory MCP server; this review treats the repository as a client-side project with a memory subsystem, not as a standalone memory service.[[readme]][[tools]]

## Architecture and data model

Maker Memory core code lives in packages/maker-core. Its default persistent unit is a directory under the current owner’s user-data root, with one subdirectory per working-directory scope. Records are human-readable Markdown shards with YAML frontmatter (title, description, type, updatedAt); MEMORY.md is a derived compact index, and meta.json records the absolute path and creation/use timestamps.[[manager]][[storage]][[types]]

The core keeps source files authoritative and maintains a derived SQLite FTS5 table in fts.db for search. FTS indexes filename, type, title, description, and body; the reviewed core does not add embeddings or vector retrieval. Ordinary project memory is workdir-scoped, remote sessions include a host-qualified scope key, linked worktrees are normalized by the scope resolver, and Cindy Bot memory uses a distinct stable bot key and Bot Home storage.[[storage]][[store]][[fts]][[manager]]

The cindy_memory MCP server exposes list_tools and call_tool as entry points, then registers memory list/read/search/write/delete/consolidate/review operations. Supported agents receive memory rules and an index snapshot when a session starts; an alternative project-local mode points the agent to ordinary Markdown files instead of injecting a growing index. The shared-memory setting is on by default and disables native Claude Code/Codex memory while active; Pi’s digest integration has a separate switch.[[tools]][[context]][[help]]

## Write, update, delete, and retrieval

**Writing.** memory_write or ordinary file editing adds records explicitly. Curated entries have type user, feedback, project, or reference; the tool accepts a slug/name, title, one-line description and Markdown body, with create, update, or append modes. Defaults define a 2 KiB soft body warning, 8 KiB hard body limit, 4 KiB index warning, and title/description limits; a warning does not itself reject a write.[[types]][[write]][[storage]]

**Updating and consolidation.** The storage API supports updates with an expected updatedAt value for conflict detection. Consolidation writes or updates a target shard, deletes the named source shards, then rebuilds the derived index and search table. Memory review asks a configured auxiliary model for suggestions; it does not perform deletion or consolidation automatically.[[storage]][[store]][[consolidate]][[review]]

**Deletion.** memory_delete unlinks a shard and rebuilds the index; the FTS row is deleted as a derived-index update. Reset controls clear a project’s or all Cindy memories; the user guide says resets are irreversible. The inspected implementation documents file deletion, but does not establish secure erasure from backups, filesystem snapshots, external copies, or previously exported content.[[delete]][[store]][[help]]

**Retrieval.** memory_search uses SQLite FTS5 phrase matching with BM25 ranking, then LIKE fallback (including substring matching for CJK text), and a tokenized fallback when phrase search has no hits. It returns filename, type, title, snippet and score, defaults to 10 results and caps at 50; agents can read a selected shard for full content. Configured provider results may be merged while their rankings remain separate.[[fts]][[search]][[store]]

## Scope isolation

Ordinary workdir scopes are separated by storage path; host code resolves the active data owner, rejects unavailable owner scope rather than falling back to ephemeral storage, closes stores when owner scope changes, and checks scope around async operations. These are source-visible isolation controls, not a measured or formal guarantee. Bot memories use a separate Bot scope and are excluded from the global workdir projection/reset path.[[storage]][[manager]]

## Provenance and evidence

Frontmatter records type, title, description and updatedAt, and the body is arbitrary Markdown. These fields provide organization and update metadata, but the inspected schema does not require source-document IDs, evidence excerpts, author identity, trust state, or citation validation. A write receipt records a filename/title/action for the calling session; the reviewed source does not establish a durable, tamper-evident mutation audit trail.[[types]][[storage]][[write]]

## Efficiency and observability

Search is local and bounded: query length is capped at 200 characters, terms at eight, result count at 50, and the LIKE candidate pool at 500. The source comments describe expected per-workdir corpus sizes as tens to a few hundred items; that is a design assumption, not a measurement. Logging includes manager initialization, store opens, owner-scope changes, and failure warnings. Writes rebuild the short Markdown index synchronously; FTS synchronization failures are logged and treated as recoverable because Markdown remains canonical.[[fts]][[store]][[manager]][[storage]]

## Metric-domain evidence

All quality and performance domains are **unmeasured in this review**. Source mechanisms and project benchmark plans are not Cindy results.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Search behavior is visible in code; no outputs were adjudicated. | Unmeasured |
| Correction accuracy and stale values | Create/update/append and conflict checks exist; no correction sequence was scored. | Unmeasured |
| Deletion leakage | Shard unlink and derived-index updates exist; no post-delete or residual-data probes were performed. | Unmeasured |
| Scope isolation | Workdir directories and owner guards exist; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Freeform Markdown has no required evidence IDs or citation checks; no support adjudication was run. | Unmeasured |
| Retrieval latency and write-to-recall delay | Local write/search mechanisms exist; no timing or scheduled recall probes were collected. | Unmeasured |
| Tokens, cost and storage efficiency | Markdown, an index, and an FTS database are persisted; no attributable byte/token/cost measurements were collected. | Unmeasured |

The [project metric definitions](../METRICS.md) and [initial execution-status record](../results/initial-baselines-status.json) define evaluation criteria and report project-wide execution status; they are not Cindy measurements.[[metrics]][[status]]

## Limitations and unknowns

This is a bounded review of selected documentation, core memory code, and MCP registrations at the pinned head. It does not establish runtime behavior, every agent adapter, desktop UI behavior, cloud-service implementation, or deployment configuration.[[readme]][[help]][[manager]][[tools]]

The user guide says Maker Memory is local to a computer, while the product README separately describes hosted/cloud companion synchronization. The inspected documentation does not establish that Maker Memory shards synchronize through that cloud path. The independent backend service is outside this repository.[[help]][[readme]]

Search is full-text/keyword based in the reviewed core; no embedding index was found. FTS fallback behavior, external file edits, cross-process mutations, residual data outside the inspected paths, and large-scale performance have not been measured.[[fts]][[store]][[storage]]

## Benchmark status

**Benchmark not run.** I did not execute Cindy, its tests, or a benchmark workload. No quality, latency, delay, token, cost, storage, correction, deletion, scope-isolation, or evidence-support result is claimed. The linked metric definitions and status record are project evaluation materials, not system results.[[metrics]][[status]]

## Contact

The official pinned [SECURITY.en.md](https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/SECURITY.en.md) publishes **feedback@cindy.app** as the fallback contact for security reports when GitHub’s private reporting form is unavailable. The address and exact checked URL are recorded in the JSON; no commit metadata, personal profile, third-party directory, or inferred address was used.[[security]]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed repository and Atlas attribution only.
- [Atlas attribution](<https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cindy.md>) — attribution only.
- [Official GitHub repository](<https://github.com/makecindy/cindy>) — public repository and default branch.
- [Main branch commit feed](<https://github.com/makecindy/cindy/commits/main.atom>) — current full SHA and feed update time.
- [Reviewed head](<https://github.com/makecindy/cindy/commit/6180b5d1f65b1e9f74329ddc9433f80304882f50>)
- [README](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/README.md>) — product and repository scope.
- [Memory user guide](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/apps/desktop/help-knowledge/memory.md>) — user-facing memory scopes and settings.
- [Memory types](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/maker-core/src/memory/types.ts>)
- [Markdown storage](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/maker-core/src/memory/storage.ts>)
- [Store implementation](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/maker-core/src/memory/store.ts>)
- [SQLite FTS implementation](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/maker-core/src/memory/fts.ts>)
- [Memory manager](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/maker-core/src/memory/manager.ts>)
- [Prompt context integration](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/maker-core/src/memory/context.ts>)
- [MCP memory server](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/lizi-mcps/src/cindy_memoryMcpServer.ts>)
- [Write tool](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/lizi-mcps/src/memory/write.ts>), [delete tool](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/lizi-mcps/src/memory/delete.ts>), [search tool](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/lizi-mcps/src/memory/search.ts>), [consolidate tool](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/lizi-mcps/src/memory/consolidate.ts>), and [review tool](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/packages/lizi-mcps/src/memory/review.ts>)
- [Project metric definitions](../METRICS.md) and [execution status](../results/initial-baselines-status.json) — project protocol/status, not Cindy results.
- [Official security policy](<https://github.com/makecindy/cindy/blob/6180b5d1f65b1e9f74329ddc9433f80304882f50/SECURITY.en.md>) — published fallback contact.

**Verification boundary:** read-only source and documentation review. No Cindy runtime, tests, or benchmarks were run.
