# EverOS source and design review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 230 / EverOS / `everos`  
**Listed repository locator:** [EverMind-AI/EverOS](https://github.com/EverMind-AI/EverOS)  
**Canonical upstream:** [EverMind-AI/EverOS](https://github.com/EverMind-AI/EverOS)  
**Default branch / reviewed head:** main / [d2b74780a443c6d7304ca9aa1bfdf36fdc6d7c9b](https://github.com/EverMind-AI/EverOS/commit/d2b74780a443c6d7304ca9aa1bfdf36fdc6d7c9b)  
**Review time:** 2026-11-25 20:05:56 UTC (2026-11-25 12:05:56 PST; America/Los_Angeles).

## Identity and review pin

The catalog records EverOS as ordinal 230 with slug `everos`, an explicit repository locator, and a pinned Agent Memory Atlas roster attribution. The catalog and Atlas attribution establish roster identity and locator context only; Atlas descriptions and capability marks are not assessment evidence. GitHub's official repository page identifies `main` as the default branch; its official `commits/main` API endpoint returned full head d2b74780a443c6d7304ca9aa1bfdf36fdc6d7c9b. The source inspection below uses that exact head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

EverOS is a local-first Python memory runtime and library for agents. It stores memory content in editable Markdown files and maintains SQLite state plus a derived LanceDB search index. The docs describe a synchronous message-to-episode write path followed by background indexing and asynchronous derived-memory strategies; search may therefore lag a successful write.[[readme]][[memory-flow]][[storage]][[api]]

## Who and what

The official repository identifies the project as EverOS under the EverMind-AI organization and describes it as a Python library and runtime. It exposes an HTTP API and CLI, with memory domain and storage layers behind service orchestration; this review does not infer individual maintainer identity from commit or profile metadata.[[readme]][[architecture]][[api]]

## Architecture and data model

The documented package layout separates entrypoints, service orchestration, memory-domain operations, and infrastructure adapters. The current storage model uses human-readable Markdown with YAML frontmatter as its canonical content, SQLite for buffers, system state, cascade queue and OME state, and LanceDB for derived vector, BM25 and scalar retrieval rows. The derived indexes are rebuildable from Markdown.[[architecture]][[memory-flow]][[storage]]

The stored kinds include user episodes, atomic facts and profiles; agent cases and skills; and shared knowledge documents and topics. Daily logs append episodes, facts and cases, profiles are rewritten as one file, and skills use a named directory. Scope is encoded in the path as app/project followed by user, agent or knowledge ownership. The entry id and frontmatter tie records to the index; entries also carry timestamps, sender/session and parent links where applicable.[[memory-flow]][[storage]]

## Write, update, delete, and retrieval

**Write and update.** `POST /memory/add` buffers messages by session, app and project; boundary detection and `/flush` extract MemCells, then the user pipeline writes episode Markdown synchronously. The Offline Memory Engine (OME) asynchronously derives summaries, facts, profiles, cases and skills. Editing Markdown directly is supported; the in-process cascade watcher queues changes durably in SQLite and updates changed index entries. The response can precede completion of derived memories or search indexing.[[api]][[memory-flow]][[memorize]][[cascade]][[storage]]

**Update and supersession.** Daily-log entries can be patched with a deprecation pointer; profile content is rewritten. Reflection can merge episode clusters, re-extract facts and deprecate the original episodes. These paths revise or supersede stored content; the reviewed sources do not describe a single versioned truth ledger with adjudicated evidence for every derived claim.[[storage]][[memory-flow]]

**Delete.** The delete service supports session, owner and session-plus-owner scopes; delete-by-ids removes selected episodes together with related merged episodes, facts and cluster membership. It removes source Markdown before index rows; the cascade catches the index up asynchronously. Purge documentation warns that old LanceDB table versions may retain deleted rows until pruning and SQLite free pages until vacuum. Whole-root local deletion does not clear remote Milvus data.[[delete]][[api]][[storage]]

**Retrieval.** The API supports keyword, vector, hybrid and agentic methods. User episode/fact hybrid search fuses three recall lanes using reciprocal-rank fusion and calibrated scoring; agent-case and skill retrieval use distinct hybrid pipelines. Filters are compiled into a backend-neutral predicate. Search may not immediately find a newly written entry while the cascade is pending; the docs report typical sync below a second and up to roughly 10–15 seconds under load, and identify a pinned-LanceDB keyword-index delay for repeated terms in recently written rows.[[api]][[adapter]][[filters]][[memory-flow]]

## Scope isolation

Every read predicate pins owner id, owner type, app id and project id; caller filter fields cannot override those reserved scope keys. User-memory reads also exclude deprecated entries. API docs describe owner and session filters and Markdown paths partitioned by app/project and owner. These code and documentation observations show intended filtering boundaries, not an independent adversarial isolation assessment; the security policy says the service assumes a trusted local caller and does not support exposing the API to an untrusted network without an external gateway/auth layer.[[filters]][[api]][[storage]][[security]]

## Provenance and evidence

Markdown entries preserve readable content and frontmatter identifiers, timestamps, sender ids, session ids and parent relationships; facts refer to their source episode. The raw accepted-input log can preserve each accepted add request before extraction, with a retention period and size controls, but it is not exposed through a read API. These provide source and lineage handles; they do not by themselves establish that model-generated summaries, facts or answers are true or adequately supported. The review did not adjudicate generated evidence or citations.[[storage]][[memory-flow]][[readme]][[api]]

## Efficiency and observability

EverOS avoids a separate database service by embedding SQLite and the default LanceDB index in the local memory root; Markdown remains portable and indexes can be rebuilt. Cascade processes changed entries and re-embeds by content digest, while bounded/open-file handling and index configuration address resource use. Search and derived-memory processing have eventual-consistency windows, and vector/rerank/agentic features require separately configured providers. The API documents request ids correlated with structured logs, tracing and metrics, plus health and metrics endpoints; optional MemTrace captures execution stages when installed and enabled. No resource or latency measurements were collected for this review.[[memory-flow]][[cascade]][[api]][[memtrace]][[configuration]]

## Metric-domain evidence

All benchmark domains are **unmeasured in this review**. Source structure and upstream-published claims are not measurements performed here. No EverOS runtime, benchmark, or test was run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) for the project's evaluation protocol and run status.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Search methods and retrieval lanes are implemented/documented; no answer set was scored in this review. | Unmeasured |
| Correction and stale values | Markdown entry deprecation and Reflection supersession exist; no correction workload was run. | Unmeasured |
| Deletion leakage | Delete/purge paths and asynchronous index cleanup were inspected; no post-delete probes were run. | Unmeasured |
| Scope isolation | Reserved scope filters are enforced in the predicate compiler; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Source links and parent/session metadata are represented; no output evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Documentation describes index lag; this review collected no runtime timings. | Unmeasured |
| Tokens, cost and storage | Local storage and provider configuration were inspected; no workload cost or resource measurements were collected. | Unmeasured |

## Limits and unknowns

This is a pinned source and documentation review, not an operational security or quality audit. The documented memory pipeline depends on configured language, embedding and reranking providers for optional behavior; asynchronous indexing and OME strategies create periods when an entry is durable but absent from retrieval or derived views. The docs also note a recent-row keyword-index limitation for the pinned LanceDB version.[[memory-flow]][[api]][[configuration]]

The security policy says the HTTP server has no built-in authentication, stores memory as plaintext Markdown, and assumes trusted local callers; use outside that threat model requires an external gateway/auth layer and OS-level protection for sensitive files. Purge may leave old index versions or SQLite free pages until cleanup, and local root deletion does not erase remote Milvus rows. This review did not measure deletion leakage, quality, isolation, performance or cost.[[security]][[storage]][[metrics]]

## Benchmark status

**Benchmark not run.** No EverOS runtime, tests or benchmark workload was executed for this review. No quality, latency, token, cost, storage, deletion, correction or isolation result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned `SECURITY.md` publishes `evermind@shanda.com` for vulnerability reports; this address is recorded with that exact source URL. No commit/profile metadata or third-party directory was used.[[security]]

## Sources

Upstream file links are pinned to the verified full SHA. The Atlas source is included only for roster attribution, not system assessment. See the structured record [everos.json](../data/system-reviews/everos.json) and [curated roster](../data/memory-systems.json).
