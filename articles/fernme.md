# FERNme

## Identity and review pin

- **Catalog position:** 237, “FERNme”; slug `fernme`.
- **Listed repository:** [mirkofr/FERNme](https://github.com/mirkofr/FERNme); catalog status is explicit. The pinned Atlas entry is recorded only as roster locator attribution.
- **Canonical upstream:** [mirkofr/FERNme](https://github.com/mirkofr/FERNme), default branch `main`. GitHub's official repository page showed `main`; its official commits API for `main` reported full head SHA `e1763d50cd3700bdb3db46f0903b8c28662edc8b`, matching a shallow checkout.
- **Reviewed:** 2026-11-25 20:20:43 UTC (2026-11-25 12:20:43 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) supplies the ordinal, name, slug, listed repository, and Atlas attribution. The [pinned Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/fernme.md) supports the roster locator attribution only; it is not assessment evidence.

## Summary

FERNme is a user-personalization memory library with a Python service, SQLite or Postgres stores, REST and MCP interfaces, and optional plugins. The deterministic core maps structured tags/events to a weighted per-user graph, compiles a bounded prompt card through spreading activation, and keeps an append-only event record for fact lookup. Optional local semantic search and proposal enrichment sit outside the core write path.

## Who and what

The official README describes FERNme as the “Fuzzy-Edged Recall Network,” a personalization layer for agents rather than a transcript store. It documents a local Python library and service, MCP server, REST API, and graph UI; its copyright notice names Acquilab Inc. No maintainer identity is inferred from repository account or commit metadata.[[README](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/README.md)] [[repository](https://github.com/mirkofr/FERNme)]

## Architecture and data model

The core model separates a sparse per-user graph from a site-level association graph and event records (“Cabinet”). User edges store a tag's weight, confidence, source state, reinforcement time/count, fast-timescale weight, salience, and stated/inferred provenance. Association edges connect co-occurring tags. Optional typed entities, aliases, fields, and relations add a structured relation layer.[[graph](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/core/graph.py)] [[schema](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/store/sqlite_store.py)]

SQLite is the zero-setup default; Postgres implements the same store interface. The SQLite schema stores per-(site,user) edges, histories, events, consent, settings, entities, assets/documents, and audit entries. Site-level association edges and population-prior tables are separate. The project describes Postgres pools, migrations, and advisory locks for concurrent writes.[[schema](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/store/sqlite_store.py)] [[Postgres store](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/store/postgres_store.py)] [[embedding guide](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/docs/embedding.md)]

## Write, update, delete, and retrieval

**Write.** `FernService.observe` first requires consent, sanitizes tags and glosses, maps event fields/catalog tags deterministically to namespaced attributes, then updates user and association weights with saturating Hebbian arithmetic, saves graph state, appends the event and audit entry. The core write path calls no LLM. Optional enrichment queues proposals separately; proposed relations or entity links do not change memory truth until accepted.[[service](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/service.py)] [[mapping](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/write/mapping.py)] [[Hebbian update](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/write/hebbian.py)]

**Update and correction.** Repeated observations reinforce weights, confidence, and history. Explicit edits create stated, non-decaying override edges. Optional curation can demote older conflicting attributes and write supersede events; this depends on configuration. Typed relation facts and pinned settings have explicit service methods. These are source-level mechanisms; they do not establish correction accuracy on live inputs.[[service](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/service.py)] [[card compiler](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/retrieve/card.py)]

**Delete.** The service exposes deletion, consent withdrawal, selective document/photo deletion when those optional features are enabled, and `forget_everywhere`. The latter writes a content-free forget audit entry, purges profile and managed files, and recomputes the site prior. Store deletion removes the user's graph, events, settings, consent, entity records, and assets/documents and removes their association contributions. The checked source does not prove erasure from external backups, filesystem snapshots, or operator copies.[[service](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/service.py)] [[SQLite store](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/store/sqlite_store.py)]

**Retrieval.** `card()` spreads activation over the user's graph and permitted association view, scores and bounds active attributes into a compact wire string, optionally applies time decay, and includes pinned settings. `recall()` opens the Cabinet using type/text filters and returns recent event payloads. Optional semantic search adds a local multilingual embedding score to keyword retrieval when separately installed; it is not required by the core. No retrieval workload was run for this review.[[service](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/service.py)] [[card compiler](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/retrieve/card.py)] [[activation](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/retrieve/activation.py)] [[semantic search docs](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/docs/semantic.md)]

**Scope isolation.** The SQLite and Postgres stores predicate user data by both `site` and `user`; service reads and writes also require consent. Remote MCP bearer tokens are bound to one profile. Site-level association edges are shared, but retrieval applies a contributor threshold (default two distinct users) and retains each user's own contribution; deletion updates contributor counts. This is code-visible isolation design, not a proof against every deployment or raw database access. The project warns that REST/MCP's caller-supplied profile identifiers are not a hosted multi-user authentication boundary; embedding apps should derive them from their own authenticated sessions.[[schema](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/store/sqlite_store.py)] [[remote MCP](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/api/remote.py)] [[embedding guide](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/docs/embedding.md)] [[security guide](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/SECURITY.md)]

## Provenance and evidence

Edges carry stated or inferred provenance and a known/guessed/override/superseded state; event records preserve payloads and mapped attributes. The audit module uses a per-install/user-keyed HMAC chain, while memory edits and other mutations may add content-free audit details or keyed references. The README describes `why()` explanations and inspectable user controls. These mechanisms preserve source context and mutation evidence within the application; they do not independently validate that a stored claim is true or that its original source is authentic.[[graph](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/core/graph.py)] [[audit](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/audit.py)] [[service](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/service.py)] [[safety](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/safety.py)]

## Efficiency and observability

Writes use deterministic arithmetic rather than a model call in the hot path. The card compiler emits at most the configured top-N graph attributes; token counts are exact only if a tokenizer is already available or explicitly allowed to download, otherwise the code estimates characters divided by four. SQLite indexes user/time event reads; the association graph keeps an adjacency index for degree-local neighbor lookup. The project includes access/history fields, audit verification, a graph UI, and optional health views. None of the published speed, token, or cost claims was independently measured here.[[Hebbian update](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/write/hebbian.py)] [[card compiler](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/retrieve/card.py)] [[graph](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/core/graph.py)] [[schema](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/store/sqlite_store.py)]

## Metric-domain evidence

| Domain | Source evidence | Review status |
| --- | --- | --- |
| Answerable recall and abstention | Activation and bounded card retrieval are source-visible; no answerability probe or calibrated abstention evaluation was run. | Unmeasured here |
| Correction and stale values | Reinforcement, decay, overrides, and optional conflict curation exist in source. | Unmeasured here |
| Deletion leakage | Profile, events, optional assets/documents, and priors have deletion paths. External replicas were not inspected. | Unmeasured here |
| Scope isolation | Per-(site,user) storage predicates, consent checks, and remote profile locks are source-visible. | Unmeasured here |
| Evidence and citations | Provenance fields, event payloads, explanations, and a hash-chain audit are source-visible. | Unmeasured here |
| Latency and write-to-recall delay | No latency or scheduled write-to-recall measurement was made. | Unmeasured here |
| Tokens and cost | The card is bounded and code estimates tokens, but no token/cost workload was run. | Unmeasured here |
| Storage efficiency | Sparse user graphs and optional differential prior behavior are documented; storage bytes were not measured. | Unmeasured here |
| Operational observability | Audit verification, histories/counters and UI health views are present. Live telemetry was not collected. | Unmeasured here |

The upstream README includes benchmark tables from synthetic or LLM-authored data and explicitly states it does not win every recall benchmark. Those are upstream-reported figures and caveats, not results reproduced or adopted as this project's measured result.[[README](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/README.md)] Project metric definitions are in [METRICS.md](../METRICS.md); benchmark execution state is in [results/initial-baselines-status.json](../results/initial-baselines-status.json), and the fixture is [fixtures/memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json).

## Limits and unknowns

This is a bounded source review at the verified `main` SHA. FERNme, its tests, and benchmarks were not run. The source review cannot establish runtime retrieval quality, real-user usefulness, calibrated abstention, complete deletion across backups, or production authorization without an integrator's authentication layer. The README characterizes published evaluation as synthetic or LLM-authored and says a real-human pilot is pending. Data-at-rest encryption and rate limiting are not provided by FERNme according to its security guide.[[README](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/README.md)] [[security guide](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/SECURITY.md)] [[head](https://github.com/mirkofr/FERNme/commit/e1763d50cd3700bdb3db46f0903b8c28662edc8b.patch)]

## Benchmark status

**Benchmark not run.** No FERNme runtime, tests, or benchmark workload was run for this review. Project metric definitions and fixtures describe a measurement protocol, not FERNme results. [METRICS.md](../METRICS.md) · [results/initial-baselines-status.json](../results/initial-baselines-status.json) · [fixtures/memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json).

## Contact

Checked the official pinned [README](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/README.md) and the official project website [fernme.dev](https://www.fernme.dev/); neither publishes a contact email. The structured record stores `contact.email: null` and the exact checked website URL.

## Sources

- [README](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/README.md) — architecture, interfaces, evaluation scope, and product claims.
- [core graph](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/core/graph.py) — graph and event structures.
- [event mapping](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/write/mapping.py) and [Hebbian writes](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/write/hebbian.py) — deterministic mapping, reinforcement, and decay.
- [card compiler](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/retrieve/card.py) and [activation](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/retrieve/activation.py) — compact card ranking.
- [SQLite store](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/store/sqlite_store.py) and [Postgres store](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/store/postgres_store.py) — persistence and per-profile filtering.
- [service](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/service.py) — consent, writes, retrieval, mutation, export, and deletion.
- [remote MCP](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/api/remote.py), [audit](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/audit.py), [safety](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/fernme/safety.py) — profile binding, audit, and input sanitation.
- [embedding guide](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/docs/embedding.md), [semantic search docs](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/docs/semantic.md), [security guide](https://github.com/mirkofr/FERNme/blob/e1763d50cd3700bdb3db46f0903b8c28662edc8b/SECURITY.md).
- Official [repository page](https://github.com/mirkofr/FERNme), [main commit API](https://api.github.com/repos/mirkofr/FERNme/commits/main), and [commit patch](https://github.com/mirkofr/FERNme/commit/e1763d50cd3700bdb3db46f0903b8c28662edc8b.patch) — identity, branch, head SHA, and current head.
- Project-owned [METRICS.md](../METRICS.md), [initial benchmark status](../results/initial-baselines-status.json), and [fixture](../fixtures/memory-benchmark-v1.json).

---
