# Hivemind (Activeloop)

**Ordinal:** 301  
**Slug:** `hivemind-activeloop`  
**Listed repository:** https://github.com/activeloopai/hivemind  
**Reviewed upstream:** https://github.com/activeloopai/hivemind/tree/main at `438796a1f243f075a45cf5ca5f0c19d8cb72432f`  
**Review time:** 2026-11-25 23:13:55 UTC (15:13:55 PST, America/Los_Angeles)  
**Status:** Reviewed from code. Benchmark not run.

## Summary

Hivemind is a multi-agent memory and trace-sharing system built around Activeloop Deeplake workspaces. It captures structured agent events, creates session summaries, mines reusable skills, and exposes data through retrieval hooks and a virtual filesystem. This assessment describes source behavior at a pinned commit; it does not measure runtime quality or establish deployment isolation.[[readme]][[architecture]][[schema]]

## Who and what

The official README identifies Activeloop as the builder and presents Hivemind as shared memory for coding agents. The TypeScript repository has a shared core plus adapters for Claude Code, Codex, Cursor, Hermes, OpenClaw, pi and other integrations.[[readme]][[architecture]]

## Architecture and data model

The central store is a Deeplake org/workspace. The `sessions` table contains JSONB agent events with an event id, session path, author, project, agent, plugin version, size and timestamps; an optional float-array column holds an event embedding. The separate `memory` table holds generated session summaries and optional summary embeddings. These are different representations with different lifecycle paths.[[schema]][[insert]][[capture]]

Capture hooks serialize prompts, tool calls and results, and assistant turns. The inspected hook redacts secret-like values before embedding and writing, then inserts a row using the event id as an idempotency key. Optional local embedding supports semantic recall; when embeddings are disabled or unavailable, capture continues without vectors.[[readme]][[capture]][[insert]][[embeddings]]

A `skills` table stores skill bodies and metadata including project key, local path, scope, author, contributors, source sessions, source agent, version and timestamps. Background workers mine recent events into reusable `SKILL.md` files; separate modules also implement rules, goals, code docs and a codebase graph.[[schema]][[skilldoc]][[architecture]]

## Write, update, delete, and retrieval

Capture writes structured event rows during supported agent sessions. Rows use stable ids and an insert guard to make retries idempotent. Background workers write AI-generated summaries periodically or at session end, and skill mining may create or merge a reusable skill from recent sessions.[[capture]][[insert]][[readme]][[skilldoc]]

Session pruning is an explicit deletion path: it deletes event rows for each selected session and then deletes that session's matching summary row. Skill updates are usually append-only version writes, with readers selecting the latest version; the inspected SkillOpt publish path writes a new team-scoped version. This does not establish erasure from backups, caches, or every local installed skill copy.[[prune]][[skills]][[skillpublish]]

The memory virtual filesystem maps stored summaries and session events to file-like paths. Grep retrieves from both tables, using lexical substring search alone when embeddings are absent, or combining lexical and semantic candidates when a query vector is available. The hybrid path ranks candidates and de-duplicates by path; per-branch limits can truncate results.[[vfs]][[grep]][[embeddings]]

Code-document retrieval is separate and filters active documents by project key, while retaining legacy documents with an empty project field. In the inspected raw-memory and session query, the SQL adds a path condition but no explicit author or project condition; the authenticated org/workspace is the broader data boundary.[[grep]][[scope]]

## Scope isolation

The README says all users in a Deeplake workspace can read its data. Workspace-level separation is the stated boundary. A nearest `.hivemind` file can route a directory tree to another authorized org/workspace, and `collect: false` opts the tree out; routing applies to reads and writes, while the token remains in local credentials.[[readme]][[scope]]

The normal memory/session search path is path-filtered but has no author or project predicate in the inspected query. The docs path does have a project predicate. I did not run cross-user or cross-project probes, so actual access enforcement beyond the configured workspace and API authorization was not verified.[[grep]][[scope]]

## Provenance and evidence

Event records include an author, session path, project, agent, plugin version, event id and timestamps. Skills additionally record source session ids, source agent, author, contributors and version, allowing a reader to trace how a shared skill was produced.[[schema]][[insert]][[skilldoc]]

These fields provide provenance metadata, not epistemic validation. The reviewed retrieval code returns matching text and metadata but does not adjudicate whether a generated summary or skill claim is supported by the source event.[[schema]][[grep]][[skilldoc]]

## Efficiency and observability

With embeddings enabled, one grep can query lexical and semantic candidates from both summary and session tables in a single combined SQL request, then de-duplicate results. The optional local embedding stack has a substantial dependency footprint and is off by default; without it, matching falls back to lexical ILIKE search. The code also reports when result caps may have truncated the set.[[grep]][[embeddings]]

Hook debug logging is opt-in through `HIVEMIND_DEBUG=1` and writes timestamped messages to `~/.deeplake/hook-debug.log`. The schema and source show event sizes, version metadata and optional vectors, but no runtime latency, cost, token, or storage-efficiency measurements were collected for this review.[[debug]][[schema]]

## Metric-domain evidence

The project defines evaluation domains and a synthetic fixture, but neither is a Hivemind result. All domains below remain unmeasured here: answerable retrieval, abstention, correction and staleness, deletion leakage, scope isolation, evidence support and citation coverage, latency, write-to-recall delay, tokens, cost, and storage efficiency.[[metrics]][[fixture]][[status]]

## Limits and unknowns

- Workspace sharing is intentional according to the README. The source review did not test account authorization or isolation across workspaces.[[readme]][[scope]]
- The inspected memory/session retrieval query has no explicit author or project filter. A path condition is present, but no isolation result was measured.[[grep]]
- Session prune deletes rows and a corresponding summary; persistence-layer backups, external exports, and already-pulled local skills were not checked.[[prune]][[skilldoc]]
- Summaries and skills are generated artifacts with provenance metadata, but correctness and source support were not adjudicated.[[schema]][[skilldoc]]
- The README reports LoCoMo performance comparisons from Activeloop's own evaluation. Those figures are upstream-reported only and were not reproduced in this review.[[readme]]

## Benchmark status

**Benchmark not run.** Hivemind, its tests, and benchmark workloads were not run. The project metrics, synthetic fixture and shared status record define evaluation protocol and execution status, not Hivemind results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README lists `hello@activeloop.ai` for teams using coding agents. The structured record stores the address and the exact pinned README URL.[[readme]]

## Sources

The catalog entry supplies the roster identity, listed repository and Atlas attribution; Atlas is retained for identity/locator context only, not assessment evidence.[[catalog]][[atlas]] Official GitHub metadata and a matching shallow checkout provide the current `main` review pin.[[repo]][[head]] All upstream file and documentation sources are pinned to the full reviewed SHA. See the structured [review record](../data/system-reviews/hivemind-activeloop.json), [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json), and [curated roster](../data/memory-systems.json).
