# Hats source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 284 / Hats / `one-agent-many-hats`  
**Listed repository locator:** [klairtech/one-agent-many-hats](https://github.com/klairtech/one-agent-many-hats)  
**Canonical upstream:** [klairtech/one-agent-many-hats](https://github.com/klairtech/one-agent-many-hats)  
**Default branch / reviewed head:** main / [a90396cff12b1e2fbb8a14f74eef6c6c89105b4f](https://github.com/klairtech/one-agent-many-hats/commit/a90396cff12b1e2fbb8a14f74eef6c6c89105b4f)  
**Review time:** 2026-11-25 22:32:54 UTC (2026-11-25 14:32:54 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Hats at ordinal 284, slug `one-agent-many-hats`, with the explicit locator `https://github.com/klairtech/one-agent-many-hats`. The pinned Agent Memory Atlas entry is recorded as roster attribution only and was not used as assessment evidence. The official repository page identifies `main` as the default branch; GitHub’s official `main.atom` feed gives full head `a90396cff12b1e2fbb8a14f74eef6c6c89105b4f`. The reviewed source links below use that SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Hats is a local agent runtime with several file-backed memory layers: user-authored workspace context, an inferred persona, short takeaways from earlier runs, and operational lessons. A separate workspace document index supports retrieval over project files. This review describes selected current sources; it does not establish measured memory quality or tenant isolation.[[readme]][[memory]][[rag]]

## Who and what

The official README presents Hats as a local runtime whose behavior and state are represented as readable files in a selected workspace. Its memory is part of that runtime, rather than a standalone hosted memory API.[[readme]]

## Architecture and data model

The memory facade constructs stores under one workspace directory: `memory/lessons.jsonl`, `memory/takeaways.jsonl`, `memory/persona.json`, and `org-context.md`. Composition reads authored context, inferred persona, retrieved takeaways, and operational lessons in that authority order. The authored context is treated as authoritative; inferred content is labelled as possibly stale.[[memory]][[orgcontext]][[persona]][[takeaways]][[lessons]]

A takeaway stores a run ID, short question and answer, timestamp, feedback verdict, tags, and optional embedding. Lessons carry their scope/status, confidence, origin category, injection history, counters, and tags. Persona holds a bounded list of inferred user facts. These shapes provide some lifecycle metadata, but they do not require retained evidence citations.[[types]]

The workspace document index is a distinct subsystem: it persists indexed chunks plus metadata, tracks file hashes for incremental rebuilds, and optionally stores embeddings. It can combine keyword and vector ranking; it is not the same store as the concise past-run takeaways.[[rag]][[readme]]

## Write, update, delete, and retrieval

**Write.** Post-run distillation receives the request, delivered answer, and concrete run signals, then proposes a concise takeaway, behavioral lessons, and at most one persona fact. The interface explicitly excludes the full transcript from the distillation input. Takeaways append to JSONL; persona updates are written atomically; authored workspace context is read-only to the agent.[[memory]][[takeaways]][[persona]][[orgcontext]]

**Update and correction.** Feedback applies to takeaways for a run. Accepted items receive a modest ranking boost; rejected items are omitted from retrieval; corrected items return the user correction in place of the stored answer. This changes retrieval but leaves the row in the JSONL file. The inspected takeaway store exposes no dedicated physical delete operation. Persona facts can be replaced when overlapping, individually forgotten, or cleared. Lessons are updated through confidence and lifecycle changes.[[takeaways]][[persona]][[lessons]]

**Operational lessons.** Lessons are constrained at write time to behavioral guidance and reject text that attempts to widen access or weaken controls. Failure-derived lessons start as drafts, while correction-derived ones start active with higher confidence. Draft/canary lessons are exposed to a deterministic half of runs; acceptance can promote a lesson and repeated rejection or silence can disable it. This is an implemented staged lifecycle, not measured evidence that lessons improve outcomes.[[lessons]]

**Retrieval.** Past-run retrieval searches takeaways with BM25 unless embeddings are configured and stored; the embedding path uses cosine similarity. The separate document index uses keyword/vector reciprocal-rank fusion when configured, and says when it is operating in keyword-only mode. Retrieval correctness and calibration were not evaluated.[[takeaways]][[rag]][[memory]]

## Scope isolation

The memory facade binds its stores to a workspace directory, which is the documented storage boundary. Lesson records have `run`, `workspace`, and `global` scope values, but this review did not establish that those labels are enforced as authorization boundaries across separate workspaces or processes. No tenant-isolation probe was run.[[memory]][[lessons]][[readme]]

## Provenance and evidence

Takeaways retain a run ID, and lessons retain a source category such as failure, correction, feedback, or pack. The inspected schemas do not require source citations or store supporting source snippets for recalled claims. Feedback records user verdicts but does not provide a general evidence audit for factual content; evidence support and citation coverage therefore remain unmeasured.[[types]][[takeaways]][[lessons]]

## Efficiency and observability

The architecture uses local JSON/JSONL files and BM25 for compact memory; optional embeddings and cosine scoring are available, while document indexing reuses chunks for unchanged files. The README describes run records and analytics, but no memory latency, write-to-recall delay, token, cost, or storage measurements were collected here.[[takeaways]][[rag]][[readme]][[metrics]][[fixture]][[status]]

## Metric-domain evidence

All project benchmark domains are **unmeasured here**. The [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the project evaluation materials, not Hats results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Takeaway and workspace-document retrieval are implemented; answer accuracy and abstention were not scored. | Unmeasured |
| Correction and staleness | Feedback can substitute a corrected answer and persona facts can be removed; correction accuracy and stale-value rate were not measured. | Unmeasured |
| Deletion leakage | Rejection filters retrieval, and persona/lesson controls exist; no physical takeaway delete or leakage probe was established. | Unmeasured |
| Scope isolation | Stores are workspace-bound and lessons carry scope labels; no cross-workspace isolation workload was run. | Unmeasured |
| Evidence support and citations | Takeaways have run IDs but no required evidence citations; support precision and citation coverage were not evaluated. | Unmeasured |
| Latency and write-to-recall delay | Local ranking and incremental indexing exist; no timings were collected. | Unmeasured |
| Tokens, cost, and storage | Compact records and bounded retrieval are implemented; no comparison was made. | Unmeasured |

## Limits and unknowns

This is a source review of selected official files at the verified main head. The README contains upstream statements about tests and runtime behavior; no tests, runtime, or benchmark were run as part of this task.[[readme]][[memory]][[takeaways]]

The review did not inspect every orchestration, feedback, backup, concurrency, or multi-workspace path. It cannot establish how data removal propagates to backups or copies, whether scope labels prevent cross-workspace access in all deployments, or how retrieval behaves under realistic workloads. A feedback rejection suppresses a takeaway from recall but does not physically erase its stored row.[[takeaways]][[lessons]][[persona]]

## Benchmark status

**Benchmark not run.** No Hats runtime, tests, or benchmark workload was executed. No recall, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define evaluation materials, not Hats measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README publishes `hello@klairtech.com` for ideas and commercial licensing. The structured record stores this address and the exact pinned README URL; no profile or commit metadata was used.[[readme]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas source records curated roster attribution only and is excluded from assessment evidence. See the structured record [one-agent-many-hats.json](../data/system-reviews/one-agent-many-hats.json) and [curated roster](../data/memory-systems.json).
