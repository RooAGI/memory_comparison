# anatid source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 54 / anatid / anatid  
**Listed repository locator:** [thedatasense/anatid](https://github.com/thedatasense/anatid)  
**Current canonical repository:** [thedatasense/anatid](https://github.com/thedatasense/anatid)  
**Default branch / reviewed head:** main / aa7edcdfb5fe220f855c6c74943f7090b561854b  
**Review time:** 2026-11-24 20:38:55 UTC (12:38:55 PST, America/Los_Angeles).

## Identity and scope

The curated roster identifies ordinal 54 as anatid, slug `anatid`, with the listed repository locator above. Its Atlas source URL and revision are recorded for attribution only; Atlas descriptions, marks, and layout were not used as assessment evidence. The official repository page identifies `main` as the default branch, and the official main commit feed identifies full head `aa7edcdfb5fe220f855c6c74943f7090b561854b`. The source and documentation links below pin to this revision.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/thedatasense/anatid)] [[main commit feed](https://github.com/thedatasense/anatid/commits/main.atom)] [[reviewed head](https://github.com/thedatasense/anatid/commit/aa7edcdfb5fe220f855c6c74943f7090b561854b)]

## Summary

anatid is an embedded Python library for agent memory backed by a DuckDB database file. It stores versioned facts and graph relationships with source episodes, and can retrieve through graph expansion, BM25 text search, and optional vector similarity. It also provides MCP and OpenAI Agents SDK integrations and an optional server profile for multiple processes sharing one database. This review records selected code and documentation observations; it did not execute anatid or evaluate runtime quality.[[README](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/README.md)]

## Who and what

The official README presents anatid as an embedded memory library for AI agents. The default profile runs in the caller's process without a required server or background worker; the optional server profile provides one process to own a file when multiple processes need access. MCP and OpenAI Agents SDK integrations expose memory operations to agents.[[README](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/README.md)] [[architecture](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/docs/architecture.md)]

## Architecture and data model

The architecture documentation describes a DuckDB file with entity, memory, episode, and typed-edge tables, plus audit and derived-index tables. Built-in memory and edge rows carry tenant scope, valid-time and transaction-time intervals, writer, source episode, confidence, and version data. Corrections append a new version under the same logical ID rather than rewriting the historical row.[[architecture](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/docs/architecture.md)] [[schema](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/src/anatid/schema.py)]

In the default embedded profile there is no background thread. Full-text, graph adjacency, and optional vector indexes are derived accelerators; canonical DuckDB tables remain the oracle. A write records changes in an index journal in the same transaction, and explicit maintenance builds and publishes index generations.[[architecture](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/docs/architecture.md)] [[derived index framework](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/src/anatid/derived.py)]

## Write, update, delete, and retrieval

**Writes and corrections.** The public verbs include `remember`, `relate`, `supersede`, `correct`, `reinforce`, `unrelate`, and `update`. Corrections close the old transaction-time version and insert a new version in one transaction; `correct` can update a belief and its changing edges together. The source episode and writer fields provide provenance for stored claims.[[mutation verbs](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/src/anatid/verbs.py)] [[architecture](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/docs/architecture.md)]

**Deletion.** Soft `forget` closes the current transaction-time version and retains history and audit information. Hard `forget` purges the memory and related derived-index rows, and the erasure module covers bundled integration tables and registered hooks. The inspection does not establish erasure from backups, external exports, or unregistered external copies.[[mutation verbs](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/src/anatid/verbs.py)] [[erasure](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/src/anatid/erasure.py)]

**Retrieval.** Recall can combine vector similarity, BM25, and graph expansion, then fuse ranked results. The graph arm can seed from entity names detected in the query or explicit seeds. An absent or unusable derived index falls back to canonical paths with status notes; an exact vector scan over the configured ceiling raises unless the caller explicitly allows the slow scan. These are source-level behavior observations, not measured results from this task.[[recall implementation](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/src/anatid/recall.py)] [[architecture](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/docs/architecture.md)]

## Scope isolation

The visibility implementation centralizes tenant and time predicates and offers a matching row-admission check. Current and historical reads use half-open valid-time and transaction-time intervals. Derived indexes may narrow candidates, but candidates are checked using the visibility rule; current-state indexes are not used to answer historical reads.[[visibility implementation](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/src/anatid/visibility.py)] [[architecture](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/docs/architecture.md)]

The project describes one database file per tenant as the actual isolation boundary because DuckDB does not provide row-level access control. The optional server profile checks a principal before opening files. This review did not audit every integration or server authorization path and did not run isolation probes.[[architecture](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/docs/architecture.md)] [[README](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/README.md)]

## Provenance and evidence

Memory rows can point to source episodes and record a writer and confidence. Supersession links preserve correction history, and provenance operations expose source episodes and versions. These fields support tracing stored claims to inputs, but the review does not establish automatic verification of claim truth or generated-answer citations.[[architecture](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/docs/architecture.md)] [[README](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/README.md)]

## Source-visible efficiency and observability

The architecture describes versioned derived-index generations and a journal that makes writes visible to subsequent reads before index maintenance. Index health and recall results report fallback reasons and participating retrieval arms. The docs state that maintenance is explicit rather than background work. These are code and documentation observations; this review collected no latency, throughput, token, cost, or storage measurements.[[architecture](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/docs/architecture.md)] [[derived index implementation](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/src/anatid/derived.py)] [[recall implementation](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/src/anatid/recall.py)]

## Metric-domain evidence

All project benchmark domains remain **unmeasured** for this review. No answerable recall or abstention set, correction/staleness probe, deletion leak check, tenant-isolation probe, evidence adjudication, latency/write-to-recall measurement, token/cost accounting, or storage measurement was run. The upstream README and benchmark documents contain their own reported results; this task did not reproduce them or treat them as project measurements.[[project metric definitions](../METRICS.md)] [[project benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[upstream README](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/README.md)]

## Contact-list follow-up

The official pinned repository README was checked for a published contact email and none was found. The JSON record stores `contact_email: null` and the exact checked README URL. No commit metadata, personal profile email, third-party email directory, or inferred address was used.[[official README](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/README.md)]

## Limits and unknowns

This review inspected selected README, architecture, visibility, recall, schema, mutation, erasure, and derived-index material at the reviewed head. It did not inspect every integration, server path, deletion/export path, or deployment control. The documentation notes that pruning commits per memory and can be partially complete after a failure, and that separate read statements may observe concurrent commits unless wrapped in a transaction. The actual runtime behavior, end-to-end authorization, deletion completeness, answer quality, and operational performance remain unknown from this review.[[architecture](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/docs/architecture.md)] [[erasure](https://github.com/thedatasense/anatid/blob/aa7edcdfb5fe220f855c6c74943f7090b561854b/src/anatid/erasure.py)]

## Benchmark status

**Benchmark not run.** This task did not execute anatid, tests, or benchmark workloads. The project metric definitions and fixture are linked for context; no source claim is presented as a result from this review.[[project metric definitions](../METRICS.md)] [[project benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

The structured source IDs and pinned source URLs are recorded in [anatid.json](../data/system-reviews/anatid.json). The roster's Atlas locator is [the attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/anatid.md); it was used only to identify this curated entry.
