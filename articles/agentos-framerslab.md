# AgentOS

## Identity and review pin

- **Curated ordinal:** 25 in `data/memory-systems.json`
- **Listed name / slug:** AgentOS / `agentos-framerslab`
- **Listed repository locator:** https://github.com/framerslab/agentos
- **Canonical repository:** https://github.com/framerslab/agentos
- **Default branch:** `master`
- **Reviewed head:** [`2ce57e171eb0af6eaa729307b41908f8e230b7d2`](https://github.com/framerslab/agentos/commit/2ce57e171eb0af6eaa729307b41908f8e230b7d2)
- **Reviewed at:** 2026-11-24 19:03:34 UTC (11:03:34 PST, America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The roster’s Atlas source attribution is [the pinned AgentOS report](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agentos-framerslab.md). It supplied identity and the listed locator only. Its descriptions, marks, and layout were excluded from this assessment.

## Summary

AgentOS is a TypeScript agent framework with a cognitive-memory layer. It encodes scoped traces, retrieves them for a query, and assembles context for an agent. The code supports working memory, graph associations, optional typed facts, and in-memory or SQL-backed storage. Findings below describe source and documentation at the pinned revision; they are not runtime results.

## Who and what

The official [README](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/README.md) identifies `@framers/agentos` as the core runtime of a TypeScript AI agent framework and lists cognitive memory among its capabilities. The repository is under the framerslab GitHub organization. No individual maintainer identity is inferred.

## Architecture and data model

[`CognitiveMemoryManager`](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/cognition/memory/CognitiveMemoryManager.ts) coordinates trace encoding, recall, prompt assembly, working memory, optional graph and typed-network components, health diagnostics, and deletion. The [GMI runtime](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/api/gmi.ts) connects a memory manager to sessions. Its [memory builder](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/api/runtime/agentCognitiveMemory.ts) wires embeddings, an in-memory vector store, a knowledge graph, and optionally a persistent Brain and archive.

A [memory trace](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/cognition/memory/core/types.ts) stores content, type, scope and scope ID, timestamps, tags/entities, encoding and access fields, and emotional context. Provenance records the source type and timestamp, confidence, verification count, and optional source/contradiction references. A source-derived trust policy separately gates authorization, personalization, and factual-claim use.

The [memory overview](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/docs/MEMORY_SYSTEM_OVERVIEW.md) describes a portable SQL adapter layer and storage for traces, indexes, graph data, feedback, consolidation records, and optional verbatim archives. These are documented design claims, not evidence of measured capacity or cross-adapter equivalence.

## Write, update, delete, and retrieval

- **Write:** `encode()` creates an episodic trace by default, or uses a caller-supplied type and scope. It defaults provenance to `user_statement`, copies the trust policy for that source type, stores the trace, and focuses it in working memory. Graph registration and typed-network extraction are optional; extraction is off by default in the manager.
- **Update/correction:** traces contain update timestamps and provenance fields, but this inspection did not establish a general correction-history contract for `encode()`. Other correction and lifecycle APIs exist; their guarantees depend on the selected facade and configuration. Metadata presence alone does not show current-value accuracy.
- **Delete:** manager deletion removes traces or a scope and cleans up graph, archive, and typed facts. The persistent [Memory facade](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/cognition/memory/io/facade/Memory.ts) removes graph copies before rows and updates indexes. Higher-level [subject erasure](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/cognition/memory/io/forgetUserMemory.ts) writes a tombstone, attempts the mind, store, pages, and sessions, then reports reached and missed parts. Its documented exclusions include the host’s conversation history, documents ingested outside the subject’s scope, and organization-scope memory.
- **Retrieval:** dense retrieval is the default. Optional hybrid mode runs dense, exact-word, and recency legs; fuses ranks, deduplicates, and cuts to top K. A configured reranker can reorder candidates. Prompt assembly applies a token budget. Optional recall capture records per-leg ranks/timing and reranker details; those fields do not establish measured quality or latency.

## Scope isolation

The [conversation scope-key implementation](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/cognition/memory/retrieval/store/conversationScopeKey.ts) encodes an agent ID and a subject kind/ID for a named user, anonymous session, or operator. The GMI path documents per-session working memory and recall scoped to the session and user. These source observations describe keying and filtering behavior; no cross-scope probes or authorization checks were run in this review.

## Provenance and evidence

Trace provenance distinguishes user statements, tool results, inferences, retrieved documents, and other source classes. The trust policy allows source-dependent use for authorization, personalization, or factual claims and can require reverification. This is a code-level policy mechanism; it does not establish that generated claims are actually supported by cited evidence.

## Source-visible efficiency and observability

The recall pipeline exposes candidate counts, retrieval legs, ranks, reranker information, and elapsed-time fields through optional capture structures. Recall logging emits structured events; absence events are limited to one per process and reason. These are source-visible observability paths. This review did not collect latency, token, cost, storage, or write-to-recall measurements.

## Metric-domain evidence

All domains below are **unmeasured** for this review. Project definitions are in [METRICS.md](../METRICS.md). The shared [execution-status record](../results/initial-baselines-status.json) and [benchmark fixture](../fixtures/memory-benchmark-v1.json) are not AgentOS measurements.

| Domain | Source observation | Measurement status |
|---|---|---|
| Answerable recall and abstention | Retrieval and confidence-policy hooks are present. | Unmeasured |
| Correction accuracy and stale values | Trace metadata and correction paths do not supply adjudicated post-correction outcomes. | Unmeasured |
| Deletion leakage | Erasure code reports reached/missed stores. | Unmeasured |
| Scope isolation | Conversation keys and GMI scope wiring are source-visible. | Unmeasured |
| Evidence support and citation coverage | Provenance and trust policy can gate source use. | Unmeasured |
| Latency and write-to-recall delay | Optional per-leg timing/capture fields exist. | Unmeasured |
| Tokens, cost, and storage | No relevant workload measurements were collected. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of selected documentation and code at one verified revision. It does not establish runtime correctness, adapter-specific behavior, security isolation, deletion completeness, retrieval quality, operational reliability, or performance. AgentOS has several memory facades and configuration paths; behavior depends on the runtime, store, enabled mechanisms, retrieval policy, providers, and deletion wiring. This review does not audit every path.

## Benchmark status

**Benchmark not run.** No AgentOS system execution, benchmark, or tests were run. Source observations above are not measurements. The [system review record](../data/system-reviews/agentos-framerslab.json) stores the structured source/citation contract. The project’s [metric definitions](../METRICS.md), [execution-status record](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json) remain separate from this system’s source findings.

## Sources

- [Current canonical repository](https://github.com/framerslab/agentos)
- [Pinned current head](https://github.com/framerslab/agentos/commit/2ce57e171eb0af6eaa729307b41908f8e230b7d2)
- [Official README at reviewed revision](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/README.md)
- [Official memory overview at reviewed revision](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/docs/MEMORY_SYSTEM_OVERVIEW.md)
- [CognitiveMemoryManager](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/cognition/memory/CognitiveMemoryManager.ts)
- [Recall pipeline](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/cognition/memory/retrieval/recall/pipeline.ts)
- [Memory trace and trust types](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/cognition/memory/core/types.ts)
- [Conversation scope keys](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/cognition/memory/retrieval/store/conversationScopeKey.ts)
- [GMI memory builder](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/api/runtime/agentCognitiveMemory.ts)
- [Subject memory deletion](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/src/cognition/memory/io/forgetUserMemory.ts)
- [Official support contact](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/SUPPORT.md)
- [Official security policy](https://github.com/framerslab/agentos/blob/2ce57e171eb0af6eaa729307b41908f8e230b7d2/.github/SECURITY.md)
- [Project metrics](../METRICS.md)
- [Benchmark status](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
