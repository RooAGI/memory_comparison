# GitMem source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 259 / GitMem / `gitmem`  
**Listed repository locator:** [gitmem-dev/gitmem](https://github.com/gitmem-dev/gitmem)  
**Canonical upstream:** [gitmem-dev/gitmem](https://github.com/gitmem-dev/gitmem)  
**Default branch / reviewed head:** main / [caef0358195dc1211891288c928c0462120d3bf0](https://github.com/gitmem-dev/gitmem/commit/caef0358195dc1211891288c928c0462120d3bf0)  
**Review time:** 2026-11-25 21:06:47 UTC (2026-11-25 13:06:47 PST; America/Los_Angeles).

## Identity and review pin

The curated roster identifies GitMem as ordinal 259, slug `gitmem`, with the explicit locator `https://github.com/gitmem-dev/gitmem`. Its Atlas attribution is retained for roster identity and locator context only. The official GitHub repository page identifies `main` as the default branch, and the official main commit feed identifies the current full head SHA shown above. The source review is pinned to that SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

GitMem is an MCP server for retaining coding-agent lessons such as scars, wins, patterns, decisions, and threads across sessions. The free path stores JSON locally and searches it lexically; the opt-in Pro/dev path uses Supabase and supports vector recall. This is a source review, not a measured quality or security result.[[readme]][[storage]][[localstore]][[recall]]

## Who and what

The official README describes GitMem as an MCP server for coding-agent clients including Claude Code, Cursor, VS Code/Copilot, Windsurf, and generic MCP clients. Setup can add configuration, instruction files, and lifecycle hooks where supported. The review is of the repository implementation and does not verify behavior in every client.[[readme]]

## Architecture and data model

The README groups memory into scars, wins, patterns, decisions, and unfinished threads. A learning record is written with an ID, type, title, description, project, keywords/domain, timestamps and active state; optional fields include severity, counter-arguments, source issue, and action/self-check guidance. The advertised lifecycle is recall, work, learn, close, then recall again.[[readme]][[create]]

The storage abstraction routes free-tier operations to local JSON collections under the GitMem directory and Pro/dev operations to Supabase. Local search uses BM25; the recall handler uses local vector search when available on the Pro path and falls back to Supabase search. These are distinct storage and retrieval paths.[[storage]][[localstore]][[recall]]

The repository exposes separate MCP handlers for creating and recalling learnings, archiving them, handling decisions and threads, managing session start/close, and transcript or document search. This review inspected representative learning, recall, archive, storage, and local-storage paths.[[readme]][[create]][[recall]][[archive]][[storage]]

## Write, update, delete, and retrieval

- **Writes:** `create_learning` generates a UUID and writes a learning. Scar writes require severity and at least two counter-arguments. The record's project is selected from the explicit parameter, current project, or `default`. Local writes upsert JSON without an embedding; the Pro path includes embedding/index work. The source reports that a record can be saved even if index refresh fails, delaying its visibility to recall.[[create]][[storage]]

- **Updates and correction:** The inspected write path creates a new learning rather than replacing an existing fact. The lifecycle can archive an older learning and create a new one, but a general fact correction or temporal supersession protocol was not established by the reviewed files. Correction accuracy and stale-value behavior were not measured.[[create]][[archive]][[metrics]]

- **Archive and deletion:** `archive_learning` accepts a full UUID or hexadecimal prefix, sets `is_active=false` and records `archived_at`, then attempts to flush the local vector cache. This is a soft archive that keeps the record. The inspected path does not establish physical erasure from backups or all derived copies.[[archive]][[localstore]]

- **Retrieval:** Recall takes a plan/query, optional project, result count, and session identifiers. The README positions recall before action. Free local search uses BM25; Pro recall uses local vector search when ready and a Supabase fallback. The handler tracks surfaced scars in session state and returns timing, cache, search-mode, network-call, and context diagnostics. A performance target appears in source comments; it is not a measured result.[[readme]][[recall]][[localstore]]

- **Scope isolation:** Writes carry a project field and recall accepts project context. The README describes local storage for solo use and Pro cloud persistence for teams. The inspected code establishes project metadata and intended boundaries, but this review did not verify every query predicate or test isolation across projects, users, or Supabase tenants.[[create]][[recall]][[readme]][[storage]]

- **Provenance and evidence:** Learning records can include a source issue, source date, and persona identity; scar records can carry counter-arguments and action/self-check fields. Recall returns learning identifiers and diagnostics. These fields help retain context, but the inspected path does not require a retained source passage or supply adjudicated claim-level citations.[[create]][[recall]]

- **Efficiency and observability:** Recall records elapsed time, result count, similarity scores, context size, cache state, search mode, network-call count, and whether retrieval was fully local. Metric write failures are non-fatal. Local file storage warns above 1 MB and, above 10 MB, evicts the oldest fifth of entries. No latency, throughput, token, cost, or storage benchmark was run.[[recall]][[localstore]]

## Metric-domain evidence

The project defines a fixed fixture and metrics for answerable retrieval, abstention, correction, deletion leakage, scope isolation, evidence support, latency, write-to-recall delay, tokens, cost, and storage. This review reports each domain as unmeasured; source structure and project protocol are not benchmark results.[[metrics]][[fixture]][[status]]

| Domain | Source observation | Result |
|---|---|---|
| Answerable retrieval and abstention | BM25 and vector/Supabase retrieval paths exist; no query workload was scored. | Unmeasured |
| Correction accuracy and stale values | Create and archive operations were inspected; no correction probes were run. | Unmeasured |
| Deletion leakage | Archive marks a record inactive but preserves it; no post-archive probes were run. | Unmeasured |
| Scope isolation | Project metadata and recall project context exist; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Optional source metadata and recall IDs exist; no claim/source pairs were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Timing and index-refresh instrumentation exist; no timings or delay observations were collected. | Unmeasured |
| Tokens, cost, and storage | No fixed-corpus model usage, price, or persistent-byte measurements were collected. | Unmeasured |

## Limits and unknowns

This review is pinned to the official `main` head and is based on the README and selected source paths. It does not establish retrieval quality, reliability, performance, authorization security, or client-specific behavior. Exact cross-project filtering, tenant isolation, conflict resolution, and end-to-end evidence guarantees remain unknown from the inspected paths.[[repo]][[head]][[readme]][[recall]][[storage]]

Local persistence rewrites JSON collections, and the local storage implementation has an entry-eviction policy when a collection exceeds 10 MB. Archive is a soft-delete path. This review did not trace every backup, remote retention path, or derived index, so it cannot establish complete deletion.[[localstore]][[archive]]

## Benchmark status

**Benchmark not run.** No GitMem runtime, tests, or benchmark workload was executed for this review. See the project [metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [initial benchmark status](../results/initial-baselines-status.json); none is a GitMem measurement.[[metrics]][[fixture]][[status]]

## Contact

The official pinned `SECURITY.md` publishes `security@gitmem.ai` for vulnerability reports. This is the only contact source checked for this review.[[security]]

## Sources

- [Curated catalog entry](../data/memory-systems.json) — ordinal 259 identity and listed locator.
- [Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/gitmem.md) — identity/locator attribution only.
- [Official repository](https://github.com/gitmem-dev/gitmem) and [main commit feed](https://github.com/gitmem-dev/gitmem/commits/main.atom) — canonical repository, branch, and current full head.
- [README at reviewed SHA](https://github.com/gitmem-dev/gitmem/blob/caef0358195dc1211891288c928c0462120d3bf0/README.md), [create-learning.ts](https://github.com/gitmem-dev/gitmem/blob/caef0358195dc1211891288c928c0462120d3bf0/src/tools/create-learning.ts), [archive-learning.ts](https://github.com/gitmem-dev/gitmem/blob/caef0358195dc1211891288c928c0462120d3bf0/src/tools/archive-learning.ts), [recall.ts](https://github.com/gitmem-dev/gitmem/blob/caef0358195dc1211891288c928c0462120d3bf0/src/tools/recall.ts), [local-file-storage.ts](https://github.com/gitmem-dev/gitmem/blob/caef0358195dc1211891288c928c0462120d3bf0/src/services/local-file-storage.ts), and [storage.ts](https://github.com/gitmem-dev/gitmem/blob/caef0358195dc1211891288c928c0462120d3bf0/src/services/storage.ts) — inspected code and documentation.
- [SECURITY.md at reviewed SHA](https://github.com/gitmem-dev/gitmem/blob/caef0358195dc1211891288c928c0462120d3bf0/SECURITY.md) — published vulnerability contact.
- [Project metrics](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [benchmark status record](../results/initial-baselines-status.json) — project protocol and status, not GitMem results.
