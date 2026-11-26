# deja-vu

## Identity and review pin

- Catalog ordinal: 185
- System: deja-vu
- Slug: `deja-vu`
- Listed repository: https://github.com/vshulcz/deja-vu
- Roster attribution: the catalog marks this locator explicit; its pinned Atlas entry is retained for curated identity and locator attribution only ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/deja-vu.md)).
- Canonical upstream: https://github.com/vshulcz/deja-vu
- Default branch: `main`
- Reviewed full head: [76aaac6b5e4c74d51916d604bbccaf34d50eb3de](https://github.com/vshulcz/deja-vu/commit/76aaac6b5e4c74d51916d604bbccaf34d50eb3de)
- Review timestamp: 2026-11-25T10:47:26Z (UTC; 2026-11-25 02:47:26 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

deja-vu is a local Go application that indexes coding-agent transcripts already stored on a machine, then exposes session search, context recall, handoff, and recovery through a CLI/TUI, MCP server, and agent hooks. Its derived append-oriented inverted index is rebuildable; it also supports explicit local notes and curated repository notes. This is a source review, not an execution or performance assessment. ([README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md), [architecture](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md))

## Current upstream revision

GitHub identifies `main` as the default branch. The official main Atom feed reports `76aaac6b5e4c74d51916d604bbccaf34d50eb3de` as the latest commit, updated 2026-11-25T09:32:59Z; the official commit page confirms the full SHA. ([repository](https://github.com/vshulcz/deja-vu), [main commit feed](https://github.com/vshulcz/deja-vu/commits/main.atom), [reviewed commit](https://github.com/vshulcz/deja-vu/commit/76aaac6b5e4c74d51916d604bbccaf34d50eb3de))

## Who and what

The official README presents deja-vu as a local memory/search tool for coding agents, with a Go binary, CLI/TUI, MCP surface, plugins, and lifecycle hooks. Its copyright attribution names Vladislav Shulcz; that attribution alone does not establish operational ownership or support commitments. ([README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md))

## Architecture and data model

The system reads existing session stores from supported agent harnesses and parses them into a shared session/message model. The architecture guide describes a registry of source-specific parsers and deterministic ordering of parallel file parsing before index writes. Its selected inputs include JSONL, JSON, and local SQLite stores; the tool does not require a capture daemon for those existing transcripts. ([architecture: source parsers](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md))

The default derived index lives under `~/.cache/deja/index.db`. The documented format uses a length-prefixed `records.bin`, token-to-posting bucket files and overlays, session offsets, and a manifest with source state and session metadata. Rebuilds can omit replaced transcript records; dead records and postings are later compacted/zeroed. The index is a cache over source transcripts rather than their canonical store. ([architecture: index format](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md), [index implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/internal/index/index.go))

Indexed messages preserve role distinctions such as user, assistant, tool output, files, commands, edits, and summaries. Search can restrict roles, and the architecture guide says tool output, file paths, and edits are not treated as ordinary user speech by default. The README describes explicit notes in a local JSONL file and a separate `.deja/memory.jsonl` repository-note format. ([architecture](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md), [README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md))

## Write, update, delete, and retrieval

**Writes and updates.** Session memory is primarily written by the harness to its own transcript store; deja-vu indexes those records. The CLI also provides `remember`, which appends a tagged note to the local notes store by default, or to repository notes with `--repo`. The code checks write policy, applies source-side secret masking to notes, and refreshes the index unless manual indexing is enabled. Existing note identity collisions are reported instead of silently adding a duplicate. ([remember implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/cmd/deja/remember.go), [architecture: notes](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md))

Transcript rewrites are represented in the derived index as superseded/dead records and are refreshed by indexing. The reviewed `remember` path is append-oriented; an in-place edit or correction workflow for an existing local note was not established from that path. Repository notes are curated additions committed by the user and use content-derived IDs and union merging as described in the architecture guide. ([index implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/internal/index/index.go), [architecture](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md))

**Deletion.** The CLI `forget` flow supports session, project, and date selectors, dry-run/listing, and restoration of forgotten items. The inspected command performs a dry selection before destructive action, refuses ambiguous multi-session matches unless explicitly allowed, and writes exclusions that indexing applies on rebuild. The README describes forgotten sessions as permanently excluded across rebuilds. This does not establish secure erasure of original harness transcripts, backups, or every derived artifact. ([forget implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/cmd/deja/forget.go), [README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md))

**Retrieval.** Search intersects token postings and ranks sessions with lexical BM25 plus bounded signals such as decision presence, reuse, and freshness; the implementation returns snippets and match metadata rather than requiring every hit's full transcript. The README documents multi-word search, phrase handling, harness/project/time/role filters, and optional hybrid vector reranking when an embedding endpoint is configured. The architecture document describes project-first recall in hooks and broader machine history in MCP recall; CLI search is whole-store unless narrowed. ([search implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/internal/search/search.go), [architecture](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md), [README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md))

## Scope isolation

Hook and session-start recall can default to the active project; explicit project and harness selectors narrow CLI search. MCP recall prioritizes the working directory's project but can also include other machine projects. These are retrieval defaults and filters, not a tenant security boundary. Repository notes are tied to their checkout, while machine-level history and notes have broader local scope. No cross-project isolation workload was run. ([architecture](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md), [README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md))

## Provenance and evidence

Session records retain harness/session identity, source path, timestamps, roles, and message text; selected records also represent commands, touched files, and edit spans. The README describes blame/origin views that connect sessions and recorded edits to files or commits, while handoff carries task state and verification commands. Promoted decisions can carry accepted/rejected/superseded/stale lifecycle state and search can surface changed-workspace warnings. These structures aid traceability but do not require claim-level source citations or guarantee that a recorded conclusion is correct. ([architecture](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md), [README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md))

The architecture guide documents indexing-time secret redaction before records are written to the derived index and warns that disabling it is unsafe. The README describes repository notes as redacted on write and framed as untrusted when injected. Redaction is pattern-based and should not be treated as a guarantee that all secrets are detected. ([architecture](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md), [README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md))

## Efficiency and observability

The source design uses incremental indexing, append records, token buckets with overlays, offsets, compression for larger message bodies, and bounded search reads for large result sets. These choices are intended to avoid repeatedly rewriting or scanning all data. Hooks use warm indexes and bounded, best-effort context payloads; a missing or stale index is refreshed asynchronously. The README advertises speed and index-size figures, but no benchmark was run here and those claims are not results for this review. ([architecture](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md), [index implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/internal/index/index.go), [README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md))

Visible operational surfaces include CLI index/search/status commands, MCP results, hook output, source-read errors, redaction counts, and optional usage/trace data. The inspected source indicates that search reports cap/estimate and policy-withheld metadata; this review did not validate the completeness of every telemetry path or inspect production deployments. ([search implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/internal/search/search.go), [architecture](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md))

## Metric-domain evidence

All project metric domains are **unmeasured** for deja-vu. The project metric definitions, fixture, and result-status record are references only; no workload was run. ([metric definitions](../METRICS.md), [fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Search tiers and results were inspected; no answerability or abstention cases were scored. |
| Correction accuracy and stale-value rate | Unmeasured | Lifecycle labels and index replacement behavior exist; no correction probes were run. |
| Deletion leakage | Unmeasured | Forget exclusions were inspected; no post-delete probes or erasure audit was run. |
| Scope isolation | Unmeasured | Project-prioritized recall and filters exist; no forbidden-scope probes were run. |
| Evidence support and citation coverage | Unmeasured | Session/file/command lineage exists; no claim-level evidence was adjudicated. |
| Retrieval latency and write-to-recall delay | Unmeasured | No timed retrieval or write-to-recall probes were run. |
| Tokens and cost | Unmeasured | No token use, provider activity, or cost was measured. |
| Storage efficiency | Unmeasured | Index structures were inspected; no attributable storage sizes were measured. |

## Limits and unknowns

This bounded review inspected the official README, architecture and security documentation, the search/index implementations, and CLI note and forget paths. It did not inspect every source parser, harness plugin, policy configuration, embedding adapter, sync protocol, or deployment. The product spans many agent transcript formats; this review cannot establish parser correctness across all of them. ([README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md), [architecture](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md), [search implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/internal/search/search.go), [index implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/internal/index/index.go))

No runtime behavior, indexing correctness under concurrent changes, retrieval quality, deletion completeness, deployed scope isolation, latency, cost, or storage efficiency was measured. README benchmark claims are upstream statements, not this project's measured results. No deja-vu runtime, tests, or benchmarks were run. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

## Contact

The official pinned README and SECURITY.md were checked for a published contact email. Neither publishes an email; the security policy directs vulnerability reports to GitHub's private reporting path. No commit/profile metadata or third-party directory was used. ([official README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md), [official security policy](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/SECURITY.md))

## Benchmark status

**Benchmark not run.** deja-vu, its tests, and project benchmark workloads were not run. ([metric definitions](../METRICS.md), [fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/deja-vu.md)
- [Official repository](https://github.com/vshulcz/deja-vu)
- [Official main commit feed](https://github.com/vshulcz/deja-vu/commits/main.atom)
- [Reviewed full head 76aaac6b5e4c74d51916d604bbccaf34d50eb3de](https://github.com/vshulcz/deja-vu/commit/76aaac6b5e4c74d51916d604bbccaf34d50eb3de)
- [Pinned official README](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/README.md)
- [Pinned architecture guide](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/docs/ARCHITECTURE.md)
- [Pinned security policy](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/SECURITY.md)
- [Pinned search implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/internal/search/search.go)
- [Pinned index implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/internal/index/index.go)
- [Pinned remember implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/cmd/deja/remember.go)
- [Pinned forget implementation](https://github.com/vshulcz/deja-vu/blob/76aaac6b5e4c74d51916d604bbccaf34d50eb3de/cmd/deja/forget.go)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project execution status](../results/initial-baselines-status.json)
