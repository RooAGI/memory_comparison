# Harness² source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 282 / Harness² / `harness2`  
**Listed repository locator:** [google-research/harness2](https://github.com/google-research/harness2)  
**Canonical upstream:** [google-research/harness2](https://github.com/google-research/harness2)  
**Default branch / reviewed head:** main / [6868817518876de8fd170c6a8354daca273b6191](https://github.com/google-research/harness2/commit/6868817518876de8fd170c6a8354daca273b6191)  
**Review time:** 2026-11-25 22:29:13 UTC (2026-11-25 14:29:13 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Harness² at ordinal 282, slug `harness2`, with the explicit locator `https://github.com/google-research/harness2`. Its pinned Atlas attribution is recorded only for roster identity and locator context. The official GitHub repository page identifies `main` as the default branch. GitHub’s official `main.atom` feed reports full head `6868817518876de8fd170c6a8354daca273b6191); a fresh shallow checkout resolved to the same branch and SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Harness² is a Python framework for recursively improving agent harnesses. Its persistent “experience library” retains the full adopted harness tree from earlier tasks in a benchmark domain together with an explanation and transferable lesson derived from task trajectories and deliverables. This is harness-design memory rather than a general store of user facts or conversation summaries. This review describes selected source at a verified commit; it does not execute the system or measure quality.[[readme]][[library]][[schedule]]

## Who and what

The official README presents Harness² as an open-source research framework that refines agent harness components around fixed model weights. The repository contains the framework, benchmark adapters, CLI and experiment documentation. It explicitly says it is not an officially supported Google product. No maintainer identity is inferred from commit or profile metadata.[[readme]]

## Architecture and data model

The system has two recursion loops. Task-level Propose–Probe–Compose edits an execution harness, runs candidate harnesses on the same task, and composes a refinement from observed contrasts. Harnessing-level recursion then selects an adopted result and distills evidence-supported lessons to influence later tasks. The editable surface is a framework-specific tree of components such as prompts, guardrails, memory, tool guidance, subagents, skills, scripts and plugins.[[readme]][[recursion]][[tree]]

The persistent library is filesystem-based. Its directory layout is run/mode/domain, with an `INDEX.md` and per-task entries under `harnesses/<task>/`; each entry contains the complete adopted component tree and an `EXPERIENCE.md`. The experience record includes the chosen candidate/run, component inventory, rationale, edits, cue, lesson, evidence and confidence when returned by the reflection step. The index is regenerated from disk.[[library]][[schedule]][[selection]]

## Write, update, delete, and retrieval

**Write.** After selection, reflection builds an evidence tree containing the task, candidate trajectories, deliverables, edited harnesses and relevant decisions. A distillation step emits an experience record. The scheduler calls the library writer for a successful selection only when cue, lesson and evidence are non-empty. The writer checks the adopted tree and experience text for grader-verdict markers, writes the harness and experience files, then rebuilds the index.[[selection]][[schedule]][[library]][[context]]

**Update.** Adding an entry for the same task path removes and rewrites that entry’s harness and experience before regenerating the index. The source does not expose a separate semantic-fact correction API or immutable revision history for experience entries. Run summaries and selection records hold additional provenance and resume state.[[library]][[schedule]]

**Delete.** The internal `forget(task_ids)` method removes selected task-entry directories and rebuilds the index; `retain(task_ids)` drops entries outside a supplied set. The domain stream uses retain to keep only entries preceding the current task. These are filesystem operations, not a user-facing memory erasure protocol; backup deletion, audit history and secure erasure are not established by the inspected code.[[library]][[schedule]]

**Retrieval.** The library is attached as a directory to improver sessions. Context construction exposes the domain index and full prior harness entries; the prompt asks the improver to browse the index and inspect entries that look relevant. Selection and execution roles do not receive this library through this context path. This is whole-directory availability followed by model-directed browsing, not a query-ranked retrieval API or bounded summary. Full trajectories are also included as files; individual observations can have explicit renderer truncation.[[library]][[context]][[recursion]]

## Scope isolation

Library paths separate benchmark, run configuration, recursion mode and domain. The task-stream code creates a library per mode and domain and prunes it to earlier tasks in the stream; the documented explicit tag can opt into sharing across runs. The source rejects sharing one mutable library across modes in the relevant scheduler path. These are data-layout and workflow boundaries, not tenant authorization: filesystem permissions, cross-process isolation and adversarial cross-scope probes were not evaluated.[[library]][[schedule]][[readme]]

## Provenance and evidence

The reflection input can include full candidate trajectories, deliverables, harness edits, adoption reason and stage decisions. Each stored entry names the chosen candidate and run, and the required cue/lesson/evidence fields connect the transferable statement to task evidence. Context code checks for grader-verdict markers before evidence reaches a model or an adopted harness is stored. The library does not impose a normalized citation schema linking every lesson claim to exact trajectory offsets, and its basic index contains a short cue rather than adjudicated support labels. Evidence quality and leakage resistance were not empirically tested.[[selection]][[context]][[library]]

## Efficiency and observability

The library stores complete component trees and prose evidence, so storage grows with retained tasks and harness contents; the inspected path does not summarize or deduplicate entries. Index rebuilding reads entries from disk. Context construction makes full prior trees available, which can increase browsing and context work as the library grows. The run ledger records rollout/session counts, attempts, cached state and USD cost where supplied by the executor; it does not establish token counts or persistent library byte measurements. No latency, cost, storage or write-to-recall timing was measured here.[[library]][[context]][[ledger]][[schedule]]

## Metric-domain evidence

All project benchmark domains are **unmeasured for Harness² in this review**. Source behavior and upstream README claims are not this project’s measured results. The [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define project evaluation materials, not Harness² results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Prior domain entries are exposed to improvers through an index and file browsing; no gold answer workload was run. | Unmeasured |
| Correction and stale values | Same-task entries can be rewritten, and stream pruning removes entries; no correction sequence or stale-value probe was evaluated. | Unmeasured |
| Deletion leakage | Internal task-entry deletion exists; no post-delete probe or backup-erasure test was performed. | Unmeasured |
| Scope isolation | Paths and stream operations separate domain/run/mode; no cross-domain or principal isolation workload was run. | Unmeasured |
| Evidence support and citations | Reflection stores rationale and evidence text; no claim-level citation adjudication was run. | Unmeasured |
| Latency and write-to-recall delay | Cost and execution counts are tracked in a run ledger; no latency or first-recall timing was collected. | Unmeasured |
| Tokens, cost, and storage | Executor USD cost can be recorded; token totals and library storage efficiency were not measured. | Unmeasured |

## Limits and unknowns

This is a bounded source review of the official README, experiment documentation, and selected current library, context, recursion, schedule, selection, tree and ledger modules. Harness², its tests and benchmarks were not run. The README’s experimental performance statements are upstream claims and were not independently reproduced.[[readme]][[library]][[recursion]]

The review does not establish whether model-directed browsing remains effective as libraries grow, whether reflection produces accurate transferable lessons, or whether domain/run boundaries prevent information leakage in real deployments. It did not inspect every benchmark adapter or deployment configuration. The library appears designed for sequential benchmark streams; access control, concurrent mutation guarantees and secure erasure are outside the evidence reviewed here.[[context]][[schedule]][[library]]

## Benchmark status

**Benchmark not run.** No Harness² runtime, test suite or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the project protocol and status, not Harness² measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email; it publishes none. The structured record stores `contact_email: null` and the exact checked URL. No address was inferred from commit/profile metadata or a third-party directory.[[readme]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas source records curated roster attribution only and is excluded from assessment evidence. See the structured record [harness2.json](../data/system-reviews/harness2.json) and [curated roster](../data/memory-systems.json).
