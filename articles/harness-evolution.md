# Harness Evolution as Learning source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 281 / Harness Evolution as Learning / `harness-evolution`  
**Listed repository locator:** [ZyGan1999/self-evolving-harness-as-learning](https://github.com/ZyGan1999/self-evolving-harness-as-learning)  
**Canonical upstream:** [ZyGan1999/self-evolving-harness-as-learning](https://github.com/ZyGan1999/self-evolving-harness-as-learning)  
**Default branch / reviewed head:** main / [9f7e8178588513f30296cd965a9923c17f5ff98c](https://github.com/ZyGan1999/self-evolving-harness-as-learning/commit/9f7e8178588513f30296cd965a9923c17f5ff98c)  
**Review time:** 2026-11-25 22:26:05 UTC (2026-11-25 14:26:05 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists ordinal 281 as Harness Evolution as Learning, slug `harness-evolution`, with the explicit repository locator above. Its pinned Atlas entry is recorded only as roster attribution, not assessment evidence. GitHub's official repository metadata identifies `main` as the default branch; the commit API, `git ls-remote`, and a fresh shallow checkout agree on full head SHA `9f7e8178588513f30296cd965a9923c17f5ff98c`. GitHub reports the commit timestamp as 2026-09-25 09:04:15 UTC. This review was checked at the timestamp above.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Harness Evolution as Learning is a Python research repository for comparing agent control and memory-learning approaches on AppWorld tasks. It runs prompt-injected memories and other harness methods through a session driver, programmatic preference checks, feedback, and checkpoint evaluation. Memory state is maintained in updater objects during a run and saved in experiment outputs; the code review does not measure runtime quality or performance.[[readme]][[driver]][[ace]][[runner]]

## Who and what

The official README presents the repository as the implementation and configurations for Q1–Q3 experiments: harness reachability, memory length, and self-evolution. It is an experiment harness rather than a hosted memory service or standalone persistent memory API. No maintainer identity is inferred from commit or profile metadata.[[readme]]

## Architecture and data model

The session driver runs an agent episode, checks it against a configured persona, constructs feedback from violations, sends that feedback to an updater, and advances session history. At configured checkpoints it evaluates a frozen memory without feeding evaluation feedback back into the updater. The rendered memory is inserted into the agent prompt at the start of an episode.[[driver]][[feedback]][[agent]]

The Q3 ACE-style updater stores an ordered set of one-sentence preference bullets with short content-derived IDs, helpful/harmful counters, and local character-trigram vectors for deduplication. Other implementations include a full-memory rewrite, a rolling Reflexion list, keyed TEPA precedents with active/revoked state, and TRACE rules that check API arguments. Q2 has a separate fixed candidate assertion bank ranked into a selected-length prompt block.[[ace]][[updaters]][[baselines]]

These objects live in process during an experiment. The runner writes experiment summaries and a final updater JSON snapshot; the driver writes episode, history, and checkpoint artifacts. The inspected runner does not load updater state from a previous experiment, so saved output is not evidence of general cross-run recall.[[runner]][[driver]][[ace]][[baselines]]

The current README describes Q1–Q3 experiment protocols and lists the baseline arms. The latest README revision removed detailed TEPA/TRACE explanatory text, while the pinned current source still contains those implementations. This review describes those mechanisms from source inspection.[[readme]][[baselines]]

## Write, update, delete, and retrieval

**Write.** Accepted episodes and feedback-free episodes are skipped. For rejected episodes, ACE asks an LLM for JSON add/modify deltas; the self-evolution updater rewrites the whole memory string and applies a character limit; Reflexion appends a reflection; TEPA produces keyed precedents from action summaries and feedback; TRACE compiles feedback into API/argument checks. Parse failures and updater state are tracked in code.[[ace]][[updaters]][[baselines]][[feedback]]

**Update and delete.** ACE can modify a bullet by ID, removes entries whose trigram-vector cosine similarity exceeds its threshold, and retains the newest entries when over capacity. Deduplication can discard a later conflicting bullet; there is no explicit bullet delete API. The rewrite arm replaces all text, and Reflexion evicts entries outside its rolling window. TEPA deactivates superseded entries under the same key but retains them in an archive and can reactivate exact repeats. TRACE maintains compiled checks with its own duplicate and capacity handling. These differ by arm and do not form a common durable CRUD interface.[[ace]][[updaters]][[baselines]]

**Retrieval.** The Q3 driver renders the complete current memory and inserts it into the prompt for each episode. There is no semantic or lexical retrieval index in this path. Q2's ranked, fixed assertion pool is a separate experimental memory-length condition, not a general recall service.[[driver]][[agent]][[ace]][[baselines]]

## Scope isolation

The updater is instantiated for an experiment arm and session; its memory objects do not carry explicit user, tenant, project, or conversation scope identifiers. The driver binds the run to a selected persona and task stream, but this source review does not establish isolation across concurrent executions or any deployment boundary.[[runner]][[driver]][[ace]][[baselines]][[persona]]

## Provenance and evidence

ACE records episode numbers, applied deltas, and counts of deduplication/capacity drops. TEPA retains episode numbers and a mutation history for additions, revocations, re-promotions, and parse failures. These are algorithm diagnostics, not source-linked evidence records for learned preferences. Feedback is produced by programmatic checkers and templates; the inspected flow does not provide a human evidence adjudication step.[[ace]][[baselines]][[feedback]][[driver]]

## Efficiency and observability

Updater state exposes quantities such as memory characters and lines, update and parse-failure counts, bullet or active-precedent counts, and selected eviction/revocation counters. The experiment runner records configuration, evaluation points, model usage, and final updater state. These are observability surfaces and output fields; this review collected no latency, token-cost, storage, or quality measurements.[[ace]][[baselines]][[runner]][[driver]]

## Metric-domain evidence

Every benchmark domain below is unmeasured for this system in this review. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the evaluation protocol and shared project status; they are not Harness Evolution as Learning results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Q3 injects the complete rendered memory; no retrieval or abstention probe was run. | Unmeasured |
| Correction accuracy and stale-value rate | The code has modify, rewrite, keyed replacement, and compiled checks; no correction workload was run. | Unmeasured |
| Deletion leakage | Some arms evict or deactivate memory; no post-deletion leakage workload was run. | Unmeasured |
| Scope-isolation leakage | Updater objects are run/session scoped in the driver; no cross-scope probe was run. | Unmeasured |
| Evidence support and citation coverage | Updater diagnostics do not provide source-linked claim evidence; no answer evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Injection/update order is source-visible; the runtime was not timed. | Unmeasured |
| Tokens, cost, and storage efficiency | The runner has usage and output fields; no values or normalized storage totals were collected. | Unmeasured |

## Limits and unknowns

The inspection covered selected README, driver, prompt integration, updater, feedback, runner, and Q3 persona files; it did not exhaustively trace every experiment or edge case. The review did not execute the system, its tests, AppWorld workloads, or benchmarks. It cannot establish runtime correctness, recall quality, generalization beyond the frozen personas/task splits, cross-run recovery, user isolation, complete deletion/retention behavior, or performance and cost. The findings apply to the pinned SHA and may change with later revisions.[[readme]][[driver]][[runner]][[metrics]]

## Benchmark status

**Benchmark not run.** No Harness Evolution as Learning runtime, tests, or benchmark workload was executed. No recall, correction, deletion, scope, evidence, latency, token, cost, or storage results are claimed. The project metric definitions, fixture, and shared status record define protocol and status only.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email; none was present. The structured record stores `contact_email: null` and the exact checked URL. No address was inferred from commit/profile metadata or taken from a third-party directory.[[readme]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas source is included only for curated roster attribution and is not assessment evidence. See the structured record [harness-evolution.json](../data/system-reviews/harness-evolution.json) and [curated roster](../data/memory-systems.json).
