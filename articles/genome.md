# GENOME

## Identity and review pin

- **Catalog position:** 255, “GENOME”; slug `genome`.
- **Listed repository:** [NORTHTEKDevs/genome](https://github.com/NORTHTEKDevs/genome); the catalog marks the locator explicit. The pinned Atlas entry is retained only for roster attribution.
- **Canonical upstream:** [NORTHTEKDevs/genome](https://github.com/NORTHTEKDevs/genome), default branch `main`. The official repository page shows `main`; the official commits API reports head `037755182b143db05e812efa1cc186b4b2ab4b32`, matching a fresh shallow checkout.
- **Reviewed:** 2026-11-25 20:55:06 UTC (2026-11-25 12:55:06 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) supplies ordinal, name, slug, listed repository, and roster attribution. The [pinned Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/genome.md) supports locator attribution only; it is not assessment evidence.

## Summary

GENOME is a Python memory library with SQLite or PostgreSQL storage, local embeddings by default, optional fact extraction and conflict resolution, scoped retrieval, temporal entity facts, and MCP or REST interfaces. Its source includes provenance quarantine and an opt-in mutation journal. This review records source behavior; no runtime or benchmark result was produced.

## Who and what

The official repository presents GENOME as an open-source Python memory layer for AI agents, with a Python API, optional MCP server, and optional REST service. The repository identifies Northtek (FrostByte Digital LLC) as the copyright holder. This review does not infer individual maintainer identity from commit or profile metadata.[[README](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/README.md)] [[repository](https://github.com/NORTHTEKDevs/genome)]

## Architecture and data model

The `Memory` facade composes an embedding provider, storage backend, extractor, optional conflict resolution, reranking, cache, and optional journal. SQLite is the default local store; a PostgreSQL backend uses pgvector and an HNSW cosine index. A MemoryRecord holds text and a float32 embedding, optional `user_id` and `agent_id`, creation/access timestamps and count, parent IDs, an operator tag, and JSON metadata.[[facade](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/facade.py)] [[schema](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/schema.py)] [[SQLite store](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/sqlite_store.py)] [[Postgres store](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/postgres_store.py)]

The default extractor is identity: it stores input as supplied after embedding. Optional LLM extraction splits text into facts, and optional conflict resolution can decide ADD, UPDATE, DELETE, or NONE. Temporal entity facts are MemoryRecords with validity bounds, optional source-memory link and confidence, and optional `believed_by` attribution.[[API reference](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/docs/api_reference.md)] [[facade](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/facade.py)] [[temporal facts](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/temporal.py)]

Retrieval supports dense cosine by default, plus hybrid BM25+dense and graph modes; optional reranking reorders a larger candidate pool. Parent filtering and a response cache are enabled by default. The README's performance and benchmark figures are upstream-reported and were not reproduced here.[[facade](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/facade.py)] [[architecture](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/docs/architecture.md)] [[README](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/README.md)]

## Write, update, delete, and retrieval

**Write.** `add()` validates input and scope IDs, calls the configured extractor (identity by default), embeds the output, and stores a record per extracted fact. The default embedding provider is local; an OpenAI provider is optional. The README describes the default write path as making no LLM or network calls, while cold setup may download the local model.[[facade](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/facade.py)] [[API reference](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/docs/api_reference.md)] [[README](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/README.md)]

**Update.** `update()` can replace content and/or metadata; content is re-embedded by default. With conflict resolution enabled, the resolver's target must be among the scope-filtered candidates, and a configured trust policy can refuse lower-trust supersession.[[facade](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/facade.py)] [[trust firewall](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/firewall.py)]

**Delete.** `delete(id)` removes the memory row and connected graph edges; `reset()` deletes all rows matching its supplied scope predicates. If both scope arguments are omitted, reset is global. MCP `forget` removes the nearest match only when its cosine score reaches `min_score` (default 0.5); this is not a tombstone API. The optional journal stores mutation payloads, so replaying an earlier prefix can reconstruct pre-delete state. Store deletion does not establish erasure from journal copies, backups, or replicas.[[facade](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/facade.py)] [[SQLite store](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/sqlite_store.py)] [[MCP server](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/mcp/server.py)] [[journal](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/journal.py)]

**Retrieval.** Dense cosine is the default. Hybrid mode combines BM25 and dense ranks; graph mode follows memory relationships; an optional reranker can reorder candidates. Search accepts `user_id` and `agent_id`, and the store filters each identifier only when supplied. Quality, evidence support, and abstention were not tested.[[facade](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/facade.py)] [[SQLite store](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/sqlite_store.py)] [[architecture](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/docs/architecture.md)]

## Scope isolation

Memory records carry nullable user and agent identifiers. SQLite and Postgres apply filters when the corresponding identifiers are supplied. REST per-request scope is optional by default; operators can set `GENOME_REQUIRE_SCOPE=1` to require scope fields and disable global reset. MCP tools use the `default` user namespace unless another is supplied. These source-visible boundaries do not establish isolation under every deployment or caller configuration.[[schema](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/schema.py)] [[SQLite store](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/sqlite_store.py)] [[Postgres store](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/postgres_store.py)] [[security policy](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/SECURITY.md)] [[MCP server](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/mcp/server.py)]

## Provenance and evidence

Callers can tag a write as `system`, `user`, `agent`, `tool`, or `web`. A configured TrustPolicy can quarantine records below a threshold and, with conflict resolution, prevent lower-trust content from superseding higher-trust records. These controls are opt-in and record origin; they do not establish truth. Temporal facts can link to a source memory and carry confidence and believer attribution. The inspected API does not establish claim-level citations to external source passages.[[facade](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/facade.py)] [[trust firewall](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/firewall.py)] [[temporal facts](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/temporal.py)]

## Efficiency and observability

SQLite computes exact cosine comparisons over the scoped rows and loads their embeddings for scoring; PostgreSQL can use pgvector HNSW. Local embeddings avoid an embedding API call after model availability, while sentence-transformers brings a substantial PyTorch dependency. Source includes structured logs, in-process counters/histograms, and an optional sink; the security policy says there is no telemetry by default. No latency, memory, cost, or storage use was measured.[[SQLite store](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/sqlite_store.py)] [[Postgres store](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/postgres_store.py)] [[README](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/README.md)] [[observability](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/observability.py)] [[security policy](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/SECURITY.md)]

## Temporal facts

The optional fact API records validity intervals, closes a prior current fact of the same type and believer, and supports `facts_valid_at()` as-of reads. This structured timeline differs from general memory retrieval; temporal question accuracy was not tested.[[temporal facts](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/temporal.py)] [[facade](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/facade.py)]

## Metric-domain evidence

| Metric domain | Status | Source observation |
|---|---|---|
| Answerable recall and abstention | Unmeasured | Retrieval modes are implemented; no benchmark queries or answers were run. |
| Correction accuracy and staleness | Unmeasured | Updates and temporal validity are represented; no correction probes were run. |
| Deletion leakage | Unmeasured | Delete/reset and optional journal replay are implemented; no post-delete probes were run. |
| Scope isolation | Unmeasured | Identifiers and filters are visible in source; no cross-scope workload was run. |
| Evidence support and citation coverage | Unmeasured | Provenance/source-memory fields exist; no claim adjudication was performed. |
| Retrieval latency | Unmeasured | No timing samples were collected. |
| Write-to-recall delay | Unmeasured | No write/read probe schedule was run. |
| Tokens and cost | Unmeasured | No usage or cost was collected. |
| Storage efficiency | Unmeasured | No corpus storage size was captured. |
| Source-visible observability | Available in code | Logging, counters, histograms, and optional metric sink exist; no production sink was measured. |

Metric definitions are in [METRICS.md](../METRICS.md); the fixture is a protocol, not a GENOME result. Project execution status remains [not run](../results/initial-baselines-status.json). Upstream README figures are not independently reproduced here.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[status](../results/initial-baselines-status.json)] [[README](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/README.md)]

## Limits and unknowns

Scope is optional in the base library and REST service unless configured as required. Trust tiers are not factual verification, and optional journal history retains mutation content that may permit reconstruction after deletion. The README reports benchmark and performance claims, but this review did not reproduce them. No system execution, tests, or benchmarks were run; runtime correctness, recall quality, latency, cost, resource use, and full deletion/isolation guarantees remain unknown.[[facade](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/memory/facade.py)] [[security policy](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/SECURITY.md)] [[firewall](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/firewall.py)] [[journal](https://github.com/NORTHTEKDevs/genome/blob/037755182b143db05e812efa1cc186b4b2ab4b32/genome/journal.py)] [[metrics](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)]

## Benchmark status

**Benchmark not run.** No GENOME runtime, tests, or project benchmark were run. The [project benchmark record](../results/initial-baselines-status.json) is an execution-status record; the [fixture](../fixtures/memory-benchmark-v1.json) defines the protocol but is not a result. The upstream's own reported figures remain upstream claims, not results of this review.[[status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[metrics](../METRICS.md)]
