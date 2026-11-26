# Context Keeper — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 143 — Context Keeper / `context-keeper`  
**Listed repository:** [jarmstrong158/context-keeper](https://github.com/jarmstrong158/context-keeper)  
**Canonical upstream:** same repository; default branch `main`; reviewed head [d08355a46548d5a20d9170d3271e2054c51a4db9](https://github.com/jarmstrong158/context-keeper/commit/d08355a46548d5a20d9170d3271e2054c51a4db9)  
**Review time:** 2026-11-25 08:52:18 UTC (2026-11-25 00:52:18 PST; America/Los_Angeles)

## Identity and scope

The catalog places Context Keeper at ordinal 143, slug `context-keeper`, with an explicit listed repository locator. The pinned Atlas attribution is retained only for roster identity and locator context, not as assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/context-keeper.md)]

The official repository page identifies `main` as the default branch. Its Atom feed reports full head `d08355a46548d5a20d9170d3271e2054c51a4db9`, updated 2026-08-06T17:09:21Z; read-only `git ls-remote` and a shallow checkout independently resolved main to the same SHA. The reviewed source links below pin that commit.[[repository](https://github.com/jarmstrong158/context-keeper)] [[main commit feed](https://github.com/jarmstrong158/context-keeper/commits/main.atom)] [[reviewed head](https://github.com/jarmstrong158/context-keeper/commit/d08355a46548d5a20d9170d3271e2054c51a4db9)]

## Summary and architecture

Context Keeper is an offline-first MCP server for structured project memory. It stores typed decisions, pipelines, and constraints in human-editable project-local JSON files. Its MCP tool set supports recording, ranked context retrieval, exact structured queries, mutation/deprecation, quality checks, snapshot exchange, and optional mirroring.[[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)] [[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)]

Entries carry type-specific fields plus status, origin, scope, tags, timestamps, and relationships. The JSON files are canonical; project summaries, `DECISIONS.md`, and optional Claude Code rule files are derived output. The server uses Python's standard library for core operation and can optionally call an embedding service.[[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)] [[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)] [[store paths](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/store_paths.py)]

Writes go through temporary files and atomic replacement. A write refuses to replace an existing store file that cannot be parsed, avoiding accidental loss of its contents. Claude Code hooks can supply context at session start and inject matching constraints before edit/write operations.[[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)] [[scope hook](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/hooks/scope_guard.py)]

## Write, update, delete, and retrieval

**Write.** `record_entry` dispatches by kind and validates required fields for minimum content. Entries can record whether they came from a user, agent, or import. Capture also returns lexical similarity/contradiction signals and possible-supersession suggestions; the advisory does not block writing. Explicit supersession marks the earlier decision as superseded.[[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)] [[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)]

**Update and correction.** `update_entry` edits an existing record and revalidates its required fields; `deprecate_entry` stores a retirement reason and can merge a duplicate into a survivor without hard-deleting the duplicate. These mechanisms provide lifecycle metadata, but do not establish correction accuracy or rule out stale retrieval.[[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)] [[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)]

**Delete.** The inspected MCP tools include deprecation but no hard-delete operation. Deprecated entries remain in the JSON store while ordinary ranked retrieval excludes them; superseded entries remain as history. The README says users may directly edit or delete their JSON data. The optional mirror is newest-wins/upsert and explicitly does not propagate deletes, so deletion across snapshots, caches, and remote copies is not established here.[[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)] [[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)] [[mirror](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/mirror.py)]

**Retrieval.** `get_context` ranks by tags and lexical text overlap, scope, recency, status, and origin; it can include related entries and a compact predecessor explanation within a token budget. Below the configured relevance floor, the response carries `no_confident_match` guidance but still returns weak matches. `query_entries` instead applies deterministic AND-combined structured filters without ranking.[[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)] [[ranking](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/ranking.py)] [[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)]

Optional semantic retrieval blends embedding similarity into lexical ranking. It supports local Ollama and OpenAI-compatible APIs, caches vectors by entry text hash, batches cache misses, and falls back to lexical ranking when the embedding backend is unavailable.[[semantic index](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/semantic_index.py)]

## Scope isolation

Each entry has a scope. Shared path-component rules define how directory and file scopes cover paths and are reused by retrieval ranking, focus selection, hooks, and Claude Code rule projection. Domain labels such as `global`, `all`, and `*` are not path matches. The session summary and hooks deliver context within the configured project/client boundary; the repository alone does not establish isolation between users or projects sharing a host.[[scope rules](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/scope_rules.py)] [[scope hook](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/hooks/scope_guard.py)] [[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)]

## Provenance and evidence

Records can identify origin (`user`, `agent`, or `import`) and carry timestamps, rationale, tags, and explicit relationship/supersession links. This is authored-entry metadata rather than an immutable change log or enforced external-source citation; it does not guarantee that generated answers provide supporting evidence.[[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)] [[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)]

## Efficiency and observability

Local JSON storage avoids a required database service. Summaries and retrieval are budgeted; the optional semantic arm caches embeddings and sends missing entries in batches. A best-effort sidecar counts entries injected into session context and entries returned by targeted retrieval, and quality checks can flag frequently injected but never retrieved entries. The counter is an advisory proxy, not a direct usefulness measure. The README states that default operation has no telemetry, analytics, or tracking.[[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)] [[semantic index](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/semantic_index.py)] [[usage sidecar](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/usage.py)] [[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)]

## Metric-domain evidence

These are source observations and unmeasured domains for this task; no Context Keeper run was performed.[[metric definitions](../METRICS.md)]

- **Answerable recall and abstention — unmeasured here.** Upstream evaluation reports retrieval measurements and known misses, but this task ran no benchmark cases.[[upstream evaluations](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/evals/README.md)] [[benchmark status](../results/initial-baselines-status.json)]
- **Correction accuracy and stale retrieval — unmeasured.** Update and supersession exist in source, but no correction probes were run.[[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)]
- **Deletion leakage — unmeasured.** No hard-delete MCP path was found and no post-delete residual-data probes were performed.[[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)] [[mirror](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/mirror.py)]
- **Scope isolation — unmeasured.** Path and hook behavior are source-visible; no cross-project or cross-user workload was executed.[[scope rules](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/scope_rules.py)]
- **Evidence support and citation coverage — unmeasured.** Origin/rationale metadata exists, but no generated answers were audited for source support.[[server](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/server.py)]
- **Retrieval latency — unmeasured.** No latency distribution was collected.[[metric definitions](../METRICS.md)]
- **Write-to-recall delay — unmeasured.** No timed write-then-recall workload was run.[[metric definitions](../METRICS.md)]
- **Tokens and cost — unmeasured.** No provider token or cost accounting was performed.[[metric definitions](../METRICS.md)]
- **Storage efficiency — unmeasured.** No corpus storage measurement was collected.[[metric definitions](../METRICS.md)]

## Limits and unknowns

This review inspected the official README and selected current server, ranking, scope, semantic, store, hook, usage, mirror, and evaluation files. It does not establish behavior across every client, provider, configuration, operating system, or error path. The upstream evaluation reports that prior-state questions were missed in its frozen set and plausible in-domain negatives can evade abstention; those are upstream-reported results, not a fresh run here.[[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)] [[upstream evaluations](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/evals/README.md)]

No Context Keeper runtime, tests, or benchmarks were run. This assessment therefore makes no measured claims about recall, abstention, correction, deletion compliance, scope isolation, evidence support, latency, write-to-recall delay, cost, or storage efficiency.[[metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark status](../results/initial-baselines-status.json)]

## Contact

The official pinned README was checked for a published contact email and contains none. No email was inferred from profile or commit metadata or third-party directories.[[README](https://github.com/jarmstrong158/context-keeper/blob/d08355a46548d5a20d9170d3271e2054c51a4db9/README.md)]

## Benchmark status

**Benchmark not run.** No runtime, tests, or benchmark execution was performed for this source review. See the [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).
