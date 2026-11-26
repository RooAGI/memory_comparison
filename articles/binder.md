# Binder

## Identity and review pin

- **System:** Binder
- **Curated position:** 94
- **Slug:** `binder`
- **Listed repository:** [mpazik/Binder](https://github.com/mpazik/Binder)
- **Canonical repository:** [mpazik/Binder](https://github.com/mpazik/Binder)
- **Default branch:** `main`
- **Reviewed head:** [`f72189f6107368f8712915254d52897b3022ef4f`](https://github.com/mpazik/Binder/commit/f72189f6107368f8712915254d52897b3022ef4f)
- **Reviewed:** 2026-11-24 23:38:42 UTC (15:38:42 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/binder.md), retained for identity and listed-locator attribution only.

The curated roster resolves position 94 to Binder, slug `binder`, with listed locator `https://github.com/mpazik/Binder` and the Atlas source URL above. Official GitHub repository metadata confirms the canonical public repository and `main` as its default branch. The official GitHub commits API for `main` returned full head `f72189f6107368f8712915254d52897b3022ef4f`; the reviewed source links below pin to that SHA. The roster's older pin is not used as assessment evidence.[[curated roster](../data/memory-systems.json)] [[repository metadata](https://api.github.com/repos/mpazik/Binder)] [[main head metadata](https://api.github.com/repos/mpazik/Binder/commits/main)] [[reviewed head](https://github.com/mpazik/Binder/commit/f72189f6107368f8712915254d52897b3022ef4f)]

## Summary

Binder is a local-first, structured knowledge base for records, configuration, and their relationships. It stores workspace data in SQLite, exposes operations through a TypeScript repository API, CLI, MCP, editor integrations, and a local HTTP API, and represents edits as hash-linked transactions. This review describes inspected source behavior; it does not establish runtime quality or benchmark performance.[[README](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/README.md>)][[repository implementation](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/knowledge-graph.ts)]

## Who and what

The official repository is maintained under the GitHub account mpazik. Its README describes Binder as a headless knowledge base/database for tools, scripts, agents, and humans, with Markdown files as a navigable editing surface over structured data. It is a local software system and libraries/CLI, not a hosted memory service. The README names no human maintainer in its project description.[[repository metadata](https://api.github.com/repos/mpazik/Binder)] [[README](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/README.md>)]

## Architecture and data model

**Code and documentation observations.** A Binder workspace is resolved from an explicit path, `BINDER_WORKSPACE`, or the nearest ancestor containing its marker file. Initialization creates the workspace data directory and opens its SQLite database. The repository API composes entity/config persistence, schema validation, query filtering, relation expansion, transaction processing, and transaction application.[[workspace opener](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/local/open.ts>)][[knowledge graph](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/knowledge-graph.ts>)]

The SQLite schema has three namespaces: records, configs, and transactions. Records and configs carry an integer ID, stable UID, optional/unique key as appropriate, type, JSON fields, transaction IDs, and tags. Transaction rows store sequential ID, current and previous hashes, record/config changesets, author, created time, and metadata such as message, source, and channel. Config entities hold the schema itself, so field/type definitions are data that record writes can use after config changes are processed.[[SQLite schema](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/schema.ts>)][[transaction processor](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-processor.ts>)][[transaction concept](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/docs/concepts/transaction.md>)]

Changesets encode typed field-level set, clear, sequence, and relation-patch operations. The transaction processor validates and normalizes input against the current schema, processes config changes before records, then hashes the transaction with its predecessor. The apply path verifies the expected next transaction ID and prior hash before updating entities and saving the transaction within the database transaction.[[changeset concept](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/docs/concepts/changeset.md>)][[transaction processor](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-processor.ts>)][[transaction applier](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-applier.ts>)]

The README describes Markdown as a view over the graph, with navigation rules mapping entities to paths; the editor/LSP layer validates and syncs file edits into repository changes. The inspected repository model is still SQLite-backed structured data. Markdown, CLI, HTTP, MCP, and editor clients share a workspace repository rather than maintaining separate memory stores.[[README](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/README.md>)][[workspace opener](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/local/open.ts>)]

## Write, update, delete, and retrieval

**Writes and updates.** The MCP registry exposes `schema`, `search`, and `transact`. The transaction tool accepts record and config changesets and calls the repository's `kg.update`. A record with a type creates it; a key or UID without type targets an existing record for update; the tool schema documents `$delete: true` for deletion. The transaction source carries configured author metadata and returns transaction ID/hash and affected counts. The public repository API also supports processing inputs without persisting, applying an externally formed transaction, and listing/fetching transactions.[[MCP registry](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/cli/src/mcp/tools/index.ts>)][[MCP transaction tool](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/cli/src/mcp/tools/transact.ts>)][[knowledge graph](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/knowledge-graph.ts>)]

Processing can resolve records by UID, key, or numeric ID, validates typed changesets, and generates the inverse information needed for rollback. Deleting an entity is encoded as clearing populated scalar fields and removing values from multi-value fields, so prior values remain represented in the transaction history and can be restored by applying inverses. This is reversible deletion, not a secure-erasure guarantee.[[entity store](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/entity-store.ts>)][[changeset concept](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/docs/concepts/changeset.md>)][[MCP transaction tool](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/cli/src/mcp/tools/transact.ts>)]

Rollback checks a caller-supplied or current version, applies inverse transactions newest-first, then deletes the reverted transaction rows. This means the implementation supports undo by removing rolled-back entries from the active history; the docs' append-only history wording does not describe that rollback path. No independent data-erasure path or guarantee for external copies/backups was established in the reviewed slice.[[transaction applier](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-applier.ts>)][[transaction concept](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/docs/concepts/transaction.md>)]

**Retrieval.** The graph API searches records/configs using structured equality, membership, string, numeric/date/range, and relation filters, with nested includes, ordering, and cursor-style pagination. The code exposes a default search limit of 50. The inspected filter compiler implements `$text` as case-insensitive substring matching across supported text fields; no embedding/vector retrieval or generated answer step appears in the reviewed repository search path. Query docs mention similarity/hybrid options but also distinguish unfinished extensions, so these docs alone do not establish that those paths are implemented at this revision.[[filter compiler](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/filter-entities.ts>)][[knowledge graph](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/knowledge-graph.ts>)][[query concept](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/docs/concepts/query.md>)]

## Scope isolation

Data and schema are scoped to the opened workspace's SQLite repository; repository documentation describes independent repositories with independent schema/data. The inspected record schema has no user, agent, tenant, or project principal column, and record searches do not add a principal predicate. Workspace selection and filesystem permissions define the visible boundary in the inspected code, but this review did not test caller authorization or cross-workspace isolation at runtime.[[workspace opener](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/local/open.ts>)][[SQLite schema](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/schema.ts>)][[repository concept](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/docs/concepts/repository.md>)]

## Provenance and evidence

Transactions include author, creation time, previous/current content hashes, and optional message, source, channel, and tags. The hash is computed over canonical transaction content, and the predecessor hash links versions. The MCP handler uses configured author metadata; tool calls expose transaction hash and ID. These fields provide change provenance and integrity structure, but the record model does not carry a general source passage, confidence/trust label, or claim-level citation relation. A hash chain is not an external witness or a tested tamper-resistance result.[[transaction concept](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/docs/concepts/transaction.md>)][[transaction processor](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-processor.ts>)][[transaction store](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-store.ts>)][[MCP transaction tool](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/cli/src/mcp/tools/transact.ts>)]

## Source-visible efficiency and observability

**Code observations, not measurements.** Search is capped at 50 by default and selected record fields can be included; indexes exist for record type/key and transaction creation/predecessor. Filter compilation and entity/relation resolution execute SQLite queries. The database wrapper serializes top-level writes on a connection and uses savepoints for nested transactions. These are visible bounds and mechanisms, not measured latency, throughput, or scaling results.[[knowledge graph](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/knowledge-graph.ts>)][[SQLite schema](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/schema.ts>)][[filter compiler](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/filter-entities.ts>)][[database wrapper](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/db.ts>)]

The transaction API exposes current version/hash, transaction fetch/list, and commit/transaction/rollback subscriptions. Subscriber failures are reported without aborting the commit; MCP transaction responses expose ID/hash and affected counts. No source-visible token accounting, inference-cost tracking, retrieval latency distribution, or benchmark score was found in the inspected memory path.[[knowledge graph](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/knowledge-graph.ts>)][[transaction store](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-store.ts>)][[MCP transaction tool](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/cli/src/mcp/tools/transact.ts>)]

## Metric-domain evidence

All domains are **unmeasured for Binder in this review**. This table records source-visible mechanisms or gaps only.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Structured filters and text matching are present; no answer-quality or abstention probes were captured. | Unmeasured |
| Correction accuracy and staleness | Updates append changesets and rollback can reverse recent transactions; no correction cases were adjudicated. | Unmeasured |
| Deletion leakage | Delete is represented by reversible field clears; no post-delete leakage probes were run. | Unmeasured |
| Scope isolation | Repository data is workspace-local; no cross-principal or cross-workspace probes were run. | Unmeasured |
| Evidence support and citation coverage | Transaction provenance is available, but the inspected memory interface lacks general claim-level source citations. | Unmeasured |
| Retrieval latency and write-to-recall delay | SQLite search and transactional writes are visible; no Binder workload timings were captured. | Unmeasured |
| Tokens and cost | No model/token/cost path was found in the inspected repository search and transaction interfaces. | Unmeasured |
| Persistent storage | SQLite table structure is visible; no bytes-per-record or corpus storage measurement was collected. | Unmeasured |

See [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) for proposed protocols and separate baseline execution tracking. These are not Binder results.[[metric definitions](../METRICS.md)][[fixture](../fixtures/memory-benchmark-v1.json)][[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded read-only review of selected documentation and source files at the recorded SHA. It did not run Binder, mutate a workspace, invoke an agent, inspect every client integration or plugin, or test failure/recovery paths. Source structure cannot establish that transactions, search filters, undo, workspace boundaries, or Markdown synchronization behave correctly under real workloads. Broader secure deletion, authorization, cross-device sync, operational reliability, and semantic-retrieval behavior remain outside the evidence collected here.[[reviewed head](https://github.com/mpazik/Binder/commit/f72189f6107368f8712915254d52897b3022ef4f)][[README](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/README.md>)][[transaction applier](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-applier.ts>)]

## Contact-list follow-up

I checked the official pinned [README](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/README.md>), the pinned [SECURITY.md location](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/SECURITY.md>), and the official project URL [binder.do](https://binder.do). The README publishes no contact email, the pinned SECURITY.md path is absent, and binder.do redirects to the repository. The JSON record therefore stores `contact.email: null` and the checked source URLs.

## Benchmark status

**Benchmark not run.** No Binder runtime, benchmark workload, build, or tests were run. Source observations and project metric definitions are not results for Binder. The project's fixture and execution-status record describe planned methodology and independent baseline tracking only.[[metric definitions](../METRICS.md)][[fixture](../fixtures/memory-benchmark-v1.json)][[execution status](../results/initial-baselines-status.json)]

## Sources

- [Curated roster entry](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution only.
- [Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/binder.md) — identity and listed-locator attribution only.
- [Official repository](https://github.com/mpazik/Binder) — canonical public repository and default branch.
- [Current main head metadata](https://api.github.com/repos/mpazik/Binder/commits/main) — current full SHA at review time.
- [Reviewed head](https://github.com/mpazik/Binder/commit/f72189f6107368f8712915254d52897b3022ef4f)
- [README](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/README.md>)
- [Workspace open and discovery](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/local/open.ts>)
- [SQLite schema](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/schema.ts>)
- [Knowledge graph API](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/knowledge-graph.ts>)
- [Filter compiler](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/filter-entities.ts>)
- [Entity store](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/entity-store.ts>)
- [Transaction processor](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-processor.ts>)
- [Transaction applier and rollback](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-applier.ts>)
- [Transaction store](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/repo/src/transaction-store.ts>)
- [MCP tools](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/cli/src/mcp/tools/index.ts>), [MCP transaction handler](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/cli/src/mcp/tools/transact.ts>), and [MCP dispatcher](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/packages/cli/src/mcp/tools.ts>)
- [Query concept](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/docs/concepts/query.md>), [transaction concept](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/docs/concepts/transaction.md>), and [changeset concept](<https://github.com/mpazik/Binder/blob/f72189f6107368f8712915254d52897b3022ef4f/docs/concepts/changeset.md>)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only source review; no Binder execution, benchmark, build, or tests.

---
