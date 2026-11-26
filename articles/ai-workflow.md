# AI Workflow Workspace — source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 39 / AI Workflow Workspace / ai-workflow  
**Listed repository locator:** [Taki7980/Ai-workflow](https://github.com/Taki7980/Ai-workflow)  
**Current canonical repository:** [Taki7980/Ai-workflow](https://github.com/Taki7980/Ai-workflow)  
**Default branch / reviewed head:** main / `ae3d3851cd89d7e6d521b79203a3cdbb99d74318`  
**Review time:** 2026-11-24 19:47:35 UTC (11:47:35 PST; America/Los_Angeles).

## Identity and scope

The curated catalog places **AI Workflow Workspace** at ordinal 39 with slug `ai-workflow` and listed locator `https://github.com/Taki7980/Ai-workflow`. The catalog's Agent Memory Atlas URL and revision are retained for identity attribution only. Atlas descriptions, marks, and layout were not used as assessment evidence.[[curated roster](../data/memory-systems.json)] [[Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ai-workflow.md)]

The official repository page identifies `Taki7980/Ai-workflow`, shows `main` as the default branch, and lists `ae3d385` as the latest commit. The official `main` Atom feed identifies the matching full SHA `ae3d3851cd89d7e6d521b79203a3cdbb99d74318`; this pins the source review.[[repository and default branch](https://github.com/Taki7980/Ai-workflow)] [[main commit feed](https://github.com/Taki7980/Ai-workflow/commits/main.atom)] [[reviewed commit](https://github.com/Taki7980/Ai-workflow/commit/ae3d3851cd89d7e6d521b79203a3cdbb99d74318)]

The README describes a reusable, agent-agnostic coding workflow. This review inspects selected workflow and persistent-knowledge scripts; it does not assess a running installation.[[README at reviewed revision](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/README.md)]

## Who and what

The repository presents a project workflow template for AI-assisted coding. Its root `AGENTS.md` is the stated rulebook, while project-local PowerShell scripts route requests, search generated indexes, capture handoffs, and preserve durable notes. This is a local workflow and knowledge workspace rather than a hosted memory service.[[README](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/README.md)] [[AI Workspace map](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/README.md)]

## Architecture and data model

The workspace separates scripts, agent configuration and references, a persistent brain, Obsidian notes, and generated caches. Its README maps scripts for session routing, index traversal, handoff validation, index generation, task completion, and brain capture/recall. Generated caches and indexes are described as rebuildable machine output.[[AI Workspace map](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/README.md)]

Brain storage has a compact Markdown index row with ID, date, type, and keywords, plus a full Markdown entry containing Problem, Solution, and required Evidence fields. Optional entry fields include root cause, failed approaches, changed files, and a lesson. Capture appends a row and full entry to the respective files.[[brain capture](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-capture.ps1)]

Incident notes use Markdown with YAML-like frontmatter. The compiler recognizes fields such as ID, kind, status, trust, title, module, error signature, related files/tests, and last verified commit, then emits compact JSONL records for lookup. Missing trust defaults to `draft`; missing status defaults to `unknown`.[[incident cache compiler](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/compile-incident-cache.ps1)]

## Write, update, delete, and retrieval

**Write.** Brain capture requires a type, keywords, problem, solution, and nonblank evidence. It assigns a date-based sequence ID and appends an index row plus a full Markdown entry; root cause, failed approaches, changed files, and lesson are optional.[[brain capture](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-capture.ps1)]

**Update and correction.** The inspected brain capture path is append-only. The task-completion path can move an open incident note to the resolved directory, update its status, trust, review date, and verified commit, then rebuild the incident cache. The reviewed paths do not show a general brain-record update API.[[brain capture](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-capture.ps1)] [[task completion](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/complete-task.ps1)]

**Delete.** The inspected brain capture, recall, and completion scripts do not expose a brain-entry deletion operation. Notes are ordinary Markdown files, but this review did not trace a supported brain cleanup or deletion workflow.[[brain capture](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-capture.ps1)] [[brain recall](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-recall.ps1)] [[task completion](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/complete-task.ps1)]

**Retrieval.** Brain recall tokenizes the query and indexed type/keywords, builds corpus statistics, computes BM25+ scores, and applies a date-based retention factor when its helper is available. Without the math helper it falls back to term counts. It ranks the top matches and extracts the matching full entries from the brain file.[[brain recall](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-recall.ps1)]

Session routing classifies queries and can consult hot or incident caches, generated indexes, and the brain index. The separate traversal script searches indexed symbols/endpoints and validates candidate source files against stored hashes; stale or unverifiable index candidates are rejected.[[session router](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brief.ps1)] [[zero-grep traversal](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/traverse.ps1)]

## Scope isolation

The brain and project notes are resolved beneath the project workspace, so source-visible scope is a local project workspace. The inspected brain and incident record formats do not include user, tenant, or agent authorization keys. This review did not verify operating-system permissions or behavior when multiple users share files.[[AI Workspace map](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/README.md)] [[brain capture](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-capture.ps1)] [[incident cache compiler](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/compile-incident-cache.ps1)]

## Provenance and evidence

Brain capture requires free-text Evidence and can store changed-file and root-cause notes. Incident records can carry a trust value and last verified commit; the completion flow marks an incident resolved and verified. These fields record context, but the inspected sources do not define claim-level citations or independent evidence review.[[brain capture](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-capture.ps1)] [[incident cache compiler](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/compile-incident-cache.ps1)] [[task completion](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/complete-task.ps1)]

## Source-visible efficiency and observability

The source uses local scripts and Markdown/JSONL data paths. Brain retrieval builds corpus statistics from the index and scores the entries on each invocation; traversal hashes only candidate files before accepting index rows. These implementation details do not establish speed, token reduction, quality, or storage efficiency. The scripts report routing/retrieval status and task-check outcomes, but this review collected no runtime telemetry.[[brain recall](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-recall.ps1)] [[zero-grep traversal](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/traverse.ps1)] [[task completion](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/complete-task.ps1)]

## Metric-domain evidence

All outcome metrics are **unmeasured** for this review:

- **Answerable recall and abstention:** keyword/BM25+ retrieval is visible in source; no answerability or abstention cases were run.
- **Correction and stale values:** append capture and incident metadata updates are visible; no correction or stale-value probes were run.
- **Deletion leakage:** no brain deletion operation was identified in the inspected paths; no post-deletion probes were run.
- **Scope isolation:** storage is project-workspace based in inspected paths; no cross-project or cross-user probes were run.
- **Evidence support and citation coverage:** free-text evidence fields exist; no answer-level evidence was adjudicated.
- **Latency and write-to-recall delay:** no timing measurements were collected.
- **Tokens and cost:** no token or provider-cost measurements were collected.
- **Storage efficiency:** no storage-size measurement was collected.

Project metric definitions, the benchmark fixture, and execution status are links to the evaluation protocol only; they are not results for AI Workflow Workspace: [metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).[[project metrics](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark status](../results/initial-baselines-status.json)]

## Limits and unknowns

This bounded review inspected the public README, workspace map, session router, index traversal, brain capture/recall, task completion, and incident compiler at the verified head. It did not inspect all scripts, every handoff lane, all Obsidian templates, or every host integration. It also did not exercise behavior against real workspace data.

Source code and comments do not establish recall quality, cognitive validity of the retention factor, effective access isolation, reliability, latency, token use, cost, or storage efficiency. Windows and PowerShell runtime behavior was not tested. No system, benchmark workload, or tests were run.

The official pinned README was checked for a published contact email; none was found. The official repository's `SECURITY.md` path was also checked and is absent at this revision. The record stores `contact_email: null` and the README URL as the checked contact source.[[official README contact check](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/README.md)] [[checked SECURITY.md path](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No AI Workflow Workspace runtime, benchmark workload, or tests were executed. Project metric definitions, fixture, and execution status document the protocol and status only; they are not system results.

## Sources

- [Official repository and default branch](https://github.com/Taki7980/Ai-workflow)
- [Official main branch commit feed](https://github.com/Taki7980/Ai-workflow/commits/main.atom)
- [Reviewed commit](https://github.com/Taki7980/Ai-workflow/commit/ae3d3851cd89d7e6d521b79203a3cdbb99d74318)
- [README at reviewed revision](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/README.md)
- [AI Workspace architecture and file map](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/README.md)
- [Session routing](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brief.ps1)
- [Traversal and index freshness](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/traverse.ps1)
- [Brain capture](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-capture.ps1)
- [Brain retrieval](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/brain-recall.ps1)
- [Task completion](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/complete-task.ps1)
- [Incident cache compiler](https://github.com/Taki7980/Ai-workflow/blob/ae3d3851cd89d7e6d521b79203a3cdbb99d74318/ai-workspace/scripts/compile-incident-cache.ps1)
- [Project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json)
- [Curated roster identity and attribution only](../data/memory-systems.json)

---