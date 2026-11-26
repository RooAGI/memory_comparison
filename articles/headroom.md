# Headroom source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 285 / Headroom / headroom  
**Listed repository locator:** [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom)  
**Current canonical repository:** [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom)  
**Default branch / reviewed head:** main / `d2014cb948d27bd9d411b147a6d203363f70b912`  
**Review time:** 2026-11-25 22:36:50 UTC (14:36:50 PST; America/Los_Angeles).

## Identity and scope

The curated roster places Headroom at ordinal 285, with slug `headroom`, listed repository locator `https://github.com/headroomlabs-ai/headroom`, and Atlas attribution pinned to revision `19199a4fc249e89c0793be06f0b166b358089ba0`. The official GitHub repository API reports the canonical repository and default branch `main`; its current `commits/main` endpoint identifies the reviewed full SHA above. Atlas is used only for roster identity and locator context, not for this assessment.[[curated roster](../data/memory-systems.json)] [[repository metadata](https://api.github.com/repos/headroomlabs-ai/headroom)] [[current main head](https://api.github.com/repos/headroomlabs-ai/headroom/commits/main)]

## Summary

Headroom is primarily an LLM context-compression library, proxy, and agent integration suite. Its optional persistent-memory subsystem adds hierarchical memory records and retrieval for applications and wrapped agents. The review covers that memory feature and its project-aware proxy storage, while treating the wider compression product as context rather than memory evidence.[[README](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/README.md)] [[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)]

## Who and what

The official README identifies Headroom as open source under Apache 2.0 and describes its library, proxy, MCP server, and coding-agent integrations. The official memory guide documents the `with_memory()` provider wrapper and direct memory API; this is software integrated into applications, not a hosted memory service by default.[[README](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/README.md)] [[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)]

## Architecture and data model

The `HierarchicalMemory` orchestrator coordinates a persistent store, vector index, full-text index, embedder, and optional cache, assembled through a configuration factory. The guide describes the local stack as SQLite for CRUD/filtering, HNSW for vector similarity, and FTS5 for keyword search; the current `LocalBackend` source instead names SQLite-vec for vector search and a persistent SQLite graph store. This documentation/source difference is unresolved here. Configuration can select other backends and adapters.[[core.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/core.py)] [[ports.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/ports.py)] [[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)]

A `Memory` record contains text, user and optional session/agent/turn identifiers, created and validity timestamps, importance, supersession and promotion lineage, access counters, entity references, optional embedding, and free-form metadata. Scope level is derived from the narrowest populated identifier. The guide notes that category is not a dedicated model field or `add()` argument; examples store categories in metadata.[[models.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/models.py)] [[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)]

The documented `with_memory()` wrapper injects retrieved memories into prompts and extracts a memory block from model responses for storage. The source also exposes a `MemorySystem` tool dispatcher and a backend protocol. This means the exact write and retrieval path depends on integration and configuration.[[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)] [[system.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/system.py)]

## Write, update, delete, and retrieval

**Write — code and documentation observations.** `HierarchicalMemory.add()` accepts content, a required user ID, optional session/agent/turn scope, importance, entities, metadata and embedding/bubbling controls. The orchestrator can generate an embedding and coordinate persistence and indexes. The wrapper's documented extraction happens inline with the model response. Neither path establishes extraction accuracy.[[core.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/core.py)] [[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)]

**Update and correction — code observation.** `update()` modifies a stored record and re-indexes changed content. `supersede()` instead closes the old record's validity and adds a linked replacement while retaining history; normal search excludes superseded records unless requested. The docs demonstrate history inspection, but no correction or stale-value workload was run.[[core.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/core.py)] [[models.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/models.py)] [[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)]

**Delete — code observation.** `delete()` removes the memory from the store, vector index, text index, and cache; `clear_scope()` removes memories in a specified scope. This path does not establish complete erasure from backups, remote adapters, replicas, or exports.[[core.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/core.py)]

**Retrieval — code and documentation observations.** `search()` embeds the query and runs filtered vector search; `text_search()` uses the full-text index with BM25; `query()` delegates structured filters to the store. The API exposes top-k, similarity, user/session/agent, scope-level, and superseded-state controls. The guide describes injecting retrieved results into the prompt. No recall or answer-quality measurement was made.[[core.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/core.py)] [[ports.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/ports.py)] [[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)]

## Scope isolation

Records have user, session, agent, and turn scope fields, and memory queries accept corresponding filters. In proxy mode the project router can open a separate SQLite database for each resolved project. It resolves scope from explicit project headers, a configured root, or supported client working-directory context. The documented default for unresolved project scope is fail closed and skip memory; USER and GLOBAL modes and a configured global fallback intentionally share storage. No cross-user, cross-agent, or cross-project probes were run.[[models.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/models.py)] [[core.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/core.py)] [[storage_router.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/storage_router.py)] [[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)]

## Provenance and evidence

The record model retains scope, timestamps, validity, lineage, entity references, and arbitrary metadata, but the inspected model does not require a source passage or citation field. A supersession chain can show record history, but does not establish what source supports the memory or a later generated claim. The documented injection/extraction flow is not a citation guarantee.[[models.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/models.py)] [[core.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/core.py)] [[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)]

## Efficiency and observability

The source separates persistence, vector and text indexes, embedding, and cache, with query bounds and access counters/timestamps. The memory guide publishes latency/storage figures; the README also describes token savings and dashboard/doctor commands. These are project documentation statements, not measurements from this review. The guide says the memory stats method currently returns a total count; this review did not establish detailed memory-specific tracing, per-category metrics, or measured storage efficiency.[[core.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/core.py)] [[models.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/models.py)] [[README](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/README.md)] [[Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)]

## Metric-domain evidence

All benchmark domains are **unmeasured**. The source contains retrieval and scope mechanisms but no adjudicated answerable-recall, abstention, correction, stale-value, deletion-leak, scope-leak, evidence-support, or citation-coverage results. This review collected no operation latency, write-to-recall delay, token or provider-cost totals, or corpus storage bytes. Published guide figures are not this project's benchmark results.[[project metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded read-only inspection of the pinned README, official Persistent Memory guide, and selected source for memory records, operations, backend interfaces, and project routing. The system, tests, and benchmark workload were not run. Runtime quality, production reliability, security properties, adapter parity, complete deletion, and actual performance remain unknown. Storage modes have different sharing boundaries, so their isolation behavior should not be treated as interchangeable.[[README](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/README.md)] [[models.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/models.py)] [[core.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/core.py)] [[system.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/system.py)] [[storage_router.py](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/storage_router.py)]

## Contact

The official README publishes `hello@headroomlabs.ai` in its Headroom for Teams contact section. No profile or commit metadata, inferred address, or third-party directory was used.[[official README contact](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/README.md)]

## Benchmark status

**Benchmark not run.** No Headroom runtime, tests, or benchmark workload was run. The project's metric definitions and fixture describe a protocol; its execution-status record is separate from measured results.[[project metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Official repository](https://github.com/headroomlabs-ai/headroom)
- [Current main head](https://github.com/headroomlabs-ai/headroom/commit/d2014cb948d27bd9d411b147a6d203363f70b912)
- [README.md](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/README.md)
- [Persistent Memory guide](https://docs.headroomlabs.ai/docs/memory)
- [Memory models](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/models.py)
- [Memory operations](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/core.py)
- [MemorySystem and backend protocol](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/system.py)
- [Memory storage router](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/storage_router.py)
- [Local memory backend](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/backends/local.py)
- [Memory backend ports](https://github.com/headroomlabs-ai/headroom/blob/d2014cb948d27bd9d411b147a6d203363f70b912/headroom/memory/ports.py)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution status](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster and Atlas attribution](../data/memory-systems.json)

**Verification boundary:** Headroom, tests, and benchmarks were not run.
