# DeerFlow

**Review status:** Reviewed from code and official documentation at `main` [`5398a584c64ae6d38381caeff2a772acbff2fc5a`](https://github.com/bytedance/deer-flow/commit/5398a584c64ae6d38381caeff2a772acbff2fc5a). Review time: 2026-11-25 10:48:15 UTC (02:48:15 PST; America/Los_Angeles).

## Summary

DeerFlow is a long-running agent harness with a pluggable memory subsystem. Its default DeerMem backend extracts structured facts and summaries, stores user-level summaries in JSON and agent-scoped facts in Markdown files, and retrieves facts with a local FTS5/BM25 index.[readme][memory_guide][deermem][storage][retrieval] Optional Mem0, OpenViking, and Honcho backends have different storage, scope, and management behavior; the shared backend contract does not make them semantically identical.[backend_contract][memory_guide] This review covers source and documentation, not runtime or benchmark results.

## Who and what

The official README describes DeerFlow as an open-source super-agent harness built around planning, tools, skills, memory, subagents, and sandboxed execution.[readme] DeerFlow is an application framework with memory backends, rather than a standalone memory database. The roster resolves ordinal 184 to DeerFlow, slug `deer-flow`, listed repository `https://github.com/bytedance/deer-flow`, with explicit repository attribution. Its pinned Atlas record is retained for roster identity and locator attribution only; it is not evidence for this assessment.[catalog][atlas]

## Architecture and data model

The official repository page identifies `main` as the default branch.[repo] The current official main commit feed reports full head `5398a584c64ae6d38381caeff2a772acbff2fc5a` at 2026-11-25T10:13:38Z; the commit page and reviewed source URLs pin that revision.[head_feed][head]

DeerFlow routes memory through a `MemoryManager` contract. Every backend implements `add` and `get_context`; management operations and lifecycle hooks are optional and default to unsupported or no-op behavior. The factory selects the backend from configuration and supplies storage path and host callbacks. The guide lists DeerMem as default, plus no-op, Mem0, OpenViking, and Honcho backends.[backend_contract]

DeerMem owns its update queue, updater, storage, and retrieval dependencies. Its default file storage separates global user/history summaries in a per-user `memory.json` from canonical fact files under agent-specific fact directories. Facts carry fields such as ID, content, category, confidence, timestamps, and source metadata. The file layout hashes unsafe user identifiers into stable directory-safe names and validates agent names; an omitted agent maps to a reserved `__default__` bucket.[deermem][storage][paths]

The default retrieval adapter maintains a derived SQLite FTS5 index; it can rebuild that index from canonical fact files. The documentation says it can rebuild at Gateway startup or on first scoped search, and also describes a substring fallback when the adapter is disabled.[storage][retrieval][memory_guide]

## Write, update, delete, and retrieval

**Write and extraction.** In DeerMem middleware mode, user inputs and final assistant replies are eligible for extraction; assistant turns that call tools are excluded. Extraction is queued and debounced independently by conversation, user, and agent, then processed serially. The documented default debounce is 30 seconds, with a 300-second maximum wait; extraction or queue backlog can delay completion, and pending work can be lost if the process exits.[memory_guide][updater] The current memory guide describes classification of extracted facts by scope, durability, and authority before a deterministic write gate accepts them. The labels guide the gate and are not persisted as fact evidence.[memory_guide][updater]

**Update and correction.** DeerMem supports explicit fact creation, update, and deletion hooks, in addition to automatic extraction. The storage/updater contract uses revisions and conflict checks to reject stale writes; repeated duplicate facts are skipped during apply. The documented automatic correction and contradiction handling are extraction paths, not an auditable version history of every prior fact value.[deermem][storage][updater][backend_contract][memory_guide]

**Delete and capacity.** Fact deletion and clear operations are exposed by DeerMem management APIs. The memory guide states capacity eviction is physical; an optional `hybrid-v1` policy can rank by confidence, explicit-confirmation freshness, and access heat and can reserve correction slots. Its bounded eviction audit stores metadata such as IDs, categories, scores, and reasons, not the evicted fact text.[deermem][updater][eviction][memory_guide] No runtime residual-data or backup-erasure check was performed.

**Retrieval.** The FTS5 adapter supports scoped text search with category filters and result limits. Its source describes BM25 ranking combined with time decay and confidence, with jieba tokenization when available and CJK bigrams as a fallback. The backend also exposes exact fact lookup by ID and context injection; query-aware relevance and diversity ranking are optional configuration.[retrieval][deermem][prompt][memory_guide] Search ranking and injection behavior are implementation details, not evidence of answerable recall accuracy.

## Scope isolation

DeerMem stores user identities under separate directory buckets and facts below a normalized per-agent path. Retrieval carries user and agent scope filters into the search adapter; the default bucket is reserved for calls without an explicit agent name.[paths][retrieval][deermem] The docs also describe a separate project-fact pool for durable project-scoped information, while temporary task state and one-time permissions stay in conversation state.[memory_guide] These source-visible boundaries do not establish deployed configuration correctness or measured cross-scope isolation. The optional OpenViking backend uses a separate single-user or fail-closed multi-user/multi-tenant configuration path.[memory_guide]

## Provenance, efficiency, and observability

Facts can retain a source value and confidence, including conversation-source metadata; the compatibility API projects structured source metadata back to a legacy string.[deermem][updater] This provides limited origin metadata, not quoted source passages, claim-level citations, or independent verification of extracted truth.[memory_guide][deermem]

Source-visible efficiency features include debounced writes, serial extraction, incremental fact-file operations, optimistic revision checks, an LRU cap on in-process scope caches, and a rebuildable SQLite index.[memory_guide][storage][retrieval] DeerFlow supplies callbacks for tracing memory-related LLM calls, while DeerMem exposes retrieval status and logs extraction, indexing, and queue issues.[backend_contract][deermem][retrieval] These are implementation and documentation observations; no latency, token, cost, storage, or reliability measurements were collected.

## Metric-domain evidence

- Answerable retrieval and abstention — unmeasured. Search and prompt injection are implemented, but no answerability workload was run.[retrieval][prompt][metrics][status]
- Correction accuracy and stale-value rate — unmeasured. Automatic updates and explicit fact edits exist, but no correction sequence was evaluated.[updater][metrics][status]
- Deletion leakage — unmeasured. Fact deletion and physical capacity eviction are documented; no residual-data probe was run.[storage][metrics][status]
- Scope isolation — unmeasured. User and agent path/search scopes are visible; no cross-user, cross-agent, or project isolation workload was run.[paths][retrieval][metrics][status]
- Evidence support and citation coverage — unmeasured. Source metadata exists, but no claim-evidence adjudication was performed.[deermem][metrics][status]
- Retrieval latency and write-to-recall delay — unmeasured. FTS5, queueing, and indexing paths are inspectable, but no timing probe was run.[memory_guide][retrieval][metrics][status]
- Tokens and cost — unmeasured. The configured extractor may call an LLM, but no usage or provider-cost data was collected.[updater][metrics][status]
- Storage efficiency — unmeasured. Canonical files and a derived index are described, but no corpus-attributed storage measurement was made.[storage][retrieval][metrics][status]

Project benchmark status is [`not_run`](../data/system-reviews/deer-flow.json); see [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution-status record](../results/initial-baselines-status.json). These define project evaluation materials; no DeerFlow runtime, tests, or benchmarks were run.[metrics][fixture][status]

## Contact

The official pinned README and SECURITY.md were checked for a contact email. The README publishes no email, and SECURITY.md directs vulnerability reports to GitHub Security; `contact_email` is therefore null. No email was inferred from commit or profile metadata.[readme][security]

## Limits and unknowns

- DeerFlow is a broad harness with several selectable memory backends. This assessment emphasizes default DeerMem; backend-specific behavior can differ materially.[readme][backend_contract]
- DeerMem extraction depends on model output and deterministic gates. Source structure cannot establish fact quality, correction accuracy, or correct scope classification in operation.[memory_guide][updater]
- A fact's source and confidence fields do not constitute citation verification or calibrated certainty.[deermem][memory_guide]
- Physical fact deletion and capacity eviction do not establish removal from backups, filesystem snapshots, or other copies. No deletion test was run.[storage][memory_guide][metrics]
- The review inspected selected official documentation and DeerMem source at the verified `main` head. It did not audit every backend, API route, deployment mode, or platform integration.
- No DeerFlow runtime, tests, or benchmarks were run; all project metric domains remain unmeasured.

## Sources

- [Official repository](https://github.com/bytedance/deer-flow) and [main commit feed](https://github.com/bytedance/deer-flow/commits/main.atom).
- [Verified current head](https://github.com/bytedance/deer-flow/commit/5398a584c64ae6d38381caeff2a772acbff2fc5a).
- [README](https://github.com/bytedance/deer-flow/blob/5398a584c64ae6d38381caeff2a772acbff2fc5a/README.md), [long-term memory guide](https://github.com/bytedance/deer-flow/blob/5398a584c64ae6d38381caeff2a772acbff2fc5a/docs/guide/memory.md), and [memory backend contract](https://github.com/bytedance/deer-flow/blob/5398a584c64ae6d38381caeff2a772acbff2fc5a/backend/packages/harness/deerflow/agents/memory/backends/README.md).
- [DeerMem manager](https://github.com/bytedance/deer-flow/blob/5398a584c64ae6d38381caeff2a772acbff2fc5a/backend/packages/harness/deerflow/agents/memory/backends/deermem/deer_mem.py), [storage](https://github.com/bytedance/deer-flow/blob/5398a584c64ae6d38381caeff2a772acbff2fc5a/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/storage.py), [updater](https://github.com/bytedance/deer-flow/blob/5398a584c64ae6d38381caeff2a772acbff2fc5a/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py), [retrieval](https://github.com/bytedance/deer-flow/blob/5398a584c64ae6d38381caeff2a772acbff2fc5a/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/retrieval.py), [paths](https://github.com/bytedance/deer-flow/blob/5398a584c64ae6d38381caeff2a772acbff2fc5a/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/paths.py), and [eviction policy](https://github.com/bytedance/deer-flow/blob/5398a584c64ae6d38381caeff2a772acbff2fc5a/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/eviction.py).
- [Official security policy](https://github.com/bytedance/deer-flow/blob/5398a584c64ae6d38381caeff2a772acbff2fc5a/SECURITY.md).
- [Roster entry](../data/memory-systems.json) and [pinned Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/deer-flow.md); Atlas is identity/locator context only.
- [Metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).
