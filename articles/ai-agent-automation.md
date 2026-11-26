# AI Agent Automation memory — source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 35 / AI Agent Automation / ai-agent-automation  
**Listed repository locator:** [vmDeshpande/ai-agent-automation](https://github.com/vmDeshpande/ai-agent-automation)  
**Current canonical repository:** [vmDeshpande/ai-agent-automation](https://github.com/vmDeshpande/ai-agent-automation)  
**Default branch / reviewed head:** main / `86b6072dd4c9bf6abe68c26c4265b3296a368737`  
**Review time:** 2026-11-24 19:35:21 UTC (11:35:21 PST; America/Los_Angeles).

## Identity and scope

The curated catalog places **AI Agent Automation** at ordinal 35 with slug `ai-agent-automation` and listed repository locator `https://github.com/vmDeshpande/ai-agent-automation`. It attributes the entry to Agent Memory Atlas revision `19199a4fc249e89c0793be06f0b166b358089ba0`; that attribution is recorded only for catalog identity. Atlas descriptions, marks, layout, and conclusions were not assessment evidence.[[curated roster](../data/memory-systems.json)] [[Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ai-agent-automation.md)]

The official GitHub repository page identifies the public canonical repository and `main` as its default branch. Its latest commit entry and the official `main` Atom feed agree on full head `86b6072dd4c9bf6abe68c26c4265b3296a368737`; that is the revision reviewed here.[[repository and default branch](https://github.com/vmDeshpande/ai-agent-automation)] [[official main commit feed](https://github.com/vmDeshpande/ai-agent-automation/commits/main.atom)] [[reviewed head commit](https://github.com/vmDeshpande/ai-agent-automation/commit/86b6072dd4c9bf6abe68c26c4265b3296a368737)]

This is a bounded inspection of selected documentation and memory-related code at that commit. The platform, its tests, and benchmark workloads were not run.

## Who and what

The README describes a self-hosted workflow automation platform with agents, tool integrations, document retrieval, and execution logs. Memory is integrated into configured workflow LLM and agent-call steps, rather than presented in the inspected code as a separate hosted memory service.[[README.md](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/README.md)] [[LLM step handler](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/handlers/llm.handler.js)] [[agent-call handler](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/handlers/agentCall.handler.js)]

## Architecture and data model

**Documentation observation.** The semantic-memory guide describes local MongoDB storage, embedding generation, cosine-similarity retrieval, top-K prompt injection, a memory management UI, and per-agent retention limits. Treat those as documented behavior claims; the implementation details below come from inspected code.[[semantic memory guide](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/docs/semantic-memory.md)]

**Code observation.** `AgentMemory` is a MongoDB/Mongoose document with required `agentId`, plaintext `content`, a numeric embedding array, optional task/workflow IDs and type metadata, embedding provider/model strings, and timestamps. The schema indexes `agentId`. There is no vector database or vector index in this inspected schema.[[AgentMemory schema](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/models/agentMemory.model.js)]

**Code observation.** The LLM and agent-call handlers opt into memory through `useMemory`: they retrieve memories before a model call, append up to 4,000 characters of formatted memory to the prompt, and then store a JSON user/assistant conversation envelope with task and workflow metadata. These are conversation records; the inspected path does not extract standalone facts or preferences.[[LLM step handler](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/handlers/llm.handler.js)] [[agent-call handler](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/handlers/agentCall.handler.js)]

## Write, update, delete, and retrieval

**Write.** `storeMemory` asks the embedding adapter to embed the supplied content, then checks that content is at least 20 characters before inserting it. It writes the embedding and metadata and then applies a fixed 500-row per-agent retention check. Because embedding is requested before the length guard, short rejected content can still incur an embedding request.[[memory service](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/services/memoryService.js)] [[embedding adapter](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/embeddingAdapter.js)]

**Update and correction.** The inspected memory routes and controller expose list and delete operations, but no update route. The semantic-memory guide says users can modify memories in the UI; this code slice does not establish that edit path or its behavior. Correction, supersession, and stale-value handling are therefore unknown from the inspected interface.[[memory routes](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/routes/memory.routes.js)] [[memory controller](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/controllers/memory.controller.js)] [[semantic memory guide](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/docs/semantic-memory.md)]

**Delete.** The authenticated management API can delete one memory or clear all memories for an owned agent. The controller checks agent ownership before deletion and uses MongoDB `deleteOne` / `deleteMany`; no tombstone or deletion audit is visible in these selected files. Physical erasure from backups or other operational copies was not established.[[memory routes](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/routes/memory.routes.js)] [[memory controller](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/controllers/memory.controller.js)]

**Retrieval.** `retrieveMemory` requires a user ID, verifies that the supplied agent belongs to that user, and rechecks ownership in the Agent collection. It embeds the query, loads all conversation memories for that agent, computes cosine similarity in application code, sorts descending, and slices to `topK`. Although the function accepts `minScore`, the inspected implementation does not apply it. A mismatch in embedding dimensions receives score zero; no abstention calibration was established.[[memory service](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/services/memoryService.js)] [[embedding adapter](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/embeddingAdapter.js)]

## Scope isolation and provenance

**Scope.** Stored rows are keyed by agent ID. Retrieval independently verifies the authenticated user's ownership of that agent and filters the memory query by agent ID and conversation type. The management API similarly constrains listing, per-agent deletion, and clear-all operations to agents owned by the authenticated user. These are source-level boundaries; no cross-user runtime probe was run, and this inspection does not establish isolation across every deployment path.[[memory service](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/services/memoryService.js)] [[memory controller](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/controllers/memory.controller.js)] [[memory routes](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/routes/memory.routes.js)]

**Provenance and evidence.** Rows retain agent, optional task/workflow identifiers, type, creation/update timestamps, and embedding provider/model fields. The service populates those provider/model fields from the agent's chat configuration, even though the embedding adapter can choose a separate embedding provider; records may therefore not identify the actual embedder when those configurations differ. No source citation, evidence span, confidence, trust state, or mutation history appears in the inspected memory schema.[[AgentMemory schema](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/models/agentMemory.model.js)] [[memory service](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/services/memoryService.js)] [[embedding adapter](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/embeddingAdapter.js)]

## Source-visible efficiency and observability

**Code observation.** Each retrieval loads every matching conversation row and their stored vectors before computing cosine similarity in JavaScript. The inspected schema has an ordinary agent ID index but no vector index, so scan work grows with the number of stored memories for an agent. The fixed retention pass counts all memory types but selects only conversation rows for pruning, and deletes at most the computed excess in one pass.[[memory service](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/services/memoryService.js)] [[AgentMemory schema](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/models/agentMemory.model.js)]

**Code observation.** The service logs each retrieval's score and the first 60 content characters to stdout. The embedding adapter logs provider/model selection. Workflow step metrics include the number of retrieved memories, but the inspected memory path does not report retrieval duration, memory-specific token/cost totals, or storage bytes. These are instrumentation observations, not measurements.[[memory service](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/services/memoryService.js)] [[embedding adapter](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/embeddingAdapter.js)] [[LLM step handler](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/handlers/llm.handler.js)]

**Documentation observation.** The platform telemetry guide says optional telemetry is disabled by default and excludes prompts, memory contents, and execution logs from remote heartbeats. This is a documentation statement; it does not change the separate code observation that memory retrieval logs a content preview locally.[[telemetry guide](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/docs/telemetry.md)] [[memory service](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/services/memoryService.js)]

## Project metric domains

All benchmark domains are **unmeasured** for AI Agent Automation. Source inspection shows a cosine ranking path and an empty/top-K interface, but no answerability or abstention results; no correction/update path was established; delete endpoints exist but deletion leakage was not probed; ownership predicates are visible but scope isolation was not measured; memory records lack source evidence fields in this schema; and no workload measured latency, write-to-recall delay, tokens, cost, or storage efficiency. Project metric definitions, fixture, and execution-status record define the measurement protocol, not system results.[[project metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark status](../results/initial-baselines-status.json)]

## Limits and unknowns

This review covered the official README, memory and agent documentation, selected memory service/model/controller/routes, embedding adapter, LLM and agent-call handlers, and telemetry guide at the verified head. It did not inspect every memory call site, the complete database/index configuration, all UI code, backup/deployment behavior, or every ownership boundary. Runtime correctness, effective retention under mixed memory types, citation support, deletion completeness, cross-user isolation, quality, latency, cost, and storage use remain unverified. “Not established here” is scoped to these inspected sources and does not prove that a capability is absent.[[README.md](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/README.md)] [[semantic memory guide](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/docs/semantic-memory.md)] [[memory service](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/services/memoryService.js)] [[memory controller](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/controllers/memory.controller.js)]

## Contact-list follow-up

I checked the official pinned README, repository SECURITY.md, and the official project website for a published contact email. None of those checked sources publishes an email address. The SECURITY.md points reporters to the maintainer's GitHub profile; I did not consult that profile or infer an address. The JSON record stores `contact_email: null` and lists the checked URLs.[[README.md](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/README.md)] [[SECURITY.md](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/SECURITY.md)] [[official project website](https://vmdeshpande.github.io/ai-automation-platform-website/)]

## Benchmark status

**Benchmark not run.** No system execution, test suite, or benchmark workload was run. Source and documentation observations are not measured results. See the project metric definitions, benchmark status record, and fixture for the separate protocol.[[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical repository](https://github.com/vmDeshpande/ai-agent-automation)
- [Official main branch commit feed](https://github.com/vmDeshpande/ai-agent-automation/commits/main.atom)
- [Reviewed full head commit](https://github.com/vmDeshpande/ai-agent-automation/commit/86b6072dd4c9bf6abe68c26c4265b3296a368737)
- [README.md](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/README.md)
- [docs/semantic-memory.md](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/docs/semantic-memory.md)
- [docs/agent-system.md](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/docs/agent-system.md)
- [docs/telemetry.md](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/docs/telemetry.md)
- [backend/src/models/agentMemory.model.js](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/models/agentMemory.model.js)
- [backend/src/services/memoryService.js](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/services/memoryService.js)
- [backend/src/controllers/memory.controller.js](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/controllers/memory.controller.js)
- [backend/src/routes/memory.routes.js](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/routes/memory.routes.js)
- [backend/src/agents/embeddingAdapter.js](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/embeddingAdapter.js)
- [backend/src/agents/handlers/llm.handler.js](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/handlers/llm.handler.js)
- [backend/src/agents/handlers/agentCall.handler.js](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/backend/src/agents/handlers/agentCall.handler.js)
- [SECURITY.md](https://github.com/vmDeshpande/ai-agent-automation/blob/86b6072dd4c9bf6abe68c26c4265b3296a368737/SECURITY.md)
- [Official project website](https://vmdeshpande.github.io/ai-automation-platform-website/)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark status](../results/initial-baselines-status.json)
- [Curated roster locator and attribution](../data/memory-systems.json)

**Verification boundary:** no AI Agent Automation system, tests, or benchmarks were run.

---
