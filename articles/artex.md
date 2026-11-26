# ARTEX source review

## Identity and review pin

- **Curated ordinal:** 72 in `data/memory-systems.json`
- **Listed name / slug:** ARTEX / `artex`
- **Listed repository locator:** https://github.com/BaaRai/ARTEX
- **Canonical repository:** https://github.com/BaaRai/ARTEX
- **Default branch:** `main`
- **Reviewed head:** [`3cb06383fd99ffe7686abe1d375de11da7cfad54`](https://github.com/BaaRai/ARTEX/commit/3cb06383fd99ffe7686abe1d375de11da7cfad54)
- **Reviewed at:** 2026-11-24 21:41:28 UTC (13:41:28 PST; America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The roster's [Atlas report](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/artex.md) is recorded for identity, the listed locator, and attribution only. Its descriptions, marks, and layout were not used as assessment evidence. The official main commit feed and a fresh read-only `git ls-remote --symref` both identified the reviewed head above.

## Summary

ARTEX is a self-hosted, LLM-driven penetration-testing application. Its persistent memory includes a shared asset graph, per-task exploration graphs, activity traces, and an optional evidence-gated lesson library. Source inspection shows how records are written, selected and framed for agents; no ARTEX runtime or benchmark was run. [official README](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/README.md)

## Who and what

The official [README](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/README.md) describes a Go application with an embedded Next.js interface, PostgreSQL, model-provider integrations, planner/worker agents and real tool execution. The memory structures reviewed here are components of that self-hosted application, rather than a standalone hosted memory service.

## Architecture and data model

The [README](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/README.md) describes two linked graph layers. A company-owned asset graph stores shared domains, IPs, services, applications and endpoints. Each task has an exploration graph of typed goal, intent, fact, finding, hint and digest nodes connected by lineage edges; anchors associate those nodes with assets. The planner and workers read and write the task graph while the asset graph is shared across tasks.

In PostgreSQL, `explorations` own `exploration_nodes` with JSONB payloads, kind, state, priority, origin, ownership and timestamps. `exploration_edges` represent `spawns`, `derived_from`, `yields`, `proves` and `covers`; `exploration_anchors` connect nodes to asset rows. Activity records retain worker/tool events, summaries, details, metadata and token-use fields. Schema indexes cover exploration/kind reads, open-intent priority and activity lookups. [schema.sql](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/schema.sql) [exploration.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/exploration.go)

A separate RSI lesson library stores short cue/action records with kind, optional task-category and company scope, status and a stable deduplication key. Evidence rows identify their finding or retest source, detail and withdrawal time; usage rows record task and shadow/inject mode. The inspected implementation derives these lessons from rules; it does not ask an LLM to invent them. [schema.sql](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/schema.sql) [lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/lessons.go) [RSI lesson guide](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/docs/rsi-lessons.md)

## Write, update, delete, and retrieval

- **Write:** agent tools and task workflows add typed nodes and edges to the task exploration. Payloads are JSONB; optional asset anchors are checked for fact writes. Terminal task outcomes, finding disposition changes and completed retests can trigger lesson extraction. Extraction creates a candidate only with a cue, action and source evidence, deduplicated by kind, scope, cue and action. [exploration.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/exploration.go) [lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/lessons.go) [RSI lesson guide](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/docs/rsi-lessons.md)
- **Update and correction:** a changed finding disposition or completed retest reruns deterministic extraction. Repeated extraction is idempotent. Reversed dispositions mark the old evidence withdrawn; lessons with no remaining live support are retired. Reconfirmation can restore evidence. This maintains lesson support; it does not show that later agent answers are corrected reliably. [lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/lessons.go) [server/lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/server/lessons.go)
- **Delete and retirement:** open, running or paused intents can be soft-deleted with a reason while retaining the node, outputs and lineage. Cancellation can physically remove an intent and descendants supported only through it, while protecting goals, origin facts and shared descendants. Task deletion cascades through per-task graph nodes, edges and activity. These paths differ; the inspected code does not establish complete physical erasure of all derived content or deployment backups. [exploration.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/exploration.go) [tasks.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/tasks.go)
- **Retrieval:** task graph reads are newest-first and paginated by kind; graph overviews and activity traces supply task context. Related-task helpers expose direct sources only and mark inherited records as read-only provenance. Lesson selection filters by company and category, ranks matching scopes first, then positive, negative and caution lessons, followed by support and recency. Task integration selects up to eight lessons and renders a block capped at 1,800 characters. [exploration.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/exploration.go) [exploration_sources.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/exploration_sources.go) [lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/lessons.go) [server/lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/server/lessons.go)

## Scope isolation

Exploration nodes belong to one exploration, so normal graph reads are scoped to that exploration. A helper permits reads from its directly related source tasks, tagging inherited nodes and activities with their source task and inherited flag; it never expands to indirect sources. The shared asset graph is visible across tasks. Lesson records are selected by company and category: companyless lessons are visible only to companyless tasks, and a task with multiple companies does not receive a newly extracted lesson. These are code-visible filters, not a cross-tenant isolation test. [schema.sql](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/schema.sql) [exploration_sources.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/exploration_sources.go) [lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/lessons.go) [RSI lesson guide](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/docs/rsi-lessons.md)

## Provenance and evidence

Exploration edges preserve reasoning lineage; anchors link reasoning nodes to assets; activity rows retain worker, tool, event, metadata, and token-use fields. Finding traffic evidence is captured through ARTEX's evidence workflow, while the optional coverage ledger stores an outcome, evidence text, reason, worker, and intent and appends changes to a history table. RSI evidence records finding/retest IDs, detail and withdrawal time, and usage rows record whether a lesson was shadowed or injected. These fields support traceability but do not establish that every generated claim is supported. [schema.sql](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/schema.sql) [README.md](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/README.md) [coverage_ledger.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/coverage_ledger.go) [lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/lessons.go)

Derived content, including facts, findings, digests and lesson blocks, can contain target-controlled text. Code wraps derived prompt content in nonce-bearing data envelopes and neutralizes copied markers; the source comments explicitly characterize the framing as advisory to the model. [data_envelope.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/agent/data_envelope.go) [lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/lessons.go)

## Source-visible efficiency and observability

**Code observations:** SQL indexes and reverse pagination support bounded graph/activity reads. Lesson selection has a default limit of eight, renders no more than 1,800 characters in task integration, and records which selected lessons were considered in shadow/inject mode. Activity schema has input/output and cache token columns. Graph compaction maintains hot/cold stamps during planner rounds and may generate digests in a guarded background pass. These code paths expose work and instrumentation points, not performance results. [schema.sql](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/schema.sql) [lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/lessons.go) [server/lessons.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/server/lessons.go) [compaction.go](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/agent/compaction.go)

No ARTEX latency, throughput, token, cost, storage, or write-to-recall measurement was collected. The optional lesson documentation proposes later comparisons such as tokens and tool calls per confirmed finding, but those are not results and do not isolate causality. [RSI lesson guide](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/docs/rsi-lessons.md)

## Metric-domain evidence

Every project metric domain is **unmeasured** for this review. The project's [metric definitions](../METRICS.md), [shared execution-status record](../results/initial-baselines-status.json) and [planned fixture](../fixtures/memory-benchmark-v1.json) define a separate protocol; they are not ARTEX results.

| Domain | Source observation | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Typed graph reads and optional lesson selection are visible. | Unmeasured |
| Correction accuracy and stale values | Finding dispositions retract or restore lesson evidence. | Unmeasured |
| Deletion leakage | Intent cancellation and task cascades are implemented. | Unmeasured |
| Scope isolation | Task exploration, related-task reads and company/category filters are in source. | Unmeasured |
| Evidence support and citation coverage | Lineage, anchors and evidence identifiers are retained. | Unmeasured |
| Retrieval latency | Indexes and paginated reads are visible; timings were not collected. | Unmeasured |
| Write-to-recall delay | No scheduled acknowledgment-to-recall probes were run. | Unmeasured |
| Tokens and cost | Token-use fields and prompt bounds exist; no workload accounting was done. | Unmeasured |
| Storage efficiency | Schema and indexes were inspected; no bytes were measured. | Unmeasured |

## Limits and unknowns

This is a selected source review at one verified commit. ARTEX, its services and its benchmark workloads were not run. Source structure does not establish recall quality, abstention calibration, correction quality, deletion completeness, deployment isolation, or latency, cost and storage behavior.

The exploration graph and company-shared asset graph have different scope boundaries. Direct related-task reads are explicitly tagged as inherited, but this review did not audit every API, authorization rule or deployment setting. Intent cancellation is selective graph cleanup; task deletion removes task-owned graph and activity rows, while cross-system erasure, backups and every derived representation remain unverified. The prompt envelope warns the model about untrusted derived text but is advisory.

The RSI lesson guide says the feature is off by default, has no time-based decay and should not be interpreted causally from support counts. Its measurement ideas are proposed comparisons only. [RSI lesson guide](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/docs/rsi-lessons.md) [SECURITY.md](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/SECURITY.md)

## Contact-list follow-up

I checked the official pinned [README](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/README.md) and [SECURITY.md](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/SECURITY.md). They publish no contact email; SECURITY.md directs vulnerability reports to GitHub's private vulnerability-report form. The JSON records a null email and the exact checked source URLs.

## Benchmark status

**Benchmark not run.** No ARTEX runtime, tests, or benchmark workload was run. Project metric definitions, fixture and shared status record describe the proposed protocol; they are not ARTEX results. [metric definitions](../METRICS.md) [execution-status record](../results/initial-baselines-status.json) [planned fixture](../fixtures/memory-benchmark-v1.json)

## Sources

- [Canonical public repository](https://github.com/BaaRai/ARTEX)
- [Official main branch commit feed](https://github.com/BaaRai/ARTEX/commits/main.atom)
- [Verified main head](https://github.com/BaaRai/ARTEX/commit/3cb06383fd99ffe7686abe1d375de11da7cfad54)
- [README.md](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/README.md)
- [Database schema](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/schema.sql)
- [Exploration graph store](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/exploration.go)
- [Related-task graph reads](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/exploration_sources.go)
- [Lesson extraction and selection](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/lessons.go)
- [RSI lesson guide](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/docs/rsi-lessons.md)
- [Task lesson integration](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/server/lessons.go)
- [Derived-data prompt envelope](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/agent/data_envelope.go)
- [Exploration compactor](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/agent/compaction.go)
- [Coverage ledger](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/coverage_ledger.go)
- [Task deletion](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/db/tasks.go)
- [Official security policy](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/SECURITY.md)
- [Metric definitions](../METRICS.md)
- [Benchmark execution-status record](../results/initial-baselines-status.json)
- [Planned benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster](../data/memory-systems.json)
- [Atlas attribution source, identity only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/artex.md)

**Review boundary:** no ARTEX runtime, benchmark workload, or tests were run.
