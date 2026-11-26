# AgentRecall-X source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 27 / AgentRecall-X / `agentrecall-x`  
**Listed repository locator:** [Goldentrii/AgentRecall-X](https://github.com/Goldentrii/AgentRecall-X)  
**Current canonical repository:** [Goldentrii/AgentRecall-X](https://github.com/Goldentrii/AgentRecall-X)  
**Default branch / reviewed head:** main / `bc03054aa12e1e766bac0780ef4a80e9a4dfb841`  
**Review time:** 2026-11-24 19:10:02 UTC (11:10:02 PST; America/Los_Angeles).

## Identity and scope

The curated roster places AgentRecall-X at ordinal 27 with slug `agentrecall-x` and listed repository locator `https://github.com/Goldentrii/AgentRecall-X`. Its source attribution is the Agent Memory Atlas record pinned at revision `19199a4fc249e89c0793be06f0b166b358089ba0`. The roster is used only for identity, locator, and attribution. Atlas descriptions, marks, prose, and layout are not assessment evidence. The official public GitHub page identifies `Goldentrii/AgentRecall-X` and default branch `main`; the current main commits feed identifies reviewed head `bc03054aa12e1e766bac0780ef4a80e9a4dfb841`. [[curated roster](../data/memory-systems.json)] [[repository](https://github.com/Goldentrii/AgentRecall-X)] [[main commits feed](https://github.com/Goldentrii/AgentRecall-X/commits/main.atom)] [[reviewed commit](https://github.com/Goldentrii/AgentRecall-X/commit/bc03054aa12e1e766bac0780ef4a80e9a4dfb841)]

AgentRecall-X is an open-source TypeScript project offering a local-first memory framework and MCP server, SDK, and CLI, plus a hosted multi-user service. Its README frames the core use as carrying user corrections and project state across agent sessions. The README documents hosted proposals that wait for the account owner’s approval and a local installation whose files remain on the machine by default. These are project documentation statements; deployment behavior was not exercised here. [[README](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/README.md)]

## Architecture and data model

**Documentation observation.** The README describes journal, semantic palace rooms, procedural skills, project pipeline history, and a persistent correction ledger, plus awareness items that can compound across projects. Local storage is plain Markdown/JSON under `~/.agent-recall/`; project records live under `projects/<slug>/`. The hosted deployment uses the same layout under a per-user tenant directory. Optional Supabase adds vector and full-text search. The default local MCP server is stdio; the hosted server uses Streamable HTTP and OAuth. [[README](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/README.md)]

**Code observation.** The correction store defines records with an id/date, project, severity, rule and context, tags, kind, holder/authorship, and active/retraction/supersession state. Optional fields track proof count and confidence, retrieval and outcome counts, heeded/recurrence precision, prediction counters, and failure class. Correction files are stored in the project’s corrections directory. Corrections are intentionally separate from transient journal entries and semantic palace memory. [[corrections store](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/storage/corrections.ts)]

## Write, update, delete, and retrieval

**Write and correction — documentation and code observations.** The README describes `remember` for saving facts and `check` for recording human corrections with a rule, rationale, and applicability. The correction store represents corrections as structured project records. For hosted use, README instructions say proposed corrections are staged until the memory owner approves them; local corrections are stored in the local project tree. Source inspection supports the record model and project file location; this review did not exercise an actual write. [[README](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/README.md)] [[corrections store](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/storage/corrections.ts)]

**Update and retraction — code observation.** The record model supports inactive/superseded records, `superseded_by`, `merged_from`, and soft retraction with timestamp and reason; the source documents that retracted records remain on disk. The README presents correction refinement and consolidation as part of its workflow. These fields preserve lifecycle context in the store, but this inspection does not establish that every edit path maintains a complete audit history or that removed content is erased from every copy. [[corrections store](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/storage/corrections.ts)] [[README](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/README.md)]

**Pre-action retrieval — code observation.** `check_action` resolves the project and compares action-description tokens with project corrections, behavior policies, and awareness items. The result can include matched records and a warning; it returns `blocked` only for a matching authoritative P0 correction that is not classified as a low-signal noise candidate. The matcher is deterministic keyword overlap, not an LLM call. The source also attempts to record a triggered outcome best-effort, without allowing outcome logging to change the check result. A source comment says this trigger channel is dormant in the maintainer’s live harness; that comment describes instrumentation status, not a result measured in this review. [[check-action implementation](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/tools-logic/check-action.ts)]

**Session and general recall — documentation observation.** The README says `session_start` loads project context, `recall` searches across stores using reciprocal-rank fusion, and results can receive usefulness feedback. It documents a default “cards” startup mode with owner identity, hard rules, and project state, with a fuller mode for additional context. The reviewed session-start source assembles project corrections, policies, identity/state, and optional broader context; it documents a cards mode and a full payload path. The request was read-only, so no retrieval behavior was executed. [[README](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/README.md)] [[session-start implementation](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/tools-logic/session-start.ts)]

**Delete and retention — code/documentation observation.** Correction records have a soft-retraction field and remain on disk according to the store’s source comments. The hosted privacy policy says account deletion removes the memory space and replaced imports are held in a server-side trash folder for seven days. These descriptions do not establish hard deletion from snapshots, backups, or every external mirror; no deletion probe was run. [[corrections store](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/storage/corrections.ts)] [[privacy policy](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/PRIVACY.md)]

## Scope isolation, provenance, and evidence

**Scope observation.** Local correction paths are rooted under the resolved project directory. The hosted README and privacy policy describe one private memory tree per user/account; hosted correction proposals wait for approval by that owner. These project and tenant boundaries are visible in path construction and documentation, but no cross-project or cross-account probes were run. Awareness can be cross-project by design, so it should not be conflated with project-local correction storage. [[project path implementation](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/storage/paths.ts)] [[corrections store](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/storage/corrections.ts)] [[README](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/README.md)]

**Provenance observation.** Correction records can identify a holder or hosted proposing credential, classify the memory kind, retain retraction reasons, supersession links, merge origins, and evidence/proof counters. The privacy policy says hosted activity records tool names and counts but not request content. These data support lifecycle and origin tracing; they do not by themselves provide claim-level citations or show that generated claims are supported by cited source passages. [[corrections store](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/storage/corrections.ts)] [[privacy policy](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/PRIVACY.md)]

## Source-visible efficiency and observability

**Code/documentation observations.** The pre-action matcher uses local tokenization and overlap and contains no model call on that path. The README describes plain-file local storage and makes vector search optional. Session-start documents a bounded cards payload, while the README states a target of fewer than 400 tokens for combined cold start; these are design/documentation facts, not measured resource use in this review. [[check-action implementation](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/tools-logic/check-action.ts)] [[session-start implementation](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/tools-logic/session-start.ts)] [[README](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/README.md)]

The hosted privacy policy describes request duration and daily aggregate response-time counts, tool-call counts, errors, and page views. It says hosted request logs exclude request bodies and query strings. This is source documentation about available observability, not a runtime sample or latency result from this review. [[privacy policy](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/PRIVACY.md)]

## Project metric domains

All benchmark domains are **unmeasured in this review**. Source and documentation show recall, correction, soft-retraction, and scope mechanisms, but this review does not provide adjudicated answerable recall, abstention, correction accuracy, stale-value, deletion-leak, cross-scope-leak, evidence-support, or citation-coverage results. No latency distribution, write-to-recall delay, token or cost totals, or corpus storage measurements were collected. The project’s definitions and result record are separate from these source observations. [[metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded read-only review of the official repository README, privacy policy, current main head metadata, and selected TypeScript source at the pinned SHA. It does not establish production reliability, recall quality, correction effectiveness, claim support, complete deletion across backups or mirrors, or runtime performance. The hosted privacy policy and README describe service behavior; no hosted account or system was used. Unknown means not verified in this review. [[README](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/README.md)] [[corrections store](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/storage/corrections.ts)] [[check-action](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/tools-logic/check-action.ts)]

## Contact-list follow-up

The official README points users with hosted-service privacy questions to the project’s privacy policy. That policy publishes Tong Wu’s contact email, `tongwu0824@gmail.com`. The JSON record stores the address and exact pinned source URL. No commit metadata, personal profile email, third-party directory, or inferred address was used. [[README](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/README.md)] [[official privacy policy](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/PRIVACY.md)]

## Benchmark status

**Benchmark not run.** No AgentRecall-X system execution, benchmark, or test was run. Source and documentation observations are not measured results. See the project-owned metric definitions, execution status, and fixture for the separate evaluation protocol. [[metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical GitHub repository](https://github.com/Goldentrii/AgentRecall-X)
- [Current main branch commits feed](https://github.com/Goldentrii/AgentRecall-X/commits/main.atom)
- [Reviewed main branch head commit](https://github.com/Goldentrii/AgentRecall-X/commit/bc03054aa12e1e766bac0780ef4a80e9a4dfb841)
- [README.md](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/README.md)
- [PRIVACY.md](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/PRIVACY.md)
- [packages/core/src/storage/corrections.ts](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/storage/corrections.ts)
- [packages/core/src/storage/paths.ts](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/storage/paths.ts)
- [packages/core/src/tools-logic/check-action.ts](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/tools-logic/check-action.ts)
- [packages/core/src/tools-logic/session-start.ts](https://github.com/Goldentrii/AgentRecall-X/blob/bc03054aa12e1e766bac0780ef4a80e9a4dfb841/packages/core/src/tools-logic/session-start.ts)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and source attribution](../data/memory-systems.json)

**Verification boundary:** no AgentRecall-X system, tests, or benchmarks were run.
