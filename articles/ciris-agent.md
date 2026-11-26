# CIRIS Agent

## Identity and review pin

- **System:** CIRIS Agent
- **Curated position:** 119
- **Slug:** `ciris-agent`
- **Listed repository:** [CIRISAI/CIRISAgent](https://github.com/CIRISAI/CIRISAgent)
- **Canonical repository at review:** [CIRISAI/CIRISAgent](https://github.com/CIRISAI/CIRISAgent)
- **Default branch:** `main`
- **Reviewed head:** [`55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a`](https://github.com/CIRISAI/CIRISAgent/commit/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a)
- **Reviewed:** 2026-11-25 07:57:01 UTC (2026-11-24 23:57:01 PST; America/Los_Angeles)
- **Review status:** Reviewed from current source and documentation
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [pinned Atlas report](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ciris-agent.md), used only for curated identity, listed repository, and roster attribution.

The local catalog places CIRIS Agent at position 119 with slug `ciris-agent`, the listed repository `https://github.com/CIRISAI/CIRISAgent`, explicit repository status, and a pinned Atlas report for attribution.[[catalog]][[atlas]] The official GitHub repository page identifies `main` as the default branch, and its commit history shows latest commit `55a2447`; `git ls-remote` and a shallow checkout both resolved `main` to full SHA `55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a`.[[repo]][[history]][[head]] GitHub's unauthenticated REST endpoint was rate-limited during this check; the branch page, read-only Git ref lookup, and checked-out HEAD supplied the branch and revision evidence.[[api_limit]][[history]][[head]]

## Summary

CIRIS Agent is an open-source assistant and agent framework whose memory is a typed graph exposed through a memory service and action bus. The checked-in Python service delegates persistent node and edge operations to the `ciris-persist` engine; nodes are keyed by identifier and scope, while agent actions provide explicit memorize, recall, and forget workflows.[[readme]][[architecture]][[memory_service]][[persist]]

## Who and what

The official repository describes a self-hostable assistant and framework, with desktop, API, and adapter use cases. The reviewed memory code is a local graph-memory service integrated with CIRIS's typed action pipeline; the repository organization is CIRISAI. This review does not infer individual maintainers from commit metadata.[[readme]][[repo]]

## Architecture and data model

CIRIS models graph nodes with an `id`, `type`, `scope`, typed or JSON attributes, version, updater, and update timestamp. Attributes can carry content, creator, timestamps, tags, and node-specific data. Edges carry source and target identifiers, relationship, scope, optional weight, and context attributes. The graph scopes are LOCAL, IDENTITY, ENVIRONMENT, and COMMUNITY.[[graph_schema]][[operations]]

The current persistence adapter maps those objects to the `ciris-persist` engine rather than issuing graph-table SQL directly. It reads an existing node, merges new attributes over the existing attribute map, increments the expected version, and calls the engine's upsert. Node lookup and deletion use the composite identity of node ID and scope. The repository's persistence documentation lists SQLite and PostgreSQL as supported storage backends; this review did not verify backend-specific behavior.[[persist]][[memory_service]][[persist_docs]]

## Write, update, delete, and retrieval

**Writing and updates.** The MEMORIZE handler validates typed parameters and sends writes through the memory bus. User-node writes pass consent and managed-attribute checks; identity changes require Wise Authority authorization and use a distinct amendment path. The memory service processes secret-bearing attributes before storage. On an existing node, persistence merges attributes and advances the version using optimistic concurrency; the code does not show a separate immutable version-history table for prior node contents.[[memorize]][[memory_service]][[persist]]

**Deletion.** FORGET checks Wise Authority authorization for IDENTITY and ENVIRONMENT scope, then delegates to the memory service. The persistence adapter requests a hard node deletion; its comment states that the persistence engine cascades deletion to connected edges. A successful handler operation reports completion. The checked code does not establish deletion from backups, synchronized databases, or other external copies.[[forget]][[memory_service]][[persist]]

**Retrieval.** RECALL first attempts an exact node-ID lookup within the selected scope, then falls back to the memory service's search if no exact result is found. Wildcard recall can list a bounded number of nodes by scope and type, and callers may request connected nodes through bounded graph traversal. Text search fetches up to its requested limit (100 by default), then matches case-insensitive substrings against node IDs and serialized attributes; the inspected implementation does not rank by semantic similarity or relevance score. Secrets are processed for recall/search before returning nodes.[[recall]][[memory_service]][[graph_schema]][[search_filters]]

## Scope isolation

The graph store applies scope as a filter on exact lookups, enumeration, and search; the persistence adapter queries by node ID and scope. The four scopes classify memory domains, and the handler adds explicit Wise Authority checks for identity and environment operations. These mechanisms establish scope-aware access in the inspected paths, but the reviewed memory-service contract does not take a user/principal identity as a query predicate. The sources inspected here therefore do not establish per-user or tenant isolation for multiple principals sharing one agent database; the deployment's actual isolation boundary was not exercised.[[graph_schema]][[persist]][[recall]][[memorize]][[forget]]

## Provenance and evidence

Nodes have a version, updater, update timestamp, and attributes that can include `created_by`, `created_at`, and tags; edges can retain relationship context. The project also documents a cryptographically signed, hash-chained audit trail for agent decisions. These provide some object and action lineage, but the reviewed graph contract does not require source URLs, quoted evidence spans, trust labels, or citation checks for ordinary memory nodes. The decision audit description does not establish an immutable history of every prior memory value.[[graph_schema]][[readme]][[audit]]

## Efficiency and observability

Exact lookup is keyed by node ID and scope. Search enumerates a bounded set of nodes and applies substring checks in Python, so the source path makes no claim of vector or full-text index ranking. The memory service exposes node count, operation count, database-size, uptime, and secret-service metrics. Its current custom metric implementation leaves edge count at zero because the persistence engine has no cheap edge-count helper; database file size is only observed when the configured database path exists as a local file. These are code observations, not measured performance results.[[memory_service]][[persist]]

## Metric-domain evidence

All quality and efficiency domains are **unmeasured** in this review. The source mechanisms and project evaluation definitions are not CIRIS Agent benchmark results.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Exact lookup and bounded substring search exist; no answerability or abstention probes were run. | Unmeasured |
| Correction accuracy and stale values | Updates merge attributes and increment a version; no correction sequence was scored. | Unmeasured |
| Deletion leakage | The inspected path performs a hard node delete with edge cascade; no residual-copy or post-delete probes were run. | Unmeasured |
| Scope isolation | Queries are scope-filtered and some writes/deletes require Wise Authority authorization; no multi-principal workload was run. | Unmeasured |
| Evidence support and citation coverage | The graph has metadata and decision audit mechanisms; no evidence adjudication was run. | Unmeasured |
| Retrieval latency and write-to-recall delay | The source path was inspected but not timed. | Unmeasured |
| Tokens, cost, and storage | Metrics include operation counts and a local database-size field; no resource measurements were collected. | Unmeasured |

The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) define evaluation work and project-wide status, not CIRIS Agent measurements.[[metrics]][[fixture]][[status]]

## Limitations and unknowns

This is a bounded review of selected documentation and current source at the verified head. It does not establish runtime behavior, behavior of the external `ciris-persist` engine beyond the adapter contract, backup/sync retention, access-control behavior outside the inspected action paths, or production isolation between principals.

The inspected text search is substring matching over a bounded node list, with no semantic ranking in this service path. Update code merges values and advances a version, but no prior-value history is established by these files. The decision audit trail is documented separately and should not be treated as proof that every memory content change is recoverable. No request-level search, correction, deletion, isolation, latency, token, cost, or storage measurement was run.[[memory_service]][[persist]][[audit]][[metrics]]

## Benchmark status

**Benchmark not run.** I did not execute CIRIS Agent, its tests, or any benchmark workload. No runtime quality, latency, token, cost, storage, correction, deletion, or scope-isolation result is claimed.

## Contact

The pinned official [SECURITY.md](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/SECURITY.md) publishes `info@ciris.ai` for vulnerability reports. This address was taken from official repository documentation, not commit or profile metadata.[[security]]

## Sources

- [Curated roster](../data/memory-systems.json) — position, slug, listed repository, and Atlas attribution only.
- [Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ciris-agent.md) — identity/locator attribution only.
- [Official repository](https://github.com/CIRISAI/CIRISAgent) — canonical repository and default branch.
- [Official main commit history](https://github.com/CIRISAI/CIRISAgent/commits/main) — latest visible main commit short SHA and date.
- [GitHub API current main endpoint](https://api.github.com/repos/CIRISAI/CIRISAgent/commits/main) — request was rate limited during this review; not relied upon for the head SHA.
- [Reviewed head](https://github.com/CIRISAI/CIRISAgent/commit/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a) — full reviewed commit SHA.
- [README](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/README.md) — product overview, deployment, framework, and decision-audit claims.
- [Architecture overview](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ARCHITECTURE_OVERVIEW.md) — graph memory and service architecture.
- [Graph node and edge schema](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ciris_engine/schemas/services/graph_core.py) — scopes and typed graph objects.
- [Memory operation schemas](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ciris_engine/schemas/services/operations.py) — operation results and recall query.
- [Memory search filters](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ciris_engine/schemas/services/graph/memory.py) — search filter fields.
- [Graph memory service](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ciris_engine/logic/services/graph/memory_service.py) — writes, exact/wildcard recall, search, secret processing, traversal, and custom metrics.
- [Persistence adapter](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ciris_engine/logic/persistence/models/graph.py) — scoped reads, merged upserts, version handling, and hard deletion.
- [Persistence documentation](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ciris_engine/logic/persistence/README.md) — documented SQLite/PostgreSQL backend choices.
- [RECALL handler](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ciris_engine/logic/handlers/memory/recall_handler.py) — exact lookup and search fallback.
- [MEMORIZE handler](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ciris_engine/logic/handlers/memory/memorize_handler.py) — consent, authorization, and write workflow.
- [FORGET handler](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ciris_engine/logic/handlers/memory/forget_handler.py) — authorization and deletion workflow.
- [Audit service overview](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/ciris_engine/logic/services/graph/audit_service/README.md) — documented signed audit chain.
- [Security policy](https://github.com/CIRISAI/CIRISAgent/blob/55a2447a61a84fa2d9fa70f4495b7a41f8e38d2a/SECURITY.md) — published contact email.
- [Project metrics](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) — metric definitions and status only.

**Verification boundary:** read-only source and documentation review at the checked-out full SHA; no CIRIS Agent runtime, tests, or benchmarks were run.
