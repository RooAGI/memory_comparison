# BrainAPI source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 101 / BrainAPI / `brainapi`  
**Listed repository locator:** [Lumen-Labs/brainapi2](https://github.com/Lumen-Labs/brainapi2)  
**Catalog source attribution:** [Atlas report at pinned revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brainapi.md)  
**Canonical repository / default branch:** [Lumen-Labs/brainapi2](https://github.com/Lumen-Labs/brainapi2) / `main`  
**Reviewed head:** [a94b911a87f54f5ba4fb4942850a19e1ba0e8e95](https://github.com/Lumen-Labs/brainapi2/commit/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95)  
**Review time:** 2026-11-25 00:05:47 UTC (2026-11-24 16:05:47 PST; America/Los_Angeles). GitHub repository metadata identifies the canonical public repository and default branch `main`; the official main commit endpoint currently resolves to the reviewed full SHA.  
**Published contact:** The official pinned [README](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md) publishes `hello@lumen-labs.ai` for commercial licensing. The contact check used only official repository documentation.

## Identity and review pin

The curated roster resolves position 101 to BrainAPI, slug `brainapi`, with listed locator `https://github.com/Lumen-Labs/brainapi2`. The Atlas report is retained only for identity and source attribution; Atlas descriptions, marks, layout, and conclusions are not assessment evidence.[[roster](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brainapi.md)]

The canonical upstream is Lumen-Labs/brainapi2, default branch `main`, at full head `a94b911a87f54f5ba4fb4942850a19e1ba0e8e95`. GitHub repository metadata and the current main commit endpoint were checked independently. Code and documentation references below are pinned to that head.[[repository metadata](https://api.github.com/repos/Lumen-Labs/brainapi2)] [[main commit endpoint](https://api.github.com/repos/Lumen-Labs/brainapi2/commits/main)] [[reviewed commit](https://github.com/Lumen-Labs/brainapi2/commit/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95)]

## Summary

BrainAPI is a Python service that turns ingested material into an event-centered knowledge graph and exposes graph, passage, and typed-fact retrieval. Its README describes an agent pipeline for extracting entities, observations, and graph relationships; inspected intent-memory code provides a separate typed fact and passage path. This review reports source observations and documentation, not measured system behavior.[[README](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md)] [[intent models](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/models.py)] [[intent service](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/service.py)]

## Who and what

The official repository describes BrainAPI as a knowledge graph backed memory service for agents and applications. It is a Python server with REST and MCP interfaces, worker processes, and a console option. The repository identifies Lumen Labs as the project organization; this review does not infer individual maintainer roles.[[README](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md)] [[repository metadata](https://api.github.com/repos/Lumen-Labs/brainapi2)]

## Architecture and data model

The README describes document ingestion as a multi-agent pipeline: Scout extracts entities, Observations records contextual facts, Architect creates event-centered relationships, and Janitor checks and deduplicates graph structures. Events connect an actor, target, and context so retrieval can return a graph path rather than only a nearest-neighbor passage. The README also describes an asynchronous task interface and accurate/lightweight pipeline modes; those are documentation statements, not end-to-end runtime findings from this review.[[README](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md)]

The inspected intent-memory API is a distinct path. An `IntentFact` has an ID and text, verification status, subject/predicate/object, validity timestamps, supersession pointer, source metadata, writer, retirement reason, and kind. Source passages can be retrieved alongside graph relationships. These fields support a typed fact/history model alongside the broader event graph.[[intent models](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/models.py)] [[intent status mapping](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/status.py)] [[intent service](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/service.py)]

A `brain_id` scopes the inspected intent APIs. The BrainPAT guard rejects access when a token is associated with a different requested brain. The code also derives a writer label from a short digest of the token. This source slice establishes a brain-level check, not the complete deployment or organization tenancy model.[[brain resolution](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/brain.py)] [[BrainPAT guard](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/services/mcp/utils.py)]

## Write, update, delete, and retrieval

**Writes.** The README describes ingestion as asynchronous, returning a task ID while the agent pipeline writes graph structures and passages. In the intent service, remember parses a fact, writes/locates graph entities and a relationship, and can associate source keys/passages. Conflicting writes are serialized by brain, subject, and predicate using Redis when available, with an in-process lock fallback. The latest main commit also changes intent extraction to use the configured LLM with regex fallback.[[README](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md)] [[intent service](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/service.py)] [[write lock](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/lock.py)] [[reviewed head](https://github.com/Lumen-Labs/brainapi2/commit/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95)]

**Update and correction.** Correction records a replacement and retires eligible prior relationships using validity end times and supersession metadata. The retirement code avoids closing a later-dated fact when an older fact arrives. It updates lifecycle properties on graph relationships; the README's broad “append-only” description refers to retained event history, not to every stored field being immutable.[[intent service](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/service.py)] [[retirement](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/retire.py)] [[validity helpers](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/saving/validity.py)] [[README](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md)]

**Delete and rejection.** The inspected fact-verification operations are `verify`, `reject`, and `reset`. Verify/reject require a principal and record a state transition. Rejected or superseded facts are filtered from ordinary retrieval paths. Rejection is not physical erasure, and I did not find a general destructive delete operation in the inspected intent service/model slice. The README says graph events are retained rather than deleted; passage, backup, and export erasure behavior was not established here.[[verification service](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/verification/service.py)] [[intent status](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/status.py)] [[README](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md)]

**Retrieval.** The context controller collects graph facts and passage results through dense and lexical channels, then applies ranking, filtering, and response shaping; it has bounded candidate collectors and optional stage profiling. The separate intent recall path collects keyword matches, vector seeds, neighboring graph relationships, and matching passages, then merges, applies status and time filters, annotates conflicts, and ranks facts. The latest main commit routes intent recall/check through this hybrid path instead of a fixed 2,000-fact verification scan.[[context retrieval](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/services/api/controllers/retrieve.py)] [[intent retrieval](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/retrieve.py)] [[validity helpers](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/saving/validity.py)] [[reviewed head](https://github.com/Lumen-Labs/brainapi2/commit/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95)]

**Provenance and evidence.** Intent facts can retain source document, URL, source key, writer, verification state, verifier, note, validity times, and supersession identifiers. Context retrieval can return source passages and graph triples. These records let a caller trace where a fact came from; they do not independently prove the fact is true.[[intent models](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/models.py)] [[intent status mapping](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/status.py)] [[verification service](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/verification/service.py)] [[README](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md)]

## Metric-domain evidence

The following are source observations and documentation, not measurements from this review. The shared project metric definitions, fixture, and execution record describe the evaluation contract and current project status; they do not contain BrainAPI results.[[context retrieval](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/services/api/controllers/retrieve.py)] [[intent retrieval](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/retrieve.py)] [[profiler](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/lib/tracing/profiler.py)] [[project metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

| Domain | Source-visible evidence | Review measurement |
|---|---|---|
| Answerable recall and abstention | Hybrid retrieval, status filters, and unmatched-result fields are implemented in inspected paths | Unmeasured |
| Correction and stale values | Validity windows, supersession pointers, and chronology guards are source-visible | Unmeasured |
| Deletion leakage | Reject/retirement operations are visible; physical erase was not established in this slice | Unmeasured |
| Scope isolation | BrainPAT-to-brain authorization checks are source-visible | Unmeasured |
| Evidence and citations | Facts retain source metadata; context can return passages and graph triples | Unmeasured |
| Latency and write-to-recall delay | Request-stage timing and bounded retrieval collectors are implemented; no runtime timing was collected | Unmeasured |
| Tokens, cost, and storage | The README documents multiple pipeline modes; no measured cost or storage data was collected | Unmeasured |
| Efficiency and observability | Source defines stage wall/CPU/IO spans and diagnostic logs; no runtime telemetry was collected | Code-visible only |

## Limits and unknowns

This review inspected selected current documentation and Python sources. It did not inspect every route, storage adapter, worker, plugin, or deployment path. The README's graph and ingestion descriptions remain documentation claims where implementation was outside the inspected slice.[[README](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md)] [[intent service](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/service.py)] [[context retrieval](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/services/api/controllers/retrieve.py)]

The README calls graph history append-only, while the inspected intent code retires existing relationships by updating lifecycle metadata. The selected sources do not establish complete physical deletion from all passage/vector stores, backups, or exports. Repository code alone also cannot establish production isolation across configuration variants.[[README](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md)] [[intent retirement](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/retire.py)] [[BrainPAT guard](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/services/mcp/utils.py)]

No service, model, tests, or benchmark was run. This review cannot establish answer quality, correction accuracy, deletion leakage, cross-brain isolation under deployment, latency, cost, or production reliability. Source-visible bounds and README targets are not measured results.[[project metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Benchmark status

**Benchmark not run.** I did not execute BrainAPI, tests, or benchmark workloads. The shared project metric definitions, fixture, and status record document the evaluation process and current project-level not-run status; they are not BrainAPI result records.[[project metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [README.md](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/README.md)
- [src/core/intent/models.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/models.py)
- [src/core/intent/service.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/service.py)
- [src/core/intent/retrieve.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/retrieve.py)
- [src/core/intent/status.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/status.py)
- [src/core/intent/retire.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/retire.py)
- [src/core/intent/brain.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/brain.py)
- [src/core/intent/lock.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/intent/lock.py)
- [src/core/verification/service.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/verification/service.py)
- [src/services/mcp/utils.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/services/mcp/utils.py)
- [src/services/api/controllers/retrieve.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/services/api/controllers/retrieve.py)
- [src/core/saving/validity.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/core/saving/validity.py)
- [src/lib/tracing/profiler.py](https://github.com/Lumen-Labs/brainapi2/blob/a94b911a87f54f5ba4fb4942850a19e1ba0e8e95/src/lib/tracing/profiler.py)
- [../METRICS.md](../METRICS.md)
- [../fixtures/memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json)
- [../results/initial-baselines-status.json](../results/initial-baselines-status.json)
- [../data/memory-systems.json](../data/memory-systems.json)
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brainapi.md)

## Contact-list follow-up

The pinned official README publishes `hello@lumen-labs.ai` for commercial licensing. The JSON stores this address and the exact README URL.
