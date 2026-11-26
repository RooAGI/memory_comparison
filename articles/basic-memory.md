# Basic Memory

## Identity and review pin

- **System:** Basic Memory
- **Curated position:** 88
- **Slug:** `basic-memory`
- **Listed repository:** [basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory)
- **Canonical repository at review:** [basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory)
- **Default branch:** `main`
- **Reviewed head:** [`8d002c93fd5d68fbb9690c6de9b90792040dce1c`](https://github.com/basicmachines-co/basic-memory/commit/8d002c93fd5d68fbb9690c6de9b90792040dce1c)
- **Reviewed:** 2026-11-24 23:21:12 UTC (15:21:12 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/basic-memory.md), used only for identity, listed repository, and source attribution.

The curated roster identifies Basic Memory at position 88, slug `basic-memory`, with the repository locator above.[[catalog]] Its Atlas source is recorded for attribution only; Atlas descriptions, marks, and layout were not assessment evidence.[[atlas]] The official repository page identifies `main` as the default branch, and its main branch Atom feed identified the full head reviewed here. A shallow checkout at that exact SHA matched both the feed and `git ls-remote --symref`.[[repo]][[head-feed]][[head]]

## Summary

Basic Memory is a local-first knowledge management system in which Markdown notes are the durable source of truth and an indexed database provides structured graph, full-text, and optional semantic retrieval. Humans and MCP clients can read and update the same notes; local and hosted deployments share the note model while using different storage and routing adapters.[[readme]][[architecture]][[note-format]]

## Who and what

The canonical repository belongs to the `basicmachines-co` GitHub organization and identifies Basic Machines as the project maker. It is a Python application exposed through MCP, a REST API, and a CLI, with hosted cloud components and agent integrations maintained in the same repository.[[repo]][[readme]][[architecture]]

## Architecture and data model

**Source observations.** Notes are plain Markdown files with optional YAML frontmatter, categorized observations, and wiki-link relations. Frontmatter carries title, type, tags, permalink, timestamps, and arbitrary metadata; parser-derived observations and relations are projections of the Markdown. Permalinks are stable note identifiers, while paths identify the source file.[[note-format]][[domain]][[models]]

The database represents each note as a project-owned entity, with observation rows for categorized facts, directed relation rows for graph links, section and search projections, and optional semantic chunks/vectors. Entity rows carry a project ID, external ID, path, permalink, checksums, timestamps, and optional creator/updater identifiers. Observation and relation rows inherit project scope and belong to an entity. A local SQLite database is the default; PostgreSQL and optional Milvus/pgvector paths are also present. The note file remains the authorable source; indexes and vectors can be rebuilt from it.[[models]][[note-format]][[semantic]][[architecture]]

The runtime has API, MCP, and CLI entrypoints wired through composition roots. MCP tools call typed API clients, which delegate through API routers, services, repositories, and indexing workflows. Accepted note changes persist the accepted entity/content snapshot in a transaction, then publish graph and search projections after commit; a derived-index failure is logged and converged later rather than rolling back the accepted note.[[architecture]][[note-writes]]

## Write, update, delete, and retrieval

**Write and update.** `bm_write` creates a note addressed by path or title plus directory. An existing note is refused unless overwrite is requested; an expected checksum can guard replacement against the version read. Overwrite replaces the body while retaining existing frontmatter keys unless new content or arguments set them. `bm_edit` changes an existing exact-resolved note by append, prepend, find/replace, section replacement/insertion, or metadata merge, and can also use an expected checksum. A missing edit target is not created. File edits made outside the application are indexed from disk by the sync/indexing workflow.[[write]][[edit]][[architecture]][[note-format]]

**Delete.** `bm_delete` removes one note or, with explicit recursive intent, a directory tree. A checksum can guard a single-note delete. The tool describes deletion as irreversible; entity-owned observations and outgoing relations cascade, while incoming relation rows retain their unresolved target name. Derived database/search/vector cleanup and filesystem cleanup follow the mutation/indexing paths. No per-fact tombstone or recoverable note-level version history is established by the inspected API; cloud backups and external copies are outside this review.[[delete]][[models]][[note-writes]]

**Retrieval.** `bm_search` can search notes, observations, and relations by full text, semantic similarity, hybrid ranking, title, or permalink, with project, path, identifier, metadata, type, category, and time filters. It returns ranked results and can return matching-line windows; `bm_read` retrieves a selected note. `bm_context` traverses relations from a starting note with bounded depth, pagination, and compact mode. Semantic search uses embeddings and vector candidates alongside full-text results; optional cross-encoder reranking is disabled by default. Indexed semantic results can lag accepted note content until vector sync catches up, and the entity model tracks checksum-based embedding freshness.[[search]][[context]][[semantic]][[models]]

## Scope isolation

Each note and its search/index projections belong to a project. MCP calls route through an explicit project or project-qualified path, and filesystem paths are checked to remain within the selected local project root. Search APIs and vector collections apply project scoping. These are project-level boundaries; the OSS security policy says Basic Memory is designed for a single-user local knowledge base and does not implement access controls between operating-system users. The hosted Teams product intentionally shares notes within a team workspace and has cloud authorization behavior beyond this core review. The local project selector and path checks do not prove isolation for every cloud deployment or integration.[[scoped-target]][[models]][[search]][[semantic]][[security]][[readme]]

## Provenance and evidence

The Markdown note is directly inspectable, and entity metadata can include arbitrary fields such as a source value. Entity rows also record file checksums, create/update timestamps, and optional creator/updater IDs in hosted contexts. These fields establish file identity and mutation bookkeeping; the inspected note format does not require claim-level citations, evidence excerpts, confidence, or a verified-truth state for observations. Relations preserve declared link text when a target is missing, which keeps unresolved links visible rather than making them evidence of a verified target. Note timestamps describe authored note time, distinct from filesystem modification bookkeeping.[[note-format]][[models]][[domain]][[security]]

## Source-visible efficiency and observability

**Code observations, not measurements.** Full-text search has indexed query paths; semantic search adds vector candidate lookup, chunking, embedding batches, and optional reranking. The docs expose controls such as vector candidate count and embedding batch size, and explain that reranking adds latency and may download a model on first use. Compact graph context omits observations to avoid the cost of loading them. The entity model records checksums to tell whether embeddings reflect the latest note content. Search trace types record stage-level values such as candidate counts, dropped candidates, thresholds, embedding time, vector query time, FTS timing, and fusion ordering. Logging and project indexing diagnostics make operational failures inspectable. None of those source mechanisms is a measured result from this review.[[semantic]][[context]][[models]][[search-trace]][[architecture]]

## Metric-domain evidence

All domains below are **unmeasured for this review**. Source mechanisms and documentation are not benchmark outcomes.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Ranked search and graph context are implemented; no answerability or abstention cases were evaluated. | Unmeasured |
| Correction accuracy and stale values | Exact edits and checksum guards are available; no correction or stale-fact probe was adjudicated. | Unmeasured |
| Deletion leakage | Note and recursive directory deletion exist; no residual-copy or deletion-leakage probe was run. | Unmeasured |
| Scope isolation | Project routing and scoped indexes are visible; no cross-project or cross-user isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Markdown supports source metadata and relation context but does not require claim citations; no support adjudication was run. | Unmeasured |
| Latency and write-to-recall delay | Search stages expose timing fields and vector freshness is tracked; no latency or freshness timing was collected. | Unmeasured |
| Tokens, cost, and storage | Local embedding and configurable hosted providers are available; no token, price, or storage measurement was collected. | Unmeasured |

The [project metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) describe measurement domains and planned reporting, not Basic Memory results.[[metrics]][[fixture]][[status]]

## Limits and unknowns

This is a bounded read-only source review of selected docs and code at the reviewed SHA. It does not establish actual retrieval accuracy, correction behavior under user workflows, secure erasure across backups or synced copies, cloud authorization behavior, index convergence time, provider reliability, or real latency, cost, and storage.[[architecture]][[write]][[delete]][[search]][[semantic]][[security]]

The project offers several deployment and retrieval options whose behavior depends on configuration, backend, and integration. This review did not exercise those variants or verify live cloud controls. Documentation statements about search and deployments are identified as documentation; implementation observations are not treated as runtime evidence.[[readme]][[semantic]][[architecture]]

## Benchmark status

**Benchmark not run.** I did not execute Basic Memory, a benchmark workload, or tests. The project metric definitions and versioned fixture define possible evaluations; the current execution-status record is project-wide and is not a result for Basic Memory.[[metrics]][[fixture]][[status]]

## Contact-list follow-up

I checked the official pinned [README](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/README.md) and [SECURITY.md](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/SECURITY.md). The README did not publish a contact email; the security policy publishes `hello@basicmachines.co` for vulnerability reports. The JSON records the email and exact source URL.

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/basic-memory.md) — source attribution only.
- [Official repository](https://github.com/basicmachines-co/basic-memory) — canonical repository and default branch.
- [Official main commit feed](https://github.com/basicmachines-co/basic-memory/commits/main.atom) — full main head at review time.
- [Reviewed head](https://github.com/basicmachines-co/basic-memory/commit/8d002c93fd5d68fbb9690c6de9b90792040dce1c)
- [README](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/README.md)
- [Security policy](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/SECURITY.md)
- [Architecture](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/docs/ARCHITECTURE.md)
- [Note format](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/docs/NOTE-FORMAT.md)
- [Semantic search guide](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/docs/semantic-search.md)
- [Domain model](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/src/basic_memory/schemas/base.py)
- [Database model](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/src/basic_memory/models/knowledge.py)
- [Project routing and path boundary](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/src/basic_memory/mcp/note_targets.py)
- [Write tool](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/src/basic_memory/mcp/tools/write.py)
- [Edit tool](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/src/basic_memory/mcp/tools/edit.py)
- [Delete tool](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/src/basic_memory/mcp/tools/delete.py)
- [Ranked search tool](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/src/basic_memory/mcp/tools/ranked_search.py)
- [Graph context tool](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/src/basic_memory/mcp/tools/context.py)
- [Accepted note write service](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/src/basic_memory/services/note_content_writes.py)
- [Search trace model](https://github.com/basicmachines-co/basic-memory/blob/8d002c93fd5d68fbb9690c6de9b90792040dce1c/src/basic_memory/repository/search_trace.py)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only source review; no Basic Memory execution, benchmarks, or tests.
