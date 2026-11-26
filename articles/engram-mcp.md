# Engram MCP (edg-l)

## Identity and review pin

- **Catalog position:** 226, “Engram MCP (edg-l)”; slug `engram-mcp`.
- **Listed repository:** [edg-l/engram-mcp](https://github.com/edg-l/engram-mcp); roster status is explicit. The pinned Atlas attribution is used only for roster identity and locator context.
- **Canonical upstream:** [edg-l/engram-mcp](https://github.com/edg-l/engram-mcp), default branch `master`. The official repository page shows `master`; `git ls-remote --symref` reported `HEAD -> refs/heads/master` at full SHA `0303bc4e052f64755d99b2247bc6d2acc38d7a1f`, matching the shallow checkout. GitHub’s REST API was rate-limited during review.
- **Reviewed:** 2026-11-25 19:27:05 UTC (2026-11-25 11:27:05 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) supplies ordinal, name, slug, listed repository, and roster attribution. The pinned [Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/engram-mcp.md) supports that attribution only; it is not assessment evidence.

## Summary

Engram MCP is a local Rust MCP server and CLI for coding-agent memory. It stores typed memories, branch-linked handoffs, todos, and ADRs in SQLite, using a local ONNX embedding model and FTS5 for hybrid retrieval. Project and branch filters organize recall; global memories intentionally cross project boundaries. No runtime, tests, or benchmarks were run for this source review.

## Who and what

The official [README](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/README.md) describes Engram as a local MCP server for persistent coding-agent memory, with an `engram-cli` for interactive commands and scripts. It says the system is single-user, local, and unauthenticated. I do not infer a maintainer identity from account or commit metadata.

## Architecture and data model

The default store is one SQLite database at `~/.local/share/engram/memories.db`, configurable with `ENGRAM_DB`. Memory rows include type, content/summary, tags, importance and relevance, access counts and timestamps, project and branch, pinned/global flags, merged-source data, and external artifact references. Relationships can represent `supersedes`, `derived_from`, and `relates_to`. Handoffs store structured sections with per-section embeddings; todos and ADRs carry their own lifecycle state.[[README](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/README.md)] [[types](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/src/memory.rs)] [[tools](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/tools.md)]

Specific memory lookup and broad context retrieval combine FTS5 BM25 with cosine similarity over local ONNX embeddings using reciprocal-rank fusion. `memory_context` can select clusters before scoring bounded candidates; `handoff_resume` ranks individual sections through a recent branch handoff chain. The documentation describes one shared embedding process per user to reduce repeated model loads; no resource use was measured here.[[retrieval](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/how-it-works.md)] [[embedding search](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/src/db/embeddings.rs)]

## Write, update, delete, and retrieval

**Write and update.** `memory_store` embeds the proposed content locally, stores it, and can create links to related or superseded memories. Similar same-type memories at cosine ≥0.88 are returned as possible supersession candidates; Engram leaves the decision to the caller and does not merge at store time. Updates can change content, tags, importance, pin/global/dead state, or patch handoff sections. Replacing content snapshots the previous version to trash.[[store and update](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/src/tools/handler.rs)] [[MCP tools](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/tools.md)] [[deduplication](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/how-it-works.md)]

**Delete and correction.** A replacement can supersede an old memory so matching retrieval redirects to the successor with a `matched_via` annotation. A memory marked dead is dropped from ordinary retrieval. Delete, prune, explicit dedup merge, and overwrite snapshot data to a local trash with embeddings and links; the default recovery window is 30 days. Restore is available while the snapshot remains. The project documents that trash/deletions do not sync between machines; secure erasure was not established by source inspection.[[curation](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/src/tools/curation.rs)] [[trash](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/src/db/trash.rs)] [[sync and retention](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/how-it-works.md)]

**Retrieval.** `memory_query` supports specific lookups and filters; `memory_context` gathers context for a task. Both use hybrid keyword/vector ranking by default, with other modes configurable. Project documentation describes a 30-question LongMemEval-S slice measured at crate version 0.4.0; this is a project-reported, version-specific result and was not independently reproduced or treated as current benchmark evidence here. Handoffs contain summary, decisions, blockers, tried approaches, mental model, next steps, and notes; resume ranks sections across up to five handoffs and also returns open todos and current blockers.[[tools](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/tools.md)] [[retrieval and reported benchmark](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/how-it-works.md)] [[data types](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/src/memory.rs)]

## Scope isolation

Project identity derives from a normalized Git remote, or a home-relative path when no remote exists; worktrees resolve to their main checkout. MCP tools default to the server’s project but allow an explicit project argument. Branch filters cover current/global, all branches, or a named branch. A `global` memory is deliberately visible across projects. These are application-level routing and recall controls; the README characterizes the product as a single-user local server with no authentication, so they do not establish multi-user authorization.[[project identity](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/src/project.rs)] [[scope reference](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/tools.md)] [[README](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/README.md)]

## Provenance and evidence

The data model can retain external artifact paths, URLs or IDs, relationship edges, `merged_from` source IDs/previews, and timestamps/access counts. The Claude Code hooks can capture session summaries, prompts, and subagent results, with common-secret redaction. These provide pointers and operational context, not truth verification or guaranteed source citations. The inspected source did not establish a general mutation audit history or citation enforcement for generated answers.[[memory types](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/src/memory.rs)] [[tools](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/tools.md)] [[setup and hooks](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/setup.md)]

## Efficiency and observability

Code and documentation describe FTS indexing, bounded candidate scoring, cluster-based diversity, local embeddings, and a shared embedding process. Access counts and last-access timestamps feed ranking/decay, while MCP, CLI, and optional Claude Code hooks provide integration. No latency, token, cost, storage-efficiency, or operational telemetry was collected in this review.[[retrieval](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/how-it-works.md)] [[embedding index](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/src/db/embeddings.rs)] [[setup](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/docs/setup.md)]

## Metric-domain evidence

- **Answerable retrieval and abstention:** retrieval and score outputs were inspected; no answerability or abstention workload was run.
- **Correction and stale values:** update, supersession, dead status, and store-day decay were inspected; no correction accuracy or stale-value probes were run.
- **Deletion leakage:** deletion-to-trash and restore paths were inspected; no residual-read or secure-erasure probe was run.
- **Scope isolation:** project, branch, and global visibility rules were inspected; no isolation workload was run.
- **Evidence support and citations:** artifact pointers and relation provenance were inspected; support precision and citation coverage were not measured.
- **Retrieval latency and write-to-recall delay:** not measured.
- **Tokens, cost, and storage efficiency:** not measured.

See the project’s [metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and [planned benchmark fixture](../fixtures/memory-benchmark-v1.json). These comparison documents are not Engram results.

## Contact

No contact email was found in the official pinned [README](https://github.com/edg-l/engram-mcp/blob/0303bc4e052f64755d99b2247bc6d2acc38d7a1f/README.md). The exact checked URL is recorded in [engram-mcp.json](../data/system-reviews/engram-mcp.json); no commit/profile metadata or third-party directory was used.

## Limits and unknowns

This review covers source at the verified current `master` head. Engram, its tests, and benchmarks were not run. The upstream docs describe a small, versioned LongMemEval experiment, but this review did not reproduce it and its results do not establish present-day general retrieval quality. The source review cannot establish answer correctness, abstention behavior, secure erasure, user isolation, adversarial-input safety, or real-world latency, cost, and scaling. GitHub’s REST API was rate-limited; the official repository page, Git smart transport, and shallow checkout provided the branch and head evidence.

## Benchmark status

**Benchmark not run.** No Engram runtime, tests, or benchmarks were run. See the project’s [metrics](../METRICS.md), [shared status](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and SHA-pinned upstream links are recorded in [engram-mcp.json](../data/system-reviews/engram-mcp.json). The [curated roster](../data/memory-systems.json) and pinned [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/engram-mcp.md) support identity and locator context only.
