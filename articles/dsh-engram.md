# dsh-engram

**Review status:** Reviewed from official code and documentation at `main` [`a0f8f2d95b7a5443c9067ecb5a7720ab728e2090`](https://github.com/kenz1117/dsh-engram/commit/a0f8f2d95b7a5443c9067ecb5a7720ab728e2090). Review time: 2026-11-25 11:31:45 UTC (03:31:45 PST; America/Los_Angeles).

## Summary

dsh-engram is a local-first DeepSeek Harness plugin that stores cross-session agent memories in three SQLite stores and combines full-text and local-vector search with relationship expansion, evidence checks, and profile injection.[readme][sqlite][tools] It also has explicit capture, correction, forgetting, export, consolidation, belief, fact-timeline, and review tools. This is a source review; no runtime, tests, or benchmarks were run.

## Who and what

The official repository describes dsh-engram as a DeepSeek Harness long-term memory plugin; the README identifies the license as MIT © KenZ (kenz1117).[readme] The catalog resolves ordinal 199 to dsh-engram, slug `dsh-engram`, listed repository `https://github.com/kenz1117/dsh-engram`, with explicit locator attribution. The pinned Atlas entry is retained only as roster identity and locator context, not as assessment evidence.[catalog][atlas]

## Architecture and data model

GitHub identifies `main` as the repository's default branch. Its official main commit feed reports current full head `a0f8f2d95b7a5443c9067ecb5a7720ab728e2090`, updated 2026-11-24T08:54:02Z; source links below pin that revision.[repo][head_feed][head]

The plugin is organized around a Node host side and a React management panel. The host owns the SQLite stores, memory tools, local embedder and optional auxiliary LLM paths; the panel uses loopback APIs for inspection and management.[readme][tools] The three scopes are user-wide, project-specific, and shared. Project stores are selected from the active session working directory and normalized Git origin when available; shared is an explicit lending space rather than an automatic-capture destination.[readme][tools][types]

A memory row has both a revision ID and a stable logical `memoryId`, plus scope, kind, text, importance/confidence, lifecycle status, timestamps, usage outcome, optional source session/round/sequence, and palace slot/review metadata. Other stored structures include relationship edges, revision snapshots, FTS5 rows and embedding blobs, mutation log entries, temporal facts, entities, belief-like observations with source IDs and status, profile versions, injection snapshots and review schedules.[types][sqlite] The schema migrations expose these as SQLite tables; the model is a typed, single-machine memory graph layered over indexed text and vectors.[sqlite]

## Write, update, delete, and retrieval

**Writes and updates.** An agent can use `engram_save` for explicit writes; optional session capture extracts candidates from session content. The README describes four write dispositions (accept, merge, defer, drop), and the host source injects scope selection, embedding availability, auxiliary-model routing, redaction, and tool availability as dependencies.[readme][tools] Update creates a new revision under the same logical memory identity and connects it to the prior version; the previous version is retained as an archived revision rather than overwritten in place.[types][sqlite]

**Deletion and maintenance.** The type model distinguishes active records from archived records and forgotten records. Archived items are excluded from retrieval but recoverable; forgetting is a soft deletion, retaining the row and supporting audit/recovery paths. The README describes forgetting with a reason/tombstone and a mutation log; database purge is a distinct broader operation.[types][sqlite][tools] Automatic decay and consolidation archive or merge selected entries; neither description establishes erasure from backups or filesystem copies.[readme][sqlite]

**Retrieval.** The README describes FTS5 keyword search (including Chinese 2-gram preprocessing), a local vector lane fused with reciprocal-rank fusion, relationship-edge expansion, recency/access boosts, optional query rewriting, and optional room routing. If embeddings are unavailable, search can fall back to keyword-only mode with a visible degraded status.[readme][sqlite][tools] Search output is registered as an in-memory, session-isolated batch of evidence references. The evidence checker rejects references outside that batch and accepts “sufficient” only when the model claims sufficiency, at least one batch reference is valid, and the requested next strategy is `answer`; otherwise the code forces a non-answer/search path.[evidence] This is a process-local control over citing retrieved rows, not proof that a memory is factually true or that retrieval is accurate.

## Scope isolation

The three stores provide physical separation for user, project, and shared memory. Project routing follows the session cwd and can use normalized Git origin to share a store across worktrees; absent repository origin it falls back to cwd-derived identity. Tools resolve the project store using the session context, while shared access is explicit.[readme][tools][types] Those boundaries are visible in code and documentation but do not establish deployment correctness or a measured absence of cross-scope leaks. Shared scope is described as intentionally readable by other agents and should not be treated as private.[types][readme]

## Provenance, efficiency, and observability

Memory records can retain session ID and, for captured events, source round and event sequence. Updates preserve a stable logical identity while recording revisions; relationship edges, evidence batches, and the operation log expose additional lineage.[types][sqlite][evidence] These mechanisms provide traceable IDs and mutation history, not external source citations or independent verification of statements.

Source-visible efficiency features include SQLite/FTS indexes, a local embedding engine, embedding reuse during consolidation, delayed startup maintenance, batched processing and bounded profile injection. The README notes that first use may download the local model; inference is local afterward. Failed embedding setup degrades retrieval and dimension mismatch blocks incompatible vectors rather than comparing them.[readme][sqlite] The repository exposes a management panel, operation-log views, injection snapshots, and process/runtime telemetry for status and diagnosis.[readme][sqlite] These are design and instrumentation observations; no performance or cost measurements were collected.

## Metric-domain evidence

- Answerable recall and abstention — unmeasured; the code has search and a batch evidence gate, but no benchmark workload was run.[readme][evidence][metrics][status]
- Correction accuracy and stale-value rate — unmeasured; revision and supersession paths exist, but no correction sequence was evaluated.[types][sqlite][metrics][status]
- Deletion leakage — unmeasured; forgetting is soft deletion and no residual-data probe was run.[types][sqlite][metrics][status]
- Scope isolation — unmeasured; user/project/shared routing is source-visible, but no cross-scope workload was run.[readme][tools][metrics][status]
- Evidence support and citation coverage — unmeasured; references are batch-checked against returned memory rows, but no evidence-quality adjudication was performed.[evidence][metrics][status]
- Retrieval latency and write-to-recall delay — unmeasured; no timing probe or capture-to-recall workload was run.[sqlite][tools][metrics][status]
- Tokens and cost — unmeasured; optional auxiliary model calls and persistent tool schemas are described, but no usage or provider-cost data was collected.[readme][tools][metrics][status]
- Storage efficiency — unmeasured; SQLite, FTS and vector structures were inspected, but no corpus-attributed storage measurement was made.[sqlite][metrics][status]

Project benchmark status is [`not_run`](../data/system-reviews/dsh-engram.json); see [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json). These are evaluation materials, not dsh-engram results.[metrics][fixture][status]

## Contact

The official pinned README and SECURITY.md were checked for a contact email. The README publishes no email, and SECURITY.md directs security reports through GitHub's private vulnerability reporting flow; `contact_email` is therefore null. No profile or commit metadata was used.[readme][security]

## Limits and unknowns

- Search references prove that a record was returned in a particular live batch; they do not validate the truth, freshness, or completeness of that record.[evidence][types]
- Soft deletion and archival affect retrieval status, but this review did not test database files, backups, exports, or other copies for residual data.[types][sqlite]
- The project is a host plugin with optional automatic capture and auxiliary-model behavior. Source inspection does not establish extraction quality, correct scope classification, or successful operation in any particular host configuration.[readme][tools]
- This review inspected selected official documentation and current storage, tool, type, and evidence code at the verified head. It did not audit every tool or UI route.
- No dsh-engram runtime, tests, or benchmarks were run; all metric domains remain unmeasured.[metrics][fixture][status]

## Sources

- [Official repository](https://github.com/kenz1117/dsh-engram) · [main commit feed](https://github.com/kenz1117/dsh-engram/commits/main.atom) · [verified current head](https://github.com/kenz1117/dsh-engram/commit/a0f8f2d95b7a5443c9067ecb5a7720ab728e2090).
- [README](https://github.com/kenz1117/dsh-engram/blob/a0f8f2d95b7a5443c9067ecb5a7720ab728e2090/README.md), [memory record types](https://github.com/kenz1117/dsh-engram/blob/a0f8f2d95b7a5443c9067ecb5a7720ab728e2090/src/types.ts), and [SQLite store](https://github.com/kenz1117/dsh-engram/blob/a0f8f2d95b7a5443c9067ecb5a7720ab728e2090/src/store/sqlite.ts).
- [Tool definitions and execution](https://github.com/kenz1117/dsh-engram/blob/a0f8f2d95b7a5443c9067ecb5a7720ab728e2090/src/tools/create.ts) and [evidence-batch validation](https://github.com/kenz1117/dsh-engram/blob/a0f8f2d95b7a5443c9067ecb5a7720ab728e2090/src/retrieve/evidence.ts).
- [Security policy](https://github.com/kenz1117/dsh-engram/blob/a0f8f2d95b7a5443c9067ecb5a7720ab728e2090/SECURITY.md).
- [Catalog roster entry](../data/memory-systems.json) · [pinned Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dsh-engram.md) (identity/locator only).
- [Metric definitions](../METRICS.md) · [benchmark fixture](../fixtures/memory-benchmark-v1.json) · [execution status](../results/initial-baselines-status.json).
