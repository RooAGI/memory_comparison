# Data quality and reproducibility review

Reviewed 2026-11-23 against [METRICS.md](METRICS.md), [BENCHMARK_ADAPTER.md](BENCHMARK_ADAPTER.md), the versioned fixture and runner, project assessment criteria, the results manifest/status record, and the site rendering logic. The Agent Memory Atlas inspired this project and helped us discover systems to study; project reviews are based on independent inspection of upstream source.

## Findings

- **Historical inventory:** `data/memory-systems.json` is a legacy snapshot of 852 reports. `data/project-assessments.json` defines the project criteria and currently contains no system roster.
- **Project source evidence:** Each source finding cites direct inspection of the upstream repository at the exact revision recorded by this project.
- **Fixture and harness pins:** The fixture is version 1.0.0 with 6 cases and 20 operations. Its SHA-256 is `2c9ed8c1e0de3ae8fb10f581d92a9f6ffea74779636ccdf4439154ae918c0785`, matching the status record. The runner is version 1.0.0; its SHA-256 is `13a35fed16c42c90469f09da0ceb39a09dad29e46fbe560a53f6d5d8a97f0b63`, also matching the status record. The status record links the fixture and harness by project path and version/hash, and records the discovery catalog revision `19199a4fc249e89c0793be06f0b166b358089ba0`.
- **Execution status and denominators:** The result manifest currently lists one execution-status record. Graphiti, Mem0, Letta, and Memori each show 0 completed, 0 unsupported, 0 failed, and 20 not-run operations. Their system repository URLs and analysis commit SHAs are present. All quality numerators and observed denominators are null; retrieval latency has zero observations, and write-to-recall and usage observations are zero. Planned fixture probe counts are explicitly presented separately from measured denominators. The site visibly labels these records as execution status and displays blockers.
- **Schema and interpretation:** The status record uses `benchmark_execution_status_record`, not `measured_benchmark_result`. The runner's measured-result structure records fixture hash/version, harness version/commit, system commit/config, model, prompt, retrieval settings, adapter version/capabilities, operation order, raw per-operation observations, and null adjudication pending review. The site renders execution and adjudication separately and links to the source result JSON. METRICS.md defines rate numerators/denominators, units, nearest-rank latency, and limits; the fixture does not itself imply measured outcomes.

## Corrections and remaining limitations

1. **No benchmark measurements exist.** Do not report a score, comparative ranking, or completed benchmark. The current status record is appropriate as a blocker record. A measured run requires runnable, system-specific adapters and checkouts, plus the frozen shared configuration described below.
2. **Model and prompt are intentionally unpinned.** Before measurement, choose and version the model/provider, prompt templates, retrieval settings, decoding, hardware/region, cache and background-job policy, timeout/retry policy, and provider price schedule. Record deviations. The record gives a reason for these unknowns; the site exposes the blocker.
3. **Review current upstreams directly.** No system has a project source assessment yet. Inspect each selected system's current upstream repository, record the exact commit and file/symbol evidence, and leave uninspected behavior unknown.
4. **Strengthen direct source navigation in result records.** The status JSON contains repository URLs and commit SHAs separately, but the UI currently shows each system's name and blockers without links to that repository commit. Add a repository-at-commit URL (and, when available, the adapter/config source) to each status entry and render it. The measured-run renderer shows system commit/config values in the run record, but a commit SHA alone is not a clickable source link.
5. **Keep adjudication separate from execution.** The runner captures outputs and leaves `result_state` null; it does not calculate quality metrics or adjudicate citations. After capture, apply the metric case rules, record each adjudication with rationale, and aggregate only eligible cases. For deletion, require acknowledged deletion before a runtime denominator exists; preserve failed/unsupported/not-run cases and unknown reasons.

## Reproduction procedure

From the project root:

