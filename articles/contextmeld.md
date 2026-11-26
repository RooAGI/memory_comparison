# ContextMeld

## Identity and review pin

- **Catalog position:** 149, “ContextMeld”; slug `contextmeld`.
- **Listed repository:** [Ste2027/ContextMeld](https://github.com/Ste2027/ContextMeld); the curated locator is explicit. The pinned Atlas entry is recorded only for roster identity and locator attribution.
- **Canonical upstream:** public GitHub repository [Ste2027/ContextMeld](https://github.com/Ste2027/ContextMeld), default branch `master`. The official [master commit feed](https://github.com/Ste2027/ContextMeld/commits/master.atom) reports full head `77d0acbdeda5769d181e7398dcea32be4e70edc9` (updated 2026-09-06 19:40:40 UTC); read-only `git ls-remote --symref` and a shallow checkout resolved the same SHA. See the official [pinned commit](https://github.com/Ste2027/ContextMeld/commit/77d0acbdeda5769d181e7398dcea32be4e70edc9).
- **Reviewed:** 2026-11-25 09:04:39 UTC (2026-11-25 01:04:39 PST; America/Los_Angeles).
- **Status:** Reviewed from current pinned upstream source and documentation. Benchmark not run.

## Summary

ContextMeld is a local-first Tauri desktop workspace that indexes supported Claude Code and Codex session files into SQLite, offers literal full-text search, and lets a person author reusable scoped memories and include selected notes in an edited cross-agent handoff. Memory notes are not automatically injected into agent sessions. This assessment is pinned to the verified current master head; no runtime, tests, or benchmarks were run. [[official README](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/README.md)] [[architecture](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/docs/architecture.md)]

## Who and what

ContextMeld is an independent, MIT-licensed desktop workspace for local coding-agent session history, search, manually authored memories, and cross-agent context handoffs. The README names Claude Code and OpenAI Codex as supported session adapters; other agents are currently detection-only or planned. The software prepares a package for a person to copy or export and does not launch an agent or submit a prompt.[[README](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/README.md)]

## Architecture and data model

The frontend invokes typed Tauri commands; Rust services normalize supported local JSONL session data and persist sessions, projects, events, and search indexes in SQLite. The documented design runs database work off the UI thread and uses FTS5 for local text search.[[architecture](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/docs/architecture.md)] [[README](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/README.md)]

A memory row stores a UUID, title, Markdown body, scope, optional project path and agent list, tags, revision, timestamps, and a soft-delete timestamp. The migration constrains scope to `global`, `project`, or `agent` and uses FTS5 triggers to index active notes and remove trashed notes from search.[[memory schema](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/migrations/002_memories.sql)] [[memory model and store](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/src/memories.rs)]

Memory notes are person-authored and stay in the local database. They do not become an automatic prompt store. A session handoff can include selected notes after the person reviews and edits the generated context.[[memory guide](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/docs/memories.md)] [[handoff builder](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src/features/ContextExport.tsx)]

## Write, update, delete, and retrieval

**Write.** The memory library accepts a title, body, scope, and optional project, agents, and tags. Source validation bounds the fields and requires a project path or at least one agent for the corresponding scope. Import accepts a bounded JSON archive and skips exact active duplicates. The inspected command surface exposes user-facing CRUD/import/export operations; no agent-authored memory writer was found.[[memory store](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/src/memories.rs)] [[memory commands](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/src/memory_commands.rs)]

**Update.** An edit carries the stored revision. The database updates only if that revision still matches and the memory is active, then increments the revision. A stale edit is rejected for reload rather than silently replacing a concurrent change.[[memory guide](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/docs/memories.md)] [[memory store](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/src/memories.rs)]

**Delete.** Trash sets `deleted_at`; restore clears it. Both change the revision, and database triggers keep trashed notes out of the active FTS index. The reviewed API has no permanent memory purge, so this is reversible logical deletion, not proof of physical erasure.[[memory store](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/src/memories.rs)] [[memory schema](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/migrations/002_memories.sql)]

**Retrieval.** Session search and active memory search use local SQLite FTS5. Memory library browsing supports scope selection, substring filtering, and pagination. For handoffs, the UI offers global notes, project notes whose path matches the session, and agent notes associated with its source agent; people can also stage notes explicitly. The resulting Markdown or JSON is editable and must be copied/exported by the user. It is not automatically injected into an agent.[[database search](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/src/database.rs)] [[memory retrieval](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/src/memories.rs)] [[memory guide](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/docs/memories.md)] [[handoff builder](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src/features/ContextExport.tsx)]

## Scope isolation

The database restricts scope labels, but the Rust listing API filters only by the scope category; project and agent matching is performed in the handoff UI. Explicitly staged memories can be included regardless of the automatic candidate filter. This supports a user-facing handoff selection flow, while the inspected source does not establish a backend authorization boundary for other consumers.[[memory schema](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/migrations/002_memories.sql)] [[memory store](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/src/memories.rs)] [[handoff builder](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src/features/ContextExport.tsx)]

## Provenance and evidence

Memory records keep authored text, scope associations, tags, revision and timestamps. The inspected schema does not include a source citation field or a mutation history of prior versions. Session events retain normalized source/session identity and event metadata, but these do not validate factual correctness or provide claim-level citations for generated answers.[[memory schema](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/migrations/002_memories.sql)] [[memory store](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/src/memories.rs)] [[architecture](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/docs/architecture.md)]

## Efficiency and observability

The source uses FTS5, bounded queries and pagination, transactional session imports, source fingerprints, and incremental file watching. The README documents counts and filters for local indexed activity; the architecture guide notes that filesystem events are not a durable queue and keeps a visible status/manual scan available. The official security policy and README state that the local SQLite index is not encrypted and can contain private transcript text. No efficiency measurements were collected.[[README](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/README.md)] [[architecture](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/docs/architecture.md)] [[security policy](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/SECURITY.md)] [[memory store](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/src-tauri/src/memories.rs)]

## Metric-domain evidence

- **Answerable retrieval and abstention:** FTS and memory retrieval code are visible; no adjudicated query set or abstention workload was run.
- **Correction and stale values:** revision-checked edits are source-visible; no correction probes were run.
- **Deletion leakage:** trash removes notes from active FTS but retains the row; no post-trash query or storage-residual check was run.
- **Scope isolation:** scope labels and handoff matching were inspected; no cross-project/agent isolation workload was run.
- **Evidence and citations:** records expose memory/session metadata but no claim-level citation evaluation was run.
- **Latency:** no retrieval latency samples were collected.
- **Write-to-recall delay:** no timed write-then-recall probes were run.
- **Tokens and cost:** no token usage or provider charges were collected.
- **Storage efficiency:** SQLite and FTS structure were inspected; no corpus-size measurement was taken.

Project metric definitions are in [METRICS.md](../METRICS.md); the shared execution record is [initial-baselines-status.json](../results/initial-baselines-status.json). The [benchmark fixture](../fixtures/memory-benchmark-v1.json) describes a planned workload and is not a result.

## Contact

The official pinned [README](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/README.md) and [SECURITY.md](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/SECURITY.md) publish no contact email. SECURITY.md points to GitHub private vulnerability reporting when available and otherwise asks reporters to contact maintainers privately. The structured record stores `contact_email: null` and both checked URLs. No commit/profile metadata or third-party directory was used.

## Limits and unknowns

The official v0.2.0 verification record reports project checks and a synthetic Windows desktop demo at its stated date. Those checks were not reproduced here and are not evidence of retrieval quality or benchmark outcomes.[[upstream verification record](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/docs/verification.md)]

This review covers selected source paths at the verified current head. It does not establish runtime accuracy, scope safety across every workflow, deletion of database bytes or exported copies, filesystem watcher reliability on a particular machine, or performance and cost. No ContextMeld runtime, tests, or benchmarks were run.[[architecture](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/docs/architecture.md)] [[security policy](https://github.com/Ste2027/ContextMeld/blob/77d0acbdeda5769d181e7398dcea32be4e70edc9/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No ContextMeld runtime, tests, or benchmark workloads were executed. The upstream verification page records checks but not this project's memory benchmark results. See [project metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and the [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

The structured source IDs and pinned URLs are recorded in [contextmeld.json](../data/system-reviews/contextmeld.json). The [pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/contextmeld.md) is included only for curated identity/locator attribution, not as assessment evidence.
