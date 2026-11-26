# Brain source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 98 / Brain / `brain-db`  
**Listed repository locator:** [arc-labs-ai/brain-db](https://github.com/arc-labs-ai/brain-db)  
**Catalog source attribution:** [Atlas report at pinned revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brain-db.md)  
**Canonical repository / default branch:** [arc-labs-ai/brain-db](https://github.com/arc-labs-ai/brain-db) / `main`  
**Reviewed head:** [69d36cb615140dadc8356ef143eeb57fb19dba65](https://github.com/arc-labs-ai/brain-db/commit/69d36cb615140dadc8356ef143eeb57fb19dba65)  
**Review time:** 2026-11-24 23:49:15 UTC (15:49:15 PST; America/Los_Angeles). The official repository page identifies the repository; `git ls-remote --symref` identified `refs/heads/main` as HEAD at the reviewed full SHA, and a shallow checkout matched it.  
**Published contact:** No email was published in the checked official [README](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md) or [SECURITY.md](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/SECURITY.md). SECURITY.md refers reporters to an address on a GitHub profile; that profile was outside the allowed source set and was not checked. The JSON therefore records null and the checked SECURITY.md URL.

## Identity and review pin

The curated roster identifies position 98 as Brain, slug `brain-db`, with listed locator `https://github.com/arc-labs-ai/brain-db`. Its pinned Atlas report is retained only for identity and attribution; Atlas descriptions, marks, and layout are not assessment evidence.[[roster](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brain-db.md)]

The canonical repository is `arc-labs-ai/brain-db`. A fresh remote symbolic-head lookup and a shallow checkout agree on default branch `main` and full head `69d36cb615140dadc8356ef143eeb57fb19dba65`. All assessment links below pin code and documentation to this revision.[[repository](https://github.com/arc-labs-ai/brain-db)] [[main history](https://github.com/arc-labs-ai/brain-db/commits/main.atom)] [[head commit](https://github.com/arc-labs-ai/brain-db/commit/69d36cb615140dadc8356ef143eeb57fb19dba65)]

## Summary

Brain is a pre-release Rust memory database with a binary wire protocol. It stores raw experiences alongside typed entities, claims, and relations, and combines semantic, lexical, and graph retrieval. Its source defines tenant and space boundaries, temporal claim history, evidence links, and soft or hard forgetting. This review describes repository code and documentation, not measured behavior.[[README](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md)] [[memory model](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/02_data_model/02_memory.md)]

## Who and what

The repository describes Brain as an open-source database for agent memory, implemented in Rust and shipped as a server. The repository names the organization as arc-labs-ai; this review does not infer individual maintainers. The repository supplies the server and wire protocol, while SDKs and other clients are separate projects.[[README](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md)]

## Architecture and data model

Brain stores four related record types. A Memory retains raw text, a 384-dimensional embedding, owner scope, session, timestamps, salience, lifecycle state, and source request. Entities represent canonical objects; Statements are typed Facts, Preferences, or Events; Relations are typed edges. The latter three are derived from memories by extraction tiers and persist only when allowed by the active schema.[[memory model](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/02_data_model/02_memory.md)] [[statement model](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/02_data_model/07_statement.md)] [[README](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md)]

The source describes one Rust process with a binary CBOR wire interface, sharded storage, a write-ahead log, metadata tables, vector and lexical indexes, and a typed graph. Each memory has a stable opaque ID and an owning namespace-space pair. A session groups memories inside one space but is explicitly not an isolation boundary.[[README](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md)] [[tenancy](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/20_tenancy/00_purpose.md)]

A Statement carries kind, subject, predicate, object, confidence, evidence, and four timestamps that separate event validity from when Brain recorded or stopped believing it. Facts may coexist when contradictory; Preferences can supersede prior values; Events remain distinct. Evidence points back to source memories. A typed schema constrains predicates and relations.[[statement model](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/02_data_model/07_statement.md)] [[statement creation](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/crates/brain-metadata/src/statement/crud.rs)]

## Write, update, delete, and retrieval

**Write and update.** The client sends ENCODE text; the server embeds it, writes the memory through the shard writer and WAL, and schedules typed extraction. Request IDs support an idempotency window. Statement creation validates subjects and predicates, records evidence and confidence, and handles duplicate or single-valued claims; supersession atomically links old and new statement versions. The wire offers typed operations rather than arbitrary SQL or a generic document update API.[[README](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md)] [[statement creation](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/crates/brain-metadata/src/statement/crud.rs)] [[supersession](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/crates/brain-metadata/src/statement/supersede.rs)]

**Retrieval.** RECALL routes queries through semantic HNSW, lexical BM25, and graph retrieval, then fuses ranked results with reciprocal rank fusion and applies type, time, confidence, tombstone, and supersession filters. Query intent influences lane weights and candidate pool width. RECALL returns a shaped membership answer; operator-only explain/trace operations expose raw ranking and per-lane detail. The README says ordinary recall is memory-focused; typed graph queries and entity-anchored recall access statement/graph lanes.[[retrieval design](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/13_retrievers/00_purpose.md)] [[query pipeline](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/13_retrievers/05_retrieval_query.md)] [[README](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md)]

**Scope isolation.** Namespace is the tenant boundary and Space is the inner agent or application boundary. The server obtains scope from the authenticated API key, stamps ownership, and partitions reads and writes accordingly; a request cannot ordinarily claim another scope. Session is only a grouping filter. Namespace-wide recall intentionally widens across spaces in that same namespace, not across namespaces. Fine-grained per-memory ACLs are not implemented.[[tenancy](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/20_tenancy/00_purpose.md)] [[README](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md)]

**Forget and deletion.** FORGET supports soft and hard modes. Soft forget makes a memory non-queryable while preserving content through a seven-day default grace period; restoration is allowed during that period. Hard forget purges text and vector data through storage/index paths and does not create a reversible undo journal. Dependent statements and relations are handled through a forget cascade. Reclamation follows the grace period; file capacity is not returned to the operating system. The source review did not establish deletion behavior in backups or external copies.[[memory lifecycle](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/02_data_model/02_memory.md)] [[forget plan](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/crates/brain-planner/src/plan/forget.rs)] [[write path](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/08_storage/03_write_path.md)]

## Metric-domain evidence

These are source observations and documentation claims, not measurements from this review. The project metrics document and benchmark status are protocol/state records only.[[observability](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/17_observability/01_signals.md)] [[retrieval metrics implementation](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/crates/brain-ops/src/metrics/retriever.rs)] [[project metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

| Domain | Source-visible evidence | Review measurement |
|---|---|---|
| Answerable recall and abstention | Membership outcomes and retrieval filters are implemented; no adjudicated probes run | Unmeasured |
| Correction and stale values | Statement supersession and record-time windows are modeled | Unmeasured |
| Deletion leakage | Soft/hard forget and dependent-data cascade are described and implemented | Unmeasured |
| Scope isolation | Namespace/space stamping and scoped retrieval are specified | Unmeasured |
| Evidence and citations | Statements reference source memories; membership results identify contributing retrieval lanes | Unmeasured |
| Latency and write-to-recall delay | Per-query and per-retriever latency metrics and a write pipeline are defined | Unmeasured |
| Tokens, cost, and storage | Source reports embedding/model and storage fields; LLM stage cost accounting is instrumented | Unmeasured |
| Efficiency and observability | Request, writer, retrieval, extractor and forget metrics plus structured logs/traces are documented | Code-visible only; runtime unmeasured |

## Limits and unknowns

Brain is marked pre-release (v0.4.0) and the repository says wire protocol, storage layouts, and schema remain in flux. It is single-node, Linux-only, English-focused, uses one embedding model per deployment, has no client in this repository, and ships without cross-encoder reranking in the current release. The summarizer is disabled by default. The README also says raw-memory recall does not resolve supersession, and per-memory ACLs are out of scope.[[README limitations](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md)]

This bounded review inspected selected current docs and Rust sources. It did not run Brain or verify runtime correctness, retrieval quality, isolation under adversarial deployment, latency, costs, or deletion across snapshots/backups. The documentation includes performance targets and numerous code-level bounds, but neither those targets nor source structure establish measured results for this review.[[README](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md)] [[retrieval design](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/13_retrievers/00_purpose.md)] [[observability](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/17_observability/01_signals.md)]

## Benchmark status

**Benchmark not run.** I did not execute Brain, tests, or benchmark workloads. The project fixture and execution-status record are not Brain measurements.[[project metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [README.md](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/README.md)
- [SECURITY.md](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/SECURITY.md)
- [spec/02_data_model/02_memory.md](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/02_data_model/02_memory.md)
- [spec/02_data_model/07_statement.md](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/02_data_model/07_statement.md)
- [crates/brain-metadata/src/statement/crud.rs](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/crates/brain-metadata/src/statement/crud.rs)
- [crates/brain-metadata/src/statement/supersede.rs](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/crates/brain-metadata/src/statement/supersede.rs)
- [crates/brain-planner/src/plan/forget.rs](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/crates/brain-planner/src/plan/forget.rs)
- [spec/08_storage/03_write_path.md](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/08_storage/03_write_path.md)
- [spec/13_retrievers/00_purpose.md](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/13_retrievers/00_purpose.md)
- [spec/13_retrievers/05_retrieval_query.md](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/13_retrievers/05_retrieval_query.md)
- [spec/20_tenancy/00_purpose.md](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/20_tenancy/00_purpose.md)
- [spec/17_observability/01_signals.md](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/spec/17_observability/01_signals.md)
- [crates/brain-ops/src/metrics/retriever.rs](https://github.com/arc-labs-ai/brain-db/blob/69d36cb615140dadc8356ef143eeb57fb19dba65/crates/brain-ops/src/metrics/retriever.rs)
- [../METRICS.md](../METRICS.md)
- [../fixtures/memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json)
- [../results/initial-baselines-status.json](../results/initial-baselines-status.json)
- [../data/memory-systems.json](../data/memory-systems.json)
- [catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brain-db.md)

## Contact-list follow-up

Checked the official README and SECURITY.md at the reviewed revision. No email is published in those repository documents; SECURITY.md refers to the maintainer's GitHub profile, which was not used. The JSON contact field is null and points to the checked official SECURITY.md URL.
