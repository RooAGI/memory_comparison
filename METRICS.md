# Proposed memory comparison metrics

This document defines a reproducible benchmark suite for comparing memory systems on a fixed corpus and workload. Results describe the tested system, model, configuration, and benchmark version; they are not universal claims about a system.

## Metric definitions

For all rates below, count a case once at the unit named in the fixture (normally one question or probe). A case is correct only when it satisfies its recorded gold criterion. Report numerator and denominator as counts as well as the percentage. Do not silently drop abstentions, errors, timeouts, or missing outputs: classify them and apply the case rule below.

### Answerable retrieval accuracy

**Numerator:** number of answerable question cases whose response contains the gold answer and satisfies the fixture's required constraints (including scope and time, where specified).

**Denominator:** all answerable question cases presented to the system, including cases with abstentions, errors, timeouts, or empty responses.

**Formula:** correct answerable cases / answerable cases.

Higher is better on this corpus and setup. Report unanswerable cases separately as a diagnostic: the count of appropriate abstentions / all unanswerable cases. Do not include unanswerable cases in the answerable accuracy denominator.

### Correction accuracy and stale-value rate

A correction fixture records an original value, an explicit replacement, and the effective time at which the replacement should govern.

**Correction accuracy numerator:** post-correction answerable probes that return the current gold value and do not assert the superseded value as current.

**Correction accuracy denominator:** all post-correction answerable probes, including abstentions and failed calls.

**Stale-value numerator:** post-correction probes that assert the superseded value as current.

**Stale-value denominator:** all post-correction probes for which the fixture specifies that the corrected fact is answerable. This includes abstentions, errors, and timeouts in the denominator, but only a returned stale value in the numerator.

Report both fractions and counts. Higher correction accuracy and lower stale-value rate are better. The two metrics are not complements: a response may be wrong without being stale, and may contain both stale and current claims. Define whether a case is multi-valued at fixture authoring time; score a stale assertion as stale even if the current value also appears.

### Deletion leak rate

After a fixture's deletion request has been accepted, issue its designated probes against the deleted material.

**Numerator:** post-deletion probes that reveal any protected deleted content according to the fixture's leakage rule. Match exact identifiers/quotes and semantic paraphrases against adjudicated gold content; record which rule triggered.

**Denominator:** all scheduled post-deletion probes for that deletion case, including failed calls and no-answer responses. A probe is eligible only if its deletion request was accepted; report rejected/failed deletion requests separately and do not treat them as successful deletion cases.

**Formula:** leaking post-deletion probes / eligible post-deletion probes.

Lower is better. Report direct, paraphrase, semantic, and identifier probe strata separately where available. Zero observed leaks means only that none of the enumerated probes leaked in this run; it does not prove deletion is complete or safe against untested queries, side channels, backups, or future changes.

### Scope isolation leak rate

A fixture identifies a principal and the scope(s) that principal may access, plus a forbidden fact stored only in another scope.

**Numerator:** cross-scope probes whose response exposes a forbidden fact or forbidden record identifier under the fixture's adjudication rule.

**Denominator:** all scheduled probes by that principal for which the fact is explicitly out of scope, including abstentions, errors, and timeouts.

**Formula:** forbidden cross-scope returns / eligible cross-scope probes.

Lower is better. Also report counts and strata by scope boundary (for example tenant, project, or user). Zero observed leaks applies only to tested principals, scopes, data, and probes; it is not a general isolation guarantee.

### Evidence support precision and citation coverage

Annotate each response with its factual claims. Before running the benchmark, define which claims are material and how claims are split. Adjudicators check citations against the stored source passage(s) actually available to the system.

**Evidence support precision numerator:** cited factual claims for which the cited source directly supports the claim without contradicting a relevant qualifier, time, or scope.

**Evidence support precision denominator:** all factual claims accompanied by at least one citation. Count a claim once even if it has multiple citations; it is supported if at least one cited source supports it. Report unsupported and contradicted claims separately.

**Citation coverage numerator:** factual claims with at least one citation that resolves to a retained source or memory item.

**Citation coverage denominator:** all adjudicated factual claims in the response, including claims with no citation.

Higher is better for both. Report the two metrics together: citation coverage prevents high precision based on citing only a small, selectively chosen subset from appearing sufficient. Report claim counts and adjudication method; distinguish invalid/unresolvable citations from absent citations.

## Efficiency and delay profile

Report these measures beside quality metrics, never folded into a composite quality score.

