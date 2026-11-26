# Helix AGI source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 287 / Helix AGI / `helix-agi`  
**Listed repository locator:** [munch2u-a11y/Helix-AGI](https://github.com/munch2u-a11y/Helix-AGI)  
**Canonical upstream:** [munch2u-a11y/Helix-AGI](https://github.com/munch2u-a11y/Helix-AGI)  
**Default branch / reviewed head:** main / [5aca6b4439efe5432cac9a2b4771902d6d49c700](https://github.com/munch2u-a11y/Helix-AGI/commit/5aca6b4439efe5432cac9a2b4771902d6d49c700)  
**Review time:** 2026-11-25 22:38:23 UTC (2026-11-25 14:38:23 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists Helix AGI at ordinal 287, slug `helix-agi`, with the explicit locator `https://github.com/munch2u-a11y/Helix-AGI`. Its pinned Agent Memory Atlas entry is retained only as roster attribution and locator context; Atlas was not used as assessment evidence. The official repository page identifies `main` as its default branch, and the official `main.atom` feed reports full head `5aca6b4439efe5432cac9a2b4771902d6d49c700`, updated 2026-10-21T04:40:10Z. This review is pinned to that current head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Helix AGI is a locally operated agent runtime that combines a persistent per-agent filesystem home with a continuous sensing, thinking, action and communication loop. The reviewed memory code uses an append-only JSONL journal for canonical event-like records, categorized JSON files for beliefs, and a separate semantic vector index for explicit recall. These are distinct storage and retrieval surfaces; this source review does not measure answer quality or reliability.[[readme]][[manual]][[journal]][[beliefs]][[index]]

## Who and what

The official README presents Helix AGI as a local Dual RWKV agent with persistent identity and memory, filesystem sensing, private thought and direct speech, and a digital body for file and workshop operations. The project is an agent application/runtime with locally configured models and supporting memory components, rather than a hosted standalone memory API.[[readme]][[manual]]

## Architecture and data model

The journal, belief store and semantic index have separate responsibilities. CognitiveJournal stores records in a JSONL file under the configured data directory; BeliefStore keeps seven categorized JSON lists for premises, propositions, preferences, people, skills, desires and concepts; MemoryManager wraps the journal and connects memory calls to a physics-backed semantic recall path.[[journal]][[beliefs]][[manager]]

Journal entries carry an ID, type, exact text content, 8D position, pulse ID, Lagrangian snapshot, metadata and timestamp, with an optional 384D embedding. Each serialized line includes a SHA-256 checksum. Beliefs hold fields such as confidence, mass, stability, relations, source-memory references, 8D position, source, and access counts. These model fields can guide internal weighting; they do not independently verify that a belief is true.[[journal]][[beliefs]]

Explicit semantic retrieval uses a separate 1024D vector index. The system manual describes additional exact-term and multi-head retrieval, context lanes and source-linked evidence briefs, while 8D fields contribute separate spatial context. The available docs describe multiple context contributions, not one unified evidence score.[[index]][[manual]]

RecordEnvelope creates a deterministic typed view of records, distinguishing private thought, inbound/outbound communication, tool calls/results and observations, with actor, visibility, evidence scopes, action status, and optional cause/tool metadata. Legacy entries can be classified from persisted fields. These labels preserve record context but are not human adjudications of whether a claim is factually correct.[[envelope]][[manual]]

## Write, update, delete, and retrieval

**Write.** MemoryManager serializes store operations with a re-entrant lock and writes through CognitiveJournal. The journal appends a line, flushes it, and calls `fsync`; loads verify checksums and skip malformed or invalid lines. The journal documentation says updates append a later version under the same ID and describes a nightly compaction step. The inspected journal module exposes append/load helpers but no compaction method, so that scheduled maintenance behavior is not confirmed by this review.[[manager]][[journal]]

**Belief maintenance.** BeliefStore normalizes category records and includes confidence/mass recomputation and attrition pruning. A pruned belief is removed from the surviving category list and, if a physics engine is attached, its belief point is removed there. The inspected sources do not establish a transaction covering belief files, historical journal records, and all derived indexes.[[beliefs]][[journal]]

**Delete and correction.** No general journal-memory correction or delete operation was present in the inspected CognitiveJournal interface. A later journal version can express a changed record under the same ID according to its documentation, but physical history remains append-only absent a verified compaction/erasure path. Belief pruning is not evidence of complete deletion from journals, backups or derived stores. Deletion durability and leak rates are unknown.[[journal]][[beliefs]][[manager]]

**Retrieval.** MemoryManager exposes explicit and contextual memory search. SemanticIndex stores normalized embeddings and uses cosine similarity via inner product; it supports ID upserts and optional metadata filtering, with NumPy exact search or FAISS FlatIP as the documented/default large-index path and optional IVF mode. The manual describes additional exact-term, multi-head and context-lane contributions. No retrieval accuracy or abstention result was measured.[[manager]][[index]][[manual]]

## Scope isolation

The system manual says the selected `data_dir` supplies persistent agent state and describes the named filesystem home as a separate configured root. The README lays out per-agent paths for memory, beliefs, spatial state and mindscape state. This provides a configuration model for agent-specific storage, but this review did not establish authorization enforcement against cross-agent access or test isolation between agents.[[manual]][[readme]]

## Provenance and evidence

Journal metadata and RecordEnvelope distinguish record kinds and evidence contexts, including whether content is private thought, received communication, tool-reported evidence or an action result. The system manual describes receipts for context/model admission, actions, observations and checkpoints, and source-linked evidence briefs. These structures can support traceability; they do not establish that recalled claims are correct or that every generated answer is supported. No evidence-support adjudication was performed.[[journal]][[envelope]][[manual]]

## Efficiency and observability

The source describes append-and-fsync persistence, checksummed JSONL records, normalized vectors, exact NumPy search and optional FAISS indexes. SemanticIndex exposes diagnostics including vector count, dimensionality, selected search strategy, model ID, dirty state and memory bytes. The system manual documents receipt and foreground-health files as operational surfaces. These are code/documentation observations, not measured latency, throughput, cost or resource use.[[journal]][[index]][[manual]]

## Metric-domain evidence

All project metric domains remain unmeasured for this reviewed revision.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Semantic and contextual retrieval mechanisms are present; answer correctness and abstention were not evaluated. | Unmeasured |
| Correction and staleness | Same-ID journal revisions are described and belief maintenance is implemented; correction accuracy and stale-value rate were not measured. | Unmeasured |
| Deletion leakage | No general journal delete method was found in the inspected interface; no deletion probe or leakage denominator was run. | Unmeasured |
| Scope isolation | Per-agent data directories and homes are configurable; cross-agent isolation was not tested. | Unmeasured |
| Evidence support and citations | Typed evidence scopes and receipt/source surfaces are documented; no answer evidence was adjudicated. | Unmeasured |
| Latency and write-to-recall delay | Persistence and search code were inspected; no timing observations were collected. | Unmeasured |
| Tokens, cost and storage | JSONL, category files and vector-index storage are visible; no token, cost or storage-efficiency comparison was made. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the pinned README, system manual, memory manager, journal, belief store, record envelope and semantic index. It does not cover every context lane, query implementation, runtime integration, migration, backup/restore route or external dependency.[[readme]][[manual]][[manager]][[journal]][[beliefs]][[envelope]][[index]]

The journal's docstring describes nightly compaction, but the inspected module does not implement that method. The behavior may be implemented elsewhere or the documentation may be stale; whether historical records are eventually compacted is unknown. Runtime correctness, agent scope enforcement, backup erasure, answer accuracy and operational costs also remain unknown.[[journal]][[manual]]

## Benchmark status

**Benchmark not run.** No Helix AGI runtime, tests or benchmark workload was run. The project's [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe evaluation protocol and shared execution status, not Helix results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and system manual were checked for contact email. Neither published one, so the structured record stores `contact_email: null` and the exact checked URLs. No commit/profile metadata, third-party directory or inferred address was used.[[readme]][[manual]]

## Sources

Upstream file citations are pinned to full reviewed SHA `5aca6b4439efe5432cac9a2b4771902d6d49c700`. The Atlas entry is roster attribution only, not assessment evidence. See the structured record [helix-agi.json](../data/system-reviews/helix-agi.json) and [curated roster](../data/memory-systems.json).
