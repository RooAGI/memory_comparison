# beads

## Identity and review pin

- **System:** beads
- **Curated position:** 89
- **Slug:** `beads`
- **Listed repository:** [gastownhall/beads](https://github.com/gastownhall/beads)
- **Canonical repository at review:** [gastownhall/beads](https://github.com/gastownhall/beads)
- **Default branch:** `main`
- **Reviewed head:** [`78624109904655d7a4609f27d34eb0982cd8963f`](https://github.com/gastownhall/beads/commit/78624109904655d7a4609f27d34eb0982cd8963f)
- **Reviewed:** 2026-11-24 23:28:48 UTC (15:28:48 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/beads.md), used only for identity, listed repository, and source attribution.

The curated roster identifies beads at position 89, slug `beads`, with the repository locator above.[[catalog]] The Atlas source is preserved for attribution only; its descriptions, marks, and layout were not assessment evidence.[[atlas]] The official repository page identifies `main` as its default branch; the official main Atom feed identified the reviewed full head `78624109904655d7a4609f27d34eb0982cd8963f`.[[repo]][[head-feed]][[head]]

## Summary

Beads is a Dolt-backed, workspace-scoped task graph for coding agents that also exposes a small persistent memory plane. Named memories are stored as string values in a reserved namespace, can be recalled or forgotten by exact key, and are appended to `bd prime` session context. This is a pinned source review, not a runtime or benchmark evaluation.[[readme]][[memory-doc]][[memory-api]][[prime]]

## Who and what

The canonical repository is `gastownhall/beads`. The README presents Beads as a distributed graph issue tracker for AI coding agents, powered by Dolt, and documents `bd remember` for saving durable project facts that `bd prime` later injects. It is a Go CLI and library with embedded or server-backed Dolt storage and an experimental HTTP backend; this article reviews its memory plane, not the whole issue-tracking system.[[repo]][[readme]][[memory-doc]]

## Architecture and data model

**Source observations.** The memory plane is a keyed string namespace exposed through four operations: `Remember`, `Recall`, `Forget`, and `List`. It is separated from workspace settings even though both share the config table. Storage implementations encode a caller's key under the reserved `kv.memory.` prefix. The package documents a separate merge rule: a config conflict is auto-resolved with the remote side only when every conflicting key has this prefix. That makes merge behavior part of what persistent memory means in Beads.[[memory-doc]][[memory-api]]

The README identifies Dolt as the database backend, with embedded mode as the default and a server mode for concurrent writers. The memory package describes the records as workspace data, not per-user objects. Dolt remotes can synchronize workspace database contents across clones. The security policy says data is stored in plaintext and access control relies on filesystem permissions; the reviewed sources do not establish separate memory isolation for agents or operating-system users.[[readme]][[security]][[memory-doc]]

`bd prime` combines workflow context and persistent memories, supports custom workflow templates while continuing to append memories, and has memory-only and no-memory modes. Its source documents optional count and character caps applied at whole-memory boundaries; explicit zero means unlimited. A store timeout is also configurable. The review inspected the prime command contract and memory interface, but did not trace all front doors into concrete database implementations.[[prime]][[memory-doc]][[memory-api]]

## Write, update, delete, and retrieval

**Write and update.** `bd remember` stores a value under an explicit key or derives a key if omitted. The interface rejects content empty after trimming and rejects content with no derivable key when the caller omitted one. Explicit keys are used verbatim. Otherwise the stored value remains verbatim, including whitespace and newlines. The returned key/value identify what was stored; a `Replaced` flag reports whether a prior row existed, including a row whose value was empty.[[memory-api]][[readme]]

Remember always performs the write, even if the value is unchanged. The API specifies that the prior-existence observation and write happen in one transaction, while the returned removed value and delete for Forget likewise share a transaction. Recall is read-only. A missing Recall key returns `Found: false`; forgetting a missing key succeeds with `Found: false` and changes nothing. Repeated Forget is therefore safe under the documented result contract.[[memory-api]][[memory-doc]]

**Delete.** `bd forget <key>` removes one keyed memory from the memory namespace. It is distinct from generic key/value rows and settings in the shared table. No per-memory tombstone or user-facing memory history is established by the inspected memory interface; the package documents how memory-key conflicts are merged, but this review did not trace whether Dolt history, remotes, backups, or external copies retain deleted values.[[readme]][[memory-api]][[memory-doc]][[security]]

**Retrieval.** `bd recall` reads one exact key. `bd memories` lists memories and may filter by case-insensitive substring in a key or value. List returns an unpaged, unordered map and the front doors sort keys for display. The package documentation says the shape is intended for workspaces with tens of rows, not thousands. `bd prime` appends the persistent memory section to agent context, with optional count and character caps; the cap boundary is a whole memory, and the command can omit memories or return only that section.[[readme]][[memory-api]][[memory-doc]][[prime]]

## Scope isolation

The memory plane is scoped to the selected Beads workspace/database. Its public requests carry a key and value but no tenant, principal, agent, or record-level ACL. Repository initialization, alternate workspace directories, and Dolt synchronization determine where the data resides and which clones share it. The security policy describes no built-in access control beyond filesystem permissions. Separate tenant/user isolation in each hosted, server, or library configuration was not fully verified from this selected source set.[[memory-doc]][[memory-api]][[readme]][[security]]

## Provenance and evidence

A memory is a string under a key. The memory API does not require a source URL, excerpt, author, timestamp, confidence, trust state, or correction lineage. The README recommends storing durable project facts and keeping operator preferences in the agent harness's own memory, but no evidence validation or human review contract appears in the inspected memory interface. The broader issue tracker has separate records and history facilities; those are not automatically attached to values in this memory plane.[[memory-api]][[readme]][[memory-doc]]

## Source-visible efficiency and observability

**Code observations, not measurements.** Memory List materializes an unordered map without paging, which keeps the interface simple for small workspaces but gives no bounded page size as a namespace grows. Search is a case-insensitive substring check against key or value at the operation contract. Remember performs a write even for an equal value. These are source-level behaviors; no CPU, storage, or throughput costs were measured.[[memory-doc]][[memory-api]]

Prime provides explicit controls for injected memory count and characters, preserves whole-memory boundaries, supports disabling memory injection, and sets a configurable store timeout (10 seconds in the inspected source when unset or invalid). These controls address context volume and slow storage. The sources do not establish measured token savings, latency, or the default cap values for count/characters, and this review collected no runtime telemetry.[[prime]]

## Metric-domain evidence

All domains below are **unmeasured for this review**. Source mechanisms and project evaluation plans are not benchmark outcomes.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Exact-key Recall and substring List exist; no answerability probes were run. | Unmeasured |
| Correction accuracy and stale values | Remember replaces a key's value; no correction sequence was scored. | Unmeasured |
| Deletion leakage | Forget removes a memory row; no post-delete probes or residual-copy checks were run. | Unmeasured |
| Scope isolation | The API is workspace-scoped and has no principal field; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Values are unstructured strings without required evidence metadata; no claim adjudication was run. | Unmeasured |
| Retrieval latency and write-to-recall delay | Prime has timeout and cap controls; no timing observations were collected. | Unmeasured |
| Tokens, cost, and storage | Prime can cap injected characters; no token, cost, or storage measurements were collected. | Unmeasured |

The [project metric definitions](../METRICS.md), [versioned benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) define plans and project-wide status only; they are not Beads results.[[metrics]][[fixture]][[status]]

## Limits and unknowns

This is a bounded read-only review of selected documentation and code at the reviewed SHA. It does not establish runtime CLI behavior, concrete transaction implementation, scope isolation across all backends, exact default memory injection caps, delete retention across Dolt history/remotes/backups, retrieval quality, or real latency, cost, and storage.[[memory-doc]][[memory-api]][[prime]][[security]]

The memory operations package is explicitly experimental and outside the compatibility promise; its documentation recommends pinning a Beads version. Its unpaged map contract is documented for a small number of workspace memories. Deployment and synchronization behavior depends on backend and configuration and was not exercised.[[memory-doc]][[readme]]

## Benchmark status

**Benchmark not run.** I did not execute Beads, a benchmark workload, or tests. The project metric definitions and versioned fixture specify planned evaluations; the current execution-status record is project-wide, not a Beads result.[[metrics]][[fixture]][[status]]

## Contact-list follow-up

I checked the official pinned [README](https://github.com/gastownhall/beads/blob/78624109904655d7a4609f27d34eb0982cd8963f/README.md) and [SECURITY.md](https://github.com/gastownhall/beads/blob/78624109904655d7a4609f27d34eb0982cd8963f/SECURITY.md). The README contains no published contact email. The security policy directs vulnerability reports through GitHub private reporting and publishes no email. The JSON records `contact_email: null` with the exact checked security-policy URL.

## Sources

- [Curated roster](../data/memory-systems.json) — position, slug, listed locator, and Atlas attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/beads.md) — source attribution only.
- [Official repository](https://github.com/gastownhall/beads) — canonical repository and default branch.
- [Official main commit feed](https://github.com/gastownhall/beads/commits/main.atom) — full current head at review time.
- [Reviewed head](https://github.com/gastownhall/beads/commit/78624109904655d7a4609f27d34eb0982cd8963f)
- [README](https://github.com/gastownhall/beads/blob/78624109904655d7a4609f27d34eb0982cd8963f/README.md)
- [Security policy](https://github.com/gastownhall/beads/blob/78624109904655d7a4609f27d34eb0982cd8963f/SECURITY.md)
- [Memory plane package documentation](https://github.com/gastownhall/beads/blob/78624109904655d7a4609f27d34eb0982cd8963f/memoryops/doc.go)
- [Memory operations contract](https://github.com/gastownhall/beads/blob/78624109904655d7a4609f27d34eb0982cd8963f/memoryops/memories.go)
- [Prime command and injection controls](https://github.com/gastownhall/beads/blob/78624109904655d7a4609f27d34eb0982cd8963f/cmd/bd/prime.go)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only source review; no Beads runtime, benchmark, or tests.