- **Retrieval latency:** elapsed time from retrieval request submission to complete retrieval response, in milliseconds. Record each operation; report p50, p95, and p99, plus sample count and failures/timeouts. State whether measurement includes network, queueing, reranking, and model generation. Keep retrieval-only latency separate from end-to-end answer latency.
- **Write-to-recall delay:** elapsed time from successful completion/acknowledgment of a write to the first scheduled retrieval that correctly returns the written fact. Probe at a fixed, published schedule and record every probe. If no probe succeeds by the final scheduled time, report right-censored at that time and count it as not recalled within the window; do not invent a successful delay. Report median and percentile summaries only for observed successes, plus the success fraction and censoring count. State whether background processing/consolidation was allowed and its schedule.
- **Tokens:** record input and output token counts separately for every model/API operation, using provider-reported usage when available; otherwise name the tokenizer and version. Report totals and per-case distributions, and separate memory/retrieval context tokens from answer-generation tokens where observable. Do not estimate missing usage without labeling it.
- **Cost:** sum measured charges for all in-scope operations in the run, including memory-system and model/API calls, under a documented provider price schedule and currency/date. Report total, per fixture case, and per successful answer. Include storage or egress charges only if measured or explicitly estimated and label estimates. If prices or usage are unavailable, report unavailable rather than zero.
- **Storage efficiency:** report bytes of persistent storage attributable to the benchmark corpus after the specified indexing/consolidation point, and bytes per successfully stored gold item (total attributable bytes / count of gold items accepted for storage). State exactly which databases, indexes, logs, backups, and metadata are included, and whether size is logical or physical. If attribution is not reliable, report raw system storage size and mark per-item efficiency unavailable.

Percentiles use the nearest-rank definition: sort the (n) observed values ascending and select rank ⌈(p n)⌉ for percentile (p), with rank starting at 1. Show sample count; do not publish a percentile for an empty sample. For cost and size, publish currency/unit and measurement boundary.

## Versioned deterministic fixture set

The machine-readable fixture is [fixtures/memory-benchmark-v1.json](fixtures/memory-benchmark-v1.json), version 1.0.0. It contains only synthetic facts, scripted ordered operations, fixed query text, expected answers/abstentions, source IDs, and gold scoring labels. Each case resets to an empty namespace before replay. Execute events in listed order; write/correction/delete operations must be acknowledged before the next operation. Fixture-relative clock offsets and cited source text are fixed, so cases do not depend on a live person, service, or external dataset.

The six stable cases cover answerable direct and paraphrase recall (REC-001), unanswerable direct and paraphrase probes (REC-002), correction/current and stale-value probes (COR-001), deletion with direct and paraphrased probes (DEL-001), forbidden cross-scope direct and paraphrased probes (SCP-001), and source-grounded answers requiring citations (EVD-001). The JSON records every operation ID, turn, variant, prompt, expected outcome, evidence/source requirement, and scoring label.

Fixture result states have these exact meanings: **supported** means the output meets the gold answer and required constraints/evidence; **unsupported** means abstention is the expected gold outcome (absent, deleted, or inaccessible fact); **unknown** means the captured observation cannot be adjudicated and is excluded from correctness numerators but counted with a reason; **not_run** means the operation was not attempted and is never a pass. For an unsupported case, asserting the protected, absent, or out-of-scope fact is a failure. A run should store one outcome state per operation plus the reason for unknown/not_run.

Each operation record requires latency in milliseconds, input/output tokens as integer token counts, cost in USD, persistent storage in bytes at a named boundary, write acknowledgment and probe timestamps, and the first successful write-to-recall delay in milliseconds. Null means unobserved/unavailable, not zero. Capture every raw retrieval latency and report p50/p95/p99 with nearest-rank, sample count, failures, and timeouts. Probe write-to-recall at fixed offsets of 0, 1, 5, and 30 seconds after acknowledgment; stop after first correct recall, otherwise right-censor at 30 seconds. Report observed delay distribution, successful-recall fraction, and censored count. For token and cost accounting include every in-scope model/API operation, split input/output tokens, retain tokenizer or provider usage source, and identify provider price schedule/date. For stored bytes, capture total persistent bytes after the final operation and background processing; state whether the count is logical or physical and which databases, indexes, logs, and backups it includes. Report bytes per accepted gold item as a separate quantity.

A run summary must include fixture version, system/version, model/version, UTC start, repeat, exact operation order, latency percentiles, write-to-recall schedule and censoring, token totals, USD cost, storage bytes, and measurement boundary. Keep all case outputs and unavailable/failure reasons. These fixtures specify portable workloads and scoring expectations; adapters may map operations to system APIs but must preserve event order, caller scopes, query text, and returned evidence. No test suite or runner is implied by this fixture document.

## Benchmark fixtures and protocol

Maintain a versioned, machine-readable fixture set with stable case IDs and gold labels. Include multi-session fact retrieval, answerable and unanswerable questions, explicit correction histories, deletion requests with post-delete probes, paired permitted/forbidden scope cases, and source-grounded claims with citation expectations. Include direct and paraphrased questions; for deletion and scope, include semantic and identifier probes where relevant. Avoid putting answer text in prompts unless the case is specifically testing such a prompt.

For each run:

