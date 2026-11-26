# Demarkus — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 186 — Demarkus / `demarkus`  
**Listed repository:** [latebit-io/demarkus](https://github.com/latebit-io/demarkus)  
**Canonical upstream:** same repository; default branch `main`; reviewed head [4bb6352f32f89e79c1ed24703e11723ba4f79b4e](https://github.com/latebit-io/demarkus/commit/4bb6352f32f89e79c1ed24703e11723ba4f79b4e)  
**Review time:** 2026-11-25 10:55:54 UTC (2026-11-25 02:55:54 PST; America/Los_Angeles)

## Identity and scope

The curated catalog lists Demarkus at ordinal 186, slug `demarkus`, with an explicit repository locator. Its pinned Atlas entry is retained only for roster identity and locator attribution; it is not evidence for this assessment.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/demarkus.md)]

The official GitHub repository identifies `main` as the default branch. Its official main commit feed reported head `4bb6352f32f89e79c1ed24703e11723ba4f79b4e`, updated 2026-11-24T20:30:48Z; read-only `git ls-remote` independently resolved HEAD and `refs/heads/main` to the same SHA. The shallow checkout used for source inspection also resolved to that commit.[[repository](https://github.com/latebit-io/demarkus)] [[main commit feed](https://github.com/latebit-io/demarkus/commits/main.atom)] [[reviewed head](https://github.com/latebit-io/demarkus/commit/4bb6352f32f89e79c1ed24703e11723ba4f79b4e)]

## Summary and architecture

Demarkus presents personal agent memory, shared team knowledge, and a graph over Markdown documents, built on the Mark Protocol. The repository describes a protocol module, server, clients, knowledge service, tools, plugins, and deployment assets. The upstream README labels the project beta and pre-1.0, and warns that features and components are in flux.[[README](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/README.md)] [[architecture](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/site/architecture/index.md)]

The Mark Protocol transports Markdown documents over QUIC. The filesystem server stores immutable version files and a current pointer; the knowledge product adds OIDC/MCP gateways and worlds backed by storage such as GCS. Clients provide CLI, terminal UI, and MCP interfaces.[[architecture](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/site/architecture/index.md)] [[README](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/README.md)]

A stored document contains body text, modification time, version, archive state, publisher metadata, ETag, and an optional retention-prune result. The filesystem writer creates a new version rather than modifying the prior one. A previous-hash chain links versions. The lookup catalog is derived from document metadata and section indexes; it does not retain full bodies in the catalog itself.[[document model](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/protocol/storefmt/model.go)] [[versioned writer](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/write.go)] [[lookup catalog](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/catalog/catalog.go)]

Markdown links become graph edges; `rel-<predicate>` metadata adds typed relations. Project docs describe lookup, explore, backlinks, and graph traversal tools for following those links.[[graph guide](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/site/graph/index.md)]

## Write, update, delete, and retrieval

**Write.** PUBLISH validates document content and commits a new immutable version. APPEND joins content to the current body and merges metadata with request values taking precedence. The request handler applies capability authorization and the write policy before committing; expected-version checks allow callers to reject a write if another version has landed first.[[writer](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/write.go)] [[metadata rules](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/protocol/storefmt/meta.go)] [[write handler](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/handler/write.go)]

**Update and correction.** Corrections are new versions, so retained history remains addressable with VERSIONS and version-pinned FETCH. The store can verify the hash chain. A write may report that the current pointer was updated but its directory sync failed, so an error does not always mean the new content was not committed.[[read and version history](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/read.go)] [[document model](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/protocol/storefmt/model.go)] [[writer](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/write.go)]

**Delete and archive.** ARCHIVE makes a document unavailable to ordinary current reads while keeping its history; publishing can restore it. Positive `retention` metadata is a distinct destructive mechanism that prunes older versions, keeping only the newest N. The filesystem writer returns the pruned range or error, and operational logs audit prune outcomes.[[archive path](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/archive.go)] [[metadata rules](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/protocol/storefmt/meta.go)] [[writer](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/write.go)] [[observability](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/deployment/observability.md)]

**Retrieval.** The memory guide describes fetching a document or section and lookup by tags/title or body. Code also supports a near-duplicate lookup mode. Body lookup ranks matching sections with BM25-style scoring and an importance prior; snippets are bounded. A budget may include related documents, while graph tools navigate links and typed relations.[[memory guide](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/site/memory/index.md)] [[catalog](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/catalog/catalog.go)] [[body lookup](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/catalog/bodymatch.go)] [[graph guide](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/site/graph/index.md)]

## Scope isolation

Local plugins share a machine-level `~/.demarkus` memory store; project resolution assigns paths using repository/worktree context. At the protocol layer, tokens grant operations over path patterns. Paths not matched by any read token are public, so local privacy depends on the store and its read-auth configuration. In hosted memory mode, the broker maps a verified person to one world and checks each world-bearing tool URL against that tenant, denying unclassified tools or cross-world access.[[memory guide](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/site/memory/index.md)] [[capability authorization](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/auth/auth.go)] [[hosted tenant gate](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/knowledge/internal/broker/gateway/mcp_tenant.go)]

These are different scope boundaries: project-root organization on a shared local store, path-token authorization at a protocol server, and identity-to-world isolation in the hosted memory broker. Inspection of those paths does not establish every adapter or deployment configuration behaves identically.[[README](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/README.md)] [[tenant gate](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/knowledge/internal/broker/gateway/mcp_tenant.go)]

## Provenance and evidence

The version hash chain and version listing give document-history integrity information. Publisher metadata can contain agent attribution and `rel-based-on` source references; for identity-bearing grants, the handler stamps the verified user rather than trusting a request-supplied user value. Server logs record write and archive outcomes. These mechanisms improve traceability, but they do not show that generated answer claims are supported by their cited notes.[[versioned writer](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/write.go)] [[user stamping](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/handler/meta.go)] [[provenance pins](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/protocol/provenance/provenance.go)] [[observability](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/deployment/observability.md)]

## Efficiency and observability

Lookup uses in-memory metadata and section indexes derived from stored documents; it does not read every body for metadata-only queries. Body mode returns selected sections with bounded snippets. These are implementation choices, not performance measurements.[[lookup catalog](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/catalog/catalog.go)] [[body lookup](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/catalog/bodymatch.go)]

The observability guide describes structured request logs, write/archive audit records, durations, and chain-verification failures. It states that the software does not embed a metrics endpoint or tracing SDK; operators can derive metrics from logs. No latency, token, cost, or storage measurements were collected for this review.[[observability](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/deployment/observability.md)]

## Metric-domain evidence

All project metric domains remain unmeasured. See the [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).

- **Answerable retrieval accuracy and abstention — unmeasured.** Lookup paths were inspected, but no adjudicated answerability or abstention workload was run.[[catalog](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/catalog/catalog.go)] [[metrics](../METRICS.md)]
- **Correction accuracy and stale-value rate — unmeasured.** Immutable versioning and expected-version conflict checks exist; no correction probes were run.[[writer](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/write.go)] [[metrics](../METRICS.md)]
- **Deletion leakage — unmeasured.** Archive and retention paths were inspected; no post-deletion probes across history, indexes, backups, or hosted copies were performed.[[archive](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/archive.go)] [[writer](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/write.go)] [[metrics](../METRICS.md)]
- **Scope isolation leak rate — unmeasured.** Capability path checks and hosted tenant gating are visible; no adversarial cross-path or cross-world workload was run.[[auth](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/auth/auth.go)] [[tenant gate](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/knowledge/internal/broker/gateway/mcp_tenant.go)] [[metrics](../METRICS.md)]
- **Evidence support precision and citation coverage — unmeasured.** Hash chains and source pins aid provenance, but answer evidence was not adjudicated.[[provenance](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/protocol/provenance/provenance.go)] [[metrics](../METRICS.md)]
- **Retrieval latency — unmeasured.** No timing distribution was collected.[[metrics](../METRICS.md)] [[observability](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/deployment/observability.md)]
- **Write-to-recall delay — unmeasured.** No timed write-then-recall workload was run.[[fixture](../fixtures/memory-benchmark-v1.json)] [[metrics](../METRICS.md)]
- **Tokens and cost — unmeasured.** No provider usage or monetary cost was collected.[[metrics](../METRICS.md)]
- **Storage efficiency — unmeasured.** Storage/version layout was inspected, but no corpus-size or per-item measurement was made.[[writer](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/store/write.go)] [[metrics](../METRICS.md)]

## Limits and unknowns

The inspected paths do not cover every plugin, transport verb, deployment backend, or error path end to end. The README marks the project beta/pre-1.0 and says interfaces can change. The memory guide notes hosted memory does not yet have self-service export. The capability-auth source lists replay-window validation, per-document ACLs, and public-server rate limiting as TODOs; these implementation comments are not a complete security assessment.[[README](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/README.md)] [[memory guide](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/docs/site/memory/index.md)] [[capability authorization](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/server/internal/auth/auth.go)]

Source inspection cannot establish retrieval accuracy, correction/stale-value rates, full erasure across copies, hostile-caller isolation, operational reliability, or performance. No Demarkus runtime, tests, or benchmarks were run; all metric domains above are unmeasured.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Contact

The official pinned README and official website homepage were checked for a published contact email. Neither published one. No commit/profile metadata or third-party directory was used.[[README](https://github.com/latebit-io/demarkus/blob/4bb6352f32f89e79c1ed24703e11723ba4f79b4e/README.md)] [[official website](https://www.demarkus.io/)]

## Benchmark status

**Benchmark not run.** No Demarkus runtime, tests, or benchmarks were run for this source review. Source observations and upstream documentation are not project benchmark results. See [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [result status](../results/initial-baselines-status.json).
