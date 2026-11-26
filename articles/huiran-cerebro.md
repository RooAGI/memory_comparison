# Huiran-cerebro source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 309 / Huiran-cerebro / `huiran-cerebro`  
**Listed repository locator:** [qilunuojiang9-hue/Huiran-cerebro](https://github.com/qilunuojiang9-hue/Huiran-cerebro)  
**Canonical upstream:** [qilunuojiang9-hue/Huiran-cerebro](https://github.com/qilunuojiang9-hue/Huiran-cerebro)  
**Default branch / reviewed head:** master / [a2a77c9e270c234c3619f8777c490a419c8fb832](https://github.com/qilunuojiang9-hue/Huiran-cerebro/commit/a2a77c9e270c234c3619f8777c490a419c8fb832)  
**Review time:** 2026-11-25 23:35:36 UTC (2026-11-25 15:35:36 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Huiran-cerebro at ordinal 309 with slug `huiran-cerebro` and the explicit locator `https://github.com/qilunuojiang9-hue/Huiran-cerebro`. Its Atlas attribution is recorded for roster identity and locator context only, not as assessment evidence. The official repository page identifies `master` as the default branch; the official `master.atom` feed reports full current head `a2a77c9e270c234c3619f8777c490a419c8fb832`, updated 2026-11-20T11:31:40Z. This review is pinned to that head. [[catalog]][[atlas]][[repo]][[head]]

## Summary

Huiran-cerebro is a local-first Python memory and knowledge system built around SQLite, with Chinese-friendly FTS5 search, local embeddings, hybrid retrieval, a command line, web UI, and MCP server. Its current code has namespace-aware paths, fragment review states and soft deletion, plus retrieval and mutation audit records. This source review makes no runtime or performance claim. [[readme]][[core]][[mcp]]

## Who and what

The official README describes a personal/team memory and knowledge-base engine that can run locally and connect to agent clients through MCP. The repository includes the engine, CLI, Flask web UI, and server adapter; this review does not establish a hosted service or deployment authorization boundary. [[readme]][[mcp]]

## Architecture and data model

The `CyberBrain` engine stores content items, knowledge-base documents/chunks, memory fragments and rolling summaries, and entities with typed, time-windowed links in one SQLite database. Additional tables cover conversations, embeddings, ingestion records, retrieval audits, and mutation history. [[core]][[readme]]

A memory fragment carries type, subject, text, tags, entity references, a caller-provided source reference, importance, namespace, lifecycle status, deletion time, and embedding state. FTS5 trigram indexes serve Chinese text search; the documented local embedding path uses fastembed/ONNX and `BAAI/bge-small-zh-v1.5`, with vectors stored in SQLite. [[core]][[readme]]

The README describes a CLI and web interface over the engine. The MCP adapter exposes recall, search, memory and content writes, statistics, entity lookup, and session logging. Its default listener is loopback, with a host override available. [[readme]][[mcp]]

## Write, update, delete, and retrieval

**Write.** `add_fragment` validates a fragment type, derives importance from type and selected keywords when absent, defaults the namespace to `default`, stores the supplied source reference, and records an add mutation. Content/document writes also accept source labels, authorization references, and namespaces; long document text is divided into overlapping chunks. [[core]]

**Update and delete.** Content items have an `update_content` path for supported fields and record changed values in mutation history. In the inspected engine paths, memory fragments are written as new rows; I did not find a general in-place body-edit operation, while their lifecycle status, importance, embedding state, and deletion marker can change. Fragment deletion sets `deleted_at`, preserving a recoverable tombstone, and restore clears it; manual review can move a fragment through pending, active, and rejected states. The changelog says only active fragments enter retrieval. Content-item deletion is a distinct hard delete, and the inspected method does not log it like fragment deletion. [[core]][[changelog]]

**Retrieval.** The README describes reciprocal-rank fusion over FTS/BM25, LIKE, entity matches, and semantic vectors. The engine also supports time windows and importance-based age ranking for memory search. Semantic search computes cosine similarity over stored vectors. These source observations do not show answer quality or runtime speed. [[readme]][[core]]

**Entry-point scope.** MCP `search` accepts a namespace and forwards it. MCP `recall` has no namespace argument and calls the core recall path without an explicit namespace. Scope behavior therefore varies by interface. [[mcp]][[core]]

## Scope isolation

Writes and several search paths accept a namespace, and semantic search checks candidate vectors against their source rows. The v1.9 change log documents a fix for orphan vectors that previously bypassed namespace filtering; the current code rejects missing source rows and mismatched namespaces. [[core]][[changelog]]

That does not establish complete authorization or tenant isolation. I did not probe every route or a deployed authentication layer. MCP recall does not expose a namespace argument, and the inspected knowledge-base search method does not consistently expose the filter. Cross-namespace leakage remains unmeasured. [[mcp]][[core]][[metrics]]

## Provenance and evidence

Memory fragments accept a supplied `source_ref`; content and documents carry source and authorization labels; ingestion tables can relate a source to stored targets. These fields record caller-provided metadata. Source inspection does not show that source references are validated or that authorization is enforced by those labels. [[core]]

Retrieval audits record queries and returned items separately from mutation records. The README describes mutation history; the inspected engine writes mutation events for several fragment lifecycle and content paths. It does not establish complete coverage of every destructive operation. [[readme]][[core]]

Human review states are available for fragments, but the MCP memory-write tool can add a fragment without first requiring review. The review state is therefore a lifecycle option rather than a universal write gate. [[core]][[mcp]][[changelog]]

## Efficiency and observability

The design uses a local SQLite database and local embedding inference, with FTS5 trigram indexing for Chinese search. Semantic lookup scans stored vectors and calculates similarity before sorting; no latency at a particular corpus size was measured. [[readme]][[core]]

The README describes retrieval audit views, statistics, lifecycle maintenance, and daily summaries. The source includes query/result and mutation logging, but this review did not exercise runtime observability or measure overhead. [[readme]][[core]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Huiran-cerebro. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the evaluation protocol and shared status, not this system’s results. [[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Hybrid keyword, entity, and vector retrieval exists; answerability and abstention were not adjudicated. | Unmeasured |
| Correction and stale values | Fragment lifecycle and manual review exist; no correction sequence was assessed. | Unmeasured |
| Deletion leakage | Memory deletion is a reversible tombstone; content deletion is hard delete. No leakage probe was run. | Unmeasured |
| Scope isolation | Namespace parameters and semantic row checks exist; no cross-namespace workload was run, and filters vary by entry point. | Unmeasured |
| Evidence support and citation coverage | Source references and authorization labels are caller supplied; no answer was adjudicated against sources. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings were collected. | Unmeasured |
| Tokens, cost, and storage efficiency | No token, cost, or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This review inspected selected current code and official documentation at the verified head. Huiran-cerebro, its tests, migrations, and benchmark workloads were not run. Upstream README claims and change-log validation figures are not reproduced results here. [[readme]][[changelog]][[core]]

The review did not evaluate deployment authentication, backups and restore, concurrent writers, model acquisition, or every namespace-aware route. It cannot establish retrieval sufficiency, answer evidence support, or consuming-agent behavior. [[core]][[mcp]][[metrics]]

## Benchmark status

**Benchmark not run.** No Huiran-cerebro runtime, tests, or project benchmark workload was executed. No retrieval, correction, deletion, isolation, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the protocol and shared status, not Huiran-cerebro measurements. [[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email; none was found. The structured record stores `contact_email: null` and that exact URL. No address was inferred from profile or commit metadata or obtained from a third-party directory. [[readme]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas URL records curated roster attribution only and is not assessment evidence. See the structured record [huiran-cerebro.json](../data/system-reviews/huiran-cerebro.json) and [curated roster](../data/memory-systems.json).
