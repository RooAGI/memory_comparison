# HippoRAG source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 299 / HippoRAG / `hipporag`  
**Listed repository locator:** [OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG)  
**Canonical upstream:** [OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG)  
**Default branch / reviewed head:** main / [d5c8329422e0a0b834a15874545cb6a74b4f9b26](https://github.com/OSU-NLP-Group/HippoRAG/commit/d5c8329422e0a0b834a15874545cb6a74b4f9b26)  
**Review time:** 2026-11-25 23:09:10 UTC (2026-11-25 15:09:10 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists HippoRAG at ordinal 299 with the explicit locator `https://github.com/OSU-NLP-Group/HippoRAG`. Its Atlas attribution is recorded only for curated identity and locator context; it is not assessment evidence. The official repository page identifies `main` as the default branch. Official Git transport reports `HEAD -> refs/heads/main` at full SHA `d5c8329422e0a0b834a15874545cb6a74b4f9b26`, and a shallow checkout resolved to the same SHA. [[catalog]][[atlas]][[repo]][[head]]

## Summary

HippoRAG is a Python framework that converts documents into passage, entity, and fact embeddings plus a knowledge graph. Retrieval scores facts, reranks them, uses Personalized PageRank to find connected passages, and falls back to dense passage retrieval when no fact is selected. An optional MCP server exposes the persistent index to agents. This is a source review, not a measured evaluation. [[readme]][[core]][[mcp]]

## Who and what

The official repository presents HippoRAG 2 as a memory framework for LLMs inspired by long-term memory. It includes a Python API, experiment/evaluation entry point, persistent MCP server, and Claude Code plugin. The README cites its NeurIPS 2024 and ICML 2025 papers; quality and efficiency claims in those materials are upstream-reported, not reproduced here. [[readme]]

## Architecture and data model

Indexing preprocesses documents into content-addressed chunks, stores passage embeddings, runs OpenIE to extract entities and triples, embeds entities and facts separately, and builds an igraph of passage/entity nodes and fact or synonymy edges. The default embedding backend stores Parquet files; configuration also supports Qdrant, ChromaDB, and Milvus. [[core]][[embedding]][[config]]

The persistent index includes chunk metadata, OpenIE state, graph state, and an index manifest describing model, extractor, preprocessor, graph, and explicit index identity. Incompatible state is rejected rather than silently reused. The index is organized by its save directory; the graph has no intrinsic tenant identity. [[core]][[state]]

The optional MCP server exposes index, retrieve, rag_qa, delete, and index_stats tools. Its HTTP transport has no built-in authentication according to the official README; operators are told to bind loopback or use an authenticating proxy. The MCP service serializes calls through a worker thread because the HippoRAG instance is not thread-safe. [[mcp]][[readme]]

## Write, update, delete, and retrieval

**Write.** Callers provide strings or `Chunk` values containing content, optional source ID, and metadata. Indexing hashes and embeds chunks, extracts entities/triples through OpenIE, embeds facts/entities, and connects them in the graph. Identical text shares a content-derived chunk ID; supplied metadata may be replaced when the duplicate is indexed again. [[misc]][[core]]

**Update.** The inspected API has indexing and deletion operations but no distinct in-place fact correction method. Changed text hashes to a new chunk; changes to model/extractor/preprocessor identity can make persisted index state incompatible. Metadata for identical content is replaced rather than versioned. [[core]][[state]]

**Delete.** The core delete path removes exact matching chunks from embedding stores, OpenIE state, metadata, and graph. Source-aware edge and entity mappings preserve shared facts while another chunk still supports them, and remove contributions that no longer have a source. The MCP wrapper can resolve a source ID to all associated chunks before deletion. These are code observations, not a verified guarantee of erasure from backups or external services. [[core]][[mcp]]

**Retrieval.** Retrieval scores and reranks facts, then uses graph search with Personalized PageRank to diffuse relevance to passages; if no fact remains after reranking, it falls back to dense passage retrieval. Results carry scores and metadata, while `rag_qa` asks the configured LLM to answer from retrieved passages. [[core]][[mcp]]

## Scope isolation

A configured save directory and optional vector-store namespace distinguish indexes. The inspected core does not establish user or tenant authorization inside the graph, and the documented MCP HTTP transport has no authentication by itself. Isolation therefore depends on deployment boundaries and correct index selection; no cross-scope probe was run. [[core]][[embedding]][[readme]]

## Provenance and evidence

Chunks can carry source IDs and arbitrary JSON metadata, which the MCP retrieval response returns alongside passages. OpenIE rows and graph edges track originating chunk IDs so deletion can remove unsupported fact contributions. This provides source lineage at passage/fact construction level, but it does not establish truth of extracted claims or enforce answer citations. [[misc]][[mcp]][[core]]

## Efficiency and observability

The code records aggregate retrieval, reranking, and PPR timings; the MCP index_stats tool reports passage/entity/fact and graph counts. The implementation supports batching and multiple embedding stores, while the README documents model/token reporting and an offline vLLM indexing path. These are implementation and documentation observations, not measurements from this review. [[core]][[mcp]][[readme]]

## Metric-domain evidence

All project metric domains are **unmeasured** for HippoRAG. The [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the protocol, not HippoRAG results. [[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Fact retrieval, reranking, graph propagation, dense fallback, and QA are implemented; no answerability workload was scored. | Unmeasured |
| Correction and stale values | No dedicated correction API was found; no correction sequence was evaluated. | Unmeasured |
| Deletion leakage | Source-aware removal is implemented; no post-delete leakage probe was run. | Unmeasured |
| Scope isolation | Index paths/namespaces are configurable; no authenticated tenant boundary or isolation probe was established. | Unmeasured |
| Evidence support and citation coverage | Passage source metadata is available; no answer citation/support adjudication was performed. | Unmeasured |
| Retrieval latency and write-to-recall delay | Timing logs exist; this review collected no latency or freshness measurements. | Unmeasured |
| Tokens, cost, and storage efficiency | Model usage and Parquet/remote vector storage are configurable; no usage or storage workload was measured. | Unmeasured |

## Limits and unknowns

The inspection covered the official README and selected implementation for indexing, deletion, retrieval, MCP, embedding storage, configuration, and index identity at the verified head. It does not establish extraction accuracy, answer quality, runtime reliability, or behavior of every optional vector backend. Metadata supports provenance references but does not prove claim truth. Complete erasure across backups and remote services is unverified. [[readme]][[core]][[mcp]][[embedding]][[state]]

Upstream research and README performance claims were not independently reproduced. No HippoRAG runtime, tests, or benchmark workload was run. [[readme]][[metrics]][[fixture]][[status]]

## Benchmark status

**Benchmark not run.** No HippoRAG runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, isolation, evidence, latency, token, cost, or storage result is claimed. The [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the shared project protocol, not HippoRAG measurements. [[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for contact email. It lists project authors and recommends opening an issue, but publishes no email. The record stores `contact_email: null` and the exact checked URL; no address was inferred from profile or commit metadata. [[readme]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas URL is included only for curated roster attribution and is not assessment evidence. See the structured [review record](../data/system-reviews/hipporag.json) and [curated roster](../data/memory-systems.json).
