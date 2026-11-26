# CSM

## Identity and review pin

- Catalog ordinal: 173
- System: CSM
- Slug: csm
- Listed repository: https://github.com/NovasPlace/CSM
- Roster attribution: explicit listed repository locator; the pinned Atlas entry is recorded only for curated identity and locator context, not as assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/csm.md)).
- Canonical upstream: https://github.com/NovasPlace/CSM
- Default branch: master
- Reviewed full head: [9c7cfb22e525eb9210c3048cb0d44544b09b95d0](https://github.com/NovasPlace/CSM/commit/9c7cfb22e525eb9210c3048cb0d44544b09b95d0)
- Review timestamp: 2026-11-25T10:14:30Z (UTC; 2026-11-25 02:14:30 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub marks master as the default branch. The official master Atom feed and commit page identify the same full head; the feed reports its latest update as 2026-09-18T00:21:00Z. ([repository](https://github.com/NovasPlace/CSM), [branches](https://github.com/NovasPlace/CSM/branches), [master history](https://github.com/NovasPlace/CSM/commits/master.atom), [head commit](https://github.com/NovasPlace/CSM/commit/9c7cfb22e525eb9210c3048cb0d44544b09b95d0))

## Summary

CSM (Cross-Session Memory) is a local and self-hosted memory and operational-continuity runtime for coding agents. It combines durable memory, project activity records, fresh-session re-entry, context controls and governance. PostgreSQL is the complete feature path; SQLite supports a narrower local core. ([README](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/README.md), [product architecture](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/PRODUCT_ARCHITECTURE.md))

## Architecture and data model

The documented runtime separates host integration, provider-selected storage, durable memory, AgentBook, re-entry, Living State, context control, work continuity and governance. Durable memory handles typed records, text/vector retrieval, relationships, lessons and transcript-derived records. AgentBook uses an append-only project event history with derived summaries, current-state projection and a Markdown front page. ([product architecture](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/PRODUCT_ARCHITECTURE.md), [README](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/README.md))

## Write, update, delete and retrieval

**Write.** Hooks and explicit tools can persist memory. The documented pipeline normalizes and redacts supported content, builds metadata and provenance, writes the durable record, and adds embeddings or relationships when the configured provider supports them. Automatic conversation and full-transcript capture default to enabled. ([product architecture](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/PRODUCT_ARCHITECTURE.md), [privacy and lifecycle](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/DATA_PRIVACY_AND_LIFECYCLE.md))

**Update and duplicate handling.** Memory records can be changed by manager operations. The exact-content merge tool groups active rows by normalized content and memory type, marks duplicate records as superseded and records merge metadata. This duplicate merge is not an immutable version history for every edit. ([memory manager](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/memory-manager-base.ts), [merge implementation](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/merge-tool.ts))

**Delete and retention.** Direct deletion requires a memory ID and active project and hard-deletes the database record plus covered dependent rows. Retention cleanup is explicit and preview-first. Neither operation erases copies already written to generated documents, exports, logs, snapshots, filesystem backups or third-party backups. ([privacy and lifecycle](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/DATA_PRIVACY_AND_LIFECYCLE.md))

**Retrieval.** Hybrid search runs vector, full-text and entity candidate lanes in parallel, then applies ranking and recency signals, content deduplication and a result limit. The README also documents metadata filters, relation traversal and text-only/vector-only fallback paths. ([hybrid search](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/hybrid-search.ts), [README](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/README.md))

## Scope isolation

OpenCode memory and continuity tools are bound to the directory that registered the plugin. Codex MCP memory operations require an explicit project identifier, and customer-facing search/list surfaces force project mode. When a project query has no rows, legacy memories with null project_id may be considered; it does not fall back to another named project. Project IDs are local partitioning, not authentication or hostile multi-tenant authorization. Separate trust domains require separate databases and credentials. ([privacy and lifecycle](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/DATA_PRIVACY_AND_LIFECYCLE.md), [security policy](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/SECURITY.md))

## Provenance and evidence

Saved memory metadata includes source kind, evidence strength, source session, agent, model and surface fields, and a read-only audit reports missing provenance across all and active memories. The security policy still treats imported memories, transcripts, lessons and derived summaries as untrusted until provenance and scope are understood. Metadata supports attribution; it does not guarantee that generated answers are fully supported by retained evidence. ([provenance audit](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/memory-provenance-audit.ts), [security policy](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/SECURITY.md))

## Efficiency and observability

The source executes candidate searches concurrently, bounds the returned results, applies rank and recency scoring, and records recall telemetry. A provenance audit reports coverage gaps and unknown/default model identifiers. These are source-visible mechanisms, not measured latency, token use, cost or storage efficiency. ([hybrid search](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/hybrid-search.ts), [memory manager](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/memory-manager-base.ts), [provenance audit](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/memory-provenance-audit.ts))

## Metric-domain evidence

Every project benchmark domain is **unmeasured** for CSM. No runtime, tests or benchmarks were run. The fixture and metric definitions specify a protocol; the project status record contains no CSM result. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Review evidence |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | No scored answerable/unanswerable probes were run. |
| Correction accuracy and stale-value rate | Unmeasured | No correction workload was tested. |
| Deletion leakage | Unmeasured | No post-deletion probes or backup/export inspection were run. |
| Scope isolation | Unmeasured | No cross-project leakage workload was run. |
| Evidence support and citation coverage | Unmeasured | No claim/citation scoring was run. |
| Retrieval latency | Unmeasured | No timing samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write/recall probes were run. |
| Tokens and cost | Unmeasured | No runtime usage or charges were collected. |
| Storage efficiency | Unmeasured | No corpus-attributed storage size was collected. |

## Limits and unknowns

This bounded review inspected the official README, product architecture, privacy/lifecycle and security documentation, selected memory manager, hybrid-search, duplicate-merge and provenance-audit code, and official GitHub head evidence. It did not inspect every tool, host, storage query, migration or deployment. ([README](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/README.md), [product architecture](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/PRODUCT_ARCHITECTURE.md), [privacy and lifecycle](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/DATA_PRIVACY_AND_LIFECYCLE.md), [memory manager](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/memory-manager-base.ts), [hybrid search](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/hybrid-search.ts))

No CSM runtime, tests or benchmarks were run. Therefore this review does not establish retrieval quality, correction reliability, deletion leakage, cross-project isolation, latency, token or cost totals, or storage efficiency. Runtime behavior also depends on selected database/provider, host configuration, retention settings and operator access controls. ([metric definitions](../METRICS.md), [project status](../results/initial-baselines-status.json), [privacy and lifecycle](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/DATA_PRIVACY_AND_LIFECYCLE.md))

## Contact

No contact email is published in the official pinned README or SECURITY.md. The security policy directs vulnerability reports to GitHub private vulnerability reporting when available. No profile, commit metadata or third-party directory was used. ([README](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/README.md), [SECURITY.md](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/SECURITY.md))

## Benchmark status

**Benchmark not run.** CSM, its tests and benchmark workloads were not run. The project fixture is a workload specification only; it is not a CSM result. ([METRICS.md](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/csm.md)
- [Official repository](https://github.com/NovasPlace/CSM)
- [Default branches page](https://github.com/NovasPlace/CSM/branches)
- [Official master commit feed](https://github.com/NovasPlace/CSM/commits/master.atom)
- [Reviewed full head 9c7cfb22e525eb9210c3048cb0d44544b09b95d0](https://github.com/NovasPlace/CSM/commit/9c7cfb22e525eb9210c3048cb0d44544b09b95d0)
- [Pinned README](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/README.md)
- [Pinned product architecture](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/PRODUCT_ARCHITECTURE.md)
- [Pinned privacy and lifecycle documentation](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/docs/DATA_PRIVACY_AND_LIFECYCLE.md)
- [Pinned security policy](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/SECURITY.md)
- [Pinned memory manager](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/memory-manager-base.ts)
- [Pinned hybrid search](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/hybrid-search.ts)
- [Pinned duplicate merge implementation](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/merge-tool.ts)
- [Pinned provenance audit](https://github.com/NovasPlace/CSM/blob/9c7cfb22e525eb9210c3048cb0d44544b09b95d0/src/memory-provenance-audit.ts)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project execution-status record](../results/initial-baselines-status.json)
