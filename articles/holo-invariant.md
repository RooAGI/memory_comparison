# HOLO-Invariant

**Ordinal:** 304  
**Slug:** `holo-invariant`  
**Listed repository:** https://github.com/Deathburgerz013/HOLO-Invariant  
**Reviewed upstream:** https://github.com/Deathburgerz013/HOLO-Invariant/tree/main at `88e54be7b7764f2ee6d318f97e3bfd946ccad4a2`  
**Review time:** 2026-11-25 23:23:23 UTC (15:23:23 PST, America/Los_Angeles)  
**Status:** Reviewed from code. Benchmark not run.

## Summary

HOLO-Invariant is a Python framework for preserving and checking state across handoffs. Its basic memory path is a local append-only JSONL chain with SHA-256 links, replay, search, and separate correction and verification artifacts. The wider repository adds optional slot storage, continuity protocols, and bounded authorization gates. This review describes inspected code and documentation, not measured memory quality or runtime performance.[[readme]][[core]][[replay]]

## Who and what

The official repository describes HOLO-Invariant as a framework, not a model or hosted memory service. The README presents a small HoloChain API and CLI alongside a much broader set of continuity, verification, and integration modules. Deployments choose a local chain path; an optional SQLite slot store is available through the service facade.[[readme]][[core]][[service]]

## Architecture and data model

`HoloChain` stores entries as JSON lines. Each entry carries a monotonically increasing index, timestamp, content, and hash; the hash is SHA-256 over the prior hash plus canonical JSON for the entry fields. Loading, state reconstruction, and replay verify the full sequence from a configured genesis hash. Append serializes the read, verification, and write transaction under a file lock and flushes the new record.[[core]]

`ReplayEngine` is a read-only view over that chain: it returns verified entries, reconstructed state, ranges, latest records, a compact timeline, and text search. The optional `HoloService` composes the chain with replay, operator/status, provenance and IDX helpers; it can also mirror a service append to a separate SQLite slot database. These are separate persistence paths, so the chain and slot store should not be assumed to be one atomic or identical memory view.[[replay]][[service]]

The repository README describes a larger three-layer design: executable invariant checks, continuity artifacts that carry relationships, and research experiments. It explicitly limits the claims of hashes and receipts: they establish identity and lineage under declared encodings, not truth, authorship, relevance, or permission. The repository contains many specialized modules, so this review focuses on the chain/replay path and the service append boundary rather than claiming to audit every subsystem.[[readme]][[implementation_map]]

## Write, update, delete, and retrieval

The low-level `HoloChain.append` path appends new content, optionally compressing it, and rejects a verified-snapshot mismatch before committing. `HoloService.append` adds an operational authorization check bound to the canonical content hash and expected service-append action; its documented failure response reports a blocked append without mutation. The README's examples route writes through this service/CLI boundary. Direct callers of the low-level chain remain a distinct boundary and are not automatically subject to the service gate.[[core]][[service]][[readme]]

Corrections are represented by separate version-bound receipts. `record_correction` requires hashes for previous, proposed, and resulting states, a non-empty reason, and at least one unique evidence-receipt hash. It preserves those links and marks the receipt as not accepted, not claiming truth, and granting no write authority. This function creates a receipt object; inspection of this path does not establish that every correction is automatically persisted into the HoloChain or applied to a memory value.[[correction]]

The chain is append-only; the inspected core exposes no delete operation. Its maintenance helpers produce review/prune suggestions and explicitly do not delete records. Search is case-insensitive substring matching over verified entries in chain order, with bounded decoding for compressed records; it is not a semantic or relevance-ranked retrieval algorithm. The README describes EnvPath evidence search and draft export, but frames draft preparation as a proposal that does not itself persist a change or grant authority.[[core]][[replay]][[readme]]

## Scope isolation

The core chain is selected by a filesystem path. The inspected chain entry format and replay methods do not add a tenant, user, project, or session key, and the core search API has no scope filter. Separate paths can provide deployment-level separation, but the inspected core does not enforce who may read a path. The service authorization described for append is not evidence of read isolation or identity authentication across callers.[[core]][[replay]][[service]]

## Provenance and evidence

The hash chain makes edits to retained interior entries detectable when checked against the rest of the chain. It does not anchor the latest head externally: a truncated tail can still form a valid prefix when verified from genesis. The README itself notes that an independently retained checkpoint is needed to compare the current file with an external reference and that internal consistency is not independent authorship.[[core]][[readme]]

Correction receipts bind the prior, proposed, and resulting receipt hashes to a reason and evidence-receipt hashes. The project documentation and source also repeatedly distinguish verification from truth and authorization. A hash or receipt therefore supports integrity and lineage claims within its declared contract; it does not show that evidence is sufficient or that a recorded claim is true.[[correction]][[readme]]

## Efficiency and observability

The source includes append locking, optional zlib compression, chain density/health summaries, age-based review suggestions, replay verification, and text search. Replay re-reads verified chain entries, and search walks them in order; the inspected path provides no indexed or vector retrieval. These are implementation observations, not latency or scaling measurements. The wider project has project-level metric definitions and fixtures, but no HOLO-Invariant workload was run for this review.[[core]][[replay]][[metrics]][[fixture]]

## Metric-domain evidence

All metric domains are unmeasured here. The repository's benchmark fixture and metric definitions provide protocols, not results for this review. In particular, no retrieval questions, abstention probes, correction or deletion probes, cross-scope cases, citation adjudication, latency sampling, token/cost collection, or storage-efficiency measurement were performed.[[metrics]][[fixture]][[status]]

## Limits and unknowns

- The hash chain can detect changed retained entries, but without an externally retained head checkpoint it does not establish that the present file contains the complete history.[[core]][[readme]]
- The core path is append-only and offers prune suggestions, not deletion. This review does not establish erasure from slot databases, backups, exports, or other copies.[[core]][[service]]
- The inspected core has path-based storage and no built-in caller or tenant scope filter; cross-user isolation is not established.[[core]][[replay]]
- Correction receipt construction is separate from chain persistence and application. This review does not establish a universal workflow that verifies evidence, applies a correction, and updates every memory backend.[[correction]][[service]]
- Exact-substring search and integrity verification do not establish retrieval completeness, semantic relevance, answer correctness, or evidence support.[[replay]][[readme]]
- The repository is broad and actively evolving; this review inspects selected current modules and is not an exhaustive audit of every adapter, experiment, or authorization path.[[implementation_map]]

## Benchmark status

**Benchmark not run.** HOLO-Invariant, its tests, and benchmark workloads were not run. Project metrics and fixture files define evaluation procedures; the shared status record is not a result for this system.[[metrics]][[fixture]][[status]]

## Contact

The official repository README was checked for a published contact email. It identifies the project author but publishes no email address; no address was inferred from commit or profile metadata. The exact checked README URL is recorded in the structured review.[[readme]]

## Sources

The catalog entry and its pinned Atlas report are retained only for curated identity and locator attribution, not for assessment claims.[[catalog]][[atlas]] The official repository page and GitHub commit API establish the canonical repository, default branch, and current reviewed head.[[repo]][[head]] Upstream file links in the structured review are pinned to the full SHA. See the structured record [holo-invariant.json](../data/system-reviews/holo-invariant.json) and [curated roster](../data/memory-systems.json).
