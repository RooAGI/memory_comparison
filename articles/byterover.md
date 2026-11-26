# ByteRover

## Identity and review pin

- **System:** ByteRover
- **Curated position:** 108
- **Slug:** byterover
- **Listed repository:** [campfirein/byterover-cli](https://github.com/campfirein/byterover-cli)
- **Canonical repository at review:** [campfirein/byterover-cli](https://github.com/campfirein/byterover-cli)
- **Default branch:** main
- **Reviewed head:** [1052ac1a5dd0fde4da8693d4712064f7876c269c](https://github.com/campfirein/byterover-cli/commit/1052ac1a5dd0fde4da8693d4712064f7876c269c)
- **Reviewed:** 2026-11-25 00:34:39 UTC (16:34:39 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [Curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/byterover.md), used for identity and source attribution only.

The curated roster places ByteRover at position 108 with slug byterover and the listed locator above. Its Atlas source is recorded for attribution only; Atlas descriptions, marks, and layout were not used as assessment evidence.[[catalog]][[atlas]] The official repository identifies main as the default branch and the latest commit. The main commit feed names full head 1052ac1a5dd0fde4da8693d4712064f7876c269c; read-only git metadata and a shallow checkout independently resolved main to the same SHA.[[repo]][[head-feed]][[head]]

## Summary

ByteRover CLI (brv) is a project knowledge and agent memory toolkit. Its main project-memory path curates structured HTML or Markdown topics under a project context tree and retrieves them with a cached local BM25 index. A separate Cipher MemoryManager stores scratch memories as blobs.[[readme]][[search]][[memory-manager]]

## Who and what

The README describes ByteRover CLI as built and maintained by the ByteRover team. It is a local CLI/TUI and agent-tool framework with an optional hosted cloud collaboration service. GitHub marks the repository archived and read-only as of 2026-09-27.[[readme]][[repo]]

## Architecture and data model

**Source observations.** The project context tree lives under .brv/context-tree. Topic files carry semantic frontmatter such as title, summary, tags, related paths, keywords, and timestamps; the ContextData model also supports facts, narrative sections, snippets, raw concept metadata, and relations. The current curation path writes HTML topics, while Markdown is still supported by selected readers and legacy paths.[[context-tree]][[markdown-writer]][[curate-tool]][[search]]

The search service builds a MiniSearch BM25 index over title, content, and path. It also builds symbol/reference structures, creates excerpts, and can include configured read-only shared project sources. Ranking signals such as importance, recency, maturity, access count, and update count live in a sidecar instead of shared topic frontmatter.[[search]][[source-schema]][[runtime-signals]]

Cipher's separate MemoryManager stores JSON memory records through an injected BlobStorage. A record has an ID, content, creation/update timestamps, optional tags, and metadata such as source or pinned status; attachments refer to separately stored blobs. The service initializer wires the manager to configured blob storage.[[memory-types]][[memory-manager]][[service-init]]

## Write, update, delete, and retrieval

**Curation.** The tool supports ADD, UPDATE, UPSERT, MERGE, and DELETE. An UPDATE reads the existing topic, detects structural loss in a proposed rewrite, merges dropped structure back, raises review impact when loss is found, backs up existing content when review is enabled, writes the new file atomically, and updates ranking signals. DELETE removes a topic file or recursively removes a topic folder and drops its sidecar entries.[[curate-tool]][[markdown-writer]][[curate-log]]

**Archive and delete are different operations.** Archiving stores the original topic losslessly as a .full.md file, writes a searchable .stub.md cue, and removes the original path. The full archived copy can be retrieved through drill-down or restored, so archiving is not erasure.[[archive]]

**Retrieval.** Search defaults to 10 results, caches its index for five seconds by default, uses a 10,000-result cap in each HTML/Markdown file-discovery pass, chunks long documents into roughly 800-character excerpts with overlap, and filters by ranking thresholds and a score gap. Multiword queries try AND and fall back to OR. If a requested path scope yields no results, the service retries globally; this makes the scope a retrieval hint rather than a guaranteed isolation boundary.[[search]]

The query executor has cache, direct-search, optimized-LLM, and full-agentic response tiers, and can prefetch up to five high-confidence documents. It passes workspace-relative scope to search, but the source comment notes that topic paths are semantic rather than directory-shaped, so scoped searches often miss and fall back to unscoped retrieval. Configured shared project sources are explicitly read-only but still participate in search.[[query-executor]][[source-schema]][[search]]

**Cipher scratch memories.** The manager exposes create, get-by-ID, list, partial update, and delete operations. Listing filters by source or pinned status and paginates after loading records; results are sorted by most recently updated. Validation caps content at 10,000 characters and tags at ten entries of at most 50 characters. The Memory schema has no project or user scope field. Delete attempts to remove attachment blobs as well as the memory record.[[memory-types]][[memory-manager]]

## Provenance and evidence

Curated topics retain structured fields such as facts, related paths, tags, and source information in content. Curate logs can preserve operation type/path, reason, before/after summaries, confidence/impact, review status, token usage, and timings. Query logs preserve query text, matched paths/titles/scores, status, resolution tier, token use, and optional timing fields. These fields aid inspection and review but do not constitute measured evidence support or citation accuracy.[[markdown-writer]][[curate-log]][[query-log-entry]][[curate-log-store]][[query-log-store]]

## Source-visible efficiency and observability

**Code observations, not measurements.** Search has a five-second default index-cache TTL and a 10,000-file discovery cap; returned results are limited by the caller (default 10), and long documents are excerpted in overlapping character chunks. Logs have configurable retention with defaults of 30 days and 1,000 query entries. The query executor records separate search, LLM, and total timings when wired, and captures token usage when provided by the model adapter.[[search]][[query-log-store]][[query-log-entry]]

The source exposes curation and query logs, ranking counters, cache/search result metadata, and per-query timing/token fields. It does not provide benchmark measurements in this review, and cost or persistent-storage bytes are not established by these code paths.[[curate-log]][[query-log-entry]][[runtime-signals]]

## Metric-domain evidence

All domains below are **unmeasured for this review**. The table describes code-visible mechanisms only.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | BM25 search, score thresholds, and no-match responses are implemented. | Unmeasured |
| Correction accuracy and stale values | Curate update includes structural-loss detection and repair. | Unmeasured |
| Deletion leakage | Topic and scratch-memory deletion paths exist; archive preserves full content. | Unmeasured |
| Scope isolation | Search has project and shared-source roots, but an empty scoped result retries globally. | Unmeasured |
| Evidence support and citation coverage | Topic metadata and matched document paths are recorded; claim support was not adjudicated. | Unmeasured |
| Latency and write-to-recall delay | Query timing fields and index caching exist; no timing samples were collected. | Unmeasured |
| Tokens and cost | Query and curate logs can hold token usage; no token totals or charges were measured. | Unmeasured |
| Persistent storage | Topic files, ranking sidecars, logs, and scratch blobs are visible storage surfaces; no byte count was collected. | Unmeasured |

The official README reports 96.1% LoCoMo and 92.8% LongMemEval-S LLM-as-Judge accuracy. These are upstream-reported figures, not reproduced measurements from this review. The [project metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) describe the local evaluation protocol; project-wide status is not a ByteRover result.[[readme]][[metrics]][[fixture]][[status]]

## Limits and unknowns

This is a read-only inspection of selected source at the pinned SHA. It does not establish capture quality, answer accuracy, score calibration, real-world isolation, cloud behavior, or deletion from Git history, backups, shared sources, and archived copies. It also does not evaluate concurrent edits, large projects, every integration, or external authorization wrappers.[[search]][[query-executor]][[archive]][[readme]]

The Cipher MemoryConfig type documents maxMemories and a default storageDir, but the inspected MemoryManager constructor receives BlobStorage and the reviewed CRUD path does not itself enforce a memory-count cap. No scale or concurrency workload was exercised.[[memory-types]][[memory-manager]][[service-init]]

## Benchmark status

**Benchmark not run.** I did not execute ByteRover, a benchmark workload, or tests. The project fixture and metric document are plans for evaluation; status remains not_run. README percentages are upstream reports and are not this review's results.[[metrics]][[fixture]][[status]][[readme]]

## Contact-list follow-up

I checked the official pinned [README](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/README.md), which lists Discord and GitHub issues but publishes no contact email. I also checked the official [SECURITY.md](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/SECURITY.md) and [SUPPORT.md](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/SUPPORT.md) paths; neither file exists at the reviewed head. The JSON records null and these exact checked source URLs.

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed repository, and Atlas attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/byterover.md) — identity and source attribution only.
- [Official repository](https://github.com/campfirein/byterover-cli) — canonical repository, default branch, and archived status.
- [Main commit feed](https://github.com/campfirein/byterover-cli/commits/main.atom) — full main head at review time.
- [Reviewed head](https://github.com/campfirein/byterover-cli/commit/1052ac1a5dd0fde4da8693d4712064f7876c269c)
- [README](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/README.md)
- [Memory types](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/agent/core/domain/memory/types.ts)
- [MemoryManager](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/agent/infra/memory/memory-manager.ts)
- [Service initializer](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/agent/infra/agent/service-initializer.ts)
- [Search service](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/agent/infra/tools/implementations/search-knowledge-service.ts)
- [Query executor](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/server/infra/executor/query-executor.ts)
- [Read-only sources schema](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/server/core/domain/source/source-schema.ts)
- [Curate tool](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/agent/infra/tools/implementations/curate-tool.ts)
- [Curate log entity](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/server/core/domain/entities/curate-log-entry.ts)
- [Curate log store](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/server/infra/storage/file-curate-log-store.ts)
- [Context data model](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/server/core/domain/knowledge/markdown-writer.ts)
- [Context tree service](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/server/infra/context-tree/file-context-tree-service.ts)
- [Archive service](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/server/infra/context-tree/file-context-tree-archive-service.ts)
- [Runtime ranking signals](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/server/core/domain/knowledge/runtime-signals-schema.ts)
- [Query log entity](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/server/core/domain/entities/query-log-entry.ts)
- [Query log store](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/src/server/infra/storage/file-query-log-store.ts)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)
- [Security policy path checked](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/SECURITY.md) — absent at reviewed head.
- [Support policy path checked](https://github.com/campfirein/byterover-cli/blob/1052ac1a5dd0fde4da8693d4712064f7876c269c/SUPPORT.md) — absent at reviewed head.

**Verification boundary:** source inspection against 1052ac1a5dd0fde4da8693d4712064f7876c269c; no ByteRover runtime, benchmark workload, or tests were executed.
