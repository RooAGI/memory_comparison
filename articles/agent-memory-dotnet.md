# AgentMemory for .NET source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 23 / AgentMemory for .NET / agent-memory-dotnet  
**Listed repository locator:** [joslat/agent-memory-dotnet](https://github.com/joslat/agent-memory-dotnet)  
**Catalog source attribution:** [Agent Memory Atlas report at catalog revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agent-memory-dotnet.md)  
**Current canonical repository:** [joslat/agent-memory-dotnet](https://github.com/joslat/agent-memory-dotnet)  
**Default branch / reviewed head:** main / [53f4cf8030fb53a33da9da0c1544f911511eaa0f](https://github.com/joslat/agent-memory-dotnet/commit/53f4cf8030fb53a33da9da0c1544f911511eaa0f)  
**Review time:** 2026-11-24 19:02:32 UTC (11:02:32 PST; America/Los_Angeles). GitHub shows `main` as the default branch and the main-branch Atom feed gives the full head SHA above.  
**Published contact:** No email was found in the checked official [README at the reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md) or [SECURITY.md](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/SECURITY.md); the JSON stores null and the exact checked security-policy URL.

## Identity and scope

The curated roster places **AgentMemory for .NET** at ordinal 23, slug `agent-memory-dotnet`, and lists `https://github.com/joslat/agent-memory-dotnet`. The roster attributes the entry to the Atlas report at revision `19199a4fc249e89c0793be06f0b166b358089ba0`. This establishes selected identity and locator only; Atlas descriptions, marks, report prose, and layout were not used as assessment evidence.[[roster entry](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agent-memory-dotnet.md)]

GitHub identifies `joslat/agent-memory-dotnet` as the canonical repository and `main` as its default branch. The main-branch Atom feed resolves head `53f4cf8030fb53a33da9da0c1544f911511eaa0f`; the commit page confirms the full SHA. All upstream documentation and source links below are pinned to that revision.[[repository](https://github.com/joslat/agent-memory-dotnet)] [[main branch history](https://github.com/joslat/agent-memory-dotnet/commits/main.atom)] [[full head](https://github.com/joslat/agent-memory-dotnet/commit/53f4cf8030fb53a33da9da0c1544f911511eaa0f)]

AgentMemory for .NET is an independent .NET framework for persistent agent memory backed by Neo4j. Its README describes it as early-stage and actively developed, maintained by its author without an SLA or support contract. The repository names José Luis Latorre Millas as the author of its associated research paper. This review covers the public repository and selected code paths, not a hosted service.[[README](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)]

## Architecture and data model

**Code and documentation observations.** The architecture separates framework-independent abstractions and core orchestration from Neo4j infrastructure. Core coordinates extraction, embedding, resolution, recall assembly, and formatting. The Neo4j package owns repositories, Cypher, schema, and transactions. Adapters connect the core to Microsoft Agent Framework, Semantic Kernel, MCP, and GraphRAG-related context.[[architecture](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/architecture.md)] [[README](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)]

The public model has three memory layers: short-term conversation/message history; long-term entities, facts, preferences, and relationships; and reasoning traces, steps, and tool calls. A fact stores subject, predicate, object, owner, timestamps, optional validity dates, metadata, and source message IDs. Its Neo4j upsert uses a canonical subject/predicate/object key together with an owner key, keeping an owner’s fact distinct from the shared bucket.[[architecture](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/architecture.md)] [[README](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)] [[fact repository](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Neo4j/Repositories/Neo4jFactRepository.cs)]

## Write, update, delete, and retrieval

**Write and update — source observations.** Messages can be written directly; extraction paths turn conversation content into structured entities, facts, preferences, and relationships. Fact upsert preserves display text and source message IDs while matching on canonical values and owner. The documented extraction pipeline supports best-effort per-item outcomes and a fail-fast mode.[[README](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)] [[fact repository](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Neo4j/Repositories/Neo4jFactRepository.cs)] [[Memory Map](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/memory-map.md)]

**Change and delete.** Supersession/invalidation generally closes a record with timestamps and a relationship to its replacement, retaining history. The README says long-term soft invalidation is the default and hard deletion is opt-in. Bitemporal change recording is configurable and off by default. The reviewed paths do not establish complete physical erasure across every memory type, audit record, and derived copy.[[README](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)] [[time model](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/time-model.md)] [[Memory Map](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/memory-map.md)]

**Retrieval.** The memory service routes a request, assembles context, and applies configured per-section and overall budgets. Long-term retrieval includes vector search and optional predicate expansion; configuration and adapters expose other retrieval paths, including full-text, hybrid, graph traversal, and GraphRAG context. Code also contains point-in-time retrieval and optional shared-memory budget splitting. These are implementation observations, not measured recall quality.[[MemoryService](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Core/Services/MemoryService.cs)] [[LongTermMemoryService](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Core/Services/LongTermMemoryService.cs)] [[architecture](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/architecture.md)]

## Scope isolation, provenance, and evidence

**Scope isolation — source observation.** Owner scope is carried through long-term repositories and recall. The default isolation mode preserves global behavior for missing owner context; `WarnOnUnscoped` logs and `StrictMultiTenant` rejects unscoped tenant operations. The README documents a short-term exception: message nodes have no `owner_id`, and possession of a session ID permits direct reads by handle. Multi-tenant hosts must establish owner scope and protect session IDs as capabilities.[[isolation policy](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Core/Services/DefaultMemoryIsolationPolicy.cs)] [[README](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)] [[Memory Map](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/memory-map.md)]

**Provenance and evidence.** Facts and other extracted records can link back to source messages through stored source IDs and `EXTRACTED_FROM` relationships. The Memory Map notes that the `EXTRACTED_BY` relationship writer has no production caller in the inspected default path and span-level provenance arguments are not populated there. Provenance identifies origin; it does not by itself establish that an answer is supported by a source passage.[[README](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)] [[fact repository](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Neo4j/Repositories/Neo4jFactRepository.cs)] [[Memory Map](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/memory-map.md)]

## Source-visible efficiency and observability

**Code and documentation observations, not measurements from this review.** The OpenTelemetry guide documents recall, composition, extraction, embedding, and database spans, including returned item counts, embedding-cache counts, extraction outcomes, query fingerprints, server timings, rows read, and transaction retries. It says a listener/exporter is required and excludes memory text, prompts, Cypher text, and owner/application IDs from span attributes. The fact repository also has an option to omit embedding vectors from recall projections. These surfaces provide operational signals but this review collected no runtime measurements.[[observability guide](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/observability.md)] [[fact repository](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Neo4j/Repositories/Neo4jFactRepository.cs)] [[MemoryService](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Core/Services/MemoryService.cs)]

## Metric-domain evidence

| Domain | Status for this review | Source evidence |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Vector/graph retrieval and context assembly are present in source; no recall probes were run.[[LongTermMemoryService](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Core/Services/LongTermMemoryService.cs)] [[metrics](../METRICS.md)] |
| Correction and stale-value behavior | Unmeasured | The time model documents supersession and historical reads; no correction probes were adjudicated.[[time model](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/time-model.md)] [[metrics](../METRICS.md)] |
| Deletion leakage | Unmeasured | Soft invalidation is the documented default; no post-delete probes or erasure workload ran.[[README](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)] [[metrics](../METRICS.md)] |
| Scope-isolation leakage | Unmeasured | A strict isolation mode exists, but no cross-owner benchmark ran; short-term reads by session handle are a documented exception.[[isolation policy](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Core/Services/DefaultMemoryIsolationPolicy.cs)] [[README](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)] [[metrics](../METRICS.md)] |
| Evidence support and citation coverage | Unmeasured | Source-message provenance exists on extracted records; answer claims were not scored against evidence.[[fact repository](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Neo4j/Repositories/Neo4jFactRepository.cs)] [[metrics](../METRICS.md)] |
| Latency and write-to-recall delay | Unmeasured | Telemetry exposes timing signals, but no timed workload ran.[[observability guide](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/observability.md)] [[metrics](../METRICS.md)] |
| Tokens, cost, and storage efficiency | Unmeasured | Provider telemetry can expose token usage; this review collected no token, cost, or corpus-attributed storage totals.[[observability guide](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/observability.md)] [[metrics](../METRICS.md)] |

**Benchmark status:** not run. Project metric definitions and the execution-status record are linked below. The fixture describes planned cases only and is not a result.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

- This is a bounded read-only review of the pinned README, selected architecture, security, time and observability docs, and selected core/Neo4j source paths. Other adapters, extensions, operations, and edge cases were not exhaustively traced.
- No AgentMemory system, tests, or benchmark workload was executed. Runtime correctness, answer quality, deployed tenant isolation, complete physical erasure, and metric values remain unverified.
- The default keeps unscoped global behavior for compatibility. Short-term by-handle reads rely on a session ID as a capability, so host scoping and identifier handling are consequential.
- Valid-time live filtering and bitemporal change recording depend on configuration. The time-model document says ordinary live recall ignores valid time unless enabled; preferences, entities, and relationship edges also have different temporal coverage.[[time model](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/time-model.md)]
- The README describes the project as early-stage, with no SLA or support contract.[[README](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)]

## Sources

- [Official README at reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/README.md)
- [Architecture documentation at reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/architecture.md)
- [Memory Map at reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/memory-map.md)
- [Time model at reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/time-model.md)
- [Observability guide at reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/docs/observability.md)
- [Security policy at reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/SECURITY.md)
- [MemoryService source at reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Core/Services/MemoryService.cs)
- [LongTermMemoryService source at reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Core/Services/LongTermMemoryService.cs)
- [Neo4jFactRepository source at reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Neo4j/Repositories/Neo4jFactRepository.cs)
- [DefaultMemoryIsolationPolicy source at reviewed revision](https://github.com/joslat/agent-memory-dotnet/blob/53f4cf8030fb53a33da9da0c1544f911511eaa0f/src/AgentMemory.Core/Services/DefaultMemoryIsolationPolicy.cs)
- [Curated roster entry](../data/memory-systems.json)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution-status record](../results/initial-baselines-status.json)
- [Benchmark fixture (planned workload)](../fixtures/memory-benchmark-v1.json)
