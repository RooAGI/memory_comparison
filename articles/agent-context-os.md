# Context OS — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 146 — Context OS / `agent-context-os`  
**Listed repository:** [conorbronsdon/agent-context-os](https://github.com/conorbronsdon/agent-context-os); locator status explicit  
**Canonical upstream:** same public repository; default branch `main`; reviewed head [1a9c688606801de6454a175081d406f47020a144](https://github.com/conorbronsdon/agent-context-os/commit/1a9c688606801de6454a175081d406f47020a144)  
**Review time:** 2026-11-25 08:58:47 UTC (2026-11-25 00:58:47 PST; America/Los_Angeles)

## Identity and scope

The curated roster places Context OS at ordinal 146, with slug `agent-context-os` and the explicit repository locator above. Its pinned Atlas entry is included only for identity and locator attribution, not as assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agent-context-os.md)]

GitHub identifies `main` as the default branch. The official main Atom feed reports full head `1a9c688606801de6454a175081d406f47020a144`, updated 2026-11-17T22:00:23Z; the official commit page confirms that SHA and timestamp. The source links below pin this revision.[[repository](https://github.com/conorbronsdon/agent-context-os)] [[main commit feed](https://github.com/conorbronsdon/agent-context-os/commits/main.atom)] [[reviewed head](https://github.com/conorbronsdon/agent-context-os/commit/1a9c688606801de6454a175081d406f47020a144)]

## Summary and architecture

Context OS keeps durable context in Markdown files in a Git repository and provides provider-neutral workflow skills with adapters for supported coding agents. The README describes a shared lifecycle kernel for setup, start, update, and end-session handoffs. Host-specific commands, hooks, and permissions remain in adapter directories.[[official README](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/README.md)]

Start assembles a read-only continuity briefing from fixed state files and the latest session, with optional explicit Markdown sources. The briefing includes freshness, normalized-text and raw SHA-256 values, and optional expected-revision checks. It labels the output a preview, not a host read log.[[continuity implementation](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/continuity.py)]

The README documents a separate-root mode. ContextRoot stores context and accepts lifecycle writes; WorkingRoot supplies bounded Git identity, status, and history evidence and receives no marker or lifecycle file. The kernel and continuity code use guarded local-state paths, but source inspection does not prove a host's permission enforcement or deployment isolation.[[root and workflow documentation](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/README.md)] [[lifecycle kernel](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/kernel.py)] [[security policy](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/SECURITY.md)]

## Write, update, delete, and retrieval

**Write and update.** Lifecycle requests produce a proposal showing the intended changes; applying it requires the proposal digest, and successful applies publish local receipts. The README describes setup proposals and update/end-session handoffs. The briefing implementation itself is read-only.[[README](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/README.md)] [[kernel](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/kernel.py)] [[continuity](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/continuity.py)]

**Delete and archival.** The inspected README and continuity implementation describe state updates, handoffs, and receipt history, but do not establish a general record-level forget API, deletion propagation contract, or physical erasure behavior. Those behaviors remain unknown beyond the inspected paths.[[README](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/README.md)] [[continuity](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/continuity.py)]

**Retrieval.** The start flow reads identity and project context, current state, priorities, blockers, decisions, and recent session handoff. A briefing accepts up to 24 additional explicit Markdown sources; each source is limited to 1 MiB, excerpts are bounded, and callers may provide expected normalized-text hashes. Routing prose cannot expand the read set.[[README](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/README.md)] [[continuity](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/continuity.py)]

## Scope isolation

The split-root design makes ContextRoot the lifecycle write target and treats WorkingRoot as bounded Git evidence. Path guards are visible in the shared kernel and continuity implementation. This does not establish runtime tenant isolation or show that every supported agent host enforces the documented boundaries.[[README](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/README.md)] [[kernel](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/kernel.py)] [[SECURITY.md](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/SECURITY.md)]

## Provenance and evidence

Briefings carry repository-relative source paths, freshness status, and normalized and raw hashes. An optional expected hash can flag a mismatch for a selected source. Receipt history links an applied proposal to its before/after file hashes and diff only when the proposal digest matches. The code warns that local receipts may be missing or edited, runtime is self-reported, human approval is not authenticated, and the report is not a complete Git or host read history.[[continuity implementation](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/continuity.py)] [[lifecycle kernel](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/kernel.py)]

## Efficiency and observability

Plain Markdown and Git are the shared storage layer; no separate memory database is required by the described architecture. The briefing bounds explicit sources, file sizes, excerpts, and receipt history (up to 1,000 entries). Freshness and revision checks provide source diagnostics, while local receipts expose selected change history. No runtime telemetry or efficiency measurement was collected.[[README](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/README.md)] [[continuity implementation](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/continuity.py)]

## Metric-domain evidence

These are source observations and unmeasured domains for this task; no Context OS run was performed.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[planned fixture](../fixtures/memory-benchmark-v1.json)]

- **Answerable recall and abstention — unmeasured.** Briefing selects and presents context files; no answerability, retrieval-quality, or abstention workload was run.
- **Correction accuracy and stale values — unmeasured.** Reviewed update proposals and freshness/hash checks are source-visible; no correction or staleness sequence was run.
- **Deletion leakage — unmeasured.** No post-delete retrieval or residual-content probes were run, and a general deletion contract was not established in inspected sources.
- **Scope isolation — unmeasured.** Root and path boundaries are documented and implemented in inspected paths; no cross-project or cross-user workload was run.
- **Evidence support and citation coverage — unmeasured.** Briefings expose source paths and hashes; no generated-claim support adjudication was performed.
- **Latency — unmeasured.** No briefing or retrieval latency distribution was collected.
- **Write-to-recall delay — unmeasured.** No timed write-then-briefing workload was run.
- **Tokens and cost — unmeasured.** No provider token usage or cost accounting was collected.
- **Storage efficiency — unmeasured.** Markdown and Git-backed state are visible in source; no corpus footprint was measured.

## Contact

The official pinned README, SECURITY.md, and CONTRIBUTING.md were checked for a published contact email. None was found; the security policy directs vulnerability reports through GitHub private vulnerability reporting. No profile or commit metadata or third-party directory was used.[[README](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/README.md)] [[SECURITY.md](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/SECURITY.md)] [[CONTRIBUTING.md](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/CONTRIBUTING.md)]

## Limits and unknowns

This bounded review covered the README, shared lifecycle kernel, continuity reporting, and official security and contributor documents; it did not audit every runtime adapter, integration, operating system, or error path. The local receipt view is not an authenticated or complete audit trail. Source review cannot establish stored-context correctness, host enforcement, live scope isolation, deletion completeness, retrieval quality, reliability, or performance.[[README](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/README.md)] [[continuity](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/contextos/continuity.py)] [[SECURITY.md](https://github.com/conorbronsdon/agent-context-os/blob/1a9c688606801de6454a175081d406f47020a144/SECURITY.md)]

No Context OS runtime, tests, or benchmarks were run. This review makes no measured claims about recall, abstention, corrections, deletion, isolation, evidence support, latency, write-to-recall delay, tokens, cost, or storage.[[metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Benchmark status

**Benchmark not run.** No Context OS runtime, tests, or benchmark workload was executed for this source review. See the [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).

## Sources

Structured source IDs and pinned URLs are recorded in [agent-context-os.json](../data/system-reviews/agent-context-os.json). The [pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agent-context-os.md) is included only as curated identity and locator attribution, not assessment evidence.
