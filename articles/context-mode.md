# Context Mode

## Identity and review pin

- Catalog ordinal: 145
- System: Context Mode
- Slug: `context-mode`
- Listed repository: https://github.com/mksglu/context-mode
- Roster attribution: explicit repository locator; pinned Atlas report is used only for curated identity/locator context ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/context-mode.md)).
- Canonical upstream: https://github.com/mksglu/context-mode
- Default branch: `main`
- Reviewed full head: [2065c0ffdf89b0ee88637c5095bff88d6bce0039](https://github.com/mksglu/context-mode/commit/2065c0ffdf89b0ee88637c5095bff88d6bce0039)
- Review timestamp: 2026-11-25T08:57:44Z (UTC; 2026-11-25 00:57:44 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

Context Mode is a local coding-agent plugin that keeps large tool output in a per-project SQLite FTS index and gives the agent bounded replies plus search and resume tools. Hooks journal selected session and tool events; `ctx_index` also stores files, text, and fetched pages. The separately hosted Context Mode Gateway is a different product. ([README](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/README.md), [architecture guide](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/docs/how-it-works.md))

## Who and what

The official README describes a free local plugin for coding agents; its hooks, sandbox, MCP tools, and per-project index run on the user's machine. The README identifies no named maintainer in its project description, so this review does not assign an owner identity. ([README](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/README.md))

## Architecture and data model

The implementation has host adapters/hooks, a local MCP server, sandbox tools, a journal, and an FTS content store. Its SQLite schema separates `events` from `sources` and `chunks`. Event rows retain session, worktree, agent, event kind, tool/key/path, result and byte fields; source rows retain kind, label, session/worktree/agent, and chunk metadata. ([schema](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/store/schema.ts), [journal append](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/journal/append.ts))

The store uses Node's built-in SQLite in WAL mode and FTS5. Word search uses Porter stemming; a trigram index supports paths and partial terms. Project identity is derived from the Git common directory, or the plain project directory outside Git, while the current worktree is recorded separately. ([database lifecycle](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/store/db.ts), [FTS store](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/store/fts.ts), [project resolution](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/project/resolve.ts))

`ctx_execute`/`ctx_batch` run local child processes. Large output is indexed and reduced to bounded selected content. `ctx_index` stores files/folders, supplied text, or fetched URLs. Host hooks capture the events exposed by adapters, including prompts, edits, commands, tool errors, decisions, and usage. ([tools reference](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/docs/tools.md), [execute](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/execute.ts), [index](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/index.ts), [hook dispatch](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/hooks/dispatch.ts))

## Write, update, delete, and retrieval

**Write/index.** `ctx_index` accepts one path, content body, or URL. Path inputs are resolved under the project worktree and checked against permitted roots. Indexed content is chunked with a source label and session/worktree/agent metadata. Large execution results and selected host-tool output can also be indexed. ([index tool](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/index.ts), [FTS store](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/store/fts.ts), [execute tool](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/execute.ts))

**Update/correction.** The inspected tools expose indexing and purge, but no update or correction operation. Re-indexing creates source records; the inspected code does not define in-place correction, supersession, or fact-level history. A caller can purge a source and index replacement content, but that sequence was not run. ([tools reference](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/docs/tools.md), [index](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/index.ts), [purge](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/purge.ts))

**Delete.** `ctx_purge` accepts exactly one session, source, or project scope and removes matching local event/index rows. This code path does not establish erasure of project files, backups, copied output, or external host logs. ([purge](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/purge.ts), [README](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/README.md))

**Retrieval.** `ctx_search` supports session, worktree, and project scopes; defaults to worktree; filters by source; supports relevance or timeline ordering and paging. Word/trigram matches use BM25 and project-scope results are combined by reciprocal rank fusion. `ctx_resume` returns a bounded state summary or a journal row by sequence. Results name source labels/headings, rather than attaching claim-level citations. ([search](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/search.ts), [FTS store](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/store/fts.ts), [resume](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/resume.ts), [architecture guide](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/docs/how-it-works.md))

## Scope isolation

Each local database belongs to a project identity. Session scope restricts to the session, worktree scope to the current worktree, and project scope includes the repository's worktrees. Path containment protects local execution/indexing boundaries; this is not a tenant authorization service. No hostile-caller or cross-project isolation workload was run. ([project resolution](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/project/resolve.ts), [search](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/search.ts), [FTS filters](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/store/fts.ts))

## Provenance and evidence

Journal rows retain event/session/worktree/agent/tool/path/result/timing/byte metadata. Indexed sources retain source kind and label with session/worktree/agent metadata; search results surface labels and headings. The inspected data model does not represent validated claims, truth/confidence states, answer citations to retained passages, or an audit linking a correction to a superseded claim. ([schema](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/store/schema.ts), [journal append](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/journal/append.ts), [search](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/search.ts))

## Efficiency and observability

Chunking, bounded output, FTS search, paging, and compact resume summaries are designed to reduce context sent to the agent. Local `ctx_stats` and read-only `ctx_doctor` report usage and installation/database health. The README claims zero telemetry and documents user-triggered network paths. Its published byte-saving and latency figures are upstream claims from separately dated, versioned benchmark runs; they are not measurements from this review. ([README](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/README.md), [tools reference](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/docs/tools.md), [architecture guide](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/docs/how-it-works.md))

## Metric-domain evidence

All project benchmark domains remain **unmeasured** for this review. The project fixture and metric definitions were inspected as contract documents only; neither was executed. ([METRICS.md](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Search and source filters are implemented; no answer outcomes were adjudicated. |
| Correction accuracy and stale-value rate | Unmeasured | No correction/supersession API was found; no correction probes were run. |
| Deletion leakage | Unmeasured | Local index purge was inspected; no post-delete probes or copy/backup checks were run. |
| Scope isolation | Unmeasured | Session/worktree/project filters are implemented; no paired leakage workload was run. |
| Evidence support and citation coverage | Unmeasured | Source labels exist; generated claims/citations were not adjudicated. |
| Retrieval latency | Unmeasured | No timing samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write/recall probes were run. |
| Tokens and cost | Unmeasured | No model usage or charges were measured. |
| Storage efficiency | Unmeasured | Store structure was inspected; no corpus size was measured. |

## Limits and unknowns

This inspection covered the README and tools/architecture guides, project resolution, SQLite schema/lifecycle, FTS store, journal append, index/search/purge/resume, hook dispatch, and sandbox execution at the verified head. It did not inspect every host adapter, policy rule, CLI operation, or all code paths. ([reviewed README](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/README.md), [tools reference](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/docs/tools.md), [architecture guide](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/docs/how-it-works.md))

The review did not run Context Mode, its tests, or benchmarks. It therefore makes no runtime claims about answer quality, isolation under adversarial use, deletion completeness, latency, cost, or storage. The upstream README's own reported performance figures are not used as project benchmark results. ([METRICS.md](../METRICS.md), [existing status record](../results/initial-baselines-status.json))

## Contact

No contact email is published in the official pinned README; it directs defect reports and ideas to Discord. The checked source is [README.md](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/README.md). No profile/commit metadata or third-party directory was used.

## Benchmark status

**Benchmark not run.** No system runtime, tests, or benchmarks were run. The project result record remains the not-run reference, and source observations remain separate from benchmark outcomes. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [result/status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Official repository](https://github.com/mksglu/context-mode)
- [Official main commit feed](https://github.com/mksglu/context-mode/commits/main.atom)
- [Reviewed head 2065c0ffdf89b0ee88637c5095bff88d6bce0039](https://github.com/mksglu/context-mode/commit/2065c0ffdf89b0ee88637c5095bff88d6bce0039)
- [Pinned README](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/README.md)
- [Pinned tools reference](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/docs/tools.md)
- [Pinned architecture guide](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/docs/how-it-works.md)
- [Pinned project resolver](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/project/resolve.ts)
- [Pinned schema](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/store/schema.ts)
- [Pinned database lifecycle](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/store/db.ts)
- [Pinned FTS store](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/store/fts.ts)
- [Pinned journal append](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/journal/append.ts)
- [Pinned index tool](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/index.ts)
- [Pinned search tool](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/search.ts)
- [Pinned purge tool](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/purge.ts)
- [Pinned resume tool](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/resume.ts)
- [Pinned hook dispatch](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/hooks/dispatch.ts)
- [Pinned execution tool](https://github.com/mksglu/context-mode/blob/2065c0ffdf89b0ee88637c5095bff88d6bce0039/src/core/tools/execute.ts)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project result/status record](../results/initial-baselines-status.json)
