# Daem0nMCP

## Identity and review pin

- Catalog ordinal: 179
- System: Daem0nMCP
- Slug: `daem0n-mcp`
- Listed repository: https://github.com/9thLevelSoftware/Daem0n-MCP
- Roster attribution: the catalog marks the repository locator explicit; the pinned Atlas entry is retained only for curated identity and locator context ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/daem0n-mcp.md)).
- Canonical upstream: https://github.com/9thLevelSoftware/Daem0n-MCP
- Default branch: `main`
- Reviewed full head: [572d58ca7ec2fe2600665b44d2996d74f393e1cd](https://github.com/9thLevelSoftware/Daem0n-MCP/commit/572d58ca7ec2fe2600665b44d2996d74f393e1cd)
- Review timestamp: 2026-11-25T10:29:16Z (UTC; 2026-11-25 02:29:16 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub’s repository page identifies `main` as the default branch. Its official main Atom feed reports full head `572d58ca7ec2fe2600665b44d2996d74f393e1cd`, updated at 2026-11-19T23:01:16Z; the commit page identifies the same revision. ([repository](https://github.com/9thLevelSoftware/Daem0n-MCP), [main history](https://github.com/9thLevelSoftware/Daem0n-MCP/commits/main.atom), [head commit](https://github.com/9thLevelSoftware/Daem0n-MCP/commit/572d58ca7ec2fe2600665b44d2996d74f393e1cd))

## Summary

Daem0nMCP is a self-hostable MCP memory and decision-governance server for AI-agent workspaces. The current v7 interface uses workspace-scoped calls, an append-only event store with a canonical SQLite projection, memory retrieval, and a preflight/counsel protocol for protected changes. The repository README says v7 is not yet published; its v6 migration material is historical context, so this review describes the v7 paths inspected at the pinned head. ([README](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/README.md), [event store](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/event_store.py), [v7 operations guide](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/docs/v7-operations.md))

## Who and what

The public repository is maintained under the 9thLevelSoftware GitHub organization. Its README describes Daem0nMCP as an AI memory and decision system and documents stdio and Streamable HTTP MCP transports. This review treats it as a deployable server/library, not a hosted memory service. ([repository](https://github.com/9thLevelSoftware/Daem0n-MCP), [README](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/README.md))

## Architecture and data model

The v7 API separates strict wire models, application routing and admission, operation handlers, workspace resolution, event persistence, and retrieval composition. The v7 router resolves a caller-supplied opaque workspace ID through the server’s workspace resolver and applies the covenant gate before dispatching an admitted operation. ([v7 models](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/models.py), [application router](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/application.py), [v7 operations guide](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/docs/v7-operations.md))

The server stores each registered workspace in its own project-local Daem0n storage by default. The SQLite database uses a format-7 generation; `record_operations.py` describes `memory_records` as a canonical projection and says mutations append complete semantic state through `EventStore` rather than directly updating that projection. Record fields include type, content and hash, rationale, context JSON, tags, relative file path, pin/archive state, outcome/worked state, importance and surprise scores, source client/model, stream version, source event ID, and timestamps. ([README](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/README.md), [database manager](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/database.py), [record operations](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/record_operations.py))

The event command records workspace and stream identity, event type, occurred/recorded times, actor, payload, optional causation/correlation IDs, schema version, and expected stream version. Appended-event results include event and payload hashes, stream version, and previous event hash. ([event store](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/event_store.py))

## Write, update, delete, and retrieval

**Write.** The v7 `memory_store_batch` operation passes records and an idempotency key to the canonical batch writer. Its record handler authorizes the workspace and schedules projection work after a successful mutation. This is evidence of the code path and replay control, not a measured write guarantee. ([record operations](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/record_operations.py), [application router](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/application.py))

**Update and archive.** Pin and archive changes are separate authorized operations. The handler appends `memory.pin_set` and `memory.archive_set` state events and schedules post-commit projection work. The inspected v7 record-operation surface does not show in-place edits to the canonical projection; broader correction semantics depend on event and maintenance operations not fully traced here. ([record operations](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/record_operations.py), [event store](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/event_store.py))

**Delete.** The reviewed record-operation mapping exposes store, pin, archive, file recall, text search, and session updates, but no per-record delete handler. The v7 tool registry separately lists destructive maintenance operations such as pruning and duplicate cleanup; their complete selection and physical-erasure semantics were not traced in this review. A hard-delete or deletion-leak claim is therefore unknown. ([record operations](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/record_operations.py), [maintenance operations](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/maintenance_operations.py), [v7 registry](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/registry.py))

**Retrieval.** The public interface documents `memory_recall`, `memory_search_text`, and file recall. Record operations construct lexical search through a SQLite retrieval provider with a bounded candidate count and timeout. The shared retrieval composer filters evidence to a token budget, builds a citation manifest from evidence references, reports provider diagnostics and token usage, and can abstain with `NO_POLICY_VALID_EVIDENCE` when no candidate survives. These are source observations; answer accuracy and abstention quality are unmeasured. ([README](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/README.md), [record operations](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/record_operations.py), [federated retrieval](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/federated_retrieval.py), [v7 models](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/models.py))

## Scope isolation

V7 operations require a resolved workspace object and authorize against the request’s workspace before accessing its active storage. The README says clients pass opaque workspace IDs, while the server owns workspace registration and access grants; IDs themselves are not credentials. The repository also documents linked workspaces and federated retrieval, so the workspace boundary is the local storage and authorization unit, while explicitly linked retrieval can cross that boundary. No isolation workload or adversarial access check was run. ([README](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/README.md), [application router](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/application.py), [runtime services](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/runtime_services.py), [federated retrieval](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/federated_retrieval.py))

## Provenance and evidence

The append-only event envelope tracks actor, event time, payload, stream version, causation/correlation, and hash-chain fields. The projected record also retains source-client/model and source-event identifiers. Retrieval’s evidence model carries source references, channels, applicability and changed-binding context; a citation manifest maps rendered citations to evidence references. This supplies record and retrieval lineage in the inspected API. It does not establish that generated answers always cite or faithfully support every claim. ([event store](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/event_store.py), [record operations](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/record_operations.py), [v7 models](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/models.py), [federated retrieval](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/federated_retrieval.py))

## Efficiency and observability

Code-level controls include batched writes, idempotency, a four-worker bound for record operations, a 1,000-candidate lexical-search cap, a five-second SQLite lexical-provider timeout, post-commit projection scheduling, and retrieval token accounting/provider diagnostics. These are implementation limits and reporting surfaces, not latency or cost results. ([record operations](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/record_operations.py), [federated retrieval](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/federated_retrieval.py))

## Metric-domain evidence

- Answerable recall and abstention — **unmeasured**; retrieval and a no-valid-evidence abstention path are source-visible, but no cases were adjudicated.
- Correction accuracy and stale-value rate — **unmeasured**; event and state-update paths were inspected, but correction probes were not run.
- Deletion leak rate — **unmeasured**; per-record deletion and physical-erasure behavior were not established.
- Scope-isolation leak rate — **unmeasured**; workspace routing and grants are source-visible, but no paired-scope workload was run.
- Evidence support precision and citation coverage — **unmeasured**; evidence references and citation manifests exist, but answer claims were not scored.
- Retrieval latency and write-to-recall delay — **unmeasured**; no runtime timing was collected.
- Tokens and cost — **unmeasured**; retrieval token-budget accounting is present, but no provider usage or charges were collected.
- Storage efficiency — **unmeasured**; no corpus-attributed storage measurements were collected.

Metric definitions are in [METRICS.md](../METRICS.md); execution status is tracked separately in [the project status record](../results/initial-baselines-status.json). The benchmark fixture is linked for context only ([fixture](../fixtures/memory-benchmark-v1.json)). No benchmark, system runtime, or tests were run.

## Limits and unknowns

- This is a source review of selected v7 API, event, storage, retrieval, and operations-guide files at one pinned commit. It does not trace every provider, projection job, federation policy, migration, client integration, or maintenance implementation.
- The README says v7 is not yet published; package/release behavior can differ from the inspected checkout.
- The code shows event append and projection boundaries, but this review does not establish transaction recovery, complete correction lifecycle, or physical deletion behavior across every maintenance path.
- Workspace authorization and evidence structures are inspected implementation surfaces. Their security, retrieval quality, and answer-grounding outcomes were not measured.
- No Daem0nMCP runtime, tests, or benchmark workload was executed.

## Benchmark status

**Benchmark not run.** The project metric definitions, fixture, and execution-status record are linked above. Source observations are not benchmark results. ([METRICS.md](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Official GitHub repository](https://github.com/9thLevelSoftware/Daem0n-MCP)
- [Official main-branch commit feed](https://github.com/9thLevelSoftware/Daem0n-MCP/commits/main.atom)
- [Verified head commit](https://github.com/9thLevelSoftware/Daem0n-MCP/commit/572d58ca7ec2fe2600665b44d2996d74f393e1cd)
- [Official README at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/README.md)
- [V7 operations guide at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/docs/v7-operations.md)
- [V7 wire models at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/models.py)
- [V7 application router at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/application.py)
- [V7 record operations at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/record_operations.py)
- [V7 event store at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/event_store.py)
- [V7 database manager at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/database.py)
- [V7 runtime services at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/runtime_services.py)
- [V7 federated retrieval at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/federated_retrieval.py)
- [V7 maintenance operations at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/maintenance_operations.py)
- [V7 tool registry at reviewed SHA](https://github.com/9thLevelSoftware/Daem0n-MCP/blob/572d58ca7ec2fe2600665b44d2996d74f393e1cd/daem0nmcp/api/v7/registry.py)
- [Project metric definitions](../METRICS.md)
- [Project fixture](../fixtures/memory-benchmark-v1.json)
- [Project execution status](../results/initial-baselines-status.json)

