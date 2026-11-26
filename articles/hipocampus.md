# Hipocampus source and design review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 297 / Hipocampus / `hipocampus`  
**Listed repository locator:** [kevin-hs-sohn/hipocampus](https://github.com/kevin-hs-sohn/hipocampus)  
**Canonical upstream:** [kevin-hs-sohn/hipocampus](https://github.com/kevin-hs-sohn/hipocampus)  
**Default branch / reviewed head:** main / [df88ca19d42a3aba4caeaba4512da46cae7827da](https://github.com/kevin-hs-sohn/hipocampus/commit/df88ca19d42a3aba4caeaba4512da46cae7827da)  
**Review time:** 2026-11-25 23:03:52 UTC (2026-11-25 15:03:52 PST; America/Los_Angeles).

## Identity and review pin

The curated roster identifies Hipocampus at ordinal 297 and lists the repository explicitly. Its pinned Atlas attribution is retained for roster identity and locator context only; Atlas was not used as assessment evidence. The official GitHub repository page identifies `main`; official Git transport reported `HEAD -> refs/heads/main` at df88ca19d42a3aba4caeaba4512da46cae7827da, which matched a shallow checkout. The official `main.atom` feed also identifies that full commit as the latest entry. Source observations below refer to that checkout.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Hipocampus is a project-local memory harness built around Markdown files, agent skills and lifecycle hooks. It keeps a compact topic index available at session start, stores raw session notes and curated knowledge in files, and organizes summaries into a daily/weekly/monthly/root compaction tree. Optional qmd search complements index triage and tree traversal. This assessment describes source and documented behavior; it does not reproduce the upstream MemAware results.[[readme]][[layers]][[compact]]

## Who and what

The official repository presents Hipocampus as an installable agent memory harness for Claude Code, OpenCode, OpenClaw and Codex support in the inspected checkout. The repository contains an npm CLI, hooks, platform setup, skills, templates and a written format/compaction specification. Memory is stored in the user's project filesystem rather than a remote memory service.[[repo]][[readme]][[package]]

## Architecture and data model

The design divides project files into hot, warm and cold tiers. Hot files include operational state and `memory/ROOT.md`, a compact topic index; warm files include raw date-stamped logs, knowledge and plans; cold memory uses the compaction tree plus optional search. ROOT entries organize active context, patterns, historical summary and topic pointers. Compaction nodes carry frontmatter such as type, tentative/fixed status, period, source files and topics, creating links back to lower-level files.[[layers]][[formats]][[core]][[compact]]

The tree flows from raw daily logs through daily, weekly, monthly and root nodes. Below line thresholds the mechanical compactor copies or concatenates source text, applying line-based secret redaction; above thresholds it emits a placeholder requiring an agent skill to produce an LLM summary. Root is recursively regenerated from monthly nodes and capped by a configurable token budget. Raw daily logs are described as permanent leaves; summary nodes are derived indexes.[[compaction]][[compact]]

The session-start hook creates memory directories, an initial ROOT stub and configuration when missing, then prints a protocol for agent injection. Platform setup wires session-start and pre-compaction behavior; agent skills describe checkpointing, compaction and retrieval. The compact command can copy a supplied transcript into a date-stamped raw log, but session checkpoints and above-threshold summarization depend on the agent following the installed protocol.[[hooks]][[init]][[core]][[compact]]

## Write, update, delete, and retrieval

**Write.** The protocol asks the agent to append structured session checkpoints to the daily Markdown log and to classify entries by type (project, feedback, user or reference). It also directs agents to save task state and durable notes in project files. The mechanical compact command can extract user/assistant text from a supplied JSONL transcript and append it to the daily file. These are file writes governed by hooks and agent instructions, not a central typed-record API.[[core]][[formats]][[compact]]

**Update and correction.** Raw daily logs are append-only by policy. The derived daily/weekly/monthly/root nodes are regenerated as their source periods change; status transitions from tentative to fixed as periods age. Feedback and user-type entries are intended to survive compaction verbatim, while completed project topics can be summarized and references marked stale. The inspected compactor writes derived nodes but does not implement semantic correction of an old raw fact or a general versioned fact API.[[core]][[compaction]][[compact]]

**Delete.** The documentation says raw daily logs are permanent and must not be removed or edited after a session; the repository provides no memory-item deletion or erasure command in the reviewed CLI. Removing a file manually is outside the supported lifecycle, and derived summaries may retain copied content until regeneration. Secret scanning is a regex-based redaction pass over lines during mechanical compaction, not verified deletion from all copies or backups.[[core]][[compaction]][[compact]]

**Retrieval.** The prescribed flow first checks ROOT's topic index, follows its file pointer, and reads selected content. If the index is insufficient, the recall skill tells the agent to inspect compaction-node frontmatter as a manifest and select up to five files; qmd BM25/vector search is a later fallback when installed. This relies on the agent to execute the skills and interpret retrieved text. No standalone answer service, access-control check, or citation enforcement appears in the reviewed project files.[[recall]][[readme]][[layers]]

## Scope isolation

The default storage boundary is a project directory, with a separate file tree for each project. The specs also describe agent-specific learning files under the project memory tree. This filesystem organization can separate corpora operationally, but the inspected design has no authenticated tenant boundary or runtime scope authorization: isolation depends on which project directory and files the agent or search tool can access. No cross-project isolation workload was run.[[layers]][[core]][[compaction]][[readme]]

## Provenance and evidence

Compaction frontmatter records source-file paths, periods and topics, and the specification requires higher-level summaries to be derived through lower-level nodes. This provides navigable file lineage, but it is not claim-level source citation: the format does not require a source span per statement, confidence state per fact, or enforcement that an answer cites the originating passage. Reference entries can receive a stale marker, and feedback/user types receive special preservation rules; these are lifecycle labels rather than verification of truth.[[formats]][[compaction]][[recall]]

The mechanical secret scanner uses a fixed set of regular expressions and replaces a matching entire line. The code path shows no guarantee that every credential format is detected, nor that raw input, other files, LLM-generated summaries, external copies or backups are scrubbed. The source does not describe a mutation audit trail or an erasure receipt.[[compact]][[compaction]]

## Efficiency and observability

The hot root index is intentionally bounded (default approximately 3,000 tokens) and loaded for every session; deeper content is read on demand. The recall guide's manifest step reads frontmatter rather than full node bodies, and the compactor uses line thresholds to decide when summaries are needed. Optional vector search may require a local embedding model and additional disk, as described by the README; no timing, token or storage values were independently measured.[[readme]][[recall]][[layers]][[compaction]]

The inspected source includes a small compaction state file with last-run and event counters, while the session-start hook emits protocol text. I found no general metrics or structured retrieval telemetry in the reviewed CLI/hooks/skills. These are code observations; no operational traces were collected.[[compact]][[hooks]][[core]]

## Metric-domain evidence

All domains below are **unmeasured in this review**. The README publishes MemAware results, but those are upstream-reported figures, not results reproduced here. No Hipocampus runtime, tests or benchmarks were run. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[readme]][[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | ROOT triage, manifest selection and qmd fallback are documented; no answer/abstention cases were scored. | Unmeasured |
| Correction and stale values | Type-aware compaction and reference staleness markers are specified; no correction or stale-value sequence was evaluated. | Unmeasured |
| Deletion leakage | Raw files are permanent by policy and no item erasure operation was inspected; no post-delete probe was run. | Unmeasured |
| Scope isolation | Project directories and optional agent subtrees organize files; no access-control or cross-project probe was run. | Unmeasured |
| Evidence support and citation coverage | Source-file lineage is represented in frontmatter; no claim-support or citation workload was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Index and search paths are described; no latency or freshness timings were collected. | Unmeasured |
| Tokens, cost and storage | Root token cap, optional vector storage and LLM compaction are documented; no usage, cost or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This review establishes the pinned source and stated protocol, not how reliably an agent follows it. Checkpoint quality, successful summarization, retrieval relevance, and whether users notice stale references depend in part on agent behavior and configuration. The repository's README benchmark table is an upstream claim and was not reproduced. No tests or benchmark workloads were run.[[core]][[recall]][[readme]]

The project favors append-only raw logs and derived summaries rather than correction and erasure. The inspected interface does not establish complete deletion semantics, tenant isolation, claim-level evidence, or credential removal across all stored copies. The actual behavior of qmd, platform-specific injection and any configured LLM provider remains deployment-dependent.[[compact]][[layers]][[formats]][[readme]]

## Benchmark status

**Benchmark not run.** No Hipocampus runtime, tests or benchmark workload was executed for this review. No measured recall, abstention, correction, deletion, isolation, evidence, latency, token, cost or storage result is claimed. The linked metric definitions, fixture and execution status are protocol artifacts, not Hipocampus results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email and contained none. `contact_email` is recorded as null with that exact checked URL; no commit/profile metadata or third-party directory was used.[[readme]]

## Sources

Upstream file sources are pinned to the verified full SHA. The Atlas entry is included only for roster attribution, not assessment evidence. See the structured record [hipocampus.json](../data/system-reviews/hipocampus.json) and the [curated roster](../data/memory-systems.json).
