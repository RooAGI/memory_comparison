# Heimdall source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 286 / Heimdall / `heimdall`  
**Listed repository locator:** [ArihantDeva/heimdall](https://github.com/ArihantDeva/heimdall)  
**Canonical upstream:** [ArihantDeva/heimdall](https://github.com/ArihantDeva/heimdall)  
**Default branch / reviewed head:** main / [0bce85902ef75e37ad9a6c097bda432d3b958203](https://github.com/ArihantDeva/heimdall/commit/0bce85902ef75e37ad9a6c097bda432d3b958203)  
**Review time:** 2026-11-25 22:38:20 UTC (2026-11-25 14:38:20 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Heimdall at ordinal 286, slug `heimdall`, with the explicit repository locator `https://github.com/ArihantDeva/heimdall`. The pinned Atlas entry is retained only to identify the curated roster attribution; it is not evidence for the assessment below. The official repository page identifies `main` as the default branch. GitHub’s official `commits/main` API identifies full head `0bce85902ef75e37ad9a6c097bda432d3b958203`, committed at 2026-11-02T04:32:48Z. This review is pinned to that SHA. [[catalog]][[atlas]][[repo]][[head]]

## Summary

Heimdall is a local agent-memory and code-knowledge system that watches selected workspaces, builds graph projections from files, and provides ranked search with file freshness and identity verdicts. Its default backend combines per-repository Graft code graphs with a global semantic index. The official README also describes an experimental fact-card layer; the two layers have different maturity and trust claims. This is a source review, not a runtime or performance evaluation. [[readme]][[journal]][[search]]

## Who and what

The official repository describes Heimdall as a CLI, daemon, and set of agent-harness integrations for persistent knowledge across repositories. It wires tools and rules into supported coding agents and can also expose an MCP server. The repository names Arihant Deva as the project author in its official commit metadata; this review does not use that metadata to source contact information. [[readme]][[repo]]

## Architecture and data model

The SQLite journal at `~/.heimdall/journal.db` is the authoritative index for paths, content hashes, sizes, timestamps, depth, generations, and presence state. It separately tracks the graph nodes and edges owned by each source path, unresolved cross-file edges, a deduplicating work queue, and an append-only `fact_history` for retracted fact-kind nodes. The journal schema uses WAL and full synchronous durability. The comments explicitly describe the graph as a projection that is rebuilt when it disagrees with this journal. [[journal]]

For each path, extraction computes a desired graph state from file bytes and the selected depth. The depth ladder ranges from path/file metadata through parsed symbols and graph edges; tree-sitter capability constrains how far extraction can go. Extraction computes a SHA-256 content hash and invokes the Python bridge for syntax-aware extraction. The README says this indexing path uses local parsing and embeddings rather than an LLM extraction call. [[extract]][[readme]]

The daemon is the single graph writer. Other processes append path hints; the reconciler reads current content from disk, computes its desired state, updates the backend projection, and commits journal ownership under a generation guard. The path queue is level-triggered and deduplicated: hints say a path may have changed, not what the change was. The README describes the default Graft sink and a selectable Mnemosyne backend; search merges backend results through the same ranked/verified output path. [[reconcile]][[journal]][[readme]][[search]]

## Write, update, delete, and retrieval

**Write and update.** Filesystem watchers, harness hooks, and CLI commands enqueue paths for reconciliation. The reconciler re-reads the current path and writes the corresponding nodes/edges to the sink before committing journal state. Repeating reconciliation for identical bytes and depth is designed to converge on the same state. The CLI also exposes `heimdall insert` for memory cards/facts. The README labels the extracted fact-card and runtime extractor layer experimental: extraction uses English patterns, contradiction resolution is absent, and fact output is described as leads to verify. [[reconcile]][[extract]][[readme]]

**Delete and move.** When a source path disappears, reconciliation retracts the nodes and edges owned by that path and records the path as absent. Reconciliation of a moved file can re-home matching graph content, while stale scans can rehome or delete dead anchors. Journal fact history is retained separately for invalidated fact-kind rows, capped at 50 rows per source path; ordinary code/symbol/file node retractions are not archived as belief changes. This is not a general user-facing delete API for arbitrary facts, and source inspection does not establish physical erasure from every backend, backup, or external store. [[reconcile]][[journal]][[readme]]

**Retrieval.** The default search script queries per-repository Graft code graphs and the global semantic index, merges and deduplicates results, optionally walks related graph edges, then applies a trust-verdict pass. It supports query count, path scope, knowledge kind, and optional recency behavior. A result can be STRONG, WEAK, REBUILT, STALE/REMOVED, or NOPATH depending on indexed evidence and path state. A semantic match alone does not establish liveness: the README says STRONG requires a matching file card and regular-file metadata, along with query coverage; the verdict pass reads metadata rather than opening the hit file. [[search]][[readme]]

## Scope isolation

Heimdall’s intended corpus spans multiple repositories under configured roots. Search’s `--scope` filters returned paths, while workspace/repository roots and per-repository graph selection define indexing boundaries. These are retrieval and filesystem boundaries, not demonstrated tenant authorization. No adversarial cross-user isolation probe or deployed access-control review was performed. [[search]][[readme]][[reconcile]]

## Provenance and evidence

For code-graph hits, the path and indexed content are linked to the source file. At query time, the verifier checks the anchor’s existence/type and card metadata, and uses indexed text to assess query coverage. The README documents the limits: metadata agreement is not cryptographic proof; timestamp resolution, privileged metadata changes, time-of-check/time-of-use races, and edits between reconciliation passes can weaken the guarantee. The system therefore offers a filesystem-grounded verdict, not proof that a returned passage answers a question. [[readme]][[search]]

Fact cards are a separate, experimental path. The README states that extraction is English-pattern based, facts may contradict one another without resolution, and secret filtering/source ownership are stronger than the interpretation layer. Treat those fact outputs as leads to verify, as the upstream documentation directs. [[readme]]

## Efficiency and observability

The inspected design stores its journal locally in SQLite, uses a local graph/semantic backend, and extracts code structure without sending files to a hosted LLM. The journal’s indexes, bounded queue, generation guard, and single-writer architecture support incremental convergence. The README describes CPU-based embeddings by default and optional GPU acceleration; these are upstream design statements, not measurements from this review. [[journal]][[reconcile]][[extract]][[readme]]

The repository documents `heimdall doctor`, health and freshness checks, a drift-only `verify` command, daemon health, telemetry snapshots, and search verdict explanations. No observability command or runtime was executed here. [[readme]][[search]]

## Metric-domain evidence

All project benchmark domains are **unmeasured for this review**. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the evaluation protocol and shared status, not Heimdall measurements. [[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Ranked code and semantic retrieval plus per-hit trust verdicts are implemented; answer quality and abstention were not scored. | Unmeasured |
| Correction and stale values | Reconciliation replaces path-owned projection state and detects drift; fact contradictions are not resolved by the experimental fact layer. No correction sequence was tested. | Unmeasured |
| Deletion leakage | Source-path deletion retracts that path’s graph objects; no deletion, recovery, or erasure probe was run. | Unmeasured |
| Scope isolation | Roots and returned-path scope filters are documented; no cross-scope authorization workload was run. | Unmeasured |
| Evidence support and citation coverage | Search outputs include paths and trust verdicts; no answer was adjudicated against supporting evidence. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings were collected. | Unmeasured |
| Tokens, cost, and storage efficiency | The source describes local parsing and embeddings, but no token, cost, or storage workload was measured. | Unmeasured |

## Limits and unknowns

This review inspected the official README and selected current journal, reconciliation, extraction, and search implementation at the verified repository head. Heimdall, its tests, and its benchmarks were not run. The code inspection cannot establish real-world retrieval quality, correction behavior in use, or whether a particular agent answer will be supported by a returned hit. [[readme]][[journal]][[reconcile]][[search]]

This review did not test authorization between users, filesystem permission configurations, alternate backend parity, backup/restore, or whether deletion removes data from all persistent layers. The README’s benchmark and hardware statements remain upstream-reported claims and were not reproduced. The experimental fact layer has documented interpretation limits. [[readme]][[search]][[journal]]

## Benchmark status

**Benchmark not run.** No Heimdall runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the project protocol and shared status, not Heimdall measurements. [[metrics]][[fixture]][[status]]

## Contact

The official pinned Code of Conduct publishes `arihantdeva@gmail.com` for reporting community conduct incidents. The structured record stores that address with the exact source URL. No commit/profile metadata, inferred address, or third-party directory was used for this contact check. [[conduct]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas URL records curated roster attribution only and is excluded from the assessment. See the structured record [heimdall.json](../data/system-reviews/heimdall.json) and [curated roster](../data/memory-systems.json).
