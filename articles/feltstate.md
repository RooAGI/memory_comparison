# Feltstate source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 236 / feltstate / feltstate  
**Listed repository locator:** [Morephine/feltstate](https://github.com/Morephine/feltstate)  
**Catalog source attribution:** [Agent Memory Atlas report at catalog revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/feltstate.md)  
**Current canonical repository:** [Morephine/feltstate](https://github.com/Morephine/feltstate)  
**Default branch / reviewed head:** main / [39f32e4ac30427871a71bfeafa3efa3c64598e5e](https://github.com/Morephine/feltstate/commit/39f32e4ac30427871a71bfeafa3efa3c64598e5e)  
**Review time:** 2026-11-25 20:19:23 UTC (12:19:23 PST; America/Los_Angeles). The official repository page identifies main as the default branch, and GitHub’s commits API resolves its current full head SHA.  
**Published contact:** No email was found in the checked official [README](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md) or [SECURITY.md](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/SECURITY.md). The security policy directs reports through private GitHub security advisories.

## Identity and scope

The curated roster places **feltstate** at ordinal 236, slug `feltstate`, and lists `https://github.com/Morephine/feltstate`. Its pinned Atlas report is recorded as roster attribution only; Atlas prose and capability marks are not used as assessment evidence.[[roster entry](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/feltstate.md)]

GitHub identifies `Morephine/feltstate` as the canonical public repository and `main` as its default branch. The official commits API resolved current head `39f32e4ac30427871a71bfeafa3efa3c64598e5e`; the commit page confirms that SHA. Reviewed source links below are pinned to it.[[repository](https://github.com/Morephine/feltstate)] [[main head API](https://api.github.com/repos/Morephine/feltstate/commits/main)] [[full head](https://github.com/Morephine/feltstate/commit/39f32e4ac30427871a71bfeafa3efa3c64598e5e)]

Feltstate is a Python reference library and local state engine for companion agents. It combines a structured memory store, an independently supplied affect estimator, and optional lifecycle and orchestration modules. The README explicitly frames the affect model as a design mechanism, not a claim of consciousness or human-like emotion. This review covers the public source, not a hosted service.[[README](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md)]

## Architecture and data model

**Code observations.** The memory core is a flat-file Canon using line-delimited JSON, with separate confirmed, pending, and bounded archived files. A memory is a compact 5W1H fact with actor/object, explanation, time, place, intensity, confidence, timestamps, an ID, reinforcement and recall counters, and optional provenance and key-web fields. Current salience is computed at read time from base intensity, age, reinforcement, and recalls; permanence and visible/archive/forgotten thresholds affect its tier.[[Canon source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)]

The broader package keeps distinct modules for fact extraction, transcript context expansion, affect associated with facts, key-web relations, skill memory, crystallization, lifecycle fingerprints and deletion, and a read-only dashboard. These are composable library surfaces; the README says the application supplies transcript storage and resolvers, and that memory is called explicitly rather than injected behind the caller’s back.[[README](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md)] [[context source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/context.py)]

## Write, update, delete, and retrieval

**Write and update — source observations.** Canon supports explicit add and ask operations; ask places a candidate in a pending “grey zone” until confirmed. Entries deduplicate by actor/object, and repeated writes reinforce an existing fact. Correction marks the old version superseded while adding the replacement; retraction marks and retains a record for history. An optional extractor proposes structured facts in a separate model pass, and by default proposals are committed through ask so the caller can confirm them.[[Canon source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)] [[extractor source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/extract.py)]

**Deletion.** Ordinary correction and retraction preserve historical rows; optional lifecycle garbage collection and reaper provide a separate physical-deletion path. The reaper writes and fsyncs a pending transaction, records a transaction-keyed `legal_death` tombstone before removing rows, removes matching rows from supplied live stores and snapshots, and clears the pending record after completion. Replay is documented as idempotent after interruption. The README and reaper both state an important boundary: source-material rows are marked eligible but are not physically purged by this adapter, and only snapshots passed to the operation are covered.[[README](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md)] [[reaper source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/lifecycle/reaper.py)] [[security policy](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/SECURITY.md)]

**Retrieval.** The default Canon offers substring search, salience-scored recall, temporal history/as-of views, and context lookup; its default scoring is lexical, and each operation reloads files, making operations O(n). The key web adds a non-vector path: each new fact collides once against existing single-word keys, a caller-provided judge decides which candidates are kin, and edges store the reason on the records. Querying enters through shared keys, follows judged edges, and orders the resulting chain by event time. The source explicitly says shared-key candidacy alone does not establish kinship.[[Canon source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)] [[key-web source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/keyweb.py)]

## Scope isolation, provenance, and evidence

**Scope isolation — source observations.** Canon supports a region distinction for facts and skills and optional actor filtering. The inspected Canon and key-web surfaces do not show tenant, user, or session isolation enforced by the store; the application must supply and separate the relevant files and transcript data. The repository’s companion examples do not establish deployment-level isolation.[[Canon source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)] [[README](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md)]

**Provenance and evidence.** The optional lifecycle path fingerprints distilled memories with source pointers and fusion lineage; drilling can resolve pointers to transcript turns when the application provides the fingerprint store, transcript loader, and source resolver. The helper can check exact source text against a pointer hash, but does not recover deleted text or locate it automatically. The optional extractor can attach turn-number references from its input slice, but this review did not establish that every Canon write carries a resolvable evidence pointer. Hash-linked records are described as tamper-evident under a trusted-ledger assumption, not as encryption or protection against an attacker who can rewrite the ledger and recompute hashes.[[README](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md)] [[extractor source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/extract.py)] [[context source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/context.py)] [[reaper source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/lifecycle/reaper.py)]

## Source-visible efficiency and observability

**Code and documentation observations, not measurements.** The implementation uses stdlib JSONL files and no vector index in the default Canon; reload and lexical scoring are O(n). Archive compaction bounds the cold sidecar, and the key-web digest pays for a whole-ledger candidate pass once per newly born fact rather than on every query. The source recommends this for one companion’s thousands of distilled facts and identifies fleet-scale corpora and semantic search as outside the default store’s intended scale.[[Canon source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)] [[key-web source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/keyweb.py)]

The library uses Python logging for observable conditions such as unavailable cross-process file locking; the README also describes a read-only dashboard for viewing records and relations. The inspected material does not provide a runtime telemetry service or measured latency, token, cost, or storage results.[[Canon source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)] [[README](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md)]

## Metric-domain evidence

| Domain | Status for this review | Source evidence |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Lexical recall and key-web chain retrieval are visible in source; no probes were run.[[Canon](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)] [[metrics](../METRICS.md)] |
| Correction and stale values | Unmeasured | Supersession and as-of history are implemented; no correction probes were run.[[Canon](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)] [[metrics](../METRICS.md)] |
| Deletion leakage | Unmeasured | The reaper implements tombstone-first deletion over supplied stores and snapshots, with source-material purge excluded; no deletion probes were run.[[reaper](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/lifecycle/reaper.py)] [[metrics](../METRICS.md)] |
| Scope-isolation leakage | Unmeasured | Region and actor filtering appear in the inspected API; no tenant boundary or cross-scope probes were run.[[Canon](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)] [[metrics](../METRICS.md)] |
| Evidence support and citation coverage | Unmeasured | Provenance pointers and transcript resolution are optional; no answer claims were adjudicated.[[README](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md)] [[metrics](../METRICS.md)] |
| Latency and write-to-recall delay | Unmeasured | The source describes O(n) file operations, but no timed workload ran.[[Canon](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)] [[metrics](../METRICS.md)] |
| Tokens, cost, and storage efficiency | Unmeasured | No runtime or corpus measurements were collected.[[metrics](../METRICS.md)] |

**Benchmark status:** not run. Project metric definitions, the execution-status record, and the planned fixture are linked below. The fixture is not a result.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

- This is a bounded source review of the pinned README, security policy, and selected Canon, extraction, context, key-web, and deletion paths. It does not exhaustively inspect every affect, companion, ladder, skill, or lifecycle operation.
- No Feltstate runtime, tests, or benchmark workload was run. Runtime correctness, retrieval accuracy, abstention, isolation in a host application, recovery under real crashes, and metric values remain unverified.
- The default file store is intended for a single companion’s modest memory corpus. Fleet-scale storage, semantic retrieval, and cross-user isolation require application-level or replacement-store design.
- Source pointers are useful only if the caller preserves the fingerprint records and referenced transcript and supplies a resolver. The optional reaper does not physically purge source-material archives, snapshots it is not given, or external backups; deletion is not cryptographic erasure.[[README](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md)] [[security](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/SECURITY.md)]
- Affect thresholds and decay constants are configurable design parameters. The project explicitly disclaims fitting them to human measurements.[[README](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md)]

## Sources

- [Official repository](https://github.com/Morephine/feltstate)
- [Current main head API](https://api.github.com/repos/Morephine/feltstate/commits/main)
- [Reviewed commit](https://github.com/Morephine/feltstate/commit/39f32e4ac30427871a71bfeafa3efa3c64598e5e)
- [README at reviewed revision](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/README.md)
- [SECURITY.md at reviewed revision](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/SECURITY.md)
- [Canon source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/canon.py)
- [Fact extraction source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/extract.py)
- [Transcript context source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/context.py)
- [Key web source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/keyweb.py)
- [Deletion reaper source](https://github.com/Morephine/feltstate/blob/39f32e4ac30427871a71bfeafa3efa3c64598e5e/feltstate/memory/lifecycle/reaper.py)
- [Curated roster entry](../data/memory-systems.json)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution-status record](../results/initial-baselines-status.json)
- [Benchmark fixture (planned workload)](../fixtures/memory-benchmark-v1.json)
