# cortex-engine

## Identity and review pin

- Catalog ordinal: 162
- System: cortex-engine
- Slug: `cortex-engine`
- Listed repository: https://github.com/fozikio/cortex-engine
- Roster attribution: the catalog lists an explicit repository locator; the pinned Atlas roster entry is used only for identity and locator context, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortex-engine.md)).
- Canonical upstream: https://github.com/Fozikio/cortex-engine
- Default branch: `master`
- Reviewed full head: [158c372b6c8ba60406ae84a2de6c143833ccdfd6](https://github.com/Fozikio/cortex-engine/commit/158c372b6c8ba60406ae84a2de6c143833ccdfd6)
- Review timestamp: 2026-11-25T09:44:25Z (UTC; 2026-11-25 01:44:25 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

The official GitHub API identifies the public, non-fork repository and `master` as its default branch. The branch endpoint reports head `158c372b6c8ba60406ae84a2de6c143833ccdfd6`, timestamped 2026-11-23T17:18:04Z. ([repository metadata](https://api.github.com/repos/Fozikio/cortex-engine), [default-branch head](https://api.github.com/repos/Fozikio/cortex-engine/commits/master))

## Summary

cortex-engine is a TypeScript cognitive-memory engine and MCP server for AI agents. It separates observations from formed memories, records belief revisions, and uses semantic, lexical and graph-based retrieval. SQLite is the local default; Firestore and JSON backends are also documented. This review is based on current pinned source and documentation, not a runtime evaluation. ([README](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/README.md), [core types](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/core/types.ts), [storage guide](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/storage-backends.md))

## Who and what

The repository is published under the Fozikio organization. Its README describes an LLM-agnostic engine that can run locally or in a cloud setup, exposing cognitive tools through MCP. The README and security policy were checked for contact information; neither publishes an email. ([repository metadata](https://api.github.com/repos/Fozikio/cortex-engine), [README](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/README.md), [security policy](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/SECURITY.md))

## Architecture and data model

The TypeScript package divides core contracts, cognitive engines, storage adapters, MCP tools, namespace management, providers and REST serving. The storage-agnostic model distinguishes long-lived memories, pending observations, belief-revision records, and edges between memories. A memory can carry a definition, category, salience, confidence, tags, source files, embedding, FSRS scheduling state, provenance metadata and an origin marker. Edges hold a relation, weight and evidence text. ([README](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/README.md), [core types](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/core/types.ts), [store contract](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/core/store.ts))

SQLite is the default backend. Firestore is described for cloud and multi-process deployments; JSON supports snapshots, migration and inspection. SQLite stores embeddings as float blobs and uses brute-force cosine search. The backend guide recommends it for stores below about 10,000 memories; that is project documentation, not a measured result from this review. ([storage guide](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/storage-backends.md), [SQLite store](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/stores/sqlite.ts))

## Write, update, delete, and retrieval

**Write.** The `observe` tool embeds an input, scores salience, checks nearby memories against namespace similarity thresholds, and optionally checks a nearby candidate for contradiction when an NLI provider is configured. It can create a high-salience novel memory immediately; other observations remain queued for consolidation. A contradiction or superseding observation is kept separately and represented with a signal instead of being merged into the old memory. Callers may supply a source file and section. ([observe](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/observe.ts), [core types](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/core/types.ts))

**Update.** The `believe` tool embeds a replacement definition and atomically writes a belief-history row with the old definition, new definition, reason, system timestamp and optional valid-time start before updating the live memory. The transaction keeps the revision record and current value together. ([believe](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/believe.ts), [concurrency guide](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/concurrency.md))

**Delete.** The `forget` tool is explicitly a fade operation: it lowers salience, marks the memory faded and reschedules it through FSRS. It does not delete the record. The typed `CortexStore` interface has no delete-memory method, although it supports deleting generic collection documents; the reviewed public tool references do not document a complete memory-erasure operation. ([forget](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/forget.ts), [store contract](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/core/store.ts), [tools reference](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/tools-reference.md))

**Retrieval.** `query` can expand a query with HyDE, combine nearest-vector results with lexical full-text hits, spread activation over graph edges, then rank using similarity, FSRS retrievability and salience. It filters by minimum score/category and returns a bounded list. `retrieve` fetches by ID or runs plain vector search; `recall` lists recent observations chronologically. The query path updates access/retrieval metadata for results. ([query](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/query.ts), [retrieve](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/retrieve.ts), [tools reference](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/tools-reference.md))

## Scope isolation

The namespace manager creates a separate store per configured namespace. A wrapper prefixes generic collection names, while typed memories and observations are delegated to that namespace’s store. The multi-agent design makes a namespace the default for an agent and documents cross-namespace queries as explicit; query_cross reads only namespaces marked queryable. These are application-level routing controls. The reviewed source does not establish caller authentication or prevent a caller with tool access from selecting another namespace. SQLite is documented as single-process per database file; clients that share a local store should use one server process. ([namespace manager](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/namespace/manager.ts), [scoped store](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/namespace/scoped-store.ts), [multi-agent design](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/multi-agent-design.md), [concurrency guide](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/concurrency.md))

## Provenance, evidence, and observability

Observation records can preserve source file/section and optional model provenance. Memory records can carry model provenance and origin; graph edges carry an evidence string; belief revisions store the reason for a change. These fields add context, but the reviewed contracts do not establish immutable source-document lineage or claim-level citations. ([core types](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/core/types.ts), [observe](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/observe.ts), [believe](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/believe.ts))

The `feedback` tool adjusts confidence by a small positive amount for helpful results and a larger negative amount for unhelpful results, then logs the event for retrieval audits. The `dream` tool records phase counts, duration, integration rate and failures after a successful run. These are operational traces and heuristics; this review did not run a store or collect telemetry. ([feedback](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/feedback.ts), [dream](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/dream.ts))

## Efficiency and limitations

Retrieval can fan out over vector, lexical and graph paths. SQLite search is brute-force cosine; the storage guide presents Firestore native vector search for larger or distributed use. Dream consolidation may call configured LLM and embedding providers, and automatic Phase A processing is asynchronous and best-effort. The observed design implies multiple retrieval and provider operations, but no latency, cost, token or storage result was measured. ([query](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/query.ts), [storage guide](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/storage-backends.md), [automatic consolidation](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/engines/auto-consolidate.ts))

## Metric-domain evidence

All benchmark domains are **unmeasured** for cortex-engine. Source-level behavior and backend documentation are not benchmark results. ([metric definitions](../METRICS.md), [fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable recall and abstention | Unmeasured | Hybrid ranking is implemented; no adjudicated probes were run. |
| Correction accuracy and stale-value rate | Unmeasured | Belief revisions and retrieval feedback exist; no correction workload was measured. |
| Deletion leakage | Unmeasured | The public forget path fades records; no deletion or erasure probes were run. |
| Scope isolation | Unmeasured | Namespaces and opt-in cross-reads exist; no isolation workload was run. |
| Evidence support and citation coverage | Unmeasured | Source/provenance fields exist; no claim-level citation assessment was run. |
| Retrieval latency and write-to-recall delay | Unmeasured | No timed probes were run. |
| Tokens and cost | Unmeasured | No provider usage or charges were collected. |
| Storage efficiency | Unmeasured | No corpus-attributed storage size was measured. |

## Limits and unknowns

This bounded review covered the official README, core model/store contracts, selected memory tools, namespace code, SQLite implementation and backend/concurrency documentation. It did not inspect every engine, backend, service route, provider or deployment setup. The code review does not establish runtime correctness, the quality of model-generated decisions, deployed namespace authorization, full erasure, or benchmark performance. ([README](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/README.md), [core types](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/core/types.ts), [security policy](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/SECURITY.md))

No cortex-engine runtime, tests or benchmarks were run. The project fixture is a workload specification only. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

## Contact

The official pinned README and SECURITY.md were checked. Neither publishes a contact email. No commit/profile metadata or third-party directory was used. ([README](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/README.md), [SECURITY.md](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/SECURITY.md))

## Benchmark status

**Benchmark not run.** No cortex-engine runtime, tests or benchmark workload was executed. The project fixture describes a workload and is not a measured result. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortex-engine.md)
- [Official GitHub repository API](https://api.github.com/repos/Fozikio/cortex-engine)
- [Verified default-branch head](https://api.github.com/repos/Fozikio/cortex-engine/commits/master)
- [Pinned official README](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/README.md)
- [Pinned core memory types](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/core/types.ts)
- [Pinned storage contract](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/core/store.ts)
- [Pinned observe tool](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/observe.ts)
- [Pinned query tool](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/query.ts)
- [Pinned belief revision tool](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/believe.ts)
- [Pinned forget tool](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/forget.ts)
- [Pinned SQLite store](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/stores/sqlite.ts)
- [Pinned namespace manager](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/namespace/manager.ts)
- [Pinned scoped store](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/namespace/scoped-store.ts)
- [Pinned dream tool](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/dream.ts)
- [Pinned automatic consolidation](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/engines/auto-consolidate.ts)
- [Pinned retrieval feedback tool](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/src/tools/feedback.ts)
- [Pinned storage backend documentation](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/storage-backends.md)
- [Pinned concurrency documentation](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/concurrency.md)
- [Pinned multi-agent design](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/multi-agent-design.md)
- [Pinned tools reference](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/docs/tools-reference.md)
- [Pinned security policy checked for contact](https://github.com/Fozikio/cortex-engine/blob/158c372b6c8ba60406ae84a2de6c143833ccdfd6/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution status](../results/initial-baselines-status.json)

---
