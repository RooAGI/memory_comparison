# Hestia source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 292 / Hestia / `hestia`  
**Listed repository locator:** [thefullnacho/hestia](https://github.com/thefullnacho/hestia)  
**Canonical upstream:** [thefullnacho/hestia](https://github.com/thefullnacho/hestia)  
**Default branch / reviewed head:** main / [6489389bbd1671582024cab1975434110d36bfe5](https://github.com/thefullnacho/hestia/commit/6489389bbd1671582024cab1975434110d36bfe5)  
**Review time:** 2026-11-25 22:51:40 UTC (2026-11-25 14:51:40 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists Hestia at ordinal 292, slug `hestia`, with the explicit repository locator `https://github.com/thefullnacho/hestia`. The pinned Atlas entry is recorded only as roster attribution and locator context; it is not assessment evidence. GitHub’s official repository page identifies `main` as the default branch, and its official `main.atom` feed reports current full head `6489389bbd1671582024cab1975434110d36bfe5`, updated 2026-11-24T12:38:15Z. A fresh shallow checkout resolved to the same branch and SHA. This review is pinned to that commit.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Hestia is a local-first household assistant with two distinct memory paths: Markdown soft facts/preferences and structured SQLite entities/events. Conversational memory supports direct writes and lexical recall; background extraction proposes durable facts for human approval. This is a source review, not a runtime or performance evaluation.[[readme]][[store]][[records]][[note]]

## Who and what

The official repository presents Hestia as a self-hosted household assistant application with a local-model brain and scoped tools. Its structured records store covers relational household entities and timestamped events, while the Markdown memory store holds freeform durable facts and preferences.[[readme]][[records]][[repo]]

## Architecture and data model

Soft-fact memory stores one Markdown file per record under the configured memory directory. YAML frontmatter holds an ID, type, confidence, source label, last-seen date, links, and a pinned flag; the body holds free text. The store rebuilds an `INDEX.md` listing from these files.[[store]][[config]]

A separate SQLite store represents entities, aliases, relations, and timestamped events for records such as pets, chores, wildlife, and garden history. The README treats those as distinct from soft facts and preferences. Transient home state is read from Home Assistant instead of being cached as a memory fact.[[readme]][[records]][[tool]]

For each chat turn, Hestia builds a lexical memory context from the user’s text and appends the selected records to the system prompt. The model-facing `memory` tool also exposes direct `write` and `recall` operations. The injected block carries the record ID, source label, and last-seen date.[[brain]][[store]][[tool]]

A background note-taker examines recent conversation after the foreground answer, proposes up to two durable household facts, and writes them into an inbox directory. The current memory design document labels the earlier vector/automatic-write plan as historical and points to the harness documentation for current behavior.[[note]][[design]][[harness]]

## Write, update, delete, and retrieval

**Write.** The model-facing tool accepts content and one of seven memory types. A direct write creates a slug-derived unique ID, writes the content and metadata to a Markdown file, and regenerates the index. If an ID already exists, the store appends a numeric suffix; the inspected path does not compare meanings or replace the old item.[[tool]][[store]]

**Recall.** The query and each record’s ID, body, and links are tokenized; a fixed stop-word list is removed, and matches are scored with corpus rarity and document-length normalization. A pinned flag only breaks a score tie after a relevant match. The API defaults to five results and caps requests at twenty; prompt context truncates each memory body to 1,200 characters. The inspected implementation has no semantic embedding arm.[[store]][[harness]]

**Update and correction.** The model-facing memory tool exposes no update operation, and the inspected write method always creates another record. A person with filesystem access can edit a memory file, or a new write can be added, but source inspection found no soft-fact supersession or correction history. Correction behavior and stale-value handling are therefore limited or unknown.[[tool]][[store]][[review]]

**Delete.** The model-facing memory tool has no delete operation. A person can remove a live Markdown file through filesystem access. The code inspection found no tombstone or dedicated memory-erasure workflow; deletion from backups or other copies is not established.[[tool]][[store]][[security]]

**Background proposals.** After a sufficiently substantive user turn, a model extracts possible durable facts. Deterministic filters reject system-related claims and wishes/tasks, normalize malformed model output, cap proposals at two, and deduplicate against live memory and the inbox using keyword overlap. Proposals stay outside live recall until a person acts on them.[[note]]

A person can keep a proposal as written, edit it before keeping, or discard it in the app. The CLI offers promote and discard. Promotion writes a new live record marked `reviewed` and removes the proposal; discard removes only the queued proposal. The note-taker logs failures and does not fail the conversation that already completed.[[review]][[memory_api]][[note]]

## Scope isolation

The inspected soft-fact store reads all top-level Markdown records in one configured memory directory and has no user, tenant, or household scope field. Hestia’s application is designed around shared household state; the memory code does not establish per-user isolation. The broader security policy says the brain has no built-in authentication and relies on a private-network boundary. No deployed isolation or authorization test was run.[[store]][[config]][[security]]

## Provenance and evidence

A record stores a source label and date, and injected memory context includes that label, record ID, and last-seen date. The reviewed schema does not retain a source quote, originating conversation ID, or evidence pointer. These metadata aid inspection but do not verify the truth of the memory. The recall tool’s direct response returns type and body, while prompt injection carries the additional metadata.[[store]][[tool]][[brain]]

## Efficiency and observability

The soft-fact store uses local Markdown files and computes recall by scanning the record corpus. Every write regenerates the index from all top-level memory records. This keeps the data human-readable and dependency-light, while retrieval work grows with the number and length of records; no timing or scale threshold was measured.[[store]]

The background extractor reuses the configured local model by default and supports disabling extraction or selecting another local model/server. When the backend is deferred, work can be queued in SQLite model jobs. The health endpoint reports a count of Markdown memory records, and note-taker exceptions are logged; no runtime monitoring or queue behavior was exercised.[[note]][[config]][[brain]]

The repo’s operator MCP server defaults to read-only. When writes are enabled, mutations are appended to an audit log before dispatch and are refused if the audit write fails. This is specific to the operator MCP path; it does not establish a complete audit history for all chat memory operations.[[mcp]][[security]]

## Metric-domain evidence

All project benchmark domains are **unmeasured for this Hestia review**. The [project metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define protocol and shared status, not Hestia measurements.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Lexical recall and a prompt instruction to recall saved facts are implemented; response accuracy and abstention were not scored. | Unmeasured |
| Correction accuracy and stale values | No model-facing update operation was found; correction sequences and stale-value rate were not measured. | Unmeasured |
| Deletion leakage | A person can remove a Markdown file, but no model delete operation or post-delete probe was run. | Unmeasured |
| Scope isolation | The memory directory is shared household state in the inspected code; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Context includes metadata but no retained source passage; no answer was adjudicated for support or citations. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings or probes were collected. | Unmeasured |
| Tokens, cost, and storage efficiency | Local Markdown and local-model options are documented; tokens, cost, and storage were not measured. | Unmeasured |

## Limits and unknowns

This review inspected the official README, memory design and harness documents, plus selected current store, note-taker, review, API, tool, configuration, and prompt-assembly code at the verified head. Hestia, its tests, and its benchmarks were not run.[[readme]][[design]][[harness]][[store]][[note]][[review]][[memory_api]][[tool]][[brain]]

The memory store has no tenant authorization key. The repository’s security model relies on keeping the unauthenticated brain behind a private network boundary; this review did not test deployed network rules or filesystem permissions. It also did not test whether removing a file erases copies from backups.[[store]][[security]]

The source label is not a retained quote or conversation reference. Source inspection cannot establish memory truth, paraphrase recall quality, real-world correction behavior, or full deletion guarantees. The historical design document mentions a git-versioned memory plan; current README and security documentation describe household memory data as private and gitignored, and deployment configuration was not inspected.[[store]][[note]][[design]][[readme]][[security]][[config]]

## Benchmark status

**Benchmark not run.** No Hestia runtime, tests, or benchmark workload was executed. All required quality, isolation, evidence, latency, token, cost, and storage domains remain unmeasured. Project metric definitions, fixture, and shared status record are not Hestia results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and SECURITY.md were checked for a published contact email; neither publishes one. The review does not use commit/profile metadata, inferred addresses, or third-party directories for contact information.[[readme]][[security]]

## Sources

All upstream file sources are pinned to the verified full SHA. The Atlas URL records curated roster attribution only and is not assessment evidence. See the structured record [hestia.json](../data/system-reviews/hestia.json) and the [curated roster](../data/memory-systems.json).
