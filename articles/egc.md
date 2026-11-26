# EGC

## Identity and review pin

- Catalog ordinal: 209
- System: EGC
- Slug: `egc`
- Listed repository: https://github.com/Fmarzochi/EGC
- Roster attribution: explicit listed repository; the pinned Atlas entry is retained for curated identity/locator context only ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/egc.md)).
- Canonical upstream: https://github.com/Fmarzochi/EGC
- Default branch: `main`
- Reviewed full head: [afb9a74ef450535f06cc25e94b76cdb4c92892fd](https://github.com/Fmarzochi/EGC/commit/afb9a74ef450535f06cc25e94b76cdb4c92892fd)
- Review timestamp: 2026-11-25T12:06:29Z (UTC; 2026-11-25 04:06:29 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

EGC is a local-first runtime for coding agents with several memory forms: encrypted project and global Markdown state, SQLite decision history and learned lessons, and expiring project-scoped working memory. It uses branch-aware state lookup, FTS5/BM25 search when available, and Team Brain synchronization for selected state and records. In the inspected history and lesson search paths, stored project attribution is not used as a project filter. This review is pinned to the verified current main head; it reports source behavior, not measured outcomes. ([README](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/README.md), [state tools](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-state-tools.ts), [decision and working-memory tools](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-misc-tools.ts), [search](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/search.ts))

## Who and what

The repository presents EGC as a local-first engine that connects multiple coding tools to shared project memory, command guardrails, and a session bus. Team Brain is an optional route for syncing sealed state to a private Git remote. ([README](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/README.md))

The official repository page identifies `main` as the default branch. Its main commit feed reports full head `afb9a74ef450535f06cc25e94b76cdb4c92892fd`, updated at 2026-11-22T05:10:00Z; the official commit page confirms the pinned revision. ([repository](https://github.com/Fmarzochi/EGC), [main feed](https://github.com/Fmarzochi/EGC/commits/main.atom), [head commit](https://github.com/Fmarzochi/EGC/commit/afb9a74ef450535f06cc25e94b76cdb4c92892fd))

## Architecture and data model

The memory implementation has two distinct durable stores. The project and global state are Markdown documents under `~/.egc/state` and `~/.egc/global/state.md`; the state-file writer encrypts them with AES-256-GCM and stores an HMAC integrity sidecar. The MCP server separately opens `~/.egc/memory/state.db` as SQLite for decision, lesson, working-memory, and session data. The README describes memory as encrypted broadly, while the inspected database open path does not apply the document encryption to `state.db`. ([README](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/README.md), [state tools](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-state-tools.ts), [database](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-db.ts), [encryption](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/encryption.ts))

A project-state document contains `Context`, `Active Decisions`, `Do Not Repeat`, `Preferences`, and `Next Session` sections. The implementation caps these at 15, 10, and 15 entries for the middle three sections. Incoming values precede existing values during merge, exact duplicates are dropped, and retired-entry hashes help synchronized copies avoid restoring entries that were deliberately displaced. ([state document](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/state-doc.ts))

The project-state filename uses the last two path components, with a separate key for each Git branch. Branch names are represented by a readable sanitized prefix plus a SHA-256 digest; detached checkouts use the exact commit ID. Decisions and lessons carry project path/key fields; working-memory rows carry project identity, key/value, expiry, machine label, and update time. ([branch resolver](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/branch-state.ts), [decisions](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-misc-tools.ts), [lessons](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-lessons.ts), [working memory](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/working-memory.ts), [sync records](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/sync/records.ts))

SQLite uses WAL when available, foreign keys, a busy timeout, and a shared write arbitration queue. FTS5 indexes support decisions and lessons when the runtime SQLite build has the extension; index setup falls back when unavailable. ([database](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-db.ts), [search](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/search.ts))

## Write, update, delete, and retrieval

**Write project state.** `update_state` validates bounded fields and scans free-text values for suspicious instruction-like content. It resolves the current project and Git state, locks the document, merges the supplied sections, encrypts the new file, writes the HMAC, and notifies active sessions. Project state is also scrubbed and propagated into supported tools' instruction files. A separate `scope: global` path writes user-wide state. ([state tools](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-state-tools.ts), [branch resolver](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/branch-state.ts), [state document](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/state-doc.ts), [tool definitions](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-tool-definitions.ts))

**Update and correction.** Context is replaced when a nonempty value is supplied, `Next Session` is rewritten, and decisions/avoid/preferences are merged with exact-text deduplication and section caps. This gives a compact current-state document, not a typed per-fact correction ledger. Decision history is append-oriented: `store_decision` adds a row, while query/search expose history. Lesson writes deduplicate exact active content/context and reinforce confidence; recall reinforces recency, and a daily sweep decays confidence after 30 days then archives below 0.2. ([state document](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/state-doc.ts), [decision tools](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-misc-tools.ts), [lesson lifecycle](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-lessons.ts))

**Delete.** The exposed memory tool definitions have no general decision-delete or lesson-delete operation. Working-memory entries expire and are physically removed by sweeps. State can be changed through section updates and cap/retirement behavior, but the reviewed surface does not provide a general per-item deletion guarantee spanning the database, derived search indexes, synchronized records, and Git history. If a state document cannot be decrypted, the source quarantines it as a backup sibling instead of erasing it. ([tool definitions](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-tool-definitions.ts), [working memory](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/working-memory.ts), [state document](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/state-doc.ts), [encryption](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/encryption.ts), [sync records](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/sync/records.ts))

**Retrieval.** `get_state` reads the current branch file, then default-branch state, with legacy flat-file compatibility; detached HEAD reads only its exact commit file. Global state may be appended after the project state. Decision search tokenizes and quotes terms for FTS5, joins terms with OR, normalizes BM25 scores, and falls back to substring search if FTS5 is absent. Lesson recall uses FTS5 where available and otherwise filters a bounded confidence-ordered set by substrings. ([tool definitions](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-tool-definitions.ts), [branch resolver](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/branch-state.ts), [search](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/search.ts), [decision operations](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-misc-tools.ts), [lesson lifecycle](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-lessons.ts))

## Scope isolation

Project Markdown has branch-aware lookup and an explicit user-wide scope. Working-memory access applies a same-project predicate: a project remote identity can join copies in different checkout folders, otherwise the exact project path is used. However, decision-history query/search and lesson recall SQL do not include a caller project predicate, despite stored project attribution. The local workspace model therefore does not establish isolation for those record searches; no runtime isolation probes were run. ([branch resolver](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/branch-state.ts), [state tools](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-state-tools.ts), [working memory](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/working-memory.ts), [decision operations](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-misc-tools.ts), [search](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/search.ts), [lesson lifecycle](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-lessons.ts))

## Provenance and evidence

State documents record project, branch, author, and update time. SQLite records include identifiers and timestamps; decisions and lessons include project and machine or author metadata, and working memory includes project identity, machine, and update time. State files are authenticated with HMAC; free-text state and lesson inputs are checked by the sanitizer. Team Brain sync seals selected state and per-record data with the team key; the README says the memory database itself does not travel. These are record-origin and integrity signals, not claim-level citations or a history connecting corrected facts to previous values. ([state document](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/state-doc.ts), [state tools](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-state-tools.ts), [decision operations](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-misc-tools.ts), [lesson lifecycle](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-lessons.ts), [working memory](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/working-memory.ts), [sync records](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/sync/records.ts), [encryption](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/encryption.ts), [README](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/README.md))

## Efficiency and observability

Source-visible controls include FTS5/BM25 search, indexed expiry lookup for working memory, SQLite WAL, write arbitration, bounded tool inputs/results, periodic expiry and lesson-decay sweeps, and structured server logs. The health tool reports the SQLite engine and arbitration mode. These mechanisms are not performance measurements; latency, token use, cost, and storage efficiency remain unmeasured. ([search](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/search.ts), [working memory](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/working-memory.ts), [database](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-db.ts), [decision operations](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-misc-tools.ts), [metric definitions](../METRICS.md))

## Metric-domain evidence

Every project benchmark domain remains **unmeasured**. The versioned fixture and metric definitions were checked as project references only; neither was executed. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | No fixture questions or response outcomes were adjudicated. |
| Correction accuracy and stale-value rate | Unmeasured | Merge, reinforcement, and decay behavior were inspected; no correction probes were run. |
| Deletion leakage | Unmeasured | No post-delete probes or erasure-completeness checks were run. |
| Scope isolation | Unmeasured | Scope predicates are visible in source; no allowed/forbidden paired probes were run. |
| Evidence support precision and citation coverage | Unmeasured | No generated answers were adjudicated for source support or citations. |
| Retrieval latency | Unmeasured | No latency samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write/recall probes were run. |
| Tokens and cost | Unmeasured | No token or cost measurements were collected. |
| Storage efficiency | Unmeasured | No persistent bytes or bytes-per-accepted-item measurements were collected. |

## Limits and unknowns

This is a selected review of the pinned README and memory MCP state, branch, document, database, decision, lesson, search, working-memory, sync-record, and encryption source files. It does not trace every agent caller, project path boundary, tool integration, migration, or Team Brain deployment. ([README](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/README.md), [state tools](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-state-tools.ts), [branch resolver](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/branch-state.ts), [state document](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/state-doc.ts), [database](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-db.ts), [decision operations](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-misc-tools.ts), [lesson lifecycle](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-lessons.ts), [search](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/search.ts), [working memory](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/working-memory.ts), [sync records](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/sync/records.ts), [encryption](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/encryption.ts))

Decision and lesson searches visibly omit project predicates, so environments that invoke these tools across projects need further scope review. This is a source-level observation, not a runtime exploit finding or isolation test. Filesystem-level encryption, backup handling, migration/recovery behavior, and whether other layers add controls were not established. ([decision operations](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-misc-tools.ts), [search](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/search.ts), [lesson lifecycle](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-lessons.ts), [database](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-db.ts))

## Contact

The official pinned README was checked for a published contact email and does not list one. `contact_email` is therefore null; the checked source is [README.md](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/README.md). No commit/profile metadata or third-party directory was used.

## Benchmark status

**Benchmark not run.** No EGC runtime, tests, or benchmarks were run. Source observations and upstream descriptions are separate from benchmark outcomes. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/egc.md)
- [Official repository](https://github.com/Fmarzochi/EGC)
- [Official main commit feed](https://github.com/Fmarzochi/EGC/commits/main.atom)
- [Reviewed head afb9a74ef450535f06cc25e94b76cdb4c92892fd](https://github.com/Fmarzochi/EGC/commit/afb9a74ef450535f06cc25e94b76cdb4c92892fd)
- [Pinned official README](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/README.md)
- [Pinned state read/write source](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-state-tools.ts)
- [Pinned branch state resolver](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/branch-state.ts)
- [Pinned state document model](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/state-doc.ts)
- [Pinned MCP memory tool definitions](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-tool-definitions.ts)
- [Pinned SQLite setup](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-db.ts)
- [Pinned decision and working-memory operations](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-misc-tools.ts)
- [Pinned lesson lifecycle](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/memory-lessons.ts)
- [Pinned FTS search](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/search.ts)
- [Pinned working-memory implementation](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/working-memory.ts)
- [Pinned synchronized records](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/sync/records.ts)
- [Pinned state encryption](https://github.com/Fmarzochi/EGC/blob/afb9a74ef450535f06cc25e94b76cdb4c92892fd/mcp/servers/egc-memory/src/encryption.ts)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark status record](../results/initial-baselines-status.json)
