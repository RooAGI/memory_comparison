# Hivemind source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 300 / Hivemind / `hivemind`  
**Listed repository locator:** [causewayai/hivemind](https://github.com/causewayai/hivemind)  
**Canonical upstream:** [causewayai/hivemind](https://github.com/causewayai/hivemind)  
**Default branch / reviewed head:** main / [666bfa105a2f70ce53b2704fe896cd14138716f0](https://github.com/causewayai/hivemind/commit/666bfa105a2f70ce53b2704fe896cd14138716f0)  
**Review time:** 2026-11-25 23:12:05 UTC (2026-11-25 15:12:05 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists Hivemind at ordinal 300, slug `hivemind`, with the explicit locator `https://github.com/causewayai/hivemind`. Its pinned Agent Memory Atlas entry is retained only as roster attribution and is not assessment evidence. The official GitHub repository API identifies `main` as the default branch; the official commits/main API reports current full head `666bfa105a2f70ce53b2704fe896cd14138716f0`. The reviewed README and source files were fetched from that pinned commit through official GitHub API content endpoints. The review timestamp records when the repository and source were checked.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Hivemind is a local MCP memory daemon backed by SQLite structured records and sqlite-vec embeddings. It supports private session memories, shared local user memories, and an optional cache workflow for GitHub Actions logs. Its built-in embedding provider is a deterministic hash stand-in, explicitly not semantic, so this source review makes no claim about conceptual recall quality.[[readme]][[daemon]][[schema]][[embedding]]

## Who and what

The official README describes a local memory store for harnesses. The daemon speaks stateless MCP over loopback HTTP and exposes memory write/query and scope-listing tools. This repository is the Local Edition, intended for one machine and one user; the design notes describe cloud tenancy as a separate concern.[[readme]][[daemon]][[design]]

## Architecture and data model

The SQLite database has a structured `memory_entries` table for content, scope, optional session ID, source, source type, optional external ID, and timestamps. Tags live in a separate table, with a cascading schema relation; embeddings use a sqlite-vec `vec0` table. A partial unique index makes non-null `(source, external_id, scope)` keys unique. The store opens one database with WAL mode and a busy timeout.[[schema]][[db-open]][[store]]

At daemon startup, Hivemind registers `memory_write`, `memory_query`, and `list_scopes` on a stateless Streamable HTTP MCP handler bound to `127.0.0.1`. The caller supplies a stable `session_id`; it is not derived from the MCP transport session. The separate CI-log workflow stores raw files locally and adds run-summary and failed-job memory entries.[[daemon]][[readme]][[ci-rules]]

## Write, update, delete, and retrieval

**Write.** `memory_write` defaults to `session` scope and `harness` source type. It accepts optional tags, a precomputed embedding, scope, source type, and external ID; if no embedding is supplied, the daemon uses its configured provider. A new entry, tags, and vector are written transactionally.[[write]][[store]]

With an external ID, the key is `(source, external_id, scope)`. Repeating the same key returns the existing entry unchanged, including its content, tags, and embedding. This is insert-if-absent ingestion, not update-in-place; the inspected MCP tool set has no general correction/update operation.[[schema]][[store]][[readme]]

**Delete.** No general MCP forget/delete tool appears in the registered tools. The store does implement transactional deletion of a memory row, its tags, and vector. The CI-log retention worker calls it for entries associated with log files removed by age or size policy. The README also documents resetting the whole store by deleting the database and its WAL/SHM files.[[daemon]][[store]][[retention]][[readme]]

**Retrieval.** For free-text queries, the handler embeds the query and separately retrieves the caller’s session-scope entries and shared user-scope entries. The store searches a candidate pool up to five times `top_k`, applies an L2-distance cutoff of 1.0, then filters by scope, session ID, source, and any matching requested tag. Structured-only queries skip embedding and the distance cutoff; they filter on exact external ID, tags, or source, order each scope’s results newest first, append the session results before the shared-user results, and truncate the combined list to `top_k`.[[query]][[store]][[readme]]

The default `HashProvider` is a deterministic non-semantic stand-in. The README says it can find identical or near-identical text, but not conceptual paraphrases; the design notes state that the 1.0 cutoff is calibrated to the hash provider and needs recalibration if a real embedding model is substituted.[[embedding]][[readme]][[design]]

## Scope isolation

The edition provides `session` and `user` scopes. Query handlers request only the caller-supplied session ID plus all `user`-scope memories; they do not request other session IDs. User-scope memories are deliberately shared among local harnesses. Because the daemon is stateless and trusts the supplied session ID, this is an application-level filter rather than an authenticated principal boundary. The review did not test isolation or hostile callers.[[scopes]][[query]][[readme]][[daemon]]

The write handler permits a direct `scope: "user"` write and clears its session ID. This is distinct from promoting an existing session record: the inspected tools have no promotion/update path. The checked code does not add human approval or caller identity checks for choosing the shared scope.[[write]][[readme]]

## Provenance and evidence

Entries retain a source label, a `harness` or `etl` source type, tags, and an optional external ID. These fields identify a writer or ingestion key, but the schema has no required source passage, evidence span, trust state, or mutation history. The insert-if-absent upsert also leaves conflicting repeat content unchanged. No reviewed path establishes answer citations or evidence support.[[schema]][[write]][[store]]

## Efficiency and observability

SQLite uses WAL mode and a configured busy timeout; vector retrieval requests a bounded candidate pool. The CI-log cache has age and soft-size caps, applied by an immediate and hourly background sweep. Sweep failures and nonzero removals are logged. These are implementation and instrumentation observations only; no latency, write-to-recall delay, token, cost, or storage measurements were collected.[[db-open]][[store]][[retention]][[ticker]][[metrics]]

## Metric-domain evidence

All benchmark domains remain **unmeasured** for Hivemind. The project metric definitions, fixture, and shared status record specify evaluation protocols and project execution state; none is a Hivemind result.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Free-text and structured query paths exist; no answer/abstention probes were scored. | Unmeasured |
| Correction accuracy and stale values | External-ID duplicates return existing entries unchanged; no correction sequence was assessed. | Unmeasured |
| Deletion leakage | Store deletion and CI-log cleanup exist; no post-delete probe or backup audit was run. | Unmeasured |
| Scope isolation | Query code applies a caller-supplied session filter and includes shared user scope; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Source labels and external IDs are available; no answer evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime query or scheduled recall timings were collected. | Unmeasured |
| Tokens, cost, and storage | SQLite, vector tables, and local log files are present; no workload accounting or storage measurement was made. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the official README, selected implementation files, and design notes at the verified head. Hivemind, tests, and benchmarks were not run. The source establishes available APIs and code paths, not whether users record useful memories or whether retrieval supports an answer.[[readme]][[store]][[metrics]]

The Local Edition has no separate user/tenant boundary: user scope is shared across local harnesses. Session isolation depends on the client supplying a stable, non-colliding session ID. The review did not test either property under adversarial use or inspect deployment hardening beyond the reviewed local daemon.[[readme]][[query]][[daemon]]

The default hash vectors do not encode meaning, and the fixed distance cutoff is tuned to those vectors. Recall under a semantic provider, provider replacement, or a changed embedding dimension remains unknown here. The semantic path also filters a bounded candidate pool, so filtered result counts under sparse candidate matches were not measured.[[embedding]][[store]][[design]]

The store deletion method removes the current entry, tags, and vector, but backup copies, copied database files, and downstream exports were outside this inspection. No general end-user deletion API or audit trail was found in the registered MCP tools.[[store]][[daemon]]

## Benchmark status

**Benchmark not run.** Hivemind, its tests, and benchmark workloads were not run. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) are project documents, not Hivemind measurement results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email; none was present. The structured record stores `contact_email: null` and the exact checked README URL. No address was inferred from commit/profile metadata or third-party directories.[[readme]]

## Sources

The catalog identity and Atlas attribution are recorded for curated roster context only; Atlas is not assessment evidence. Upstream implementation links use the full reviewed SHA. See the structured record [hivemind.json](../data/system-reviews/hivemind.json) and [curated roster](../data/memory-systems.json).
