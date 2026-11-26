# AgentSwarms memory subsystem — source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 31 / AgentSwarms / agentswarms  
**Listed repository locator:** [AgentSwarms-fyi/agentswarms](https://github.com/AgentSwarms-fyi/agentswarms)  
**Current canonical repository:** [AgentSwarms-fyi/agentswarms](https://github.com/AgentSwarms-fyi/agentswarms)  
**Default branch / reviewed head:** main / `ebb0816479074dbef561c4f1f6a2b437c3229c66`  
**Review time:** 2026-11-24 19:21:17 UTC (11:21:17 PST; America/Los_Angeles).

## Identity and scope

The curated catalog places **AgentSwarms** at ordinal 31, slug `agentswarms`, with listed repository locator `https://github.com/AgentSwarms-fyi/agentswarms`. The catalog attributes the entry to Agent Memory Atlas revision `19199a4fc249e89c0793be06f0b166b358089ba0`; this is recorded for identity and attribution only. Atlas descriptions, marks, and layout were not used as assessment evidence.[[curated roster](../data/memory-systems.json)] [[Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agentswarms.md)]

The official repository page identifies the public canonical repository and shows `main` as its default branch. The official `main` feed and head commit page identify `ebb0816479074dbef561c4f1f6a2b437c3229c66` as the current head used for this review.[[repository and default branch](https://github.com/AgentSwarms-fyi/agentswarms)] [[main commit feed](https://github.com/AgentSwarms-fyi/agentswarms/commits/main.atom)] [[reviewed commit](https://github.com/AgentSwarms-fyi/agentswarms/commit/ebb0816479074dbef561c4f1f6a2b437c3229c66)]

The project README presents a self-hosted agent and data platform. This review examines selected memory subsystem files, not the whole platform or a running deployment.[[README](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/README.md?plain=1)]

## Who and what

AgentSwarms integrates memory into its agent runtime. Its source distinguishes short-term conversation memory from optional, per-agent long-term notes. The default configuration enables short-term memory and summarization, enables automatic extraction, but leaves long-term recall disabled; it sets a 20-message window, a 200-item cap and a recall top-K of five.[[memory configuration](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/types.ts?plain=1)]

## Architecture and data model

The short-term path summarizes older conversation messages into a rolling summary and maintains a separate conversation scratchpad. The long-term path stores items with user, agent and optional conversation IDs, a category and content; item views also carry an ID, score, creation time and last-use time. Categories are fact, preference, episodic and instruction.[[memory orchestration](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/memory.server.ts?plain=1)] [[memory types and defaults](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/types.ts?plain=1)] [[memory tools](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/tools.server.ts?plain=1)]

The app uses its per-user sealing helpers for memory item content, summaries and scratchpads. For sealed long-term records, indexed search words are stored as blind tokens derived for the owner, so the database can match terms without using plaintext words as the index. The code also retains compatibility with pre-existing plaintext rows.[[sealing and blind tokens](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/sealed.server.ts?plain=1)]

## Write, update, delete, and retrieval

**Automatic writes.** After a chat turn, extraction can send up to 4,000 characters from the user message and assistant reply to the configured model. The prompt asks for durable facts, preferences, ongoing decisions, instructions or episodic notes, and asks it to avoid temporary context and raw personal information. The parser accepts at most eight items, enforces a 500-character maximum, validates categories, and rejects redaction placeholders. Items are inserted with user, agent and optional conversation IDs; the item-cap RPC is called afterward, but its implementation was not inspected.[[extraction](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/extract.server.ts?plain=1)] [[memory configuration](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/types.ts?plain=1)]

**Manual writes and deletion.** The `memory_remember` tool inserts a single item and returns its ID. The inspected path does not deduplicate or update an existing item. `memory_forget` deletes a row by ID under the current user. No update or supersession API was established, so a changed fact should not be assumed to replace an older item automatically.[[memory tools](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/tools.server.ts?plain=1)] [[sealed item insertion](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/sealed.server.ts?plain=1)]

**Retrieval.** The tokenizer lowercases and keeps unique ASCII letter/digit terms at least four characters long, after removing a stop-word list. Recall queries keyword-array overlap, restricted by explicit user and agent IDs, and caps the candidate set at 50. It scores keyword overlap alongside the stored score and a recency boost, sorts locally, then returns a bounded top-K. The automatic context path can use the configured top-K; direct tool requests are capped at 10. Returned long-term items are numbered and inserted as text in the system prompt. This is keyword matching, not semantic retrieval.[[tokenizer](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/tokenize.ts?plain=1)] [[retrieval and context formatting](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/recall.server.ts?plain=1)] [[request assembly](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/memory.server.ts?plain=1)] [[manual recall tool](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/tools.server.ts?plain=1)]

**Short-term summary and scratchpad.** When configured, a model folds older conversation messages into a rolling summary, prompted to keep it under 350 words; the current conversation retains a separate message window. The scratchpad provides conversation-scoped JSON key/value storage through `memory_set` and `memory_get`. Both summary and scratchpad have sealing helpers.[[summary generation](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/summarize.server.ts?plain=1)] [[memory tools](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/tools.server.ts?plain=1)] [[sealing helpers](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/sealed.server.ts?plain=1)]

## Scope isolation

Long-term writes include the current user and agent IDs; recall applies equality predicates for both. Tool code comments say these calls are scoped by Supabase row-level security. Summary and scratchpad operations use conversation IDs with the authenticated client. These are source-visible controls; this review did not inspect the full database policy history or run cross-user or cross-agent probes.[[extraction scope](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/extract.server.ts?plain=1)] [[recall scope](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/recall.server.ts?plain=1)] [[tool scope](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/tools.server.ts?plain=1)] [[security policy](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/SECURITY.md?plain=1)]

## Provenance and evidence

Items retain a category and optional originating conversation ID, but the inspected memory type and tool response do not provide source-document IDs, quoted evidence, claim-level citations, or mutation history. An item ID addresses a record; it does not establish that an answer is supported by cited evidence.[[memory types](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/types.ts?plain=1)] [[write and recall tools](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/tools.server.ts?plain=1)] [[extraction](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/extract.server.ts?plain=1)]

## Source-visible efficiency and observability

Long-term recall does not call an embedding model in the inspected path. It uses a GIN-indexed keyword overlap query, considers up to 50 candidate rows and returns a bounded result. Summary and extraction each make a configured model call and record provider token counts and elapsed time through the gateway usage recorder when usage is returned. These are code observations, not measured latency, accuracy, token cost or storage results.[[retrieval](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/recall.server.ts?plain=1)] [[summarization](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/summarize.server.ts?plain=1)] [[extraction](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/extract.server.ts?plain=1)]

## Metric-domain evidence

All outcomes below remain **unmeasured** for this review:

- **Answerable recall and abstention:** keyword matching and an empty-result response exist; no answerability probes were run.
- **Correction and stale values:** no update/supersession interface was established; no correction workload was run.
- **Deletion leakage:** the delete tool exists; there were no post-delete retrieval or storage-erasure probes.
- **Scope isolation:** user and agent predicates are visible; no cross-scope probes were run.
- **Evidence support and citation coverage:** no claim-level evidence was adjudicated.
- **Latency and write-to-recall delay:** no end-to-end timing or delayed recall probes were run.
- **Tokens, cost and storage:** some model calls can record returned token usage, but no cost or storage measurements were collected.

Project definitions, fixture, and current execution status are linked for protocol/status only: [metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json). Those files are not AgentSwarms results.[[project metrics](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark status](../results/initial-baselines-status.json)]

## Limits and unknowns

This was a bounded source review of the README and selected memory files at the verified head. It did not inspect every database migration and policy, the item-pruning RPC, every chat integration path, or complete deletion behavior. The system, benchmark and tests were not run. Retrieval quality, extraction accuracy, duplicate growth, correction behavior, backup erasure, security isolation under adversarial use, latency, cost and storage remain unknown.

The official pinned `SECURITY.md` publishes `hello@agentswarms.fyi` for vulnerability reports; the exact source URL is recorded in the JSON review entry.[[official security contact](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/SECURITY.md?plain=1)]

## Benchmark status

**Benchmark not run.** No AgentSwarms runtime, project fixture, benchmark, or test suite was executed. Project metrics, the fixture, and result record document the protocol and execution status only.

## Sources

- [Official repository and default branch](https://github.com/AgentSwarms-fyi/agentswarms)
- [Official main branch commit feed](https://github.com/AgentSwarms-fyi/agentswarms/commits/main.atom)
- [Reviewed commit](https://github.com/AgentSwarms-fyi/agentswarms/commit/ebb0816479074dbef561c4f1f6a2b437c3229c66)
- [README at reviewed revision](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/README.md?plain=1)
- [Memory types and defaults](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/types.ts?plain=1)
- [Memory orchestration](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/memory.server.ts?plain=1)
- [Short-term summarization](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/summarize.server.ts?plain=1)
- [Automatic long-term extraction](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/extract.server.ts?plain=1)
- [Long-term recall](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/recall.server.ts?plain=1)
- [Tokenizer](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/tokenize.ts?plain=1)
- [Agent memory tools](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/tools.server.ts?plain=1)
- [Sealing and blind tokens](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/src/utils/memory/sealed.server.ts?plain=1)
- [Security policy and contact](https://github.com/AgentSwarms-fyi/agentswarms/blob/ebb0816479074dbef561c4f1f6a2b437c3229c66/SECURITY.md?plain=1)
- [Project metrics](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json)
- [Curated roster identity and attribution only](../data/memory-systems.json)
