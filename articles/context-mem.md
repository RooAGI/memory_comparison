# Context Mem — source review

## Identity and review pin

- **Roster ordinal / name / slug:** 144 / Context Mem / `context-mem`
- **Listed repository locator:** https://github.com/JubaKitiashvili/context-mem
- **Roster attribution:** `repository_status: explicit`; Atlas locator is retained for identity only. [Curated roster](../data/memory-systems.json) · [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/context-mem.md)
- **Canonical upstream / default branch:** [JubaKitiashvili/context-mem](https://github.com/JubaKitiashvili/context-mem) / `main`
- **Reviewed head:** [2a55af0a4bf3467df89f1315a74bb2e15ad903f7](https://github.com/JubaKitiashvili/context-mem/commit/2a55af0a4bf3467df89f1315a74bb2e15ad903f7)
- **Verification:** GitHub’s official repository page showed `main` and head prefix `2a55af0`; `git ls-remote --symref` resolved HEAD to `refs/heads/main` at the full SHA, and a shallow checkout matched.
- **Reviewed:** 2026-11-25 08:53:29 UTC (2026-11-25 00:53:29 PST; America/Los_Angeles)
- **Status:** Reviewed from current pinned upstream code and documentation; benchmark not run.

## Summary

Context Mem is a local TypeScript memory and context system for coding agents. Its core stores observations and structured knowledge in SQLite, with FTS and optional vector search; an optional Markdown vault is a derived, human-readable knowledge layer. Hooks can capture tool activity, summarize content, and inject selected context into agent sessions. These are source-level findings; this review did not run the system or validate the upstream’s performance claims. [README](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/README.md)

## Architecture and data model

The repository describes a three-layer design: raw observations, a synthesized Markdown wiki, and a schema governing wiki pages. SQLite is authoritative for observations, knowledge, entities, events, and indexes; the vault syncs from this store and can be enabled through configuration. The README describes an MCP server, editor integrations, and hooks for capture and context injection. [README](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/README.md) · [wiki schema](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/docs/llm-wiki-schema.md)

The SQLite migrations define observations with content, optional summaries, metadata, timestamps, privacy level, session and correlation IDs, importance, pinning, and compression tier. Separate knowledge and entity tables represent structured entries and graph links; later migrations add temporal validity and supersession fields to knowledge. [storage migrations](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/plugins/storage/migrations.ts)

## Write, update, delete, and retrieval

**Write and update.** The `observe` pipeline accepts content, type, source, and optional path. The processing path applies privacy handling, a matching content summarizer, importance and entity/topic extraction, then stores the observation and indexes it. Re-observing is not documented as a general correction protocol; structured knowledge has explicit contradiction resolution and temporal/supersession fields. [pipeline](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/core/pipeline.ts) · [kernel](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/core/kernel.ts) · [knowledge tools](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/mcp-server/tools/knowledge.ts)

**Delete and retention.** Source includes lifecycle cleanup for expired observations and private session data. Pinned observations are protected from age-based cleanup/compression; this is retention behavior, not a general tombstone or erasure guarantee. The inspected source does not establish deletion of every derived artifact or physical removal from SQLite/WAL storage. [lifecycle](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/core/lifecycle.ts) · [kernel](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/core/kernel.ts)

**Retrieval.** Search supports lexical BM25 and vector paths, plus fusion with additional text similarity strategies; the README describes temporal search, query expansion, and an optional LLM judge. The knowledge API has separate search and graph traversal functions, and temporal queries can use validity windows. Search quality and abstention were not tested. [BM25](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/plugins/search/bm25.ts) · [vector search](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/plugins/search/vector.ts) · [fusion](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/plugins/search/fusion.ts) · [knowledge graph](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/plugins/knowledge/knowledge-base.ts)

## Scope isolation

The default project store is located under the project’s `.context-mem` directory. The README also lists global knowledge and cross-project search/promotion features, so project-local storage does not mean every read is project-limited. Search scopes such as observations, knowledge, content, topics, or all are query categories; the inspected sources do not establish an authenticated tenant boundary or adversarial cross-project isolation. [README](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/README.md) · [storage configuration and migrations](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/plugins/storage/migrations.ts) · [knowledge base](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/plugins/knowledge/knowledge-base.ts)

## Provenance and evidence

Observations retain source, session/correlation metadata, and timestamps; knowledge records support temporal validity and supersession. The README describes decision-trail reconstruction from source observations and related events. This provides traceability structures, but the review found no basis to treat those links as proof that a generated claim is supported or correct. [migrations](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/plugins/storage/migrations.ts) · [README](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/README.md) · [decision trail](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/src/core/decision-trail.ts)

## Efficiency and observability

The project describes content-specific summarizers, compression tiers, query fusion, and diagnostic/dashboard features. Its README reports benchmark and throughput figures, but those are upstream-reported claims with project-specific methodology, not measurements from this review. Source inspection alone cannot establish practical latency, token savings, model/API costs, or storage growth for a deployment. [README](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/README.md) · [benchmark methodology](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/docs/benchmarks/methodology.md)

## Metric domains

All project metric domains remain **unmeasured** here: answerable retrieval and abstention; correction accuracy and staleness; deletion leakage; scope isolation; evidence support and citation coverage; retrieval latency; write-to-recall delay; token use; cost; and storage efficiency. The planned fixture and shared execution record are protocol/status references, not results. [METRICS.md](../METRICS.md) · [benchmark status](../results/initial-baselines-status.json) · [fixture](../fixtures/memory-benchmark-v1.json)

## Limitations and unknowns

This is a selected-source review, not an audit of every integration, plugin, migration, or deployment configuration. Runtime isolation and global-store access rules require deployment-level verification. The inspected code does not establish comprehensive deletion across backups, derived wiki files, and database storage remnants. The review did not measure retrieval quality, correction behavior, deletion leakage, cost, or performance.

## Contact

The official pinned [README](https://github.com/JubaKitiashvili/context-mem/blob/2a55af0a4bf3467df89f1315a74bb2e15ad903f7/README.md) was checked for a published contact email; none was found. No address was inferred from account or commit metadata.

## Benchmark status

**Not run.** No Context Mem runtime, benchmark, or test was run for this review. See [project metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and the [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured evidence IDs and pinned URLs are recorded in [context-mem.json](../data/system-reviews/context-mem.json). The [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/context-mem.md) supports identity and locator attribution only.
