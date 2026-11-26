# Anda Brain source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 55 / Anda Brain / anda-brain  
**Listed repository locator:** [ldclabs/anda-brain](https://github.com/ldclabs/anda-brain)  
**Current canonical repository:** [ldclabs/anda-brain](https://github.com/ldclabs/anda-brain)  
**Default branch / reviewed head:** main / a139642f1eeb2bd2079f4d8aea0dc7365e299546  
**Review time:** 2026-11-24 20:45:17 UTC (12:45:17 PST; America/Los_Angeles).

## Identity and review pin

The curated roster identifies Anda Brain at ordinal 55 and lists the repository locator above. The roster's Atlas source URL and revision are retained for identity attribution only; Atlas descriptions, marks, layout, and prose were not used as assessment evidence.[[project roster](../data/memory-systems.json)]

The GitHub repository page identifies the canonical public repository and default branch `main`; the official `main.atom` feed reports full head `a139642f1eeb2bd2079f4d8aea0dc7365e299546`, matching the abbreviated latest commit on the repository page. This review is pinned to that full SHA.[[repository](https://github.com/ldclabs/anda-brain)] [[main branch history](https://github.com/ldclabs/anda-brain/commits/main.atom)] [[reviewed head patch](https://github.com/ldclabs/anda-brain/commit/a139642f1eeb2bd2079f4d8aea0dc7365e299546.patch)]

## Summary

Anda Brain is a self-hosted service that turns interactions into a versioned knowledge graph, retrieves supported claims, and runs background maintenance to consolidate and review memory. It exposes REST, MCP, and a receipt-based Memory Interface. The findings below are observations from pinned documentation and selected source files; they are not runtime measurements.[[overview](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/README.md)] [[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)]

## Who and what

Anda Brain is the Rust library and service behind the Anda Brain product. Its official repository describes the Cognitive Nexus on AndaDB as the persistent graph layer. The official Anda site says the foundation is developed openly by LDC Labs and ICPanda DAO. The repository also documents a Cloudflare Worker edition, which is a separate deployment with a different engine and storage model; this review's implementation observations focus on the Rust service.[[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)] [[official organization site](https://anda.ai/)]

## Architecture and data model

The Rust service has three layers: REST/MCP or Memory Interface clients; Brain's Formation, Recall, and Maintenance agents plus host-side authorization and settlement; and a Cognitive Nexus stored in AndaDB, with one database per Space. Local filesystem, S3, and in-memory storage are documented.[[overview](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/README.md)] [[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)] [[Space implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/space.rs)]

The graph separates identity from belief. Concepts identify entities; Propositions represent truth-neutral subject/predicate/object statements; Assertions record an actor's stance, confidence, valid time, and evidence; Evidence holds observed messages, tool results, or document passages; Activities record how a result was produced. The engine projects belief at read time under a named policy.[[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)]

Formation captures input messages as Evidence, then processes a Space's queue sequentially. The inspected implementation bounds its retained Formation history and limits failed rounds; the technical guide describes grounding against existing memory before KIP writes and host checks that reject bulk administrative operations from the conversation input.[[Formation implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/agents/formation.rs)] [[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)]

Recall performs read-only graph queries. Maintenance runs deterministic settlement before model-assisted consolidation and review, including correction/dependency handling, commitments, retention, and self-test sampling. Space code owns background processing and lifecycle management.[[Recall implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/agents/recall.rs)] [[Space implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/space.rs)] [[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)]

## Write, update, delete, and retrieval

**Write.** REST Formation and Memory Interface observe/revise/feedback intents enqueue work and return while encoding proceeds asynchronously. The Memory Interface stages sources, accepts idempotency keys, and returns receipts that progress from recorded to available or failed; a later recall can wait for earlier receipts. Formation grounds new claims against existing graph state and writes through KIP. The inspected code includes the per-Space queue and receipt handling.[[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)] [[Formation implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/agents/formation.rs)] [[Memory Interface implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/memory_interface/mod.rs)]

**Update and correction.** Anda Brain represents different changes separately: temporal succession for a changed world, supersession for a claim that was wrong, and invalidation for a misrecorded extraction. Claims from different actors can disagree without one silently overwriting the other. This is an append-oriented history, not an in-place update protocol.[[overview](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/README.md)] [[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)]

**Delete.** Explicit forget supports a dry run and physical purge of selected graph IDs, subject to reference checks and legal holds. The technical reference says the service scrubs its own saved previews. It cannot erase external original data, backups, or provider copies; conversations and wiki documents have separate lifecycles.[[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)]

**Retrieval.** Recall grounds names to graph nodes, uses BELIEF projection for belief questions, and can answer contested or insufficient rather than treating lack of evidence as “no.” Structured Recall adds trace-derived citations and a found flag. Optional budgeted Recall emits a host-packed packet with explicit coverage and a pinned tokenizer. Reading does not reinforce memory. The Recall implementation sets a default seven-turn cap and request timeouts; these are source-visible bounds, not performance results.[[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)] [[Recall implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/agents/recall.rs)]

## Scope isolation and provenance

Each Space has its own database, graph, conversation history, tokens, and policy. The inspected authorization code handles signed CWT and Space tokens and derives stable caller identities. Label-restricted tokens are denied agentic Recall and conversation reads because those surfaces can span wiki labels. This is source-visible separation and authorization behavior, not a result from isolation testing.[[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)] [[authorization implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/authz.rs)] [[Space implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/space.rs)]

Evidence and provenance are modeled separately from the claim: an Assertion records who asserted it and cites Evidence, while an Activity records a process such as formation, consolidation, revision, or import. The technical reference says structured Recall derives citations from its trace. This review did not assess whether generated citations support claims in practice.[[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)]

## Source-visible efficiency and observability

These are source observations, not measurements. Budgeted Recall can cap output at 65,536 tokens and context at 131,072 tokens in its tool schema; the host uses a pinned tokenizer. The documented default Recall turn limit is seven, and source defines per-request timeouts and process-wide limits on concurrent model calls. None of these settings measures latency, quality, or provider charges.[[Recall implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/agents/recall.rs)] [[Space implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/space.rs)] [[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)]

The usage ledger records indexed recall, self-test, and correction counters; project documentation also describes graph counts, probe counters, and the latest settlement report. The repository lists JSON structured logs and operational limits. These indicate available instrumentation, but this review collected no telemetry.[[usage ledger implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/ledger.rs)] [[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)]

## Metric-domain evidence

All benchmark domains remain unmeasured in this review. The implementation and docs provide observable mechanisms for answerable retrieval and abstention, correction/staleness, deletion, Space isolation, evidence/citations, retrieval latency, write-to-recall delay, token/cost accounting, and storage. No benchmark probes, runtime calls, or corpus-size measurements were performed.[[project metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

The technical reference documents a 65,536-solution ceiling for correction discovery and self-test full scans; the operations report errors beyond that threshold. Several coordination controls are in-process, so the service documents one writer per Space storage location. Formation is asynchronous and fresh memories may take a minute or more to become searchable. Forgetting does not remove data held by external applications or providers.[[technical reference](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)] [[Formation implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/agents/formation.rs)]

This bounded review did not inspect every module, the separate Worker implementation, or a deployment configuration. It did not run the system, tests, or benchmarks. Actual recall quality, abstention behavior, citation support, deletion propagation, isolation under deployment, latency, tokens, cost, and storage efficiency remain unknown.

## Contact-list follow-up

The pinned official repository README and official Anda organization website were checked for a published contact email. Neither publishes one in the reviewed content, so the structured record stores `contact_email: null` with the exact checked URLs. The repository's SECURITY.md path was also checked and is absent at this revision. No commit metadata, personal profile, third-party directory, or inferred address was used.[[official README](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/README.md)] [[official organization site](https://anda.ai/)]

## Benchmark status

**Benchmark not run.** No Anda Brain runtime, benchmark workload, or tests were run. The project's metric definitions and fixture describe a protocol; the execution-status record records `not_run` and contains no results.[[project metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Canonical GitHub repository](https://github.com/ldclabs/anda-brain)
- [Current main branch feed](https://github.com/ldclabs/anda-brain/commits/main.atom)
- [Reviewed full main head patch](https://github.com/ldclabs/anda-brain/commit/a139642f1eeb2bd2079f4d8aea0dc7365e299546.patch)
- [README.md](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/README.md)
- [anda_brain/README.md](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/README.md)
- [Formation implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/agents/formation.rs)
- [Recall implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/agents/recall.rs)
- [Space implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/space.rs)
- [Memory Interface implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/memory_interface/mod.rs)
- [Authorization implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/authz.rs)
- [Usage ledger implementation](https://github.com/ldclabs/anda-brain/blob/a139642f1eeb2bd2079f4d8aea0dc7365e299546/anda_brain/src/ledger.rs)
- [Official Anda organization website](https://anda.ai/)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Curated catalog locator and source attribution](../data/memory-systems.json)

**Verification boundary:** code and documentation observations at `a139642f1eeb2bd2079f4d8aea0dc7365e299546`; no runtime, tests, or benchmarks were run.
