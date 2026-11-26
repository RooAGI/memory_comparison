# ALTK-Evolve

## Identity and review pin

- **System:** ALTK-Evolve
- **Curated position:** 51
- **Listed repository:** https://github.com/AgentToolkit/altk-evolve
- **Default branch:** `main`
- **Reviewed head:** [`03f83be7480bf0be3f4aa6e868b832486e064718`](https://github.com/AgentToolkit/altk-evolve/commit/03f83be7480bf0be3f4aa6e868b832486e064718)
- **Reviewed:** 2026-11-24 20:31:28 UTC (12:31:28 PST; America/Los_Angeles)
- **Source status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/altk-evolve.md), used only to resolve the catalog entry and its listed repository locator.

## Summary

ALTK-Evolve learns reusable guidelines from agent trajectories, stores entities in a selectable backend, and retrieves a task-specific set for later sessions. This review describes source-visible behavior at the pinned revision; it is not a runtime or benchmark evaluation.

## Who and what

The project presents Evolve as an open-source toolkit for on-the-job agent learning. Full mode provides a Python core with MCP/service integration and selectable memory backends. Evolve Lite integrates learning and retrieval into supported agent assistants. This article reviews the full-mode Python core and MCP surface. ([README](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/README.md), [client](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/frontend/client/evolve_client.py))

## Architecture and data model

An entity contains searchable text or structured content, a type and metadata; a recorded entity adds an ID and creation time. Namespaces group entities. Guideline records add content, rationale, category, trigger, implementation steps, support count and an optional success/failure evidence label. ([entity schema](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/schema/core.py), [guideline schema](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/schema/guidelines.py))

The client selects a filesystem, PostgreSQL or Milvus backend. Filesystem namespaces use JSON files and case-insensitive text matching. PostgreSQL and Milvus provide vector-oriented search; the backend guide describes one file, table or collection per namespace. ([client](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/frontend/client/evolve_client.py), [filesystem backend](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/backend/filesystem.py), [backend guide](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/docs/guides/backend-configuration.md))

Trajectory processing extracts guidelines and persists them through a preparation/commit path. When conflict resolution is enabled, a model compares incoming entities with stored candidates and proposes ADD, UPDATE, DELETE or NONE decisions. Hooks and backend commit logic apply the prepared changes. These code paths do not establish that each generated guideline or conflict decision is correct. ([backend write pipeline](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/backend/base.py), [client processing](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/frontend/client/evolve_client.py))

## Write, update, delete and retrieval

**Write.** `save_trajectory` stores trajectory messages with task, user and session metadata and generates guidelines through processing. `create_entity` supports manual entities. The update pipeline runs policy hooks and reconciliation before committing storage changes. Atomic backends check prepared targets and may retry concurrent-change conflicts. ([MCP server](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/frontend/mcp/mcp_server.py), [backend write pipeline](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/backend/base.py), [hook manager](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/hooks/manager.py))

**Update and provenance.** Conflict decisions can update an entity in place; metadata can also be patched independently. Provenance helpers merge source associations, distinguish supporting from superseded sources, and timestamp associations. No correction accuracy or stale-value rate was measured. ([backend write pipeline](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/backend/base.py), [provenance helpers](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/schema/provenance.py))

**Delete.** Direct entity deletion is exposed by the client and MCP tool. The MCP path checks ownership when an entity has an owner, and a pre-delete hook can veto. Retention can flag or delete by age, disuse or source deletion, and trajectory deletion can cascade to eligible derived entities. The retention scan defaults to 100,000 entities and warns when it reaches the limit. This review does not establish deletion completeness across stores, backups or downstream copies. ([MCP server](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/frontend/mcp/mcp_server.py), [hook-wrapped backend](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/backend/base.py), [retention engine](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/retention/engine.py))

**Retrieval.** Guideline retrieval combines an always-included core whose support meets a threshold with up to `top_k` candidates ranked by similarity to source-task descriptions. It removes candidates already covered by the core or near-duplicates. The filesystem backend uses text matching rather than vector similarity. ([retrieval](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/llm/guidelines/retrieval.py), [filesystem backend](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/backend/filesystem.py))

