# Dynamics-memory

## Identity and review pin

- Catalog ordinal: 204
- System: Dynamics-memory
- Slug: dynamics-memory
- Listed repository: https://github.com/1173591564/Dynamics-memory
- Roster attribution: catalog has an explicit repository locator; the pinned Atlas entry is used only for identity and locator attribution, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dynamics-memory.md)).
- Canonical repository after GitHub redirect: https://github.com/1173591564/memory-manage
- Default branch: mvp-2
- Reviewed full head: [a779a92d32b888eae4c5141d1bb416472cf093a7](https://github.com/1173591564/memory-manage/commit/a779a92d32b888eae4c5141d1bb416472cf093a7)
- Review timestamp: 2026-11-25T11:51:42Z (UTC; 2026-11-25 03:51:42 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub redirects the listed repository locator to 1173591564/memory-manage. Official repository metadata identifies mvp-2 as the default branch, and the branch endpoint reports full head a779a92d32b888eae4c5141d1bb416472cf093a7. The root README describes tasklog as the current runnable project and refers to Dynamics-memory as prior research. This review therefore describes current tasklog source and does not attribute uninspected historical Dynamics-memory internals to it. ([listed locator](https://github.com/1173591564/Dynamics-memory), [repository metadata](https://api.github.com/repos/1173591564/memory-manage), [default branch head](https://api.github.com/repos/1173591564/memory-manage/commits/mvp-2), [pinned root README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/README.md))

## Summary

The current default-branch project, tasklog, is a local SQLite and MCP history layer for coding agents. It stores raw events, organizes them into tasks, builds symbol and text indexes, and lets an agent retrieve history by task, symbol, or query. Its README distinguishes historical rationale from current code state: the repository says to consult current code and Git for “what is now,” and tasklog for past decisions and failed attempts. This is a review of the current canonical repository at the verified SHA, with the catalog-to-current-project naming shift called out explicitly. ([tasklog README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/README.md), [core types](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/types.ts))

## Who and what

The catalog lists the name Dynamics-memory and an explicit GitHub locator. GitHub redirects that locator to the public repository 1173591564/memory-manage. At the reviewed default branch, the root README describes tasklog as the current runnable project and lists Dynamics-memory under research/source notes. The available source establishes the redirect and repository contents, but does not independently establish that current tasklog is an unchanged version of the catalogued Dynamics-memory system. ([catalog](../data/memory-systems.json), [listed locator](https://github.com/1173591564/Dynamics-memory), [repository metadata](https://api.github.com/repos/1173591564/memory-manage), [root README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/README.md))

## Architecture and data model

Tasklog’s core unit is an event, not a distilled memory or summary. Its SQLite schema stores event/session/task metadata, tasks with stable identifiers and boundary/status evidence, task edges such as continues and supersedes, extracted symbols, and FTS indexes. The core types say there is no Memory or Summary type. ([schema](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/db/schema.ts), [types](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/types.ts))

The database defaults to .tasklog/log.db under the project root, with a sibling blobs directory. Event records include timestamps, session sequence, role, kind, tool names and arguments, call/result IDs, outcome, task ID, and optional source identity fields. Tool outputs above the inline size threshold are content-addressed on disk; event text retains a mechanical preview and blob locator. ([database open](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/db/open.ts), [schema](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/db/schema.ts), [ingestion and blob code](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/ingest/events.ts))

## Write, update, delete, retrieval, and scope

**Write.** The ingestion implementation inserts events, mechanically extracts symbols, lets SQLite’s FTS index update, and stores large outputs in blob files. The README describes this path as zero LLM calls; source imports preserve a host’s stable record ID to prevent duplicate ingestion. ([ingestion](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/ingest/events.ts), [symbol extraction](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/ingest/symbols.ts), [types](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/types.ts), [tasklog README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/README.md))

**Update.** Source imports use source/source_id for idempotence. Task boundaries are maintained as indexes over the event log and can be revised; task relationships can mark a superseding task. The reviewed MCP tool set is query-oriented and does not expose an editing operation for an individual memory record. ([schema](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/db/schema.ts), [queries](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/query/index.ts), [MCP server](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/mcp/server.ts))

**Delete.** No deletion or erasure operation appears in the reviewed query and MCP surface. This bounded inspection does not establish whether separate administrative code can delete local databases or blobs, and it does not establish physical erasure from backups or imported host snapshots. ([MCP server](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/mcp/server.ts), [event/blob implementation](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/ingest/events.ts))

**Retrieval.** The documented tools provide task listing, history search, symbol history, task resumption, paged event reads, and blob reads. Query results carry task, session, sequence, and event locators. Optional vector search uses a configured embedding API and joins chunk-level matches to source events; a missing embedding configuration leaves the embedding provider unavailable. ([tasklog README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/README.md), [queries](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/query/index.ts), [vector search](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/query/vector.ts), [MCP server](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/mcp/server.ts))

**Scope isolation.** The default database is project-local, and the server accepts explicit repository and database paths. The reviewed server is stdio-based and does not implement user authentication or tenant authorization. Isolation therefore depends on the host process and filesystem configuration; no cross-project workload was run. ([database open](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/db/open.ts), [MCP server](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/mcp/server.ts))

## Provenance, evidence, efficiency, and observability

Imported event records can retain the host name, stable source ID, and original source metadata, while inferred fields remain distinguishable. Large outputs retain content-addressed blob locators that can be read in ranges. Task segmentation records a source and evidence separately from task status; the README warns that inferred task boundaries do not prove a task was completed. These fields support trace-back but do not validate whether recorded content is true. ([types](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/types.ts), [schema](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/db/schema.ts), [ingestion](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/ingest/events.ts), [tasklog README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/README.md))

Efficiency mechanisms visible in source include per-kind symbol quotas, SQLite FTS5/trigram indexing, database indexes, paged event reads, bounded previews for large outputs, and optional vector retrieval. The CLI and MCP surface include index health and event counts. These are code-visible mechanisms; no runtime throughput, latency, storage, token, or cost values were measured. ([schema](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/db/schema.ts), [symbol index](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/ingest/symbols.ts), [queries](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/query/index.ts), [vector search](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/query/vector.ts), [MCP server](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/mcp/server.ts))

## Metric-domain evidence

All project benchmark domains are **unmeasured** for this review. Source code, project documentation, and a benchmark fixture are not measured results. ([metric definitions](../METRICS.md), [fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval accuracy and abstention | Unmeasured | History search and task resumption exist; no adjudicated retrieval workload was run. |
| Correction accuracy and stale-value rate | Unmeasured | Task supersedes relationships are represented; no correction workload was run. |
| Deletion leakage | Unmeasured | No deletion or erasure probe was run. |
| Scope isolation leak rate | Unmeasured | The code configures project-local databases; no isolation workload was run. |
| Evidence support precision and citation coverage | Unmeasured | Event provenance and locators exist; no claim/source adjudication was run. |
| Retrieval latency | Unmeasured | No timed workload was run. |
| Write-to-recall delay | Unmeasured | Ingest and retrieval paths exist; no delay was measured. |
| Tokens and cost | Unmeasured | The write path is documented as zero-LLM and embeddings are optional; no usage or cost accounting was collected. |
| Storage efficiency | Unmeasured | SQLite and blob storage are used; no storage comparison was measured. |

## Limits and unknowns

The catalogued repository URL redirects to memory-manage. The verified default branch now identifies tasklog as the current runnable project and Dynamics-memory as prior research. The review describes that current source and preserves uncertainty about continuity with the catalogued system. It does not claim that the historical system name maps unchanged to the current default-branch project. ([catalog](../data/memory-systems.json), [listed locator](https://github.com/1173591564/Dynamics-memory), [repository metadata](https://api.github.com/repos/1173591564/memory-manage), [root README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/README.md))

This bounded source review covered the current root and tasklog READMEs, schema, types, SQLite opening, event ingestion, symbol extraction, queries, optional vector search, and MCP server. It did not audit every adapter, task segmentation implementation, evaluation path, deployment, or host integration. Code inspection cannot establish deployed access control, deletion behavior outside the reviewed surface, actual retrieval quality, benchmark metrics, or runtime correctness. ([root README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/README.md), [tasklog README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/README.md), [schema](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/db/schema.ts), [MCP server](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/mcp/server.ts))

## Contact

The pinned official root README and tasklog README were checked; neither publishes a contact email. The repository has no SECURITY.md at the reviewed head. No commit/profile metadata or third-party directories were used. ([root README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/README.md), [tasklog README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/README.md), [SECURITY.md check](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/SECURITY.md))

## Benchmark status

**Benchmark not run.** No system runtime, tests, or benchmark workload was executed. See the [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dynamics-memory.md)
- [Listed repository URL and canonical redirect](https://github.com/1173591564/Dynamics-memory)
- [Official canonical repository metadata](https://api.github.com/repos/1173591564/memory-manage)
- [Verified default-branch head](https://api.github.com/repos/1173591564/memory-manage/commits/mvp-2)
- [Reviewed full-SHA commit](https://github.com/1173591564/memory-manage/commit/a779a92d32b888eae4c5141d1bb416472cf093a7)
- [Pinned root README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/README.md)
- [Pinned tasklog README](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/README.md)
- [Pinned database schema](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/db/schema.ts)
- [Pinned core types](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/types.ts)
- [Pinned event ingestion](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/ingest/events.ts)
- [Pinned symbol extraction](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/ingest/symbols.ts)
- [Pinned query implementation](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/query/index.ts)
- [Pinned optional vector search](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/query/vector.ts)
- [Pinned MCP server](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/mcp/server.ts)
- [Pinned SQLite initialization](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/tasklog/src/db/open.ts)
- [Official SECURITY.md contact check](https://github.com/1173591564/memory-manage/blob/a779a92d32b888eae4c5141d1bb416472cf093a7/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution status](../results/initial-baselines-status.json)

---