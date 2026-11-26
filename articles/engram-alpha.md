# Engram Alpha

## Identity and review pin

- **Catalog position:** 223, “Engram Alpha”; slug `engram-alpha`.
- **Listed repository:** [techtheist/engram](https://github.com/techtheist/engram); roster status is explicit. The pinned Atlas attribution is used only for roster identity and locator context.
- **Canonical upstream:** [techtheist/engram](https://github.com/techtheist/engram), default branch `main`. The official Git remote reports `HEAD -> refs/heads/main` at `f816646eb85531012e95b26d27eef76dd894db86`; a fresh shallow checkout of `main` resolved to the same full SHA. GitHub REST API access was rate-limited during this review.
- **Reviewed:** 2026-11-25 19:24:12 UTC (2026-11-25 11:24:12 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) supplies ordinal, name, slug, listed repository, and roster attribution. The pinned [Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/engram-alpha.md) supports that attribution only; it is not assessment evidence.

## Summary

Engram Alpha is a local-first graph memory for software projects, exposed through an MCP and HTTP core, CLI, IDE extensions, and a web pane. It stores typed nodes and relations in one graph file per project, then serves hybrid keyword/vector retrieval with graph context, trust and confidence signals. This is a source review; no runtime or benchmark was executed.

## Who and what

The official [README](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/README.md) describes Engram Alpha as a local graph memory shared by coding assistants, with Rust core crates, a Vue/TypeScript pane, and JetBrains, VS Code, and Claude Code integrations. The README identifies the project as “built on reproducible research”; this review does not infer an individual maintainer identity.

## Architecture and data model

The Rust workspace separates the reusable core, MCP server, HTTP server, CLI, and evaluation program. Its core schema stores typed nodes with text, source/session, temporal validity, tags, code references, custom fields, and trust timestamps; edges connect nodes through configured verbs. A suspects queue supports conflict review, while tasks are stored separately and are excluded from memory search. The mutation journal stores before/after snapshots and writer context.[[workspace](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/Cargo.toml)] [[schema](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/schema.rs)] [[types](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/types.rs)]

The README describes TepinDB as the current self-describing graph file, with SQLite retained for migration and an interchangeable store interface. The core also uses local embedding, reranking, and NLI components when configured; the project docs describe these as swappable local models. This is architecture documented by the project, not a measurement of resource use.[[readme](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/README.md)] [[storage guide](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/docs/storage.md)] [[core crate](https://github.com/techtheist/engram/tree/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src)]

## Write, update, delete, and retrieval

**Write and update.** The checked write path embeds a proposed note, looks for a same-type current near-duplicate, and either returns a match for caller-side merging or creates the node and returns warnings/suspect pairs. Writes can nominate duplicates or conflicts; the model/NLI checks do not themselves approve a judgment. Node updates validate configured types and fields and are journaled. User-authored notes begin approved; agent-authored notes await review, according to the memory model docs.[[write path](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/engine/write.rs)] [[node operations](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/engine/nodes.rs)] [[memory model](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/docs/memory-model.md)]

**Supersession and deletion.** A replacement archives the old node behind a `replaces` relation, preserving history while excluding it from current retrieval. Explicit hard deletion can create a Tombstone carrying the removed title/text and reason; a later similar write can receive a tombstone warning. The code also exposes direct deletion, which removes the node and connected edges; the review did not establish secure erasure from backups or storage media. Merge operations can rehome edges and archive merged-away nodes.[[node operations](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/engine/nodes.rs)] [[merge](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/engine/merge.rs)] [[recall and capture](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/docs/recall-and-capture.md)]

**Retrieval.** Search fuses keyword and vector results, optionally reranks candidates, applies configured delivery thresholds and session diversity, attaches one-hop neighbors (including conflicts and supersessions), and stamps returned hits for observability. Time windows can use capture time or configured event-date fields. Confidence is reported as none/weak/strong when a calibrated reranker is available; without one, nonempty results have no calibrated confidence verdict. These are code and documentation observations; retrieval quality and latency were not measured here.[[search](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/engine/search.rs)] [[recall and capture](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/docs/recall-and-capture.md)]

## Scope isolation

The registry maps project roots to separate graph files; the hub binds a session to one project, can read the home graph, and supports read-only cross-project search/claim checks with project provenance on foreign hits. The core can therefore reach more than the current project when configured for it. The source review found project routing and separate stores, but did not establish OS-level authorization between local users or security against a compromised local process.[[registry](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/registry.rs)] [[hub federation](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/hub/federation.rs)] [[multi-project guide](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/docs/multi-project.md)]

## Provenance and evidence

Nodes retain a source category and session identifier; audit rows record mutation action, entity snapshots, front-end origin, session, working directory, process, and version. Search hits include neighboring graph relations and standing indicators such as contested, superseded, stale, or tombstone. These provide traceability and context, but do not prove that a note is correct or that an assistant cited it faithfully.[[schema](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/schema.rs)] [[audit log](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/engine/audit_log.rs)] [[types](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/types.rs)]

## Efficiency and observability

Code observations include FTS indexing, vector retrieval, bounded reranker candidate fetch, result limits, and one-hop context attachment. The schema and search path track `last_seen` on returned hits for observability; policy comments explicitly keep exposure separate from trust. The README and docs report project benchmark outcomes, but these were not independently rerun or adopted as this review's measurements. No latency, token, cost, storage-efficiency, or operational-load result was collected here.[[schema](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/schema.rs)] [[search](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/crates/engram-core/src/engine/search.rs)] [[readme](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/README.md)]

## Metric-domain evidence

- **Answerable retrieval and abstention:** the source exposes confidence verdicts and the project describes negative-question evaluation. This review ran no answerability or abstention workload.
- **Correction and stale values:** supersession, conflict review, trust/decay, and temporal fields are present in source. Correction accuracy and stale-value rate remain unmeasured here.
- **Deletion leakage:** hard delete and tombstone paths are source-inspected; no residual-read or secure-erasure probe was run.
- **Scope isolation:** project-specific graph routing and optional cross-project reads are visible in source; no isolation workload was run.
- **Evidence support and citation coverage:** source/session lineage, audit context, graph relations, and standing are present; answer support precision and citation coverage were not scored.
- **Retrieval latency and write-to-recall delay:** not measured.
- **Tokens, cost, and storage efficiency:** not measured.

See the project's [metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and [benchmark fixture](../fixtures/memory-benchmark-v1.json). These project comparison documents are not Engram measurements.

## Contact

No contact email was found in the official pinned [README](https://github.com/techtheist/engram/blob/f816646eb85531012e95b26d27eef76dd894db86/README.md). The exact checked URL is recorded in [engram-alpha.json](../data/system-reviews/engram-alpha.json); no commit/profile metadata or third-party directory was used.

## Limits and unknowns

This is a source review at the verified `main` head. Engram Alpha, its tests, and benchmarks were not run. The review cannot establish retrieval quality on live projects, actual user-facing abstention, secure erasure, access control against other local processes, model quality, scaling, or real-world latency and cost. GitHub's REST API was rate-limited during metadata verification; the official Git remote and shallow checkout agreed on branch and full head SHA.

## Benchmark status

**Benchmark not run.** No Engram Alpha runtime, tests, or benchmarks were run. See the [project metrics](../METRICS.md), [shared status](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and SHA-pinned upstream links are recorded in [engram-alpha.json](../data/system-reviews/engram-alpha.json). The [curated roster](../data/memory-systems.json) and [pinned Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/engram-alpha.md) support identity and locator context only.
