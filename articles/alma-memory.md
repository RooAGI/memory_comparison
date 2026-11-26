# ALMA — source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 49 / ALMA / alma-memory  
**Listed repository locator:** [RBKunnela/ALMA-memory](https://github.com/RBKunnela/ALMA-memory)  
**Current canonical repository:** [RBKunnela/ALMA-memory](https://github.com/RBKunnela/ALMA-memory)  
**Default branch / reviewed head:** main / `4365767478b42f1f4bb79b4a2835d91ea1b4fb41`  
**Review time:** 2026-11-24 20:28:28 UTC (12:28:28 PST; America/Los_Angeles).

## Identity and scope

The curated roster places **ALMA** at ordinal 49, slug `alma-memory`, and lists `https://github.com/RBKunnela/ALMA-memory`. Its Agent Memory Atlas locator is preserved only for identity and source attribution; Atlas descriptions, marks, and layout are not assessment evidence.[[curated roster](../data/memory-systems.json)] [[Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/alma-memory.md)]

The official repository page identifies the public repository and shows `main` as its default branch. The official main-branch Atom feed names full head `4365767478b42f1f4bb79b4a2835d91ea1b4fb41`; this review is pinned to that revision.[[repository and default branch](https://github.com/RBKunnela/ALMA-memory)] [[main commit feed](https://github.com/RBKunnela/ALMA-memory/commits/main.atom)] [[reviewed commit](https://github.com/RBKunnela/ALMA-memory/commit/4365767478b42f1f4bb79b4a2835d91ea1b4fb41)]

## Who and what

The official README calls ALMA a local-first agent learning and memory library, rather than a hosted service. It credits the project to `@RBKunnela` and describes Python and JavaScript interfaces, MCP integration, and configurable storage.[[README at reviewed revision](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/README.md)]

## Architecture and data model

The README presents a feedback cycle: retrieve context before work, record task outcomes afterward, and consolidate repeated outcomes into reusable heuristics or repeated failures into anti-patterns. It also documents five memory categories: heuristics, outcomes, anti-patterns, domain knowledge, and user preferences.[[README](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/README.md)]

The Python data classes give these records distinct fields. Heuristics carry an agent and project, condition/strategy, confidence, occurrence and success counts, validation and creation times, and optional embedding/metadata. Outcomes store task type and description, success, strategy, optional duration/error/feedback, timestamp, embedding, and metadata. Domain knowledge includes a source label, confidence, and last-verified time; preferences include a source and confidence; anti-patterns include a pattern, why it is bad, and an alternative.[[memory data types](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/types.py)]

For the SQLite backend, the source describes relational tables for the memory types and a separate embeddings table; SQLite is the structured store and FAISS is the vector index, with NumPy cosine search as a fallback when FAISS is unavailable. The storage base class also defines save and query contracts, with SQLite as one implementation among multiple configured backends.[[SQLite storage](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/storage/sqlite_local.py)] [[storage interface](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/storage/base.py)]

## Write, update, delete, and retrieval

**Write and update.** The README documents `learn(agent, task, outcome, strategy_used)` and describes automatic heuristic creation after three or more similar outcomes and anti-pattern creation after two or more similar failures. The data model supports reinforcement counts and user-supplied feedback. These are documented/code paths, not a measurement of extraction or consolidation quality.[[README](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/README.md)] [[memory data types](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/types.py)]

The selected storage interface defines save and read operations for its core records. I did not establish a uniform update or delete contract across the storage adapters from the inspected interface. The README describes decay, compression, consolidation, and archival; that description does not demonstrate complete physical erasure or consistent behavior across backends.[[storage interface](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/storage/base.py)] [[README](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/README.md)]

**Retrieval.** The README demonstrates `retrieve(task, agent)`. The retrieval engine accepts query, agent, project, optional user, top-k, sharing scope, and a workflow scope filter. It embeds a sanitized query, retrieves records from storage, ranks them using similarity, recency, success rate, and confidence, and supports an optional feedback-aware reranker. It can cache query results and exposes cache controls; the code returns retrieval timing and records embedding latency. These source-visible mechanisms do not establish recall quality, end-to-end latency, or write-to-recall delay.[[README](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/README.md)] [[retrieval engine](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/retrieval/engine.py)] [[SQLite storage](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/storage/sqlite_local.py)] [[observability metrics](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/observability/metrics.py)]

## Scope isolation

Memory records and retrieval calls carry `project_id` and `agent`; the retrieval API also accepts a `MemoryScope` for inherited-agent sharing and a `ScopeFilter` with tenant, workflow, run, node, and branch identifiers. Shared retrieval is intentionally configurable and marks inherited origin in metadata. This is evidence of scope parameters and filtering paths, not a security guarantee: this review did not trace every backend query, integration, or authorization boundary and did not run cross-scope probes.[[memory data types](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/types.py)] [[retrieval engine](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/retrieval/engine.py)] [[SQLite storage](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/storage/sqlite_local.py)]

## Provenance and evidence

The typed records retain some provenance indicators, including preference source, domain-knowledge source and verification time, outcome metadata, and agent/project identity. The verification module models `verified`, `uncertain`, `contradicted`, and `unverifiable` states with confidence, reason, method, contradicting source, and verification time. The README describes persistence of verification status when storage is connected. This is record-level provenance and conflict state; the inspected sources do not establish claim-level citations to source passages or adjudicated evidence support for generated answers.[[memory data types](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/types.py)] [[verification model](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/retrieval/verification.py)] [[README](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/README.md)]

## Source-visible efficiency and observability

The SQLite implementation keeps vectors in a separate table and uses per-memory-type FAISS indexes, falling back to NumPy cosine similarity when FAISS is absent. The retrieval engine includes configurable caching, result scoring, query sanitization, embedding-dimension validation, and metrics/tracing/logging hooks. Its source records embedding latency and retrieval duration and exposes cache statistics. These are implementation observations; no latency, token, cost, or storage measurements were collected.[[SQLite storage](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/storage/sqlite_local.py)] [[retrieval engine](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/retrieval/engine.py)] [[observability metrics](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/observability/metrics.py)]

## Metric-domain evidence

All project benchmark outcomes are **unmeasured** for this review:

- **Answerable recall and abstention:** retrieval and ranking are visible in source; no answerability or abstention probes were run.
- **Correction accuracy and stale values:** types expose update/reinforcement-related fields and the README describes learning cycles; no correction workload or stale-value probe was run.
- **Deletion leakage:** the README describes lifecycle and archival, but a uniform deletion path was not established; no deletion or post-delete probe was run.
- **Scope isolation:** project, agent, inherited-agent, and workflow scope fields are visible; no forbidden cross-scope probes were run.
- **Evidence support and citation coverage:** verification states are modeled, but claim-level citations were not established or adjudicated.
- **Latency and write-to-recall delay:** code exposes some timing hooks; no end-to-end latency or delayed-recall measurements were collected.
- **Tokens, cost, and storage efficiency:** no provider usage, cost, or database-size measurements were collected.
- **Source-visible instrumentation:** retrieval and embedding timing, metrics/tracing hooks, and cache statistics are present in code; these do not constitute benchmark results.

The project’s [metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) define the protocol and show project-wide status only; they are not ALMA results.[[project metrics](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This bounded review inspected the official README and selected current source for record types, the storage interface and SQLite backend, retrieval, verification, and observability. It did not inspect every learning/consolidation path, adapter, migration, MCP operation, or database policy. It cannot establish the correctness of extracted memories, consistency of update/deletion semantics, isolation across every backend, or performance and quality under workload.

The official pinned README was checked for a published contact email and lists `dev@friendlyai.fi` under Questions; the exact URL is recorded in the JSON review record.[[official README contact](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/README.md)]

## Benchmark status

**Benchmark not run.** No ALMA runtime, benchmark workload, or tests were executed. Project metric definitions, fixture, and execution status are protocol/status references only.[[project metrics](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Official repository and default branch](https://github.com/RBKunnela/ALMA-memory)
- [Official main branch commit feed](https://github.com/RBKunnela/ALMA-memory/commits/main.atom)
- [Reviewed commit](https://github.com/RBKunnela/ALMA-memory/commit/4365767478b42f1f4bb79b4a2835d91ea1b4fb41)
- [README at reviewed revision](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/README.md)
- [Memory data types](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/types.py)
- [Storage interface](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/storage/base.py)
- [SQLite storage](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/storage/sqlite_local.py)
- [Retrieval engine](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/retrieval/engine.py)
- [Verification model](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/retrieval/verification.py)
- [Observability metrics](https://github.com/RBKunnela/ALMA-memory/blob/4365767478b42f1f4bb79b4a2835d91ea1b4fb41/alma/observability/metrics.py)
- [Project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json)
- [Curated roster identity and attribution only](../data/memory-systems.json)
