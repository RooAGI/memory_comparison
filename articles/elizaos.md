# elizaOS source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 214 / elizaOS / elizaos  
**Listed repository locator:** [elizaOS/eliza](https://github.com/elizaOS/eliza)  
**Current canonical repository:** [elizaOS/eliza](https://github.com/elizaOS/eliza)  
**Default branch / reviewed head:** develop / 16ecc03e23ce338c6d8fab2a08e544813c0a1ca3  
**Review time:** 2026-11-25 19:03:25 UTC (11:03:25 PST; America/Los_Angeles). GitHub's official repository metadata names `develop` as the default branch; its branch endpoint returned the full head SHA above.

## Identity and scope

The curated roster identifies ordinal 214 as elizaOS, slug `elizaos`, and lists `https://github.com/elizaOS/eliza`. The roster's locator attribution is the Agent Memory Atlas entry at catalog revision `19199a4fc249e89c0793be06f0b166b358089ba0`. GitHub confirms that the listed locator is the canonical repository and that `develop` is its default branch. Atlas is used only for roster identity and locator attribution; no Atlas descriptions or capability claims are assessment evidence.[[roster](../data/memory-systems.json)] [[official repository metadata](https://api.github.com/repos/elizaOS/eliza)] [[develop branch metadata](https://api.github.com/repos/elizaOS/eliza/branches/develop)]

The reviewed head describes “Eliza on Vibestack,” a rewrite specified top-down in VibeLang and Effect. Its README says agents run on the owner's device while cloud services handle identity, billing, and model access. The core specification assigns memory contracts, authorization, and lifecycle to the kernel, with storage adapters, embedding providers, and assistant behavior installed by hosts. The current source tree includes VibeLang memory, access-control, and retrieval modules. This review covers those current artifacts; the README says the rewrite is not a descendant of the older source baseline, and the published spec does not establish full implementation-to-spec conformance.[[README — current project and rewrite scope](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/README.md)] [[core specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/index.md)] [[memory types and constructors](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/types/memory.vibe)] [[memory implementation](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/memory.vibe)]

## Architecture and data model

The public memory types distinguish message, document, fragment, description, and custom memories. A message memory includes entity, optional agent, room, content, optional embedding, creation time, and metadata. Metadata supports scope, source identifiers, timestamps, tags, and sharing information. The separate long-term-memory type describes episodic, semantic, and procedural records with agent/entity identity, content, optional embedding, confidence, source, timestamps, and access counters. These are contracts and type declarations, not proof that every host persists every field.[[memory types](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/types/memory.vibe)] [[long-term-memory type](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/types/long-term-memory.vibe)]

Persistence is adapter-owned. The core specification retains batch-first CRUD for memories among other records and says adapters own durable I/O and transaction semantics. A separate fact-write model describes serializing concurrent contributions by natural fact key: read existing canonical data, merge under one owner, then commit while preserving earlier evidence on writer failure. The model does not specify a universal physical database or independently demonstrate that every host implements the contract.[[storage specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/storage.md)] [[serialized fact writes](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/factWrites.md)]

## Write, update, delete, and retrieval

**Writes.** Message-memory construction stamps a timestamp and defaults scope to private when an agent ID is present, otherwise shared. App conversation provenance fills provider, account, platform-message, and source identifiers when absent. Response-memory persistence can be skipped through explicit transient/do-not-persist flags. Storage itself crosses the host adapter boundary. For facts, the spec models per-key serialized read/merge/commit. Embedding writes capture the source before inference, retry within policy, and compare the source revision before accepting a stored receipt; an edited source can make the result stale.[[memory implementation](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/memory.vibe)] [[fact-write specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/factWrites.md)] [[embedding-write specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/embeddingWrite.md)]

**Updates and deletion.** The persistence contract includes memory CRUD; runtime mutation wrappers preserve adapter results/errors and invalidate relevant cached reads after successful mutations. Single-memory writes perform secret redaction before publication, and embedding-only writes use adapter compare-and-swap. The reviewed specifications do not establish one end-to-end deletion policy for message memories, long-term memories, derived facts, embeddings, or backups, so complete erasure behavior is unknown.[[entity and memory mutation contract](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/entities.md)] [[storage specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/storage.md)]

**Retrieval.** Core retrieval tokenizes a corpus and supports BM25 lexical scoring, phrase matching, and ranked memory candidates. The specification describes lexical score, then trigram/vector similarity, recency, and stable identity as ordering dimensions. It filters candidates to caller-authorized room/world scopes before ranking and pagination, so out-of-scope items neither appear nor displace eligible results. A non-positive memory limit returns an empty page. The VibeLang source implements the BM25 and message ranking logic; no result-quality claim follows from that implementation alone.[[retrieval implementation](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/retrieval.vibe)] [[retrieval specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/retrieval.md)]

## Scope isolation and provenance

Memory scope has seven declared values: shared, private, room, global, owner-private, user-private, and agent-private. Message construction chooses a default based on whether an agent ID is supplied. The retrieval contract requires the caller's allowed rooms and worlds to be decided before retrieval and removes other scopes before ranking. The memory-scope helper validates scope names and resolves an entity scope from metadata. These are code/spec observations; no adversarial cross-user or cross-room test was run in this review.[[memory scope types and implementation](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/access-control/memory-scope.vibe)] [[scope-filtered retrieval contract](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/retrieval.md)]

Provenance fields include source/sourceId and platform-message identifiers. The app provenance helper requires a durable memory ID and fills missing source identity from the platform message ID. The fact-write model retains contributions by writer, and embedding writes bind a vector to the exact source revision captured before inference. These mechanisms preserve lineage or source identity; the inspected sources do not establish evidence-backed answer citations or human adjudication of extracted facts.[[memory provenance implementation](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/memory.vibe)] [[fact-write specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/factWrites.md)] [[embedding-write specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/embeddingWrite.md)]

## Efficiency and observability

The retrieval implementation uses an in-memory BM25 corpus, term/document frequencies, typed numeric score buffers, and a top-K path; the specification defines query limits and stable ranking. Embedding writes are batched through a queue with retries and exact-source receipts. These structures suggest bounded candidate work and explicit write settlement but are not performance measurements. The bounded inspection found no memory-specific runtime telemetry or benchmark outcomes; latency, token/cost, storage, and write-to-recall efficiency remain unmeasured.[[retrieval implementation](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/retrieval.vibe)] [[embedding service specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/embeddingService.md)] [[project metrics](../METRICS.md)]

## Limits and unknowns

This is a bounded review of the current README, memory types and constructors, retrieval and scope source, and core specifications at the verified head. The system, tests, and benchmarks were not run. Host adapter choices, migration behavior, durable fact-store implementation, production authorization configuration, cross-scope isolation under deployment, extraction quality, correction behavior, complete deletion, and runtime performance remain unverified. The README describes a formal-specification-led rewrite; model/spec properties should not be treated as runtime guarantees without implementation conformance evidence.

The official project website linked by GitHub publishes `hello@elizaresearch.ai` as a contact address. No other contact source was used.[[official project website and contact](https://elizaresearch.ai/)]

## Benchmark status

**Benchmark not run.** No elizaOS process, benchmark workload, or test suite was run for this review. The project metric definitions describe measurement dimensions only.[[project metric definitions](../METRICS.md)] [[benchmark status record](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical repository metadata](https://api.github.com/repos/elizaOS/eliza)
- [Current develop branch metadata](https://api.github.com/repos/elizaOS/eliza/branches/develop)
- [Reviewed repository tree at full SHA](https://github.com/elizaOS/eliza/tree/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3)
- [README — current project and rewrite scope](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/README.md)
- [Core specification index](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/index.md)
- [Message memory types](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/types/memory.vibe)
- [Long-term memory type](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/types/long-term-memory.vibe)
- [Memory construction, provenance, and persistence flags](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/memory.vibe)
- [Memory scope helper](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/access-control/memory-scope.vibe)
- [Retrieval implementation](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/packages/core/src/retrieval.vibe)
- [Retrieval specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/retrieval.md)
- [Storage specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/storage.md)
- [Entity and memory mutation contract](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/entities.md)
- [Fact-write specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/factWrites.md)
- [Embedding-write specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/embeddingWrite.md)
- [Embedding service specification](https://github.com/elizaOS/eliza/blob/16ecc03e23ce338c6d8fab2a08e544813c0a1ca3/spec/core/embeddingService.md)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution status](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster identity and Atlas locator attribution](../data/memory-systems.json)
- [Official project website and contact email](https://elizaresearch.ai/)
