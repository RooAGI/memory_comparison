# aigent-OS

## Identity and review pin

- **Curated ordinal:** 42 in `data/memory-systems.json`
- **Listed name / slug:** aigent-OS / `aigent-os`
- **Listed repository locator:** https://github.com/wrg32786/aigent-os
- **Canonical repository:** https://github.com/wrg32786/aigent-os
- **Default branch:** `master`
- **Reviewed head:** [`89157fba56b734b8e0a45b3e9d45966f07d11203`](https://github.com/wrg32786/aigent-os/commit/89157fba56b734b8e0a45b3e9d45966f07d11203)
- **Reviewed at:** 2026-11-24 19:58:22 UTC (11:58:22 PST, America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The curated entry supplies the ordinal, listed locator, and Atlas attribution only. The Atlas description, capability marks, and layout were not used as assessment evidence. The official repository page and `master` commit feed identified the canonical repository, default branch, and current full head.[[head](https://github.com/wrg32786/aigent-os/commit/89157fba56b734b8e0a45b3e9d45966f07d11203)]

## Summary

aigent-OS is a local Claude Code harness that manages context refresh and cross-session memory. Its README describes memory as Markdown files in a Git-backed vault, with local semantic search and checkpoint capsules. This review is a bounded source review, not an execution or quality assessment.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)]

## Who and what

The official README describes the project as an open-source MIT Claude Code harness that runs locally and provides hooks, skills, a persistent vault, and managed context refresh. It names the team behind The AIgent but does not establish an individual maintainer identity in the inspected material.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)]

## Architecture and data model

The README describes an event-hook and local-runner architecture around a Markdown/Obsidian vault. It says sessions read the vault at startup and write at checkpoints; daily notes, decisions, open threads, and capsules are among the documented memory materials. The project also describes three levels of memory (a short “napkin,” an index, and full topic files), with heat-ranked notes and a staged digest above the full files.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)]

Managed Auto-Refresh is documented as a context-pressure threshold followed by a capsule request, an exact acknowledgement, one `/clear`, a fresh session identity, and a resume prompt. The README identifies separate local components for telemetry, transport authorization, PTY writes, capsule generation, and resume. These are documented roles; this review did not trace their implementations end to end.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)]

## Write, update, delete, and retrieval

- **Write and checkpoint:** The README describes the agent writing Markdown memory and a resume-ready capsule. At a completed capsule cycle, the harness commits the memory folder and pushes it when the install directory has a Git remote. That documented sync behavior depends on the user's local Git configuration.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)]
- **Update and deletion:** The documented memory format is ordinary files, so edits and removals are file changes; Git history can provide diffs and rollback where the vault is versioned. I did not locate a dedicated memory CRUD or hard-delete API in the inspected README or current code diff. Purge behavior for indexes, backups, remotes, or provider-side data is unknown.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)]
- **Retrieval:** The README documents local semantic search over the vault using all-MiniLM-L6-v2 and says embeddings/search run on the user's machine after model files are downloaded. It also describes validity-window notes ranking below current notes and heat-ranked summaries pointing to full topic files. Search ranking, filtering, and deletion consistency were not verified in the implementation during this review.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)]
- **Code inspection boundary:** The current head's visible commit diff includes `inspectSessionLog` in `daemons/nightly-context-hygiene.mjs`. It strips a leading byte-order mark, parses one-line capsule entries and dated blocks, reports malformed entries, and checks retention count and newest-first order. This is a narrow current-code observation about session-log hygiene, not evidence that memory retrieval or capsule persistence works at runtime.[[code-diff](https://github.com/wrg32786/aigent-os/commit/89157fba56b734b8e0a45b3e9d45966f07d11203)]

## Scope isolation

The README says each aigent-OS seat has its own vault and that folders marked confidential stay out of search. This suggests per-seat and vault-path organization, but the inspected documentation does not establish a security boundary between seats or prove that every retrieval path enforces confidential-folder exclusions. Those implementation details remain unknown.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)]

## Provenance and evidence

The README describes memory as Git-tracked Markdown that can be read, diffed, and rolled back. It also documents a capsule verification and acknowledgement step before automatic clearing, and says retrieved memory is treated as data rather than instructions. The code diff confirms the session-log hygiene checker validates entry format, count, and ordering, but this inspection did not verify a complete provenance chain from source conversation through memory write to later answer.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)] [[code diff](https://github.com/wrg32786/aigent-os/commit/89157fba56b734b8e0a45b3e9d45966f07d11203)]

The official repository landing page, which renders the README, was checked for a published contact email. No address appears in the checked material; the review record stores `contact.email: null` with the exact checked URL. No commit metadata, personal profile, third-party directory, or inferred address was used.[[official repository page contact check](https://github.com/wrg32786/aigent-os)]

## Source-visible efficiency and observability

The README describes search as local and states that the model is downloaded on first use; it also says the harness has no server of its own. These are documented design claims, not measurements of query latency, memory size, token use, cost, or write-to-recall delay.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)]

The inspected code diff shows the context-hygiene checker returns a pass/fail summary with session-entry count, retention limit, malformed-entry count, newest-first status, and other checks. This is source-visible observability for that checker only; no runtime output or performance data was collected.[[code-diff](https://github.com/wrg32786/aigent-os/commit/89157fba56b734b8e0a45b3e9d45966f07d11203)]

## Limits and unknowns

GitHub's file-level source pages and unauthenticated contents API were unavailable during this review. I inspected the official repository README, current repository and commit metadata, and the current head's visible code diff for the context-hygiene checker. The memory search implementation, capture hooks, capsule writer/reader, scope filters, and purge path were not directly inspected; related claims above are labeled as README documentation. A fresh source-page review should examine those implementation paths before making stronger claims.[[README](https://github.com/wrg32786/aigent-os/blob/89157fba56b734b8e0a45b3e9d45966f07d11203/README.md)] [[head diff](https://github.com/wrg32786/aigent-os/commit/89157fba56b734b8e0a45b3e9d45966f07d11203)]

The project README reports bounded single-seat release observations for Auto-Refresh, but those are not this project's benchmark results and were not independently reproduced. No aigent-OS runtime, benchmark workload, or tests were run. The [structured review](../data/system-reviews/aigent-os.json) records `benchmark_status: not_run`; project [metric definitions](../METRICS.md), the [execution-status record](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json) remain separate.

## Sources

The structured source IDs and pinned URLs are recorded in [aigent-os.json](../data/system-reviews/aigent-os.json). The roster attribution is [the Atlas report locator](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/aigent-os.md); it was used only to identify the curated entry.
