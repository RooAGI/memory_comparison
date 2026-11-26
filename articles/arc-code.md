# arc-code source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 63 / arc-code / `arc-code`  
**Listed repository locator:** [jerber/arc-code](https://github.com/jerber/arc-code)  
**Current canonical repository:** [jerber/arc-code](https://github.com/jerber/arc-code)  
**Default branch / reviewed head:** main / `6b33c1f7c2ad45997663c69157f5559d1be61bd9`  
**Review time:** 2026-11-24T21:09:58Z (UTC (2026-11-24 13:09:58 PST; America/Los_Angeles)).

## Identity and review pin

The curated roster identifies ordinal 63 as arc-code and lists `https://github.com/jerber/arc-code`; its pinned Atlas source is recorded only as attribution. Atlas prose, capability marks, descriptions and layout were not assessment evidence. The official GitHub repository page shows `main` as the default branch. A fresh `git ls-remote --symref` reported `refs/heads/main` at `6b33c1f7c2ad45997663c69157f5559d1be61bd9`, and a shallow clone of `main` resolved to that same full SHA. [[curated roster](../data/memory-systems.json)] [[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/arc-code.md)] [[repository](<https://github.com/jerber/arc-code>)] [[reviewed commit](<https://github.com/jerber/arc-code/commit/6b33c1f7c2ad45997663c69157f5559d1be61bd9>)] [[README](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/README.md)]

## Summary

arc-code is a coding-agent harness for ARC-AGI-3. The agent's primary game history is a text log written by the actuator; agents inspect it with shell tools and keep longer-lived findings and helper programs as ordinary workspace files. A broker, per-game sandbox, audit and optional Postgres recorder support runs. This review describes source and documentation, not execution results. [[README](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/README.md)] [[prompt](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/PROMPT.md)] [[actuator](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/act.py)]

## Who and what

The GitHub repository page lists one contributor as jerber (Jeremy Berman), but does not explicitly describe an owner or maintainer role. The project is a Python harness around coding-agent CLIs and a game actuator; it is not presented as a standalone memory database or retrieval service. [[repository](<https://github.com/jerber/arc-code>)] [[README](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/README.md)]

## Architecture and data model

`logs.txt` is the actuator-written run history: one block per action with the plan, action, score/level context and resulting board. `state.json` holds current game/run state such as the action budget and count, score, level, attempt, session identifiers, history and last board. The prompt treats the log as the complete record and directs the agent to inspect selected portions programmatically; notes and helper scripts are agent-authored files. [[actuator](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/act.py)] [[prompt](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/PROMPT.md)]

The brief describes a 64×64 colored-cell board and game-specific actions. `run.py` creates an independent workspace for each game and launches one agent session per game. In broker mode it places a forwarding client in the workspace; the broker holds the game key and runs the actuator. [[ARC brief](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/ARC.md)] [[session runner](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/run.py)] [[broker](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/broker.py)]

The supporting rig includes provider adapters, E2B sandbox configuration, scoring, auditing and export. The optional Postgres schema stores run and game metadata, parsed action rows, and named workspace artifacts; artifacts are gzip-compressed for transfer/storage. These tables support run records, not a general-purpose memory query service. [[README](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/README.md)] [[agent adapters](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/agents.py)] [[sandbox/fence](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/cloud.py)] [[database](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/db.py)]

## Write, update, delete, and retrieval

**Write.** The actuator appends each action and resulting board to `logs.txt` and rewrites `state.json` after the step. The prompt asks the agent to test a hypothesis in one or two actions, then batch roughly 10–20 actions once its model is stable. A batch stops when score changes or the game reaches a terminal state; remaining actions are dropped. [[actuator](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/act.py)] [[prompt](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/PROMPT.md)]

**Update.** The agent can freely edit its notes and scripts. In the optional recorder, run/game state is updated, action rows are inserted, and artifacts are replaced when their file size differs from the saved size. The source describes size as a cheap, coarse change detector, so a same-size rewrite is not observed by that mirroring path. I found no agent-facing versioned memory edit API. [[database](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/db.py)] [[runner](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/run.py)]

**Delete.** I found no general memory-delete operation in the agent interface. Game reset/restart is separate from erasing stored run evidence. Database foreign keys cascade action and artifact rows with their parent game/run, but the reviewed interface does not expose a record-erasure workflow, and this inspection does not establish deletion from backups or other retained copies. [[actuator](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/act.py)] [[database](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/db.py)] [[README](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/README.md)]

**Retrieval.** The agent retrieves by reading its files with shell tools. The prompt specifically recommends grep, sed and Python to select and compare log states, and directs a resumed agent to recover from notes and logs. The inspected interface has no semantic index, ranked search API, or explicit abstention policy. No retrieval query was executed in this review. [[prompt](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/PROMPT.md)] [[runner](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/run.py)] [[actuator](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/act.py)]

## Scope isolation, provenance, and evidence

The runner provisions one workspace and E2B sandbox per game. Database records are keyed by run and game. This is source-visible execution scoping; the inspected code does not establish a user/tenant authorization model or a tested cross-scope isolation guarantee. In broker mode the key remains at the broker, and the sandbox egress policy denies traffic except configured hosts. [[runner](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/run.py)] [[database](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/db.py)] [[sandbox/fence](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/cloud.py)] [[broker](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/broker.py)]

The actuator log links a proposed plan and each game action to the board returned by the game. Agent adapters retain an event stream of tool activity and usage; the audit grades that stream and stores findings. The schema allows a later stricter re-audit alongside the original verdict. These records support traceability of actions and process behavior; they do not themselves establish that an answer is correct or cite evidence for an answer-level claim. [[actuator](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/act.py)] [[agent adapters](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/agents.py)] [[audit](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/audit.py)] [[database](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/db.py)]

## Source-visible efficiency and observability

The prompt recommends batching actions after mechanics are understood to reduce interaction overhead, while ending batches on score changes to avoid acting on an outdated board. The recorder mirrors a workspace every 60 seconds and after a game ends; it pushes parsed action slices, current state and changed artifacts, compressing artifact bodies. Session records include elapsed seconds, tool counts, tokens and cost fields. These are source-visible design and recording fields, not measured efficiency results from this review. [[prompt](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/PROMPT.md)] [[actuator](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/act.py)] [[database](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/db.py)] [[agent adapters](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/agents.py)]

## Metric-domain evidence

All project comparison domains are **not measured** here. The code offers run-level token/cost/time fields and workspace artifact byte counts, but no controlled recall, abstention, correction, deletion, scope, citation, latency, write-to-recall or storage-efficiency results were collected. See the project definitions, status record and fixture for the separate protocol. [[metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[database](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/db.py)]

## Limits and unknowns

This review inspected selected current README, prompt, interface, orchestration, broker, database, audit, scoring and sandbox code. It did not execute the harness or independently verify figures reported in its README. The repository describes an ARC-specific evaluation; portability to other tasks remains unestablished by this inspection. Whether the run store supports complete erasure, how same-size artifact changes are handled outside the observed size check, and what authorization protects records in a deployment were not established. [[README](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/README.md)] [[reproduction guide](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/docs/REPRODUCE.md)] [[database](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/db.py)] [[sandbox/fence](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/cloud.py)]

## Contact-list follow-up

The official pinned README and repository page publish no contact email. The repository has no SECURITY.md at the reviewed revision (the expected pinned path returned GitHub’s “File not found” page); the JSON records a null email and the exact official URLs checked. I did not use commit metadata, profile emails, third-party directories or inferred addresses. [[README](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/README.md)] [[checked SECURITY.md path](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/SECURITY.md)] [[repository](<https://github.com/jerber/arc-code>)]

## Benchmark status

**Benchmark not run.** I did not execute arc-code, its benchmarks, or its tests. Source observations above are distinct from measured results. The project metric definitions, execution-status record and fixture describe the separate evaluation protocol. [[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[reproduction guide](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/docs/REPRODUCE.md)]

## Sources

- [Current canonical repository](https://github.com/jerber/arc-code)
- [Current main branch head](<https://github.com/jerber/arc-code/commit/6b33c1f7c2ad45997663c69157f5559d1be61bd9>)
- [README.md](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/README.md>)
- [PROMPT.md](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/PROMPT.md>)
- [ARC.md](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/ARC.md>)
- [act.py](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/act.py>)
- [run.py](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/run.py>)
- [rig/agents.py](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/agents.py>)
- [rig/broker.py](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/broker.py>)
- [rig/db.py](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/db.py>)
- [rig/audit.py](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/audit.py>)
- [rig/cloud.py](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/cloud.py>)
- [rig/score.py](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/rig/score.py>)
- [docs/REPRODUCE.md](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/docs/REPRODUCE.md>)
- [Checked official SECURITY.md path](<https://github.com/jerber/arc-code/blob/6b33c1f7c2ad45997663c69157f5559d1be61bd9/SECURITY.md>)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster identity and attribution](../data/memory-systems.json)
