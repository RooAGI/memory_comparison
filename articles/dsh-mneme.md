# dsh-mneme

## Identity and review pin

- Catalog ordinal: 201
- System: dsh-mneme
- Slug: `dsh-mneme`
- Listed repository: https://github.com/modusensus/dsh-mneme
- Roster attribution: explicit repository locator; the pinned Atlas entry is retained for identity and locator context only ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-mneme.md)).
- Canonical upstream: https://github.com/slow-stack/mneme (the listed URL redirects here)
- Default branch: `main`
- Reviewed full head: [9e66506deede3cc0facfb02271578fa501555e2c](https://github.com/slow-stack/mneme/commit/9e66506deede3cc0facfb02271578fa501555e2c)
- Review timestamp: 2026-11-25T11:39:01Z (UTC; 2026-11-25 03:39:01 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

dsh-mneme (Mneme) is a local-first, cross-session memory plugin for DeepSeek Harness. It stores typed memory records in SQLite with editable Markdown mirrors, summarizes conversation content, injects selected memories, and can consolidate them in background dream or sleep passes. The implementation also exposes MCP and standalone interfaces. This assessment is based on current source inspection; no runtime or benchmark results were collected. ([official README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/README.md), [package README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/README.md), [store](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js), [service](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js))

## Who and what

The official project describes Mneme as cross-session memory for DeepSeek Harness. The installable package includes plugin tools and interfaces for MCP and a standalone daemon/API; this review focuses on the memory subsystem. ([official README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/README.md), [package README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/README.md), [tool surface](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/tools.js))

The catalog's 201st position names the system `dsh-mneme`, slug `dsh-mneme`, and lists `https://github.com/modusensus/dsh-mneme` as an explicit locator. That URL redirects to the canonical public repository at `slow-stack/mneme`. The Atlas entry is roster attribution only and is not assessment evidence. ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-mneme.md), [official repository](https://github.com/slow-stack/mneme))

The official repository page identifies `main` as default. Its official main feed reports full head `9e66506deede3cc0facfb02271578fa501555e2c`, updated 2026-11-24T13:31:28Z; the page, full-SHA commit URL, read-only `git ls-remote --symref`, and shallow checkout agreed on the reviewed SHA. ([repository](https://github.com/slow-stack/mneme), [main commit feed](https://github.com/slow-stack/mneme/commits/main.atom), [head commit](https://github.com/slow-stack/mneme/commit/9e66506deede3cc0facfb02271578fa501555e2c))

## Architecture and data model

The primary data store is local SQLite. The `memories` table represents typed entries with title, content, tags, importance, forgotten/archive state, source, content history/hash, optional embedding, epistemic status, event/access timestamps, evidence and document path. The package documentation describes ten memory types and per-type Markdown mirrors; document entries are pointers to externally stored files. ([SQLite store](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js), [package README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/README.md), [mirror implementation](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/mirror.js))

The documented lifecycle connects explicit `memory_save` and session-end summarization to SQLite and Markdown, then retrieval/injection and optional background consolidation. Source modules divide storage, service orchestration, tool APIs, scope resolution, summarization, and dream decisions. ([package README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/README.md), [tools](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/tools.js), [service](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js), [summarization](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/summarize.js), [dream decisions](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/dream/decisions.js))

The Markdown mirror is human-readable and editable. Edits to entry titles or content can be reconciled with human changes taking precedence; a generation/applied-generation state tracks synchronization debt so it can be recovered after interruption. The document mirror is a read-only pointer view rather than an editable round-trip. ([mirror implementation](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/mirror.js), [store schema](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js), [package README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/README.md))

Agent and workspace labels are stored with memories and participate in same-title deduplication. Scope resolution uses the session's agent preset and workspace registry/path. When configured, `strictScope` filters records outside the caller's resolved scope. The effective boundary depends on configuration and identity availability. ([scope resolver](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/scope.js), [retrieval and dedupe](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js), [tools](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/tools.js))

## Write, update, delete, and retrieval

**Write.** The model can call `memory_save`; session lifecycle hooks also distill conversation content into typed memory. Same-title entries merge only when type, agent scope, workspace scope, and sensitivity match. A merge appends content and updates content history; a new entry can also be rejected by configured admission checks. Session-derived memories can be linked to source session sequence ranges. ([tool API](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/tools.js), [save and deduplication](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js), [session distillation](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/summarize.js), [provenance tables](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js))

**Update and consolidation.** `memory_update` applies an ID-targeted patch to supported fields. The service preserves content history, may record the prior and corrected values when reflection tracking is enabled, and audits explicit scope changes. Dream/sleep consolidation supports keep, merge, update, archive, create, supersede, and conflict handling subject to policy. Decision runs record a snapshot digest, decision list, per-ID outcomes, and receipt; this supports inspection/replay but does not verify correctness. ([update tool](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/tools.js), [update service](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js), [decision validation](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/dream/decisions.js), [audit schema](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js))

**Delete.** `memory_forget` suppresses a memory from injection, search and lists while retaining it; `memory_archive` hides it and supports restoration. `memory_delete` permanently removes the row and explicitly clears memory provenance, mint, and pin side rows in a transaction. This source path does not establish erasure from external backups or copies outside the store. ([forget/archive/delete tools](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/tools.js), [transactional removal](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js), [package README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/README.md))

**Retrieval.** Search modes include auto, keyword, vector and hybrid. The service combines literal text matching, BM25 token recall, optional vector similarity and optionally entity-linked recall; it fuses candidate lists, applies scope filtering/ranking, optional semantic deduplication and reranking, then returns a bounded result set. When recall recording is enabled, the returned candidates and scores can be written to `recall_runs`. Automatic context injection is a separate bounded selection path. ([search tool](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/tools.js), [search pipeline](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js), [recall audit schema](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js), [semantic-search design](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/docs/SEMANTIC.md), [package README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/README.md))

The semantic-search docs describe local, Ollama and OpenAI-compatible embedding backends. If an embedder is absent or fails, source code retains keyword results or falls back to keyword retrieval; optional reranking depends on configuration. These are code paths, not verified runtime outcomes. ([semantic-search documentation](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/docs/SEMANTIC.md), [retrieval fallback](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js))

## Scope isolation

Records can carry agent and workspace labels, and scope participates in deduplication. Scope-aware ranking and strict filtering are separate controls; strict behavior is configuration-dependent. Unlabelled records and calls where scope identity cannot be resolved require careful treatment, so the inspected design alone does not establish a deployment-level tenant boundary. No cross-scope probes were run. ([scope resolver](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/scope.js), [scope gates](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js), [tool visibility checks](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/tools.js))

## Provenance and evidence

The schema supports an optional source string, evidence, content history, hashes, epistemic status, and links from a memory to a session plus sequence range. Dream runs retain inputs, decisions, outcomes and receipts; recall runs can retain the retrieved candidates. This provides source and process traces, but the selected sources do not establish universal claim-level citation coverage or the truth of a memory. ([schema and audit tables](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js), [distillation provenance](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/summarize.js), [recall receipts](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js))

## Efficiency and observability

Source-visible controls include SQLite indexes, bounded retrieval, asynchronous embedding/summarization paths, optional local embeddings and reranking, and configurable background consolidation. Mirror health and local audit records make some persistence and retrieval activity inspectable. LLM audit rows can retain operation timing, token counts and cost where available; this review collected no usage, latency, cost or storage measurements. ([SQLite schema](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js), [service pipeline](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js), [semantic-search design](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/docs/SEMANTIC.md), [official README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/README.md))

## Metric-domain evidence

All project benchmark domains are **unmeasured**. The project metric definitions and fixture were referenced but not executed. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | No fixture questions or outcomes were run. |
| Correction accuracy and stale-value rate | Unmeasured | Update and consolidation paths exist; no correction probes were adjudicated. |
| Deletion leakage | Unmeasured | A direct deletion path exists; no post-delete probes were run. |
| Scope isolation | Unmeasured | Scope labels and filters exist; no allowed/forbidden probe pairs were run. |
| Evidence support and citation coverage | Unmeasured | Provenance links exist; no generated claims were adjudicated. |
| Retrieval latency | Unmeasured | No samples collected. |
| Write-to-recall delay | Unmeasured | No timed probes run. |
| Tokens and cost | Unmeasured | No fixture usage or charge measurements collected. |
| Storage efficiency | Unmeasured | No corpus-attributed byte measurement collected. |

## Limits and unknowns

This selected review inspected the official root and package READMEs, SQLite store, service, tools, scope resolver, summarization, dream decision validation, Markdown mirror, and semantic-search documentation at the verified head. It did not trace every host integration, migration, external API authorization path, or consolidation scheduler. ([README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/README.md), [package README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/README.md), [store](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js), [service](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js), [tools](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/tools.js), [scope](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/scope.js), [summarization](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/summarize.js), [dream decisions](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/dream/decisions.js), [mirror](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/mirror.js), [semantic docs](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/docs/SEMANTIC.md))

LLM-based summarization and consolidation can change or omit details. Audit receipts make decisions inspectable, not necessarily correct. The source review does not establish runtime quality, completeness of deletion, isolation guarantees, backup behavior, index recovery, large-corpus performance, or concurrent write outcomes. ([summarization](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/summarize.js), [dream decisions](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/dream/decisions.js), [service](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js), [store](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js), [metric definitions](../METRICS.md))

## Contact

The official `SECURITY.md` publishes `work@modusensus.space` for vulnerability reports. The root README and installable package README were also checked. The pinned policy source is [SECURITY.md](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/SECURITY.md); no commit/profile metadata or third-party directory was used.

## Benchmark status

**Benchmark not run.** No dsh-mneme runtime, tests, or benchmarks were run. Source observations and documentation are not benchmark results. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

## Sources

- [Curated roster identity, listed locator and ordinal](../data/memory-systems.json)
- [Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-mneme.md) (roster attribution only)
- [Canonical official GitHub repository](https://github.com/slow-stack/mneme)
- [Official main commit feed](https://github.com/slow-stack/mneme/commits/main.atom)
- [Reviewed current upstream head](https://github.com/slow-stack/mneme/commit/9e66506deede3cc0facfb02271578fa501555e2c)
- [Official repository README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/README.md)
- [Installable dsh-mneme package README](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/README.md)
- [Official security policy](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/SECURITY.md)
- [SQLite schema and store implementation](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/store.js)
- [Memory service and retrieval pipeline](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/service.js)
- [Memory tool API and lifecycle operations](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/tools.js)
- [Agent/workspace scope resolution](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/scope.js)
- [Conversation distillation write path](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/summarize.js)
- [Dream and sleep consolidation decisions](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/dream/decisions.js)
- [Editable Markdown mirror](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/src/mirror.js)
- [Semantic search design and documentation](https://github.com/slow-stack/mneme/blob/9e66506deede3cc0facfb02271578fa501555e2c/dsh-mneme/docs/SEMANTIC.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution status record](../results/initial-baselines-status.json)
