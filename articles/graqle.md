# GraQle

**Ordinal:** 274  
**Slug:** `graqle`  
**Listed repository:** https://github.com/quantamixsol/graqle  
**Reviewed upstream:** https://github.com/quantamixsol/graqle/tree/master at `434ca7a4bcb71c56058db565e3d7aeb87fdbb30c`  
**Review time:** 2026-11-25 22:00:28 UTC (14:00:28 PST, America/Los_Angeles)  
**Status:** Reviewed from code. Benchmark not run.

## Summary

GraQle is a Python knowledge-graph and reasoning framework for coding and organisational agents. Its main durable project memory is a graph of typed nodes and relations, normally stored as a local JSON graph; optional Neo4j and Neptune backends are projections. A separate in-process reasoning memory stores findings from multi-agent reasoning rounds. Source inspection establishes the mechanisms described below, not their retrieval quality or operational isolation in a deployment.[[readme]][[graph]][[memory]][[tiers]]

## Who and what

The official README names Quantamix Solutions as the project builder and describes GraQle as a persistent organisational knowledge graph and reasoning tool. It offers a Python package, CLI, MCP tools, server, and agent integrations. This review assesses the current public `master` source, not a particular installed release.[[readme]][[repo]]

## Architecture and data model

The core `Graqle` object holds `CogniNode` objects and `CogniEdge` relationships in dictionaries, backed by a NetworkX multigraph during serialization and traversal. Node data includes an ID, label, entity type, description, properties, and attached chunks. Edges carry source and target IDs, relationship, and weight. The default persistent format is a node-link JSON file; source records can include file path and source labels in node properties. Optional Neo4j reads/writes and an optional Neptune tier are also present, with the tier facade describing JSON as primary and graph databases as projections.[[graph]][[node]][[tiers]]

The CLI's `graq learn knowledge` creates a typed KNOWLEDGE node with domain, tags, timestamp, and manual-source metadata, then can connect it to related nodes using semantic or keyword matching and extracted entities. Learning nodes, entities, and files follow similar graph mutation paths. A file learned through `graq learn file` stores its path and content length and uses the first 500 characters as its description; node chunk loading is a separate graph capability.[[learn]][[graph]][[node]]

A distinct `ReasoningMemory` holds prior round results keyed by agent, round, and node. Entries contain the result value, confidence, source agent, stored and verified rounds, node ID, tenant ID, clearance, TRACE gap scores, timestamp, and contradiction count. It is an in-memory store with per-tenant dictionaries and up to ten MVCC snapshots per tenant; this is separate from the persistent project graph.[[memory]][[memory-types]][[memory-service]]

## Write, update, delete, and retrieval

The `graq learn` commands write nodes and relationships. Knowledge writes create timestamp-derived IDs, while learning an existing explicit node ID replaces the node's current object. The CLI wraps graph-file read/modify/write paths with a file lock; graph serialization validates node/edge structure and uses a cross-platform file lock for writes. The main graph API inspected exposes add-node and add-edge operations. I did not find a first-class delete or forget operation in the inspected core graph operations and learn commands, so content deletion, removal from backups, or erasure from a remote projection remain unverified.[[learn]][[graph]]

For recall, `areason` selects a subgraph using the configured activation backend and ranking strategy, then runs an orchestrator over the selected nodes. Semantic activation may use a direct filename lookup and activation-memory boosts; the code also supports other rankings and backend-specific activators. The prompt templates ask reasoning nodes to cite evidence chunks and state confidence. These are retrieval and response-format mechanisms; this review did not score answers, abstentions, or citations for correctness.[[graph]][[readme]]

Round memory stores results with source-agent and round attribution, detects same-node findings from different agents as contradictions, and reduces confidence according to caller-supplied decay and contradiction parameters. Summaries apply decay, discard entries below the configured confidence floor, sort remaining entries by confidence, redact values above the viewer's clearance, and cap the output at 8,000 characters. Snapshot and rollback operate on the currently bound tenant's slice.[[memory]][[memory-types]]

## Scope isolation

