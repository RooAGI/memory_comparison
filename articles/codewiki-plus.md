# CodeWiki-Plus source review

**Roster position:** 133 — CodeWiki-Plus (codewiki-plus)  
**Listed repository:** [mambo-wang/CodeWiki-Plus](https://github.com/mambo-wang/CodeWiki-Plus) (explicit catalog locator)  
**Canonical upstream:** [mambo-wang/CodeWiki-Plus](https://github.com/mambo-wang/CodeWiki-Plus)  
**Default branch:** develop  
**Reviewed head:** [7cd5740673c9166184372095e7286f5fd115e5c8](https://github.com/mambo-wang/CodeWiki-Plus/commit/7cd5740673c9166184372095e7286f5fd115e5c8)  
**Reviewed:** 2026-11-25 08:29:39 UTC (2026-11-25 00:29:39 PST; America/Los_Angeles)  
**Review status:** Reviewed from current upstream source and documentation  
**Benchmark status:** Benchmark not run

The curated catalog places CodeWiki-Plus at ordinal 133 with slug codewiki-plus, an explicit repository locator, and a pinned Atlas roster attribution. The catalog and Atlas report establish identity and attribution only; assessment claims below come from official upstream documentation and source.[[catalog]][[atlas]] GitHub's repository page selects develop; the official develop commits feed reported full head 7cd5740673c9166184372095e7286f5fd115e5c8, updated 2026-11-24T01:40:25Z. The repository page's abbreviated head and the official commit page agree.[[repository]][[head]][[revision]]

## Summary

CodeWiki-Plus is an AI IDE driven repository knowledge engine and memory toolkit. It combines a structured repository wiki, lifecycle managed notes, per-task memory files, MCP tools, IDE hooks, and team usage telemetry. The IDE's own agent performs reasoning while CodeWiki-Plus exposes tools for reading, writing, retrieval, and maintenance.[[readme]]

## Who and what

The official README describes CodeWiki-Plus as an independently evolved open-source project built on the CodeWiki toolchain. It is distributed as a Python package and provides an MCP server, CLI, hooks, and workflow prompts; this review does not infer maintainer identity from GitHub profile or commit metadata.[[readme]]

## Architecture and data model

The default knowledge workspace is a repository-local repowiki tree. It stores wiki pages, structured notes, imported raw sources, conversation transcripts, task records, and metadata. A SQLite analysis/search cache and BM25 index support repository analysis and wiki retrieval; the README also describes a wikilink graph and progressive overview, directory, and detail reading.[[readme]][[note_query]]

Notes are Markdown files with YAML frontmatter. The lifecycle uses draft, stable, and deprecated statuses, with a separate strong/weak/shadow confidence value. The note writer normalizes legacy status names, extracts an optional source_ref, derives a trust tier from verification entries, and performs status rewrites under a cross-process lock before atomically writing the file.[[readme]][[note_writer]]

Task memory is separate from wiki notes: each task has per-user append-oriented memory files and per-user compaction archives. The current user's file is loaded in full; other users' files are exposed as a summary plus a small recent portion. The task manager documents file-level isolation for concurrent users and compaction confined to the caller's own file.[[task_manager]][[readme]]

## Write, update, delete, and retrieval

**Writing.** ingest_note stores structured notes in the wiki; the README documents draft as the default and direct stable ingestion as requiring a reason. The writer refreshes the wiki index and BM25 search entry after a write on a best-effort basis. Conversation capture stores transcripts separately, while distillation can create notes and task memories. add_task_memory writes directly to the selected task's current user's memory file.[[readme]][[note_ingest]][[note_writer]][[task_manager]]

**Correction and lifecycle.** confirm_note promotes a note to stable and records a verification entry; evidence references can raise confidence. reject_note marks the note deprecated and shadow, and default note retrieval filters deprecated records while retaining them on disk. Task-memory corrections can supersede entries, and compaction archives older material while keeping a recent hot layer. These lifecycle actions preserve useful history but are not themselves benchmark evidence of correction accuracy.[[readme]][[note_writer]][[note_query]][[task_manager]]

**Deletion.** The task manager documents delete_task as removing the task directory, task index entry, and session bindings pointing to the task. The reviewed note lifecycle exposes rejection/deprecation, not a general secure-erasure guarantee; the inspected documentation does not establish erasure from backups, Git history, or other copies. Deleting a task can leave notes that carry a task_id reference.[[task_manager]][[note_query]][[readme]]

**Retrieval.** Wiki search uses BM25 and supports progressive reading, confidence/status annotations, and optional shadow inclusion. The query implementation has overview, directory, detail, check, and by-file paths; check is a capped top-three precheck that omits graph expansion and retrieval statistics. Task-memory search runs an in-memory BM25 pass over the chosen task corpus, with archive search available by default.[[readme]][[note_query]][[task_manager]]

## Scope isolation

Wiki data is located under a configured repository workspace. Task memories are addressed by caller-supplied task_id and stored in per-user files; the task manager's layered loading and author-exclusive compaction reduce accidental cross-user writes. The inspected sources do not establish that task IDs or repository paths are an authenticated authorization boundary, or that shared-workspace users are isolated against a malicious caller.[[readme]][[task_manager]][[note_query]]

## Provenance and evidence

Notes may carry a source_ref to an archived source conversation, and verification entries record an actor and timestamp. The README describes evidence stamping for wiki assertions, conflict case files, and bidirectional provenance when compiled skills refer back to source notes. These mechanisms vary by write path: source_ref extraction is best-effort, and the reviewed note writer does not require every note to have a source, quoted evidence, or independent review.[[readme]][[note_writer]]

## Efficiency and observability

The README and source describe BM25 indexing, a wikilink retrieval graph, bounded/progressive reads, and token estimates for MCP output. Team telemetry uses per-user JSONL event files for retrieval hits, adoptions, and outcomes, while wiki statistics summarize usage and outcome signals. These are observability mechanisms, not performance results; the review collected no latency, token, cost, or storage measurements.[[readme]][[note_query]][[telemetry]]

## Metric-domain evidence

All benchmark domains are **unmeasured** in this review. Source-visible mechanisms are not accuracy, isolation, or resource measurements.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Status |
|---|---|---|
| Answerable recall and abstention | BM25 search, graph expansion, progressive reads, and a check mode are present; no labeled answerability probes were run. | Unmeasured |
| Correction accuracy and stale values | Note status transitions and task-memory supersession exist; no correction sequence was adjudicated. | Unmeasured |
| Deletion leakage | Task deletion removes its directory and bindings; no post-delete or residual-copy audit was run. | Unmeasured |
| Scope isolation | Repository workspaces, task IDs, and per-user files are source-visible; no cross-user or cross-workspace isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Source references, verification records, and wiki evidence features exist; no claim-evidence adjudication was performed. | Unmeasured |
| Retrieval latency and write-to-recall delay | Search and indexing paths are visible; no timings were collected. | Unmeasured |
| Tokens and cost | The project exposes output token estimates; no token totals or provider charges were measured. | Unmeasured |
| Storage efficiency | Workspace files, SQLite cache, and JSONL telemetry are documented; no corpus-attributable storage measurement was collected. | Unmeasured |

The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) describe evaluation criteria and project status only; they are not CodeWiki-Plus results.[[metrics]][[fixture]][[status]]

## Limitations and unknowns

The system delegates much knowledge extraction and use to an IDE agent, so source structure and workflow prompts cannot establish that a model creates accurate notes or follows retrieval and verification instructions. Status and confidence metadata are part of the workflow, but the reviewed code does not make them independent adjudication of truth. Optional task_id filters are caller-selected, and deletion behavior is not evidence of secure erasure.[[readme]][[note_writer]][[note_query]][[task_manager]]

This review inspected the official README, note ingestion and lifecycle code, note query code, task-memory code, and telemetry code at the pinned head. It did not execute CodeWiki-Plus, its tests, hooks, or benchmark workloads, and did not inspect every integration, hook, persistence, or security path. Runtime quality, authorization behavior, and resource consumption remain unknown.[[revision]][[readme]][[note_ingest]][[note_writer]][[note_query]][[task_manager]][[telemetry]]

## Contact

The official pinned [README.md](https://github.com/mambo-wang/CodeWiki-Plus/blob/7cd5740673c9166184372095e7286f5fd115e5c8/README.md) was checked and publishes no contact email. The exact pinned [SECURITY.md](https://github.com/mambo-wang/CodeWiki-Plus/blob/7cd5740673c9166184372095e7286f5fd115e5c8/SECURITY.md) URL returned GitHub's “File not found” page. No commit/profile metadata or third-party directory was used.[[readme]][[security]]

## Benchmark status

**Benchmark not run.** I did not run CodeWiki-Plus, its tests, or benchmarks. The project's metric definitions, fixture, and execution status are evaluation context only and do not contain CodeWiki-Plus measurements.[[metrics]][[fixture]][[status]]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed repository, repository status, and Atlas attribution only.
- [Pinned Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/codewiki-plus.md) — identity and locator attribution only.
- [Official repository](https://github.com/mambo-wang/CodeWiki-Plus) — canonical repository and selected default branch.
- [Official develop commits feed](https://github.com/mambo-wang/CodeWiki-Plus/commits/develop.atom) — full head SHA and update timestamp.
- [Reviewed commit](https://github.com/mambo-wang/CodeWiki-Plus/commit/7cd5740673c9166184372095e7286f5fd115e5c8)
- [README](https://github.com/mambo-wang/CodeWiki-Plus/blob/7cd5740673c9166184372095e7286f5fd115e5c8/README.md)
- [Note ingestion](https://github.com/mambo-wang/CodeWiki-Plus/blob/7cd5740673c9166184372095e7286f5fd115e5c8/codewiki/mcp/tools/note_ingest.py)
- [Note writer and lifecycle](https://github.com/mambo-wang/CodeWiki-Plus/blob/7cd5740673c9166184372095e7286f5fd115e5c8/codewiki/mcp/tools/note_writer.py)
- [Note query and retrieval](https://github.com/mambo-wang/CodeWiki-Plus/blob/7cd5740673c9166184372095e7286f5fd115e5c8/codewiki/mcp/tools/note_query.py)
- [Task memory manager](https://github.com/mambo-wang/CodeWiki-Plus/blob/7cd5740673c9166184372095e7286f5fd115e5c8/codewiki/mcp/tools/task_manager.py)
- [Team telemetry](https://github.com/mambo-wang/CodeWiki-Plus/blob/7cd5740673c9166184372095e7286f5fd115e5c8/codewiki/mcp/tools/telemetry.py)
- [Project metrics](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) — definitions/status only.

**Verification boundary:** Current pinned upstream documentation and source review; no CodeWiki-Plus runtime, tests, or benchmarks were run.
