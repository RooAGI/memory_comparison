# dsh-auto-memory

## Identity and review pin

- Catalog position: 197
- System name: `dsh-auto-memory`
- Slug: `dsh-auto-memory`
- Listed repository: https://github.com/AskTheWay/dsh-auto-memory
- Roster attribution: explicit repository locator; the pinned Atlas entry is retained for curated identity and locator attribution only, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-auto-memory.md)).
- Canonical upstream: https://github.com/AskTheWay/dsh-auto-memory
- Default branch: `main`
- Current full head: [ac3cfd4ba161adf9b48f01238e58d677a55cb09b](https://github.com/AskTheWay/dsh-auto-memory/commit/ac3cfd4ba161adf9b48f01238e58d677a55cb09b)
- Reviewed at: 2026-11-25T11:26:37Z (UTC; 2026-11-25 03:26:37 PST, America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

The official public repository page identifies `main` as the default branch. GitHub's official main commits feed reports full head `ac3cfd4ba161adf9b48f01238e58d677a55cb09b`, updated at 2026-11-23T14:24:50Z; the commit page identifies the same revision on `main`. ([repository](https://github.com/AskTheWay/dsh-auto-memory), [main history](https://github.com/AskTheWay/dsh-auto-memory/commits/main.atom), [commit](https://github.com/AskTheWay/dsh-auto-memory/commit/ac3cfd4ba161adf9b48f01238e58d677a55cb09b))

## Summary

dsh-auto-memory is a DeepSeek Harness plugin that stores typed, scoped memories as Markdown files and injects a bounded index into the agent prompt. It adds user-controlled trust states, transcript evidence for automatic consolidation, lexical search, memory lifecycle tools, and an append-only injection audit. This is a source review; the system, tests, and benchmark workloads were not run. ([README](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/README.md), [store](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/store.ts), [prompt](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/prompt.ts))

## Who and what

The repository describes a plugin for DeepSeek Harness, installable through its plugin manager or CLI. GitHub identifies the repository owner as AskTheWay; the inspected README does not provide a more specific maintainer identity or a contact email. It is a local plugin, not a hosted memory service. ([repository](https://github.com/AskTheWay/dsh-auto-memory), [README](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/README.md))

## Architecture and data model

Each memory is a Markdown file with YAML frontmatter and a body. The record includes a kebab-case file key, description, one of four types (`user`, `feedback`, `project`, `reference`), scope, and optional importance, pin/disabled flags, read counters, expiry, retrieval keywords, lifecycle links, trust status, evidence, and import origin. The generated `MEMORY.md` in each scope is an index, not the source of truth. ([types](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/types.ts), [store](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/store.ts))

The plugin keeps a shared `_user` directory and a project directory derived from the owning session's working directory. It registers memory tools, one dynamic system-prompt section, lifecycle hooks for optional consolidation, and a web panel. Scope is selected from the session's trusted cwd and configuration; a project operation without an owning session cwd is rejected. User scope can be disabled across tool and injection paths. ([types](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/types.ts), [tools](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/tools.ts), [README](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/README.md))

## Write, update, delete, and retrieval

**Writes and updates.** `memory_write` accepts name, description, type, body, optional scope, pin/mute state, expiry and keywords. Without an explicit scope it updates a same-named record in an available layer, otherwise creates in project scope. Store writes normalize names, sanitize content, redact detected secrets, acquire a cross-process lock, atomically write the Markdown file, and rebuild the derived index. Rewriting a record changes content in place; unchanged content can retain trust state, while changed content is downgraded and its old evidence is cleared. ([tools](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/tools.ts), [store](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/store.ts))

**Automatic consolidation.** It is off by default. When enabled, session text is buffered with size limits; at root-agent disposal a model proposes a bounded set of candidate records. The output is validated and sanitized before it enters the same store path. Candidates may include a session ID and a purported verbatim quote; the quote is checked against captured transcript text, and user action in the panel is required to grant `verified`. A session buffer not yet consolidated can be lost if the process crashes. ([README](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/README.md), [consolidation](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/consolidate.ts), [types](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/types.ts))

**Deletion and lifecycle.** A direct delete removes a selected file; soft-disable, expiry, and stale zero-read eviction hide records from automatic injection while retaining them on disk. Bulk prune and delete-all have an approval hook; delete-all also requires explicit confirmation. Superseding records retain a successor link. The inspected code does not establish secure erasure from filesystem backups or other copies, and deleted facts can be reintroduced by later conversation/consolidation. ([tools](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/tools.ts), [store](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/store.ts), [types](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/types.ts))

**Retrieval.** The prompt path injects the user and current-project indexes, not every full memory body. The index is wrapped as stored data rather than instructions, neutralizes template braces, and is bounded by a configurable byte budget (16 KiB default at the reviewed head, including guidance and wrapper). The first user message freezes the selection for the session; writes are immediately available to tools but enter prompt injection in the next session. If both scopes exceed budget, project memories receive a guaranteed share before remaining capacity is allocated. Pinned entries rank first; other ranking uses importance, recency, reads, aging, and query coverage when truncation applies. ([prompt](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/prompt.ts), [audit](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/audit.ts), [README](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/README.md))

Explicit `memory_search` uses lexical coverage over names, titles, descriptions, bodies and keywords, returns up to eight matches with excerpts, and does not use embeddings. Explicit reads and search results carry status, disabled, expired, and superseded context. `disputed` and `superseded` records are not automatically injected; candidates are still eligible for injection, with their unverified state shown. ([recall](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/recall.ts), [tools](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/tools.ts), [types](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/types.ts))

## Provenance and evidence

The four-state trust model is `candidate`, `verified`, `disputed`, and `superseded`; absence of a status is treated as legacy/trusted state. Verification is reserved for the user through the panel. Consolidation evidence stores a source session ID and quote, but the quote originates from model output and is only accepted when it matches the captured text. Content changes invalidate prior evidence. This supports review and lifecycle cues, but does not prove factual truth or attach independent source citations to every claim. Store-level injection-pattern checks can mark suspicious content disputed, and every injected record is wrapped as untrusted data. ([types](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/types.ts), [consolidation](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/consolidate.ts), [prompt](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/prompt.ts))

## Efficiency and observability

The source uses plain local files, synchronous bounded index reads, atomic writes and file locks with orphan recovery. Index rebuilding scans the scope's memory files. Injection records include session, cwd, included and truncated entries, bytes, budget and snapshot state in `audit.jsonl`; appends are serialized and the log is rotated at a size cap. The web panel summarizes injection/truncation, memory reads, health findings and recent consolidation outcomes. These are implementation and product-documentation observations, not independently measured performance. ([store](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/store.ts), [audit](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/audit.ts), [README](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/README.md))

## Metric-domain evidence

All project benchmark domains are **unmeasured in this review**. The upstream README reports its own evaluation results, including an end-to-end coding-task result and a LongMemEval-S result; those figures are upstream-reported, not reproduced or independently adjudicated here. The reviewed head changes the default prompt budget to 16 KiB and notes historical 4 KiB measurements, so older results should not be assumed to describe the current default. ([README](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/README.md), [metric definitions](../METRICS.md), [fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | The plugin has index injection and lexical search; no benchmark questions were scored. |
| Correction accuracy and stale-value rate | Unmeasured | In-place updates and supersession exist; no correction probes were run. |
| Deletion leakage | Unmeasured | Direct and bulk deletion exist; no post-delete, backup, or reintroduction probes were run. |
| Scope isolation | Unmeasured | User and cwd-derived project layers are source-visible; no cross-workspace isolation workload was run. |
| Evidence support and citation coverage | Unmeasured | Consolidation captures a session quote and trust state; no claim-support adjudication was run. |
| Retrieval latency and write-to-recall delay | Unmeasured | No timings were collected; source describes next-session prompt visibility after writes. |
| Tokens and cost | Unmeasured | Injection is byte-budgeted; no token or provider-cost observations were collected. |
| Storage efficiency | Unmeasured | File-per-memory and audit-log storage are visible; no corpus size was measured. |

## Limits and unknowns

This review inspected the official pinned README and selected current TypeScript sources for record types, storage, tools, prompt injection, retrieval, consolidation, and audit. It did not inspect every panel route, import/export edge case, host version, or deployment configuration, and no local checkout was available in this worker. Source inspection cannot establish deployed scope enforcement, model extraction quality, effective security, deletion completeness, real-world recall, concurrency under load, latency, cost, or storage use. No system, tests, or benchmark workload was run. ([README](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/README.md), [store](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/store.ts), [metric definitions](../METRICS.md))

The official pinned README was checked for a contact email and publishes none. `contact_email` is null; the exact checked URL is recorded. No profile/commit metadata, third-party directory, or inferred address was used. ([README](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/README.md))

## Benchmark status

**Benchmark not run.** dsh-auto-memory, its tests, and benchmark workloads were not run. Project metric definitions, fixture, and status record are included for context only, not as results. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and position](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-auto-memory.md)
- [Official repository](https://github.com/AskTheWay/dsh-auto-memory)
- [Official main branch feed](https://github.com/AskTheWay/dsh-auto-memory/commits/main.atom)
- [Reviewed full head](https://github.com/AskTheWay/dsh-auto-memory/commit/ac3cfd4ba161adf9b48f01238e58d677a55cb09b)
- [Pinned README](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/README.md)
- [Pinned memory types](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/types.ts)
- [Pinned storage and index implementation](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/store.ts)
- [Pinned memory tools](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/tools.ts)
- [Pinned prompt injection](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/prompt.ts)
- [Pinned retrieval and excerpts](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/recall.ts)
- [Pinned automatic consolidation](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/consolidate.ts)
- [Pinned injection audit](https://github.com/AskTheWay/dsh-auto-memory/blob/ac3cfd4ba161adf9b48f01238e58d677a55cb09b/src/audit.ts)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project execution-status record](../results/initial-baselines-status.json)
