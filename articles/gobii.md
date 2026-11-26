# Gobii source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 263 / Gobii / `gobii`  
**Listed repository locator:** [gobii-ai/gobii-platform](https://github.com/gobii-ai/gobii-platform)  
**Canonical upstream:** [gobii-ai/gobii-platform](https://github.com/gobii-ai/gobii-platform)  
**Default branch / reviewed head:** main / [c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb](https://github.com/gobii-ai/gobii-platform/commit/c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb)  
**Review time:** 2026-11-25 21:12:02 UTC (2026-11-25 13:12:02 PST; America/Los_Angeles).

## Identity and review pin

The project catalog lists Gobii at ordinal 263, slug `gobii`, with the explicit repository locator `https://github.com/gobii-ai/gobii-platform`. Its pinned Agent Memory Atlas entry is recorded only as roster attribution, not as assessment evidence. The official GitHub repository API identifies `main` as the default branch and returns the full current head SHA above; a fresh shallow checkout of `main` resolved to the same SHA. The review timestamp is when the repository metadata and source were checked.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Gobii is an open-source platform for persistent, always-on agents. Its memory behavior is split between agent-authored tables in a per-agent SQLite database and separate summaries of older messages and execution steps. Agents can create and query their own SQL schemas through `sqlite_batch`; Gobii also supplies schema context, execution guardrails, SQL recovery/advice, and compacted history in prompts. This source review does not establish answer quality or measured performance.[[readme]][[sqlite-state]][[sqlite-batch]][[history-compaction]]

## Who and what

The official README describes this repository as the open-source Gobii Platform for self-hosting and development, with a hosted product at gobii.ai. It presents a durable agent runtime rather than a standalone memory library or memory-only API. No individual maintainer identity was inferred from commit or profile metadata.[[readme]]

## Architecture and data model

The README describes Gobii as an always-on, event-driven agent platform and calls its memory substrate “SQLite-native operational state.” The agent SQLite helper restores one SQLite archive keyed by agent UUID from configured object storage into a temporary working directory, coordinates access, then validates, compresses, and persists the resulting database. The code drops eight built-in ephemeral tables before persistence; the remaining schema is whatever the agent has authored, so there is no single framework-defined durable memory record type.[[readme]][[sqlite-state]]

For conversational and execution history, Django stores `PersistentAgentCommsSnapshot` and `PersistentAgentStepSnapshot` records. Each includes an agent foreign key, an optional link to the previous snapshot, an inclusive `snapshot_until` cutoff, summary text, and creation time. Snapshot uniqueness and indexes are per agent and cutoff. New summaries extend the previous summary; the prompt builder inserts the latest message and step summaries alongside a detailed recent tail.[[models]][[compaction]][[history-compaction]][[prompt-context]]

## Write, update, delete, and retrieval

**Write and update.** An agent defines its durable data model and uses SQL through `sqlite_batch`; ordinary SQL inserts, updates, and deletes apply to that schema. Gobii introspects the database and gives the agent a bounded schema description including table definitions, row counts, and compact samples. Query execution is wrapped in a transaction, and failed batches roll back. Selected syntax and schema errors can be retried with reported corrections. The application also has built-in ephemeral state tables, which are removed before the durable database snapshot is saved.[[sqlite-state]][[sqlite-batch]][[sqlite-autocorrect]]

**Delete.** SQL can remove records from an agent-authored table; the reviewed sources do not define a semantic memory-delete API, record-level tombstone, or general mutation history for those rows. Database state is stored separately per agent, but deletion propagation, recovery, and retention behavior for a particular user-authored record were not established in this inspection. A database above 100 MB is deleted from object storage instead of being persisted, according to the state helper; this is a database-size fallback, not a per-memory deletion feature.[[sqlite-batch]][[sqlite-state]]

**Retrieval.** The documented path is agent-authored SQL against the agent's SQLite tables. Gobii injects a schema prompt capped at 30,000 bytes and 25 tables, with bounded row samples, to help the model query its own evolving schema. Tool results are available in a temporary `__tool_results` table during a cycle; that and other built-in operational tables are dropped before persistence. This review did not score whether SQL retrieval finds answer-bearing records or abstains appropriately.[[sqlite-state]][[sqlite-batch]]

History retrieval is separate from the agent-authored SQL database: the prompt builder selects each agent's most recent step and communications snapshots, then includes newer raw events after the respective cutoff. Compaction is scheduled when configured raw history limits are exceeded; it checks that the captured range has not changed before committing a new snapshot. Raw messages are retained by the compaction path, and long-term pruning is out of scope there.[[history-compaction]][[compaction]][[prompt-context]]

## Scope isolation

The durable SQLite object key includes the agent UUID, and agent database access is coordinated by UUID. The snapshots have an explicit agent foreign key; prompt and compaction queries filter snapshots and raw histories by that agent. These are code-level per-agent boundaries. This review did not run cross-agent isolation probes or establish the behavior of every deployment storage backend and authorization path.[[sqlite-state]][[models]][[history-compaction]][[prompt-context]]

The SQLite connection authorizer blocks ATTACH/DETACH and selected dangerous functions and PRAGMAs in regular agent query connections; it also enforces a query timeout through a progress handler. These restrictions constrain database access, but do not constitute a tested tenant-isolation guarantee for a deployed Gobii instance.[[sqlite-guardrails]]

## Provenance and evidence

The durable SQLite schema is authored by the agent, so record-level provenance is optional unless the agent's schema and writes include it. Gobii's SQL quality advisory code encourages deriving structured values from tool results and retaining `result_id` or `source_url` provenance, but this is guidance and instrumentation rather than a mandatory memory evidence model. Tool results are cycle-scoped and are removed before the agent database is persisted. No reviewed path establishes that recalled claims are source-supported or that generated answers carry citations.[[sqlite-query-quality]][[sqlite-state]][[sqlite-batch]]

The compaction prompt instructs the summarizer to preserve identifiers, evidence links, decisions, commitments, attribution, and source channel, and to replace superseded state. This is a prompt-level policy; no assessment of summary fidelity was performed.[[compaction]]

## Efficiency and observability

SQLite keeps the agent-authored durable store embedded in the platform; storage state is restored to a temporary file and persisted as a validated compressed archive. Schema presentation is capped by bytes and table count, and samples are limited to control prompt size. Query tooling supports batches and set-wise data handling, while query-quality advisories identify some inefficient repeated-result and literal-copy patterns.[[sqlite-state]][[sqlite-query-quality]][[sqlite-batch]]

Compaction code emits tracing attributes for counts, cutoffs, creation, and skips; the SQLite persistence path records validation, byte-size, duration, and persistence status, and the step summarizer records completion usage through Gobii's completion accounting. These code paths provide observability hooks, but this review collected no latency, token, cost, or storage measurements.[[history-compaction]][[compaction]][[sqlite-state]][[step-compaction]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Gobii in this review. Source code and documentation are not benchmark results. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the project's evaluation protocol and shared execution state, not Gobii results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Agent-authored SQL retrieval is present; answer quality and abstention were not scored. | Unmeasured |
| Correction and stale values | SQL permits model-authored updates; no correction sequence was assessed. | Unmeasured |
| Deletion leakage | SQL deletion and per-agent storage exist; no deletion probe or recovery audit was run. | Unmeasured |
| Scope isolation | Per-agent database keys and agent-filtered snapshots are present; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Provenance can be represented and is encouraged by query advisories; no answer evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timings were collected. | Unmeasured |
| Tokens, cost, and storage | Schema bounds and completion telemetry exist; no workload, billing, token, or storage comparison was made. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the official README and selected current implementation files at the verified upstream head. Gobii, its tests, and benchmark workloads were not run. The source shows a flexible agent-authored SQL store, but does not establish which facts an agent will retain, whether a generated query is correct, or whether a returned row supports an answer.[[readme]][[sqlite-state]][[sqlite-batch]]

The review did not inspect every tool path, object-storage backend, deployment policy, backup process, or account-level authorization boundary. It did not test whether a database-size persistence fallback can lose valuable state in a deployment, how user-authored deletes interact with backups, or how summary errors recover over repeated compaction attempts. Those operational outcomes remain unknown here.[[sqlite-state]][[compaction]][[history-compaction]]

## Benchmark status

**Benchmark not run.** No Gobii runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json); these describe the project protocol and status, not Gobii measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email; none was present. The structured record stores `contact_email: null` and the exact checked URL. No address was inferred from commit/profile metadata or obtained from a third-party directory.[[readme]]

## Sources

All upstream source file citations are pinned to the verified full SHA. The Atlas source records curated roster attribution only and is excluded from system assessment evidence. See the structured record [gobii.json](../data/system-reviews/gobii.json) and [curated roster](../data/memory-systems.json).
