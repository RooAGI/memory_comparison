# Artesian

## Identity and review pin

- **Curated position:** 71
- **Slug:** `artesian`
- **Listed repository:** [aquifer-labs/artesian](https://github.com/aquifer-labs/artesian)
- **Canonical repository:** [https://github.com/aquifer-labs/artesian](https://github.com/aquifer-labs/artesian)
- **Default branch:** `main`
- **Reviewed head:** [`14e4f2d9494d396695f79350b9e42bacd82d953d`](https://github.com/aquifer-labs/artesian/commit/14e4f2d9494d396695f79350b9e42bacd82d953d)
- **Reviewed:** 2026-11-24 21:39:38 UTC (13:39:38 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/artesian.md), used only for identity, listed locator and source attribution.

The curated roster places Artesian at ordinal 71 with slug `artesian` and listed locator `https://github.com/aquifer-labs/artesian`. The official repository page identifies `main` as the default branch and shows latest commit prefix `14e4f2d`; the official main commit feed gives full head `14e4f2d9494d396695f79350b9e42bacd82d953d`. Review links to upstream files below pin to that SHA.[[catalog](../data/memory-systems.json)] [[repo](https://github.com/aquifer-labs/artesian)] [[feed](https://github.com/aquifer-labs/artesian/commits/main.atom)] [[head](https://github.com/aquifer-labs/artesian/commit/14e4f2d9494d396695f79350b9e42bacd82d953d)]

## Summary

Artesian is a Rust memory and context-control system for agents. Its aquifer crate provides durable memory backends and retrieval; the optional headgate layer qualifies what enters a bounded working context. This review describes pinned source and documentation, not runtime behavior.[[readme](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/README.md)] [[architecture](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/architecture.md)]

## Who and what

The repository is published under the aquifer-labs GitHub organization. It describes Artesian as a local-first, open-source Rust context governor and provides a composable library, CLI and optional daemon, plus an MCP integration. The repository presents a self-hosted tool, not a hosted memory service.[[repo](https://github.com/aquifer-labs/artesian)] [[readme](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/README.md)]

## Architecture and data model

**Code and documentation observations.** The architecture separates durable long-term memory from the bounded committed context held by an agent. The `aquifer` crate defines memory backends and vector-store adapters; `headgate` provides the optional qualify gate and bounded committed state; `artesian-mcp` exposes tools, and the CLI/daemon provide local entry points. Traits keep the memory, store, gate and agent seams replaceable.[[architecture](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/architecture.md)]

A `MemoryRecord` contains an id, drill-down `node_id`, content, tags, metadata, tier and creation time. Optional fields represent scope and agent/session/task ownership, with additional source, author, confidence, lifecycle, relation and access-utility data. The stable ID hashes content, tier and supplied node/scope/owner values, so repeated content with the same identity can deduplicate.[[types](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/types.rs)] [[identity](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/identity.rs)]

The memory guide describes Markdown “headwater” files as the readable source of truth and vector/search indexes as rebuildable projections. The vector path uses multilingual-e5-small embeddings and supports Files, sqlite-vec and Qdrant backends. The documented embedding dimension is 384.[[memory](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/memory.md)] [[vector_memory](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/vector_memory.rs)]

The guide describes deterministic chunking and small-to-big retrieval: rank a small matching chunk, then return surrounding sibling chunks within a bounded context budget. Reranking, entity and temporal signals, HyDE, multi-query and consolidation are optional stages; options that use an LLM are off by default.[[memory](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/memory.md)] [[retrieval](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/retrieval.rs)]

## Write, update, delete, and retrieval

**Writes.** The shared `MemoryBackend` contract provides `store` and `bulk_store`. Its default bulk implementation loops over individual stores; specialized backends can batch. The concurrency guide describes append-mostly, content-hash-idempotent writes, which avoid a shared read-modify-write on each point.[[backend](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/backend.rs)] [[identity](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/identity.rs)] [[concurrency](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/concurrency.md)]

**Updates and deletion.** The record state enum includes Active, Archived and Retracted. The backend contract exposes `retract` separately from hard deletion and recommends retaining an auditable retraction/supersession record. The memory documentation describes explicit `node_id` drill-down and rebuild from headwater files. I did not inspect every backend-specific hard-delete path, so this review does not establish erasure completeness.[[types](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/types.rs)] [[backend](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/backend.rs)] [[memory](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/memory.md)]

**Retrieval.** The contract exposes `find`, `hybrid_rrf` and deterministic `get_node`. The documented vector path combines keyword and dense rankings with Reciprocal Rank Fusion (default rank constant 60) and cosine vector similarity. Chunk hits can expand to parent context within a configured bound; direct node lookup preserves a path to the stored record.[[backend](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/backend.rs)] [[memory](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/memory.md)] [[retrieval](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/retrieval.rs)]

**Short-term state.** The memory guide describes in-process buffer and sliding-window modes that add no LLM call by default. A session anchor plus targeted recall is the documented self-repair path after compaction; summary/consolidation paths are opt-in.[[memory](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/memory.md)]

## Scope isolation

The concurrency guide describes project-per-collection separation, then payload filters for scope classes (shared, agent, session and task) and owner fields such as user ID. It describes shared records as visible to workers in a project and per-user collections as an optional stricter configuration. The file backend has project-union matching in its source. These are architecture and implementation observations; this review did not test all backends, authentication, or caller-to-filter enforcement.[[concurrency](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/concurrency.md)] [[files](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/files.rs)] [[types](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/types.rs)]

## Provenance and evidence

Records provide source and author fields, confidence, creation time, metadata, relations and a stable node handle for retrieving the underlying record. The documentation also describes an append-only qualify decision log for the bounded committed-state layer. These structures can retain provenance and decision context, but this review found no adjudicated measure of evidence support or claim-level citation coverage.[[types](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/types.rs)] [[memory](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/memory.md)] [[architecture](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/architecture.md)]

## Source-visible efficiency and observability

**Code observations, not measurements.** Source structure shows deterministic content hashing, batched bulk writes where supported, rank fusion, local embedding, and bounded context expansion. The concurrency guide describes Qdrant as the parallel multi-writer option, sqlite-vec as WAL with serialized writers, and Files as a single-writer local backend. A local embedder is loaded lazily and shared by process through the documented implementation; resource use still depends on configuration and workload.[[identity](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/identity.rs)] [[backend](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/backend.rs)] [[concurrency](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/concurrency.md)] [[vector_memory](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/vector_memory.rs)]

The repository documents token and retrieval metrics, a `tokens` command, performance diagnostics and a gauge evaluation harness. The committed benchmark guide reports roughly 876–1,046 context tokens per query across its 13k-to-1M-token scaling tiers, with all answer documents retrieved in those cases. These are upstream-reported results and source observations; this review did not rerun them.[[readme](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/README.md)] [[benchmarks](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/benchmarks/README.md)]

## Metric-domain evidence

All domains below are **unmeasured for this review**. The evidence column describes source-visible mechanisms or gaps only.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Vector/keyword retrieval, fusion and a regression harness are documented. No answerable or unanswerable probe was run. | Unmeasured |
| Correction accuracy and stale-value rate | Lifecycle states and optional temporal supersession are described. No correction sequence was adjudicated. | Unmeasured |
| Deletion leakage | Retraction is a separate operation from hard deletion; no deletion or post-delete probes were run. | Unmeasured |
| Scope isolation | Project collections and payload filters are described; no cross-scope probes or auth checks were run. | Unmeasured |
| Evidence support and citation coverage | Source fields and node drill-down are available; no claim-support or citation-coverage adjudication was performed. | Unmeasured |
| Retrieval latency and write-to-recall delay | Embedding, batch writes and backend consistency options are visible; no timing data was collected. | Unmeasured |
| Tokens, cost and persistent storage | Upstream token results are reported in the benchmark guide; this review collected no token, cost or corpus-attributed storage measurements. | Unmeasured |

The [project metric definitions](../METRICS.md), [versioned benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) define proposed workloads and reporting. Their fixture cases are not Artesian measurements.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded read-only inspection of selected documentation and code at the reviewed commit. It does not establish retrieval quality, threshold calibration, durability, concurrency behavior, deletion completeness, security isolation, latency, cost, or storage efficiency.[[architecture](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/architecture.md)] [[concurrency](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/concurrency.md)] [[metrics](../METRICS.md)]

The concurrency guide describes project-level collection boundaries and payload-filtered scope boundaries, with optional per-user collections for stricter separation. This review did not verify every backend predicate, authentication setup, or enforcement of caller identity.[[concurrency](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/concurrency.md)] [[security](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/SECURITY.md)]

The upstream benchmark guide says its retrieval/token comparison does not establish end-to-end answer quality, and results apply to its fixtures and setup. Its numbers are not reproduced here.[[benchmarks](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/benchmarks/README.md)]

## Contact-list follow-up

I checked only official project documentation: the pinned [README](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/README.md) and [SECURITY.md](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/SECURITY.md). The README directs users to GitHub Issues and Discussions; the security policy requests private vulnerability reports. Neither publishes a contact email, so the JSON record stores `contact.email: null` and lists both exact checked URLs.

## Benchmark status

**Benchmark not run.** No Artesian runtime, benchmark workload, build, or tests were run for this review. The pinned upstream benchmark guide reports results for its own published retrieval/token workloads; those are source-reported upstream results, not measurements produced by this review. Project metric definitions and fixture links describe the local comparison protocol, and the execution-status record is not an Artesian result.[[benchmarks](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/benchmarks/README.md)] [[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[status](../results/initial-baselines-status.json)]

## Sources

- [Curated roster entry](../data/memory-systems.json) — ordinal, slug, listed repository, and Atlas attribution only.
- [Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/artesian.md) — identity and listed-locator attribution only; no assessment claims.
- [Official repository](https://github.com/aquifer-labs/artesian)
- [Official main branch feed](https://github.com/aquifer-labs/artesian/commits/main.atom)
- [Reviewed upstream head](https://github.com/aquifer-labs/artesian/commit/14e4f2d9494d396695f79350b9e42bacd82d953d)
- [README](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/README.md)
- [Architecture](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/architecture.md)
- [Memory architecture](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/memory.md)
- [Concurrency guide](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/docs/concurrency.md)
- [Memory types](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/types.rs)
- [Stable IDs](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/identity.rs)
- [Backend contract](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/backend.rs)
- [Vector memory](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/vector_memory.rs)
- [Headwater file backend](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/files.rs)
- [Reranking](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/crates/aquifer/src/retrieval.rs)
- [Security policy](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/SECURITY.md)
- [Upstream benchmark guide](https://github.com/aquifer-labs/artesian/blob/14e4f2d9494d396695f79350b9e42bacd82d953d/benchmarks/README.md)
- [Metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Initial execution status](../results/initial-baselines-status.json)

**Verification boundary:** source review only; no Artesian execution, benchmark, build, or tests.
