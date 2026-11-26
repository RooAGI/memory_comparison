# CASS — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 113 — CASS / `cass-memory-system`  
**Listed repository:** [Dicklesworthstone/cass_memory_system](https://github.com/Dicklesworthstone/cass_memory_system)  
**Canonical upstream:** same repository; default branch `main`; reviewed head `f4cefd2726e527f4a027cc4673412490daf69b84`  
**Review time:** 2026-11-25 07:40:16 UTC (2026-11-24 23:40:16 PST; America/Los_Angeles)

## Identity and scope

The local roster places CASS at ordinal 113 and lists the explicit repository locator above. The catalog’s Atlas source attribution is retained only to identify the roster entry and locator; Atlas descriptions and capability marks were not used as assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cass-memory-system.md)]

GitHub’s official repository metadata identifies the repository and its default branch as `main`. The current branch head was independently resolved by `git ls-remote` and a shallow checkout, both returning the full SHA recorded above.[[repository](https://github.com/Dicklesworthstone/cass_memory_system)] [[reviewed head](https://github.com/Dicklesworthstone/cass_memory_system/commit/f4cefd2726e527f4a027cc4673412490daf69b84)]

The repository describes cass-memory as procedural memory for AI coding agents. Its CLI and library work over local files and the separate `cass` session-search tool; this source review does not establish deployed or runtime behavior.[[README](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/README.md)]

## Architecture and data model

**Code observation.** The system separates raw session history (searched through `cass`), working-memory diary entries, and a procedural playbook of rules. The playbook is YAML with bullets carrying content, category, kind/type, scope, state and maturity, helpful/harmful feedback events, timestamps, pin/deprecation fields, source sessions and agents, reasoning, and tags. Zod schemas validate and default persisted records while preserving supported extension fields.[[types](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/types.ts)] [[playbook](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/playbook.ts)] [[README](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/README.md)]

Global and repository playbooks can be merged for context retrieval. Semantic embeddings are derived and cached separately rather than persisted back into the playbook YAML. Semantic retrieval can use the local Transformers model or configured Ollama; a keyword-only path remains available when semantic retrieval is off or unavailable.[[playbook](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/playbook.ts)] [[context](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/commands/context.ts)] [[README](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/README.md)]

## Write, update, delete, and retrieval

**Write and update — code observation.** Reflection turns a diary and optional session-search history into structured proposed deltas using the configured LLM. The curation stage checks duplicates and conflicts, adds feedback/provenance, merges compatible rules, and applies lifecycle changes before the playbook is saved. Manual playbook operations and feedback commands also mutate rule records. The checked write path validates bounded YAML, uses a lock and atomic write, and checks pending reflection-commit state before replacing the file.[[reflect](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/reflect.ts)] [[curation](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/curate.ts)] [[playbook](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/playbook.ts)]

**Forget and delete — code observation.** `cm forget` appends the rule ID, text, reason, and timestamp to a separate global or repository `blocked.log`, then marks the playbook bullet retired/deprecated; optional inversion creates an anti-pattern. Active retrieval excludes retired/deprecated bullets. The inspected command is a logical removal from active use with retained blocklist/provenance data, not physical erasure of every historical copy or backup.[[forget](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/commands/forget.ts)] [[playbook](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/playbook.ts)]

**Retrieval — code observation.** `cm context` merges applicable playbooks, drops inactive rules, filters workspace rules against the canonical requested workspace and named language/framework/task selectors, then ranks keyword and optionally embedding similarity together with confidence/feedback scoring. Results are capped by relevance, maximum bullet count, and estimated token budget; optional history queries call `cass`. A failed semantic attempt falls back to keyword scoring and exposes that mode/error in structured output.[[context](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/commands/context.ts)] [[scoring](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/scoring.ts)]

## Scope isolation

Bullets support global, workspace, language, framework, and task scopes. Context retrieval applies workspace matching and explicit selector values before ranking. Omitting a selector leaves that named scope’s values eligible, so callers that need a narrower result must supply the selector. The inspected design provides applicability filtering, not an authenticated multi-tenant security boundary; no cross-workspace isolation probes were run.[[types](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/types.ts)] [[context](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/commands/context.ts)] [[README](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/README.md)]

## Provenance and evidence

A bullet records source session paths and agent identities, plus reasoning and search pointers; feedback events can retain a session path, context, reason, timestamp, and outcome/evidence identifiers. Reflection overwrites any model-supplied source path with the diary’s actual session path before curation. The `cm why` workflow surfaces rule provenance and related session history. This is source lineage for memories; the inspected context result does not promise claim-level citations for downstream generated answers.[[types](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/types.ts)] [[reflect](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/reflect.ts)] [[README](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/README.md)]

## Efficiency and observability

The source uses bounded playbook reads, optional cached local embeddings, relevance/maximum-result/token-budget selection, and batched audit work. These are implementation mechanisms, not measured efficiency. The repository includes usage-event logging for command duration, success, feedback, reflection totals, playbook changes, and errors, plus status/statistics and audit commands. No latency telemetry, token/cost measurement, or storage-efficiency result was collected for this review.[[playbook](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/playbook.ts)] [[context](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/commands/context.ts)] [[tracking](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/tracking.ts)] [[audit](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/audit.ts)]

## Contact

The official pinned README was checked for a contact email and does not publish one; the record stores `contact_email: null` with that exact checked URL.[[README](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/README.md)]

## Metric-domain evidence

All benchmark domains remain unmeasured: answerable retrieval and abstention; correction/staleness; deletion leakage; scope isolation; evidence support/citation coverage; retrieval latency/write-to-recall delay; tokens/cost; and storage efficiency. The project’s metric definitions describe planned measurements, while the initial execution-status record is `not_run`; neither fixture counts nor source structure are system results.[[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a read-only source review at the verified head. No CASS instance, system commands, tests, or benchmark workloads were run. Source inspection cannot establish live provider behavior, retrieval quality, confidence calibration, correction success, deletion completeness, authorization boundaries in deployment, latency, token/cost use, or storage per accepted memory. The separation between a workspace selector and an authenticated principal should be treated as an unknown deployment boundary, not an isolation result.

## Sources

- [Roster entry and ordinal](../data/memory-systems.json)
- [Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cass-memory-system.md)
- [Official repository and default branch](https://github.com/Dicklesworthstone/cass_memory_system)
- [Reviewed full head](https://github.com/Dicklesworthstone/cass_memory_system/commit/f4cefd2726e527f4a027cc4673412490daf69b84)
- [README.md](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/README.md)
- [src/types.ts](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/types.ts)
- [src/playbook.ts](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/playbook.ts)
- [src/commands/context.ts](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/commands/context.ts)
- [src/reflect.ts](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/reflect.ts)
- [src/curate.ts](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/curate.ts)
- [src/commands/forget.ts](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/commands/forget.ts)
- [src/scoring.ts](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/scoring.ts)
- [src/tracking.ts](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/tracking.ts)
- [src/audit.ts](https://github.com/Dicklesworthstone/cass_memory_system/blob/f4cefd2726e527f4a027cc4673412490daf69b84/src/audit.ts)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** system commands, tests, benchmarks, and runtime behavior were not executed or measured for this review.
