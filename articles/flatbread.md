# Flatbread Proof source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 241 / Flatbread Proof / `flatbread`  
**Listed repository locator:** [FlatbreadLabs/flatbread](https://github.com/FlatbreadLabs/flatbread)  
**Canonical upstream:** [FlatbreadLabs/flatbread](https://github.com/FlatbreadLabs/flatbread)  
**Default branch / reviewed head:** main / [afd50940308d30d868281bf8111c824707eac476](https://github.com/FlatbreadLabs/flatbread/commit/afd50940308d30d868281bf8111c824707eac476)  
**Review time:** 2026-11-25 20:31:01 UTC (2026-11-25 12:31:01 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Flatbread Proof at ordinal 241, slug `flatbread`, with the explicit repository locator `https://github.com/FlatbreadLabs/flatbread`. Its pinned Agent Memory Atlas record is retained as roster attribution only; Atlas descriptions and capability marks were not used as assessment evidence. The official GitHub repository page shows the default branch `main`; GitHub's official current-commit API resolved it to full head SHA `afd50940308d30d868281bf8111c824707eac476`. This review uses documentation and source pinned to that head.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Flatbread Proof keeps project memory as typed Markdown records tracked in Git. Its CLI exposes bounded reads and typed mutations over a relational graph grouped by Effort. The inspected docs and code describe how the system is designed; this review did not run it or measure its behavior.[[readme]][[proof-readme]]

## Who and what

The official README presents Flatbread as a project by FlatbreadLabs and Proof as its durable-memory path for coding agents. Proof is a package and CLI in the Flatbread monorepo, not a hosted memory service. The broader repository also supports relational content for apps; this review focuses on Proof.[[readme]][[proof-readme]]

## Architecture and data model

The memory graph has eight typed record kinds: Effort, Issue, Finding, Decision, Constraint, Risk, Citation, and Blob. An Effort anchors one coherent work thread; its records are Markdown files with frontmatter and bodies, and ID fields form typed relations.[[proof-readme]]

By default, record files live under `.flatbread-proof/` in one directory per kind. The records remain in Git, while the write journal and derived read cache are intended to be ignored. Normal Git branches, diffs, reviews, history, and reverts provide collaboration and versioning.[[proof-readme]][[readme]]

The writer takes a lock, recovers pending transactions, builds a filesystem snapshot, plans the requested mutation, commits planned file changes through the journal, and returns touched artifacts with a generation token. This summarizes source structure; the writer was not executed.[[writer]][[snapshot]][[journal]]

## Write, update, delete, and retrieval

**Write and update.** One CLI write command accepts 17 typed mutations. The planner validates IDs, kinds, relation rules, and Effort boundaries before producing file changes. The packaged agent skill asks the agent to apply a four-part durability gate, but the documentation says the CLI does not enforce that gate.[[proof-readme]][[planner]]

Typed transitions can resolve Issues, accept or reopen Decisions, change Risk state, supersede or invalidate records, and retract a record. `Retract` marks a record with a reason and timestamp, removes it from browse reads, and strips inbound relation IDs while keeping its file and body. It is not hard deletion; Efforts are abandoned rather than retracted.[[proof-readme]][[planner]]

For a multi-file mutation, the journal stores before and after images, writes through temporary files and renames, and publishes a new generation after commit. On recovery, an uncommitted transaction is rolled back and a committed transaction can finish publishing. The documentation says recovery runs on a later write or live-server start, not on a read alone.[[journal]][[writer]][[proof-readme]]

Read operations list Efforts, retrieve records within an Effort, follow selected relations, find blocking Decisions, or get a record by ID. Results are bounded, paged digests with completeness metadata; the documentation specifies caps on records, relation hops, edges, and digest bytes. A strict minimum-generation option supports read-your-write consistency with a finite timeout.[[proof-readme]][[read]][[digest]]

## Scope isolation

Most record browsing is organized by Effort, and the planner checks Effort boundaries for relations. The current docs permit a live `derives_from` reference across Efforts and render its target as a short checkpoint; state-changing links and `cites` remain within the same Effort. Effort grouping and these checks are source-level behavior, not a tested tenant or principal authorization guarantee.[[proof-readme]][[planner]][[read]]

## Provenance and evidence

Causal `derives_from`, supersession, invalidation, and citation links preserve relationships among records. Citation records can hold an external source and optionally point to a Blob; supported record kinds can cite Citation IDs. These structures can retain provenance, but they do not by themselves prove a claim or guarantee that an agent's generated answer cites supporting evidence.[[proof-readme]][[planner]]

## Efficiency and observability

Bounded digests and progressive reads limit the amount returned per operation; paging reports when results are incomplete. The read source includes read-cache pruning limits, while the write journal and reader use generation tokens and structured errors for consistency handling. These design features do not establish latency, token savings, storage efficiency, or operational reliability; none were measured here.[[proof-readme]][[read]][[digest]][[journal]]

## Metric-domain evidence

All benchmark domains are **unmeasured** for Flatbread Proof. The project metric definitions, fixture, and shared execution status are protocol material, not system results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Typed, bounded read paths exist; no answers were scored. | Unmeasured |
| Correction accuracy and stale values | Supersession and lifecycle operations exist; no correction sequence was assessed. | Unmeasured |
| Deletion leakage | Retract hides a record from browse reads but retains its file and body; no probes were run. | Unmeasured |
| Scope isolation | Reads and relation validation use Effort boundaries; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Citation and Blob relations exist; no answer citations were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings or scheduled probes were collected. | Unmeasured |
| Tokens, cost, and storage | No usage, charge, or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the official README, Proof documentation, and selected source at the verified head. Flatbread Proof, its tests, and its benchmark workloads were not run. The inspection cannot establish answer quality, abstention, correction quality, or real-world agent memory selection.[[readme]][[proof-readme]][[writer]][[planner]]

Retract is an archive-like lifecycle operation, not erasure: content remains in tracked files and may remain in Git history. Retention, branch protection, backup handling, and remote repository access controls were not assessed.[[proof-readme]][[planner]]

The repository's Effort boundaries organize reads and constrain relations, but they do not establish a security boundary for distinct users or tenants. Global Effort discovery and direct ID-based gets are documented; hostile cross-scope behavior was not tested.[[proof-readme]][[read]][[planner]]

## Benchmark status

**Benchmark not run.** No Flatbread Proof runtime, tests, or benchmark workload was executed. No recall, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [shared execution status](../results/initial-baselines-status.json); these define the project protocol and status, not Flatbread Proof measurements.[[metrics]][[fixture]][[status]]

## Contact

The official pinned root README and Proof package README were checked for a published contact email; neither contained one. The structured record stores `contact_email: null` and the exact checked URLs. No address was inferred from commit or profile metadata or taken from a third-party directory.[[readme]][[proof-readme]]

## Sources

Upstream file citations are pinned to reviewed SHA `afd50940308d30d868281bf8111c824707eac476`. The Atlas source is listed only for curated roster attribution. See the structured record [flatbread.json](../data/system-reviews/flatbread.json) and the [curated roster](../data/memory-systems.json).