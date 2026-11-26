# Dexto

## Identity and review pin

- **Catalog position:** 190, “Dexto”; slug `dexto`.
- **Listed repository:** [truffle-ai/dexto](https://github.com/truffle-ai/dexto); roster locator status is explicit. The pinned Atlas entry is retained only as curated identity and repository attribution.
- **Canonical upstream:** public repository [truffle-ai/dexto](https://github.com/truffle-ai/dexto), default branch `main`. The official repository page showed `main`; its official [main commit feed](https://github.com/truffle-ai/dexto/commits/main.atom) reported full head `c34d726f7d1addfe43c137028f924fc6981c2f03` at 2026-11-25T06:48:20Z. `git ls-remote --symref` resolved HEAD and `refs/heads/main` to that SHA, and a shallow checkout matched.
- **Reviewed:** 2026-11-25 11:05:33 UTC (2026-11-25 03:05:33 PST; America/Los_Angeles).
- **Status:** Reviewed from selected code and documentation at the verified main SHA. Benchmark not run.

## Summary

Dexto is an agent harness whose core package includes a small persistent-memory facility. Memories are validated records with content, timestamps, optional tags, and source/pinned metadata. The manager exposes create, read, update, delete, and filtered listing; configured agents can inject a bounded list into their system prompt. The inspected implementation does not provide semantic memory search or a per-memory user/session scope.

## Who and what

The official README calls Dexto an agent harness and says it is built by Truffle AI. The repository includes a TypeScript SDK, CLI, server, and storage packages. The official website publishes `founders@dexto.ai`; that is stored as the published contact address and is not inferred from commit metadata.[[README](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/README.md)] [[official website](https://dexto.ai/)]

## Architecture and data model

The core `Memory` record has a generated ID, content, creation and update timestamps, optional tags, and optional metadata. The metadata schema defines `source` as `user` or `system` and a Boolean `pinned` flag, while allowing custom fields. Validation caps content at 10,000 characters, tags at ten, and each tag at 50 characters.[[types](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/types.ts)] [[schemas](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/schemas.ts)]

The `MemoryManager` wraps a five-operation `MemoryStore` contract. The default database-backed store writes records under `memory:item:<id>`; an in-memory implementation is also present. Storage is injected into the manager, so the concrete persistence behavior depends on the selected Dexto storage configuration.[[manager](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/manager.ts)] [[store contract](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/storage/memories/types.ts)] [[database store](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/storage/stores/backend.ts)] [[in-memory store](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/storage/stores/in-memory.ts)]

Memory tools expose list, get, create, update, and delete through the agent's manager. A separate `MemoryContributor` can put listed records into the system prompt. Its configuration defaults to disabled; when enabled it can limit results, include timestamps/tags, and select pinned memories only.[[memory tools](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/tools-lifecycle/src/memory-tools.ts)] [[prompt contributor](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/systemPrompt/contributors.ts)] [[memory config](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/schemas.ts)]

## Write, update, delete, and retrieval

**Write.** The manager validates the input, generates a 12-character ID, stamps creation and update times, validates the complete record, and calls the store. The tool defaults source to `system` and pinned to false when omitted.[[manager](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/manager.ts)] [[memory tools](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/tools-lifecycle/src/memory-tools.ts)]

**Update.** Updates address an existing ID, replace supplied content or tags, merge supplied metadata, and set `updatedAt`. The database-backed store overwrites the record at the same key. The inspected data model has no revision history or supersession chain.[[manager](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/manager.ts)] [[database store](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/storage/stores/backend.ts)]

**Delete.** Deletion first reads the ID to check existence, then calls the store's delete operation. The database-backed implementation removes the key. No tombstone or memory-specific deletion audit is present in the inspected paths; this does not establish erasure from external database backups or storage-engine remnants.[[manager](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/manager.ts)] [[database store](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/storage/stores/backend.ts)]

**Retrieval.** `get` reads by ID. `list` obtains the store's records, filters in process by tags, source, and pinned status, sorts newest-updated first, then applies offset and limit. The database implementation lists matching keys and loads each record sequentially. The prompt contributor uses this listing path; there is no vector or semantic query in the reviewed memory manager.[[manager](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/manager.ts)] [[database store](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/storage/stores/backend.ts)] [[prompt contributor](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/systemPrompt/contributors.ts)]

**Scope isolation.** Memory records have no user, project, workspace, agent, or session field, and their database keys contain only the generated ID. The manager has an explicit TODO for multi-scope memory. The prompt contributor receives a dynamic context argument but the inspected implementation does not use it to filter memory. An agent's configured storage may provide an outer deployment boundary; this source inspection does not prove tenant isolation for a particular deployment.[[types](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/types.ts)] [[manager](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/manager.ts)] [[database store](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/storage/stores/backend.ts)] [[prompt contributor](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/systemPrompt/contributors.ts)]

**Provenance and evidence.** The record's `source` field distinguishes user and system; tags and pinned status are available for organization and prompt selection. The inspected schema has no source URI, quote, evidence span, confidence, trust state, or mutation history. These fields therefore identify record metadata, not factual support.[[types](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/types.ts)] [[schemas](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/schemas.ts)]

**Efficiency and observability.** Listing loads the full store result before in-process filtering and sorting; the database-backed implementation fetches each matching record in a loop. Prompt injection can be bounded with a limit or restricted to pinned items. Manager create/update/delete paths log the operation and ID, while the prompt contributor logs loaded count or errors. No memory-specific latency or token metrics were identified in the inspected files; no performance or cost measurements were collected.[[manager](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/manager.ts)] [[database store](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/storage/stores/backend.ts)] [[prompt contributor](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/systemPrompt/contributors.ts)]

## Metric-domain evidence

- **Answerable recall and abstention:** the inspected retrieval path is ID lookup and filtered listing; no retrieval accuracy or abstention workload was run.
- **Correction and stale values:** update overwrites the current record; no correction sequence or stale-value probe was run.
- **Deletion leakage:** the store deletes the record key; no post-delete retrieval or residual-storage check was run.
- **Scope isolation:** the memory schema and key do not carry an explicit scope; no cross-user or cross-agent isolation workload was run.
- **Evidence and citations:** source/pinned metadata exist, but no evidence-grounding evaluation was run.
- **Retrieval latency:** no latency workload was run.
- **Write-to-recall delay:** no first-recall timing was measured.
- **Tokens and cost:** no token or cost measurements were collected.
- **Storage efficiency:** no storage-footprint measurement was collected.

Project metric definitions are in [METRICS.md](../METRICS.md); the shared execution record is [initial-baselines-status.json](../results/initial-baselines-status.json). The [benchmark fixture](../fixtures/memory-benchmark-v1.json) describes a planned workload, not a measured result.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Contact

The official [Dexto website](https://dexto.ai/) publishes `founders@dexto.ai`. The structured review record stores the exact checked URL.

## Limits and unknowns

The inspected source establishes the memory manager and store behavior, but not how every agent configuration or deployment chooses its storage backend. The older [memory guide](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/docs/examples/memory.md) describes automatic memory creation/retrieval and configurable local/Redis/PostgreSQL/SQLite storage; current core code instead exposes explicit memory tools and optional prompt injection (disabled by default). The guide and implementation describe different levels or versions of the feature; this review follows the pinned code for runtime behavior. No Dexto runtime, tests, or benchmarks were executed, so isolation, retrieval quality, erasure guarantees, latency, token usage, cost, and storage efficiency remain unknown.[[memory guide](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/docs/examples/memory.md)] [[memory config](https://github.com/truffle-ai/dexto/blob/c34d726f7d1addfe43c137028f924fc6981c2f03/packages/core/src/memory/schemas.ts)] [[project metrics](../METRICS.md)]

## Benchmark status

**Benchmark not run.** No Dexto runtime, tests, or benchmark workloads were executed. See [project metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and the [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and SHA-pinned source URLs are recorded in [dexto.json](../data/system-reviews/dexto.json). The [pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dexto.md) is included only for curated identity and repository attribution, not as assessment evidence.
