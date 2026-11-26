# AgentMemory source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 21 / AgentMemory / `agentmemory-markdown`  
**Listed repository locator:** [jayzeng/agentmemory](https://github.com/jayzeng/agentmemory)  
**Current canonical repository:** [jayzeng/agentmemory](https://github.com/jayzeng/agentmemory)  
**Default branch / reviewed head:** `main` / `a6c256bf3eb0ef63c6bab78f528136a882d45f10`  
**Review time:** 2026-11-24 18:52:11 UTC (10:52:11 PST; America/Los_Angeles).

## Identity and scope

The curated catalog entry at ordinal 21 identifies the system as AgentMemory, slug `agentmemory-markdown`, and lists `https://github.com/jayzeng/agentmemory`. Its source attribution points to the Agent Memory Atlas catalog revision `19199a4fc249e89c0793be06f0b166b358089ba0`. I used the catalog only for identity, locator, and attribution; its descriptive fields, marks, and layout were not assessment evidence. The official GitHub repository page identifies `main` as the default branch, and the current main history plus the latest commit patch identify the full head recorded above.[[curated roster](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agentmemory-markdown.md)] [[GitHub repository](https://github.com/jayzeng/agentmemory)] [[main history](https://github.com/jayzeng/agentmemory/commits/main)] [[reviewed head patch](https://github.com/jayzeng/agentmemory/commit/a6c256bf3eb0ef63c6bab78f528136a882d45f10.patch)]

AgentMemory is a local-first TypeScript/Node memory layer for coding agents. The README describes durable Markdown files for long-term memory, daily logs, topic notes, and a scratchpad; optional qmd search; a CLI; and a stdio MCP server exposing the same core operations. GitHub identifies Jay Zeng as the repository owner; this review does not establish a broader maintainer group.[[README.md](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/README.md)]

## Architecture and data model

**Documentation and code observations.** The default store is a directory under `~/.agent-memory`, configurable through `AGENT_MEMORY_DIR`. The core names four Markdown-backed stores: `MEMORY.md`, `SCRATCHPAD.md`, dated files in `daily/`, and topic files in `topics/`. The README describes Markdown as the source of truth and says basic read/write works without qmd. The CLI and MCP server delegate to the same core functions rather than maintaining separate behavior.[[README.md](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/README.md)] [[core.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/core.ts)] [[mcp-server.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/mcp-server.ts)]

The MCP transport is JSON-RPC 2.0 over newline-delimited stdio. Its five documented tools—context, search, read, write, and scratchpad—call the CLI-shaped core behavior. The README says a remote-only hosted connector needs a separate relay; that relay is deployment-specific and outside this package.[[README.md](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/README.md)] [[mcp-server.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/mcp-server.ts)]

## Write, update, delete, and retrieval

**Write and update.** The core write operation appends timestamped entries to daily or topic Markdown, and by default to long-term memory; long-term memory also accepts overwrite mode. Entries can include a short session identifier and optional source URI. Before writing, the inspected code redacts recognized credential patterns in new content and in the existing text used for previews. Daily and topic writes append; overwrite replaces the long-term file. The README documents the corresponding `write` CLI command and source-of-truth files.[[core.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/core.ts)] [[README.md](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/README.md)]

The scratchpad has explicit add, done, undo, clear-done, and list actions over a Markdown file. The inspected public write and MCP surfaces do not expose a per-entry deletion or correction API. The README says users can inspect, edit, and delete the plain files with ordinary tools; the CLI's uninstall flow can optionally remove the entire memory directory. These mechanisms should not be read as indexed, audited deletion semantics.[[core.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/core.ts)] [[mcp-server.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/mcp-server.ts)] [[README.md](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/README.md)] [[cli.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/cli.ts)]

**Retrieval.** The documented interfaces include reading selected memory targets, building context, and searching. Keyword mode is available directly; qmd is an optional local search/index helper, so a basic file workflow remains possible without it. This source review does not establish retrieval quality, ranking behavior under a workload, or whether every caller uses the same context limits.[[README.md](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/README.md)] [[core.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/core.ts)]

## Scope isolation and provenance

**Scope isolation.** The default store is user-local and the memory directory can be changed by environment variable. This supports separate directory configuration, but the inspected sources do not establish authenticated tenant boundaries or authorization checks between users or projects. A local path choice is not itself an access-control guarantee.[[README.md](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/README.md)] [[core.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/core.ts)]

**Provenance and evidence.** Stored entries can carry a timestamp, an abbreviated session ID, and an optional source URI. Those are traceability hints, not a structured claim-to-evidence graph, trust state, or verification that a source supports a remembered statement. The README also documents credential-shape redaction before AgentMemory writes or injects content; the review did not measure its coverage or false-positive rate.[[core.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/core.ts)] [[README.md](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/README.md)]

## Source-visible efficiency and observability

**Code and documentation observations.** Markdown storage is directly inspectable and avoids requiring a database service. qmd indexing and semantic/local search are optional; source-visible write paths schedule qmd updates after file changes, while the core also exposes status/probe behavior for qmd and embeddings. The stdio MCP server is dependency-light and reuses core logic. These are implementation and design observations only. No latency, write-to-recall delay, token use, cost, or storage efficiency was measured.[[README.md](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/README.md)] [[core.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/core.ts)] [[mcp-server.ts](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/src/mcp-server.ts)]

## Project metric domains

All project benchmark domains remain **unmeasured** for AgentMemory. No system, benchmark workload, or tests were run for this review. The metric definitions, fixture, and baseline status record describe the project protocol, not AgentMemory results.[[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark status record](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded review of the current README, core implementation, MCP server, and CLI at the verified head. It does not establish runtime correctness, retrieval quality, capture reliability across supported agents, exact qmd indexing/update behavior under failure, or cross-process concurrency behavior. No individual-entry delete API was found in the inspected core write and MCP tool surfaces; manual file deletion and whole-directory removal do not establish cleanup of any separately configured or derived qmd state. Further inspection or execution would be needed to answer those questions, and no execution was performed here.

The official README and security policy page, and the official project site, were checked for a published contact email. None was published in those checked sources; the review record stores `contact_email: null` and the checked URLs.[[README.md](https://github.com/jayzeng/agentmemory/blob/a6c256bf3eb0ef63c6bab78f528136a882d45f10/README.md)] [[security policy](https://github.com/jayzeng/agentmemory/security/policy)] [[official project site](https://jayzeng.github.io/agentmemory/)]

## Benchmark status

**Benchmark not run.** Source inspection is not a measurement. The project result record remains the only benchmark-status reference for this review; no AgentMemory benchmark result is claimed.[[benchmark status record](../results/initial-baselines-status.json)] [[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]
