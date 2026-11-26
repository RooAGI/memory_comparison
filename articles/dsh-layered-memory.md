# dsh-layered-memory

## Identity and review pin

- Catalog ordinal: 200
- System name: `dsh-layered-memory`
- Slug: `dsh-layered-memory`
- Listed repository: https://github.com/JunNanLYS/dsh-layered-memory
- Roster attribution: the explicit catalog locator is recorded, and the pinned Atlas entry is used only for curated identity and locator context, not as assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-layered-memory.md)).
- Canonical upstream: https://github.com/JunNanLYS/dsh-layered-memory
- Default branch: `main`
- Reviewed full head: [69028fbee43e9950fffecc578430909fc827527e](https://github.com/JunNanLYS/dsh-layered-memory/commit/69028fbee43e9950fffecc578430909fc827527e)
- Review timestamp: 2026-11-25T11:39:02Z (UTC; 2026-11-25 03:39:02 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

The official repository API identifies a public, non-fork repository with `main` as the default branch. The branch API resolves `main` to [69028fbee43e9950fffecc578430909fc827527e](https://github.com/JunNanLYS/dsh-layered-memory/commit/69028fbee43e9950fffecc578430909fc827527e), and the official main commit feed reports the same head, timestamped 2026-09-07T01:12:22Z. ([repository metadata](https://api.github.com/repos/JunNanLYS/dsh-layered-memory), [main branch](https://api.github.com/repos/JunNanLYS/dsh-layered-memory/branches/main), [main commit feed](https://github.com/JunNanLYS/dsh-layered-memory/commits/main.atom))

## Summary

dsh-layered-memory is a DeepSeek Harness plugin that captures conversation messages, distills atomic memories, and consolidates them into scene and persona summaries. It stores append-only JSONL sources beside a SQLite retrieval index, supports keyword and optional embedding search, and injects bounded recall before model steps. This is a pinned source review, not a runtime or benchmark assessment. ([README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md), [memory types](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/types.ts), [L1 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l1.ts))

## Who and what

The README presents the project as a layered long-term memory plugin for DeepSeek Harness. It describes web, TUI and headless host modes, plus a separate stdio MCP integration. GitHub metadata identifies the public repository owner as JunNanLYS; the reviewed README does not publish a contact email or name an individual maintainer. ([repository metadata](https://api.github.com/repos/JunNanLYS/dsh-layered-memory), [README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md))

## Architecture and data model

The system separates L0 conversation messages, L1 atomic memories, L2 scene documents and L3 persona summaries. L0 records retain session and message IDs, role, content and timestamps. L1 records carry content, type, family, scene, timestamps, version and source-message IDs. ([types](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/types.ts), [L0 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l0.ts), [L1 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l1.ts))

L0 and L1 use append-only daily JSONL records alongside a SQLite retrieval index. The README describes full text search and optional vector search. L2 scenes are family-specific Markdown files, while scene navigation and persona summaries can be injected as stable prompt context. ([README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md), [L0 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l0.ts), [L1 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l1.ts), [scene store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/scenes.ts))

Host capture and pre-step hooks connect to LLM extraction and deduplication, family stores, retrieval tools, a settings interface and optional embeddings. ([README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md), [L1 pipeline](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/pipeline/l1.ts), [recall hook](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/hooks/recall.ts))

## Write, update, delete, and retrieval

**Writes.** Capture appends non-off session messages to L0 JSONL and indexes them in SQLite. L1 extraction groups facts into scenes and attaches source message IDs. A second LLM decision step can store, update, merge or skip a proposed memory against same-family candidates. ([README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md), [L0 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l0.ts), [L1 pipeline](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/pipeline/l1.ts))

**Updates.** L1 update and merge decisions create a new record ID and advance the version from replaced candidates, then append the replacement and remove prior targets from SQLite. Older JSONL entries remain. ([L1 pipeline](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/pipeline/l1.ts), [L1 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l1.ts))

**Deletion.** The README documents editing and deleting memories in the settings panel. The inspected model-callable tools expose search and read operations, not a memory-delete tool. L2 scene storage unlinks a file when its write receives the `[DELETED]` marker. Since L1 JSONL is append-only and separate from the SQLite index, this inspection does not establish erasure from source logs, backups or later rebuilds. ([README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md), [memory tools](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/tools/index.ts), [scene store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/scenes.ts), [L1 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l1.ts))

**Retrieval.** L1 supports FTS5 keyword search, vector search, or hybrid search with reciprocal-rank fusion and freshness decay. The recall hook searches using recent context, limits the query to eight messages and 2,000 characters, applies a timeout, deduplicates already injected records per session and bounds injected text. A timeout skips injection rather than delaying the chat. ([L1 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l1.ts), [recall hook](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/hooks/recall.ts), [configuration](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/config.ts))

The model-callable tools are `memory_search` for L1, `conversation_search` for raw L0 and `memory_read_scene` for L2/L3. These tools can retrieve detail that was not included in automatic prompt injection. ([memory tools](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/tools/index.ts), [recall hook](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/hooks/recall.ts))

## Scope isolation

The system separates `chat` and `work` memory families. Single-family sessions filter L1 recall by family; `auto` may search both. Scene and persona stores are also divided by family. This is software-level routing, not demonstrated hard authorization: the tools fall back to unfiltered family search when the host omits caller agent ID, conversation search remains global, and scene lookup may try the other family. No deployment authorization was evaluated. ([types](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/types.ts), [memory tools](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/tools/index.ts), [recall hook](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/hooks/recall.ts), [scene store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/scenes.ts))

## Provenance and evidence

L0 retains source session and message IDs. L1 records point to source-message IDs and retain replacement history in append-only JSONL. The README also describes consolidation receipts with an input snapshot, decision details and result hash. These fields trace records to conversation messages and processing runs, but the inspected contracts do not establish independent source citations or human verification for each extracted factual claim. ([README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md), [types](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/types.ts), [L0 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l0.ts), [L1 pipeline](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/pipeline/l1.ts))

## Efficiency and observability

The recall path bounds query length, result count, injected text and execution time. Session deduplication avoids reinjecting the same records during a session. Embeddings are optional, with a local embedding option; JSONL records and SQLite indexing separate recoverable storage from retrieval. ([README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md), [recall hook](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/hooks/recall.ts), [configuration](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/config.ts), [L1 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l1.ts))

The README describes local logs, activity and recall views, and token-cost accounting grouped by provider, model and distillation layer. Extraction and consolidation still use configured host/provider LLM calls; local embeddings alone do not make all processing local. This review collected no telemetry or provider costs. ([README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md), [recall hook](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/hooks/recall.ts), [configuration](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/config.ts))

## Metric-domain evidence

All benchmark domains are **unmeasured in this review**. The README describes upstream benchmark runs, but none was reproduced or independently adjudicated here. ([README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md), [metric definitions](../METRICS.md), [fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | L0/L1 search exists; no probes were scored. |
| Correction accuracy and stale-value rate | Unmeasured | L1 replacement versions are visible; no correction workload was run. |
| Deletion leakage | Unmeasured | SQLite replacement/deletion and scene deletion were inspected; no erasure probes were run. |
| Scope isolation | Unmeasured | Family routing exists; no cross-family or cross-session workload was run. |
| Evidence support and citation coverage | Unmeasured | Source-message and run provenance exist; no claim-support adjudication was performed. |
| Retrieval latency and write-to-recall delay | Unmeasured | A recall timeout and duration counter exist; no timings were collected. |
| Tokens and cost | Unmeasured | Project accounting is described; no provider usage or charges were measured here. |
| Storage efficiency | Unmeasured | JSONL and SQLite layers are visible; no corpus-attributed size was measured. |

## Limits and unknowns

This inspection covered the pinned English README and selected current source for data types, L0/L1 storage, extraction, recall, tools, L2 scenes and configuration. It did not inspect every SQLite query, UI route, host integration, provider adapter or deployment path. Source review cannot establish extraction quality, complete erasure across source files and backups, deployed family isolation, runtime stability, real-world recall, latency, cost or storage growth. No local upstream checkout was available in the read-only worker environment. ([README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md), [types](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/types.ts), [L1 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l1.ts), [metric definitions](../METRICS.md))

The official pinned English README was checked for contact. It publishes no email; no commit/profile metadata or third-party directory was used. ([README.en.md](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md))

## Benchmark status

**Benchmark not run.** The system, tests and benchmark workload were not run. Project metric definitions, fixture and execution record are context only, not results. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

## Sources

- [Catalog entry and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-layered-memory.md)
- [Official GitHub repository metadata](https://api.github.com/repos/JunNanLYS/dsh-layered-memory)
- [Verified default-branch head](https://api.github.com/repos/JunNanLYS/dsh-layered-memory/branches/main)
- [Official main commit feed](https://github.com/JunNanLYS/dsh-layered-memory/commits/main.atom)
- [Pinned English README](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/README.en.md)
- [Pinned memory types](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/types.ts)
- [Pinned L0 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l0.ts)
- [Pinned L1 store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/l1.ts)
- [Pinned L1 extraction pipeline](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/pipeline/l1.ts)
- [Pinned recall hook](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/hooks/recall.ts)
- [Pinned model-callable memory tools](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/tools/index.ts)
- [Pinned L2 scene store](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/store/scenes.ts)
- [Pinned configuration](https://github.com/JunNanLYS/dsh-layered-memory/blob/69028fbee43e9950fffecc578430909fc827527e/src/config.ts)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution status](../results/initial-baselines-status.json)

---
