# GMR source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 262 / GMR / gmr  
**Listed repository locator:** [Anchorstate-Lab/GMR](https://github.com/Anchorstate-Lab/GMR)  
**Catalog source attribution:** [Agent Memory Atlas report at catalog revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/gmr.md) (used only to identify the curated roster entry and locator)  
**Canonical repository / default branch:** [Anchorstate-Lab/GMR](https://github.com/Anchorstate-Lab/GMR) / main  
**Reviewed head:** [7bee2a081a455e9d48331af7594ee50508588d77](https://github.com/Anchorstate-Lab/GMR/commit/7bee2a081a455e9d48331af7594ee50508588d77)  
**Review time:** 2026-11-25 21:18:09 UTC (13:18:09 PST; America/Los_Angeles). GitHub metadata, official commit API, git ls-remote, and a shallow checkout agree on default branch main and full head SHA.  
**Published contact:** No email was found in the checked official [README at the reviewed revision](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/README.md); the JSON records null and that exact URL.

## Identity and scope

The curated roster places **GMR** at ordinal 262, slug gmr, with listed locator https://github.com/Anchorstate-Lab/GMR. The roster attribution points to the pinned Atlas report above. That report was used only for selected identity and locator context; none of its descriptions, capability marks, analysis, or measurements are assessment evidence.[[roster entry](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/gmr.md)]

The official repository identifies main as default. GitHub metadata and commit API, a fresh git ls-remote --symref, and a shallow checkout resolve the current head to 7bee2a081a455e9d48331af7594ee50508588d77. The inspected source links below pin to that commit.[[repository](https://github.com/Anchorstate-Lab/GMR)] [[full head](https://github.com/Anchorstate-Lab/GMR/commit/7bee2a081a455e9d48331af7594ee50508588d77)]

GMR is a Rust runtime, library, and CLI for connecting memories or one-shot conclusions to versioned observations of facts. It surfaces a bound memory when its declared grounding changes and reports whether a conclusion still stands. Memory content normally remains in an external provider or user-owned file; GMR stores the binding and grounding history. It is an anchoring layer rather than a semantic fact store or truth evaluator.[[README](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/README.md)] [[architecture](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/docs/ARCHITECTURE.md)]

## Architecture and data model

The workspace separates domain vocabulary and journal projection (gmr-core), expression evaluation, probe invocation, content-provider contracts, stores, and orchestration. Batteries and domain packs supply concrete transports, providers, and probes. The console assembles the substrate for CLI, Node, and Python entry points.[[architecture](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/docs/ARCHITECTURE.md)] [[README](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/README.md)] [[content provider](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-content/src/lib.rs)]

An Anchor combines a key, probe reference, JSON state transition rules, optional terminal states, and optional supersession. Observations record their outcome, content-addressed fact address, and versions for the declaration, probe derivation, and evaluator. Journal entries include Open, Transition, Still, Attempt, Revise, and Close; current state is reconstructed by folding the ordered entries. The SQLite backend separates journal, bindings, revocations, links, immutable sealed rationale, and mutable execution settings and queue state.[[Anchor model](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-core/src/anchor.rs)] [[Journal model](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-core/src/journal.rs)] [[probe model](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-core/src/probe.rs)] [[SQLite schema](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-store/src/sqlite/schema.rs)]

A memory reference is a provider ID plus external ID. A binding connects that reference, or a one-shot said: conclusion, to one or more Anchors. It can record the bound provider version, the reading address shown to the author, an invariant expression, source classification, and bind-time Journal sequence. The provider contract fetches current content and optionally supports historical reads or listing. GMR keeps the grounding relationship and does not copy external provider content into its Journal.[[binding](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/bind.rs)] [[provider resolution](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/memory.rs)] [[provider contract](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-content/src/lib.rs)]

## Write, update, delete, and retrieval

**Writes and updates.** Opening an Anchor invokes the probe, evaluates its initial state, and appends an Open event. Later observations append Transition, Still, or Attempt. Memory writes themselves occur in the selected external store or user file; a caller then binds or attests the provider reference to Anchor(s). Rebinding records a new assertion and its grounding basis. Criteria changes use explicit journal revisions with sealed rationale.[[observation path](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/observe.rs)] [[binding path](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/bind.rs)] [[README](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/README.md)]

**Delete and retire.** Revoke appends a revocation naming the binding tags it observed, so a future re-add is not accidentally killed by an older revocation. This removes the relation from grounded views; it does not erase provider content. Close retires an Anchor. The inspected runtime paths establish no general physical-delete operation for the external memory itself.[[binding revocation](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/bind.rs)] [[SQLite revocation schema](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-store/src/sqlite/schema.rs)] [[architecture](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/docs/ARCHITECTURE.md)]

**Retrieval and freshness.** Read projects recorded history without a new probe; observe obtains a fresh observation. Grounded reads resolve bound records against the current provider version and return distinct states including current, unverified, rewritten, gone, missing provider, unreachable, or budget not asked. A caller may request a maximum staleness and budget. For said: conclusions, GMR separately reports cited readings and declared dependencies; a conclusion can lose standing because its stated invariant breaks or its cited reading was not actually observed. These are grounding checks, not judgments of truth or semantic entailment.[[read implementation](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/read.rs)] [[architecture: read and observe](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/docs/ARCHITECTURE.md)] [[README](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/README.md)]

## Scope isolation, provenance, efficiency, and observability

The inspected substrate is assembled around a project root and provider namespace, but it does not define per-user or per-tenant authorization or a principal-aware read filter. A host sharing stores or providers across principals needs to supply its own authorization and namespace boundary. No cross-user isolation behavior was exercised.[[architecture](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/docs/ARCHITECTURE.md)] [[Anchor model](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-core/src/anchor.rs)] [[provider contract](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-content/src/lib.rs)]

Provenance is structural: fact addresses identify readings and their probe derivation; readings carry time and version data; bindings can preserve the reading shown (saw), bound provider version, source class, and invariant; and the Journal retains events and rationale hashes. These fields expose the declared basis and change history, but do not prove that prose is true or entailed by a source.[[probe model](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-core/src/probe.rs)] [[Journal](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-core/src/journal.rs)] [[binding](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/bind.rs)]

Source-visible efficiency controls include per-operation and batch budgets, bounded observation concurrency, optional scheduled queue leases, and references from repeated unchanged observations to earlier entries. SQLite indexes support journal, binding, and link lookup. Health reporting includes sighting/answer counts, whether a memory moved, failure/stall ratios, and rationale sizes. These are implementation features, not measured results; this review did not establish broad built-in telemetry coverage.[[observe](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/observe.rs)] [[architecture](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/docs/ARCHITECTURE.md)] [[health reporting](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/health.rs)] [[SQLite schema](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-store/src/sqlite/schema.rs)]

## Metric-domain evidence

| Domain | Status in this review | Source evidence |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Grounded retrieval and footing states exist; no answer-quality or abstention probes ran.[[read](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/read.rs)] [[metrics](../METRICS.md)] |
| Correction and stale-value behavior | Unmeasured | Provider rewrites can be reported distinctly; no correction workload was scored.[[read](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/read.rs)] [[provider contract](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-content/src/lib.rs)] |
| Deletion leakage | Unmeasured | Binding revocation does not establish provider erasure; no deletion probes ran.[[binding](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/bind.rs)] [[metrics](../METRICS.md)] |
| Scope-isolation leakage | Unmeasured | No principal-aware filter was found in inspected substrate paths; no isolation probes ran.[[architecture](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/docs/ARCHITECTURE.md)] [[metrics](../METRICS.md)] |
| Evidence support and citation coverage | Unmeasured | Reading addresses and dependencies are retained; no claims were adjudicated against evidence.[[read](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/read.rs)] [[metrics](../METRICS.md)] |
| Retrieval latency and write-to-recall delay | Unmeasured | Budgets and health counters are source-visible; no timed workload ran.[[observe](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/observe.rs)] [[health](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/health.rs)] |
| Tokens, cost, and storage efficiency | Unmeasured | No token, cost, or corpus-attributed storage totals were collected.[[metrics](../METRICS.md)] |
| Operational observability | Source-visible only | Health APIs expose operational counters and last failure; no runtime telemetry was collected.[[health](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/health.rs)] |

**Benchmark status:** not run. Project metric definitions, execution status, and fixture are linked here; the fixture defines a planned workload, not results.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

- This is a bounded read-only inspection of the pinned README, architecture guide, core model, runtime read/observe/bind paths, provider interface, SQLite schema, and health reporting. Other adapters, providers, and CLI policy paths were not exhaustively traced.
- GMR, tests, and benchmark workloads were not run. Runtime correctness, answer quality, provider behavior, deployed authorization, physical erasure, latency, token use, cost, and storage efficiency remain unverified.
- GMR reports whether the declared basis of a memory or conclusion changed. It does not decide whether a claim was true when written or whether the prose follows from its cited reading.
- Per-user and per-tenant access control was not found in the inspected substrate; host and provider configuration must define those boundaries.
- Revocation and Anchor closure affect grounding relationships and lifecycle. They do not by themselves erase provider content, backups, exports, or other copies.

## Sources

- [Official README at reviewed revision](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/README.md)
- [Architecture at reviewed revision](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/docs/ARCHITECTURE.md)
- [Anchor model](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-core/src/anchor.rs)
- [Journal model](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-core/src/journal.rs)
- [Probe and fact-address model](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-core/src/probe.rs)
- [Runtime read](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/read.rs)
- [Runtime observe](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/observe.rs)
- [Runtime bind/revoke](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/bind.rs)
- [Runtime memory/provider resolution](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/memory.rs)
- [Content-provider contract](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-content/src/lib.rs)
- [SQLite schema](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-store/src/sqlite/schema.rs)
- [Health reporting](https://github.com/Anchorstate-Lab/GMR/blob/7bee2a081a455e9d48331af7594ee50508588d77/crates/gmr-runtime/src/health.rs)
- [Curated roster](../data/memory-systems.json)
- [Project metric definitions](../METRICS.md)
- [Execution-status record](../results/initial-baselines-status.json)
- [Benchmark fixture, planned only](../fixtures/memory-benchmark-v1.json)
