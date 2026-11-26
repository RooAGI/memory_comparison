# DreamGraph

## Identity and review pin

- Catalog ordinal: 195
- System: DreamGraph
- Slug: `dreamgraph`
- Listed repository: https://github.com/mmethodz/dreamgraph
- Roster attribution: explicit repository locator; the pinned Atlas entry is included only for curated identity and locator context ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dreamgraph.md)).
- Canonical upstream: https://github.com/mmethodz/dreamgraph
- Default branch: `main`
- Reviewed full head: [41f65091746bc1cf0ac17e34eedda6d29973f9f0](https://github.com/mmethodz/dreamgraph/commit/41f65091746bc1cf0ac17e34eedda6d29973f9f0)
- Review timestamp: 2026-11-25T11:21:09Z (UTC; 2026-11-25 03:21:09 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

DreamGraph is a project-scoped cognitive graph and development environment. Its persistent memory separates source and human-grounded project entities from speculative dream hypotheses; normalization evaluates hypotheses and publishes supported claims into the graph. Retrieval assembles a bounded, typed context pack from the graph. The review is based on selected current documentation and source at the pinned upstream head; no DreamGraph runtime, tests, or benchmarks were run. ([README](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/README.md), [architecture](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/architecture.md), [cognitive engine guide](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/cognitive-engine.md))

## Who and what

The official README presents DreamGraph as a graph-governed conceptual development environment for software projects, with a daemon, MCP tools, CLI, VS Code extension, Explorer, and browser Architect. It describes the graph and its evidence as the durable project understanding used across these surfaces. The repository page identifies `main` as the default branch; its official main commit feed reports full head `41f65091746bc1cf0ac17e34eedda6d29973f9f0`, updated 2026-10-09T06:30:46Z. ([README](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/README.md), [repository](https://github.com/mmethodz/dreamgraph), [main commit feed](https://github.com/mmethodz/dreamgraph/commits/main.atom), [head commit](https://github.com/mmethodz/dreamgraph/commit/41f65091746bc1cf0ac17e34eedda6d29973f9f0))

## Architecture and data model

DreamGraph describes two related knowledge spaces: a fact graph for project entities and validated relationships, and a dream graph for candidate nodes and edges. The current documented graph includes features, workflows, data-model entities, ADRs, UI elements, tensions, and relationships. Instance data is held in JSON stores under an instance directory; the architecture documentation says an instance is scoped to a project and repository bindings define paths considered in bounds. ([architecture](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/architecture.md), [data model](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/data-model.md), [cognitive types](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/types.ts))

The dream graph stores hypothetical nodes and edges with fields such as confidence, plausibility, evidence, contradiction, strategy, TTL, reinforcement count, and lifecycle status. Candidate normalization outcomes are recorded separately; validated relationships live in a validated-edge store, and tensions retain unresolved questions and resolution state. The data-model guide describes the candidate outcome log as append-only and resolved tensions as archived. ([data model](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/data-model.md), [cognitive types](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/types.ts))

## Write, update, delete, and retrieval

**Writes and promotion.** Scans and enrichment populate project entities; dream strategies generate candidate relationships and nodes. Normalization evaluates candidates, then publishes graph changes through the shared publication boundary. Current documentation distinguishes supported source-backed claims, human assertions, and derived hubs, and says ungrounded hypotheses remain speculative rather than being promoted as facts. ([cognitive engine guide](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/cognitive-engine.md), [normalizer](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/normalizer.ts), [publication writer](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/graph/publication.ts))

**Evidence and correction.** The normalization evidence ledger records claim-specific observations as supporting or contradicting, with origin, ancestry, operation ID, timestamp, and optional source proof. A source proof identifies a configured repository and path, content hash, JSON pointer, and independence ID. The implementation checks that source paths stay within the configured repository, the bytes match the recorded hash, and the selected JSON value supports the encoded claim. Withdrawals are recorded separately. This is evidence for normalization claims, not a guarantee that every graph fact has a complete external citation. ([normalization evidence](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/normalization-evidence.ts), [cognitive engine guide](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/cognitive-engine.md))

**Updates and removal.** Cognitive curation supports reject, retire, reopen, restore, and assert decisions with an expected graph revision, actor, reason, and operation identity. It stores dispositions in the maintenance state and supports reversible, hash-bound archives. The evidence ledger also permits withdrawal of an observation. These are history-aware lifecycle controls; the inspected sources do not establish universal hard erasure from every snapshot, export, or backup. ([curation](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/curation.ts), [normalization evidence](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/normalization-evidence.ts), [data model](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/data-model.md))

**Retrieval.** The canonical RAG entry point assembles a graph context pack and returns included entities, relationships, tensions, narrative entries, token count, and a selection receipt. The older comparison path uses lexical TF-IDF entity matching, graph expansion, ranking, and token estimation; current documentation marks canonical retrieval as the default and notes that legacy retrieval has fewer controls. The inspected canonical path is read-only. ([graph RAG](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/graph-rag.ts), [architecture](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/architecture.md))

## Scope isolation

The architecture documents per-instance directories under a master directory, with each instance attached to a project and optional repositories. The normalization evidence implementation resolves a source only through configured repository IDs and rejects absolute paths, parent traversal, and symlinks escaping the configured root. These are code and documentation observations; no cross-instance or hostile-caller isolation probes were run, so deployment-wide isolation is unmeasured. ([architecture](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/architecture.md), [normalization evidence](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/normalization-evidence.ts))

## Provenance and evidence

Provenance is richer than a plain note store: typed graph identities and relationship records can carry source or derivation context, and the claim ledger tracks support, contradiction, human origin, ancestry, source hashes, and withdrawal. The documented promotion policy distinguishes source-backed facts, human assertions, and derived hubs. Human assertion remains a distinct origin and does not itself mean independent source corroboration. ([cognitive engine guide](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/cognitive-engine.md), [normalization evidence](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/normalization-evidence.ts), [normalizer](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/normalizer.ts))

## Efficiency and observability

Canonical retrieval is deterministic and does not require an embedding provider for the inspected path; it builds a bounded context pack from the graph. The normalizer yields to the Node event loop in batches to avoid monopolizing it during large candidate passes. Publication records hashes, revisions, operation receipts, affected stores, and a reconciliation journal; the cognitive-store reader rejects content that does not match published state instead of treating corrupt or changed history as empty. These are implementation controls, not measured latency or reliability results. ([graph RAG](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/graph-rag.ts), [normalizer](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/normalizer.ts), [publication writer](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/graph/publication.ts), [cognitive store](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/cognitive-store.ts))

## Metric-domain evidence

All benchmark domains remain **unmeasured**. The project definitions, fixture, and shared status record are references only; no workload was run. ([metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | No answerable or abstention probes were scored. |
| Correction accuracy and stale-value rate | Unmeasured | No post-correction recall cases were probed. |
| Deletion leakage | Unmeasured | No post-removal probes or backup/snapshot checks were run. |
| Scope isolation | Unmeasured | No cross-instance, project, or repository probes were run. |
| Evidence support and citation coverage | Unmeasured | No output claims were adjudicated against stored evidence. |
| Retrieval latency and write-to-recall delay | Unmeasured | No reads, writes, or recall timings were collected. |
| Tokens and cost | Unmeasured | No token counts or provider charges were measured. |
| Storage efficiency | Unmeasured | No corpus or persistent-byte measurements were collected. |

## Limits and unknowns

This is a selected source review of the official README, architecture and cognitive-engine/data-model documentation, and current retrieval, normalization, provenance, curation, publication, and store code. It did not inspect every graph write API, plugin/client, deployment configuration, or recovery/export route. The source review establishes implementation structure, not operational correctness or security under every deployment. ([README](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/README.md), [architecture](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/docs/architecture.md), [normalizer](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/normalizer.ts), [graph RAG](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/graph-rag.ts))

The inspected evidence gate is specific to cognitive normalization; the breadth and completeness of provenance for all entity types and all mutation surfaces remain unknown. Practical isolation, backup retention, concurrency behavior under load, and quality of generated claims were not tested or measured. ([normalization evidence](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/cognitive/normalization-evidence.ts), [publication writer](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/src/graph/publication.ts))

The pinned official README and SECURITY.md were checked for a contact email. Neither publishes one; contact_email is recorded as null with the exact URLs checked. No profile or commit metadata, third-party directory, or inferred address was used. ([README](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/README.md), [SECURITY.md](https://github.com/mmethodz/dreamgraph/blob/41f65091746bc1cf0ac17e34eedda6d29973f9f0/SECURITY.md))

**Benchmark not run.** No DreamGraph runtime, tests, or benchmark workload were executed. The structured [system review](../data/system-reviews/dreamgraph.json) records `benchmark_status: not_run`; project metric definitions and status records remain references, not results. ([metric definitions](../METRICS.md), [execution status](../results/initial-baselines-status.json), [benchmark fixture](../fixtures/memory-benchmark-v1.json))