1. Pin the fixture corpus and protocol version. Reset each system to a clean, documented state, then load the same ordered events and wait the same defined interval or readiness condition before probing.
2. Execute the same case order, prompts, principal/scope identity, retry policy, and probe schedule for every system. Randomize or rotate system order across repeated runs when feasible, and record the order.
3. Freeze the benchmark-visible model and version, system/repository commit, system configuration, memory policy, retrieval parameters, prompt templates, tool definitions, and decoding settings. Keep hardware, region, network conditions, concurrency, and provider settings fixed or record deviations.
4. Define warm/cold cache policy, background job policy, timeout, retry, and rate-limit handling before measurement. Record failed and retried calls rather than silently dropping them. For stochastic outputs, run the published number of repeats with documented seeds when supported.
5. Adjudicate outputs against the versioned gold rules. Use blinded review for subjective claim support where feasible, with disagreements resolved by a documented second review. Preserve raw output for audit.

Do not compare runs with different fixture versions or materially different controlled variables as if they were directly comparable. If a variable changes, publish a separate run/configuration and explain the change.

## Per-case record

Retain one record per operation/probe with at least:

- run ID, timestamp, case ID, fixture version, system name, system commit/version, and repeat number;
- event history and relevant gold answer, current/superseded values, deletion state, principal, allowed scopes, and expected source references (or stable references to the fixture);
- exact prompt, response, returned memory/source IDs, citations, tool calls, and adjudication labels;
- operation start/end times, status, timeout/retry details, token usage by operation and input/output, measured or estimated cost with provenance;
- write acknowledgment time, scheduled and actual probe times, and whether/when the first correct recall occurred;
- storage measurement boundary, raw byte count, measurement time, and gold-item count;
- hardware, region, provider/model, cache state, relevant configuration, and any deviation or unavailable field.

Protect sensitive fixture and response content appropriately. A published report may use redacted content and stable hashes, but retain enough audit data under the project's data policy to reproduce labels.

## Aggregation and reporting

Publish each system's numerator/denominator and count next to every rate. Aggregate by metric across all eligible cases and show useful strata (such as correction age, probe type, scope boundary, and repeat); do not average percentages with different denominators. Where repeated runs are used, show per-run results and a pooled result formed by summing numerators and denominators. Add uncertainty intervals for proportions when sample sizes support them, naming the method; do not use an interval to imply coverage beyond the fixture.

Show latency percentiles, write-to-recall success and censoring, token/cost/storage distributions, failures, and unavailable measurements alongside the quality results. Keep system descriptions, Atlas feature flags, and measured benchmark outcomes in separate sections or tables. Do not calculate one combined score or ranking from them.

## Reproducibility metadata and limitations

Every published run should include the fixture and protocol version/hash, harness source revision, system source commit and configuration, model/provider/version, prompt and decoding configuration, hardware/region, run date, repeat count/order, cache and background-job policy, measurement scripts/version, price schedule/date, adjudication rules, and deviations. Keep machine-readable per-case outputs and an aggregation procedure available where the project's data and licensing rules permit.

These metrics estimate behavior only for the tested fixtures, query distribution, model, system version, configuration, and measurement window. Gold labels and claim adjudication can be incomplete or subjective; outputs may be stochastic; provider usage and cost may be missing or change; storage boundaries differ; benchmark probes cannot establish universal security, deletion, or isolation guarantees. Report failures and uncertainty, and do not interpret an unobserved leak as proof that none is possible.

## Atlas fields versus benchmark results

The [Atlas comparative matrix](https://neoneye.github.io/agent-memory-atlas/compare/) contains descriptive fields generated from report frontmatter, including memory unit, storage backend, retrieval and write strategies, update/delete model, scoping model, agent integration, background processing, trust/provenance model, strengths, and risks. These characterize a system; they are not measured outcomes under this benchmark.

The [Atlas capability index](https://neoneye.github.io/agent-memory-atlas/capabilities/) lists seven reviewer-checked feature rubric fields: Tombstone, Trust state, Bi-temporal, Scope enforced, Mutation audit, Human review, and Negative evals. A checked mark means the report reviewer found the feature in code at the pinned commit; a dash means it was not found, not that it is impossible or planned. The page describes “of 7” as a shape indicator, not a score. Preserve each mark as a feature/evidence claim and keep it separate from measured results.

The [Atlas benchmark overview](https://neoneye.github.io/agent-memory-atlas/benchmarks/) discusses benchmark approaches, but the inspected analysis does not specify complete formulas and protocols for every quantitative result it cites. For example, it reports LoCoMo accuracy/context-token/latency summaries and ForgetEval cost/latency figures without enough formula, model/run, or aggregation detail on the inspected page to reproduce all values. Treat these as Atlas-reported claims with their stated source, not as fully specified metrics or directly comparable results. This document proposes our own protocol and does not assert that Atlas has measured these project metrics.

Other useful Atlas sources: [A–Z system index](https://neoneye.github.io/agent-memory-atlas/a-z/) and [Atlas source repository](https://github.com/neoneye/agent-memory-atlas).
