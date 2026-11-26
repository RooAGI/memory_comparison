# Habitus AI source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 279 / Habitus AI / `habitus-ai`  
**Listed repository locator:** [munch2u-a11y/Habitus-AI](https://github.com/munch2u-a11y/Habitus-AI)  
**Canonical upstream:** [munch2u-a11y/Habitus-AI](https://github.com/munch2u-a11y/Habitus-AI)  
**Default branch / reviewed head:** main / [f93b770e4b3c1875151dc13eb90421598c3efa5f](https://github.com/munch2u-a11y/Habitus-AI/commit/f93b770e4b3c1875151dc13eb90421598c3efa5f)  
**Review time:** 2026-11-25 22:13:16 UTC (2026-11-25 14:13:16 PST; America/Los_Angeles).

## Identity and review pin

The catalog identifies ordinal 279 as Habitus AI (`habitus-ai`) and lists the explicit repository locator `https://github.com/munch2u-a11y/Habitus-AI`. The catalog's pinned Agent Memory Atlas source is retained only as curated identity/locator attribution; it is not assessment evidence. The official GitHub repository page identifies `main` as the default branch. Its official `main.atom` commit feed reports current head `f93b770e4b3c1875151dc13eb90421598c3efa5f`, updated 2026-08-28T12:50:53Z. This review is pinned to that full SHA. [[catalog]][[atlas]][[repo]][[head]]

## Summary

Habitus AI is a Python agent-memory library built around immutable SQLite records and a pair of directional concept graphs. Retrieval combines a direct dense record lane with graph-path and vault retrieval; later outcomes can reinforce graph edges under a receipt gate. This is a source review and makes no runtime quality or performance claim. [[readme]][[architecture]][[pipeline]]

## Who and what

The official README describes a Python engine for agent memory and RAG, with a local database, library and CLI/app entry points. The architecture document describes model, embedding and execution boundaries as replaceable components. No maintainer identity is asserted here. [[readme]][[architecture]]

## Architecture and data model

A canonical `MemoryRecord` stores record and event IDs, record type, source ID, timestamp, text, embedding, provenance and metadata, and may point to the record it supersedes. SQLite is the authority for these records and for concepts, directional graph edges, edge evidence, vault membership, traversal traces, outcomes, experience states, projections and overlap clusters. Database triggers reject both update and delete on canonical records. [[types]][[store]][[architecture]]

The topology has one SELF origin, input trunks HEAR, SEE and NOTICE, output trunks SPEAK, LOOK and DO, and a semantic crown shared across both directions. Edges store vertical distance, log-strength, conflict penalty and activity information. The architecture describes globally normalized live edge weights and locally normalized outgoing choices; lower experience projections refer to canonical record IDs and do not duplicate prose. [[architecture]][[graph]][[store]]

By default, the pipeline selects a local `habitus_memory.sqlite` file and a 1024-dimensional deterministic hash embedder. That embedder hashes tokens, trigrams and adjacent-token pairs; the implementation describes it as an offline reproducible adapter and recommends a real semantic model for production. A caller can supply an embedder, while the stored embedding-space identity and dimension are checked when opening the database. [[pipeline]][[embeddings]][[store]][[architecture]]

## Write, update, delete, and retrieval

**Write.** The pipeline accepts an event envelope and creates an immutable record with event/source identity, timestamp, text, embedding, provenance and metadata. The event ID is unique in the database. Graph structure and lower projections provide routing and learned preference information while the canonical record remains the text authority. [[types]][[pipeline]][[store]][[architecture]]

**Update.** The documented correction path creates a new record whose `supersedes_id` points to the earlier record; it does not overwrite canonical history. Active-record retrieval can omit superseded records. The SQLite layer also rejects direct record deletion. I did not find a normal record purge operation in the inspected documentation and core paths, so physical erasure and retention behavior remain unknown. [[architecture]][[types]][[store]][[pipeline]]

**Delete.** The inspected implementation provides supersession as the canonical-fact lifecycle mechanism. Graph edges have an archived state, but canonical records have delete-preventing triggers. Backups, WAL retention, database-file disposal and external retention integrations were not inspected. [[store]][[types]][[graph]]

**Retrieval.** Each recall has two lanes. A direct dense lane scans active canonical records and selects up to three above a configurable similarity floor. A graph lane admits semantic endpoints, traverses weighted Y paths, expands visited concepts and searches their vault records with dense similarity plus BM25. Results are deduplicated by canonical ID. The retrieval packet includes endpoint candidates, paths, selected record IDs, contradictions, a context budget and a trace hash; context packing uses record text under a character limit. [[retrieval]][[types]][[architecture]]

## Scope isolation

The inspected `MemoryRecord` and records schema include source and event identity but no tenant, user, project or agent namespace. Callers can choose a database path, which provides a file-level separation option; the reviewed core does not establish per-user authorization or safe multi-tenant sharing. No cross-scope workload was run. [[types]][[store]][[pipeline]]

## Provenance and evidence

Canonical records retain source IDs, timestamps, provenance and metadata. Edges can link to supporting canonical record IDs, while traversal and retrieval packets retain paths and selected IDs. These structures give the implementation traceable links to stored inputs; they do not independently verify that the input is true or that a generated answer is supported. [[types]][[store]][[graph]][[retrieval]]

The architecture requires verified outcomes for durable edge reinforcement and says an external outcome must carry a receipt ID. The pipeline rejects a verified output without a receipt ID before reinforcement. Separately, the optional ToolRegistry marks a receipt verified after a registered handler returns successfully; that flag records handler success, not an independent audit of external state. Integrators should treat the receipt boundary according to their own verification process. [[architecture]][[pipeline]][[tools]]

## Efficiency and observability

The described default is local SQLite with WAL and no external database server. Retrieval parameters bound the direct lane, graph candidates, traversals, expansions and context length. The default dense path computes similarities over active records rather than using a built-in production vector index. The deterministic default embedder is lexical hashing, so its semantic quality should not be inferred from the README's description of the system. [[store]][[retrieval]][[pipeline]][[embeddings]]

The data model records retrieval traces, path scores, selected record IDs and outcomes; the README documents a status view for records, concepts, edges and graph health. The code also times tool handlers for their receipts. These are observability hooks, not evidence of latency, cost, quality or scale. No timings or resource measurements were collected. [[types]][[store]][[readme]][[tools]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Habitus AI. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [shared execution status](../results/initial-baselines-status.json) describe the evaluation protocol, not Habitus AI results. [[metrics]][[fixture]][[status]]

| Domain | Code evidence | Status |
|---|---|---|
| Answerable retrieval and abstention | Direct dense and graph-vault retrieval with a direct similarity floor; no answerability or abstention workload was scored. | Unmeasured |
| Correction and stale values | Immutable superseding records and active-record retrieval; no correction sequence was run. | Unmeasured |
| Deletion leakage | Record deletion is blocked by a SQLite trigger; no deletion or recovery probe was run. | Unmeasured |
| Scope isolation | No tenant or user key appears in the inspected record model; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Provenance and supporting-record links exist; no answer was adjudicated against source evidence. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings were collected. | Unmeasured |
| Tokens, cost, and storage | Context is character-bounded and storage is local SQLite; no token, cost or storage workload was measured. | Unmeasured |

## Limits and unknowns

This review covers the official README, architecture document, core data model, store, retrieval, pipeline, graph, embedding and optional tool-registry paths at the verified head. Habitus AI, its tests and benchmarks were not run. The source does not establish answer quality, useful abstention, semantic quality under production embeddings, multi-user isolation, concurrency under load, backup/restore behavior, complete erasure, or runtime cost and scale. [[readme]][[architecture]][[types]][[store]][[retrieval]][[pipeline]][[graph]][[embeddings]][[tools]]

The architecture document explicitly lists several base capabilities as absent, including a production semantic embedding/index, destructive graph-branch merging, automatic skill/tool discovery, and an authority policy for external actions. The README makes claims such as “zero eviction” and “ultra-fast”; those remain upstream statements and were not reproduced or measured here. The optional tool registry's meaning of `verified` merits integration-specific scrutiny because success means the registered handler returned without raising. [[architecture]][[readme]][[tools]]

## Benchmark status

**Benchmark not run.** No Habitus AI runtime, tests or benchmark workload was executed. No recall, correction, deletion, scope, evidence, latency, token, cost or storage result is claimed. The [metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json) and [execution status record](../results/initial-baselines-status.json) are protocol references, not system results. [[metrics]][[fixture]][[status]]

## Contact

The official pinned README and official security policy were checked for a published contact email; neither lists one. The structured record stores `contact_email: null` with both exact checked URLs. No address was inferred from commit/profile metadata or a third-party directory. [[readme]][[security]]

## Sources

Upstream file citations are pinned to reviewed SHA `f93b770e4b3c1875151dc13eb90421598c3efa5f`. The Atlas URL records curated roster attribution only, not implementation evidence. See the structured review record [habitus-ai.json](../data/system-reviews/habitus-ai.json) and [curated roster](../data/memory-systems.json).
