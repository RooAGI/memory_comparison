# Decision Keeper source review

**Review status:** Reviewed from code
**Benchmark status:** Not run
**Roster ordinal / name / slug:** 181 / Decision Keeper / `decision-keeper`
**Listed repository locator:** `https://github.com/mudassirzulfiqar/Decision-Keeper` (explicit)
**Catalog attribution:** [Pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/decision-keeper.md), used only for identity and locator attribution
**Canonical repository / default branch:** [mudassirzulfiqar/Decision-Keeper](https://github.com/mudassirzulfiqar/Decision-Keeper) / `main`
**Reviewed head:** [`911ff6b88e7c5e65b64326f9a5719291e6608ab6`](https://github.com/mudassirzulfiqar/Decision-Keeper/commit/911ff6b88e7c5e65b64326f9a5719291e6608ab6); official main history agrees
**Review time:** 2026-11-25 10:43:20 UTC (2026-11-25 02:43:20 PST; America/Los_Angeles)
**Published contact:** No email found in the [official README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md).

## Identity and scope

The catalog places Decision Keeper at ordinal 181, gives it slug `decision-keeper`, and lists the explicit repository locator above. The pinned Atlas report is retained for roster attribution only; the implementation assessment below comes from the current official upstream README, skill, and installer.[[catalog entry](../data/memory-systems.json)] [[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/decision-keeper.md)]

GitHub identifies `main` as the default branch. The official branch history and a shallow checkout both resolve to full head `911ff6b88e7c5e65b64326f9a5719291e6608ab6`; the commit page dates it 2026-11-16T13:03:03+01:00. All cited upstream files below pin this revision.[[repository](https://github.com/mudassirzulfiqar/Decision-Keeper)] [[main history](https://github.com/mudassirzulfiqar/Decision-Keeper/commits/main.atom)] [[reviewed head](https://github.com/mudassirzulfiqar/Decision-Keeper/commit/911ff6b88e7c5e65b64326f9a5719291e6608ab6)]

## Summary

Decision Keeper is an instruction-and-skill workflow for keeping project decisions as Markdown files under `docs/decision/`. It installs guidance and a skill for Codex or Claude Code, then asks the agent to recognize lasting decisions, apply existing rules, and update the human-readable decision tree. It does not provide a database, retrieval service, or independent runtime API in the reviewed files. The intended read and write behavior is therefore mediated by the host agent and repository instructions rather than enforced by a memory service.[[README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md)] [[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)] [[installer](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/install.py)]

## Architecture and data model

The README describes an installer that appends a marked section to an existing root instruction file and copies a skill into the client-specific skill directory. Codex uses `.agents/skills/decision-keeper/`; Claude Code uses `.claude/skills/decision-keeper/`. Both clients share the project's `docs/decision/` files.[[README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md)] [[installer](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/install.py)]

The memory unit is a decision or reusable correction represented in Markdown. The skill directs the agent to resolve `docs/decision/decision-keeper.md` from the project root, read it in full, and follow relevant topic and child links. The repository contains no structured decision schema, database model, record identifiers, timestamps, source fields, or retrieval index in the reviewed files.[[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)] [[README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md)]

The installer contains path and overwrite checks: it rejects unsafe project roots and symlinks, limits installation to a repository root when Git detects a nested repository, recognizes only expected managed instruction blocks, and uses known hashes before replacing existing skill files. The installed organizer procedure keeps one writer, organizes active rules into linked topic files, and caps each file at ten decision bullets. Its checker validates links, duplicate placements, unlinked files and that limit. These tools are part of the package, while the decision workflow remains agent-mediated.[[installer](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/install.py)] [[organizer procedure](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/.agents/skills/decision-keeper/references/organizer.md)] [[tree checker](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/.agents/skills/decision-keeper/scripts/check_tree.py)]

## Write, update, delete, and retrieval

**Write.** The skill captures clear, lasting user-confirmed rules and reusable corrections. It skips one-off requests, tentative ideas, vague feedback, quoted examples, and explicit exceptions. The user may also use `/keep` or `/keep and go`, which the instructions treat as explicit recording requests. The agent records decisions in the project's decision files.[[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)] [[README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md)]

**Update and correction.** The documented workflow applies relevant rules at their narrowest supported scope and resolves material conflicts before recording a new default. Examples describe revising an existing rule while preserving portions the user did not change. This is a prose-directed editing workflow; the inspected repository does not define a typed correction operation or transactional update protocol.[[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)]

**Delete.** The README and skill say a user can remove or drop a rule. No delete API, tombstone, mutation ledger, or retention contract appears in the reviewed files. Whether old content persists in version control, backups, or host context depends on the project and its tools; erasure behavior is not established here.[[README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md)] [[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)]

**Retrieval.** Before work, the instructions call for reading the index in full and following relevant topic links. This is deterministic file-reading guidance, not query ranking or semantic retrieval. Read cost grows with the index and linked material; no retrieval latency or quality measurements are provided.[[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)]

## Scope isolation

The skill is explicitly limited to projects that opted in by installing its files and adding the guidance block to project instructions. The installer requires an existing client instruction file, refuses installation at filesystem root or home, and rejects installation into a subdirectory of a Git repository when Git is available. Decision-file scope is consequently project-root based. These are installer and instruction boundaries, not access-control checks on every later file read or write; no user, tenant, or per-decision authorization model is defined.[[README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md)] [[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)] [[installer](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/install.py)]

## Provenance and evidence

The skill asks the agent to store only clear, user-confirmed decisions and to omit secrets, personal data, and transcripts. Manual `/keep` entries are identified as manual entries in the workflow. The Markdown data model shown by the repository has no required fields for author, confirmation event, source quotation, evidence URL, confidence, trust state, or audit history. Provenance thus depends on the agent's process and any optional prose a project chooses to retain; it is not enforced by a record schema.[[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)]

## Efficiency and observability

The design uses ordinary project Markdown and requires no database service. The skill asks the agent to read the index in full and then follow relevant links, favoring a readable, inspectable workflow over automated retrieval. As the decision tree grows, the required read may add context and token cost; no compaction, indexing, background processing, telemetry, or usage accounting is shown in the reviewed files. These are source observations, not measured performance results.[[README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md)] [[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)]

## Metric-domain evidence

| Domain | Review status | Evidence |
|---|---|---|
| Answerable retrieval accuracy | Unmeasured | The workflow reads Markdown files; no retrieval probes were run.[[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)] |
| Correction accuracy and stale-value rate | Unmeasured | User-confirmed edits are described, but no correction workload was run.[[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)] |
| Deletion leakage | Unmeasured | Rule removal is described without a retention contract; no deletion probes were run.[[README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md)] |
| Scope isolation leak rate | Unmeasured | Opt-in and root boundaries are documented; no cross-project probes were run.[[installer](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/install.py)] |
| Evidence support precision and citation coverage | Unmeasured | User confirmation is a workflow criterion, but there is no evidence schema or citation adjudication.[[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)] |
| Retrieval latency | Unmeasured | No timed retrieval workload was run.[[METRICS](../METRICS.md)] |
| Write-to-recall delay | Unmeasured | No acknowledged-write/probe schedule was run.[[METRICS](../METRICS.md)] |
| Tokens and cost | Unmeasured | No host usage or provider accounting was collected.[[METRICS](../METRICS.md)] |
| Storage efficiency | Unmeasured | No persistent storage footprint was measured.[[METRICS](../METRICS.md)] |

These are project benchmark domains, not Decision Keeper results. The shared status and fixture specify project measurement context only.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Contact

The official pinned [README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md) was checked for contact information and publishes no email. The JSON record stores `contact_email: null` and the exact checked URL. No commit or profile metadata or third-party directories were used.

## Limitations and unknowns

- The organizer and checker provide deterministic file-organization rules and structural checks, but they do not validate whether a decision is true, user-confirmed, correctly scoped, or applied by the host agent. The checker is only useful when the workflow invokes it.[[organizer procedure](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/.agents/skills/decision-keeper/references/organizer.md)] [[tree checker](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/.agents/skills/decision-keeper/scripts/check_tree.py)]
- Decision recognition, scope application, file selection, correction, and verification depend on the host agent following prose instructions. The reviewed source does not provide an independent enforcement layer or audit trail.[[skill](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/SKILL.md)]
- Removal is documented as a user-facing action, but the reviewed sources do not establish secure erasure across Git history, backups, or host context.[[README](https://github.com/mudassirzulfiqar/Decision-Keeper/blob/911ff6b88e7c5e65b64326f9a5719291e6608ab6/README.md)]
- No Decision Keeper runtime, tests, or benchmark workloads were run. All project metric domains remain unmeasured.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)]

## Benchmark status

**Benchmark not run.** No system, tests, or benchmark workloads were executed. This source assessment is not a measured result. See [project metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and pinned upstream URLs are in [decision-keeper.json](../data/system-reviews/decision-keeper.json). The [pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/decision-keeper.md) is included for curated identity and locator attribution only.
