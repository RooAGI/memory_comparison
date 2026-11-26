# AgentOS (Tanglies) source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 26 / AgentOS (Tanglies) / tanglies-agentos  
**Listed repository locator:** [Tanglies/AgentOS](https://github.com/Tanglies/AgentOS)  
**Current canonical repository:** [Tanglies/AgentOS](https://github.com/Tanglies/AgentOS)  
**Default branch / reviewed head:** main / `5b2718165d9af11d84ab4eec74492ed21fe506d7`  
**Review time:** 2026-11-24 19:09:17 UTC (11:09:17 PST; America/Los_Angeles).

## Identity and scope

The curated roster places **AgentOS (Tanglies)** at ordinal 26, with slug `tanglies-agentos` and listed repository locator `https://github.com/Tanglies/AgentOS`. The roster attributes its entry to Agent Memory Atlas revision `19199a4fc249e89c0793be06f0b166b358089ba0`; this is used only for identity, locator, and attribution. Atlas descriptions, marks, and layout were not used as assessment evidence.[[curated roster](../data/memory-systems.json)] [[Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/tanglies-agentos.md)]

The official GitHub repository page identifies Tanglies/AgentOS as public and shows `main` as its default branch. The official `main` commit feed identifies the current full head as `5b2718165d9af11d84ab4eec74492ed21fe506d7`. Review time: 2026-11-24 19:09:17 UTC (11:09:17 PST; America/Los_Angeles).[[repository](<https://github.com/Tanglies/AgentOS>)][[main commit feed](<https://github.com/Tanglies/AgentOS/commits/main.atom>)][[reviewed head](<https://github.com/Tanglies/AgentOS/commit/5b2718165d9af11d84ab4eec74492ed21fe506d7>)]

The README presents AgentOS as a Python agent platform with runtime, tools, memory, evaluation, and observability. This review concerns the session and long-term memory paths at the pinned revision; source observations are not benchmark measurements.[[README](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/README.md>)]

## Architecture and data model

**Code observation.** AgentOS has separate session and long-term stores. `MemoryStore` keeps message history in a process-local ordered map. `LongTermMemory` delegates persistent operations to a SQLite database and repository. The long-term row schema contains an ID, workspace ID, optional user ID, scope, content, optional session ID, and creation time.[[session memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/memory.py?plain=1>)][[long-term memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/long_term_memory.py?plain=1>)][[repository schema](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/repositories.py?plain=1>)]

**Code observation.** Session entries are keyed by workspace, user, and session. Session state stores messages plus created and updated timestamps. Long-term content is plain text with a 4,000-character source limit. The inspected long-term record schema does not show embeddings, source citations, event-time validity, or supersession/version fields.[[session memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/memory.py?plain=1>)][[long-term memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/long_term_memory.py?plain=1>)][[repository schema](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/repositories.py?plain=1>)]

**Documentation and code observation.** The README describes memory integrated with the Agent runtime and context budgets. The long-term recall implementation uses token and Chinese bigram extraction with substring matching; it does not use semantic/vector retrieval in the inspected path.[[README](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/README.md>)][[long-term memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/long_term_memory.py?plain=1>)]

## Write, update, delete, and retrieval

**Session writes.** Appends add new messages, trim history to a configured per-session bound while aligning at user-turn boundaries, and refresh the update timestamp. Touched sessions move to the newest position; when the configured session count is exceeded, least-recently-used sessions are evicted. `clear` removes the scoped session, and the process-local history does not survive process exit.[[session memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/memory.py?plain=1>)]

**Long-term writes and deletion.** `remember` accepts content, optional session ID, and a scope that defaults to workspace. `forget`, `forget_many`, and `clear` delegate removal of visible records to the repository. The inspected interface establishes those operations, but this bounded review did not inspect every SQL mutation body and does not claim audit, backup, transaction, or physical erasure guarantees.[[long-term memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/long_term_memory.py?plain=1>)][[repository schema](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/repositories.py?plain=1>)]

**Agent tools and correction.** The `remember` tool lets the agent choose stable information to store and accepts `user` or `workspace` scope. `recall` accepts a query and optional scope. The tool documentation cautions against saving temporary content or sensitive credentials. No update or supersession operation was established in the inspected long-term API, so prior content should not be assumed to be automatically corrected when a fact changes.[[memory tools](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/memory_tools.py?plain=1>)][[long-term memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/long_term_memory.py?plain=1>)]

**Retrieval.** Recall extracts lowercase ASCII tokens of at least two characters and Chinese runs with overlapping bigrams, then performs weighted substring matching and returns bounded records. The implementation documentation calls this keyword matching rather than semantic retrieval and notes the tradeoff for synonyms and paraphrases. Context assembly reports recalled count, character count, and an estimated token count; the estimate is not a provider tokenizer.[[long-term memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/long_term_memory.py?plain=1>)]

**Scope isolation.** Session keys include workspace and user IDs. Long-term methods resolve the current workspace/user context and pass those IDs to repository operations; records can be user-only or workspace-visible. These are source-visible predicates, not a demonstrated security guarantee: no cross-scope probes or complete route authorization review were run.[[session memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/memory.py?plain=1>)][[long-term memory](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/long_term_memory.py?plain=1>)][[repository schema](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/repositories.py?plain=1>)]

**Provenance and evidence.** The inspected long-term row preserves content, scope, session ID, and creation timestamp. It does not show source-document IDs, quoted evidence, answer citations, or mutation history. The tool returns memory IDs, which provides record addressing but does not itself establish that an answer is supported by evidence.[[repository schema](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/repositories.py?plain=1>)][[memory tools](<https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/memory_tools.py?plain=1>)]

## Metric-domain evidence

Source observations above describe implementation only. The following outcomes remain unmeasured for this review:

- **Answerable recall and abstention:** keyword recall and an empty-result response exist; no answerability probes were run.
- **Correction and stale values:** no correction/supersession workload was run.
- **Deletion leakage:** scoped removal methods exist; no post-delete probes were run.
- **Scope isolation:** workspace/user filters are visible; no cross-scope probes were run.
- **Evidence support and citation coverage:** these were not adjudicated.
- **Latency and write-to-recall delay:** no timing probes were run.
- **Tokens, cost, and storage:** a token estimate exists, but provider usage, cost, and storage were not measured.

The project definitions and result record are linked here for protocol/status only: [metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json). The status is `not_run`; fixture counts are planned operations, not observations.

## Limits and unknowns

This is a bounded review of the official README and selected memory source files at the verified head. The system, tests, and benchmarks were not run. Production reliability, retrieval quality, durability under failure, concurrency behavior, complete deletion semantics, authorization across all routes, latency, cost, and storage remain unverified. The inspected memory implementation does not establish correction, semantic retrieval, or source-grounded answer behavior.

The official repository README was checked for a published contact email. None is published, so the JSON record stores `contact_email: null` and the exact checked README URL.

## Benchmark status

**Benchmark not run.** No AgentOS system execution, project fixture run, benchmark, or test suite was performed. Project metric definitions, fixture, and result record document the protocol and execution status; they are not measurements of AgentOS.

## Sources

- [Official repository and default branch](https://github.com/Tanglies/AgentOS)
- [Main branch commit feed](https://github.com/Tanglies/AgentOS/commits/main.atom)
- [Reviewed commit](https://github.com/Tanglies/AgentOS/commit/5b2718165d9af11d84ab4eec74492ed21fe506d7)
- [README at reviewed revision](https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/README.md)
- [Session memory at reviewed revision](https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/memory.py?plain=1)
- [Long-term memory at reviewed revision](https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/long_term_memory.py?plain=1)
- [Memory tools at reviewed revision](https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/memory_tools.py?plain=1)
- [Memory repository schema at reviewed revision](https://github.com/Tanglies/AgentOS/blob/5b2718165d9af11d84ab4eec74492ed21fe506d7/src/agentos/runtime/repositories.py?plain=1)
- [Project metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [benchmark status](../results/initial-baselines-status.json)
