# brain-mcp source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 99 / brain-mcp / brain-mcp  
**Listed repository locator:** [mordechaipotash/brain-mcp](https://github.com/mordechaipotash/brain-mcp)  
**Current canonical repository:** [mordechaipotash/brain-mcp](https://github.com/mordechaipotash/brain-mcp)  
**Default branch / reviewed head:** main / db1a175237cedbd26bb233c40210662d1175fc24  
**Review time:** 2026-11-24 23:56:09 UTC (15:56:09 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog places brain-mcp at ordinal 99 and lists the repository locator above. Its Atlas URL is retained for identity and attribution only; Atlas descriptions, marks, and layout were not used as assessment evidence. GitHub identifies main as the default branch. A fresh git ls-remote --symref identified refs/heads/main as remote HEAD at the full SHA shown here, and a shallow checkout resolved to the same SHA. The official repository page's latest commit prefix agrees with it. [[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/mordechaipotash/brain-mcp)] [[reviewed commit](https://github.com/mordechaipotash/brain-mcp/commit/db1a175237cedbd26bb233c40210662d1175fc24)] [[main branch feed](https://github.com/mordechaipotash/brain-mcp/commits/main.atom)] [[Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brain-mcp.md)]

## Summary

brain-mcp is a local recorder and MCP server for AI coding-agent conversations. It captures transcript bytes into an append-only file floor, builds a re-derivable DuckDB full-text index, and returns search results with file, line, and hash citations or an explicit abstention. The reviewed implementation exposes recall and health tools; it does not provide a project-scoped memory store. This is source inspection only: no runtime, benchmark, or tests were run. [[README](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/README.md)] [[MCP server](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/server.py)] [[recorder API](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/api.py)]

## Who and what

The repository is published under the GitHub account mordechaipotash; the README names brainmcp.dev and describes the package as a local-first recorder for Claude Code, Codex, and Pi history. It is a Python CLI, scheduled recorder, and stdio MCP server. The inspected official sources do not confirm a separate maintainer identity or publish a contact email. [[README](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/README.md)] [[project website](https://brainmcp.dev/)]

## Architecture and data model

**Code observation.** The local BRAIN_HOME layout separates a spool, a per-lane lake, a JSONL manifest, offsets and heartbeats, and brain.duckdb. The lake plus manifest are the durable floor; DuckDB is a disposable index. Its schema records lane configuration, source-file identity and path, visit witnesses, original line bytes/text and line hashes, and per-file ingestion offsets with prefix hashes. Raw-line identity uses file, generation, and byte offset. [[storage paths](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/paths.py)] [[DuckDB floor schema](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/floor_db.py)] [[manifest writer](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/manifest.py)]

**Code observation.** Claude Code has Stop and SessionEnd hook capture with the scanner as a backstop. Codex and Pi are polled; the scanner also mirrors Claude Code session-folder transcripts and associated files. Complete transcript lines are appended byte-for-byte to the lake before the manifest and DuckDB are updated; an incomplete trailing line waits for a later pass. Dialect views normalize Claude Code, Codex, and Pi messages into one searchable table, and the derived FTS index is rebuilt when needed. [[README](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/README.md)] [[scanner](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/scanner.py)] [[capture and generation handling](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/visit.py)] [[derived schema and refresh](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/derived.py)] [[Claude Code hooks](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/plugin/hooks/hooks.json)] [[hook stream script](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/plugin/scripts/brain-stream-on-turn.sh)]

## Write, update, delete, and retrieval

**Write and update.** Capture appends complete new lines. When an origin shrinks or its prior prefix hash changes, a new generation is started and the previous one is retained. Repeated rewrite generations are capped at five per 24 hours; the health path can report a degraded lane if the cap is hit. The MCP surface offers search, get, recent, sessions, health, capture status, and backup; it has no MCP memory write, edit, or delete tool. [[capture and generation handling](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/visit.py)] [[scanner](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/scanner.py)] [[MCP tools](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/server.py)]

**Redaction and deletion.** The CLI redact operation replaces selected lake lines with marker lines and appends the old span hash and reason to the manifest. It instructs the operator to rebuild derived data with a later record pass. Earlier backups may still contain original bytes, and retained generations are not erased. The inspected slice has no general permanent deletion or automatic floor-retention operation. [[redaction command](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/cli.py)] [[manifest writer](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/manifest.py)] [[derived refresh](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/derived.py)]

**Retrieval.** Search uses DuckDB FTS BM25, with optional agent, role, date bounds, rank threshold, and ordering. By default it excludes detected harness-injected user text and subagent transcripts; callers may opt in. Each hit includes a citation with lake path, line span, and hash. Zero hits produce an abstention with searched coverage and a warning that absence applies only to that scope. brain_get reads the requested lake lines and can compare their hash with an expected citation hash, reporting mismatches without repair. [[retrieval API](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/api.py)] [[search filters and FTS](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/derived.py)] [[MCP tool contracts](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/server.py)]

**Scope isolation.** The default store is one local corpus under one user's BRAIN_HOME. Search can narrow by agent, role, and event-time range, but its query contract has no project, tenant, or caller-identity filter. These optional content filters do not provide tenant isolation; access to local files and the MCP process is the visible boundary in the reviewed code. This is a source observation, not an isolation test. [[storage paths](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/paths.py)] [[lane and file schema](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/floor_db.py)] [[search filters](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/derived.py)] [[MCP server](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/server.py)]

**Provenance and evidence.** Ingestion records lane, agent, session key, generation, origin path, capture time, source mechanism, byte and line ranges, and SHA-256 for each chunk. Search citations point back to lake lines, and brain_get recomputes the span hash. The manifest supports receipt checks after an origin disappears. These checks establish byte correspondence to captured data, not whether transcript content is true or supports a generated conclusion. [[capture](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/visit.py)] [[manifest](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/manifest.py)] [[citation and verification API](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/api.py)]

## Metric-domain evidence

**Code observations, not measurements.** Retrieval loads DuckDB FTS and executes BM25 against the derived message table. Search has a caller-provided result limit and excerpt cap; the code supports agent/role/time filters and opt-ins for machine-injected content and subagents. The scanner skips unchanged files by recorded size; the index rebuild path is visible in the derived refresh code. No latency, recall, cost, or storage measurements were made for this review. [[FTS search](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/derived.py)] [[retrieval API](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/api.py)] [[scanner](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/scanner.py)]

**Source-visible observability.** Health compares configured origins with the local floor and uses fresh, stale, unknown, disabled, and degraded states; capture status reports spool, heartbeat, and floor information. The manifest provides capture and redaction history. Telemetry functions are no-op shims in this revision. These diagnostics do not establish production monitoring or reliability. [[health and capture API](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/api.py)] [[MCP diagnostics](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/server.py)] [[manifest](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/manifest.py)] [[telemetry shim](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/telemetry.py)]

| Domain | Source-visible evidence | Review measurement |
|---|---|---|
| Answerable recall and abstention | BM25 uses a rank threshold and explicit zero-hit abstention with coverage | Unmeasured |
| Correction and staleness | Origin rewrites open retained generations; the query index selects current-generation rows | Unmeasured |
| Deletion leakage | CLI redaction rewrites lake lines; prior backups may retain originals and index refresh is separate | Unmeasured |
| Scope isolation | Agent, role, and time filters exist; no project or tenant predicate was found | Unmeasured |
| Evidence support and citation coverage | Results identify file, lines, and SHA-256; truth and claim support are not adjudicated | Unmeasured |
| Retrieval latency and write-to-recall delay | Capture cadence and FTS rebuild paths are visible; no timings were collected | Unmeasured |
| Tokens, cost, and storage | Local file and DuckDB design is visible; no token, provider cost, or corpus storage measurement was made | Unmeasured |

The project's metric definitions and benchmark fixture specify measurement targets only; they are not brain-mcp results. [[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This review covers the README and selected storage, capture, search, health, citation, and redaction paths at one revision. It does not establish answer quality, abstention calibration, correctness of human-versus-injected-text classification, capture completeness, recovery under failures, or isolation between multiple processes or users. Redaction requires a later index refresh and does not erase old backups or retained generations. The README identifies Windows as out of scope. Runtime durability, FTS behavior on a populated corpus, latency, write-to-recall delay, token use, cost, and storage remain unmeasured. [[README](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/README.md)] [[scanner](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/scanner.py)] [[derived index](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/derived.py)] [[redaction command](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/cli.py)]

## Benchmark status

**Benchmark not run.** No brain-mcp runtime, benchmark workload, or tests were run for this review. Source structure, documentation, and historical project claims are not results from this review. See [project metric definitions](../METRICS.md), the [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).

## Sources

- [Curated roster entry](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution only.
- [Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/brain-mcp.md) — identity/locator attribution only.
- [Official repository](https://github.com/mordechaipotash/brain-mcp) — repository identity.
- [Reviewed full head](https://github.com/mordechaipotash/brain-mcp/commit/db1a175237cedbd26bb233c40210662d1175fc24) — main, verified against remote HEAD and shallow checkout.
- [README](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/README.md)
- [Storage paths](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/paths.py)
- [DuckDB floor schema](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/floor_db.py)
- [Manifest writer](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/manifest.py)
- [Capture and generation handling](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/visit.py)
- [Poll scanner](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/scanner.py)
- [Derived views, search filters and FTS](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/derived.py)
- [Retrieval, health, restore and citations](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/api.py)
- [MCP tool contract](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/server.py)
- [Redaction and restore CLI](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/recorder/cli.py)
- [Claude Code hook configuration](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/plugin/hooks/hooks.json)
- [Hook stream script](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/plugin/scripts/brain-stream-on-turn.sh)
- [Telemetry no-op shim](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/brain_mcp/telemetry.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

## Contact-list follow-up

I checked the official pinned [README](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/README.md), the official [project website](https://brainmcp.dev/), and the pinned repository [SECURITY.md](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/SECURITY.md) and [SUPPORT.md](https://github.com/mordechaipotash/brain-mcp/blob/db1a175237cedbd26bb233c40210662d1175fc24/SUPPORT.md) locations. The README and website publish no contact email, and SECURITY.md and SUPPORT.md are absent at this revision. The review record stores a null email and these exact checked source URLs.

## Verification boundary

Read-only source inspection at the reviewed full SHA. No brain-mcp runtime, benchmark, or tests were run.
