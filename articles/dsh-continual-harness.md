# dsh-continual-harness

**Review status:** Reviewed from code and official documentation at `main` [`0432de6bb0d66f420f1b40f3889833d14d385f9e`](https://github.com/jasen215/dsh-continual-harness/commit/0432de6bb0d66f420f1b40f3889833d14d385f9e). Review time: 2026-11-25 11:30:42 UTC (03:30:42 PST; America/Los_Angeles).

## Summary

dsh-continual-harness is a DeepSeek Harness plugin that stores reusable prompts, memories, skills, and subagent instructions in session-local and shared global layers. It injects ranked context and supports model-proposed refinements with validation, an append-only history, rollback, optional review gates, and an explicit A/B benchmark tool.[readme][types][storage][refine][driver] This is a bounded source review; the system, tests, and benchmarks were not run.

## Who and what

The official README presents the package as a plugin for DeepSeek Harness, not a standalone memory database. It integrates with host agent, session, LLM, tool, and system-prompt capabilities.[readme] The roster resolves ordinal 198 to dsh-continual-harness, slug `dsh-continual-harness`, listed repository https://github.com/jasen215/dsh-continual-harness, with explicit attribution. Its pinned Atlas entry is retained for curated identity and locator attribution only, not as assessment evidence.[catalog][atlas]

## Architecture and data model

The official repository identifies `main` as default branch.[repo] The current main commit feed reports full head `0432de6bb0d66f420f1b40f3889833d14d385f9e`, updated 2026-10-14T03:03:43Z; this review’s source links pin that revision.[head_feed][head]

The package separates entry/refinement types, filesystem state, validation and apply/rollback, projection and rendering, automatic review driver, telemetry/audit, skill materialization, and optional benchmark evaluation.[readme][types][store][driver] State schema version 1 has four entry kinds—prompt, memory, skill, and subagent—with id, version, content, and updatedAt; optional fields record title, project tags, blast radius, protection, source session, lifecycle, pin state, and last injection time.[readme][types]

The shared harness root stores global state and refinement history; session-local state and history are stored under a session key. Local entries shadow same-kind/id global entries during merge. Skill entries are also rendered as SKILL.md bundles under the configured DSH skills directory.[readme][storage][skills_fs]

A pre-step projection injects a digest-marked message and replaces the previous harness block when it changes. The default stable anchor uses the opening request and project cwd; query mode can rank against the live question. Ranking is bounded per kind and includes project priority, freshness, and id tie-breaking.[readme][render][projection]

## Write, update, delete, and retrieval

**Writes and updates.** The model can propose create, update, and delete operations through harness_refine; an optional /refine command offers the same workflow. Automatic refinement runs through the review gate on configured turn or compaction triggers.[readme][driver] Updates and deletes require a reason; create/update require content. The base system prompt is immutable, protected entries and invalid scope/layer combinations are rejected, growth is capped, and planning can detect an entry fingerprint changed since the proposal was formed.[refine]

**History and rollback.** Committed refinements increment entry versions and append an applied-edit record with before/after snapshots to refinements.jsonl. A rollback by refinement id constructs inverse edits from that history. Archive is a lifecycle update that hides an entry from injection and skill materialization; delete removes the entry from active state.[readme][types][refine][storage][rollback][skills_fs]

**Scope.** The local layer belongs to a session; the global layer is shared across sessions. Local state shadows a matching global entry. Project tags affect ranking but do not filter entries, so they are not project isolation.[readme][storage][render] Blast-radius declarations are checked against destination layer: general entries cannot be committed locally and session-scoped entries cannot be committed globally. Global writes require approval only when the optional setting is enabled; its default is false.[types][refine][approval][readme]

**Retrieval.** The plugin builds a bounded query from the session context and renders a ranked prompt overview; it does not expose a general-purpose memory search API in the reviewed README.[readme][render][projection] Injection telemetry records intended inclusion, but the implementation describes it as approximate rather than proof that the model read or cited an entry.[usage]

## Provenance, efficiency, and observability

Refinement history records action, kind, id, reason, applied status, and entry snapshots, enabling inspection and rollback. Entry metadata can retain a source session and project tags are derived from the applying session, but the reviewed record model does not provide independent source passages or complete claim-level citations.[types][refine][storage][project]

Review-gate verdicts can be appended to reviews.jsonl. The plugin log is JSONL, written with private file permissions and rotated by size; usage events are scope-qualified and aggregated as approximate injection telemetry.[audit][logfile][usage] These are code observations, not measured reliability or quality results.

The README documents bounded trajectory and prefix sizes, planner token limits, per-kind injection caps, digest deduplication, and automatic review cadence/cooldown. Stable projection is intended to preserve a reusable prefix, but no latency or token savings were measured.[readme][projection][driver][render]

## Metric-domain evidence

- Answerable retrieval accuracy and abstention — unmeasured; no answerable or unanswerable cases were run.[render][metrics][fixture][status]
- Correction accuracy and stale-value rate — unmeasured; no correction sequence or post-correction probes were evaluated.[refine][rollback][metrics][fixture][status]
- Deletion leak rate — unmeasured; no delete request or residual-data probe was run.[storage][metrics][fixture][status]
- Scope isolation leak rate — unmeasured; no cross-session or cross-project forbidden-fact probe was run.[storage][render][metrics][fixture][status]
- Evidence support precision and citation coverage — unmeasured; no response claims were adjudicated against retained evidence.[types][usage][metrics][fixture][status]
- Retrieval latency — unmeasured; no timing samples were collected.[render][metrics][fixture][status]
- Write-to-recall delay — unmeasured; no acknowledged-write probe schedule was run.[refine][projection][metrics][fixture][status]
- Tokens and cost — unmeasured; no provider usage or price data were collected.[readme][driver][metrics][fixture][status]
- Storage efficiency — unmeasured; no corpus-attributed storage size was measured.[storage][metrics][fixture][status]

Project benchmark status is [`not_run`](../data/system-reviews/dsh-continual-harness.json). See [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution-status record](../results/initial-baselines-status.json). These are protocol and status references, not measurements for this system.[metrics][fixture][status]

## Limits and unknowns

The review covers selected official documentation and source paths at the verified SHA. It did not inspect every host integration, migration, packaging, or downstream runtime behavior.[readme][types][store][refine][projection][driver]

The README documents last-writer-wins behavior for concurrent processes and automatic refinement failures that may be logged without interrupting a session. Real multi-process safety, failure recovery, tenant authorization, practical isolation, deletion residuals, generated-memory quality, and all benchmark metrics remain unverified or unmeasured.[readme][storage][driver][metrics][fixture][status]

The global approval gate is disabled by default and can be enabled by configuration; no deployment configuration was inspected.[readme][approval] Skill materialization writes to a shared configured skills directory, so session-level state boundaries do not alone establish filesystem isolation.[readme][skills_fs]

## Contact

The official pinned README was checked and publishes no contact email. The official SECURITY.md path returned File not found at the reviewed revision. The record stores null and both exact checked URLs.[readme][security]

## Sources

- [catalog] Curated memory-systems roster: ../data/memory-systems.json
- [atlas] Pinned Atlas roster attribution only: https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-continual-harness.md
- [repo] Official GitHub repository: https://github.com/jasen215/dsh-continual-harness
- [head_feed] Official main commit feed: https://github.com/jasen215/dsh-continual-harness/commits/main.atom
- [head] Official current head commit: https://github.com/jasen215/dsh-continual-harness/commit/0432de6bb0d66f420f1b40f3889833d14d385f9e
- [readme] Official README: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/README.md
- [security] Official security policy path: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/SECURITY.md
- [types] Entry and refinement types: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/types.ts
- [storage] Filesystem state storage: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/storage.ts
- [refine] Refinement validation and apply: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/refine.ts
- [store] HarnessStore: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/store.ts
- [project] Project tag derivation: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/project.ts
- [rollback] Rollback projection: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/rollback.ts
- [render] Ranking and prompt rendering: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/render.ts
- [projection] Pre-step projection: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/projection.ts
- [driver] Automatic refinement driver: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/driver.ts
- [audit] Review gate audit: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/audit.ts
- [usage] Injection telemetry: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/usage.ts
- [wrapup] Deterministic wrap-up suggestions: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/wrapup.ts
- [skills] Skill entry validation: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/skills.ts
- [skills_fs] Skill bundle reconciliation: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/skills-fs.ts
- [approval] Optional global approval gate: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/approval.ts
- [logfile] Plugin file logging: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/logfile.ts
- [benchmark] Explicit A/B benchmark contracts: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/benchmark.ts
- [score] Code-owned benchmark decisions: https://github.com/jasen215/dsh-continual-harness/blob/0432de6bb0d66f420f1b40f3889833d14d385f9e/src/score.ts
- [metrics] Project metric definitions: ../METRICS.md
- [fixture] Project benchmark fixture: ../fixtures/memory-benchmark-v1.json
- [status] Project benchmark execution status: ../results/initial-baselines-status.json
