# HoloMem source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 306 / holomem / `holomem`  
**Listed repository locator:** [polmanas1998-star/holomem](https://github.com/polmanas1998-star/holomem)  
**Canonical upstream:** [polmanas1998-star/holomem](https://github.com/polmanas1998-star/holomem)  
**Default branch / reviewed head:** main / [b09cb1b05a96bd4d271d3a2aad27ec93006cb596](https://github.com/polmanas1998-star/holomem/commit/b09cb1b05a96bd4d271d3a2aad27ec93006cb596)  
**Review time:** 2026-11-25 23:23:41 UTC (2026-11-25 15:23:41 PST; America/Los_Angeles).

## Identity and review pin

The curated roster lists HoloMem at ordinal 306, slug `holomem`, with the explicit locator `https://github.com/polmanas1998-star/holomem`. Its pinned Agent Memory Atlas entry is recorded only as roster attribution, not as assessment evidence. The official repository page identifies `main`; the official `main.atom` feed reports full head `b09cb1b05a96bd4d271d3a2aad27ec93006cb596`, and a fresh shallow checkout plus `git ls-remote --symref` independently resolve the same branch and SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

HoloMem is a small NumPy library implementing Fourier Holographic Reduced Representation (FHRR) for relational facts. It keeps an in-memory fact list as the source of truth and derives a current weighted trace plus a second trace keyed by the month each fact was learned. It can retrieve subjects and objects in either direction, gate uncertain answers, age and reinforce facts, and damp contradicted facts. The repository README also publishes capacity and cost benchmarks; those are upstream-reported figures, not measurements made for this review.[[readme]][[core]]

## Who and what

The official README describes HoloMem as a memory component built for the Dermioz assistant. The upstream is a single-module Python library with NumPy as its runtime dependency; it does not provide a persistence service or integration server in the reviewed tree.[[readme]][[packaging]][[core]]

## Architecture and data model

Each `Fact` stores subject, relation, object, a mutable weight, creation timestamp, and last-confirmed timestamp. Names are folded to normalized symbols; a deterministic BLAKE2 hash seeds a NumPy generator for each symbol vector. The instance holds a Python fact list and lazily builds two complex-valued traces: one for current relational recall and one that also binds the creation month. Mutations invalidate both traces, which are rebuilt from the facts on the next read.[[core]]

Binding multiplies unit phasors elementwise; unbinding multiplies by the conjugate. A query unbinds the current trace with a subject/relation pair, then scores every known object candidate by normalized complex cosine and returns the top candidate, score, and margin. The inverse query decodes a subject using relation/object. The dated query uses the epochal trace with an `epoch:YYYY-MM` symbol. The gated query abstains when the top score is not sufficiently separated from the other candidates, using a z threshold when there are at least three candidates and an absolute floor for smaller pools.[[core]][[readme]]

## Write, update, delete, and retrieval

**Write and reinforcement.** `learn` scans the fact list for an exactly matching folded triple. A match increases weight by 0.25, capped at 1.5, updates `last_seen_ts`, invalidates the traces, and returns false; a new triple is appended at the supplied weight and timestamp (or current clock time) and returns true. There is no disk write or durable store in this module.[[core]]

**Correction and deletion.** `contradict(subject, relation, object)` multiplies the weight of other objects for that subject/relation by 0.35; omitting object damps every object for the pair. This preserves the old fact at reduced weight rather than replacing or auditing it. `forget_faded` physically removes facts whose decayed effective weight is below 0.18, but there is no direct delete-by-key operation, tombstone, or mutation history. A faded fact can remain in the fact list until that cleanup method is explicitly called.[[core]]

**Retrieval.** `query` always returns the highest-scoring known object candidate, even when confidence is low. `query_gated` may return no object; `query_subject` retrieves the inverse relation; `query_at` decodes a month-specific object. Candidate pools are assembled from the retained fact list, including facts that are currently too faded to contribute to the trace. No natural-language, document, or semantic embedding search is implemented.[[core]][[readme]]

## Scope isolation

The reviewed API has no tenant, user, project, or namespace field and no access-control boundary. Each `HolographicMemory` instance can be used as a separate in-memory object by its caller, but isolation, lifecycle, and secure separation are caller responsibilities and were not tested.[[core]]

## Provenance and evidence

The stored fact records creation and last-confirmed timestamps and a weight, but no origin, supporting document, source citation, author, trust state, or mutation log. Month-level lookup is based on creation time; it is not a full valid-time/record-time history. Contradiction damping lets a reduced-weight old triple remain queryable, but it does not retain evidence explaining why the belief changed.[[core]]

## Efficiency and observability

The trace is fixed at dimension `d`, but total state is not: the Python fact list and symbol candidates grow with fact count. `learn` linearly scans existing facts, so repeated insertion is quadratic overall; trace rebuild is linear in fact count with vector work per fact. Each query scores and sorts the candidate pool. A process-global symbol cache is capped at 4096 entries and cleared wholesale at capacity. The inspected module has no telemetry, timing, or cost instrumentation. The README publishes benchmark tables and reproduction commands; this review did not run those scripts or verify their figures.[[core]][[readme]][[packaging]]

## Metric-domain evidence

Project benchmark domains are **unmeasured here**. Source structure and upstream README claims are not results from this project evaluation. The [metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the project protocol and current status.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Approximate candidate retrieval and an abstaining gate exist; quality was not evaluated here. | Unmeasured |
| Correction and stale values | Contradiction dampens conflicting facts; no correction workload was run. | Unmeasured |
| Deletion leakage | Explicit cleanup exists for faded facts; no deletion probe or persistence boundary was evaluated. | Unmeasured |
| Scope isolation | The API contains no scope identifiers or authorization; no isolation probe was run. | Unmeasured |
| Evidence support and citations | Fact records do not contain source evidence; no claim support was adjudicated. | Unmeasured |
| Latency and write-to-recall delay | No runtime timings were collected for this review. | Unmeasured |
| Tokens, cost, and storage | No token/cost/storage measurements were collected; the in-memory fact list grows with N. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the current README, packaging metadata, and `holomem.py` at the verified head. HoloMem, its tests, and its benchmark scripts were not run. Performance and quality values in the README remain upstream-reported and are not reproduced results from this review.[[readme]][[core]]

The repository does not define persistence, multi-process coordination, authorization, or application-level evidence capture. This review cannot establish behavior when callers serialize or share the fact list, actual retrieval accuracy on external workloads, or production latency and cost.[[core]][[packaging]]

## Benchmark status

**Benchmark not run.** No HoloMem runtime, test suite, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe project evaluation materials, not HoloMem measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README points to Dermioz as the associated project. I checked the pinned README and the official Dermioz website; the website publishes `hello@dermiozai.com`. The structured record stores that address with the exact official website URL, without using profile, commit, or third-party metadata.[[readme]][[contact]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas source records curated roster attribution only and is excluded from assessment evidence. See the structured record [holomem.json](../data/system-reviews/holomem.json) and [curated roster](../data/memory-systems.json).
