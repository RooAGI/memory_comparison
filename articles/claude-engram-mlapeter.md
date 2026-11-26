# Claude Engram (mlapeter) source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 121 / Claude Engram (mlapeter) / `claude-engram-mlapeter`  
**Listed repository locator:** [mlapeter/claude-engram](https://github.com/mlapeter/claude-engram) (explicit roster attribution)  
**Canonical upstream:** [mlapeter/claude-engram at reviewed commit](https://github.com/mlapeter/claude-engram/tree/d7366c6396f769d0267254ca648199978d5b63cb)  
**Default branch / current head:** `main` / `d7366c6396f769d0267254ca648199978d5b63cb`  
**Review time:** 2026-11-25 07:58:28 UTC (2026-11-24 23:58:28 PST; America/Los_Angeles). GitHub's repository page identified `main` as the default branch; its official commits feed resolved the current head and feed timestamp above.[[repository](https://github.com/mlapeter/claude-engram)] [[commits feed](https://github.com/mlapeter/claude-engram/commits/main.atom)]

## Identity and scope

The curated catalog places Claude Engram at ordinal 121 and lists the repository with explicit attribution. The catalog and its Atlas locator are retained for identity and attribution only; Atlas descriptions and capability marks are not assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/claude-engram-mlapeter.md)]

Claude Engram is a Claude Code memory application organized around three persistent stores: a world store of extracted facts, first-person episode files, and identity documents. Claude Code hooks write buffered transcript spans and load briefing/identity context; MCP tools provide explicit recall and mutation. Its README also describes a manual paste bridge for claude.ai, rather than automatic sync.[[official README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)] [[core memory types](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/types.ts)]

## Architecture and data model

The world-store record schema includes content, global/project scope, episodic/semantic type, self/person/craft register, four salience values, tags, access and creation metadata, source session, and update lineage. Archive flags and `merged_into`/`gist_of` pointers represent pruning, merging, and gist lineage. The schema does not define source citations or a trust-state field.[[types.ts](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/types.ts)]

The default data root is `~/.claude-engram` (overridable with `ENGRAM_DATA_DIR`). World memory has a global partition and project partitions keyed by a 12-character prefix of SHA-256 over the working-directory path. Identity, episode, backup, log, and derived embedding files are also local. The README calls out Anthropic API use for extraction/consolidation and optional Voyage API use for embeddings.[[types.ts](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/types.ts)] [[official README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)]

## Write, update, delete, and retrieval

**Write.** The Stop hook appends timestamped/session-tagged transcript spans to a plain-text per-project buffer; README documents detached extraction when the buffer reaches its size/age thresholds and on flush hooks. The buffer implementation claims content with an atomic rename, retains undersized fragments for later, chunks only at span boundaries, and restores failed claims or failed chunks by appending their original text. This is a durability design visible in code, not a crash-recovery test performed for this review.[[README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)] [[buffer.ts](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/buffer.ts)]

**Update and consolidation.** The README exposes `store` for deliberate writes and `reinforce` for strengthening with optional content update. Detached consolidation can merge redundancies, dampen superseded memories, generalize, archive pruned/merged originals, promote episodic memories to semantic gists, and write association edges. The code records archive lineage rather than deleting merge/prune sources.[[README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)] [[consolidation.ts](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/consolidation.ts)] [[store.ts](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/store.ts)]

**Delete.** The README exposes a `forget` tool, while the store interface has a `remove(id)` operation. The README also says archived memories can be recovered with `deep_recall` and that archived memories may be reactivated. This review did not trace every forget code path across active records, backups, and archives, so complete erasure semantics remain unknown.[[README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)] [[store.ts](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/store.ts)]

**Retrieval.** README describes text recall ranked by relevance and memory strength, with optional vector search, tag lookup, associated-memory and same-session expansion; retrieval can strengthen results. High-specificity `deep_recall` searches the archive and can reactivate an archived item. An optional observer mode disables strengthening. These are documented behaviors, not measured recall quality.[[README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)] [[store.ts](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/store.ts)]

## Scope isolation and provenance

Global and project world stores are physically separated, with project directories derived from the caller's working-directory path. The inspected schema and README describe a local, single-user installation; this review does not establish authenticated tenant isolation or protection against a caller choosing another working directory. No cross-project isolation probe was run.[[types.ts](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/types.ts)] [[official README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)]

Records retain session origin, timestamps, and update/archive lineage; the README says each consolidation can be committed into local Git history. Those fields make some mutation history inspectable, but the reviewed model does not attach source quotations, evidence spans, or claim-level citations to ordinary memories. The README warns that local diary-like contents and screenshots can expose personal data, and that secrets may still require review.[[types.ts](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/types.ts)] [[official README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)]

## Efficiency and observability

Hooks are designed to keep the synchronous path short by appending locally and delegating model calls to detached processes. Extraction and consolidation still depend on external model APIs; optional semantic search and associations depend on Voyage embeddings. README gives qualitative cost expectations and model defaults, but this review did not measure latency, tokens, cost, or storage use.[[official README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)] [[buffer.ts](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/buffer.ts)]

The optional localhost dashboard is documented to show memory counts, search, hook latency percentiles, failures, and log tail. The README also says failures are surfaced in a later session's context. No dashboard or operational telemetry was run or inspected in this review.[[official README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)]

## Limitations and unknowns

The upstream README says the project is no longer being developed and that its last code change was July 17, 2026; the current main-head change is a README update. Users may need to update model names in local configuration as provider models retire. The README also requires an Anthropic API key for the hook-based system; optional semantic search requires a Voyage key. claude.ai integration is a paste/import workflow with no automatic sync.[[official README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)] [[current main head](https://github.com/mlapeter/claude-engram/commits/main.atom)]

The source review did not establish deletion completeness across archives/backups, empirically verified scope isolation, evidence support, retrieval correctness, or behavior under current provider/API changes. Those remain unknown from this review; no source claim here should be read as a project benchmark result.[[README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)] [[project metrics](../METRICS.md)]

## Contact

The official pinned README was checked for a published contact email. It gives a maintainer name for commercial licensing but no email address. The pinned `SECURITY.md` path returns GitHub's file-not-found page, and no root `SUPPORT.md` appears in the repository file listing. The JSON records `contact_email: null` and the exact official URLs checked. No commit/profile metadata, third-party directory, or inferred address was used.[[README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)] [[checked SECURITY.md path](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/SECURITY.md)] [[checked SUPPORT.md path](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/SUPPORT.md)]

## Benchmark status

**Benchmark not run.** No Claude Engram code, benchmark workload, or tests were executed for this task. The structured [system review](../data/system-reviews/claude-engram-mlapeter.json) marks `benchmark_status: not_run`; the project metric definitions, execution status, and fixture are not measurements for this system.[[project metrics](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current upstream repository at reviewed commit](https://github.com/mlapeter/claude-engram/tree/d7366c6396f769d0267254ca648199978d5b63cb)
- [Official README](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/README.md)
- [Core memory types and project hashing](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/types.ts)
- [Durable buffer implementation](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/buffer.ts)
- [Memory store implementation](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/store.ts)
- [Consolidation implementation](https://github.com/mlapeter/claude-engram/blob/d7366c6396f769d0267254ca648199978d5b63cb/src/core/consolidation.ts)
- [Official commits Atom feed for current main head](https://github.com/mlapeter/claude-engram/commits/main.atom)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster attribution](../data/memory-systems.json)

**Verification boundary:** This is a source and documentation review. No Claude Engram runtime, benchmark, or test was run.