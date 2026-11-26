# Engram source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 221 / Engram / `engram`  
**Listed repository locator:** [Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram)  
**Canonical upstream:** [Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram)  
**Default branch / reviewed head:** main / [11521f4f3776db6d94dc17c11731bad35b71c7bc](https://github.com/Gentleman-Programming/engram/commit/11521f4f3776db6d94dc17c11731bad35b71c7bc)  
**Review time:** 2026-11-25 19:18:02 UTC (2026-11-25 11:18:02 PST; America/Los_Angeles).

## Identity and review pin

The project catalog lists Engram at ordinal 221, slug `engram`, and gives the explicit repository locator `https://github.com/Gentleman-Programming/engram`. Its pinned Agent Memory Atlas entry is recorded only as roster attribution. Atlas descriptions and capability marks were not used as assessment evidence. The official GitHub repository page shows `main`; its current commit list identifies the latest commit, and the official commit patch supplies the full head SHA and commit date. The review is pinned to that SHA; the review timestamp above is when the repository and sources were checked.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Engram is a Go application that provides persistent memory for coding agents through MCP, local HTTP, CLI, and TUI interfaces. Its default store is a local SQLite database with FTS5; optional Git export and cloud replication support portability and sharing. The repository describes memory as deliberately curated by the agent rather than a raw tool-call transcript. The implementation and documentation support source-level behavior claims, but this review did not run Engram or measure its quality or resource use.[[readme]][[architecture]]

## Who and what

The upstream README identifies Alan Buscaglia (Gentleman Programming) as the builder and describes Engram as a standalone memory layer used by Gentle-AI. This is a software repository with a local-first Go runtime and optional cloud service, not a hosted-only memory API. No contact email was published in the official pinned README; the structured record stores null and the exact checked URL.[[readme]][[repo]]

## Architecture and data model

The README describes the common path as an agent using MCP stdio to a single Go binary backed by SQLite and FTS5. The architecture guide maps core responsibilities to the store, MCP server, HTTP server, project resolver, Git sync, optional Postgres cloud service, and terminal UI. Local SQLite remains authoritative when cloud replication is enabled.[[readme]][[architecture]][[store]]

The store represents observations with content and metadata such as title, type, project, scope, topic key, pin/review state, and revision counters. It also stores sessions, captured prompts, relation records, and sync state. A topic key identifies an evolving item within project and scope; it is an application key, not a hierarchical graph path. Full search results can be progressively opened through timeline and get-observation operations.[[architecture]][[store]]

## Write, update, delete, and retrieval

**Write and update.** Agents are expected to call `mem_save` for selected durable knowledge. A save with a topic key updates the matching project/scope/topic item; ordinary saves use duplicate detection and update duplicate metadata rather than always inserting another row. User-visible content changes preserve a prior observation version. The HTTP managed-runtime update path additionally binds edits to a live attachment and operation ID, commits the edit and retry receipt together, and rejects project changes. These behaviors are code/documentation observations, not runtime measurements.[[architecture]][[store]][[managed-update]]

**Delete.** `mem_delete` soft-deletes by default; hard delete is an explicit option. Soft-deleted observations are excluded from search, context, recent lists, and timeline while their IDs remain available in the local store. The repository documents replication and delete-tombstone handling, but this review did not exercise local or cloud deletion, restoration, or copy cleanup.[[architecture]][[store]]

**Retrieval.** Search uses FTS5 and returns compact previews with stable IDs and lifecycle metadata; the intended workflow is search, inspect surrounding session history with timeline when useful, then fetch the full observation. Context and project-aware read paths resolve a project from an explicit selector, `ENGRAM_PROJECT`, or working-directory detection. CLI `--all` and HTTP `all_projects=true` intentionally widen a read. Search results are candidates; the reviewed source does not establish answer accuracy or calibrated abstention.[[readme]][[architecture]][[search]]

## Scope isolation

Project and scope are stored on observations, and topic-key upserts are separated by both fields. Reads resolve a project by explicit selection, environment override, or cwd detection; global reads require an explicit all-project option. This is an application-level boundary with intentional widening controls. The documented ID-based observation fetch is a direct lookup, so callers should not treat it as equivalent to a project-filtered search. No hostile-tenant security claim or cross-scope runtime isolation result was established here.[[readme]][[architecture]][[store]]

## Provenance and evidence

The code keeps local project-capture provenance separately from routing and ownership: its type comment explicitly says capture evidence is not an ownership or enrollment grant. Observation relations and supersession metadata carry structured links between records, and the search projection may annotate compact results with those relations. These facilities record context and relationships; they do not independently establish that a memory claim is true or provide source citations for generated answers. Imported or older records can lack capture provenance.[[capture-provenance]][[observation-provenance]][[search]]

## Efficiency and observability

The single-binary local path avoids requiring a separate database service; FTS5 supports full-text lookup. Compact search previews and progressive retrieval reduce the amount of memory text returned at once. The repository also documents a read-only `doctor` diagnostic and optional timing/diagnostic paths. Those design choices do not establish latency, token savings, storage efficiency, or operational reliability: this review collected no workload measurements.[[readme]][[architecture]][[search]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Engram in this review. Source code and documentation are not benchmark results. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the evaluation protocol and shared project status, not Engram results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Search, context, and progressive disclosure are documented; no answers were scored. | Unmeasured |
| Correction and stale values | Topic upserts, update paths, and revision history are present; no correction sequence was assessed. | Unmeasured |
| Deletion leakage | Soft/hard delete paths are documented; no post-delete probe or cloud-copy audit was run. | Unmeasured |
| Scope isolation | Project/scope selectors and widening controls are documented; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Relations and capture provenance are stored; no answer evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timings were collected. | Unmeasured |
| Tokens, cost, and storage | No workload, token, charge, or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the official README, architecture documentation, and selected store source at the verified head. It did not run the service, tests, or benchmarks. Code presence does not show that an agent chooses useful facts to save or that retrieval returns correct and appropriately qualified answers. The review also did not test concurrent writers, sync conflict outcomes, account-level authorization, backup/restore, or deletion across replicated copies.[[readme]][[architecture]][[store]][[managed-update]]

The docs describe review dates as prompts for human/agent review rather than empirically calibrated expiration. Global read options intentionally broaden scope; local HTTP routes have optional bearer authentication by default, so deployment configuration matters. Whether these controls meet a particular deployment's isolation or threat model remains unassessed.[[architecture]]

## Benchmark status

**Benchmark not run.** No Engram runtime, tests, or benchmark workload was executed. No recall, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json); these describe the project protocol and status, not Engram measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email and none was present. The record stores `contact_email: null` and the checked URL. No address was inferred from commit/profile metadata or obtained from a third-party directory.[[readme]]

## Sources

Repository citations are pinned to the verified full SHA except the repository identity page, head patch, and Atlas roster attribution. The Atlas source is used only to identify the curated listing. See the structured record [engram.json](../data/system-reviews/engram.json) and [curated roster](../data/memory-systems.json).
