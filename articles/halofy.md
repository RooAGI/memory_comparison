# Halofy source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 280 / Halofy / halofy  
**Listed repository locator:** [halofyai/halofy](https://github.com/halofyai/halofy)  
**Canonical upstream:** [halofyai/halofy](https://github.com/halofyai/halofy)  
**Default branch / reviewed head:** main / [3763e64f521df8dc58d00d4632e732e702dd76ef](https://github.com/halofyai/halofy/commit/3763e64f521df8dc58d00d4632e732e702dd76ef)  
**Review time:** 2026-11-25 22:24:45 UTC (2026-11-25 14:24:45 PST; America/Los_Angeles).

## Identity and review pin

The curated roster lists Halofy at ordinal 280, slug halofy, with the explicit repository locator https://github.com/halofyai/halofy. The Atlas URL and pinned revision are retained as roster attribution only; Atlas descriptions and assessments were not used as review evidence. The official GitHub repository API identifies halofyai/halofy and default branch main; its commits/main endpoint returned full head SHA 3763e64f521df8dc58d00d4632e732e702dd76ef. The review is pinned to that head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Halofy is a self-hostable TypeScript kernel that governs organizational memory access, writes, policy, audit, and erasure while delegating retrieval ranking to replaceable drivers. Its operational tier stores vector-backed memory objects in Postgres/pgvector, with embedded PGlite as the local default; a cold knowledge tier stores reviewed concepts. Credentials resolve namespace and role on the server, and retrievers receive a read-only scoped view. This is an inspection of current docs and source, not a runtime or benchmark assessment.[[readme]][[architecture]][[types]]

## Who and what

The repository presents Halofy as the open access and governance layer for organizational agent context. It exposes HTTP and MCP syscalls and a CLI, plus a browser control room; it is a kernel/service rather than a standalone agent or a retrieval model. The repository is published under the halofyai organization. Official SUPPORT.md gives conduct@halofy.ai for conduct matters; the record stores that exact official source URL.[[readme]][[docs-index]][[support]]

## Architecture and data model

The architecture separates identity and policy gates, a write pipeline, an authoritative database, context assembly/fault handling, and a driver boundary. Postgres is the system of record for memory, embeddings, policy, provenance, tombstones, and audit; PGlite uses the same schema for local development. Warm-store mirrors and retrieval sidecars are described as rebuildable caches rather than authority.[[architecture]][[types]]

A warm memory object has a stable ID, namespace, content, type/status, inline embedding, classification, provenance, source access, access/fault telemetry, and time fields. The time model distinguishes event time, assertion time, and validity bounds; supersedence is represented by a link to the replaced object. Cold L3 concepts are Markdown knowledge documents parsed into a concept index; private concept bodies are encrypted with envelope encryption.[[types]][[architecture]]

## Write, update, delete, and retrieval

**Write.** The documented write path extracts candidate facts (or stores verbatim when no model is configured or the model path browns out), verifies candidates, resolves entities, classifies sensitivity and destination policy, then exact-deduplicates and inserts. Connector imports go through this same path. The result reports stored, rejected, superseded, or deduplicated outcomes, and write plus audit are transactional where the database handle is available.[[architecture]][[write]]

**Update and conflict handling.** A correction closes the old fact’s validity interval and inserts a new object linking back through supersedes; the prior content remains in history. Exact normalized duplicates are deduplicated. The architecture guide describes an out-of-band semantic conflict scan and provenance trust ranking, while the current write module header says semantic similarity does not alter validity in the write path and confirmed conflicts are presented for human resolution. I did not trace every conflict-autopilot and dispute producer, so the exact deployed resolution behavior remains uncertain.[[architecture]][[write]][[types]]

**Delete.** The governed mem.forget path is the documented exception to ordinary non-deletion: within the caller’s permitted subtree it hard-deletes matching objects and inline embeddings, inserts tombstones, creates an Ed25519-signed deletion certificate, and keeps the append-only audit record. The implementation also queues warm-store purges in the same transaction when that integration is configured. A deployment without a persistent signing key may use a boot-generated ephemeral key, which weakens certificate verification after restart.[[architecture]][[erasure]]

**Retrieval.** mem.read fetches by ID; mem.search ranks warm-tier candidates through the policy-selected driver; mem.assemble packs a bounded working set; and mem.fault checks warm L2 before consulting cold L3 when the warm result does not clear an absolute score floor. The baseline driver combines vector and BM25 ranking with reciprocal-rank fusion and token-budget trimming. Other shipped drivers include graph and Mem0-style options; a driver receives a ScopedView rather than direct database or index access and can return references but cannot write.[[architecture]][[driver-kit]][[view]]

## Scope isolation

API keys resolve namespace, actor, and role server-side; public syscall requests cannot choose those identity values. The base namespace rule permits a caller to read its own namespace and slash-delimited ancestors, not sibling or descendant namespaces. Query-layer source grants and human access projections can further shape eligible reads. The driver view delegates scope enforcement to the index and cold-store methods and fails closed for source-scoped cold reads when the cold tier lacks provenance. Erasure is separately constrained to the caller’s subtree, with administrative/global exceptions gated by identity and role.[[readme]][[architecture]][[index]][[view]][[erasure]]

## Provenance and evidence

Memory objects carry provenance entries, classification, source access, and temporal relationships; connector source access is enforced during reads. Audit events include successful operations as well as denied, missing, degraded, and error outcomes, and the architecture guide describes transactional audit for state changes. Erasure certificates make the erased ID set and event independently verifiable while audit history remains. These mechanisms show traceability and control flow; they do not establish that a stored assertion is true or that an answer’s cited evidence supports it.[[types]][[architecture]][[write]][[erasure]]

## Efficiency and observability

Retrieval is bounded by candidate and token limits, with vector and lexical lanes, a stable working-set order, and fallback behavior for unavailable models, embedders, drivers, mirrors, or policy data. PGlite supports a no-database local start; durable deployments use Postgres. The project documents operation timing, audit, retrieval driver/degradation labels, fault latency, and stats such as working-set size and fault-hit rate. These are implementation and documentation observations, not measured throughput, latency, token, cost, or storage results.[[architecture]][[driver-kit]][[readme]][[metrics]][[status]]

## Metric-domain evidence

Every assessment domain remains unmeasured for Halofy in this review. The project metric definitions, fixture, and execution status describe the evaluation framework; they are not Halofy results. No system runtime, tests, or benchmarks were run.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
| --- | --- | --- |
| Answerable retrieval and abstention | Search and fault paths exist; no answers were scored. | Unmeasured |
| Correction accuracy and stale values | Validity intervals and supersedence are implemented; no correction sequence was evaluated. | Unmeasured |
| Deletion leakage | Signed erasure and tombstones are implemented; no deletion probes were run. | Unmeasured |
| Scope isolation | Namespace and source-access filters are present; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Provenance and audit fields exist; no answer evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Timing and retrieval instrumentation exist; no runtime timings were collected. | Unmeasured |
| Tokens, cost, and storage | Candidate/token bounds and storage backends are documented; no workload or resource measurements were collected. | Unmeasured |

## Limits and unknowns

This bounded inspection covered the pinned README, documentation index and architecture/driver guides, shared types, write and index modules, driver view, and erasure implementation. It did not inspect every syscall, policy path, connector, conflict worker, migration, or deployment mode. Documentation and current source describe conflict resolution differently, and the end-to-end behavior was not run. Source presence cannot establish retrieval quality, correct access enforcement under adversarial inputs, successful operational backup/restore, or erasure propagation to external stores.[[architecture]][[write]][[index]][[view]][[erasure]]

Performance and cost remain unknown. The README’s stated test and conformance totals are upstream claims, not results from this review. I did not verify all security threat-model claims or exercise the project’s hermetic test lane.[[readme]][[driver-kit]][[metrics]][[status]]

## Benchmark status

**Benchmark not run.** No Halofy runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json); these describe project protocol/status, not Halofy measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned SUPPORT.md publishes conduct@halofy.ai for conduct matters. Contact metadata records the exact checked URL; no commit or profile metadata or third-party directory was used.[[support]]

## Sources

Official upstream file links in the structured record are pinned to the verified full head SHA. The Atlas source is retained solely for roster attribution. See the structured record [halofy.json](../data/system-reviews/halofy.json) and [curated roster](../data/memory-systems.json).