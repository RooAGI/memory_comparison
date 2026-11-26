# ECC

## Identity and review pin

- Catalog ordinal: 206
- System: ECC
- Slug: `ecc`
- Listed repository: https://github.com/affaan-m/ECC
- Roster attribution: explicit repository locator; the pinned Atlas entry is retained for curated identity and locator context only ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ecc.md)).
- Canonical upstream: https://github.com/affaan-m/ECC
- Default branch: `main`
- Reviewed full head: [4adeee6732a12d1540f49a4d50a38ce8c97f9a53](https://github.com/affaan-m/ECC/commit/4adeee6732a12d1540f49a4d50a38ce8c97f9a53)
- Review timestamp: 2026-11-25T11:58:45Z (UTC; 2026-11-25 03:58:45 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

ECC is a multi-harness agent engineering toolkit. Its Unified Memory Vault stores scoped Markdown records and offers create-only writes, lexical search, ID reads, and diagnostics through a CLI and optional local MCP server. This review focuses on that explicit memory facility; ECC's separate continuous-learning workflows are not treated as the same store. ([README](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/README.md), [Memory CLI](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory.js), [MCP server](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory-mcp.mjs))

## Who and what

The official README describes ECC as an open-source engineering toolkit spanning agent harnesses, with reusable agents, skills, hooks, rules, memory, and security scanning. The Memory Vault is a local file feature rather than a hosted memory service. ([README](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/README.md))

The catalog resolves ordinal 206 to ECC, slug `ecc`, listed repository `https://github.com/affaan-m/ECC`, with explicit repository attribution. The pinned Atlas entry is included only for roster identity and locator context, not assessment evidence. ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ecc.md))

