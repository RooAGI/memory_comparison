# Engram source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 222 / engram (NickCirv) / `engram-nickcirv`  
**Listed repository locator:** [NickCirv/engram](https://github.com/NickCirv/engram)  
**Canonical upstream:** [NickCirv/engram](https://github.com/NickCirv/engram)  
**Default branch / reviewed head:** main / [df445d3132583100e6d5106af4b4c91c01a2ba15](https://github.com/NickCirv/engram/commit/df445d3132583100e6d5106af4b4c91c01a2ba15)  
**Review time:** 2026-11-25 19:20:58 UTC (2026-11-25 11:20:58 PST; America/Los_Angeles).

## Identity and review pin

The curated roster lists engram (NickCirv), slug `engram-nickcirv`, at ordinal 222 with an explicit repository locator and a pinned Agent Memory Atlas roster source. The roster and Atlas attribution are recorded for identity and locator context only; Atlas descriptions and capability marks are not assessment evidence. GitHub's official repository page identifies `main` as the default branch. Its latest commit page and patch identify the full current head as `df445d3132583100e6d5106af4b4c91c01a2ba15`; the patch header dates that commit 2026-09-22. The source review is pinned to this head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Engram is a local code graph and context tool for coding agents. It indexes source entities and relationships, selected Git and session information, and optional skills into project-local SQLite, then exposes graph retrieval through a CLI, hooks, MCP, and a local authenticated HTTP interface. Repository documentation describes token estimates and benchmark tooling, but those are not measurements collected in this review.[[readme]][[core]][[store]]

## Who and what

The official repository presents Engram as a TypeScript/Node project and source-backed CLI/library, with agent integrations. Its owner/maintainer name is not needed to assess behavior and is not inferred from account or commit metadata. The project docs identify the public API, CLI, graph store, query engine, providers, hook interception, HTTP, and MCP entry points.[[readme]][[guide]][[core]]

## Architecture and data model

The core initializer derives a graph path under each project root at `.engram/graph.db`, acquires an exclusive `.engram/init.lock`, then mines source structure and Git history, reverts, bug-fix commits, and session history. Skill mining is optional. Incremental initialization uses saved file mtimes to skip unchanged files. The graph store uses sql.js to load a SQLite file into memory and exports the database to disk on save/close.[[core]][[store]]

The SQLite schema includes `nodes`, `edges`, `stats`, and `provider_cache`. Nodes store an identifier, label, kind, source file and location, confidence label and score, last-verified and query counters, JSON metadata, and optional mistake lifecycle fields such as validity, invalidating commit, then-believed, found-false-at, truth-now, and applies-to. Edges record source and target node IDs, relation, confidence, source location, verification time, and metadata. This is a structural and selected project-memory graph; it is not a store of complete source documents or a general-purpose personal memory timeline.[[store]][[schema]]

## Write, update, delete, and retrieval

**Write and update.** Indexing mines graph entities and relationships. The store writes nodes and edges with `INSERT OR REPLACE` keyed by node ID and by the source/target/relation tuple, so reindexing can replace extracted records. The core API also exposes `learn` and mistake/session mining for project memory. The reviewed public command surface documents init, reindex, watch, learn, and mistakes. The repository describes a write lock for indexing; write correctness under other concurrent paths was not exercised here.[[core]][[store]][[guide]][[readme]]

**Delete.** The reviewed README and command reference do not document a general per-memory delete command. The store exposes low-level SQL access, but that alone does not establish a supported user-facing deletion workflow. Reinitialization, cache clearing, database commands, or manual file removal have broader effects and should not be treated as equivalent to a targeted, auditable memory deletion. Deletion guarantees and post-delete retrieval behavior were not tested in this review.[[readme]][[guide]][[store]]

**Retrieval.** Query terms are matched against graph nodes, with SQL-backed search returning bounded seed sets and immediate neighbors. The query engine scores label and source-file matches, boosts mistake nodes, downweights hidden skill-keyword nodes, starts traversal from the top three seeds, then traverses graph relations and renders a bounded context. Default traversal is breadth-first with depth 3 and a 2,000-token budget; the token count is estimated from rendered characters at four characters per token. Empty matches return a no-matching-nodes message. Results are navigation aids and do not establish that a source was read or that a generated answer is correct.[[query]][[guide]][[readme]]

## Scope isolation

The graph path is derived from a supplied project root, so different project roots normally use separate `.engram/graph.db` files. Source rows do not show a tenant or user authorization key; project-root separation is an operational boundary, not a demonstrated security boundary. The HTTP interface is documented as loopback-bound and authenticated for protected graph/data routes. No cross-project or hostile-local-user isolation probes were run.[[core]][[store]][[guide]][[readme]]

## Provenance and evidence

Graph nodes and edges retain source-file paths, optional source locations, confidence labels and scores, timestamps, IDs, and metadata. Git miners can add repository history and revert-derived facts, and mistake records can retain temporal fields such as the invalidating commit and then-believed/truth-now text. These fields provide structural provenance cues, but they do not amount to claim-level citations to exact source passages or independent proof that a node is true. Retrieval and evidence support were not evaluated against answer outputs.[[store]][[schema]][[core]][[readme]]

## Efficiency and observability

The implementation uses SQLite indexes for node kind/source file and edge source/target/relation/source file, plus provider-cache lookup and staleness. Query search caps results per term, uses a small seed set and bounded traversal/rendering, and tracks query counts. The CLI and dashboard expose graph statistics; benchmark and measure commands exist, but the README cautions that estimated structural context size is not task correctness or invoice savings. No latency, write-to-recall, token, cost, storage, throughput, or quality results were collected for this review.[[store]][[query]][[guide]][[readme]][[metrics]]

## Metric-domain evidence

All project evaluation domains are **unmeasured** for Engram in this review. Code structure and repository descriptions do not establish runtime performance. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the evaluation protocol and project status, not Engram results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Graph matching and bounded traversal are implemented; no answer set was scored. | Unmeasured |
| Correction accuracy and stale values | Replacement upserts and mistake lifecycle fields exist; no correction probes were run. | Unmeasured |
| Deletion leakage | No supported general delete workflow was verified; no deletion or post-delete probes were run. | Unmeasured |
| Scope isolation | Per-project graph paths are implemented; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Source file/location and confidence metadata are stored; no generated claims were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timing samples were collected. | Unmeasured |
| Tokens, cost, and storage | The query budget uses an estimate; no corpus or provider resource measurements were collected. | Unmeasured |

## Limits and unknowns

This is a source-based review pinned to the current verified repository head. The README and source describe substantial code and integration surfaces, but this review did not install, build, or run Engram. A code graph can omit unsupported syntax, stale files, or relevant relationships; term and traversal ranking can select incomplete context. The repository itself instructs users to inspect original source before relying on graph output.[[readme]][[core]][[query]]

The graph uses project-local SQLite, but optional providers and integrations may execute external processes or access networks; local storage does not make every configured workflow network-free. Confidence scores and source paths are not runtime-validated truth or claim citations. Deletion semantics, cross-project security, retrieval correctness, and actual resource use remain unverified here.[[readme]][[store]][[guide]]

## Benchmark status

**Benchmark not run.** No Engram runtime, tests, or benchmark workload was executed. No quality, latency, token, cost, storage, deletion, correction, or isolation measurement is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json); these describe the protocol and status, not Engram results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email. None was found; the structured record stores `contact_email: null` and the exact checked URL. No commit/profile metadata, third-party directory, or inferred address was used.[[readme]]

## Sources

Upstream source citations are pinned to the verified full SHA except the official repository/API and current-head identity records. The Atlas link is retained only for roster attribution, not system assessment. See the structured record [engram-nickcirv.json](../data/system-reviews/engram-nickcirv.json) and [curated roster](../data/memory-systems.json).
