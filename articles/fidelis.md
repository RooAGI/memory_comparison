# Fidelis Memory source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 238 / Fidelis Memory / fidelis  
**Listed repository locator:** [hermes-labs-ai/fidelis](https://github.com/hermes-labs-ai/fidelis)  
**Canonical upstream:** [hermes-labs-ai/fidelis](https://github.com/hermes-labs-ai/fidelis)  
**Default branch / reviewed head:** main / [9504c4a8f2592464112ca771d6aaefec07698d23](https://github.com/hermes-labs-ai/fidelis/commit/9504c4a8f2592464112ca771d6aaefec07698d23)  
**Review time:** 2026-11-25 20:22:07 UTC (2026-11-25 12:22:07 PST; America/Los_Angeles).

## Identity and review pin

The curated roster lists Fidelis Memory at ordinal 238, slug fidelis, with the explicit locator https://github.com/hermes-labs-ai/fidelis. The associated Agent Memory Atlas source is retained only as roster attribution; Atlas descriptions and assessments were not used as evidence in this review. The official GitHub repository reports default branch main; GitHub's current commit endpoint and patch, plus a fresh git ls-remote and shallow checkout, agree on full head 9504c4a8f2592464112ca771d6aaefec07698d23. This review is pinned to that head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Fidelis Memory is a local-first Python memory service for agents. Its default design stores original passages in a local Chroma vector store, embeds with a configured local Ollama model, and serves bounded retrieval through HTTP and MCP. The documented default MCP recall is fast vector search; a thorough mode combines dense candidate search and optional BM25 with reciprocal-rank fusion. Stored passages are returned as source text rather than generated summaries by default.[[readme]][[reference]][[config]]

## Who and what

The repository identifies Hermes Labs as the project organization and presents Fidelis as a local memory service and client integration for coding agents. The service supports MCP, a loopback HTTP API, and a CLI; the agent decides when to call memory tools. The published Code of Conduct gives roli@hermes-labs.ai as the project maintainer contact; this address is recorded with the exact official source URL in the JSON record.[[readme]][[reference]][[conduct]]

## Architecture and data model

The default store is a local Chroma collection configured under ~/.cogito/store, with Ollama used for embeddings and optional model-backed paths. A service process binds a configured user_id namespace to writes and reads. The code comments explicitly characterize user_id as a storage namespace rather than an authenticated identity or authorization boundary.[[config]][[reference]][[security]]

A stored item contains original text and a stable record ID. When the temporal feature is enabled, the write path adds service-recorded time, a SHA-256 content hash, and optional caller-declared event time, validity bounds, source, and IDs it supersedes. A lightweight SQLite sidecar indexes supersession edges and can be reconciled from the vector-store payloads; it is derived lookup state, not the record store's source of truth.[[degrade]][[temporal]][[temporal-index]]

## Write, update, delete, and retrieval

**Write.** The MCP surface exposes fidelis_store for explicit verbatim storage and fidelis_recall, fidelis_correct, fidelis_get, fidelis_recent, and fidelis_health. The separate HTTP /add path can request model extraction; /store writes supplied text. A deterministic gate can reject recognized secret-shaped or obvious noise content. Successful stores report stored or duplicate; if the backing store or embedding call fails, the write path can persist a queued item for replay. Queueing is not the same as a committed record, and replay rechecks pending supersession declarations.[[reference]][[mcp]][[write-gate]][[degrade]]

**Update and correction.** The documented correction operation creates a new passage whose supersedes field names an existing record in the same configured namespace. It does not overwrite the earlier text. Recall annotates current, superseded, expired, and not-yet-valid records, orders current results first, and normally retains non-current matches with their status visible. An as_of read excludes records not yet recorded by that instant and ignores later correction links. Declared source strings and temporal dates are metadata, not independent proof that a claim is true.[[reference]][[temporal]][[temporal-recall]][[mcp]]

**Delete.** The documented current MCP tool set and HTTP operation table expose no record deletion operation. Correction preserves the prior record as history; a local service uninstall also leaves the store intact. The inspected interfaces therefore provide no supported user-facing fact deletion path in this reviewed revision.[[reference]][[mcp]][[readme]]

**Retrieval.** Fast MCP recall calls the bounded vector route with local embeddings. The zero-LLM recall implementation decomposes a query into multiple searches and merges candidates with reciprocal-rank fusion. Thorough hybrid retrieval admits dense candidates and optionally applies BM25 within that candidate pool before rank fusion; zero-LLM means no generative model, not no learned embedding model. Optional filter or flagship tiers can call configured model endpoints. The default retrieval returns stored wording; the calling agent still interprets it and may answer incorrectly.[[reference]][[recall-b]][[hybrid]][[readme]]

## Scope isolation

The server binds one user_id from local configuration rather than accepting an identity on each request. Reachable vector searches filter on that configured value, and ID-based browse paths reject records whose stored user_id differs. This is useful namespace partitioning within a process and local store, not tenant authentication. The official security policy says the local HTTP interface has no network authentication and is intended for trusted loopback use; the user-fit guide describes the release as single-machine rather than a hosted team service.[[config]][[server]][[recall-b]][[browse]][[security]][[reference]]

## Provenance and evidence

The record model can preserve original text, a service timestamp, content hash, declared source, validity/event times, and explicit supersession links. These fields support traceability to what was stored and how later records relate; the implementation does not verify that caller-provided source metadata is genuine or that a memory's assertion is true. Retrieval results can include temporal status and correction links so a consumer can distinguish current from historical passages. No answer-level citation adjudication or evidence precision was performed here.[[temporal]][[degrade]][[browse]][[reference]]

## Efficiency and observability

The deployment is local and uses a persistent vector store, with multi-query retrieval bounded by configured limits. Thorough retrieval can add BM25 and rank fusion; temporal lookups use a small rebuildable SQLite sidecar. When dependencies fail, writes can be queued for later replay, while retrieval may return a simpler fallback path. Health reports service/store state; MCP diagnostics record tool outcome and elapsed time without query or memory text, while optional retrieval telemetry records bounded query and result metadata with basic secret-pattern redaction. Best-effort diagnostics can be dropped or fail without stopping retrieval.[[config]][[recall-b]][[hybrid]][[temporal-index]][[degrade]][[mcp]][[retrieval-telemetry]][[reference]]

These are implementation observations only. This review collected no latency, indexing, storage, token, cost, or availability measurements. Local deployment also means embeddings and memory storage consume the operator's machine resources.[[metrics]][[status]][[readme]]

## Metric-domain evidence

All Fidelis benchmark domains are unmeasured in this review. The project metric definitions and fixture describe evaluation criteria; they are not a result for Fidelis. No benchmark, system runtime, or tests were run.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
| --- | --- | --- |
| Answerable retrieval and abstention | Search routes and result statuses are implemented; no answers were scored. | Unmeasured |
| Correction and stale values | Supersession links and temporal status are implemented; no correction sequence was evaluated. | Unmeasured |
| Deletion leakage | No supported record-delete operation was found; no deletion probes were run. | Unmeasured |
| Scope isolation | Configured namespace filters are present; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Source metadata and temporal provenance are available; no answer evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timings were collected. | Unmeasured |
| Tokens, cost, and storage | No workload or resource measurements were collected. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the official README, reference, security and contact documentation, and selected source files at the verified head. No runtime, tests, or benchmarks were run. Source structure cannot establish retrieval accuracy, whether agents save useful information, successful deletion, or safe operation under adversarial inputs. The project explicitly says its screening catches common patterns rather than all sensitive data, its local store is not application-encrypted, and the local HTTP service should not be exposed to untrusted networks.[[readme]][[reference]][[write-gate]][[security]]

The review did not audit every client installer or optional model route, nor test backup/restore, concurrent writes, queue recovery, or namespace behavior under hostile access. A configured user_id is not a security boundary. The absence of a documented delete operation is an inspection finding for the reviewed public interface, not proof that no private or future mechanism exists.[[config]][[degrade]][[browse]][[reference]]

## Benchmark status

**Benchmark not run.** No Fidelis runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json); these describe the project protocol and status, not Fidelis measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned Code of Conduct publishes roli@hermes-labs.ai as the maintainer contact. The structured record includes this address and the exact checked source URL. No commit or profile metadata or third-party directory was used.[[conduct]]

## Sources

Repository source links are pinned to the verified full SHA, except the repository identity page and current head patch. The Atlas source is used solely for curated roster attribution. See the structured record [fidelis.json](../data/system-reviews/fidelis.json) and [curated roster](../data/memory-systems.json).
