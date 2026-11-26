# Hermes Memory Installer source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 291 / Hermes Memory Installer / hermes-memory-installer  
**Listed repository locator:** [mage0535/hermes-memory-installer](https://github.com/mage0535/hermes-memory-installer)  
**Canonical repository:** [mage0535/hermes-memory-installer](https://github.com/mage0535/hermes-memory-installer)  
**Default branch / reviewed head:** main / `049d9ac628e516da2462cf7bada5460aec3d62a3`  
**Review time:** 2026-11-25 22:53:32 UTC (14:53:32 PST; America/Los_Angeles).

## Identity and scope

The project catalog places Hermes Memory Installer at ordinal 291 with slug `hermes-memory-installer`, listed repository `https://github.com/mage0535/hermes-memory-installer`, and an Atlas attribution pinned to `049d9ac628e516da2462cf7bada5460aec3d62a3`. Atlas is used here only to record the curated roster identity and locator. The official GitHub repository page identifies `main` as the default branch; official Git transport reports `main` at the full SHA above, and a shallow checkout resolved to the same SHA. The review is pinned to that current head.[[roster](../data/memory-systems.json)] [[repository](https://github.com/mage0535/hermes-memory-installer)] [[current main commits](https://github.com/mage0535/hermes-memory-installer/commits/main.atom)] [[reviewed commit](https://github.com/mage0535/hermes-memory-installer/commit/049d9ac628e516da2462cf7bada5460aec3d62a3)]

## Summary and project type

Hermes Memory Installer packages an agent-agnostic memory sidecar. It reads an agent data home and session records, indexes and archives context into external stores, retrieves from local and remote memory layers, and writes generated recall context for later agent use. The README names PostgreSQL, Hindsight and gbrain as required external services for the described deployment; the repository supplies Python scripts, configuration, installer, evaluation, governance and operator tooling rather than replacing the agent runtime.[[README](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/README.md)] [[architecture](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/ARCHITECTURE.md)]

## Architecture and data model

The documented layers are the agent's hot local context, Hindsight for warm facts and observations, and a cold layer combining archived sessions and gbrain pages, with a separate curated Markdown knowledge index. The README and architecture guide describe query-family routing, candidate retrieval from layers, reciprocal rank fusion, reranking, and context generation. Embeddings are optional; keyword and full-text paths remain available without them.[[readme](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/README.md)] [[architecture](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/ARCHITECTURE.md)] [[retrieval](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/tiered_context_injector.py)]

The governance rebuild maintains SQLite tables for session rows, Hindsight facts, hubs, canonical memory objects, and curated notes, with corresponding FTS5 indexes. A canonical memory object includes a stable ID, type/entity type, title/summary, entities and hub IDs, source references, status, confidence/freshness, validity dates, version and conflict-group tags, and indexed text. Fact-derived objects retain Hindsight IDs and session tags; session-derived objects retain session IDs. The rebuild normalizes and aggregates source rows into these derived indexes; these are index records, not the source-of-truth stores.[[rebuild](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_governance_rebuild.py)]

## Write, update, delete, and retrieval

**Write and archive.** The sidecar is not the primary fact-write service: the inspected rebuild reads existing agent state and Hindsight memories and derives local index rows. The session archiver parses session files, checkpoints processed sessions, and creates or updates corresponding gbrain pages and timeline/link data through the gbrain CLI or MCP transport. Thus session archival and indexing are sidecar writes, while durable fact creation is delegated to configured agent/Hindsight components.[[rebuild](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_governance_rebuild.py)] [[session archive](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/session_to_gbrain.py)] [[README](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/README.md)]

**Update and deletion.** Rebuild clears and repopulates its derived session, Hindsight, hub, object, and FTS tables, so source changes and removals can be reflected by a later rebuild; this is index refresh behavior, not a general user-facing memory delete API. The code preserves original session data, and the policy layer stores additive validity and supersession metadata. Policy injection and confidence decay default to dry-run; `--apply` is required to persist proposals. Decay marks eviction candidates but does not delete source memories. The inspected paths do not establish deletion or erasure across Hindsight, gbrain, agent state, backups, or replicas.[[rebuild](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_governance_rebuild.py)] [[policy](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/governance/policy.py)] [[policy injection](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/governance/inject_policy.py)] [[architecture](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/ARCHITECTURE.md)]

**Retrieval.** The context injector combines recent session context, indexed session search, governance layers, and optional live Hindsight recall. Candidate lists are fused with reciprocal-rank contributions and reranked; the selected context is atomically written to configured Markdown outputs. Query-family rules and keyword evidence affect which layers are consulted. The repository includes optional embedding synchronization and canonical semantic search. Code structure does not establish retrieval accuracy or that an agent consumes every generated context file.[[retrieval](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/tiered_context_injector.py)] [[family routing](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_family_registry.py)] [[semantic index](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_governance_rebuild.py)]

## Scope isolation

The sidecar uses `AGENT_HOME` (with documented compatibility fallbacks) for local state and configuration, and provides profile isolation checks and a two-profile soak script. Those mechanisms can separate local files when configured with distinct homes. Hindsight's bank defaults to `hermes`; the inspected Hindsight index records fact and session IDs but no general principal/tenant authorization field. A shared remote service therefore needs deployment-level access controls, and the presence of isolation scripts is not a measured isolation guarantee.[[README](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/README.md)] [[rebuild](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_governance_rebuild.py)] [[profile isolation](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/profile_isolation_check.py)] [[isolation soak](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/profile_isolation_soak.py)]

## Provenance and evidence

Canonical objects retain source-reference IDs pointing to Hindsight memories or sessions, while policy metadata records a source layer, sanitized provenance string, fact key, conflict group, validity dates and supersession link. Session archival also stores source session identity in the created page. These support tracing back to source records; they do not by themselves guarantee claim-level citation support in answers or human review of ingested material.[[rebuild](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_governance_rebuild.py)] [[policy](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/governance/policy.py)] [[session archive](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/session_to_gbrain.py)]

## Efficiency and observability

The source shows batched inserts during rebuild, FTS5 indexes for lexical search, optional embedding batches, a bounded recall refresh queue, and cached governance queries. Instrumentation includes recall metrics and rollups, synthetic/private evaluation reports, health artifacts, acceptance checks, OpenMetrics, dashboards, and SLO summaries. These are implementation and operational affordances; no production telemetry, latency, token usage, cost, or storage measurements were collected for this review.[[rebuild](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_governance_rebuild.py)] [[retrieval](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/tiered_context_injector.py)] [[metrics and adapters](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/memory_eval/metrics.py)] [[README observability](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/README.md)] [[operations report](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/memory_ops/report.py)]

## Metric-domain evidence

All domains below are **unmeasured** for this source review. The repository contains evaluation machinery, but no Hermes Memory Installer run was performed; the project's shared benchmark record remains `not_run`. Code paths are evidence of mechanisms only.[[metrics](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

| Domain | Source evidence and measurement status |
|---|---|
| Answerable recall and abstention | Layered retrieval, filtering and an evaluation adapter exist; no adjudicated system workload or abstention score was run. |
| Correction and staleness | Policy metadata models validity/supersession; no correction sequence or stale-value probe was measured. |
| Deletion | Derived index rebuild and policy inactivity exist; cross-store erasure and deletion-leak rate were not measured. |
| Scope isolation | Local profile tools exist; no forbidden cross-profile probe was run. |
| Provenance and citations | Source references and policy provenance are retained; evidence support precision and citation coverage were not measured. |
| Latency | Recall metric code and SLO tooling exist; no run-specific latency distribution was collected. |
| Write-to-recall delay | Indexing and background schedules exist; no acknowledged write followed by timed recall probes. |
| Tokens and cost | No operation-level token or charge data was collected. |
| Storage | Local and external persistence are described; no attributed byte count or per-item storage measure was collected. |

## Limits and unknowns

This is a bounded inspection of the official README, architecture guide, and selected current implementation at the verified head SHA. The sidecar, its tests, and benchmarks were not run. The review cannot establish runtime reliability, recall correctness, authorization isolation in a deployed Hindsight/gbrain environment, complete erasure in external stores or backups, or operational performance. The README describes operator features and supported configuration; those claims were not independently exercised here.[[README](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/README.md)] [[rebuild](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_governance_rebuild.py)] [[retrieval](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/tiered_context_injector.py)]

## Contact check

I checked the official pinned repository README for a published contact email. It contained no contact email; `contact_email` is recorded as null and the exact checked URL is in the review JSON. No commit/profile metadata, inference, or third-party directory was used.[[README](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/README.md)]

## Benchmark status

**Benchmark not run.** No Hermes Memory Installer runtime, test, or benchmark execution was performed. Project metric definitions and fixtures are evaluation protocol artifacts, not this system's results.[[metrics](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Canonical repository](https://github.com/mage0535/hermes-memory-installer)
- [Reviewed main head](https://github.com/mage0535/hermes-memory-installer/commit/049d9ac628e516da2462cf7bada5460aec3d62a3)
- [README.md](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/README.md)
- [ARCHITECTURE.md](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/ARCHITECTURE.md)
- [scripts/memory_governance_rebuild.py](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_governance_rebuild.py)
- [scripts/tiered_context_injector.py](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/tiered_context_injector.py)
- [scripts/session_to_gbrain.py](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/session_to_gbrain.py)
- [scripts/memory_family_registry.py](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/scripts/memory_family_registry.py)
- [governance/policy.py](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/governance/policy.py)
- [governance/inject_policy.py](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/governance/inject_policy.py)
- [memory_eval/metrics.py](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/memory_eval/metrics.py)
- [memory_ops/report.py](https://github.com/mage0535/hermes-memory-installer/blob/049d9ac628e516da2462cf7bada5460aec3d62a3/memory_ops/report.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster identity and locator](../data/memory-systems.json)

**Verification boundary:** no system, tests, or benchmark workload was run.
