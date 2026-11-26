# Honcho source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 308 / Honcho / `honcho`  
**Listed repository locator:** [plastic-labs/honcho](https://github.com/plastic-labs/honcho)  
**Canonical upstream:** [plastic-labs/honcho](https://github.com/plastic-labs/honcho)  
**Default branch / reviewed head:** main / [1747caf8a388a8efde8fecee9056fc5dc28c473d](https://github.com/plastic-labs/honcho/commit/1747caf8a388a8efde8fecee9056fc5dc28c473d)  
**Review time:** 2026-11-25 23:32:30 UTC (2026-11-25 15:32:30 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists Honcho at ordinal 308, slug `honcho`, with the explicit repository locator `https://github.com/plastic-labs/honcho`. The catalog’s pinned Agent Memory Atlas entry is retained only for roster attribution and is not assessment evidence. The official repository page identifies the canonical project as `plastic-labs/honcho` and shows `main` as the default branch. The repository’s official `main.atom` feed identifies full head `1747caf8a388a8efde8fecee9056fc5dc28c473d`, updated at 2026-11-25T20:23:56Z. I inspected the README, architecture guide, current CRUD, scope, lifecycle and graph source at that SHA. The GitHub REST commit API was rate-limited during this review; the repository page and official main commit feed were used for branch and head verification.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Honcho is a memory service and library for stateful agents. It stores peer-attributed messages in sessions, processes them asynchronously into conclusions and representations, and exposes semantic search, context and chat APIs. It can be used as a managed service, a local stack or a self-hosted FastAPI server. Its workspace, tenant and named-scope boundaries are significant parts of its data model.[[readme]][[architecture]]

## Who and what

The repository is maintained under the Plastic Labs GitHub organization. Its README describes this repository as the core FastAPI service, alongside Python and TypeScript SDKs and a CLI. It presents managed Honcho, a locally started stack and self-hosting as deployment choices. No individual maintainer identity is asserted in this review.[[readme]][[repo]]

## Architecture and data model

A workspace is the top-level application namespace. Workspaces contain peers and sessions; peers can participate in multiple sessions, and each session stores chronological messages attributed to peers. A peer is a durable person, agent or other entity whose representation is updated from its interactions. Named scopes group sessions within a peer to restrict which session history may inform recall.[[readme]][[architecture]][[scopes]]

The service separates synchronous storage from asynchronous reasoning. Message writes persist to PostgreSQL and enqueue derivation work; background deriver workers update conclusions and representations, while scheduled/on-demand dream work revisits existing conclusions. The README also describes Redis-backed queues, vector search and configurable providers. This review did not inspect every worker, provider or deployment component.[[readme]][[architecture]][[messages]]

Conclusions are stored as documents associated with an observer/observed peer pair. They may be explicit or derived and can link to source conclusions and source messages. Representations, summaries and peer cards are other queryable projections. Semantic conclusion search and message search are separate paths; message retrieval can include nearby context messages, while graph endpoints expose conclusion structure and source lineage.[[documents]][[conclusions]][[messages]][[graph]]

## Write, update, delete, and retrieval

**Write.** The documented SDK flow creates peers and sessions, then appends peer-attributed messages. Current architecture documentation describes message persistence and reasoning-queue insertion as part of the write request, with derivation performed asynchronously. The API also accepts explicit conclusion creation. Derived conclusions can retain links to source conclusion IDs and source message IDs; malformed source identifiers are dropped by the inspected link-building helpers.[[readme]][[architecture]][[conclusions]][[documents]]

**Update and correction.** Messages have update endpoints and conclusions can be created, derived, consolidated or removed. The inspected source exposes source links and reasoning histories, but this bounded review did not establish one universal correction policy across explicit conclusions, derived conclusions, summaries and representations. How quickly a changed message is reflected in all derived views depends on queued processing and was not measured.[[readme]][[conclusions]][[documents]]

**Delete.** The conclusion API exposes an irreversible delete endpoint; its route says deletion also removes copied Representation History for affected dreams. Workspace/session/message deletion paths are also described by the project, and read queries apply lifecycle filters. This inspection does not establish physical erasure from every database, vector index, backup or retained external copy; no deletion leakage probe was run.[[conclusions]][[documents]][[lifecycle]][[readme]]

**Retrieval.** Honcho offers peer or workspace chat, session context, peer representations, conclusions search, message search and an experimental conclusion graph API. Conclusion semantic search is constrained to an observer/observed perspective. Message search supports semantic and text matching with optional dates, context windows, observers and session allowlists. The graph endpoint exports structure as Arrow IPC; a separate text endpoint fetches content for selected conclusion IDs. These interfaces establish available retrieval paths, not answer quality.[[readme]][[conclusions]][[messages]][[graph]][[graph-route]][[graph-doc]]

## Scope isolation

Workspace is the application boundary; the current README describes multi-tenant deployments with tenant-bound PostgreSQL row-level security, including tenant identity on every table and separate app/service roles. Within a workspace, peers represent perspectives and named scopes bind recall to member sessions. Scope identity uses a reserved `scope.` peer namespace plus an internal marker; named-scope reads reject peer-scoped keys and incompatible session/filter options.[[readme]][[scopes]][[lifecycle]]

The message search code distinguishes an unrestricted query from an empty allowlist and fails closed when an observer has no allowed sessions, avoiding an empty `IN` filter that might otherwise be dropped by an external vector backend. The review did not run cross-tenant or cross-scope probes, so isolation behavior under real deployment configuration remains unmeasured.[[messages]][[scopes]][[metrics]][[fixture]]

## Provenance and evidence

Derived conclusions can carry ordered source-conclusion links and links to cited source messages. The graph query returns source edges plus lineage state and counts for sources outside the requested graph, deleted sources and unknown IDs. This makes missing or partial lineage visible to a graph consumer, but it does not show that an LLM-derived conclusion is true or that every answer exposes citations to the user.[[documents]][[graph]][[graph-doc]]

Message identity and peer/session attribution provide source context. The inspected code validates and deduplicates source identifiers before persisting links; it does not independently adjudicate whether source text supports the derived conclusion. Evidence support precision and user-visible citation coverage therefore remain unestablished without response capture and review.[[documents]][[metrics]][[fixture]]

## Efficiency and observability

The service uses asynchronous reasoning so an LLM call does not block ordinary message writes. Retrieval can use text and vector paths; search and graph code include timeouts, bounded results and instrumentation. The graph implementation checks the configured conclusion cap before materializing rows, serializes builds through a per-process semaphore, reports stage timings and graph size, and supports ETags. The default graph cap is 150,000 and the documentation labels its sizing provisional pending shared-pool measurement.[[architecture]][[readme]][[messages]][[graph]][[graph-route]][[graph-doc]]

These are source-level design and observability facts. This review collected no retrieval latency, write-to-recall delay, token counts, provider cost, queue lag distribution or storage footprint. README and documentation benchmark statements are upstream claims and are not reproduced Honcho results.[[readme]][[metrics]][[status]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Honcho. The metric definitions and synthetic fixture describe a protocol, while the shared execution status is project status rather than a Honcho result.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Semantic and text retrieval, representations and chat are implemented; no fixture probes were run or scored. | Unmeasured |
| Correction accuracy and stale-value rate | Derivation, conclusion management and source linkage exist; no correction sequence or stale-value probes were run. | Unmeasured |
| Deletion leak rate | Conclusion and other deletion paths exist; physical erasure across all stores and copies is unverified; no post-delete probes were run. | Unmeasured |
| Scope isolation leak rate | Workspace, tenant, peer and scope filters exist; no cross-boundary fixture probes were run. | Unmeasured |
| Evidence support precision and citation coverage | Source IDs and lineage can be retained; no answer claims or citations were adjudicated. | Unmeasured |
| Retrieval latency | No timed retrieval calls were collected. | Unmeasured |
| Write-to-recall delay | No scheduled post-write recall probes were collected. | Unmeasured |
| Tokens and cost | No model usage or billing observations were collected. | Unmeasured |
| Storage efficiency | PostgreSQL and vector storage are part of the architecture; no attributable bytes or per-item size was measured. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the pinned README, architecture guide and selected current source. Honcho, its tests and benchmarks were not run. Source inspection establishes documented or implemented paths, not runtime recall quality, production isolation, deletion completeness, queue recovery, or behavior under a particular hosted configuration.[[readme]][[architecture]][[messages]][[documents]]

The repository supports multiple deployment modes, vector backends, providers and optional multi-tenant settings. The results of this review cannot establish that every deployment has the same behavior or that its role, row-level security and external store configuration is correct. The official README and security policy were checked for contact; no general contact address was published in the README, while the security policy publishes a vulnerability-reporting email.[[readme]][[security]]

## Benchmark status

**Benchmark not run.** No Honcho runtime, tests or benchmark workload was run. No recall, correction, deletion, isolation, citation, latency, token, cost or storage result is claimed. The [project metric definitions](../METRICS.md), [synthetic fixture](../fixtures/memory-benchmark-v1.json) and [shared execution status](../results/initial-baselines-status.json) define protocol and status only; they are not Honcho results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned [SECURITY.md](https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/SECURITY.md) publishes `support@honcho.dev` for private vulnerability reports. This is recorded as a security-reporting contact, not inferred from commit/profile metadata. The official README was also checked for a general contact address and did not publish one.[[security]][[readme]]

## Sources

The catalog record and pinned Atlas attribution are included only for curated roster identity; Atlas is not assessment evidence. Every upstream file source below is pinned to the full reviewed SHA. See the structured record [honcho.json](../data/system-reviews/honcho.json), [curated catalog](../data/memory-systems.json), [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json) and [execution status](../results/initial-baselines-status.json).

## Citation source map

[[catalog]] ../data/memory-systems.json
[[atlas]] https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/honcho.md
[[repo]] https://github.com/plastic-labs/honcho
[[head]] https://github.com/plastic-labs/honcho/commits/main.atom
[[readme]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/README.md
[[architecture]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/docs/v3/documentation/core-concepts/architecture.mdx
[[messages]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/src/crud/message.py
[[documents]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/src/crud/document.py
[[conclusions]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/src/routers/conclusions.py
[[scopes]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/src/utils/scopes.py
[[lifecycle]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/src/crud/lifecycle.py
[[graph]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/src/crud/graph.py
[[graph-route]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/src/routers/graph.py
[[graph-doc]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/docs/v3/api-reference/endpoint/graph/get-graph.mdx
[[security]] https://github.com/plastic-labs/honcho/blob/1747caf8a388a8efde8fecee9056fc5dc28c473d/SECURITY.md
[[metrics]] ../METRICS.md
[[fixture]] ../fixtures/memory-benchmark-v1.json
[[status]] ../results/initial-baselines-status.json
