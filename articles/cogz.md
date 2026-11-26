# CogZ — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 139 — CogZ / `cogz`  
**Listed repository:** [balaianu/CogZ](https://github.com/balaianu/CogZ)  
**Canonical upstream:** same repository; default branch `master`; reviewed head [83a5a19aad58063ade3b16fcfc2b19a01643791e](https://github.com/balaianu/CogZ/commit/83a5a19aad58063ade3b16fcfc2b19a01643791e)  
**Review time:** 2026-11-25 08:45:00 UTC (2026-11-25 00:45:00 PST; America/Los_Angeles)

## Identity and scope

The curated catalog places CogZ at ordinal 139 with slug `cogz`, an explicit repository locator, and a pinned Atlas attribution. Atlas is used only to record curated identity and locator attribution; it is not assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cogz.md)]

The official GitHub repository page identifies `master` as the default branch. GitHub's official `master` commit feed reports current full head `83a5a19aad58063ade3b16fcfc2b19a01643791e`, updated 2026-11-22T21:54:44Z. Documentation and implementation links below pin that SHA.[[repository](https://github.com/balaianu/CogZ)] [[master commit feed](https://github.com/balaianu/CogZ/commits/master.atom)] [[reviewed head](https://github.com/balaianu/CogZ/commit/83a5a19aad58063ade3b16fcfc2b19a01643791e)]

## Summary and architecture

CogZ is a local-first Rust system for repository-specific engineering memory and code-aware context. Its README describes a CLI/library, an MCP server, and agent lifecycle hooks. It stores observations, rules, and knowledge as Markdown under `.cogz/`; SQLite is a disposable index that can be rebuilt from those files and the repository source.[[README](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/README.md)] [[architecture](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/architecture.md)]

The architecture separates files and storage, code indexing, embeddings, hybrid search, context assembly, consolidation, MCP, and hooks. FTS5 and sqlite-vec share a per-repository SQLite database. Tree-sitter extracts code entities and structural edges. The entity model stores IDs, type, status, timestamps, references, and optional type-specific fields in constrained YAML frontmatter; code entity IDs derive deterministically from normalized paths and qualified names.[[architecture](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/architecture.md)] [[entity model](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/entity-model.md)]

## Write, update, delete, and retrieval

**Write.** The MCP `create_entity` handler dispatches observation, rule, or knowledge writes after validation. The write path scans for secrets, writes the canonical file first, syncs the file to SQLite, computes embeddings when available, checks duplicates and contradictions, and records an event. Manual Markdown edits are another supported source path when indexed.[[write handler](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/src/mcp/tools_write.rs)] [[write helpers](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/src/mcp/helpers.rs)] [[architecture](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/architecture.md)] [[consolidation](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/consolidation.md)]

**Update and correction.** Knowledge entries support in-place edits. The implementation locks the canonical file update, writes the revised Markdown, syncs only that file, rolls back on sync failure, then re-embeds and records an update event. Observations are append-only for content; substantive rule changes use a superseding rule. `verify` re-stamps code provenance but is an attestation, not a truth check.[[update implementation](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/src/mcp/update_knowledge.rs)] [[entity model](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/entity-model.md)]

**Delete and retention.** The inspected pruning path applies to rejected or superseded observations after the configured retention period. It empties the file body and title, removes the embedding and FTS entry, and preserves graph edges; old tombstones are removed when the configured tombstone cap is exceeded. Active or stale observations and rules/knowledge are not pruned through this path. These mechanics do not prove erasure from Git history, backups, or downstream copies.[[prune implementation](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/src/doctor/prune.rs)] [[entity model](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/entity-model.md)]

**Retrieval.** Search combines FTS5, separate code and knowledge vector spaces, graph-first retrieval, reciprocal-rank fusion, and graph expansion. Ranking can demote drifted entities and diversify results. Context assembly prioritizes sections, deduplicates and compresses them, fits a token budget, and returns pointers for dropped entities. Direct search has an answer-coverage silence gate; context-pack retrieval does not wholesale-silence the pack.[[search design](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/search.md)] [[architecture](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/architecture.md)]

