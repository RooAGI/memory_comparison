# ctx source review

**Review status:** Reviewed from code (selected source review)  
**Benchmark status:** Not run  
**Roster ordinal / name / slug:** 174 / ctx / `ctx`  
**Listed repository locator:** `https://github.com/ActiveMemory/ctx` (explicit; current page is the ActiveMemory/ctx repository)  
**Catalog attribution:** [Pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ctx.md), used only for roster identity and locator attribution  
**Canonical repository / default branch:** [ActiveMemory/ctx](https://github.com/ActiveMemory/ctx) / `main`  
**Reviewed head:** [`a0058eacc06a4e2a5423aafbdfdd927966d078ca`](https://github.com/ActiveMemory/ctx/commit/a0058eacc06a4e2a5423aafbdfdd927966d078ca); the official [main commit feed](https://github.com/ActiveMemory/ctx/commits/main.atom) reports that full head and an update time of 2026-11-07T20:24:25Z.  
**Review time:** 2026-11-25 22:21:18 UTC.  
**Published contact:** No email address was found in the pinned official README reviewed for this record.

## Identity and scope

The catalog entry at ordinal 174 has slug `ctx` and explicitly lists `https://github.com/ActiveMemory/ctx`. GitHub opens that URL as the public ActiveMemory/ctx repository. The pinned Atlas report is used only to attribute the catalog identity and locator; it is not implementation evidence. [Catalog entry](../data/memory-systems.json) · [Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ctx.md)

There is no observed redirect from ActiveMemory/ctx to diegoxtr/ctx-open. The latter remains a separate repository with its own README and implementation; it is the catalog's separate `ctx-open` record and is not assessed here. The previous version of this article linked to that separate project's sources and described its .NET implementation, so those claims have been removed. [ActiveMemory/ctx](https://github.com/ActiveMemory/ctx) · [separate ctx-open README at its reviewed revision](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/README.md)

## Summary

ActiveMemory/ctx describes itself as a lightweight, file based system for coding assistants to persist, structure, and reload project context across sessions. Its documented user interface is a Go CLI that works against project-local `.context/` Markdown files; its README also describes session journal import and knowledge-base workflows. This is a source review, not a runtime or benchmark result. [README](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/README.md) · [context command reference](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/docs/cli/context.md) · [journal command reference](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/docs/cli/journal.md)

## Who and what

The official repository identifies the project as `ctx (Context)`, describes it as a file based system, and publishes Apache-2.0 as its license. Its README demonstrates task, decision, and learning commands, plus a separate knowledge-base workflow. The checked README does not establish a contact email. [README](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/README.md)

## Architecture and data model

The documented context model uses Markdown files under the current project's `.context/` directory. The command reference maps `ctx task add`, `ctx decision add`, `ctx learning add`, and `ctx convention add` to `TASKS.md`, `DECISIONS.md`, `LEARNINGS.md`, and `CONVENTIONS.md`. The README says commands operate from the project root, require a Git repository, and use `$PWD/.context/` without environment-variable or parent-directory discovery. [README](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/README.md) · [context command reference](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/docs/cli/context.md)

The README documents journal import from supported assistant session formats into editable files under `.context/journal/`. The journal reference says imports can be incremental, detect transcript growth, preserve user-edited content, and support locks for entries. These are documented behaviors, not runtime-verified results. [journal command reference](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/docs/cli/journal.md)

## Write, update, delete, and retrieval

**Write.** The CLI adds tasks, decisions, learnings, and conventions to their named Markdown files. Its documented provenance flags can attach session ID, branch, and commit metadata; decisions and learnings also require structured context fields. [context command reference](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/docs/cli/context.md)

**Update and cleanup.** The inspected reference documents task completion, archival of completed tasks, snapshots, formatting, context synchronization, and journal import protections. It does not establish a general deletion API or prove how every edit is retained. The reference describes archiving as moving completed tasks into timestamped archive files. [context command reference](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/docs/cli/context.md) · [journal command reference](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/docs/cli/journal.md)

**Retrieval.** The README's quick start uses `ctx agent --budget` to produce an AI-ready context packet. The journal command can list, filter, and show imported sessions. The inspected sources do not establish retrieval ranking quality or whether a relevant file will always be discovered. [README](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/README.md) · [journal command reference](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/docs/cli/journal.md)

**Scope and provenance.** The documented project boundary is the current working directory's Git repository and `.context/` tree. Provenance fields such as session ID, branch, and commit can accompany typed entries. A selected code inspection also found a dream write guard that restricts targets to designated paths, with a specific promotion exception; this concerns that write flow and does not establish read isolation or general repository authorization. [README](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/README.md) · [context command reference](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/docs/cli/context.md) · [dream write guard](https://github.com/ActiveMemory/ctx/blob/a0058eacc06a4e2a5423aafbdfdd927966d078ca/internal/dream/guard.go)

## Metric-domain evidence

No ctx workload, benchmark, or test was run for this review. Retrieval accuracy, abstention, correction accuracy, stale-value rate, deletion leakage, scope isolation, evidence support, latency, write-to-recall delay, token/cost efficiency, and storage efficiency remain unmeasured. Project metric definitions, the shared benchmark status record, and the planned fixture describe evaluation materials, not ctx results. [Metric definitions](../METRICS.md) · [shared benchmark status](../results/initial-baselines-status.json) · [planned fixture](../fixtures/memory-benchmark-v1.json)

## Limits and unknowns

This selected source review establishes documented file and CLI behavior plus one inspected code guard. It does not establish runtime correctness, data-loss resistance, retrieval quality, security boundaries, or measured efficiency. The README describes a local file based workflow; the checked material does not establish multi-user isolation. No contact email was found in the pinned README.

## Benchmark status

Benchmark status is **not run**. No runtime, benchmark, or test command was executed. See the project's [metric definitions](../METRICS.md), [shared benchmark status](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json) for evaluation context only.

## Sources

All implementation and documentation links below are pinned to the reviewed ActiveMemory/ctx revision. The branch feed and repository page are used only to verify repository identity, default branch, and current head. The Atlas source is attribution only.

