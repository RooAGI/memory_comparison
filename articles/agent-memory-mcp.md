# agent-memory-mcp source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 14 / agent-memory-mcp / agent-memory-mcp  
**Listed repository locator:** [ipiton/agent-memory-mcp](https://github.com/ipiton/agent-memory-mcp)  
**Current canonical repository:** [ipiton/agent-memory-mcp](https://github.com/ipiton/agent-memory-mcp)  
**Default branch / reviewed head:** main / 1794edb14f727c8120eae11d1f30468cfdbf7d20  
**Review time:** 2026-11-24 18:40:37 UTC (10:40:37 PST; America/Los_Angeles).

## Identity and scope

The curated roster places **agent-memory-mcp** at ordinal 14, lists the repository locator above, and attributes the entry to Atlas catalog revision `19199a4fc249e89c0793be06f0b166b358089ba0`. GitHub identifies the canonical public repository and shows `main` as its default branch. The repository page’s latest commit and its patch identify the reviewed full head as `1794edb14f727c8120eae11d1f30468cfdbf7d20`. The roster was used only for identity and attribution; Atlas descriptions, marks, prose, ordering, and layout were not used as assessment evidence.[[project roster](../data/memory-systems.json)] [[GitHub repository](https://github.com/ipiton/agent-memory-mcp)] [[main branch head patch](https://github.com/ipiton/agent-memory-mcp/commit/1794edb14f727c8120eae11d1f30468cfdbf7d20.patch)]

agent-memory-mcp is a Go MCP server and CLI for persistent agent memories and project-document search. Its documented architecture has an MCP protocol layer over memory, RAG, allowlisted file access, and stewardship components. This review covers selected code and official documentation at the verified revision. Product documentation is treated as documentation, not runtime evidence.[[README.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/README.md)] [[docs/ARCHITECTURE.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/ARCHITECTURE.md)] [[docs/CONTRIBUTING.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/CONTRIBUTING.md)]

## Architecture and data model

**Code observation.** The memory package defines episodic, semantic, procedural, and working entries. A memory row carries content, title, tags, a context string, importance, metadata, embedding and model identity, timestamps, access counts, and temporal/supersession fields. SQLite is the durable store; the implementation also maintains an in-process cache and optional embedding data. The architecture guide separates this memory store from document indexing/search and the stewardship service.[[internal/memory/memory.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/memory.go)] [[internal/memory/store_sql.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/store_sql.go)] [[docs/ARCHITECTURE.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/ARCHITECTURE.md)]

The architecture document describes separate memory and SQLite-backed RAG stores, embedding providers, and a stewardship service with policy, scheduler, inbox, drift, and verification functions. It documents Jina, OpenAI-compatible, and local Ollama embedding options; model identity is retained and incompatible embedding spaces are not mixed during recall. Changing models requires reindexing documents and re-embedding memories.[[docs/ARCHITECTURE.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/ARCHITECTURE.md)] [[docs/INSTALLATION.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/INSTALLATION.md)]

## Write, update, delete, and retrieval

**Code observation — write and update.** `Store` validates memory, rejects provider tokens and redacts credential-shaped content before embedding, then computes an embedding before taking the store write lock. It inserts the SQLite row, reads it back to confirm persistence, updates the cache, logs the event, and may asynchronously fan out triple extraction. `Update` computes replacement embeddings outside the write lock; if embedding fails, the update can continue without a vector. Revision code stores old text and title in the same transaction as a content replacement. These are source-visible paths, not reliability measurements.[[internal/memory/write.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/write.go)] [[internal/memory/store_sql.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/store_sql.go)] [[internal/memory/revisions.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/revisions.go)]

**Documentation observation — delete and correction.** The MCP tool reference exposes `delete_memory` by ID and `update_memory`. It also documents `mark_outdated` with temporal validity and supersession links, and `recall_as_of` for historical queries. The inspected sources establish revision and validity-window support, but do not establish that delete removes every related record, embedding, revision, or derived index; deletion completeness remains unknown here.[[docs/MCP_TOOLS.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/MCP_TOOLS.md)] [[internal/memory/temporal.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/temporal.go)] [[internal/memory/revisions.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/revisions.go)]

**Retrieval.** The tool documentation describes semantic/text recall with optional filters and trust-aware ranking, plus separate hybrid document search. Context can filter memory operations; the docs advise setting it for project, task, or service memories. The code has per-context snapshots and a pre-cache-load path that queries SQLite for the requested context. These paths establish interfaces and filters, not answerable recall quality or calibrated abstention.[[docs/MCP_TOOLS.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/MCP_TOOLS.md)] [[internal/memory/read.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/read.go)]

## Scope isolation and provenance

**Scope.** The installation guide describes a solo-local setup with runtime state under one project directory. For shared HTTP deployments, the security guide describes bearer-token authentication, host/origin checks, loopback defaults, and an explicit unsafe unauthenticated override. Repository file tools are restricted to `MCP_ROOT` and configured allowlisted directories. A context value is a retrieval filter; it should not be mistaken for authenticated tenant isolation. Deployment-specific authorization was not independently exercised.[[docs/INSTALLATION.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/INSTALLATION.md)] [[docs/SECURITY.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/SECURITY.md)] [[internal/memory/memory.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/memory.go)]

**Evidence and trust.** The trust implementation derives a knowledge layer, source type, confidence, owner, last-verified time, and freshness score from memory metadata, tags, lifecycle, and timestamps. Official tool documentation exposes source-oriented recall and review operations; stewardship docs describe verification, duplicate/conflict/staleness scans, an inbox, promotion, and drift checks against source files. These are provenance signals and workflows; source review does not prove a source currently supports a claim or that every reference resolves.[[internal/memory/trust.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/trust.go)] [[docs/STEWARDSHIP.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/STEWARDSHIP.md)] [[docs/MCP_TOOLS.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/MCP_TOOLS.md)]

## Source-visible efficiency and observability

**Code observation.** Embedding calls happen before the serialized SQLite write section, writes perform a read-after-write check, and the memory layer maintains a cache with context snapshots. The architecture documents model-aware vector recall and local SQLite search. These implementation details can shape resource use but do not demonstrate measured throughput or latency.[[internal/memory/write.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/write.go)] [[internal/memory/read.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/read.go)] [[docs/ARCHITECTURE.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/ARCHITECTURE.md)]

The stats package supports sampled JSONL events with duration, success/error, tool/method, query length, and request limits. Memory rows also track access counts and timestamps. These are source-visible observability mechanisms; no trace, token/cost result, or runtime metric was collected for this review.[[internal/stats/stats.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/stats/stats.go)] [[internal/memory/memory.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/memory.go)]

## Project metric domains

All benchmark domains are **unmeasured** for agent-memory-mcp. Source and documentation show retrieval, temporal correction, delete, scope filters, trust metadata, indexing, and observability paths. They do not provide answerable recall or abstention scores; correction or stale-value accuracy; deletion or scope-isolation leak rates; evidence support or citation coverage; latency distribution; write-to-recall delay; token/cost totals; or storage efficiency. Project metric definitions and the fixture describe a measurement protocol, not system results.[[project metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded read-only review of selected Go memory, trust, revision, and stats files and official repository documentation at the verified SHA. The system, its tests, and benchmarks were not run. Exact physical deletion semantics, deployed tenant authorization, claim support quality, and behavior under concurrent load remain unverified. Unknown means unverified in this review.[[internal/memory/write.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/write.go)] [[docs/SECURITY.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/SECURITY.md)] [[docs/MCP_TOOLS.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/MCP_TOOLS.md)]

## Contact-list follow-up

The official security policy, contributor guide, and README were checked for a published contact email. None of those pages publishes one. The security policy points to a private GitHub advisory and mentions a maintainer profile; I did not consult that profile or infer an email.[[docs/SECURITY.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/SECURITY.md)] [[docs/CONTRIBUTING.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/CONTRIBUTING.md)] [[README.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/README.md)]

## Benchmark status

**Benchmark not run.** No system execution, test suite, or benchmark workload was run. Code observations and product documentation are not measured results. See the project metric definitions, execution status, and fixture for the separate measurement protocol.[[project metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical GitHub repository](https://github.com/ipiton/agent-memory-mcp)
- [Reviewed full main head patch](https://github.com/ipiton/agent-memory-mcp/commit/1794edb14f727c8120eae11d1f30468cfdbf7d20.patch)
- [README.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/README.md)
- [docs/ARCHITECTURE.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/ARCHITECTURE.md)
- [docs/INSTALLATION.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/INSTALLATION.md)
- [docs/MCP_TOOLS.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/MCP_TOOLS.md)
- [docs/SECURITY.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/SECURITY.md)
- [docs/STEWARDSHIP.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/STEWARDSHIP.md)
- [docs/CONTRIBUTING.md](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/docs/CONTRIBUTING.md)
- [internal/memory/memory.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/memory.go)
- [internal/memory/write.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/write.go)
- [internal/memory/read.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/read.go)
- [internal/memory/store_sql.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/store_sql.go)
- [internal/memory/trust.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/trust.go)
- [internal/memory/revisions.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/revisions.go)
- [internal/memory/temporal.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/memory/temporal.go)
- [internal/stats/stats.go](https://github.com/ipiton/agent-memory-mcp/blob/1794edb14f727c8120eae11d1f30468cfdbf7d20/internal/stats/stats.go)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated catalog locator and source attribution](../data/memory-systems.json)

**Verification boundary:** no agent-memory-mcp system, tests, or benchmarks were run.
