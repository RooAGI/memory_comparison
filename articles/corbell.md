# Corbell source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 153 / Corbell / corbell  
**Listed repository locator:** [Corbell-AI/Corbell](https://github.com/Corbell-AI/Corbell)  
**Current canonical repository:** [Corbell-AI/Corbell](https://github.com/Corbell-AI/Corbell)  
**Default branch / reviewed head:** main / `75c7b20ac95292185b5fef6a4680e3e10de9da66`  
**Review time:** 2026-11-25 09:14:37 UTC (01:14:37 PST; America/Los_Angeles).

## Identity and scope

The curated roster places Corbell at ordinal 153, slug `corbell`, with listed repository locator `https://github.com/Corbell-AI/Corbell` and an Atlas attribution pinned to revision `19199a4fc249e89c0793be06f0b166b358089ba0). That catalog entry is used only for identity and locator context. GitHub identifies the public canonical repository and default branch `main`; its official main commits Atom feed reports full head `75c7b20ac95292185b5fef6a4680e3e10de9da66`, updated 2026-05-23T20:32:59Z. The repository page's latest-commit marker and the full commit page agree with that head. This review inspected SHA-pinned GitHub source and documentation pages at that revision.[[catalog roster](../data/memory-systems.json)] [[repository](https://github.com/Corbell-AI/Corbell)] [[main commits feed](https://github.com/Corbell-AI/Corbell/commits/main.atom)] [[reviewed full head](https://github.com/Corbell-AI/Corbell/commit/75c7b20ac95292185b5fef6a4680e3e10de9da66)]

The README describes Corbell as a local Python tool for building architecture graphs from code repositories and extracting design patterns and decisions from team documents. It uses those structures to assemble context for design-spec generation, review, decomposition, and issue export. The README says it runs locally without a hosted service; this source review covers selected graph, embedding, document-learning, and generation paths, not every integration or deployment configuration.[[README.md](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/README.md)]

## Architecture and data model

**Code observation — architecture graph.** The graph schema models services, datastores, queues, methods, and named flows, joined by directed dependency and call edges. Method nodes retain repository and file path, class/method name, signature, optional docstring, and start/end lines. The SQLite graph store persists nodes in `graph_nodes` with JSON data and edges in `graph_edges` with kind and metadata; it creates indexes on edge source and target. Node upserts replace a row by ID, while edge upserts replace metadata for the unique source/target/kind tuple.[[graph schema](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/schema.py)] [[SQLite graph store](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/sqlite_store.py)]

**Code observation — code and document memory.** A separate SQLite embedding store holds code chunks with service ID, repository, path, line range, content, language, chunk type, symbol, and an optional float32 embedding blob. The document-learning model stores extracted patterns, headings, terminology, format examples, and decisions; decisions retain a source file path and optional rationale. The pattern store serializes the full pattern list to a workspace JSON file (documented as `.corbell/doc_patterns.json`) and keeps scanned candidates separately in `doc_candidates.json`.[[embedding store](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/embeddings/sqlite_store.py)] [[document models](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/models.py)] [[document pattern store](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/store.py)]

## Write, update, delete, and retrieval

**Code observation — repository graph writes.** The graph builder scans configured local repositories and infers service, datastore, queue, and dependency structure using language/framework patterns and scanners. Its output is written through the graph-store upsert interface. Rebuilding is an explicit command path; the inspected store exposes whole-graph `clear()`, but no per-node or per-edge delete method. Therefore this inspection supports replace/upsert and whole-store clearing behavior, not a claim of historical versioning or fine-grained deletion.[[graph builder](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/builder.py)] [[graph schema](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/schema.py)] [[SQLite graph store](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/sqlite_store.py)]

**Code observation — document writes and changes.** The scanner finds likely ADR/RFC/spec/design Markdown files and returns unconfirmed candidates. The learner skips candidates not marked confirmed, extracts headings, frontmatter field names, terminology, and up to ten regex-derived decisions (or asks a configured LLM for enhanced extraction). The candidate model defaults `confirmed` to false. Saving learned patterns writes the complete list to JSON; no pattern-level update, supersession, or delete API was located in the inspected store. This bounded inspection does not establish how every CLI workflow chooses candidate confirmation.[[document scanner](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/scanner.py)] [[document learner](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/learner.py)] [[document models](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/models.py)] [[document pattern store](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/store.py)]

**Code observation — retrieval and context assembly.** The embedding store computes cosine similarity over stored vectors, optionally filters candidates by service IDs, and returns the requested top K. With no service filter, the inspected implementation queries all rows with embeddings and scores them in Python. The PRD processor turns feature text into several natural-language search queries (or fallback sentences), finds matching chunks, and ranks services by matches. The spec generator combines relevant learned patterns, graph context, design-doc patterns supplied for that request, and code chunks before calling a configured LLM. A retrieval result is context for generation; source inspection alone does not establish whether the generated spec is correct or whether recall is complete.[[embedding store](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/embeddings/sqlite_store.py)] [[PRD processor](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/prd_processor.py)] [[spec generator](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/spec/generator.py)]

## Scope isolation, provenance, and evidence

**Scope observation.** The graph and embedding records carry a service ID; vector lookup accepts an optional service-ID filter, with no filter meaning all services. The reviewed pattern JSON is workspace-local, and design-document paths can be supplied directly to a generation request. These are retrieval and workspace boundaries visible in code, not principal-level authorization. No cross-workspace leakage or access-control probes were run.[[graph schema](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/schema.py)] [[embedding store](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/embeddings/sqlite_store.py)] [[spec generator](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/spec/generator.py)]

**Provenance observation.** Code chunks preserve repository, file path, and line ranges; method graph records preserve file and line information; extracted design decisions keep their source file path. The inspected data shapes do not show a source-content hash, repository revision on each item, or a claim-to-source citation contract for generated output. These paths aid navigation to origins but do not themselves prove that a decision is current or that an LLM-generated factual claim is supported by its cited source.[[embedding store](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/embeddings/sqlite_store.py)] [[graph schema](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/schema.py)] [[document models](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/models.py)]

## Source-visible efficiency and observability

The embedding table has a service-ID index and stores vectors as float32 blobs; batch writes are available. Query scoring loads matching rows and computes cosine similarity in Python, so this implementation has no approximate-nearest-neighbor index in the inspected path. The spec generator uses a context pruner and token estimator to limit sections, and the token tracker records input/output token counts per LLM call and estimates cost from an internal price table or environment overrides. Those estimates are not provider billing measurements and the review collected no runtime latency, token, cost, or storage observations.[[embedding store](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/embeddings/sqlite_store.py)] [[spec generator](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/spec/generator.py)] [[token tracker](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/token_tracker.py)]

## Project metric domains

All benchmark domains are **unmeasured** for Corbell. The source includes graph/document retrieval and generated-context paths, but this task did not run a fixture or adjudicate answerable recall, abstention, corrections, stale values, deletion leakage, scope leakage, evidence support, or citation coverage. No latency distribution, write-to-recall delay, provider token totals, measured cost, or storage-efficiency measurement was collected. Project metric definitions, fixture cases, and the shared execution-status record describe evaluation protocol/status; they are not Corbell results.[[project metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded inspection of the official README and selected graph, embedding, document-learning, PRD, generation, and token-tracking source at the verified SHA. It did not inspect every command, integration, provider, or scanner; it did not run Corbell, its tests, or benchmarks. Runtime quality, scaling, production reliability, generated-claim support, per-user isolation, complete deletion and stale-index behavior remain unknown. The repository describes the product as local-first; this review did not independently assess the security of local files, configured repositories, or optional external LLM providers.[[README.md](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/README.md)] [[graph builder](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/builder.py)] [[spec generator](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/spec/generator.py)]

## Contact-list follow-up

The official pinned README was checked and publishes no contact email. The official repository's `SECURITY.md` and `SUPPORT.md` paths are absent at the reviewed revision, so no contact email was recorded. No commit metadata, profile metadata, third-party directory, or inferred address was used.[[README.md](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/README.md)] [[SECURITY.md](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/SECURITY.md)] [[SUPPORT.md](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/SUPPORT.md)]

## Benchmark status

**Benchmark not run.** No Corbell runtime, tests, or benchmark workload was run. Source and README observations are not measured results. See project metric definitions, fixture, and shared execution-status record for the separate evaluation protocol.[[project metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark execution status](../results/initial-baselines-status.json)]

## Sources

- [Current canonical GitHub repository](https://github.com/Corbell-AI/Corbell)
- [Current main branch commits feed](https://github.com/Corbell-AI/Corbell/commits/main.atom)
- [Reviewed full head commit](https://github.com/Corbell-AI/Corbell/commit/75c7b20ac95292185b5fef6a4680e3e10de9da66)
- [README.md](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/README.md)
- [corbell/core/graph/schema.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/schema.py)
- [corbell/core/graph/sqlite_store.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/sqlite_store.py)
- [corbell/core/graph/builder.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/graph/builder.py)
- [corbell/core/docs/scanner.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/scanner.py)
- [corbell/core/docs/learner.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/learner.py)
- [corbell/core/docs/models.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/models.py)
- [corbell/core/docs/store.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/docs/store.py)
- [corbell/core/embeddings/sqlite_store.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/embeddings/sqlite_store.py)
- [corbell/core/prd_processor.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/prd_processor.py)
- [corbell/core/spec/generator.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/spec/generator.py)
- [corbell/core/token_tracker.py](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/corbell/core/token_tracker.py)
- [Official security-policy path checked](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/SECURITY.md)
- [Official support path checked](https://github.com/Corbell-AI/Corbell/blob/75c7b20ac95292185b5fef6a4680e3e10de9da66/SUPPORT.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Curated roster locator and attribution](../data/memory-systems.json)

**Verification boundary:** no Corbell runtime, tests, or benchmarks were run.
