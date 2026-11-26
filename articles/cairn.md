# Cairn source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 109 / Cairn / cairn  
**Listed repository locator:** [oritera/Cairn](https://github.com/oritera/Cairn)  
**Canonical repository:** [oritera/Cairn](https://github.com/oritera/Cairn)  
**Default branch / reviewed head:** main / `8e7e0ea67552383851dfcabfba0c4e9c8d007878`  
**Review time:** 2026-11-25 00:42:06 UTC (2026-11-24 16:42:06 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog places Cairn at ordinal 109 and lists the repository above. Its Atlas source URL and revision are retained only for identity attribution; Atlas descriptions, marks, and layout were not used as assessment evidence. GitHub’s official repository page showed `main`; fresh `git ls-remote --symref` identified `main` as HEAD at `8e7e0ea67552383851dfcabfba0c4e9c8d007878`, and a shallow checkout resolved to that same full SHA.[[catalog](../data/memory-systems.json)] [[repository](https://github.com/oritera/Cairn)] [[reviewed commit](https://github.com/oritera/Cairn/commit/8e7e0ea67552383851dfcabfba0c4e9c8d007878)] [[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cairn.md)]

## Summary

Cairn is a server and dispatcher for goal-directed exploration. It stores project knowledge as a graph of facts and intents, with hints as separate project annotations, then gives worker agents the project state to explore. This review reports source observations only; no Cairn workload or benchmark was run.[[README](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/README.md)] [[server models](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/models.py)]

## Who and what

The official repository describes Cairn as a general-purpose problem-solving engine, with autonomous penetration testing as its initial validated domain. The repository is owned by the oritera GitHub account; the inspected README does not identify a separate maintainer. Cairn is an application comprising a FastAPI server and a dispatcher for Claude Code, Codex, Pi, or mock workers, rather than a standalone memory library.[[README](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/README.md)] [[server app](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/app.py)] [[dispatcher config](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/config.py)]

## Architecture and data model

The server is the protocol authority. Its SQLite database stores projects, facts, intents, intent-source edges, hints, settings, and ID counters. Facts are scoped by project and have only an ID and description; intents record source fact IDs, destination fact, description, creator, worker, and timestamps; hints contain content, creator, and creation time. SQLite connections enable WAL mode and foreign keys.[[database schema](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/db.py)] [[data models](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/models.py)]

The graph represents exploration as intents connecting one or more existing facts to a resulting fact. Hints are project-level guidance outside that causal graph. The dispatcher reads structured project state and a full YAML export, selects bootstrap, reason, or explore work, starts configured worker processes, parses their structured JSON, and writes accepted results through the server API.[[README](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/README.md)] [[protocol spec](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/docs/specs/server-protocol.md)] [[dispatcher design](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/docs/specs/dispatcher-design.md)] [[scheduler](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/scheduler/loop.py)]

By default, workers run in a container per project; the documented local mode instead uses per-project working directories on the dispatcher host and reuses installed CLI programs. The README says local workers run with host-user permissions and without a sandbox. These are execution boundaries; the inspected server API does not authenticate a caller as a project principal.[[README](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/README.md)] [[dispatcher config](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/config.py)] [[server app](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/app.py)]

## Write, update, delete, and retrieval

**Write — code observation.** Creating a project stores its origin and goal as special facts and may add initial hints. Other hints are appended through the hint route. An intent can be proposed from one or more existing fact IDs, then claimed or heartbeated by a worker; conclusion creates a new fact and connects it to the intent. A reason pass may instead propose new intents or mark the project complete.[[project routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/projects.py)] [[hint route](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/hints.py)] [[intent routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/intents.py)] [[reason task](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/reason.py)]

**Update and correction — code observation.** Project title and active/stopped status can be updated. The inspected API has no general fact edit route and no intent or hint edit route. Completion has a special reopen operation: it deletes the completion intent, appends an external-feedback fact, and creates a replacement intent using the completion's source facts. This is a narrow reopen flow rather than general correction or version history.[[project routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/projects.py)] [[intent routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/intents.py)]

**Delete — code observation.** Deleting a project removes its database row and dependent rows through foreign-key cascades. No individual fact or hint deletion route was found in the inspected routers. Reopen is the only inspected path that deletes an intent. This does not establish cleanup of exported YAML snapshots, worker files, backups, or other copies.[[project routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/projects.py)] [[database schema](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/db.py)] [[worker snapshot helper](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/common.py)]

**Retrieval — code observation.** GET project and YAML/timeline export return project data selected by project ID; the inspected API exposes no ranked or semantic fact-search endpoint. Dispatcher reason work receives the complete graph export plus fact IDs and open intents; explore receives the complete export plus its assigned intent. The prompts tell workers to read the whole graph snapshot. This is source-visible context delivery, not measured answer recall.[[project routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/projects.py)] [[export route](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/export.py)] [[reason task](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/reason.py)] [[explore task](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/explore.py)] [[snapshot helper](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/common.py)]

**Scope isolation — code observation.** Project IDs are part of composite keys and the inspected reads, writes, and exports filter on project ID. That separates project records in the data model. The app registers routes without an authentication dependency or principal-level authorization in the inspected code, so project-ID filtering alone does not establish protection between untrusted callers. Local execution also runs with host permissions.[[database schema](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/db.py)] [[project routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/projects.py)] [[export route](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/export.py)] [[server app](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/app.py)] [[README](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/README.md)]

## Metric-domain evidence

All entries below are **unmeasured**. Source structure does not establish runtime quality, isolation or cost.[[project metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

- **Answerable recall and abstention:** full-project export and whole-graph prompt delivery are visible; no adjudicated answerable or unanswerable probes were run.[[export route](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/export.py)] [[reason task](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/reason.py)]
- **Correction and stale values:** facts are not generally editable, and completion can be reopened by appending feedback; no correction or stale-value probes were adjudicated.[[project routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/projects.py)]
- **Deletion leakage:** project deletion cascades database rows, while individual fact and hint deletion is not exposed in inspected routes. No post-delete probe or copy-cleanup measurement was run.[[project routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/projects.py)] [[database schema](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/db.py)]
- **Scope isolation:** project-key filters are source-visible, but caller-principal authorization was not located in the inspected route setup and no forbidden cross-project workload was run.[[database schema](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/db.py)] [[server app](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/app.py)]
- **Evidence and citations:** intent edges preserve contributing fact IDs and worker/creator labels; fact records do not require source citations. No evidence-support or citation-coverage adjudication was performed.[[data models](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/models.py)] [[intent routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/intents.py)]
- **Latency and write-to-recall delay:** dispatcher logs selected phase and total durations, but no latency samples or write-to-recall timing were collected.[[worker helpers](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/common.py)] [[explore task](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/explore.py)]
- **Tokens, cost, and storage:** SQLite persistence and prompt snapshots are source-visible; no token usage, price, or storage measurements were collected.[[database schema](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/db.py)] [[worker helpers](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/common.py)]

## Limits and unknowns

This is a bounded read-only source inspection at the verified `main` head. The server, dispatcher, worker adapters and benchmark were not executed; source presence does not establish runtime correctness or effective retrieval.[[repository](https://github.com/oritera/Cairn)] [[reviewed commit](https://github.com/oritera/Cairn/commit/8e7e0ea67552383851dfcabfba0c4e9c8d007878)]

The model has no required evidence URL or citation field on facts. Project-ID scoping does not prove tenant isolation because caller authentication was not located in the inspected route setup. Individual fact/hint erasure and cleanup of copies outside SQLite remain unestablished.[[data models](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/models.py)] [[server app](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/app.py)] [[database schema](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/db.py)]

The README reports the project's participation and results in a Tencent Cloud hackathon, including a 54/54 problems-solved figure. That is an upstream README claim, not a result reproduced or adjudicated here; project benchmark status remains not_run.[[README](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/README.md)] [[project metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)]

## Benchmark status

Benchmark status is **not_run**. Project metric definitions, the synthetic fixture and execution-status record describe the separate evaluation protocol; they are not Cairn measurements. No Cairn system, benchmark, or tests were run.[[project metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Official repository](https://github.com/oritera/Cairn)
- [Reviewed commit 8e7e0ea67552383851dfcabfba0c4e9c8d007878](https://github.com/oritera/Cairn/commit/8e7e0ea67552383851dfcabfba0c4e9c8d007878)
- [README at reviewed commit](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/README.md)
- [Server models](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/models.py)
- [SQLite schema](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/db.py)
- [Project routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/projects.py)
- [Intent routes](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/intents.py)
- [Hint route](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/hints.py)
- [Validation and lease services](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/services.py)
- [YAML/timeline export](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/routers/export.py)
- [FastAPI app](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/server/app.py)
- [Explore worker](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/explore.py)
- [Reason worker](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/reason.py)
- [Worker snapshot and timing helpers](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/tasks/common.py)
- [Dispatcher configuration](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/config.py)
- [Dispatcher scheduler](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/cairn/src/cairn/dispatcher/scheduler/loop.py)
- [Server protocol spec](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/docs/specs/server-protocol.md)
- [Dispatcher design](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/docs/specs/dispatcher-design.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status record](../results/initial-baselines-status.json)
- [Project fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster / Atlas attribution](../data/memory-systems.json)

**Contact-list follow-up:** checked the official README and the repository's SECURITY.md and SUPPORT.md locations at the reviewed revision. No published contact email was found in those sources, so the JSON record stores `contact_email: null` with the checked source URLs.[[README](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/README.md)] [[SECURITY.md](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/SECURITY.md)] [[SUPPORT.md](https://github.com/oritera/Cairn/blob/8e7e0ea67552383851dfcabfba0c4e9c8d007878/SUPPORT.md)]
