# ClawMem

## Identity and review pin

- **System:** ClawMem
- **Curated position:** 128
- **Slug:** `clawmem`
- **Listed repository:** [yoloshii/clawmem](https://github.com/yoloshii/clawmem)
- **Canonical repository at review:** [yoloshii/clawmem](https://github.com/yoloshii/clawmem)
- **Default branch:** `main`
- **Reviewed head:** [`3c23948c306fcbca44fba6f3ba671944977c7140`](https://github.com/yoloshii/clawmem/commit/3c23948c306fcbca44fba6f3ba671944977c7140)
- **Reviewed:** 2026-11-25 08:14:44 UTC (2026-11-25 00:14:44 PST; America/Los_Angeles)
- **Review status:** Reviewed from current source and documentation
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/clawmem.md), used for roster identity and locator attribution only.

The catalog places ClawMem at position 128 with slug `clawmem`, listed repository `yoloshii/clawmem`, and the pinned Atlas attribution above.[[catalog]][[atlas]] GitHub identifies `main` as the default branch; its official commits feed reported full head `3c23948c306fcbca44fba6f3ba671944977c7140` at 2026-11-25T08:05:13Z, and the shallow checkout resolved to the same SHA.[[repo]][[head]][[revision]] The review timestamp records the time of source inspection: 2026-11-25T08:14:44Z (UTC; 2026-11-25 00:14:44 PST, America/Los_Angeles).

## Summary

ClawMem is a local-first memory layer for coding and assistant agents. It indexes Markdown into a SQLite vault and connects retrieval, session capture, and maintenance through hooks, MCP tools, and agent plugins. Its retrieval paths include keyword, vector, hybrid, temporal, entity, and causal search; its lifecycle model uses deactivation and reversible archival. This is a source-based review, not a runtime evaluation.[[readme]][[store]][[mcp]]

## Architecture and data model

The store separates document metadata from content. A document is identified by collection and path and points to a content-addressed body; metadata includes title, creation/modification and authored timestamps, content type, domain, workstream, tags, confidence, access counts, origin, active state, invalidation, and lifecycle fields. FTS5 supports lexical search, while content vectors and optional sqlite-vec support semantic retrieval. Related tables represent memory relations, entity mentions and triples, causal and temporal structures, and session/usage information.[[store]][[readme]]

A local SQLite file is the vault boundary. The default setup uses one vault; named vaults can point to separate database files, and tools may select a configured vault. Collections divide material within a vault. Generated observations, handoffs, and deductions use the internal `_clawmem` collection, which several general retrieval tools exclude by default; some intent, timeline, and entity routes intentionally use internal memory.[[readme]][[mcp]]

ClawMem integrates with Claude Code hooks, MCP clients, OpenClaw, and Hermes. The README describes automatic prompt-time context surfacing and session capture alongside direct retrieval and lifecycle tools. This review did not measure whether every integration captures or retrieves every eligible event.[[readme]][[context]]

## Write, update, delete, and retrieval

**Writing and updates.** The filesystem indexer maps files to collection/path document rows, stores bodies separately, updates changed content, and reconciles missing files after collection scans. Additional paths import conversation exports, accept agent/MCP writes, and generate structured session observations and handoffs. Optional enrichment can extract entities, links, and metadata. Imported conversation history can retain authored time so ranking and temporal queries can reflect when a memory was written rather than when it was imported.[[indexer]][[store]][[readme]]

**Correction and deletion.** Changed file content updates the stored document. The current lifecycle contract forgets a match by deactivating it, and lifecycle sweeps archive stale documents; archived rows can be restored. The current README and code describe no physical document-row deletion operation. Contradiction handling can reduce confidence or invalidate eligible observation rows, but it is gated by configuration and is not equivalent to a general hard-delete API.[[mcp]][[store]][[readme]]

**Retrieval.** ClawMem exposes BM25 keyword search, semantic vector search, hybrid query with reciprocal-rank fusion and optional reranking, intent-aware graph/causal search, timeline, entity-triple queries, and auto-routing through `memory_retrieve`. Hook context surfacing combines retrieval lanes, applies gating and relevance admission, and bounds the context payload. Collection/date eligibility and internal-collection visibility vary by route, so the MCP tools do not share one identical filter contract.[[readme]][[mcp]][[store]][[causal]][[context]]

## Scope isolation

Named vaults provide separate SQLite files when configured; collections and query filters provide organization inside a vault. These are useful operational boundaries, but the reviewed docs and source do not establish per-user authorization for multiple principals sharing a vault. The security policy describes local data storage, while the REST server uses a bearer token and request-origin/host checks.[[readme]][[security]][[mcp]]

## Provenance and evidence

Document collection/path, origin, timestamps, authorship time, and content type provide some lineage. Entity triples may retain source document and fact evidence; causal and judge audit rows include run metadata, prompt/response hashes, outcomes, and mutation events. However, the document model does not require a source URL, quoted evidence span, author/trust label, or independent adjudication for every memory. Provenance depth therefore depends on the write path and memory type.[[store]][[indexer]][[audit]][[readme]]

## Efficiency and observability

Source-described efficiency mechanisms include SQLite FTS/vector indexes, cached work, candidate limits, bounded graph traversal, background-work caps, hook context budgets, and optional local inference. Operators have status and doctor checks, lifecycle and recall statistics, retrieval diagnostics, audit tables, and logs. Optional remote embedding, reranking, or judge services add network and credential dependencies and may receive queries or content snippets. These are implementation and documentation claims; this review collected no latency, token, cost, or storage measurements.[[readme]][[store]][[mcp]][[security]]

## Metric-domain evidence

All benchmark domains are **unmeasured in this review**. The project metric definitions and fixture describe evaluation methods, not ClawMem results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Multiple retrieval paths and context gates are present; no answerability workload was run. | Unmeasured |
| Correction accuracy and stale-value rate | Update, contradiction, confidence, and invalidation paths exist; no correction sequence was scored. | Unmeasured |
| Deletion leakage | Forget and archive deactivate rows; no post-forget residual or backup probe was run. | Unmeasured |
| Scope isolation | Named vaults and collection filters are documented; no cross-principal workload was run. | Unmeasured |
| Evidence support and citation coverage | Some structured provenance is recorded; no claims were adjudicated against stored evidence. | Unmeasured |
| Retrieval latency and write-to-recall delay | Retrieval and write paths are source-visible; no timing data were collected. | Unmeasured |
| Tokens, cost, and storage | Local and optional remote components are documented; no resource measurements were collected. | Unmeasured |

The [project metrics](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) provide definitions and project-wide status only.[[metrics]][[fixture]][[status]]

## Limitations and unknowns

This review covers the pinned README, store, indexer, MCP implementation, causal retrieval, context surfacing, and security policy. It did not execute ClawMem, its tests, or any benchmark and did not inspect every provider, integration, migration, and worker in depth.[[revision]][[readme]][[store]][[indexer]][[mcp]][[causal]][[context]]

Forgetting and archival are reversible lifecycle states that retain document rows; the reviewed sources do not establish secure erasure from SQLite pages, backups, or copied vault files. Configured named vaults can separate database files, but shared-vault authorization was not established. Retrieval depends on the corpus, route, classifier, gates, and configured models. Optional remote services also create data-egress considerations. Independent quality, reliability, and resource measurements remain unknown.[[readme]][[store]][[mcp]][[security]][[metrics]]

## Benchmark status

**Benchmark not run.** I did not execute ClawMem, tests, or benchmark workloads. No runtime quality, latency, token, cost, storage, correction, deletion, or scope-isolation result is claimed.[[metrics]][[fixture]][[status]]

## Contact

The official pinned [SECURITY.md](https://github.com/yoloshii/clawmem/blob/3c23948c306fcbca44fba6f3ba671944977c7140/SECURITY.md) lists `sciros@lazyvibecoder.com` for vulnerability reports. The official pinned [README.md](https://github.com/yoloshii/clawmem/blob/3c23948c306fcbca44fba6f3ba671944977c7140/README.md) was also checked for a contact email; it did not publish one. This contact comes from project documentation, not commit or profile metadata.[[security]][[readme]]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed repository and Atlas attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/clawmem.md) — attribution only.
- [Official repository](https://github.com/yoloshii/clawmem) — canonical repository and default branch.
- [Official main commits feed](https://github.com/yoloshii/clawmem/commits/main.atom) — current full SHA and feed update time observed during review.
- [Reviewed head](https://github.com/yoloshii/clawmem/commit/3c23948c306fcbca44fba6f3ba671944977c7140)
- [README](https://github.com/yoloshii/clawmem/blob/3c23948c306fcbca44fba6f3ba671944977c7140/README.md)
- [SQLite store](https://github.com/yoloshii/clawmem/blob/3c23948c306fcbca44fba6f3ba671944977c7140/src/store.ts)
- [Filesystem indexer](https://github.com/yoloshii/clawmem/blob/3c23948c306fcbca44fba6f3ba671944977c7140/src/indexer.ts)
- [MCP server](https://github.com/yoloshii/clawmem/blob/3c23948c306fcbca44fba6f3ba671944977c7140/src/mcp.ts)
- [Causal retrieval](https://github.com/yoloshii/clawmem/blob/3c23948c306fcbca44fba6f3ba671944977c7140/src/causal-retrieval.ts)
- [Context surfacing hook](https://github.com/yoloshii/clawmem/blob/3c23948c306fcbca44fba6f3ba671944977c7140/src/hooks/context-surfacing.ts)
- [Security policy](https://github.com/yoloshii/clawmem/blob/3c23948c306fcbca44fba6f3ba671944977c7140/SECURITY.md) — project contact and security architecture.
- [Project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial status](../results/initial-baselines-status.json) — evaluation definitions/status only.

**Verification boundary:** Read-only source and documentation review; no ClawMem runtime, tests, or benchmarks.