The official repository page identifies `main` as the default branch. Its main Atom feed reports current full head 4adeee6732a12d1540f49a4d50a38ce8c97f9a53 at 2026-11-20T01:13:45Z; the official commit page identifies that commit on main. Review timestamp: 2026-11-25T11:58:45Z (UTC; 2026-11-25 03:58:45 PST; America/Los_Angeles). ([repository](https://github.com/affaan-m/ECC), [main feed](https://github.com/affaan-m/ECC/commits/main.atom), [head commit](https://github.com/affaan-m/ECC/commit/4adeee6732a12d1540f49a4d50a38ce8c97f9a53))

## Architecture and data model

The reviewed persistent subsystem is a local file vault with a CLI and opt-in stdio MCP server. The README also describes continuous learning that proposes reusable skill changes; that is a related feature but a separate workflow from the memory records reviewed here. ([README](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/README.md), [Memory CLI](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory.js), [MCP server](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory-mcp.mjs))

Each memory is a Markdown document with validated frontmatter: stable ID, title, kind, scope, trust, status, source harness, target harnesses, tags, related memory IDs, timestamps, and body. Supported kinds include context, decision, fact, handoff, lesson, note, preference, and runbook. ([memory format](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault-format.js))

Project and team scopes use separate directories under the project vault, normally `.ecc/memory`; user scope uses `~/.ecc/memory`. Environment variables can override vault roots. Project memory installs restrictive ignore rules, and path checks reject access outside configured trusted roots or through symlinks. ([README](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/README.md), [vault implementation](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault.js))

The save path creates records with restrictive file permissions, rejects suspected secrets, and does not overwrite an existing ID. The format and implementation impose body, document, file-count, and scan-size limits. ([vault implementation](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault.js), [memory format](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault-format.js))

## Write, update, delete, and retrieval

- **Write:** the CLI exposes `init`, `save`, and `handoff`; the optional MCP server exposes `memory_save`. New records default to project scope, note kind, unknown source harness, all target harnesses, unreviewed trust, and active status. Saving is create-only; a duplicate ID is rejected. ([Memory CLI](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory.js), [vault implementation](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault.js), [MCP server](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory-mcp.mjs))
- **Update and delete:** the reviewed CLI and MCP tools expose no update, supersede, reject, or delete operation. The schema contains active, rejected, and superseded statuses, but the save path assigns active and unreviewed automatically. The inspected interfaces therefore do not document a supported correction or erasure workflow. ([Memory CLI](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory.js), [vault implementation](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault.js), [memory format](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault-format.js), [MCP server](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory-mcp.mjs))
- **Retrieval:** search scans Markdown files and ranks active records lexically using phrase and token matches across title, tags, metadata, and body. It supports scope, kind, trust, and target-harness filters, returns metadata plus a short excerpt, and orders ties by update time and ID. Read-by-ID returns the full record and active linked backlinks. ([vault implementation](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault.js), [MCP server](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory-mcp.mjs))
- **MCP scope:** host configuration supplies a harness identity that filters search, read, and doctor results by target harness. Project and team are default recall scopes; user scope requires explicit server enablement. The server says it is host-bound and does not provide OAuth or delegated credential authentication. ([MCP server](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory-mcp.mjs), [vault implementation](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault.js))

## Metric-domain evidence

Every domain below is unmeasured. Source-visible behavior describes implementation only; the project execution record is `not_run` and has no ECC-specific system row. ([metric definitions](../METRICS.md), [execution status](../results/initial-baselines-status.json), [fixture](../fixtures/memory-benchmark-v1.json))

| Domain | Status | Source observation and measurement gap |
|---|---|---|
| Answerable retrieval and abstention | unmeasured | Lexical search and ID read are source-visible, but no answerable or unanswerable cases were run and no accuracy or abstention result was collected. |
| Correction accuracy and stale-value rate | unmeasured | The reviewed save interfaces are create-only and expose no supported correction operation; no correction sequence or stale-value probe was run. |
| Deletion and forget compliance | unmeasured | No deletion tool is exposed in the inspected CLI or MCP interface. No deletion or post-deletion leak probe was run. |
| Scope isolation | unmeasured | Separate local roots and MCP target-harness filtering are visible in source. No cross-scope or adversarial isolation probes were run. |
| Evidence support and citation coverage | unmeasured | Records carry source-harness attribution and linked memory IDs, but no citation-support precision or claim-level citation coverage was evaluated. |
| Retrieval latency | unmeasured | Source contains scan bounds but no measured latency distribution was collected. |
| Write-to-recall delay | unmeasured | No timed acknowledged-write-to-correct-recall workload was executed. |
| Tokens and cost | unmeasured | The reviewed local memory operations do not report a measured token or provider-cost result; none was collected. |
| Storage efficiency | unmeasured | The implementation sets per-record and scan bounds, but no corpus-attributed disk-byte measurement was made. |

## Limits and unknowns

- The inspected retrieval implementation is lexical and file-scanning; source inspection does not establish recall quality, ranking usefulness or production performance. ([vault](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault.js))
- MCP harness filtering is a host integration boundary. The local CLI permits explicit scopes and optional target-harness filtering, and the MCP server does not supply OAuth or delegated credentials; deployment authorization still depends on the host environment. ([cli](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory.js), [mcp](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory-mcp.mjs))
- The record schema includes a sourceHarness and internal links but no required source URL or claim-level evidence field. The fixed trust vocabulary contains only unreviewed, so stored content is explicitly context rather than verified policy. ([format](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault-format.js), [readme](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/README.md))
- The review inspected the README and selected memory CLI, vault format, vault implementation, MCP server and security policy at one pinned commit. It did not inspect every harness adapter, hook, installer, learning workflow, deployment or host permission path. ([readme](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/README.md), [cli](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory.js), [vault](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault.js), [format](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault-format.js), [mcp](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory-mcp.mjs), [security](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/SECURITY.md))

## Benchmark status

**Benchmark not run.** No ECC runtime, tests, or benchmark workload was executed. The project metric definitions and fixture define measurements but provide no ECC result in the execution status record. ([metrics](../METRICS.md), [status](../results/initial-baselines-status.json), [fixture](../fixtures/memory-benchmark-v1.json))

## Contact

The pinned official `SECURITY.md` publishes `affaan@ecc.tools` for vulnerability reports and says `security@ecc.tools` is an unmonitored alias. The pinned README was also checked and publishes no email. No profile or commit metadata or third-party directory was used. ([README](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/README.md), [SECURITY.md](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/SECURITY.md))

## Sources

- **Curated memory-system roster:** [data/memory-systems.json](../data/memory-systems.json) — Ordinal 206 identity, slug, listed repository, and Atlas attribution
- **Official GitHub repository:** [Repository page](https://github.com/affaan-m/ECC) — Public affaan-m/ECC repository; default branch main
- **Official main commit feed:** [main Atom feed](https://github.com/affaan-m/ECC/commits/main.atom) — Current main head SHA and feed updated timestamp 2026-11-20T01:13:45Z
- **Official head commit:** [Commit page](https://github.com/affaan-m/ECC/commit/4adeee6732a12d1540f49a4d50a38ce8c97f9a53) — Full current main head 4adeee6732a12d1540f49a4d50a38ce8c97f9a53
- **Official README:** [README.md](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/README.md) — ECC overview, cross-harness memory and trust model, install/support description
- **Memory CLI:** [scripts/memory.js](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory.js) — CLI commands and save/search/read/doctor interface; no update/delete command
- **Memory vault implementation:** [scripts/lib/memory-vault.js](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault.js) — Scope roots, create-only save, bounded file scan, lexical scoring, read and doctor behavior
- **Memory vault format:** [scripts/lib/memory-vault-format.js](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault-format.js) — Record fields, enums, bounds, validation and secret detection
- **Memory MCP server:** [scripts/memory-mcp.mjs](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/memory-mcp.mjs) — memory_save/search/read/doctor tools, host-bound harness filtering, user-scope authorization
- **Official security policy:** [SECURITY.md](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/SECURITY.md) — Private vulnerability reporting email affaan@ecc.tools; security@ecc.tools alias is not monitored
- **Project benchmark metric definitions:** [METRICS.md](../METRICS.md) — Project benchmark metric definitions
- **Project benchmark execution status:** [results/initial-baselines-status.json](../results/initial-baselines-status.json) — Project-wide execution status is not_run; no ECC-specific system row
- **Project benchmark fixture:** [fixtures/memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json) — Benchmark probe definitions; not measurements
- **Atlas roster entry (identity/locator attribution only):** https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ecc.md
