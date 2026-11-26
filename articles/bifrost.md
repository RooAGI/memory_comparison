# Bifrost source review

## Identity and review pin

**System:** Bifrost  
**Curated ordinal / slug:** 92 / bifrost  
**Listed repository locator:** https://github.com/MegaWiz-Dev-Team/Bifrost  
**Canonical repository:** https://github.com/MegaWiz-Dev-Team/Bifrost  
**Default branch / reviewed head:** main / 936957b350091997c34380ffdd91b395d47225ae  
**Reviewed at:** 2026-11-24 23:31:32 UTC (15:31:32 PST; America/Los_Angeles)  
**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run

The curated roster identifies Bifrost at ordinal 92 and attributes its entry to the cited Atlas source revision. The official repository page identifies main; its current commits feed and a fresh read-only git ls-remote --symref both identify the full reviewed head above. The roster is used only for identity and attribution; Atlas descriptions, marks, and layout are not assessment evidence.[[roster](../data/memory-systems.json)] [[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/bifrost.md)] [[repository](https://github.com/MegaWiz-Dev-Team/Bifrost)] [[main feed](https://github.com/MegaWiz-Dev-Team/Bifrost/commits/main.atom)] [[reviewed head](https://github.com/MegaWiz-Dev-Team/Bifrost/commit/936957b350091997c34380ffdd91b395d47225ae)]

## Summary

Bifrost is a Rust/Axum agent runtime with a small Memvid-backed conversation-memory path. At the reviewed source, each completed orchestration appends a query/answer frame to a local capsule; a tool can search a tenant/session capsule. The findings below are code and documentation observations. Quality, isolation, latency, and cost have not been benchmarked.[[README](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/README.md)] [[manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)] [[overseer](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/swarm_engine/overseer.rs)]

## Who and what

The official README describes Bifrost as a self-hosted agent runtime in the Asgard platform. The public repository is owned by the MegaWiz-Dev-Team GitHub organization; no individual maintainer identity is asserted. This review concerns its conversation-memory slice, not the full orchestration platform.[[README](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/README.md)] [[repository](https://github.com/MegaWiz-Dev-Team/Bifrost)]

## Architecture and data model

**Documentation observation.** The README describes a Rust/Axum runtime, a MemvidManager, .mv2 files, and Qdrant, Neo4j, and PageIndex retrieval components. It says each agent receives an independent file. The inspected integration differs: the current Overseer passes tenant_id into the manager's agent_id parameter, so its actual Memvid key uses tenant and session.[[README](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/README.md)] [[manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)] [[overseer](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/swarm_engine/overseer.rs)]

**Code observation.** The manager creates or opens agent_<id>_session_<id>.mv2 under MEMVID_DATA_DIR (default data/agents). It writes UTF-8 text with an optional title through Memvid put_bytes_with_options, then commits. The manager adds no separate frame schema, patient metadata, source citation, or provenance record.[[manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)] [[runtime setup](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/main.rs)]

A second, short-term layer stores JSON conversation history in swarm_checkpoints.state_json, keyed by tenant and a patient-prefixed session identifier when a patient is present. The design note says this full history is loaded every turn without truncation. The patient prefix is not used for the Memvid capsule key.[[overseer](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/swarm_engine/overseer.rs)] [[memory design note](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/docs/design/agent-memory-evolution.md)]

## Write, update, delete, and retrieval

**Write — code observation.** After orchestration, the Overseer formats the original user query and final answer into a text frame, titles it with session and current time, and calls commit_memory with tenant ID and raw session ID (or anon). The write appends and commits. A commit error is logged while the response still returns. This frame path uses the original query, while other paths use a scrubbed query value.[[overseer](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/swarm_engine/overseer.rs)] [[manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)]

**Update and delete — code observation.** The inspected manager and tool expose no per-frame correction, deletion, retention, or erasure operation. The design note describes frames as append-only and names the missing prune/delete path; its suggested frame deletion, vacuum, redaction, and stronger ACL enforcement remain proposals in that note.[[manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)] [[search tool](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/tool.rs)] [[memory design note](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/docs/design/agent-memory-evolution.md)]

**Retrieval — code observation.** The search tool accepts a query and has its capsule identifiers bound when constructed. It requests five hits with 200-character snippets. Memvid search is called with no URI or scope filter, no time boundary, and ACL enforcement in Audit mode. Missing capsules return an empty result. The tool formats only hit title and text, omitting returned elapsed time, engine, and count metadata.[[search tool](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/tool.rs)] [[manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)]

The Overseer attaches the search tool on the regular tool-calling path; bypass providers search directly and add hits to manual context. At both read and write call sites, the argument occupying the manager's agent_id slot is tenant ID, not the request agent ID.[[overseer](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/swarm_engine/overseer.rs)]

**Scope and isolation — code observation.** Capsules are keyed by tenant and session, not by agent or patient. Different agents in the same tenant/session address the same capsule; missing sessions share the tenant's anon capsule. Memvid search supplies scope=None and Audit-mode ACL handling. The inspected path therefore does not show patient-level or per-agent Memvid isolation. SQL checkpoints separately include tenant and patient-prefixed session scope.[[manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)] [[overseer](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/swarm_engine/overseer.rs)] [[memory design note](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/docs/design/agent-memory-evolution.md)]

**Provenance and evidence — code observation.** A frame preserves query/answer text and a generated title, but the inspected write path supplies no message ID, patient tag, source-document ID, citation, confidence, or mutation history. Search returns text and title, not a source locator. This shows stored content, not whether a later answer is supported by external evidence.[[overseer](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/swarm_engine/overseer.rs)] [[manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)] [[search tool](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/tool.rs)]

**Source-visible efficiency and observability.** Search bounds hits and snippet length; the Memvid response includes an elapsed-time field and engine metadata, but the tool discards these fields. The runtime has tracing spans, orchestration-latency logs, search query logs, and a log path for memory write failures. These are source-visible implementation details, not measured performance. The design note also describes full checkpoint-history loading and warns of growth in prompt size; its compaction proposal is not implemented evidence.[[manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)] [[search tool](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/tool.rs)] [[overseer](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/swarm_engine/overseer.rs)] [[runtime setup](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/main.rs)] [[memory design note](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/docs/design/agent-memory-evolution.md)]

## Metric-domain evidence

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Search API exists; no answerable workload inspected. | Unmeasured |
| Correction and stale values | No correction path found in inspected manager/tool. | Unmeasured |
| Deletion leakage | No erasure path wired in inspected manager/tool. | Unmeasured |
| Scope isolation | Tenant/session file naming; search uses no scope filter and Audit ACL mode. | Unmeasured |
| Evidence support and citations | Stored query/answer pair without source citations. | Unmeasured |
| Latency and write-to-recall delay | Search returns elapsed time; no measurement collected here. | Unmeasured |
| Tokens, cost, and storage | No runtime usage or growth measurements collected. | Unmeasured |
| Source-visible efficiency and observability | Bounded top-k/snippets, timing field, tracing/logging paths. | Code observation only |

The metric domains are based on the project protocol. Source structure and available telemetry do not constitute measured results.[[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[baseline status](../results/initial-baselines-status.json)]

## Limits and unknowns

This was a bounded review of the pinned README, manager, tool, orchestration call sites, runtime initialization, and memory design note. The runtime, tests, and benchmark fixture were not run. Memvid internals, full deployment authorization, backup/replica retention, actual cross-tenant behavior under deployment, and production performance were not independently audited.

The README's per-agent capsule statement and claimed sub-millisecond retrieval are documentation claims; the inspected call path uses tenant/session values, and this review collected no timing result. The catalog was used only for identity and source attribution; its assessment content was not used.[[README](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/README.md)] [[manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)] [[roster](../data/memory-systems.json)]

## Benchmark status

**Benchmark not run.** No Bifrost runtime, tests, or benchmark workload was executed. The project metric definitions, fixture, and initial-baseline status record are linked for future protocol reference only; they contain no measured Bifrost result from this review.[[metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[baseline status](../results/initial-baselines-status.json)]

## Sources

- [Repository and default branch](https://github.com/MegaWiz-Dev-Team/Bifrost)
- [Reviewed full head](https://github.com/MegaWiz-Dev-Team/Bifrost/commit/936957b350091997c34380ffdd91b395d47225ae)
- [Current main commits feed](https://github.com/MegaWiz-Dev-Team/Bifrost/commits/main.atom)
- [README](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/README.md)
- [SECURITY.md — published contact](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/SECURITY.md)
- [Memory manager](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/memvid_manager.rs)
- [Memory search tool](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/memory/tool.rs)
- [Overseer memory integration](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/swarm_engine/overseer.rs)
- [Memory evolution design note](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/docs/design/agent-memory-evolution.md)
- [Runtime initialization](https://github.com/MegaWiz-Dev-Team/Bifrost/blob/936957b350091997c34380ffdd91b395d47225ae/src/main.rs)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Initial baseline status](../results/initial-baselines-status.json)
- [Curated catalog](../data/memory-systems.json)
