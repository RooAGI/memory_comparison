# Animus source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 57 / Animus / animus  
**Listed repository locator:** [railstracks/animus](https://github.com/railstracks/animus)  
**Catalog source attribution:** [Atlas catalog report at pinned revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/animus.md)  
**Canonical repository:** [railstracks/animus](https://github.com/railstracks/animus)  
**Default branch / reviewed head:** main / [13609b59ab2cd944fcd50aeb36df5c061dc29ba0](https://github.com/railstracks/animus/commit/13609b59ab2cd944fcd50aeb36df5c061dc29ba0)  
**Review time:** 2026-11-24 20:48:26 UTC (12:48:26 PST; America/Los_Angeles). GitHub repository metadata identified main as default branch; the official current-commit API resolved its full SHA, matching the official commit page.  
**Published contact:** No email was published in the checked [official pinned README](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/README.md) or [official project website](https://animus.steadyfort.com/); the JSON record stores null and both checked URLs.

## Identity and review pin

The curated roster places **Animus** at ordinal 57 with slug `animus`, listed locator `https://github.com/railstracks/animus`, and a pinned Atlas source URL for attribution. I used the roster only for identity and attribution; its descriptions, marks, report text, and layout are not assessment evidence.[[roster](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/animus.md)]

The official repository page identifies `railstracks/animus` and `main` as the default branch. GitHub's current commit lookup returned full head `13609b59ab2cd944fcd50aeb36df5c061dc29ba0`; selected source links below pin that revision.[[repository metadata](https://api.github.com/repos/railstracks/animus)] [[head commit](https://github.com/railstracks/animus/commit/13609b59ab2cd944fcd50aeb36df5c061dc29ba0)]

## Summary

Animus is a self-hosted C++ agent framework with a multi-part memory subsystem: per-agent episodic observations, semantic ontology, raw memory files, consolidation, and unified search/context assembly. The inspected source establishes storage fields and selected mutation/search paths, not measured recall quality or speed.[[README](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/README.md)] [[MemoryStore header](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/include/animus_kernel/MemoryStore.h)] [[MemorySearch](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemorySearch.cpp)]

## Who and what

The README describes Animus as an open-source, self-hosted C++ framework/runtime for persistent AI agents, with memory, tools, and communication adapters. GitHub identifies the repository owner account as railstracks; the official site footer attributes the site to GMR Ventures BV.[[README](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/README.md)] [[official website](https://animus.steadyfort.com/)]

## Architecture and data model

**Code and documentation observations.** The README describes four connected memory areas: episodic observations in configurable temporal layers; a semantic ontology with per-agent worldviews and evidence-linked properties; raw MemoryFiles with chunking and embeddings; and unified search across observations, ontology, files, diary, and sessions. Active memory provides assembled context, and a consolidation pipeline handles intake, review, and perspectives.[[README](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/README.md)]

The inspected public data model gives a MemoryLayer an owning agent, name, horizon hint, order, evaluation interval, cron schedule, prompts, token budget, and enabled flag. An Observation stores layer and agent IDs, text, weight, decay rate, tags, source, timestamps, review schedule, lifecycle state, and a `superseded_by` link. A LayerPerspective has retrospective, current, and future text with valence fields.[[MemoryStore header](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/include/animus_kernel/MemoryStore.h)]

`MemoryMutation` records mutation kind, target, prior state, optional layer transition, motivation, timestamp, and a full-row JSON snapshot. The serializer includes the observation text and lifecycle/provenance fields. MemoryFiles have a source path, type, content, mutability, agent association, superseded/status state, and import times; chunks store path, heading, line bounds, content hash, text, and optional embedding data.[[MemoryStore header](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/include/animus_kernel/MemoryStore.h)] [[MemoryStore implementation](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemoryStore.cpp)] [[MemoryFileStore](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemoryFileStore.cpp)]

The README names ontology and active-context components, but their implementations were not inspected here. Their detailed schema and enforcement behavior remain documentation claims in this review.[[README](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/README.md)]

## Write, update, delete, and retrieval

**Write.** The public API creates and updates layers; creates observations, including agent-scoped observations; changes memory state; records evaluation times; sets perspectives; and logs mutations. `ReviseObservation` is documented as copy-on-write and returns a new ID while preserving the previous version. A source override can label the revision. The README describes durable retirement and full-row mutation snapshots on destructive paths.[[MemoryStore header](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/include/animus_kernel/MemoryStore.h)] [[MemoryStore implementation](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemoryStore.cpp)] [[README](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/README.md)]

**Update and correction.** The explicit revision method creates a version chain available through `GetObservationHistory`. This is a code-visible correction mechanism; I did not verify that every write path uses it or measure whether all retrieval paths consistently choose the corrected value. The inspected implementation also documents a retired-wins-until-revised guard for identical observations that are re-derived.[[MemoryStore header](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/include/animus_kernel/MemoryStore.h)] [[MemoryStore implementation](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemoryStore.cpp)]

**Delete and retire.** The README describes lifecycle states `new → current → deprecated`, durable retirement tombstones, and explicit revision as the revival route. The public API includes agent-layer deletion and memory-state changes. The selected sources do not establish physical erasure across indexes, mutation history, backups, federation peers, or exports.[[README](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/README.md)] [[MemoryStore header](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/include/animus_kernel/MemoryStore.h)] [[MemoryStore implementation](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemoryStore.cpp)]

**Retrieval.** The inspected search code creates SQLite FTS5 indexes and synchronization triggers, or PostgreSQL `tsvector` columns with a GIN index, for observations. It normalizes backend scores, merges and sorts results, and enforces the requested result limit. The README documents unified search across memory domains; active-context assembly was not traced end to end.[[MemorySearch](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemorySearch.cpp)] [[README](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/README.md)]

**Scope isolation.** Layers and observations carry `agent_id`; per-agent APIs bind that key into queries, and the inspected unified search source filters by agent key. The header also retains legacy observation calls without an agent argument. These are code-level partitioning signals, not proof of authorization or complete tenant isolation. No cross-agent probes were run.[[MemoryStore header](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/include/animus_kernel/MemoryStore.h)] [[MemoryStore implementation](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemoryStore.cpp)] [[MemorySearch](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemorySearch.cpp)]

**Provenance and evidence.** Observations retain a source field; mutation snapshots and motivations preserve prior state and change context. The README describes ontology properties linked to evidence, while MemoryFiles and chunks retain source paths, line bounds, and content hashes. These support traceability, but do not establish truth, evidence quality, or complete citation propagation into generated responses.[[MemoryStore header](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/include/animus_kernel/MemoryStore.h)] [[MemoryStore implementation](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemoryStore.cpp)] [[MemoryFileStore](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemoryFileStore.cpp)] [[README](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/README.md)]

## Metric-domain evidence

All rows below are **unmeasured**. Indexes, schema fields, and documented behavior are source observations, not benchmark outcomes.[[metric definitions](../METRICS.md)] [[status record](../results/initial-baselines-status.json)]

| Domain | Source observations | Measurement status |
|---|---|---|
| Answerable recall and abstention | Search and context components exist; no adjudicated fixture outputs were collected. | Unmeasured |
| Correction and stale values | Copy-on-write revision and lifecycle state are visible; no post-correction probes were run. | Unmeasured |
| Deletion leakage | Retirement and mutation history exist; no post-delete probes or erasure audit were run. | Unmeasured |
| Scope isolation | Per-agent fields and query filters are present; no cross-agent probes were run. | Unmeasured |
| Evidence support and citation coverage | Source/provenance fields and documented evidence links exist; no response claims were adjudicated. | Unmeasured |
| Latency and write-to-recall delay | Index design is visible; no timing was collected. | Unmeasured |
| Tokens and cost | No model usage was observed. | Unmeasured |
| Storage efficiency | No persistent bytes were measured. | Unmeasured |

## Limits and unknowns

This is a bounded, read-only inspection of selected docs and code at one verified main-branch SHA. It does not establish runtime correctness, reliability, security, deployment suitability, or measured performance. Per-agent query predicates do not by themselves prove authorization boundaries, and legacy unscoped APIs remain visible. Retirement does not demonstrate physical erasure from every derived or replicated copy. Ontology and active-context internals, complete MemoryFile ingestion and cleanup paths, and generated-answer evidence propagation remain uninspected.

## Benchmark status

**Benchmark not run.** The shared execution record remains `not_run`; planned fixture counts are not measured denominators. No Animus runtime, benchmarks, or tests were run, and no metric values are reported.[[metrics](../METRICS.md)] [[status record](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current repository](https://github.com/railstracks/animus)
- [GitHub repository metadata](https://api.github.com/repos/railstracks/animus)
- [Full-SHA main head commit](https://github.com/railstracks/animus/commit/13609b59ab2cd944fcd50aeb36df5c061dc29ba0)
- [README.md at reviewed SHA](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/README.md)
- [MemoryStore public header](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/include/animus_kernel/MemoryStore.h)
- [MemoryStore implementation](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemoryStore.cpp)
- [MemorySearch implementation](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemorySearch.cpp)
- [MemoryFileStore implementation](https://github.com/railstracks/animus/blob/13609b59ab2cd944fcd50aeb36df5c061dc29ba0/src/kernel/memory/MemoryFileStore.cpp)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution status](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster identity and attribution](../data/memory-systems.json)
- [Official project website](https://animus.steadyfort.com/)
