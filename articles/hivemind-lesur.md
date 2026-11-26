# Hivemind (Lesur) source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 302 / Hivemind (Lesur) / `hivemind-lesur`  
**Listed repository locator:** [Lesur-ai/hivemind](https://github.com/Lesur-ai/hivemind)  
**Canonical upstream:** [Lesur-ai/hivemind](https://github.com/Lesur-ai/hivemind)  
**Default branch / reviewed head:** main / [6b05533bdf71bf2dfeb6a50281050608e6630df3](https://github.com/Lesur-ai/hivemind/commit/6b05533bdf71bf2dfeb6a50281050608e6630df3)  
**Review time:** 2026-11-25 23:15:34 UTC (2026-11-25 15:15:34 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists Hivemind (Lesur) at ordinal 302, slug `hivemind-lesur`, with explicit locator `https://github.com/Lesur-ai/hivemind`. Its pinned Atlas attribution is recorded for curated identity and locator context only; it is not assessment evidence. The official repository page identifies `main`; GitHub's official commits API and a fresh `git ls-remote --symref` report full head `6b05533bdf71bf2dfeb6a50281050608e6630df3`. A shallow checkout resolved to the same SHA. [[catalog]][[atlas]][[repo]][[head]]

## Summary

Hivemind is a self-hosted MCP service that organizes agent memory into short-lived notes, an editable Markdown project bank, and a derived graph/vector index. SHORT captures activity, MID is the project handbook, and LONG helps discover historical context without deciding authoritative project state. This is a source review; no Hivemind runtime, tests, or benchmarks were run. [[readme]][[architecture]]

## Who and what

The official README describes Hivemind as a vendor-neutral, self-hosted MCP service for shared agent memory, and credits Christophe Lesur as the creator of Hivemind and its original memory engines. It ships a Python service, embedded graph-memory service, WAF, and maintenance tooling; agents connect through MCP. [[readme]]

## Architecture and data model

The product separates three horizons. SHORT stores timestamped Markdown note objects per space, with category, text, tags, and authenticated agent identity. MID stores project-handbook Markdown and its rules. LONG projects source documents and retained MID captures into graph entities and relations plus chunk embeddings. A `space_id` connects these tiers; LONG remains a derived discovery index. [[readme]][[architecture]][[live]][[graph]]

The engine boundaries keep the tiers distinct. SHORT notes are unique append-only objects. MID consolidation reads the rules, prior summary, selected notes, and current bank, then asks the configured model for structured file edits and note dispositions. LONG uses the embedded Graph Memory service backed by Neo4j and Qdrant, retaining source paths, hashes, and chunk context. [[live]][[consolidator]][[graph]][[vector]]

## Write, update, delete, and retrieval

**Write.** An agent uses `short_note` (legacy alias `live_note`) to append a note. Agent identity comes from the authenticated token, not a caller-supplied name. The regular integration guide recommends recording decisions, observations, questions, and work summaries as concise notes. [[live]][[live_tools]][[agent_setup]]

**Update and consolidate.** `mid_consolidate` queues asynchronous consolidation. By default it processes the caller's notes; selecting other agents' notes or all notes requires manage permission. One job runs at a time per space. The implementation validates structured edits before applying them and records operation counters; notes are deleted only after successful processing. Manager tools also support direct bank write and confirmed bank-file deletion. [[bank_tools]][[consolidator]]

**Delete.** Ordinary short-note tools expose append, read, and search, not a per-note delete. Administrative collection is a separate maintenance path. Confirmed MID deletion removes a bank file subject to the write route; it does not prove removal from backups or every derived copy. LONG has document and memory lifecycle operations, while captured MID preimages have their own retention and projection lifecycle. Space deletion is an explicit destructive operator action. [[live_tools]][[bank_tools]][[graph_tools]][[graph]][[archive]][[security]]

**Retrieval.** SHORT reads newest-first with category, agent, and time filters; text search is case-insensitive substring matching. MID can list and read bank Markdown. LONG query embeds the query and searches the graph and vector projection without a generative chat call. Graph search uses full-text matching with a `CONTAINS` fallback; vector lookup applies a memory namespace filter and validates returned payload ownership. The integration guide advises checking canonical files before acting on long-memory results. [[live]][[live_tools]][[bank_tools]][[graph_tools]][[graph]][[vector]][[agent_setup]]

## Scope isolation

Within one deployment, bearer-token permissions and space allowlists gate tool access. The official security contract is explicit: Hivemind OSS is mono-tenant, and a token's `space_ids` allowlist is not a tenant boundary. Project Mesh can coordinate one project across two paired nodes with a signed invitation and full-mesh all-ACK writes; it does not claim quorum consensus, offline CRDT merging, or multi-tenant isolation. No isolation workload was run. [[auth]][[security]][[mesh]][[architecture]]

## Provenance and evidence

SHORT records the token-derived agent identity, timestamp, category, tags, and space; Hivemind-specific provenance can enrich note reads with origin metadata. MID consolidation reports which notes were processed and how operations completed, but its model-authored text is not independently verified. LONG records document source paths, hashes, ingestion status, and section context, and preserves relation endpoints and direction. This helps trace a result to source material but does not establish that extracted claims are entailed, complete, or current. [[live]][[consolidator]][[graph]][[vector]]

## Efficiency and observability

SHORT reads and searches list objects for a space and apply filtering in application code. MID consolidation is batched and exposes asynchronous job state, queues, progress, and counters; separate spaces can progress concurrently. LONG combines graph full-text and vector retrieval with namespace-specific storage and bounded result limits. Health and audit surfaces provide operational signals, though some job and admin views are process-local diagnostics. No performance or resource measurements were collected. [[live]][[bank_tools]][[consolidator]][[graph]][[vector]][[security]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Hivemind in this review. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [baseline status record](../results/initial-baselines-status.json) are project evaluation materials, not Hivemind results. [[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | SHORT search and LONG graph/vector retrieval are implemented; no answers or abstentions were scored. | Unmeasured |
| Correction and stale values | MID supports structured edits and manager changes; no correction workload was run. | Unmeasured |
| Deletion leakage | Notes, bank files, LONG documents, and backups have separate lifecycles; no deletion/restore probes were run. | Unmeasured |
| Scope isolation | Space access checks and a mono-tenant deployment boundary are documented; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | LONG returns source context and metadata; no claim-support adjudication was performed. | Unmeasured |
| Retrieval latency and write-to-recall delay | Status and operation counters exist; no workload was timed. | Unmeasured |
| Tokens, cost, and storage efficiency | No token, cost, or corpus-attributed storage measurements were collected. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of selected official documentation and implementation paths at the verified current head. It does not exhaustively review every adapter, operator flow, or deployment configuration. Hivemind, tests, and benchmark workloads were not run. [[readme]][[architecture]][[metrics]][[status]]

The tiers have deliberately different authority. LONG is a derived retrieval index, not the source of truth for commits, rollback, membership, audit, backups, or recovery. Current project state should be checked in MID and recent SHORT notes. OSS deployments are mono-tenant, and source inspection does not establish real-world retrieval quality or customer isolation. [[architecture]][[agent_setup]][[security]]

## Benchmark status

**Benchmark not run.** No Hivemind runtime, tests, or benchmarks were executed. No project result is claimed for retrieval, correction, deletion, scope isolation, evidence support, latency, token use, cost, or storage. See the [project metrics](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), and [baseline status record](../results/initial-baselines-status.json). [[metrics]][[fixture]][[status]]

## Contact

The official pinned README and `SUPPORT.md` were checked for a published contact email; none was present. The structured record stores `contact_email: null` and the exact checked URLs. No address was inferred from commit/profile metadata or taken from a third-party directory. [[readme]][[support]]

## Sources

All upstream file links in the structured record are pinned to the verified full SHA. The Atlas link records curated roster attribution only and is excluded as assessment evidence. See the structured record [hivemind-lesur.json](../data/system-reviews/hivemind-lesur.json) and [curated roster](../data/memory-systems.json).
