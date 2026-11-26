# Forgetful

## Identity and review pin

- **Catalog position:** 246, “Forgetful”; slug `forgetful`.
- **Listed repository:** [scottrbk/forgetful](https://github.com/scottrbk/forgetful); the locator is explicit in the catalog. The pinned Atlas entry is roster attribution only.
- **Canonical upstream:** [ScottRBK/forgetful](https://github.com/scottrbk/forgetful), default branch `main`.
- **Reviewed head:** `3b816f97f4ff20d26fd47f559b9a7567ba427c00`, verified against the official [main commit feed](https://github.com/scottrbk/forgetful/commits/main.atom) and matching commit page.
- **Reviewed:** 2026-11-25 23:42:52 UTC (2026-11-25 15:42:52 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) supplies the ordinal, identity, listed repository, and Atlas attribution. The [pinned Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/forgetful.md) is used only for curated identity and locator attribution, never as assessment evidence.

## Summary

Forgetful is a self-hostable memory and knowledge service for agents, exposed through MCP, HTTP, and a CLI. It stores atomic memory records with embeddings and links, supports SQLite or PostgreSQL, and offers semantic retrieval with optional reranking and hybrid keyword search.

## Who and what

The official README describes Forgetful as an open-source MCP storage and retrieval tool for agents that share a knowledge base. It also provides HTTP APIs and a CLI over the tool registry. This review does not assign maintainer identity beyond what the official sources state.[[README](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/README.md)] [[repository](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/models/memory_models.py)]

## Architecture and data model

The code follows a routes → services → repository protocols → SQLite/PostgreSQL adapters shape. The bootstrap composes the selected database, embedding/reranking providers, services, events, and MCP tool registry. This is one application with selectable adapters rather than separate memory services.[[architecture](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/architecture.md)]

A memory is a single concept with title, content, context, keywords, tags, importance, and creation/update metadata. It can be associated with projects, documents, code artifacts, files, and skills. Optional provenance fields include source repository/files/URL, confidence, encoding process, agent identity/version, and model. Embeddings support retrieval; links connect related memories and query results may expand one hop into linked memories.[[memory model](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/models/memory_models.py)] [[README](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/README.md)]

SQLite is the zero-configuration default and uses sqlite-vec for vectors; PostgreSQL uses pgvector. The search guide documents an optional keyword leg backed by SQLite FTS5 or PostgreSQL tsvector/GIN. Similarity links form a lightweight knowledge graph alongside entity, project, document, and other records.[[SQLite repository](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/repositories/sqlite/memory_repository.py)] [[PostgreSQL repository](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/repositories/postgres/memory_repository.py)] [[search guide](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/docs/search.md)]

## Write, update, delete, and retrieval

**Write.** Agents explicitly create atomic memories; the request model validates content and supports metadata, provenance, and associations. The service applies configured provenance defaults, persists the record, and may then search for similar memories and create links. The architecture notes that persistence and auto-linking are separate repository calls, so the overall flow is not one service-wide transaction.[[memory model](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/models/memory_models.py)] [[memory service](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/services/memory_service.py)] [[architecture](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/architecture.md)]

**Update and deletion.** The API supports partial updates to memory fields. Forgetful also documents a lifecycle operation to mark a memory obsolete with a reason and optional replacement; this is a soft lifecycle state that keeps the record available for direct lookup while excluding it from active search. The reviewed sources do not establish physical erasure from database files, backups, or other retained copies.[[memory service](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/services/memory_service.py)] [[memory model](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/models/memory_models.py)] [[README](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/README.md)]

**Retrieval.** Querying searches user-owned memories, returns ranked primary results, may add one-hop linked memories, and applies result count/token budgets. Dense vector search is the default; optional reranking reorders candidates. Hybrid search is opt-in and combines dense and keyword rankings with reciprocal-rank fusion; SQLite uses FTS5 and PostgreSQL uses tsvector/GIN. Query context enriches reranking, while project filtering applies to primary results and is also applied to linked results only when strict project filtering is requested.[[memory service](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/services/memory_service.py)] [[SQLite repository](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/repositories/sqlite/memory_repository.py)] [[PostgreSQL repository](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/repositories/postgres/memory_repository.py)] [[search guide](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/docs/search.md)]

**Scope isolation.** The reviewed architecture and repositories pass an authenticated internal user ID into repository calls and apply user ownership conditions in storage queries. Project filters are an additional organization/query constraint, not a substitute for user identity. The review did not run adversarial cross-user or deployment tests.[[architecture](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/architecture.md)] [[SQLite repository](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/repositories/sqlite/memory_repository.py)] [[PostgreSQL repository](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/repositories/postgres/memory_repository.py)]

## Provenance and evidence

Optional provenance fields can attribute a memory to source files, a repository or URL, and an encoding agent/model; operators can configure defaults, with an option to override caller-supplied values. These fields record asserted origin metadata, not independent verification of the memory's truth. Search returns stored memory records and scores; this review did not assess whether recalled claims are supported by their recorded sources.[[memory model](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/models/memory_models.py)] [[architecture](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/architecture.md)] [[concepts guide](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/docs/concepts.md)]

## Efficiency and observability

The system supports local embedding and reranking, bounded search candidates, result count/token limits, and incremental use of either a local SQLite store or PostgreSQL. Optional activity events cover writes and access tracking; architecture documentation describes event delivery as asynchronous and not a durable queue. These are code and documentation observations, not measured performance or reliability results.[[README](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/README.md)] [[search guide](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/docs/search.md)] [[architecture](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/architecture.md)]

The search guide reports synthetic vector-versus-hybrid retrieval figures for a committed 300-memory corpus. Those upstream-reported figures are not reproduced or independently evaluated here. No latency, token, cost, or storage measurement was collected.[[search guide](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/docs/search.md)]

## Metric-domain evidence

| Domain | Source evidence | Review status |
| --- | --- | --- |
| Answerable recall and abstention | Dense and optional hybrid retrieval are visible in docs/code; no answerability or abstention workload was evaluated. | Unmeasured |
| Correction and stale values | Patch updates and obsolete lifecycle are documented; no correction/staleness probes were run. | Unmeasured |
| Deletion leakage | Obsolescence removes a record from active search; physical erasure across backups/copies was not established and no leakage probes were run. | Unmeasured |
| Scope isolation | User ID filters and optional project filters are visible in repositories; no adversarial cross-user workload was run. | Unmeasured |
| Evidence support and citations | Provenance fields record asserted source metadata; no returned fact was adjudicated against evidence. | Unmeasured |
| Retrieval latency and write-to-recall delay | Search and indexing paths are visible; no timings were collected. | Unmeasured |
| Tokens and cost | Result budgets and provider choices are documented; no token or cost workload was measured. | Unmeasured |
| Storage efficiency | SQLite and PostgreSQL persistence and vector indexes are visible; no bytes-per-memory measurement was made. | Unmeasured |
| Operational observability | Logging, optional activity events, and access counters are source-visible; no live reliability or telemetry interval was collected. | Unmeasured |

These are implementation observations, not benchmark results. Project metric definitions are in [METRICS.md](../METRICS.md); the [fixture](../fixtures/memory-benchmark-v1.json) and [initial status record](../results/initial-baselines-status.json) describe the project protocol/status, not Forgetful measurements.

## Limits and unknowns

This is a source review of the official repository at the recorded SHA. It did not run Forgetful, tests, or benchmarks. It cannot establish retrieval accuracy, calibrated abstention, correction quality, deletion leakage, adversarial scope isolation, SQLite/PostgreSQL behavioral parity, provider behavior, production reliability, or actual resource use. The security policy warns that HTTP listens on all interfaces and has no authentication unless configured; safe deployment requires binding locally or configuring authentication and TLS termination.[[architecture](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/architecture.md)] [[security policy](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No Forgetful runtime, tests, or benchmark workload was executed for this review. See [project metric definitions](../METRICS.md), the [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial benchmark status](../results/initial-baselines-status.json).

## Contact

The pinned official [README](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/README.md) and [SECURITY.md](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/SECURITY.md) were checked for a contact email. Neither publishes an email; SECURITY.md directs vulnerability reports through GitHub private vulnerability reporting. No address was inferred and no commit/profile metadata or third-party directory was used.

## Sources

- [Official repository](https://github.com/scottrbk/forgetful), [main commit feed](https://github.com/scottrbk/forgetful/commits/main.atom), and [reviewed commit](https://github.com/scottrbk/forgetful/commit/3b816f97f4ff20d26fd47f559b9a7567ba427c00) — identity, branch, and head.
- [README](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/README.md), [architecture](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/architecture.md), [memory models](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/models/memory_models.py), and [memory service](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/services/memory_service.py) — product, architecture, schema, and operations.
- [SQLite repository](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/repositories/sqlite/memory_repository.py), [PostgreSQL repository](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/app/repositories/postgres/memory_repository.py), and [search guide](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/docs/search.md) — storage and retrieval.
- [Concepts guide](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/docs/concepts.md) and [security policy](https://github.com/scottrbk/forgetful/blob/3b816f97f4ff20d26fd47f559b9a7567ba427c00/SECURITY.md) — provenance and deployment guidance.
- Project-owned [METRICS.md](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), [initial result status](../results/initial-baselines-status.json), and [catalog](../data/memory-systems.json).

---