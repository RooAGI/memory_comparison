# continuity v2 source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 151 / continuity v2 / continuity-v2  
**Listed repository locator:** [Haustorium12/continuity-v2](https://github.com/Haustorium12/continuity-v2)  
**Canonical repository:** [Haustorium12/continuity-v2](https://github.com/Haustorium12/continuity-v2)  
**Default branch / reviewed head:** main / 4e98d464555603a6166df7acc177bd990096dedb  
**Review time:** 2026-11-25 09:10:34 UTC (01:10:34 PST; America/Los_Angeles).

## Identity and scope

The curated roster lists continuity v2 at ordinal 151 with explicit repository locator https://github.com/Haustorium12/continuity-v2. Its source attribution points to the Agent Memory Atlas catalog entry at revision 19199a4fc249e89c0793be06f0b166b358089ba0. The roster and Atlas source are recorded for identity and locator attribution only; the assessment below is based on the official upstream README and source. GitHub identifies main as the default branch. Its main commits feed reports the full current head 4e98d464555603a6166df7acc177bd990096dedb; the repository page shows the same latest commit.[[curated roster](../data/memory-systems.json)] [[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/continuity-v2.md)] [[GitHub repository](https://github.com/Haustorium12/continuity-v2)] [[main commits feed](https://github.com/Haustorium12/continuity-v2/commits/main.atom)] [[reviewed commit](https://github.com/Haustorium12/continuity-v2/commit/4e98d464555603a6166df7acc177bd990096dedb)]

## Summary

continuity v2 builds a local episodic-memory index over Claude Code JSONL session transcripts and exported claude.ai conversations. It stores sessions and turns in SQLite, mirrors text into FTS5, adds optional sentence-vector and turn-edge indexes, and exposes retrieval through a stdio MCP server. Its README also describes hooks for saving and injecting compaction context.[[README.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/README.md)]

## Who and what

The official README presents this as a local tool for Claude Code, rather than a hosted memory service. The primary record is the conversation transcript; continuity v2 indexes it for cross-session retrieval. Product descriptions in the README are kept distinct from implementation observations below.[[README.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/README.md)]

## Architecture and data model

The indexer stores session identity, project and source labels, title, working directory, times, turn count, source path and source modification time. Turn rows hold session ID, order, timestamp, role and extracted text. An FTS5 external-content table mirrors turn text with insert and delete triggers. SQLite WAL mode is used for indexing and MCP access.[[index.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/index.py)]

The extractor keeps text blocks, represents tool calls as a tool marker plus optional description, and truncates tool-result content to 500 characters. Semantic vectors use 384 dimensions from all-MiniLM-L6-v2 in sqlite-vec, keyed by turn row ID. Separate scripts create TEMPORAL edges between adjacent turns and SIMILAR_TO edges between semantically close turns.[[index.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/index.py)] [[embed.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/embed.py)] [[wire_edges.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/wire_edges.py)] [[wire_similar.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/wire_similar.py)]

## Write, update, delete, and retrieval

**Write/index.** The indexer scans Claude Code project JSONL files. A session with unchanged source modification time is skipped. For a changed file, it removes the old turn/session rows and parses the transcript again. The README documents a separate importer for claude.ai export data. The inspected interfaces do not expose an API for editing an individual memory independently of its transcript.[[index.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/index.py)] [[README.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/README.md)]

**Update and deletion.** Updates are whole-session reindexing rather than fact-level correction. No explicit delete or forget operation appears in the reviewed MCP tool list. The inspected reindex path deletes turn rows but does not show cleanup of sqlite-vec vectors or derived edge rows before new turn IDs are assigned. The selected source review cannot establish whether another operation cleans those derived stores, so physical deletion completeness remains unknown.[[index.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/index.py)] [[mcp_server.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/mcp_server.py)] [[embed.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/embed.py)] [[wire_edges.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/wire_edges.py)]

**Retrieval.** FTS5 search returns ranked snippets and supports optional project substring and source filters. Semantic search encodes the query, fetches vector neighbors, and reranks an over-fetched candidate set using semantic similarity, recency, and session length; the response shows the score components. The README describes TEMPORAL-edge breadth-first thread recall and full or sliced session replay.[[README.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/README.md)] [[mcp_server.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/mcp_server.py)] [[embed.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/embed.py)] [[wire_edges.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/wire_edges.py)]

## Scope isolation

Project and source filters are optional arguments for lexical search and recent-session listing. The documented semantic, thread, and session-replay calls do not expose equivalent project/source filters. These interface observations do not establish access isolation for every deployment or retrieval path; no cross-project probes were run.[[README.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/README.md)] [[mcp_server.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/mcp_server.py)]

## Provenance and evidence

Stored identifiers, roles, timestamps, project labels and source-file paths help locate the originating conversation. Tool calls and results become synthesized text, and result content is truncated during extraction. The inspected sources did not show a citation object or claim-to-source support record. Embedding eligibility excludes short text and text beginning with tool/result markers, using a string-prefix test.[[index.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/index.py)] [[embed.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/embed.py)]

## Efficiency and observability

The indexer skips source files whose modification time is unchanged, uses WAL and FTS optimization, and reports new/updated, unchanged, error, session and turn counts. Embedding generation uses batches of 128 and text prefixes capped at 512 characters. The MCP loads the sentence-transformer model only when semantic search is used, exposes index health and FTS integrity tools, and reranks three times as many vector candidates as the requested result limit. These are source-visible design choices, not measured performance.[[index.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/index.py)] [[embed.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/embed.py)] [[mcp_server.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/mcp_server.py)] [[README.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/README.md)]

## Project metric domains

All workload metrics remain unmeasured. The repository documents and implements retrieval routes, optional filters, transcript reindexing and local indexes, but no answerable recall, abstention, correction, deletion leakage, scope leakage, evidence support, latency, write-to-recall delay, token, cost, or controlled storage observations were collected. See the project metric definitions, status record and fixture for the separate protocol.[[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This bounded inspection focused on the pinned README, indexer, MCP server, embedding generator and edge builders. It did not inspect or run every hook, importer, installer, dependency, or auxiliary script. The system, tests and benchmarks were not run. Physical deletion completeness, end-to-end scope isolation, answer quality, redaction across all input paths, and runtime resource use remain unverified. Unknown here means not established by this review.[[README.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/README.md)] [[index.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/index.py)] [[mcp_server.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/mcp_server.py)] [[embed.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/embed.py)]

## Contact-list follow-up

The official pinned README was checked for a published contact email and none was listed. The repository's SECURITY.md and SUPPORT.md paths were also checked at the reviewed revision and each returned GitHub's “File not found” page. The record stores contact_email as null with the exact checked URLs; no profile or third-party source was consulted.[[README.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/README.md)] [[SECURITY.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/SECURITY.md)] [[SUPPORT.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/SUPPORT.md)]

## Benchmark status

**Benchmark not run.** No runtime, tests, or benchmark workload was run. Source inspection and repository documentation are not measured benchmark results.[[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Canonical GitHub repository](https://github.com/Haustorium12/continuity-v2)
- [Current main commits feed](https://github.com/Haustorium12/continuity-v2/commits/main.atom)
- [Reviewed full head commit](https://github.com/Haustorium12/continuity-v2/commit/4e98d464555603a6166df7acc177bd990096dedb)
- [README.md](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/README.md)
- [index.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/index.py)
- [mcp_server.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/mcp_server.py)
- [embed.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/embed.py)
- [wire_edges.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/wire_edges.py)
- [wire_similar.py](https://github.com/Haustorium12/continuity-v2/blob/4e98d464555603a6166df7acc177bd990096dedb/wire_similar.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status record](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and attribution](../data/memory-systems.json)

**Verification boundary:** continuity v2, its tests, and benchmarks were not run.
