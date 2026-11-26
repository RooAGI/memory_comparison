# ai-memory source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 40 / ai-memory / `ai-memory`  
**Listed repository locator:** [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory)  
**Current canonical repository:** [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory)  
**Default branch / reviewed head:** main / `ccc7dc0db1271e94785b3e7e5a1758a89fde202d`  
**Review time:** 2026-11-24 19:48:55 UTC (11:48:55 PST; America/Los_Angeles).

## Identity and scope

The curated roster places ai-memory at ordinal 40 and lists `https://github.com/akitaonrails/ai-memory`. Its attribution points to the Agent Memory Atlas entry pinned at `19199a4fc249e89c0793be06f0b166b358089ba0`. The roster is used only for ordinal, identity, listed locator, and source attribution; Atlas descriptions, marks, prose, and layout are not assessment evidence. The official GitHub repository page identifies the public repository and default branch `main`; the visible latest commit and read-only `git ls-remote --symref` both identify `ccc7dc0db1271e94785b3e7e5a1758a89fde202d` as main/HEAD. A shallow checkout resolved to the same SHA. [[curated roster](../data/memory-systems.json)] [[repository](https://github.com/akitaonrails/ai-memory)] [[main commits feed](https://github.com/akitaonrails/ai-memory/commits/main.atom)] [[reviewed commit](https://github.com/akitaonrails/ai-memory/commit/ccc7dc0db1271e94785b3e7e5a1758a89fde202d)]

The repository describes a Rust application for coding-agent memory, with lifecycle hooks, an MCP server, CLI, and optional HTTP/web surfaces. The project website credits Fabio Akita in its footer. The current article records source structure and documentation, not runtime behavior. [[README](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/README.md)] [[architecture](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/docs/ARCHITECTURE.md)] [[official project site](https://aimemory.sh/)]

## Architecture and data model

The durable knowledge base is a git-versioned tree of ordinary Markdown pages. SQLite is a derived index for page versions and retrieval, plus sessions, observations, handoffs, audit state, and optional embeddings. The README describes the index as rebuildable from the wiki files. [[README](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/README.md)] [[architecture](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/docs/ARCHITECTURE.md)]

Lifecycle hooks send prompt, tool, and session-boundary observations to a router that sanitizes the content before storage. Observation records carry workspace, project, and session IDs, event kind, body, time, importance, and trust class. A single-writer actor serializes SQLite mutations. [[hook router](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-hooks/src/router.rs)] [[observation model](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-core/src/observation.rs)] [[writer actor](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/writer.rs)]

The wiki layer atomically writes files and indexes versions. A page rewrite creates a new version and supersedes the prior version. Page provenance can link a page version to captured source observations, subject to ownership/read access when source details are returned. [[wiki mutation layer](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-wiki/src/wiki.rs)] [[provenance reader](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/provenance.rs)]

## Write, update, delete, and retrieval

**Write and compile.** Hooks store sanitized observations. At session end, the documented path can produce a rule-based session page and a handoff without calling an LLM. When configured, consolidation can rewrite that summary or produce additional durable wiki pages. These source paths describe mechanisms; no writes were performed in this review. [[architecture](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/docs/ARCHITECTURE.md)] [[hook router](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-hooks/src/router.rs)] [[README](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/README.md)]

**Update.** `Wiki::write_page` writes a Markdown file and upserts its indexed page version. The store uses page versioning/supersession, and conditional writes can fail without changing the page when the expected current version is stale. Older versions remain available to version-history and restore paths. [[wiki mutation layer](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-wiki/src/wiki.rs)] [[MCP operations](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-mcp/src/server.rs)]

**Delete and restore.** MCP documentation says page deletion checkpoints the wiki before removing the file and its indexed versions; restore can recreate a page from a retained Git revision or version. Retention sweeps also remove eligible page files and indexes under configured rules. This review did not perform a deletion or verify erasure from backups or replicas. [[MCP operations](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-mcp/src/server.rs)] [[wiki mutation layer](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-wiki/src/wiki.rs)] [[architecture](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/docs/ARCHITECTURE.md)]

**Retrieval.** `memory_query` combines FTS5, entity matches, and linked-page neighbors with reciprocal-rank fusion; configured embeddings add a vector stream. The architecture docs describe an observation-evidence stream and bounded raw-observation fallback on non-global misses. Explain mode exposes stream ranks, score contributions, authority adjustment, and per-stream timings. This inspection did not execute a query or assess ranking quality. [[architecture](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/docs/ARCHITECTURE.md)] [[retrieval implementation](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/reader.rs)] [[MCP query](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-mcp/src/server.rs)]

Handoffs are typed session-continuity records separate from wiki pages. The README describes ownership and claim-once delivery. Ordinary search is project-scoped; explicit global search and cross-project messaging are designed to cross the project boundary, so they must be distinguished from project-isolated retrieval. [[README](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/README.md)] [[architecture](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/docs/ARCHITECTURE.md)]

## Scope isolation, provenance, and evidence

Observation and page records use workspace/project coordinates, and retrieval code applies the caller's readable-project filter. Handoffs additionally have ownership semantics. The explicit `global=true` retrieval option and directed cross-project messaging are intentional exceptions to ordinary project-scoped operations; no cross-scope probes were run. [[observation model](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-core/src/observation.rs)] [[retrieval implementation](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/reader.rs)] [[README](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/README.md)]

The immutable trust class differentiates operator-authored input, model-generated content, and tool results. A compiled page derives trust from the least-trusted contributing observation. The provenance reader exposes version-specific observation lineage and hides observations the caller is not authorized to read. This provides origin/lineage metadata; it does not prove claims are true or that retrieved answers include supporting external citations. [[trust model](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-core/src/trust.rs)] [[provenance reader](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/provenance.rs)]

## Source-visible efficiency and observability

The repository describes capture, search, and handoff as usable without a configured LLM, while vector search and provider-backed consolidation are optional. A single SQLite writer actor serializes mutations. Retrieval's explained path records per-stream elapsed times, and MCP metrics code exposes query latency and ingestion counters. These are source-visible design and instrumentation facts, not timings or throughput measured in this review. [[README](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/README.md)] [[writer actor](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/writer.rs)] [[retrieval implementation](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/reader.rs)] [[MCP metrics](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-mcp/src/metrics.rs)]

## Project metric domains

All comparison metric domains are **not measured** here. Source shows recall paths, versioning, deletion and scope controls, trust/provenance fields, and explain/latency instrumentation. This review collected no answerable recall or abstention scores; correction/stale-value, deletion-leak, scope-isolation, evidence-support, or citation-coverage adjudication; latency distributions; write-to-recall delay; token/cost totals; or storage measurements. The project-owned metric definitions, status record, and fixture describe the separate benchmark protocol. [[metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded read-only review of selected current documentation and Rust source at the verified SHA. It does not establish deployment reliability, retrieval quality, correction effectiveness, adversarial isolation, complete deletion across backups/replicas, or runtime performance. Trust lineage and source-observation links are not answer-level evidence adjudication. Unknown means not verified in this review. [[architecture](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/docs/ARCHITECTURE.md)] [[trust model](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-core/src/trust.rs)] [[provenance reader](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/provenance.rs)]

## Contact-list follow-up

I checked the official pinned README and SECURITY.md and the project website. They publish no contact email; the security policy directs reporters to the repository's security reporting process. The JSON record stores `contact_email: null` and the exact checked source URLs. No commit metadata, personal profile address, third-party directory, or inferred address was used. [[README](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/README.md)] [[SECURITY.md](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/SECURITY.md)] [[official project site](https://aimemory.sh/)]

## Benchmark status

**Benchmark not run.** No ai-memory runtime, benchmark workload, or tests were executed. Source observations above are not measured results. See the project metric definitions, benchmark status, and fixture for the separate evaluation protocol. [[metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical repository](https://github.com/akitaonrails/ai-memory)
- [Current main branch commits feed](https://github.com/akitaonrails/ai-memory/commits/main.atom)
- [Reviewed main branch head commit](https://github.com/akitaonrails/ai-memory/commit/ccc7dc0db1271e94785b3e7e5a1758a89fde202d)
- [README.md](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/README.md)
- [docs/ARCHITECTURE.md](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/docs/ARCHITECTURE.md)
- [DATA_HANDLING.md](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/DATA_HANDLING.md)
- [observation.rs](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-core/src/observation.rs)
- [trust.rs](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-core/src/trust.rs)
- [router.rs](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-hooks/src/router.rs)
- [wiki.rs](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-wiki/src/wiki.rs)
- [writer.rs](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/writer.rs)
- [reader.rs](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/reader.rs)
- [provenance.rs](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-store/src/provenance.rs)
- [MCP server](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-mcp/src/server.rs)
- [MCP metrics](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/crates/ai-memory-mcp/src/metrics.rs)
- [SECURITY.md](https://github.com/akitaonrails/ai-memory/blob/ccc7dc0db1271e94785b3e7e5a1758a89fde202d/SECURITY.md)
- [Official project site](https://aimemory.sh/)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and source attribution](../data/memory-systems.json)

**Verification boundary:** no ai-memory system, benchmark, or tests were run.
