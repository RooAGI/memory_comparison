# Agent-MemoryForge source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 15 / Agent-MemoryForge / agent-memoryforge  
**Listed repository locator:** [hellangleZ/Agent-MemoryForge](https://github.com/hellangleZ/Agent-MemoryForge)  
**Catalog source attribution:** [Agent Memory Atlas report at catalog revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agent-memoryforge.md)  
**Current canonical repository:** [hellangleZ/Agent-MemoryForge](https://github.com/hellangleZ/Agent-MemoryForge)  
**Default branch / reviewed head:** main / [a582a70394138acc4a19e642ed8c070faf1bfb2e](https://github.com/hellangleZ/Agent-MemoryForge/commit/a582a70394138acc4a19e642ed8c070faf1bfb2e)  
**Review time:** 2026-11-24 18:35:00 UTC (10:35:00 PST; America/Los_Angeles). The repository page, main branch history, and full-SHA commit patch were checked.  
**Published contact:** No contact email was found in the checked official [repository README](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/README.md); the JSON record stores null and that exact source URL.

## Identity and scope

The curated roster places **Agent-MemoryForge** at ordinal 15, slug `agent-memoryforge`, and lists `https://github.com/hellangleZ/Agent-MemoryForge`. Its source attribution points to the catalog’s pinned Atlas report. That attribution establishes the locator only: Atlas descriptions, capability marks, report prose, and layout were not used as assessment evidence.[[roster entry](../data/memory-systems.json)]

The current GitHub repository page identifies the canonical repository and shows `main`; its branch history lists head `a582a70`. The commit patch resolves the full SHA recorded above. This review is tied to that revision.[[repository](https://github.com/hellangleZ/Agent-MemoryForge)] [[main branch history](https://github.com/hellangleZ/Agent-MemoryForge/commits/main)] [[full head patch](https://github.com/hellangleZ/Agent-MemoryForge/commit/a582a70394138acc4a19e642ed8c070faf1bfb2e.patch)]

Agent-MemoryForge is a Python memory service and SDK/Gateway integration for customer-owned agents, with a reference framework and operator portal. Its architecture document separates the public SDK, framework, Memory Service data plane, Product Gateway, and Portal UI.[[README](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/README.md)] [[architecture](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/ARCHITECTURE.md)]

## Architecture and data model

**Code and documentation observations.** The current architecture document describes Markdown files as canonical memory and SQLite FTS as the default derived search index. The File-First backend formats metadata-bearing Markdown entries, writes them under workspace paths, and updates the search index best-effort; the index can be rebuilt from stored files. The README also describes optional vector and graph indexes and Redis operational services; these are derived or supporting components, not the source of truth.[[architecture](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/ARCHITECTURE.md)] [[file backend](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/backends/file_first.py)] [[Markdown entries](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/file_first/entries.py)]

The documented tiers are actor-private short-term conversation summaries (`stm`), active task state (`wm`), and preferences, plus workspace-shared semantic facts and graph relations. Entries carry identifiers, tier/scope, timestamps, tenant/workspace values, and other metadata. Search results provide file path and line citations back to Markdown.[[README](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/README.md)] [[API reference](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/API_REFERENCE.md)] [[entry encoding](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/file_first/entries.py)]

## Write, update, delete, and retrieval

**Write — code observation.** `POST /v1/memory/write` takes tenant/workspace, tier, scope, content, metadata, and a tier-specific target. The backend appends entries for append-style records and atomically replaces files for overwrite-style state. It then best-effort updates its derived index; logging records index failures while the canonical write remains successful. The Gateway authenticates customer requests, forwards the authenticated user identity, and records structured write observability/audit data. The README places memory distillation on an asynchronous worker path outside the chat request.[[API reference](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/API_REFERENCE.md)] [[file backend](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/backends/file_first.py)] [[Gateway](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_runtime/product/gateway/core_routes.py)] [[distillation worker](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/scripts/memory_distill_worker.py)] [[README](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/README.md)]

**Update and delete.** The inspected API reference documents write, search, direct read/get, stats, and index rebuild, but no general memory-delete endpoint. Preferences have a normalized-key upsert path, and overwrite replaces a target file. The documented working-memory TTL can remove expired state on read. Stewardship and temporal recall documentation describes marking items outdated and querying historical state; these features do not establish complete erasure across canonical files and all derived stores.[[API reference](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/API_REFERENCE.md)] [[file backend](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/backends/file_first.py)] [[README](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/README.md)]

**Retrieval.** `POST /v1/memory/search` returns indexed hits with path/line citations and clamps `top_k` to 1–100. The service supports tier, kind, scope, and path-prefix filters; lexical results can be merged with vector results when configured. Direct reads target state-like tiers, while semantic memory is retrieved through search. The documented index rebuild endpoint is disabled by default.[[API reference](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/API_REFERENCE.md)] [[SQLite FTS index](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/file_first/index_sqlite.py)] [[file backend](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/backends/file_first.py)]

## Scope isolation and provenance

**Scope isolation — source observation.** The architecture assigns tenant/workspace checks to the Gateway and requires both IDs at the Memory Service. Private tiers are checked against the actor for search hits and direct reads/writes; semantic and graph tiers are workspace-shared. The inspected service helper defaults a missing `actor_role` to `system`, a privileged role. The Gateway is documented as forwarding authenticated identity, so service-level callers rely on the internal boundary and correctly supplied actor fields. I did not execute or probe these paths.[[architecture](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/ARCHITECTURE.md)] [[API reference](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/API_REFERENCE.md)] [[backend actor checks](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/backends/file_first.py)] [[service request fields](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/app.py)] [[Gateway identity forwarding](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_runtime/product/gateway/core_routes.py)]

**Provenance and evidence.** Markdown entries can include source metadata, and search returns paths and line numbers for inspecting the stored source text. Gateway and distillation code attach source, actor, and trace-related metadata. These citations locate memory records; they do not themselves verify that a record supports a generated claim.[[API reference](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/API_REFERENCE.md)] [[entry encoding](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/file_first/entries.py)] [[Gateway](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_runtime/product/gateway/core_routes.py)] [[distillation worker](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/scripts/memory_distill_worker.py)]

## Source-visible efficiency and observability

**Code observations, not measurements.** SQLite FTS provides keyword retrieval, and optional vector search can be merged with lexical hits. The backend checks for stale indexes, supports rebuild controls, logs failed index updates, and records structured search-event fields. The service can report file counts/bytes and derived-index status. These mechanisms show implementation and operational visibility only; no latency, throughput, token, cost, or storage-efficiency measurements were collected.[[SQLite index](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/file_first/index_sqlite.py)] [[file backend](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/backends/file_first.py)] [[Gateway](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_runtime/product/gateway/core_routes.py)]

## Project metric domains

Every metric domain is **unmeasured** for Agent-MemoryForge. Source code and documentation describe interfaces and mechanisms, not benchmark outcomes. See the project’s [metric definitions](../METRICS.md), [benchmark status](../results/initial-baselines-status.json), and [benchmark fixture](../fixtures/memory-benchmark-v1.json).

## Limits and unknowns

This is a bounded read-only review of the README, architecture/API documentation, and selected service and Gateway source at the verified SHA. No system execution, tests, or benchmarks were performed. Source inspection does not establish runtime reliability, access-control correctness, answer quality, complete deletion, or performance.

The architecture document describes File-First as the current default and only backend, while the README also discusses optional derived vector/graph indexes and Redis. Which optional components are active depends on deployment configuration; I did not trace every configuration and call path.

## Benchmark status

**Benchmark not run.** No Agent-MemoryForge system, benchmark workload, or test suite was run for this review. Project metric definitions and fixtures are protocol, not results.[[metrics](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current repository](https://github.com/hellangleZ/Agent-MemoryForge)
- [Main branch history](https://github.com/hellangleZ/Agent-MemoryForge/commits/main)
- [Full-SHA head patch](https://github.com/hellangleZ/Agent-MemoryForge/commit/a582a70394138acc4a19e642ed8c070faf1bfb2e.patch)
- [README.md](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/README.md)
- [docs/ARCHITECTURE.md](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/ARCHITECTURE.md)
- [docs/API_REFERENCE.md](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/docs/API_REFERENCE.md)
- [agent_memory_service/backends/file_first.py](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/backends/file_first.py)
- [agent_memory_service/file_first/entries.py](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/file_first/entries.py)
- [agent_memory_service/file_first/index_sqlite.py](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/file_first/index_sqlite.py)
- [agent_memory_service/app.py](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_memory_service/app.py)
- [agent_runtime/product/gateway/core_routes.py](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/agent_runtime/product/gateway/core_routes.py)
- [scripts/memory_distill_worker.py](https://github.com/hellangleZ/Agent-MemoryForge/blob/a582a70394138acc4a19e642ed8c070faf1bfb2e/scripts/memory_distill_worker.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster and attribution](../data/memory-systems.json)

**Verification boundary:** no system, tests, or benchmarks were run.

---