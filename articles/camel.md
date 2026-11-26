# CAMEL

## Identity and review pin

- **Ordinal:** 111
- **Catalog name and slug:** CAMEL (`camel`)
- **Listed repository locator:** https://github.com/camel-ai/camel (catalog marks locator explicit)
- **Canonical upstream repository:** https://github.com/camel-ai/camel
- **Default branch:** `master`
- **Reviewed head:** [c9f270d06b80d408809ff4553557a7f5ec4aef64](https://github.com/camel-ai/camel/commit/c9f270d06b80d408809ff4553557a7f5ec4aef64)
- **Reviewed:** 2026-11-25 07:40:58 UTC (2026-11-24 23:40:58 PST; America/Los_Angeles)
- **Status:** Reviewed from source; benchmark not run
- **Catalog attribution:** The [ordinal 111 catalog entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/camel.md) is used only to identify the curated system and its listed locator. Technical observations below come from CAMEL's current upstream source and official docs.

## Summary

CAMEL is a multi-agent framework with a modular memory package. The reviewed memory interfaces represent message records, adapt chat-history and vector stores, and assemble records into agent context. Its default in-process history and vector memory are configurable through storage interfaces; long-term memory combines both paths. This review describes source behavior at the verified `master` head, not measured recall, isolation, or performance.[[README](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/README.md)] [[Memory cookbook](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/docs/cookbooks/advanced_features/agents_with_memory.ipynb)]

## Architecture and data model

The `AgentMemory` contract extends a memory block with retrieval and context-creation operations. `ChatAgent` uses a supplied memory object or constructs `ChatHistoryMemory` by default; `ChatHistoryMemory` uses in-memory key-value storage unless configured otherwise. `VectorDBMemory` wraps a vector block, which defaults to `OpenAIEmbedding` and in-memory `QdrantStorage`; callers can provide alternate backends. `LongtermAgentMemory` composes chat history and vector storage. The official cookbook documents these options and the `write_records()` / context retrieval flow.[[memory interfaces](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/base.py)] [[memory implementations](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/agent_memories.py)] [[vector block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/vectordb_block.py)] [[ChatAgent](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/agents/chat_agent.py)]

A `MemoryRecord` stores a message, backend role, UUID, timestamp, string-valued `extra_info`, and `agent_id`. Vector records serialize that record as payload. The stored unit is a message, rather than an automatically extracted fact or claim.[[record model](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/records.py)] [[vector block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/vectordb_block.py)]

## Write, update, delete, and retrieval

**Write.** Chat history serializes and appends supplied records. Vector memory embeds nonempty message text and stores each vector with its serialized record payload. Long-term memory writes to both stores and updates its current query topic from user messages. The core path is record persistence; it does not itself extract or consolidate new facts.[[chat history block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/chat_history_block.py)] [[vector block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/vectordb_block.py)] [[memory implementations](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/agent_memories.py)]

**Update and deletion.** Chat history supports popping recent records, removing selected indices, and clearing all records; its initial system/developer record is protected from the indexed and pop operations. Vector memory does not implement individual rollback or indexed removal; it exposes full clear. In the combined long-term class, popping/removing affects chat history while the vector memory remains, so clearing the combined object is needed to clear both stores.[[chat history block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/chat_history_block.py)] [[memory implementations](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/agent_memories.py)]

**Retrieval.** Chat history returns all records or a recent window, preserving an initial system/developer message. Vector retrieval embeds the current topic and asks the configured vector store for the top `k` similar payloads; the combined memory places recalled records around the conversation. The core vector query carries a vector and top-k limit, with no agent or tenant filter in this memory block's query construction.[[chat history block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/chat_history_block.py)] [[vector block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/vectordb_block.py)] [[memory implementations](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/agent_memories.py)]

## Scope, provenance, and evidence

The `agent_id` is attached to records by memory wrappers and may be used by configured storage integrations, but the inspected core Qdrant query does not filter on it. Therefore scope separation depends on storage configuration or backend behavior; the core vector-memory path alone does not establish tenant isolation. No isolation workload was run.

Records retain role, timestamp, UUID, and optional metadata, which provide basic message identity and context. The inspected record and vector-memory interfaces do not attach claim-level source citations, confidence/trust state, or an audit trail for edits. These are observations about the reviewed memory paths, not every optional integration in the broader framework.[[record model](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/records.py)] [[vector block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/vectordb_block.py)]

## Efficiency and observability

Vector recall is bounded by `retrieve_limit` (three by default in the memory wrapper), while chat history can be unwindowed or restricted to recent turns. Vector writes embed each nonempty record and retrieval embeds the query, so embedding and backend costs depend on the configured providers and store. The inspected memory path exposes no memory-specific latency, token-cost, or retrieval-quality telemetry. The repository README documents optional model request/response logging, which is broader model logging rather than evidence of memory retrieval metrics.[[memory implementations](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/agent_memories.py)] [[vector block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/vectordb_block.py)] [[README](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/README.md)]

## Limits and unknowns

The default stores are in-memory, so persistence depends on selecting and configuring another backend. Vector memory's source path does not provide per-record deletion or an explicit scope filter. The reviewed sources do not establish encryption, retention guarantees, concurrent-write behavior, or cross-tenant isolation for a production deployment; those properties depend on the selected storage and deployment configuration. No runtime behavior, recall quality, isolation, latency, or storage efficiency was measured.

## Benchmark status

**not_run.** This task inspected source and official docs only. No CAMEL system, benchmark, or test was run. Project metric definitions and fixtures are evaluation protocol, not results.[[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Official repository](https://github.com/camel-ai/camel)
- [Verified master head](https://github.com/camel-ai/camel/commit/c9f270d06b80d408809ff4553557a7f5ec4aef64)
- [Official README](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/README.md)
- [Official memory cookbook](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/docs/cookbooks/advanced_features/agents_with_memory.ipynb)
- [Memory interfaces](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/base.py)
- [Memory implementations](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/agent_memories.py)
- [Memory record model](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/records.py)
- [Chat history block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/chat_history_block.py)
- [Vector database block](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/memories/blocks/vectordb_block.py)
- [ChatAgent integration](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/camel/agents/chat_agent.py)
- [Curated identity and attribution entry](../data/memory-systems.json)
- [Atlas locator attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/camel.md)

**Contact:** The official pinned README lists `camel-ai@eigent.ai` under Community & Contact.[[README](https://github.com/camel-ai/camel/blob/c9f270d06b80d408809ff4553557a7f5ec4aef64/README.md)]
