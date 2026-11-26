# flow source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 242 / flow / `facets-flow`  
**Listed repository locator:** [Facets-cloud/flow](https://github.com/Facets-cloud/flow)  
**Canonical upstream:** [Facets-cloud/flow](https://github.com/Facets-cloud/flow)  
**Default branch / reviewed head:** main / [9ee3c405bf3d99b08f5ca204d7d1482c85513867](https://github.com/Facets-cloud/flow/commit/9ee3c405bf3d99b08f5ca204d7d1482c85513867)  
**Review time:** 2026-11-25 20:35:23 UTC (2026-11-25 12:35:23 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists ordinal 242 as flow, slug `facets-flow`, with the explicit repository locator `https://github.com/Facets-cloud/flow`. The pinned Atlas attribution is retained only for roster identity and locator context; Atlas descriptions and capability marks are not assessment evidence. GitHub identifies the canonical repository and default branch as `main`; a fresh `git ls-remote --symref` reported `main` at full head `9ee3c405bf3d99b08f5ca204d7d1482c85513867`, and a shallow checkout resolved to the same SHA. The official GitHub commit page also identifies that commit.[[catalog]][[atlas]][[repo]][[head]]

## Summary

flow is a local CLI for tracking work across agent sessions. It keeps task and project metadata in SQLite and briefs, progress notes, and a small shared knowledge base as Markdown files. Retrieval is directed through task context and agent file reads rather than a dedicated memory search engine. This is a source review; no system behavior or performance was measured.[[readme]][[schema]][[skill]][[show]]

## Who and what

The official README describes flow as a local CLI that gives work named tasks, briefs, dated notes, resumable Claude Code or Codex sessions, and messaging between sessions. It presents the tool as a personal workflow manager rather than a team task board or a standalone semantic-memory service.[[readme]]

The project is open source under Facets-cloud. The README names Rohit Raveendran and Anshul Sao as maintainers; this review does not infer a broader maintainer roster.[[readme]][[repo]]

## Architecture and data model

The SQLite schema stores projects, tasks, playbooks, owners, workdirs, status, priority, work directory, session identifiers and timestamps, parent-task relations, and archival timestamps. Task and project briefs and dated updates are separate Markdown files under the flow root; task updates and project updates live beside their respective entity directories.[[schema]][[skill]]

The five knowledge-base buckets are `user.md`, `org.md`, `products.md`, `processes.md`, and `business.md` under the flow root's `kb/` directory. The agent skill defines each bucket and instructs sessions to append dated bullets. The binary manages task metadata and orchestration; the skill directs the model to read and write Markdown.[[skill]][[done]]

A task binds to a harness session and its transcript; `flow show task` displays task fields and paths to the brief, updates, and KB files. The shown KB values are file paths, not indexed or ranked memory results.[[show]][[schema]]

The agent skill is embedded and installed into Claude Code or Codex with a session-start hook. Session instructions carry the task brief and direct the model to recover context from files. The README also describes child sessions and background tasks; these extend orchestration beyond memory storage.[[readme]][[skill]]

## Write, update, delete, and retrieval

**Write.** Task/project/playbook creation stores structured metadata in SQLite and creates a brief file. During ordinary sessions the skill directs the model to capture a durable user fact by reading the matching KB bucket, deduplicating, and appending a dated bullet without asking. Knowledge-base writes are model-mediated file edits rather than typed database facts.[[schema]][[skill]]

**Update and correction.** Task state and metadata are edited through CLI operations; task progress notes are dated Markdown files. The KB rule is append-only: a changed fact should become a new dated entry, not an edit to an old bullet. This is a convention instructed to the model and is not an enforced versioned fact or supersession structure.[[skill]][[schema]]

**Close-out capture.** `flow done` marks a task done, then asks the task's configured harness to run a headless sweep over its transcript. That sweep may append durable KB facts and, for project-attached tasks, a project update. Task completion remains successful when the optional sweep fails; the implementation describes it as best effort.[[done]]

**Delete and archive.** Task, project, and playbook archive operations set `archived_at`; unarchive clears it. Task archival also cleans task message-bus data. The skill and README state that archive does not remove briefs or progress updates. The inspected archive path does not provide a content-level deletion or erasure procedure for KB entries.[[archive]][[skill]][[readme]]

**Retrieval.** There is no dedicated semantic, lexical, or vector retrieval layer in the inspected design. `flow show` surfaces task/project/playbook metadata and relevant file paths; the skill says to read task briefs and recent updates for continuity and consult KB files on demand. What enters the model context depends on the agent following those instructions and selecting files.[[show]][[skill]][[readme]]

**Scope isolation.** Task and project notes are physically separated by entity directories, and task records carry project and work-directory references. The five KB files are global to the flow root and listed to task sessions without per-task, project, or user access checks in the inspected code. This is local single-user storage, not a tenant-isolated memory service; process and filesystem access controls were not evaluated.[[schema]][[show]][[skill]][[security]]

## Provenance and evidence

KB bullets contain a date and a short quote or paraphrase, but the KB format has no structured originating session, source span, confidence, trust state, or review status. Task records include session identifiers and timestamps, and close-out reads a transcript, but the resulting KB bullet is not linked back to transcript evidence by the reviewed data model. The append-only instruction reduces silent overwrites by convention, not enforcement.[[skill]][[schema]][[done]]

## Efficiency and observability

Context lookup is file-based and model-directed, avoiding a separate embedding service, vector database, or ranking stage. That design also places file reading and selection in the agent context window. `flow stats` parses Claude Code transcript events for file reads under default `~/.flow` paths and reports KB/task/project lookups and tokens; source matching is path-string based, and this review does not establish equivalent coverage for Codex sessions or relocated roots.[[stats]][[skill]][[readme]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for flow. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe evaluation materials, not results for flow.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | File exposure and agent-directed reads are present; no answer or abstention workload was scored. | Unmeasured |
| Correction accuracy and stale values | KB corrections are append-only by instruction; no competing-fact or stale-value probe was run. | Unmeasured |
| Deletion leakage | Archive is a soft state change and no KB erasure path was found in the inspected files; no deletion probe was run. | Unmeasured |
| Scope isolation | Source shows root-level shared KB files; no isolation workload or OS permission review was performed. | Unmeasured |
| Evidence support and citation coverage | Dated bullets and transcripts exist; no answer claims were adjudicated against originating evidence. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings or write-to-recall measurements were collected. | Unmeasured |
| Tokens, cost, and storage efficiency | A Claude transcript scanner exists, but this review collected no token, cost, corpus-size, or storage measurements for flow. | Unmeasured |

## Limits and unknowns

This bounded review inspected the current README, task schema, agent skill, task-show path, close-out sweep, archive behavior, and transcript statistics scanner at the verified main SHA. Flow, tests, and benchmarks were not run.[[readme]][[schema]][[skill]][[show]][[done]][[archive]][[stats]]

The README reports its authors' experience and describes reliability and context costs; those statements are upstream-reported and were not independently measured here.[[readme]]

No answer quality, abstention calibration, correction quality, deletion leakage, filesystem access-control boundary, concurrency behavior, latency, tokens per workload, monetary cost, or storage efficiency was measured. Whether a shared root-level KB is appropriate depends on the local installation's trust and filesystem boundary.[[skill]][[schema]][[metrics]][[fixture]][[status]]

## Benchmark status

**Benchmark not run.** No Flow runtime, tests, or benchmarks were executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned [README](https://github.com/Facets-cloud/flow/blob/9ee3c405bf3d99b08f5ca204d7d1482c85513867/README.md), [SECURITY.md](https://github.com/Facets-cloud/flow/blob/9ee3c405bf3d99b08f5ca204d7d1482c85513867/SECURITY.md), [CONTRIBUTING.md](https://github.com/Facets-cloud/flow/blob/9ee3c405bf3d99b08f5ca204d7d1482c85513867/CONTRIBUTING.md), and [project website](https://facets-cloud.github.io/flow/) were checked for a contact email; none was found.[[readme]][[security]][[contributing]][[website]] No contact was inferred from commit/profile metadata or a third-party directory.

## Sources

Repository code and documentation links are pinned to the verified full SHA. The Atlas attribution above is included only for curated identity and locator context. See the structured record [facets-flow.json](../data/system-reviews/facets-flow.json) and the [curated roster](../data/memory-systems.json).
