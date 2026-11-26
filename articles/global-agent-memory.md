# Global Agent Memory source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 260 / Global Agent Memory / `global-agent-memory`  
**Listed repository locator:** [ozankasikci/global-agent-memory](https://github.com/ozankasikci/global-agent-memory)  
**Canonical upstream:** [ozankasikci/global-agent-memory](https://github.com/ozankasikci/global-agent-memory)  
**Default branch / reviewed head:** main / [53480fd2906b41c9921326f1c61e4c42fe8d5134](https://github.com/ozankasikci/global-agent-memory/commit/53480fd2906b41c9921326f1c61e4c42fe8d5134)  
**Review time:** 2026-11-25 21:05:34 UTC (2026-11-25 13:05:34 PST; America/Los_Angeles).

## Identity and review pin

The curated roster identifies Global Agent Memory as ordinal 260, slug `global-agent-memory`, with the explicit locator `https://github.com/ozankasikci/global-agent-memory`. The Atlas attribution is retained only for roster identity and locator context; it is not assessment evidence. The official GitHub repository page identifies `main` as the default branch. GitHub’s official `main.atom` feed lists full head `53480fd2906b41c9921326f1c61e4c42fe8d5134`, which matches the pinned repository content inspected here. This review is pinned to that SHA.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Global Agent Memory is a local-first memory MCP service and companion CLI/dashboard. It stores canonical notes as Markdown in an Obsidian-compatible Vault, with a rebuildable SQLite index for keyword and optional semantic retrieval. It supports project-aware context, reviewable candidate memories, and owner-controlled visibility and access. These are source and documentation observations, not quality or isolation measurements.[[readme]][[vault]][[search]][[access]]

## Who and what

The official README describes the product as shared durable memory for Claude Code, Codex, and other MCP-compatible agents. It provides an MCP interface, CLI, optional local dashboard, and Obsidian-compatible Markdown Vault. This review does not infer individual maintainer roles.[[readme]][[repo]]

## Architecture and data model

The README describes a hybrid runtime: a healthy optional local daemon can provide the shared service, while clients can fall back to the same MCP application services in-process. The documented dependency direction is transport and client adapters to application services to domain, with Vault, SQLite/index, vectors, embeddings, Git, file watching, and client integrations at adapter boundaries. The canonical store is a Vault of Markdown notes; SQLite, FTS, vectors, queues, and caches are generated state intended to be rebuildable from Markdown.[[readme]]

Managed notes carry stable memory IDs and structured metadata such as type, scope, project, lifecycle status, visibility, confidence, importance, tags, links, source references, and supersession relationships. The Vault repository code scans managed Markdown files, parses notes by immutable ID, refuses ambiguous duplicate IDs, and writes files atomically. The README distinguishes canonical notes from database-only operational or history data that needs its own backup.[[readme]][[vault]]

## Write, update, delete, and retrieval

**Write.** The documented agent flow uses `memory_remember` to propose explicitly supplied content as a candidate; candidates are not active until approved. The Vault repository exposes candidate creation and appends content-free audit events for repository mutations. The source review did not trace every write caller through the whole MCP/application stack.[[readme]][[vault]]

**Update and lifecycle.** The README documents safe updates using optimistic concurrency, so stale writes fail rather than silently overwrite newer content. Candidate memories can be approved or rejected, and memories can be superseded or archived. The Vault repository code uses atomic replacement for note writes and records event IDs, event type, memory ID, path, timestamp, and safe metadata in its append-only audit log.[[readme]][[vault]]

**Delete.** The repository implements an explicit hard-delete operation: it writes a tombstone containing the memory ID, relative path, timestamp, reason, and content hash, removes the Markdown file, and appends a hard-delete audit event. This implementation does not establish physical erasure from backups or other copies outside the inspected Vault path.[[vault]]

**Retrieval.** The README documents SQLite FTS5 keyword retrieval and optional Ollama embeddings with sqlite-vec for semantic ranking; keyword retrieval and lifecycle operations remain available without Ollama. The inspected search request supports hybrid, keyword, semantic, and metadata modes, project and scope filters, explicit cross-project access, status controls, pagination, and access grants. Results include excerpts and supporting passage/rank metadata. The sources describe ranking and access paths but do not establish their answer accuracy.[[readme]][[search]]

## Scope isolation

Project detection and project-aware retrieval are core documented behavior. Search requests carry a resolved project and explicit `cross_project` option, and the README describes protected memory grants as limited to selected memory IDs, projects, agents, permission levels, purposes, and durations. The access service requires owner-controlled grants; agents can request and poll but cannot approve, deny, or revoke them. The security policy describes the supported boundary as a single-user local service, localhost-only, with remote hosting unsupported. These controls do not substitute for adversarial isolation testing, which was not performed.[[readme]][[search]][[access]][[security]]

## Provenance and evidence

The README describes source references and supersession links on Markdown records, owner review before candidates become durable, and protected or sealed visibility modes. The security policy treats Markdown as untrusted data and documents that retrieved context is labeled accordingly to avoid promoting stored text to instructions. Repository audit records capture mutation metadata, while hard-delete tombstones retain a content hash and deletion details. These fields and controls preserve lineage or lifecycle evidence; they do not prove that a memory is true or that a generated answer is supported by it.[[readme]][[vault]][[security]]

## Efficiency and observability

The project documents a local keyword-only path, optional local Ollama embeddings, rebuildable search state, health and repair commands, and an opt-in performance suite. The inspected search implementation uses bounded keyword and semantic candidate sets and reciprocal-rank fusion; the Vault repository uses sorted file traversal and atomic writes. The README’s performance claims are upstream-reported documentation and were not reproduced in this review. No runtime telemetry, latency, write-to-recall delay, token, cost, or storage measurements were collected.[[readme]][[search]][[vault]][[metrics]]

## Metric-domain evidence

All project benchmark domains are **unmeasured in this review**. Documentation, source structure, and any upstream performance claims are not results collected here. Global Agent Memory, its tests, and benchmarks were not run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Search modes and candidate ranking were inspected; no query or abstention workload was scored. | Unmeasured |
| Correction accuracy and stale values | Optimistic update and lifecycle operations are documented; no correction workload was run. | Unmeasured |
| Deletion leakage | Explicit hard delete and tombstone behavior were inspected; no post-delete probes were run. | Unmeasured |
| Scope isolation | Project filters and protected access grants were inspected; no adversarial cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Notes retain source references and retrieval returns supporting passages; generated claims were not adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Search and indexing paths were inspected; no timings were collected. | Unmeasured |
| Tokens, cost, and storage | Local and optional embedding paths are documented; no resource measurements were collected. | Unmeasured |

## Limits and unknowns

This is a pinned source and documentation review, not a runtime, security, or quality assessment. A single-user local deployment is the stated supported boundary; this review does not establish safety for remote or multi-user operation. Candidate approval and owner grants are documented controls, but no adversarial test of prompt injection, access policy, or project isolation was run. The documented rebuild path applies to generated state; it does not show that all history, backups, or external copies are erased by deleting a note. The search code and upstream performance documentation do not establish actual recall quality, latency, resource use, or benchmark performance.[[readme]][[security]][[vault]][[search]][[metrics]]

## Benchmark status

**Benchmark not run.** No Global Agent Memory runtime, tests, or benchmark workload was executed for this review. No quality, latency, token, cost, storage, deletion, correction, evidence, or isolation result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and `SECURITY.md` were checked for a published contact email; neither lists one. The structured record stores `contact_email: null` and both exact checked URLs. No commit/profile metadata or third-party directory was used.[[readme]][[security]]

## Sources

All upstream file links below are pinned to the verified full SHA. The Atlas entry is included only for curated roster attribution, not system assessment. See the structured record [global-agent-memory.json](../data/system-reviews/global-agent-memory.json) and [curated roster](../data/memory-systems.json).
