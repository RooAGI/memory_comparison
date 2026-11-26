# Cortex (Obelyth)

## Identity and review pin

- Catalog ordinal: 160
- System: Cortex (Obelyth)
- Slug: `obelyth-cortex`
- Listed repository: https://github.com/Obelyth/cortex
- Roster attribution: explicit repository locator. The pinned Atlas entry is retained for identity and locator attribution only; it is not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/obelyth-cortex.md)).
- Canonical upstream: https://github.com/Obelyth/cortex
- Default branch: `main`
- Reviewed full head: [65d449a3275eee51efd6ce0c275572806ee9d553](https://github.com/Obelyth/cortex/commit/65d449a3275eee51efd6ce0c275572806ee9d553)
- Review timestamp: 2026-11-25T09:37:59Z (UTC; 2026-11-25 01:37:59 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub repository metadata identifies Obelyth/cortex as public, non-fork, and defaulting to `main`. Its official main commit feed identifies full head `65d449a3275eee51efd6ce0c275572806ee9d553`, updated 2026-10-06T18:12:42Z. The official repository page, feed, full-SHA commit page, a shallow checkout, and a fresh `git ls-remote` agreed on the head. ([repository metadata](https://api.github.com/repos/Obelyth/cortex), [main history](https://github.com/Obelyth/cortex/commits/main.atom), [head commit](https://github.com/Obelyth/cortex/commit/65d449a3275eee51efd6ce0c275572806ee9d553))

## Summary

Cortex is a self-hosted memory service for private Markdown notes. A private GitHub repository is authoritative for durable notes; an MCP server exposes note reads/writes and question answering, while a protected dashboard handles inspection and operational controls. Optional Supabase/Upstash services add a rebuildable note mirror, working state, and operations history. ([README](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/README.md), [corpus loader](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/corpus.ts), [MCP tools](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/tools.ts))

## Who and what

The official README calls Cortex an AI memory system by OBELYTH and describes the public repository as a template for a user's own deployment. It is a hosted web application and MCP server, with GitHub and optional service providers behind it; the review does not infer an individual maintainer from account or commit metadata. ([README](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/README.md))

## Architecture and data model

The durable “brain” is a separate private GitHub repository of Markdown files. The code recognizes `profile.md`, `INDEX.md`, and notes under `projects/`, `notes/`, `log/`, and `history/`; `archive/` is readable by exact path but excluded from the live reader corpus and rejected for writes. YAML-like frontmatter can hold a description, tags, and optional decay/re-verification hints; descriptions and tags populate a generated routing view, while the note text remains the evidence source. ([README](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/README.md), [note policy and writes](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/brain.ts), [frontmatter/router](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/frontmatter.ts), [corpus loader](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/corpus.ts))

At request time the server resolves the configured GitHub branch head, downloads one tarball, and filters to live Markdown notes. A warm instance caches the corpus by commit SHA and shares in-flight builds. An optional Postgres mirror is reconciled against Git and used when healthy; it is documented as rebuildable and falls back to the tarball path on failure. Working notes (“bubble”), device records, and operations receipts live outside the notes repository, so the README says they require separate backup. ([corpus loader](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/corpus.ts), [mirror](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/mirror.ts), [README](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/README.md))

## Write, update, delete, and retrieval

**Writes and updates.** Trusted MCP tools can create, replace, append to, or edit a note. An edit requires the exact target passage to occur once; append/edit retry against fresh content after a Git SHA conflict. Successful note changes are Git commits, and the generated human-facing index is refreshed afterward; an index refresh failure is returned as a warning after the note commit. `brain_capture` appends a timestamped entry to a daily log. Guest access exposes proposal rather than direct commit tools, and accepted proposals are written by a trusted path. ([MCP tools](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/tools.ts), [note mutation code](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/brain.ts), [README](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/README.md))

**Delete and retention.** No note deletion tool appears in the inspected trusted or guest MCP roster. The durable note lifecycle uses replacement/edit, and `archive/` provides read-only history that can be fetched by path but is not searched as live memory. The inspected source does not establish a server-side permanent erasure API for note Git history. Working items can be updated, filed into a note, or manually aged; a read sweep ages items untouched for 14 days. The code comments state filed/aged items are retained rather than deleted. ([MCP tools](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/tools.ts), [note policy](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/brain.ts), [working state](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/bubble.ts))

**Retrieval.** `brain_context` returns a bounded profile, note router, and recent context; if the bubble is absent, empty, or failing, it expands recent logs. `brain_handoff` assembles a byte-budgeted project bundle from the project page, matching open working items, recent log mentions, and graph-selected neighboring notes, and says why each item was included. `brain_ask` narrows a question with lexical matching, sends selected note text to an allowlisted reader model, and then verifies the returned citation. Its default candidate count is 15, with a 400,000 UTF-8-byte note-body budget; “full” mode considers notes in corpus order under the same budget. `brain_corpus` supports exact paths or relevance/listing modes with an enforced reply ceiling and resumable cursors. ([MCP tools](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/tools.ts), [context and writes](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/brain.ts), [handoff](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/handoff.ts), [lexical retrieval](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/lexical.ts), [ask](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/ask.ts))

## Scope isolation

The trusted brain exposes corpus-level reads. Project selection narrows working items and project-tagged recent log entries in context/handoff, but the durable Markdown corpus itself has no universal tenant/project authorization key; a project directory or note name should not be read as an authorization boundary. The guest door is narrower: SECURITY.md says its allowed note paths are removed from the corpus before the reader runs, and its server-side answer/proposal tools have distinct credentials from trusted read/write access. ([security policy](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/SECURITY.md), [MCP tools](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/tools.ts), [context](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/brain.ts), [handoff](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/handoff.ts), [working state](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/bubble.ts))

## Provenance and evidence

Every successful durable note mutation returns a Git commit SHA. `brain_ask` gives each candidate file an opaque tag, discards any reader-invented path, and checks that the returned quote appears within one source block in the corpus at the loaded commit. The result reports the commit and source location; correction and superseded markers change the verdict wording. This proves textual presence at that revision, not that the quoted text is true or that it entails the answer. ([note mutation code](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/brain.ts), [ask](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/ask.ts), [verifier](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/verify.ts), [security policy](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/SECURITY.md))

Handoff entries carry an inclusion reason (such as the project page, an open bubble item, a log mention, or a graph edge with its evidence). These receipts explain retrieval selection; they do not constitute claim-level verification of the content. ([handoff](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/handoff.ts))

## Efficiency and observability

The code limits source loading to a single GitHub tarball request with a decompressed-size ceiling, caches by immutable SHA, deduplicates concurrent builds, and can use a reconciled Postgres mirror. Question answering uses a bounded lexical index and note pack; handoff defaults to 24,000 bytes and shortlists at most eight graph neighbors. These are implementation limits, not measured latency or quality. ([corpus loader](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/corpus.ts), [mirror](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/mirror.ts), [lexical index](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/lexical.ts), [ask](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/ask.ts), [handoff](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/handoff.ts))

Calls record tool name, surface, outcome stamp, duration, and selected answer-model/token-savings fields. The optional durable call log uses a bounded Upstash KV list; if unavailable, an in-process ring is used and the console identifies that fallback. The log intentionally omits question text, retaining only an optional keyed digest. README documents Trends views for usage, memory growth, and retrieval patterns. This inspection did not configure telemetry or collect runtime observations. ([call log](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/calls.ts), [README](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/README.md))

## Metric-domain evidence

All project benchmark domains are **unmeasured** for Cortex. This is source inspection, not a benchmark result. ([metric definitions](../METRICS.md), [benchmark fixture, not run](../fixtures/memory-benchmark-v1.json), [execution status](../results/initial-baselines-status.json))

| Domain | Status | Code observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | Ask has a reader contract, abstention protocol, lexical narrowing, and coverage; no answerability workload was run. ([ask](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/ask.ts)) |
| Correction accuracy and stale-value rate | Unmeasured | Exact edits and correction/superseded recognition exist; no correction probes were scored. ([brain](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/brain.ts), [verifier](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/verify.ts)) |
| Deletion leakage | Unmeasured | Durable deletion is not exposed in inspected tools; no post-delete or history/backup probe was run. ([tools](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/tools.ts), [metrics](../METRICS.md)) |
| Scope isolation | Unmeasured | Guest paths and project context are scoped in code/docs; no cross-scope workload was run. ([security](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/SECURITY.md), [handoff](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/handoff.ts)) |
| Evidence support and citation coverage | Unmeasured | Quotes are checked for textual presence, not entailment; no material-claim scoring was run. ([verifier](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/verify.ts), [metrics](../METRICS.md)) |
| Retrieval latency | Unmeasured | Calls have duration observations, but no latency samples were collected for this review. ([call log](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/calls.ts)) |
| Write-to-recall delay | Unmeasured | Git writes return a commit SHA; no scheduled post-write retrieval probes were run. ([brain](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/brain.ts), [metrics](../METRICS.md)) |
| Tokens and cost | Unmeasured | The call log records token-savings estimates for asks, but this review collected no provider usage or cost totals. ([call log](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/calls.ts), [metrics](../METRICS.md)) |
| Storage efficiency | Unmeasured | Notes, optional mirror, and operational stores have distinct persistence boundaries; no corpus-attributed bytes were measured. ([README](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/README.md), [metrics](../METRICS.md)) |

## Limits and unknowns

This review inspected the pinned README and security policy plus selected corpus, note, retrieval, verification, handoff, working-state, lexical-index, mirror, and call-log files. It did not inspect every route, migration, provider adapter, or deployment configuration. The source does not establish a deployment's active optional services, reader model, private corpus contents, retention configuration, backup practices, or production scope behavior. ([README](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/README.md), [corpus](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/corpus.ts), [tools](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/tools.ts), [metrics](../METRICS.md))

No Cortex runtime, tests, or benchmarks were run. This assessment does not establish recall accuracy, correction success, erasure completeness, guest-policy deployment, production isolation, end-to-end latency, cost, or storage efficiency. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status](../results/initial-baselines-status.json))

## Contact

The official pinned SECURITY.md publishes `support@obelyth.cloud` for vulnerability reports. The pinned official README was also checked. No commit/profile metadata or third-party directories were used. ([SECURITY.md](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/SECURITY.md), [README](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/README.md))

## Benchmark status

**Benchmark not run.** No Cortex system, tests, or benchmark workload was executed. The project fixture is a workload definition, not a result; the shared status record contains no Cortex measurement. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status](../results/initial-baselines-status.json))

## Sources

- [Curated catalog identity and roster attribution](../data/memory-systems.json)
- [Pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/obelyth-cortex.md)
- [Official GitHub repository metadata](https://api.github.com/repos/Obelyth/cortex)
- [Official main branch commit feed](https://github.com/Obelyth/cortex/commits/main.atom)
- [Verified full head commit](https://github.com/Obelyth/cortex/commit/65d449a3275eee51efd6ce0c275572806ee9d553)
- [Official README](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/README.md)
- [Official security policy](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/SECURITY.md)
- [Live corpus loader](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/corpus.ts)
- [Rebuildable Postgres mirror](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/mirror.ts)
- [Note and context implementation](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/brain.ts)
- [Note frontmatter and router](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/frontmatter.ts)
- [MCP tool registration and schemas](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/tools.ts)
- [Reader and retrieval implementation](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/ask.ts)
- [Quote verifier](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/verify.ts)
- [Project handoff assembly](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/handoff.ts)
- [Working-state store](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/bubble.ts)
- [Lexical index](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/lexical.ts)
- [Call log and operational observations](https://github.com/Obelyth/cortex/blob/65d449a3275eee51efd6ce0c275572806ee9d553/lib/calls.ts)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
