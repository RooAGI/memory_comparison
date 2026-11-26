# Citra Decision System

## Identity and review pin

- **Ordinal:** 120
- **Catalog name and slug:** Citra Decision System (`citra`)
- **Listed repository locator:** https://github.com/Trustedwear-Tech/citra-decision-system (catalog status: explicit)
- **Canonical upstream repository:** https://github.com/Trustedwear-Tech/citra-decision-system
- **Default branch:** `main`
- **Reviewed head:** [`6f200f2992291eda45c23d95c5e231b82e8f1cf3`](https://github.com/Trustedwear-Tech/citra-decision-system/commit/6f200f2992291eda45c23d95c5e231b82e8f1cf3)
- **Commit timestamp:** 2026-09-09T21:40:16+05:30
- **Reviewed:** 2026-11-25 07:55:35 UTC (2026-11-24 23:55:35 PST; America/Los_Angeles)
- **Review status:** Reviewed from current source and documentation
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [Atlas attribution entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/citra.md), used only for the catalog identity, listed locator, and attribution.

The project catalog identifies ordinal 120 as Citra Decision System, slug `citra`, and lists the repository above with explicit locator status. Its Atlas source/revision are recorded for roster attribution only.[[catalog]][[atlas]] Official GitHub's advertised symbolic `HEAD` resolves to `refs/heads/main`; a read-only shallow clone checked out full head `6f200f2992291eda45c23d95c5e231b82e8f1cf3`. The checkout's commit object reports timestamp 2026-09-09T21:40:16+05:30.[[repo]][[head]] The repository describes Citra as a decision application platform whose learned judgement is stored as clauses and used alongside its decisions, rather than a general-purpose personal memory store.[[readme]][[how]]

## Summary

Citra's community implementation records officer corrections in a MongoDB-backed evidence ledger, periodically consolidates correction clusters into short learned clauses, and retrieves applicable clauses while forming later recommendations. Clauses are scoped by tenant, app, modality, task type, and optionally case facets. The design treats these judgements as citable evidence for an agent recommendation, while keeping the human's decision authority and the SOP above them. This is an implementation review, not a measurement of decision quality or operational performance.[[readme]][[corrections]][[clause]][[learned]][[how]]

## Architecture and data model

The write path begins with an officer correction. A correction record retains the officer's reason, the case facets, the recommendation and override context, the officer identity, and a stable correction ID; it is stored as pending evidence until a consolidation pass consumes it.[[corrections]] The clause store is MongoDB-backed. A clause contains concise rule text, tenant/app/modality/task keys, scope facets, support and dissenting officer sets, correction provenance IDs, firing and blame counters, status, version/history, and links such as refines, contradicts, and merged-from.[[clause]]

Consolidation clusters compatible corrections, uses an LLM to author a short clause from that evidence, and stores the clause with its correction provenance. The store rejects a clause with no provenance. A clause is a candidate until the configured count of distinct supporting officers is reached (three by default); the gate counts people, not weighted seniority. Later matching corrections can reinforce a live clause. The consolidation pass marks corrections consumed only after the clause write succeeds, allowing a failed write to be retried.[[consolidation]][[clause]][[corrections]]

The learned-memory reader selects clauses for decision, image, document, and other supported analysis paths and returns clause IDs as a traceability tag. Repository documentation states that SOP text outranks a learned judgement: memory fills gaps in written policy, and a clause changes the agent's argument rather than granting it authority to decide or write.[[learned]][[how]]

## Write, update, deletion, and retrieval

**Write.** Human corrections are appended to the correction ledger. Background consolidation folds compatible evidence into clauses; the LLM supplies a compact expression while the cited corrections remain the evidence. An existing live clause can absorb further evidence when its scope and correction-language fingerprint match. Pending evidence is consumed only after successful clause persistence.[[corrections]][[consolidation]][[clause]]

**Update and correction.** Reinforcement updates the clause's supporting officers and provenance. Status changes through `set_status` snapshot prior text, scope, status, actor, cause, and time into a history array, and increment the version. Measured low precision can park a clause as underperforming; other states include candidate, active, dissented, challenged, quarantined, retired, superseded, and orphaned. Some states stop a clause from being injected while preserving its record and evidence. This is a status lifecycle, not proof of a universal hard-delete or correction-erasure contract.[[clause]][[consolidation]][[readme]]

**Retrieval.** The reader selects clauses in a tenant/app/modality/task bucket. The MongoDB query filters by live status and requires clause scope facets to be a subset of the case's facets; empty facet scope is global within that already keyed bucket. A multikey index on the bucket, status, and scope facets is intended to narrow candidates before the exact subset test. The selected clauses are ranked and bounded by a word budget before being placed into the relevant analysis prompt.[[clause]][[learned]][[how]]

**Retrieval evidence.** The clause evidence lookup follows provenance IDs back to officer corrections and can return the officer's text, the agent's prior recommendation, the case facets, changed fields, record reference, and a snapshot of the record as it appeared at decision time. This gives an operator a path from compressed rule back to examples; the lookup's optional enrichment may fail without failing the clause read.[[clause]]

## Scope isolation

Every clause query shown in the store is keyed by tenant, app, modality, and task type, and the facet predicate limits reuse to cases whose facets contain the clause's scope. This provides explicit logical partitioning in the reviewed memory access path.[[clause]][[learned]] These filters are not, by themselves, evidence that all callers are authorized correctly or that database-level tenant isolation is enforced across every service path. The review did not audit all authorization boundaries or run a cross-tenant isolation workload. Deployment and access-control guarantees beyond the inspected query remain unknown.

## Provenance and evidence

A clause cannot be created without correction provenance; the correction IDs and distinct supporting officers remain attached to it. The system can expose those corrections and decision-time context through its evidence lookup. Clause status history records previous state, actor, cause, and timestamp when the shared status-transition helper is used. The README also describes decision records that retain recommendation, cited passages, and the human's approval or override rationale.[[clause]][[corrections]][[readme]]

The audit path is not uniformly append-only: `record_dissent` updates dissent fields and status directly rather than adding a history snapshot. Thus the implementation offers useful evidence lineage, but the reviewed code does not establish that every mutation is captured by the same audit mechanism.[[clause]] The repository describes stronger tamper-evident ledger and assurance capabilities in its product overview; this review did not verify their implementation end to end.

## Efficiency and observability

Clause retrieval uses bucket/status/facet indexes, exact subset filtering, ranking, and a configurable prompt word budget. Consolidation runs outside the decision hot path, batches pending corrections, and preserves retryability around writes. These are source-visible controls, not latency or scale measurements.[[clause]][[consolidation]][[learned]]

The clause store tracks fired/blamed counters and computes precision after a minimum number of firings. Below a configured floor, the precision monitor parks a live clause pending human review. The memory code also logs clause creation, status transitions, and precision parking. The README describes an optional Prometheus/Grafana/Loki/Tempo monitoring stack; memory-specific production telemetry coverage and deployment configuration were not assessed.[[clause]][[readme]] No latency, tokens, cost, storage, or retrieval-quality measurements were collected.

## Limitations and unknowns

The public repository separates some lifecycle controls from its Community offering: its README describes officer erasure with re-fold, scheduled drift detection, threshold tuning, and fleet-wide memory health under Enterprise Memory+. Those capabilities should not be assumed to be available in the reviewed community path.[[readme]] The inspected clause store exposes reversible status transitions and exports; the reviewed sources do not establish a general hard-delete API, backup erasure behavior, or how correction erasure re-fold works.

The code review also does not establish the correctness of every correction-to-clause path, concurrent consolidation behavior under load, retention settings, or all service authorization checks. A direct status update in `record_dissent` does not use the history helper. No runtime, security, quality, scope, deletion, or performance workload was run. All benchmark domains therefore remain unmeasured.

## Benchmark status

**Benchmark not run.** This review inspected the current upstream source and documentation only. Citra, its tests, and benchmarks were not run.

## Contact

The official pinned README publishes **contact@citra-ai.com** in its contact/about sections. This address is taken from project documentation, not commit or profile metadata.[[readme]]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution.
- [Atlas attribution entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/citra.md) — attribution only.
- [Official repository](https://github.com/Trustedwear-Tech/citra-decision-system) — repository and advertised default branch.
- [Verified current head](https://github.com/Trustedwear-Tech/citra-decision-system/commit/6f200f2992291eda45c23d95c5e231b82e8f1cf3) — reviewed commit and commit timestamp.
- [Official README](https://github.com/Trustedwear-Tech/citra-decision-system/blob/6f200f2992291eda45c23d95c5e231b82e8f1cf3/README.md) — product architecture, memory overview, edition boundaries, observability stack, and contact.
- [How clause memory works](https://github.com/Trustedwear-Tech/citra-decision-system/blob/6f200f2992291eda45c23d95c5e231b82e8f1cf3/docs/how-clause-memory-works.md) — design and operating principles.
- [Correction evidence ledger](https://github.com/Trustedwear-Tech/citra-decision-system/blob/6f200f2992291eda45c23d95c5e231b82e8f1cf3/smart-app-service/corrections.py) — correction storage and consumption.
- [Clause store](https://github.com/Trustedwear-Tech/citra-decision-system/blob/6f200f2992291eda45c23d95c5e231b82e8f1cf3/smart-app-service/clause_store.py) — clause schema, provenance, statuses, index/query, scoring, evidence lookup.
- [Consolidation](https://github.com/Trustedwear-Tech/citra-decision-system/blob/6f200f2992291eda45c23d95c5e231b82e8f1cf3/smart-app-service/consolidation.py) — clustering, authoring, matching, merging, and background pass.
- [Learned-memory reader](https://github.com/Trustedwear-Tech/citra-decision-system/blob/6f200f2992291eda45c23d95c5e231b82e8f1cf3/smart-app-service/learned_memory.py) — retrieval integration and traceability tag.
- [Roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/citra.md) — identity and locator attribution only.

**Verification boundary:** read-only source and documentation review; no Citra runtime, tests, or benchmarks.
