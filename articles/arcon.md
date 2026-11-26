# Arcon source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 66 / Arcon / arcon  
**Listed repository locator:** [vmDeshpande/Arcon](https://github.com/vmDeshpande/Arcon)  
**Current canonical repository:** [vmDeshpande/Arcon](https://github.com/vmDeshpande/Arcon)  
**Default branch / reviewed head:** main / ea59c28349bae303118e6f7388016628585723b7  
**Review time:** 2026-11-24 21:26:10 UTC (13:26:10 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog places Arcon at ordinal 66, with the listed repository locator above and an Atlas attribution source pinned at revision 19199a4fc249e89c0793be06f0b166b358089ba0. I used the catalog entry and Atlas link only to record identity and attribution; their descriptions, marks, and layout were not assessment evidence. The official repository identifies main as the default branch, and its main commit feed identifies current head ea59c28349bae303118e6f7388016628585723b7. [[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/vmDeshpande/Arcon)] [[main branch feed](https://github.com/vmDeshpande/Arcon/commits/main.atom)] [[reviewed commit](https://github.com/vmDeshpande/Arcon/commit/ea59c28349bae303118e6f7388016628585723b7.patch)]

## Summary

Arcon is a local-first digital companion application with a modular TypeScript memory subsystem. The reviewed package combines SQLite records, extraction and review, lifecycle and scope filters, lexical ranking, entity knowledge, and reflection proposals. This is a source review tied to the pinned head, not an execution or performance assessment. [official README](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/README.md)

## Who and what

The official README presents Arcon as a digital companion architecture rather than a standalone hosted memory service. This review focuses on its TypeScript memory package inside the larger Node.js application; the README describes a separate Python inference service. [official README](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/README.md)

## Architecture and data model

The package separates durable personal memories from conversation history. Its code is organized into extraction, pipeline and review, retrieval, reflection, semantic helpers, and entity knowledge modules. [memory package index](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/index.ts)

A personal-memory row stores a typed item in SQLite with status, content, importance and confidence scores, source type, timestamps, optional subject and tags, evidence count, last-used time, supersession link, and scope. The repository enables WAL mode and creates indexes for type, status, type/status, subject, update time, and scope. [personal-memory.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/personal-memory.ts)

Conversation messages are stored in separate conversation and message tables with conversation IDs, timestamps, roles, summaries, topics, and metadata. The store supports reads scoped by conversation ID and clearing a conversation. [conversation-store.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/conversation-store.ts)

## Write, update, delete, and retrieval

**Write and extraction.** The inspected MemoryExtractor rejects a set of instruction-like patterns, validates messages, applies phrase rules, and deduplicates similar candidate text; it returns candidates without persisting them. The pipeline then normalizes and validates candidates and applies a review decision. The README separately describes semantic extraction with an LLM and regex fallback; that model-backed path was not inspected. [memory-extractor.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/extractor/memory-extractor.ts) [candidate.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/extractor/candidate.ts) [memory-pipeline.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/pipeline/memory-pipeline.ts) [memory-review.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/pipeline/memory-review.ts) [README.md](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/README.md)

**Create, update, and correction.** The pipeline implements CREATE, UPDATE, IGNORE, and CONFLICT decisions; a conflict can create a PENDING_CONFIRMATION memory. The README documents broader lifecycle actions including supersession and archive. Correction accuracy and consistency across callers were not measured. [memory-pipeline.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/pipeline/memory-pipeline.ts) [memory-review.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/pipeline/memory-review.ts) [personal-memory.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/personal-memory.ts) [README.md](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/README.md)

**Delete and retirement.** Documentation and pipeline expose archive and supersession as ways to retire or hide a memory while preserving history. This bounded review did not establish a physical-erasure API or completeness across databases, backups, exports, and derived data; erasure behavior remains unknown here. [README.md](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/README.md) [memory-pipeline.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/pipeline/memory-pipeline.ts) [personal-memory.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/personal-memory.ts)

**Retrieval.** MemoryRetriever combines entity-derived memories with stored memories, filters non-current statuses on the normal path, deduplicates by type and content, scores and sorts candidates, then applies a result limit. The score uses substring keyword matches, importance, confidence, capped evidence count, recency, and status. The implementation is lexical; the README says semantic vector search is deferred. [memory-retriever.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/retrieval/memory-retriever.ts) [memory-ranking.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/retrieval/memory-ranking.ts) [README.md](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/README.md)

**Scope isolation.** Records have a scope field and index. Normal retrieval restricts general memories to USER or ARCON; the threshold API accepts optional type and scope filters. Entity memories are fetched separately and merged with general results. The inspected record model has no tenant or principal identifier, so these filters do not establish multi-tenant authorization. [personal-memory.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/personal-memory.ts) [memory-retriever.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/retrieval/memory-retriever.ts)

**Provenance and evidence.** A memory can retain source type, confidence, timestamps, evidence count, and a supersession link. The repository schema includes an audit log with prior and new status/content, reason, source, and time; the README describes a mutation audit trail. Reflection candidates also carry experience type, counts, time range, and optional context. The inspected processor passes a reason string and scores into a candidate rather than the full evidence array, so durable evidence retention through that path is not established. [personal-memory.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/personal-memory.ts) [README.md](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/README.md) [reflection-candidate.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/reflection/reflection-candidate.ts) [reflection-engine.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/reflection/reflection-engine.ts) [reflection-processor.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/reflection/reflection-processor.ts)

**Source-visible efficiency and observability.** SQLite indexes support type, status, scope, and time lookups, with WAL mode enabled. Retrieval loads candidate rows, scores them in application code, sorts them, and updates last-used timestamps for returned memories. The context formatter caps output at 15 entries. The pipeline returns action counters; the inspected scorer has no timing instrumentation. These are code observations, not latency, throughput, token, cost, or storage measurements. [personal-memory.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/personal-memory.ts) [memory-retriever.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/retrieval/memory-retriever.ts) [memory-ranking.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/retrieval/memory-ranking.ts) [context-builder.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/retrieval/context-builder.ts) [memory-pipeline.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/pipeline/memory-pipeline.ts)

## Metric-domain evidence

All metric domains remain unmeasured for this review. Source-visible records, filters, and scoring steps are implementation evidence only. No Arcon workload was run for answerable recall or abstention, corrections and stale values, deletion leakage, scope isolation, evidence support or citation coverage, retrieval latency, write-to-recall delay, tokens or cost, or storage efficiency. The project definitions and fixture specify a separate protocol; the execution-status record is not_run. [[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This bounded review covered the official README and selected memory, extraction, pipeline, retrieval, reflection, and conversation-store files at the verified full SHA. Arcon, its tests, and benchmark workloads were not run. The README's reported test and runtime status is upstream documentation, not verification performed for this review. The inspected lexical scorer does not establish answer quality or calibrated abstention; physical-erasure completeness, principal-level isolation, and end-to-end persistence of reflection evidence remain unverified. [README.md](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/README.md) [memory-pipeline.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/pipeline/memory-pipeline.ts) [memory-retriever.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/retrieval/memory-retriever.ts) [reflection-processor.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/reflection/reflection-processor.ts)

## Contact-list follow-up

The official pinned SECURITY.md publishes vedant.milind.deshpande@gmail.com for security reports. I also checked the official README and SUPPORT.md; SUPPORT directs usage questions to GitHub Discussions and issues and does not publish an email. [SECURITY.md](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/SECURITY.md) [README.md](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/README.md) [SUPPORT.md](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/SUPPORT.md)

## Benchmark status

**Benchmark not run.** No Arcon runtime, tests, or benchmark workload were run. Project metric definitions, fixture, and the not_run status record describe a separate protocol; they are not Arcon results. [[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Official repository](https://github.com/vmDeshpande/Arcon)
- [Official main branch commit feed](https://github.com/vmDeshpande/Arcon/commits/main.atom)
- [Reviewed full head commit](https://github.com/vmDeshpande/Arcon/commit/ea59c28349bae303118e6f7388016628585723b7.patch)
- [README.md](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/README.md)
- [Memory package index](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/index.ts)
- [personal-memory.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/personal-memory.ts)
- [memory-extractor.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/extractor/memory-extractor.ts)
- [candidate.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/extractor/candidate.ts)
- [memory-pipeline.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/pipeline/memory-pipeline.ts)
- [memory-review.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/pipeline/memory-review.ts)
- [memory-retriever.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/retrieval/memory-retriever.ts)
- [memory-ranking.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/retrieval/memory-ranking.ts)
- [context-builder.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/retrieval/context-builder.ts)
- [reflection-candidate.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/reflection/reflection-candidate.ts)
- [reflection-engine.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/reflection/reflection-engine.ts)
- [reflection-processor.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/reflection/reflection-processor.ts)
- [conversation-store.ts](https://github.com/vmDeshpande/Arcon/blob/ea59c28349bae303118e6f7388016628585723b7/packages/memory/src/conversation-store.ts)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and attribution](../data/memory-systems.json)
- [Atlas roster attribution source, identity only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/arcon.md)

**Verification boundary:** no Arcon runtime, tests, or benchmarks were run.
