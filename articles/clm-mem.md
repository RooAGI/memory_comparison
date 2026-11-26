# clm-mem

## Identity and review pin

- **Catalog position:** 130, “clm-mem”; slug `clm-mem`.
- **Listed repository:** [GentianLine/clm-mem](https://github.com/GentianLine/clm-mem); catalog locator status is explicit. The pinned Atlas roster entry is recorded only for curated identity and locator attribution.
- **Canonical upstream:** public GitHub repository `GentianLine/clm-mem`, default branch `main`. The official repository page showed latest abbreviated commit `ef9c219`; the official [main commit feed](https://github.com/GentianLine/clm-mem/commits/main.atom) identifies full head `ef9c21917137208441857eecfebc59eb6b70a17c`, updated 2026-11-24 22:22:16 UTC. The [pinned commit page](https://github.com/GentianLine/clm-mem/commit/ef9c21917137208441857eecfebc59eb6b70a17c) confirms the full SHA is on `main`.
- **Reviewed:** 2026-11-25 08:20:31 UTC (2026-11-25 00:20:31 PST; America/Los_Angeles).
- **Status:** Reviewed from pinned upstream documentation and source. Benchmark not run.

## Summary

clm-mem is a Python memory harness and optional server for OpenAI-compatible chat backends. It classifies conversation blocks as long-term, short-term, or transient and applies deterministic token-budget eviction, archiving long-term overflow for later recall. The review is source-based; no runtime or benchmark results were collected.[[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)]

## Who and what

The official README describes clm-mem as a zero-training memory harness for open chat models, usable as a library or through a proxy/server, CLI, web studio, REST, and MCP interfaces. It says the Python package has been renamed to `shatterling` while `clm-mem` remains a deprecated CLI alias in the reviewed documentation.[[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)]

## Architecture and data model

The memory unit is an in-process `Block` with an integer ID, role, content, tag (`longterm`, `shortterm`, or `transient`), turn, chat slot, pinned flag, importance, and access/freshness counters. The README says the live context is mirrored to `context.md` and `context.jsonl`; evicted long-term blocks are appended to `archive.jsonl`.[[Block model](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/blocks.py)] [[harness](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/harness.py)] [[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)]

The engine wraps a chat backend. Inline `<longterm>` and `<shortterm>` markers classify generated content as it is produced; the markers are split into separate blocks and stripped from visible output. A post-turn classifier call can label untagged blocks as long-term, short-term, or transient. The harness sequence adds input, evicts before generation, calls the model, classifies the reply, evicts again, and mirrors the resulting context.[[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)] [[tagging implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/tagging.py)] [[harness implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/harness.py)]

The serving layer treats a session as a branch with its own harness and sandbox; workspace IDs use a `ws:<name>` form. The README describes separate context and archive files per workspace. Chats inside a workspace share its memory, so chat slots divide transcript attribution rather than memory itself.[[server implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/purslane/server.py)] [[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)]

## Write, update, delete, and retrieval

Writes add user or assistant messages to the live window. Model output can be tagged inline, and an additional classifier call can label untagged blocks. A direct `remember` operation seeds a long-term block and mirrors the context files. These mechanisms rely on model classification and do not verify the truth of stored assertions.[[harness implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/harness.py)] [[tagging implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/tagging.py)]

When the context exceeds its token budget, the README describes three phases: remove transient blocks except recent-turn and pinned blocks; FIFO-evict older short-term blocks in rounds; then offload the oldest long-term blocks to the archive while leaving a pointer stub. Archive recall is described as case-insensitive substring search, and reinjection places a selected archived block back into the live window as short-term.[[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)] [[harness implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/harness.py)]

The README documents explicit session open and turn routes, workspace creation/deletion, archive search and reinjection, and session reset/delete. The session DELETE route closes and drops the session while retaining its archive on disk; workspace deletion is documented as removing workspace files. Long-term overflow is archived; short-term and transient eviction removes blocks from the live window. I did not inspect every filesystem cleanup path or verify residual copies.[[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)] [[server implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/purslane/server.py)] [[harness implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/harness.py)]

Workspace branches have separate harnesses and files, while chats within a workspace share memory. The server defines validation patterns for session and workspace IDs and exposes per-workspace REST operations. This code-level partitioning does not establish an independently tested authorization boundary or tenant isolation.[[server implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/purslane/server.py)] [[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)]

The inspected Block model includes classification and access metadata but no source-document citation or claim-origin field. The harness emits sequenced classifier and eviction events; these support operational visibility but do not establish evidence provenance for remembered assertions.[[Block model](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/blocks.py)] [[harness implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/harness.py)]

The README describes token and block counts, eviction events, snapshots, and a backend `/metrics` route. It also says the timing recorder/session metrics module is a stub not wired to the server. True incremental streaming is listed as not started; `/turns` SSE is described as replay after generation. No efficiency or resource measurements were collected.[[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)] [[metrics module](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/purslane/metrics.py)] [[server implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/purslane/server.py)]

## Metric-domain evidence

- **Answerable recall and abstention:** Archive lookup and reinjection are visible in source and documented; no answerability or abstention benchmark was run.
- **Correction and staleness:** The README lists optional supersession and decay controls; no correction or stale-value probes were run.
- **Deletion:** Session/workspace deletion and eviction are documented. No deletion-leak probe or residual-copy audit was run.
- **Scope isolation:** Workspace branches and session ID validation appear in source. No cross-workspace isolation probe was run.
- **Evidence and citations:** The inspected Block model has no claim-source citation field. No evidence-support or citation-coverage adjudication was run.
- **Latency and write-to-recall delay:** Not measured; the README says timing instrumentation is not wired.
- **Tokens and cost:** The harness enforces a token budget, but token usage and provider charges were not measured.
- **Storage efficiency:** The README names context and archive files; no storage measurement was collected.

## Contact

The official pinned README was checked for a published contact email. No email was found; the structured record stores `contact_email: null` and the exact README URL checked. No commit/profile metadata, third-party directory, or inferred address was used.[[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)]

## Limits and unknowns

The README says tag quality depends on the base model's zero-shot judgment; smaller models may omit inline markers, with a post-turn router pass as a backstop. Long-term overflow leaves pointer stubs in live context, so it notes that pathological sessions can require token-budget headroom.[[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)] [[tagging implementation](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/shatterling/engine/tagging.py)]

This is a selected source and documentation review at the verified main head. It did not run the software, tests, or benchmarks; inspect all mutation/security paths; establish live deployment behavior; or measure retrieval quality, scope isolation, latency, token use, cost, or storage. The README's embedded status line references an older short SHA than the current head verified from the official main commit feed.[[README](https://github.com/GentianLine/clm-mem/blob/ef9c21917137208441857eecfebc59eb6b70a17c/README.md)] [[main commit feed](https://github.com/GentianLine/clm-mem/commits/main.atom)]

## Benchmark status

**Benchmark not run.** No clm-mem runtime, tests, or benchmark workloads were executed. The project definitions are in [METRICS.md](../METRICS.md); shared execution status is in [initial-baselines-status.json](../results/initial-baselines-status.json). The [benchmark fixture](../fixtures/memory-benchmark-v1.json) is a planned workload, not a result.

## Sources

Structured source IDs and pinned URLs are recorded in [clm-mem.json](../data/system-reviews/clm-mem.json). The roster attribution source is [the pinned Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/clm-mem.md), used only to resolve this catalog identity and listed repository locator.
