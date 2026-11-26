# GrayMatter source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 275 / GrayMatter / `graymatter`  
**Listed repository locator:** [angelnicolasc/graymatter](https://github.com/angelnicolasc/graymatter)  
**Canonical upstream:** [angelnicolasc/graymatter](https://github.com/angelnicolasc/graymatter)  
**Default branch / reviewed head:** main / [b7d1b0c78779fddd6f5db6fd1f7fea0d3af61b54](https://github.com/angelnicolasc/graymatter/commit/b7d1b0c78779fddd6f5db6fd1f7fea0d3af61b54)  
**Review time:** 2026-11-25 22:02:06 UTC (2026-11-25 14:02:06 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists GrayMatter at ordinal 275, slug `graymatter`, with the explicit locator `https://github.com/angelnicolasc/graymatter`. The pinned Atlas attribution is included only to document catalog identity and locator; it is not assessment evidence. The official repository page identifies `main` as the default branch and shows commit prefix `b7d1b0c`; the official `main.atom` feed gives the full current head `b7d1b0c78779fddd6f5db6fd1f7fea0d3af61b54` and timestamp 2026-11-19T13:26:45Z. This review is pinned to that SHA. [[catalog]][[atlas]][[repo]][[head]]

## Summary

GrayMatter is a local-first Go memory store and MCP server for agent facts, with hybrid retrieval, correction and retirement handling, optional citation and subject-aware tools, and optional knowledge-graph extraction. It can also be embedded as a Go library. This is a source review and makes no runtime quality or performance claim. [[readme]][[integration]]

## Who and what

The official README describes a persistent memory layer for Go agents, distributed as one local binary or imported as a Go library. It documents MCP integrations with several agent clients. No individual maintainer identity is asserted here. [[readme]]

## Architecture and data model

A `Fact` holds an agent namespace, text, ULID, creation and access metadata, decaying weight, optional embedding, confidence declaration, alias/pin fields, supersession state and lineage projection. Citation evidence and subject projections are hydrated from separate versioned stores rather than written into the fact row. [[fact]][[citation]]

The bbolt store keeps facts and related session, metadata, namespace and pending-vector state. By default, a persistent chromem-go vector index lives under the data directory; callers can provide another implementation through the `VectorStore` interface. A reserved `__shared__` namespace is available for facts shared across agents. bbolt serializes concurrent writes with a file lock; configuration controls read-only fallback and strict-write behavior. [[store]]

The README describes a recall, inject, write, then consolidate lifecycle. Current documentation says consolidation performs maintenance such as decay and pruning and may run configured graph extraction; generative compaction is disabled. The MCP `full` profile is the default, while `core` is an opt-in profile with citation and subject write fields and combined project/shared search. [[readme]][[integration]]

## Write, update, delete, and retrieval

**Write.** The library and CLI expose fact writes, while MCP exposes `memory_add`. In the `core` profile a write can include a source, literal quote, subject, or replacement target. Those fields are opt-in; the default `full` profile retains its legacy input contract. [[readme]][[integration]]

**Update and delete.** Explicit revisions can write replacement text and retire selected source facts atomically in one transaction. A nonempty `SupersededBy` immediately excludes an old fact from recall while retaining its tombstone for listing, export and the TUI. `Retire` records removal without a replacement. Explicit deletion removes the record, while unpinned tombstones can decay and later be pruned. [[fact]][[revise]][[readme]]

**Retrieval.** Recall fuses vector similarity, keyword relevance and recency with reciprocal-rank fusion; default weights are vector 1.0, keyword 1.0 and recency 0.5. It returns top-k fact text. The README also describes an optional relevance floor, confidence filtering or weighting, query expansion through aliases, and explain receipts. Alias facts are routed to query expansion rather than injected as results. [[recall]][[fact]][[readme]]

The integration guide says core search reads project and `__shared__` memories together and can fetch an omitted citation by fact ID. The default full profile retains single-namespace search behavior. [[integration]]

## Scope isolation

Facts are stored under agent namespaces, and `__shared__` is deliberately readable by all agents through shared recall. These are storage and query boundaries in the code. No cross-namespace probe or deployed authorization review was performed, so this inspection does not establish tenant isolation. [[store]][[integration]]

## Provenance and evidence

The optional core profile accepts a source and exact quote alongside a fact. Citation records are tied to the namespace, fact ID and content hash; source and quote are writer-declared untrusted strings. The code records capture time as receipt time, not verification, so attached evidence does not by itself establish truth or answer support. [[citation]][[integration]]

Facts also support a confidence label, but the implementation describes it as the writer's epistemic declaration rather than a calibrated probability. Retrieval may filter or weight confidence when explicitly configured. [[fact]][[readme]]

## Efficiency and observability

The implementation uses local bbolt storage, a persistent vector index by default, and a pending-vector queue with a background reconciler. Recall uses a lite fact projection for ranking to avoid decoding fields the ranking does not use; the source comments cite an internal measured reduction in per-fact decode cost, which was not independently evaluated here. [[store]][[fact]]

The README documents status and doctor views, retrieval explanation receipts, usage observations, and upstream benchmarks for context tokens, retrieval, revisions and hooks. Those published figures are upstream-reported only; this review ran no runtime or benchmark. [[readme]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for GrayMatter in this review. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the project protocol and shared status, not GrayMatter results. [[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Hybrid top-k recall and optional relevance filtering are implemented; answer quality and abstention were not scored. | Unmeasured |
| Correction and stale values | Explicit revisions tombstone selected sources atomically; no correction sequence was assessed. | Unmeasured |
| Deletion leakage | Retirement excludes facts from recall and explicit deletion exists; no deletion or recovery probe was run. | Unmeasured |
| Scope isolation | Per-agent namespaces and intentional shared memory exist; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Optional writer-declared citation snapshots exist; no answer was adjudicated against evidence. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings were collected. | Unmeasured |
| Tokens, cost, and storage | The README reports upstream comparisons, but none were reproduced or measured in this review. | Unmeasured |

## Limits and unknowns

This review inspected the official README, integration guide, and selected current implementation paths at the verified head. GrayMatter, its tests, and benchmark workloads were not run. The source does not establish what agents will choose to store, whether recall will return a sufficient fact for a particular task, or whether an answer will abstain appropriately. [[readme]][[integration]][[recall]]

The review did not test authorization, provider configuration, backup and restore, custom vector backend behavior, or cross-process deployment boundaries. Reported performance and cost figures remain upstream claims rather than independently reproduced measurements. [[store]][[readme]]

## Benchmark status

**Benchmark not run.** No GrayMatter runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the evaluation protocol and shared execution status, not GrayMatter measurements. [[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email; none was present. The structured record stores `contact_email: null` with the exact checked URL. No address was inferred from commit or profile metadata or obtained from a third-party directory. [[readme]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas URL records curated roster attribution only and is excluded from the system assessment. See the structured record [graymatter.json](../data/system-reviews/graymatter.json) and [curated roster](../data/memory-systems.json).
