# claude-mem-lite source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 125 / claude-mem-lite / claude-mem-lite  
**Roster attribution:** repository status is explicit; [curated roster](../data/memory-systems.json) and its pinned Atlas record are used only for identity, locator, and roster attribution. Atlas descriptions are not assessment evidence.  
**Listed repository locator:** [sdsrss/claude-mem-lite](https://github.com/sdsrss/claude-mem-lite)  
**Canonical repository:** [sdsrss/claude-mem-lite](https://github.com/sdsrss/claude-mem-lite)  
**Default branch / reviewed head:** main / [3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb](https://github.com/sdsrss/claude-mem-lite/commit/3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb)  
**Review time:** 2026-11-25 08:09:22 UTC (2026-11-25 00:09:22 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists ordinal 125 as claude-mem-lite, slug `claude-mem-lite`, with the explicit locator `https://github.com/sdsrss/claude-mem-lite` and a pinned Atlas roster source. The official repository page identifies `main` as its default branch. GitHub's official main Atom feed was updated at 2026-11-25T01:50:27Z and identifies full head `3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb`; the official repository page showed the corresponding short SHA. The code and README reviewed below are linked at that full SHA.[[catalog]][[atlas]][[repo]][[history]][[head]]

## Summary

claude-mem-lite is a Claude Code plugin that captures session activity through lifecycle hooks, batches related tool activity into observations, and exposes persistent memory through an MCP server and command-line tools. The reviewed source uses a local SQLite database with FTS5 text search. This is a source review and makes no runtime or benchmark claim.[[readme]][[schema]][[server]]

## Who and what

The official README describes a Claude Code focused memory plugin, distributed with hooks, an MCP server, CLI commands, and session-start context injection. The official repository is maintained under the sdsrss account; this review does not infer an individual maintainer identity from commit or profile metadata.[[repo]][[readme]]

## Architecture and data model

The shared schema initializes a SQLite database in the user's claude-mem-lite data directory. The code defines persistent observations and supporting session, user-prompt, and activity-event records, with FTS5 indexes and triggers to keep indexed text aligned with writes. Observations carry structured fields such as type, title, narrative, facts, concepts, project, branch, files, lesson, importance, timestamps, and memory-session identity. Database initialization enables WAL mode; the schema also contains migrations and consistency checks.[[schema]][[readme]]

Seven Claude Code lifecycle hooks cover session start, compaction, tool calls and failures, stop, and user prompts. Tool activity is filtered and buffered into episodes; a background model call can enrich an episode, while manual save/update/search/retrieval paths are available through MCP and CLI. The MCP server and hook processes share the database schema and local data directory.[[readme]][[server]]

## Write, update, delete, and retrieval

**Write and update — code observations.** Automatic capture records eligible tool activity and groups related operations into episodes before writing observations. Explicit saves are available through MCP and CLI. The shared observation update path accepts a patch to title, narrative, type, importance, lesson, or concepts, scrubs string values, updates the row transactionally, and rebuilds derived search text. The README describes degraded-save behavior when enrichment is unavailable; it is a documented fallback, not a runtime result from this review.[[readme]][[server]][[write]]

**Delete — code and documentation observations.** The project exposes deletion through its MCP and CLI surfaces, and the implementation centralizes hard-delete handling. Official documentation describes making a pre-delete database copy; that protects a recoverable copy but means a delete request does not establish erasure from backups. This review did not inspect or exercise every backup-retention path.[[server]][[delete]][[readme]]

**Retrieval — code observations.** Search uses FTS5/BM25 over observations and applies project, type, time, importance, and branch filters when supplied. The current search source scores candidates using recency decay, type, importance, lesson presence, noise and citation-related factors; where there are too few direct matches, concept co-occurrence and pseudo-relevance feedback can expand results. Query relaxation can retry an AND search as OR. The README also describes synonym and stop-word expansion, timeline browsing, file-aware recall, prompt-time injection, and token-budgeted startup context. These are implementation paths, not evidence of answer quality.[[search]][[readme]][[server]]

## Scope isolation

The observation search query supports an explicit project filter and the system derives a current project for context-aware ranking. The reviewed query permits an absent project filter, so project ranking and project filtering are distinct behaviors; the source does not establish tenant isolation or authorization between users sharing access to one data directory. Project-specific context features should not be read as a measured cross-project isolation guarantee.[[search]][[server]][[readme]]

## Provenance and evidence

Observation records retain project, branch, session identity, timestamps, files, and descriptive memory fields. The provenance helper distinguishes explicit/manual session IDs from machine-written hook, import, compression, enrichment, and restore records; an automatically written lesson is marked in rendered output. Search tracks citation interactions and uses citation-related state as a ranking signal. These mechanisms support origin and usage tracing, but the reviewed ordinary observation schema does not require a source URL, verbatim evidence span, or claim-level citation validation.[[schema]][[provenance]][[search]]

## Efficiency and observability

SQLite, WAL, FTS5 indexes, bounded search results, and episode batching are visible design choices that can reduce repeated work. The README's token/cost comparisons are explicitly illustrative architecture estimates, not end-to-end measurements. The inspected sources do not provide a result for this review's latency, token, cost, or storage workload. The project includes diagnostic and telemetry code, but no live telemetry was collected here.[[schema]][[readme]][[server]][[metrics]]

## Metric-domain evidence

All evaluation domains are **unmeasured** in this review. Source mechanisms and the project fixture do not establish claude-mem-lite benchmark results.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | FTS5 retrieval, query expansion, filters, and fallback paths are source-visible; no answerability or abstention cases were scored. | Unmeasured |
| Correction and stale values | Explicit field updates and supersession mechanisms exist; no correction sequence or stale-value rate was adjudicated. | Unmeasured |
| Deletion leakage | Hard-delete code and backup behavior are documented; no post-delete search, backup, or derived-data probe was run. | Unmeasured |
| Scope isolation | Project filters and current-project ranking are visible; no cross-project or multi-user isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Provenance and citation-related ranking fields exist; no evidence-support adjudication was run. | Unmeasured |
| Retrieval latency and write-to-recall delay | The source paths were reviewed but not timed. | Unmeasured |
| Tokens, cost, and storage | README estimates are architecture estimates; no resource use was measured. | Unmeasured |

The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) define evaluation protocols and project status, not results for this system.[[metrics]][[fixture]][[status]]

## Limits and unknowns

This review is bounded to official documentation and selected code at the verified main SHA. It does not establish runtime correctness, retrieval quality, effective data isolation, backup retention, complete erasure across copies, or performance under load. The source shows local project-aware behavior but no tenant authorization contract in the inspected retrieval path.[[repo]][[head]][[search]][[delete]]

No claude-mem-lite runtime, benchmark workload, or tests were run. The README's comparative quality and cost statements and its search-quality figures are upstream claims; they were not independently reproduced or treated as measurements in this assessment.[[readme]][[metrics]][[fixture]][[status]]

## Benchmark status

Benchmark status is **not_run**. I did not run claude-mem-lite, its tests, or any benchmark workload. No quality, latency, token, cost, storage, deletion, correction, or isolation measurement is claimed.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and SECURITY.md were checked for a contact email. The security page directs security reports through GitHub's private vulnerability reporting flow and publishes no email address. No contact email was found; commit metadata, profile metadata, and third-party directories were not used.[[readme]][[security]]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed repository locator, repository status, and Atlas attribution only.
- [Pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/claude-mem-lite.md) — roster attribution only, not assessment evidence.
- [Official repository](https://github.com/sdsrss/claude-mem-lite) — canonical repository and default branch.
- [Official main commit history](https://github.com/sdsrss/claude-mem-lite/commits/main.atom) — full current head and feed timestamp.
- [Reviewed commit](https://github.com/sdsrss/claude-mem-lite/commit/3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb) — full reviewed SHA.
- [README at reviewed SHA](https://github.com/sdsrss/claude-mem-lite/blob/3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb/README.md) — product, hooks, episode capture, retrieval, installation, and project-reported estimates.
- [Shared database schema](https://github.com/sdsrss/claude-mem-lite/blob/3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb/schema.mjs) — SQLite schema, FTS5, migrations, and persistent records.
- [MCP server](https://github.com/sdsrss/claude-mem-lite/blob/3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb/server.mjs) — memory tools and shared database integration.
- [Search engine](https://github.com/sdsrss/claude-mem-lite/blob/3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb/search-engine.mjs) — filtered FTS search, scoring, fallback, and expansion.
- [Observation write and update core](https://github.com/sdsrss/claude-mem-lite/blob/3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb/lib/observation-write.mjs) — insert and patch update handling.
- [Delete core](https://github.com/sdsrss/claude-mem-lite/blob/3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb/lib/delete-core.mjs) — shared delete orchestration.
- [Provenance helper](https://github.com/sdsrss/claude-mem-lite/blob/3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb/lib/provenance.mjs) — manual and machine-written record labels.
- [Security policy at reviewed SHA](https://github.com/sdsrss/claude-mem-lite/blob/3f6d5dcc4d0b59b35420f3d33a75ac61617df1fb/SECURITY.md) — official vulnerability reporting route; no email published.
- [Project metric definitions](../METRICS.md), [initial execution status](../results/initial-baselines-status.json), and [benchmark fixture](../fixtures/memory-benchmark-v1.json) — project protocol/status only.

**Verification boundary:** official repository and SHA-pinned documentation/source review only; no system execution, tests, or benchmarks.
