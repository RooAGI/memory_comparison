# Helm source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 288 / Helm / `helm`  
**Listed repository locator:** [GOODMAN-PRO/helm](https://github.com/GOODMAN-PRO/helm)  
**Canonical upstream:** [GOODMAN-PRO/helm](https://github.com/GOODMAN-PRO/helm)  
**Default branch / reviewed head:** main / [f453eaa9683ea0a66b45c76275cb6576bcf14f73](https://github.com/GOODMAN-PRO/helm/commit/f453eaa9683ea0a66b45c76275cb6576bcf14f73)  
**Review time:** 2026-11-25 22:43:47 UTC (2026-11-25 14:43:47 PST; America/Los_Angeles).

## Identity and review pin

The project catalog resolves ordinal 288 to Helm (`helm`) and lists the explicit locator `https://github.com/GOODMAN-PRO/helm`. Its pinned Atlas entry is retained as roster attribution only and is not evidence for this assessment. The official GitHub repository page identifies `main` as the default branch. GitHub's official commits API reports full head SHA `f453eaa9683ea0a66b45c76275cb6576bcf14f73`; a shallow checkout of the upstream repository resolved the same branch and SHA. The source review below is pinned to that head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Helm is a self-hosted personal agent whose structured memory is a local SQLite database containing keyed facts and conversation episodes. Its command-line and registered tools write facts and retrieve them with lexical ranking blended with local TF-IDF or, when a cached model is available, MiniLM embeddings. Periodic reflection and consolidation can turn repeated episode terms into learned facts and age out weak, single-evidence facts. This review describes source behavior; runtime quality and performance remain unmeasured.[[readme]][[memory]][[embed]][[consolidate]][[think]]

## Who and what

The official README presents Helm as an open-source personal agent running on the user's hardware, connected to Discord and optionally iMessage and a terminal. The reviewed structured-memory component is part of the repository's Node workspace and uses Node's built-in SQLite API; the README also describes a separate Helm Mind Markdown knowledge base. Detailed Helm Mind internals were not reviewed here, so its claims are not attributed to the structured-memory implementation.[[readme]][[memory]][[claude]]

## Architecture and data model

The structured store opens `workspace/memory/memory.db`. Its `facts` table stores an integer ID, kind, key, value, optional source, confidence, created/updated timestamps, evidence count, last-seen time, validity start, expiry timestamp, and access count. A partial unique index permits one active fact per (kind, key) while retaining expired rows. `episodes` stores timestamp, channel, summary, and optional raw reference; a `links` table exists, although the inspected CLI paths do not use it. Embedding vectors are lazily stored in a separate `vectors` table, and optional episode vectors use `episode_vectors`.[[memory]][[embed]]

The `memory.mjs` CLI implements remember, recall, unsure, forget, dump, history, and episode operations. Registered `memory.remember` and `memory.recall` tools delegate to that CLI. A separate refresh script exports current facts and recent episodes to a generated Markdown index. The agent's scheduled think process performs periodic reflection and invokes weekly consolidation; those background jobs are distinct from direct memory-tool writes.[[memory]][[tools]][[tool-recall]][[registry]][[index]][[think]][[consolidate]]

## Write, update, delete, and retrieval

**Write and correction.** `remember <kind> <key> <value>` inserts a fact or updates an existing active row. Repeating the same value increments evidence count and updates source, confidence, and timestamps. A changed value expires the prior row and inserts a new row, preserving the old value for `history`; active recall excludes expired rows. For `--source observed` without `--force`, first-observation confidence is capped at 0.7, with a small step-up ceiling on repeated observations. The CLI accepts confidence values directly for other source modes; the inspected path does not validate independent evidence or confidence ranges.[[memory]][[claude]]

**Episodes and consolidation.** The episode command appends timestamped summaries with optional channel and raw reference. Weekly consolidation tokenizes recent episode summaries, turns terms repeated across at least three episodes into `learned` facts, decays stale facts with fewer than two observations, and prunes those below a confidence floor. Facts sourced from `CLAUDE.md` are excluded from decay and prune. Consolidation also deduplicates active (kind, key) rows. These heuristics describe the implementation, not the quality of the generated memories.[[memory]][[consolidate]][[think]]

**Delete.** `forget <id>` hard-deletes one fact and attempts to delete its associated fact vector; it does not delete episodes. Consolidation also physically deletes eligible low-confidence and duplicate rows. The reviewed paths do not establish secure erasure from SQLite journals, filesystem backups, generated indexes, or other copies. Changing a fact's value is implemented as expiry plus insertion, rather than deletion of its history.[[memory]][[consolidate]][[index]]

**Retrieval.** Recall considers up to the 500 most recently updated active facts. It tokenizes and stems query and fact text, computes BM25, and, unless keyword-only mode is selected, fuses BM25 and cosine ranks with reciprocal-rank fusion; confidence and key-match boosts affect ranking. Cosine uses cached MiniLM vectors only when the model is already locally available; otherwise the current path falls back to TF-IDF cosine. The implementation silently catches embedding failures. Optional episode recall separately searches up to the 500 newest episodes and ranks by BM25, optional embedding similarity, and recency. Returned facts increment access_count. Results are bounded by a caller-supplied limit, but no explicit abstention threshold is applied to fact results.[[memory]][[embed]][[tools]]

## Scope isolation

The database path is fixed relative to the workspace's memory module. Fact rows have no user, project, session, or tenant key; episodes have a channel field, but fact recall is not filtered by channel. The Discord gateway rejects messages not authored by the configured owner before dispatch, which is a product-level owner boundary. It is not isolation implemented inside the database or retrieval API; deployments that share a workspace/database should not assume per-user separation from these inspected paths.[[memory]][[index]][[gateway]]

## Provenance and evidence

Fact rows retain a free-form source label, confidence, evidence count, and timestamps; episodes retain channel and optional raw_ref. The README prompt instructs the agent to use `source observed` for owner preferences, but source values are labels rather than validated links to source passages. Repeated identical values increase evidence count without checking independence or truth. The schema and inspected retrieval output do not expose a general citation or evidence-span mechanism, so stored provenance metadata does not itself establish factual support.[[memory]][[claude]][[readme]]

## Efficiency and observability

SQLite and local vector caches avoid a required remote memory service. Retrieval scans the newest 500 active facts and computes BM25/TF-IDF ranking in process; cached MiniLM can add local inference work. The code has a `--keyword-only` option, configurable result limits, and consolidation's dry-run mode. The generated index reports fact/episode counts, while consolidation prints counts of distilled, decayed, pruned, and deduplicated rows; think logs tick and consolidation status. These provide operational signals, not measured performance or recall quality. No latency, token, cost, storage, or workload-scale measurements were collected.[[memory]][[embed]][[index]][[consolidate]][[think]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Helm in this review. Code observations do not substitute for results. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the evaluation protocol and shared status, not Helm results.[[metrics]][[fixture]][[status]]

| Domain | Code evidence | Status |
|---|---|---|
| Answerable retrieval and abstention | Ranked fact/episode recall inspected; no answerability or abstention cases scored. | Unmeasured |
| Correction and stale values | Changed-value supersession and history behavior inspected; no correction probes run. | Unmeasured |
| Deletion leakage | Fact deletion exists; episode deletion and copy erasure are not established; no post-delete probes run. | Unmeasured |
| Scope isolation | Owner gate is in the Discord gateway; the database schema has no principal or project key; no cross-scope workload run. | Unmeasured |
| Evidence support and citation coverage | Source labels and evidence counters exist, but no claims were checked against stored source passages. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings collected. | Unmeasured |
| Tokens, cost, and storage | Local SQLite and optional embeddings inspected; no workload token, cost, or storage measurements collected. | Unmeasured |

## Limits and unknowns

This is a source review of the open repository at a verified current head. Helm, its tests, and its benchmarks were not run. The README's product descriptions do not establish operational reliability, privacy outcomes, or quality. The reviewed structured-memory paths do not establish episode deletion, secure erasure from side files/backups, caller-level tenant isolation, correctness of confidence values, or evidence entailment. Detailed Helm Mind behavior, database backup lifecycle, and runtime measurements are outside the inspected scope.[[readme]][[memory]][[consolidate]][[claude]]

## Benchmark status

**Benchmark not run.** No Helm runtime, tests, or benchmark workload was executed. No retrieval accuracy, abstention, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) are protocol and status references, not Helm results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and the official website linked from it were checked for a published contact email; neither published one. The structured record stores `contact_email: null` and records both exact checked URLs. No commit/profile metadata, third-party directory, or inferred address was used.[[readme]][[website]]

## Sources

All upstream file citations are pinned to full SHA `f453eaa9683ea0a66b45c76275cb6576bcf14f73`. The Atlas URL is roster attribution only, not assessment evidence. See the structured review record [helm.json](../data/system-reviews/helm.json) and the [curated roster](../data/memory-systems.json).
