# Agno memory subsystem — source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 33 / Agno / agno  
**Listed repository locator:** [agno-agi/agno](https://github.com/agno-agi/agno)  
**Current canonical repository:** [agno-agi/agno](https://github.com/agno-agi/agno)  
**Default branch / reviewed head:** main / `bd24f44997b3cc86b3cfa9f6608bacc0353c601f`  
**Review time:** 2026-11-24 19:30:38 UTC (11:30:38 PST; America/Los_Angeles).

## Identity and scope

The curated catalog places **Agno** at ordinal 33, slug `agno`, with listed repository locator `https://github.com/agno-agi/agno`. The catalog's Agent Memory Atlas entry is recorded only for identity and source attribution; its descriptions, marks, and layout were not used as assessment evidence.[[curated roster](../data/memory-systems.json)] [[Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agno.md)]

The official repository page identifies `agno-agi/agno` and shows `main` as the default branch. The official main-branch feed identifies `bd24f44997b3cc86b3cfa9f6608bacc0353c601f` as its current head, which pins this review.[[repository and default branch](https://github.com/agno-agi/agno)] [[main commit feed](https://github.com/agno-agi/agno/commits/main.atom)] [[reviewed commit](https://github.com/agno-agi/agno/commit/bd24f44997b3cc86b3cfa9f6608bacc0353c601f)]

The README describes Agno as a self-managing agent platform. This review covers selected learning and memory source code; it does not assess a running deployment.[[README at reviewed revision](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/README.md)]

## Who and what

Agno combines agent, team, and workflow orchestration with AgentOS. Its learning package is a platform subsystem with separate configurations and stores for structured user profiles, unstructured user memories, session context, learned knowledge, entity memory, and decision logs.[[README](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/README.md)] [[learning configuration](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/config.py)]

## Architecture and data model

The learning configuration defines ALWAYS extraction after responses and AGENTIC writes through agent tools, alongside PROPOSE and HITL modes. The code documents PROPOSE as limited to learned knowledge and HITL as reserved; support varies by store. Configuration accepts database and model dependencies, and the module uses dataclasses for these options.[[learning configuration](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/config.py)] [[learning machine](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/machine.py)]

The types separate structured profile fields from free-form user observations. Entity memory models things other than the user, with names and types, properties, facts, events, and relationships. Its agent-facing operations are `remember_about`, `link_entities`, `search_entities`, and `forget`; entity memory is AGENTIC-only.[[user memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_memory.py)] [[user profile store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_profile.py)] [[entity memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/entity_memory.py)] [[learning schemas](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/schemas.py)]

## Write, update, delete, and retrieval

**Write.** In ALWAYS mode, `UserMemoryStore.process` extracts observations from conversation messages using its configured model. In AGENTIC mode, the agent can use memory tools to add or update observations. Profile extraction updates structured fields. Entity memories are entered through tools rather than an automatic extraction pass.[[learning configuration](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/config.py)] [[user memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_memory.py)] [[user profile store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_profile.py)] [[entity memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/entity_memory.py)]

**Update and correction.** User memory exposes add/update/delete operations, and profile updates act on fields. Entity memory upserts entities; it can retire a fact with supersession metadata or archive an entity through `forget`. These operations do not demonstrate correction accuracy or a complete mutation audit history.[[user memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_memory.py)] [[user profile store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_profile.py)] [[entity memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/entity_memory.py)]

**Delete.** User memory supports deleting selected memories or clearing a user's memories. Entity `forget` retires facts or archives entities; archival is not evidence of physical erasure. This review did not trace deletion across every backend, replica, or backup.[[user memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_memory.py)] [[entity memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/entity_memory.py)]

**Retrieval.** User-memory recall requires a user ID and retrieves that user's memory object. Entity search supports query-based lookup and recency listing, and entity context can expose live facts and events. Source inspection describes available retrieval paths, not their measured quality or end-to-end behavior across every backend.[[user memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_memory.py)] [[entity memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/entity_memory.py)]

## Scope isolation

User memories are retrieved by `user_id`. The store documentation says agents using the same database see the same memories for that user; `agent_id` and `team_id` are stored for audit purposes and do not add retrieval boundaries. Entity memory offers a private user namespace, a shared global namespace (the documented default), and custom group namespaces. These are source-visible scope rules, not results of cross-scope probes.[[user memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_memory.py)] [[entity memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/entity_memory.py)] [[learning configuration](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/config.py)]

## Provenance and evidence

Entity facts and events have record identity and temporal/supersession information, and an entity can carry a note pointer. User memories have record IDs and content. The inspected records do not establish source-document passages, claim-level citations, or an evidence adjudication flow for agent answers.[[entity memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/entity_memory.py)] [[learning schemas](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/schemas.py)] [[user memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_memory.py)]

## Source-visible efficiency and observability

The configuration module uses dataclasses and allows the application to choose model and database dependencies. ALWAYS-mode extraction can call a model, while recall is backed by the configured store. These are implementation observations; they do not establish latency, token cost, storage efficiency, or quality measurements.[[learning configuration](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/config.py)] [[user memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_memory.py)] [[entity memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/entity_memory.py)]

## Metric-domain evidence

All outcome metrics below are **unmeasured** for this review:

- **Answerable recall and abstention:** store and entity-search APIs are visible; no answerability or abstention probes were run.
- **Correction and stale values:** update and entity supersession paths are visible; no correction cases were run.
- **Deletion leakage:** delete, clear, and archive operations are visible; no post-deletion probes were run.
- **Scope isolation:** user ID selection and entity namespaces are visible; no forbidden cross-scope probes were run.
- **Evidence support and citation coverage:** no claim-level evidence was adjudicated.
- **Latency and write-to-recall delay:** no end-to-end timing probes were collected.
- **Tokens, cost, and storage:** no provider usage, cost, or storage measurements were collected.

Project definitions, fixture, and current execution status are references for the evaluation protocol only: [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json). They are not Agno results.[[project metrics](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark status](../results/initial-baselines-status.json)]

## Limits and unknowns

This bounded review inspected the README and selected learning configuration, user-memory, and entity-memory code at the verified head. It did not trace all agent integrations, database adapters and migrations, learned-knowledge behavior, or every retrieval path. The current scope behavior cannot establish effective authorization without examining and exercising each caller and backend.

The source does not establish extraction correctness, retrieval quality, correction freshness, deletion completeness, evidence support, performance, token usage, cost, or storage efficiency. No Agno runtime, benchmark workload, or tests were run.

The official pinned README was checked for a published contact email; none was found. The review record stores `contact_email: null` and the exact checked README URL.[[official README contact check](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/README.md)]

## Benchmark status

**Benchmark not run.** No Agno runtime, benchmark workload, or test suite was executed. The project metrics, fixture, and execution status document the protocol and status only; they are not Agno benchmark results.

## Sources

- [Official repository and default branch](https://github.com/agno-agi/agno)
- [Official main branch commit feed](https://github.com/agno-agi/agno/commits/main.atom)
- [Reviewed commit](https://github.com/agno-agi/agno/commit/bd24f44997b3cc86b3cfa9f6608bacc0353c601f)
- [README at reviewed revision](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/README.md)
- [Learning configuration](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/config.py)
- [Learning machine](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/machine.py)
- [User memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_memory.py)
- [User profile store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/user_profile.py)
- [Session context store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/session_context.py)
- [Entity memory store](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/stores/entity_memory.py)
- [Learning schemas](https://github.com/agno-agi/agno/blob/bd24f44997b3cc86b3cfa9f6608bacc0353c601f/libs/agno/agno/learn/schemas.py)
- [Project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json)
- [Curated roster identity and attribution only](../data/memory-systems.json)
