# Dev MCP Suite

**Review status:** Reviewed from code and official documentation at `master` [`6b69c5b5bb2db80e70814efaa3e9a3308bc54d14`](https://github.com/MaximaLabs/dev-mcp-suite/commit/6b69c5b5bb2db80e70814efaa3e9a3308bc54d14). Review time: 2026-11-25T11:09:19Z UTC (2026-11-25 03:09:19 PST; America/Los_Angeles).

## Summary

Dev MCP Suite is a local-first collection of MCP servers for project notes, session journals, checkpoints, and context tooling.[readme] Its project-memory component stores Markdown notes and an index per caller-selected project directory, with keyword retrieval and optional local or configured remote embeddings.[server][embedding] This is a source review, not a measured memory-quality assessment.

## Who and what

The official README presents four core local MCP servers—project-memory, devjournal, checkpoint, and context-pack—with optional Armada fleet operations.[readme] This review focuses on project-memory, the part that stores and retrieves notes.[server] The catalog resolves ordinal 189 to Dev MCP Suite, slug `codex-dev-mcp-suite`, and listed locator `https://github.com/verrysimatupang99/codex-dev-mcp-suite`; the pinned Atlas entry is retained only for curated identity and locator attribution.[catalog][atlas] The listed repository redirects to the canonical `MaximaLabs/dev-mcp-suite` repository.[repo]

## Architecture and data model

The project-memory component is a Node.js stdio MCP server. Its source describes a local Markdown vault with one notes directory and an `index.json` per project slug; the default server path is `~/.ai-shared-memory/vault`, overridable with `MEMORY_VAULT_DIR`.[server] The slug combines a sanitized directory basename with a short hash of its resolved path.[server]

Each note is a Markdown file with YAML frontmatter, while the JSON index carries note metadata and keyword-search material.[server] The MCP surface includes save, recall, list, get, delete, reindex, wiki-link graph, cross-project recall, deduplication, and auto-indexing operations.[server][readme] Wiki links can resolve by title or alias; graph state stores links and backlinks.[graph]

Retrieval supports keyword search, optional local vector embeddings, or configured embedding endpoints; the README also describes optional LLM reranking.[readme][embedding] The local embedding mode is documented as a 384-dimensional term-frequency/hash vector.[readme] The embedding helper falls back to keyword mode when embeddings are unavailable or fail, and deterministic mode disables embeddings.[embedding][privacy]

GitHub identifies `master` as the default branch.[branches] The official master feed reports current head [`6b69c5b5bb2db80e70814efaa3e9a3308bc54d14`](https://github.com/MaximaLabs/dev-mcp-suite/commit/6b69c5b5bb2db80e70814efaa3e9a3308bc54d14), updated 2026-11-22T07:35:45Z.[head][commit] Review recorded 2026-11-25T11:09:19Z UTC.

## Write, update, delete, and retrieval

`memory_save` accepts a title and Markdown content, plus optional project directory, tags, kind, aliases, and a created timestamp.[server] The declared `memory_delete` operation deletes a note by ID from the vault and index.[server] The inspected tool declarations do not expose a dedicated update or correction operation. Users can work with the Markdown files directly, but this review did not establish how external edits are reconciled into the index.[server][readme]

`memory_recall` accepts a query and optional directory, limit, full-body flag, and auto/semantic/keyword mode.[server] The README describes keyword fallback and optional semantic search and reranking.[readme] Global recall reads project indexes and orders current-project matches first, while still searching across projects; it is an intentional cross-project operation.[global][server]

The auto-indexer can inspect recent Git commits and selected session or log directories. It scans up to five recently modified candidate files and extracts up to ten lines matching a fixed set of decision and architecture keywords, then emits notes containing snippets, role labels, and relative paths.[autoindex] This is heuristic extraction, so a keyword match does not establish that a note is correct or that the quoted text is a verified decision.[autoindex]

## Scope, provenance, efficiency, and observability

The project slug is calculated from a directory argument that defaults to the current working directory.[server] The inspected code does not establish an authenticated tenant or principal boundary; the suite also offers global recall across those project indexes.[server][global] Project-directory partitioning should therefore not be treated as a tested isolation guarantee.

Manually saved notes accept a free-form body and optional kind/tags/aliases; the inspected API does not require citations or a source record.[server] Auto-generated digest notes preserve a role, snippet, and relative file path, which gives limited origin context but is not a structured claim-to-source evidence chain.[autoindex] No independent review gate for auto-derived notes was established in the inspected path.[autoindex][server]

The project’s privacy documentation says storage is local by default and there is no built-in telemetry or hosted backend.[privacy] If remote embedding or reranking endpoints are configured, query text and candidate snippets may be sent to them; deterministic mode disables those model calls.[privacy][embedding] The README advertises sub-millisecond local vector search, but this review did not measure it.[readme]

## Metric-domain evidence

- Answerable retrieval and abstention — unmeasured; no fixed answerability workload was run.[metrics][fixture][status]
- Correction accuracy and stale-value rate — unmeasured; the inspected MCP surface exposes no dedicated correction operation, and no correction workload was run.[server][metrics][fixture][status]
- Deletion leakage — unmeasured; a delete tool is declared, but no post-delete probe or residual-data inspection was run.[server][metrics][fixture][status]
- Scope isolation — unmeasured; project directories are stored separately but global recall crosses them, and no isolation workload was run.[server][global][metrics][fixture][status]
- Evidence support precision and citation coverage — unmeasured; no claim-support or citation-scoring run was performed.[metrics][fixture][status]
- Retrieval latency and write-to-recall delay — unmeasured; the local-search speed statement is a README claim, not a result from this review.[readme][metrics][fixture][status]
- Token use and cost — unmeasured; provider configuration exists, but no usage or charge was collected.[privacy][metrics][fixture][status]
- Storage efficiency — unmeasured; no corpus size or per-item byte measurement was collected.[server][metrics][fixture][status]

Project benchmark status is [`not_run`](../data/system-reviews/codex-dev-mcp-suite.json). See [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution-status record](../results/initial-baselines-status.json). These local documents define a workload and result format; no benchmark, system runtime, or tests were executed.[metrics][fixture][status]

## Limits and unknowns

- This is a bounded review of the official README, privacy guide, project-memory server, auto-indexer, graph, global-index, and embedding helper at one verified master SHA; other suite servers and adapters were not reviewed.
- The project-directory slug comes from the caller’s directory argument, and global recall intentionally spans project indexes. No tenant or user isolation boundary was verified.[server][global]
- The docs/privacy guide describes defaults under `~/.codex/memories`, while the inspected server source defaults the project-memory vault to `~/.ai-shared-memory/vault`. Whether the privacy guide is stale or deployments override the path was not tested.[privacy][server]
- The source review does not establish atomic index/file updates, backup behavior, or complete erasure from copies and filesystem backups.
- Auto-indexing is keyword-based and can turn transcript snippets into persistent notes without independent factual verification.[autoindex]
- No Dev MCP Suite runtime, tests, or benchmarks were run. All metric domains remain unmeasured.

## Sources

- [Canonical repository](https://github.com/MaximaLabs/dev-mcp-suite), [default branch listing](https://github.com/MaximaLabs/dev-mcp-suite/branches), [master feed](https://github.com/MaximaLabs/dev-mcp-suite/commits/master.atom), and [verified head](https://github.com/MaximaLabs/dev-mcp-suite/commit/6b69c5b5bb2db80e70814efaa3e9a3308bc54d14).
- [README](https://github.com/MaximaLabs/dev-mcp-suite/blob/6b69c5b5bb2db80e70814efaa3e9a3308bc54d14/README.md), [privacy and data flow](https://github.com/MaximaLabs/dev-mcp-suite/blob/6b69c5b5bb2db80e70814efaa3e9a3308bc54d14/docs/privacy.md), [project-memory MCP server](https://github.com/MaximaLabs/dev-mcp-suite/blob/6b69c5b5bb2db80e70814efaa3e9a3308bc54d14/project-memory/server.js), and [auto-indexer](https://github.com/MaximaLabs/dev-mcp-suite/blob/6b69c5b5bb2db80e70814efaa3e9a3308bc54d14/project-memory/auto-indexer.js).
- [Wiki-link graph](https://github.com/MaximaLabs/dev-mcp-suite/blob/6b69c5b5bb2db80e70814efaa3e9a3308bc54d14/project-memory/graph.js), [global index](https://github.com/MaximaLabs/dev-mcp-suite/blob/6b69c5b5bb2db80e70814efaa3e9a3308bc54d14/project-memory/global-index.js), and [embedding helper](https://github.com/MaximaLabs/dev-mcp-suite/blob/6b69c5b5bb2db80e70814efaa3e9a3308bc54d14/project-memory/embedding.js).
- [Catalog identity](../data/memory-systems.json) and the [pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/codex-dev-mcp-suite.md); Atlas is identity/locator attribution only.
- [Metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).
