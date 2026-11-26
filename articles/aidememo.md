# AideMemo source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 41 / AideMemo / aidememo  
**Listed repository locator:** [taeyun16/aidememo](https://github.com/taeyun16/aidememo)  
**Current canonical repository:** [taeyun16/aidememo](https://github.com/taeyun16/aidememo)  
**Default branch / reviewed head:** main / 60ad69a6dc679b628e27abc91591af1e2afb8be2  
**Review time:** 2026-11-24 19:51:37 UTC (11:51:37 PST; America/Los_Angeles).

## Identity and scope

The curated catalog identifies AideMemo at ordinal 41, with the listed repository locator above and an attribution source at Atlas revision `19199a4fc249e89c0793be06f0b166b358089ba0`. I used the catalog and Atlas link only to record identity and attribution; their descriptions and marks were not assessment evidence. The official GitHub repository page identifies `main` as the default branch, and its official main branch feed identifies the current head as `60ad69a6dc679b628e27abc91591af1e2afb8be2`.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/taeyun16/aidememo)] [[main branch feed](https://github.com/taeyun16/aidememo/commits/main.atom)] [[reviewed head patch](https://github.com/taeyun16/aidememo/commit/60ad69a6dc679b628e27abc91591af1e2afb8be2.patch)]

AideMemo is a Rust memory library and agent integration toolkit. Its README presents typed facts, entity relations, and temporal history behind a local-first store, with CLI, MCP, SDK, and native bindings. The source and documentation observations below are tied to the reviewed revision; they are not measurements.[[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)]

## Architecture and data model

The README describes a local-first embedded-store design. Current README identifies SQLite as the default and redb as an optional feature. The inspected redb implementation contains entity, relation, fact, and metadata tables; name and fact-by-entity lookup indexes; and a source-aware exact-content hash index.[[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)] [[store.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/store.rs)]

Facts are typed records linked to entities and may carry tags, source namespace, confidence, created/updated and observed timestamps, access fields, and supersession state. Entities use canonical ULID identifiers, with names and aliases serving lookup. Relations are directed and typed, and their input can include namespace, weight, and evidence.[[types.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/types.rs)]

The Markdown ingest path walks `.md` files, parses frontmatter, extracts wikilinks and heading-based facts, and writes graph objects and facts. Relation extraction uses bounded, deterministic phrase matching between neighboring wikilinks; it preserves the matched source phrase as evidence. The current `incremental` parameter is documented in code as equivalent to a full ingest.[[ingest.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/ingest.rs)] [[relations.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/relations.rs)]

## Write, update, delete, and retrieval

**Write.** The README and core types describe explicit typed writes through the CLI, MCP, SDK, and bindings, along with Markdown ingestion. Inputs can specify fact type, entities, tags, namespace, confidence, and observation time. Exact-content deduplication is source-aware. Optional privacy filtering and model-based extraction or embedding are distinct opt-in paths.[[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)] [[types.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/types.rs)] [[store.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/store.rs)]

**Update and correction.** The README exposes fact editing and supersession. Records include updated and observed timestamps plus a supersession marker; retrieval can request current-only facts or an as-of time. These are temporal controls in source, not evidence of correction accuracy for arbitrary caller paths.[[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)] [[types.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/types.rs)] [[search.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/search.rs)]

**Delete.** The README lists a fact-delete command. This inspection does not establish physical erasure from backups, archives, replicas, prior exports, or all derived indexes. Deletion leakage was not tested.[[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)]

**Retrieval.** The README describes BM25-first retrieval, with optional semantic or hybrid paths. The inspected search engine reuses a caller-owned BM25 cache, rebuilding it when marked dirty; it applies confidence, entity, source namespace, time-window, as-of, and current-only filters before ranking. Graph APIs provide namespace-aware traversal and path search. This source review does not establish answerable recall or calibrated abstention.[[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)] [[search.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/search.rs)] [[graph.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/graph.rs)]

## Scope isolation and provenance

Local MCP and SDK interfaces can pass a `source_id`; an installed environment default is a convenience rather than an authorization boundary if callers can override tool arguments. For shared HTTP MCP, the README documents bearer-token bindings that inject source and actor identity and reject caller overrides. The README also notes entity names/types are shared across source partitions, and recommends separate stores for mutually untrusted tenants. Those are deployment-dependent boundaries, not a guarantee across every local interface.[[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)] [[mcp_tools.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-cli/src/cmd/mcp_tools.rs)] [[graph.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/graph.rs)]

Fact source, source confidence, observation/record timestamps, entity links, and session context can preserve provenance; relation records can retain evidence text. Actor identity is available at integrations. These fields support traceability but do not prove the fact is true or that a source supports a generated claim.[[types.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/types.rs)] [[relations.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/relations.rs)] [[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)]

## Source-visible efficiency and observability

**Code and documentation observations.** The BM25 search engine holds a reusable inverted-index cache and rebuilds only after it is marked dirty. It fetches a bounded candidate set before applying result filters. The README documents daemon mode to keep the store and optional models warm, plus stats, doctor, and bench commands. Store opening has debug tracing instrumentation. These facts describe implementation and available tools; they do not establish latency, throughput, or resource use.[[search.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/search.rs)] [[store.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/store.rs)] [[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)]

## Metric domains

All project benchmark domains remain **unmeasured for this review**. No workload was run for answerable recall or abstention, correction and stale values, deletion leakage, scope leakage, evidence support or citation coverage, latency, write-to-recall delay, token or dollar cost, or storage efficiency. The project metric definitions and fixture specify the protocol; the execution status record remains `not_run`. These project artifacts are not results for AideMemo.[[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This bounded source review inspected the official README and selected current core types, ingestion, relation, search, store, graph, and MCP source at the verified SHA. The system, tests, and benchmark workloads were not run. Answer quality, deployed authorization, physical deletion completeness across all storage/export paths, and performance remain unverified. Unknown here means not established by this inspection, not absent.[[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)] [[store.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/store.rs)] [[mcp_tools.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-cli/src/cmd/mcp_tools.rs)]

## Contact-list follow-up

The official repository `SECURITY.md` publishes `taeyun16@pm.me` for vulnerability reports. The official README and `SUPPORT.md` were also checked; SUPPORT directs general questions to GitHub Discussions and publishes no email. The contact recorded here is the published security-report email, not an inferred or profile-derived address.[[SECURITY.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/SECURITY.md)] [[SUPPORT.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/SUPPORT.md)] [[README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)]

## Benchmark status

**Benchmark not run.** No AideMemo runtime, test suite, or benchmark workload was run. Source and documentation observations are not measured results. See the project metric definitions, status record, and fixture for the separate benchmark protocol.[[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical GitHub repository](https://github.com/taeyun16/aidememo)
- [Official main branch commit feed](https://github.com/taeyun16/aidememo/commits/main.atom)
- [Reviewed full main head patch](https://github.com/taeyun16/aidememo/commit/60ad69a6dc679b628e27abc91591af1e2afb8be2.patch)
- [README.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/README.md)
- [crates/aidememo-core/src/types.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/types.rs)
- [crates/aidememo-core/src/ingest.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/ingest.rs)
- [crates/aidememo-core/src/relations.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/relations.rs)
- [crates/aidememo-core/src/search.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/search.rs)
- [crates/aidememo-core/src/store.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/store.rs)
- [crates/aidememo-core/src/graph.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-core/src/graph.rs)
- [crates/aidememo-cli/src/cmd/mcp_tools.rs](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/crates/aidememo-cli/src/cmd/mcp_tools.rs)
- [SECURITY.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/SECURITY.md)
- [SUPPORT.md](https://github.com/taeyun16/aidememo/blob/60ad69a6dc679b628e27abc91591af1e2afb8be2/SUPPORT.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status record](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and attribution](../data/memory-systems.json)
- [Roster attribution source (identity only)](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/aidememo.md)

**Verification boundary:** no AideMemo system, tests, or benchmarks were run.
