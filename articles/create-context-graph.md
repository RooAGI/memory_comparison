# Create Context Graph — source review

## Identity and review pin

- **Roster ordinal / name / slug:** 170 / Create Context Graph / `create-context-graph`
- **Listed repository locator:** https://github.com/neo4j-labs/create-context-graph
- **Roster attribution:** `repository_status: explicit`; the Atlas entry is retained only for identity and locator attribution. [Curated roster](../data/memory-systems.json) · [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/create-context-graph.md)
- **Canonical upstream / default branch:** [neo4j-labs/create-context-graph](https://github.com/neo4j-labs/create-context-graph) / `main`
- **Reviewed head:** [926e3b3e7a2d3318f94e8a2cc5196677046bbe6d](https://github.com/neo4j-labs/create-context-graph/commit/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d)
- **Verification:** The official repository page showed public `neo4j-labs/create-context-graph` with `main` selected and latest commit prefix `926e3b3`; GitHub's official commit API resolved `main` to the full SHA above. The commit API reports commit time 2026-10-09T14:51:25Z.
- **Reviewed:** 2026-11-25 10:05:17 UTC (2026-11-25 02:05:17 PST; America/Los_Angeles)
- **Status:** Reviewed from source and documentation pinned to the verified upstream head; benchmark not run.

## Summary

Create Context Graph is a Python CLI scaffold generator. It creates a domain-specific web application with a FastAPI backend, selectable agent framework, graph memory integration, and Next.js frontend. The generated application can use Neo4j Agent Memory Service (NAMS) by default or a self-hosted Neo4j Bolt backend. The generator, the generated application, and the selected memory backend have distinct responsibilities; findings here describe their code and documentation, not a running deployment. [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md) · [generator](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/generator.py)

## Who and what

The README identifies this as an experimental Neo4j Labs project maintained by Neo4j staff and the community, with no official product support; it directs support requests to GitHub Issues or the Neo4j Community Forum. It is a scaffold generator rather than a hosted memory service. [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md)

## Architecture and data model

A domain ontology is the generator's central specification. Its typed definitions cover entity labels and POLE+O categories, node and relationship properties, document templates, decision-trace scenarios, agent tools with Cypher, and visualization settings. The generator renders backend, agent, frontend, and Cypher assets into a project; the README describes a common HTTP and UI layer with selectable agent framework implementations. [ontology](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/ontology.py) · [generator](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/generator.py) · [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md)

The README describes three memory categories in generated applications: short-term conversation/document messages; long-term entities and relationships modeled as a knowledge graph; and reasoning memory represented by decision traces with thought, action, observation, and causal links. The precise persistence shape depends on the backend and its API. [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md) · [memory template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/memory.py.j2)

## Write, update, delete, and retrieval

**Writes.** Generated applications store conversation messages through the `MemoryIntegration` wrapper. The wrapper resolves session IDs and calls `store_message`; errors and backend-specific unsupported operations are caught, logged, and returned as absent/empty results. Fixture ingestion and optional SaaS connectors provide separate import paths. [memory template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/memory.py.j2) · [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md)

**Backend differences.** In self-hosted Bolt mode, the generated client executes Cypher against Neo4j, including a database reset that deletes all nodes and relationships. In NAMS mode, the adapter maps entities to the REST API's narrower shape: extra properties are serialized into descriptions, outbound edges are encoded in a `ccg-edges` text block, and documents are written both as long-term entities and short-term messages. The README says native relationship writes, arbitrary Cypher writes, GDS, and preference/fact features are unavailable or reduced on that REST path. [client template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/context_graph_client.py.j2) · [memory adapter](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/memory_adapter.py.j2) · [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md)

**Updates and deletion.** The inspected message wrapper and adapter do not establish a general correction, supersession, or per-record deletion workflow. The Bolt client exposes whole-database reset; NAMS behavior is limited by the service REST surface. A full purge guarantee across service storage, imports, derived files, and backups was not established by these sources. [memory template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/memory.py.j2) · [client template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/context_graph_client.py.j2) · [memory adapter](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/memory_adapter.py.j2)

**Retrieval.** The README describes session context retrieval (messages, entities, preferences, traces), domain-specific Cypher agent tools, graph exploration, and a decision-trace viewer. Generated clients can return Cypher results for graph display. Retrieval ranking, answer grounding, and abstention are delegated to generated code and memory backend behavior; this review did not measure them. [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md) · [memory template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/memory.py.j2) · [client template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/context_graph_client.py.j2)

## Scope isolation

The wrapper passes a session or NAMS-created conversation ID to memory calls, and the app config includes a domain identifier. The client applies domain predicates in selected graph operations, while also providing arbitrary Cypher execution in Bolt mode; the inspected sources do not establish that every read/write is tenant-filtered or that domain labels form a security boundary. NAMS workspace isolation and access control are service-side and were not audited. [memory template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/memory.py.j2) · [client template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/context_graph_client.py.j2) · [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md)

## Provenance and evidence

The documented reasoning-memory structure retains thought/action/observation steps and causal relationships; data imports and conversation records can also be presented in the generated graph. These structures provide source-visible trace records, but do not by themselves verify that a recalled fact is supported or that a generated answer cites the right evidence. [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md) · [ontology](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/ontology.py)

## Efficiency and observability

The README documents provider selection for entity extraction and embeddings, with a local sentence-transformers default for Bolt and server-managed embeddings on NAMS unless overridden. The source logs memory connection/write errors, exposes an error category to the app, and uses an event collector to stream tool activity and graph results to the UI. These are code/documentation observations; no latency, token, cost, storage, reliability, or telemetry measurements were made. [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md) · [memory template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/memory.py.j2) · [client template](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/src/create_context_graph/templates/backend/shared/context_graph_client.py.j2)

## Metric-domain evidence

All domains below are **unmeasured**. The shared fixture and execution status describe the project evaluation protocol and status only; they are not results. [METRICS.md](../METRICS.md) · [execution status](../results/initial-baselines-status.json) · [fixture](../fixtures/memory-benchmark-v1.json)

## Limitations and unknowns

This selected-source review covers the scaffolder README, ontology and generation flow, and shared memory/client templates. It did not inspect every generated agent framework, route, connector, query template, or NAMS service implementation. The sources do not establish practical recall quality, abstention behavior, per-record correction/deletion guarantees, tenant isolation, evidence support, or resource use. The README calls the project experimental and unsupported; generated output and backend versions/configuration may change those behaviors. [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md) · [METRICS.md](../METRICS.md)

## Contact

The official pinned [README](https://github.com/neo4j-labs/create-context-graph/blob/926e3b3e7a2d3318f94e8a2cc5196677046bbe6d/README.md) was checked for an email address. It directs help requests to GitHub Issues and the Neo4j Community Forum and publishes no contact email; no address was inferred from commit or profile metadata.

## Benchmark status

**Not run.** No Create Context Graph runtime, benchmark, or test was run for this review. See [project metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and the [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and pinned URLs are recorded in [create-context-graph.json](../data/system-reviews/create-context-graph.json). The [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/create-context-graph.md) supports identity and locator attribution only.