## Scope isolation

Storage is per checkout, and CogZ's stateless MCP interface requires every call to specify its target repository. The inspected design does not describe user or tenant authorization inside a single repository database, so the host and caller remain responsible for repository access and selection.[[architecture](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/architecture.md)] [[README](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/README.md)] [[write handler](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/src/mcp/tools_write.rs)]

## Provenance and evidence

Frontmatter can record sources, references, supporting observations, derived-from links, and code hashes used for verification. Search can return graph paths and expose coverage signals; status/events and access tracking record operational activity. These features provide lineage and observability, but they do not guarantee claim-level citations or that a generated answer is supported by its retrieved material.[[entity model](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/entity-model.md)] [[search design](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/search.md)] [[architecture](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/architecture.md)]

## Efficiency and observability

The system uses local embedded storage, FTS-only fallback, optional/lazy model loading, and bounded context packs. Search documentation describes batched candidate processing and separate model spaces. The CLI includes status and doctor views; event, usage, and access tables support operational inspection. Performance figures in the upstream README are project-reported results, not observations from this review.[[architecture](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/architecture.md)] [[search design](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/search.md)] [[README](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/README.md)]

## Metric-domain evidence

All metric domains below remain unmeasured in this review. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [existing result status](../results/initial-baselines-status.json).

- **Answerable recall and abstention — unmeasured.** A coverage-based silence gate and diagnostic signals are documented; no adjudicated queries were run.[[search design](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/search.md)]
- **Correction and staleness — unmeasured.** Knowledge updates and drift demotion are source-visible; no correction probes were run.[[update implementation](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/src/mcp/update_knowledge.rs)] [[entity model](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/entity-model.md)]
- **Deletion leakage — unmeasured.** Tombstone pruning is implemented; no post-prune leakage checks were run.[[prune implementation](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/src/doctor/prune.rs)]
- **Scope isolation — unmeasured.** Per-repository storage and explicit repository arguments are documented; no isolation workload was run.[[architecture](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/architecture.md)]
- **Evidence support and citation coverage — unmeasured.** Provenance and graph paths exist; no generated answer was adjudicated.[[entity model](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/entity-model.md)] [[search design](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/search.md)]
- **Retrieval latency — unmeasured.** No latency distribution was collected.
- **Write-to-recall delay — unmeasured.** No timed write-then-recall workload was run.
- **Tokens and cost — unmeasured.** No token or provider-cost accounting was performed.
- **Storage efficiency — unmeasured.** No corpus storage measurement was collected.[[metric definitions](../METRICS.md)]

## Limitations and unknowns

The search documentation describes residual false opens and false silences for its answer-coverage gate, and notes that graph expansion can dilute precision. Optional embeddings improve semantic retrieval but require models; FTS-only mode remains lexical. The design and source inspection do not establish semantic answerability or correctness across all query types.[[search design](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/search.md)] [[degradation guide](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/degradation.md)]

This review covered selected current documentation, MCP write/update handlers, and observation pruning. It did not inspect every tool, hook, platform, model, or failure path. No CogZ runtime, tests, or benchmarks were run, so retrieval quality, correction accuracy, deletion leakage, isolation, latency, token/cost use, and storage efficiency remain unknown.[[architecture](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/docs/design/architecture.md)] [[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Contact

The official pinned README and SECURITY.md were checked for contact information. Neither publishes an email; SECURITY.md directs vulnerability reports through GitHub Security Advisories. No profile or commit metadata, or third-party directory, was used.[[README](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/README.md)] [[security policy](https://github.com/balaianu/CogZ/blob/83a5a19aad58063ade3b16fcfc2b19a01643791e/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No CogZ runtime, benchmark, or tests were run for this review. Source observations and upstream README results are not results from this task. See [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [result status](../results/initial-baselines-status.json).
