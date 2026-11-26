# enquire-mcp source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 229 / enquire-mcp / `enquire-mcp`  
**Listed repository locator:** [oomkapwn/enquire-mcp](https://github.com/oomkapwn/enquire-mcp)  
**Canonical upstream:** [oomkapwn/enquire-mcp](https://github.com/oomkapwn/enquire-mcp)  
**Default branch / reviewed head:** main / [5b60b277ddb4006c737dfc87c8b86e05441305f3](https://github.com/oomkapwn/enquire-mcp/commit/5b60b277ddb4006c737dfc87c8b86e05441305f3)  
**Review time:** 2026-11-25 19:57:08 UTC (2026-11-25 11:57:08 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists enquire-mcp at ordinal 229, slug `enquire-mcp`, with the explicit locator `https://github.com/oomkapwn/enquire-mcp`. Its pinned Atlas attribution is retained as roster context only; Atlas descriptions and capability marks are not assessment evidence. The official GitHub repository page identifies the canonical repository and default branch `main`. The official main commit feed identifies full head `5b60b277ddb4006c737dfc87c8b86e05441305f3`, updated 2026-10-22 08:46:47 UTC.[[catalog]][[atlas]][[repo]][[head]]

## Summary

enquire-mcp is a local-first MCP server and CLI that makes an Obsidian-format vault searchable by multiple agents. It combines lexical, TF-IDF, embedding, and optional reranking paths, and exposes note paths, excerpts, freshness metadata, and PDF page citations. This review describes selected source and official documentation only; it does not measure system behavior or performance.[[readme]][[api]]

## Who and what

The pinned README identifies Alex (@OomkaBear) as the builder. The repository presents enquire-mcp as an open-source TypeScript MCP server and CLI for a local vault; this does not establish a broader maintainer roster.[[readme]]

The vault files remain the source of truth. The server builds searchable local indexes and exposes MCP tools over stdio or HTTP; it is not a hosted memory database.[[readme]][[api]]

## Architecture and data model

The README describes a local retrieval stack over Markdown, Canvas, Bases, and optional PDFs. Depending on setup, search can use in-memory TF-IDF, persistent FTS5/BM25, local multilingual embeddings, and an optional cross-encoder reranker. Fused search uses reciprocal rank fusion, with optional HNSW for approximate vector retrieval.[[readme]][[fts]][[embed]]

The API reference documents tools, resources, and prompts over the vault. The tool surface includes note read/list, search, link and graph navigation, frontmatter and structured-format queries, and opt-in write tools. The repository also documents stdio and Streamable HTTP transports.[[api]][[readme]]

The inspected text-search response includes the query, search mode, number of scanned Markdown notes, and matches with vault-relative path, excerpt, score, line, and matched terms. Its score is an occurrence count within that response, not a calibrated probability.[[search]]

## Write, update, delete, and retrieval

**Write.** The default surface is read-only. Seven write tools are registered only with `--enable-write`: create, append, rename, replace, archive, set frontmatter, and append to a chat thread. The create implementation checks the vault and delegates to guarded note writing; overwrite must be explicitly requested.[[readme]][[api]][[write]]

**Update and delete.** Updates use file operations such as replace, rename, frontmatter changes, append, or archive, rather than a separate extracted-fact lifecycle. The README says destructive write operations support dry runs. No mutation sequence was executed in this review.[[readme]][[api]][[write]]

**Retrieval.** The umbrella search can fuse available lexical, TF-IDF, and embedding signals; optional BGE reranking rescales candidates. Dedicated tools cover exact text, semantic and full-text search, PDF reading, Canvas parsing, Dataview-style queries, and supported Bases filters. Results can carry source paths, snippets, age/staleness, per-signal scores, and PDF page markers.[[readme]][[api]][[search]]

**Scope isolation.** The server is configured for a vault and applies filesystem path checks to reads and writes; the README says symlinks resolving outside the vault are rejected. Read-path and exclusion policies and tool allow/disable lists can narrow access. These controls bound filesystem and tool access; they do not establish per-memory tenant authorization. HTTP deployment and operator configuration were not tested.[[readme]][[api]][[vault]]

## Provenance and evidence

Search results retain the source note path, and PDF results include page markers. The API guidance asks agents to cite note paths and treat retrieved vault content as untrusted data rather than instructions. These features make source material inspectable; they do not establish that a cited note entails a generated answer or that its claims are correct.[[readme]][[api]][[search]]

## Efficiency and observability

The documented retrieval tiers range from in-memory TF-IDF through persistent FTS5/BM25 and local embeddings, with optional reranking and HNSW. Search exposes per-signal scores and stage explanations; text search reports the number of scanned notes. These are implementation and observability features, not measured latency or efficiency for this review.[[readme]][[api]][[search]][[fts]][[embed]]

README reports a BGE reranking ablation and other retrieval examples. Those remain project-published figures; this review did not reproduce them.[[readme]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for enquire-mcp. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe project evaluation materials, not enquire-mcp results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Hybrid retrieval and evaluation tooling are documented; no answer or abstention was scored. | Unmeasured |
| Correction and stale values | Vault editing tools and freshness indicators exist; no correction sequence was assessed. | Unmeasured |
| Deletion leakage | Archive and destructive write surfaces are documented; no post-delete probe was run. | Unmeasured |
| Scope isolation | Vault path checks and tool-surface controls are documented; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Results include source paths and PDF page markers; no answer claim was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | README includes project-reported figures; this review collected no timings. | Unmeasured |
| Tokens, cost, and storage | No workload token counts, charges, or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This bounded review covers the official README, API reference, and selected search, write, vault, FTS5, and embedding database paths at the verified head. The system, tests, and benchmarks were not run.[[readme]][[api]][[search]][[write]][[vault]][[fts]][[embed]]

Source presence and README benchmark claims do not establish recall quality, abstention, latency, cost, privacy outcomes, deletion behavior, or deployment security. These remain unverified here.[[readme]][[metrics]][[fixture]][[status]]

The implementation targets an Obsidian-format vault and documents supported subsets of Canvas, Dataview, Bases, and PDF handling. Format edge cases, large-vault behavior, concurrent edits, index repair, and real HTTP deployment were not assessed.[[readme]][[api]][[vault]][[fts]][[embed]]

## Benchmark status

**Benchmark not run.** No enquire-mcp runtime, tests, or benchmarks were executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned README publishes `oomkapwn@gmail.com` for vulnerability contact; this is the only contact email recorded. It was not inferred from commit/profile metadata or taken from a third-party directory.[[readme]]

## Sources

Repository file citations are pinned to the verified full SHA. The Atlas attribution is included only for curated identity and locator context. See the structured record [enquire-mcp.json](../data/system-reviews/enquire-mcp.json) and the [curated roster](../data/memory-systems.json).
