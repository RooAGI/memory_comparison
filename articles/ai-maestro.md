# AI Maestro long-term memory — source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 38 / AI Maestro / ai-maestro  
**Listed repository locator:** [23blocks-OS/ai-maestro](https://github.com/23blocks-OS/ai-maestro)  
**Canonical repository:** [23blocks-OS/ai-maestro](https://github.com/23blocks-OS/ai-maestro)  
**Default branch / reviewed head:** `main` / `ead48472b0ff7d966c62eba6cd90a5c413951482`  
**Review time:** 2026-11-24 19:44:45 UTC (11:44:45 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists ordinal 38 as **AI Maestro**, slug `ai-maestro`, with repository locator https://github.com/23blocks-OS/ai-maestro. Its Atlas URL and revision are retained as roster attribution only; Atlas descriptions, marks, and layout were not assessment evidence.[[curated roster](../data/memory-systems.json)] [[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ai-maestro.md)]

The official repository page identifies `23blocks-OS/ai-maestro` and shows `main` as the default branch. The official main-branch feed reports current head `ead48472b0ff7d966c62eba6cd90a5c413951482` at 2026-11-24 17:46:05 UTC; this review uses that full SHA.[[repository and default branch](https://github.com/23blocks-OS/ai-maestro)] [[main commit feed](https://github.com/23blocks-OS/ai-maestro/commits/main.atom)] [[reviewed commit](https://github.com/23blocks-OS/ai-maestro/commit/ead48472b0ff7d966c62eba6cd90a5c413951482)]

## Summary

AI Maestro is a self-hosted agent orchestration platform with an optional per-agent long-term memory skill. The system indexes conversation messages, consolidates selected passages into memory cards and an entity graph, and injects relevant context into later prompts. This is a source review, not a review of a running deployment.[[README](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/README.md)] [[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)]

## Who and what

The README describes AI Maestro as a platform for managing AI agents across terminals and machines. Long-term memory is one optional skill attached to an agent profile, rather than a standalone memory-only library or hosted service.[[README](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/README.md)] [[memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)]

## Architecture and data model

The guide places each agent's CozoDB at `~/.aimaestro/agents/<id>/agent.db`. It stores the message index, memories, memory cards and vectors, evidence passages, entities, relations, and dated relation statements. The schema models memory tier, system/category, content/context, source conversation and message IDs, confidence, reinforcement/access counts, and timestamps; vectors are 384-dimensional with a cosine HNSW index.[[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)] [[memory schema](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/cozo-schema-memory.ts)]

The guide distinguishes episodic history (indexed messages), semantic memory (cards and the entity graph), and procedural memory (skills, not captured automatically). A card is a short statement backed by passages. Entity relations are directed typed edges; dated relation statements say when a relation was stated and whether it still holds. This is provenance at the memory/evidence level, not a general citation graph linking every generated answer to source passages.[[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)] [[cards and entity graph](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/cards.ts)] [[relation model](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/relations.ts)]

## Write, update, delete, and retrieval

**Write and consolidation — source observation.** The guide describes hourly and idle indexing, nightly consolidation, and a 2–8 AM history-backfill window. Consolidation redacts candidate passages, classifies and summarizes them, checks generated cards against evidence, reinforces duplicates, and links entities and relations. The implementation selects a configured Jev, Ollama, or Claude provider and uses embedding similarity plus classifier checks to find duplicates; new memories are stored in the agent database.[[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)] [[consolidation implementation](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/consolidate.ts)] [[card and evidence handling](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/cards.ts)]

**Update and correction.** Consolidation can reinforce repeated knowledge and the guide says user corrections receive a lower retention threshold and high recall priority. A separate API PATCH route accepts a memory ID and optional replacement content, category, or context. The inspected source does not establish that manual edits refresh every derived embedding or relation, and no correction accuracy was measured.[[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)] [[long-term memory API](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/app/api/agents/[id]/memory/long-term/route.ts)] [[agent memory service](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/services/agents-memory-service.ts)]

**Delete and forgetting.** A DELETE route removes one selected memory by ID. Separately, the documented lifecycle fades unused one-off memories: they remain stored but are not recalled, and can be revived if they recur. This review did not trace deletion across evidence, vector and relation records, raw indexed messages, backups, or host copies, so complete erasure is unknown.[[long-term memory API](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/app/api/agents/[id]/memory/long-term/route.ts)] [[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)] [[memory schema](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/cozo-schema-memory.ts)]

**Retrieval.** The search function embeds a query and performs per-agent semantic similarity retrieval, with optional category, confidence, and tier filters and optional related-memory expansion. The API also exposes paged results and special views. The guide describes injecting memories near the prompt, relevant relations for entities named in the prompt, recurring decisions at session start, and an on-demand skill that searches cards before raw history. These are retrieval mechanisms, not measured answer quality.[[memory search](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/search.ts)] [[long-term memory API](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/app/api/agents/[id]/memory/long-term/route.ts)] [[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)]

## Scope isolation

The guide states that memories belong to one agent and are stored in that agent's database. The inspected search path takes an agent ID and scopes memory retrieval to it. This documents a per-agent boundary in these paths; it does not establish operating-system isolation between agents under one user, or authorization guarantees for all callers and deployment modes.[[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)] [[memory search](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/search.ts)] [[agent memory service](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/services/agents-memory-service.ts)]

## Provenance and evidence

The card pipeline retains source passages and checks a generated statement against its evidence; the guide describes memory evidence as passages associated with a memory and a session. Relations retain statement time and whether the relation continues to hold. This supports traceability within memory creation, but the inspected system does not establish that every answer carries validated claim-level citations.[[cards and entity graph](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/cards.ts)] [[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)] [[relation model](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/relations.ts)]

## Source-visible efficiency and observability

**Code observations.** Semantic search uses vector embeddings and an HNSW index. Consolidation searches a bounded set of similar memories before a classifier decides whether to reinforce; the schema and service expose consolidation-run counts/status, memory statistics, and recall logging. The guide documents a per-run budget of about 1,000 passages and 10 summarizer calls, resumable progress, and nightly backfill. These structures and documented budgets do not establish measured latency, reliability, throughput, or cost.[[memory search](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/search.ts)] [[consolidation implementation](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/consolidate.ts)] [[memory schema](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/cozo-schema-memory.ts)] [[memory service](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/services/agents-memory-service.ts)] [[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)]

## Metric-domain evidence

All outcome metrics are **unmeasured** in this review:

- **Answerable recall and abstention:** semantic retrieval and prompt injection are implemented; no answerability or abstention cases were evaluated.
- **Correction accuracy and stale values:** correction classification, reinforcement, and manual update paths are visible; no correction probes were run.
- **Deletion leakage:** per-memory deletion and fading are documented; no post-delete probes or full erasure audit were performed.
- **Scope isolation:** per-agent database paths and query scoping are source-visible; no cross-agent isolation workload was run.
- **Evidence support and citation coverage:** cards are checked against passages; no answer support or citation coverage was adjudicated.
- **Latency and write-to-recall delay:** no timing data was collected.
- **Tokens, cost, and storage:** provider options and documented run budgets exist; no spend, token, or corpus-size measurement was collected.

The project's [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) define or track the evaluation protocol; they are not AI Maestro results.[[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This bounded inspection covered the README and memory guide, plus memory schema, consolidation, cards/entities, relations, search, the agent memory service, and long-term API route at the verified head. It did not inspect every caller, adapter, migration, backup, authorization path, or deletion dependency.

The guide states that raw message-index content is not redacted even though secrets are removed before memories are stored. Procedural knowledge is not captured automatically, and relations depend on what conversations mention. Its capacity and cost descriptions are documentation claims, not results measured here. The official SECURITY.md publishes `support@23blocks.com`; this is a security-reporting contact, not a claim about general support response beyond that policy.[[long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)] [[official security policy](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/SECURITY.md)]

No source inspection establishes answer accuracy, abstention, correction freshness, deletion completeness, cross-agent security, latency, token spend, or storage efficiency. No system, benchmark workload, or test suite was run.

## Benchmark status

**Benchmark not run.** No AI Maestro execution, benchmark workload, or tests were run. Project metrics, fixtures, and execution-status records are protocol artifacts only, not AI Maestro results.[[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Contact-list follow-up

The official repository README and SECURITY.md were checked. SECURITY.md publishes `support@23blocks.com`; the review record stores the email with the exact checked source URL.[[official README contact check](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/README.md)] [[official security contact](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/SECURITY.md)]

## Sources

- [Official repository and default branch](https://github.com/23blocks-OS/ai-maestro)
- [Official main branch commit feed](https://github.com/23blocks-OS/ai-maestro/commits/main.atom)
- [Reviewed full commit](https://github.com/23blocks-OS/ai-maestro/commit/ead48472b0ff7d966c62eba6cd90a5c413951482)
- [README at reviewed revision](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/README.md)
- [Long-term memory guide](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/docs/LONG-TERM-MEMORY.md)
- [Memory schema](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/cozo-schema-memory.ts)
- [Consolidation implementation](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/consolidate.ts)
- [Card and entity implementation](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/cards.ts)
- [Relation implementation](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/relations.ts)
- [Search implementation](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/lib/memory/search.ts)
- [Agent memory service](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/services/agents-memory-service.ts)
- [Long-term memory API route](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/app/api/agents/[id]/memory/long-term/route.ts)
- [Official security policy and contact](https://github.com/23blocks-OS/ai-maestro/blob/ead48472b0ff7d966c62eba6cd90a5c413951482/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Curated roster identity and Atlas attribution](../data/memory-systems.json)

**Verification boundary:** source claims above are tied to the reviewed SHA; no AI Maestro runtime, benchmark, or tests were run.
