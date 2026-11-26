# Cortexes

## Identity and review pin

- Catalog ordinal: 164
- System: Cortexes
- Slug: `cortexes`
- Listed repository: https://github.com/XBlueSky/cortexes
- Roster attribution: explicit repository locator; the pinned Atlas entry is recorded for identity/locator context only, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortexes.md)).
- Canonical upstream: https://github.com/XBlueSky/cortexes
- Default branch: `plugin`
- Reviewed full head: [4bcbd96230cab4b46d2be9a47f3df9f1efacf65c](https://github.com/XBlueSky/cortexes/commit/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c)
- Review timestamp: 2026-11-25T09:47:42Z (UTC; 2026-11-25 01:47:42 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub’s branches page marks `plugin` as the default branch. The official plugin branch Atom feed reports head `4bcbd96230cab4b46d2be9a47f3df9f1efacf65c`, updated at 2026-11-25T03:54:58Z; the commit page confirms the full revision. ([repository](https://github.com/XBlueSky/cortexes), [branches](https://github.com/XBlueSky/cortexes/branches), [plugin history](https://github.com/XBlueSky/cortexes/commits/plugin.atom), [head commit](https://github.com/XBlueSky/cortexes/commit/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c))

## Summary

Cortexes is a Claude Code plugin that records sessions into a Markdown-and-git vault, offers workflows to distill and edit knowledge pages, and retrieves them with a local BM25 index plus an optional Chroma vector index. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md))

## Who and what

The official README describes Cortexes as a personal knowledge-vault plugin for Claude Code. The Markdown vault is the source of truth; search indexes are derived local data. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md))

## Architecture and data model

The repository separates Claude Code commands, skills and lifecycle hooks from the Python `cortex-vec` indexing/search CLI. The vault is organized into Raw session records, Notes, Projects, `_index.md` and `log.md`; the Chroma vector index and pickled BM25 index live under `~/.cortex/`. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [vector store](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/store.py), [BM25 index](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/bm25.py))

SessionStart surfaces vault status and a menu; SessionEnd filters and writes session material to Raw. Manual evolve writes a page and updates the index/log before calling `cortex-vec upsert`. Distill turns Raw records into Notes or Projects pages, and broadcast merges new material into existing pages. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [SessionEnd recorder](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/hooks/scripts/session-end-record.sh), [evolve workflow](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-evolve/SKILL.md))

The vector store keeps page documents and metadata in Chroma. The lexical index stores tokenized records as a pickle and reconstructs BM25 scoring state when loaded. Search can combine vector, lexical and optional wikilink-neighbor streams. ([vector store](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/store.py), [BM25 index](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/bm25.py), [fusion](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/fusion.py))

## Write, update, delete, and retrieval

**Write.** SessionEnd filters the transcript before recording it under Raw; the README says sessions over 4 KB are recorded automatically, without a per-session prompt, and `CORTEX_SKIP_RECORD=1` opts out for a session. Manual evolve writes Markdown pages to Notes or Projects with title/tag/date/source frontmatter, updates `_index.md` and `log.md`, and calls `cortex-vec upsert`. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [recorder](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/hooks/scripts/session-end-record.sh), [evolve](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-evolve/SKILL.md))

**Update and curation.** Evolve can modify saved Markdown pages; distill selects material from Raw for Notes/Projects, and broadcast fuses new material into existing pages. The article store remains editable Markdown, with git as its revision history. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [evolve](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-evolve/SKILL.md))

**Delete and retention.** The CLI exposes `cortex-vec delete <path>` for an indexed page; the BM25 implementation removes the corresponding document record and the vector store deletes the indexed document. Removing a vault file alone does not remove committed copies from git history. The privacy policy says the user controls retention and describes deleting files, rewriting history when needed, and removing/rebuilding derived indexes. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [BM25 index](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/bm25.py), [vector store](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/store.py), [privacy policy](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/PRIVACY.md))

**Retrieval.** Search defaults to BM25 plus vector results combined with reciprocal-rank fusion; the documented default weights are 0.4 for BM25 and 0.6 for vectors. It can degrade to BM25-only when embeddings are unavailable. Optional graph-neighbor expansion and LLM reranking are off by default. The query workflow then reads specific files or uses grep for exact matching; Raw search is reserved for requests about session history. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [fusion](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/fusion.py), [query workflow](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-query/SKILL.md))

## Scope isolation

The `--repo` filter narrows Projects pages by repository; Notes are cross-repository by design. Type and category filters are also available. The filter is part of retrieval in the configured vault, not a tenant boundary. It depends on the caller supplying the right repository context, while the query skill includes a broad-search route when the user asks for it. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [query workflow](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-query/SKILL.md), [fusion](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/fusion.py))

## Provenance and evidence

