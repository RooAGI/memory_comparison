# Cua

**Review status:** Reviewed from code and official documentation at `main` [`848e2a561a5f8b01286d855afb58bc1ac19a150c`](https://github.com/trycua/cua/commit/848e2a561a5f8b01286d855afb58bc1ac19a150c). Review time: 2026-11-25 10:26:40 UTC (02:26:40 PST; America/Los_Angeles).

## Summary

Cua is a computer-use platform and toolkit spanning desktop automation, sandboxes, VMs, and agent integrations.[readme] Its current repository includes a narrow Computer History preview for local action metadata, but marks that feature deprecated and off by default.[driver][preview] Cua is not presented as a general-purpose persistent memory system.

## Who and what

The official README describes Cua as Cua Spaces, Cua Driver, Lume, a sandbox SDK and CLI, CUA-S1, and Cua Bench.[readme] Its citation metadata names Cua AI, Inc.[readme] This is a software product suite and framework, not a standalone memory database. The catalog resolves ordinal 177 to Cua, slug `cua`, and the listed locator `https://github.com/trycua/cua`; its Atlas URL is retained for roster attribution only, not as assessment evidence.[catalog][atlas]

## Architecture and data model

The repository combines several layers: Cua Driver exposes computer inspection and action tools to agents over MCP or CLI and provides native Python and TypeScript SDKs; the Cua SDK and CLI manage local containers, VMs, images, and Spaces; Cua Spaces provides desktop environments; Lume manages local VMs; Cua Bench supports evaluation.[readme][driver] This is computer-use architecture, not a general-purpose user-fact memory architecture.

Computer History is a distinct opt-in preview that records Cua-mediated actions, session lifecycle, control, access, and writer-health events.[architecture][event_schema][preview] Its event schema uses opaque session/action IDs, sequence numbers, timestamps, platform and capability fields, optional fixed application identity, and enumerated outcomes, routes, evidence kinds, and health categories; it excludes free-form content.[event_schema]

The implementation sends events to a bounded, nonblocking writer queue and stores them as a CBOR sequence of COSE_Encrypt0 records.[history_core][profile] The documented profile uses ChaCha20-Poly1305 with keys protected by the platform credential store; per-chunk keys are derived from a namespace root key.[history_core][preview] The implementation defines 7-day retention, a 100 MiB quota, a 512-event writer queue, and a 200-event query cap.[history_core][preview]

GitHub identifies `main` as the default branch.[repo] The official main Atom feed reported the current head [`848e2a561a5f8b01286d855afb58bc1ac19a150c`](https://github.com/trycua/cua/commit/848e2a561a5f8b01286d855afb58bc1ac19a150c) at 2026-11-25T09:02:16Z.[head][commit]

## Write, update, delete, and retrieval

The preview records only activity mediated by Cua Driver, not ambient desktop activity.[architecture][preview] It omits screenshots, raw keystrokes or typed text, clipboard, raw tool arguments/results, accessibility trees, paths, window titles, URLs, and free-form diagnostics.[architecture][preview][event_schema]

Event capture uses a nonblocking `try_send` path, so queue backpressure or storage failure does not fail the computer action.[history_core] The bounded writer, fixed schema, encrypted chunks, health categories, retention, and quota are source-visible engineering controls; no latency or reliability measurements were collected.[history_core][event_schema][preview]

The preview is documented as deprecated and off by default; its tools are scheduled for removal after 26 Nov 2026.[driver][preview] It offers enable, pause, resume, disable, status, list/show, and delete controls. Documentation says disable preserves history; delete destroys the namespace key and removes encrypted files.[preview] The core also has an offline purge path.[history_core] No update or correction operation is documented for event records.

Agents can use permission-gated, read-only `history_status` and `history_query` tools; the preview guide says queries return at most 200 metadata events and record a fixed access-audit event.[driver][preview][event_schema] The inspected guide does not specify semantic ranking, and the preview does not establish a general memory retrieval interface.

## Scope, provenance, efficiency, and observability

History is described as local and encrypted, with platform-specific credential stores and separate namespaces for installed and local-development builds.[preview][architecture][history_runtime] The inspected design does not establish tenant, project, or agent identity isolation; local device/profile boundaries are not equivalent to tested access-control guarantees.

Event fields record action outcome categories and limited evidence kinds such as accessibility/browser/value readback or window change.[event_schema] These fields provide provenance about Cua Driver actions, not source-document citations or claim-level support for arbitrary agent answers.

The preview has local CLI and permission-gated agent reads, along with health categories for dropped events, quota, key, writer, and storage failures.[history_core][preview] The repository describes no broader memory indexing, consolidation, or memory-specific telemetry; source inspection does not measure cost, tokens, storage efficiency, or query latency.

## Metric-domain evidence

- Answerable retrieval and abstention — unmeasured. The preview exposes bounded history reads, but no general memory retrieval workload or answerability probe was run.[preview][metrics][status]
- Correction accuracy and stale-value rate — unmeasured. No event correction contract or correction workload was documented or executed.[event_schema][metrics][status]
- Deletion leakage — unmeasured. A delete and offline purge path are documented/implemented, but no runtime deletion or residual-data probe was run.[history_core][preview][metrics][status]
- Scope isolation — unmeasured. Device-local key namespaces are visible, but no tenant, project, agent, or session isolation test was run.[history_runtime][preview][metrics][status]
- Evidence support precision and citation coverage — unmeasured. Structured action evidence categories exist, but no answer-citation evaluation was run.[event_schema][metrics][status]
- Retrieval latency and write-to-recall delay — unmeasured. The nonblocking writer path is source-visible; no runtime timing probe was run.[history_core][metrics][status]
- Token use and cost — unmeasured. No memory-specific model usage or cost data was collected.[readme][metrics][status]
- Storage efficiency — unmeasured. Quota and retention limits are documented, but no history-size or corpus-attributed storage measurement was collected.[history_core][preview][metrics][status]

Project benchmark status is [`not_run`](../data/system-reviews/cua.json); see [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution-status record](../results/initial-baselines-status.json). These documents define the workload; no benchmark was executed.[metrics][fixture][status]

## Limits and unknowns

- This is a bounded review of the official root and Driver documentation plus the Computer History core/runtime, event schema, and file-profile sources at one verified main SHA. It did not inspect every platform key adapter, tool integration, or deployment.
- Cua is a broad computer-use platform. The inspected docs do not define it as a general-purpose memory system; this assessment treats Computer History as the narrow memory-adjacent feature.
- Computer History is documented as deprecated and off by default, with tool removal scheduled after 26 Nov 2026. Runtime availability was not tested.
- The feature records action metadata, not full conversations or desktop state. It therefore cannot support general recall from screenshots, typed content, clipboard data, or ambient activity.
- The encrypted store is bounded by documented retention and quota, but physical erasure from backups, snapshots, copied ciphertext, SSD wear leveling, or already decrypted process memory is not guaranteed by the preview guide.
- No Cua runtime, tests, or benchmarks were run. All project benchmark domains remain unmeasured.

## Sources

- [Official repository](https://github.com/trycua/cua) and [main feed](https://github.com/trycua/cua/commits/main.atom).
- [Verified current head](https://github.com/trycua/cua/commit/848e2a561a5f8b01286d855afb58bc1ac19a150c).
- [README](https://github.com/trycua/cua/blob/848e2a561a5f8b01286d855afb58bc1ac19a150c/README.md), [Cua Driver README](https://github.com/trycua/cua/blob/848e2a561a5f8b01286d855afb58bc1ac19a150c/libs/cua-driver/README.md), [Computer History architecture](https://github.com/trycua/cua/blob/848e2a561a5f8b01286d855afb58bc1ac19a150c/libs/cua-driver/docs/computer-history-architecture.md), and [preview guide](https://github.com/trycua/cua/blob/848e2a561a5f8b01286d855afb58bc1ac19a150c/libs/cua-driver/docs/computer-history-preview.md).
- [History core](https://github.com/trycua/cua/blob/848e2a561a5f8b01286d855afb58bc1ac19a150c/libs/cua-driver/rust/crates/cua-driver-core/src/history.rs), [runtime integration](https://github.com/trycua/cua/blob/848e2a561a5f8b01286d855afb58bc1ac19a150c/libs/cua-driver/rust/crates/cua-driver/src/history_runtime.rs), [event schema](https://github.com/trycua/cua/blob/848e2a561a5f8b01286d855afb58bc1ac19a150c/libs/cua-driver/docs/computer-history-event-v0.schema.json), and [encrypted file profile](https://github.com/trycua/cua/blob/848e2a561a5f8b01286d855afb58bc1ac19a150c/libs/cua-driver/docs/computer-history-profile-v1.cddl).
- [Catalog identity and Atlas locator](../data/memory-systems.json); Atlas is identity/locator attribution only.
- [Metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).