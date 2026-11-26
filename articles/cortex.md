# Cortex

## Identity and review pin

- Catalog ordinal: 157
- System: Cortex
- Slug: `cortex`
- Listed repository: https://github.com/CortexPrism/cortex
- Roster attribution: explicit repository locator; the pinned Atlas entry is recorded only for curated identity and locator context, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortex.md)).
- Canonical upstream: https://github.com/CortexPrism/cortex
- Default branch: `main`
- Reviewed full head: [0c446572ddaad588164af939f2e093441b06921f](https://github.com/CortexPrism/cortex/commit/0c446572ddaad588164af939f2e093441b06921f)
- Review timestamp: 2026-11-25T09:29:16Z (UTC; 2026-11-25 01:29:16 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

The official GitHub API identifies `CortexPrism/cortex` as a public, non-fork repository with `main` as its default branch. Its main-branch Atom feed names full head `0c446572ddaad588164af939f2e093441b06921f`, updated 2026-06-25T23:47:43Z; the repository page shows the matching short SHA. ([repository metadata](https://api.github.com/repos/CortexPrism/cortex), [main history](https://github.com/CortexPrism/cortex/commits/main.atom), [head commit](https://github.com/CortexPrism/cortex/commit/0c446572ddaad588164af939f2e093441b06921f))

## Summary

CortexPrism is a self-hosted Deno agent operating system. Its memory subsystem combines episodic and semantic records, procedural skills, a relationship graph, and reflection memories in local SQLite databases; it injects a small set of retrieved memories into each agent turn. The code also supports optional embedding and external vector-store paths. ([README](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/README.md), [architecture](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/docs/ARCHITECTURE.md), [memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts))

## Who and what

The official README describes CortexPrism as an open-source, self-hosted agent runtime with CLI, web UI, tools, persistent memory, and security layers. It says the project is Apache-2.0 licensed and runs locally or on the operator's server. The review did not use contributor or commit metadata to identify maintainers. ([README](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/README.md))

## Architecture and data model

Cortex is a single-process Deno application. The README describes six package boundaries for core/configuration and databases, security and sandboxing, agent/AI and memory, HTTP/WebSocket server, infrastructure, and CLI. SQLite in WAL mode is the durable backend, split across application, memory, audit, and vault databases. The memory subsystem obtains its database through the shared database client. ([README](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/README.md), [architecture](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/docs/ARCHITECTURE.md), [memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts))

The README describes five memory tiers: episodic conversation summaries, semantic knowledge, procedural skills, graph relations, and reflections. The inspected store models episodic entries with session ID, summary, topics, entities, timestamps, importance, decay, sensitivity, and optional embedding; semantic entries hold content, category, tags, importance, decay, and optional embedding. Graph entities and typed relations are stored separately. ([README](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/README.md), [memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts), [graph](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/graph.ts))

## Write, update, delete, and retrieval

**Writes.** Episodic and semantic write functions insert records into SQLite and add corresponding FTS rows. When an embedder is configured, vectors are stored with the record and mirrored to an optional configured vector backend. Embedding failures are non-fatal; vector mirror write failures are suppressed. The heuristic layer assigns category and tags from regular-expression rules, tracks access, boosts importance or slows decay for frequently accessed records, and strengthens co-occurring graph relations. ([memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts), [heuristics](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/heuristics.ts), [vector backends](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/vector_backends.ts))

**Updates and consolidation.** Re-adding an existing graph relation raises its strength and access count. Hourly consolidation joins recent summaries by session into the newest episodic record; daily consolidation updates decay, deletes stale entries, runs heuristic maintenance, and enforces retention; weekly consolidation also runs reflection consolidation when a provider is configured. The inspected memory files do not establish a general versioned correction or mutation-audit model for arbitrary facts. ([graph](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/graph.ts), [consolidation](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/consolidate.ts))

**Delete and retention.** Daily maintenance deletes episodic and semantic rows after they pass the stale-score and age conditions, then asks the optional vector backend to delete the corresponding IDs. Retention cleanup deletes old episodic, semantic, and reflection rows. The vector delete path suppresses errors; the inspected paths do not demonstrate physical erasure from SQLite free pages, WAL files, backups, or external vector-service backups. ([consolidation](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/consolidate.ts), [privacy and retention](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/privacy.ts), [memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts))

**Retrieval.** Retrieval combines episodic and semantic keyword search, optional vector search, and graph-derived hits, then applies age-decay scoring, deduplicates, ranks, and limits results. The agent loop can inject a default of five formatted hits into the system prompt. Episodic keyword/vector paths accept a session ID, while semantic and graph retrieval are not given that filter in the inspected aggregator; its final session filter runs after the result limit and allows entries with no session ID. This is a code-path observation, not a measured cross-session leakage result. ([memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts), [memory injection](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/inject.ts), [architecture](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/docs/ARCHITECTURE.md))

## Scope isolation

Episodic records carry a session ID, and selected episodic search paths can filter by one. Semantic entries and graph entities/relations have no session field in the inspected model, and the combined retrieval path can include those results regardless of the caller's session. The separate security documentation describes session isolation as application-layer enforcement and explicitly says it is not a kernel-level boundary. No cross-session isolation workload was run. ([memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts), [graph](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/graph.ts), [security policy](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/SECURITY.md))

## Provenance and evidence

Episodic entries retain a session identifier, timestamps, topics, and entity labels. Semantic entries retain content, category, and tags; graph relations can carry a context string in relation metadata. Retrieved memories are formatted with a tier label, age, selected metadata, and a truncated text excerpt. The inspected injection contract does not attach source-document references or claim-level citations to returned memories. Sensitivity classification is applied to episodic writes, and the separate privacy module exposes an in-process policy map and PII redaction helper; this bounded review did not establish that those policies govern every memory write or recall path. ([memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts), [graph](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/graph.ts), [memory injection](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/inject.ts), [privacy](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/privacy.ts))

## Efficiency and observability

FTS5 provides lexical retrieval; embeddings and configured Qdrant, Chroma, or Pinecone adapters are optional. Retrieval fans out across lexical, vector, and graph paths, caps candidate counts and result count, and uses decay/access statistics. Consolidation is scheduled hourly, daily, and weekly. These are implementation features, not measured latency, storage, token, or cost results. ([README](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/README.md), [memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts), [vector backends](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/vector_backends.ts), [consolidation](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/consolidate.ts))

The project documents structured logs, a Prometheus-compatible `/metrics` endpoint, OTLP export, and optional Langfuse traces with model, token, cost, tool input/output, and duration fields. The observability documentation says components are opt-in and default to errors only. This review did not configure or collect telemetry. ([observability documentation](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/docs/observability.md))

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Cortex. Source inspection is not a benchmark result. ([metric definitions](../METRICS.md), [project result status](../results/initial-baselines-status.json), [fixture, not run](../fixtures/memory-benchmark-v1.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Hybrid retrieval and prompt injection are implemented; no scored answerability or abstention probes were run. |
| Correction accuracy and stale-value rate | Unmeasured | Summary consolidation and relation strengthening are source-visible; no correction workload or adjudication was run. |
| Deletion leakage | Unmeasured | Age/decay deletion paths exist; no post-delete probe, storage inspection, or backup check was run. |
| Scope isolation | Unmeasured | Episodic session filters exist, with broader semantic/graph paths; no leakage workload was run. |
| Evidence support and citation coverage | Unmeasured | Retrieved records carry limited metadata; no claim or citation support scoring was run. |
| Retrieval latency | Unmeasured | No latency samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write-to-recall probes were run. |
| Tokens and cost | Unmeasured | Observability documents token and cost fields; no runtime measurements were collected. |
| Storage efficiency | Unmeasured | No corpus-attributed storage measurement was collected. |

## Limits and unknowns

This bounded review inspected the official README, architecture and observability documentation, memory store, graph, heuristics, vector adapters, injection, consolidation, privacy/retention, and security policy. It did not inspect every database migration, memory tool route, model/provider implementation, or host deployment configuration. The code and docs do not establish how a deployment configures session IDs, vector stores, privacy policies, retention schedules, or remote telemetry. ([README](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/README.md), [architecture](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/docs/ARCHITECTURE.md), [memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts), [privacy](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/privacy.ts))

No Cortex runtime, tests, or benchmark workloads were run. This review does not establish runtime correctness, recall quality, correction quality, deletion completeness, deployed tenant isolation, measured latency, write-to-recall delay, token/cost totals, or storage efficiency. ([metric definitions](../METRICS.md), [project result status](../results/initial-baselines-status.json))

## Contact

The official pinned SECURITY.md publishes `security@cortexprism.io`; this is the only contact email recorded. The official pinned README was also checked. No commit/profile metadata or third-party directories were used. ([SECURITY.md](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/SECURITY.md), [README](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/README.md))

## Benchmark status

**Benchmark not run.** Cortex, its tests, and benchmark workloads were not run. The fixture is a workload specification only; the shared execution-status record contains no Cortex measurement. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortex.md)
- [Official GitHub API repository metadata](https://api.github.com/repos/CortexPrism/cortex)
- [Official main commit feed](https://github.com/CortexPrism/cortex/commits/main.atom)
- [Verified full head 0c446572ddaad588164af939f2e093441b06921f](https://github.com/CortexPrism/cortex/commit/0c446572ddaad588164af939f2e093441b06921f)
- [Pinned README](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/README.md)
- [Pinned architecture documentation](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/docs/ARCHITECTURE.md)
- [Pinned memory store](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/store.ts)
- [Pinned graph implementation](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/graph.ts)
- [Pinned consolidation jobs](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/consolidate.ts)
- [Pinned heuristic maintenance](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/heuristics.ts)
- [Pinned memory injection](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/inject.ts)
- [Pinned privacy and retention code](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/privacy.ts)
- [Pinned vector adapters](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/packages/ai/src/memory/vector_backends.ts)
- [Pinned security policy](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/SECURITY.md)
- [Pinned observability documentation](https://github.com/CortexPrism/cortex/blob/0c446572ddaad588164af939f2e093441b06921f/docs/observability.md)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)

---
