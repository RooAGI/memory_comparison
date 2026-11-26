# Hermes Fleet Memory

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 290 / Hermes Fleet Memory / `hermes-fleet-memory`  
**Listed repository locator:** [amrlazw/hermes-fleet-memory](https://github.com/amrlazw/hermes-fleet-memory)  
**Canonical upstream:** [amrlazw/hermes-fleet-memory](https://github.com/amrlazw/hermes-fleet-memory)  
**Default branch / reviewed head:** main / [87ce8978accdeb2e5a4252b51e7d02842c95ebd5](https://github.com/amrlazw/hermes-fleet-memory/commit/87ce8978accdeb2e5a4252b51e7d02842c95ebd5)  
**Review time:** 2026-11-25 22:47:15 UTC (2026-11-25 14:47:15 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Hermes Fleet Memory at ordinal 290 with explicit locator `https://github.com/amrlazw/hermes-fleet-memory`; its pinned Agent Memory Atlas record is retained solely for curated identity and locator attribution, not used as assessment evidence. The official repository page identifies `main` as the default branch, and the official `main.atom` feed reports full head `87ce8978accdeb2e5a4252b51e7d02842c95ebd5` updated 2026-09-24T14:02:18Z. The feed's commit, official repository page, and catalog pin agree.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Hermes Fleet Memory is a self-operated, on-demand memory server for Hermes and other MCP clients. It embeds memory text locally and stores vectors and metadata in a shared Qdrant collection, while node-configured domain checks control which records a client may request. The repository also contains remote desktop and task-plane features; this review focuses on its memory behavior.[[readme]][[core]][[skill]]

## Who and what

The official README describes a Python FastMCP stdio server intended to connect multiple agent instances to operator-owned Qdrant infrastructure. It is a deployable library/server project rather than a hosted memory service; the operator supplies or configures the vector database endpoint.[[readme]][[core]]

## Architecture and data model

The README describes a single Qdrant collection named `hermes_fleet_memory`, 384-dimensional embeddings from BAAI/bge-small-en-v1.5, and on-demand tools rather than ambient prompt injection. The inspected client defines that collection name, reads `FLEET_HARD_DOMAIN` (default `work`), configures Qdrant connectivity, and sets a bounded client timeout.[[readme]][[core]]

A memory card is described as text plus an embedding and payload metadata such as domain, optional client and slot identifiers, memory type, active/pinned state, author node, revision, and expiry. The README describes deterministic UUID5 identifiers for named slots and separate episodic records. The small graph helper extracts explicit wiki links, backticked identifiers, and capitalized phrases, then derives a limited set of directional relations with fixed verb patterns; this is heuristic entity extraction, not a separately persisted graph database.[[readme]][[skill]][[kg]]

The MCP server exposes the memory tools alongside optional desktop and task-plane tools. The README documents Hermes configuration with `memory.provider: none`, leaving recall to explicit MCP calls; the skill guide instructs agents to search before trying local shell inspection for fleet facts.[[readme]][[skill]][[core]]

## Write, update, delete, and retrieval

**Write.** The README documents `fleet_memory_store` as the explicit write path. A named slot is intended to overwrite the deterministic UUID5 point for its domain/client/slot key; episodic writes use a semantic near-duplicate check at a documented cosine threshold of 0.95. The docs say records carry author-node attribution and a monotonic revision. These are documented behaviors; no live write was run in this review.[[readme]][[skill]][[core]]

**Update and correction.** Named-slot replacement and near-duplicate episodic refresh are documented as in-place updates. The README describes last-write-wins timestamp validation to reject stale updates. The inspected materials do not establish a retained correction history or a temporal query interface, so update semantics should not be treated as an audit trail.[[readme]][[skill]][[core]]

**Delete and expiry.** No direct user-facing memory-forget tool is described in the inspected memory-tool guide. The current cleanup worker selects active, unpinned points with an expired timestamp, appends their IDs and payloads to a JSONL archive, then deletes those point IDs from Qdrant in batches. It stops after a 200-batch cap and logs if expired points may remain; the archive is an additional retained copy, so this is not complete erasure.[[readme]][[skill]][[cleaner]]

**Retrieval.** The README and skill describe `fleet_memory_search` as an embedding-based Qdrant query filtered by active status, authorized domain, and optional client ID. `fleet_graph_search` is described as a graph-style lookup over extracted entities and relations. The inspected entity extractor caps each extraction at 15 entities and 15 relations and uses regex/pattern matching, so it does not imply general graph reasoning or semantic relation extraction.[[readme]][[skill]][[kg]][[core]]

## Scope isolation

The client derives an allowed domain set from the operator-controlled `FLEET_HARD_DOMAIN`: a `work` or `personal` node may access its own domain and `shared`, while `all` has broad access. The documentation says unauthorized tool arguments are rejected before retrieval. This is client-side policy around a common Qdrant collection and credential; the inspected documentation does not establish independent server-side per-domain authorization or isolation from a compromised node with the database key.[[readme]][[skill]][[security-policy]][[core]]

## Provenance and evidence

The documented payload includes author-node attribution and a monotonic revision, and the cleanup process preserves expired point payloads in an offline JSONL archive. The client also includes a pattern-based credential scanner whose function returns pattern names rather than matched values; it is a guard for listed formats, not an evidence or truth-validation mechanism. The memory interface documentation does not require source documents, quotations, or claim-level citations on stored cards or retrieved answers. Provenance fields can show which node wrote a card, but they do not by themselves establish that its factual content is supported.[[readme]][[skill]][[cleaner]][[core]][[secret-scan]]

## Efficiency and observability

On-demand MCP retrieval and the documented `memory.provider: none` setup avoid routine memory injection into each prompt. The client defines a Qdrant request timeout, while the cleaner emits batch and total archive/eviction messages. The README also advertises embedding/search timings, storage capacity, and other performance figures; this review did not reproduce them, and they are not benchmark results for this project.[[readme]][[core]][[cleaner]]

The README says setup telemetry is opt-in via `FLEET_TELEMETRY=1` and can be overridden by `DO_NOT_TRACK=1`. This review did not inspect telemetry transport behavior or verify the privacy claims at runtime.[[readme]]

## Metric-domain evidence

Project metric definitions, fixture, and baseline status record describe how to measure these domains; none was measured for Hermes Fleet Memory in this task.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Vector and graph search tools are documented; response correctness and abstention were not adjudicated. | Unmeasured |
| Correction and stale values | Slot overwrite and timestamp ordering are described; correction sequences were not probed. | Unmeasured |
| Deletion leakage | Expiry cleanup archives then deletes eligible Qdrant points; no user-delete or post-delete probe was run. | Unmeasured |
| Scope isolation | The client documents domain validation and filters; no cross-domain workload or server-side authorization test was run. | Unmeasured |
| Evidence support and citations | Node attribution is described, but required source evidence and claim citations were not found in the inspected interface. | Unmeasured |
| Latency and write-to-recall delay | Timeout and cleanup logging exist; no retrieval timings or write-to-recall probes were collected. | Unmeasured |
| Tokens, cost, and storage | On-demand access and vector storage are described; no token, cost, or storage measurement was made. | Unmeasured |

## Limits and unknowns

This is a source-based review of selected official documentation and implementation files at the verified head. It cannot establish runtime correctness, recall quality, actual tenant isolation, deletion completeness across backups or archive copies, latency, cost, or operational reliability. README performance numbers and security claims remain upstream-reported claims, not independently reproduced results.[[readme]][[core]][[cleaner]][[security-policy]]

The review did not inspect every client handler or deployment path. The visible implementation includes a broad MCP client that also handles desktop/task functionality, so the exact behavior of all tools and their integrations remains outside this assessment.[[core]][[repo]]

## Benchmark status

**Benchmark not run.** No Hermes Fleet Memory runtime, tests, or benchmark workload was executed. No recall, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [baseline execution status](../results/initial-baselines-status.json) define the project protocol, not results for this system.[[metrics]][[fixture]][[status]]

## Contact

The official pinned SECURITY.md publishes `amirulazw94@gmail.com` for confidential vulnerability reports. The structured record stores this email with the exact pinned policy URL; no profile metadata or third-party directory was used.[[security-policy]]

## Sources

All upstream file sources are pinned to the verified full SHA. The Atlas record is included only for curated roster attribution. See the structured record [hermes-fleet-memory.json](../data/system-reviews/hermes-fleet-memory.json) and [curated roster](../data/memory-systems.json).
