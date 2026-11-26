# Brigade

## Identity and review pin

- **System:** Brigade
- **Curated position:** 103
- **Slug:** `brigade`
- **Listed repository:** [escoffier-labs/brigade](https://github.com/escoffier-labs/brigade)
- **Canonical repository at review:** [escoffier-labs/brigadestack](https://github.com/escoffier-labs/brigadestack)
- **Default branch:** `main`
- **Reviewed head:** [`126cb1270e868613a4caa8814e44f3f0777af9d5`](https://github.com/escoffier-labs/brigadestack/commit/126cb1270e868613a4caa8814e44f3f0777af9d5)
- **Reviewed:** 2026-11-25 00:14:02 UTC (2026-11-24 16:14:02 PST, America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brigade.md), used only for identity and source attribution.

The curated roster identifies Brigade, slug `brigade`, and the listed repository URL; that locator currently resolves to the BrigadeStack repository. Atlas content, marks, and layout were not used as assessment evidence.[[catalog]][[atlas]][[repo]] The official repository page identifies `main`; its latest commit prefix `126cb12` matches the full SHA on the official commit patch.[[repo]][[head-feed]][[head]]

## Summary

BrigadeStack is an agent-workspace CLI whose memory surfaces include repository Markdown cards, handoffs that pass through an ingester, deterministic local search, bounded session-start recall, and optional hub synchronization. The README describes session-start recall for Claude Code and inbox-plus-search access for Codex; its MCP server exposes card reads and a handoff writer that drafts proposals rather than editing canonical cards.[[readme]][[mcp]][[hooks]]

A separate optional Obsidian-vault interface indexes configured roots and stages additive proposals into an allowlisted inbox. It uses its own derived index and lexical search; its limits and trust labeling should not be conflated with the repository-card search path.[[vault]]

## Who and what

The README identifies Escoffier Labs and presents BrigadeStack as a CLI for shared agent memory, handoffs, MCP servers and skills, and work verification. The memory implementation reviewed here centers on Markdown cards and handoff ingestion; the separately inspected vault module is optional.[[readme]][[repo]][[overview]]

## Architecture and data model

**Repository cards and handoffs.** The README describes Markdown cards under the repository memory tree, shared by commits. The overview describes cards with YAML frontmatter (topic, category, tags, created/updated fields) and an opaque stable card ID, while `MEMORY.md` is a one-line index loaded at session start. Writer harnesses draft handoffs; the memory owner or reviewer ingests eligible changes into cards.[[readme]][[overview]][[care]][[ingest]]

**Search and recall.** Local search builds a plain BM25 index from card title, tags, summary, and searchable body for each call, with no persistent index. Session-start recall runs in a child process, caps output to five matches/ten lines, and has a five-second search deadline; prompt text is passed over stdin rather than saved in the recall path.[[care]][[memory-cmd]][[bm25]][[hooks]]

**Other storage surfaces.** The memory MCP tool contract resolves repository and user stores and supports read-only listing/search/get plus `write_handoff`; the latter writes a draft and never changes a canonical card. Optional hub synchronization can make cards available across machines. The Obsidian vault module instead stores an owner-readable derived index at `.brigade/vault-index/index.json` and stages additive proposals under `.brigade/vault-propose`.[[mcp]][[readme]][[vault]]

## Write, update, delete, and retrieval

**Create and update.** An agent-facing MCP `write_handoff` creates a draft in the repo or user inbox and labels `create-card`/`update-card` as proposals. The ingester validates card structure and destination, screens untrusted content, and publishes eligible create/update actions through a bounded file-write path. `create-card` may reinforce a known fact rather than create a near-duplicate; `update-card` uses replacement semantics and can require an expected SHA so stale proposals do not silently replace a changed card. This is a gated workflow, not direct MCP card mutation.[[mcp]][[ingest]][[overview]]

**Search and recall.** `memory search` returns paths, stable card IDs/aliases, title/tags/summary, and BM25 score; archived cards are excluded by default. Session recall accepts explicit or prompt terms, then falls back to checkout or folder terms, returns titles/tags/paths rather than bodies, and fails open with empty output on errors. The optional hub path can fuse scoped remote results with local cards.[[care]][[memory-cmd]][[bm25]][[hooks]][[readme]]

**Retirement and vault proposals.** Memory-care can move eligible cards into an archive and journal the change with before-bytes for undo; archived cards leave ordinary search. Automatic unused-card retirement is documented as disabled pending hub read coverage. This is reversible archival, not hard deletion. Separately, the vault module only proposes additive note delivery, refuses overwrites and unsafe symlink traversal, and checks for a committed projection receipt; it does not provide vault-note update or delete.[[care]][[vault]]

## Scope isolation

The MCP contract distinguishes repository and user stores (and allows `repo`, `user`, or `all` reads); an unwired workspace falls back to the user store. Repository cards are scoped by the selected target and may be shared through Git or a configured hub. Vault search can filter by a configured root scope, and safe path handling constrains its proposal inbox.[[mcp]][[readme]][[vault]]

These are store and path boundaries, not proof of tenant authorization or cross-user isolation. The inspected MCP contract derives stores from local target/context and does not establish a server-side identity boundary for all deployments or adapters.[[mcp]][[vault]]

## Provenance and evidence

Cards can carry stable IDs, metadata, freshness fields, fingerprints and optional evidence references; handoff writers can include facts/evidence, and updates may bind to an expected content SHA. These fields and gates make records identifiable and changes reviewable, but do not independently establish truth or claim-level support. The vault search result gives a scoped path/snippet; show includes content hash and labels the note untrusted, while proposal receipts report operation state.[[care]][[mcp]][[ingest]][[vault]]

The official security policy publishes `me@solomonneas.dev` for vulnerability reports. This is recorded as an official contact listing, not as evidence about system security performance.[[security]]

## Source-visible efficiency and observability

**Code observations, not measurements.** Card search reads the target’s cards and rebuilds an in-memory BM25 index for each query; the source sets `k1=1.2` and `b=0.75`, deduplicates query terms, and breaks equal scores by path. Recall is separately bounded to five matches/ten output lines and a five-second child-process deadline. Search logs are capped at 500 records and retain card IDs; explicit CLI queries are logged, while prompt recall stores a keyed query digest. These are implementation bounds and data-retention choices, not measured latency, cost, or accuracy.[[care]][[memory-cmd]][[bm25]][[hooks]]

The memory-care status command summarizes search counts and a rolling follow-up signal; docs call this second-class evidence that does not determine doctor/valid status. Vault output includes scope counts, result scores, note hashes, trust labels, diagnostics and proposal receipts. Work verification records commands, exit codes, logs and a tree fingerprint, but these are not memory retrieval measurements.[[care]][[vault]][[readme]]

## Metric-domain evidence

All domains below are **unmeasured in this review**. The table records source observations only. Project metric definitions, fixture, and execution status are separate from Brigade measurements.[[metrics]][[fixture]][[status]]

| Domain | Source observation | Measurement status |
|---|---|---|
| Answerable recall and abstention | Repository cards use BM25 search and session recall; the vault has separate lexical search. No adjudicated answerability probes were run. | Unmeasured |
| Correction accuracy and stale values | Ingest supports expected-SHA-guarded card replacement, and care changes can be undone. No correction or stale-value evaluation was run. | Unmeasured |
| Deletion leakage | Memory-care archives cards and records undo state; hard deletion and erasure from Git history/clones were not evaluated. | Unmeasured |
| Scope isolation | MCP resolves repo/user stores and the vault supports named root scopes. No cross-project or cross-user isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Cards can retain evidence references and recall returns card locators; no answer-support adjudication was run. | Unmeasured |
| Latency and write-to-recall delay | Local index, lexical scores, and repository commits are source-visible. No timing or propagation workload was run. | Unmeasured |
| Tokens, cost, and storage | The system uses Markdown cards and a derived JSON index; no token, provider-cost, or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This is a bounded review of the official README and overview, memory-care guide, selected card search/recall/MCP/ingestion code, vault module and security policy at one verified commit. It does not establish runtime behavior, retrieval accuracy, prompt token cost, fault durability, concurrency safety, or practical scaling. Not every memory command or agent adapter was inspected.[[head]][[readme]][[overview]][[care]][[memory-cmd]][[hooks]][[mcp]][[ingest]][[vault]]

Repo/user stores, named vault roots and safe proposal delivery do not by themselves establish authorization or tenant isolation. Archiving is not complete erasure across Git history, existing clones, backups, or downstream agent contexts.[[mcp]][[vault]][[care]][[readme]]

## Benchmark status

**Benchmark not run.** No BrigadeStack system, benchmark workload, or tests were executed. Source observations above are not measurements. The [project metric definitions](../METRICS.md), [planned fixture](../fixtures/memory-benchmark-v1.json), and [execution-status record](../results/initial-baselines-status.json) describe project-wide evaluation artifacts, not Brigade results.[[metrics]][[fixture]][[status]]

## Contact-list follow-up

I checked the official pinned [README](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/README.md), [SECURITY.md](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/SECURITY.md), and [MAINTAINERS.md](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/MAINTAINERS.md). The README points to Discussions but does not publish an email; SECURITY.md publishes `me@solomonneas.dev` for vulnerability reports, and MAINTAINERS.md lists it as the project email. The JSON records the email and exact security-policy source URL.[[readme]][[security]][[maintainers]]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed repository and Atlas attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brigade.md) — identity and source attribution only.
- [Canonical repository](https://github.com/escoffier-labs/brigadestack) — current repository identity and default-branch view.
- [Official main commit feed](https://github.com/escoffier-labs/brigadestack/commits/main.atom) — latest abbreviated main commit observed at review.
- [Reviewed head commit](https://github.com/escoffier-labs/brigadestack/commit/126cb1270e868613a4caa8814e44f3f0777af9d5)
- [README at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/README.md)
- [Memory vault implementation at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/src/brigade/memory_vault.py)
- [Overview and memory architecture at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/docs/overview.md)
- [Memory lifecycle and retrieval documentation at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/docs/memory-care.md)
- [Card search and recall dispatch at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/src/brigade/memory_cmd.py)
- [BM25 implementation at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/src/brigade/memory_bm25.py)
- [Session recall implementation at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/src/brigade/memory_hooks.py)
- [MCP memory contract at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/src/brigade/memory_mcp_core.py)
- [Handoff ingestion at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/src/brigade/ingest.py)
- [Official maintainer contact at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/MAINTAINERS.md)
- [Security policy at reviewed SHA](https://github.com/escoffier-labs/brigadestack/blob/126cb1270e868613a4caa8814e44f3f0777af9d5/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only source review at the pinned revision; no runtime, benchmark, or tests were run.
