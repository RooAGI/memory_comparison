# AKB source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 47 / AKB / akb  
**Listed repository locator:** [dnotitia/akb](https://github.com/dnotitia/akb)  
**Current canonical repository:** [dnotitia/akb](https://github.com/dnotitia/akb)  
**Default branch / reviewed head:** main / 9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68  
**Review time:** 2026-11-24 20:14:00 UTC (12:14:00 PST, America/Los_Angeles).

## Identity and scope

The curated roster identifies ordinal 47 as AKB, slug `akb`, with the listed repository locator above. The roster’s Atlas URL and revision are recorded for attribution only; Atlas descriptions, marks, and layout were not used as assessment evidence. The official GitHub repository page identifies `main` as the default branch, and its current page and main commit feed agree on full head `9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68`. The code and documentation links below pin to that revision.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/dnotitia/akb)] [[main branch commit feed](https://github.com/dnotitia/akb/commits/main.atom)] [[reviewed head](https://github.com/dnotitia/akb/commit/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68)]

## Summary

AKB is an organizational knowledge base for agents, exposed through MCP, REST, and a web UI. Its core offers versioned documents, tables, files, relations, and retrieval across semantic vectors and BM25 keyword search. PostgreSQL is the primary store in the Native backend; a pluggable vector index is derived search data. The repository also retains an explicit Bare Git backend for compatible installations. This article reports selected pinned source and documentation observations; it does not assess runtime quality or performance.[[README](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/README.md)]

## Who and what

The official README describes AKB as organizational memory for AI agents and identifies Dnotitia, Inc. as the trademark holder. AKB is a self-hostable knowledge-base service with MCP client tooling and reference agent plugins. The memory store is designed as a read/write knowledge substrate; its README says consolidation and other knowledge-maintenance policies belong in external consumers rather than a built-in consolidator.[[README](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/README.md)]

## Architecture and data model

The README describes an access layer (MCP, REST, and web UI), core document/search/relation/session/publication services, and PostgreSQL-backed storage. The Native backend stores document text, metadata, revisions, and BM25 vocabulary in PostgreSQL. A configurable vector-store driver holds derived dense embeddings and sparse vectors; the README says the index can be rebuilt from PostgreSQL after vector-store loss. Explicit Bare Git deployments remain supported as a separate backend mode.[[README](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/README.md)]

Vaults are the knowledge and authorization boundary. Collections group resources. Documents are Markdown with YAML frontmatter; stable `akb://` URIs identify documents, collections, tables, and files. Documents can carry explicit relation edges such as `depends_on`, `related_to`, and `implements`. The README lists agent session lifecycle on a dedicated REST surface and agent-memory vaults as ordinary searchable vaults; this review did not inspect those session internals.[[README](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/README.md)]

## Write, update, delete, and retrieval

**Writes and updates.** The README exposes document put/update/edit operations and revision history. In the Native revision service, a resource mutation is published as a PostgreSQL authority transaction; the service also defines payload verification by byte size and SHA-256 digest before returning a text snapshot. The README describes the vector index as derived state, not the authority for document contents.[[README](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/README.md)] [[native revision service](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/backend/app/services/native_revision_service.py)]

**Deletion and retirement.** The README lists `akb_delete` for document CRUD and documents archive as the way to retire an old version from default search while keeping its citation resolvable. This review did not trace every deletion path through the Native backend, file storage, indexes, backups, or external exports, so it cannot establish complete erasure behavior.[[README](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/README.md)] [[citation guide](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/docs/guides/citing-the-exact-source-behind-an-answer.md)]

**Retrieval.** The search-service docstring describes metadata/ACL prefiltering, query embedding, dense-plus-BM25 search with reciprocal-rank fusion, optional cross-encoder reranking, and hydration with PostgreSQL metadata. It logs per-phase timings and returned counts without query text, user IDs, or result data. The README and evaluation guide describe a published historical LongMemEval-S result, but it is not a measurement from this review or the current head.[[search service](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/backend/app/services/search_service.py)] [[retrieval evaluation guide](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/docs/guides/evaluating-retrieval-claims.md)]

The official citation guide describes document- and section-level references: search hits carry stable URIs, `akb_drill_down` reads a selected section, `akb_get` returns the current commit, and versioned reads can retrieve older text. It explicitly says citations are not attached to each generated sentence. Its guidance also describes indexing edits for search and retaining archived documents for historical review.[[citation guide](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/docs/guides/citing-the-exact-source-behind-an-answer.md)]

## Scope isolation

The README identifies the vault as the access-control unit and says Native SQL isolation uses PostgreSQL ACLs and per-user roles. In the inspected SQL executor, user-supplied SQL runs in a transaction after `SET LOCAL ROLE`; transaction-local scope resets on commit or rollback, and PostgreSQL enforces cross-vault boundaries. The source documents an administrative bypass for active human system administrators. These are implementation observations for the inspected SQL boundary, not a cross-client isolation test or proof for every file, plugin, export, or deployment path.[[README](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/README.md)] [[SQL executor](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/backend/app/services/user_sql_executor.py)]

## Provenance and evidence

Documents expose revision history, current commit identifiers, diffs, and provenance for authorship and relations. The citation guide says a citation can identify the maintained document URI, section, and revision. These fields make source material easier to inspect, but the guide notes citations are document/section-level, not sentence-level; this review does not establish automatic claim-to-evidence validation or truth checking.[[citation guide](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/docs/guides/citing-the-exact-source-behind-an-answer.md)]

## Source-visible efficiency and observability

The README describes PostgreSQL as the source of truth, a rebuildable vector index, configurable vector drivers, and optional event outbox/Redis stream fanout. The search service shows metadata prefiltering, a bounded candidate-page model for Native search, optional reranking, phase timing logs, and a degradation-aware result contract. These are code and documentation observations; no latency, cost, or storage measurements were collected for this review.[[README](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/README.md)] [[search service](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/backend/app/services/search_service.py)]

## Metric-domain evidence

All project benchmark domains for this task remain **unmeasured**. No answerable or unsupported question set, correction/staleness probe, deletion-leak check, cross-vault isolation probe, citation-support adjudication, latency/write-to-recall timing, token/cost accounting, or storage measurement was run. AKB’s own evaluation guide documents a historical LongMemEval-S Recall@5 result of 98.4% (492/500) using hybrid search without a reranker, measured 2026-05-20 on backend revision `b54184a`. The guide cautions that this is a historical configuration-specific retrieval result, not generated-answer accuracy, a current-release guarantee, or a controlled cross-system comparison. The project task status remains benchmark not run.[[retrieval evaluation guide](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/docs/guides/evaluating-retrieval-claims.md)] [[metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Contact-list follow-up

The official pinned README publishes `support@dnotitia.com` for commercial licensing and trademark permission inquiries. The structured record stores that email with the exact README source URL. No commit metadata, personal profile email, third-party directory, or inferred address was used.[[official README](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/README.md)]

## Limits and unknowns

This bounded review inspected the pinned README and evaluation/citation guides plus selected Native revision, search, and SQL-scope code. It did not inspect all CRUD routes, relation/provenance internals, every vector driver, file deletion and retention paths, session-memory internals, or every deployment adapter. No AKB system, benchmark workload, or tests were run. The historical upstream result is reported only as a source-published result with its older revision and date; it was not reproduced. Answer quality on other workloads, complete deletion, end-to-end isolation, and operational performance remain unknown from this review.[[README](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/README.md)] [[native revision service](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/backend/app/services/native_revision_service.py)] [[search service](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/backend/app/services/search_service.py)] [[SQL executor](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/backend/app/services/user_sql_executor.py)]

## Benchmark status

**Benchmark not run.** This task did not execute AKB, tests, or benchmark workloads. The published historical AKB result is not a result from this review and uses an older backend revision. See project metric definitions, execution-status record, and fixture for the separate protocol.[[retrieval evaluation guide](https://github.com/dnotitia/akb/blob/9f5f9e2df283c4b8a4e8a9b21b38195876aa9a68/docs/guides/evaluating-retrieval-claims.md)] [[metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

The structured source IDs and pinned URLs are in [akb.json](../data/system-reviews/akb.json). The roster’s Atlas locator is [the attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/akb.md); it was used only to identify the curated entry.
