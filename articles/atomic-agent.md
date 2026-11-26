# Atomic Agent source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 73 / Atomic Agent / `atomic-agent`  
**Listed repository locator:** [AtomicBot-ai/atomic-agent](https://github.com/AtomicBot-ai/atomic-agent)  
**Current canonical repository:** [AtomicBot-ai/atomic-agent](https://github.com/AtomicBot-ai/atomic-agent)  
**Default branch / reviewed head:** main / `89d65615e36b763b35bc81c1e64304bd2d0e5c7c`  
**Review time:** 2026-11-24T21:42:08Z (UTC; 2026-11-24 13:42:08 PST; America/Los_Angeles).

## Identity and review pin

The curated roster places Atomic Agent at ordinal 73 with slug `atomic-agent` and lists the AtomicBot-ai repository locator. Its pinned Atlas source is recorded only for roster attribution; Atlas descriptions and marks were not used as assessment evidence. The official repository page identifies `main` as the default branch, and the official `main.atom` feed reports full head `89d65615e36b763b35bc81c1e64304bd2d0e5c7c`. Review time is 2026-11-24 21:42:08 UTC (13:42:08 PST, America/Los_Angeles). [[curated roster](../data/memory-systems.json)] [[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/atomic-agent.md)] [[repository](https://github.com/AtomicBot-ai/atomic-agent)] [[main commit feed](https://github.com/AtomicBot-ai/atomic-agent/commits/main.atom)] [[reviewed head](https://github.com/AtomicBot-ai/atomic-agent/commit/89d65615e36b763b35bc81c1e64304bd2d0e5c7c)]

## Summary

Atomic Agent keeps durable memory outside the chat transcript in a local SQLite database. It combines profile facts, searchable notes, links, lessons, and procedures, then places bounded selected material into prompts. This is a source review, not a runtime evaluation. [[README](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/README.md>)] [[memory guide](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/docs/user/memory.md>)] [[memory subsystem](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/README.md>)]

## Who and what

The project is presented as a local-first AI agent, not a standalone memory database. The curated roster lists the AtomicBot-ai repository; the inspected official pages do not establish an individual maintainer role. [[repository](https://github.com/AtomicBot-ai/atomic-agent)] [[README](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/README.md>)]

## Architecture and data model

Durable memory is stored separately from session history in a versioned SQLite database. The schema includes profile facts and freeform notes; note rows carry content, timestamps, source, optional session and working-directory identifiers, tags, recall counters, and lifecycle fields. FTS5 mirrors note text for full-text ranking, while migrations track the database schema version. [[schema](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-schema.ts>)] [[memory store](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-store.ts>)] [[subsystem ownership](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/README.md>)]

Specialized stores and background workers provide profile history, links, lessons, procedures, votes, reflection, reconciliation, and consolidation. Profile facts retain stable IDs and supersession links with valid-from times, pinning/contextual keywords, disable state, vote score, and name-grounding status. Replacing a fact creates a new version and leaves the previous row in history. [[profile store](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/profile-store.ts>)] [[formation design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/formation.md>)]

A context provider assembles bounded prompt sections for recalled notes, a compact note index, lessons, and procedures. Optional one-hop or bounded graph expansion adds linked notes after ranked retrieval and removes duplicate IDs. The user guide describes durable memory as separate from the transcript, with only selected facts, previews, and indexes entering the prompt. [[context provider](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-context-provider.ts>)] [[retrieval design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/retrieval.md>)] [[user guide](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/docs/user/memory.md>)]

The guide describes profile, notes, reflection, recall/index injection, and query rewriting as enabled by current defaults; embeddings, typed-note extraction, and segmented reflection are optional and disabled by default. Installed configuration may differ after overrides or migration. [[user guide](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/docs/user/memory.md>)] [[retrieval design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/retrieval.md>)] [[formation design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/formation.md>)]

## Write, update, delete, and retrieval

**Write.** Reflection can form bounded profile facts and notes from completed turns. Probe-like turns and one-off instructions are skipped; name-like facts remain stored but are kept out of prompts until checks find their name in user messages. These are implementation/documentation observations, not a test of formation quality. [[formation design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/formation.md>)] [[profile store](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/profile-store.ts>)] [[user guide](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/docs/user/memory.md>)]

**Update.** Profile writes use a supersession chain: a new fact version points to the row it replaces, preserving history. Optional note reconciliation marks older replaced notes as superseded and filters them from normal recall/index output. Consolidation may distill durable notes into lessons and manage archived lifecycle state. [[profile store](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/profile-store.ts>)] [[formation design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/formation.md>)] [[context provider](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-context-provider.ts>)]

**Delete or disable.** Notes and profile facts can be removed or turned off. Disabling retains a listed row but excludes it from recall, search, prompt context, and consolidation; profile removal of the active fact does not delete the historical chain. Chat deletion is separate from durable-memory deletion. The inspected sources do not establish physical erasure from SQLite pages, journals, backups, or exports. [[memory store](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-store.ts>)] [[schema](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-schema.ts>)] [[profile store](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/profile-store.ts>)] [[user guide](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/docs/user/memory.md>)]

**Retrieval.** Notes use FTS5/BM25; configured embeddings enable a hybrid of normalized BM25 and cosine similarity. Meaning-only matches fill open slots subject to a similarity floor and the same working-directory/tag filters. Query rewriting is enabled by default and heuristic-gated; vector recall errors fall back to keyword recall. TUI search and lesson/procedure recall remain keyword-only. [[retrieval design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/retrieval.md>)] [[context provider](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-context-provider.ts>)] [[memory store](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-store.ts>)]

The embedding recall implementation is bounded by a configured brute-force ceiling (documented default: 2,000 vectors); above it, the documented path scans the newest subset plus vectors attached to keyword hits and records overflow. Backfill is serialized in small batches; while it runs, recall remains keyword-only to avoid ranking a partially indexed corpus. This describes source-visible work, not measured speed or recall quality. [[retrieval design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/retrieval.md>)] [[schema](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-schema.ts>)]

**Provenance and observability.** Note rows retain source (`agent` or `user`), timestamps, optional session ID, working directory, and tags; profile history preserves the row that a newer fact supersedes. These fields support item lineage, but the inspected model does not establish claim-level citations to source passages. The store accepts an optional metrics sink for dedup decisions, eviction sweeps, and clock-skew detection; memory sub-runners track repeated failures/timeouts by session and can emit operator warnings. These are source-visible instrumentation paths, not observed production telemetry. [[memory store](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-store.ts>)] [[schema](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-schema.ts>)] [[profile store](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/profile-store.ts>)] [[formation design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/formation.md>)]

**Scope.** Notes carry an optional `working_dir`. Project filtering is applied when the context provider receives a working directory; otherwise retrieval can cover any project. The recall tool permits caller/model-selected scope, and profile facts have no project key. This is conditional filtering in code, not a principal authorization boundary or an isolation test. [[schema](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-schema.ts>)] [[context provider](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-context-provider.ts>)] [[retrieval design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/retrieval.md>)]

## Metric-domain evidence

All rows below are **not measured** in this review.

| Domain | Source observation | Measurement |
|---|---|---|
| Answerable retrieval and abstention | Ranked note retrieval and bounded context are present. | Not measured; no answerable/unanswerable probes. |
| Correction and stale values | Profile version history and superseded-note filtering are present. | Not measured; no corrected-value probes. |
| Deletion leakage | Remove and disable lifecycle paths exist. | Not measured; no acknowledged-delete probes. |
| Scope isolation | Working-directory filtering is conditional; profile facts are not scoped. | Not measured; no cross-scope probes. |
| Evidence and citations | Notes retain source/session metadata. | Not measured; no claim support or citation adjudication. |
| Retrieval latency | Optional vector scan is bounded by a ceiling. | Not measured; no latency samples. |
| Write-to-recall delay | Writes and background reflection are separate paths. | Not measured; no scheduled write/recall probes. |
| Tokens and cost | Prompt context is bounded and split among channels. | Not measured; no token or cost observations. |
| Storage efficiency | SQLite, FTS, and optional embedding tables are represented in source. | Not measured; no storage-byte capture. |

The metric definitions, fixture and status record describe the project protocol and planned probes only; they are not results for Atomic Agent. [[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[retrieval design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/retrieval.md>)]

## Limits and unknowns

This review covers selected documentation and TypeScript at one verified repository head. It does not establish retrieval accuracy, answer correctness, configuration on an installed copy, runtime latency, or memory cost. Conditional working-directory filtering does not establish tenant isolation, and source inspection cannot establish safe erasure from physical database artifacts or backups. The effect of the bounded vector scan on recall quality was not measured. [[user guide](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/docs/user/memory.md>)] [[schema](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-schema.ts>)] [[context provider](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-context-provider.ts>)] [[retrieval design](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/retrieval.md>)]

## Contact-list follow-up

The official pinned `SECURITY.md` publishes `support@atomicbot.ai` for private vulnerability reports. The official pinned README was also checked for a published contact address. [[SECURITY.md](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/SECURITY.md>)] [[README](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/README.md>)]

## Benchmark status

**Benchmark not run.** I did not execute Atomic Agent, its benchmark workload, or tests. All performance, quality, token/cost, and storage outcomes remain unmeasured; source structure and project metric definitions are not benchmark results. [[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Official repository](https://github.com/AtomicBot-ai/atomic-agent)
- [Current main branch head](https://github.com/AtomicBot-ai/atomic-agent/commit/89d65615e36b763b35bc81c1e64304bd2d0e5c7c)
- [Official main branch commit feed](https://github.com/AtomicBot-ai/atomic-agent/commits/main.atom)
- [README.md](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/README.md>)
- [docs/user/memory.md](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/docs/user/memory.md>)
- [src/memory/README.md](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/README.md>)
- [src/memory/memory-schema.ts](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-schema.ts>)
- [src/memory/memory-store.ts](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-store.ts>)
- [src/memory/profile-store.ts](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/profile-store.ts>)
- [src/memory/memory-context-provider.ts](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/memory-context-provider.ts>)
- [src/memory/docs/retrieval.md](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/retrieval.md>)
- [src/memory/docs/formation.md](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/src/memory/docs/formation.md>)
- [SECURITY.md](<https://github.com/AtomicBot-ai/atomic-agent/blob/89d65615e36b763b35bc81c1e64304bd2d0e5c7c/SECURITY.md>)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster identity and attribution](../data/memory-systems.json)
- [Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/atomic-agent.md)
