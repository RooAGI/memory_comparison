# CORE (ordinal 154)

**Identity:** CORE — slug `core-redplanet`. Listed repository: [RedPlanetHQ/core](https://github.com/RedPlanetHQ/core). Roster attribution: [Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/core-redplanet.md) (identity and locator only; not assessment evidence).

**Review pin:** default branch `main`; full head [`b9da284b13aa64a0938043cde9ce9a46cffe9b5e`](https://github.com/RedPlanetHQ/core/commit/b9da284b13aa64a0938043cde9ce9a46cffe9b5e); reviewed 2026-11-25 09:21:12 UTC (2026-11-25 01:21:12 PST, America/Los_Angeles). The official Git remote resolved symbolic HEAD to `main`; a shallow clone matched this SHA. Its commit timestamp is 2026-11-24T15:51:41+05:30.[[repository](https://github.com/RedPlanetHQ/core)] [[head](https://github.com/RedPlanetHQ/core/commit/b9da284b13aa64a0938043cde9ce9a46cffe9b5e)]

## Summary

CORE is an open-source, self-hosted personal AI workspace with a persistent memory pipeline. This review examines source and documentation at the pinned head; it did not run CORE, tests, or benchmarks.[[README](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/README.md)]

## Who and what

The official README describes a self-hosted product integrating conversations, connected applications, coding-agent workflows, and a temporal memory graph. This assessment focuses on the memory system, not all product features.[[README](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/README.md)]

## Architecture and data model

An Episode retains original content together with source, reference time, session, labels, workspace, and optional end-user identity. Ingestion normalizes and embeds episode content, then extracts world facts and voice facts through model calls. Entity and statement resolution run in follow-on jobs.[[episode model](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/packages/types/src/graph/graph.entity.ts)] [[ingestion](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/knowledgeGraph.server.ts)] [[ingest guide](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/docs/memory/how-core-ingests.mdx)]

Twelve aspects divide between six graph aspects represented as subject-predicate-object triples in Neo4j, and six voice aspects stored as complete statements in Postgres. Both connect facts to source episodes. Embeddings use separate namespaces for entities, statements, episodes, labels, aspects, and compacted sessions.[[memory overview](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/docs/memory/overview.mdx)] [[aspect guide](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/docs/memory/aspects.mdx)] [[voice store](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/aspectStore.server.ts)]

Documented write paths include integration sync, Butler conversations, document uploads, and MCP `memory_ingest`. MCP ingest requires a session ID and accepts optional label IDs; it queues the episode for processing. Documents use content and chunk hashes for versioning; conversations are treated as append-oriented.[[ingestion guide](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/docs/memory/how-core-ingests.mdx)] [[MCP tools](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/utils/mcp/memory.ts)] [[versioning](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/episodeVersioning.server.ts)]

## Write, update, delete, and retrieval

**Write.** `addEpisode` creates or loads an episode, gathers recent session context, normalizes and saves content, stores its embedding, extracts graph triples and voice aspects, and writes embeddings for extracted graph facts and entities. The code records processing times and token-use counters.[[ingestion implementation](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/knowledgeGraph.server.ts)]

**Update and correction.** For changed documents, versioning compares content and chunk hashes; the resolution path can invalidate statements associated with replaced chunks. Graph resolution uses structural and embedding-similarity candidates, then a model classifies duplicates or contradictions. Contradicted statements receive `invalidAt` and `invalidatedBy`; duplicate provenance is moved before the duplicate statement and embedding are deleted. Voice-aspect resolution separately asks a model whether similar entries are duplicates, evolutions, or new facts. These are model-mediated source behaviors; correction accuracy was not measured.[[versioning](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/episodeVersioning.server.ts)] [[graph resolution](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/jobs/ingest/graph-resolution.logic.ts)] [[statement helpers](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/graphModels/statement.ts)] [[aspect resolution](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/jobs/ingest/aspect-resolution.logic.ts)]

**Delete.** The inspected episode-delete path removes the selected episode, statements and entities that become orphaned, associated graph embeddings, and voice aspects whose episode links become empty. A date-range route also deletes recent workspace documents and their sessions. These are source observations about application-store cleanup; this review does not establish erasure from every provider copy, backup, or external integration system.[[episode helpers](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/graphModels/episode.ts)] [[Neo4j delete](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/packages/providers/src/graph/neo4j/domains/episode.ts)] [[date-range delete route](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/routes/api.v1.memory.delete-range.tsx)]

**Retrieval.** V2 resolves the workspace, finds matching topic labels by vector search, then calls a structured language-model router to classify aspects, query type, time, and entity hints. Dedicated handlers cover aspect, entity, temporal, facets, exploratory, and relationship queries; graph, vector, and voice-aspect results can be combined. Optional Cohere reranking is followed by a 10,000-token default budget that drops episodes from the tail. Older workspace versions can fall back to V1 BM25, vector, and graph traversal when V2 returns no results. Returned records retain episode provenance; the reviewed path does not establish claim-level citation quality or answer accuracy.[[search guide](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/docs/memory/how-core-searches.mdx)] [[V2 entry](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/search-v2/index.ts)] [[V2 graph queries](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/packages/providers/src/graph/neo4j/domains/searchV2.ts)] [[V1 graph queries](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/packages/providers/src/graph/neo4j/domains/search.ts)] [[token budget](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/search/tokenBudget.ts)]

## Scope isolation

The V2 entry point validates a requested workspace against active user membership, or selects the user's first active workspace. Graph queries include user predicates and conditionally include workspace predicates; some provider interfaces accept an optional workspace ID. Labels and voice-aspect retrieval also support workspace filters. These are code observations, not isolation test results; this review did not run cross-user or cross-workspace probes.[[workspace resolver](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/models/workspace.server.ts)] [[V2 entry](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/search-v2/index.ts)] [[V2 provider](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/packages/providers/src/graph/neo4j/domains/searchV2.ts)] [[voice store](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/aspectStore.server.ts)]

## Provenance and evidence

Episodes preserve original text and source metadata. Graph statements have temporal fields such as `validAt`, `invalidAt`, and `invalidatedBy`, and link to source episodes; voice aspects retain episode UUIDs. This supports origin and temporal lineage in storage. The inspected model does not establish calibrated confidence, factuality, or answer-level evidence-support scores.[[episode and statement types](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/packages/types/src/graph/graph.entity.ts)] [[ingestion guide](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/docs/memory/how-core-ingests.mdx)] [[voice store](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/aspectStore.server.ts)]

## Efficiency and observability

Ingestion batches embedding writes and logs token counters and processing durations. V2 combines retrieval paths, can rerank, and applies a token ceiling; search logs response time and result counts and writes recall analytics. The telemetry guide describes default feature and error event collection with opt-out settings. These are source and documentation observations, not measured latency, cost, or storage results.[[ingestion implementation](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/knowledgeGraph.server.ts)] [[search entry](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/search-v2/index.ts)] [[token budget](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/search/tokenBudget.ts)] [[telemetry guide](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/docs/TELEMETRY.md)]

## Limits and unknowns

This review covered selected memory guides, ingestion and resolution jobs, persistence helpers, search paths, workspace resolution, deletion, and telemetry. It did not inspect every connector, hosting mode, provider implementation, or UI workflow. Runtime correctness, concurrent ingestion behavior, isolation under adversarial conditions, and complete deletion from every copy remain unestablished by this inspection.

The README reports a LoCoMo accuracy figure and points to a separate benchmark repository. This review did not inspect or reproduce that run; it is not a measurement from this project review. Project metric definitions and the fixture are available in [METRICS.md](../METRICS.md) and [the benchmark fixture](../fixtures/memory-benchmark-v1.json); the [status record](../results/initial-baselines-status.json) contains no result produced by this review.

## Benchmark status

**Benchmark not run.** No CORE runtime, tests, or benchmarks were run. All project quality and efficiency domains remain unmeasured for CORE here.[[metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[result status](../results/initial-baselines-status.json)]

## Published contact

The official pinned [README](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/README.md) lists `harshith@poozle.dev` for vulnerability reports. I recorded it as the published security contact; the README does not present it as general support. No commit/profile metadata, third-party directory, or inferred address was used.

## Sources

- [Official repository](https://github.com/RedPlanetHQ/core)
- [Reviewed commit](https://github.com/RedPlanetHQ/core/commit/b9da284b13aa64a0938043cde9ce9a46cffe9b5e)
- [Pinned README](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/README.md)
- [Memory overview](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/docs/memory/overview.mdx)
- [Ingestion guide](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/docs/memory/how-core-ingests.mdx)
- [Search guide](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/docs/memory/how-core-searches.mdx)
- [Graph resolution](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/jobs/ingest/graph-resolution.logic.ts)
- [V2 search](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/services/search-v2/index.ts)
- [Workspace resolver](https://github.com/RedPlanetHQ/core/blob/b9da284b13aa64a0938043cde9ce9a46cffe9b5e/apps/webapp/app/models/workspace.server.ts)
