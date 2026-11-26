# Cashew

## Identity and review pin

- **System:** Cashew
- **Curated position:** 112
- **Slug:** \`cashew\`
- **Listed repository:** [rajkripal/cashew](https://github.com/rajkripal/cashew)
- **Canonical repository at review:** [rajkripal/cashew](https://github.com/rajkripal/cashew)
- **Default branch:** \`main\`
- **Reviewed head:** [\`1bb7ae6549a9814e58c866ca18f70d760e9bf493\`](https://github.com/rajkripal/cashew/commit/1bb7ae6549a9814e58c866ca18f70d760e9bf493)
- **Reviewed:** 2026-11-25 07:41:37 UTC (2026-11-24 23:41:37 PST; America/Los_Angeles)
- **Review status:** Reviewed from current source and documentation
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cashew.md), used for curated identity, listed repository, and source attribution only.

The local roster places Cashew at position 112 with slug \`cashew\`, listed repository \`rajkripal/cashew\`, and the pinned Atlas attribution above.[[catalog]] The official GitHub repository is public and names \`main\` as its default branch; the GitHub API for \`commits/main\` returned full head \`1bb7ae6549a9814e58c866ca18f70d760e9bf493\` during this review.[[repo]][[head]] The API commit date is 2026-11-10T09:50:51Z; the review timestamp above records when the sources were checked.[[head]]

## Summary

Cashew is a local persistent thought graph for agent memory. It stores typed thought nodes and derivation edges in SQLite, keeps embeddings in SQLite tables with optional sqlite-vec support, and retrieves context by combining vector-seeded search with a bounded graph walk. Extractors and maintenance cycles use language models for knowledge extraction and synthesis, while retrieval embeddings can run locally. This is a source-based review of the memory system, not a runtime evaluation.[[readme]][[design]][[retrieval]]

## Architecture and data model

The design describes a single SQLite database with thought_nodes, derivation_edges, embeddings, and a sqlite-vec virtual table when available. Nodes carry content, node type, domain, storage timestamp, optional referent time, source file, access statistics, tags, decay/permanence flags, and metadata. Derivation edges record parent and child ids, weight, and reasoning. The design document is a high-level specification; the repository also contains a schema-management module and current code may evolve beyond the design text.[[design]][[db]]

The system's main memory unit is therefore an individual thought, with edges preserving the stated derivation path. Node types in the design include facts, observations, insights, decisions, beliefs, derived hypotheses, meta-reflections, core memories, and cross-links. The graph can retain both user and AI domains in one database; the domain is a field used by retrieval filters, not a separate physical store.[[design]][[retrieval]]

## Write, update, delete, and retrieval

**Writing.** The README documents extracting text from a stream or file, plus built-in ingestion paths for Obsidian, Markdown directories, OpenClaw session logs, and Claude conversation archives. The documented default is LLM-based extraction into typed knowledge; an explicit no-LLM option uses paragraph splitting. The design describes extracted thoughts being linked to similar parent nodes with reasoning edges. These paths produce source-aware nodes where extractor metadata is available; the reviewed interface does not impose a universal citation or evidence schema on every node.[[readme]][[design]][[extractors]]

**Updates and deletion.** The documented maintenance model is organic decay: nodes that are not accessed can lose fitness, and low-fitness nodes are marked decayed and excluded from retrieval. Sleep/consolidation also cross-links related nodes, deduplicates highly similar nodes, promotes selected nodes to permanent/core status, and records decay transitions in an audit table. The decay-audit module describes a hard-GC path: if a node is already deleted when the event is logged, it writes a stub audit row; its default cleanup prunes audit entries older than seven days, and its content summary is truncated to 80 characters. The design describes deduplication as redirecting edges to a keeper and decaying duplicates; the pinned sleep implementation contains merge logic for updated facts. The reviewed sources do not establish a general user-facing delete contract or how content persists in backups and database copies.[[readme]][[design]][[sleep]][[decay]][[audit]][[head]]

**Retrieval.** A query is embedded and used to seed nearest-neighbor search; the repository describes sqlite-vec's current scan as brute-force O(N), followed by bounded recursive breadth-first traversal across graph edges. The walk scores neighbors and returns ranked context. The README specifies local all-MiniLM-L6-v2 embeddings (384 dimensions), with no API calls required for retrieval; LLMs are used for extraction and think cycles. Retrieval supports optional domain and tag filters and excludes decayed nodes. Its result representation can include node ids, content, type, domain, score, and the graph path used to reach a result.[[readme]][[design]][[retrieval]]

## Scope isolation

Cashew stores multiple domains within one graph and exposes optional domain filtering on retrieval. That provides a query filter, but the reviewed model does not show tenant identity, principal-specific authorization, or a per-node access-control policy. The deployment boundary described in the README is a local SQLite file. Separate database files can provide operational separation, but the sources reviewed here do not establish enforced isolation across multiple users or agent principals sharing a database. No scope-isolation workload was run.[[design]][[retrieval]][[readme]]

## Provenance and evidence

Nodes include a source_file field, and derivation edges include reasoning text; the decay audit records snapshots of the node state when it is marked decayed. The model can therefore preserve some input-location and derivation context. However, the reviewed sources do not establish required source URLs, quoted evidence spans, author identity, trust labels, citation validation, or human approval as a condition of storage or retrieval. Provenance is best understood as optional source and graph lineage, not a verified evidence chain.[[design]][[audit]][[extractors]]

## Efficiency and observability

The README identifies brute-force O(N) vector seeding as the main retrieval scaling limit and says an approximate-nearest-neighbor index would be needed at much larger vector counts; the subsequent bounded BFS limits graph expansion. These are source claims, not measurements collected for this review. The sleep design describes a work-capped pipeline over a limited set of nodes, batched/vectorized similarity processing, and an optional legacy text similarity path. A warm daemon and content-hash embedding cache can reduce repeated model-loading and embedding work. The repository includes metrics and a dashboard, but this review did not inspect every telemetry path or collect timing, token, cost, or storage measurements.[[readme]][[design]][[sleep]][[repo]]

## Metric-domain evidence

All performance and quality domains are **unmeasured in this review**. Source mechanisms and the project evaluation plan are not Cashew benchmark results.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Vector seeding and graph expansion return context; no answerability probes were run. | Unmeasured |
| Correction accuracy and stale values | Sleep deduplication can merge near-duplicates; no correction sequence was scored. | Unmeasured |
| Deletion leakage | Decayed nodes are filtered and decay events are audited; no post-delete or residual-copy probes were run. | Unmeasured |
| Scope isolation | Retrieval offers a domain filter; no multi-principal isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Source-file and derivation fields exist, but no evidence adjudication was run. | Unmeasured |
| Latency and write-to-recall delay | Retrieval path is source-visible; no timings were collected. | Unmeasured |
| Tokens, cost, and storage | Local embedding and work-cap mechanisms are documented; no resource measurements were collected. | Unmeasured |

The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) describe evaluation plans and project-wide status, not Cashew measurements.[[metrics]][[fixture]][[status]]

## Limitations and unknowns

This review is bounded to the pinned README, design documentation, and selected current source modules. It did not execute Cashew, trace every extraction entry point into its database writes, or inspect every backend/integration. It does not establish whether arbitrary node deletion is exposed separately from decay, how deletion propagates through backups or synced copies, or whether domain filters provide security isolation.

The documented retrieval seed search is a brute-force vector scan, so its work grows with the number of stored vectors. Optional local embeddings avoid a retrieval API dependency but require the model download and local resources described in the README. LLM-dependent extraction and think cycles require a configured model provider. The repository's documented performance statements are not independently reproduced here.[[readme]][[design]][[retrieval]][[extractors]]

## Benchmark status

**Benchmark not run.** I did not execute Cashew, its tests, or any benchmark workload. No runtime quality, latency, token, cost, storage, correction, deletion, or scope-isolation result is claimed.

## Contact

The pinned official [SECURITY.md](https://github.com/rajkripal/cashew/blob/1bb7ae6549a9814e58c866ca18f70d760e9bf493/SECURITY.md) publishes \`rajkripal.danday@gmail.com\` for private security reports. This is a project-documentation contact, not an address inferred from commit metadata.[[security]]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cashew.md) — attribution only.
- [Official repository](https://github.com/rajkripal/cashew) — canonical repository and default branch.
- [GitHub API current main head](https://api.github.com/repos/rajkripal/cashew/commits/main) — full head SHA and commit timestamp observed during review.
- [Reviewed head](https://github.com/rajkripal/cashew/commit/1bb7ae6549a9814e58c866ca18f70d760e9bf493)
- [README](https://github.com/rajkripal/cashew/blob/1bb7ae6549a9814e58c866ca18f70d760e9bf493/README.md) — usage, ingestion, retrieval overview, local embeddings, scaling statement, daemon/cache, and resource requirements.
- [Design document](https://github.com/rajkripal/cashew/blob/1bb7ae6549a9814e58c866ca18f70d760e9bf493/DESIGN.md) — schema, graph model, retrieval, extraction, sleep cycle, decay and stated limitations.
- [Database schema and access helper](https://github.com/rajkripal/cashew/blob/1bb7ae6549a9814e58c866ca18f70d760e9bf493/core/db.py) — graph tables, schema and connection management.
- [Retrieval implementation](https://github.com/rajkripal/cashew/blob/1bb7ae6549a9814e58c866ca18f70d760e9bf493/core/retrieval.py) — embedding seeds, filters, graph path and retrieval results.
- [Extractor implementation](https://github.com/rajkripal/cashew/blob/1bb7ae6549a9814e58c866ca18f70d760e9bf493/core/extractors.py) — ingestion/extraction pathways.
- [Sleep/consolidation implementation](https://github.com/rajkripal/cashew/blob/1bb7ae6549a9814e58c866ca18f70d760e9bf493/core/sleep.py) — cross-linking, deduplication, decay, permanence and work caps.
- [Decay implementation](https://github.com/rajkripal/cashew/blob/1bb7ae6549a9814e58c866ca18f70d760e9bf493/core/decay.py) — fitness-based decay behavior.
- [Decay audit implementation](https://github.com/rajkripal/cashew/blob/1bb7ae6549a9814e58c866ca18f70d760e9bf493/core/decay_audit.py) — decay transition snapshots.
- [Security policy](https://github.com/rajkripal/cashew/blob/1bb7ae6549a9814e58c866ca18f70d760e9bf493/SECURITY.md) — published security contact email.
- [Project metrics](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) — evaluation definitions/status only.

**Verification boundary:** read-only source and documentation review; no Cashew runtime, tests, or benchmarks.
