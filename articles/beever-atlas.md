# Beever Atlas source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 90 / Beever Atlas / beever-atlas  
**Listed repository locator:** [Beever-AI/beever-atlas](https://github.com/Beever-AI/beever-atlas)  
**Current canonical repository:** [Beever-AI/beever-atlas](https://github.com/Beever-AI/beever-atlas)  
**Default branch / reviewed head:** main / 7d791af27ef4aa19644cb385c7ca24619bc4f848  
**Review time:** 2026-11-24 23:30:44 UTC (15:30:44 PST; America/Los_Angeles).

## Identity and review pin

The curated roster places Beever Atlas at ordinal 90 with the listed repository locator above. Its Atlas entry is retained for identity and attribution only; Atlas descriptions, marks, and layout were not used as assessment evidence. A fresh `git ls-remote --symref` identified `refs/heads/main` as HEAD at the full SHA shown here, and a shallow checkout resolved to the same SHA. GitHub's official main-branch Atom feed also identified that SHA as its newest entry (feed updated 2026-07-01T06:56:51Z). The repository responds at the listed canonical path. [[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/Beever-AI/beever-atlas)] [[main commit feed](https://github.com/Beever-AI/beever-atlas/commits/main.atom)] [[reviewed commit](https://github.com/Beever-AI/beever-atlas/commit/7d791af27ef4aa19644cb385c7ca24619bc4f848)]

## Summary

Beever Atlas turns connected team conversations into channel-scoped atomic facts and entity relationships, then serves them through hybrid retrieval, a cited Q&A agent, an automatically maintained wiki, and MCP tools. The reviewed code shows structured source-message metadata and channel access checks, with channel deletion implemented as a cross-store purge that can report partial completion. This is a pinned source review, not a runtime or benchmark evaluation. [[README.md](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/README.md)] [[AtomicFact model](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/models/domain.py)] [[channel access guard](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/infra/channel_access.py)]

## Who and what

The project is published under the Beever-AI GitHub organization. The README identifies Beever.ai as the builder and presents Beever Atlas as a self-hostable team knowledge application, combining a Python backend, bot, web frontend, and MCP server. The reviewed sources do not establish a maintainer's personal identity. [[README.md](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/README.md)]

## Architecture and data model

**Code observation.** The README describes a unified ingestion path that distills Slack, Discord, Teams, Mattermost, and imported conversations into a semantic store and graph store. The semantic side is layered into channel summaries, topic clusters, and atomic facts; the graph captures entities and relationships. A wiki compiler and QA agents consume these stores, with dashboard and MCP as delivery surfaces. The root README names Weaviate, Neo4j, MongoDB, and Redis as backing stores. [[README.md](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/README.md)] [[backend package map](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/README.md)]

**Code observation.** The ADK ingestion workflow preprocesses messages, runs fact and entity extraction in parallel, then embedding and deterministic cross-batch validation in parallel before a joined persistence stage. The join nodes are explicitly used to ensure fan-in runs persistence once. `AtomicFact` stores the fact text and quality score alongside tier, channel/platform/guild, author and timestamp, source message ID, thread, topic/entity/action tags, media and link references, temporal validity, supersession links, contradiction flag, and optional rationale/context. [[ingestion pipeline](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/agents/ingestion/pipeline.py)] [[AtomicFact model](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/models/domain.py)]

**Code observation.** The persistence agent resolves fact attribution against source messages, stamps channel and platform context, and batch-upserts facts to Weaviate. The store uses a replacement-style upsert keyed by the fact UUID, maps model fields into object properties, and logs failed batch objects and property types when writes fail. [[fact persistence](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/agents/ingestion/persister.py)] [[Weaviate store](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/stores/weaviate_store.py)]

## Write, update, delete, and retrieval

**Write and refresh.** The ingestion workflow stores extracted and enriched facts in batches. Weaviate's `upsert_fact` uses object replacement for an existing UUID or creation for a new one. The fact model includes `valid_at`, `invalid_at`, `supersedes`, and `superseded_by`; hybrid search excludes facts with `invalid_at` set by default. These fields support temporal and correction representation in code, but do not by themselves establish correction accuracy. [[fact persistence](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/agents/ingestion/persister.py)] [[Weaviate store](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/stores/weaviate_store.py)] [[AtomicFact model](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/models/domain.py)]

**Retrieval.** Channel fact search embeds the query and requests Weaviate-native BM25-plus-vector hybrid search, over-fetching up to three times the requested result count, capped at 30, then applies a lightweight maximum marginal relevance reranker. If embedding or hybrid search fails, the capability attempts BM25-only retrieval. Results include fact text, author, channel, time, source message identifier/permalink, fact identifier, confidence-like quality score, tags, and media/link references. The separate MCP `ask_channel` tool exposes quick, deep, and summarize modes, a 90-second timeout, and a response contract with answer and citations. [[memory retrieval capability](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/capabilities/memory.py)] [[Weaviate hybrid search](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/stores/weaviate_store.py)] [[MCP retrieval tools](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/api/mcp_server/_tools_retrieval.py)]

**Scope and isolation.** Public retrieval capabilities take a principal and call the shared channel access guard. The guard checks connection ownership, principal kind, selected-channel membership, and a configurable single-tenant compatibility mode; bridge principals do not inherit the user fallback. The MCP retrieval tool also requires a principal and checks channel access before running the query. These are source-visible authorization rules, not results of an isolation test; deployment settings affect the compatibility branches. [[channel access guard](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/infra/channel_access.py)] [[memory retrieval capability](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/capabilities/memory.py)] [[MCP retrieval tools](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/api/mcp_server/_tools_retrieval.py)]

**Delete.** The API exposes a channel data reset and a separate full hard purge. The purge path applies stricter destructive authorization, then deletes graph data, Weaviate facts/clusters/summaries, QA history, wiki pages and cache, chat history, Mongo channel records, and durable media. Each store failure is captured separately; partial purges are surfaced with errors and retained for retry by the reaper. The source shows a broad deletion workflow, but no execution or copy-completeness audit was performed for this review. [[channel API](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/api/channels.py)] [[channel deletion service](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/services/channel_deletion.py)] [[Weaviate store](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/stores/weaviate_store.py)]

**Provenance and evidence.** Atomic facts retain source message identity, author, timestamp, platform and channel, plus optional thread, link/media, and derivation context. Wiki citations retain fact ID, author, channel, timestamp, excerpt, and permalink. The citation registry assigns stable source IDs from native identity, records retrieval metadata and excerpts, maps answer markers to source IDs, resolves permalinks, and finalizes only sources referenced in the answer. Provenance is therefore represented through source links and citation structures; the code review does not adjudicate whether each cited item supports a generated claim. [[AtomicFact model](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/models/domain.py)] [[citation types](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/agents/citations/types.py)] [[citation registry](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/agents/citations/registry.py)]

## Metric-domain evidence

**Code observations, not measurements.** The retrieved fact path has explicit costs and bounds visible in code: one query embedding, a Weaviate hybrid search with channel/tier filters, up to 30 candidates, then token-overlap MMR selection. It falls back to BM25 when the hybrid path raises; failures are logged. The MCP answer path caps question length and has a 90-second timeout. The README's descriptions of cheaper query-time inference and low latency are project claims, not measurements from this review. [[memory retrieval capability](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/capabilities/memory.py)] [[MCP retrieval tools](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/api/mcp_server/_tools_retrieval.py)] [[README.md](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/README.md)]

**Source-visible observability.** Retrieval logs hybrid/BM25 fallback and MMR activation; the Weaviate batch writer logs failed-object details and failed-property types; channel purge returns per-store counts and errors. The citation registry exposes registered/referenced source counts and null-permalink counts by source kind. These are implementation-level diagnostics, not evidence of a monitored production service or measured performance. [[memory retrieval capability](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/capabilities/memory.py)] [[Weaviate fact store](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/stores/weaviate_store.py)] [[channel deletion service](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/services/channel_deletion.py)] [[citation registry](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/agents/citations/registry.py)]

| Domain | Source-visible evidence | Review measurement |
|---|---|---|
| Answerable recall and abstention | Hybrid semantic/BM25 fact search, MMR reranking, and cited QA tools are present; no answer-quality score was produced here | Unmeasured |
| Correction and staleness | Temporal validity and supersession fields exist; default hybrid retrieval filters invalidated facts | Unmeasured |
| Deletion leakage | Reset and hard purge fan out across stores and expose partial errors; no post-delete probes or replica audit was made | Unmeasured |
| Scope isolation | Read paths check channel access against principal and connection state, with single-tenant compatibility branches | Unmeasured |
| Evidence support and citations | Facts and wiki pages retain message provenance; the citation registry maps cited answer markers to sources | Unmeasured |
| Retrieval latency and write-to-recall delay | Embedding, Weaviate query, reranking, and async ingestion are source-visible; no timings were collected | Unmeasured |
| Tokens, cost, and storage | Retrieval candidate limits and answer timeout are visible; no token, charge, or corpus-attributed storage measurements were collected | Unmeasured |

The comparison project's metric definitions specify answerable recall, abstention, correction, deletion, scope, evidence, latency, write-to-recall delay, token/cost, and storage measurements. The fixture and status record describe the protocol and current execution state; they are not Beever Atlas results. [[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This review is limited to the root README, package map, and selected current ingestion, fact store, retrieval, access, channel deletion, and citation code. It does not establish retrieval quality, correction/stale-value behavior under a corpus, scope isolation under every deployment setting, full deletion of external provider backups or platform originals, runtime performance, token usage, cost, or storage efficiency. The source's partial-purge reporting indicates failures can occur; no purge was triggered or validated here. Upstream statements about latency or cost remain project claims unless measured under a pinned workload. [[README.md](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/README.md)] [[channel access guard](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/infra/channel_access.py)] [[channel deletion service](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/services/channel_deletion.py)]

## Benchmark status

**Benchmark not run.** No Beever Atlas runtime, benchmark workload, or tests were run for this review. Source observations, README claims, and this project's fixture definitions are not benchmark results. See [project metric definitions](../METRICS.md), the [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).[[metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Curated roster entry](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution only.
- [Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/beever-atlas.md) — identity/locator attribution only.
- [Official repository](https://github.com/Beever-AI/beever-atlas) — repository identity.
- [Official main branch feed](https://github.com/Beever-AI/beever-atlas/commits/main.atom) — current head at review time.
- [Reviewed full head](https://github.com/Beever-AI/beever-atlas/commit/7d791af27ef4aa19644cb385c7ca24619bc4f848)
- [README](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/README.md)
- [Backend package map](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/README.md)
- [AtomicFact data model](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/models/domain.py)
- [Ingestion workflow](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/agents/ingestion/pipeline.py)
- [Fact persistence](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/agents/ingestion/persister.py)
- [Weaviate fact store](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/stores/weaviate_store.py)
- [Memory retrieval capability](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/capabilities/memory.py)
- [Channel access guard](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/infra/channel_access.py)
- [MCP retrieval tools](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/api/mcp_server/_tools_retrieval.py)
- [Channel API deletion paths](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/api/channels.py)
- [Cross-store channel deletion service](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/services/channel_deletion.py)
- [Citation types](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/agents/citations/types.py)
- [Citation registry](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/src/beever_atlas/agents/citations/registry.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

## Contact-list follow-up

The official pinned [README contact section](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/README.md#community--contact) publishes `tech@beever.ai` for commercial support, partnerships, or press. I also checked the official pinned [SECURITY.md](https://github.com/Beever-AI/beever-atlas/blob/7d791af27ef4aa19644cb385c7ca24619bc4f848/SECURITY.md), which contains the vulnerability-reporting instructions. The JSON records the published email and exact README source URL.

## Verification boundary

Read-only source inspection at the reviewed full SHA. No Beever Atlas runtime, benchmark, or tests were run.
