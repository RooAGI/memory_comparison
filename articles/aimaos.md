# AIMAOS source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 43 / AIMAOS / `aimaos`  
**Listed repository locator:** [munch2u-a11y/AIMAOS](https://github.com/munch2u-a11y/AIMAOS)  
**Canonical repository:** [munch2u-a11y/AIMAOS](https://github.com/munch2u-a11y/AIMAOS)  
**Default branch / reviewed head:** main / `0d8c58c2bee5addc72a13c5c95839635d809b5b0`  
**Review time:** 2026-11-24 20:09:46 UTC (12:09:46 PST; America/Los_Angeles).

## Identity and scope

The curated roster places AIMAOS at ordinal 43, gives the slug `aimaos`, lists the repository locator above, and attributes the entry to the Agent Memory Atlas document pinned at `19199a4fc249e89c0793be06f0b166b358089ba0`. The roster is used only to establish identity, locator, and attribution. Atlas descriptions, marks, prose, and layout are not assessment evidence. The official repository page identifies the canonical public repository and default branch `main`; the page's latest commit and official main Atom feed both identify `0d8c58c2bee5addc72a13c5c95839635d809b5b0` as the current head at review time. [[curated roster](../data/memory-systems.json)] [[repository](https://github.com/munch2u-a11y/AIMAOS)] [[main commits feed](https://github.com/munch2u-a11y/AIMAOS/commits/main.atom)] [[reviewed commit](https://github.com/munch2u-a11y/AIMAOS/commit/0d8c58c2bee5addc72a13c5c95839635d809b5b0)]

AIMAOS is a local-first office workstation with specialized agents, matter/task state, document workflows, and human review. The repository documents a single-operator Linux public beta. This review focuses on its mRAG agent-memory path, rather than treating the whole workstation as a standalone memory service. [[README](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/README.md>)] [[OfficeAgent](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/office_agent.py>)]

## Architecture and data model

Each roster agent is assigned an agent-named workspace, and the shared `OfficeAgent` kernel connects that workspace to an agent's private mRAG belief store. The prompt path can add task-relevant retrieved memories before calling the model. A separate compatibility `AgentBeliefStore` persists a compact office snapshot under `comms/`; that shared snapshot is distinct from the categorized mRAG data. [[OfficeAgent](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/office_agent.py>)] [[belief snapshot store](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag_beliefs.py>)]

`BeliefStore` persists eight JSON category files, including raw conversation memory and structured premises, propositions, preferences, people, skills, concepts, and desires. Records carry IDs, content, confidence, source text, timestamps, access and verification counts, stability, relations, memory references, and derived tags/relevance. On load it builds an in-memory belief cache plus reverse-relation and phrasing-template indexes. [[belief store](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/memory/belief_store.py>)]

The raw ingestion path chunks text at a target of roughly 100 tokens and stores source/session/turn metadata with deterministic event/chunk identifiers; the module describes ingestion as LLM-free. Consolidation later turns raw chunks into structured beliefs. Optional vector adapters index embeddings for similarity retrieval, while JSON category files remain the belief store's durable representation. [[memory ingestor](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/memory_ingestor.py>)] [[consolidator](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/belief_consolidator.py>)] [[vector backends](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/vector_store.py>)]

## Write, update, delete, and retrieval

**Write.** `add_belief` rejects a duplicate ID in its category, timestamps and normalizes a new row, and writes the category JSON. Raw conversation events are chunked into the `memory` category with source and session/turn metadata. The README also describes redacting completed work and errors before storing experiences, then periodically reflecting over recent experiences. [[belief store](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/memory/belief_store.py>)] [[memory ingestor](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/memory_ingestor.py>)] [[OfficeAgent](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/office_agent.py>)] [[README](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/README.md>)]

**Update and correction.** `merge_or_add_belief` checks ID, a same-template salient-value contradiction, and optionally a same-category vector match. A contradiction can replace the current text, save one prior text in `previous_content`, reset verification count and confidence to the new input, and lower stability. A corroborating restatement raises confidence and verification count. This is a mutable record with a single previous-content field, rather than an append-only revision history. [[belief store](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/memory/belief_store.py>)]

**Delete.** `remove_belief` removes a matching row from the loaded cache and relation/template indexes, filters it from the category JSON, and increments the store version. The reviewed method does not call a vector-backend deletion operation. The retrieval path only accepts returned vector IDs present in the belief cache, but code inspection cannot establish erasure from persistent vector indexes, backups, or other copies. [[belief store](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/memory/belief_store.py>)][[retrieval](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/pre_generative_injection.py>)][[vector backends](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/vector_store.py>)]

**Retrieval.** Before prompt generation, the injector synchronizes its index, extracts up to four query keywords/phrases, scores category-allowed beliefs by keyword and conceptual-tag overlap, and unions those candidates with vector top-k results. It fuses cosine similarity and lexical/tag signals, prioritizes exact lexicon matches, suppresses some synthesis duplicates, removes near duplicates, and selects memories within a token budget. Search-head and top-k limits bound parts of the retrieval work; context can reserve space for adjacent raw-memory turns. These are source-visible mechanisms, not measured retrieval quality or latency. [[OfficeAgent](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/office_agent.py>)][[retrieval](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/pre_generative_injection.py>)][[vector backends](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/vector_store.py>)]

**Consolidation.** A later review can use an LLM to derive structured beliefs from raw memory chunks and link those beliefs back to their source memory IDs. Confidence decay and pruning skip the raw `memory` category. The inspected source does not establish that all raw chunks are reviewed or that derived beliefs are correct. [[consolidator](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/belief_consolidator.py>)][[belief store](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/memory/belief_store.py>)][[memory ingestor](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/memory_ingestor.py>)]

## Scope isolation, provenance, and evidence

The application places agent workspaces and mRAG stores by agent name. The README describes the public beta as single-operator and says it does not provide multi-user roles or tenant isolation. This supports a per-agent data layout, not an independently verified access-control boundary between hostile agents, users, or tenants; no isolation probes were run. [[OfficeAgent](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/office_agent.py>)][[README](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/README.md>)][[security policy](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/SECURITY.md>)]

Belief source strings, memory references, timestamps, and raw event IDs preserve origin/lineage. They do not by themselves verify a fact or provide external citations that support each generated claim. [[belief store](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/memory/belief_store.py>)][[memory ingestor](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/memory_ingestor.py>)]

## Source-visible efficiency and observability

Raw ingestion chunks and persists text without an LLM call. Retrieval uses a loaded in-memory belief set, limits keyword extraction and parts of parallel search, and applies a token ceiling when assembling context. Optional Chroma/Pinecone-style adapters can add embedding work and distinct storage/network boundaries. These implementation details are not measured time, throughput, memory, token, or cost results. [[memory ingestor](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/memory_ingestor.py>)][[belief store](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/memory/belief_store.py>)][[retrieval](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/pre_generative_injection.py>)][[vector backends](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/vector_store.py>)]

## Metric-domain evidence

All comparison metrics are **not measured** for AIMAOS. Source inspection identifies retrieval and abstention paths, mutable correction behavior, a category-file delete method, per-agent stores, provenance fields, and a token-budgeted prompt injection path. No answerable/abstention probes, correction or deletion adjudication, scope probes, evidence review, latency sample, write-to-recall schedule, token/cost accounting, or storage measurement was collected. See the project metric definitions, fixture, and execution-status record for the separate protocol. [[metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This bounded source review does not establish runtime reliability, retrieval quality, stale-value rate, deletion completeness, or adversarial isolation. Per-agent workspace naming and local JSON persistence do not prove tenant isolation. The reviewed delete path does not establish cleanup across vector indexes or backups. Source and memory-reference fields describe lineage, not claim-level evidence correctness. Corpus-specific performance and resource use remain unknown without measurements. [[README](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/README.md>)][[security policy](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/SECURITY.md>)][[belief store](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/memory/belief_store.py>)][[retrieval](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/pre_generative_injection.py>)]]

## Contact-list follow-up

I checked the official pinned README and SECURITY.md for a published contact email. Neither page published one, so the JSON record stores `contact_email: null` with the exact checked SECURITY.md URL and both checked official source URLs. No commit metadata, personal profile email, third-party directory, or inferred address was used. [[README](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/README.md>)][[SECURITY.md](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/SECURITY.md>)]

## Benchmark status

**Benchmark not run.** No AIMAOS runtime, benchmark workload, or tests were executed. The local metrics document, fixture, and run-status record are protocol/status references, not AIMAOS findings. [[metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Canonical repository and default branch](https://github.com/munch2u-a11y/AIMAOS)
- [Current main commits feed](https://github.com/munch2u-a11y/AIMAOS/commits/main.atom)
- [Reviewed full head](https://github.com/munch2u-a11y/AIMAOS/commit/0d8c58c2bee5addc72a13c5c95839635d809b5b0)
- [README.md](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/README.md>)
- [SECURITY.md](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/SECURITY.md>)
- [core/office_agent.py](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/office_agent.py>)
- [core/mrag_beliefs.py](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag_beliefs.py>)
- [core/mrag/memory/belief_store.py](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/memory/belief_store.py>)
- [core/mrag/core/memory_ingestor.py](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/memory_ingestor.py>)
- [core/mrag/core/pre_generative_injection.py](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/pre_generative_injection.py>)
- [core/mrag/core/vector_store.py](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/vector_store.py>)
- [core/mrag/core/belief_consolidator.py](<https://github.com/munch2u-a11y/AIMAOS/blob/0d8c58c2bee5addc72a13c5c95839635d809b5b0/core/mrag/core/belief_consolidator.py>)
- [Project metric definitions](../METRICS.md)
- [Project fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark status](../results/initial-baselines-status.json)
- [Curated roster locator and attribution](../data/memory-systems.json)

**Verification boundary:** source observations above are from the pinned SHA; no runtime, benchmark, or tests were run.
