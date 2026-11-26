# gaius source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 250 / gaius / gaius  
**Listed repository locator:** [jkubo/gaius](https://github.com/jkubo/gaius)  
**Current canonical repository:** [jkubo/gaius](https://github.com/jkubo/gaius)  
**Default branch / reviewed head:** main / `76ff7c5422bbeddcb7101c5802242989a583f3ac`  
**Review time:** 2026-11-25 20:37:29 UTC (12:37:29 PST; America/Los_Angeles).

## Identity and scope

The curated roster places **gaius** at ordinal 250, slug `gaius`, with the explicit listed repository locator `https://github.com/jkubo/gaius` and attribution to Agent Memory Atlas revision `520c2eb12627e2c7eb886999b5377a20ee31a7b8`. The official repository is jkubo/gaius; the official Git remote reports `main` as the default branch and current head `76ff7c5422bbeddcb7101c5802242989a583f3ac`. The roster is used only for system identity, locator, and attribution. Atlas descriptions and assessments are not evidence in this review.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/jkubo/gaius)] [[reviewed head commit](https://github.com/jkubo/gaius/commit/76ff7c5422bbeddcb7101c5802242989a583f3ac)]

Gaius describes itself as an ops memory lifecycle manager for AI coding agents. It is a self-hosted Python package and CLI with optional MCP and semantic-search extras. The README describes session capture, fact extraction, a local SQLite corpus, review and decay, and context injection; this review covers the checked-in implementation and docs, not a hosted service.[[README.md](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/README.md)] [[package architecture](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/ARCHITECTURE.md)]

## Architecture and data model

The core facts store is a local SQLite database. Its schema includes facts, sessions, domains, entities, temporal triples, and fact-to-entity links. Fact rows carry content and topic domain, timestamps, confirmation counts, agent/session/principal/model-family lists, provenance, scores, confidence and review state, outcomes, verification metadata, and tombstone fields. If sqlite-vec is available the database also gets a vector table; semantic retrieval is optional.[[facts schema and upsert](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/facts.py)]

The package separates session parsing and extraction, storage/deduplication, review, scoring, injection, embeddings, knowledge graph, telemetry, and the MCP server. `gaius inject` ranks stored facts together with memory and skills; MCP exposes fact search and direct fact addition.[[architecture](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/ARCHITECTURE.md)] [[injection](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/landscape.py)] [[MCP server](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/mcp_server.py)]

## Write, update, delete, and retrieval

**Write and update.** Session retirement and ingest paths extract facts into the corpus, while MCP's `gaius_fact_add` writes through the same upsert path. An exact fact-key match updates last-seen time, confirmation count, and provenance-related identity lists rather than replacing the stored text. Optional semantic deduplication can corroborate a close vector match; low-confidence or contradictory new facts enter a pending review state. This describes code behavior, not correction accuracy.[[README.md](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/README.md)] [[upsert and deduplication](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/facts.py)] [[MCP fact add](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/mcp_server.py)]

**Correction and deletion.** Review commands can confirm, reject, or defer a fact. Rejection keeps the row but excludes it from relevant retrieval. Duplicate cleanup uses soft tombstones; the decay command can also tombstone stale `live` facts when its TTL option is enabled. I did not find a general permanent-delete or user-forget operation in the inspected public CLI/MCP paths, nor a versioned correction history. Tombstones and rejection do not establish physical erasure.[[review lifecycle](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/review.py)] [[fact tombstones](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/facts.py)] [[optional live TTL](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/maturity.py)]

**Retrieval.** Injection ranks facts against task or prompt terms with TF-IDF/BM25-style scoring and, when enabled, semantic similarity, recency/decay, and review-state weighting. It then applies token budgets and session deduplication. MCP search combines keyword and optional vector scores and returns ranked fact text, domain, score, and first/last-seen dates. The README documents chunking long facts for embeddings. These ranking mechanisms do not establish answer correctness or calibrated abstention.[[README.md](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/README.md)] [[injection and ranking](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/landscape.py)] [[MCP search](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/mcp_server.py)] [[embedding chunking](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/embed.py)]

## Scope isolation, provenance, and evidence

**Scope isolation.** Facts have topic domains and injection/search accept optional domain filters. The default session injection path does not inherently select an authorization scope, and the inspected fact schema/retrieval paths do not enforce user, tenant, or project ACLs on fact rows. A project field on the sessions table is not by itself an access boundary. No cross-user or cross-project leakage probes were run.[[facts schema](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/facts.py)] [[injection filter](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/landscape.py)] [[MCP search](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/mcp_server.py)]

**Provenance and evidence.** Facts retain agent, session, principal, model-family, source, and provenance labels, along with confidence, review/outcome state, and optional verification metadata. Knowledge-graph triples can retain source session, agent, fact ID, extraction time, confidence, and validity windows. These fields preserve lineage and review signals; the inspected retrieval output does not provide claim-level quotations or demonstrate that a fact is true.[[facts schema](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/facts.py)] [[architecture](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/ARCHITECTURE.md)] [[review and retrieval output](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/review.py)] [[MCP search](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/mcp_server.py)]

## Efficiency and observability

The README and code describe offline SQLite storage, optional 384-dimensional vector embeddings, chunked long-fact embeddings, and an optional warm embedding daemon. Injection telemetry can record session/prompt identifiers, skip reasons, injected counts, token use and budget, and top cosine score; per-fact events record score and priority. These are source-visible mechanisms, not measured efficiency or quality.[[README.md](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/README.md)] [[vector storage](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/facts.py)] [[embedding implementation](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/embed.py)] [[telemetry schema](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/telemetry.py)] [[injection](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/landscape.py)]

## Project metric domains

All project benchmark domains are **unmeasured in this review**. No answerable-recall or abstention workload, correction or stale-value probe, post-delete leakage probe, cross-scope isolation probe, or evidence-support adjudication was run. No retrieval latency distribution, write-to-recall delay, token or provider-cost total, or corpus storage measurement was collected. Project metric definitions, fixtures, and result status are protocol/status references, not gaius measurements.[[project metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded, read-only inspection of the current README, architecture notes, and selected storage, write, review, retrieval, embedding, and telemetry source at the verified repository head. Gaius, its tests, and benchmarks were not run. Retrieval quality, safe correction, physical deletion, access isolation, production behavior, and runtime performance remain unknown. Any upstream benchmark or performance statements were not reproduced or treated as this review's measurements.[[README.md](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/README.md)] [[facts](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/facts.py)] [[retrieval](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/gaius/landscape.py)] [[project metric definitions](../METRICS.md)]

## Contact

The official README at the reviewed commit was checked for a published contact email; none was found. No address was inferred from package metadata, commit data, or profiles.[[checked official README](https://github.com/jkubo/gaius/blob/76ff7c5422bbeddcb7101c5802242989a583f3ac/README.md)]

## Benchmark status

**Benchmark not run.** No gaius runtime, tests, or benchmark workload was run. Project metrics, fixture, and execution-status files define protocols and status; they are not gaius results.[[project metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]
