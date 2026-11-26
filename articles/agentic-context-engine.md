# Agentic Context Engine source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 17 / Agentic Context Engine / agentic-context-engine  
**Listed repository locator:** [kayba-ai/agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine)  
**Catalog source attribution:** [Agent Memory Atlas report at catalog revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agentic-context-engine.md)  
**Current canonical repository:** [kayba-ai/agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine)  
**Default branch / reviewed head:** main / [3a319831785ede6ba4a3a4002756233095c59e17](https://github.com/kayba-ai/agentic-context-engine/commit/3a319831785ede6ba4a3a4002756233095c59e17)  
**Review time:** 2026-11-24 18:45:47 UTC (10:45:47 PST; America/Los_Angeles). GitHub's repository page identifies `main`; its main-branch Atom feed resolves the current head to the full SHA above.  
**Published contact:** No email was found in the checked official [repository README at the reviewed revision](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/README.md); the JSON record stores null with that exact checked URL.

## Identity and scope

The curated roster places **Agentic Context Engine** at ordinal 17, slug `agentic-context-engine`, and lists `https://github.com/kayba-ai/agentic-context-engine`. The roster attributes this entry to the Atlas report at revision `19199a4fc249e89c0793be06f0b166b358089ba0`. This information establishes the selected identity and locator only; Atlas descriptions, marks, report prose, and layout were not used as assessment evidence.[[roster entry](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agentic-context-engine.md)]

GitHub identifies the canonical repository as `kayba-ai/agentic-context-engine` and the default branch as `main`. The main-branch Atom feed gives head `3a319831785ede6ba4a3a4002756233095c59e17`; the commit page confirms the release merge commit. The code and documentation links below are pinned to that full revision.[[repository](https://github.com/kayba-ai/agentic-context-engine)] [[main branch history](https://github.com/kayba-ai/agentic-context-engine/commits/main.atom)] [[full head](https://github.com/kayba-ai/agentic-context-engine/commit/3a319831785ede6ba4a3a4002756233095c59e17)]

ACE is an agent learning framework, rather than a general-purpose personal memory database. Its Skillbook stores readable strategies learned from task feedback. The documented learning loop uses an Agent, Reflector, and SkillManager; a full ACE pipeline can evaluate and update its own runs, while integrations can inject Skillbook context into an external agent and learn from its results.[[README](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/README.md)] [[overview](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/overview.md)]

## Architecture and data model

**Code and documentation observations.** A Skillbook is a collection of structured `Skill` records. The documented fields include an ID, one of two sections (`context` or `harness`), keywords, issue, optional insight, active state, effectiveness counters, and provenance occurrences. The source model also stores usage counters and created/updated timestamps. The framework groups skills by section and renders their text, keywords, issue, and insight as prompt context.[[Skillbook guide](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/skillbook.md)] [[Skill and Skillbook source](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/core/skillbook.py)]

The guide documents JSON persistence via `save_to_file` and `load_from_file`, alongside an embeddings sidecar file. It also documents Skillbook statistics and optional embedding-similarity deduplication. The README says the core approach does not require a vector database. These describe storage and features, not measured storage use or retrieval quality.[[Skillbook guide](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/skillbook.md)] [[README](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/README.md)]

## Write, update, delete, and retrieval

**Write and update — source observation.** The documented operations are ADD, UPDATE, TAG, and REMOVE. ADD creates a skill; UPDATE refines its issue, insight, or keywords; TAG adjusts helpful, harmful, or neutral counters; REMOVE soft-removes a skill by making it inactive. Current SkillManager code exposes tools for search/read and add/update/remove/tag. Those tools mutate the supplied Skillbook directly, and the returned operation list is an audit log of actions already applied. This is not a database transaction or an append-only mutation history.[[update operations](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/updates.md)] [[SkillManager](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/implementations/skill_manager.py)] [[Skillbook source](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/core/skillbook.py)]

**Delete.** REMOVE is a soft removal from active Skillbook views; it does not establish physical erasure from a saved JSON file, prior copies, traces, or an embeddings sidecar. The reviewed docs and source do not describe a general hard-delete or retention-erasure workflow.[[update operations](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/updates.md)] [[Skillbook source](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/core/skillbook.py)]

**Retrieval.** The agent receives Skillbook content rendered as prompt text. The SkillManager has read-only search and read tools for inspecting skills before it mutates them. The reviewed paths do not document a separate, general user-query memory retrieval service that ranks skills and returns factual evidence; optional similarity-based deduplication is documented for consolidation, not as a measured recall method.[[Skillbook guide](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/skillbook.md)] [[SkillManager](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/implementations/skill_manager.py)] [[overview](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/overview.md)]

## Scope isolation and provenance

**Scope isolation — source observation.** The reviewed Skill record and documented Skillbook schema contain no tenant, user, or project scope field, and the core Skillbook API has no authorization boundary. Scope therefore depends on which Skillbook instance or file an integration supplies. The inspected materials do not establish isolation between users, agents, or projects when a Skillbook is shared; no isolation probes were run.[[Skillbook guide](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/skillbook.md)] [[Skillbook source](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/core/skillbook.py)]

**Provenance and evidence.** Skills may retain structured occurrences that link learned strategies to trace identity and learning context. The guide lists `trace_uid`, source system, trace ID, display name, epoch/step, learning text, and optional in-trace references such as JSON paths, step/message indices, and span IDs. The source supports deduplicating these records, exporting a source map, aggregating provenance counts, and filtering occurrences by source/trace/epoch/question. These links help audit where a strategy came from; they do not prove that a generated answer is factually supported by a cited passage.[[Skillbook guide](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/skillbook.md)] [[Skillbook source](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/core/skillbook.py)]

## Source-visible efficiency and observability

**Code observations, not measurements.** The Skillbook is an in-process collection with explicit file save/load; the documented embeddings sidecar and optional deduplicator add separate work and storage. Its stats and provenance summaries expose counts. The SkillManager output includes run metadata and a trace summary with iteration and compaction counts, and its code logs budget exhaustion or failures. The repository README describes model/provider caching and supported integrations. These are implementation and observability signals; no latency, throughput, token, cost, or storage-efficiency result was measured for this review.[[Skillbook guide](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/skillbook.md)] [[Skillbook source](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/core/skillbook.py)] [[SkillManager](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/implementations/skill_manager.py)] [[README](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/README.md)]

## Project metric domains

Every benchmark metric domain remains **unmeasured** for Agentic Context Engine. The source observations above describe implementation. The project metric definitions are protocol; the shared execution record remains `not_run` and contains no Agentic Context Engine measurements. The fixture is a planned workload, not evidence of system performance.[[metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded read-only review of the official README and selected Skillbook/learning-loop documentation and code at the verified SHA. I did not execute the system, benchmarks, or tests.

The reviewed Skillbook surface establishes strategy storage and mutation behavior, not what strategies are selected or how reliably an external agent follows them in a given deployment. The integrations and caller determine which Skillbook is used and how it is persisted. The reviewed core model does not establish tenant or user authorization, full erasure, runtime isolation, or production service behavior. I did not trace every runner, integration, serialization edge case, or optional deduplication configuration.

## Benchmark status

**Benchmark not run.** No Agentic Context Engine system, benchmark workload, or test suite was executed. No metric values were produced. The project metric definitions, fixture, and shared status record are references for the evaluation protocol only.[[metrics](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current repository](https://github.com/kayba-ai/agentic-context-engine)
- [Main branch Atom history](https://github.com/kayba-ai/agentic-context-engine/commits/main.atom)
- [Full-SHA head commit](https://github.com/kayba-ai/agentic-context-engine/commit/3a319831785ede6ba4a3a4002756233095c59e17)
- [README.md](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/README.md)
- [Concept overview](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/overview.md)
- [Skillbook guide](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/skillbook.md)
- [Update operations](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/docs/concepts/updates.md)
- [Skillbook data model and methods](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/core/skillbook.py)
- [SkillManager tools and execution](https://github.com/kayba-ai/agentic-context-engine/blob/3a319831785ede6ba4a3a4002756233095c59e17/ace/implementations/skill_manager.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster and catalog attribution](../data/memory-systems.json)

**Verification boundary:** no system, tests, or benchmarks were run.
