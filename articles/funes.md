# funes

## Identity and review pin

- **Catalog position:** 248, “funes”; slug `funes`.
- **Listed repository:** [huggingface/funes](https://github.com/huggingface/funes); the catalog locator is explicit. The pinned Atlas entry is recorded only as roster attribution.
- **Canonical upstream:** [huggingface/funes](https://github.com/huggingface/funes), default branch `main`. The official repository page names `main`; `git ls-remote --symref` reports `HEAD -> refs/heads/main`, and the remote ref and shallow checkout agree on full current head `7b933e7f73297d2105be05f2d88b7babde118261`.
- **Reviewed:** 2026-11-25 20:44:15 UTC (2026-11-25 12:44:15 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) supplies ordinal, name, slug, listed repository, and Atlas attribution. The [pinned Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/funes.md) is used only for curated identity and locator attribution, never as assessment evidence.

## Summary

funes is a local-first, Rust command-line memory that indexes coding-agent transcripts into a Lance vector dataset. It chunks turns, keeps session and source coordinates with each passage, embeds locally, and recalls with hybrid vector and BM25 search followed by cross-encoder reranking. Optional Hugging Face Hub publishing lets multiple agents or machines share a dataset; the local index and remote dataset are append-oriented.

## Who and what

The official README presents funes as durable, searchable memory for agent coding sessions, with integrations for Claude Code, Codex, pi, and Hermes and a turns-file format for other producers. The core is a CLI and local dataset, with optional agent hooks, MCP tools, and Hub sharing; it does not provide a hosted memory service. The official security policy directs vulnerability reports to security@huggingface.co.[[README](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/README.md)] [[security policy](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/SECURITY.md)]

## Architecture and data model

An integration converts source-specific transcripts into a common turn/block shape or writes funes JSONL. Indexing renders selected blocks, splits text into chunks up to 1,200 Unicode characters with 150-character overlap, and assigns stable IDs from session, turn, block, and split coordinates. Each row stores text and its embedding together with session ID, turn UUID, sequence, timestamp, role, block type, tool name, source path, harness, working directory, and resolved repository.[[turn format](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/funes-jsonl.md)] [[chunk model](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/chunk.rs)]

The memory is a Lance dataset with a pinned embedding-model identity. It is local by default; an optional Hugging Face dataset repository holds a shared copy. Each memory uses one embedding model, so a host with a different model cannot push vectors into it. Remote reads fetch dataset files into a local cache, while embedding and reranking remain local.[[dataset implementation](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/memory/dataset.rs)] [[storage guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/storage.md)] [[README](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/README.md)]

## Write, update, delete, and retrieval

**Write and update.** Indexing reads converted session units, chunks them, resolves repository facets, and appends only IDs not already in the dataset. Re-indexing is incremental and uses persisted source signatures and chunk IDs to resume. Text rows are written before embeddings; later passes fill pending vectors. A changed turn under an already-seen chunk ID does not replace its stored text. New turns append, so corrections generally remain as additional passages rather than mutating old rows.[[index implementation](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/commands/index.rs)] [[dataset implementation](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/memory/dataset.rs)] [[index guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/index.md)]

**Delete and redaction.** The inspected CLI and docs provide no general per-session or per-row deletion operation from a memory. `funes scrub` is a specialized replacement operation: it scans reconstructed blocks for secrets, redacts safe matches or drops unsafe blocks, rewrites the dataset, rebuilds indexes, and removes older local dataset versions. It does not alter source transcripts or automatically delete an already-published remote dataset. Remote memories are append-oriented; the security guide says a compromised published secret requires rotating the credential and deleting/recreating the Hub dataset before republishing scrubbed data. Compaction merges index fragments and drops old dataset versions while retaining live rows; it is not logical memory deletion.[[push and scrub guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/push.md)] [[scrub implementation](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/commands/scrub.rs)] [[compaction guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/index.md)] [[security policy](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/SECURITY.md)]

**Retrieval.** Recall runs vector and BM25 searches per block type, combines ranks with reciprocal-rank fusion, and applies a cross-encoder reranker when the candidate pool exceeds the requested hits. Results are source passages, not generated summaries, and include a drill-down to reassemble surrounding turns. Filters include block type, role, harness, repository, and inclusive date bounds. Ranking is relevance-oriented rather than recency-oriented; users must constrain dates when they need recent answers. `funes ask` delegates a grounded answer to a configured coding agent and names the sessions it draws from.[[recall guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/recall.md)] [[recall implementation](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/commands/recall.rs)] [[ask guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/ask.md)]

**Scope isolation.** A local memory can combine sessions across installed agents and repositories. Harness and repository filters narrow retrieval but are not authorization boundaries. Sharing is controlled at the Hugging Face dataset repository by owner, visibility, and access token; public datasets can be read by anyone. A caller with local access to the dataset can inspect its indexed content. The inspected design has no row-level tenant or user ACL inside a memory.[[README](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/README.md)] [[recall guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/recall.md)] [[security policy](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/SECURITY.md)]

## Provenance and evidence

Each passage retains the session, turn UUID and sequence, timestamp, role, block and split positions, harness, working directory, source path, and repository when resolution succeeds. Recall prints the matched text and a `get` command for the originating turns; `get` reassembles split blocks. This makes a result traceable to stored transcript material, but does not establish that a transcript claim was true, that its author was authorized, or that source files still exist. `ask` can cite the sessions used for its answer.[[chunk model](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/chunk.rs)] [[recall guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/recall.md)] [[ask guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/ask.md)]

## Efficiency and observability

Indexing is designed for repeated incremental passes: stable chunk IDs deduplicate previously written rows, new text is searchable before embedding completes, and budgeted runs resume pending work. Per-turn hooks can index recent activity; optional session-boundary hooks publish it. Retrieval bounds output with a hit count and candidate pool; an oneline mode reduces returned passage text. A larger reranked candidate pool costs more work and may take seconds per call. Local compaction merges fragments and rebuilds search indexes; remote compaction can remove old versions after appends.[[index guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/index.md)] [[automation guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/automation.md)] [[recall guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/recall.md)]

`funes status` reports local indexing and embedding backlog, memory language counts, pending pushes, update availability, and secret-gate holdbacks. The README also describes an anonymous random install UUID sent with Hugging Face requests for install counts; `DO_NOT_TRACK=1` or `FUNES_NO_TELEMETRY=1` disables it. These are implementation and documentation observations, not collected operational telemetry. Storage documentation gives a model for growth, but this review measured no disk use, latency, tokens, or cost.[[push guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/push.md)] [[README](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/README.md)] [[storage guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/storage.md)]

## Metric-domain evidence

| Domain | Source evidence | Review status |
| --- | --- | --- |
| Answerable recall and abstention | Hybrid retrieval, candidate limits, and no-result output are visible in code/docs; no answerability or calibrated abstention probe was run. | Unmeasured here |
| Correction and stale values | Indexing appends new turns and deduplicates stable chunk IDs; no overwrite/correction accuracy or stale-value workload was run. | Unmeasured here |
| Deletion leakage | Secret scrub and old-version cleanup exist; arbitrary passage deletion and remote erasure are not provided by the inspected flow. No leakage probe was run. | Unmeasured here |
| Scope isolation | Repository visibility/tokens and query filters are documented; no adversarial local or remote access probe was run. | Unmeasured here |
| Evidence support and citations | Stored transcript coordinates and session citations are source-visible; factual support precision was not adjudicated. | Unmeasured here |
| Retrieval latency and write-to-recall delay | Index hooks and retrieval pipeline are source-visible; no latency distribution or end-to-end delay was measured. | Unmeasured here |
| Tokens and cost | Hit and candidate counts bound output and reranking work; no token or cost workload was measured. | Unmeasured here |
| Storage efficiency | Chunk vectors, text rows, indexes, and compaction are documented; bytes per transcript or retained fact were not measured. | Unmeasured here |
| Operational observability | Status output and progress/error messages expose backlog and push state; no live telemetry or reliability interval was collected. | Unmeasured here |

These statements are source observations only. The project metric definitions are in [METRICS.md](../METRICS.md), benchmark execution state is [results/initial-baselines-status.json](../results/initial-baselines-status.json), and the common probe fixture is [fixtures/memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json). The fixture and upstream benchmark documentation do not constitute funes results.

## Limits and unknowns

This review inspected the official repository at its verified `main` head; it did not run funes, tests, or benchmarks. It cannot establish retrieval quality, correction handling in real conversations, calibrated abstention, deletion leakage, isolation against local processes, actual storage growth, or production reliability. The append-oriented design makes stale material and removal policy important; local transcripts retain credentials as written until scrubbed, and published data requires separate Hub-side remediation. Public memory content is untrusted input and can contain prompt injection. Search language/model fit, host setup, and upstream transcript converters also affect results.[[README](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/README.md)] [[security policy](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/SECURITY.md)] [[index guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/index.md)]

## Benchmark status

**Benchmark not run.** No funes runtime, tests, or benchmark workload was run for this review. Project metric definitions and fixtures describe a protocol, not funes results. [METRICS.md](../METRICS.md) · [initial benchmark status](../results/initial-baselines-status.json) · [fixture](../fixtures/memory-benchmark-v1.json).

## Contact

The official pinned [SECURITY.md](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/SECURITY.md) publishes security@huggingface.co for vulnerability reports. The official pinned README was also checked and contains no contact email. The structured record stores the published address and exact source URL.

## Sources

- [README](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/README.md) — project, indexing, sharing, telemetry, and model policy.
- [turn format](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/funes-jsonl.md) and [chunk model](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/chunk.rs) — input and provenance fields.
- [index implementation](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/commands/index.rs), [dataset implementation](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/memory/dataset.rs), and [index guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/index.md) — incremental writes, vectors, and compaction.
- [recall implementation](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/commands/recall.rs), [recall guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/recall.md), and [ask guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/ask.md) — search, drill-down, filters, and grounded answers.
- [push guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/push.md), [scrub implementation](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/src/commands/scrub.rs), and [security policy](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/SECURITY.md) — publication gate and deletion limits.
- [automation guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/automation.md) and [storage guide](https://github.com/huggingface/funes/blob/7b933e7f73297d2105be05f2d88b7babde118261/docs/storage.md) — hooks, backlog, storage, and maintenance.
- Official [repository page](https://github.com/huggingface/funes), [main ref](https://github.com/huggingface/funes/tree/main), [commit API](https://api.github.com/repos/huggingface/funes/commits/main), and [pinned commit](https://github.com/huggingface/funes/commit/7b933e7f73297d2105be05f2d88b7babde118261) — repository identity, branch, and head.
- Project-owned [METRICS.md](../METRICS.md), [initial benchmark status](../results/initial-baselines-status.json), [fixture](../fixtures/memory-benchmark-v1.json), and [catalog](../data/memory-systems.json).
