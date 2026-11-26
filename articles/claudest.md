# Claudest (claude-memory) source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 126 / Claudest (claude-memory) / claudest  
**Listed repository locator:** [gupsammy/claudest](https://github.com/gupsammy/claudest) (explicit)  
**Catalog source attribution:** [Atlas report at catalog revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/claudest.md); used for roster identity and locator attribution only  
**Current canonical repository:** [gupsammy/claudest](https://github.com/gupsammy/claudest)  
**Default branch / reviewed head:** main / [266a7281bf9dbae9b025fae1d9fef3acb35e7636](https://github.com/gupsammy/claudest/commit/266a7281bf9dbae9b025fae1d9fef3acb35e7636)  
**Review time:** 2026-11-25 08:10:25 UTC (2026-11-25 00:10:25 PST; America/Los_Angeles). GitHub's main feed reports this head at 2026-10-29T07:09:47Z; the repository page confirms main as default branch.  
**Published contact:** No email was found in the official pinned [claude-memory README](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md), which was checked for contact. The JSON records null and that checked URL. No commit/profile metadata, third-party directory, or inferred address was used.

## Identity and scope

The catalog places Claudest (claude-memory) at ordinal 126, slug `claudest`, and lists `https://github.com/gupsammy/claudest` with explicit locator status. It attributes the roster entry to the pinned Atlas report linked above. Atlas was used only for roster identity and locator attribution; this assessment is grounded in current official upstream docs and source.[[roster entry](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/claudest.md)]

GitHub identifies the public canonical repository and default branch `main`. The official main feed names full head `266a7281bf9dbae9b025fae1d9fef3acb35e7636` and update time 2026-10-29T07:09:47Z; the commit page and repository page corroborate the reviewed revision. All upstream documentation and source links in this review pin that SHA.[[repository](https://github.com/gupsammy/claudest)] [[main branch history](https://github.com/gupsammy/claudest/commits/main.atom)] [[reviewed head](https://github.com/gupsammy/claudest/commit/266a7281bf9dbae9b025fae1d9fef3acb35e7636)]

Claudest is a curated Claude Code plugin marketplace. Its `claude-memory` plugin stores conversation transcripts locally, injects selected previous-session context, and offers search and learning extraction. The plugin README specifies Python 3.7+ and uses Python's standard library and SQLite for the default storage path; it is not presented as a hosted service.[[official plugin README](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md)]

## Architecture and data model

The plugin stores its database at `~/.claude-memory/conversations.db` using SQLite WAL and a five-second busy timeout. Its schema separates projects, sessions, messages, branches and branch-to-message membership. Messages are stored once per session by UUID, while each conversation branch has its own active state and aggregated searchable content. An import log tracks transcript file hashes and counts.[[plugin README](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md)] [[database schema](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/db.py)]

A Stop hook launches transcript synchronization asynchronously. The importer parses JSONL records, reconstructs branches from message UUID parent links, and follows `logicalParentUuid` through compaction boundaries. Sync prunes stale branch rows when a fresh parse no longer contains them. A minimal Codex adapter also imports selected user messages and final answers into the shared database.[[architecture notes](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/.claude/rules/claude-memory-architecture.md)] [[sync implementation](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/sync_current.py)] [[branch parser](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/parsing.py)]

On SessionStart, the context hook selects recent sessions from the current resolved project, favors substantive sessions, and injects a bounded context string. Search defaults to the working-directory project and supports project selection, chronological browsing and keyword search. Full-text search adapts from FTS5/BM25 to FTS4 or LIKE according to platform support. Optional semantic retrieval embeds exchanges with EmbeddingGemma 2 through local Ollama and falls back to lexical search when Ollama is unavailable.[[context hook](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/memory-context.py)] [[search implementation](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/search_conversations.py)] [[plugin README](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md)]

## Write, update, delete, and retrieval

**Write.** Session stop reads the transcript file and writes parsed messages and branch membership into SQLite. Hashes in the import log allow unchanged files to be skipped. The Codex path imports user turns and final answers while deliberately omitting commentary, tool calls, function results and reasoning. This can leave Codex recall with less intermediate context than a comparable Claude session.[[importer](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/import_conversations.py)] [[architecture notes](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/.claude/rules/claude-memory-architecture.md)]

**Update.** Re-imports synchronize records by stable message identity; branch reconstruction follows transcript relationships, and stale branch rows are pruned. The selected documentation describes backups and migrations for data rewrites. I did not find a user-facing per-message correction or supersession API in the inspected README and hook paths. For durable extracted learnings, the README describes proposing a target memory-file diff and rationale, then writing only after explicit approval.[[importer](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/import_conversations.py)] [[branch parser](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/parsing.py)] [[plugin README](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md)]

**Delete.** The documented manual reset is to delete `~/.claude-memory/conversations.db` and re-import. I did not locate a per-message deletion workflow in the inspected interface. Database reset is broad; this review did not establish that backups or every derived copy are erased.[[plugin README](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md)]

**Retrieval.** Startup context uses recent same-project sessions and a character budget. On-demand search returns conversation excerpts ranked by FTS/BM25, with platform fallback; optional semantic ranking fuses keyword and vector results. The README describes the agent iterating queries when results need refinement. I found no answer-level abstention or source-citation contract in the inspected retrieval paths; no recall quality was measured.[[context hook](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/memory-context.py)] [[search implementation](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/search_conversations.py)] [[plugin README](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md)]

## Scope isolation, provenance, and evidence

Search resolves the current working directory against stored project paths, and uses a path-keyed filter. Worktrees may map to their main checkout; folderless sessions share a scratch project. Semantic related-session suggestions can intentionally span projects. These implementation choices indicate project scoping behavior but do not establish authorization or isolation guarantees without runtime tests.[[scope resolver](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/cli_common.py)] [[architecture notes](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/.claude/rules/claude-memory-architecture.md)] [[context hook](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/memory-context.py)]

Messages keep session/message identity, timestamps, project association and branch membership; the import log records transcript file path, hash and import count. Search can return snippets of matching transcript text. The reviewed interface does not attach answer claims to source passages or provide a citation ledger, so stored provenance should not be read as evidence that a generated answer is supported.[[database schema](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/db.py)] [[importer](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/import_conversations.py)] [[search implementation](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/search_conversations.py)]

## Efficiency and observability

SQLite and its full-text indexes provide the default local search without external services. Branch aggregation supports searching complete threads; startup summaries are cached and bounded. Optional embeddings run through local Ollama and the README describes background index construction. Logging is configurable. These are source-visible design facts; no runtime timings, token totals, costs, or storage figures were collected.[[database schema](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/db.py)] [[architecture notes](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/.claude/rules/claude-memory-architecture.md)] [[plugin README](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md)]

## Metric-domain evidence

| Domain | Review status | Evidence |
|---|---|---|
| Answerable recall and abstention | Unmeasured | Search and context assembly exist; no answerable recall or abstention probes were run.[[search implementation](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/search_conversations.py)] |
| Correction accuracy and staleness | Unmeasured | Imports reconcile messages and branches; no correction or staleness probes were run.[[importer](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/import_conversations.py)] |
| Deletion leakage | Unmeasured | The documented reset deletes the local database; no residual-copy or leakage audit was run.[[plugin README](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md)] |
| Scope isolation | Unmeasured | Project path filters are implemented; no cross-project isolation probe was run.[[scope resolver](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/cli_common.py)] |
| Evidence support and citation coverage | Unmeasured | Source session identity is retained; answer-level evidence was not scored.[[database schema](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/db.py)] |
| Retrieval latency | Unmeasured | No timed retrieval workload was run.[[metric definitions](../METRICS.md)] |
| Write-to-recall delay | Unmeasured | No timed write/read workload was run.[[sync implementation](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/sync_current.py)] |
| Tokens and cost | Unmeasured | No token or cost measurement was collected.[[metric definitions](../METRICS.md)] |
| Storage efficiency | Unmeasured | No database or index size measurement was collected.[[database schema](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/db.py)] |

**Benchmark status:** not run. The linked metric definitions and benchmark-status record are project context, not Claudest results. The fixture is a planned workload and was not executed.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

- This review covered selected official documentation and source files at one SHA. It did not exhaustively inspect every hook, migration, command, or failure path.
- No Claudest runtime, tests, or benchmark workload was run. Runtime correctness, recall quality, semantic rank quality, and all metric values remain unknown.
- Codex import intentionally skips commentary and tool activity, which can omit useful intermediate session context.[[architecture notes](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/.claude/rules/claude-memory-architecture.md)]
- Project filters were read in source but not tested across project/worktree boundary cases. Isolation guarantees are unverified.
- No per-message delete API was found in the inspected paths. The database reset and documented backup behavior do not establish complete erasure from all copies.[[scope resolver](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/cli_common.py)] [[plugin README](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md)]

## Sources

- [Official claude-memory README at reviewed revision](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/README.md)
- [Architecture notes at reviewed revision](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/.claude/rules/claude-memory-architecture.md)
- [Database implementation at reviewed revision](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/db.py)
- [Importer at reviewed revision](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/import_conversations.py)
- [Session sync at reviewed revision](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/sync_current.py)
- [Branch parsing implementation at reviewed revision](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/parsing.py)
- [Context hook at reviewed revision](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/hooks/memory-context.py)
- [Search implementation at reviewed revision](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/search_conversations.py)
- [Scope resolver at reviewed revision](https://github.com/gupsammy/claudest/blob/266a7281bf9dbae9b025fae1d9fef3acb35e7636/plugins/claude-memory/skills/recall-conversations/scripts/memory_lib/cli_common.py)
- [Curated roster entry](../data/memory-systems.json)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution-status record](../results/initial-baselines-status.json)
- [Benchmark fixture (planned workload)](../fixtures/memory-benchmark-v1.json)
