# agentmemory source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 22 / agentmemory / agentmemory  
**Listed repository locator:** [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory)  
**Current canonical repository:** [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory)  
**Default branch / reviewed head:** main / `5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb`  
**Review time:** 2026-11-24 18:55:42 UTC (10:55:42 PST; America/Los_Angeles).

## Identity and scope

The curated order places **agentmemory** at ordinal 22, with slug `agentmemory`, listed repository locator `https://github.com/rohitg00/agentmemory`, and source attribution to Agent Memory Atlas revision `19199a4fc249e89c0793be06f0b166b358089ba0`. The official GitHub repository page identifies the canonical public repository and default branch `main`; its current commits feed identifies the reviewed head SHA above. The roster is used only for identity and attribution. Atlas descriptions, marks, prose, and layout are not assessment evidence.[[curated roster](../data/memory-systems.json)] [[repository](https://github.com/rohitg00/agentmemory)] [[main commits feed](https://github.com/rohitg00/agentmemory/commits/main.atom)] [[reviewed full head](https://github.com/rohitg00/agentmemory/commit/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb)]

The project presents agentmemory as a local-first persistence service for coding agents. It connects supported agent hooks and plugins, MCP clients, and REST callers to a shared local server, with a live viewer and CLI. The README describes automatic capture, cross-session recall, and controls for inspecting, editing, exporting, and forgetting saved information. This review covers selected official documentation and source at the verified SHA; README descriptions are distinguished from code observations below.[[README.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/README.md)]

## Architecture and data model

**Documentation observation.** The README describes four memory tiers: working observations, episodic session summaries, semantic facts and patterns, and procedural workflows. Session events are captured, privacy-filtered, stored as observations, and may be compressed; later session hooks can load project context and retrieve memories. The README documents a local API and viewer, agent integrations, and file-backed state with optional Redis deployment.[[README.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/README.md)]

**Code observation.** The type model distinguishes raw observations, compressed observations, sessions, and saved memories. Captured records can retain hook/tool details, source payload, timestamps, session and agent identifiers, an immutable origin channel, and compression state. Saved memories carry content and type, project and agent scope, version/supersession fields, source observation IDs, and lifecycle metadata. State scopes and key helpers are centralized in the state schema and accessed through the KV layer.[[types](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/types.ts)] [[state schema](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/state/schema.ts)] [[state KV](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/state/kv.ts)]

## Write, update, delete, and retrieval

**Write and update — code observation.** The `mem::remember` function validates content and metadata, normalizes project and agent identifiers, and serializes writes with a keyed lock. It searches likely duplicate candidates, only supersedes a sufficiently similar latest memory within the matching scope, retains a version chain, and emits a near-match hint below the supersession threshold. The memory is indexed for recall and can retain source observation identifiers and an expiry. These are implementation paths, not measured correction quality.[[remember](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/remember.ts)] [[types](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/types.ts)]

**Capture and derived writes — documentation observation.** The README describes durable event capture, privacy filtering, optional compression, BM25 indexing, and optional vector embedding. Session-end processing can add summaries and optional graph extraction. Recent source changes also route flow-compressed and auto-paged memories through the search index when they are written; that change addresses indexing visibility, not retrieval accuracy.[[README.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/README.md)] [[reviewed head commit](https://github.com/rohitg00/agentmemory/commit/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb)] [[observe](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/observe.ts)]

**Delete and expiry — code/documentation observation.** The README documents forgetting memories and automatic expiry/retention. The inspected memory functions include a forget path that deletes selected records and related session/summary data, cleans search/access/facet state, and writes a forget audit record; auto-forget and governance functions are separate lifecycle paths. These code paths do not establish complete erasure from every backup or external storage layer, and no deletion leakage workload was run.[[README.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/README.md)] [[remember and forget functions](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/remember.ts)] [[governance](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/governance.ts)] [[auto-forget](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/auto-forget.ts)]

**Retrieval — code/documentation observation.** Keyword recall uses a BM25 index. When a vector index and embedding provider are configured, memory ranking fuses keyword and vector ranks; a graph ranker can add structural evidence to smart search. Search filters can constrain project, working directory, agent, or result layer, and responses can be token-budgeted. The search source expands candidate windows to satisfy filters up to a fixed candidate bound; a result below the bound can be empty even when a qualifying item exists farther down the rank list. These implementation details do not establish answer quality or latency.[[README.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/README.md)] [[search](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/search.ts)]

## Scope isolation, provenance, and evidence

**Scope observation.** The README documents project and per-agent scoping, with shared or isolated agent modes. The `remember` path stores normalized project and agent IDs and checks scope before considering a prior memory for supersession; the search path accepts project and working-directory filters and applies agent filtering. These are code-level scope controls. The review did not run cross-project or cross-agent probes, and deployments that expose the server beyond its documented loopback default need their own network and authentication review.[[README.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/README.md)] [[remember](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/remember.ts)] [[search](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/search.ts)]

**Evidence and provenance.** The type model defines write-time origin channels such as user, agent, tool, import, and shared, and observations can link to source and capture information. Saved memories can carry source observation IDs, and audit entries record lifecycle operations. These fields provide traceability signals; they do not prove that a retrieved memory supports a generated claim or that every answer exposes a claim-level citation.[[types](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/types.ts)] [[remember](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/remember.ts)] [[audit](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/audit.ts)]

## Source-visible efficiency and observability

**Code observation.** Memory supersession uses BM25 candidate generation and compares only a bounded top set when the memory index is ready, with a full-scan fallback for a cold index or failed candidate lookup. Search uses rank fusion, batches record hydration, and expands the candidate window only as needed for filters up to a maximum. The README documents a dedicated in-memory lesson index, per-session result diversity, optional local or remote embeddings, and bounded vector backfill. These are source-visible design choices, not measured cost or performance.[[remember](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/remember.ts)] [[search](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/search.ts)] [[README.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/README.md)]

The README describes a status command and viewer that expose health, provider and embedding mode, capture delivery and recovery, vector backfill state, and pending index changes. Search and audit code also emit logs and maintain access metadata. This review collected no runtime traces, token accounting, provider charges, latency histograms, or storage measurements.[[README.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/README.md)] [[search](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/search.ts)] [[audit](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/audit.ts)]

## Project metric domains

All benchmark domains are **unmeasured** for this review. Source code shows retrieval and scoping mechanisms but no adjudicated answerable-recall, abstention, correction, stale-value, deletion-leak, cross-scope-leak, citation-support, or citation-coverage results. No latency distribution, write-to-recall delay, token/cost total, or corpus storage efficiency was collected. Project metric definitions and the fixture describe evaluation protocols, not agentmemory results.[[project metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded read-only inspection of the official repository page, README, selected TypeScript types and memory/search/lifecycle functions at the verified SHA. The system, its tests, and benchmark workloads were not run. The review does not establish production reliability, answer support quality, cross-tenant isolation, complete deletion from backups or replicas, or runtime performance. Unknown means unverified in this review.[[README.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/README.md)] [[types](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/types.ts)] [[search](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/search.ts)]

## Contact-list follow-up

The official repository README and security policy were checked. The published security policy gives `ghumare64@gmail.com` as an encrypted-email fallback, so that exact address and the pinned policy URL are recorded in the JSON review record. No commit metadata, profile email, third-party directory, or inferred address was used.[[SECURITY.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No agentmemory system execution, tests, or benchmark workload was run. Code and documentation observations are not measured results. See project metric definitions, execution status, and fixture for the separate evaluation protocol.[[project metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical GitHub repository](https://github.com/rohitg00/agentmemory)
- [Reviewed main branch head commit](https://github.com/rohitg00/agentmemory/commit/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb)
- [README.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/README.md)
- [SECURITY.md](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/SECURITY.md)
- [src/types.ts](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/types.ts)
- [src/state/schema.ts](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/state/schema.ts)
- [src/state/kv.ts](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/state/kv.ts)
- [src/functions/observe.ts](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/observe.ts)
- [src/functions/remember.ts](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/remember.ts)
- [src/functions/search.ts](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/search.ts)
- [src/functions/governance.ts](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/governance.ts)
- [src/functions/auto-forget.ts](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/auto-forget.ts)
- [src/functions/audit.ts](https://github.com/rohitg00/agentmemory/blob/5c9e2e698bda138dcb7de50ee4dd3260ee4fb8eb/src/functions/audit.ts)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and source attribution](../data/memory-systems.json)

**Verification boundary:** no agentmemory system, tests, or benchmarks were run.
