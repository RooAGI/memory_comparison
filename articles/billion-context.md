# billion-context source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 93 / billion-context / `billion-context`  
**Listed repository locator:** [ranxianglei/billion-context](https://github.com/ranxianglei/billion-context)  
**Current canonical repository:** [ranxianglei/billion-context](https://github.com/ranxianglei/billion-context)  
**Default branch / reviewed head:** master / `85afa7b212ce20981d66c9e6ecb1e944751cb3c4`  
**Review time:** 2026-11-24 23:38:56 UTC (15:38:56 PST; America/Los_Angeles).

## Identity and scope

The curated roster places **billion-context** at ordinal 93 and lists `https://github.com/ranxianglei/billion-context`. Its Atlas report URL and revision are retained for catalog attribution only. Atlas descriptions, marks, prose, and layout are not assessment evidence. The official repository page and a fresh `git ls-remote --symref` identify `master` as the default branch; the full head `85afa7b212ce20981d66c9e6ecb1e944751cb3c4` agrees with the official branch feed and the shallow checkout. [[curated roster](../data/memory-systems.json)] [[repository](https://github.com/ranxianglei/billion-context)] [[master feed](https://github.com/ranxianglei/billion-context/commits/master.atom)] [[reviewed commit](https://github.com/ranxianglei/billion-context/commit/85afa7b212ce20981d66c9e6ecb1e944751cb3c4)]

## Summary

billion-context is a model-facing context compression proxy and host plugin. It lets an agent fold ranges of conversation into its own summaries, keeps block and message references for later lookup, and can restore the original range when needed. The review concerns session history and context management, not a general-purpose cross-session personal knowledge base. [[README](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/README.md)]

## Who and what

The repository presents the project as a context-compression plugin/proxy that sits between coding agents and model APIs. Its README lists native integrations and launcher or URL-routing modes for multiple clients. The reviewed sources identify the repository account as `ranxianglei`; they do not confirm a legal owner or maintainer identity, so none is inferred here. [[README](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/README.md)]

## Architecture and data model

The `acp-kernel` package owns the transport-independent compression state machine and tool schemas; the proxy wraps it in request processing and host-specific session handling. A `CompressionBlock` stores a block/run ID, tier, model-written topic and summary, direct and effective message IDs, nested block IDs, compressed-token count, timestamps, active/retired lifecycle flags, and message-reference bounds when they can be proven. Higher-tier folds can consume lower-tier blocks. [[kernel types](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/types.ts)] [[compression implementation](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/compress.ts)] [[tool contracts](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/compress-tools.ts)]

Persistence is session-oriented. The proxy writes a versioned JSON envelope per session through an atomic temp-file-and-rename path, while unified SQLite storage can hold messages, blocks, content, references, and related state. The storage documentation describes one SQLite WAL writer and batched ingest; the compression state is also serialized as a JSON field alongside row tables. Optional zstd and AES-256-GCM encoding are configurable. [[persistence implementation](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/persist.ts)] [[storage architecture](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/docs/architecture/storage.md)]

Original folded messages can be held in per-session block-content snapshots. Large tool outputs may also enter a content-addressed store: SHA-256 deduplicates text, a message reference maps to metadata and a content hash, and retrieval resolves the original independently of a pruned message-reference map. Session objects can lazily reload block contents from persistence. [[session model](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/session.ts)] [[content store](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/content-store.ts)]

## Write, update, delete, and retrieval

**Write.** The model calls `compress` with message-reference bounds and a summary. The kernel validates/resolves the range, excludes protected or filtered messages, creates a block with direct/effective message IDs and summary metadata, and marks consumed child blocks inactive. Tiered folding records the relationship to earlier blocks. These are source-observed mechanics; this review did not perform a fold. [[compression implementation](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/compress.ts)] [[tool contracts](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/compress-tools.ts)]

**Update.** There is no generic fact editor. A restored block can be refolded in place under specific full-span/ancestor conditions. When optional block operations are enabled, `acp_rewrite` replaces an active block summary and retains one prior summary for a single-step rollback; a further rewrite overwrites that retained predecessor. [[kernel types](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/types.ts)] [[block operations](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/block-ops.ts)] [[tool contracts](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/compress-tools.ts)]

**Delete and retirement.** `acp_retire` removes an active block's summary from the resident prompt while retaining coverage and search/decompress access; `acp_restore` puts it back. These are visibility controls rather than erasure. The CLI's `bili sessions rm <id>` removes a session's files and unified-storage rows and releases content references; the store code deliberately retains pinned checkpoint replicas. Archive/restore is a separate session-management path. Erasure from external client histories, backups, or other retained checkpoints is not established by this review. [[block operations](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/block-ops.ts)] [[session commands](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/storage-maintenance.ts)] [[storage deletion](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/storage/store.ts)] [[CLI](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/cli.ts)]

**Retrieval.** `search_context` ranks stored block summaries with lexical search and can search retained folded originals for matching text; its result is a preview and block/message reference, not an answer-quality guarantee. It searches block history in the addressed session and can return inactive/consumed blocks. `decompress` restores a chosen block or subrange; `acp_retrieve` resolves a stored original message reference, with very large results exported to a file. A derived session can fall back to its recorded parent chain for read-only search. [[kernel search](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/search/index.ts)] [[search host](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/decompress-shared.ts)] [[content store](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/content-store.ts)] [[README](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/README.md)]

## Scope isolation and provenance

Session identity is the principal storage boundary: the session identifier keys its compression state, message references, and persisted contents. Identity documentation describes host session IDs and canonical message identity, with fallbacks for anonymous traffic. Ordinary search is session-local. The host has explicit foreign-session lookup machinery for a supplied target identifier, and derived-session search can read parent sessions; those paths are read-only. Thus session partitioning is visible in code, but a deployment's authentication and authorization around proxy endpoints remains important and was not adversarially tested. [[identity architecture](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/docs/architecture/identity.md)] [[session model](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/session.ts)] [[search host](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/decompress-shared.ts)] [[MCP integration](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/mcp.ts)]

Block records retain message IDs, reference spans, and the `compressCallId`; the content store retains a hash and raw message ID alias for each stored reference. These fields link a summary or retrieved payload back to session history, but the summary itself is written by the model and the inspected structures do not independently adjudicate whether it faithfully represents the source. The project prompts warn that summaries are fallible historical records. [[kernel types](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/types.ts)] [[content store](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/content-store.ts)] [[compression rules](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/compression-rules.ts)]

## Source-visible efficiency and observability

**Code observations.** The kernel tracks compressed-token counts, compression count, stored-message count, retrieval count, and context composition. `acp_status` reports visible text/tool/summary token breakdowns and block tiers; the proxy records request and cache usage fields and exposes status/cache reports. Session data can be lazily evicted from memory and reloaded; persistence is debounced. These are implementation and instrumentation observations, not measurements from this review. [[kernel types](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/types.ts)] [[status report](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/report.ts)] [[persistence](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/persist.ts)] [[session model](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/session.ts)]

**Documented claims.** The README reports context-token reduction and cache-hit goals, and links upstream operational and third-party benchmark material. Those are project-published claims for their stated versions and workloads; this source review did not reproduce them or treat them as results for the current head. [[README](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/README.md)]

## Metric-domain evidence

All comparison outcomes are unmeasured for this review. The source shows write/retrieval paths and lifecycle controls, but no workload was run to estimate answer quality, scope leakage, deletion leakage, or cost. [[metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

| Domain | Source observation | Status |
| --- | --- | --- |
| Answerable recall and abstention | Lexical block/original search and bounded previews are visible; answer quality and abstention are not scored here. | Unmeasured |
| Correction accuracy and stale values | Refold and optional summary rewrite paths exist; correction accuracy and stale-value rates were not measured. | Unmeasured |
| Deletion leakage | Session removal cascades through indexed content and releases unshared blobs; pinned checkpoint replicas can survive. No leak workload was run. | Unmeasured |
| Scope isolation | Session-keyed state and read-only foreign/derived lookup paths are visible; no cross-session attack workload was run. | Unmeasured |
| Evidence support and citation coverage | Blocks and stored entries preserve refs/IDs; summary truth and answer-level support were not adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Search and persistence paths are inspectable; no latency distribution or write-to-recall delay was collected. | Unmeasured |
| Tokens, cost, and storage efficiency | Counters and cache reporting exist; no current-head token, cost, or storage efficiency result was measured. | Unmeasured |

## Limits and unknowns

This review inspected selected official documentation and code at the verified repository head. It did not establish deployment reliability, summary faithfulness, answerable recall, adversarial scope isolation, complete deletion across every external copy, or runtime performance. The source review did not execute billion-context, benchmarks, or tests. Unknown means not established by these inspected sources. [[storage architecture](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/docs/architecture/storage.md)] [[identity architecture](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/docs/architecture/identity.md)] [[benchmark status](../results/initial-baselines-status.json)]

## Contact-list follow-up

The official pinned README was checked for a published contact email and none was found. The repository has no root `SECURITY.md` or `SUPPORT.md` at the reviewed revision. The JSON records `contact_email: null` and the checked README URL; no address was inferred from commit or profile metadata. [[README contact check](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/README.md)]

## Benchmark status

**Benchmark not run.** No billion-context runtime, benchmark workload, or tests were run. This article records source observations only. Project metric definitions, status, and fixture describe the comparison protocol, not billion-context results. [[metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Official repository](https://github.com/ranxianglei/billion-context)
- [Verified master head](https://github.com/ranxianglei/billion-context/commit/85afa7b212ce20981d66c9e6ecb1e944751cb3c4)
- [Official master commits feed](https://github.com/ranxianglei/billion-context/commits/master.atom)
- [Official README](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/README.md)
- [Unified storage architecture](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/docs/architecture/storage.md)
- [Session and message identity architecture](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/docs/architecture/identity.md)
- [Kernel data model](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/types.ts)
- [Compression implementation](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/compress.ts)
- [Content-addressed message store](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/content-store.ts)
- [Kernel search](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/search/index.ts)
- [Host search and retrieval routing](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/decompress-shared.ts)
- [Kernel tool contracts](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/compress-tools.ts)
- [Block lifecycle operations](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/block-ops.ts)
- [Persistence layer](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/persist.ts)
- [Session runtime](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/session.ts)
- [MCP integration](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/mcp.ts)
- [Session management commands](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/storage-maintenance.ts)
- [Unified storage store](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/src/storage/store.ts)
- [Status report implementation](https://github.com/ranxianglei/billion-context/blob/85afa7b212ce20981d66c9e6ecb1e944751cb3c4/kernel/src/report.ts)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster entry](../data/memory-systems.json)
- [Atlas attribution source (identity only)](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/billion-context.md)

**Verification boundary:** no system, tests, or benchmarks were run.
