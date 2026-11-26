# DiffMem

## Identity and review pin

- Catalog ordinal: 191
- System: DiffMem
- Slug: `diffmem`
- Listed repository: https://github.com/growth-kinetics/diffmem
- Roster attribution: explicit repository locator; the pinned Atlas entry is recorded only for curated identity/locator context, not assessment evidence ([catalog](../data/memory-systems.json), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/diffmem.md)).
- Canonical upstream: https://github.com/Growth-Kinetics/DiffMem
- Default branch: `main`
- Reviewed full head: [48ecbb61e7fedca40d1b41bdfb217a5f80432b20](https://github.com/Growth-Kinetics/DiffMem/commit/48ecbb61e7fedca40d1b41bdfb217a5f80432b20)
- Review timestamp: 2026-11-25T11:14:44Z (UTC; 2026-11-25 03:14:44 PST; America/Los_Angeles)
- Source status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub identifies Growth-Kinetics/DiffMem as a public, non-fork repository with `main` as its default branch. Its official `main` Atom feed reports full head `48ecbb61e7fedca40d1b41bdfb217a5f80432b20`, updated at 2026-08-28T11:06:51Z; the repository page's latest-commit prefix and the full commit page agree. ([repository metadata](https://api.github.com/repos/growth-kinetics/diffmem), [main history](https://github.com/growth-kinetics/diffmem/commits/main.atom), [head commit](https://github.com/Growth-Kinetics/DiffMem/commit/48ecbb61e7fedca40d1b41bdfb217a5f80432b20))

## Summary

DiffMem is a Python memory service and library that keeps each user's current memory in Markdown files on an isolated Git branch, with Git history preserving previous committed states. An LLM writer processes transcripts and edits memory files; a separate LLM retrieval agent explores the current files and Git history through constrained shell commands. This review describes pinned source and documentation, not runtime or benchmark behavior. ([README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md), [code index](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/docs/CODE_INDEX.md))

## Who and what

The README identifies Growth Kinetics as the project maintainer and describes DiffMem as a self-hostable backend for conversational agent memory, also importable as a Python library. The repository describes production use with Annabelle; this is an upstream-reported deployment claim, not independently checked here. ([README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md), [Python API](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/api.py))

## Architecture and data model

The public API is the `DiffMemory` class. The service routes HTTP requests to it; writer, retrieval, onboarding, and consolidation agents are separate modules. Storage is a local Git repository plus one worktree per user. The default executor runs jobs inline through a thread pool, while the README documents an optional Hatchet-backed worker deployment. ([code index](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/docs/CODE_INDEX.md), [Python API](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/api.py), [local storage](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/storage/local_storage.py), [README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md))

A user's orphan branch is named `user/{user_id}`; its worktree contains the user profile, generated index, entity Markdown files, monthly timeline files, and archived raw session transcripts. The selected ontology controls entity folders and prompts; the repository documents built-in personal and corporate profiles plus custom profiles. YAML frontmatter stores structured entity metadata such as type and status, with support for legacy trailing semantic-index blocks. ([local storage](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/storage/local_storage.py), [writer](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/writer_agent/agent.py), [frontmatter](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/frontmatter.py), [README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md))

## Write, update, delete, and retrieval

**Writes and updates.** Session processing archives the input transcript under `sessions/`, asks the writer agent to identify entities to create or update, applies those changes, writes a timeline entry, refreshes per-entity and master indexes, and optionally rebuilds followups. The commit step stages the worktree changes and creates a commit named with the session ID and affected entities. Later edits produce newer current-state files while earlier committed versions remain in Git history. ([writer](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/writer_agent/agent.py), [Python API](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/api.py))

**Retrieval.** The retrieval path starts from a baseline that can include the user entity, recent timeline, and always-loaded entities. A multi-turn model then plans file, file-section, and Git-history pointers using a command tool; the resolver fetches those pointers and applies a token budget. The command router allowlists read-oriented Unix commands and selected Git subcommands, limits command time/output, and records command timing in logs. This is repository exploration guided by an LLM, not vector or embedding search. ([code index](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/docs/CODE_INDEX.md), [retrieval agent](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/retrieval_agent/agent.py), [resolver](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/retrieval_agent/resolver.py), [command router](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/retrieval_agent/command_router.py))

**Deletion and lifecycle.** Ordinary writer edits replace current file content but leave prior committed content in Git history. The storage backend has a user wipe operation that removes the local worktree and branch; the coordinator attempts a backup backend deletion when that method exists. The inspected GitHub backup implementation provides push/pull but no `delete_user` method, so this review did not establish deletion of a mirrored remote branch, Git object reclamation, snapshots, or other copies. The one-time consolidation migration can also remove legacy commitment files after folding their content into owner entities. ([local storage](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/storage/local_storage.py), [repository manager](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/repo_manager.py), [GitHub backup](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/storage/github_backup.py), [code index](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/docs/CODE_INDEX.md))

## Scope isolation

The documented storage model creates separate orphan branches and worktrees per user ID. The HTTP routes address a user by path parameter, while the README describes one optional shared bearer API key and defaults authentication off; it recommends enabling auth for public exposure. The reviewed paths do not show a per-user principal/authorization binding, so branch separation is a storage boundary and not by itself proof of authenticated caller isolation. No cross-user leakage workload was run. ([README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md), [local storage](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/storage/local_storage.py), [server](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/server.py))

## Provenance and evidence

Git commits record session/consolidation changes, and raw session transcripts are archived in each user worktree. Entity frontmatter supports structured metadata and status normalization. In the inspected flow, I did not find a required per-fact pointer from an entity claim back to its source transcript or a claim-level citation format; commit and transcript history provide broader traceability rather than demonstrated source support for each answer. ([writer](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/writer_agent/agent.py), [frontmatter](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/frontmatter.py), [status](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/status.py), [README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md))

## Efficiency and observability

DiffMem avoids vector databases, embeddings, and BM25; the README emphasizes plain Markdown and Git-based retrieval. Retrieval uses bounded turn, time, output, and token controls, and local Git is required because the retrieval agent runs repository commands. GitHub backup is optional and the README says synchronization runs outside the write request path. The project also lists a more robust indexing strategy and configurable retrieval caps as roadmap items. These are source/documentation observations, not measured speed, cost, or storage outcomes. ([README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md), [command router](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/retrieval_agent/command_router.py), [retrieval agent](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/retrieval_agent/agent.py), [code index](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/docs/CODE_INDEX.md))

## Metric-domain evidence

All project benchmark metrics are **unmeasured** for DiffMem. Source inspection establishes mechanisms only. ([metric definitions](../METRICS.md), [project status record](../results/initial-baselines-status.json), [fixture, not run](../fixtures/memory-benchmark-v1.json))

| Domain | Status | Source observation |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | LLM-guided file/Git exploration can return selected context; no answerability or abstention cases were scored. |
| Correction accuracy and stale-value rate | Unmeasured | Writer updates and Git history are present; no correction workload was run. |
| Deletion leakage | Unmeasured | Local user wipe and file lifecycle code exist; no post-delete probes, remote branch deletion, or storage reclamation checks were made. |
| Scope isolation | Unmeasured | Per-user branches/worktrees and shared-key auth settings are source-visible; no cross-user leakage workload was run. |
| Evidence support precision and citation coverage | Unmeasured | Session transcripts and commits provide history, but no claim-level citation contract was established in the inspected path; no claims were adjudicated. |
| Retrieval latency and write-to-recall delay | Unmeasured | Retrieval logs and timeouts exist; no timed retrieval or write-to-recall samples were collected. |
| Tokens and cost | Unmeasured | LLM calls and token budgets are configured, but no usage or cost was measured. |
| Storage efficiency | Unmeasured | Markdown and Git storage are used; no corpus-attributed bytes were measured. |

## Limits and unknowns

This bounded review inspected the README, code index, Python API, session writer, retrieval agent/resolver/command router, local storage, backup backend, frontmatter, and status helper. It did not inspect every server route, executor implementation, deployment configuration, ontology, consolidation tool, or provider integration. ([README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md), [code index](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/docs/CODE_INDEX.md), [Python API](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/api.py), [writer](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/writer_agent/agent.py), [retrieval agent](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/retrieval_agent/agent.py), [local storage](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/storage/local_storage.py))

Source inspection cannot establish retrieval quality, writer correctness, effective deployment authentication, actual cross-user isolation, deletion from all copies, remote backup cleanup, latency, model cost, or storage efficiency. No DiffMem runtime, tests, or benchmark workload were run. The README's deployment and performance statements remain upstream-reported claims, not measurements from this review. ([README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md), [metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

The official pinned README was checked for a published contact email; none was found. No commit/profile metadata or third-party directories were used. ([checked official README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md))

## Benchmark status

**Benchmark not run.** DiffMem, its tests, and benchmark workloads were not run. The project fixture is a workload specification only; the project status record does not provide a DiffMem measurement from this review. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity and ordinal](../data/memory-systems.json)
- [Atlas roster entry, attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/diffmem.md)
- [Official repository metadata](https://api.github.com/repos/growth-kinetics/diffmem)
- [Official main commit feed](https://github.com/growth-kinetics/diffmem/commits/main.atom)
- [Reviewed full head 48ecbb61e7fedca40d1b41bdfb217a5f80432b20](https://github.com/Growth-Kinetics/DiffMem/commit/48ecbb61e7fedca40d1b41bdfb217a5f80432b20)
- [Pinned README](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/README.md)
- [Pinned code index](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/docs/CODE_INDEX.md)
- [Pinned Python API](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/api.py)
- [Pinned session writer](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/writer_agent/agent.py)
- [Pinned retrieval agent](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/retrieval_agent/agent.py)
- [Pinned command router](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/retrieval_agent/command_router.py)
- [Pinned retrieval resolver](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/retrieval_agent/resolver.py)
- [Pinned local storage](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/storage/local_storage.py)
- [Pinned repository manager](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/repo_manager.py)
- [Pinned GitHub backup backend](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/storage/github_backup.py)
- [Pinned frontmatter helper](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/frontmatter.py)
- [Pinned status helper](https://github.com/Growth-Kinetics/DiffMem/blob/48ecbb61e7fedca40d1b41bdfb217a5f80432b20/src/diffmem/status.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
