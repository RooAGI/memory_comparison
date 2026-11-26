# Engraphis

## Identity and review pin

- **Catalog position:** 228, “Engraphis”; slug `engraphis`.
- **Listed repository:** [Coding-Dev-Tools/engraphis](https://github.com/Coding-Dev-Tools/engraphis); catalog status is explicit. The pinned Atlas attribution is retained only as roster locator context.
- **Canonical upstream:** [Coding-Dev-Tools/engraphis](https://github.com/Coding-Dev-Tools/engraphis), default branch `main`. The official repository page shows `main`; its latest commit patch supplies full head SHA `7d0a2c8a2776b154cd431af944f159f31260dca3`.
- **Reviewed:** 2026-11-25 19:56:58 UTC (2026-11-25 11:56:58 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) supplies ordinal, name, slug, listed repository, and roster attribution. The [pinned Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/engraphis.md) supports the locator attribution only; it is not assessment evidence.

## Summary

Engraphis is a local-first memory system for coding agents. Its source describes a scoped SQLite store with temporal history, graph and vector retrieval, lexical search, and MCP or dashboard interfaces. This review records source behavior only; no local benchmark or runtime result was produced.

## Who and what

The official README presents Engraphis as local-first memory for coding agents, with a Python service, MCP server, and self-hosted web dashboard. The canonical repository is Coding-Dev-Tools/engraphis. The Atlas snapshot is used only to attribute the catalog locator, not as assessment evidence.[[README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md)] [[repository](https://github.com/Coding-Dev-Tools/engraphis)]

## Architecture and data model

The SQLite schema models workspaces, repositories, sessions, and atomic memories. Memory rows carry workspace/repository/session identifiers, a session/repo/workspace/user scope, a memory type, content and summary, importance/confidence/stability fields, validity bounds, a recorded time for learned closure, and provenance metadata. The schema documents portable NumPy vectors and an optional sqlite-vec backend behind a common interface; full-text indexing uses FTS5 when available and a plain-table fallback otherwise.[[schema](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/schema.py)]

The recall module documents scope/time filtering, semantic-vector plus lexical plus graph candidate generation, reciprocal-rank fusion, retention-aware scoring, reranking, context packing, and reinforcement. The README describes hybrid vector, lexical, graph, and code-aware search, with bounded context and citations or abstention when support is weak.[[recall](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/recall.py)] [[README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md)]

The README describes a local dashboard for graph/relation views, memory health, history, review, and operator controls. Source fields include access counts and last-access times; no live observability or resource use was measured.[[README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md)] [[schema](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/schema.py)]

## Write, update, delete, and retrieval

**Write.** The README documents a Python `MemoryService.remember` call and HTTP/MCP memory interfaces. It describes typed and scoped memories. The schema includes provenance and confidence fields; the service was not executed, so persistence behavior was not verified end to end.[[README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md)] [[schema](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/schema.py)]

**Update and correction.** The README says Engraphis preserves temporal history rather than silently overwriting. The schema stores `valid_from`, `valid_to`, and `valid_to_recorded_at` separately, and the mutation module includes closure-observation helpers. These source structures support temporal representation; they do not establish correction accuracy or stale-answer behavior at runtime.[[README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md)] [[schema](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/schema.py)] [[mutations](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/mutations.py)]

**Delete.** The README documents subject erasure and describes per-subject crypto-shredding while retaining an audit record. The inspected source excerpts do not establish complete removal from every index, backup, sync peer, or derived artifact; erasure was not exercised.[[README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md)] [[schema](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/schema.py)]

**Retrieval.** The code-level overview places scope/time filtering before hybrid candidate generation, then fuses, scores, reranks, and packs context. The README documents evidence citations and abstention. Candidate counts, recall quality, and calibrated abstention were not measured.[[recall](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/recall.py)] [[README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md)]

**Scope.** Rows carry workspace, repository, session, and scope identifiers; the recall pipeline begins with scope/time filtering. This establishes explicit scope fields and a source-visible filter stage, not adversarial or cross-tenant isolation; no isolation probe was run.[[schema](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/schema.py)] [[recall](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/recall.py)]

## Provenance and evidence

The README describes provenance on memories and cited or abstaining grounded responses. The poisoning policy defines external source categories and pending/approved review states, and says suspicious content is quarantined for inspection rather than discarded or immediately trusted. This documents a governance design; no security or evidence-support evaluation was run.[[README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md)] [[poisoning](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/poisoning.py)]

## Metric-domain evidence

| Domain | Source evidence | Review status |
| --- | --- | --- |
| Answerable recall and abstention | Hybrid retrieval and abstention are described. | Unmeasured here |
| Correction and stale values | Temporal validity and closure metadata are present. | Unmeasured here |
| Deletion leakage | Subject erasure is documented; propagation was not tested. | Unmeasured here |
| Scope isolation | Explicit workspace/repository/session fields and filter stage. | Unmeasured here |
| Evidence and citations | Provenance, review states, and cited responses are described. | Unmeasured here |
| Latency and write-to-recall delay | Retrieval pipeline is source-visible. | Unmeasured here |
| Tokens and cost | Context packing is documented. | Unmeasured here |
| Storage efficiency | SQLite, FTS, and vector structures are source-visible. | Unmeasured here |
| Observability | Access counters and dashboard health/history are documented. | Available in source; no telemetry measured |

Project metric definitions: [METRICS.md](../METRICS.md). Benchmark execution record: [results/initial-baselines-status.json](../results/initial-baselines-status.json). Fixture: [fixtures/memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json). The pinned upstream README reports 71.1% lower mean retrieved top-5 context tokens (18 questions), a 54.71% lower serialized-JSON payload proxy (26 samples; 260 recalls), and 11/11 grounded decisions. These are upstream-reported fixture figures, not results independently reproduced or adjudicated in this review; benchmark status here remains not_run.[[README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md)] [[metrics](../METRICS.md)] [[record](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded source review pinned to the verified main SHA. Engraphis, its tests, and benchmarks were not run. Source structure and README statements do not independently establish reliability, retrieval quality, authorization, complete erasure, or performance. Hosted services, local configuration, and end-to-end trust boundaries were outside the inspected evidence.[[head](https://github.com/Coding-Dev-Tools/engraphis/commit/7d0a2c8a2776b154cd431af944f159f31260dca3.patch)] [[schema](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/schema.py)] [[README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md)]

## Benchmark status

**Benchmark not run.** No Engraphis runtime, tests, or benchmark workload was run. Project metric definitions and fixtures describe a measurement protocol, not Engraphis results. [METRICS.md](../METRICS.md) · [results/initial-baselines-status.json](../results/initial-baselines-status.json) · [fixtures/memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json).

## Contact

Checked the official pinned README for a published email; none was found. The structured record stores `contact.email: null` and the exact checked README URL.

## Sources

- [README](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/README.md) — project interfaces, architecture, provenance, and dashboard documentation.
- [schema](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/schema.py) — data model and backend structure.
- [recall pipeline](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/recall.py) — source-visible retrieval stages.
- [mutation helpers](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/mutations.py) — closure observations.
- [poisoning policy](https://github.com/Coding-Dev-Tools/engraphis/blob/7d0a2c8a2776b154cd431af944f159f31260dca3/engraphis/core/poisoning.py) — external-source and quarantine policy.
- [repository page](https://github.com/Coding-Dev-Tools/engraphis) — canonical repository and default branch.
- [latest main commit patch](https://github.com/Coding-Dev-Tools/engraphis/commit/7d0a2c8a2776b154cd431af944f159f31260dca3.patch) — full reviewed SHA.
- Project-owned [METRICS.md](../METRICS.md), [results/initial-baselines-status.json](../results/initial-baselines-status.json), [fixtures/memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json).
