# AutoBot

## Identity and review pin

- **System:** AutoBot
- **Curated position:** 81
- **Slug:** `autobot-ai`
- **Listed repository:** [mrveiss/AutoBot-AI](https://github.com/mrveiss/AutoBot-AI)
- **Canonical repository at review:** [mrveiss/AutoBot-AI](https://github.com/mrveiss/AutoBot-AI)
- **Default branch:** `main`
- **Reviewed head:** [`cb66dab5f250803c98b334ea318e27a8e119ec48`](https://github.com/mrveiss/AutoBot-AI/commit/cb66dab5f250803c98b334ea318e27a8e119ec48)
- **Reviewed:** 2026-11-24 23:03:34 UTC (15:03:34 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/autobot-ai.md), used only for identity, listed locator, and source attribution.

The curated roster identifies AutoBot at position 81 with slug `autobot-ai` and the listed locator above. The official GitHub repository resolves to `mrveiss/AutoBot-AI`; its default branch is `main`. A fresh read-only `git ls-remote --symref` and shallow checkout agreed on full head `cb66dab5f250803c98b334ea318e27a8e119ec48`. Atlas descriptions, marks, and layout were not used as assessment evidence.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/mrveiss/AutoBot-AI)] [[main commit feed](https://github.com/mrveiss/AutoBot-AI/commits/main.atom)] [[reviewed head](https://github.com/mrveiss/AutoBot-AI/commit/cb66dab5f250803c98b334ea318e27a8e119ec48)]

## Summary

AutoBot is a self-hosted AI platform whose memory is split across a general SQLite store, a knowledge-fact pipeline with durable PostgreSQL rows and Redis/vector projections, a Redis-backed memory graph, and conversation-derived stores for verbatim turns and scored trajectories. This is a source review at one pinned revision; it does not establish retrieval quality, runtime isolation, or measured cost.

## Who and what

The public repository is under the GitHub account `mrveiss`. Its README describes AutoBot as an Apache-2.0, self-hosted platform with chat, a retrieval-augmented knowledge base, a knowledge graph, a provider-agnostic model gateway, and installable modules. It is a platform and service stack, not a standalone memory library. The README points users to GitHub Issues and Discussions for community support; `FUNDING.md` says its production-support contact path is pending.[[README](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/README.md)] [[FUNDING](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/FUNDING.md)]

## Architecture and data model

**Source observations.** AutoBot implements several memory lanes rather than one common record type. The general memory manager stores category, content, metadata, timestamp, reference path, embedding, and required `user_id` in SQLite. Task execution history is another SQLite-oriented record with task status, timing, agent attribution, inputs, outputs, errors, and parent/child identifiers.[[general storage](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/storage/general_storage.py)] [[memory models](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/models.py)] [[task storage](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/storage/task_storage.py)]

Knowledge facts use a separate write pipeline. `FactsMixin` prepares metadata and writes the fact through `knowledge.fact_store` before projecting it to Redis and ChromaDB. The projection code describes the PostgreSQL `knowledge_facts` row as authoritative, with Redis hashes and vector entries derived from it; vectorization failures are recorded and queued for reconciliation. This design distinguishes durable fact content from rebuildable search projections.[[facts](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/facts.py)] [[fact projection](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/fact_projection.py)]

Other lanes include a Redis/RediSearch memory graph with entities and relations, ChromaDB-backed conversation trajectories, ChromaDB verbatim turn chunks, and Redis working memory. Chat turn completion enqueues verbatim writes and fact extraction to Celery; trajectory capture is also attempted after the durable-write tasks are enqueued. These paths have different schemas, APIs, and scope rules.[[graph owner scope](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/autobot_memory_graph/owner_scope.py)] [[trajectory store](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/trajectory_store.py)] [[verbatim store](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/verbatim_store.py)] [[turn completion hook](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/chat_workflow/stop_hook.py)]

## Write, update, delete, and retrieval

**Write and update.** General-memory writes reject blank owners and the reserved legacy owner; reads include a required owner predicate. Fact writes sanitize content and caller metadata, add identifiers, timestamps, embedding model, provenance defaults and a content fingerprint, then persist the row and update Redis and vector projections. Updates merge sanitized metadata and content changes, update the durable row first, and refresh affected projections. Chat completion enqueues user and assistant turn chunks and combined-turn fact extraction without waiting for background processing.[[general storage](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/storage/general_storage.py)] [[facts](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/facts.py)] [[fact projection](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/fact_projection.py)] [[turn completion hook](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/chat_workflow/stop_hook.py)]

**Delete.** The fact delete path removes the durable fact row and then cleans Redis mappings and the Chroma vector; vector deletion errors are logged. General memory has owner-scoped deletion. A separate privacy “forget everywhere” operation enumerates six stores—verbatim, trajectory, working memory, graph, retrieval learner, and general memory—but does not enumerate the knowledge-fact store. It therefore is not evidence of complete deletion across every AutoBot memory subsystem.[[facts](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/facts.py)] [[general storage](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/storage/general_storage.py)] [[memory transparency](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/transparency.py)]

**Retrieval.** General memory supports owner/category retrieval and search. Knowledge search includes vector, lexical/BM25, hybrid, and related graph-oriented components, with result filtering through knowledge ownership and principal rules on permission-aware paths. The Essential Story builder fetches at most 200 facts, requires a knowledge principal, filters by that principal, scores by quality with optional bounded access/recency reinforcement, then formats within a model-specific token budget. Trajectory recall asks Chroma for up to four times the requested count (at least 20), then filters by minimum reward and any supplied tenant and user scopes. Verbatim search is a separate semantic lane with optional symbolic candidate lookup and recency reranking.[[knowledge search](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/search.py)] [[search filters](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/search_filters.py)] [[essential story](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/essential_story.py)] [[trajectory store](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/trajectory_store.py)] [[verbatim store](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/verbatim_store.py)]

## Scope isolation

Scope is enforced differently by lane. The general SQLite API requires an owner on reads and writes, and the memory-graph API requires an `OwnerScope`; cross-owner graph reads must pass the explicit `UNSCOPED_ALL_USERS` sentinel. Trajectory retrieval applies tenant and user filters only when those identifiers are supplied, and the chat call derives them from session metadata, so empty/missing scope values deserve deployment-specific attention. Knowledge access uses ownership, visibility, organization, group, or sharing rules on permission-aware reads; the Essential Story path requires a principal and filters its candidate facts. These code paths do not establish that every integration and retrieval route has been tested for cross-scope leakage.[[general storage](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/storage/general_storage.py)] [[graph owner scope](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/autobot_memory_graph/owner_scope.py)] [[trajectory store](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/trajectory_store.py)] [[chat handler](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/chat_workflow/llm_handler.py)] [[search filters](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/search_filters.py)] [[essential story](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/essential_story.py)]

## Provenance and evidence

Knowledge facts carry fields such as source type, connector ID, verification status and method, verifier and time, quality score, provenance chain, timestamps, owner/visibility metadata, and content fingerprint. The code includes research quarantine and promotion/verification paths, but correctness depends on which reader is used and how its filters are applied. Verbatim chunks retain turn/session, role, user, and timestamp metadata. Trajectories retain task text, action sequence, outcome, reward, duration, agent/plan/strategy identifiers, and timestamp. A fact's provenance fields and a trajectory's reward are recorded metadata, not independent proof that a claim is true or a trajectory is safe to reuse.[[facts](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/facts.py)] [[quarantine](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/quarantine.py)] [[verbatim store](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/verbatim_store.py)] [[trajectory store](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/trajectory_store.py)]

## Source-visible efficiency and observability

**Code observations, not measurements.** Fact retrieval bounds the Essential Story scan to 200 records and its rendered context to a configured token budget; trajectory search oversamples candidates to offset reward filtering. Fact vectorization has a buffering/reconciliation path and records failed attempts; the code also exposes embedding counters and fact usage/access fields. Trajectory query time is logged, general memory has indexed owner/category lookups, and the platform has memory monitoring/statistics. These mechanisms show what can be observed or bounded in source, not actual latency, recall, storage, or cost.[[essential story](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/essential_story.py)] [[trajectory store](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/trajectory_store.py)] [[facts](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/facts.py)] [[general storage](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/storage/general_storage.py)] [[memory monitor](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/monitor.py)]

## Metric-domain evidence

All domains below are **unmeasured for this review**. The source links show implementation surfaces and evidence gaps, not outcome estimates.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Multiple retrieval lanes and a bounded essential-fact context are present; no answerability or abstention workload was run. | Unmeasured |
| Correction accuracy and staleness | Fact update, verification, and quarantine code are present; no correction or stale-value probes were run. | Unmeasured |
| Deletion leakage | Fact row deletion and a six-store privacy path are visible; that path omits knowledge facts, and no residual-copy probing was performed. | Unmeasured |
| Scope isolation | Owner and principal predicates exist in several paths; no cross-user, tenant, or integration isolation probes were performed. | Unmeasured |
| Evidence support and citation coverage | Facts carry provenance fields and chat can return citations; no claim-level support adjudication was run. | Unmeasured |
| Latency and write-to-recall delay | Trajectory query timing and background task paths are visible; no timing workload was collected. | Unmeasured |
| Tokens, cost, and storage | Essential-context budgets, vectorization counters, and store statistics are source-visible; no memory-attributed usage, cost, or storage measurement was made. | Unmeasured |

The [project metric definitions](../METRICS.md), [versioned benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) describe planned workloads and reporting, not AutoBot results.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded inspection of selected documentation and code at one verified SHA. It does not establish end-to-end correctness, citation quality, completeness of deletion across backups or every store, behavior during partial projection failures, cross-tenant isolation across every route, production latency, or reliability under load. The number and lifetime of copies in deployment-specific logs, backups, vector stores, and external model providers are not measured. No AutoBot runtime, benchmark, or tests were run for this review.[[README](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/README.md)] [[fact projection](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/fact_projection.py)] [[memory transparency](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/transparency.py)]

## Contact-list follow-up

I checked the official pinned [README](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/README.md) and [FUNDING.md](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/FUNDING.md). Neither publishes a contact email; `FUNDING.md` says the production-support contact path is pending. The JSON records `contact_email: null` and both checked URLs.

## Benchmark status

**Benchmark not run.** I did not execute AutoBot, benchmark workloads, or tests. Source-visible bounds and instrumentation are not measured results. See the [project metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/autobot-ai.md) — source attribution only.
- [Official repository](https://github.com/mrveiss/AutoBot-AI) — canonical repository and default branch.
- [Main commit feed](https://github.com/mrveiss/AutoBot-AI/commits/main.atom) — branch head source.
- [Reviewed head](https://github.com/mrveiss/AutoBot-AI/commit/cb66dab5f250803c98b334ea318e27a8e119ec48)
- [README](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/README.md)
- [FUNDING.md](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/FUNDING.md)
- [General memory storage](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/storage/general_storage.py)
- [Task memory models](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/models.py)
- [Task storage](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/storage/task_storage.py)
- [Knowledge facts](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/facts.py)
- [Fact projections](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/fact_projection.py)
- [Knowledge search](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/search.py)
- [Search scope filters](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/search_filters.py)
- [Essential Story retrieval](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/essential_story.py)
- [Research quarantine](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/knowledge/quarantine.py)
- [Trajectory store](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/trajectory_store.py)
- [Verbatim store](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/verbatim_store.py)
- [Turn completion hook](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/chat_workflow/stop_hook.py)
- [Chat handler](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/chat_workflow/llm_handler.py)
- [Memory privacy and transparency](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/transparency.py)
- [Memory graph owner scope](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/autobot_memory_graph/owner_scope.py)
- [Memory monitor](https://github.com/mrveiss/AutoBot-AI/blob/cb66dab5f250803c98b334ea318e27a8e119ec48/autobot-backend/memory/monitor.py)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only pinned-source review; no AutoBot runtime, benchmarks, or tests.
