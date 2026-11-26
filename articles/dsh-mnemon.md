# dsh-mnemon

## Identity and review pin

- Catalog ordinal: 202
- System: dsh-mnemon
- Slug: `dsh-mnemon`
- Listed repository: https://github.com/omdsh-dev/dsh-mnemon
- Roster attribution: explicit repository locator; the pinned Atlas entry is retained for curated identity and locator context only ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-mnemon.md)).
- Canonical upstream: https://github.com/omdsh-dev/dsh-mnemon
- Default branch: `main`
- Reviewed full head: [ee53e0dc5004adecd09a7a23208e163901fc5699](https://github.com/omdsh-dev/dsh-mnemon/commit/ee53e0dc5004adecd09a7a23208e163901fc5699)
- Review timestamp: 2026-11-25T11:40:55Z (UTC; 2026-11-25 03:40:55 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

dsh-mnemon is a composable DeepSeek Harness plugin that gives each turn a pinned View over three memory tiers: compact Runtime Memory injected into context, larger Project Documents searched as needed, and Provider-backed Memory Spaces recalled on demand. A Strategy controls which sources and operations are available to the turn. ([README](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/README.md), [storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md))

## Who and what

The official README describes dsh-mnemon as a plugin for DeepSeek Harness with pluggable Sources, Strategies, and Enhancements, a management interface, and public extension SDKs. It is a host plugin rather than a standalone hosted memory service. ([README](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/README.md))

The catalog resolves ordinal 202 to dsh-mnemon, slug `dsh-mnemon`, listed repository `https://github.com/omdsh-dev/dsh-mnemon`, with explicit locator attribution. The pinned Atlas entry is included only for roster identity and locator attribution, not as evidence for the assessment. ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-mnemon.md))

