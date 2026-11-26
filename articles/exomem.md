# Exomem source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 233 / Exomem / `exomem`  
**Listed repository locator:** [Artexis10/exomem](https://github.com/Artexis10/exomem)  
**Canonical upstream:** [substrate-systems/evermatter](https://github.com/substrate-systems/evermatter)  
**Default branch / reviewed head:** main / [5ef9dfb10e4b948390293bd14d9c5ff6a41e0269](https://github.com/substrate-systems/evermatter/commit/5ef9dfb10e4b948390293bd14d9c5ff6a41e0269)  
**Review time:** 2026-11-25 20:11:28 UTC (2026-11-25 12:11:28 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists Exomem at ordinal 233, slug `exomem`, with the explicit locator `https://github.com/Artexis10/exomem`. That locator redirects to the official `substrate-systems/evermatter` repository; its README identifies Evermatter as “formerly Exomem.” The catalog's pinned Atlas entry is included only for roster attribution and locator context; it is not assessment evidence. GitHub's official repository page identifies `main` as the default branch, and its official commits API identifies full current head `5ef9dfb10e4b948390293bd14d9c5ff6a41e0269`.[[catalog]][[atlas]][[repo]][[head]]

## Summary

The current project describes a local-first memory server for agent clients that reads and writes a user's Markdown/Obsidian vault through MCP, CLI, and REST interfaces. Its design separates captured Sources, authored knowledge pages, and Evidence; retrieval combines lexical, semantic, and graph-related paths. This review is limited to public source and documentation, not runtime behavior.[[readme]][[find]]

## Who and what

The official README identifies the repository as Evermatter, formerly Exomem, and describes it as a memory server and library that works over an owned Markdown vault. It exposes MCP tools and shared CLI/REST operations. No individual maintainer identity is inferred for this review.[[readme]]

## Architecture and data model

The README describes Markdown pages under a governed Knowledge Base as the user-owned content, with sidecar indexes for search and graph/resolver data. The current search module says it scans Markdown pages, parses frontmatter, applies structured filters, and performs text matching; it caches parsed pages in process and invalidates them by file modification time.[[readme]][[find]]

The documented memory types separate raw captured Sources, compiled notes, entities, Evidence, and superseded conclusions. The README also describes typed Record and Planning collections. The reviewed files show indexes and operation history being updated alongside page writes. These structures preserve organization and links; they do not establish that a stored statement is true.[[readme]][[add]][[semantic_writes]]

## Write, update, delete, and retrieval

**Write.** The documented `add` operation captures a raw Source page, while `note` creates authored, typed knowledge pages. The implementation describes preparing the page, indexes, and operation log together and using a batch-atomic write. The inspected path does not establish autonomous extraction of memories from arbitrary conversations; the documented client or agent invokes the write tools.[[readme]][[add]]

**Update and correction.** The `edit` path patches a compiled page. `replace` marks the predecessor superseded and writes a successor linked to it; the implementation refuses to claim success if it cannot safely mark the predecessor. Supersession preserves history, but does not itself demonstrate that retrieval always excludes stale conclusions.[[readme]][[replace]]

**Delete.** The documented Tier-2 `delete_file` operation moves a page to dated `_trash` with recovery metadata; permanent removal is outside that tool. The implementation requires explicit confirmation and protects append-only Sources and Evidence from ordinary deletion. This review did not test recovery, store-backed deletion, or downstream replicas.[[readme]][[delete]]

**Retrieval.** The README documents `find` and `ask_memory` for searches, and `recall_context` for a bounded context packet or abstention. The inspected `find` module performs structured filtering and text matching, has semantic lanes and cache/degradation counters, and separates page parsing from result caching. The README describes FTS5/BM25 and optional embedding and media paths. These are implementation and documentation observations, not independently scored recall or abstention results.[[readme]][[find]]

**Scope isolation.** The governance policy loader defines selectors for paths, projects, tags, types, classes, and references; the README documents project/type/tag filters and a release plane for audiences. This establishes that scope controls exist in the code and product design. The review did not trace every caller through the complete authorization and release path or test cross-scope leakage, so enforcement strength remains unmeasured.[[policy]][[readme]]

## Provenance and evidence

The documented model keeps raw Sources and append-only Evidence separate from compiled conclusions. Replacement records a predecessor relationship and its content hash in the mutation path; writes also update the vault activity log. Those mechanisms provide lineage and change context, not independent verification of a source or proof that an authored claim follows from it.[[readme]][[replace]][[semantic_writes]][[add]]

## Efficiency and observability

The README describes FTS5/BM25 lexical search, optional local text/image embeddings, and deferred media processing. The search module contains cache status and process-scoped degradation counters, and the writer uses operation spans and logs. These support operational visibility, but this review did not measure resource use or inspect a deployed dashboard/retention configuration.[[readme]][[find]][[add]]

The README reports a retrieval benchmark of 864 ms at 50,000 notes on a reference desktop. That is an upstream-reported figure, not reproduced in this review and not a result in this project's benchmark record.[[readme]]

## Metric-domain evidence

All comparison-project benchmark domains are **unmeasured** for Exomem. The [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the evaluation protocol/status, not Exomem results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Text/semantic search and bounded context retrieval are documented; no cases were scored. | Unmeasured |
| Correction and stale values | Edit and linked supersession paths exist; no correction probes were run. | Unmeasured |
| Deletion leakage | Recoverable trash and append-only protections are documented; no deletion probes were run. | Unmeasured |
| Scope isolation | Governance selectors and release controls exist; no adversarial scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Sources and Evidence are distinct memory types; no claim-evidence adjudication was performed. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timing workload was run. | Unmeasured |
| Tokens, cost, and storage | No such measurements were collected. | Unmeasured |

## Limits and unknowns

The catalog's listed Exomem URL now redirects to a renamed repository. This review follows the canonical official repository and pins observations to its current `main` head. GitHub briefly returned an error page while opening one source path; that path was not used as evidence.[[catalog]][[repo]][[head]]

The inspected material cannot establish production deployment settings, full authorization behavior across all entry points, deletion behavior across backups or replicas, factual correctness of memories, or measured system performance. The upstream README's reported retrieval number was not reproduced here.[[readme]][[policy]]

## Benchmark status

**Benchmark not run.** No Exomem runtime, tests, or benchmarks were executed. No recall, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json); these files define project protocol/status and contain no Exomem measurement.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email and none was present. The structured record stores `contact_email: null` and that exact checked URL. No email was inferred from commit/profile metadata or third-party directories.[[readme]]

## Sources

Upstream repository source citations use the verified full SHA. The Atlas entry is recorded only for roster attribution and locator context. See the structured record [exomem.json](../data/system-reviews/exomem.json) and the [curated roster](../data/memory-systems.json).
