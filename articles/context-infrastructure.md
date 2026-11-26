# Context Infrastructure — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 142 — Context Infrastructure / `context-infrastructure`  
**Listed repository:** [grapeot/context-infrastructure](https://github.com/grapeot/context-infrastructure)  
**Canonical upstream:** same repository; default branch `main`; reviewed head [74511fbd5465ac302524d9e6878fab85727fc645](https://github.com/grapeot/context-infrastructure/commit/74511fbd5465ac302524d9e6878fab85727fc645)  
**Review time:** 2026-11-25 08:51:22 UTC (2026-11-25 00:51:22 PST; America/Los_Angeles)

## Identity and scope

The project catalog places Context Infrastructure at ordinal 142, slug `context-infrastructure`, with an explicit repository locator and pinned Atlas attribution. Atlas is recorded only for curated identity and locator attribution; it is not assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/context-infrastructure.md)]

The official repository page identifies `main` as its default branch. GitHub's official main commit feed reports full head `74511fbd5465ac302524d9e6878fab85727fc645`, updated 2026-11-24T18:54:32Z. The source and documentation links below pin that SHA.[[repository](https://github.com/grapeot/context-infrastructure)] [[main commit feed](https://github.com/grapeot/context-infrastructure/commits/main.atom)] [[reviewed head](https://github.com/grapeot/context-infrastructure/commit/74511fbd5465ac302524d9e6878fab85727fc645)]

## Summary and architecture

Context Infrastructure is a reference implementation and workspace blueprint for an AI coding agent. The README describes persistent personal rules, skills, daily observations, and scheduled jobs, and explicitly frames the repository as a blueprint that requires user-specific data and configuration. Markdown files in the workspace are the canonical store; the README says semantic search has moved to a separately installed public skill repository.[[README](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/README.md)]

The documented model has three layers: L3 rules and user constraints loaded at session start, L1 dated observations written to `contexts/memory/OBSERVATIONS.md`, and L2 reflection that proposes reusable rules from observations. The observer and reflector are Python trigger scripts that create OpenCode sessions; the agent reads workspace files and writes Markdown. There is no central database or service in the described core.[[PRD](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/docs/PRD.md)] [[observer source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/observer.py)] [[reflector source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/reflector.py)]

## Write, update, delete, and retrieval

**Write.** The L1 observer first checks whether a dated entry already exists, then asks the OpenCode agent to inspect workspace changes and append observations to the Markdown log. The prompt requests relative file paths and High/Medium/Low tags. The trigger itself does not extract facts or validate claims; those tasks are assigned to the agent.[[observer source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/observer.py)] [[PRD](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/docs/PRD.md)]

**Update and correction.** The observer's date check makes repeated runs for the same date skip writes, rather than revising an existing day's block. At the reviewed head, the reflector's default proposal stage reads observations and writes candidate rules with a target path, exact proposed change, reason, and source entries. It snapshots `rules/` and fails if proposal generation changes any rule file. A human must approve candidates in the file before a separate `--apply` invocation merges approved changes and removes corresponding/expired observations. Thus rule promotion has an explicit review gate, while the inspected observer does not establish a fact correction or versioned correction ledger.[[observer source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/observer.py)] [[reflector source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/reflector.py)]

**Delete and retention.** The reflector's approved apply stage garbage-collects observations after rule integration and removes expired Low entries. This is Markdown rewriting; inspected sources do not establish deletion from Git history, backups, or copies. The observer has no general delete operation.[[reflector source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/reflector.py)] [[PRD](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/docs/PRD.md)]

**Retrieval.** `AGENTS.md` is the session-start route into workspace rules and directory guidance. The PRD describes pull-based access to the observation log and sparse, task-selected context rather than injecting the entire log. Semantic search is an optional separately installed skill, so this repository alone does not provide that retrieval implementation. No ranked retrieval API or built-in answerability gate was established in the inspected files.[[README](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/README.md)] [[PRD](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/docs/PRD.md)]

## Scope isolation

The design is a single workspace for one user's agent context. Rules and observations are shared across the workspace; the inspected scripts have no user, tenant, project, or agent authorization boundary. Isolation therefore depends on separate workspaces and the host filesystem/runtime permissions.[[README](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/README.md)] [[observer source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/observer.py)]

## Provenance and evidence

Observation entries are dated, tagged, and instructed to include workspace-relative paths; current reflector candidates carry source observation references and a rationale. The README presents many rules and skills as accumulated experience, but the inspected flow does not establish durable claim-level citations, truth-status tracking, or a mutation audit across edits and deletion. Priority tags express retention or importance categories, not verified truth.[[observer source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/observer.py)] [[reflector source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/reflector.py)] [[PRD](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/docs/PRD.md)]

## Efficiency and observability

The core favors plain-text append and agent-selected reads; trigger scripts find changed files and delegate reading/filtering to OpenCode. The reflector uses file hashes to detect unauthorized changes to rules during its proposal stage. These choices avoid a required database service but depend on configured cron jobs, a reachable OpenCode server, and model work. The README and inspected scripts provide no measured latency, token, cost, or storage results.[[README](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/README.md)] [[observer source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/observer.py)] [[reflector source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/reflector.py)]

## Metric-domain evidence

All project metric domains remain unmeasured. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [existing result status](../results/initial-baselines-status.json).

- **Answerable recall and abstention — unmeasured.** No adjudicated query workload or abstention gate was run or established in the inspected core.[[README](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/README.md)]
- **Correction accuracy and stale-value rate — unmeasured.** The reflector provides a human-approved rule change path, but no correction workload was run.[[reflector source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/reflector.py)]
- **Deletion leakage — unmeasured.** Apply-stage garbage collection exists; no post-delete checks across Git history or copies were performed.[[reflector source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/reflector.py)]
- **Scope isolation — unmeasured.** The inspected design is workspace-based; no cross-user or cross-project workload was run.[[observer source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/observer.py)]
- **Evidence support and citation coverage — unmeasured.** No answers were evaluated for claim support or citation correctness.[[PRD](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/docs/PRD.md)]
- **Retrieval latency — unmeasured.** No timing distribution was collected.
- **Write-to-recall delay — unmeasured.** No timed write-then-recall workload was run.
- **Tokens and cost — unmeasured.** No token or provider-cost accounting was performed.
- **Storage efficiency — unmeasured.** No corpus storage measurement was collected.[[README](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/README.md)]

## Limitations and unknowns

This review inspected the README, PRD, observer and reflector at the verified current head. It did not inspect every rule, skill, job, or external semantic-search implementation. The scripts contain workspace/model placeholders and require local OpenCode and cron configuration, so the repository is a reference setup rather than a configured turnkey service. Retrieval relevance, fact accuracy, conflict handling, correction quality, deletion completeness, and the effect of model or prompt changes remain unknown. No Context Infrastructure runtime, tests, or benchmarks were run.[[README](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/README.md)] [[observer source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/observer.py)] [[reflector source](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/periodic_jobs/ai_heartbeat/src/v0/reflector.py)]

## Contact

The official pinned README and the official SECURITY.md path were checked. The README publishes no contact email, and the repository has no SECURITY.md at the reviewed head; no profile/commit metadata or third-party directory was used.[[README](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/README.md)] [[SECURITY.md check](https://github.com/grapeot/context-infrastructure/blob/74511fbd5465ac302524d9e6878fab85727fc645/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No Context Infrastructure runtime, tests, or benchmarks were run for this review. Source observations and upstream claims are not project benchmark results. See [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [result status](../results/initial-baselines-status.json).
