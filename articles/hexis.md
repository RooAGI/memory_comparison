# Hexis

## Identity and review pin

- **System:** Hexis
- **Listed repository:** https://github.com/quixiai/hexis
- **Canonical upstream:** https://github.com/QuixiAI/Hexis
- **Default branch:** `main`
- **Reviewed head:** `209804c84ed1ff449f37b9508c91b97384a80e13`
- **Reviewed at:** 2026-11-25T22:57:42Z (2026-11-25 14:57:42 PST; America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The catalog resolves ordinal 294 to Hexis (`hexis`) and lists the repository above; its Atlas attribution is retained only for curated identity and locator context, not as assessment evidence.[[roster]][[atlas]] GitHub identifies `main` as the default branch, and its official main commit feed reports the full current head and update time recorded here.[[repo]][[head]]

## Summary

Hexis is a PostgreSQL centered cognitive architecture for a persistent agent. Its database stores memory, graph, belief/evidence, identity, and runtime state; PostgreSQL extensions provide vector and graph capabilities, while Python services expose database functions to chat, workers, CLI, and MCP paths.[[readme]][[tables]] This is a source review, not an evaluation of answer quality, safety, or operational performance.[[metrics]][[status]]

## Who and what

The official repository identifies QuixiAI and describes Hexis as an open source, locally runnable agent architecture rather than a standalone memory API. The README documents a Python client/CLI, PostgreSQL brain, stateless workers, and optional dashboard, messaging and MCP interfaces.[[repo]][[readme]]

## Architecture and data model

The README calls PostgreSQL the system of record and lists pgvector, Apache AGE, btree_gist, and pg_trgm among the stack. The base schema initializes graph labels and typed relationships alongside relational tables; the repository describes episodic, semantic, procedural, strategic, and working memory.[[readme]][[tables]]

Memory is not only a vector row: retrieval uses a unified RecMem context path, while graph edges connect memories with episodes and other cognitive objects. Memory rows carry lifecycle and temporal fields; source attribution and JSON metadata carry evidence references, trust, sensitivity, and related state.[[core]][[provenance]][[supersessions]]

The official retention design document is explicitly marked “proposed (v5)”. Its conceptual claims should not be treated as the shipped contract; this review relies on the current SQL implementations for retention and lifecycle behavior.[[retention-design]][[retention]]

## Write, update, delete, and retrieval

**Write and evidence.** The README documents memory operations such as remembering a claim and attaching supporting or contradicting evidence. The provenance SQL normalizes source kind/reference, author, observation time, trust, content hash, source document and chunk identifiers, and sensitivity. The belief revision function accepts independent evidence for semantic memories, updates confidence within configured bounds, and writes an audit row with prior/posterior values, evidence, policy, reason, and a digest.[[readme]][[provenance]][[belief]]

**Update and correction.** The SQL provides temporal validity and explicit supersession records with a reason, actor, effective time, replacement pointer, and status. An active supersession closes the old memory’s validity window; the old row is retained so point-in-time recall can reconstruct prior state. Confidence revision is a separate evidence-driven path and does not itself prove a corrected answer will be retrieved.[[supersessions]][[belief]]

**Delete and forgetting.** The current retention SQL can consolidate eligible episodic memories into a gist and archive originals; its header states irreversible pruning is separately opt-in and off by default. The SQL exposes retention status and a rollback-based dry run. The README’s `hexis uninstall --purge` is an explicit whole-install purge path, distinct from deleting one memory. This inspection does not establish erasure from backups, external provider logs, or all deployment copies.[[retention]][[readme]]

**Retrieval.** `fast_recall` delegates to `recmem_recall_context`, so its callers share a unified ranker. The source documents association, episode binding, recency, strength, mood congruence, trust, activation, and sensitivity inputs; the filtered wrapper returns active, currently valid records and applies memory-type and importance filters. The base schema also defines graph and property indexes. These are implementation observations, not measured retrieval speed or recall quality.[[core]][[provenance]][[tables]]

## Scope, provenance, efficiency, and observability

The README describes one database per user as the multi-tenant deployment pattern. The reviewed sources show sensitivity filtering and per-instance/deployment concepts, but this review did not test credential boundaries or cross-instance isolation; deployment configuration remains part of the security boundary.[[readme]][[provenance]]

Provenance is more explicit than a plain text store: source references can retain chunk-level handles, hashes, trust and observed time; belief changes are audited; supersession records preserve actor and reason. These records establish lineage metadata, not that a cited source semantically entails a generated answer.[[provenance]][[belief]][[supersessions]]

The schema installs PostgreSQL indexes and extensions for graph, vector and text-related access. Source functions expose ingestion aggregates and retention status/dry-run summaries. Neither source structure nor the project README’s reported figures are measurements from this review; no load, latency, token, cost, or storage experiment was performed.[[tables]][[retention]][[readme]][[metrics]]

## Metric-domain evidence

Every benchmark domain is **unmeasured** in this review. The source inspection supports mechanism descriptions only; the project metric definitions, fixture, and status record define evaluation protocol and currently report no run.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Review status |
|---|---|---|
| Answerable recall and abstention | Unified scored retrieval and active/valid filters are visible; no answers were scored. | Unmeasured |
| Correction and stale values | Evidence revision and temporal supersession are implemented; no correction probes were run. | Unmeasured |
| Deletion leakage | Retention/archive/pruning controls exist; no deletion probes or residue checks were run. | Unmeasured |
| Scope isolation | README documents a database-per-user pattern; no isolation workload was run. | Unmeasured |
| Evidence support and citations | Source references and belief audit exist; source entailment and answer citations were not adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timings were collected. | Unmeasured |
| Tokens, cost, and storage | No usage, cost, or database-size measurements were collected. | Unmeasured |

## Limits and unknowns

The review inspected selected current README, schema, SQL lifecycle/retrieval/provenance, and retention files at one verified commit. It did not inspect every tool/service adapter, every deletion route, all migrations, production deployment settings, or external provider retention behavior. Hexis, its tests, and its benchmark suite were not run.[[readme]][[tables]][[core]][[retention]][[status]]

Consequently, this review cannot establish answer correctness, abstention behavior, correction robustness, physical deletion completeness, scope-isolation safety, evidence support precision, availability, or cost/latency at any workload. The proposed retention design document may describe intended directions; shipped behavior should be determined from the code and configuration at the reviewed revision.[[retention-design]][[metrics]]

## Benchmark status

**Benchmark not run.** No Hexis runtime, tests, or benchmark workload was executed. No metric value is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) are project evaluation materials, not Hexis results.[[metrics]][[fixture]][[status]]

## Contact

I checked the official README at the reviewed commit for a published contact email; none was listed there. The structured record stores `contact_email: null` and the exact checked README URL. I did not use commit/profile metadata or third-party directories.[[readme]]

## Sources

Upstream file citations below are pinned to the verified full head SHA. The Atlas source is listed solely as roster attribution. See the structured review [hexis.json](../data/system-reviews/hexis.json), curated catalog [entry](../data/memory-systems.json), and [project metric definitions](../METRICS.md).
