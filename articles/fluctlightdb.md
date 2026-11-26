# FluctlightDB source and design review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 245 / FluctlightDB / `fluctlightdb`  
**Listed repository locator:** [voxmastery/FluctlightDB](https://github.com/voxmastery/FluctlightDB)  
**Canonical upstream:** [voxmastery/FluctlightDB](https://github.com/voxmastery/FluctlightDB)  
**Default branch / reviewed head:** main / [f8ef9d609ff39b4770b257aaf64d7feb74a08b7a](https://github.com/voxmastery/FluctlightDB/commit/f8ef9d609ff39b4770b257aaf64d7feb74a08b7a)  
**Review time:** 2026-11-25 23:46:30 UTC (2026-11-25 15:46:30 PST; America/Los_Angeles).

## Identity and review pin

The catalog records ordinal 245 as FluctlightDB (`fluctlightdb`) and lists the repository explicitly. Its pinned Agent Memory Atlas entry is retained only as curated identity and locator attribution; Atlas descriptions are not assessment evidence. The official GitHub repository page identifies `main` as the default branch, and its official `main.atom` feed identifies current full head `f8ef9d609ff39b4770b257aaf64d7feb74a08b7a`, updated 2026-11-03T06:20:01Z. The review is pinned to that head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

FluctlightDB is a Rust memory engine with Python and HTTP interfaces. It stores episodic memories as Episodes inside neural Engrams and recalls them from cues through an index and graph activation path. A brain is persisted in a local brain directory or legacy file; multi-agent and server setups add per-agent or per-tenant storage and access configuration.[[readme]][[types]][[engram]][[store]]

## Who and what

The official repository presents FluctlightDB as a database engine for AI-agent memory, with a Rust core and Python SDK, plus optional HTTP and MCP interfaces. The repository is under the voxmastery GitHub account; this review does not infer an individual maintainer identity from commit or profile metadata.[[repo]][[readme]]

## Architecture and data model

`FluctlightBrain` aggregates life and development state, a synapse graph, hippocampal and cortical structures, amygdala and prefrontal state, and other systems. An `Episode` stores content, context, optional outcome, salience, optional semantic vector, optional agent and tenant IDs, optional RAG reference, and optional provenance. An `Engram` links an episode to sparse neuron sets, salience, and encoding metadata.[[brain]][[types]][[engram]]

The README describes `activate(cue)` as combining FTS5/vector candidates with graph spreading; the activation source implements cue-driven propagation over the brain graph and supports vector-fast and agent-fast paths. The Python entry points include `connect_embedded()` for local use and `connect_project()` for multi-tool project memory, with HTTP/MCP integrations available separately.[[readme]][[activation]][[multi-agent]]

Persistence is explicit. The README example flushes working memory at turn end and calls `checkpoint()`; the store code writes atomic snapshots in v3 or v4 layouts and truncates and flushes the WAL after a successful locked save. Optional backup and post-save verification are controlled by environment settings.[[readme]][[store]]

## Write, update, delete, and retrieval

**Write.** `experience()` records an episode as an Engram. `wm_push()` adds working-memory content, which can be flushed with `turn_end(flush=True)`. The caller supplies episode content and fields such as salience, optional semantic vector, scope IDs, and provenance.[[readme]][[types]][[engram]]

**Update and correction.** The inspected CLI reference documents new writes and forgetting an Engram by UUID, but does not describe an in-place edit or versioned correction API. A caller can remove an old Engram and write a corrected experience; this review did not establish atomic replacement or retained correction history.[[cli]][[readme]]

**Delete.** The shell exposes `forget UUID` (with `--writable`), and the HTTP query operations include `forget` and `forget_before`. These are explicit removal operations. The inspected sources do not establish erasure from backups, replicas, prior exports or every derived/cache structure, and do not document a deletion audit receipt.[[cli]][[store]][[security]]

**Retrieval.** `recall()` serves same-turn working memory; `activate(cue)` retrieves from a cue using graph spreading and can use index candidates and optional semantic input. Results include matched Episodes, activation/completion values and diagnostic fields. HTTP activation responses are capped, with the CLI reference documenting a default API limit of eight.[[readme]][[activation]][[types]][[cli]]

## Scope isolation

The getting-started guide recommends one brain folder per agent and describes tenant-specific server paths. `Episode` also has optional `agent_id` and `tenant_id` fields, while `TenantConfig` resolves tenant storage under a hashed path and checks that the locus remains under the configured tenant root. The multi-agent guide describes a shared project hub plus per-tool agent brains. These are storage and metadata mechanisms; this review did not establish automatic scope filtering for arbitrary embedded callers or measure isolation.[[getting-started]][[types]][[tenant]][[multi-agent]]

## Provenance and evidence

`Episode.provenance` can store a provenance kind, source URI, confidence, and a `verified` flag; kinds distinguish chat assertions, file observations, tool-grounded information, ledger-verified information, and user-explicit content. An optional RAG reference can retain source URI, document ID, and chunk ID. The confidence module combines source kind, recency, and corroboration into a confidence score used as an activation multiplier.[[types]][[confidence]]

These fields provide provenance metadata and ranking signals, but the inspected types do not prove that the caller's `verified` value is independently checked, nor do they define claim-to-source citation adjudication. Evidence support and citation quality therefore remain unmeasured here.[[types]][[confidence]][[metrics]]

## Efficiency and observability

The README describes a local embedded path, hybrid indexing, and graph recall; the CLI reference documents an activation cache and a default candidate cap. These are code/documentation observations, not latency results. `ExperienceReport`, `SleepReport`, `VizExport`, and status/export commands expose separation, gate, replay, pruning, and brain-size signals, while the README describes a graph viewer. The inspected sources do not establish a general tracing or production metrics interface.[[readme]][[activation]][[cli]][[types]]

## Metric-domain evidence

All benchmark domains are **unmeasured in this review**. The README includes maintainer-reported benchmark claims and notes their reproduction caveats; none was reproduced or treated as a result here. No FluctlightDB runtime, tests, or benchmarks were run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[readme]][[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Cue-based recall and graph activation are implemented; no answer/abstention workload was scored. | Unmeasured |
| Correction and stale values | Forget plus a new write is documented; no correction sequence was measured. | Unmeasured |
| Deletion leakage | Forget operations exist; no post-delete or durable-erasure probe was run. | Unmeasured |
| Scope isolation | Per-agent and tenant-specific storage are documented; no leakage workload was run. | Unmeasured |
| Evidence support and citation coverage | Provenance and RAG references exist; no claims or citations were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Fast paths and index/cache controls are documented; no timings were collected. | Unmeasured |
| Tokens, cost and storage | Snapshot and WAL formats were inspected; no workload token, cost, or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This is a source review of current `main`, not a runtime assessment. FluctlightDB has multiple connection modes and optional retrieval features, so actual behavior depends on mode and configuration. Public benchmark figures in the README are maintainer-reported and were not independently reproduced for this task.[[head]][[readme]][[activation]]

Scope depends on how callers provision and select brain paths and server tenant configuration. The optional Episode scope fields are not evidence that every embedded recall is filtered. The official security policy says the service has not had a professional penetration test or formal security audit and that HTTP multi-tenant serve is not production-hardened.[[types]][[getting-started]][[tenant]][[multi-agent]][[security]]

The pinned getting-started guide contains older package-version examples than the current README, so some usage details may lag. No quality, correction, deletion-leakage, scope-isolation, latency, token, cost, or storage result was measured here.[[readme]][[getting-started]][[metrics]][[fixture]][[status]]

## Benchmark status

**Benchmark not run.** No FluctlightDB runtime, tests, or benchmarks were executed for this review. Upstream README performance claims are not results measured here. See [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and SECURITY.md were checked for a published contact email. They direct contact through GitHub but publish no email address. The structured record therefore stores `contact_email: null` and both exact checked URLs; no commit/profile metadata or third-party directory was used.[[readme]][[security]]

## Sources

Upstream code and documentation citations are pinned to the verified full SHA. The Atlas source appears only for roster identity/locator attribution and is not assessment evidence. See the structured [FluctlightDB review record](../data/system-reviews/fluctlightdb.json) and [curated roster](../data/memory-systems.json).
