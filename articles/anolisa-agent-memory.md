# ANOLISA Agent Memory

## Identity and review pin

- **Curated ordinal:** 58 — **ANOLISA Agent Memory** (`anolisa-agent-memory`). The roster lists [`https://github.com/agentic-os-org/ANOLISA`](https://github.com/agentic-os-org/ANOLISA); its Atlas URL and revision are retained for attribution only.[[catalog](../data/memory-systems.json)] [[atlas](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/anolisa-agent-memory.md)]
- **Canonical upstream:** [agentic-os-org/ANOLISA](https://github.com/agentic-os-org/ANOLISA), default branch `main`. The repository root opened on `main`; the official [main commit feed](https://github.com/agentic-os-org/ANOLISA/commits/main.atom) identified current head **9878def83cd9e7ce988e0fa02feea175c92ebfe3**.[[repo](https://github.com/agentic-os-org/ANOLISA)] [[head-feed](https://github.com/agentic-os-org/ANOLISA/commits/main.atom)] [[head](https://github.com/agentic-os-org/ANOLISA/commit/9878def83cd9e7ce988e0fa02feea175c92ebfe3)]
- **Reviewed:** 2026-11-24T20:58:05Z (12:58:05 PST, America/Los_Angeles); **Reviewed from code** at the full SHA above.

## Summary

ANOLISA Agent Memory is a Linux-oriented, file-first memory component served to agents through MCP. Markdown files are the durable store; an optional SQLite search index supplies keyword and embedding retrieval, while tools support explicit observation, context assembly, snapshots, and user-controlled forgetting. This is a pinned source review, not a runtime or benchmark evaluation.[[readme](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/README.md)]

## Who and what

ANOLISA is a multi-component system software stack. Agent Memory is one component in its Agent Semantic Layer: a Rust MCP server and filesystem memory service rather than a hosted memory API. The reviewed project pages do not name an individual maintainer for this component.[[readme](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/README.md)] [[root README](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/README.md)]

## Architecture and data model

Markdown files under the memory mount are the primary memory objects. Ordinary file tools provide filesystem-style access, while observations are stored as `notes/observed/<ULID>.md` with frontmatter for type, optional hint, source, and creation time. The closed observation types are `user`, `feedback`, `project`, and `reference`; an omitted type defaults to `user`.[[observation](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_observe.rs)] [[readme](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/README.md)]

The top-level service owns the user namespace mount and audit logger, with optional session logging, indexing, embeddings, and Git history. With indexing enabled, an index worker maintains a SQLite database at `.anolisa/index/bm25.db`. The store uses SQLite FTS5 BM25 and can include dense embeddings; a search hit carries a path, snippet, score, and suspicious-content flag.[[index interface](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/index/mod.rs)] [[SQLite store](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/index/store.rs)]

The service treats index startup as optional: when opening the index fails, it logs a warning and continues without it. The component documentation describes namespace isolation, sandboxed filesystem paths, optional Git auto-commits, and tar.gz snapshots.[[service](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/service/mod.rs)] [[readme](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/README.md)]

## Write, update, delete, and retrieval

`mem_write(path, content)` creates parent directories and enforces a configured payload-size limit. With overwrite disabled it rejects existing files; overwrite mode atomically replaces an existing file. The writer validates mount-relative paths and checks for symlink traversal. `memory_observe` creates a new identified Markdown note instead; automatic `memory_capture` is consent-gated.[[writer](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/write.rs)] [[observation](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_observe.rs)]

`memory_search` supports BM25 by default, plus vector and hybrid reciprocal-rank fusion when embeddings are configured. It returns ranked paths and snippets. The user guide notes a short index debounce after writes, making `mem_grep` a filesystem-based fallback for an immediate lookup. Search refuses to return known-incomplete index results while retry is pending.[[search](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_search.rs)] [[guide](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/docs/user-guide/en/agent-memory/index.md)] [[index interface](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/index/mod.rs)]

BM25 scope can be configured as `shared`, `isolated`, or `filter`, with `MCP_CLIENT_NAME` used to derive the agent key. If isolated/filter mode lacks that environment variable, the implementation warns and falls back to unscoped shared search. Vector and hybrid routes do not return unscoped vector results: they degrade to scoped BM25 because the vector rows lack an agent-scope column. Category filtering is pushed into SQL before top-k for BM25, but is applied after top-k for vector/hybrid and can therefore leave fewer results.[[search](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_search.rs)] [[index interface](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/index/mod.rs)]

`memory_get_context(max_tokens)` is a separate heuristic: it walks eligible files, excludes the `.anolisa` and `.git` trees, sorts by modification time, and assembles previews capped at about four bytes per requested token and 256 preview bytes per file. It does not use the search index.[[context](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_get_context.rs)]

`memory_forget(topic, confirm)` searches at most 20 matching hits. Without confirmation it previews paths; with confirmation it deletes each matching file and reports successes or failures. The general `mem_remove` tool can delete a file or, with `recursive=true`, a directory; it rejects the mount root and metadata directory and uses sandboxed path handling. These are file deletion operations, not proof that Git history, snapshots, backups, or external copies have been erased.[[sovereignty](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_sovereignty.rs)] [[remove](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/remove.rs)]

## Metric-domain evidence

The following are **code observations** only. All domains remain unmeasured in this review.

| Domain | Source observation | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Search exposes BM25, vector/hybrid modes and snippets. | Unmeasured; no answerable or unsupported probes. |
| Correction and staleness | File overwrite/edit and consolidation tools can change stored material. | Unmeasured; no correction history or stale-value probes. |
| Deletion leakage | Forget/removal deletes matching files and logs operations. | Unmeasured; no post-delete probes or residual-copy audit. |
| Scope isolation | BM25 has scope filtering and a source-visible missing-client fallback. | Unmeasured; no cross-agent isolation probes. |
| Evidence support and citation coverage | Hits identify a memory path/snippet; observations can carry source/hint metadata. | Unmeasured; no claim adjudication or citation scoring. |
| Latency and write-to-recall delay | Search depends on index readiness; docs describe a debounce window. | Unmeasured; no timing collected. |
| Tokens and cost | Selected retrieval audit records estimate tokens as bytes divided by four. | Unmeasured; this is not provider token accounting or a cost measurement. |
| Storage | Markdown files and a derived SQLite index are visible persistence components. | Unmeasured; no attributable storage bytes collected. |

The project’s [metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution-status record](../results/initial-baselines-status.json) specify a proposed protocol and show `not_run`; their domains and planned cases are not ANOLISA results.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded inspection of selected documentation and Rust files at the reviewed SHA. It does not establish runtime correctness, retrieval quality, deployment safety, or behavior across all adapters and configuration combinations. Index freshness is eventually consistent after writes, and the unscoped fallback when isolated/filter mode lacks `MCP_CLIENT_NAME` is a configuration hazard.[[search](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_search.rs)] [[guide](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/docs/user-guide/en/agent-memory/index.md)]

The forget path considers at most 20 search hits. This review cannot establish that all semantically related material, Git history, snapshots, backups, or external copies are erased. No runtime deletion or isolation audit was run.[[sovereignty](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_sovereignty.rs)] [[readme](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/README.md)]

The reviewed source set did not trace every consolidation heuristic, namespace implementation, embedding backend, or adapter path. Their detailed guarantees and the effects of all configuration defaults remain unknown.

## Contact-list follow-up

I checked the official pinned root README, component README, and `SECURITY.md` for a published contact email. None publishes one; the security policy directs vulnerability reports through GitHub Security Advisories. The JSON record stores `contact.email: null` and the exact pinned security-policy URL, with all checked sources listed. No address was inferred.[[root README](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/README.md)] [[component README](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/README.md)] [[security](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No Agent Memory system execution, benchmark workload, build, or tests were run for this source review. Source structures and documentation statements are not measured results. See [metric definitions](../METRICS.md), the [versioned benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).

## Sources

- [Curated roster entry](../data/memory-systems.json) — ordinal, identity, listed repository locator, and Atlas attribution only.
- [Atlas attribution entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/anolisa-agent-memory.md) — locator/source attribution only.
- [Official repository](https://github.com/agentic-os-org/ANOLISA) and [main commit feed](https://github.com/agentic-os-org/ANOLISA/commits/main.atom); reviewed head [9878def83cd9e7ce988e0fa02feea175c92ebfe3](https://github.com/agentic-os-org/ANOLISA/commit/9878def83cd9e7ce988e0fa02feea175c92ebfe3).
- [Agent Memory component README](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/README.md)
- [Agent Memory user guide](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/docs/user-guide/en/agent-memory/index.md)
- [Search tool](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_search.rs)
- [Filesystem writer](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/write.rs)
- [Observation and capture](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_observe.rs)
- [Context retrieval](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_get_context.rs)
- [Forget tool](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/memory_sovereignty.rs)
- [Filesystem removal](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/tools/remove.rs)
- [Index interface](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/index/mod.rs) and [SQLite index store](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/index/store.rs)
- [Audit records](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/audit/mod.rs) and [service](https://github.com/agentic-os-org/ANOLISA/blob/9878def83cd9e7ce988e0fa02feea175c92ebfe3/src/agent-memory/src/service/mod.rs)
- [Project metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only source review; no system execution, benchmark, build, or tests.
