# agents-memory

## Identity and review pin

- **Curated ordinal:** 30 in `data/memory-systems.json`
- **Listed name / slug:** agents-memory / `agents-memory`
- **Listed repository locator:** https://github.com/Lolaplex/agents-memory
- **Canonical repository:** https://github.com/Lolaplex/agents-memory
- **Default branch:** `main`
- **Reviewed head:** [`7973f746e768e2e931839054391899467410f709`](https://github.com/Lolaplex/agents-memory/commit/7973f746e768e2e931839054391899467410f709)
- **Reviewed at:** 2026-11-24 19:22:30 UTC (11:22:30 PST, America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The roster's Atlas source is [the pinned agents-memory report](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agents-memory.md). It supplied identity, locator and source attribution only. Atlas descriptions, marks and layout were not used as assessment evidence.

## Summary

agents-memory is a local, Markdown-first memory vault with a Python MCP server and CLI. It separates global user memory from per-repository notes, builds a disposable SQLite FTS5 index for retrieval, and uses staging and explicit distillation to move selected material into typed files. Findings below describe selected source and documentation at the verified revision; they are not runtime results.

## Who and what

The official [README](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/README.md) presents agents-memory as a local memory layer for coding agents. Its MCP server is an interface to the on-disk vault, with CLI equivalents for people and scripts. This review makes no individual-maintainer claim.

## Architecture and data model

The global user store is `~/.agents/memory`; each registered repository can have its own `.agents/memory` tree. The user store holds cross-cutting concepts, entities, workflows, project links and personal notes. Repository stores hold staging, research, ordered work files, decisions and lifecycle notes. Markdown files are the source of truth, and the path expresses the note type. See the [layout contract](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/abi/LAYOUT.md) and [store implementation](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/src/agents_memory/store.py).

The Python package includes the reference FastMCP server, CLI operations, ingestion, sync, rules rendering and project inventory. Search acceleration is a SQLite FTS5 cache in the user store's `.index` directory. The [index code](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/src/agents_memory/index.py) defines document and FTS5 tables and configures WAL with NORMAL synchronization. The [MCP server](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/src/agents_memory/mcp_server.py) attempts to rebuild the index at startup. These are code observations, not durability or performance measurements.

Markdown files can carry YAML frontmatter for identity, relations, project association, declared provenance, verification date and correction/addition/deletion pin type. The allowed schema includes explicit relations such as `refs`, `supersedes` and `same_as`. See the [hygiene contract](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/abi/HYGIENE.md).

## Write, update, delete, and retrieval

- **Write:** `add_memory` files provided text into a typed location and triggers host-context sync. User-taxonomy entries require a kind and name; in-tree notes use a project scope. Categories intended for revision in place, such as research, decisions, ADRs and implemented notes, must be rewritten with `write_memory_file` rather than appended again. The MCP contract refuses direct writes to hard-rule files.
- **Update and delete:** `write_memory_file` replaces a file's text. `delete_memory` removes a bullet identified by a search result ID; the ID includes a content hash so the target can be located again if earlier lines shift. This review did not establish a tombstone or cross-device deletion guarantee for the separately packaged sync tool.
- **Retrieval:** `search_memory` searches local Markdown. It defaults to the user store, returns up to two exact substring matches per file with stable hash-anchored IDs, then fills from ranked SQLite FTS5 results. `get_related` follows explicit frontmatter relations and can also offer content-overlap results; it is not vector search. See the [MCP contract](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/abi/MCP.md).
- **Ingestion:** catalog ingestion records titles and paths, while extraction stages selected user-authored lines. The [hygiene contract](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/abi/HYGIENE.md) says to filter assistant turns, tool data, system prompts, large code dumps, PII patterns, one-shot how-to prompts and duplicates. A person or agent explicitly distills staging into typed memory; original chat bodies remain in their product folders. See the [ingest contract](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/abi/INGEST.md).
- **Rules:** agents can submit hard-rule proposals to staging; a user applies one through the CLI. The rule renderer produces bounded content for supported host instruction surfaces. Generic memory writes do not directly edit rule files.

## Scope isolation

The empty/default project argument searches only the user store. A project slug adds that repository's in-tree notes, and `project=*` (also `all`) searches every registered clone. The contract says an unqualified search must not leak all clones. These are caller-selected search scopes, not an authenticated authorization boundary.

## Provenance and evidence

The frontmatter schema can declare `provenance: human|agent|import`, `checked_at`, and `pin_kind` values for corrections, additions and deletions. It also supports explicit links between files. These fields record declared origin and relationships; they do not establish that a fact is accurate, currently supported, or appropriate to cite in an answer.

## Source-visible efficiency and observability

**Code observations:** exact substring matches are capped per file before the FTS5 ranking leg; SQLite stores the rebuildable index, and the MCP server tries to rebuild it at startup. This avoids treating the index as durable memory, but the review collected no search latency, throughput, or size measurements.

The CLI exposes mechanical store checks and ingest status, while staging has an inbox depth/nag mechanism. The MCP server also attempts optional integration with `agents-traces` for tool-call traces. These are documented or source-visible observability hooks, not runtime telemetry gathered for this review.

## Metric-domain evidence

All metric domains below are **unmeasured**. Project definitions are in [METRICS.md](../METRICS.md); the [shared execution-status record](../results/initial-baselines-status.json) and [planned fixture](../fixtures/memory-benchmark-v1.json) are not agents-memory results.

| Domain | Source observation | Measurement status |
|---|---|---|
| Answerable recall and abstention | Substring and ranked FTS5 retrieval are documented. | Unmeasured |
| Correction accuracy and stale values | Files can be revised in place and linked with relations such as `supersedes`. | Unmeasured |
| Deletion leakage | A search-result ID can remove a bullet line by content hash. | Unmeasured |
| Scope isolation | User, per-project and all-project selectors are documented. | Unmeasured |
| Evidence support and citation coverage | Frontmatter can declare provenance and verification dates; claim support was not adjudicated. | Unmeasured |
| Latency and write-to-recall delay | A substring leg and SQLite FTS5 ranking leg are visible in the contract and source. | Unmeasured |
| Tokens, cost and storage | Local Markdown plus an SQLite cache are described; no workload measurements were taken. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of selected official documentation and source at one verified revision. No runtime, benchmark workload, or tests were run. Correctness under concurrent mutation, retrieval quality, scaling, synchronization completeness, deletion across copies, and operational recovery remain unverified.

A project argument selects the retrieval scope. The contract does not establish that the caller is authorized to request a particular registered repository. Likewise, provenance fields and explicit relations do not verify the factual support or freshness of a retrieved claim.

## Contact-list follow-up

The official [README](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/README.md) and [GitHub security-policy page](https://github.com/Lolaplex/agents-memory/security/policy) were checked for a published contact email. The README contains an installation-time `ADMIN_EMAIL` example, not a project contact. GitHub reports that the repository has no `SECURITY.md`; neither checked source publishes an email. The JSON record therefore stores `contact.email: null` and both checked source URLs.

## Benchmark status

**Benchmark not run.** No agents-memory system execution, benchmark, or tests were run. Source observations are not measurements. The [project metric definitions](../METRICS.md), [execution-status record](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json) remain separate.

## Sources

- [Canonical repository](https://github.com/Lolaplex/agents-memory)
- [Verified main head](https://github.com/Lolaplex/agents-memory/commit/7973f746e768e2e931839054391899467410f709)
- [Official README at the reviewed revision](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/README.md)
- [MCP tool contract](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/abi/MCP.md)
- [Memory layout contract](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/abi/LAYOUT.md)
- [Memory hygiene contract](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/abi/HYGIENE.md)
- [Ingest contract](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/abi/INGEST.md)
- [Store implementation](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/src/agents_memory/store.py)
- [Search index implementation](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/src/agents_memory/index.py)
- [MCP server implementation](https://github.com/Lolaplex/agents-memory/blob/7973f746e768e2e931839054391899467410f709/src/agents_memory/mcp_server.py)
- [Official security-policy page](https://github.com/Lolaplex/agents-memory/security/policy)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution-status record](../results/initial-baselines-status.json)
- [Planned benchmark fixture](../fixtures/memory-benchmark-v1.json)
