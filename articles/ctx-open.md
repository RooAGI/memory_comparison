# CTX Cognitive Version Control

## Identity and review pin

- Catalog ordinal: 175
- System: CTX Cognitive Version Control
- Slug: `ctx-open`
- Listed repository: https://github.com/diegoxtr/ctx-open
- Roster attribution: explicit repository locator; the pinned Atlas entry is recorded only as curated identity/locator context ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ctx-open.md)).
- Canonical upstream: https://github.com/diegoxtr/ctx-open
- Default branch: `main`
- Reviewed full head: [c31d84e07c830f2d126f780f65ad2b0228fe54eb](https://github.com/diegoxtr/ctx-open/commit/c31d84e07c830f2d126f780f65ad2b0228fe54eb)
- Official main feed: [commits/main.atom](https://github.com/diegoxtr/ctx-open/commits/main.atom), updated 2026-09-21T19:27:36Z
- Review timestamp: 2026-11-25T10:19:51Z (UTC; 2026-11-25 02:19:51 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

CTX is a local-first .NET application that stores typed cognitive work artifacts in a project-local `.ctx` directory and versions durable state as immutable snapshots. It exposes a CLI, local viewer, and read-only-by-default stdio MCP adapter. Context packets are assembled with deterministic item caps and relation-based selection. No runtime, tests, or benchmarks were run. ([README](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/README.md), [architecture](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/TECHNICAL_ARCHITECTURE.md), [context builder](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/ContextBuilder.cs))

## Who and what

The official README describes CTX as a CLI and structured cognitive-state repository for agents, alongside local viewer and stdio MCP/ACP adapters. It names Diego Mariano Verrastro and publishes a contact email in the pinned README. The implementation inspected here is a .NET 8 modular application with filesystem JSON persistence. ([README](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/README.md), [architecture](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/TECHNICAL_ARCHITECTURE.md))

## Architecture and data model

CTX separates Domain, Application, Core, Persistence, Providers, Infrastructure, CLI, Viewer, and MCP projects. CLI, viewer, and MCP use the shared application/service model; MCP runs over local stdio, defaults to read-only, and requires explicit write mode for mutations. ([architecture](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/TECHNICAL_ARCHITECTURE.md), [MCP tool parity](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/CTX_MCP_TOOL_PARITY.md), [write tools](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Mcp/Mcp/CtxWriteTools.cs))

A project-local `.ctx/` tree stores configuration, project identity, HEAD and branch references, mutable working state, immutable commit snapshots, graph state, runs, packets, operational artifacts, and metrics. The inspected format is JSON on the local filesystem; the documented index directory is reserved for future indexing. ([storage structure](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/CTX_STRUCTURE.md), [working repository](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Persistence/WorkingContextRepository.cs), [commit repository](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Persistence/CommitRepository.cs))

Typed domain records represent goals, tasks, hypotheses, evidence, decisions, conclusions, runs, and operational artifacts. Core entities carry creator/updater timestamps and relationships. A commit snapshots working state with runbooks and triggers and retains a parent, snapshot hash, diff, and trace metadata. ([domain model](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/DOMAIN_MODEL.md), [commit engine](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/CommitEngine.cs))

## Write, update, delete, and retrieval

**Write.** CLI and MCP expose typed create operations for goals, tasks, hypotheses, evidence, decisions, conclusions, runbooks, and triggers. MCP writes pass through the write-mode repository guard. Persistence stores JSON beneath the project’s `.ctx` directory, and a repository lock coordinates writes. ([write tools](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Mcp/Mcp/CtxWriteTools.cs), [repository guard](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Mcp/Mcp/RepositoryGuard.cs), [working repository](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Persistence/WorkingContextRepository.cs), [write lock](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Persistence/RepositoryWriteLock.cs))

**Update and correction.** Typed updates allow field and state changes; hypotheses also have relate, merge, and supersede operations. Earlier committed snapshots and diffs preserve prior state. The inspected MCP write surface does not expose record deletion; Archived and Superseded are state transitions, not proof of physical erasure. ([write tools](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Mcp/Mcp/CtxWriteTools.cs), [MCP tool parity](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/CTX_MCP_TOOL_PARITY.md), [domain model](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/DOMAIN_MODEL.md), [commit engine](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/CommitEngine.cs))

**Delete.** No explicit delete tool was present in the inspected MCP write surface or parity document. This bounded inspection does not establish behavior across every CLI or internal path, and does not establish erasure from prior commits, exports, or backups. ([write tools](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Mcp/Mcp/CtxWriteTools.cs), [MCP tool parity](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/CTX_MCP_TOOL_PARITY.md), [storage structure](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/CTX_STRUCTURE.md))

**Retrieval.** Agents can request a compact `ctx_plan` or context packet, inspect typed artifacts, and traverse graph, history, diff, or lineage views. Packet selection is bounded and relation-driven. The inspected architecture and storage docs do not describe general full-text memory search. The context builder does not filter selected hypotheses, decisions, or evidence by lifecycle state, so their state labels do not act as exclusion rules in this packet path. ([README](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/README.md), [MCP tool parity](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/CTX_MCP_TOOL_PARITY.md), [context builder](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/ContextBuilder.cs), [domain model](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/DOMAIN_MODEL.md))

## Scope isolation

Each `.ctx` repository is physically local to its project. MCP requests use the configured repository by default; alternate paths require an allowed root and must remain at or below that root. This is a local path boundary, not a multi-tenant authorization service. No cross-project or hostile-caller isolation workload was run. ([storage structure](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/CTX_STRUCTURE.md), [repository guard](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Mcp/Mcp/RepositoryGuard.cs), [README](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/README.md))

## Provenance and evidence

Core entities carry creator/updater and UTC timestamp fields, tags, and related IDs. Evidence records a source, kind, confidence, state, and supported-entity references; context packets retain typed references and a fingerprint. These structures provide lineage, but do not validate external truth or establish claim-level citation quality. ([domain model](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/DOMAIN_MODEL.md), [context builder](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/ContextBuilder.cs), [commit engine](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/CommitEngine.cs))

## Efficiency and observability

Packet assembly has explicit item caps and estimates tokens. Repository configuration includes a packet-token limit and metrics flag. Run orchestration persists packets and runs and updates aggregate run, token, cost, and duration counters. These source structures are not measured latency, cost, or storage outcomes. ([context builder](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/ContextBuilder.cs), [storage structure](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/CTX_STRUCTURE.md), [run orchestration](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/RunOrchestrator.cs))

## Metric-domain evidence

All benchmark domains remain **unmeasured**. Project metric definitions, the versioned fixture, and status record were consulted as contracts only; they were not executed. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Bounded packet assembly was inspected; no answer outcomes were adjudicated. |
| Correction accuracy and stale-value rate | Unmeasured | Update and supersession surfaces exist; no correction probes were run. |
| Deletion leakage | Unmeasured | No MCP delete operation was identified; no post-delete probes were run. |
| Scope isolation | Unmeasured | The repository-path guard was inspected; no paired isolation workload was run. |
| Evidence support and citation coverage | Unmeasured | Typed evidence references exist; generated claims were not adjudicated. |
| Retrieval latency | Unmeasured | No timing samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write/recall probes were run. |
| Tokens and cost | Unmeasured | Counters exist; no usage or charges were measured. |
| Storage efficiency | Unmeasured | JSON persistence was inspected; no corpus size was measured. |

## Limits and unknowns

This review inspected the official README, architecture/domain/storage and MCP parity documents, plus current packet building, write/guard, runbook selection, commit, persistence, and run orchestration sources at the verified SHA. It did not inspect every CLI, provider, viewer, merge, or concurrency path. ([README](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/README.md), [architecture](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/TECHNICAL_ARCHITECTURE.md), [domain model](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/DOMAIN_MODEL.md), [context builder](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/ContextBuilder.cs), [write tools](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Mcp/Mcp/CtxWriteTools.cs))

No CTX runtime, tests, or benchmarks were run. The review therefore does not establish recall quality, correction outcomes, deletion completeness, practical isolation, or performance and storage characteristics. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Contact

The official pinned README publishes **diego.verrastro.ctx@gmail.com** and names Diego Mariano Verrastro. The checked source is [README.md](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/README.md). No profile/commit metadata or third-party directory was used.

## Benchmark status

**Benchmark not run.** No CTX runtime, tests, or benchmarks were run. Source observations remain separate from benchmark outcomes. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [result/status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ctx-open.md)
- [Official repository](https://github.com/diegoxtr/ctx-open)
- [Official main commit feed](https://github.com/diegoxtr/ctx-open/commits/main.atom)
- [Reviewed head c31d84e07c830f2d126f780f65ad2b0228fe54eb](https://github.com/diegoxtr/ctx-open/commit/c31d84e07c830f2d126f780f65ad2b0228fe54eb)
- [Pinned README](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/README.md)
- [Pinned technical architecture](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/TECHNICAL_ARCHITECTURE.md)
- [Pinned domain model](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/DOMAIN_MODEL.md)
- [Pinned storage structure](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/CTX_STRUCTURE.md)
- [Pinned context builder](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/ContextBuilder.cs)
- [Pinned runbook selection](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/OperationalRunbookSelection.cs)
- [Pinned application service](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/CtxApplicationService.cs)
- [Pinned MCP write tools](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Mcp/Mcp/CtxWriteTools.cs)
- [Pinned MCP repository guard](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Mcp/Mcp/RepositoryGuard.cs)
- [Pinned MCP tool parity](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/docs/CTX_MCP_TOOL_PARITY.md)
- [Pinned commit engine](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/CommitEngine.cs)
- [Pinned working-context repository](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Persistence/WorkingContextRepository.cs)
- [Pinned commit repository](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Persistence/CommitRepository.cs)
- [Pinned write lock](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Persistence/RepositoryWriteLock.cs)
- [Pinned run orchestration](https://github.com/diegoxtr/ctx-open/blob/c31d84e07c830f2d126f780f65ad2b0228fe54eb/Ctx.Core/RunOrchestrator.cs)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project result/status record](../results/initial-baselines-status.json)
