# Daimon

## Identity and review pin

- Catalog ordinal: 180
- System: Daimon
- Slug: `daimon`
- Listed repository: https://github.com/Daily-Nerd/daimon
- Roster attribution: explicit repository locator. The pinned Atlas report is recorded only for curated identity and locator attribution ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/daimon.md)).
- Canonical upstream: https://github.com/Daily-Nerd/daimon
- Default branch: `main`
- Reviewed full head: [3e94f9441671abf1e9fa7c932b9e956dbf891fe8](https://github.com/Daily-Nerd/daimon/commit/3e94f9441671abf1e9fa7c932b9e956dbf891fe8)
- Review timestamp: 2026-11-25T10:35:44Z (UTC; 2026-11-25 02:35:44 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

Daimon is a local-first memory and briefing system for coding-agent sessions. It serializes transcript-derived checkpoints at session end, then carries selected open items into a compact, trust-labeled briefing for a later session. Durable state is project-scoped JSON plus append-oriented ledgers; a SQLite FTS5 index is disposable derived state. The architecture places deterministic code between model extraction and persistence to verify quotations, attach provenance, apply carry and deletion policy, and render the briefing. ([README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md), [runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md))

The upstream README says the product is not a live background-agent monitor and skips sub-agent exchanges. It also describes host-specific differences: Claude Code, Codex, Kimi, Windsurf, and Gemini do not all expose the same capture or briefing hooks. ([README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md), [runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md))

## Architecture and data model

The current runtime is documented as a host-agnostic Python modular monolith. Host adapters translate lifecycle events into a shared runtime. Hook and CLI serialization enter one capture pipeline; local MCP and viewer surfaces are optional readers. The system does not require a remote memory service, vector database, graph database, or always-on daemon. ([runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md))

A checkpoint contains structured cognitive items extracted from a transcript, along with project/session/branch and source metadata. The store keeps per-session JSON, project pointers, and lifecycle/knowledge ledgers. The SQLite recall database is rebuilt from those durable files and ledgers when missing, corrupt, or stale; it is not the source of truth. Atomic file replacement is used for checkpoint writes, while pointer routing keeps one project’s latest state separate from another’s. ([store](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/store.py), [recall index](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/recall.py))

## Write, update, delete, and retrieval

**Write.** The shared capture pipeline reads session messages, checks readability and minimum content, prepares a source reference and transcript hash where available, asks a configured model/CLI to serialize candidate items, verifies and stamps them, carries eligible items from the prior project checkpoint, then writes the checkpoint. Advisory carry and candidate-emission steps can fail without losing the checkpoint. Host lifecycle hooks are documented as fail-open so memory errors do not break the host session. ([capture pipeline](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/capture.py), [runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md))

**Update and correction.** New captures merge unresolved prior items forward, while explicit resolution and supersession records preserve lifecycle history instead of silently overwriting a value. Candidate supersession is not itself a human decision: trust and ranking distinguish suggested or observed changes from confirmed lifecycle transitions. The exact behavior depends on configured carry limits and the capture/read path; this review did not exercise it. ([capture pipeline](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/capture.py), [recall index](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/recall.py), [runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md))

**Delete.** The forget operation uses a declared surface registry and runs its deletion steps in phase order. It records a value-keyed tombstone before other changes, then scrubs or purges registered plaintext and derived surfaces; failures are reported per surface, and failure to write the tombstone refuses the operation before touching the others. The architecture notes tombstones also prevent forgotten values from re-entering through recapture or team synchronization. This is a code-path description; no deletion probes were run, and it does not establish erasure of copies outside declared surfaces. ([forget implementation](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/forget.py), [runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md))

**Retrieval.** Session-start hooks render a deterministic briefing from the current project’s checkpoint. The broader recall command searches checkpoint history through a derived SQLite FTS5 index. By-id inspection uses a read-only locator instead of rebuilding the index. Search results can demote superseded or contradicted items, but those flags are evidence/ranking signals rather than automatic filters. A memory item that no longer fits the live carry set remains available to explicit recall. ([README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md), [recall index](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/recall.py), [runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md))

## Scope isolation

Project identity is stamped at the write boundary and checked during reads and carry. Per-project pointers route briefings; project slugs and aliases support deliberate cross-project operations. CLI operations can intentionally select another project, while the architecture describes local MCP as read-only and defaulted to its own project unless the host grants broader access. Team synchronization is opt-in and uses a private Git remote; the README explicitly says author attribution is declared rather than authenticated, with repository membership as the access boundary. These mechanisms describe local routing and policy, not a tested multi-tenant security boundary. No isolation workload was run. ([store](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/store.py), [runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md), [README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md))

## Provenance and evidence

Daimon distinguishes verbatim items, which are bound to exact source quotations, from inferred items produced by the model. The model proposes content but deterministic code verifies quotes and attaches source/checkpoint provenance before storage. The provenance module resolves supported host transcript references only within registered local roots and records states such as resolved, absent-local, unreadable, ambiguous, remote-author, or unsupported. Carry snapshots provenance so an older source checkpoint can later be garbage-collected without losing the evidence receipt. Corroboration is tracked separately and does not upgrade an item’s trust class. ([README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md), [provenance implementation](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/provenance.py), [runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md))

These receipts improve inspectability but do not independently prove that an inference is true. Team author names are not cryptographically authenticated by default; signed receipts are an opt-in feature. ([README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md), [provenance implementation](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/provenance.py))

## Efficiency and observability

The design avoids embeddings and keeps retrieval local with FTS5. The README describes a short session-start briefing and explicit full-history recall; the architecture says the index can be thrown away and rebuilt from durable files. These choices make storage and operation inspectable, but no corpus-size or performance measurements were taken for this review. ([README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md), [recall index](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/recall.py), [store](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/store.py))

Operational signals include `daimon status` for capture health and retry state, structured error breadcrumbs for recall failures, and explicit reach reporting for forget steps. The README also documents one automatic retry for failed capture and manual recovery commands. These are inspectable status surfaces, not measured reliability outcomes. ([README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md), [recall index](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/recall.py), [forget implementation](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/forget.py))

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Daimon. The fixture and metric definitions were consulted as project contract only; neither the system nor benchmark was run. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

| Domain | Status | Evidence available from source review |
|---|---|---|
| Answerable retrieval accuracy and abstention | Unmeasured | Briefing and FTS retrieval code inspected; no scored query outcomes. |
| Correction accuracy and stale-value rate | Unmeasured | Carry and lifecycle code inspected; no correction probes or adjudication. |
| Deletion leakage | Unmeasured | Forget surface registry and failure handling inspected; no post-delete probes. |
| Scope isolation | Unmeasured | Project routing and MCP policy documented; no paired allowed/forbidden workload. |
| Evidence support precision and citation coverage | Unmeasured | Quote receipts inspected; no generated claims or citations were adjudicated. |
| Retrieval latency | Unmeasured | No timings collected. |
| Write-to-recall delay | Unmeasured | No timed probes run. |
| Tokens and cost | Unmeasured | No model/provider usage or charges collected. |
| Storage efficiency | Unmeasured | JSON/SQLite design inspected; no storage size measured. |

## Limitations and unknowns

This review inspected the README, runtime architecture, capture pipeline, provenance resolution, checkpoint store, recall index, and forget implementation at the reviewed head. It did not inspect every host adapter, serializer prompt, CLI command, policy rule, team synchronization path, or UI/MCP read surface. ([reviewed README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md), [runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md), [capture pipeline](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/capture.py), [forget implementation](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/forget.py))

Host capabilities differ, some surfaces are opt-in, and the README marks certain host behavior as capture-only or not yet verified. Code inspection does not establish answer accuracy, complete erasure beyond registered surfaces, or security against a hostile local user or team member. ([README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md), [runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md))

## Contact

No contact email is published in the official pinned README or SECURITY.md. The README links to project documentation and the SECURITY.md directs vulnerability reports through GitHub private vulnerability reporting. The exact checked sources are [README.md](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md) and [SECURITY.md](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/SECURITY.md). No profile/commit metadata or third-party directory was used.

## Benchmark status

**Benchmark not run.** No Daimon runtime, tests, or benchmarks were run. The project metric definitions, fixture, and result/status reference were read as documentation only; they are not evidence of Daimon benchmark results. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Pinned Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/daimon.md)
- [Official repository](https://github.com/Daily-Nerd/daimon)
- [Official main commit feed](https://github.com/Daily-Nerd/daimon/commits/main.atom)
- [Reviewed head 3e94f9441671abf1e9fa7c932b9e956dbf891fe8](https://github.com/Daily-Nerd/daimon/commit/3e94f9441671abf1e9fa7c932b9e956dbf891fe8)
- [Pinned README](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/README.md)
- [Pinned runtime architecture](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/docs/RUNTIME-ARCHITECTURE.md)
- [Pinned capture pipeline](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/capture.py)
- [Pinned provenance implementation](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/provenance.py)
- [Pinned checkpoint store](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/store.py)
- [Pinned recall index](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/recall.py)
- [Pinned forget implementation](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/plugin/daimon_briefing/forget.py)
- [Official security policy](https://github.com/Daily-Nerd/daimon/blob/3e94f9441671abf1e9fa7c932b9e956dbf891fe8/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project result/status record](../results/initial-baselines-status.json)
