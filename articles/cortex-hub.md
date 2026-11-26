# Cortex Hub

## Identity and review pin

- Catalog ordinal: 161
- System: Cortex Hub
- Slug: `cortex-hub`
- Listed repository: https://github.com/lktiep/cortex-hub
- Roster attribution: explicit repository locator; the pinned Atlas entry is recorded for curated identity/locator context only, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortex-hub.md)).
- Canonical upstream: https://github.com/lktiep/cortex-hub
- Default branch: `master`
- Reviewed full head: [173a612df830b70e9d3d8632a4ae95e7b9adf670](https://github.com/lktiep/cortex-hub/commit/173a612df830b70e9d3d8632a4ae95e7b9adf670)
- Review timestamp: 2026-11-25T09:38:33Z (UTC; 2026-11-25 01:38:33 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub’s official repository API identifies the public canonical repository and `master` as its default branch. The official master Atom feed reports head `173a612df830b70e9d3d8632a4ae95e7b9adf670`, updated at 2026-10-30T03:20:03Z, and the official commit page confirms that full revision. ([repository metadata](https://api.github.com/repos/lktiep/cortex-hub), [master history](https://github.com/lktiep/cortex-hub/commits/master.atom), [head commit](https://github.com/lktiep/cortex-hub/commit/173a612df830b70e9d3d8632a4ae95e7b9adf670))

## Summary

Cortex Hub is a self-hosted TypeScript platform that exposes agent memory and a shared knowledge base through MCP. Its mem9 memory path stores facts in Qdrant and combines dense vectors with a lexical BM25 arm; a separate knowledge path stores documents and supports tags, project filters, hall types, validity dates, and file links. This is a source review pinned to the repository head, not a runtime or benchmark assessment. ([README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md), [architecture](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/docs/architecture/overview.md))

## Who and what

The official README describes Cortex Hub as a self-hosted backend for persistent agent memory, shared knowledge, code intelligence, and quality workflows, exposed through an MCP endpoint. It is a deployable platform rather than a hosted memory API; the README names a Docker Compose deployment and local service components. ([README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md), [architecture](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/docs/architecture/overview.md))

## Architecture and data model

The architecture has an MCP gateway, a Hono dashboard API, a web dashboard, Qdrant, GitNexus code graph, and supporting local embedding/LLM services. The memory MCP handlers proxy to dashboard API routes; the dashboard API owns the in-process mem9 instance and Qdrant connection. ([README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md), [architecture](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/docs/architecture/overview.md), [memory tools](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/hub-mcp/src/tools/memory.ts), [mem9 API proxy](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/dashboard-api/src/routes/mem9-proxy.ts))

There are two different memory-like records. mem9 stores a memory string in a Qdrant point with an ID, content hash, `user_id`, `agent_id`, optional metadata, and created/updated timestamps. The knowledge path accepts a title and full content plus tags, project ID, contributing agent, hall type, `validFrom`, file paths, and category; it automatically chunks and embeds documents. ([mem9](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/packages/shared-mem9/src/memory.ts), [knowledge tools](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/hub-mcp/src/tools/knowledge.ts), [README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md))

The README describes SQLite as the application database for sessions, quality, usage, and knowledge metadata, while Qdrant holds vectors. The inspected schema also records API keys and organization bindings, projects, query logs with latency/status, and usage token counts. ([README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md), [architecture](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/docs/architecture/overview.md), [database schema](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/dashboard-api/src/db/schema.sql))

## Write, update, delete, and retrieval

**Memory writes.** The mem9 implementation documents two model calls when an LLM is configured: fact extraction and an ADD/UPDATE/DELETE/NONE decision. It then embeds and writes to Qdrant. Without an LLM, each input message is retained as written before embedding. A normalized-text hash supports exact duplicate detection. An LLM-selected update replaces a point by ID; a selected delete removes it. ([mem9](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/packages/shared-mem9/src/memory.ts), [mem9 API proxy](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/dashboard-api/src/routes/mem9-proxy.ts))

**Memory retrieval.** Search embeds the query and searches the dense vector arm plus a BM25-style sparse arm when the collection supports sparse vectors, then fuses ranks and blends recency. If the collection lacks a sparse index, initialization warns and search falls back to vectors only. The MCP search path checks branch scope before project scope and accumulates results up to the requested limit. The MCP surface also provides deletion by memory ID. ([mem9](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/packages/shared-mem9/src/memory.ts), [memory tools](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/hub-mcp/src/tools/memory.ts))

**Knowledge writes and retrieval.** Knowledge is separate from mem9: its MCP tool forwards a document to the knowledge API with `source="agent"` and the contributing agent ID. Search supports tag, project, hall-type, and `asOf` filters; an ID fetch returns the full document. The README describes invalidation with a `supersededBy` link and a timeline endpoint, as well as recipe capture and derived/fixed lineage. I did not inspect every knowledge route or migration, so those implementation details remain outside this bounded review. ([knowledge tools](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/hub-mcp/src/tools/knowledge.ts), [README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md))

## Scope isolation

The memory MCP tool constructs a `user_id` from caller-supplied project and branch, project alone, or agent identity. The dashboard proxy resolves unscoped calls to the active session project when available; organization-bound keys without a session project use a key-specific bucket. It checks whether a bound key may access a requested project or memory before store, search, or delete. Branch memory search falls back to project scope. These are source-visible controls, not a measured isolation result. ([memory tools](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/hub-mcp/src/tools/memory.ts), [mem9 API proxy](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/dashboard-api/src/routes/mem9-proxy.ts), [database schema](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/dashboard-api/src/db/schema.sql))

## Provenance and evidence

Knowledge records can carry contributing agent, category, tags, hall type, project, file paths, validity start, and the README describes invalidation/supersession and recipe lineage. mem9 points carry agent/user IDs, timestamps, content hash, and optional arbitrary metadata. Retrieved results expose content and IDs, but the inspected memory tool contract does not require source citations or provide a claim-level evidence format for generated answers. ([knowledge tools](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/hub-mcp/src/tools/knowledge.ts), [mem9](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/packages/shared-mem9/src/memory.ts), [README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md))

## Efficiency and observability

The mem9 path uses shared initialization, bounded search results, Qdrant filters, a bounded 1,000-point sample to estimate BM25 average document length, and hybrid-arm over-fetching. Architecture documentation describes per-tool timing and logging; the schema includes query latency/status and model token usage fields. These are implementation mechanisms and observability surfaces, not measured efficiency outcomes. ([mem9](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/packages/shared-mem9/src/memory.ts), [architecture](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/docs/architecture/overview.md), [database schema](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/dashboard-api/src/db/schema.sql))

## Metric-domain evidence

All project benchmark metrics are **unmeasured** for Cortex Hub. Source inspection establishes available mechanisms only. ([metric definitions](../METRICS.md), [project status record](../results/initial-baselines-status.json), [fixture, not run](../fixtures/memory-benchmark-v1.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Hybrid memory search and empty-result responses exist; no cases were scored. |
| Correction accuracy and stale-value rate | Unmeasured | Memory update decisions and knowledge invalidation/supersession are present; no correction workload was run. |
| Deletion leakage | Unmeasured | A memory ID can be deleted; no post-delete probes, physical-storage inspection, or backup checks were made. |
| Scope isolation | Unmeasured | User/agent filters and session/organization project checks are source-visible; no leakage workload was run. |
| Evidence support and citation coverage | Unmeasured | Knowledge carries metadata and lineage, but no claim-level citation contract was established; no claims were adjudicated. |
| Retrieval latency and write-to-recall delay | Unmeasured | The schema can log tool latency; no timings or timed probes were collected. |
| Tokens and cost | Unmeasured | Token-usage fields exist; no runtime counts or charges were collected. |
| Storage efficiency | Unmeasured | Qdrant and SQLite roles are documented; no corpus-attributed size was measured. |

The official README includes upstream benchmark figures and examples. They were not reproduced or independently adjudicated in this review and are not project benchmark results. ([README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md))

## Limits and unknowns

This bounded review inspected the official README and architecture overview, mem9 implementation and MCP/API memory paths, knowledge MCP tools, and database schema. It did not inspect every API route, knowledge migration, deployment override, embedding provider, or integration hook. ([README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md), [architecture](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/docs/architecture/overview.md), [mem9](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/packages/shared-mem9/src/memory.ts), [memory tools](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/hub-mcp/src/tools/memory.ts), [mem9 API proxy](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/dashboard-api/src/routes/mem9-proxy.ts), [knowledge tools](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/hub-mcp/src/tools/knowledge.ts), [schema](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/dashboard-api/src/db/schema.sql))

Source inspection cannot establish runtime correctness, retrieval quality, correction or deletion outcomes, effective deployed key/session grants, data retention or physical erasure, latency, token/cost totals, or storage efficiency. No Cortex Hub runtime, tests, or benchmarks were run. The README’s figures are upstream-reported claims only. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json), [README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md))

The official pinned README was checked for contact; it does not publish a contact email. No commit/profile metadata or third-party directories were used. ([checked official README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md))

## Benchmark status

**Benchmark not run.** Cortex Hub, its tests, and benchmark workloads were not run. The project fixture is a workload specification only; the status record does not provide a Cortex Hub result from this review. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortex-hub.md)
- [Official repository metadata](https://api.github.com/repos/lktiep/cortex-hub)
- [Official master commit feed](https://github.com/lktiep/cortex-hub/commits/master.atom)
- [Reviewed full head 173a612df830b70e9d3d8632a4ae95e7b9adf670](https://github.com/lktiep/cortex-hub/commit/173a612df830b70e9d3d8632a4ae95e7b9adf670)
- [Pinned README](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/README.md)
- [Pinned architecture overview](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/docs/architecture/overview.md)
- [Pinned mem9 implementation](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/packages/shared-mem9/src/memory.ts)
- [Pinned MCP memory tools](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/hub-mcp/src/tools/memory.ts)
- [Pinned mem9 API proxy](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/dashboard-api/src/routes/mem9-proxy.ts)
- [Pinned MCP knowledge tools](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/hub-mcp/src/tools/knowledge.ts)
- [Pinned database schema](https://github.com/lktiep/cortex-hub/blob/173a612df830b70e9d3d8632a4ae95e7b9adf670/apps/dashboard-api/src/db/schema.sql)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