1. Serve the static site with `python3 -m http.server 8000` and open `http://localhost:8000`. The browser reads `data/project-assessments.json` and `results/index.json`; refresh the page after editing either JSON file. There is no automatic data refresh.
2. Refresh project assessments after direct inspection of the selected upstream repository. Record its exact current commit, evidence paths/symbols, review scope, date, and unknowns in the project model.
3. Validate fixture structure without executing adapters with `python3 scripts/benchmark_runner.py --check` when a structural check is needed. This is not a benchmark run.
4. For a benchmark, prepare a versioned JSON config and adapter following BENCHMARK_ADAPTER.md, freeze and record system/model/prompt/retrieval and measurement settings, then execute to a new result path. Add that path to `results/index.json` and adjudicate each operation using METRICS.md.
5. Keep execution status, adjudication, measured denominators, failures, unknowns, and per-operation provenance distinct. Never infer correctness from successful execution or treat planned fixture counts as measured denominators.

This review did not run tests or execute the benchmark. The read-only structural inspection confirmed catalog counts/schema sets, fixture and harness hashes, four 20-operation not-run system records, null observed score denominators, and visible blocker fields. Independent verification of all upstream repository contents and a live full-catalog refresh were outside this review.

## Project-owned system assessment standard

This section defines the project's independent review record and its relationship to benchmark measurements.

### Required report record

Create one report per system and pin the analyzed source at an exact revision. Use an explicit unavailable value and reason rather than guessing a missing field.

- **Identity and provenance:** system name; canonical repository URL; exact analyzed commit SHA (or `unknown` with reason); clickable repository-at-commit URL when available; source checkout/path; review date; reviewer; catalog slug; fixture, harness, adapter, and protocol versions if applicable.
- **Source inspection:** files, line ranges or symbols inspected; commit associated with each source item; claim or question examined; concise observation tied to that evidence; evidence links; inspection scope and excluded areas. Distinguish “observed in inspected source,” “not located in inspected source,” and “unknown/not inspected.” “Not located” is limited to the stated scope and does not establish absence or impossibility.
- **Project capability assessment:** each capability or benchmark-relevant behavior assessed independently, with status, evidence, and scope. Source presence is evidence of implementation structure only; runtime behavior remains unverified until measured.
- **Adapter and execution:** adapter name/version and source; adapter-declared capabilities kept as declarations; per-operation execution counts/states using the adapter contract's `completed`, `unsupported`, `failed`, and `not_run` labels; reasons for unsupported, failed, or not-run work; run-record path and configuration pin where a run exists. Execution completion is not correctness.
- **Adjudication and measured results:** keep the adjudicated `result_state` separate from execution status. For every metric in METRICS.md, record status, numerator, denominator, and percentage where defined; include counts and eligible case IDs. Keep latency distributions with units, sample count and nearest-rank p50/p95/p99; write-to-recall successes and censoring; token usage; cost and price provenance; storage bytes and boundary; failures, unknowns, and unavailable reasons. Link raw per-operation records and adjudication rationale. If not run, not captured, or not adjudicated, use `not_run`/unknown and null observations with a reason; never substitute zero or planned fixture counts for measured denominators.
- **Unknowns and limits:** list uninspected source areas, unavailable repository/revision/configuration, unverified runtime behavior, measurement gaps, and claims the evidence cannot support. Keep this visible beside conclusions.

Source inspection may support narrow statements about code at the pinned revision (for example, which API is called, what data structure is persisted, or whether a fixture operation has an apparent adapter path). It cannot establish measured quality, latency, cost, storage, operational reliability, or security outcomes. Implementation claims cite inspected source; performance claims use measured results. Use METRICS.md formulas and the versioned fixture for measured claims; do not collapse metric results into a composite score or ranking.

### Atlas discovery attribution and project separation

The [Agent Memory Atlas](https://neoneye.github.io/agent-memory-atlas/) inspired this project and helped us discover systems to study. Project reviews are based on independent inspection of upstream source. Atlas references remain attributed discovery context; source findings cite the exact revision inspected, and workload observations link their project result record.

### Roster and assessment records

`data/project-assessments.json` defines the project-owned evaluation criteria and currently contains no system roster. Benchmark execution records remain separate under `results/`; they do not imply that a system is part of the project assessment roster. When a system receives a project assessment, record its exact upstream revision, review date, inspected evidence paths/symbols, observation scope, and unknowns. Benchmark records separately capture fixture/harness/config provenance, operation statuses, metric values and denominators, and unknown reasons. A system with no direct review is **not reviewed**; a system with no workload observations is **benchmark not run**. Preserve prior assessment revisions when new evidence supersedes them.
