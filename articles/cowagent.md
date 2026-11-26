# CowAgent

## Identity and review pin

- Catalog ordinal: 168
- System: CowAgent
- Slug: `cowagent`
- Listed repository: https://github.com/zhayujie/CowAgent
- Roster attribution: explicit repository locator; the pinned Atlas entry is retained for curated identity and locator context only ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cowagent.md)).
- Canonical upstream: https://github.com/zhayujie/CowAgent
- Default branch: `master`
- Reviewed full head: [7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd](https://github.com/zhayujie/CowAgent/commit/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd)
- Review timestamp: 2026-11-25T10:00:39Z (UTC; 2026-11-25 02:00:39 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

CowAgent is an open-source personal AI assistant and agent harness. Its long-term memory moves from conversation context to dated daily Markdown files and then to a distilled `MEMORY.md` plus a dream diary. Historical recall uses keyword and embedding search; `MEMORY.md` is injected into each conversation. ([README](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/README.md), [memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx), [Deep Dream guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/deep-dream.mdx))

## Who and what

The project presents CowAgent as a personal AI assistant and a broader agent harness with tools, skills, channels, multi-agent support, and a personal knowledge base. The memory review here concerns its long-term conversation memory and the associated searchable storage layer. ([README](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/README.md), [memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx))

The official repository identifies `master` as its default branch. The official `master` commit feed reports full head 7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd, updated at 2026-11-25T09:41:50Z; the reviewed source and documentation links below pin that SHA. ([repository](https://github.com/zhayujie/CowAgent), [master feed](https://github.com/zhayujie/CowAgent/commits/master.atom), [head commit](https://github.com/zhayujie/CowAgent/commit/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd))

## Architecture and data model

The documented durable flow is conversation context → dated daily memory files → `MEMORY.md`. Daily summaries and dream diaries are Markdown files under the configured workspace; `MEMORY.md` holds distilled long-term notes and is included in the system prompt. A SQLite-backed memory store chunks content for keyword and vector retrieval. ([memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx), [storage source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/storage.py))

The memory chunk model contains an ID, user ID, scope, source kind, path, start/end lines, text, optional embedding, content hash, and metadata. SQLite FTS5 supports keyword search while the vector backend stores embeddings; these are searchable representations associated with source text, alongside the workspace Markdown files. ([storage source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/storage.py), [vector backend](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/vector_backend.py))

The guides describe automatic summaries when context is trimmed, a scheduled daily summary at 23:55, emergency saving on API context overflow, and Deep Dream after the daily summary. Background work is asynchronous so memory summarization does not block normal replies. ([memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx), [Deep Dream guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/deep-dream.mdx), [short-term context guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/context.mdx))

The configured workspace defaults to `~/cow`. The README describes team agents as having their own memory and workspace. The inspected chunk records also carry user and scope labels; the reviewed material does not establish deployment-wide tenant authorization. ([README](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/README.md), [memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx), [storage source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/storage.py))

## Write, update, delete, and retrieval

**Write.** When conversation limits cause old turns to be trimmed, the system summarizes them into the current date's daily memory file and asynchronously injects a summary into retained context. Daily scheduled summarization and an emergency save on model context overflow are also documented. The agent can read and write workspace memory through its tools. ([memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx), [short-term context guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/context.mdx), [README](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/README.md))

**Update and consolidation.** Deep Dream reads the existing `MEMORY.md` and daily notes, then asks an LLM to merge, deduplicate, prune, and extract information. It overwrites `MEMORY.md`; the documented conflict rule gives newer information precedence. The resulting dream diary records consolidation observations in prose. The guides do not describe a per-fact revision ledger linking a replacement value to its prior version. ([Deep Dream guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/deep-dream.mdx))

**Delete.** The inspected memory documentation describes clearing short-term conversation context but does not define a long-term erasure operation or guarantee removal across daily files, `MEMORY.md`, dream diaries, derived indexes, and backups. The memory is workspace-file based, but deletion completeness was not tested. ([memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx), [short-term context guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/context.mdx))

**Retrieval.** CowAgent combines FTS5/BM25 keyword matching and embedding similarity, normalizes their ranks, and uses a documented default weighting of 0.3 keyword and 0.7 vector. Daily memory decays with a 30-day half-life; core memory does not. Optional local reranking is disabled by default. `MEMORY.md` is injected directly, while relevant daily history is retrieved on demand. ([memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx), [storage source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/storage.py), [vector backend](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/vector_backend.py))

## Scope isolation

The configured workspace contains the memory files, team agents are documented with separate workspaces, and stored chunks include user and scope metadata. The review did not trace every identity and search path or test cross-agent and hostile-caller isolation, so these design elements do not establish an isolation guarantee. ([README](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/README.md), [memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx), [storage source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/storage.py), [manager source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/manager.py))

## Provenance and evidence

Indexed chunks retain source kind, path and line range, content hash, user/scope, and optional metadata, giving the implementation a way to associate retrieved text with a stored location. The reviewed documentation does not specify claim-level citations, truth/confidence states, or a structured audit trail for fact corrections. Dream diaries are narrative records of consolidation rather than a typed mutation ledger. ([storage source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/storage.py), [Deep Dream guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/deep-dream.mdx))

## Efficiency and observability

Context trimming, asynchronous summarization, FTS5, vector search, daily decay, and optional reranking provide context and retrieval controls. The web console documents browsing memory files and dream diaries; short-term context commands provide context statistics and clearing/compaction. The README warns that Agent mode can consume substantially more tokens than regular chat. These are design and documentation observations; no latency, token, cost, or storage measurements were collected. ([memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx), [context guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/context.mdx), [README](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/README.md))

## Metric-domain evidence

All project benchmark domains remain **unmeasured**. The fixture and metric definitions were inspected only as project references; they were not executed. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | No answer outcomes were adjudicated. |
| Correction accuracy and stale-value rate | Unmeasured | Distillation has a documented conflict rule; no correction workload was run. |
| Deletion leakage | Unmeasured | Long-term deletion completeness and post-delete behavior were not tested. |
| Scope isolation | Unmeasured | Workspace and user/scope labels are documented or represented in source; no isolation probes were run. |
| Evidence support and citation coverage | Unmeasured | No generated claims and citations were adjudicated. |
| Retrieval latency | Unmeasured | No latency samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write/recall probes were run. |
| Tokens and cost | Unmeasured | No token or cost measurements were collected. |
| Storage efficiency | Unmeasured | No corpus size or storage boundary was measured. |

## Limits and unknowns

This was a selected review of the official README, long-term memory and Deep Dream guides, short-term context guide, and memory storage, manager, service, and vector backend sources at the verified head. It did not trace every tool integration, identity propagation path, workspace permission, migration, or all memory code. ([README](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/README.md), [memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx), [Deep Dream guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/deep-dream.mdx), [storage source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/storage.py), [manager source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/manager.py), [service source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/service.py), [vector backend](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/vector_backend.py))

The flow relies on LLM summarization and overwrite-based distillation. The source and documentation describe its intended conflict and deduplication behavior but provide no adjudicated accuracy, deletion-completeness, isolation, or performance results. Large-corpus behavior, concurrent mutations, index recovery, and backup retention remain unknown from this review. ([Deep Dream guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/deep-dream.mdx), [storage source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/storage.py), [metric definitions](../METRICS.md))

## Contact

The official pinned README publishes `sales@simple-future.tech` for enterprise inquiries. The exact checked source is [README.md](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/README.md). No commit/profile metadata or third-party directory was used.

## Benchmark status

**Benchmark not run.** No CowAgent runtime, tests, or benchmarks were run. Source observations remain separate from project benchmark outcomes. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cowagent.md)
- [Official repository](https://github.com/zhayujie/CowAgent)
- [Official master commit feed](https://github.com/zhayujie/CowAgent/commits/master.atom)
- [Reviewed head 7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd](https://github.com/zhayujie/CowAgent/commit/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd)
- [Pinned official README](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/README.md)
- [Pinned long-term memory guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/index.mdx)
- [Pinned Deep Dream guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/deep-dream.mdx)
- [Pinned short-term context guide](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/docs/memory/context.mdx)
- [Pinned memory storage source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/storage.py)
- [Pinned memory manager source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/manager.py)
- [Pinned memory service source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/service.py)
- [Pinned vector backend source](https://github.com/zhayujie/CowAgent/blob/7e7f68e8e3a6a53cf92852f12c2cc5499c7586cd/agent/memory/vector_backend.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark status record](../results/initial-baselines-status.json)
