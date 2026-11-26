# Gortex source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 268 / Gortex / `gortex`  
**Listed repository locator:** [zzet/gortex](https://github.com/zzet/gortex)  
**Canonical upstream:** [zzet/gortex](https://github.com/zzet/gortex)  
**Default branch / reviewed head:** main / [b6327e53624b3cce99412fa56a5a14cf74de634b](https://github.com/zzet/gortex/commit/b6327e53624b3cce99412fa56a5a14cf74de634b)  
**Review time:** 2026-11-25 21:28:44 UTC (2026-11-25 13:28:44 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists Gortex at ordinal 268, slug `gortex`, with the explicit locator `https://github.com/zzet/gortex`. The pinned Agent Memory Atlas entry is recorded solely as roster attribution and locator context. The official repository page identifies `main` as its default branch, and the official `main.atom` feed reports full head `b6327e53624b3cce99412fa56a5a14cf74de634b` (updated 2026-11-24T17:37:13Z). This review is pinned to that head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Gortex is a local code-intelligence and agent-context system. It parses tracked source repositories into a persistent SQLite knowledge graph, then exposes graph navigation, code search, impact analysis, and related context through CLI, MCP, HTTP, and a daemon. The README also describes project documents, decisions, and captured agent sessions as memory attached to code. The inspection centers on the graph and its source-grounded retrieval; it does not establish the lifecycle or quality of every memory feature.[[readme]][[architecture-doc]]

Gortex is therefore most directly evidenced here as repository and coding-session memory. The reviewed sources do not establish it as a general-purpose personal fact store with measured answer accuracy, correction quality, or deletion guarantees.[[readme]][[architecture-doc]]

## Who and what

The official README identifies Gortex as a code-intelligence engine for coding agents and IDEs, distributed as a local binary with CLI, MCP, HTTP, and web interfaces. It names Andrey Kumanyaev in its copyright notice and publishes `me@zzet.org` in that same official README; this identity and contact are taken from project documentation, not commit or profile metadata.[[readme]]

## Architecture and data model

The architecture documentation describes one binary with a CLI-driven multi-repository indexer, a shared SQLite graph, an MCP query engine, an HTTP API, and a long-lived daemon. Tree-sitter language extractors create code nodes and relations; resolvers add cross-file and cross-repository links. The daemon watches tracked repositories and patches changed files, while persisted graph state is reused and reconciled after restart.[[architecture-doc]]

The graph represents files, packages, functions, methods, types, interfaces, imports, contracts, and other code structures as nodes. Edges represent relations such as calls, imports, definitions, implementations, references, data flow, configuration reads/writes, and matched provider/consumer contracts. Repository-qualified identifiers and workspace metadata let a single graph cover multiple repositories.[[architecture-doc]][[edge]]

Edges also carry an `Origin` provenance tier describing how a relationship was resolved. The source defines tiers including LSP-resolved, LSP-dispatch, AST-resolved, AST-inferred, text-matched, and speculative; confidence scores and provenance tiers are related but distinct signals. The README and search guide describe provenance-aware ranking and evidence-oriented graph results.[[edge]][[semantic-search]][[readme]]

The graph is durable on disk. Cold indexing stages parsed output in memory for a repository pass before writing it to SQLite; warm starts reconcile only changed repositories/files when possible, and indexing mutations are persisted as they occur. The architecture guide documents route and timing summaries in daemon logs. These are design and observability descriptions, not measurements collected for this review.[[architecture-doc]]

## Write, update, delete, and retrieval

**Write and update.** Adding a repository with `gortex track` initiates indexing. The indexer parses source files into nodes and edges, resolves relationships, and writes graph state to the shared store. A filesystem watcher reindexes changed files through bounded per-file patches and reruns relevant resolution. A periodic reconciliation is documented as a fallback for missed filesystem events, network filesystems, or daemon downtime. These operations maintain an index of repository contents; they are not equivalent to a user explicitly asserting a fact into a conversational memory.[[readme]][[architecture-doc]][[multi-repo]]

**Deletion and forgetting.** The architecture describes changed and deleted files being reconciled from disk, and the multi-repository guide documents explicit untracking that evicts a repository's nodes and edges. This is index maintenance/removal behavior. The reviewed sources do not establish a tombstone history for removed code, cryptographic erasure, backup removal, or a deletion-leak guarantee for separately captured session and document memories.[[architecture-doc]][[multi-repo]]

**Retrieval.** Query tools traverse graph relations for symbol lookup, callers, call chains, impact, contracts, and other code questions. The semantic-search guide describes a default-on lexical FTS5/BM25 plus vector channel, adaptive rank fusion, optional embedding providers, and additional graph-based reranking. The README describes outputs with exact source file and line references and a caller-controlled token budget. This review did not test recall, abstention, or whether citations support generated answers.[[readme]][[semantic-search]][[edge]]

## Scope isolation

Each graph node is associated with a repository prefix; workspace and optional project slugs group repositories for cross-repository graph operations. The multi-repository guide says graph queries are clamped to the active session's workspace and that repository/project/workspace/scope parameters narrow within that boundary. It also documents exceptions and per-tool narrowing behavior, including some analysis kinds that remain workspace-wide.[[architecture-doc]][[multi-repo]]

That graph boundary does not itself constrain filesystem tools: the official guide says path-argument tools can access the union of tracked repository roots, rather than only the session workspace. Scope isolation is therefore surface-specific. The review did not run cross-repository or cross-workspace isolation probes, and cannot establish deployment authorization beyond the documented rules.[[multi-repo]]

## Provenance and evidence

The graph records extracted relationships with their resolution origin, and the edge source includes confidence-label handling. The README describes graph-grounded responses that identify source files and lines. Those mechanisms help callers inspect why a code relationship was returned; they do not by themselves prove the code is current in every deployment or guarantee that a natural-language answer is supported by the cited excerpts. No factual-answer evidence adjudication was performed.[[edge]][[readme]]

## Efficiency and observability

The search guide describes a small baked static embedding table, store-native lexical search, adaptive fusion, chunked embedding for long symbols, and persisted vector indexes. Local and remote embedding providers are configurable, with bounded concurrency for API embedding. The architecture guide documents incremental indexing, warm restart routes, and parse/resolve/enrichment timing summaries. The README says telemetry is off by default and limited to anonymous command/tool counts when explicitly configured. These are inspected implementation and documentation claims, not measured results from this task.[[semantic-search]][[architecture-doc]][[readme]]

Upstream documentation publishes scale and token-savings figures. They are not reproduced here and are not entered as project benchmark results. Latency, token usage, cost, storage efficiency, and write-to-recall delay for this reviewed revision remain unmeasured by this task.[[readme]][[metrics]][[fixture]][[status]]

## Metric-domain evidence

The rows below distinguish source-level mechanisms from benchmark results. All project metric domains are unmeasured here.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Graph traversal and lexical/vector search are implemented; answer correctness and abstention were not evaluated. | Unmeasured |
| Correction and staleness | File changes trigger reindex and relation reconciliation; no correction sequence or stale-answer rate was measured. | Unmeasured |
| Deletion leakage | Deleted files and explicitly untracked repositories are reconciled/evicted; no post-delete leak probe or backup review was performed. | Unmeasured |
| Scope isolation | Workspace and repo/project filters are documented, with tool-specific caveats; no isolation workload was run. | Unmeasured |
| Evidence support and citations | Provenance tiers and file/line source references are documented; no answer evidence was adjudicated. | Unmeasured |
| Latency and write-to-recall delay | Index/reconcile timing is logged and documented; no task latency or write-to-recall timings were collected. | Unmeasured |
| Tokens, cost, and storage | Token-budgeted context, embedding choices, and durable SQLite storage are described; no token, cost, or storage comparison was made. | Unmeasured |

## Limits and unknowns

This is a bounded review of the official README, architecture, search, and multi-repository documentation plus the graph edge source at the verified head. Gortex, its tests, and benchmark workloads were not run. Claims about language coverage, retrieval quality, scale, and token savings are upstream statements and were not independently checked as runtime results.[[readme]][[architecture-doc]][[semantic-search]][[multi-repo]][[edge]]

The inspected material does not establish answer quality, reliable abstention, cross-surface scope isolation, deletion propagation through backups, or the lifecycle and evidence model for every document and agent-session memory feature. Filesystem and Git-hook freshness also depend on deployment configuration and environment; no outage or reconciliation scenario was exercised.[[readme]][[multi-repo]][[architecture-doc]]

## Benchmark status

**Benchmark not run.** No Gortex runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the project evaluation protocol, not Gortex measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README publishes `me@zzet.org`. The structured record stores this address and the exact pinned README URL as its source. No commit/profile metadata or third-party directory was used.[[readme]]

## Sources

Upstream file citations are pinned to the verified full SHA. The Atlas entry records curated identity and locator attribution only; it is not assessment evidence. See the structured record [gortex.json](../data/system-reviews/gortex.json) and [curated roster](../data/memory-systems.json).
