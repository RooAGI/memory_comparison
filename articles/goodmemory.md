# GoodMemory source and design review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 266 / GoodMemory / `goodmemory`  
**Listed repository locator:** [hjqcan/GoodMemory](https://github.com/hjqcan/GoodMemory)  
**Canonical upstream:** [hjqcan/GoodMemory](https://github.com/hjqcan/GoodMemory)  
**Default branch / reviewed head:** main / [c7d8060036010762512c292b84f1d23b86ba2787](https://github.com/hjqcan/GoodMemory/commit/c7d8060036010762512c292b84f1d23b86ba2787)  
**Review time:** 2026-11-25 21:21:54 UTC (2026-11-25 13:21:54 PST; America/Los_Angeles).

## Identity and review pin

The catalog records GoodMemory as ordinal 266, slug `goodmemory`, with an explicit locator at `https://github.com/hjqcan/GoodMemory` and a pinned Agent Memory Atlas roster attribution. The catalog and Atlas attribution are used only to establish roster identity and locator context. GitHub's official repository page identifies `main` as the default branch; the official commits API reports full current head `c7d8060036010762512c292b84f1d23b86ba2787` (commit timestamp 2026-10-20T03:50:03Z). The inspected source pages below use that exact commit.[[catalog]][[atlas]][[repo]][[head]]

## Summary

GoodMemory is a TypeScript memory library for applications and coding-agent integrations. Its public flow combines scoped `remember`, `recall`, context assembly, feedback/correction, and forget/export operations. The current source separates domain records, write extraction and governance, storage adapters, retrieval/selection, and optional runtime/host integrations. Bun's zero-config path uses durable local SQLite; Node without a configured durable adapter falls back to in-memory storage.[[readme]][[domain-records]][[remember]][[recall-engine]][[memory-store]][[sqlite-store]]

## Who and what

The official README describes GoodMemory as a memory layer for AI products and coding agents, published from the `hjqcan/GoodMemory` repository. It is a TypeScript package with application, AI SDK, host, HTTP, and CLI integration surfaces. The README assigns authentication, product policy, user interface, and model orchestration to the integrating application; this review does not infer individual maintainer identity from commit or profile metadata.[[repo]][[readme]]

## Architecture and data model

The source is organized around typed memory records and service boundaries. Fact records include scope fields, category/content, confidence, importance, source metadata, optional validity and expiry times, and lifecycle state. The domain also defines preference, feedback, reference, note, episode, profile, and session-continuity record types. Source provenance distinguishes explicit, inferred, imported, and confirmed memory; lifecycle states are active, superseded, and inactive.[[domain-records]][[provenance]]

Storage is behind document, session, and vector-store contracts. The in-memory implementation is an adapter, while the SQLite module provides durable document/session/vector storage and can use an optional SQLite vector extension. The README also documents explicit Postgres and injected adapters. Storage durability therefore depends on runtime and configuration rather than being uniform across all zero-config deployments.[[memory-store]][[sqlite-store]][[readme]]

## Write, update, delete, and retrieval

**Write.** The remember engine composes an extraction pipeline with a write pipeline. The write path resolves candidates, applies source-derived enrichment, redaction and persistence masking, coordinates document changes with rollback actions, then commits embeddings and optional claim projections. Results distinguish committed, failed, and no-admissible-candidate outcomes. The source records the method and extraction time; this code review did not execute a write or verify provider behavior.[[remember]][[write-pipeline]][[provenance]]

**Update and correction.** The README exposes feedback and targeted `reviseMemory()` for corrections. The revision service checks a scoped target and idempotency digest, then conditionally commits a successor alongside the prior-target snapshot and evidence record. Its result includes previous/new memory IDs; an embedding update can fail after the durable revision and is returned as a warning, so vector freshness is a separate concern.[[readme]][[revision]]

**Delete.** The public API includes `forget()` and `deleteAllMemory()`. Admin operations filter records against the requested scope, delete document records, and report operation trace attributes; the scope-deletion coordinator serializes overlapping mutations and deletion work. Omitted optional scope fields act as wildcards in the admin record matcher, so callers must provide the intended boundary when deletion should be narrow. This source inspection does not establish erasure from external backups, adapter-managed replicas, or the host application's own logs.[[readme]][[admin]][[scope-deletion]][[tracer]]

**Retrieval.** Recall builds a query plan and passes it through a retrieval pipeline. The architecture document describes production selection using general query/record signals and bounded candidate selection; the README documents a rules-only default and an optional recommended preset that fuses BM25, entity adjacency, and available dense candidates with reciprocal-rank fusion. Optional multi-hop retrieval and reranking add further work and may use configured providers. Recall traces can represent retrieval channels, candidate ranks/scores, fallback reasons, and reranker latency/status. No recall query was run for this review.[[recall-engine]][[retrieval-pipeline]][[recall-architecture]][[retrieval-trace]][[readme]]

## Scope isolation

A normalized scope requires a non-empty `userId` and may include tenant, workspace, agent, and session. The implementation encodes all five components into a versioned key; recall evidence matching compares complete normalized scopes. Deletion accepts partial scope values and treats omitted optional fields as unrestricted, an intentional broad-selection behavior that callers must account for. These code observations show the library's scope model, not an adversarial test of every adapter, integration, deployment, or authorization boundary. The README leaves authentication and product authorization to the integrating application.[[scope]][[evidence]][[admin]][[readme]]

## Provenance and evidence

Memory records retain a source method and extraction timestamp, and may retain source session and locale metadata. Recall evidence records can link to memory/archive IDs; evidence selection is scope-filtered and capped. The evidence ledger can connect evidence excerpts to projected claims, label temporal status as current, superseded, or uncertain, and classify a relation as supporting, contradicting, or contextual. Those are internal lineage and retrieval annotations; they do not by themselves establish that an extracted claim is true or that every answer presented to an application will expose its supporting evidence.[[provenance]][[evidence]][[evidence-ledger]][[domain-records]]

## Efficiency and observability

The production recall documentation describes bounded candidate/fact selection, and the implementation resolves dynamic fusion budgets from the query plan. SQLite offers a local durable path; the optional generalized dense channel and reranker can add provider work, latency, and cost. The README says the recommended preset is opt-in and default retrieval remains rules-only when it is unset. No storage, token, latency, or cost values were measured here.[[recall-architecture]][[retrieval-pipeline]][[sqlite-store]][[readme]][[metrics]]

An optional tracer emits started/succeeded/failed/blocked spans to a supplied sink. Scope identifiers are represented by HMAC digests, while retrieval trace structures can include per-channel evidence IDs, ranks and scores, fallback state, and reranker provider/model/latency. Tracing is useful for inspecting operations but does not amount to a benchmark or a complete service-level monitoring deployment.[[tracer]][[retrieval-trace]]

## Metric-domain evidence

Every benchmark domain is **unmeasured in this review**. Source structure and README descriptions are not measurements collected here. No GoodMemory runtime, tests, or benchmarks were run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) for the project's evaluation protocol and run status.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Recall and selection paths were inspected; no answer set was scored. | Unmeasured |
| Correction and stale values | Scoped revision and lifecycle code were inspected; no correction probes were run. | Unmeasured |
| Deletion leakage | Scope deletion and forget paths were inspected; no post-delete probes were run. | Unmeasured |
| Scope isolation | Five-part scope encoding and scope-aware evidence selection were inspected; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Source/evidence links and ledger classifications were inspected; no response claims were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Bounded retrieval and trace fields exist; no runtime timings were collected. | Unmeasured |
| Tokens and cost | Provider-dependent paths are documented; no token usage or charges were measured. | Unmeasured |
| Storage efficiency | SQLite and adapter paths were inspected; no corpus-attributable byte count was collected. | Unmeasured |

## Limits and unknowns

This review is a source inspection pinned to one verified commit, not an operational, security, or quality audit. It did not run GoodMemory, its tests, or benchmark workloads. It cannot establish end-to-end correctness, provider availability, isolation under hostile callers, deletion from backups or externally managed stores, measured quality, or resource use.[[head]][[metrics]][[fixture]]

Durability depends on storage selection: the README documents Bun's local SQLite default and in-memory fallback for Node without a durable adapter. Rules-only retrieval is the default unless the optional preset is enabled; dense retrieval and provider reranking require configuration. The inspected scope and evidence structures demonstrate intended boundaries and traceability, but do not prove every adapter and host integration enforces them identically.[[readme]][[sqlite-store]][[retrieval-pipeline]][[scope]][[evidence]]

## Benchmark status

**Benchmark not run.** No GoodMemory runtime, tests, or benchmark workload was executed for this review. No retrieval, correction, deletion, isolation, evidence, latency, token, cost, or storage result is claimed. The current README describes its benchmark-claim gate and states that no end-to-end benchmark runner is allowlisted for public or versioned claims; that is an upstream documentation statement, not a result from this review. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[readme]][[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email; it contains no email address. Accordingly, `contact_email` is null and the exact checked README URL is recorded. No commit/profile metadata or third-party directory was used.[[readme]]

## Sources

All upstream source links are pinned to the verified full SHA. The Atlas source above is retained only as roster attribution, not system assessment evidence. See the structured record [goodmemory.json](../data/system-reviews/goodmemory.json) and [curated roster](../data/memory-systems.json).
