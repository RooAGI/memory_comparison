# Flowly source and design review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 244 / Flowly / `flowly`  
**Listed repository locator:** [Nocetic/flowly](https://github.com/Nocetic/flowly)  
**Canonical upstream:** [Nocetic/flowly](https://github.com/Nocetic/flowly)  
**Default branch / reviewed head:** main / [05efe13436db77adffb888795d8dd47f9a87d19a](https://github.com/Nocetic/flowly/commit/05efe13436db77adffb888795d8dd47f9a87d19a)  
**Review time:** 2026-11-25 20:36:57 UTC (2026-11-25 12:36:57 PST; America/Los_Angeles).

## Identity and review pin

The catalog identifies Flowly as ordinal 244, slug `flowly`, with an explicit locator at Nocetic/flowly and a pinned Atlas attribution. The Atlas record is used only to identify the curated entry and locator; its descriptions and capability assessments are not evidence below. The official repository page identifies `main` as the default branch and links latest commit `05efe13`; the official patch for that commit gives full SHA `05efe13436db77adffb888795d8dd47f9a87d19a`. Source inspection is pinned to that SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Flowly is a self-hosted personal agent with layered memory: workspace Markdown notes, a SQLite-backed chunk search index, a temporal knowledge graph, and a separate SQLite governance store for confidence, privacy, lifecycle and audit metadata. The reviewed code combines keyword retrieval with optional embeddings and background consolidation; these source observations do not establish retrieval quality or isolation.[[readme]][[governance]][[manager]][[kg]][[indexer]]

## Who and what

The official repository describes Flowly as a personal AI agent that runs on the operator's machine and provides shared memory across terminal and messaging surfaces. The inspected memory code is a subsystem of the broader Python agent rather than a standalone memory service. This review does not infer individual maintainer identity.[[readme]][[repo]][[governance]][[manager]]

## Architecture and data model

The memory design has multiple stores. Free-form notes live in workspace `MEMORY.md` and dated notes; structured facts live in a SQLite temporal knowledge graph; lifecycle metadata and references live in `memory_governance.sqlite3` under the state directory; and a workspace-specific SQLite index stores searchable chunks and optional embedding vectors. Governance items reference graph triples, memory-file anchors, inline text, or imported Obsidian notes instead of replacing those engines.[[governance]][[kg]][[manager]][[indexer]]

The graph stores entities, aliases and triples with subject, predicate, object, validity dates, confidence, source and extraction timestamp. The search index tracks files and chunk line ranges, hashes, text, optional JSON-encoded embeddings and FTS5 rows. The manager defaults to 400-token chunks with 80-token overlap and a maximum of six results; these are configuration defaults, not measured operating characteristics.[[kg]][[indexer]][[manager]]

## Write, update, delete, and retrieval

**Write paths.** The README describes live memory tools, a background dreamer that extracts across sessions, and a consolidation pass. The governance coordinator's `post_tool_call` hook mirrors successful `memory_append` and `knowledge_graph` operations into governance; the governance store therefore wraps the primary memory engines, and this hook runs after a successful tool call. The dreamer uses a watermark and single-writer lock, retries extraction failures without advancing the watermark, and commits candidates through the governance state machine.[[readme]][[coordinator]][[governance]][[dreamer]]

**Trust and review.** Governance records candidate, active, needs_review, stale, superseded and rejected states with enforced transitions, confidence, privacy level and an append-only transition audit. Consolidation lets an LLM propose merge, supersede or stale operations, then validates and applies them in code. The coordinator excludes secret items from recall and generated `MEMORY.md` content; sensitive items require explicit inclusion in recall. These controls govern their respective paths and do not show that every primary write is withheld pending review.[[governance]][[coordinator]][[summary]][[consolidate]]

**Update and correction.** User-facing lifecycle actions include accepting, rejecting, correcting and undoing memories. Consolidation can supersede redundant items, mark outdated items stale, and merge duplicates by superseding one item into another. A superseded graph fact can have its validity closed and can be restored by undo. These mechanisms preserve lifecycle state and audit transitions, rather than demonstrating one immutable version history for every edit.[[readme]][[coordinator]][[governance]][[consolidate]][[kg]]

**Delete.** The inspected governance state model has no delete transition and treats rejection as terminal; consolidation operations also explicitly avoid deleting items. The graph has temporal invalidation and retains triples with validity fields. I did not find a hard-erasure path in these inspected lifecycle and graph sources. This is limited to the inspected APIs and does not establish that no other product or manual filesystem deletion route exists.[[governance]][[consolidate]][[kg]][[readme]]

**Retrieval.** The agent's `memory_recall` path reads active governed items and applies privacy rules; the graph provides entity, relationship and as-of queries. The separate workspace search manager lazily syncs Markdown files and retrieves text through FTS5 plus optional vector embeddings, with a hybrid result path. If no embedding provider is configured, the manager reports keyword-only search. These paths are distinct; the reviewed sources do not establish one universal ranking or answer-generation policy across them.[[coordinator]][[summary]][[kg]][[manager]][[indexer]][[search]][[embeddings]]

## Scope isolation

The index manager is created for a workspace and searches Markdown beneath that workspace's `memory/` directory; governance is stored separately beneath a state directory. This indicates filesystem/configuration scope in the inspected implementation. I found no basis here for claiming an authorization boundary or verified cross-profile isolation, and no adversarial scope test was run.[[manager]][[governance]][[readme]][[metrics]]

## Provenance and evidence

Governance rows carry source-session and message provenance, reference kind/id, confidence, privacy level and status; graph triples carry source labels and extraction time alongside validity dates. The dreamer preserves a watermark and routes extracted candidates through governance. These are lineage and lifecycle fields, not proof that an extracted fact or generated answer is true or supported by its source. No output evidence was adjudicated in this review.[[governance]][[kg]][[dreamer]][[metrics]]

## Efficiency and observability

The index is local SQLite with FTS5 and optional vector embeddings. It tracks file hashes and modification times, lazily syncs on search with a one-second debounce, and removes index rows when source Markdown files disappear. The manager serializes sync and embedding work with async locks; the coordinator coalesces generated summary refreshes until turn end to avoid repeated prompt-cache invalidation. SQLite WAL and the in-process governance writer are implementation choices, not measured performance results. No latency, resource, token or cost data was collected.[[indexer]][[manager]][[coordinator]][[governance]][[embeddings]][[metrics]]

## Metric-domain evidence

All benchmark domains are **unmeasured in this review**. Code structure and upstream documentation are not measurements performed here. Flowly, its tests and benchmarks were not run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Recall, graph query and hybrid search paths were inspected; no query set or abstention workload was scored. | Unmeasured |
| Correction accuracy and stale values | Correction, undo, supersession and stale paths were inspected; no correction workload was run. | Unmeasured |
| Deletion leakage | Lifecycle rejection and graph invalidation were inspected; no erase or post-delete probe was run. | Unmeasured |
| Scope isolation | Workspace/state-directory organization was inspected; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Provenance fields exist; generated claims and answers were not adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Lazy indexing behavior was inspected; no runtime timings were collected. | Unmeasured |
| Tokens, cost and storage | Chunking, SQLite and optional embeddings were inspected; no workload resource measurements were collected. | Unmeasured |

## Limits and unknowns

This is a pinned source review, not a runtime, security or quality assessment. Behavior depends on tool wiring, workspace/state configuration and optional embedding providers. Governance and underlying content are separate layers, and the post-tool hook mirrors successful primary writes into governance. Status filtering on governed recall should not be read as proof that unreviewed content is absent from every prompt or storage path. Workspace organization is not an adversarial isolation test.[[readme]][[governance]][[coordinator]][[summary]][[manager]][[embeddings]]

The inspected code shows provenance references, not an evidence guarantee. Graph invalidation and lifecycle status changes do not establish physical erasure from all files, backups or derived copies. This review did not measure support precision, citation coverage, stale-value rates, deletion leakage, isolation, latency, cost or storage efficiency.[[governance]][[kg]][[metrics]][[status]]

## Benchmark status

**Benchmark not run.** No Flowly runtime, tests or benchmark workload was executed for this review. No quality, latency, token, cost, storage, deletion, correction or isolation result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned `SECURITY.md` directs private vulnerability reports to `contact@nocetic.com`; that email and exact source URL are recorded in the JSON. No commit/profile metadata or third-party directory was used.[[security]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas record is included solely as roster attribution, not system assessment evidence. See the structured record [flowly.json](../data/system-reviews/flowly.json) and [curated roster](../data/memory-systems.json).
