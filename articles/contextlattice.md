# ContextLattice — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 148 — ContextLattice / `contextlattice`  
**Listed repository:** [sheawinkler/ContextLattice](https://github.com/sheawinkler/ContextLattice)  
**Canonical upstream:** same repository; default branch `main`; reviewed head [087f89365508e601a4fb0101fd5bcc6d5e7fac3e](https://github.com/sheawinkler/ContextLattice/commit/087f89365508e601a4fb0101fd5bcc6d5e7fac3e)  
**Review time:** 2026-11-25 09:03:52 UTC (2026-11-25 01:03:52 PST; America/Los_Angeles)

## Identity and scope

The curated catalog lists ContextLattice at ordinal 148, slug `contextlattice`, with an explicit repository locator. Its pinned Atlas entry is retained only as roster attribution for identity and locator context; it is not evidence for this assessment.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/contextlattice.md)]

The official repository page identifies `main` as the default branch. GitHub’s official main Atom feed reports full head `087f89365508e601a4fb0101fd5bcc6d5e7fac3e`, updated 2026-11-24T09:35:24Z. The inspected README and source links below pin that commit.[[repository](https://github.com/sheawinkler/ContextLattice)] [[main commit feed](https://github.com/sheawinkler/ContextLattice/commits/main.atom)] [[reviewed head](https://github.com/sheawinkler/ContextLattice/commit/087f89365508e601a4fb0101fd5bcc6d5e7fac3e)]

## Summary and architecture

ContextLattice presents itself as a local-first context and memory layer for coding agents, with a CLI as the primary interface and a dashboard, HTTP, and MCP integration surfaces. The README describes reopening a mission from durable state, selecting evidence into bounded context packs, transporting signed context, and recording outcomes. It says the live application path is Go and Rust; Python remains in tooling rather than the live request path.[[README](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/README.md)]

The Go gateway’s memory store models records with project, file and topic path, agent and session identifiers, tags, summary, content hash/reference, data class, lifecycle, storage tier, object ID, horizon, confidence, timestamps, source, task attribution, and structured references. This is a project/file-oriented memory lane; a separate temporal-claim store represents subject-predicate-object claims with validity times, status, provenance, verification, evidence/support and opposition, supersession, contradiction, and causal links.[[memory store](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_store.go)] [[claim model](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/temporal_claim_graph.go)]

The README describes a gateway path that validates and durably stores writes before asynchronous fanout, and a retrieval path that merges available sources into a bounded response with provenance and degradation information. This review inspected representative Go gateway code, not every Rust service, adapter, or integration lane.[[README](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/README.md)] [[memory store](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_store.go)]

## Write, update, delete, and retrieval

**Write.** The README documents `contextlattice remember` as a save path and describes validated durable persistence before fanout. In the gateway memory model, stored events include project/file identity, content hash/reference, lifecycle, source and optional task attribution; the store has separate paths and policies for history and current state.[[README](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/README.md)] [[memory store](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_store.go)]

**Update and correction.** The inspected v1 update handler fetches the prior memory payload, overlays fields from a patch, and writes the resulting project/file content. The claim model can represent superseding or contradicting claims and carries validity/status fields. These source structures do not establish correction accuracy or that every retrieval lane suppresses stale material.[[v1 update handler](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_v1.go)] [[claim model](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/temporal_claim_graph.go)]

**Delete and retirement.** The inspected lifecycle helpers treat retired, superseded, retracted, ephemeral, and test records as hidden from ordinary surface-by-default behavior; a tombstone is represented by a `memory_tombstone` data class. This supports logical lifecycle filtering, but the reviewed paths do not establish physical erasure from history, content-addressed blobs, indexes, backups, or all integrations. No general hard-delete handler was inspected.[[lifecycle rules](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_lifecycle.go)] [[memory store](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_store.go)]

**Retrieval.** The inspected current-state search requires a non-empty project and query, scores lexical overlap and topic coverage, and can fill sparse exact-topic results from the nearest topic ancestor. Its comments and code specify that this fallback stays within the selected project and does not widen to a project-wide scan. It is a current-state lane; historical `as_of` reads use temporal paths. The README describes broader retrieval over available sources, which was not exhaustively traced here.[[current-state search](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_current_state_search.go)] [[README](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/README.md)]

## Scope isolation

The reviewed current-state search returns no results without a project and confines the exact-topic/ancestor fallback to that project. The README also presents project-scoped context use. These observations cover the inspected lane and documented usage; they do not establish that every provider, vector adapter, MCP surface, configuration, or caller enforces tenant/user isolation consistently. No cross-project isolation workload was run.[[current-state search](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_current_state_search.go)] [[README](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/README.md)]

## Provenance and evidence

Memory records can retain source, agent/session metadata, content hashes/references, task attribution, and structured references. Temporal claims have explicit support and opposition evidence items, with fields for reference IDs, memory IDs or URIs, content hashes, excerpts, observed time, and admission information. The README describes returned source receipts and coverage/degradation information. These are provenance mechanisms in the source model; they do not demonstrate that generated factual claims are always supported by retained sources.[[memory store](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_store.go)] [[claim model](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/temporal_claim_graph.go)] [[README](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/README.md)]

## Efficiency and observability

The Go current-state search applies project/topic scoping and bounded ranking inputs; the memory store config includes limits for startup history reads, scans, rollups, and caches. The README describes bounded context packs and asynchronous index fanout. A graph telemetry endpoint reports document/edge counts, connectedness and isolation, edge classes, graph quality, recommendations, and storage metadata. These implementation features do not provide latency, token, cost, or storage-efficiency measurements for this review.[[current-state search](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_current_state_search.go)] [[memory store](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_store.go)] [[graph telemetry](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_graph_telemetry.go)] [[README](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/README.md)]

## Metric-domain evidence

All project metric domains remain unmeasured for this review. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).

- **Answerable retrieval accuracy and abstention — unmeasured.** A lexical scoring path and response/evidence surfaces are visible in code, but no adjudicated answerability or abstention workload was run.[[current-state search](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_current_state_search.go)] [[metrics](../METRICS.md)]
- **Correction accuracy and stale-value rate — unmeasured.** Patch update and claim supersession/validity mechanisms exist, but no correction probes were run.[[v1 update handler](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_v1.go)] [[claim model](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/temporal_claim_graph.go)]
- **Deletion leakage — unmeasured.** Lifecycle filtering and tombstones are present; no post-delete probes or checks across retained copies were performed.[[lifecycle rules](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_lifecycle.go)] [[metrics](../METRICS.md)]
- **Scope isolation — unmeasured.** Project filtering is explicit in the inspected search lane, but no cross-project or cross-user workload was run.[[current-state search](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_current_state_search.go)] [[metrics](../METRICS.md)]
- **Evidence support and citation coverage — unmeasured.** Provenance and claim evidence structures exist, but generated answers were not adjudicated for support or citation correctness.[[claim model](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/temporal_claim_graph.go)] [[metrics](../METRICS.md)]
- **Retrieval latency — unmeasured.** No retrieval timing distribution was collected.[[metrics](../METRICS.md)]
- **Write-to-recall delay — unmeasured.** No timed write-then-recall workload was run.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)]
- **Tokens and cost — unmeasured.** No provider usage or cost accounting was performed.[[metrics](../METRICS.md)]
- **Storage efficiency — unmeasured.** The source shows history, current-state, and optional content-blob storage structures; no corpus size or per-item measurement was collected.[[memory store](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/services/gateway-go/memory_store.go)] [[metrics](../METRICS.md)]

## Limits and unknowns

The inspection covered the official README and representative Go gateway files for memory storage, v1 update, lifecycle filtering, current-state search, temporal claims, and graph telemetry. It did not inspect every retrieval adapter, HTTP/MCP integration, Rust component, configuration profile, or end-to-end error path. README capability statements are project documentation, not independent runtime verification. The available source review cannot establish recall quality, correction behavior across all lanes, complete deletion, tenant isolation, evidence support, operational reliability, or measured performance. No ContextLattice runtime, tests, or benchmarks were run.[[README](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/README.md)] [[metrics](../METRICS.md)]

## Contact

The official pinned README was checked for a published contact email and contains none. Contact was not inferred from commit/profile metadata or third-party directories.[[README](https://github.com/sheawinkler/ContextLattice/blob/087f89365508e601a4fb0101fd5bcc6d5e7fac3e/README.md)]

## Benchmark status

**Benchmark not run.** No ContextLattice runtime, tests, or benchmarks were run for this source review. Source observations and upstream documentation claims are not project benchmark results. See [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [result status](../results/initial-baselines-status.json).
