# Hillock

**Ordinal:** 295  
**Slug:** `hillock`  
**Listed repository:** https://github.com/roandejager/Hillock  
**Reviewed upstream:** https://github.com/roandejager/Hillock/tree/master at `b5e2569ab3aafe1a076c6787c82f6d7d65b82431`  
**Review time:** 2026-11-25 22:58:46 UTC (14:58:46 PST, America/Los_Angeles)  
**Status:** Reviewed from code. Benchmark not run.

## Summary

Hillock is a local neuro-symbolic memory engine built around a SQLite knowledge graph, Hebbian co-activation weights, and hyperdimensional vector gating. Document ingestion extracts structured facts; retrieval checks whether a matching fact clears similarity and predicate thresholds before passing it to a local language model. This review describes the pinned public source and documentation, not measured runtime quality.[[readme]][[database]][[engine]][[reservoir]]

## Who and what

The official README presents Hillock as a local Python library, CLI, and OpenAI-compatible FastAPI service for agent and desktop integrations. It describes CPU-only/headless use as well as an optional local Ollama renderer. No maintainer identity is needed for this assessment.[[readme]][[api]]

## Architecture and data model

The symbolic store in `database.py` is a SQLite database in WAL mode. It defines `entities` (ID, name, type), `relations` (subject ID, predicate, object ID, source-document label, confidence, creation time), `hebbian_weights` (entity-pair association strength), `entity_aliases`, and `hdc_reservoirs` for compact document path vectors. Relations use a triple primary key and foreign keys; entity deletion cascades to relations, weights, and aliases that reference the entity.[[database]]

`IntegratedHillock` composes the SQLite graph, a plasticity engine, and a hyperdimensional reservoir. The reservoir maps entity and predicate strings into packed bipolar hypervectors, supports subword and GloVe-derived encodings, and computes similarity with Hamming distance/bit counts. The README describes a 10,000-bit representation packed into 157 64-bit words; source configuration is the authority for a particular run.[[engine]][[reservoir]][[readme]]

The ingestion path routes local text or PDF content through TALON extraction, persists extracted subject-predicate-object triples, and can bind nearby relation paths into a per-document reservoir vector. The ingestor resolves requested paths and rejects files outside the project directory. It labels facts with a source document, but the inspected relation schema does not retain source text offsets or quoted evidence spans.[[ingestor]][[database]]

## Write, update, delete, and retrieval

The CLI supports document ingestion and manual relation updates. `update_relation` delegates to a transactional batch writer that ensures entities exist and inserts or replaces triples; configured single-valued predicates first remove earlier values for the same subject and predicate. Writes record a source label, confidence, and timestamp, but replacing a triple does not preserve a revision history in the relation row. Entity aliases and merge operations consolidate duplicate names and migrate their relations and associations.[[database]][[engine]][[readme]]

Hillock has targeted mutation paths: an ambiguous pronoun fact can be deleted and replaced with a human-disambiguated fact; relation updates overwrite or replace matching rows; merging an entity moves its relations and Hebbian weights, records an alias, and deletes the old entity. A database reset drops the tables and reseeds initial knowledge. These are code-level mutation mechanisms, not a documented end-to-end erasure guarantee for backups or copies.[[engine]][[database]]

Recall first links query text to entity IDs, fetches relations touching those entities, and filters candidate facts using a hypervector similarity gate plus predicate alignment. When facts pass, the renderer receives the verified triples and their source-document labels. Hebbian weights can prime related concepts and decay during turns. Strict mode returns a fixed refusal when no fact passes; balanced or conversational modes may call Ollama to phrase a refusal. The API's chat endpoint uses one engine/database instance and reports zero token usage in its response object, so that field is not a token measurement.[[engine]][[database]][[plasticity]][[api]]

## Scope isolation

The inspected schema has no user, tenant, project, session, or namespace column. The engine and API initialize one database path and one in-process context for their instance; the README instructs local use and binds its API server to loopback by default. This is a local deployment boundary, not per-caller data isolation. A deployment that shares a database or exposes the API beyond loopback would need its own access controls; no authorization layer was found in the inspected API source.[[database]][[engine]][[api]][[readme]]

## Provenance and evidence

Relations retain a `source_doc` label, confidence, and creation timestamp. Document ingestion uses the input file's basename as its document identity; human disambiguation uses a special source label. The answer prompt can mention the source document. These fields let the application label a fact's origin, but the inspected schema does not retain evidence spans, a trust state, mutation audit history, or temporal supersession records. Labels and prompt instructions do not prove that a fact or answer is correct.[[database]][[ingestor]][[engine]][[readme]]

## Efficiency and observability

The implementation uses SQLite WAL, compact packed hypervectors, bitwise similarity, and optional local model rendering. The ingestor computes extraction timings, sentence rate, and optional CPU/RAM snapshots; engine and API paths provide debug/logging and HTTP health/model endpoints. These are instrumentation mechanisms. No latency, write-to-recall delay, token use, cost, or storage measurements were collected for this review.[[database]][[reservoir]][[ingestor]][[engine]][[api]]

The README reports that a bundled verification script covers 21 checks, an end-to-end script uses 22 answerable questions and 10 negative controls, and a synthetic labyrinth harness measures multi-hop behavior. These are descriptions of upstream evaluation assets, not results independently verified or run here.[[readme]]

## Metric-domain evidence

The project's metric definitions and fixture specify comparison protocols; the shared status record is not a Hillock result. Every benchmark domain remains unmeasured in this review.[[metrics]][[fixture]][[status]]

## Limits and unknowns

- The database provides source labels, confidence, and timestamps, but no source-span citation or trust-state model was found in the inspected schema.[[database]]
- Relation correction and entity merging exist, but the inspected representation does not keep a relation revision chain. Full deletion from backups, external copies, or downstream consumers was not established.[[database]][[engine]]
- The schema has no scope key, and the inspected API contains no caller authentication. Cross-user isolation is therefore not established by the reviewed code.[[database]][[api]]
- The README's claims about extraction throughput, memory footprint, sub-millisecond similarity, and refusal behavior are upstream descriptions. They were not reproduced as part of this source review.[[readme]]
- Optional model behavior, extraction quality, retrieval accuracy, abstention quality, and evidence support depend on configuration and data; no runtime workload was executed.[[engine]][[ingestor]][[metrics]]

## Benchmark status

**Benchmark not run.** Hillock, its tests, and benchmark workloads were not run. Project metrics, fixtures, and shared status provide evaluation protocol only; they are not Hillock measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README lists `contact.roandejager@gmail.com` for enterprise licensing inquiries. The structured record stores this address with the exact official README URL. No commit/profile metadata, third-party directory, or inferred address was used.[[readme]]

## Sources

The catalog confirms the roster identity and listed repository; its Atlas URL is retained only as attribution, not assessment evidence.[[catalog]][[atlas]] Official GitHub repository metadata and the current branch commit provide the review pin.[[repo]][[head]] Upstream source links below are pinned to the full reviewed SHA. See the structured record [hillock.json](../data/system-reviews/hillock.json) and [curated roster](../data/memory-systems.json).
