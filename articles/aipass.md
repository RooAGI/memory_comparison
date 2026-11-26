# AIPass source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 46 / AIPass / aipass  
**Listed repository locator:** [AIOSAI/AIPass](https://github.com/AIOSAI/AIPass)  
**Current canonical repository:** [AIOSAI/AIPass](https://github.com/AIOSAI/AIPass)  
**Default branch / reviewed head:** main / 7670b1131a63ffa5699a9f620e37cccddc725979  
**Review time:** 2026-11-24 20:15:01 UTC (12:15:01 PST; America/Los_Angeles).

## Identity and scope

The curated roster places **AIPass** at ordinal 46 with slug `aipass`, the listed locator above, and an Atlas attribution URL. I used the roster entry only for identity, repository locator, and attribution; its descriptions, marks, and layout were not assessment evidence. The official repository page identifies `main`; its `main` Atom feed and a fresh `git ls-remote --symref` both identify full head `7670b1131a63ffa5699a9f620e37cccddc725979`. A shallow checkout of that head matched the remote revision.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/AIOSAI/AIPass)] [[main commit feed](https://github.com/AIOSAI/AIPass/commits/main.atom)] [[reviewed commit](https://github.com/AIOSAI/AIPass/commit/7670b1131a63ffa5699a9f620e37cccddc725979)]

AIPass is a local agent workspace and orchestration system. Its in-tree `@memory` branch stores agent memory in plain JSON files, rolls older entries into ChromaDB vectors, and offers semantic search across branches. It also manages the shared entry shape, size limits, and todo backlog. The project README describes the system as Linux-first and emphasizes per-agent identity and memory.[README](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/README.md) [[memory branch README](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/README.md)]

## Architecture and data model

The memory module separates CLI routing in `apps/memory.py` and verb modules in `apps/modules/` from handlers for JSON I/O, rollover, templates, monitoring, search, storage, and schema normalization. Its README describes the source data as each branch's `.trinity/` JSON files: sessions, learnings, observations, and todos. The configured `memory.config.json` defines the closed entry field shape, character caps, keep counts, and whole-file budgets; templates provide canonical prose and entry content is authored by the agent.[[memory README](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/README.md)] [[trinity standard](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/trinity_standard.md)] [[entry limits](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/json/entry_limits.py)] [[config loader](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/json/config_loader.py)]

Rollover embeds the oldest entries after configured counts are exceeded, writes them to a global Chroma store and, when available, a branch-local `.chroma` store, then trims the live file. Chroma collections are named by branch and memory type; IDs use a content hash, salted by source file when present, so repeated upserts are idempotent. Metadata accompanies documents. Todos instead move to a per-branch backlog and are not vectorized.[[rollover pipeline](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/rollover_pipeline.md)] [[Chroma subprocess](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/storage/chroma_subprocess.py)] [[todo and backlog docs](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/todos_and_backlog.md)]

## Write, update, delete, and retrieval

**Write and update.** A memory JSON write is fenced to the AIPass root, checked against the configured field and character limits, written to a same-directory temporary file, and atomically replaced. The gate rejects malformed or unmeasurable authored entries; unchanged carried entries can be reported without blocking a shrinking write. Updates are ordinary file edits through that write path; no separate versioned record history for each edit was established by the reviewed sources.[[memory file I/O](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/json/memory_files.py)] [[trinity standard](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/trinity_standard.md)]

**Rollover and removal.** The documented pipeline extracts the oldest excess entries, embeds and stores them, and writes the trimmed JSON only after global storage succeeds. Content-hash IDs support retry without duplicate vectors. The separate `push` lane rebuilds canonical metadata, archives non-canonical entries verbatim, reads them back by ID, and compares the stored content before pruning; failed verification leaves the branch file intact. The reviewed live command documentation describes rollover and push, but does not establish a user-facing permanent-delete or vector-expungement command. Storage-level source-based deletion exists for internal maintenance; its end-user lifecycle and completeness across local/global copies are not established.[[rollover pipeline](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/rollover_pipeline.md)] [[trinity push](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/trinity_push.md)] [[memory module inventory](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/modules/push.py)] [[storage deletion implementation](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/storage/chroma_subprocess.py)]

**Retrieval.** `drone @memory search` encodes the query with fastembed in a subprocess, searches Chroma, filters empty results and similarities below 0.40, and returns up to the requested result count (default five). It can filter by branch and memory type; with neither filter, the global archive can search across branches. Exact plan IDs get a metadata lookup and can be pinned above semantic results. The system uses `sentence-transformers/all-MiniLM-L6-v2`; the model is cached or downloaded, and there is no documented fallback if it cannot load. Search is over archived content, so live JSON entries are not thereby shown to participate in this vector search.[[vector search docs](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/vector_search.md)] [[search query executor](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/search/query_executor.py)] [[Chroma subprocess](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/storage/chroma_subprocess.py)]

## Scope isolation and provenance

Each memory entry and vector collection is associated with branch and memory type. Search can narrow to a branch, and storage uses branch-specific collection names. The monitor separates writes from reads: rollover's write scope is registry-based and fenced to the AIPass root, while read-only operations may include external projects declared through roots. Branch and project names are scope labels, not authenticated identities by themselves; the reviewed code does not establish a tenant-grade authorization boundary for vector search.[[detector and scope](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/monitor/detector.py)] [[vector search docs](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/vector_search.md)] [[write fence](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/write_fence.py)]

The vector metadata includes source file and timestamp fields where supplied; trinity push additionally constructs archive metadata identifying branch, source, and archive operation. Verification before pruning demonstrates preservation of the archived entry text, not a complete source citation chain for generated answers. No answer-citation mechanism or adjudicated evidence-support behavior was established in this review.[[Chroma subprocess](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/storage/chroma_subprocess.py)] [[trinity push](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/templates/trinity_push.py)] [[trinity push docs](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/trinity_push.md)]

## Source-visible efficiency and observability

**Code observations.** ML work runs in subprocesses, keeping fastembed and ChromaDB out of the main process. The model is loaded from cache or downloaded; embedding requests have timeouts, and search has a store timeout. Rollover processes entries in batches. The source documents a 0.40 similarity threshold, default top-five return size, per-entry caps, and configured keep counts. These implementation choices are not measurements of latency, throughput, token use, cost, or storage efficiency.[[vector search docs](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/vector_search.md)] [[query executor](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/search/query_executor.py)] [[rollover orchestrator](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/rollover/orchestrator.py)] [[memory configuration](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/json/config_loader.py)]

**Observability observations.** The handlers emit structured operation records, log rollover stages and search counts, and report subprocess failure reasons including exit status and a bounded stderr tail. The memory branch also exposes lint, health, rollover status, and verification commands. These diagnostics describe code paths, not observed operational reliability.[[query executor](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/search/query_executor.py)] [[storage lane](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/storage/lane.py)] [[rollover orchestrator](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/rollover/orchestrator.py)] [[memory README](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/README.md)]

## Metric-domain evidence

All outcome domains below are **unmeasured**. Source behavior is not a benchmark result.[[metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

| Domain | Source observation | Status |
| --- | --- | --- |
| Answerable recall and abstention | Semantic search, a similarity threshold, and top-result limit are visible; answer quality and abstention were not evaluated. | Unmeasured |
| Correction accuracy and stale values | File edits and archival are visible; no correction workload or stale-value adjudication was run. | Unmeasured |
| Deletion leakage | Rollover and push prune only after archive, while user-facing permanent deletion was not established. No deletion probes were run. | Unmeasured |
| Scope isolation | Branch filters and registry fences exist; no cross-branch isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Archive metadata records source details, but answer support/citation behavior was not adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Subprocess timeouts and model caching are source-visible; end-to-end timings and delay were not measured. | Unmeasured |
| Tokens, cost, and storage efficiency | No token, cost, or storage measurements were collected. | Unmeasured |

## Limits and unknowns

The review covered the official root and memory READMEs, memory architecture documentation, the trinity and rollover/push/vector-search docs, and current handler source for JSON writes, search, storage, scope detection, and rollover. It did not inspect every memory module or all integration callers. In particular, this review cannot establish production retrieval quality, whether search results are always correctly scoped by every caller, complete deletion semantics across stores, or real resource use. The project's published memory docs describe a semantic archive, but they do not establish that every live entry is searchable before rollover. Unknown means not verified in this bounded source review.[[memory README](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/README.md)] [[trinity standard](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/trinity_standard.md)] [[vector search docs](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/vector_search.md)] [[detector](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/monitor/detector.py)]

## Contact-list follow-up

The official pinned `SECURITY.md` publishes `aipass.system@gmail.com` for vulnerability reports. The official README and project website were also checked; the email is attributed only to the security policy, not inferred from commit or profile metadata.[[security contact](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/SECURITY.md)] [[README](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/README.md)] [[official project website](https://aipass.ai/)]

## Benchmark status

**Benchmark not run.** No AIPass runtime, tests, or benchmark workloads were executed. The project metric definitions, fixture, and baseline status are protocol references; they are not AIPass measurements.[[metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical repository and default branch](https://github.com/AIOSAI/AIPass)
- [Reviewed default-ref commit](https://github.com/AIOSAI/AIPass/commit/7670b1131a63ffa5699a9f620e37cccddc725979)
- [Official root README](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/README.md)
- [Memory branch README](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/README.md)
- [Trinity standard](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/trinity_standard.md)
- [Rollover pipeline](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/rollover_pipeline.md)
- [Trinity push](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/trinity_push.md)
- [Vector search](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/docs/vector_search.md)
- [Memory file I/O](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/json/memory_files.py)
- [Entry limits](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/json/entry_limits.py)
- [Memory configuration loader](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/json/config_loader.py)
- [Search query executor](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/search/query_executor.py)
- [Storage lane](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/storage/lane.py)
- [Chroma subprocess](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/storage/chroma_subprocess.py)
- [Rollover orchestrator](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/rollover/orchestrator.py)
- [Scope detector](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/monitor/detector.py)
- [Write fence](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/write_fence.py)
- [Push implementation](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/src/aipass/memory/apps/handlers/templates/trinity_push.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster identity and attribution only](../data/memory-systems.json)
- [Atlas roster attribution source (identity only)](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/aipass.md)
- [Official published contact](https://github.com/AIOSAI/AIPass/blob/7670b1131a63ffa5699a9f620e37cccddc725979/SECURITY.md)
- [Official project website](https://aipass.ai/)

**Verification boundary:** no AIPass runtime, tests, or benchmarks were run.
