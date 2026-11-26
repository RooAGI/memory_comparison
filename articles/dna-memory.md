# DNA Memory

## Identity and review pin

- **Catalog position:** 193, “DNA Memory”; slug `dna-memory`.
- **Listed repository:** [AIPMAndy/dna-memory](https://github.com/AIPMAndy/dna-memory); locator status is explicit. Atlas is retained for curated identity and attribution only.
- **Canonical upstream:** public [AIPMAndy/dna-memory](https://github.com/AIPMAndy/dna-memory), default branch `main`. Its official [main feed](https://github.com/AIPMAndy/dna-memory/commits/main.atom) reports full head `f135344d7d6f90f1be73e209cd0c6a7083f328ea`, updated 2026-11-19T15:17:48Z. A fresh `git ls-remote --symref` resolved HEAD and main to that SHA; a shallow checkout matched.
- **Reviewed:** 2026-11-25 11:14:09 UTC (2026-11-25 03:14:09 PST; America/Los_Angeles).
- **Status:** Reviewed from documentation and source at the verified SHA. Benchmark not run.

The [roster entry](../data/memory-systems.json) identifies the ordinal, slug, locator, and Atlas attribution. The pinned [Atlas page](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dna-memory.md) is used only for roster attribution, not as assessment evidence.

## Summary

DNA Memory is a local-first shared memory service for Codex, Claude, Hermes, and Obsidian. Markdown pages in a configured vault are canonical; SQLite is a rebuildable index and telemetry store. Its MCP interface offers keyword recall, direct writes, feedback, explicit replacement, and reindexing. The inspected recall path does not enforce project or session isolation.

## Who and what

The official [README](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/README.md) and [English README](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/README_EN.md) describe a shared stdio MCP server, client integrations, and local-first Markdown storage. The README identifies its author, but no email is published. I also checked the official [security policy](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/SECURITY.md) and the official [website named by the README](https://metaver.vip/); neither provides a contact email. The security policy directs sensitive reports to GitHub Security advisories.

## Architecture and data model

Seven MCP tools provide `memory_recall`, `memory_get`, `memory_remember`, `memory_feedback`, `memory_close_session`, `memory_status`, and `memory_reindex`. Configuration selects a vault, managed Markdown directory, SQLite database, source locations, and backup policy.[[README](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/README.md)] [[MCP adapter](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_mcp.py)]

Each page carries YAML frontmatter with stable ID, type, status, confidence, importance, timestamps, source hash and references, supersedes relationship, client, project path, and session ID. The first body paragraph is indexed as its summary. SQLite holds a rebuildable index, candidate events and importer checkpoints, feedback, and hashed-query recall events.[[service](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_service.py)] [[Markdown indexer](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/markdown_memory.py)] [[SQLite store](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/unified_memory.py)] [[candidate queue](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/candidate_events.py)]

Markdown is the durable source of truth; reindex validates pages and synchronizes the SQLite view. Writes stage file replacements with backups and rollback, then scan the configured knowledge root to rebuild the index.[[service](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_service.py)] [[indexer](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/markdown_memory.py)]

## Write, update, delete, and retrieval

**Write.** `memory_remember` validates a supported type, nonempty summary, and sensitive-content policy, then creates a Markdown record. An active source-hash match deduplicates; otherwise same-type summaries are compared after Unicode NFKC, whitespace, and case normalization. This exact-text check is not fuzzy semantic deduplication.[[MCP](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_mcp.py)] [[service](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_service.py)] [[policy](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/policy.py)]

**Automatic proposals.** Importers enqueue bounded events. Daily maintenance selects pending memory proposals and sends them through the same write service after type, emptiness, and sensitive-content checks. The inspected implementation does not ask for or record human approval; that qualifies README language about reviewable proposals and verified conclusions.[[queue](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/candidate_events.py)] [[daily operations](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_operations.py)] [[extractor](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/native_auto_extract.py)] [[README](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/README.md)]

**Update and replacement.** No separate update MCP tool is registered. A caller may pass exact active IDs in `supersedes`; a new page is written, while old pages remain and are marked superseded. Recall returns active records. The service does not infer replacement from fuzzy similarity or project context.[[MCP](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_mcp.py)] [[service](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_service.py)] [[English README](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/README_EN.md)]

**Delete.** There is no memory-delete MCP tool. Removing a Markdown file and reindexing removes its row from the current SQLite index; it does not guarantee erasure from backups or copies. Daily maintenance deletes terminal queue rows after retention, while weekly maintenance creates and rotates SQLite backups.[[indexer](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/markdown_memory.py)] [[store](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/unified_memory.py)] [[maintenance](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_operations.py)]

**Retrieval.** Recall splits a query into distinct terms and matches case-insensitive substrings in active summaries using SQLite `LIKE`. Ranking uses matched-term count, useful-minus-misleading feedback, confidence, importance, and update time, with at most 20 results. `memory_get` reads by ID; no vector or semantic search appears in this path.[[service](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_service.py)] [[store](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/unified_memory.py)] [[MCP](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_mcp.py)]

**Scope isolation.** Records carry client, project-path, and session metadata, and recall accepts client/session arguments. The inspected SQL uses those arguments only in telemetry, not as filters, and does not filter by project. Separate vaults, databases, and OS permissions can form an outer boundary; per-project or per-session isolation is not enforced by the reviewed recall path.[[service](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_service.py)] [[store](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/unified_memory.py)] [[security policy](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/SECURITY.md)]

**Provenance and evidence.** Source references, source hashes, client/project/session metadata, and explicit supersedes links provide lineage and relationship data. Confidence and importance affect ranking. Records do not require an evidence quote or verify source content. Direct writes validate type and sensitive patterns, not the truth of a claim.[[service](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_service.py)] [[indexer](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/markdown_memory.py)] [[MCP](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_mcp.py)]

**Efficiency and observability.** Recall performs substring predicates and feedback aggregation. Writes scan active records of the same type for exact duplicates and reindex the configured root. Recall stores a hash of the query with client, session, and result count, and increments per-memory recall counters. Feedback is stored separately. The API accepts any nonempty outcome, but only `useful` and `misleading` change ranking. These are code observations; no latency, token, or cost measurements were collected.[[service](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_service.py)] [[SQLite store](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/unified_memory.py)]

## Metric-domain evidence

- **Answerable retrieval and abstention:** keyword matching is visible in source; no accuracy or abstention workload was run.
- **Correction and stale values:** replacement uses explicit IDs and retains old pages; no correction sequence was measured.
- **Deletion leakage:** reindex removes absent pages from the current index; no residual-storage check was run.
- **Scope isolation:** recall does not filter client, project, or session; no isolation workload was run.
- **Evidence and citations:** lineage pointers exist; no claim-support evaluation was run.
- **Retrieval latency:** not measured.
- **Write-to-recall delay:** not measured.
- **Tokens and cost:** not measured.
- **Storage efficiency:** not measured.

See project [metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and the [benchmark fixture](../fixtures/memory-benchmark-v1.json). The fixture describes a planned workload, not a DNA Memory result.[[metrics](../METRICS.md)] [[status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Contact

No contact email was published in the official README, English README, security policy, or the official website checked. Exact URLs are recorded in [dna-memory.json](../data/system-reviews/dna-memory.json).

## Limits and unknowns

The public documentation describes verified and reviewable memory, but the inspected daily processor automatically promotes pending proposals after syntactic and sensitive-content checks without a recorded approval step. Direct MCP writes also accept a caller-supplied summary without validating factual support.

Client/project/session fields are not used to scope recall. Deleting a file and reindexing removes the row from the current index, but backups and other copies are outside that behavior. Retrieval quality, scaling, isolation, correction, retention, latency, cost, and physical erasure are unknown. No DNA Memory runtime, tests, or benchmarks were run.[[README](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/README.md)] [[operations](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_operations.py)] [[service](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/scripts/memory_service.py)] [[security](https://github.com/AIPMAndy/dna-memory/blob/f135344d7d6f90f1be73e209cd0c6a7083f328ea/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No DNA Memory runtime, tests, or benchmark workloads were executed. See [project metrics](../METRICS.md), [shared status](../results/initial-baselines-status.json), and the [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and SHA-pinned URLs are in [dna-memory.json](../data/system-reviews/dna-memory.json). The [curated roster](../data/memory-systems.json) and [pinned Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dna-memory.md) are used only for identity and locator attribution.
