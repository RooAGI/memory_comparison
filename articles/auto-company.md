# Auto Company

## Identity and review pin

- **System:** Auto Company (renamed Autonomous Company upstream)
- **Curated position:** 80
- **Slug:** `auto-company`
- **Listed repository:** [MaxMiksa/Auto-Company](https://github.com/MaxMiksa/Auto-Company)
- **Canonical repository at review:** [MaxMiksa/Autonomous-Company](https://github.com/MaxMiksa/Autonomous-Company)
- **Default branch:** `main`
- **Reviewed head:** [`211baad12b08d25c75b10ade86ed301098be69b2`](https://github.com/MaxMiksa/Autonomous-Company/commit/211baad12b08d25c75b10ade86ed301098be69b2)
- **Reviewed:** 2026-11-24 22:06:17 UTC (14:06:17 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/auto-company.md), used only for identity, listed locator, and source attribution.

The curated roster places Auto Company at position 80, slug `auto-company`, with listed locator `https://github.com/MaxMiksa/Auto-Company`. That locator now redirects to the canonical public repository `MaxMiksa/Autonomous-Company`; its official repository page identifies `main` as the default branch. The official main-branch commit feed reported full head `211baad12b08d25c75b10ade86ed301098be69b2` at review time. The upstream README says the project was formerly Auto-Company and documents the v3 rename. Atlas descriptions, capability marks, and layout were not used as assessment evidence.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/MaxMiksa/Autonomous-Company)] [[main commit feed](https://github.com/MaxMiksa/Autonomous-Company/commits/main.atom)] [[reviewed head](https://github.com/MaxMiksa/Autonomous-Company/commit/211baad12b08d25c75b10ade86ed301098be69b2)] [[README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md)]

## Summary

Auto Company is a self-hosted continuous-work framework for coding assistants. Each fresh CLI cycle receives a shared Markdown consensus file, performs work under project prompts and rules, and rewrites that file as the handoff for the next cycle. A shell loop, file-based governance checks, and cycle logs provide the memory lifecycle; this review does not assess task quality or actual long-running reliability.[[README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md)] [[loop](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/auto-loop.sh)] [[cycle prompt](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/PROMPT.md)]

## Who and what

The repository is maintained by GitHub user MaxMiksa; the README identifies Zheyuan (Max) Kong and describes Autonomous Company as an AI company framework. It is a self-hosted application and orchestration framework using Claude Code by default, with Codex CLI and explicitly configured optional adapters. The README names macOS and Windows/WSL support and describes systemd/launchd daemon modes; it also calls the project experimental and warns that continuous operation depends on engine services and model availability.[[README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md)] [[engine adapters](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/ENGINE_ADAPTERS.md)]

## Architecture and data model

**Source observations.** The memory baton is a Markdown document at `memories/consensus.md`, initialized from the tracked `memories/consensus.template.md`. The repository's `.gitignore` and README distinguish runtime memory from the template. The README and cycle script describe each cycle as an independent CLI invocation: the loop loads `PROMPT.md` and the consensus, runs the selected agent engine, and the prompt requires a rewritten consensus before the cycle ends. This is whole-document, human-readable state rather than an indexed or semantic memory store.[[README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md)] [[loop](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/auto-loop.sh)] [[prompt](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/PROMPT.md)] [[consensus template](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/memories/consensus.template.md)]

The template organizes the baton into cycle timestamp and phase, work done, decisions, active projects, next action, company state, human overrides, priority issues, and open questions. The guard and format utility recognize exactly two canonical governance sections: `## Human Overrides` and `## Priority Issues`. The loop's supporting state is also file-backed: a baseline backup, pending-cycle marker, pause/state files, snapshots, logs, and a usage ledger are named in the guard and loop. Product identity and project files are maintained by surrounding framework components; they are not fields in the shared consensus alone.[[template](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/memories/consensus.template.md)] [[format validator](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-format.py)] [[governance guard](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-guard.sh)] [[loop](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/auto-loop.sh)]

## Write, update, delete, and retrieval

**Write and update.** The prompt directs the agent to update the consensus before cycle end. Before execution, the guard initializes a missing file only when no prior state indicates an unexpected loss, validates the two governance headings, and checks unresolved P1 items. It records a pre-cycle baseline; the format helper compares the Human Overrides section byte-for-byte and compares P1 items so a cycle cannot remove or resolve prior items. A failed verification restores the prior consensus and pauses governance. The loop also records successful cycles and their snapshots. The underlying model-written body remains plain text and its other headings are not schema-validated as semantic facts.[[prompt](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/PROMPT.md)] [[guard](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-guard.sh)] [[format validator](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-format.py)] [[loop](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/auto-loop.sh)]

**Retrieval.** Retrieval is direct file loading: the current consensus is preloaded into the prompt for the next independent CLI cycle, with instructions to read it from disk if it was not provided. The reviewed path does not select memories by query, rank records, or retrieve historical snapshots into the prompt automatically; snapshots are recovery/history artifacts in the inspected contract.[[README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md)] [[prompt](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/PROMPT.md)] [[guard](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-guard.sh)]

**Delete and reset.** I found no per-claim forget or delete interface in the reviewed consensus workflow. The guard exposes a reset operation; the format helper archives the pre-reset document and rebuilds from the template while retaining the two human-governed sections. That is a whole-baton reset with a recoverable copy, not verified erasure. Removing the checkout or other runtime files is outside this review; persistence in backups, logs, snapshots, or external copies is not measured.[[guard](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-guard.sh)] [[format validator](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-format.py)]

## Scope isolation

The consensus baton is one shared file for the running framework checkout, and the cycle prompt treats it as the common handoff across fresh sessions. The current project also maintains product records and separate project workspaces, and its README says connected products retain separate identity and history. That product-catalog boundary does not make the consensus content a per-user or per-agent memory: the inspected consensus format has no tenant, user, or role access fields. The loop's engine permissions and local filesystem boundary are deployment settings; prompts and the charter are behavioral instructions, not a proof of authorization isolation.[[README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md)] [[prompt](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/PROMPT.md)] [[charter](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/CLAUDE.md)] [[format validator](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-format.py)]

## Provenance and evidence

The baton contains free-form summaries, decisions, and state supplied by the model. The template has no required source identifiers, claim-level citations, author identity, confidence, trust label, or event-time/valid-time fields. The guard preserves two human-governed regions and blocks a cycle when an unresolved P1 exists, but those process controls do not establish the truth or provenance of other recorded claims. The README describes persistent logs, product history, and usage data around the cycle, but the reviewed memory path does not join those records to individual consensus statements.[[template](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/memories/consensus.template.md)] [[prompt](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/PROMPT.md)] [[format validator](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-format.py)] [[README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md)]

## Source-visible efficiency and observability

**Code observations, not measurements.** The design loads the shared summary into each new engine cycle, so the prompt context grows with that document unless an operator or agent keeps it compact. The loop has configurable cycle interval and timeout, a consecutive-error circuit breaker, usage-limit waits, pause controls, structured usage accounting, cycle logs, snapshots, and state files. These make operational state and some provider-reported usage visible; they do not provide benchmarked retrieval latency, token counts attributable to memory alone, or correctness results. No cost or storage measurements were made for this review.[[loop](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/auto-loop.sh)] [[README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md)] [[usage accounting](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/usage.py)]

## Metric-domain evidence

All domains below are **unmeasured for this review**. These are source-visible mechanisms and evidence gaps, not outcome estimates.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | The full consensus is loaded into the prompt; no relevant-fact or abstention probe was run. | Unmeasured |
| Correction accuracy and stale values | Rewriting and guarded P1 preservation are implemented; no correction history or post-correction probes were evaluated. | Unmeasured |
| Deletion leakage | Reset retains a recoverable pre-reset archive; no deletion or residual-copy probes were run. | Unmeasured |
| Scope isolation | One shared baton is used by cycles in a checkout; no cross-user or cross-project isolation probes were run. | Unmeasured |
| Evidence support and citation coverage | The template is prose-oriented without claim-level citation fields; no adjudication was run. | Unmeasured |
| Latency and write-to-recall delay | Loop interval, cycle timing, and logs are source-visible; no timings were collected. | Unmeasured |
| Tokens, cost, and storage | The loop records usage and has configurable budget pauses; no memory-attributed token, price, or storage measurement was collected. | Unmeasured |

The [project metric definitions](../METRICS.md), [versioned benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) define workloads and reporting. Planned cases are not results for Auto Company.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded read-only inspection of selected current documentation and source at the reviewed SHA. It does not establish actual task completion quality, whether generated consensus statements remain correct, whether all engine adapters report usage completely, runtime stability, deletion completeness across backup/log copies, or project isolation under concurrent work. The README calls the project experimental and notes that continuous operation relies on external engines, services, and available model quota. No system execution, benchmarks, or tests were run for this review.[[README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md)] [[engine adapters](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/ENGINE_ADAPTERS.md)] [[loop](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/auto-loop.sh)]

## Contact-list follow-up

I checked the official pinned [README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md). Its contribution/contact section publishes Zheyuan (Max) Kong's addresses `kongzheyuan@outlook.com` and `zheyuank@tepper.cmu.edu`; the JSON records both and this exact source URL.

## Benchmark status

**Benchmark not run.** I did not execute Auto Company, a benchmark workload, or tests. Source-visible safeguards, operational logs, and upstream-reported product behavior are not measured results from this review. See the [project metric definitions](../METRICS.md), [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Curated roster](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution only.
- [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/auto-company.md) — source attribution only.
- [Official repository](https://github.com/MaxMiksa/Autonomous-Company) — canonical current location and default branch.
- [Official main commit feed](https://github.com/MaxMiksa/Autonomous-Company/commits/main.atom) — full main head at review time.
- [Reviewed head](https://github.com/MaxMiksa/Autonomous-Company/commit/211baad12b08d25c75b10ade86ed301098be69b2)
- [README](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/README.md)
- [Cycle loop](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/auto-loop.sh)
- [Consensus governance guard](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-guard.sh)
- [Consensus format validator](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/consensus-format.py)
- [Consensus template](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/memories/consensus.template.md)
- [Cycle prompt](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/PROMPT.md)
- [Project charter](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/CLAUDE.md)
- [Engine adapters](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/ENGINE_ADAPTERS.md)
- [Usage accounting](https://github.com/MaxMiksa/Autonomous-Company/blob/211baad12b08d25c75b10ade86ed301098be69b2/scripts/core/usage.py)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only source review; no Auto Company execution, benchmarks, or tests.