Saved pages can carry title, tags, date, source and repository metadata, and the vault keeps git history and a chronological log. Raw records include session context and are filtered before they are saved. Search results provide metadata and summaries but not source excerpts; the query workflow reads the underlying file for precise content. I found no enforced claim-level citation or evidence object for arbitrary generated answers in the inspected paths. ([evolve workflow](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-evolve/SKILL.md), [SessionEnd recorder](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/hooks/scripts/session-end-record.sh), [query workflow](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-query/SKILL.md), [README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md))

## Efficiency and observability

The local BM25 index stores token records, while Chroma stores vector documents and summaries. Search fuses ranked streams and limits result counts; the CLI reports degraded streams and index status. The project states it has no telemetry or usage reporting. These are source and documentation observations, not measurements. ([BM25 index](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/bm25.py), [vector store](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/store.py), [fusion](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/fusion.py), [README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [privacy policy](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/PRIVACY.md))

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Cortexes. No runtime, test suite, or benchmark was run; the fixture and metric definitions are protocol material, not Cortexes results. ([metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), [execution-status record](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Hybrid retrieval and empty-result reporting exist; no scored answer or abstention probes were run. |
| Correction accuracy and stale-value rate | Unmeasured | Pages can be edited or fused through evolve/broadcast; no correction workload was adjudicated. |
| Deletion leakage | Unmeasured | Indexed documents can be deleted and users can remove files/history; no residual-content probes were run. |
| Scope isolation | Unmeasured | Repo filtering applies to Projects while Notes remain cross-repository; no leakage workload was run. |
| Evidence support and citation coverage | Unmeasured | Files retain metadata and history; no answer-citation scoring was run. |
| Retrieval latency | Unmeasured | No timing samples were collected. |
| Write-to-recall delay | Unmeasured | No timed write/recall probes were run. |
| Tokens and cost | Unmeasured | Provider/model settings are documented; no runtime use or charge data was collected. |
| Storage efficiency | Unmeasured | No corpus-attributed vault or index sizes were collected. |

The README includes retrieval-evaluation instructions and descriptions of upstream experiments. They are not this project's measurements and were not independently re-run for this review. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [metric definitions](../METRICS.md), [execution-status record](../results/initial-baselines-status.json))

## Limits and unknowns

This bounded review inspected the official README, privacy and security policies, SessionEnd recorder, manual save and query workflows, and selected current indexing, lexical retrieval, vector storage and fusion code. It did not inspect every command, hook, parser branch, model provider, vault mutation, or deployment environment. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [recorder](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/hooks/scripts/session-end-record.sh), [evolve](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-evolve/SKILL.md), [query](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-query/SKILL.md), [vector store](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/store.py), [BM25 index](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/bm25.py), [fusion](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/fusion.py))

No Cortexes runtime, tests, or benchmarks were run. This review therefore does not establish retrieval quality, abstention quality, actual cross-project isolation, correction reliability, deletion leakage, latency, token/cost totals, or storage efficiency. The default vault scope is one configured vault; removing a file does not remove its committed history or erase content already sent to providers. ([privacy policy](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/PRIVACY.md), [metric definitions](../METRICS.md), [execution-status record](../results/initial-baselines-status.json))

## Contact

No contact email is published in the official README or SECURITY.md at the reviewed revision. The README directs security issues to private vulnerability reporting, while SECURITY.md describes that reporting path; the privacy policy directs privacy questions to GitHub issues. No profile/commit metadata or third-party directory was used. ([README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md), [SECURITY.md](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/SECURITY.md), [PRIVACY.md](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/PRIVACY.md))

## Benchmark status

**Benchmark not run.** Cortexes, its tests, and benchmark workloads were not run. Project metric definitions and the fixture specify measurement protocol; the project status record has no Cortexes measurement. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortexes.md)
- [Official repository](https://github.com/XBlueSky/cortexes)
- [Default branches page](https://github.com/XBlueSky/cortexes/branches)
- [Plugin branch feed](https://github.com/XBlueSky/cortexes/commits/plugin.atom)
- [Reviewed full head 4bcbd96230cab4b46d2be9a47f3df9f1efacf65c](https://github.com/XBlueSky/cortexes/commit/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c)
- [Pinned README](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/README.md)
- [Pinned privacy policy](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/PRIVACY.md)
- [Pinned security policy](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/SECURITY.md)
- [Pinned SessionEnd recorder](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/hooks/scripts/session-end-record.sh)
- [Pinned evolve workflow](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-evolve/SKILL.md)
- [Pinned query workflow](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/skills/cortex-query/SKILL.md)
- [Pinned vector store](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/store.py)
- [Pinned BM25 index](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/bm25.py)
- [Pinned retrieval fusion](https://github.com/XBlueSky/cortexes/blob/4bcbd96230cab4b46d2be9a47f3df9f1efacf65c/cortex-vec/src/cortex_vec/fusion.py)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project execution-status record](../results/initial-baselines-status.json)
