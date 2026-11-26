# Claude Self-Reflect

## Identity and review pin

- **Catalog position:** 122, “Claude Self-Reflect”; slug `claude-self-reflect`.
- **Listed repository:** [ramakay/claude-self-reflect](https://github.com/ramakay/claude-self-reflect); catalog locator is explicit. The pinned Atlas roster entry is recorded only as identity and locator attribution.
- **Canonical upstream:** public GitHub repository `ramakay/claude-self-reflect`, default branch `main`. GitHub’s official main commit feed reported head `f2f749ce02d80ba961fd0153ae30def978eeaa74`, updated 2026-11-24 04:17:11 UTC. The GitHub repository page independently showed `main` and the matching abbreviated head `f2f749c`.
- **Reviewed:** 2026-11-25 08:02:46 UTC (2026-11-25 00:02:46 PST; America/Los_Angeles).
- **Status:** Reviewed from pinned upstream documentation and source. Benchmark not run.

## Summary

Claude Self-Reflect is a local Rust application for Claude Code that imports session transcripts into SQLite, retrieves prior work, and creates evidence-linked recaps, receipts, and stale-conclusion checks. It integrates through Claude Code hooks and an on-demand stdio MCP server; an optional daemon handles background work. The repository describes the memory store and vector search as local, while some narrative and dream features invoke the user's Claude Code account.

## Who and what

The official README describes the project as a Claude Code continuity and self-reflection layer. Its current package is a single Rust binary with embedded SQLite and no database server. It includes hooks, MCP tools, a daemon, and an optional companion interface. This review does not establish production deployments or usage beyond the repository's own descriptions.[[README](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/README.md)] [[architecture guide](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/docs-site/src/content/architecture.md)]

## Architecture and data model

The architecture guide describes JSONL transcript import into searchable chunks, local 384-dimensional FastEmbed vectors, and one SQLite database at `~/.claude-self-reflect/csr-engine.db`. It lists chunks, embeddings, reflections, enrichment state, retrieval events, and import de-duplication state; SQLite is opened behind a mutex and uses WAL for concurrent reads.[[architecture guide](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/docs-site/src/content/architecture.md)]

The inspected importer defines chunks with a conversation ID, project name, timestamp, text, message count, speaker, sequence, and sidechain label. Chunk IDs are deterministic UUIDv5 values. Import code tracks source evidence and speaker trust; its sanitizer distinguishes stored transcript chunks from derived artifacts and suppresses recognized CSR tool blocks and hook wrappers from derived material.[[import implementation](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/csr-engine/src/import/mod.rs)] [[provenance implementation](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/csr-engine/src/provenance.rs)]

The docs describe a vector index for chunks and reflections, with a newer immutable memory-mapped f16 generation for chunk vectors and HNSW for reflections. The search source also has HNSW chunk/reflection structures, generation manifests, and per-side update cursors. This is a multi-generation index path; the reviewed pages do not establish the active index mix or resource use for a particular installed database.[[architecture guide](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/docs-site/src/content/architecture.md)] [[search implementation](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/csr-engine/src/search/mod.rs)]

## Write, update, delete, and retrieval

Transcript import parses Claude Code JSONL, chunks the conversation, derives embeddings, and records provenance. The repository describes import de-duplication and layered enrichment. The README describes installation/setup hooks that import conversations and install the MCP integration; setup is consent-first.[[README](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/README.md)] [[architecture guide](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/docs-site/src/content/architecture.md)]

The hybrid-ranking module provides reciprocal-rank fusion for semantic, full-text, identifier, and other rankings, plus a dated score for keyword-only hits. The README describes MCP search over past sessions and reports dense-plus-full-text results in its own evaluation. The reviewed source pages show retrieval machinery, not accuracy or latency established by this review.[[hybrid ranking implementation](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/csr-engine/src/search/hybrid.rs)] [[README](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/README.md)]

The README documents uninstall options that preserve user data by default, purge the main data directory, or additionally purge the transcript mirror. I did not inspect every user-facing mutation or erasure route, so completeness across indexes, backups, exports, and other copies is unknown.[[README](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/README.md)]

## Scope isolation

The importer assigns a project namespace to each transcript chunk. The project-resolution code handles Claude Code's encoded project folders and recognizes certain hyphenated aliases only when the corresponding shorter project directory exists under `~/projects`. This is project-level retrieval context, not evidence of an authenticated tenant boundary. I did not inspect every tool and hook call path or run cross-project isolation probes.[[import implementation](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/csr-engine/src/import/mod.rs)] [[project resolution implementation](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/csr-engine/src/search/cross_project.rs)]

## Provenance and evidence

The provenance source defines trust tiers including external, trusted-tool, user-history, and user-confirmed, along with transcript event and chunk-span evidence. The README describes receipts that cite commits, tasks, verdicts, or corrections and says unsupported recap clauses drop out. These mechanisms provide source lineage and ranking or presentation signals; this review did not adjudicate the truth of stored claims or generated receipts.[[provenance implementation](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/csr-engine/src/provenance.rs)] [[README](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/README.md)]

## Efficiency and observability

The architecture guide describes local embeddings, batched import, a persisted vector index, retrieval telemetry, and a local SQLite store. The README discloses that some briefings, narratives, ratification, and dream operations run `claude -p` under the user's Claude Code account; its security policy cautions against using conversation data that should not be sent to Anthropic unless those features are disabled. No latency, token, cost, or storage measurement was collected here.[[architecture guide](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/docs-site/src/content/architecture.md)] [[README](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/README.md)] [[security policy](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/SECURITY.md)]

## Metric-domain evidence

- **Answerable recall and abstention:** Retrieval channels are visible in source. No independent answerable or abstention set was run.
- **Correction and staleness:** The README describes dreams that compare older conclusions with Git history and mark stale conclusions with the changing commit. No correction/staleness probes were run.
- **Deletion:** The README documents uninstall/purge controls. No deletion-leak check was run.
- **Scope isolation:** Project namespaces and alias handling appear in source. No cross-project probes were run.
- **Evidence and citations:** The README describes evidence-backed receipts and provenance records are present in source. No evidence-support adjudication was run.
- **Latency and write-to-recall delay:** Not measured in this review.
- **Tokens and cost:** Not measured in this review.
- **Storage efficiency:** Not measured in this review.

The README reports the project's own pre-registered development-history evaluations, including differing outcomes for similarity walks and hybrid dense/full-text retrieval. These are upstream-reported findings on the author's corpus, not measurements from this task; the README itself identifies external-corpus generalization and several labeled evaluation sets as open work.[[README](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/README.md)]

## Contact

The official pinned README and security policy were checked for a published contact email. No email was found. The structured record stores `contact_email: null` and the exact README URL checked. No commit or profile metadata, third-party directory, or inferred address was used.[[README](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/README.md)] [[security policy](https://github.com/ramakay/claude-self-reflect/blob/f2f749ce02d80ba961fd0153ae30def978eeaa74/SECURITY.md)]

## Limits and unknowns

This was a selected source and documentation review at the verified main head. It did not run the software, tests, or benchmarks; inspect all mutation, MCP, hook, authorization, or erasure paths; validate a live installation; or measure retrieval quality, privacy isolation, operational cost, or performance. The upstream README says evaluation is based on one operator's history and identifies external-corpus generalization, paraphrased queries, staleness cases, and labeled sets for some features as open questions.

## Benchmark status

**Benchmark not run.** No system, tests, or benchmark workloads were executed. The project metric definitions are in [METRICS.md](../METRICS.md), and shared execution status is in [initial-baselines-status.json](../results/initial-baselines-status.json). Neither was modified.

## Sources

Structured source IDs and pinned URLs are recorded in [claude-self-reflect.json](../data/system-reviews/claude-self-reflect.json). The roster attribution source is [the pinned Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/claude-self-reflect.md), used only to resolve this catalog identity and repository locator.
