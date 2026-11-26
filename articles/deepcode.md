# DeepCode

## Identity and review pin

- Catalog ordinal: 182
- System: DeepCode
- Slug: `deepcode`
- Listed repository: https://github.com/HKUDS/DeepCode
- Roster attribution: explicit repository locator; the pinned Atlas entry is included only for curated identity and locator context ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/deepcode.md)).
- Canonical upstream: https://github.com/HKUDS/DeepCode
- Default branch: `main`
- Reviewed full head: [bfe34b668831848f144bb586f466e74b08846498](https://github.com/HKUDS/DeepCode/commit/bfe34b668831848f144bb586f466e74b08846498)
- Review timestamp: 2026-11-25T10:39:55Z (UTC; 2026-11-25 02:39:55 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

## Summary

DeepCode is a coding-agent harness whose persistent project memory is a workspace-local set of Markdown notes. A short `MEMORY.md` index is loaded into each new session; the agent can list, read, write, append, and delete topic files through a memory tool. Retrieval is explicit and filename-directed rather than a built-in semantic search. This review covers the memory subsystem at the verified upstream head; no DeepCode runtime, tests, or benchmark workload were run. ([README](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/README.md), [memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py))

## Who and what

The official README describes DeepCode as an open-source coding agent with TUI, Desktop, Web, and headless clients over a shared local service. It presents project notes as one part of its context alongside project instructions, Skills, and session history. The memory implementation reviewed here is the durable project-note layer under the active workspace. ([README](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/README.md), [Skills and memory guide](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/docs/guide/skills-and-memory.md))

GitHub identifies `main` as the default branch. The official `main` Atom feed reports head `bfe34b668831848f144bb586f466e74b08846498`, updated 2026-11-23T08:23:32Z; the review's upstream source links pin that full revision. ([repository](https://github.com/HKUDS/DeepCode), [main commit feed](https://github.com/HKUDS/DeepCode/commits/main.atom), [head commit](https://github.com/HKUDS/DeepCode/commit/bfe34b668831848f144bb586f466e74b08846498))

## Architecture and data model

Project memory lives in `<workspace>/.deepcode/memory/`. `MEMORY.md` is an index of topic links and short hooks; topic files hold the longer notes. The implementation caps the index injected into the system prompt at 8,000 characters, and the guide says the index is loaded into new sessions while other notes can be read on demand. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py), [Skills and memory guide](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/docs/guide/skills-and-memory.md))

The memory is filesystem-backed Markdown rather than a database of typed facts: the reviewed tool lists regular files, reads a named topic, overwrites on `write`, concatenates on `append`, and unlinks on `delete`. The implementation also defines an offline Orient → Gather → Consolidate → Prune index-consolidation pass that returns a candidate index instead of writing it. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py))

Project instructions are a separate layer. DeepCode can load `AGENTS.md`, `DEEPCODE.md`, or `CLAUDE.md` guidance from the project and user-level locations; the user guide distinguishes these standing instructions from editable project memory notes. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py), [Skills and memory guide](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/docs/guide/skills-and-memory.md))

The shared agent-session builder assembles the memory guidance and tool set for the TUI, headless entry point, and Web backend. The README describes the clients and service as local and shared; this review did not inspect every client or deployment path. ([agent setup source](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/agent_setup.py), [README](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/README.md))

## Write, update, delete, and retrieval

**Write and append.** The agent calls the `memory` tool with a filename and content. `write` requires non-empty content and replaces the file contents. `append` reads an existing file, trims its trailing whitespace, adds a newline, and appends the new content. The tool creates the memory directory when needed. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py))

**Update and consolidation.** Updating a note through `write` overwrites its previous contents; no per-note revision history or mutation log is added by this tool. The consolidation helper produces a proposed `MEMORY.md` index and deliberately does not persist it, leaving acceptance and writing to the surrounding flow. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py))

**Delete.** `delete` removes the named file with `unlink`; there is no tombstone or recovery history in the inspected memory-tool path. This describes the file operation only and does not establish removal from backups, filesystem snapshots, or copies made elsewhere. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py))

**Retrieval.** The `MEMORY.md` index is included in the session prompt, while the agent chooses whether to list files or read a specific topic. The inspected interface has no keyword or vector-search action. Reads go through a helper that caps returned content and refuses a symlink that leaves the memory directory. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py), [Skills and memory guide](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/docs/guide/skills-and-memory.md))

