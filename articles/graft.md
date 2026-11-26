# Graft source and design review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 269 / Graft / `graft`  
**Listed repository locator:** [AEndrix03/Graft](https://github.com/AEndrix03/Graft)  
**Canonical upstream:** [AEndrix03/Graft](https://github.com/AEndrix03/Graft)  
**Default branch / reviewed head:** master / [f9913b045ef927f5b9afad37f3e6544111f05736](https://github.com/AEndrix03/Graft/commit/f9913b045ef927f5b9afad37f3e6544111f05736)  
**Review time:** 2026-11-25 21:25:50 UTC (2026-11-25 13:25:50 PST; America/Los_Angeles).

## Identity and review pin

The catalog records Graft at ordinal 269, slug `graft`, and an explicit GitHub locator. Its Atlas entry is retained only as roster attribution for identity and locator context; Atlas claims are not used as assessment evidence. The official GitHub repository page identifies `master` as the default branch. The official `master.atom` feed reports full head `f9913b045ef927f5b9afad37f3e6544111f05736`, updated 2026-11-14T00:51:59Z. The observations below use files pinned to that commit.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Graft is a local-first coding-agent memory system built around a CLI and a long-lived daemon. It stores titled memory nodes, vectors, full-text indexes, graph edges, and source provenance in a per-profile SQLite database. Retrieval offers a gated single-answer query, hybrid ranked recall, and graph exploration. No Graft workload was run for this review.[[readme]][[architecture]][[storage]][[retrieval]]

## Who and what

The official repository presents Graft as a persistent memory layer for coding agents, with Claude Code and Codex plugins, OpenCode skills, MCP integrations, and a CLI for other callers. It ships a thin CLI and resident daemon rather than a language-specific SDK; the daemon owns the database and embedding model. This review does not infer an individual maintainer identity.[[readme]][[architecture]]

## Architecture and data model

The CLI encodes operations as MessagePack, sends them over a profile-specific Unix socket, and prints JSON. The daemon loads BGE-M3, verifier state and configuration, owns SQLite, and dispatches requests. The optional HTTP API and browser viewer reuse the same dispatcher. The architecture docs describe per-connection worker threads sharing storage calls serialized by a mutex.[[architecture]]

A node records a title, body, author, timestamps, expiry, access counters and lifecycle state. SQLite holds node rows, title embeddings in sqlite-vec, FTS5 title/body indexes, keywords and graph edges; WAL mode is enabled. Edges represent semantic and keyword relationships, supersession, and contradictions.[[storage]][[schema-code]]

An insert embeds the title, upserts keywords, constructs similarity edges, and commits the node and related rows in one transaction. A BLAKE3 hash over title, body and sorted keywords makes identical content idempotent; author and timestamps are excluded. Similarity-based duplicates are not automatically collapsed.[[insert]][[insert-code]]

Profiles are physical partitions: each has its own SQLite file, daemon and socket. The CLI selects profile paths before connecting. Sharing across profiles requires explicit export/import/merge or manual SQLite-file sync; the docs do not describe profiles as request-level tenant IDs within one database.[[profiles]][[architecture]]

## Write, update, delete, and retrieval

**Write.** `graft insert` accepts a title, body, keywords, optional author/expiry and repeatable source locators. File sources are resolved against the caller's project root and fingerprinted; a missing source file fails the insert. Duplicate content returns the existing node and may attach refreshed source links. Embedding and edge construction use the title; the insert implementation does not call an LLM to write or normalize the node.[[insert]][[insert-code]]

**Update and correction.** An insert can supersede an existing node by marking it superseded and adding a SUPERSEDES edge in the same transaction as the successor. The old node remains retrievable by ID but is excluded from normal search and traversal. Maintenance exposes stale, retire, restore, supersede, merge, refresh and keep/contradiction decisions; the agent resolves semantic candidates after a scan.[[insert]][[storage]][[maintenance]]

**Delete.** `graft delete` is documented as a hard delete with cascading removal of dependent rows. `retire` is a reversible soft-delete state excluded from search until restore or physical purge after the configured retention window. Apply-safe purges expired retired nodes. The storage documentation lists soft deletion for direct delete as missing; backups and exported copies are outside the database lifecycle.[[architecture]][[storage]][[maintenance]]

**Retrieval.** `query` embeds the question and applies lexical/vector gates to a bounded candidate set. It returns at most one STRONG node with body, a WEAK title without body, or MISS with fallback candidates. A STALE note can still be searchable and even STRONG, so its source should be checked. `retrieve` fuses title-vector, title-BM25 and body-BM25 lists with reciprocal-rank fusion. `explore` uses bounded beam search through keyword and semantic edges, so it can miss a globally relevant node that is not reachable from its seeds.[[retrieval]][[retrieve-code]][[storage]]

## Scope isolation

The documented isolation boundary is a profile, with one database, daemon and socket per profile. Callers select a profile before connecting; independent profiles do not share storage unless explicitly merged or synced. This describes architecture, not an adversarial isolation measurement. The profile guide also documents remote synchronization by copying/merging rows in a shared SQLite file, not an HTTP remote service.[[profiles]]

## Provenance and evidence

A node may link to file, URL, conversation or manual sources. File links include a BLAKE3 fingerprint for freshness checks; maintenance can report source-changed or source-removed candidates, after which an agent reopens the current file and decides whether to refresh, supersede, stale or retire the note. The source tables retain locators and fingerprints, not source contents. This supports lineage and change detection, but does not prove that a memory or generated answer is correct.[[insert]][[storage]][[maintenance]]

## Efficiency and observability

The daemon keeps the embedding model warm across CLI calls. SQLite WAL, sqlite-vec and FTS5 support local storage and retrieval; the architecture guide notes the model's substantial memory footprint and thread-per-connection request handling. The CLI appends operation, status, latency and hit outcome to a local JSONL usage log; stats report similarity percentiles, and analytics aggregates latency and hit rates. The docs identify gaps including unbounded usage-log growth, free-form daemon logs and limited health details. No runtime latency, storage, resource, token or cost measurements were collected.[[architecture]][[storage]][[maintenance]]

## Metric-domain evidence

All domains below are **unmeasured in this review**. Code and documentation show mechanisms, not measured quality. No Graft runtime, tests or benchmark workload was run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json) and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Query has STRONG, WEAK and MISS outcomes; no answer set was scored. | Unmeasured |
| Correction and stale values | Supersession and stale-state maintenance exist; no correction workload was run. | Unmeasured |
| Deletion leakage | Direct hard delete and delayed retirement purge were inspected; no deletion probes were run. | Unmeasured |
| Scope isolation | Separate per-profile storage is documented; no cross-profile adversarial workload was run. | Unmeasured |
| Evidence support and citation coverage | Source locators and fingerprints are recorded; no answer evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Docs describe warm-path behavior; no timings were collected. | Unmeasured |
| Tokens and cost | Integrations and local embedding architecture were inspected; no usage cost was measured. | Unmeasured |
| Storage efficiency | SQLite/index schema was inspected; no corpus-size measurement was collected. | Unmeasured |

## Limits and unknowns

This review is tied to the verified source pin and is not an operational security or quality audit. Graft's README labels the project Alpha and says its CLI JSON may change before 1.0. A retrieval confidence gate is not proof that a note is accurate or current; stale notes remain searchable, and retrieval documentation says normal results do not surface unresolved contradiction partners alongside a hit.[[readme]][[retrieval]][[maintenance]]

The profile boundary is described by the project, but this review did not inspect an adversarial threat model for profile handling or the optional HTTP/OAuth gateway. File provenance stores locators and fingerprints rather than source snapshots. The review did not measure retrieval quality, evidence support, deletion leakage, scope isolation, latency, resource use, tokens, cost or storage efficiency.[[profiles]][[storage]][[insert]][[metrics]]

## Benchmark status

**Benchmark not run.** No Graft runtime, tests or benchmark workload was executed for this review. The README contains upstream-reported benchmark claims; they were not reproduced and are not recorded as this project's results. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json) and [execution status record](../results/initial-baselines-status.json).[[readme]][[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked and publishes no contact email. The expected official `SECURITY.md` path returned GitHub's File not found page. `contact_email` is therefore null; no commit/profile metadata or third-party directory was used.[[contact-readme]][[contact-security]]

## Sources

Upstream file links in the structured record are pinned to the reviewed full SHA. The Atlas entry is listed only as roster attribution, not assessment evidence. See the [structured review record](../data/system-reviews/graft.json), [curated roster](../data/memory-systems.json), [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).