## Scope isolation

Namespaces provide the primary physical separation; user and session identifiers are metadata. The general guideline tools accept user/session IDs for attribution but intentionally do not apply them as hard filters. Public entity retrieval can span namespaces. The README documents a separate personal-facts path that requires explicit namespace and user IDs and filters by that pair. These source patterns do not establish authenticated tenant isolation across all APIs or deployment configurations. ([backend guide](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/docs/guides/backend-configuration.md), [MCP retrieval](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/frontend/mcp/mcp_server.py), [README](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/README.md))

## Provenance and evidence

Source associations can retain conversation, task, user and agent IDs, status and association time. Guideline records may carry an evidence label of success, failure or both; an attribution tool can return source task IDs. These fields support traceability, but they are not claim-level citations or proof that a returned answer is supported by its source. ([provenance](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/schema/provenance.py), [guideline schema](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/schema/guidelines.py), [README](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/README.md))

## Source-visible efficiency and observability

Backend choice trades simple file/text search against vector search and its indexing or coordination requirements. Evolve telemetry defines operation-duration histograms and outcome counters with bounded labels. Its own instrumentation excludes prompts, memory content, SQL values, exception messages and user/entity IDs from exported data. The README says asynchronous OTLP export uses bounded queues and unsent telemetry may be dropped. These are source and documentation observations; no latency, tokens, cost or storage was measured. ([backend guide](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/docs/guides/backend-configuration.md), [telemetry](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/altk_evolve/telemetry.py), [README](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/README.md))

## Metric-domain evidence

| Domain | Status | Source evidence |
|---|---|---|
| Answerable recall and abstention | Unmeasured | Entity and guideline retrieval paths exist; no outputs were scored against answerable or unsupported cases. |
| Correction accuracy and stale values | Unmeasured | Conflict resolution and update paths exist; no correction probes were run. |
| Deletion leakage | Unmeasured | Delete and retention paths exist; no acknowledged deletion and post-delete probes were run. |
| Scope isolation | Unmeasured | Namespaces and metadata scope are visible; no cross-scope probes were run. |
| Evidence support and citation coverage | Unmeasured | Provenance and evidence fields exist; no answers were adjudicated for claim support or citations. |
| Retrieval latency and write-to-recall delay | Unmeasured | Operation timing is instrumented; no workload timings or recall-delay observations were collected. |
| Tokens, cost and persistent storage | Unmeasured | No ALTK-Evolve measurements were collected. |

The project defines its proposed metrics in [METRICS.md](../METRICS.md), specifies planned cases in the [versioned fixture](../fixtures/memory-benchmark-v1.json), and records execution state in [initial-baselines-status.json](../results/initial-baselines-status.json). That record remains `not_run`; fixture counts are planned case counts, not measurements.

## Limits and unknowns

This is read-only inspection at the recorded SHA. It does not establish runtime correctness, answer quality, security, deployed authorization, backend parity, concurrency behavior, deletion completeness or performance. Optional hooks, model settings and backend choices may differ by deployment.

The upstream README reports results from separate AppWorld and τ²-bench experiments. They are upstream-reported results under their own model and configuration protocols, not measurements from this review or entries in the project benchmark record. ([README](https://github.com/AgentToolkit/altk-evolve/blob/03f83be7480bf0be3f4aa6e868b832486e064718/README.md), [project metric definitions](../METRICS.md), [execution status](../results/initial-baselines-status.json))

## Benchmark status

**Benchmark not run.** No ALTK-Evolve system execution, benchmark workload or tests were run for this review. See [metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).

## Sources

- [Official repository](https://github.com/AgentToolkit/altk-evolve) — canonical locator; default branch confirmed as `main`.
- [Official main commit feed](https://github.com/AgentToolkit/altk-evolve/commits/main.atom) — current full head recorded above.
- [Official documentation site](https://agenttoolkit.github.io/altk-evolve/) — checked for a published contact email; none found.
- [METRICS.md](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)
