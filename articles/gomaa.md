# Gomaa source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 264 / Gomaa / `gomaa`  
**Listed repository locator:** [M4F-S/gomaa](https://github.com/M4F-S/gomaa)  
**Canonical upstream:** [M4F-S/gomaa](https://github.com/M4F-S/gomaa)  
**Default branch / reviewed head:** main / [3764b37797b3a0ba68e7f767a84ca401d209c825](https://github.com/M4F-S/gomaa/commit/3764b37797b3a0ba68e7f767a84ca401d209c825)  
**Review time:** 2026-11-25 21:20:49 UTC (2026-11-25 13:20:49 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Gomaa at ordinal 264, slug `gomaa`, with the explicit locator `https://github.com/M4F-S/gomaa`. Its pinned Agent Memory Atlas entry is recorded only as roster attribution, not as assessment evidence. The official GitHub repository page identifies `main` as the default branch. GitHub’s official `main.atom` feed reports full head `3764b37797b3a0ba68e7f767a84ca401d209c825`; a fresh shallow checkout and `git ls-remote --symref` independently resolved the same branch and SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Gomaa is a Python agent-memory system that pairs an Obsidian-compatible Markdown vault with SQLite or PostgreSQL stores. It exposes semantic notes and other memory forms through a Python API, CLI, MCP server, and framework adapters. The inspected implementation includes admission checks, embeddings, scoped search, graph links, lifecycle operations, and shared-store options. This review describes source behavior; it does not reproduce the upstream README’s performance figures or verify runtime quality.[[readme]][[core]][[mcp]]

## Who and what

The official README presents Gomaa as a local-first memory engine for agent frameworks and standalone deployments. The repository contains the memory library and integrations; it is not only a remote hosted service. No maintainer identity is asserted from commit, package-author, or profile metadata.[[readme]]

## Architecture and data model

The top-level `UnifiedMemorySystem` composes a `VaultManager`, `Embedder`, `AdmissionControl`, a selected `MemoryStore`, an optional shared store, a consolidation engine, and prospective-memory support. SQLite is the lightweight backend; PostgreSQL with pgvector is available for database deployments. Both implement the shared store interface for notes, search, lifecycle, graph links, timeline, episodic events, playbooks, and working memory.[[core]][[base]][[factory]][[readme]]

Semantic notes are Markdown files with YAML frontmatter (title, date, tags, type, status, salience, wing, room, links) and corresponding database rows containing content, scope, status, salience, embedding metadata, origin agent, lifecycle and access fields. Wiki links written in notes are also materialized into graph edges. Other records include episodic events, procedural playbooks, working-memory state, conflicts, and an activity timeline.[[vault]][[sqlite]][[postgres]][[core]]

The vault path builder rejects traversal components and resolves paths under the vault root. Writes use a sibling temporary file and atomic replace, with an EXDEV fallback. The vault-to-store sync reads titles from frontmatter, parses wiki links, upserts rows, and attempts missing embeddings without blocking the whole sync when embedding fails.[[vault]][[core]]

## Write, update, delete, and retrieval

**Write and update.** `remember` normalizes tags, promotes pinned notes to salience 1.0, neutralizes selected prompt-control tokens in prose, and applies length, pattern, near-duplicate, and same-title admission checks. An accepted note is embedded, written to the vault, then upserted to the database and linked; the vault file is restored or removed if the database step fails. Store upserts keep prior versions for ordinary same-scope updates. Admission checks are heuristic: near-duplicate and contradiction checks are best-effort and errors bypass those checks.[[core]][[security]][[sqlite]][[vault]]

**Delete and forgetting.** `forget` locates a matching title and wing/room, deletes the corresponding database row, and by default removes matching vault files; it also searches for identical-content copies in other scopes to avoid a later sync resurrecting the note. It supports dry-run and can retain vault files when requested. This is a coordinated delete, not a tombstone or cryptographic erasure guarantee; backups, external sync copies, and concurrent changes were not tested.[[core]][[sqlite]][[vault]]

**Retrieval.** The main API offers semantic, keyword, graph, associative-PPR, procedural, episodic, and hybrid modes. Store implementations accept optional wing/room filters; hybrid paths combine semantic and keyword result ranks, while the newer read-only recall service uses a shared ranker and bounded context formatter. Its per-turn endpoint defaults shared memory off and logs query, selected titles, latency, and rendered character count when configured. The general `UnifiedMemorySystem.recall` supports shared recall by default when a shared store exists, so scope and shared-store choices matter to callers.[[core]][[base]][[rank]][[service]]

## Scope isolation

Notes carry `wing` and `room`; SQLite and PostgreSQL search helpers add predicates only for supplied values. Omitting scope therefore searches broadly within the selected store. The default scope values on writes are `general/general`, but they are not authorization principals. Shared-store recall is a separate opt-in/opt-out decision depending on API path. The code provides data partitioning controls, but this review did not run tenant-isolation probes or establish deployment-level authorization for database credentials and shared stores.[[sqlite]][[postgres]][[core]][[service]]

## Provenance and evidence

The note schema can carry origin-agent, status, supersession, confidence, and embedding identity fields; wiki links and the timeline provide additional relationships and activity context. Admission control rejects some writes but does not preserve a durable record of rejected content. The timeline records operation summaries, and code does not make a source citation mandatory for a note or recalled answer. Consequently provenance quality depends on the caller’s chosen note content and workflow; evidence support and citation coverage remain unmeasured.[[sqlite]][[postgres]][[security]][[core]][[rank]]

## Efficiency and observability

The implementation supports local SQLite WAL and PostgreSQL/pgvector, optional local or remote embedding providers, indexed search, bounded candidate counts, and a character-bounded recall formatter. The read-only service caches query embeddings in memory up to a fixed entry cap and can append a JSONL record of query, returned titles, elapsed milliseconds, and output characters. The library also exposes timeline and stats paths. These are implementation hooks, not measurements from this review. The README publishes latency/throughput values, but this task did not independently reproduce them and they are not project benchmark results.[[readme]][[sqlite]][[postgres]][[embedder]][[service]]

## Metric-domain evidence

All project benchmark domains are **unmeasured here**. Source inspection is not a benchmark result. The [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define project evaluation materials, not Gomaa results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Multiple retrieval modes and a bounded formatter exist; answer correctness and abstention were not scored. | Unmeasured |
| Correction and stale values | Same-key upserts, versions, supersession, and lifecycle fields exist; correction sequences were not evaluated. | Unmeasured |
| Deletion leakage | `forget` coordinates store and vault deletion; no leakage, backup, or recovery probe was run. | Unmeasured |
| Scope isolation | Wing/room query filters and optional shared storage exist; no cross-scope workload was run. | Unmeasured |
| Evidence support and citations | Provenance can be represented but source evidence is not mandatory; no answers were adjudicated. | Unmeasured |
| Latency and write-to-recall delay | A service timer/logging path exists; no task timings were collected. | Unmeasured |
| Tokens, cost, and storage | Context bounding and multiple backends exist; no token, cost, or storage comparison was made. | Unmeasured |

## Limits and unknowns

This is a bounded review of the current README and selected implementation files at the verified upstream head. Gomaa, its tests, and benchmark workloads were not run. The README’s architecture, feature matrix, test results, and performance figures are upstream statements; they were not independently validated here.[[readme]]

The review did not inspect every adapter, backend query, backup/sync race, deployment authorization setup, or all consolidation paths. It cannot establish retrieval accuracy, secure tenant isolation, deletion propagation through external backups, embedding quality, or operational reliability. Optional provenance and broad queries without scope are material limitations for applications that need auditable, tenant-separated memory.[[core]][[vault]][[service]]

## Benchmark status

**Benchmark not run.** No Gomaa runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the project protocol and status, not Gomaa measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and SECURITY.md were checked for a published contact email. Neither publishes one; the security policy directs reporters to GitHub’s private vulnerability reporting feature. The structured record stores `contact_email: null` and both exact checked URLs. No address was inferred from commit/profile metadata, package metadata, or a third-party directory.[[readme]][[security-policy]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas source records curated roster attribution only and is excluded from assessment evidence. See the structured record [gomaa.json](../data/system-reviews/gomaa.json) and [curated roster](../data/memory-systems.json).
