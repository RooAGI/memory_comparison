# A-MEM source review

**Review status:** Reviewed from code  
**Benchmark status:** not_run  
**Roster name / slug:** A-MEM / a-mem  
**Catalog locator:** [agiresearch/A-mem](https://github.com/agiresearch/A-mem)  
**Reviewed repository:** [agiresearch/A-mem at ceffb860f0712bbae97b184d440df62bc910ca8d](https://github.com/agiresearch/A-mem/tree/ceffb860f0712bbae97b184d440df62bc910ca8d)  
**Default branch / reviewed head:** main / ceffb860f0712bbae97b184d440df62bc910ca8d  
**Review time:** 2026-11-25 22:21:20 UTC (14:21:20 PST, America/Los_Angeles).

## Identity and scope

The catalog entry names A-MEM and lists https://github.com/agiresearch/A-mem as its repository locator. At review time, GitHub opened that locator at agiresearch/A-mem itself; no redirect to Cipher208/a-memory was observed. The earlier A-MEM record linked to Cipher208/a-memory and described a different codebase. This review uses the repository currently at the catalog locator, and keeps the roster attribution separate from the assessment.[[catalog locator](../data/memory-systems.json)] [[repository at reviewed head](https://github.com/agiresearch/A-mem/tree/ceffb860f0712bbae97b184d440df62bc910ca8d)]

## Project description

The README describes A-MEM as an agentic memory system for LLM agents. It presents structured notes, LLM-generated context and tags, ChromaDB indexing, similarity links, and memory evolution as project features. These are repository descriptions, not measured outcomes.[[README.md — project description and features](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/README.md)]

The README's usage example documents adding, reading, searching, updating, and deleting notes through AgenticMemorySystem. It also points readers to a separate WujiangXu/AgenticMemory repository to reproduce the paper's reported results; those paper results are not measurements from this implementation or from this review.[[README.md — API example and reproduction note](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/README.md)]

## Code observations

MemoryNote stores content and fields for identifiers, keywords, links, timestamps, context, category, tags, retrieval count, and evolution history. AgenticMemorySystem constructs a ChromaRetriever and an LLMController. These are source observations, not a runtime validation.[[memory_system.py — MemoryNote and AgenticMemorySystem](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/memory_system.py)]

ChromaRetriever constructs a ChromaDB client, SentenceTransformer embedding function, and collection; it exposes add-document, delete-by-ID, and search methods. The inspected path uses chromadb.Client and get_or_create_collection. This does not establish durable storage or complete deletion across all state.[[retrievers.py — ChromaRetriever](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/retrievers.py)]

## Evaluation status and limits

All project metric domains remain **unmeasured** for A-MEM: answerable recall, abstention, correction accuracy, stale values, deletion leakage, scope isolation, evidence support, citation coverage, latency, token use, cost, and storage. The project status record contains no A-MEM execution result; fixture cases are planned probes, not measurements.[[METRICS.md](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

This is a bounded, read-only source review at the pinned revision. No A-MEM system, benchmark workload, or test suite was run. Runtime correctness, reliability, quality, security, privacy, deletion completeness, and performance remain unknown.

Atlas supplied only the roster name and repository locator attribution. Its review prose, capability marks, ordering, and presentation are not used as evidence or as this project's assessment.[[catalog roster snapshot](../data/memory-systems.json)]

## Sources

- [A-MEM repository at reviewed commit](https://github.com/agiresearch/A-mem/tree/ceffb860f0712bbae97b184d440df62bc910ca8d)
- [README.md — project overview and usage](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/README.md)
- [agentic_memory/memory_system.py — notes and memory API](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/memory_system.py)
- [agentic_memory/retrievers.py — ChromaDB retrieval](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/retrievers.py)
- [agentic_memory/llm_controller.py — LLM controller](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/llm_controller.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Catalog locator attribution](../data/memory-systems.json)

**Verification boundary:** no A-MEM system, benchmark, or test suite was run for this article.