The official repository page identifies `main` as the default branch. Its official main feed reports full head ee53e0dc5004adecd09a7a23208e163901fc5699, updated 2026-11-24T18:15:57Z; reviewed source links below pin that SHA. ([repository](https://github.com/omdsh-dev/dsh-mnemon), [main feed](https://github.com/omdsh-dev/dsh-mnemon/commits/main.atom), [head commit](https://github.com/omdsh-dev/dsh-mnemon/commit/ee53e0dc5004adecd09a7a23208e163901fc5699))

## Architecture and data model

The default composition has three independent memory Sources. Runtime Memory holds compact facts for direct prompt context; Project Documents hold larger structured notes searched and read when useful; Memory Spaces hold durable facts and relationships recalled on demand. A Strategy decides what stays resident and which sources can be searched or written. Core validates the composition into an immutable View that the Host pins to the turn. ([README](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/README.md), [storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md))

Runtime Memory stores its authoritative state in `runtime/memories.json` and derives `USER.md` and `MEMORY.md`. Records include content, target, timestamps, importance, optional branch labels, and optional pin state. Branch labels filter the turn projection when the workspace branch is known; detached HEAD and non-git workspaces project all entries. ([storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md), [Runtime controller](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/controller.ts))

Project Documents are managed Markdown plus `documents/index.json`, which tracks IDs, titles, status, source paths, session and revision metadata, hashes, sizes, and references to Memory Spaces. Active documents are the default search set; archived documents may be represented by a cold reference while the original text is archived. ([storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md))

A Memory Space is a named Provider-backed scope. Mnemon Native uses local Mnemon stores; third-party Providers can use remote services or local processes. Relationship graphs, deletion, browsing, and enumeration depend on Provider capabilities. ([README](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/README.md), [storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md), [Memory Spaces Source guide](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-memory-spaces/README.md))

The Runtime Source declares exact-snapshot consistency. Its search route is bounded to four calls, 50 results, and 16,000 characters by its contract. Each result carries revision and entry metadata. These are source-level limits, not measured performance. ([Runtime Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/source.ts))

## Write, update, delete, and retrieval

**Write and update.** Runtime mutations support add, replace, and remove for the user or memory target. Replacement and removal match old text within the selected target; missing and ambiguous matches are rejected. The controller persists the JSON source and Markdown projections using temporary files and rename under a lock, with revision checks. ([Runtime Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/source.ts), [Runtime controller](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/controller.ts))

Runtime defaults to a 4 KiB user profile and 10 KiB working memory. With the Layered strategy, an overflowing write can start capacity maintenance. Exact entries are routed to eligible Memory Spaces or a local archive before the remaining Runtime state commits under a revision fence. A Provider write cannot share the same filesystem transaction, so a later conflict can leave an archived duplicate while preserving current Runtime entries. ([storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md), [Runtime controller](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/controller.ts))

Documents are managed Markdown with revision metadata. Source paths are references only, constrained to the session workspace for new writes, and are not modified by the plugin. Search defaults to active documents and updates access metadata. The reviewed docs do not specify guaranteed erasure across indexes, archives, backups, and copies. ([storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md))

Memory Spaces support explicit remember, forget by exact item ID, linking, and space management. Remember requires an explicit destination when the View does not contain exactly one active writable space; mutations outside the View grant are rejected. Native forget is a soft delete, and other Providers define their own behavior. ([Memory Spaces Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-memory-spaces/src/source.ts), [storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md))

Retrieval depends on the selected Strategy. The default Layered strategy injects Runtime Memory, searches then reads Documents when relevant, and recalls from active Memory Spaces when needed. Runtime search reads the exact snapshot associated with the turn; Memory Space operations are bounded by the View and admitted evidence. General strategy exposes sources within a shared budget. ([README](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/README.md), [storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md), [Runtime Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/source.ts), [Memory Spaces Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-memory-spaces/src/source.ts))

Correction semantics vary by tier: Runtime replaces an exact entry, Documents retain revisions, and Memory Spaces follow Provider-specific mutation behavior. The inspected sources do not establish one cross-tier fact identity or revision ledger linking every replacement to its earlier value. ([Runtime controller](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/controller.ts), [storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md), [Memory Spaces Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-memory-spaces/src/source.ts))

## Scope isolation

A turn View and source grants constrain which memory components and data the model-facing turn can use. Storage location and conversation participation are separate controls: global or custom storage roots can allow Documents or Memory Spaces to be shared across workspaces. Runtime, Documents, and Memory Spaces do not automatically flow into other agents' contexts, but agents using the same Native root and Store can share durable facts. ([storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md), [Runtime Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/source.ts), [Memory Spaces Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-memory-spaces/src/source.ts))

These are code and documentation observations, not an isolation guarantee. The security policy states that Sources, Providers, and Strategies run as ordinary JavaScript in the Host process and are not sandboxed. ([security policy](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/SECURITY.md))

## Provenance and evidence

Runtime search results carry a turn View ID, route ID, source instance, timestamp, revision, and item metadata. Documents carry source path, session, revision, and content hash metadata. Memory Space results use View-scoped read grants; mutations return receipts. These fields make retrieved content traceable to source and operation, but do not prove that the remembered claim is true or current. ([Runtime Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/source.ts), [storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md), [Memory Spaces Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-memory-spaces/src/source.ts))

## Efficiency and observability

The three tiers avoid injecting all historical material into every prompt: Runtime is bounded, Documents and Memory Spaces are read on demand, and Strategies impose composition budgets. The UI exposes what a turn read and wrote, while the storage model documents byte limits and archive behavior. These are design and inspection surfaces; no latency, token, cost, or storage measurements were collected. ([README](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/README.md), [storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md))

## Metric-domain evidence

All benchmark domains remain **unmeasured**. The fixture and metric definitions were read as project references only; they were not executed. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Layered and General retrieval and View-scoped evidence exist in documentation/source; no workload was run. |
| Correction accuracy and stale-value rate | Unmeasured | Runtime replacement, document revisions, and provider-specific mutations are visible; no correction cases were evaluated. |
| Deletion leakage | Unmeasured | Runtime removal, document archive/delete paths, and provider-dependent forget are described; no residual-data probes were run. |
| Scope isolation | Unmeasured | View grants and configurable storage scopes are source-visible; no cross-scope probes were run. |
| Evidence support and citation coverage | Unmeasured | Read grants and evidence items bind data to a View; no claims were adjudicated. |
| Retrieval latency | Unmeasured | Search and recall contracts were inspected; no timing samples were collected. |
| Write-to-recall delay | Unmeasured | Writes and recalls use different operations and may depend on providers; no timed probes were run. |
| Tokens and cost | Unmeasured | Prompt budgets and optional provider/model paths are documented; no token or cost data was collected. |
| Storage efficiency | Unmeasured | JSON, Markdown, indexes, local stores and remote provider boundaries were inspected; no corpus-attributed size was measured. |

Project benchmark status is [`not_run`](../data/system-reviews/dsh-mnemon.json); see [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json). These are evaluation materials, not dsh-mnemon results.

## Limits and unknowns

- Scope isolation depends on Host composition, configured storage scope, Provider behavior, and in-process extension code. Source inspection did not test hostile callers or cross-workspace leakage. ([storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md), [security policy](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/SECURITY.md))
- Native Memory Space forget is soft deletion; third-party Provider deletion semantics differ. The review did not inspect every Provider or test residual data in local stores, backups, exports, or remote services. ([storage model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md))
- The project documents that deterministic secret detection is absent. It also states that Extensions are not sandboxed. ([security policy](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/SECURITY.md))
- The review covered selected official documentation, Runtime Source/controller, Memory Spaces Source, and security policy at the verified head. It did not audit every Provider, Strategy, document implementation, Host permission route, migration, or UI flow.
- No dsh-mnemon runtime, tests, or benchmarks were run; all metric domains remain unmeasured. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Contact

The official pinned SECURITY.md publishes `grivn.wang@gmail.com` for private vulnerability reports. The exact checked sources are the [README](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/README.md) and [SECURITY.md](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/SECURITY.md). No profile or commit metadata or third-party directory was used.

## Benchmark status

**Benchmark not run.** No dsh-mnemon runtime, tests, or benchmarks were run. Source observations remain separate from project benchmark outcomes. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Official repository](https://github.com/omdsh-dev/dsh-mnemon) · [main commit feed](https://github.com/omdsh-dev/dsh-mnemon/commits/main.atom) · [verified current head](https://github.com/omdsh-dev/dsh-mnemon/commit/ee53e0dc5004adecd09a7a23208e163901fc5699).
- [Pinned README](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/README.md) · [storage and memory model](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/docs/en/reference/storage-model.md) · [security policy](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/SECURITY.md).
- [Runtime Memory Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/source.ts) · [Runtime Memory controller](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-runtime/src/controller.ts).
- [Memory Spaces Source](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-memory-spaces/src/source.ts) · [Memory Spaces Source guide](https://github.com/omdsh-dev/dsh-mnemon/blob/ee53e0dc5004adecd09a7a23208e163901fc5699/plugins/dsh-mnemon-source-memory-spaces/README.md).
- [Catalog roster entry](../data/memory-systems.json) · [pinned Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-mnemon.md).
- [Metric definitions](../METRICS.md) · [benchmark fixture](../fixtures/memory-benchmark-v1.json) · [execution status](../results/initial-baselines-status.json).
