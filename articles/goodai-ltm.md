# GoodAI LTM source and design review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 265 / GoodAI LTM / `goodai-ltm`  
**Listed repository locator:** [GoodAI/goodai-ltm](https://github.com/GoodAI/goodai-ltm)  
**Canonical upstream:** [GoodAI/goodai-ltm](https://github.com/GoodAI/goodai-ltm)  
**Default branch / reviewed head:** main / [22ca10c21771d0192d550517cb06c3aab6e602aa](https://github.com/GoodAI/goodai-ltm/commit/22ca10c21771d0192d550517cb06c3aab6e602aa)  
**Review time:** 2026-11-25 21:17:06 UTC (2026-11-25 13:17:06 PST; America/Los_Angeles).

## Identity and review pin

The catalog records GoodAI LTM at ordinal 265 with slug `goodai-ltm`, an explicit repository locator, and a pinned Agent Memory Atlas roster attribution. The catalog and Atlas entry establish identity and locator context only; Atlas descriptions are not assessment evidence. GitHub's official repository API identifies `main` as the default branch, and its official `commits/main` endpoint resolves to full head SHA 22ca10c21771d0192d550517cb06c3aab6e602aa, whose commit timestamp is 2024-02-28T20:48:35Z. The inspection below is pinned to that head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

GoodAI LTM is a Python library for text-based long-term memory and conversational agents. Its low-level memory stores a bounded stream of tokenized text chunks, indexes their embeddings, and retrieves relevant passages; optional models can rewrite queries or memories and rerank retrieved candidates. The repository also includes LTMAgent, which layers dialog and knowledge-base behavior over the memory library.[[readme]][[factory]][[default]]

## Who and what

The official repository is maintained under the GoodAI organization and describes GoodAI-LTM as a Python package. It offers both a low-level text-memory API and an LTMAgent integration for Python applications; this review does not infer any individual maintainer identity from commit or profile metadata.[[repo]][[readme]]

## Architecture and data model

`AutoTextMemory.create` is the factory for `DefaultTextMemory`. The default configuration uses a tokenizer, an embedding model, a bounded `ChunkQueue`, and the simple vector database; FAISS flat L2 is an alternative. Optional matching, reranking, rewriting, and importance models can be supplied.[[factory]][[default]][[config]]

A `Chunk` holds an integer chunk id, token-sequence bounds, metadata, importance, timestamp, indexing state, and associated text keys. The queue maps integer keys to token-sequence ranges and stores token ids and section boundaries. Text is split into capacity-limited, overlapping chunks; default configuration is 24 tokens per chunk, 50,000 chunks, and 50% overlap. Queue overflow discards oldest chunks, so the default memory is a bounded recent-text buffer rather than an automatically growing durable archive.[[chunk]][[queue]][[config]]

The simple vector database stores NumPy embedding arrays and chunk ids; its search computes squared L2 distances over stored vectors. The alternative FAISS mode uses a flat L2 index. The memory object can serialize its state to text, and separate persistence classes save the queue plus vector index as JSON or JSON plus NPZ. The low-level factory itself constructs an in-process memory; durable storage requires the caller to use the persistence/state APIs.[[simple-db]][[foundation]][[default]][[persistence]]

## Write, update, delete, and retrieval

**Write.** `add_text` accepts text, optional metadata, rewrite settings, and an optional timestamp, then returns an integer text key. The implementation tokenizes the text, inserts it into the queue, and indexes changed chunks with corpus embeddings. `add_separator` prevents chunk expansion across logical sections. Optional memory rewriting and importance scoring depend on explicitly supplied models.[[base]][[default]][[queue]][[readme]]

**Update.** `replace_text` is exposed by the base interface and is routed through the same keyed chunk-queue operation used for text replacement; the returned key lets callers address the stored text. This is mutable in-memory replacement, not a documented version history or correction ledger. The source inspection did not establish transactional persistence across a process restart without the caller's persistence layer.[[base]][[default]][[queue]]

**Delete.** `delete_text(text_key)` removes a selected text entry, and the example also deletes the keys associated with a retrieved result. `clear()` resets the queue and vector database. The reviewed interface and example do not describe deletion receipts, tombstones, an audit log, backup erasure, or cross-process deletion guarantees.[[base]][[delete-example]][[default]]

**Retrieval.** `retrieve(query, k)` returns `RetrievedMemory` passages ordered by relevance. Search encodes the query, asks the vector database for candidates, removes duplicate chunk ids, expands candidates with adjacent tokens within configured boundaries, and can apply a matching model or custom reranker. It can also remove highly overlapping passages and optionally rewrite the query. Retrieved records expose timestamp, distance, relevance, optional confidence and importance, metadata, passage offsets, and associated text keys.[[readme]][[foundation]][[default]][[base]][[config]]

## Scope isolation

The low-level `BaseTextMemory` operations accept text, keys, queries, and metadata but no user, tenant, project, or session scope argument, and the chunk/vector records contain no scope field. LTMAgent maintains dialog session history, but that does not create an isolation boundary for the underlying shared text memory. Applications requiring separation must provide distinct memory instances or enforce scope outside this library; this source review did not test isolation.[[base]][[chunk]][[readme]]

## Provenance and evidence

The library records a timestamp and caller-supplied metadata on chunks and returns associated text keys with retrieval results. Those fields can carry caller-defined references, but the reviewed implementation does not define a source-document identity contract, citation format, confidence provenance, or claim-to-source verification flow. Optional matching confidence and importance are ranking signals, not evidence that a retrieved passage supports a generated answer.[[chunk]][[base]][[default]]

## Efficiency and observability

Chunking bounds each indexed unit and controls overlap/expansion; corpus embeddings are encoded in batches, and FAISS flat L2 provides an alternative to the simple NumPy vector store. The simple store performs dense pairwise distance computation and retains its arrays in process memory, so corpus size and batch size affect memory and search work. The queue's fixed default capacity also bounds retained chunks. Optional `tqdm` progress bars and diagnostic `dump` are the observability surfaces found in the inspected code; no operational metrics or tracing API was identified in these sources.[[config]][[default]][[simple-db]][[base]]

## Metric-domain evidence

All benchmark domains are **unmeasured in this review**. Source structure and repository documentation are not results measured here. No GoodAI LTM runtime, benchmark, or test was run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) for the project's protocol and run status.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Embedding retrieval and optional matching/reranking are implemented; no answer set or abstention behavior was scored. | Unmeasured |
| Correction and stale values | Keyed replacement exists; no correction sequence or stale-value probe was run. | Unmeasured |
| Deletion leakage | Keyed deletion and full clear are exposed; no post-delete probe or durable erasure audit was run. | Unmeasured |
| Scope isolation | The low-level API has no scope key; no cross-user workload was run. | Unmeasured |
| Evidence support and citation coverage | Metadata and text keys are returned; no claims or citations were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Search and indexing code were inspected; no timings or write-to-recall schedule were measured. | Unmeasured |
| Tokens, cost and storage | Token chunk limits and persistence formats were inspected; no workload token, cost, or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This review establishes source behavior at the verified SHA, not runtime quality, deployment safety, or suitability for multi-tenant use. The core memory is in-process and bounded by a chunk queue; persistence is available through explicit state or persistence APIs. The simple vector implementation uses dense pairwise distance arrays. Provider-specific quality, resource use, deletion behavior under persistence, and any application-level isolation depend on configuration and integration and were not independently exercised.[[default]][[queue]][[simple-db]][[persistence]]

The inspected records preserve text, metadata, timestamps, and keys, but do not define source provenance or answer citation verification. No scope key appears in the low-level API or data model. The review did not run the library, its tests, or any benchmark, so recall quality, abstention, correction accuracy, deletion leakage, scope isolation, latency, token use, cost, and storage efficiency remain unknown.[[chunk]][[base]][[metrics]]

## Benchmark status

**Benchmark not run.** No GoodAI LTM runtime, tests, or benchmark workload was executed for this review. No quality, latency, token, cost, storage, deletion, correction, or isolation result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned repository README was checked for a project contact email; it does not publish one. The record therefore stores `contact_email: null` and the exact checked URL. No commit/profile metadata or third-party directory was used.[[readme]]

## Sources

Upstream files are pinned to the verified full SHA. The Atlas source is included only for roster attribution, not system assessment. See the structured record [goodai-ltm.json](../data/system-reviews/goodai-ltm.json) and [curated roster](../data/memory-systems.json).
