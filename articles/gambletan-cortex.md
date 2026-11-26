# Cortex (gambletan)

## Identity and review pin

- Catalog ordinal: 158
- System: Cortex (gambletan)
- Slug: gambletan-cortex
- Listed repository: https://github.com/gambletan/cortex
- Roster attribution: explicit repository locator; the pinned Atlas entry below is recorded only for curated identity and locator context, not as assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/gambletan-cortex.md)).
- Canonical upstream: https://github.com/gambletan/cortex
- Default branch: main
- Reviewed full head: [de02006c7e81f8955ddc25489440f73cd829492e](https://github.com/gambletan/cortex/commit/de02006c7e81f8955ddc25489440f73cd829492e)
- Review timestamp: 2026-11-25T09:34:33Z (UTC; 2026-11-25 01:34:33 PST, America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub identifies main as the repository default branch. Its current main commit endpoint returned de02006c7e81f8955ddc25489440f73cd829492e; the repository page shows the same abbreviated head. The commit is dated 2026-10-22T21:24:43Z. ([repository](https://github.com/gambletan/cortex), [main head](https://api.github.com/repos/gambletan/cortex/commits/main), [head commit](https://github.com/gambletan/cortex/commit/de02006c7e81f8955ddc25489440f73cd829492e))

## Summary

Cortex is a local-first Rust memory engine and MCP server. Its core model stores typed memories in episodic, semantic, working, procedural, and archived tiers; it combines an embedded vector index and several retrieval signals, with optional sync and a separately controlled sharing gateway. The upstream README describes these capabilities and its performance claims; this review did not reproduce them. ([README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md), [memory types](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/types.rs))

## Who and what

The official README describes a local memory engine for personal AI agents, distributed as a Rust workspace with an MCP server and additional HTTP, Python, WebAssembly, and agent-plugin interfaces. The local SQLite store is the documented default; PostgreSQL and hosted sharing/sync paths are optional integrations. ([README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md))

## Architecture and data model

The workspace separates the core memory logic, storage and in-memory index, MCP server, HTTP API, Python bindings, WebAssembly build, sync, and plugins. The README documents a local SQLite store and an in-memory vector index; it also documents optional PostgreSQL storage. SQLite storage uses WAL mode, separate write and read connections, a four-connection read pool, and bounded LRU caches for memory objects and entity-query results. ([README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md), [SQLite storage](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/storage/sqlite.rs))

A MemObject has a tier, typed content, optional embedding, event and ingestion times, access data, salience, source metadata, privacy level, links, tags, metadata, an optional content hash, and an optional namespace. Content variants include text, subject-predicate-object facts, preferences, relationships, patterns, and events. MemSource records a channel and optional identity, chat, thread, and message identifiers. ([memory types](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/types.rs))

## Write, update, delete, and retrieval

**Write.** EpisodeStore.add builds an episodic MemObject from content and MemSource, applies a salience hint and optional embedding, stores it, and inserts the embedding into the memory index when supplied. SemanticStore.add_fact similarly builds and stores a typed fact. The MCP tool surface includes memory_ingest and memory_ingest_batch; the source defines a 100 KB single-memory text cap and a 100-item batch cap. ([episode store](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/episode.rs), [semantic store](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/semantic.rs), [MCP tools](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-mcp-server/src/tools.rs))

**Correction and updates.** The semantic store exposes confidence updates for preferences. Its merge_facts operation adds a Supersedes link from the replacement to the old fact and multiplies the old fact's base salience by 0.3; it retains the old object rather than replacing its content in place. The README also describes archive and restore tools. ([semantic store](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/semantic.rs), [MCP tools](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-mcp-server/src/tools.rs), [README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md))

**Delete and archive.** The storage contract defines delete_memory, and the MCP tool description calls memory_delete a permanent delete by ID. Consolidation archives low-salience episodic memories instead of deleting them and removes their IDs from the active vector index. This bounded review did not trace every storage deletion, derived-record cleanup, or filesystem/WAL behavior, so it does not establish complete physical erasure. ([storage contract](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/storage/traits.rs), [MCP tools](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-mcp-server/src/tools.rs), [consolidation](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/consolidation.rs))

**Retrieval.** Retrieval queries can carry text, an optional embedding, channel, person, namespace, time context, limit, and work budget. The default budget caps gathered candidates at 10,000 and expansion at 250 ms. The README describes ranking with vector similarity, temporal weighting, salience, social and channel signals, full-text search, and frecency; its SQLite and PostgreSQL paths use different fusion strategies. These are implementation and documentation observations, not measured quality or speed. ([retrieval](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/retrieval.rs), [README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md))

## Scope isolation

Namespace is an optional field on each memory and an optional caller-supplied filter on search. Context generation filters semantic memories by namespace and uses a namespace-filtered episode query when no channel is selected; when a channel is selected, it instead lists recent memories by channel. Semantic fact and preference query APIs do not take a namespace. The README recommends separate database files for physical project isolation. These code paths mean callers should not treat an omitted namespace, channel-based context, or the general semantic query APIs as enforced isolation. Privacy levels instead govern sync eligibility; they are not a per-caller authorization boundary in the inspected types. ([memory types](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/types.rs), [retrieval](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/retrieval.rs), [context generation](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/context.rs), [semantic store](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/semantic.rs), [README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md))

## Provenance and evidence

MemSource preserves channel, identity, chat, thread, and message identifiers. Semantic facts can be linked through typed relations such as Supersedes, while source text and structured content remain separate fields. The inspected model does not define a required source span or citation record for every claim, and source identifiers alone do not verify the claim's truth. The README describes local reference-resolution grading as structural checking rather than independent fact verification. ([memory types](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/types.rs), [semantic store](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/semantic.rs), [README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md))

## Efficiency and observability

The source exposes a candidate and time budget for retrieval. SQLite uses WAL, a read pool, and LRU caches, while the README describes bounded context generation and distinct SQLite/PostgreSQL retrieval paths. The README also publishes upstream benchmark figures, including sub-millisecond operations, but their hardware/configuration and version boundaries are not measurements from this review. No runtime timings, resource use, token counts, charges, or storage measurements were collected. ([retrieval](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/retrieval.rs), [SQLite storage](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/storage/sqlite.rs), [README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md))

## Metric-domain evidence

All project benchmark metrics for Cortex are **unmeasured**. Source and documentation inspection does not establish benchmark outcomes. ([metric definitions](../METRICS.md), [execution status](../results/initial-baselines-status.json), [fixture, not run](../fixtures/memory-benchmark-v1.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Multiple ranking signals and query limits are implemented; no answerable or unanswerable probes were adjudicated. |
| Correction accuracy and stale-value rate | Unmeasured | A supersedes link and salience reduction are implemented; no correction workload was run. |
| Deletion leakage | Unmeasured | A delete tool/API is exposed; no accepted delete or post-delete probes were run. |
| Scope isolation | Unmeasured | Optional namespace filters exist, with documented code-path caveats above; no cross-scope workload was run. |
| Evidence support and citation coverage | Unmeasured | Channel and message provenance fields exist; no claim-support or citation workload was scored. |
| Retrieval latency | Unmeasured | No timing samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write/recall probes were run. |
| Tokens and cost | Unmeasured | No model usage or charges were collected. |
| Storage efficiency | Unmeasured | No corpus-attributed persistent storage measurement was collected. |

The upstream README includes benchmark claims with a stated system/version and setup; those claims are not re-run here and are not results for this project's comparison protocol. ([README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md))

## Limits and unknowns

This is a bounded source review of the official README, core data types, episode and semantic stores, retrieval/query configuration, context generation, storage contract and SQLite implementation, consolidation, MCP tool surface, and security policy. The listed repository and its current head were verified on GitHub; the review used official SHA-pinned source pages, not a local checkout. The review did not inspect every database operation, inference path, PostgreSQL adapter, sync path, plugin, or deployment configuration. The overview file docs/architecture.md is absent at the reviewed head. ([README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md), [context generation](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/context.rs), [storage contract](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/storage/traits.rs), [checked architecture path](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/docs/architecture.md))

No Cortex runtime, tests, or benchmarks were run. This review therefore does not establish operational correctness, answer quality, abstention behavior, deployed scope isolation, complete erasure, latency, write-to-recall delay, token or cost totals, or storage efficiency. It also does not establish that each host configures namespaces or separate databases as recommended. ([metric definitions](../METRICS.md), [execution status](../results/initial-baselines-status.json))

## Contact

No contact email was published in the checked official README or SECURITY.md. The README directs support to GitHub Issues; the security policy says to report through GitHub Issues or contact maintainers directly, without publishing an email address. No profile or commit metadata or third-party directory was used. ([README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md), [SECURITY.md](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/SECURITY.md))

## Benchmark status

**Benchmark not run.** Cortex, its tests, and benchmark workloads were not run. The shared execution-status record contains no Cortex result; its fixture counts describe planned probes, not outcomes. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/gambletan-cortex.md)
- [Official GitHub repository](https://github.com/gambletan/cortex)
- [Official main head endpoint](https://api.github.com/repos/gambletan/cortex/commits/main)
- [Reviewed full head](https://github.com/gambletan/cortex/commit/de02006c7e81f8955ddc25489440f73cd829492e)
- [Pinned README](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/README.md)
- [Pinned memory types](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/types.rs)
- [Pinned episode store](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/episode.rs)
- [Pinned semantic store](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/semantic.rs)
- [Pinned retrieval](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/retrieval.rs)
- [Pinned context generation](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/context.rs)
- [Pinned storage contract](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/storage/traits.rs)
- [Pinned SQLite storage](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/storage/sqlite.rs)
- [Pinned consolidation](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-core/src/consolidation.rs)
- [Pinned MCP tools](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/cortex-mcp-server/src/tools.rs)
- [Pinned security policy](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/SECURITY.md)
- [Checked architecture documentation path](https://github.com/gambletan/cortex/blob/de02006c7e81f8955ddc25489440f73cd829492e/docs/architecture.md)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
