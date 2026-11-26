# AgenticTrading source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 20 / AgenticTrading / agentictrading  
**Listed repository locator:** [Open-Finance-Lab/AgenticTrading](https://github.com/Open-Finance-Lab/AgenticTrading)  
**Current canonical repository:** [Open-Finance-Lab/AgenticTrading](https://github.com/Open-Finance-Lab/AgenticTrading)  
**Default branch / reviewed head:** main / 9d8fce579dbd57b88a2b6c5f7a19740f62615cbe  
**Review time:** 2026-11-24 18:53:59 UTC (10:53:59 PST; America/Los_Angeles).

## Identity and scope

The curated roster identifies ordinal 20 as AgenticTrading, with the repository locator and Atlas catalog attribution recorded in the companion JSON. I used that catalog only to establish identity, locator, and attribution. Its descriptions, capability marks, and layout were not used to assess the system. GitHub identifies `main` as the default branch; a fresh read of `HEAD` and `refs/heads/main` returned the same full SHA listed above, and a shallow clone resolved to that SHA.[[curated roster](../data/memory-systems.json)] [[GitHub repository](https://github.com/Open-Finance-Lab/AgenticTrading)] [[main ref and current head](https://github.com/Open-Finance-Lab/AgenticTrading/commit/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe)]

AgenticTrading is a research and trading-agent platform. This review focuses on the FinAgent Memory component under `orchestration/FinAgents/memory`, while noting how the shipping dashboard stores run traces separately. The root README describes a FastAPI dashboard and a separate multi-agent orchestration framework; the orchestration README presents the memory agent as a shared context and logging component.[[README.md](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/README.md)] [[orchestration/README.md](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/README.md)]

## Who and what

The official README identifies Open Finance Lab as the project group. The memory component is documented as a Neo4j-backed service exposed through REST, MCP, and A2A interfaces; it is one subsystem inside the broader platform, not the whole dashboard product.[[README.md](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/README.md)] [[memory README](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/README.md)]

## Architecture and data model

**Documentation observation.** The memory README describes three protocol servers over a unified interface and database manager, with Neo4j as the graph store. The current memory server constructs the unified manager and interface with configured connection values, and retains a legacy manager fallback. The repo docs describe the dashboard and orchestration framework as separate platform areas; the dashboard's persisted traces are a distinct store from FinAgent memory.[[memory README](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/README.md)] [[memory_server.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/memory_server.py)] [[dashboard architecture](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/docs/source/lab/architecture.rst)]

**Code observation.** `UnifiedDatabaseManager.store_memory` creates a `Memory` node with generated ID, agent ID, type, serialized content, searchable text, summary, keywords, event/log type, timestamp, optional session and correlation IDs, creation time, and lookup count. It also creates/ensures an agent node and attempts `SIMILAR_TO` relationships based on keyword overlap. The data model does not include a source-document URI or claim-to-evidence record in this write path.[[unified_database_manager.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/unified_database_manager.py)]

**Separate run provenance.** The current dashboard trace schema stores trace/run, agent/version, user, status, initial input, and timestamps, plus ordered events with actor, step/decision/artifact references, payload, parent links, idempotency keys, and schema version. Shared trace validation rejects sensitive-key names and payloads above 64 KiB. This supports an inspectable execution history, but it is separate from the FinAgent memory graph and does not itself establish factual support for a stored claim.[[trace repository](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/dashboard/backend/domain/traces/repository.py)] [[trace common validation](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/dashboard/backend/domain/traces/common.py)]

## Write, update, delete, and retrieval

**Write.** The memory server exposes structured store and batch-store tools. The manager inserts a new graph node for each memory and returns its ID and metadata; the inspected API does not provide an in-place correction/update operation. Store also attempts keyword-overlap links and emits a memory-stored event when the optional stream component is available. The method calls async `index_memory` without awaiting it and supplies only two positional arguments, while the inspected definition requires four. This path does not establish a completed index write; awaiting the call as written would also fail argument binding.[[memory_server.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/memory_server.py)] [[unified_database_manager.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/unified_database_manager.py)] [[intelligent_memory_indexer.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/intelligent_memory_indexer.py)]

**Update and deletion.** The inspected manager exposes no update-by-ID or direct delete-by-ID method. Its pruning path detaches and deletes graph memories older than a configured age when their lookup count is below a threshold; relationship edges are removed with the node. Completeness across the separate optional indexer, stream, backups, and other derived data was not established by this bounded inspection.[[unified_database_manager.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/unified_database_manager.py)] [[memory_server.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/memory_server.py)]

**Retrieval.** The manager offers keyword matching over lowercased content text, summary, and keywords, ordered newest first, with a result limit; a configured indexer selects a semantic-search path. Expanded retrieval starts from search hits and follows `SIMILAR_TO` or `RELATES_TO` links. Structured filtering can accept agent, session, event, and time fields, but those filters are caller-supplied options rather than mandatory scope constraints.[[unified_database_manager.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/unified_database_manager.py)]

## Scope isolation and provenance

**Scope isolation.** The normal keyword query matches all `Memory` nodes, and the semantic candidate query also loads graph memories without an agent predicate. Relationship expansion likewise follows links without checking agent identity. Although a structured filter accepts `agent_id` and `session_id`, those are optional caller inputs; the inspected memory service does not show an authenticated tenant boundary enforcing them. Treat this as a cross-agent isolation limitation in the inspected memory path, not as a claim about every other platform service.[[unified_database_manager.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/unified_database_manager.py)] [[memory_server.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/memory_server.py)]

**Provenance and evidence.** The graph memory records who wrote an item (`agent_id`), event type, time, and optional session/correlation identifiers; graph relationships record contextual links. Those are provenance metadata, not source citations. The dashboard trace event model adds actor and decision/artifact references, but no inspected integration binds a memory result to a verifiable source passage or checks whether evidence supports a generated statement.[[unified_database_manager.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/unified_database_manager.py)] [[trace repository](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/dashboard/backend/domain/traces/repository.py)]

## Source-visible efficiency and observability

The manager configures a Neo4j driver pool (default maximum 50 connections), tracks an operation counter, and creates full-text and structured indexes. Keyword retrieval is limit-bounded; semantic search first loads up to 1,000 graph memories and then fetches details for each selected result. The indexer source supports a SentenceTransformer model when available and otherwise falls back to TF-IDF. The un-awaited, under-argumented async index call noted above means the indexed path's availability and cost cannot be inferred from configuration alone.[[unified_database_manager.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/unified_database_manager.py)] [[intelligent_memory_indexer.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/intelligent_memory_indexer.py)]

The manager logs connection and operation failures and exposes statistics and lookup counts. Several retrieval, pruning, and indexing error paths return empty results or zero counts after logging, which can make a failure look like an empty result to a caller unless the surrounding response is checked. These are source observations; no latency, token, cost, storage, or reliability measurements were collected.[[unified_database_manager.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/unified_database_manager.py)]

## Project metric domains

All benchmark domains are **unmeasured** for this review. The inspected sources show memory search and pruning interfaces, optional graph scope filters, provenance fields, and separate run traces. No workload measured answerable recall or abstention, correction/staleness, deletion leakage, cross-agent isolation, evidence support/citation coverage, latency, write-to-recall delay, tokens/cost, or storage efficiency. Project metric definitions, status, and fixture describe measurement protocol only.[[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded source review of the current root README, memory documentation and service, manager/indexer implementation, dashboard architecture, and trace schema at the verified SHA. The inspected project includes legacy and unified memory paths; this review did not establish which path every deployment uses or validate parity between them. It did not inspect a deployed Neo4j database or authenticate a production service. Retrieval quality, runtime scope isolation, physical deletion across derived stores, and operational performance remain unknown beyond the concrete code paths described above.[[memory README](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/README.md)] [[unified_database_manager.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/unified_database_manager.py)] [[trace repository](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/dashboard/backend/domain/traces/repository.py)]

## Contact-list follow-up

I checked the official root README and the official orchestration README's Contact & Support section. They publish links to documentation, issues, and discussions, but no contact email; no address was inferred or taken from commit metadata or personal profiles. The JSON record stores `contact_email: null` and the exact checked source URLs.[[README.md](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/README.md)] [[orchestration/README.md](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/README.md)]

## Benchmark status

**Benchmark not run.** No AgenticTrading/FinAgent memory execution, tests, or benchmark workload was run. Code and documentation observations above are not measured results. See the project metric definitions, status record, and fixture for the separate protocol.[[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical GitHub repository and default branch](https://github.com/Open-Finance-Lab/AgenticTrading)
- [Reviewed full main head commit](https://github.com/Open-Finance-Lab/AgenticTrading/commit/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe)
- [README.md](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/README.md)
- [FinAgent orchestration README](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/README.md)
- [FinAgent memory README](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/README.md)
- [unified_database_manager.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/unified_database_manager.py)
- [intelligent_memory_indexer.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/intelligent_memory_indexer.py)
- [memory_server.py](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/orchestration/FinAgents/memory/memory_server.py)
- [Dashboard architecture](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/docs/source/lab/architecture.rst)
- [Trace repository](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/dashboard/backend/domain/traces/repository.py)
- [Trace common validation](https://github.com/Open-Finance-Lab/AgenticTrading/blob/9d8fce579dbd57b88a2b6c5f7a19740f62615cbe/dashboard/backend/domain/traces/common.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status record](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster identity and source attribution](../data/memory-systems.json)

**Verification boundary:** the system, tests, and benchmarks were not run.
