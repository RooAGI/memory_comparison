# AgentRT

## Identity and review pin

- **Curated ordinal:** 28 in `data/memory-systems.json`
- **Listed name / slug:** AgentRT / `agentrt`
- **Listed repository locator:** https://github.com/openairymax/agentrt
- **Canonical repository:** https://github.com/openairymax/agentrt
- **Default branch:** `main`
- **Reviewed head:** [`2719f88253f59369cea7fad460515b6cc8ac5547`](https://github.com/openairymax/agentrt/commit/2719f88253f59369cea7fad460515b6cc8ac5547)
- **Reviewed at:** 2026-11-24 19:14:19 UTC (11:14:19 PST, America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The roster's Atlas source is [the pinned AgentRT report](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agentrt.md). It supplied identity, locator and attribution only. Atlas descriptions, feature marks and layout were excluded from this assessment.

## Summary

AgentRT is a C11 agent runtime whose `mem_d` service stores bounded memory records in JSONL. It provides writes, reads, deletion, ranked retrieval and knowledge-base operations, with TF-IDF and substring scoring plus optional embeddings. Findings below describe selected documentation and code at the reviewed revision; they are not runtime results.

## Who and what

The official [README](https://github.com/openairymax/agentrt/blob/2719f88253f59369cea7fad460515b6cc8ac5547/README.md) describes AirymaxAgentRT as a runtime platform and this repository as a release aggregate that pins component repositories as Git submodules. The official [daemon overview](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/README.md) identifies `mem_d` as the persistent memory service. No individual maintainer identity is inferred.

## Architecture and data model

The release README describes kernel, storage, gateway, protocol, daemon and SDK layers. The `mem_d` daemon exposes memory operations over the `mem.*` JSON-RPC namespace and separates handlers, service orchestration, scoped retrieval, JSONL persistence, knowledge-base, embedding, cache, context ledger and compression modules. See the [daemon overview](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/README.md) and [mem_d guide](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/README.md).

A memory record contains a generated ID, content and length, optional JSON metadata, and creation time. In memory, the service also caches a term-frequency vector and may hold an embedding. It keeps records in a bounded array and indexes IDs for direct lookup. The root [heapstore documentation](https://github.com/openairymax/heapstore/blob/fb79d0683a4f8d6bbb23756b782fbec34aab1d5a/README.md) and [heapstore memory API](https://github.com/openairymax/heapstore/blob/fb79d0683a4f8d6bbb23756b782fbec34aab1d5a/include/heapstore_memory.h) describe a separate pool/allocation accounting subsystem; that API is not AgentRT's long-term memory record store.

The daemon stores records as JSONL under the runtime data directory. Writes append and sync a line; deletion and capacity eviction rewrite the active file through a temporary file, sync and rename. Term vectors are rebuilt from text on startup. The external embedding service is optional. These persistence properties are source observations, not a durability test.

## Write, update, delete, and retrieval

- **Write:** `mem.write` creates a 32-character hexadecimal ID, stores the content and optional caller-supplied metadata, builds a TF-IDF vector and appends the record. When the configured record cap is reached, the oldest record is evicted. The inspected RPC contract has no general in-place update operation; callers can write another record and delete the prior ID.
- **Read and delete:** `mem.get` reads by ID. `mem.delete` removes a record from the live array and index, adjusts document frequencies, and rewrites JSONL. `mem.kb_delete` removes the records associated with one KB. These are hard removals from the active store, not a versioned correction or tombstone history.
- **Search:** `mem.search` tokenizes and scores query candidates with TF-IDF cosine similarity fused with substring-match density (default TF-IDF weight 0.6). An optional embedding endpoint supplies vector scores; failed requests enter a cooldown and fall back to TF-IDF. The implementation scans candidate records, scores them, sorts positive hits, and trims to the requested limit. `mem.recent` walks insertion order newest-first. `mem.evolve` merges search hits or copies a selected record into a new record with source metadata; it leaves the source records in place.
- **Knowledge bases:** `mem.kb_ingest` splits text at UTF-8-safe byte boundaries (512 bytes by default), tagging chunks with `kb_id`, optional `doc_id`, and a chunk number. KB search filters to the requested KB before ranking; KB delete removes all records with that KB ID.
- **Adjacent facilities:** `mem_d` also includes a semantic cache and context ledger/compressor. Cache calls expose exact/semantic hit results, hit rate, eviction count and bytes; the ledger records context structure and token counts. These facilities are distinct from the persisted memory record search path.

See the [service implementation](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/core/service.c), [record and scope API](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/core/mem_service.h), [scoped search implementation](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/core/scope.c), [RPC handlers](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/handlers/mem_handlers.c), [persistence code](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/engine/mem_persist.c), [KB engine](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/engine/kb.c), [vector API](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/engine/vector.h), and [embedding client](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/engine/emb_client.c).

## Scope isolation

Search and recent accept optional `conv` and `tenant` filters; the service also supports a KB filter. Filtering happens before ranking so out-of-scope hits do not consume the requested limit. Missing tenant metadata maps to the default tenant. The RPC exposes these as optional caller fields, so omitting them broadens reads. Direct `get` and `delete` use record IDs and have no scope argument in the inspected handlers. These observations do not establish authorization or tenant isolation.

## Provenance and evidence

Normal record metadata is optional JSON supplied by the writer. `mem.evolve` stores source record identifiers and query/evolution metadata, and KB chunks record their document and chunk identifiers. The inspected interfaces do not require provenance fields or validate that a retrieved item supports a generated answer; citation quality and source trust are unknown.

## Source-visible efficiency and observability

The service holds records, vectors and an ID index in memory, caps record count (1,024 by default), appends writes, and performs candidate scoring followed by a full sort of positive hits. Embeddings use network calls outside the record lock and have timeout/cooldown fallback behavior. These are code observations; no latency, scale, token or cost measurements were collected.

The daemon provides health and record-count endpoints, configured capacity, cache statistics (hits, misses, hit rate, evictions and bytes), context-ledger counts and structured log messages. The reviewed search path logs hit counts and vector usage but does not expose measured search duration through the inspected RPC response.

## Metric-domain evidence

All metric domains below are **unmeasured** for this review. Definitions are in [METRICS.md](../METRICS.md); the [shared status record](../results/initial-baselines-status.json) and [planned fixture](../fixtures/memory-benchmark-v1.json) are not AgentRT measurements.

| Domain | Source observation | Measurement status |
|---|---|---|
| Answerable recall and abstention | Ranked search results and configurable retrieval legs exist. | Unmeasured |
| Correction accuracy and stale values | No general in-place correction-history contract was established. | Unmeasured |
| Deletion leakage | Active records and JSONL are removed or rewritten. | Unmeasured |
| Scope isolation | Optional conversation, tenant and KB filters exist. | Unmeasured |
| Evidence support and citation coverage | Metadata and evolve source IDs are available, without required evidence validation. | Unmeasured |
| Latency and write-to-recall delay | Candidate scan, sorting and optional embedding calls are visible in code. | Unmeasured |
| Tokens, cost and storage | Ledger token and cache byte counters exist; no workload measurements were taken. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of selected documentation and source at one verified revision. It does not establish runtime correctness, retrieval quality, performance, operational reliability, security boundaries, or deletion completeness. The aggregate repository pins component repositories as submodules; this review followed the daemon and heapstore paths at the reviewed aggregate commit.

Default capacity is 1,024 records and configurable; the record table is bounded, and search scores candidate records before sorting hits. The review does not establish practical scaling or provider cost. Search scope filters are optional, and direct get/delete do not accept scope parameters in the inspected handler contract. Metadata is caller-provided and no enforced provenance or correction precedence was established. The embedding service's actual behavior, persistence durability under faults, and tenant safety remain untested.

## Benchmark status

**Benchmark not run.** No AgentRT runtime, benchmark workload, or tests were run. Source observations above are not measurements. The [structured system review](../data/system-reviews/agentrt.json) records the source contract. The [project metric definitions](../METRICS.md), [execution-status record](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json) remain separate.

## Sources

- [Canonical AgentRT repository](https://github.com/openairymax/agentrt)
- [Reviewed head commit](https://github.com/openairymax/agentrt/commit/2719f88253f59369cea7fad460515b6cc8ac5547)
- [Official README at reviewed revision](https://github.com/openairymax/agentrt/blob/2719f88253f59369cea7fad460515b6cc8ac5547/README.md)
- [Official support contact](https://github.com/openairymax/agentrt/blob/2719f88253f59369cea7fad460515b6cc8ac5547/SUPPORT.md)
- [Daemon overview](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/README.md)
- [mem_d guide](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/README.md)
- [Memory service implementation](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/core/service.c)
- [Memory service record and scope API](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/core/mem_service.h)
- [Scoped retrieval implementation](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/core/scope.c)
- [JSON-RPC handlers](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/handlers/mem_handlers.c)
- [JSONL persistence implementation](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/engine/mem_persist.c)
- [Knowledge-base implementation](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/engine/kb.c)
- [TF-IDF vector API](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/engine/vector.h)
- [Embedding client](https://github.com/openairymax/daemons/blob/bfa20573b7e1fcb9046e83b487f7d8d08ffbd907/mem_d/src/engine/emb_client.c)
- [heapstore documentation](https://github.com/openairymax/heapstore/blob/fb79d0683a4f8d6bbb23756b782fbec34aab1d5a/README.md)
- [heapstore memory API](https://github.com/openairymax/heapstore/blob/fb79d0683a4f8d6bbb23756b782fbec34aab1d5a/include/heapstore_memory.h)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution-status record](../results/initial-baselines-status.json)
- [Planned benchmark fixture](../fixtures/memory-benchmark-v1.json)
