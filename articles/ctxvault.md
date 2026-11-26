# CtxVault

## Identity and review pin

- Catalog position: 176, “CtxVault”; slug `ctxvault`.
- Listed repository: [Filippo-Venturini/ctxvault](https://github.com/Filippo-Venturini/ctxvault); roster locator status is explicit. The pinned Atlas roster entry is recorded only for curated identity and locator attribution.
- Canonical upstream: [Filippo-Venturini/ctxvault](https://github.com/Filippo-Venturini/ctxvault), default branch `main`.
- Reviewed full head: [bee8578d49ea35c440d9bee6cd91d4cb139d8744](https://github.com/Filippo-Venturini/ctxvault/commit/bee8578d49ea35c440d9bee6cd91d4cb139d8744).
- Review timestamp: 2026-11-25T10:23:12Z (UTC; 2026-11-25 02:23:12 PST; America/Los_Angeles).
- Source status: reviewed from current upstream code and documentation.
- Benchmark status: not run.

The official repository page identifies `main` as the default branch. Its official main-branch Atom feed reports head `bee8578d49ea35c440d9bee6cd91d4cb139d8744`, updated 2026-11-20T09:12:56Z; the full-SHA commit page shows the same commit on `main`. ([repository](https://github.com/Filippo-Venturini/ctxvault), [main history](https://github.com/Filippo-Venturini/ctxvault/commits/main.atom), [head commit](https://github.com/Filippo-Venturini/ctxvault/commit/bee8578d49ea35c440d9bee6cd91d4cb139d8744))

## Summary

CtxVault is local-first memory infrastructure organized as independent vaults for semantic knowledge, procedural skills, and episodic facts. Each type has its own storage and retrieval path: document chunks in a Chroma vector index, named Markdown procedures, or bitemporal statements in SQLite. Agents can reach public or explicitly restricted vaults through Python, CLI, HTTP, and MCP interfaces.[[README](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/README.md)] [[memory types](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)]

It leaves memory capture to the agent or caller rather than extracting facts automatically. The local directory layout and viewer make stored content inspectable. Episodic records retain corrections and time history; semantic document indexes can become stale until synchronized. This assessment is based on current source and documentation; no CtxVault runtime, tests, or benchmarks were run.[[README](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/README.md)] [[episodic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/episodic.py)] [[semantic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/semantic.py)]

## Who and what

The official README describes CtxVault as local memory infrastructure for AI agents, with three typed memory modes and four integration surfaces. It explicitly says automatic fact extraction is not included: the agent decides what to write. The system review does not infer individual maintainer identity.[[README](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/README.md)]

## Architecture and data model

A registry records vault names, types, paths, and access configuration. A vault is a separate directory and index. Semantic vaults hold source documents and a local Chroma collection; skill vaults hold Markdown files; episodic vaults hold an `episodes.db` SQLite database. The Python client, CLI, HTTP API, and MCP server expose the vault operations, while the read-only local viewer displays vault contents and access topology.[[README](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/README.md)] [[memory types](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)]

- **Semantic memory** stores supported documents as extracted text chunks with document identity and caller metadata, embedded in a local Chroma collection. Queries embed the question and return the nearest chunks with source, metadata, and similarity information.[[memory types](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)] [[semantic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/semantic.py)]
- **Skill memory** stores procedures as Markdown with a name and description in frontmatter. Agents list available skills and read a selected procedure; these records are not embedded for semantic search.[[memory types](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)]
- **Episodic memory** stores statement text, source, confidence, salience, occurrence/validity/recording times, entity links, metadata, and optional embeddings. Separate tables keep attestations, disputes, and closure/reopen events. Valid time (when the statement held in the world) and transaction time (when the vault recorded or closed it) are independently queryable.[[episodic documentation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)] [[SQLite store](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/storage/sqlite_store.py)]

## Write, update, delete, and retrieval

**Semantic documents.** Indexing extracts and chunks a file, then indexes the chunks. The API can write a document and index it immediately; overwriting changes the file and reindexes it. A document deleted through the vault removes its indexed records and file. If a file is edited or removed outside the vault API, the index can still answer from stale text until status/sync or reindex is used. The synchronization path reports changed, missing, and unindexed files.[[semantic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/semantic.py)] [[memory types](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)]

**Skill procedures.** A skill is a Markdown file; creating or editing the file changes the instruction record, and listing then reading selects it by name. Skills are not semantically ranked. The reviewed documentation does not specify a separate version or archival history for edits.[[memory types](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)]

**Episodes.** A write creates a statement with caller-provided content and optional entity, source, confidence, salience, and time metadata. Invalidation closes a statement. Supersession closes it and links a successor; revision restates it while preserving its validity window. Reopen can undo a close while retaining the closure interval, confirmations are recorded as dated attestations, and unresolved contradictions remain as a dispute between two open statements. The SQLite module states that records are not deleted through ordinary episode operations; vault removal is the whole-store boundary. These lifecycle operations preserve history rather than replacing text in place.[[memory types](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)] [[episodic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/episodic.py)] [[SQLite store](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/storage/sqlite_store.py)]

**Retrieval.** Semantic queries use vector similarity over chunks, with a default result count of five in the vault API. Skill retrieval is list/read by name. Episodic retrieval first filters in SQLite by entities, source, confidence, valid/known time, metadata, and open/closed or dispute state, then ranks candidate rows by relevance, recency, salience, or a weighted combination. Relevance uses cosine similarity when vectors exist and distinct-word overlap otherwise. Episodic embeddings are optional; without a configured model, structured and keyword retrieval remain available.[[semantic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/semantic.py)] [[episodic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/episodic.py)] [[SQLite store](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/storage/sqlite_store.py)] [[memory types](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)]

## Scope isolation

The vault is the primary isolation boundary: each vault has an independent index, and restricted vaults name the agents allowed to access them. Python, HTTP, and MCP interfaces identify the caller differently and check access for agent reads and writes. Public vaults are open to any agent. The CLI and viewer are owner surfaces that can inspect restricted vaults; HTTP indexing and vault listing are documented exceptions to agent-name checks. Agent names are declarations rather than credentials, so the HTTP API needs localhost binding or separate authentication when exposed beyond it. There is no per-record scope inside a vault; sharing a vault makes its contents available at that vault’s access boundary.[[access control](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/access-control.md)] [[README](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/README.md)]

## Provenance and evidence

Semantic results retain document and chunk identifiers, source path, and caller-supplied metadata. Skill files preserve their Markdown text and frontmatter. Episodes carry source and metadata, entity associations, confidence, time fields, and histories of attestations, disputes, closures, reopens, and supersession/revision links. These fields let a caller inspect where stored material came from and how episode state changed. The reviewed sources do not define a system-wide claim-level citation format for an agent’s generated answer; provenance availability should not be mistaken for measured answer support.[[semantic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/semantic.py)] [[episodic documentation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)] [[SQLite store](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/storage/sqlite_store.py)]

## Efficiency and observability

The storage is local: Chroma and its embedding model serve semantic indexing, SQLite serves episodes, and skill retrieval reads files. Episodic vectors are optional, avoiding embedding work for installations that use structured or keyword retrieval. The tradeoffs are local model/index costs for semantic search and full database-row selection followed by ranking for episodic queries; no latency or scaling measurements were collected.[[README](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/README.md)] [[memory types](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)] [[episodic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/episodic.py)]

The project describes no cloud service or telemetry. Operators can inspect files directly, use the CLI to list/query/index vaults, and use a local read-only viewer for records and episodic time history. The semantic status/sync path exposes index drift. These are inspection and maintenance surfaces, not operational metrics measured in this review.[[README](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/README.md)] [[semantic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/semantic.py)]

## Metric-domain evidence

All benchmark domains for this project are **unmeasured** for CtxVault. Source inspection establishes available operations and declared design, not measured retrieval quality, isolation, speed, cost, or storage use. ([metric definitions](../METRICS.md), [project execution-status record](../results/initial-baselines-status.json), [benchmark fixture, not run](../fixtures/memory-benchmark-v1.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Semantic and episodic retrieval paths exist; no answerability or negative-query probes were run. |
| Correction accuracy and stale-value rate | Unmeasured | Episode supersession, revision, and dispute operations preserve state; no correction workload was run. |
| Deletion leakage | Unmeasured | Semantic deletion removes its indexed records; no post-deletion queries or physical-storage checks were run. |
| Scope-isolation leakage | Unmeasured | Restricted-vault checks are documented; no permitted/forbidden access workload was run. |
| Evidence support and citation coverage | Unmeasured | Stored sources and episode history are inspectable; no generated-answer citations were scored. |
| Retrieval latency | Unmeasured | No timing samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write/retrieval probes were run. |
| Tokens and cost | Unmeasured | No runtime token usage or charges were collected. |
| Storage efficiency | Unmeasured | No corpus-attributed logical or physical storage size was collected. |

## Limitations and unknowns

- Automatic conversation extraction and graph-structured semantic memory are not part of the reviewed product description. Semantic files can drift from their index if they are changed outside the synchronization path.[[README](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/README.md)] [[semantic implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/semantic.py)]
- Access control is vault-level. Agent names are not authentication credentials, owner surfaces bypass agent restrictions, and documented HTTP exceptions need deployment-aware handling.[[access control](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/access-control.md)]
- Episode timestamps are stored and compared as ISO-8601 strings; the SQLite implementation warns that lexical order is correct only when offsets are consistent, and recommends UTC for caller-supplied times. Legacy v3 closures may lack the previous valid-to value, limiting what reopen can restore.[[SQLite store](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/storage/sqlite_store.py)]
- This bounded review inspected the README, memory-type and access-control documentation, episodic storage/ranking, and semantic vault implementation. It did not trace every endpoint, migration, Chroma query, or deployment configuration.
- No system runtime, test suite, or benchmark was run. Runtime correctness, retrieval quality, deployed access isolation, physical erasure, latency, token/cost totals, and storage efficiency therefore remain unknown.

## Contact

No contact email is published in the official [README](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/README.md) or on the official [documentation home](https://filippo-venturini.github.io/ctxvault/). The checked URLs are recorded in the review data. No profile or commit metadata and no third-party directory was used.

## Benchmark status

**Not run.** CtxVault, its tests, and benchmark workloads were not run. Project metric definitions and the fixture are workload specifications, not CtxVault measurements. ([metrics](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ctxvault.md)
- [Official repository](https://github.com/Filippo-Venturini/ctxvault)
- [Official main branch history](https://github.com/Filippo-Venturini/ctxvault/commits/main.atom)
- [Reviewed full head bee8578d49ea35c440d9bee6cd91d4cb139d8744](https://github.com/Filippo-Venturini/ctxvault/commit/bee8578d49ea35c440d9bee6cd91d4cb139d8744)
- [Pinned README](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/README.md)
- [Pinned memory-type documentation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/memory-types.md)
- [Pinned access-control documentation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/docs/how-it-works/access-control.md)
- [Pinned episodic vault implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/episodic.py)
- [Pinned SQLite episodic store](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/storage/sqlite_store.py)
- [Pinned semantic vault implementation](https://github.com/Filippo-Venturini/ctxvault/blob/bee8578d49ea35c440d9bee6cd91d4cb139d8744/src/ctxvault/core/vaults/semantic.py)
- [Official documentation home](https://filippo-venturini.github.io/ctxvault/)
