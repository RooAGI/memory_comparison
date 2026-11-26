# GBrain source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 252 / GBrain / `gbrain`  
**Listed repository locator:** [garrytan/gbrain](https://github.com/garrytan/gbrain)  
**Canonical upstream:** [garrytan/gbrain](https://github.com/garrytan/gbrain)  
**Default branch / reviewed head:** master / [cab1738a937be08f646db31306796e49dccc83b2](https://github.com/garrytan/gbrain/commit/cab1738a937be08f646db31306796e49dccc83b2)  
**Review time:** 2026-11-25 20:50:57 UTC (2026-11-25 12:50:57 PST; America/Los_Angeles).

## Identity and review pin

The catalog identifies GBrain as ordinal 252, slug `gbrain`, with the explicit locator `https://github.com/garrytan/gbrain`; its Atlas attribution is retained only for roster identity and locator context. The official repository page identifies `master` as the default branch. GitHub’s official `master.atom` feed reported current head `cab1738a937be08f646db31306796e49dccc83b2`; the corresponding official commit patch agrees on that full SHA. The GitHub REST commit endpoint was rate-limited and was not used as corroboration. Source inspection below is pinned to this SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

GBrain is a self-hostable memory service and agent integration that presents Markdown pages and structured knowledge through CLI, MCP, and agent-specific setup. The README describes PGLite as the default personal engine and Postgres with pgvector for larger or shared brains. It combines keyword and semantic page search, graph retrieval, optional synthesis, and background maintenance. These are documented architecture and feature descriptions, not measured quality results.[[readme]][[engine]]

## Who and what

The README identifies Garry Tan as the builder and describes GBrain as the production brain behind his own agent deployments. The repository presents a CLI/server and MCP integration around a brain database and canonical Markdown content, rather than a standalone model. This statement follows the official README and does not infer additional maintainer identities.[[readme]][[repo]]

## Architecture and data model

The README describes two storage engines behind one `BrainEngine` contract: PGLite, a zero-configuration Postgres-compatible default for personal brains, and Postgres with pgvector for shared, larger, or multi-machine deployments. The TypeScript engine interface is broad and includes page, search, graph, timeline, source, and fact-related operations. The Rust engine is described as experimental and selected through explicit configuration; the README warns that some SQL-dependent operations are unavailable on it.[[readme]][[engine]]

Markdown files are the canonical representation for file-backed knowledge; the database is an index that can be rebuilt from those files. The README distinguishes those pages from database-only content, unresolved facts, history, and operational state, for which it calls out database backup. It also distinguishes a brain (database) from a source (a repository mounted in that brain).[[readme]]

## Write, update, delete, and retrieval

**Writes and updates.** The README documents explicit memory writes, importing or syncing Markdown sources, and optional signal capture after opt-in. It describes capture, page writes, graph auto-linking, and scheduled maintenance as distinct parts of the broader loop. For Git-backed sources, it says only committed files are read during sync; ordinary folders can be imported without Git. The README also describes source/provenance-aware fact and decision pages. The inspected engine contract confirms these are exposed through a common persistence interface, but this review did not trace each write operation through every backend implementation.[[readme]][[engine]]

**Update and deletion.** The README says canonical file deletions become soft deletes in the database index. It describes database state that cannot be reconstructed from Markdown, including unresolved facts and history, as requiring its own backup. It also distinguishes explicit import, sync, and maintenance choices. The README does not establish physical erasure from backups, embeddings, caches, or all derived data; those paths were not audited here.[[readme]][[engine]]

**Retrieval.** The README distinguishes raw `search`, which returns ranked source pages without answer generation, from `think`, which synthesizes an answer with source citations and a statement of gaps. It documents hybrid scoring with vector and keyword retrieval, reciprocal-rank fusion, source-tier boosting, and reranking. It also warns that a search index may still be rebuilding or a bounded vector scan may return short, incomplete results, so an empty result is not proof a page is absent. Embeddings and reranking may send text to configured providers; keyless mode is keyword-only, while synthesis needs a configured chat capability.[[readme]]

## Scope isolation

The README describes sources mounted within a brain, source routing, and access for personal and shared brains. It presents Postgres as the shared and multi-machine option and documents source-level organization and routing. The broad engine interface alone does not prove authorization correctness, and this source review did not exercise remote roles, household access rules, or adversarial cross-source reads. Isolation quality therefore remains unmeasured here.[[readme]][[engine]]

## Provenance and evidence

The README describes source citations in synthesized answers, source provenance on imported or extracted material, and a gap statement when the brain lacks support. It also says extracted graph edges are evidence to inspect rather than proof that a relationship is true. These are documented lineage and answer-format features; this review did not adjudicate any answer against its source, so citation support precision and factual accuracy are unknown.[[readme]]

## Efficiency and observability

The README documents keyword-only operation without embedding credentials, optional embedding and reranking providers, database health/repair commands, and background maintenance. It notes that configured embedding and reranking providers may receive text and incur charges. The repository page and engine interface provide no workload measurements in this review for latency, token use, cost, or storage efficiency. I did not run the system or inspect operational telemetry.[[readme]][[engine]][[metrics]]

## Metric-domain evidence

All project benchmark domains are **unmeasured in this review**. The project metric definitions and fixture describe evaluation scope, not results collected for this review. GBrain, its tests, and benchmarks were not run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Search and synthesis paths are documented; no query workload was scored. | Unmeasured |
| Correction accuracy and stale values | Page and source update paths are documented; no correction workload was run. | Unmeasured |
| Deletion leakage | File deletion is documented as a soft delete; no post-delete probes were run. | Unmeasured |
| Scope isolation | Brain/source organization is documented; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Synthesis is documented to cite pages and report gaps; no answers were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Search, indexing and maintenance are documented; no timings were collected. | Unmeasured |
| Tokens, cost and storage | Optional providers and storage modes are documented; no resource measurements were collected. | Unmeasured |

## Limits and unknowns

This is a pinned README and interface review, not a runtime, security, or quality assessment. The README summarizes a large, rapidly changing system; the engine contract confirms the shared interface but does not establish backend parity or each operation’s runtime semantics. Repository documentation itself warns that search readiness and vector scan bounds can affect completeness. Provider configuration affects whether retrieval is keyword-only or uses external embeddings, reranking, or synthesis.[[readme]][[engine]]

This inspection does not establish physical deletion across backups and derived indexes, answer correctness, citation support, or adversarial scope isolation. It also does not independently reproduce figures or test claims published in upstream docs. Those remain unknown without targeted source tracing and execution.[[readme]][[metrics]]

## Benchmark status

**Benchmark not run.** No GBrain runtime, tests, or benchmark workload was executed for this review. No recall, correction, deletion, isolation, citation, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned README publishes `support@gbrain.io` and describes hosted support. The address and exact pinned README URL are recorded in the JSON. No commit or profile metadata or third-party directory was used.[[readme]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas entry is included solely as roster attribution, not assessment evidence. See the structured record [gbrain.json](../data/system-reviews/gbrain.json) and [curated roster](../data/memory-systems.json).
