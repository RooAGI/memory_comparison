# Bot Board source review

## Identity and review pin

- **Curated ordinal:** 97 in `data/memory-systems.json`
- **Listed name / slug:** Bot Board / `bot-board`
- **Listed repository locator:** https://github.com/jalemieux/bot_board
- **Canonical repository:** https://github.com/jalemieux/bot_board
- **Default branch:** `main`
- **Reviewed head:** [`8a98c0f18bb60c44d0637bc418b8fa2d333c9c90`](https://github.com/jalemieux/bot_board/commit/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90)
- **Reviewed at:** 2026-11-24 23:49:45 UTC (15:49:45 PST; America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The curated [Atlas report](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/bot-board.md) is recorded for identity, the listed repository locator, and attribution only. Its descriptions, marks, and layout were not used as assessment evidence. GitHub identifies `main` as the default branch; its main commit feed and the full commit page identify the reviewed head. The README says this GitHub repository mirrors development on a self-hosted Forgejo instance, so this review describes the verified GitHub mirror snapshot.

## Summary

Bot Board is a self-hosted coordination board for coding agents. Its persistent memory is a workspace knowledge base of path-addressed Markdown documents with revision history, author, reason, and source strings. Agents find documents through the HTTP API and channel references; the board does not automatically inject the whole knowledge base into prompts. This review is based on source and documentation at the pinned commit; the application and benchmarks were not run. [README](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/README.md) [workspaces.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/workspaces.py)

## Who and what

The GitHub repository is owned by the account `jalemieux`; the README describes Bot Board as a local, self-hosted message board through which Claude Code, Codex, Copilot, and OpenCode sessions coordinate. The reviewed memory component is part of that application, not a separate memory service. The README says project development happens on self-hosted Forgejo and GitHub is a mirror. [repository](https://github.com/jalemieux/bot_board) [README](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/README.md)

## Architecture and data model

Each workspace owns a shared knowledge base stored in the board's SQLite database. The `knowledge_docs` table records workspace ID, document path, integer revision, body, reason, serialized source strings, deleted flag, author ID, and creation time. A uniqueness constraint on `(workspace_id, path, revision)` and an index on the same lookup tuple support versioned documents. Paths are file-like and bodies are Markdown by convention, not files on disk. [workspaces.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/workspaces.py)

The knowledge base is one of several workspace-owned objects alongside channels, bots, and threads. A channel can refer to knowledge paths and mark some as mandatory reading. The application tells the bot which paths to read; content remains in the API until requested. The workspace guide recommends an index document that points to more specific pages. [README](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/README.md) [main.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/main.py)

## Write, update, delete, and retrieval

- **Write and update:** `PUT /api/knowledge/{path}` creates or replaces a document using `body`, `base_revision`, `reason`, and `sources`. Revision zero is used for a new path. Under the board's write lock, the handler compares the supplied base revision with the current revision and rejects stale writes with a conflict so the writer must reread and merge. An accepted change inserts a new revision; it does not overwrite the old row. Bodies must be nonempty, path-valid, and at most 200,000 UTF-8 bytes; archived workspaces reject writes. [main.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/main.py) [workspaces.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/workspaces.py)
- **Delete:** `DELETE /api/knowledge/{path}` also requires the current base revision. It appends a new revision marked deleted with an empty body; earlier revisions remain available through history and explicit revision reads. This is document removal from the current listing, not erasure of its prior contents. [main.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/main.py) [workspaces.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/workspaces.py)
- **Retrieval:** the API map describes a current-document listing with path, revision, byte count and update time; optional `q` searches paths and bodies. A path read returns the current revision by default or a requested historical revision; a history route returns newest-first revisions (the helper's default page is 50). This is direct lookup and substring search, not vector or ranked semantic retrieval. [main.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/main.py) [workspaces.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/workspaces.py)
- **Scope and isolation:** documents are queried by workspace and path. A bot's token scopes its API access to its own workspace; humans can access all workspaces, and admin-workspace bots can use cross-workspace routes. The project explicitly warns that default anonymous reads and open registration make network placement part of the boundary; private reads and an invite code are required when others can reach a shared board. These are code and documentation observations, not a tested isolation result. [workspaces.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/workspaces.py) [main.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/main.py) [SECURITY.md](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/SECURITY.md)

## Provenance and evidence

Each document revision records the writer, a free-text reason, source strings, and timestamp. The revision history makes edits auditable, and the compare-and-set base revision guards against silently lost updates. The source field is stored as strings; the inspected code does not validate that they resolve to messages, links, or evidence, nor does it attach evidence spans or trust states. README-described reconciliation routines may compare conversations with documents and cite source conversations, but the returned memory remains a human-readable document, not an independently verified claim graph. [workspaces.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/workspaces.py) [README](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/README.md)

## Source-visible efficiency and observability

**Code observations:** path/revision lookup is indexed; knowledge documents have a 200,000-byte write cap; history returns newest revisions with a default limit of 50. The API summary reports current document byte counts and update times. Search uses a query string against paths and document bodies. These bounds and fields expose design choices, not measured speed or cost. [workspaces.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/workspaces.py) [main.py](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/main.py)

No recall latency, throughput, write-to-recall delay, token usage, cost, or storage measurement for this memory path was collected. The project README's broader performance and operating statements are not results from this review.

## Metric-domain evidence

All benchmark domains are **unmeasured** for this review. The project's [metric definitions](../METRICS.md), [shared execution-status record](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json) define the evaluation protocol; they are not Bot Board results.

| Domain | Source observation | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Path/list reads and substring search are visible; no answerability probes were run. | Unmeasured |
| Correction accuracy and stale values | Compare-and-set revisions prevent stale writes from silently replacing current content. | Unmeasured |
| Deletion leakage | Delete hides a document from current reads but preserves older bodies in history. | Unmeasured |
| Scope isolation | Workspace ownership and token-scoped access are visible; configuration-dependent anonymous reads remain a limit. | Unmeasured |
| Evidence support and citation coverage | Revision source strings are retained but not resolved or validated by inspected code. | Unmeasured |
| Retrieval latency | Indexed path/revision access is visible; timings were not collected. | Unmeasured |
| Write-to-recall delay | No scheduled acknowledgment-to-recall probes were run. | Unmeasured |
| Tokens and cost | No workload or provider accounting was done for knowledge operations. | Unmeasured |
| Storage efficiency | SQLite document rows and the body cap are visible; bytes attributable to a corpus were not measured. | Unmeasured |

## Limits and unknowns

This is a selected source review at one verified GitHub mirror commit. Bot Board, its deployment settings, and its benchmark workloads were not run. Source inspection cannot establish retrieval usefulness, correction behavior at the agent level, complete erasure, isolation under a particular network configuration, or operational performance.

The knowledge store is path-addressed Markdown rather than a typed evidence graph. Source strings are not verified against their targets, and deleted text remains readable through revision history. The exact limits and access checks of every UI and API route were not exhaustively audited. The public GitHub repository says it mirrors a self-hosted Forgejo source of development; this review verifies the mirror's branch and commit, not that the Forgejo instance had no unmirrored changes.

## Contact-list follow-up

I checked the official pinned [README](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/README.md), [SECURITY.md](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/SECURITY.md), and [official project website](https://jalemieux.github.io/bot_board/). None publishes a contact email. The JSON records a null email with the checked source URLs.

## Benchmark status

**Benchmark not run.** No Bot Board runtime, tests, or benchmark workload was run. The project metric definitions, fixture, and shared execution-status record describe the proposed protocol; they are not Bot Board results. [metric definitions](../METRICS.md) [execution-status record](../results/initial-baselines-status.json) [planned fixture](../fixtures/memory-benchmark-v1.json)

## Sources

- [Canonical public repository](https://github.com/jalemieux/bot_board)
- [Official main branch commit feed](https://github.com/jalemieux/bot_board/commits/main.atom)
- [Verified main head](https://github.com/jalemieux/bot_board/commit/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90)
- [README.md](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/README.md)
- [Workspace and knowledge implementation](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/workspaces.py)
- [HTTP API and token scope](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/app/main.py)
- [Official security policy](https://github.com/jalemieux/bot_board/blob/8a98c0f18bb60c44d0637bc418b8fa2d333c9c90/SECURITY.md)
- [Official project website](https://jalemieux.github.io/bot_board/)
- [Metric definitions](../METRICS.md)
- [Benchmark execution-status record](../results/initial-baselines-status.json)
- [Planned benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster](../data/memory-systems.json)
- [Atlas attribution source, identity only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/bot-board.md)

**Review boundary:** no Bot Board runtime, benchmark workload, or tests were run.
