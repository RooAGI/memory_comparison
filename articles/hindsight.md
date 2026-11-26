# Hindsight source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 296 / Hindsight / `hindsight`  
**Listed repository locator:** [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)  
**Canonical upstream:** [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)  
**Default branch / reviewed head:** main / [00c9d19e2d9386a54d84a9a12b9fc385df7009e1](https://github.com/vectorize-io/hindsight/commit/00c9d19e2d9386a54d84a9a12b9fc385df7009e1)  
**Review time:** 2026-11-25 23:04:21 UTC (2026-11-25 15:04:21 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Hindsight at ordinal 296 with the explicit locator `https://github.com/vectorize-io/hindsight`. Its Atlas attribution is recorded only to explain roster identity and locator; it is not assessment evidence. GitHub identifies `main` as the default branch, and its official `main.atom` feed reports full current head `00c9d19e2d9386a54d84a9a12b9fc385df7009e1`, updated 2026-11-25T17:22:18Z. This review is pinned to that SHA. [[catalog]][[atlas]][[repo]][[head]]

## Summary

Hindsight is a service and SDK for agent memory. It retains inputs into a bank, retrieves them through semantic, keyword, graph, and temporal search, and offers a deeper reflect operation. The upstream describes derived observations and mental models that are refreshed as the bank learns. This is a source review; it makes no runtime-quality or performance claim. [[readme]][[retain]][[retrieval]]

## Who and what

The official README presents Hindsight as “Agent Memory That Learns,” built by Vectorize.io. It can run as a self-hosted API service, an embedded Python service, or Hindsight Cloud, and exposes SDK, REST, and MCP integrations. [[readme]]

## Architecture and data model

Memory is organized into banks described as isolated stores for a user, agent, or project. The README describes four memory forms: world facts, experiences, evidence-backed observations, and mental models; retained inputs are represented through entities, relationships, and time series, with sparse and dense search representations. [[readme]]

The current retain pipeline is split into modules for content/chunk handling, fact extraction and storage, entity processing, embeddings, link creation, and orchestration. The orchestrator also tracks operation/document checkpoints and memory-defense decisions. [[retain]]

## Write, update, delete, and retrieval

**Write.** The public `retain` operation accepts content and optional context and timestamp. The documented pipeline uses an LLM to extract facts, temporal data, entities, and relationships, then normalizes these into canonical entities, time series, and search indexes. The README describes routing new inputs through world-fact or experience pathways. [[readme]][[retain]]

**Update and correction.** The README says observations consolidate related facts into deduplicated beliefs with supporting evidence and exact quotes; new evidence can strengthen, weaken, or extend an observation rather than silently overwriting it. The inspected sources do not establish a general direct-update API or the behavior for every explicit correction workflow. [[readme]][[retain]]

**Delete.** The sources inspected for this review do not establish the memory-item deletion API, retention of derived observations after deletion, or erasure from backups and external indexes. Deletion behavior is therefore unknown here. [[readme]][[retain]]

**Retrieval.** Recall runs semantic, BM25 keyword, graph, and temporal retrieval strategies in parallel. The implementation describes the dispatcher as passing all four arms to the memory store; PostgreSQL SQL shown in the reviewed source scopes the BM25 arm by `bank_id`. Results are fused with reciprocal-rank fusion, reranked by a cross-encoder, and trimmed to a token limit per the README. Reflect performs a deeper analysis rather than ordinary lookup. [[retrieval]][[sql]][[readme]]

## Scope isolation

The README describes each bank as an isolated memory store and states that banks do not leak across one another. In the inspected PostgreSQL retrieval source, the BM25 SQL arm requires a `bank_id` predicate. This supports bank-level query scoping in the reviewed path; this task did not exercise runtime behavior or inspect every backend and endpoint. [[readme]][[sql]]

## Provenance and evidence

The README describes observations as retaining exact supporting quotes and a proof count, with later evidence refining existing beliefs. The reviewed retain orchestrator includes operation events and observation-change tracking in its imports and pipeline. Those structures provide provenance-related evidence, but this inspection does not establish that extracted claims are true or that generated answers are fully supported by the cited source material. [[readme]][[retain]]

## Efficiency and observability

The README and retrieval dispatcher describe four parallel retrieval arms followed by rank fusion and cross-encoder reranking. The README documents PostgreSQL with pgvector or Oracle AI Database storage and Prometheus monitoring for model calls, tokens, and latency. These are architecture and observability descriptions, not measurements from this review. [[readme]][[retrieval]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Hindsight in this review. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the project protocol and status, not Hindsight results. [[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Four retrieval arms, fusion, reranking, and reflect are documented; answer correctness and abstention were not scored. | Unmeasured |
| Correction and stale values | The README describes evidence-based observation refinement; no correction sequence was tested, and direct correction semantics remain partly unknown. | Unmeasured |
| Deletion leakage | Deletion and post-delete behavior were not established by the inspected sources; no deletion probe was run. | Unmeasured |
| Scope isolation | Bank isolation is documented and the inspected PostgreSQL BM25 arm filters by bank; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Observations are described with exact supporting quotes and proof counts; no answer was adjudicated against retained evidence. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings were collected. | Unmeasured |
| Tokens, cost, and storage efficiency | Monitoring and storage backends are documented; no token, cost, or storage workload was measured. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the official README, SECURITY policy, retain orchestrator, retrieval dispatcher, and PostgreSQL retrieval SQL at the verified head. Hindsight, its tests, and benchmarks were not run. The inspection does not establish actual recall accuracy, abstention quality, end-to-end isolation, deletion completeness, correction success, or production performance. [[readme]][[retain]][[retrieval]][[sql]]

The reviewed paths do not resolve all deletion semantics, every backend's scope enforcement, backup erasure, or how each derived memory type responds to item removal. The README's descriptions and any benchmark figures published upstream are not independently reproduced results. [[readme]][[security]]

## Benchmark status

**Benchmark not run.** No Hindsight runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the protocol and shared status, not Hindsight measurements. [[metrics]][[fixture]][[status]]

## Contact

The official pinned README and SECURITY.md were checked for a published contact email. Neither provides an email; SECURITY.md directs vulnerability reports through GitHub Security Advisories. The structured record stores `contact_email: null` and both exact checked URLs. No address was inferred from commit or profile metadata or obtained from a third-party directory. [[readme]][[security]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas URL records curated roster attribution only and is not assessment evidence. See the structured record [hindsight.json](../data/system-reviews/hindsight.json) and [curated roster](../data/memory-systems.json).
