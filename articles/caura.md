# Caura — source review

## Identity and review pin

- **Roster ordinal / name / slug:** 114 / Caura / `caura`
- **Listed repository locator:** https://github.com/caura-ai/caura
- **Roster attribution:** `repository_status: explicit`; Atlas locator retained for identity only.[[curated roster](../data/memory-systems.json)] [[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/caura.md)]
- **Canonical upstream / default branch:** [caura-ai/caura](https://github.com/caura-ai/caura) / `main`
- **Reviewed head:** [8dbb7f40a76cdc75827923f1a82597b4c8393130](https://github.com/caura-ai/caura/commit/8dbb7f40a76cdc75827923f1a82597b4c8393130)
- **Official main feed:** [main commit feed](https://github.com/caura-ai/caura/commits/main.atom) reports this head at 2026-11-25 07:30:29 UTC.
- **Reviewed:** 2026-11-25 07:44:46 UTC (2026-11-24 23:44:46 PST; America/Los_Angeles)
- **Status:** Reviewed from code; benchmark not run

## Summary

Caura is an open-source memory service for multi-agent fleets, exposing REST and MCP interfaces. It stores scoped, attributed memories and supports hybrid retrieval, lifecycle and correction workflows. This review describes official source and documentation; it is not a runtime or benchmark evaluation.[[README](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/README.md)] [[fleet memory guide](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/agent-fleet-memory.md)]

## Who and what

The official project describes Caura as a memory layer separate from agent runtimes. The repository documents REST and MCP, client libraries, and an OpenClaw integration; managed and self-hosted setups differ in how agent identity and credentials are provisioned.[[README](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/README.md)] [[fleet memory guide](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/agent-fleet-memory.md)]

## Architecture and data model

The self-hosted design separates the FastAPI core API, which owns REST/MCP and business logic, from a core-storage API that owns PostgreSQL CRUD and migrations. PostgreSQL with pgvector stores memories; Redis and worker/operations services support configured caches, asynchronous work, and lifecycle processing.[[API reference](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/api-reference.md)] [[README](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/README.md)]

The inspected memory model includes tenant, optional fleet, agent, type, content, embedding, weight, source URI, and run ID. It defines verification states and derives `tool_observed` when a row has a real source URI or tool-call ID; `corroborated` is reserved in the cited model contract.[[memory model](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/common/models/memory.py)]

## Write, update, delete, and retrieval

**Write.** Documented REST/MCP writes accept content and identity/scope metadata. With a configured provider, the system enriches a write with classification and other metadata; keyless standalone mode uses deterministic local heuristics and keyword retrieval without embeddings. The model marks verification as server-derived. No write was sent during this review.[[README](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/README.md)] [[API reference](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/api-reference.md)] [[memory model](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/common/models/memory.py)]

**Update and correction.** The project documents corrections as superseding stale memories while retaining lineage and exposes correction workflows. The inspected sources do not establish that every correction refreshes all derived artifacts or that corrections are accurate in practice.[[fleet memory guide](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/agent-fleet-memory.md)] [[API reference](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/api-reference.md)]

**Delete and forgetting.** The API includes deletion and the project documents lifecycle processing. Its deletion matrix lists copies that can persist beyond a memory deletion, including correction/conflict records, digests, skill documents, bus notices, and logs; retention or organization purge handles some of these later.[[API reference](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/api-reference.md)] [[deletion matrix](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/deletion-matrix.md)]

**Retrieval.** The README describes hybrid vector, full-text, and graph-expanded recall with composite ranking. The documented visibility tiers are `scope_agent`, `scope_team`, and governed cross-fleet `scope_org`; callers can identify fleet and agent scope. These are retrieval mechanisms, not measured answer quality.[[README](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/README.md)] [[fleet memory guide](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/agent-fleet-memory.md)]

**Scope isolation.** Project documentation places tenant and visibility checks inside service operations and explains separate credential boundaries for managed and self-hosted deployments. The self-hosted guide requires callers to pass the correct explicit agent identity. This review did not test authorization or cross-scope isolation.[[fleet memory guide](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/agent-fleet-memory.md)] [[API reference](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/api-reference.md)]

**Provenance and evidence.** Rows carry agent identity and source/run metadata, and the model derives a limited verification state from source evidence. The docs also describe audit records and identify the writing agent on shared recall. That supports tracing, but it does not prove every generated answer is supported by a source citation.[[memory model](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/common/models/memory.py)] [[fleet memory guide](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/agent-fleet-memory.md)]

**Efficiency and observability.** The API reference publishes configuration-specific single-instance latency figures; they are upstream documentation claims, not measurements from this review. OpenTelemetry spans can report operation, tenant, record, agent, scope, trust, policy decisions, and payload size. Content is not exported by these spans, while query capture requires an explicit setting.[[API reference](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/api-reference.md)] [[OpenTelemetry guide](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/opentelemetry.md)]

## Limits and unknowns

The architecture guide states that it is not a fleet-scale benchmark and calls for workload-specific validation of throughput, latency, retrieval quality, concurrency, and policy. This review did not trace every storage query, authorization route, migration, worker, or deletion cascade; it cannot establish answer quality, correction accuracy, complete erasure, deployment isolation, latency distributions, cost, or storage efficiency.[[fleet memory guide](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/agent-fleet-memory.md)] [[deletion matrix](https://github.com/caura-ai/caura/blob/8dbb7f40a76cdc75827923f1a82597b4c8393130/docs/deletion-matrix.md)]

## Benchmark status

**Not run.** Project metrics, fixture, and execution-status records describe the protocol only. No Caura system, benchmark, or test was run.[[metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Contact

The official website lists **info@caura.ai**.[[official website](https://caura.ai/)]

