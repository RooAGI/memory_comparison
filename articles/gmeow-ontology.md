# GMEOW source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 261 / GMEOW / `gmeow-ontology`  
**Listed repository locator:** [Blackcat-Informatics/gmeow-ontology](https://github.com/Blackcat-Informatics/gmeow-ontology)  
**Canonical upstream:** [Blackcat-Informatics/gmeow-ontology](https://github.com/Blackcat-Informatics/gmeow-ontology)  
**Default branch / reviewed head:** main / [c0139e0018f5b64b2f81a32e2dfe542522b26f4f](https://github.com/Blackcat-Informatics/gmeow-ontology/commit/c0139e0018f5b64b2f81a32e2dfe542522b26f4f)  
**Review time:** 2026-11-25 21:11:44 UTC (2026-11-25 13:11:44 PST; America/Los_Angeles).

## Identity and review pin

The catalog identifies GMEOW as ordinal 261, slug `gmeow-ontology`, with the explicit listed locator `https://github.com/Blackcat-Informatics/gmeow-ontology`. Its pinned Atlas attribution is retained only for roster identity and locator context; Atlas descriptions and capability marks are not assessment evidence. The official repository page identifies `main` as the default branch, and the official `main.atom` feed reports full current head `c0139e0018f5b64b2f81a32e2dfe542522b26f4f`. This inspection is pinned to that SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

GMEOW is a Rust-first ontology project whose MCP server also exposes a grounded-memory triad: store claims, recall them, and revise beliefs by suppressing superseded claims. The guide describes the memory as an append-only, content-addressed GTS ai-package stored at a configurable path. These are documentation and code observations; no runtime quality or efficiency was measured.[[mcp-guide]][[storage]]

## Who and what

The official repository presents GMEOW as an ontology project with a native CLI and MCP server. The MCP surface combines grounded-memory tools with ontology lookup, but the review here focuses on the memory tools and their storage boundary rather than assessing the full ontology reasoning and projection system.[[repo]][[mcp-guide]][[mcp-source]]

## Architecture and data model

The documented client setup launches `gmeow mcp` over stdio and sets `GMEOW_MEMORY_PATH`, defaulting to `~/.gmeow/memory.gts`. The guide describes that file as a content-addressed, append-only GTS ai-package intended to survive across sessions, models, and vendors. It separately describes ontology lookups as reading a bundled `gmeow.gts` snapshot, so the memory file and ontology bundle have distinct roles.[[mcp-guide]][[mcp-source]]

A memory item is a reified RDF 1.2 claim. The documented response includes a minted claim ID, text, creation time, and optional confidence, `according_to` standpoint, and source label. In the implementation, the storage module defines a `ClaimStore` seam for storing, recalling, and revising claims. The native backend delegates claim and revision behavior to `purrdf::gts::examples::agent_memory::Memory`; the lower-level claim encoding is owned by that dependency and was not inspected in this review.[[mcp-guide]][[storage]]

The same storage source documents a browser backend that stores claims in process memory and implements recall and revision. That backend has a shorter persistence lifetime than the native file-backed path.[[storage]]

## Write, update, delete, and retrieval

**Write.** `store_claim` appends one well-formed claim. The guide documents optional confidence in [0, 1], a source label, and a `according_to` standpoint. Contradictory claims may coexist; the documented approach is to store both rather than have the system automatically adjudicate which is true. The guide also documents transaction-gated writes and a non-committing `dry_run` path.[[mcp-guide]][[mcp-source]]

**Update and deletion.** `revise_belief` requires an existing claim identifier, records suppression, and may link a successor. The guide describes revision as suppression rather than deletion, retaining the previous belief for audit. The documented memory tool set does not include a hard-delete operation; physical erasure outside those tools was not established.[[mcp-guide]][[mcp-source]]

**Retrieval.** `recall` returns recent claims for an empty query and otherwise ranks claims by case-insensitive token overlap. The API accepts an optional confidence floor and result limit, with a documented default limit of 10. Suppressed claims are omitted by default; `include_suppressed=true` enables an audit view with suppression flags. These documented behaviors do not establish retrieval relevance or abstention quality.[[mcp-guide]]

**Write gate.** The guide says writes execute through the native Transaction-Logic engine. A well-formed claim is the store precondition; revision requires the target claim to exist. A dry run computes the verdict and discards the effect. No write or retrieval operation was executed for this review.[[mcp-guide]][[mcp-source]]

## Scope isolation

The native memory path is chosen with `GMEOW_MEMORY_PATH`, which gives deployments a file-level storage boundary. The per-claim `according_to` field records a standpoint; the documented recall options do not describe it as an access-control filter. This inspection did not establish user, project, or tenant isolation guarantees and did not exercise cross-scope reads.[[mcp-guide]][[storage]]

## Provenance and evidence

A stored claim may include a source label and standpoint, and the response includes a creation timestamp. The guide also says committed writes record tool-call context, including the action schema, turn anchor, start state, timestamp, and temporal frame, for read-only trajectory audit. These fields record attribution and operation context; this review did not validate source materials, adjudicate truth, or test whether retrieved answers are supported by cited evidence.[[mcp-guide]][[storage]]

## Efficiency and observability

The documented native deployment uses a single GTS file, and the storage abstraction has a separate in-process browser implementation. The MCP guide describes audit records and dry-run witnesses, but this review found no measured workload for recall latency, write-to-recall delay, tokens, cost, or storage efficiency. The storage source delegates native claim operations to the purrdf memory implementation, so its lower-level I/O and concurrency behavior were not assessed.[[mcp-guide]][[storage]][[metrics]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for GMEOW in this review. The project metric definitions and fixture specify evaluation scope; they are not GMEOW results. The system, tests, and benchmarks were not run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Token-overlap ranking and empty-query recency are documented; no queries were scored. | Unmeasured |
| Correction accuracy and stale values | Suppression and successor linkage are documented; no correction sequence was evaluated. | Unmeasured |
| Deletion leakage | The tool set documents suppression rather than deletion; no leakage probes were run. | Unmeasured |
| Scope isolation | A configurable file path and standpoint metadata are documented; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Source labels and audit context are documented; no answer was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timings were collected. | Unmeasured |
| Tokens, cost, and storage | No resource measurements were collected. | Unmeasured |

## Limits and unknowns

This is a bounded source review, not a runtime, security, or benchmark assessment. The MCP guide documents the tool contract, while the storage code delegates the lower-level claim implementation to purrdf; that dependency was not inspected here. The review therefore does not establish behavior under concurrency, crash recovery, backup/restore, or storage corruption.[[mcp-guide]][[storage]][[mcp-source]]

Source and standpoint metadata do not prove the underlying claim, verify source material, or calibrate confidence. The documented surface does not establish a hard-delete path or tenant authorization. Physical erasure, recovery, key custody, and user/project isolation remain unknown from the inspected sources.[[mcp-guide]][[storage]]

## Benchmark status

**Benchmark not run.** No GMEOW runtime, tests, or benchmark workload was executed. No recall, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The project metric definitions, fixture, and shared execution record describe the protocol and status, not a GMEOW measurement.[[metrics]][[fixture]][[status]]

## Contact

The official pinned MCP server guide was checked for a published contact email and none was present. The structured record stores `contact_email: null` and the exact checked URL. No commit or profile metadata, third-party directory, or inferred address was used.[[mcp-guide]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas entry is recorded only as roster attribution. See the structured record [gmeow-ontology.json](../data/system-reviews/gmeow-ontology.json) and [curated roster](../data/memory-systems.json).
