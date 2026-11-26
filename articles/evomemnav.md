# EvoMemNav

## Identity and review pin

- **Catalog position:** 231, “EvoMemNav”; slug `evomemnav`.
- **Listed repository:** [caicaiya123/EvoMemNav](https://github.com/caicaiya123/EvoMemNav); the roster marks the locator explicit. Its pinned Atlas entry is recorded only for roster attribution and locator context.
- **Canonical upstream:** [caicaiya123/EvoMemNav](https://github.com/caicaiya123/EvoMemNav), default branch `main`. The official GitHub repository API reports `main`; official Git smart transport reports `HEAD -> refs/heads/main` at `5770e8cc31763f11374a74483c6e4b1ca982513f`, matching a shallow checkout of `main`.
- **Reviewed:** 2026-11-25 20:05:30 UTC (2026-11-25 12:05:30 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) establishes the ordinal, name, slug, listed locator, and Atlas attribution. The pinned [Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/evomemnav.md) is recorded for roster attribution only and was not used as assessment evidence.

## Summary

EvoMemNav is a training-free embodied navigation agent. Its visual-semantic graph keeps observations, object instances, rooms, and navigable views for an episode; separate experience memory retains verification counts and frontier outcomes in episode-local state and per-scene JSON files. Coarse candidate ranking and VLM selection use those scores to guide later navigation. This is a source review; EvoMemNav, tests, and benchmarks were not run.

## Who and what

The official [README](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/README.md) identifies a research evaluation codebase for the EvoMemNav navigation method and lists its authors and Fudan University affiliations. The repository describes a GOAT-Bench evaluation using Habitat, visual perception models, and an OpenAI-compatible VLM endpoint. This is an application/research codebase rather than a standalone memory service.

## Architecture and data model

The agent builds an episode-local Visual-Semantic Memory Graph (VSMGraph): visited views are linked by navigability edges; anchor views link to observed object instances; frontier views represent unexplored regions; and room labels group nodes using CLIP image/text similarity. View records point to captured images and retain object detections, positions, and anchor clusters. The graph resets at episode boundaries.[[README](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/README.md)] [[view records](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/memory/views.py)] [[VSMGraph](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/memory/vsmgraph.py)] [[agent lifecycle](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/agent.py)]

ExperienceMemory combines Episode-STM, keyed by goal L1 digest and view ID, with Scene-LTM, persisted as JSON for one scene. Anchor records count accepted and rejected goal verifications; frontier records store exponential moving averages of newly explored area and dead-end outcomes plus decayed support. Goal keys have exact-content/category/modality levels, and spatial node keys map positions to a configurable grid cell.[[experience model](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/experience/memory.py)] [[goal and cell keys](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/experience/keys.py)] [[configuration](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/cfg/evomemnav_goatbench.yaml)]

## Write, update, delete, and retrieval

**Writes and updates.** After each verification, Episode-STM records whether the anchor was accepted (`STOP`) or rejected, and temporarily suppresses rejected views. Finished frontier legs record explored-area gain and whether the gain fell below the configured dead-end threshold. At each subtask end, Scene-LTM decays existing counts/support, aggregates the new events at three goal-key levels, prunes weak or contradicted records, enforces a per-key record cap, then writes the JSON through a temporary file and atomic replacement. A new episode clears STM and reloads that scene’s LTM.[[experience model](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/experience/memory.py)] [[agent lifecycle](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/agent.py)]

**Update and delete limits.** There is no general user-facing CRUD API for memory records in the inspected repository. Updates are the agent’s accumulated verification/frontier events followed by decay, contradiction/low-support pruning, and replacement of the scene JSON file. Pruning deletes individual records; the inspected implementation exposes no explicit user-requested per-memory delete or scene purge operation. Whole LTM reset/deletion behavior was not found in the inspected experience module.[[experience model](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/experience/memory.py)] [[experience keys](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/experience/keys.py)]

**Retrieval and decisions.** At recall time, Scene-LTM chooses the most specific goal key with at least the configured number of stored cells, falling back from exact goal content to category to modality. It then looks up the current cell. Anchor reliability is acceptances divided by total decisions; frontier experience combines normalized information gain with dead-end rate. Coarse ranking also considers visible target category, room hints, recency, unexplored area, and path distance, then caps the candidate set. The fine stage asks the VLM to select among candidates; a non-certain anchor selection is replaced with a frontier when one exists. Goal verification can receive the anchor’s acceptance/rejection counts as an experience hint. A rejected anchor is temporarily suppressed, and repeated rejections trigger a frontier-only fallback period.[[experience model](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/experience/memory.py)] [[coarse policy](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/policy/coarse.py)] [[fine policy](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/policy/fine.py)] [[agent decisions](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/agent.py)]

## Scope isolation

The long-term store is partitioned by scene file; within a scene, records are keyed by goal modality/category/content and a spatial cell. Episode-STM is cleared at episode boundaries. The inspected code does not show user, tenant, project, or authorization boundaries, and the scene-file path/configuration does not establish access control. Cross-scene/user isolation was not tested.[[experience model](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/experience/memory.py)] [[experience keys](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/experience/keys.py)] [[configuration](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/cfg/evomemnav_goatbench.yaml)]

## Provenance and evidence

The experience store is trained from the agent’s own STOP/RESELECT judgments and navigation trajectory. The README says benchmark goal viewpoints are consulted only after a subtask to compute SR/SPL, and the code’s verification and frontier callbacks append those self-generated events. The inspected records do not retain source observations, evidence references, reviewer identity, or an audit history linking each aggregate score to its originating episode events. A false STOP can therefore contribute positive acceptance evidence; the README’s cautionary description of visual verification is not a formal provenance or truth guarantee.[[README](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/README.md)] [[experience model](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/experience/memory.py)] [[agent decisions](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/agent.py)]

## Efficiency and observability

The design bounds anchor/frontier candidates and VLM selection retries, uses grid-cell dictionary lookups for Scene-LTM, and configures a fixed suppression interval and record cap. Evaluation records include per-subtask wall time, VLM call count, token count, VLM time, policy/graph/frontier timings, steps, and result summaries. These are instrumentation paths visible in source; this review collected no timing, token, cost, or storage measurements.[[configuration](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/cfg/evomemnav_goatbench.yaml)] [[agent decisions](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/agent.py)] [[result recorder](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/evomemnav/eval/recorder.py)]

## Metric-domain evidence

- **Answerable retrieval and abstention:** candidate filtering, ranking, VLM selection, and a confidence gate are source-inspected; answerability and abstention were not evaluated.
- **Correction and stale values:** accept/reject feedback, decay, and contradiction pruning are source-inspected; correction accuracy and stale-value rate were not measured.
- **Deletion leakage:** pruning removes weak/contradicted records; no delete-leak or persistent-erasure workload was run.
- **Scope isolation:** per-scene file partitioning and goal/cell keys are source-inspected; no isolation workload was run.
- **Evidence support and citation coverage:** verification uses images, detected objects, and experience counts; source-grounded answer support and citation coverage were not scored.
- **Latency and write-to-recall delay:** timing fields are present in evaluation records; no timings or write-to-recall schedule were collected.
- **Tokens, cost, and storage efficiency:** recorder code tracks VLM tokens/calls and reports cost-related summaries; this review collected no token, cost, or persistent-storage measurements.

See the project’s [metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and [planned benchmark fixture](../fixtures/memory-benchmark-v1.json). These comparison documents are not EvoMemNav measurements.

## Contact

No contact email was found in the official pinned [README](https://github.com/caicaiya123/EvoMemNav/blob/5770e8cc31763f11374a74483c6e4b1ca982513f/README.md). The exact checked URL is recorded in [evomemnav.json](../data/system-reviews/evomemnav.json); no commit/profile metadata or third-party directory was used.

## Limits and unknowns

This is a source review of the verified current `main` head. EvoMemNav, its tests, and benchmarks were not run. The README reports GOAT-Bench and HM3D performance figures; these are upstream-reported results and were not reproduced or independently adjudicated here. The code review cannot establish navigation/retrieval quality, robustness to incorrect verification, cross-scene/user access control, persistent-data recovery, or operational performance. The inspected repository has no separate top-level documentation directory; the README describes the method, setup, evaluation, and results.

## Benchmark status

**Benchmark not run.** No EvoMemNav runtime, tests, or benchmarks were run. See the [project metric definitions](../METRICS.md), [shared status](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and SHA-pinned upstream links are recorded in [evomemnav.json](../data/system-reviews/evomemnav.json). The [curated roster](../data/memory-systems.json) and pinned [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/evomemnav.md) support identity and locator context only.
