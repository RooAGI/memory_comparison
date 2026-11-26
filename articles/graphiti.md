# Graphiti source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 272 / Graphiti / \`graphiti\`  
**Listed repository locator:** [getzep/graphiti](https://github.com/getzep/graphiti)  
**Canonical upstream:** [getzep/graphiti](https://github.com/getzep/graphiti)  
**Default branch / reviewed head:** main / [b8ea9c5dcba4b0031c9c204f733bcd7ad5e2dadc](https://github.com/getzep/graphiti/commit/b8ea9c5dcba4b0031c9c204f733bcd7ad5e2dadc)  
**Review time:** 2026-11-25 21:54:31 UTC (2026-11-25 13:54:31 PST; America/Los_Angeles).

## Identity and review pin

The curated roster lists Graphiti at ordinal 272, slug \`graphiti\`, with the explicit locator https://github.com/getzep/graphiti. Its pinned Agent Memory Atlas entry is retained only as catalog attribution and locator context; it is not assessment evidence. The official repository page identifies \`main\` as the default branch. A fresh official Git remote check reported \`HEAD -> refs/heads/main\` at full SHA \`b8ea9c5dcba4b0031c9c204f733bcd7ad5e2dadc\`; a shallow checkout of \`main\` resolved to the same SHA. Source inspection below is pinned to that checkout.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Graphiti is an open-source Python framework for constructing and querying temporal knowledge graphs from source episodes. It stores raw episodes alongside extracted entities and temporal relationship facts, and supports graph-aware hybrid retrieval. It is a framework rather than a complete hosted agent-memory service: the application supplies the database, models, authentication, authorization, and operational controls.[[readme]][[core]]

## Who and what

The official README presents Graphiti as a Python framework and distinguishes it from Zep's managed context layer. The repository includes the reusable graph library plus reference MCP and REST servers. The server examples are explicitly not production deployments.[[readme]][[security]]

## Architecture and data model

The Graphiti facade composes graph-driver, LLM, embedder, search, and ingestion components. Core records include episodic nodes for source data, entity nodes, relationship edges, and optional community and saga structures. The graph backend is selected through the driver abstraction.[[core]][[nodes]][[edges]]

Episode nodes preserve raw content, source type and description, a group ID, a creation timestamp, a reference/valid timestamp, and links to derived edges. Entity edges store a fact and endpoint UUIDs, source episode UUIDs, and temporal fields. This lets callers trace a derived relation back to the episodes that contributed it.[[nodes]][[edges]][[edgeops]]

The README documents Neo4j, FalkorDB, Amazon Neptune, and Relate as graph backends. The supported retrieval mechanisms depend on provider capabilities such as full-text and vector search.[[readme]][[search]]

## Write, update, delete, and retrieval

**Write.** \`add_episode\` accepts raw episode content, its source description and type, reference time, and optional group and ontology configuration. The pipeline extracts and resolves entities and edges, creates embeddings, persists graph records, and handles contradictory facts through temporal edge resolution. LLM structured-output behavior and provider configuration affect ingestion reliability.[[core]][[nodes]][[edgeops]]

**Update and correction.** New episodes add source evidence and can resolve duplicates or invalidate contradicted edges while preserving prior temporal facts. The inspected facade does not establish a general arbitrary field-edit API for existing episodes. Correction quality therefore depends on extraction and resolution behavior; it was not tested here.[[core]][[edges]][[edgeops]]

**Delete.** \`remove_episode\` removes an episode and its relationships, removes the episode UUID from edges that still have other support, deletes unsupported edges and nodes mentioned only by that episode, and rebuilds summaries for surviving nodes. Group-wide node deletion is also implemented. These graph operations do not demonstrate erasure from backups or external copies.[[core]][[nodes]]

**Retrieval.** \`search\` provides a basic edge-oriented hybrid query; \`search_\` accepts a configurable recipe and can return edges, nodes, episodes, and communities. Recipes combine BM25/full-text, cosine similarity, and optionally BFS, with RRF, MMR, cross-encoder, or node-distance reranking. Search filters can constrain temporal fields and graph properties.[[core]][[search]][[recipes]]

**Temporal correction.** Edges distinguish valid time (when a fact held) from transaction time (when Graphiti recorded or expired the assertion). Contradiction resolution may set the earlier edge's \`invalid_at\` to the newer fact's \`valid_at\` while retaining the older edge for historical queries.[[edges]][[edgeops]]

## Scope isolation

Nodes and edges carry \`group_id\`, and search accepts optional \`group_ids\` that are propagated to graph queries. Because these filters are optional, callers that omit them can query without a group restriction. The code's grouping is a data partition, not authorization.[[nodes]][[search]]

The official security policy says the reference MCP and REST servers do not isolate callers: any caller can read, change, or delete data in any group. It also states that the core library trusts episodes in the same group equally, so an ingested episode can change facts attributed to earlier episodes. Production tenancy and admission controls belong in the host application.[[security]]

## Provenance and evidence

Episode nodes preserve the ingested content and its source type/description. Derived relationship edges retain episode UUIDs and temporal fields, allowing lineage back to source records. These fields provide provenance links; this review did not adjudicate whether extracted facts are entailed by the episode or whether answers cite the right evidence.[[nodes]][[edges]]

## Efficiency and observability

The implementation supports indexed graph search, candidate limits, configurable reranking, async concurrency controls, and opt-in concurrent ingestion. Concurrent ingestion changes the context in which extraction runs and the README notes that it may produce a graph different from serial ingestion. Tracing and timing instrumentation exist in the search/ingestion paths; no performance claim was reproduced.[[core]][[search]][[recipes]][[readme]]

## Metric-domain evidence

All project benchmark domains are **unmeasured for Graphiti**. The [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe project evaluation materials, not Graphiti results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Hybrid graph search, temporal filters, and rerankers exist; answer correctness and abstention were not scored. | Unmeasured |
| Correction and stale values | New episodes can resolve duplicates and temporally invalidate edges; correction sequences were not evaluated. | Unmeasured |
| Deletion leakage | Episode and group deletion paths exist; leakage, recovery, and backup propagation were not probed. | Unmeasured |
| Scope isolation | Group filters exist; no cross-group isolation workload was run. | Unmeasured |
| Evidence support and citations | Episodes and derived edges preserve lineage identifiers; no answer evidence was adjudicated. | Unmeasured |
| Latency and write-to-recall delay | Timings and tracing are implemented; no end-to-end task timings were collected. | Unmeasured |
| Tokens, cost, and storage | Backends, model providers, and concurrency are configurable; no token, cost, or storage comparison was made. | Unmeasured |

## Limits and unknowns

This is a bounded source review at the verified current upstream head. Graphiti, tests, and benchmark workloads were not run. It cannot establish retrieval accuracy, structured-output reliability for a selected provider, tenant isolation in a host deployment, deletion propagation through backups, or production latency and cost.[[readme]][[security]][[core]]

The README notes that Graphiti works best with models that reliably support structured output and that weaker compatibility can cause extraction schema errors. The exact operational effect depends on the configured models and database; this review did not validate a deployment.[[readme]]

## Benchmark status

**Benchmark not run.** No Graphiti runtime, tests, or benchmark fixture was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage measurement is claimed. The project [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) are protocol materials, not Graphiti measurements.[[metrics]][[fixture]][[status]]

## Contact

The pinned official README and SECURITY.md were checked for a published contact email. Neither publishes an email; the README routes general support to GitHub issues and the security policy uses private vulnerability reporting. The structured review stores \`contact_email: null\` with both exact URLs checked. No email was inferred from account, commit, or third-party metadata.[[readme]][[security]]

## Sources

All upstream file links in the structured record and this review use the verified full SHA. The Atlas link is catalog attribution only, not assessment evidence. See the structured record [graphiti.json](../data/system-reviews/graphiti.json) and [curated roster](../data/memory-systems.json).
