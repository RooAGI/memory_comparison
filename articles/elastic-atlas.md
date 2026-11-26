# Elastic Atlas

## Identity and review pin

- **Catalog position:** 211
- **Name and slug:** Elastic Atlas (elastic-atlas)
- **Listed repository:** [https://github.com/noamschwartz/atlas-memory-demo](https://github.com/noamschwartz/atlas-memory-demo) — explicit catalog locator.[[catalog](../data/memory-systems.json)] [[atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/elastic-atlas.md)]
- **Canonical upstream:** [noamschwartz/atlas-memory-demo](https://github.com/noamschwartz/atlas-memory-demo), default branch **main**; the official repository page and current main commit API resolve to **d84f9235a69d45a4fe326aaa691ad024699d0daa**.[[repo]][[head]]
- **Reviewed at:** 2026-11-25 16:29:08 PST (America/Los_Angeles; 2026-11-26T00:29:08Z)
- **Status:** Reviewed from code. Benchmark not run.

The catalog lists Elastic Atlas at ordinal 211 with slug elastic-atlas and the explicit repository locator above. Its pinned Atlas roster record is cited only for curated identity and locator attribution; the implementation assessment below is based on official upstream documentation and source.[[catalog]][[atlas]]

## Summary

Elastic Atlas is a research demo and agent memory layer built on Elasticsearch. It stores episodic events, semantic facts, and procedural playbooks in separate indices, exposes recall and mutation through an agent and MCP tools, and supports a shared catalog index.[[readme]][[guide]][[ops]]

## Who and what

The official README describes Atlas as a research demo and identifies Noam Schwartz in the project license line. The README presents a FastAPI backend, a Vite/React frontend, Elasticsearch, Kibana, and Elastic Inference Service; it also documents an MCP endpoint for external clients. This review treats it as a demonstration application and memory implementation, not a hosted service or a verified production deployment.[[readme]]

## Architecture and data model

The memory layer maps episodic, semantic, and procedural memories to atlas_memory_episodic, atlas_memory_semantic, and atlas_memory_procedural; the optional shared knowledge index is atlas_catalog. Elasticsearch semantic_text invokes the configured Jina v5 embedding inference endpoint during indexing. The repository README describes the frontend ↔ FastAPI ↔ Elastic Stack arrangement and calls out server-side embeddings.[[constants]][[readme]][[guide]]

Episodic writes retain user ID, text, role, event type, timestamp, session/agent identifiers, and metadata. Semantic documents carry text, a fact type, confidence, supporting episode IDs, creation/last-use timestamps, use count, metadata, and optional validity dates and pending-outcome state. Procedural documents carry a name, trigger, description, steps, version, success/failure counts, and creation time.[[ops]]

## Write, update, delete, and retrieval

**Write.** The write_memory operation assigns a UUID and inserts into the index selected by memory type. Semantic writes attach supporting episode IDs and validity metadata; procedural writes store playbook fields and counters. A semantic write can name a superseded fact. The old record is retained with supersession fields, and harsh contradictions may additionally mark it retracted. These are source-visible mutation paths, not a check of their runtime behavior.[[ops]][[tools]]

**Consolidation and update.** The chat agent stores customer messages as episodes and runs consolidation after the reply. The consolidation prompt limits factual extraction to customer statements or confirmations, uses assistant replies only as context, and asks for episode IDs supporting extracted facts. A per-user watermark in atlas_memory_state selects new episodes; a bounded set of earlier episodes is supplied as synthesis context. If that index is unavailable, source comments and code describe a fallback to the recent-window path. Procedural updates increment success/failure counts and may replace steps after checking the record's user ID.[[agent]][[consolidate]][[state]][[ops]]

**Delete.** The documented forget_memory tool deletes one memory by ID and memory type. The implementation documentation says it writes a tombstone event in the episodic index for audit; the general source review does not establish end-to-end erasure from backups, logs, replicas, or downstream copies.[[guide]][[ops]][[tools]]

**Retrieval.** The recall_memory operation combines BM25 text search and Jina semantic retrieval with reciprocal-rank fusion, fetches an over-sized candidate set, then uses a Jina reranker for top-k. It can select memory types, include the shared catalog, include superseded facts for retrospective queries, and optionally bump use statistics on final results. Results include IDs, memory type, score/rank, and stored source data; retrieval APIs do not themselves guarantee an answer or a citation for every generated claim.[[ops]][[constants]][[tools]]

## Scope isolation

Recall's filter admits documents with the requested user_id and, when catalog retrieval is enabled, user-agnostic catalog records. The helper returns match_all when no user ID is supplied, so isolation depends on callers providing the intended identity and deployment access controls. The official guide says the development MCP endpoint has no authentication and uses the path's user_id plus Elasticsearch filtering; it recommends adding bearer authentication before production use. The README describes optional Elasticsearch document-level security keys. No cross-user probe or authorization test was run.[[ops]][[guide]][[readme]]

## Provenance and evidence

Semantic records retain source_episodes, and consolidation's output contract requires supporting episode IDs from recent customer events. This links extracted facts to stored episodes, but the inspected API does not establish claim-level citations, source resolvability, or evidence-support precision in generated answers. Supersession and retraction fields preserve some prior-state information; explicit forget writes an episodic tombstone according to the implementation docstring.[[ops]][[consolidate]]

## Efficiency and observability

Source describes automatic embeddings at index time, an 80-candidate recall over-fetch before reranking, time-decay and use-count ranking, and a separate per-user watermark to avoid repeatedly extracting the same episodes. Optional retrieval-stat updates bump last_used_at and use_count; the README mentions an inline inspector of recalled and written documents. These are design and instrumentation observations only. No latency, token, cost, storage, or reliability measurement was made.[[ops]][[constants]][[state]][[readme]]

## Metric-domain evidence

- **Answerable recall and abstention:** unmeasured; source APIs return ranked memory records, not adjudicated answerability or correctness.[[ops]][[metrics]]
- **Correction and stale values:** semantic supersession and validity fields are implemented; correction accuracy and stale-value rate remain unmeasured.[[ops]][[metrics]]
- **Deletion leakage:** single-record forget and tombstone paths are visible; deletion completeness and leakage remain unmeasured.[[ops]][[metrics]]
- **Scope isolation:** user filters and optional document-level security are described, with caller-supplied identity and unauthenticated development MCP limits; no isolation workload was run.[[ops]][[guide]][[metrics]]
- **Evidence support and citation coverage:** episode provenance is stored, but generated-answer support and citation coverage are unmeasured.[[ops]][[consolidate]][[metrics]]
- **Latency, write-to-recall delay, tokens, cost, and storage:** no workload measurements were taken.[[metrics]][[record]]

## Limits and unknowns

This is a bounded read-only source review at the verified current main head. It does not establish retrieval correctness, model abstention, correction reliability, deletion completeness, effective deployment authorization, large-corpus behavior, or operational performance. The official guide includes demo and evaluation instructions, but none were executed for this review. Source structure and documentation are not benchmark results. Structured source IDs and pinned URLs are recorded in the [review record](../data/system-reviews/elastic-atlas.json).[[repo]][[head]][[guide]][[metrics]]

## Benchmark status

**Not run.** The project metric definitions and benchmark fixture describe evaluation dimensions and cases; the existing execution-status record is not a result for this system. No system, benchmark, or test was run.[[metrics]][[fixture]][[record]]

## Contact

The official pinned README was checked for a project contact email and publishes none. The structured record stores contact_email: null and this exact checked URL. No commit/profile metadata, third-party directories, or inferred address was used.[[readme]]

## Sources

- [Catalog record — identity and locator](../data/memory-systems.json)
- [Pinned Atlas roster entry — attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/elastic-atlas.md)
- [Official repository page](https://github.com/noamschwartz/atlas-memory-demo)
- [Official GitHub current main head API response](https://api.github.com/repos/noamschwartz/atlas-memory-demo/commits/main)
- [Pinned README](https://github.com/noamschwartz/atlas-memory-demo/blob/d84f9235a69d45a4fe326aaa691ad024699d0daa/README.md)
- [Pinned ATLAS guide](https://github.com/noamschwartz/atlas-memory-demo/blob/d84f9235a69d45a4fe326aaa691ad024699d0daa/ATLAS.md)
- [Pinned memory operations](https://github.com/noamschwartz/atlas-memory-demo/blob/d84f9235a69d45a4fe326aaa691ad024699d0daa/backend/app/atlas/memory/operations.py)
- [Pinned memory constants](https://github.com/noamschwartz/atlas-memory-demo/blob/d84f9235a69d45a4fe326aaa691ad024699d0daa/backend/app/atlas/memory/constants.py)
- [Pinned consolidation watermark](https://github.com/noamschwartz/atlas-memory-demo/blob/d84f9235a69d45a4fe326aaa691ad024699d0daa/backend/app/atlas/memory/state.py)
- [Pinned agent loop](https://github.com/noamschwartz/atlas-memory-demo/blob/d84f9235a69d45a4fe326aaa691ad024699d0daa/backend/app/atlas/agent.py)
- [Pinned tool definitions and dispatch](https://github.com/noamschwartz/atlas-memory-demo/blob/d84f9235a69d45a4fe326aaa691ad024699d0daa/backend/app/atlas/tools.py)
- [Pinned consolidation implementation](https://github.com/noamschwartz/atlas-memory-demo/blob/d84f9235a69d45a4fe326aaa691ad024699d0daa/backend/app/atlas/consolidate.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
