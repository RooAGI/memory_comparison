# Graphify source and design review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 271 / Graphify / `graphify`  
**Listed repository locator:** [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)  
**Canonical upstream:** [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)  
**Default branch / reviewed head:** v8 / [02c27dc246cd7bc359d0f4acaf53a3fce595bc1e](https://github.com/Graphify-Labs/graphify/commit/02c27dc246cd7bc359d0f4acaf53a3fce595bc1e)  
**Review time:** 2026-11-25 21:55:18 UTC (2026-11-25 13:55:18 PST; America/Los_Angeles).

## Identity and review pin

The curated roster identifies Graphify at ordinal 271, with an explicit repository locator and an Atlas attribution retained for identity context only. The Atlas entry was not used as assessment evidence. GitHub's official repository metadata identifies `v8` as the default branch; the official commits API resolves its current head to 02c27dc246cd7bc359d0f4acaf53a3fce595bc1e, committed at 2026-11-25T13:52:34Z. Source inspection below is pinned to that head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Graphify is a local-first codebase knowledge graph and agent context tool. It parses code and can map documents and media into a graph, then exposes graph queries through a CLI or MCP server. A separate work-memory feature stores Q&A records and derives a lessons artifact from outcome signals; the review covers the open-source repository, not the hosted Graphify Cloud product.[[readme]][[how]][[ingest]][[contact]]

## Who and what

The official repository describes a Python CLI and MCP server for building a queryable knowledge graph from a project. Graphify's primary memory is a structural code and document graph; its work-memory feature adds saved Q&A records and reflection-derived node annotations. Graphify Cloud's hosted shared memory and cross-repository product are outside this repository review.[[repo]][[readme]][[contact]]

## Architecture and data model

The documented pipeline has three passes: deterministic local parsing for code, local audio/video transcription, and optional model-assisted semantic extraction for documents, papers, images and transcripts. The graph is stored in NetworkX node-link JSON. Nodes include stable IDs, labels, file types and source-file paths; edges store relations, confidence labels and source-file provenance. The persisted graph also records schema and producer version.[[how]][[readme]]

Graphify applies graph community detection and traversal rather than a separate embedding or vector index. It writes graph.json, a visualization and a report under graphify-out by default. Work memory is separate: save-result records are Markdown files under graphify-out/memory, while reflect derives LESSONS.md and a .graphify_learning.json sidecar. The sidecar overlays learning annotations at read time and does not mutate graph.json.[[how]][[readme]][[ingest]][[reflect]][[serve]]

## Write, update, delete, and retrieval

**Write.** Extraction builds the project graph from selected files. A separate `graphify save-result` command writes a uniquely named Q&A Markdown record with a question, answer, timestamp, optional outcome/correction, and up to ten cited source-node IDs. URL ingestion can also capture a user-provided web source as annotated Markdown for later extraction.[[readme]][[how]][[ingest]]

**Update and correction.** The documented `graphify update` path re-extracts changed files, using content hashes to skip unchanged inputs. Work-memory saves are separate records rather than edits to earlier answers. A corrected answer can be recorded as a new correction/outcome signal; `graphify reflect` combines signals using time decay and corroboration.[[readme]][[how]][[ingest]][[reflect]]

**Delete.** I found no user-facing work-memory deletion or erasure operation in the inspected save/reflection code. Removing a saved Q&A file is an external filesystem action. The repository documents purge for generated graph data, but this review did not execute it. I did not independently exercise graph-update behavior for deleted source files.[[ingest]][[reflect]][[readme]][[security]]

**Retrieval.** CLI query returns a scoped graph for a natural-language question; path traces relations, and explain describes a node. The MCP server exposes graph tools including query_graph, shortest_path, get_node, get_neighbors, community and graph_stats against a selected graph file. Reflection-derived node annotations are display metadata, not an enforced read filter.[[readme]][[serve]][[reflect]]

## Scope isolation

The local CLI and memory files are organized around a project directory and graphify-out location; the MCP server loads a caller-selected graph path. Those paths allow separate project graphs, but the inspected community server does not provide an authenticated tenant-isolation contract. HTTP transport is optional and its host/API-key configuration matters to deployment exposure. No cross-project or tenant workload was run.[[readme]][[serve]][[security]]

## Provenance and evidence

Each graph edge carries a relation and source-file location plus one of EXTRACTED, INFERRED, or AMBIGUOUS. EXTRACTED marks a source-explicit relation; INFERRED marks a resolved or model-inferred relationship with a confidence score; AMBIGUOUS marks uncertainty for review. These tags make graph derivations inspectable, but they do not prove that a generated answer is correct or fully supported.[[how]][[readme]]

Work-memory records can retain source-node IDs and correction/outcome fields. Reflection aggregates useful, dead-end and corrected outcomes with time-decayed scores, corroboration requirements, and source staleness checks; the derived labels are attached as display-only metadata. The review did not evaluate whether these signals produce better answers.[[ingest]][[reflect]][[serve]]

## Efficiency and observability

Code parsing is local and does not require an LLM; semantic document extraction can use a configured model. The documented content-hash cache skips unchanged inputs, and parallel code extraction is an implementation/documentation feature. These are source-level mechanisms, not timings reproduced in this review.[[how]][[readme]]

The implementation supports optional JSONL query logging with fields such as question, corpus, returned-node count and duration; full responses require an additional setting. The pinned README says queries are logged by default, but the pinned querylog implementation makes logging opt-in and leaves it off unless explicitly enabled. No runtime telemetry, latency, token or storage measurements were collected.[[querylog]][[readme]]

## Metric-domain evidence

All benchmark domains below are **unmeasured in this review**. Graph structure, code inspection and upstream benchmark statements do not constitute results measured here. No Graphify runtime, tests or benchmarks were run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Graph queries and path traversal are implemented; no answer set or abstention workload was scored. | Unmeasured |
| Correction and stale values | Work-memory supports corrected outcomes and time-decayed reflection; no correction sequence was evaluated. | Unmeasured |
| Deletion leakage | No memory deletion or post-deletion probe was run. | Unmeasured |
| Scope isolation | Project-specific graph paths exist; no tenant or cross-project workload was evaluated. | Unmeasured |
| Evidence support and citation coverage | Edges retain source-file provenance and confidence labels; answer support was not adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Hash caching and query instrumentation are source features; no timings were collected. | Unmeasured |
| Tokens, cost and storage | Local graph persistence and optional model-assisted extraction are documented; no workload totals were measured. | Unmeasured |

## Limits and unknowns

This review establishes source behavior at the verified commit, not runtime quality or deployment safety. The local filesystem layout does not by itself establish tenant isolation. Graph confidence labels describe relation provenance and uncertainty, not answer truth. Work-memory annotations are derived from recorded outcomes and displayed with nodes, but their effect on answer quality is unmeasured.[[readme]][[how]][[reflect]][[serve]]

The README/querylog mismatch about whether query logs are enabled by default is unresolved in the documentation. The source implementation says opt-in; operators should verify the specific version and configuration they deploy. This review did not run Graphify, its tests, or any workload; recall, correction, deletion, isolation and efficiency outcomes remain unknown.[[readme]][[querylog]][[metrics]]

## Benchmark status

**Benchmark not run.** No Graphify runtime, tests, or benchmark workload was executed for this review. No measured recall, correction, deletion, isolation, latency, token, cost or storage result is claimed. The project metric definitions and execution status record are linked above.[[metrics]][[fixture]][[status]]

## Contact

The official Graphify website contact page publishes `founders@graphify.com`. This exact official page is recorded as the contact source; no commit/profile metadata or third-party directory was used.[[contact]]

## Sources

Upstream files are pinned to the verified full SHA. The Atlas entry is included only for roster attribution, not as assessment evidence. See the structured record [graphify.json](../data/system-reviews/graphify.json) and the [curated roster](../data/memory-systems.json).