The durable graph is commonly a project-local file. The shared MCP server documentation describes workspace roots, per-session gate state, and—on Team or Enterprise—a multi-project hub with separate graph, config, caches, and cost counters per project. It says sessions bind to one project, but this review did not exercise server authentication or cross-project access.[[readme]][[multi-agent]]

Round memory validates tenant IDs and binds each instance to one tenant's slice; non-default tenant use fails unless `GRAQLE_TENANT_SCOPING=1` was enabled when the module loaded. IDs must be the default sentinel, a SHA-256 hex value, or a `team-<slug>`; validation does not prove that a tenant exists, so authorization must be supplied by the caller. Clearance redaction replaces the value but retains metadata such as source agent, confidence, and TRACE scores. Thus tenant binding is a code-level boundary for this in-memory component, not evidence of end-to-end isolation across every GraQle surface.[[tenant]][[memory]][[memory-types]][[memory-service]]

## Provenance and evidence

Learned graph nodes can carry source labels, file paths, domains, tags, and timestamps, while file-derived nodes retain a source path and length. Reasoning-memory records retain the producing agent and round and expose confidence, contradiction count, and TRACE scores. Prompt templates request numbered evidence citations. These are provenance and evidence affordances; they do not by themselves establish that a stored claim is true, that a citation entails the answer, or that a cited passage remains current.[[learn]][[node]][[memory]][[memory-types]][[readme]]

The README separately documents a Decision Assurance Gate that records signed, hash-chained provenance events for governed decisions. It is opt-in and is an action-governance record, distinct from the knowledge-graph source metadata and round-memory entries reviewed here.[[readme]]

## Efficiency and observability

Activation is configurable and can use direct file lookup, semantic selection, other ranking strategies, and an optional Neo4j runtime connector. The reasoning path logs activation and errors; query results carry latency and cost fields, and the graph records query/context and graph statistics through its metrics engine. The inspected metric path estimates answer tokens from character length, so it is an estimate rather than provider-reported token usage.[[graph]]

GraQle's official README and shared-server guide report a 20,000-node fixture comparison: 687.0 MB for three separate servers and 492.8 MB for one shared server plus three relays. These are upstream-reported figures for that fixture, not measurements reproduced in this review. No recall, correction, deletion, isolation, latency, token, cost, or storage benchmark was run here.[[readme]][[multi-agent]]

## Metric-domain evidence

The project defines benchmark measures and a fixed synthetic fixture; these are evaluation protocol, not GraQle results. Every domain below remains unmeasured for this review.[[metrics]][[fixture]][[status]]

## Limits and unknowns

- The durable graph and the per-round `ReasoningMemory` have different persistence and scope models; claims about one should not be assumed to describe the other.[[graph]][[memory]]
- No first-class graph deletion path was located in the inspected graph operations and learning commands. Deletion behavior for other interfaces, persisted copies, Neo4j/Neptune projections, and backups was not established.[[graph]][[learn]][[tiers]]
- Tenant validation and instance binding exist for round memory, but tenant existence and caller authorization are delegated elsewhere. Shared-server project/session behavior was read from documentation, not probed.[[tenant]][[memory-service]][[multi-agent]]
- Citation prompts and provenance metadata are not an adjudication of factual support. Runtime recall quality, stale-value behavior, abstention, and scope leakage remain unknown.[[memory-types]][[readme]]
- The upstream README's memory figures apply to one 20,000-node setup only. No measurements for this assessment were collected.[[multi-agent]]

## Benchmark status

**Benchmark not run.** GraQle, its tests, and benchmark workloads were not run. The project metric definitions, fixture, and shared status record describe comparison protocol and execution status; none is a GraQle result.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README publishes `security@quantamixsolutions.com` for vulnerability reports. The structured record stores that address with the exact pinned README URL. No commit/profile metadata, third-party directory, or inferred address was used.[[readme]]

## Sources

The catalog confirms the roster identity and listed locator; its Atlas URL is retained only as attribution, not assessment evidence.[[catalog]][[atlas]] The official repository metadata and current branch commit provide the review pin.[[repo]][[head]] Upstream source and documentation links below are pinned to the full reviewed SHA. See the structured record [graqle.json](../data/system-reviews/graqle.json) and [curated roster](../data/memory-systems.json).
