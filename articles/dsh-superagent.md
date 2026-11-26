# dsh-superagent

## Identity and review pin

- Catalog ordinal: 203
- System: dsh-superagent
- Slug: `dsh-superagent`
- Listed repository: https://github.com/deepseek-ai/dsh-superagent-prototype
- Roster attribution: explicit repository locator; the pinned Atlas report is used only for curated identity and locator context ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-superagent.md)).
- Canonical upstream: https://github.com/deepseek-ai/dsh-superagent-prototype
- Default branch: `main`
- Reviewed full head: [8c32a9dc5d72c033816c6a8110b37f40cf94fba4](https://github.com/deepseek-ai/dsh-superagent-prototype/commit/8c32a9dc5d72c033816c6a8110b37f40cf94fba4)
- Review timestamp: 2026-11-25T11:48:06Z (UTC; 2026-11-25 03:48:06 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

dsh-superagent is a proactive coding agent bundle for one GitHub repository, with optional Feishu integration. Its durable state tracks incoming events, conversation threads, routing decisions, authorized work tickets, worker assignments, settings and prompt revisions, plus a queue for side effects. It runs a main orchestration session and a separate worker session and directory per ticket; it is a research prototype rather than a general-purpose memory service. This assessment is pinned to the verified current `main` head and is source-based, not a runtime or benchmark assessment. ([README](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/README.md), [domain model](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/001-domain.md), [architecture](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/007-architecture.md))

## Who and what

The official README describes the repository as a research prototype for reference, says it is not an official DeepSeek product and is not production-ready, and notes that its published implementation differs from an internal version and the accompanying research article. It describes a DeepSeek Harness bundle that listens to GitHub and optionally Feishu, then opens and works on a human-requested or policy-admitted work item. ([README](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/README.md))

The official GitHub repository page identifies `main` as the default branch. Its official main commit feed reports full head 8c32a9dc5d72c033816c6a8110b37f40cf94fba4, updated at 2026-10-31T12:06:31Z; read-only `git ls-remote --symref` and a shallow checkout independently resolved `main` to the same SHA. ([repository](https://github.com/deepseek-ai/dsh-superagent-prototype), [main commit feed](https://github.com/deepseek-ai/dsh-superagent-prototype/commits/main.atom), [reviewed commit](https://github.com/deepseek-ai/dsh-superagent-prototype/commit/8c32a9dc5d72c033816c6a8110b37f40cf94fba4))

## Architecture and data model

The core Engine coordinates intake, evaluation, tickets, assignments and replies. Source adapters translate upstream events into Triggers; the main Session evaluates and routes candidates; DshExecutor creates a worker Session and directory for each Ticket. GitHub and Feishu are the bundled sources described by the README and architecture guide. ([domain model](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/001-domain.md), [architecture](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/007-architecture.md), [README](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/README.md), [runtime](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/runtime.ts))

The domain records are operational work history rather than free-form semantic memories. A Trigger holds source and actor identity, human/addressed flags, timestamp, text, thread references and source metadata. A Thread is the consistency boundary for pending triggers, an evaluation, subscriptions and decision history. A Decision records the outcome, reason, policy version, strength and optional audit; an accepted Ticket carries an immutable Mandate, origin triggers, inputs, assignments, channels and thread bindings. ([domain model](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/model.ts), [Engine](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/engine.ts))

The Store persists the core aggregates in one SQLite database: trigger, disposition, thread, ticket, decision, outbox, trigger_thread and effect tables, plus typed key-value rows for other state. JSON values hold the domain records; generated indexed columns and indexes support open/active tickets, active/subscribed threads, and pending outbox work. The connection enables WAL and `synchronous=FULL`; Engine commands use nested savepoints and post-commit callbacks. ([SQLite store](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/store.ts), [typed keys](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/kv.ts), [architecture persistence description](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/007-architecture.md))

Settings and prompt configurations are versioned snapshots. A saved revision has a monotonically increasing number and becomes the current pointer; prompt saves are checked against a base revision, and a rollback is saved as another revision. A durable SQLite effect queue writes side-effect requests within the command transaction and dispatches after commit with concurrency limits, retry backoff and health reporting. ([versions](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/versions.ts), [settings](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/settings.ts), [effects](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/effects.ts))

## Write, update, delete, and retrieval

**Writes and lifecycle.** Source events enter through Engine intake as Triggers, are associated with Threads and recorded with dispositions, then wait for evaluation and a routing Decision. Accepting work creates a Ticket and Assignment; worker reports, incoming messages and policy changes append or update ticket inputs and assignment state. These state transitions are written through repository operations in SQLite savepoint transactions, while external work is queued for post-commit delivery. ([Engine](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/engine.ts), [domain model](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/model.ts), [SQLite store](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/store.ts), [effects](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/effects.ts))

**Updates and correction.** Ticket state is updated in place as messages arrive, workers report, assignments retry and the work ends. A person can retry certain blocked/failed tickets, stop a ticket, or unsubscribe tickets from a thread; the domain distinguishes completed, merged, closed, dropped and stopped outcomes. This is work-state management, not a correction ledger for factual memories. Prompt and settings edits instead preserve numbered snapshots and their origin/revision information. ([ticket model](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/model.ts), [Engine commands](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/engine.ts), [main tools](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/tools/main.ts), [versions](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/versions.ts))

**Deletion and retention.** The inspected user-facing Engine and resource APIs expose stop, unsubscribe, dismiss and retry operations, but no hard-delete operation for Triggers, Decisions or Tickets. Stopping a Ticket withdraws its Mandate and ends it; it does not constitute source-level evidence of erasure of its stored history. SQLite code also deletes selected operational rows such as queued effects or key-value entries. The selected source review did not establish a retention policy or complete erasure behavior for all persisted records, logs, session transcripts or backups. ([Engine commands](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/engine.ts), [SQLite store](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/store.ts), [resources](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/resources.ts))

**Retrieval.** The `orchestrator_read` tool serves named, paginated resources such as tickets, triggers, threads, decisions, assignments, reports, inputs and transcripts. This is addressed operational retrieval; the inspected paths do not provide vector, semantic or general text search over the stored work records. The worker tool is constructed with its Ticket ID, and resource handling rejects another ticket's ticket resource, restricts trigger reads to reached/origin/followed triggers, and limits thread reads to subscribed or followed threads. On shared threads, the worker view omits the other tickets and decision history. ([resource definitions and reader](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/resources.ts), [main read tool](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/tools/main.ts), [worker tools](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/tools/executor.ts))

## Scope isolation

The primary scope is a deployment for one GitHub repository, as described in the README. At the model-facing resource layer, worker sessions are bound to a ticket and the resource reader applies ticket, trigger and thread checks; main-session resources can read the deployment's full operational state. This is an application-level boundary for the exposed read tool. The source review does not establish a separate OS account, database per worker, or tenant-grade process isolation, so the tool checks alone should not be treated as proof of isolation from arbitrary host-level access. No cross-scope workload was run. ([README](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/README.md), [worker tools](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/tools/executor.ts), [resources](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/resources.ts), [runtime](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/runtime.ts))

## Provenance and evidence

Triggers preserve source, actor, timestamp, thread references and source-provided metadata. Decisions record a policy version, strength, reason and optional assessor audit; accepted Tickets retain the Mandate basis and origin trigger IDs. Inputs and Assignments preserve work handoffs and worker reports, and each Ticket has a worker session transcript resource. This supports operational lineage from incoming event through decision and execution, but the model is not a source-cited fact store and these fields do not by themselves establish factual correctness. ([domain model](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/model.ts), [resource reader](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/resources.ts), [Engine](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/engine.ts))

## Efficiency and observability

SQLite uses WAL with full synchronous mode, indexes active work sets, and provides paged reads; the resource reader fetches text bodies on demand and caps ordinary lists. The durable effect queue supports coalescing by kind/key, concurrency controls, retries and backoff. A HealthBoard exposes component health, while ticket cards and delivery state expose worker/report and input-delivery problems. These are implementation and inspection mechanisms, not measured latency, cost, token or storage outcomes. ([SQLite store](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/store.ts), [resources](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/resources.ts), [effects](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/effects.ts), [health board](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/infra/health.ts), [architecture](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/007-architecture.md))

## Metric-domain evidence

All project benchmark domains are **unmeasured** in this review. Metric definitions, the fixture and the existing result-status record are linked as project contract/status documents only. No system runtime, tests or benchmark workload was executed. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
| --- | --- | --- |
| Answerable retrieval accuracy and abstention | Unmeasured | Addressed ticket, trigger and thread resources were inspected; no answerability cases were scored. |
| Correction accuracy and stale-value rate | Unmeasured | Ticket lifecycle and versioned configuration updates were inspected; no correction probes were run. |
| Deletion leakage | Unmeasured | Stop and unsubscribe paths were inspected; no post-deletion or retention probes were run. |
| Scope isolation | Unmeasured | Worker resource checks were inspected; no paired allowed/forbidden workload was run. |
| Evidence support precision and citation coverage | Unmeasured | Trigger and decision lineage fields were inspected; no output claims were adjudicated for support. |
| Retrieval latency and write-to-recall delay | Unmeasured | No latency samples or timed write/recall probes were collected. |
| Tokens and cost | Unmeasured | No model usage or provider charges were measured. |
| Storage efficiency | Unmeasured | SQLite table and index structure was inspected; no corpus-attributed bytes or per-item size was measured. |

## Limits and unknowns

This bounded review inspected the README, domain and architecture documentation, Engine and domain model, SQLite persistence, resource filtering, main and worker read tools, versioning, side-effect queue and health reporting. It did not inspect every Source adapter, prompt and policy rule, deployment/security setting, or external DeepSeek Harness behavior. The README itself cautions that this is research code and not production-ready; source inspection cannot establish deployed configuration, runtime correctness, isolation, deletion completeness, retrieval quality or performance. ([README](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/README.md), [architecture](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/007-architecture.md), [project metric definitions](../METRICS.md))

The official pinned README was checked for a contact email; none was published there. No commit or profile metadata or third-party directory was used. ([README](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/README.md))

## Benchmark status

**Benchmark not run.** No dsh-superagent runtime, tests or benchmarks were run. Source observations and upstream documentation statements are separate from measured results. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-superagent.md)
- [Official repository](https://github.com/deepseek-ai/dsh-superagent-prototype)
- [Official main commit feed](https://github.com/deepseek-ai/dsh-superagent-prototype/commits/main.atom)
- [Reviewed head 8c32a9dc5d72c033816c6a8110b37f40cf94fba4](https://github.com/deepseek-ai/dsh-superagent-prototype/commit/8c32a9dc5d72c033816c6a8110b37f40cf94fba4)
- [Pinned README](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/README.md)
- [Pinned domain model documentation](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/001-domain.md)
- [Pinned architecture documentation](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/007-architecture.md)
- [Pinned domain model](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/model.ts)
- [Pinned Engine](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/engine.ts)
- [Pinned SQLite store](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/store.ts)
- [Pinned runtime](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/runtime.ts)
- [Pinned resource reader](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/resources.ts)
- [Pinned main Session tools](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/tools/main.ts)
- [Pinned worker Session tools](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/tools/executor.ts)
- [Pinned settings history](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/settings.ts)
- [Pinned versioned snapshots](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/versions.ts)
- [Pinned effect queue](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/effects.ts)
- [Pinned typed key-value records](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/kv.ts)
- [Pinned health board](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/infra/health.ts)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project result/status record](../results/initial-baselines-status.json)

---