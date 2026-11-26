# Apache Maka source review

**Review status:** Reviewed from code at the pinned upstream revision  
**Benchmark status:** Benchmark not run  
**Roster name / slug:** Apache Maka / maka  
**Canonical repository:** [apache/maka](https://github.com/apache/maka/tree/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3)  
**Default branch / reviewed head:** `main` / `16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3`  
**Review time:** 2026-11-24 21:11:34 UTC (13:11:34 PST, America/Los_Angeles)

## Identity and review pin

The curated roster identifies ordinal 62 as Apache Maka, slug `maka`, with listed repository locator [apache/maka](https://github.com/apache/maka). The Atlas source locator and revision are retained for roster attribution only; Atlas descriptions, marks, and layout are not assessment evidence. I independently checked the official repository and read-only `git ls-remote --symref`: the canonical repository is apache/maka, the default branch is `main`, and both `HEAD` and `refs/heads/main` resolve to `16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3`. A shallow checkout resolved to the same SHA.[[official repository](https://github.com/apache/maka)] [[verified main head](https://github.com/apache/maka/commit/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3)] [[curated roster locator](../data/memory-systems.json)]

## Summary

Apache Maka is a local-first agent workspace whose memory combines revisioned personal/project facts with searchable conversation history. A Rust Runtime Host owns model execution, permission checks, sandboxing, and SQLite state. Memory facts can preserve evidence and correction history; Recall can search prior authorized conversations and return source pointers. This is a full application platform rather than a standalone memory library.[[README](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/README.md)] [[memory data types](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/facts/src/memory.rs)] [[conversation Recall](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/assistant/src/recall/search.rs)]

## Who and what

The official repository identifies Apache Maka as an Apache Software Foundation incubating project and describes a local-first terminal and desktop agent workspace. The memory features are part of the integrated Maka Runtime Host and agent tools; they are not a separately deployed memory service.[[README](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/README.md)]

## Architecture and data model

**Code observation.** Maka has two related memory paths. The event log stores durable Run facts and immutable content behind the Host’s SQLite state. Conversation Recall projects selected events into indexed message records. Structured memory is separate: a record has a stable ID, revision/assertion numbers, mode, lifecycle state, body, metadata, and timestamps; versions and evidence are kept in supporting tables.[[README](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/README.md)] [[memory types](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/facts/src/memory.rs)] [[Recall index](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall/index.rs)] [[memory resolution](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/resolution.rs)]

Conversation index rows retain session, turn, message and source positions, role, timestamps, attachments, content references, origin, and field spans. An index row is a derived search view: source history remains available through authorized history reads. Session recap is another derived artifact with an operation receipt and source sequence fence; it reads history under the source’s access boundary.[[Recall store](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall.rs)] [[history contract](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/ports/src/session/history.rs)] [[session recap](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/session-recap/src/recap.rs)]

Personal memory is separate from project memory. The namespace derives from the Run owner; project scope is associated with a Session and a verified workspace identity/permission basis. The inspected source establishes local owner and project boundaries, but does not establish behavior for cross-device synchronization.[[memory types](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/facts/src/memory.rs)] [[memory owner and scope](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/native/src/owner/memory.rs)]

## Write, update, delete, and retrieval

**Fact writes and updates — code observation.** Management operations include create, correct, delete, restore, set-always, and add-evidence. Writes use expected revisions; the resolver checks the scope snapshot before commit and retries if it changed during resolution. It validates edits before applying a batch in a savepoint. Conflicting or unresolved semantic comparisons can retain an unresolved record rather than silently replacing another assertion. Agent extraction is subject to owner policy and Session admission checks.[[memory types](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/facts/src/memory.rs)] [[memory owner](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/native/src/owner/memory.rs)] [[resolution implementation](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/resolution.rs)]

**Delete and restore — code observation.** Deleting a fact suppresses the assertion and related assertions in the same scope; it is a versioned lifecycle action. Restore is explicit and creates a revision. Session removal has a separate cleanup path that removes per-Run Recall rows and schedules referenced content for release. This inspection does not establish physical or backup erasure.[[memory resolution](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/resolution.rs)] [[session removal](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/store/removal.rs)]

**Fact retrieval — code observation.** Recall searches active current facts in the caller’s personal and, when authorized, project scopes. The SQLite FTS5 query uses prefix terms and optional modified-time bounds, applies temporal validity, returns at most 16 facts per page, examines up to 64 matching keys, and enforces a 32 KiB response budget. Results include fact identity/revision, scope and metadata, source references, and an evidence-completeness flag.[[fact Recall](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/recall.rs)] [[memory types](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/facts/src/memory.rs)]

**Conversation retrieval — code observation.** Conversation Recall uses case-insensitive Unicode-normalized literal substring matching. Query terms have OR semantics; results rank by distinct matched terms, then match density, recency, and stable identifiers. Callers can bound by Session and time, and choose a result limit. Each passage includes a source row pointer and history fence; adjacent context defaults to four messages before and after. The uncompacted live tail of the current agent turn is excluded. The UI supports searching within one conversation or across readable conversations.[[Recall query](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall/query.rs)] [[Recall contract](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/assistant/src/recall/types.rs)] [[assistant orchestration](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/assistant/src/recall/search.rs)] [[workbench search](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/products/maka/workbench/app/RecallSearch.tsx)]

**Scope isolation — code observation.** Fact reads recheck caller identity, enabled memory policy, project Session binding, and workspace observation. Agent reads are denied for incognito Sessions and disallowed child/tool/remote origins; a model cannot request another project Session’s scope. Conversation recall uses the authorized Run owner and Session prefix, includes only ready and visible Sessions, and rechecks access around the search worker. These are source predicates; this review did not execute isolation probes.[[memory owner](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/native/src/owner/memory.rs)] [[Recall query](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall/query.rs)] [[history contract](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/ports/src/session/history.rs)]

**Provenance and evidence — code observation.** A memory can reference a conversation Session, sequence, item index, fact ID, byte range, SHA-256 fingerprint, and exact quote. Before accepting that evidence, code checks the immutable source fact, fingerprint, range, and quote text. User-created changes have operation IDs and observation time; version records retain body, metadata, source, and generation method. This provides traceability to stored material, not proof the claim is true.[[memory data types](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/facts/src/memory.rs)] [[evidence verification](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/resolution.rs)] [[content matching](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/matching.rs)]

Conversation recall returns message IDs, source positions and a `SessionRead` pointer so the complete source can be reopened through history authorization. The fact retrieval path checks source visibility and can report incomplete evidence; restricted spans may be masked. These links do not ensure that a generated answer uses or correctly interprets its evidence.[[Recall contract](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/assistant/src/recall/types.rs)] [[history contract](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/ports/src/session/history.rs)] [[fact Recall](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/recall.rs)]

## Metric-domain evidence

No runtime or benchmark observations were collected. The following are source observations or unknowns, not measured results.

- **Answerable recall and abstention:** unmeasured; Recall offers keyword/prefix fact matching and literal conversation search. No answer quality or abstention probes were run.[[fact Recall](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/recall.rs)] [[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)]
- **Correction accuracy and stale-value rate:** unmeasured. Code supports revisioned correction and temporal metadata; no correction workload was run.[[memory types](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/facts/src/memory.rs)] [[metric definitions](../METRICS.md)]
- **Deletion leakage:** unmeasured. Fact deletion suppresses assertions; Session removal has an index and content cleanup path. No post-delete query or physical-erasure audit was performed.[[memory resolution](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/resolution.rs)] [[session removal](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/store/removal.rs)] [[metric definitions](../METRICS.md)]
- **Scope isolation leakage:** unmeasured. Owner, project, Session, and visible-history predicates were found in code; no cross-scope workload was run.[[memory owner](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/native/src/owner/memory.rs)] [[Recall query](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall/query.rs)] [[metric definitions](../METRICS.md)]
- **Evidence support and citation coverage:** unmeasured. Source quotes and pointers are available, but no answer claims were adjudicated.[[memory types](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/facts/src/memory.rs)] [[metric definitions](../METRICS.md)]
- **Latency and write-to-recall delay:** unmeasured; no timing observations were collected.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)]
- **Tokens, cost, and storage:** unmeasured. Recap output has a 1,024-token cap, but this does not measure total input/output tokens or operating cost.[[session recap](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/session-recap/src/recap.rs)] [[metric definitions](../METRICS.md)]
- **Source-visible efficiency and observability:** Conversation Recall uses an FTS5 gram index, paged scans, and bounded context; fact Recall has explicit page and byte limits. Gaps, incomplete evidence, source pointers, and recap pending/ready/failed receipts are represented. These do not establish latency or reliability.[[Recall term index](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall/terms.rs)] [[Recall query](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall/query.rs)] [[fact Recall](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/recall.rs)] [[session recap](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/session-recap/src/recap.rs)]