## Scope isolation

The tool instance is constructed with a workspace and uses that workspace's `.deepcode/memory` directory. It rejects names that are not plain filenames, and the read helper refuses links escaping the directory. These are code-visible path boundaries. They do not by themselves establish tenant isolation for a deployment that shares a workspace or filesystem; no cross-workspace or hostile-caller probes were run. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py))

The README says project notes and service data are kept on the user's computer and that DeepCode has no account system or analytics. It also says prompts, files, and tool results are sent to the configured model endpoint, unless a local model is used. Those product statements do not prove isolation or data handling for every custom deployment. ([README](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/README.md))

## Provenance and evidence

The inspected memory tool stores caller-provided text in ordinary files and returns text on read. It does not attach structured source identifiers, authorship, timestamps, confidence, or a correction ledger to each note. Any source trail or evidence links therefore depend on what the agent or user writes into the Markdown content. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py))

The guide asks users to inspect saved notes and says they may edit or remove them as project context changes. This is a human-editable workflow, but the inspected path does not require approval before a tool write, append, or delete and does not report note-level audit history. ([Skills and memory guide](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/docs/guide/skills-and-memory.md), [memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py))

## Efficiency and observability

Loading a bounded index on session start and reading topic files only when requested limits how much note text is automatically placed in context. The 8,000-character index cap and read truncation are explicit implementation controls. The inspected memory path exposes no dedicated retrieval ranking, latency metrics, token accounting, or storage-efficiency reporting, and none was measured here. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py))

The README documents service status and recent logs for operating DeepCode, and says analytics are not sent. Those are product-level service observability and privacy claims, not measurements of memory retrieval or memory-specific telemetry. ([README](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/README.md))

## Metric-domain evidence

All project benchmark domains remain **unmeasured**. The metric definitions, fixture, and project status record are linked for reference only; they were not used to run a workload. ([metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), [execution status record](../results/initial-baselines-status.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | No answer or abstention cases were scored. |
| Correction accuracy and stale-value rate | Unmeasured | No post-update factual probes were run. |
| Deletion leakage | Unmeasured | No post-delete probes or recovery checks were run. |
| Scope isolation | Unmeasured | No cross-workspace or cross-user probes were run. |
| Evidence support and citation coverage | Unmeasured | No generated claims or citations were adjudicated. |
| Retrieval latency and write-to-recall delay | Unmeasured | No timed reads, writes, or retrieval probes were run. |
| Tokens and cost | Unmeasured | No token counts or charges were collected. |
| Storage efficiency | Unmeasured | No corpus or disk-size measurements were collected. |

## Limits and unknowns

This was a selected source review of the official README, the Skills and memory guide, the memory tool implementation, shared agent-session assembly, and the official security policy at the verified head. It did not inspect every project permission path, deployment, lifecycle, or backup behavior. ([README](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/README.md), [Skills and memory guide](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/docs/guide/skills-and-memory.md), [memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py), [agent setup source](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/agent_setup.py), [security policy](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/SECURITY.md))

Memory quality depends on the text authored into notes and the agent's decision to follow the index and read a topic. Large-note behavior beyond the visible read cap, concurrent edits, and practical isolation and deletion guarantees remain unmeasured. ([memory implementation](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/core/harness/memory.py))

The official README and SECURITY.md at the reviewed revision were checked for a contact email. The README lists GitHub Issues for bugs and feature requests; SECURITY.md directs vulnerability reports through GitHub private vulnerability reporting. Neither publishes an email, so the structured record stores `contact_email: null` with those exact checked URLs. No commit or profile metadata, third-party directory, or inferred address was used. ([README](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/README.md), [SECURITY.md](https://github.com/HKUDS/DeepCode/blob/bfe34b668831848f144bb586f466e74b08846498/SECURITY.md))

**Benchmark not run.** No DeepCode runtime, tests, or benchmark workload were executed. The structured [system review](../data/system-reviews/deepcode.json) records `benchmark_status: not_run`; project metric definitions and status records remain references, not results. ([metric definitions](../METRICS.md), [execution status](../results/initial-baselines-status.json), [benchmark fixture](../fixtures/memory-benchmark-v1.json))
