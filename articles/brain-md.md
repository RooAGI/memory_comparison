# brain.md

## Identity and review pin

- **System:** brain.md
- **Curated position:** 100
- **Slug:** `brain-md`
- **Listed repository:** [mindmuxai/brain.md](https://github.com/mindmuxai/brain.md)
- **Canonical repository at review:** [mindmuxai/brain.md](https://github.com/mindmuxai/brain.md)
- **Default branch:** `main`
- **Reviewed head:** [`02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6`](https://github.com/mindmuxai/brain.md/commit/02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6)
- **Reviewed:** 2026-11-25 00:01:10 UTC (16:01:10 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brain-md.md), used only for identity, listed repository, and source attribution.

The curated roster places brain.md at position 100 with slug `brain-md` and the listed repository locator above.[[catalog]] Its Atlas source is recorded only for attribution; Atlas descriptions, marks, and layout were excluded from this assessment.[[atlas]] The official GitHub page identifies `main` as the default branch, and the official main commit feed identifies full head `02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6`, which matches the repository page's latest commit.[[repo]][[head-feed]]

## Summary

brain.md is a repository-native memory toolkit for coding agents. It uses Markdown files plus a small Node.js CLI to store durable project knowledge, with explicit commands for reading, writing, revising, indexing, and archiving pages.[[readme]][[cli]][[library]]

## Who and what

The repository is maintained under the MindMux organization; its README describes brain.md as led and incubated by MindMux. It is a CLI and set of agent skills/protocol files rather than a hosted memory service. The data lives in a project's repository or a configured sidecar directory.[[repo]][[readme]][[skill]]

## Architecture and data model

**Source observations.** The `brain` CLI is implemented as a zero-dependency Node.js ESM script. A shared library resolves the brain directory from `.mindmux/preferences.json`'s optional `brainRoot`, relative to the project root when needed, and otherwise uses `./brain`. The directory contains an auto-generated index, six fixed root-page slots, and `pages/<id>.md` records.[[cli]][[library]][[skill]]

A page has generated frontmatter (including ID, category, title, status, timestamps and optional tags/source), a rewritable `compiled_truth` section, and a visible timeline of typed entries such as decision, evidence, reversal, or note. The root-page slots cover background, architecture, flow, mindmap, stack, and roadmap; root pages have no timeline and rely on Git history for revision history.[[cli]][[skill]][[readme]]

The CLI and companion skills define the operating protocol. Agent configuration files can be wired with a marked instruction block; optional Claude Code and Codex SessionStart hooks add a page listing to session context. The README describes the brain as agent-agnostic because the shared contract is Markdown and a `BRAIN.md` instruction file.[[readme]][[skill]][[cli]]

## Write, update, delete, and retrieval

**Create and update.** `create-page` validates a kebab-case page ID, writes generated frontmatter and a starter timeline entry, then rebuilds the index. `update-truth` replaces the current-truth section and appends a decision entry in one atomic file replacement, so a CLI truth rewrite cannot omit its corresponding timeline entry. `append-timeline` adds a typed entry; `set-tags` changes tags; `archive-page` marks a page archived and can append a reversal entry. Six root pages can be written through `update-root`, which also updates the index. Existing timeline entries are not rewritten by these commands.[[cli]][[library]][[skill]]

**Delete.** The current CLI command list and operating manual provide no page-delete or timeline-delete command. Archiving changes lifecycle status but does not erase page contents. The README says uninstalling the toolkit does not touch project brain data. The inspected source therefore establishes an archive path, not a deletion or secure-erasure guarantee; it does not establish the behavior of manually deleting files or removing them from Git history.[[cli]][[skill]][[readme]]

**Retrieval.** `list-pages` returns page IDs, titles, categories, and statuses; `read-page` returns a selected page and `read-root` reads a selected root page. `reindex` rebuilds the generated index, whose entries summarize pages with their first compiled-truth sentence; `lint-links` checks current-truth and root-page wiki-links. Retrieval is explicit by listing and page ID, not semantic or embedding search. The SessionStart integration supplies a listing snapshot, while page bodies are loaded on demand.[[cli]][[library]][[skill]][[readme]]

## Scope isolation

A brain is selected by the invoking project root and can be redirected to a repository sidecar with `brainRoot`. This gives projects separate physical directories when configured, but the inspected record format has no tenant or user scope field and the CLI's separation is not an authorization boundary. The Codex hook command embeds an absolute project path, so the operating manual instructs users to reinstall after moving a project or using another clone/worktree. No cross-project or cross-user isolation workload was run.[[library]][[skill]][[readme]]

## Provenance and evidence

Timeline entries preserve caller-provided summaries, kinds, optional source strings, and affected page IDs alongside the current truth. The CLI appends the history during truth updates and does not rewrite prior entries through its timeline commands. Root-page history instead relies on Git. This provides a human-readable change narrative, but the inspected schema does not require claim-level citations, evidence excerpts, confidence, or independent review. The project's own documentation cautions that manual edits bypass CLI invariants; therefore the CLI's append-only behavior is not tamper-proof immutability.[[cli]][[library]][[skill]][[readme]]

## Source-visible efficiency and observability

**Code observations, not measurements.** Page mutations synchronously rebuild the generated index, and link linting is an explicit check. Reads list metadata or load selected Markdown pages; no vector store, embedding pipeline, or background retrieval service was found in the inspected CLI and library. The optional Codex hook emits at most 8 KiB of complete listing rows and tells the agent to request the full list when truncated. The README documents a five-second Codex hook limit; the Claude Code branch is described as unbounded listing output. These are documented/source-level bounds, not measured latency or token savings.[[cli]][[library]][[skill]][[readme]]

The reviewed code exposes no operational metrics for retrieval quality, latency, tokens, cost, or storage efficiency. Git provides repository-level history for files, and command failures print errors, but neither is an adjudicated performance or reliability result.[[cli]][[library]]

## Metric-domain evidence

Every domain below is **unmeasured for this review**. The table records source-visible mechanisms only.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Explicit page listing and ID-based reads; no semantic retrieval or answerability evaluation inspected. | Unmeasured |
| Correction accuracy and stale values | Truth rewrite is paired with a timeline entry; no correction or stale-value probe was adjudicated. | Unmeasured |
| Deletion leakage | Archive exists; no deletion command or post-deletion leakage evaluation was found. | Unmeasured |
| Scope isolation | Project-root/sidecar directory selection is visible; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Timeline accepts source strings, but claim-level citations are not required by the inspected model. | Unmeasured |
| Latency and write-to-recall delay | Index rebuild and bounded Codex snapshot are source-visible; no timing was collected. | Unmeasured |
| Tokens, cost, and storage | Markdown files and hook snapshot bounds are visible; no token, price, or storage measurements were collected. | Unmeasured |

The [project metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) describe measurement domains and planned reporting; they are not brain.md results.[[metrics]][[fixture]][[status]]

## Limits and unknowns

This is a read-only review of selected official documentation and code at the pinned head. It does not establish how reliably agents capture useful facts, whether readers find the right page, how stale beliefs are corrected in practice, or how Git history and backups affect erasure. It also does not establish behavior under concurrent edits, large brains, all agent integrations, or non-POSIX environments.[[readme]][[cli]][[library]][[skill]]

The source describes the CLI's invariants as correct-by-construction, but also says manual edits are unsupported and can silently break those invariants. The review did not execute the CLI or its tests, so it makes no runtime claim about those guarantees.[[readme]][[skill]]

## Benchmark status

**Benchmark not run.** I did not execute brain.md, a benchmark workload, or tests. Project metric definitions and the versioned fixture describe evaluation plans; the project-wide execution status is not a brain.md result.[[metrics]][[fixture]][[status]]

## Contact-list follow-up

I checked the official pinned [README](https://github.com/mindmuxai/brain.md/blob/02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6/README.md) and the official repository's [SECURITY.md path](https://github.com/mindmuxai/brain.md/blob/02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6/SECURITY.md). The README does not publish a contact email, and SECURITY.md is absent at the reviewed revision. The JSON records null and both checked source URLs.

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed repository, and Atlas attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brain-md.md) — identity and source attribution only.
- [Official repository](https://github.com/mindmuxai/brain.md) — canonical repository and default branch.
- [Official main commit feed](https://github.com/mindmuxai/brain.md/commits/main.atom) — current main head at review time.
- [Reviewed head](https://github.com/mindmuxai/brain.md/commit/02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6)
- [README](https://github.com/mindmuxai/brain.md/blob/02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6/README.md)
- [Brain CLI](https://github.com/mindmuxai/brain.md/blob/02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6/skills/brain-page/bin/brain.mjs)
- [Shared brain library](https://github.com/mindmuxai/brain.md/blob/02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6/skills/brain-page/lib/brain.mjs)
- [Brain page operating manual](https://github.com/mindmuxai/brain.md/blob/02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6/skills/brain-page/SKILL.md)
- [Security policy path checked](https://github.com/mindmuxai/brain.md/blob/02e77c3bb5ca3a5e51130af03f43d4bc5723c6a6/SECURITY.md) — not found at review time.
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only source review; no brain.md execution, benchmarks, or tests.
