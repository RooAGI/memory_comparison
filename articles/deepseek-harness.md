# DeepSeek Harness — source review

- **Review status:** Reviewed from code at the verified upstream head
- **Benchmark status:** Benchmark not run
- **Roster position:** Ordinal 183 — DeepSeek Harness / `deepseek-harness`
- **Listed repository:** [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
- **Canonical upstream:** same repository; default branch `master`; reviewed head [4b399c39a6d1479cd84ca591b4d7c88e24d38a96](https://github.com/deepseek-ai/deepseek-harness/commit/4b399c39a6d1479cd84ca591b4d7c88e24d38a96)
- **Review time:** 2026-11-25 02:45:10 UTC (2026-11-24 18:45:10 PST; America/Los_Angeles)

## Identity and scope

The project catalog lists DeepSeek Harness at ordinal 183 with slug `deepseek-harness`, an explicit GitHub locator, and a pinned Atlas attribution. The Atlas reference is recorded for curated identity and locator attribution only; it is not assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/deepseek-harness.md)]

The official repository page identifies `master` as the default branch. Its master commit feed reports head `4b399c39a6d1479cd84ca591b4d7c88e24d38a96`, updated 2026-11-22T08:50:28Z; the SHA-pinned repository sources below use that revision.[[repository](https://github.com/deepseek-ai/deepseek-harness)] [[master commit feed](https://github.com/deepseek-ai/deepseek-harness/commits/master.atom)] [[reviewed head](https://github.com/deepseek-ai/deepseek-harness/commit/4b399c39a6d1479cd84ca591b4d7c88e24d38a96)]

## Summary and architecture

DeepSeek Harness is an open-source agent harness built on Cordis. It composes the model adapter, tool registry, session log, agent loop, and persistence through plugins and ordered profile bundles. The official README labels the project a developer preview and warns of compatibility-breaking changes.[[README](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/README.md)] [[architecture](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/architecture.md)]

A `SessionHeader` holds session metadata, including working directory and optional parent/fork lineage. The event log contains typed `SessionEvent` records with sequence numbers and timestamps. Events cover user and system context, turns and steps, request headers, assistant outputs, tool calls/results, and extension records. The Session package is in-memory; a separately mounted persistence plugin makes it durable.[[event types](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/core/session/src/types.ts)] [[session docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/session.md)] [[persistence docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/persistence.md)]

The log is append-only. The current model history is a derived surface folded from message-producing events. A surface replacement can shadow earlier messages for future requests while leaving those events in the raw log. Compaction records its summary and source range, then adds a replacement message; it does not erase the replaced history.[[surface implementation](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/core/session/src/surface.ts)] [[compaction docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/compaction.md)]

## Write, update, delete, and retrieval

**Write.** `Session.append` validates and freezes JSON event payloads before adding a typed event to the session log. The persistence contract allows write-behind; callers that require a durable checkpoint await `flush`. The documented providers include compressed JSONL event frames and an optional SQLite segmented store.[[session docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/session.md)] [[persistence API](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/session/session-persistence/src/index.ts)] [[persistence docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/persistence.md)]

**Update and correction.** The inspected log contract does not overwrite an earlier event. Compaction summarizes a selected surface range and appends a replacement user message with source-event references. This changes the model’s active context but preserves the original events for replay and transcript views; it is not a general fact-correction ledger.[[session docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/session.md)] [[compaction docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/compaction.md)]

**Delete.** The inspected Session and SessionPersistence contracts expose append, create/open, stat/list, close, and flush operations, but no per-event or session-delete method. These sources do not establish physical erasure of stored history.[[persistence API](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/session/session-persistence/src/index.ts)] [[persistence docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/persistence.md)]

**Retrieval.** The model receives messages derived from the session log. An optional Session Query service provides exact event reads, bounded windows, metadata filters, event relationship traces, and paginated full-text search; its SQLite provider owns the FTS index. Query documents describe extracted semantic text and omit reasoning blocks, blocked prompts, structural events, and stream chunks.[[session docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/session.md)] [[query docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/session-query.md)] [[query types](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/session-query/session-query/src/types.ts)]

## Scope isolation

Session metadata can include `cwd`, parent session, seed status, and the agent preset. Query filters include working directory, lineage, availability, and event properties. These provide selection and lineage context, but the inspected persistence contract does not define a tenant ACL. Isolation beyond the mounted query integration depends on caller authorization and deployment configuration; no isolation workload was run.[[event types](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/core/session/src/types.ts)] [[query docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/session-query.md)] [[architecture](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/architecture.md)]

## Provenance and evidence

Events preserve their order, source attribution, model/tool activity, and optional event-to-event references. Assistant records may include the compact model stream and adapter-reported token usage. Compaction records the summarized source range and event sequence IDs. This supports reconstruction and lineage but does not verify the truth of conversation claims or establish external evidence citations.[[event types](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/core/session/src/types.ts)] [[session docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/session.md)] [[compaction docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/compaction.md)]

## Efficiency and observability

The source describes cached incremental surface folding, cursor-paginated full-text search, metadata-first session listing, query cache revisions, compressed persistence frames, SQLite FTS indexing, and explicit flush barriers. Logs can retain request/attempt timing, event timestamps, adapter-reported usage, query traces, and persistence revisions. These are implementation observations; no latency, reliability, token, cost, or storage measurement was collected.[[surface implementation](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/core/session/src/surface.ts)] [[query docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/session-query.md)] [[persistence docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/persistence.md)]

## Metric-domain evidence

All benchmark domains remain unmeasured. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).

- **Answerable retrieval and abstention — unmeasured.** Session and full-text query APIs are documented, but no adjudicated retrieval workload was run.[[query docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/session-query.md)]
- **Correction accuracy and stale-value rate — unmeasured.** Compaction replaces active context and retains the raw log; no correction probes were run.[[compaction docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/compaction.md)]
- **Deletion leakage — unmeasured.** A deletion API was not found in the inspected persistence contract, and no residual-data probe was run.[[persistence API](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/session/session-persistence/src/index.ts)]
- **Scope isolation — unmeasured.** Query filters and profile composition are code-visible; no cross-scope workload was run.[[query docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/session-query.md)] [[architecture](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/architecture.md)]
- **Evidence support and citation coverage — unmeasured.** Event references support reconstruction, but no answer-evidence evaluation was run.[[event types](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/core/session/src/types.ts)]
- **Retrieval latency and write-to-recall delay — unmeasured.** Indexing and persistence mechanisms are documented, but no timing probes were run.[[persistence docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/persistence.md)]
- **Tokens and cost — unmeasured.** The log can store adapter-reported usage; no provider-cost or token workload was measured.[[event types](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/packages/core/session/src/types.ts)]
- **Storage efficiency — unmeasured.** Compressed storage is documented, but no bytes-per-item measurement was collected.[[persistence docs](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/docs/subsystems/persistence.md)]

## Limits and unknowns

This review covers the official README and architecture/session/persistence/query/compaction documentation plus the pinned Session event/surface and persistence/query contract sources. It did not inspect every provider implementation, profile composition, or deployment policy. The project describes itself as an evolving developer preview. Runtime configuration, active persistence provider, query-tool availability, caller-specific authorization, deletion behavior outside the inspected contracts, retrieval quality, reliability, and all benchmark metrics remain unverified. No system, tests, or benchmarks were run.

## Contact

The official pinned README was checked for a published contact email. It directs feedback and bug reports to GitHub Discussions and publishes no contact email; no profile, commit metadata, or third-party directory was used.[[official README](https://github.com/deepseek-ai/deepseek-harness/blob/4b399c39a6d1479cd84ca591b4d7c88e24d38a96/README.md)]

## Benchmark status

**Benchmark not run.** No DeepSeek Harness runtime, tests, or benchmark workload was executed. Source observations are not measured results. See [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).
