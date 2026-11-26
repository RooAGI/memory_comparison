# FAVA Trails source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 235 / FAVA Trails / `fava-trails`  
**Listed repository locator:** [MachineWisdomAI/fava-trails](https://github.com/MachineWisdomAI/fava-trails)  
**Canonical upstream:** [MachineWisdomAI/fava-trails](https://github.com/MachineWisdomAI/fava-trails)  
**Default branch / reviewed head:** main / [aff22ae2eb3b0b032fa7c75c9a4d9afadf742dd8](https://github.com/MachineWisdomAI/fava-trails/commit/aff22ae2eb3b0b032fa7c75c9a4d9afadf742dd8)  
**Review time:** 2026-11-25 20:17:13 UTC (2026-11-25 12:17:13 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists FAVA Trails at ordinal 235 with slug `fava-trails`, an explicit repository locator, and a pinned Agent Memory Atlas roster attribution. The catalog and Atlas record establish roster identity and locator only; Atlas descriptions and capability marks are not assessment evidence. The official GitHub repository metadata reports canonical repository MachineWisdomAI/fava-trails and default branch main; the official commits/main API reports current full head aff22ae2eb3b0b032fa7c75c9a4d9afadf742dd8. Assessment claims below are tied to files pinned to that SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

FAVA Trails is an MCP memory server for reviewed agent decisions and observations. It stores each thought as Markdown with YAML frontmatter in a separate data repository managed with Jujutsu alongside Git. Drafts remain private to their configured authoring identity; approved, current records are the default shared recall view. Search is lexical substring matching, not semantic retrieval.[[readme]][[models]][[governance]][[retrieval]]

## Who and what

The official README describes FAVA Trails as an open-source agent memory system by Machine Wisdom AI. The engine repository contains the MCP server and related code, while the operator's separate data repository contains the durable trail records. The review attributes the project to the organization named in upstream documentation and does not infer individual maintainer identity from commit or profile metadata.[[readme]][[repo]]

## Architecture and data model

The engine process coordinates MCP calls, a TrailManager per trail, typed thought models, lifecycle hooks, and a Jujutsu backend. Durable thought content lives outside the engine in Markdown files, grouped by trail scope and namespace; Jujutsu colocates with Git so the data repository remains Git-compatible. Optional hooks can run around save, promotion, and recall, and optional protocols add processing to those lifecycle points.[[readme]][[trail]][[models]]

A thought has a ULID-like identifier, optional parent and supersession links, authoring agent ID, bounded confidence, source type, lifecycle status, creation time, typed relationships, and project/branch/tags/extra metadata. The six statuses are draft, proposed, approved, rejected, error, and tombstoned. These are record fields; their presence alone does not establish factual correctness or an effective deletion guarantee.[[models]]

## Write, update, delete, and retrieval

**Write and review.** The documented flow saves a draft under drafts/, then propose_truth sends it to the configured Trust Gate or records explicit operator approval on an operator-controlled endpoint. A successful approval promotes it to an appropriate namespace such as observations or decisions. A model review is recorded as advisory; the project says the reviewer has limited context and does not verify project facts. A rejected draft is frozen and revised by creating a new draft whose parent points to it.[[readme]][[governance]][[models]]

**Update and correction.** update_thought edits mutable records in place, preserving frontmatter, but refuses approved, rejected, tombstoned, and already superseded records. Corrections to approved knowledge therefore use supersede: the new record starts as a draft, and the old record remains current unless and until the replacement is approved. Approval then records the successor link so default recall selects the approved current record while history retains lineage. Supersession records replacement, not truth.[[trail]][[governance]][[readme]]

**Delete and forget.** The inspected README and governed-recall guide do not document a user-facing content deletion operation. The model includes a tombstoned state, but the reviewed TrailManager forget method abandons a Jujutsu revision; this does not establish logical deletion or erasure of a thought across working files, repository history, backups, or remotes. Content deletion and its guarantees remain unknown from the inspected interface and source paths.[[models]][[trail]][[governance]]

**Retrieval.** recall and get_thought share visibility rules. Governed mode returns approved records without an approved successor; authoring mode is limited to the configured process identity's drafts/proposals; history mode requires an operator-controlled endpoint and can include selected statuses and superseded records. Query matching lowercases and splits on whitespace, then requires every token to occur as a substring of the searchable text. Synonyms and paraphrases can miss; an empty query returns visibility-allowed records up to the limit.[[governance]][[retrieval]][[readme]]

## Scope isolation

Trail names, namespaces, and metadata scopes narrow selection; they do not grant access. The server derives authoring identity and operator authority from process configuration, not tool arguments. Upstream explicitly warns that one shared MCP endpoint or shared data filesystem is one identity boundary, not per-caller isolation; separate authenticated processes/endpoints are needed for independent authoring identities. This documents intended filtering and deployment boundaries, not an independently tested isolation guarantee.[[governance]][[readme]]

## Provenance and evidence

Frontmatter records author identity, source type, confidence, lifecycle status, timestamps, parent/supersession links, relationships, and project metadata. Jujutsu version history preserves changes, and approval metadata distinguishes an advisory model result from explicit operator approval. These provide authorship and change lineage, but the reviewer does not independently fact-check a candidate, compare it against existing records, or guarantee an approved claim is true. The reviewed sources do not establish a general citation mechanism binding factual claims to external source passages.[[models]][[governance]][[readme]]

## Efficiency and observability

The implementation uses an asyncio lock per trail, snapshots the Markdown records for a consistent read view, and can garbage-collect the Jujutsu repository. Lexical matching is simple to inspect but does not provide semantic recall or ranking. Lifecycle hooks can observe or transform save, promotion, and recall events. Documentation also describes version/runtime diagnostics and reviewer-destination reporting. No latency, token, cost, corpus-scale, or storage measurements were collected in this review.[[trail]][[governance]][[readme]]

## Metric-domain evidence

All project metric domains are **unmeasured** for FAVA Trails in this review. Code and documentation observations are not benchmark results. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define evaluation protocols and project status, not FAVA Trails measurements.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Governed lexical retrieval and visibility filters inspected; no answers scored. | Unmeasured |
| Correction and stale values | Approved successor rules inspected; no correction probes run. | Unmeasured |
| Deletion leakage | No content deletion path or post-delete probe was verified. | Unmeasured |
| Scope isolation | Process identity and view filtering inspected; no cross-scope workload run. | Unmeasured |
| Evidence support and citation coverage | Approval and lineage metadata inspected; no output claims adjudicated against sources. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timings collected. | Unmeasured |
| Tokens, cost, and storage | No workload usage or persistent-storage measurements collected. | Unmeasured |

## Limits and unknowns

This is a source review at a verified current main SHA, not a runtime, security, or operational audit. The README cautions that main may be ahead of the installed package, so installed-version behavior must be checked separately. The reviewer is a quality-control gate with limited context, not factual verification. Shared endpoints and filesystems are operator trust boundaries. Retrieval misses paraphrases and synonyms. The inspected API and sources do not establish content erasure semantics, deletion from repository history or remote copies, or cross-scope isolation under adversarial deployment. No system runtime, tests, or benchmarks were run.[[readme]][[governance]][[trail]][[retrieval]]

## Benchmark status

**Benchmark not run.** No FAVA Trails runtime, tests, or benchmark workload was executed. No quality, latency, token, cost, storage, deletion, correction, or isolation measurement is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json); these describe evaluation protocol and status, not FAVA Trails results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and official project website were checked for a published contact email. Neither publishes an address; the structured record stores contact_email as null and records both exact checked URLs. No commit/profile metadata, third-party directory, or inferred address was used.[[readme]][[website]]

## Sources

Upstream code and documentation citations are pinned to the verified full SHA. The Atlas URL is retained only as roster attribution and is not assessment evidence. See the structured record [fava-trails.json](../data/system-reviews/fava-trails.json) and [curated roster](../data/memory-systems.json).
