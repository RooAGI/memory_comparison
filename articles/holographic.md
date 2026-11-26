# Holographic source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 305 / Holographic / `holographic`  
**Listed repository locator:** [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)  
**Canonical maintained provider:** [itpartypattaya/hermes-plugin-holographic](https://github.com/itpartypattaya/hermes-plugin-holographic)  
**Default branch / reviewed head:** main / [ceb802be781e9e31cd9509755ad18ea46194a774](https://github.com/itpartypattaya/hermes-plugin-holographic/commit/ceb802be781e9e31cd9509755ad18ea46194a774)  
**Review time:** 2026-11-25 23:28:14 UTC (2026-11-25 15:28:14 PST; America/Los_Angeles).

## Identity and review pin

The catalog places Holographic at ordinal 305, slug `holographic`, and explicitly lists NousResearch/hermes-agent. That listed repository remains the roster locator. Its current repository page identifies `main`; the current commit feed identifies full head `6e447b2c2f01c12c4a6544e2e92c5de4944743f1`. The official Hermes provider guide says Holographic moved out of core and is maintained as a catalog plugin by itpartypattaya; that maintained repository identifies itself as the same provider formerly shipped in Hermes. I therefore pin the current provider implementation to `itpartypattaya/hermes-plugin-holographic`, default branch `main`, full head `ceb802be781e9e31cd9509755ad18ea46194a774` from its official commit feed. The Atlas record is retained for curated identity/locator attribution only and is not assessment evidence.[[roster]][[atlas]][[listed]][[repo]][[head]][[provider-docs]][[readme]]

## Summary

Holographic is a local SQLite memory provider for Hermes Agent. It stores versioned facts and entity links, and combines multilingual full-text matching, entity-aware recall, trust weighting, and optional holographic vector similarity. The default path needs no API key, network call, or model call; optional embedding and reranking services are configured separately. This is a source review, not a runtime evaluation.[[readme]][[provider-docs]]

## Who and what

The maintained project README identifies the implementation as a Hermes Agent memory provider and says it has been maintained by itpartypattaya since October 2026. Hermes' official guide says the provider is installed from the plugin catalog and runs alongside built-in memory. It is a local plugin integrated with Hermes rather than a hosted service in the inspected path.[[readme]][[provider-docs]][[memory-docs]]

## Architecture and data model

The current store uses SQLite. Current facts include text, category, tags, trust score, retrieval/helpfulness counts, timestamps, and an optional HRR vector. FTS5 indexes fact text and tags. Separate tables relate facts to entities and aliases; additional tables store per-fact embeddings, history, provenance and forgetting state.[[store]][[history]]

The implementation is split across a MemoryStore, retrieval logic, HRR encoding, entity resolution, version history, optional embedding/reranking clients, and an optional experience journal. Hermes treats this as an external provider. Its built-in MEMORY.md and USER.md remain active alongside it.[[store]][[retrieval]][[entities]][[experience]][[provider-docs]][[memory-docs]]

## Write, update, delete, and retrieval

**Write.** The fact store accepts a fact with optional category, tags, entities, validity date, origin and source metadata. The SQLite store updates FTS and entity links, and can compute an HRR vector when NumPy support is available. The README also documents opt-in automatic extraction and mirroring of built-in memory writes.[[readme]][[store]][[entities]][[history]]

**Update and correction.** The tool surface includes update, change, correct, revert, merge and history operations. Version history retains previous fact text and validity intervals; origin and source fields are associated with versions. Similar facts and possible conflicts are surfaced as information for the agent, not as an automatic truth-resolution guarantee.[[readme]][[history]]

**Delete and forgetting.** Fact forgetting removes the current fact and associated versions and records keyed digests instead of the forgotten text. Entity deletion removes links and records keyed tombstones. The inspected sources describe these operations within the local provider store; this review does not establish deletion from backups or exported copies.[[history]][[entities]][[store]]

**Retrieval.** FTS5 supplies text candidates; multilingual tokenization/stemming, term overlap, similarity, entity recall, trust weighting, and optional HRR similarity contribute to ranking. Before-turn prefetch applies relevance/coverage rules, caps the result set, and suppresses recently repeated facts. Entity probe and compositional reasoning actions offer targeted query paths. These mechanisms are code/documentation observations, not measured recall quality.[[retrieval]][[readme]]

## Scope isolation

The plugin README documents profile, user, chat and thread scopes using separate local databases and states that a required identity must be available for reads/writes in the selected modes. Hermes' official guide describes Holographic as a local provider whose data is isolated per profile. No cross-scope workload was run, so these are described boundaries rather than measured isolation guarantees.[[readme]][[provider-docs]][[metrics]]

## Provenance and evidence

Fact versions can retain source context and an origin label such as said, confirmed or inferred, along with valid-time and recorded-time fields. The optional experience journal can record which fact versions were emitted and a later outcome, but its own source warns that emission does not prove the answer used a fact and that outcomes are agent reports, not human verification. Provenance metadata is useful for inspection; it does not establish that a claim is true or that an answer is supported by its source.[[history]][[experience]][[readme]]

## Efficiency and observability

FTS5 is maintained by triggers when indexed text changes; fact vectors and optional per-fact embeddings are stored in SQLite. Prefetch count and token limits, repeat suppression, and optional graph expansion bound some retrieval work. The optional journal is off by default, bounded by retention and count limits, and records stage timings; logs are designed not to include fact or query text. Optional embedding and cross-encoder reranking paths send text to configured endpoints and are explicitly online. No latency, write-to-recall, token, cost, or storage measurements were collected.[[store]][[retrieval]][[experience]][[readme]][[metrics]]

## Metric-domain evidence

Every project benchmark domain remains **unmeasured** for this review. The [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the workload/status, not Holographic results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Multilingual text/entity retrieval and a prefetch coverage gate are present; no answers were scored. | Unmeasured |
| Correction and staleness | Versioned update, valid time and revert are present; no correction probes were run. | Unmeasured |
| Deletion leakage | Fact/entity forgetting and keyed tombstones are present; no post-delete probes were run. | Unmeasured |
| Scope isolation | Profile, user, chat and thread scope are documented; no leakage workload was run. | Unmeasured |
| Evidence support and citation coverage | Version provenance and optional recall traces exist; no answer-level claim evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timing samples were collected. | Unmeasured |
| Tokens, cost and storage | Bounded prefetch and local SQLite are documented; no resource measurements were collected. | Unmeasured |

## Limits and unknowns

Trust scores and retrieval ranks are heuristics, not truth verification. The documented conflict path surfaces possible conflicts but leaves the agent to decide; the inspected code does not establish semantic entailment or answer-level citation guarantees. Multilingual normalization and relevance thresholds may miss a relevant fact or admit a weak match; practical quality is unknown without a workload.[[retrieval]][[history]][[readme]]

Local-only storage is the default, but configured embedding and reranking endpoints receive fact/query text. Scope behavior depends on identity and local deployment configuration; filesystem permissions and real multi-user isolation were not tested. The review did not run the provider, tests, or benchmarks.[[readme]][[provider-docs]][[metrics]][[status]]

## Benchmark status

**Benchmark not run.** No Holographic runtime, tests, or benchmark workload was run. Upstream-reported results and synthetic examples are not measurements for this review. See the project's [metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json); none is a Holographic result record.[[readme]][[metrics]][[fixture]][[status]]

## Contact

The maintained plugin's official README and Hermes' official provider guide were checked for a published contact email. Neither published one. No address was inferred from commit/profile metadata or a third-party directory.[[readme]][[provider-docs]]

## Sources

All implementation-file links are pinned to `ceb802be781e9e31cd9509755ad18ea46194a774`. The Atlas link is retained only for curated identity and locator attribution. See the structured [Holographic review record](../data/system-reviews/holographic.json) and [curated catalog](../data/memory-systems.json).