## Limits and unknowns

This is a bounded source review at one repository revision. It does not establish runtime retrieval quality, model-generated memory correctness, scope isolation under a running deployment, physical deletion from backups or SQLite remnants, performance, token use, cost, or storage consumption. Conversation search in the inspected implementation is literal and keyword-based; no semantic conversation retrieval was identified in these files. Model-assisted fact resolution exists, but its quality was not assessed. No system, benchmark, or tests were run.[[README](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/README.md)] [[memory retrieval](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/recall.rs)] [[conversation search](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall/query.rs)]

The roster’s Atlas report is retained for ordinal, name, slug, listed repository locator, and source attribution only; its descriptions, marks, and layout were not used as assessment evidence.[[curated roster locator](../data/memory-systems.json)]

## Benchmark status

**Benchmark not run.** The shared execution record is `not_run`; the fixture is a planned workload rather than a Maka result. This review did not execute Maka, benchmarks, or tests. All metric domains remain unmeasured.[[metric definitions](../METRICS.md)] [[project execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Official repository page](https://github.com/apache/maka)
- [Verified main branch head](https://github.com/apache/maka/commit/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3)
- [README.md — project overview](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/README.md)
- [SECURITY.md — published vulnerability contact and trust boundaries](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/SECURITY.md)
- [Memory domain types](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/facts/src/memory.rs)
- [Memory owner and scope enforcement](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/native/src/owner/memory.rs)
- [Memory resolution and mutation implementation](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/resolution.rs)
- [Memory matching and evidence](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/matching.rs)
- [Memory fact retrieval](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/memory/recall.rs)
- [Conversation Recall store](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall.rs)
- [Conversation Recall index](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall/index.rs)
- [Conversation Recall query](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall/query.rs)
- [Conversation Recall term index](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/recall/terms.rs)
- [Assistant Recall orchestration](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/assistant/src/recall/search.rs)
- [Recall query and passage contract](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/assistant/src/recall/types.rs)
- [Authorized Session history contract](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/ports/src/session/history.rs)
- [Workbench Recall search UI](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/products/maka/workbench/app/RecallSearch.tsx)
- [Session recap implementation](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/session-recap/src/recap.rs)
- [Session removal cleanup](https://github.com/apache/maka/blob/16e3a7703eccf5f08b62fcb341b7b903f9a3e7e3/plugins/agent/state/src/store/removal.rs)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator](../data/memory-systems.json)

**Verification boundary:** no Maka process, benchmark workload, or tests were run.

---
