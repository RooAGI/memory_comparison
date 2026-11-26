# Beevibe source review

## Identity and review pin

- **Curated ordinal:** 91
- **Listed name / slug:** Beevibe / `beevibe`
- **Listed repository locator:** https://github.com/beevibe-ai/beevibe
- **Canonical repository:** https://github.com/beevibe-ai/beevibe
- **Default branch:** `main`
- **Reviewed head:** [`81530ccae3519738b16a2b5d4aa81a61989a4ce8`](https://github.com/beevibe-ai/beevibe/commit/81530ccae3519738b16a2b5d4aa81a61989a4ce8)
- **Reviewed at:** 2026-11-24 23:31:19 UTC (15:31:19 PST; America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The curated roster supplies ordinal, listed name and locator, and attribution to [the pinned Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/beevibe.md) only. Atlas descriptions, capability marks, and layout were not used as assessment evidence. The official GitHub repository page shows `main`; read-only `git ls-remote --symref` identified `refs/heads/main` as HEAD at the full SHA above, and a shallow checkout resolved to the same commit.[[roster](../data/memory-systems.json)][[repository](<https://github.com/beevibe-ai/beevibe>)][[reviewed head](<https://github.com/beevibe-ai/beevibe/commit/81530ccae3519738b16a2b5d4aa81a61989a4ce8>)]

## Summary

Beevibe is a self-hosted workspace for people and persistent agent roles. Its memory layer combines stable per-agent prompt blocks with vector-searchable facts stored in Postgres/pgvector. The observations below come from selected docs and source at the reviewed SHA, not from running the service.[[README](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/README.md>)][[schema](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/migrations/1776391747576_initial-schema.sql>)]

## Who and what

The official [README](https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/README.md) calls Beevibe an agent-native operating system for companies and describes it as self-hosted. The repository identifies a TypeScript monorepo with API, core, daemon, scheduler, and web packages. It names no individual maintainer in the reviewed passages, so this review makes no individual ownership claim.[[README](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/README.md>)][[core package](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/README.md>)]

## Architecture and data model

**Code observation.** The core package separates memory domain types and repository ports from services and Postgres adapters. `MemoryAgent` composes a session briefing; `FactStore` owns archival fact writes and vector queries; `CoreMemory` reads and edits stable blocks. The API exposes MCP tools such as `save_memory` and `update_core_memory`, while the database migration defines the persisted tables.[[core package](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/README.md>)][[memory types](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/domain/memory.ts>)][[memory agent](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/memory-agent.ts>)][[MCP tools](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/api/src/tools/save-memory.ts>)]

The schema has two distinct representations. `core_memory_block` stores per-agent named text blocks with a character limit and timestamps. `memory_fact` stores an ID, agent ID, one of three scopes (`ic`, `team`, `org`), one of five fact types, content, a 1536-dimensional embedding, source session IDs, and creation time. PostgreSQL indexes agent/scope and the embedding with HNSW.[[schema](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/migrations/1776391747576_initial-schema.sql>)][[memory types](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/domain/memory.ts>)]

## Write, update, delete, and retrieval

**Write — code observation.** The MCP `save_memory` tool derives scope from the saving agent’s hierarchy and supplies its agent and session IDs. `FactStore.addOrMerge` embeds the content, searches for the nearest fact with the same agent, scope, and type, and merges it with an LLM when similarity reaches 0.88; otherwise it inserts a fact. A merge re-embeds the combined text and unions source session IDs. The threshold is source configuration, not an independently measured safe boundary.[[save tool](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/api/src/tools/save-memory.ts>)][[fact store](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/fact-store.ts>)]

**Update and promotion — code observation.** Archival near-duplicate writes rewrite the selected fact’s content and embedding. Post-session, `FactPromoter` asks an LLM whether each touched fact should move upward from individual to team or org scope and records a reason; org facts are not promoted further. `update_core_memory` supports append and exact-substring replacement in a named block; both paths enforce that block’s character limit. The owner-facing block editor can replace full block content.[[fact store](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/fact-store.ts>)][[promoter](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/fact-promoter.ts>)][[core memory service](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/core-memory.ts>)][[core block repository](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/adapters/postgres/core-memory-repo.ts>)]

**Delete — code observation.** The fact repository deletes by fact ID, and the API README documents an owner-only fact delete endpoint. Core blocks have an agent-and-block keyed delete method in the repository. This inspection did not establish a unified erasure workflow across facts, blocks, session history, backups, or external systems.[[fact repository](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/adapters/postgres/memory-fact-repo.ts>)][[API README](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/api/README.md>)][[core block repository](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/adapters/postgres/core-memory-repo.ts>)]

**Retrieval — code observation.** Session start embeds the intent and performs a cosine vector query with a 0.35 similarity floor and default cap of 10 facts; `search_context` uses the same path mid-session. The caller requests all three scopes. Results appear in an archival-memory prompt envelope alongside stable core blocks. These limits and prompts describe implementation behavior, not recall accuracy.[[memory agent](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/memory-agent.ts>)][[fact repository](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/adapters/postgres/memory-fact-repo.ts>)]

## Metric-domain evidence

- **Answerable recall and abstention — unmeasured.** The source has vector recall, a threshold and a result cap; no answerable or unanswerable probes were run.[[memory agent](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/memory-agent.ts>)]
- **Correction and stale values — unmeasured.** Merging and scope movement mutate facts, but no correction history or stale-value adjudication was measured.[[fact store](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/fact-store.ts>)]
- **Deletion leakage — unmeasured.** Delete methods are present; no post-delete probes were run.[[fact repository](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/adapters/postgres/memory-fact-repo.ts>)][[metrics](../METRICS.md)]
- **Scope isolation — unmeasured.** Search predicates require both `agent_id` and `scope`, but the inspected briefing requests all tiers and promotion changes only scope while retaining the fact’s agent ID. Thus the code shows tier filtering within an agent’s records; it does not show promoted facts becoming retrievable under another agent ID. This observation does not replace cross-agent or tenant isolation tests.[[memory agent](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/memory-agent.ts>)][[fact repository](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/adapters/postgres/memory-fact-repo.ts>)][[promoter](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/fact-promoter.ts>)]
- **Evidence and citations — unmeasured.** Facts retain source session IDs, and promotion decisions retain reason and source-session metadata. No generated answers were adjudicated for evidence support or claim-level citation coverage.[[memory types](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/domain/memory.ts>)][[memory agent](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/memory-agent.ts>)]
- **Efficiency and observability — source features, no measurements.** The schema’s HNSW and agent/scope indexes and bounded top-k are visible design choices. API views provide activity summaries, while PostgreSQL notifications expose fact create/delete and promotion events. The activity view documents that core-block write churn is undercounted because it stores only current-row timestamps, not a write event log. No latency, tokens, cost, or storage measurements were collected.[[schema](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/migrations/1776391747576_initial-schema.sql>)][[activity view](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/api/src/views/memory-activity.ts>)][[event migration](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/migrations/1779300000000_add-bv-event-triggers-extension.sql>)][[metrics](../METRICS.md)]

## Limits and unknowns

This is a bounded review of selected documentation, schema, and source at one verified SHA. The application, tests, and benchmark workload were not run. The inspection does not establish production correctness, the quality of generated merges or promotion decisions, cross-tenant authorization, deletion completeness beyond inspected data paths, or measured retrieval and resource behavior. In particular, fact retrieval’s agent predicate means that broader scope labels alone do not prove cross-agent sharing.[[fact store](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/fact-store.ts>)][[memory agent](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/memory-agent.ts>)][[fact repository](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/adapters/postgres/memory-fact-repo.ts>)]

The official [README](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/README.md>) was checked for a published contact email. No email was published there. Root `SECURITY.md`, `SUPPORT.md`, and `.github/SECURITY.md` are absent at this revision. The JSON records null and the exact checked README URL.

## Benchmark status

**Benchmark not run.** No Beevibe service, benchmark, fixture, or tests were run. All metric domains remain unmeasured; code mechanisms and project protocol documents are not results.[[metric definitions](../METRICS.md)][[execution status](../results/initial-baselines-status.json)][[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Canonical repository](<https://github.com/beevibe-ai/beevibe>)
- [Reviewed main head](<https://github.com/beevibe-ai/beevibe/commit/81530ccae3519738b16a2b5d4aa81a61989a4ce8>)
- [Official README](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/README.md>)
- [Core package README](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/README.md>)
- [API package README](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/api/README.md>)
- [Memory fact domain](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/domain/memory.ts>)
- [Core memory domain](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/domain/core-memory.ts>)
- [Initial schema](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/migrations/1776391747576_initial-schema.sql>)
- [FactStore](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/fact-store.ts>)
- [MemoryAgent briefing and promotion flow](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/memory-agent.ts>)
- [FactPromoter](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/fact-promoter.ts>)
- [Postgres fact repository](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/adapters/postgres/memory-fact-repo.ts>)
- [CoreMemory service](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/services/memory/core-memory.ts>)
- [Core memory repository](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/core/src/adapters/postgres/core-memory-repo.ts>)
- [MCP save-memory tool](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/api/src/tools/save-memory.ts>)
- [Activity and KPI view](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/packages/api/src/views/memory-activity.ts>)
- [Memory event trigger migration](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/migrations/1779300000000_add-bv-event-triggers-extension.sql>)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated identity and attribution](../data/memory-systems.json)
- [Atlas attribution source](<https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/beevibe.md>)

## Contact-list follow-up

Official repository contact sources checked at the reviewed revision: [README](<https://github.com/beevibe-ai/beevibe/blob/81530ccae3519738b16a2b5d4aa81a61989a4ce8/README.md>), `SECURITY.md`, `SUPPORT.md`, and `.github/SECURITY.md`. No published email was found in the README and the three policy/support paths are absent. Contact email is recorded as null in the JSON.

**Verification boundary:** no Beevibe runtime, tests, or benchmark workload was run.
