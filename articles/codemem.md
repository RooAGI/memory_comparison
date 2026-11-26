# codemem — source review

**Review status:** Reviewed from source at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 132 — codemem / `codemem`  
**Listed repository:** [kunickiaj/codemem](https://github.com/kunickiaj/codemem)  
**Canonical upstream:** same repository; default branch `main`; reviewed head [`a76ce405b5014e8ed0d2d3e956a2c770d75305cb`](https://github.com/kunickiaj/codemem/commit/a76ce405b5014e8ed0d2d3e956a2c770d75305cb)  
**Review time:** 2026-11-25 08:24:16 UTC (2026-11-25 00:24:16 PST; America/Los_Angeles)  
**Roster attribution:** [pinned Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/codemem.md), used only to identify the curated entry and listed locator.

## Identity and review pin

The local roster places codemem at ordinal 132, slug `codemem`, with the explicit listed locator above. The Atlas attribution is roster context only; its system descriptions and capability claims were not used as assessment evidence.[[catalog]][[atlas]]

GitHub’s official repository page identifies `main` as the default branch. The official main commits feed reports full head `a76ce405b5014e8ed0d2d3e956a2c770d75305cb`, updated 2026-11-25T08:03:39Z. Review time is 2026-11-25T08:24:16Z (UTC; 2026-11-25 00:24:16 PST, America/Los_Angeles).[[repo]][[head]][[revision]]

## Summary

codemem is persistent coding-agent memory across sessions and devices. Host plugins and hooks capture activity for an observer pipeline, while SQLite stores typed memories and FTS5/vector indexes support retrieval. Automatic context injection and explicit MCP/native tools expose recall. Projects, visibility and device identity govern filtering and optional sharing. The README notes that observer context is sent to the configured model and may incur cost; “local-first” storage does not mean all processing remains local.[[readme]][[store]][[search]]

## Architecture and data model

The primary store is local SQLite using better-sqlite3 and a versioned schema. Memory records include fields for kind, title/subtitle, body, confidence, tags, visibility, workspace kind, origin, trust state, narrative/facts/concepts, file references, session and prompt identifiers, project, active/deleted state, and metadata. FTS5 provides lexical search; sqlite-vec provides a semantic retrieval path.[[db]][[store]][[readme]]

The shared memory-kind catalog accepts discovery, change, feature, bugfix, refactor, decision, and exploration; the store also accepts observer-written session summaries. OpenCode, Claude Code, Codex, Pi, MCP, and a local Viewer provide automatic and explicit integration surfaces.[[kinds]][[readme]]

Projects represent repository/workspace context. Visibility and workspace kinds distinguish private/personal from shareable material; actor/device ownership and visible scopes participate in search filtering. Optional peer sync, device sharing and Teams extend selected project memory across devices.[[readme]][[search]]

## Write, update, delete, and retrieval

**Writes.** Host adapters capture conversations, tool activity, and session events. A queue-first path has the local Viewer accept raw event envelopes before SQLite ingestion; when unavailable, hooks can retain envelopes in a local spool. Observer processing converts captured context into typed memories. Explicit memory tools accept the documented kinds. Creation provenance is recorded transactionally with source identity, scope and an immutable content snapshot; inbound foreign revisions are tracked separately.[[readme]][[store]][[kinds]][[provenance]]

**Updates and deletion.** The inspected MemoryStore exposes CRUD and mutation surfaces and the record schema contains active/deleted state, but this source subset did not establish one general update or hard-delete contract across every integration. The README says removing sharing access stops future delivery, while already copied memories may remain on recipient devices. That is access revocation, not remote erasure. Physical deletion, backup erasure, and exact correction semantics require path-specific review.[[store]][[readme]][[provenance]]

**Retrieval.** Search combines FTS5/BM25 with optional semantic candidates. Pack construction fuses and deduplicates candidates, ranks them, renders context, and applies an approximate token budget; source also describes bounded scans and retrieval traces. Scoring considers factors including kind, recency, memory role and trust state. Automatic prompt injection and explicit search, pack, get, timeline and explain surfaces are documented.[[readme]][[search]][[pack]][[store]]

## Scope isolation

The search layer builds ownership context from actor and device identity, claimed peer devices and currently visible scope IDs, and enables scope enforcement for read paths. Project and caller filters further narrow results. This documents intended application-level filtering; it is not a measurement of cross-scope isolation or proof of a multi-tenant authorization boundary.[[search]][[store]]

## Provenance and evidence

Creation provenance includes an immutable snapshot of selected memory content and scope, bound to a source identity; separately recorded foreign revisions prevent that local-creation evidence from being treated as current proof after inbound changes. Memory rows also carry origin, project, prompt/session and file-context fields. These structures support lineage but do not require quote-level evidence, source citations, or verified factual support for every memory.[[provenance]][[store]]

The retrieval ledger records attempt and exposure metadata such as retrieval surface, trigger/status, candidate counts, disposition, latency, token metadata, query hash/length, filters, bounded working-set paths, score summaries and reason codes. The README says the ledger does not copy prompt or pack text, memory contents, or absolute paths. Ledger events describe retrieval and delivery; they do not establish whether a generated answer was correct.[[ledger]][[readme]]

## Efficiency and observability

Source-visible mechanisms include indexed FTS5, semantic vector search, bounded/batched candidate processing, approximate token budgets, prompt-context replay, background event ingestion, and bounded diagnostic payloads. Operators can inspect status, capture diagnostics/backlogs, memory statistics, retrieval traces and Viewer health. Optional observer models, embeddings, MCP exposure and sync introduce additional dependencies and resource or data-egress considerations.[[search]][[pack]][[ledger]][[readme]]

## Metric-domain evidence

All benchmark domains are **unmeasured**. The project metric definitions and fixture describe evaluation methods, not codemem results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Hybrid retrieval and automatic packing exist; no answerability workload was run. | Unmeasured |
| Correction accuracy and stale-value rate | Memory state and provenance structures exist; no correction sequence was probed. | Unmeasured |
| Deletion leakage | No residual-content or recipient-copy probe was run. | Unmeasured |
| Scope isolation | Actor/device/scope filters are present; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Some lineage is recorded; no claims were adjudicated against source evidence. | Unmeasured |
| Retrieval latency and write-to-recall delay | Ledger supports timing fields; no timings were collected. | Unmeasured |
| Tokens, cost, and storage efficiency | Token/usage instrumentation and provider cost documentation exist; no measurements were collected. | Unmeasured |

The [project metrics](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) are definitions and project status only.[[metrics]][[fixture]][[status]]

## Limitations and unknowns

This is a selective source review, not an exhaustive audit of every observer path, host adapter, mutation route, sync/coordinator protocol, schema migration, or deployment configuration. Source inspection cannot establish capture completeness, recall quality, trust calibration, correction behavior, deletion completeness, security, operational reliability, or resource use.[[readme]][[store]][[db]][[search]][[pack]][[provenance]][[ledger]]

The README describes optional observer processing through configured model providers and warns that remote MCP is an advanced setup and the local Viewer is not intended for public exposure. Sharing removal stops future delivery but does not erase copies already transferred. Exact permanent deletion, backup lifecycle and cross-principal authorization guarantees remain unverified here.[[readme]][[security]]

## Benchmark status

**Benchmark not run.** No codemem runtime, tests, commands, or benchmark operations were run for this review. All metric domains remain unmeasured; source observations are not benchmark outcomes.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and [SECURITY.md](https://github.com/kunickiaj/codemem/blob/a76ce405b5014e8ed0d2d3e956a2c770d75305cb/SECURITY.md) were checked for a project contact email. Neither publishes one, so the record stores `contact_email: null` with both exact checked URLs. No commit/profile metadata, third-party directory, or inferred address was used.[[readme]][[security]]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed repository and Atlas attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/codemem.md) — roster attribution only.
- [Official repository](https://github.com/kunickiaj/codemem) — repository identity and default branch.
- [Main commits feed](https://github.com/kunickiaj/codemem/commits/main.atom) — full current head and feed update time.
- [Reviewed head](https://github.com/kunickiaj/codemem/commit/a76ce405b5014e8ed0d2d3e956a2c770d75305cb)
- [README](https://github.com/kunickiaj/codemem/blob/a76ce405b5014e8ed0d2d3e956a2c770d75305cb/README.md)
- [MemoryStore](https://github.com/kunickiaj/codemem/blob/a76ce405b5014e8ed0d2d3e956a2c770d75305cb/packages/core/src/store.ts)
- [Database primitives](https://github.com/kunickiaj/codemem/blob/a76ce405b5014e8ed0d2d3e956a2c770d75305cb/packages/core/src/db.ts)
- [Memory kinds](https://github.com/kunickiaj/codemem/blob/a76ce405b5014e8ed0d2d3e956a2c770d75305cb/packages/core/src/memory-kinds.ts)
- [Search and scope](https://github.com/kunickiaj/codemem/blob/a76ce405b5014e8ed0d2d3e956a2c770d75305cb/packages/core/src/search.ts)
- [Memory pack builder](https://github.com/kunickiaj/codemem/blob/a76ce405b5014e8ed0d2d3e956a2c770d75305cb/packages/core/src/pack.ts)
- [Creation provenance](https://github.com/kunickiaj/codemem/blob/a76ce405b5014e8ed0d2d3e956a2c770d75305cb/packages/core/src/memory-creation-provenance.ts)
- [Retrieval ledger](https://github.com/kunickiaj/codemem/blob/a76ce405b5014e8ed0d2d3e956a2c770d75305cb/packages/core/src/retrieval-ledger.ts)
- [Security policy](https://github.com/kunickiaj/codemem/blob/a76ce405b5014e8ed0d2d3e956a2c770d75305cb/SECURITY.md)
- [Project metrics](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial status](../results/initial-baselines-status.json).

**Verification boundary:** Read-only source and documentation review; no codemem runtime, tests, or benchmarks.
