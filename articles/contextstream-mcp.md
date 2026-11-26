# ContextStream MCP Server — source review

## Identity and review pin

- **Roster ordinal / name / slug:** 150 / ContextStream MCP Server / `contextstream-mcp`
- **Listed repository locator:** https://github.com/contextstream/mcp-server
- **Roster attribution:** `repository_status: explicit`; the Atlas locator is retained for identity only. [Curated roster](../data/memory-systems.json) · [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/contextstream-mcp.md)
- **Canonical upstream / default branch:** [contextstream/mcp-server](https://github.com/contextstream/mcp-server) / `main`
- **Reviewed head:** [`c9d4cfe5727a26cc00b39736c9371dd95886a31e`](https://github.com/contextstream/mcp-server/commit/c9d4cfe5727a26cc00b39736c9371dd95886a31e)
- **Official main feed:** [main commit feed](https://github.com/contextstream/mcp-server/commits/main.atom) reported this head at 2026-11-25 01:11:02 UTC.
- **Reviewed:** 2026-11-25 09:07:01 UTC (2026-11-25 01:07:01 PST; America/Los_Angeles)
- **Status:** Reviewed from source; benchmark not run

## Summary

ContextStream MCP Server is an open-source Rust client and MCP tool layer for a hosted context platform. It exposes memory, project, code and document context operations to agent clients. The hosted API and persistence backend are separate and absent from this repository, so this review describes visible client behavior and official documentation, while treating server-side storage and guarantees as unknown. No runtime, benchmark, or test was run. [README](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/README.md>) · [Architecture](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/docs/architecture.md>)

## Architecture and data model

The repository includes local stdio and HTTP transport, MCP domain tools, shared types, session and checkout identity logic, and setup and installer code. The Rust memory domain exposes tools for memory nodes and events, tasks, todos, diagrams, documents, roadmaps and transcript search, and delegates operations through the hosted client. The repo does not contain a local canonical memory database; its architecture document excludes the hosted backend and production deployment. [Architecture](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/docs/architecture.md>) · [memory tool layer](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/memory.rs>)

The client handles tool-level workspace/project scope and keeps a short-lived in-process search cache. The cache lasts 30 seconds and is bounded to 64 entries overall, eight per caller and 128 KiB per entry. Memory search also has a six-second tool timeout, with shorter internal document-search timeouts. These are implementation limits, not performance measurements. [Memory tool source](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/memory.rs>)

## Write, update, delete, and retrieval

**Write and update.** The memory tool layer exposes create and update operations for memory nodes and events, as well as typed operations for other context records. It resolves workspace/project scope before dispatching through the hosted client. The private API handles canonical persistence and validation; its transaction and conflict behavior cannot be established from this code. No memory was written during this review. [Memory tool source](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/memory.rs>) · [Scope resolver](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/scope.rs>) · [Architecture](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/docs/architecture.md>)

**Delete.** Irreversible actions are grouped in a dedicated `delete` tool marked destructive. Its registry includes deletion of memory nodes, events, tasks, todos, diagrams, documents and transcripts. Project purge removes indexed server-side project content and is documented as irreversible; `project.forget_local` removes the local machine mapping without deleting server data. Backend erasure, replica and retention behavior was not inspected or tested. [Delete-action registry](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/destructive.rs>) · [Data handling](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/docs/data-handling.md>)

**Retrieval.** Memory tools include typed reads and search; the client resolves scope and briefly caches eligible rendered search responses. Product documentation describes code/document indexing, saved decisions and traceable sources, and instructs agents to cite retrieved sources. Search ranking, evidence selection and answer quality are partly hosted-service behavior and cannot be verified here. No retrieval call was made. [README](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/README.md>) · [Memory tool source](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/memory.rs>) · [Scope resolver](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/scope.rs>)

## Scope isolation

The client resolves workspace and project identifiers from explicit arguments, session state, authentication overrides and configured defaults. It can resolve a project name within a workspace and checks that a selected project belongs to that workspace for reads. This is client-side scope handling; hosted authorization and tenant isolation guarantees are outside the repository. No cross-scope probe was run. [Scope resolver](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/scope.rs>) · [Architecture](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/docs/architecture.md>)

## Provenance and evidence

The README describes traceable sources and citation-oriented use. The data-handling document specifies repository content and metadata sent during indexing, along with ignore rules, transcript controls and project purge. The client code cannot establish how the hosted backend persists per-memory provenance, selects evidence, or validates that citations support an answer. Those properties remain unknown from this review. [README](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/README.md>) · [Data handling](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/docs/data-handling.md>) · [Architecture](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/docs/architecture.md>)

## Efficiency and observability

The client applies cache and timeout bounds and provides setup/status and diagnostic surfaces. The README reports 61 ms median and 127 ms p95 server-side search in an October 27 production run; these are project-reported figures and were not reproduced. This review collected no latency, write-to-recall delay, token, cost or storage measurements. [README](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/README.md>) · [Memory tool source](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/memory.rs>)

## Metric-domain evidence

All benchmark domains remain **unmeasured** here: answerable retrieval and abstention; correction accuracy and stale values; deletion leakage; scope isolation; evidence support and citation coverage; latency; write-to-recall delay; tokens; cost; storage; and observability. The project’s metric definitions and fixture describe the evaluation protocol, not ContextStream results. [Metric definitions](../METRICS.md) · [benchmark status](../results/initial-baselines-status.json) · [benchmark fixture](../fixtures/memory-benchmark-v1.json)

## Limits and unknowns

This review inspected the official README, architecture and data-handling docs, plus the memory tool layer, scope resolver and destructive-action registry at the pinned head. It did not inspect every client or tool family, hosted endpoint, database, retention job or deployment configuration. Backend schema, authorization, write/update conflict semantics, ranking, provenance retention, and deletion completeness remain unknown. The documented indexing and transcript flows are product statements; this review was not a privacy or erasure audit. [Architecture](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/docs/architecture.md>) · [Data handling](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/docs/data-handling.md>) · [Memory source](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/memory.rs>) · [Scope source](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/scope.rs>) · [Delete source](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/crates/mcp-tools/src/domains/destructive.rs>)

## Benchmark status

**Not run.** No ContextStream system, benchmark, or test was run. The project metrics, status file and fixture are protocol material only. [Metric definitions](../METRICS.md) · [benchmark status](../results/initial-baselines-status.json) · [benchmark fixture](../fixtures/memory-benchmark-v1.json)

## Contact

The official pinned README and SUPPORT.md were checked; neither publishes an email. SUPPORT.md directs account, billing, hosted-service, and customer-data questions to ContextStream's support channel. [Pinned README](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/README.md>) · [Pinned SUPPORT.md](<https://github.com/contextstream/mcp-server/blob/c9d4cfe5727a26cc00b39736c9371dd95886a31e/SUPPORT.md>)
