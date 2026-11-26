# Gini Agent source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 257 / Gini Agent / `gini-agent`  
**Listed repository locator:** [Open-Curiosity/gini-agent](https://github.com/Open-Curiosity/gini-agent)  
**Canonical upstream:** [Open-Curiosity/gini-agent](https://github.com/Open-Curiosity/gini-agent)  
**Default branch / reviewed head:** main / [6c5d85ed0ecd7fe8567124bd4890b16c329970d8](https://github.com/Open-Curiosity/gini-agent/commit/6c5d85ed0ecd7fe8567124bd4890b16c329970d8)  
**Review time:** 2026-11-25 21:01:10 UTC (2026-11-25 13:01:10 PST; America/Los_Angeles).

## Identity and review pin

The curated roster identifies Gini Agent as ordinal 257, slug `gini-agent`, with the explicit locator `https://github.com/Open-Curiosity/gini-agent`. Its Atlas attribution is recorded only for curated identity and locator context. The official GitHub repository page identifies `main` as the default branch; its latest-commit patch reports the full head SHA recorded above. The source review is pinned to that SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Gini Agent is a personal agent runtime whose Hindsight memory subsystem stores structured memory units in a per-instance SQLite database. It extracts facts from task text, associates entities and temporal data, and recalls units through semantic, lexical, graph, and temporal channels. The project describes this as a local memory implementation; this source review did not run it or measure retrieval quality.[[readme]][[memorydoc]][[db]]

## Who and what

The official README presents Gini Agent as a personal agent with a Bun runtime gateway, web and mobile clients, CLI, MCP surfaces, and messaging bridges. Memory is one subsystem of that runtime. The reviewed memory guide distinguishes Hindsight from the always-injected `USER.md` and `SOUL.md` identity surfaces; this review concerns Hindsight unless stated otherwise.[[readme]][[memorydoc]]

## Architecture and data model

The memory guide says each instance stores Hindsight data in `~/.gini/instances/<instance>/memory.db` using SQLite, while local embedding and reranking model caches live under `~/.gini/models/`. The state module defines memory banks and units, with networks for world, experience, opinion, and observation and link types for temporal, semantic, entity, and causal relations. Units include agent and bank scope, status, embedding metadata, temporal fields, source task/session identifiers, and usage metadata.[[memorydoc]][[db]]

The retain pipeline asks a configured model to extract structured facts, normalizes supported temporal expressions, embeds fact narratives, inserts units, resolves entities, and creates links. The source describes this pipeline as best-effort: failures are audited and rethrown, while the callers are expected to keep a retain failure from blocking the originating task. Reflection reuses recall to draft a response and can store extracted opinions; reinforcement assesses a bounded candidate set of opinions against new facts.[[retain]][[reflect]][[reinforce]]

## Write, update, delete, and retrieval

**Writes.** The memory guide says automatic retain runs at the end of each chat task, with CLI and API retain surfaces also available. Retain requires an `agentId`, extracts facts from supplied text, and stores source task/session and embedding metadata where provided. This review did not trace every API caller or evaluate extraction quality.[[memorydoc]][[retain]]

**Updates and correction.** The inspected retain path inserts extracted units and links; the guide describes review and pruning, but the inspected documentation and source do not establish a general fact-replacement or stale-value correction workflow. Reflection can add opinions, while reinforcement changes opinion confidence based on model-generated verdicts. These mechanisms do not by themselves demonstrate reliable correction of contradictory factual units.[[retain]][[reflect]][[reinforce]]

**Deletion.** The guide says users can prune individual units from the Memory page. I did not inspect the UI mutation implementation or verify whether pruning physically erases a unit, leaves a tombstone, or clears all derived copies and backups. Deletion semantics and post-delete leakage are therefore unknown in this review.[[memorydoc]]

**Retrieval.** Recall requires an `agentId` and combines semantic vector search, SQLite FTS5 BM25, graph spreading activation, and temporal range matching. The implementation uses reciprocal-rank fusion, reranks the top candidates, and packs results under a default 2,000-token budget. The guide says retrieval is used automatically each turn and through the `recall_memory` tool. Embeddings from another active model are excluded from semantic search until re-embedded; the guide exposes embedding status and re-embedding commands.[[recall]][[memorydoc]][[embedding]]

## Scope isolation

The guide describes one bank per agent and says memory units carry an agent identifier; recall filters each channel on that active agent. Retain and recall reject a missing `agentId`, and the recall source applies the scope before channel fusion. This is implementation evidence for the intended boundary, not an adversarial isolation result; no cross-agent workload was run for this review.[[memorydoc]][[retain]][[recall]]

## Provenance and evidence

The guide describes provenance fields for source task, source trace IDs, and embedding model, and says users can review units in the Memory page. Retain also records audit events and can append task traces; recall returns channel names and per-channel subscores intended to explain why a unit surfaced. These are lineage and diagnostic mechanisms. No retrieved answer was adjudicated against its source, so evidence support and citation quality are unmeasured.[[memorydoc]][[retain]][[recall]]

## Efficiency and observability

The implementation bounds retrieval channel candidate sets, limits graph propagation to two hops, reranks only a top-N subset, and caps the final pack by token budget. The memory guide documents local embedding/reranking defaults, provider selection, model status, cache status, and re-embedding; the embedding status code reports cache size and per-bank model counts. Retain and recall also emit audit or trace information. These are source observations, not latency, token-cost, or storage measurements.[[recall]][[embedding]][[retain]][[metrics]]

## Metric-domain evidence

All benchmark domains remain **unmeasured in this review**. The project metric definitions and fixture describe how to measure them; they are not results for Gini Agent. Gini Agent, its tests, and benchmarks were not run. See [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Four retrieval channels are implemented; no query workload was scored. | Unmeasured |
| Correction accuracy and stale values | Opinion confidence reinforcement exists; no fact correction workload was run. | Unmeasured |
| Deletion leakage | Individual-unit pruning is documented; no deletion probes were run. | Unmeasured |
| Scope isolation | Agent IDs are required and filtered in recall; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Provenance metadata and recall-channel diagnostics are described; no claims were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Candidate limits, reranking, and automatic retain/recall are documented; no timings were collected. | Unmeasured |
| Tokens, cost, and storage | Token packing and local model cache status are implemented; no resource measurements were collected. | Unmeasured |

## Limits and unknowns

This is a pinned documentation and source review, not a runtime, security, or quality assessment. It does not establish extraction accuracy, reliable contradiction resolution, end-to-end physical deletion, backup erasure, or whether every surface applies authorization identically. The temporal parser intentionally handles a limited set of supported patterns and returns no range when it cannot parse a date. Model/provider behavior and embedding configuration can affect extracted facts and recall. No tests were run as part of this task.[[memorydoc]][[temporal]][[retain]][[recall]]

## Benchmark status

**Benchmark not run.** No Gini Agent runtime, tests, or benchmark workload was executed for this review. No recall, correction, deletion, isolation, citation, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned [SECURITY.md](https://github.com/Open-Curiosity/gini-agent/blob/6c5d85ed0ecd7fe8567124bd4890b16c329970d8/SECURITY.md) publishes `security@lilaclabs.ai` for vulnerability reports. The exact checked URL is recorded in the JSON. No commit/profile metadata or third-party directory was used.[[security]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas entry is included solely as roster attribution, not assessment evidence. See the structured record [gini-agent.json](../data/system-reviews/gini-agent.json) and [curated roster](../data/memory-systems.json).
