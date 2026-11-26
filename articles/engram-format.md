# Engram Format source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 225 / Engram Format / `engram-format`  
**Listed repository locator:** [El-AI-Intelligence/engram-format](https://github.com/El-AI-Intelligence/engram-format)  
**Canonical upstream:** [El-AI-Intelligence/engram-format](https://github.com/El-AI-Intelligence/engram-format)  
**Default branch / reviewed head:** main / [f1e92dadff542c12d37613279619adbadd412303](https://github.com/El-AI-Intelligence/engram-format/commit/f1e92dadff542c12d37613279619adbadd412303)  
**Review time:** 2026-11-25 19:27:09 UTC (2026-11-25 11:27:09 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Engram Format at ordinal 225, slug `engram-format`, with the explicit locator `https://github.com/El-AI-Intelligence/engram-format`. Its pinned Atlas attribution is recorded only as roster context. Atlas descriptions and capability claims were not used as assessment evidence. The official Git remote advertised `main` as HEAD at full SHA `f1e92dadff542c12d37613279619adbadd412303`; a shallow checkout resolved to the same branch and SHA. GitHub REST API metadata requests returned HTTP 403, so they were not used to corroborate the pin.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Engram Format is an open Rust crate and specification for an encrypted SQLite vault and encrypted sync wire format associated with the separate Engram product. The inspected crate includes storage, FTS5 and vector retrieval, optional local embeddings, and a write-through QEM associative cache. This review describes public source and documentation only; product runtime quality and performance were not measured.[[readme]][[lib]][[format]]

## Who and what

The README attributes copyright to EL AI Intelligence, LLC. It describes this repository as the open format and reference crate while identifying the daemon, relay, browser vault, and MCP servers as closed source. No individual maintainer identity is inferred from repository metadata.[[readme]]

The crate provides a native storage feature and a WASM feature for parsing format entries and sync blobs. It is a library and reference implementation, not the complete Engram service.[[readme]][[lib]][[wasm]]

## Architecture and data model

The crate documents three layers: `QemCache` as an L1 associative cache, `EngramStore` as an encrypted SQLite/FTS5/vector store, and `ContextAssembler` as a token-budgeted retrieval layer. Product interfaces and service orchestration sit outside this public repository.[[lib]][[readme]]

The vault stores engrams with content, capture context, layer/source, strength, valence, retrieval count, imagined/grounded flags, project, tags, scope, timestamps, privacy level, and optional agent identity. Related tables store embeddings, links, evidence pairs, annotations, application counters, deletion tombstones, access events, and FTS5 text.[[schema]][[format]][[engram]]

The README and FORMAT describe SQLCipher encryption at rest and local key derivation. The specification says machine-ID keys protect against offline disk cloning but not a local user, while passphrase vaults use Argon2id. Those are design statements; this review did not perform a cryptographic audit.[[readme]][[format]][[store]]

There is version drift in the checked material: the README dependency example says 0.1.4 while Cargo.toml identifies 0.1.6, and FORMAT's introduction says schema version 9 while its schema section and implementation identify version 10.[[readme]][[format]][[schema]]

## Write, update, delete, and retrieval

**Write and update.** `EngramStore::write` applies episodic capture gates: a noise filter, normalized-content hash deduplication, and optional near-duplicate checks when an embedding is supplied. Duplicate captures strengthen an existing row. A successful write upserts the row, updates FTS text, optionally stores embeddings, and handles explicit or inferred links. `write_curated` bypasses capture gates for reviewed changes. The public generic backend contract does not expose a general patch operation.[[store]][[noise]][[trait]]

**Retrieval.** The store supports direct get by ID, FTS5 text search with a LIKE fallback, vector search, related-link search, and a context-surface scoring path. A get updates retrieval counters and timestamps. The format describes deterministic ranking for the file format, but this review did not measure retrieval correctness or abstention behavior.[[store]][[adapter]][[format]]

**Delete.** The store removes rows and records tombstones in the same local transaction; a separate lower-level method deletes without a tombstone. The format describes sync tombstones as protection against resurrecting a deleted row, but no relay acknowledgment or cross-device deletion was exercised.[[store]][[schema]][[format]]

**Scope isolation.** Project, scope, privacy, and agent identity are represented in the data model. The generic `Query` type offers project and scope fields, but `EngramStoreAdapter::search` dispatches only on layer, text, tags, or list; it does not apply project or scope. It also calls store helpers with their default quarantine filter, `All`. Therefore those fields do not enforce isolation through this adapter search path.[[schema]][[trait]][[adapter]][[store]]

## Provenance and evidence

The schema supports memory-to-memory evidence relationships, annotations, and access events containing a memory ID, operation, client, content hash, and timestamp without content. However, conversion from stored `Engram` to shared `MemoryEntry` sets evidence to an empty list, and the inspected adapter does not hydrate the evidence table. These structures record relationships and access metadata; they do not demonstrate the truth of a claim or attach source citations to retrieved claims.[[schema]][[entry]][[adapter]]

## Efficiency and observability

The format specifies FTS5 text indexing and a separate 384-dimensional embedding table. Optional local embeddings use Candle and can fall back to FTS-only operation when unavailable. QEM uses 32-bit XOR codes as a cache with write-through to persistent storage; the implementation explicitly accepts possible code collisions. These are design and code observations, not latency or efficiency results.[[format]][[embed]][[qem]]

The source contains QEM hit/miss counters, capture skip counters, and access events. The inspected crate does not establish whether the closed product exposes dashboards, alerting, or a retention policy for these signals.[[qem]][[store]][[schema]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Engram Format. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the evaluation framework and shared status, not Engram Format results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | FTS, vector, and context-surface paths exist; no answers or abstentions were scored. | Unmeasured |
| Correction and stale values | Upsert and curated-write paths exist; no correction sequence was measured. | Unmeasured |
| Deletion leakage | Local tombstone code exists; no post-delete probe or replica audit was run. | Unmeasured |
| Scope isolation | Project/scope fields exist, but the generic adapter omits those filters; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Evidence relationships are stored, but generic entry conversion drops them; no claim-evidence adjudication was done. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings were collected. | Unmeasured |
| Tokens, cost, and storage | No workload, token, cost, or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This review covers the public crate and specification, not the closed daemon, relay, MCP servers, or browser vault. It cannot establish product-level wiring, runtime enforcement, or service behavior. The adapter observations apply to the inspected generic search path; callers may use other APIs, and no broader security conclusion was tested.[[readme]][[lib]][[adapter]]

The presence of encryption parameters, evidence tables, or tombstones does not establish resistance to attacks, factual validity, citation quality, or correctness across crashes and multiple devices. Those behaviors were not experimentally verified.[[format]][[schema]][[sync]]

GitHub REST API metadata requests returned HTTP 403 during review. The official remote's advertised HEAD and the shallow checkout agreed on `main` and the full reviewed SHA; this API limitation is recorded rather than treated as extra confirmation.[[repo]][[head]]

## Benchmark status

**Benchmark not run.** No Engram Format runtime, tests, or benchmarks were executed. No recall, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json); these are project protocol/status files, not Engram Format measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email and none was present. The structured record stores `contact_email: null` and the exact checked URL. No address was inferred from commit/profile metadata or taken from a third-party directory.[[readme]]

## Sources

Repository file citations are pinned to the verified full SHA. The Atlas attribution is included only for curated roster identity and locator context. See the structured record [engram-format.json](../data/system-reviews/engram-format.json) and the [curated roster](../data/memory-systems.json).
