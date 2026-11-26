# gh-aw source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 256 / gh-aw / `gh-aw`  
**Listed repository locator:** [github/gh-aw](https://github.com/github/gh-aw)  
**Canonical upstream:** [github/gh-aw](https://github.com/github/gh-aw)  
**Default branch / reviewed head:** main / [ea7bc4dd637ff9c9f61e1706a53041c34cd4724c](https://github.com/github/gh-aw/commit/ea7bc4dd637ff9c9f61e1706a53041c34cd4724c)  
**Review time:** 2026-11-25 20:55:28 UTC (2026-11-25 12:55:28 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists gh-aw at ordinal 256 with the explicit locator `https://github.com/github/gh-aw`; the catalog's Agent Memory Atlas revision is recorded only as roster attribution and locator context. The official repository page identifies `main` as its default branch. Official `git ls-remote --symref` reported `refs/heads/main` at `ea7bc4dd637ff9c9f61e1706a53041c34cd4724c`, matching a fresh shallow checkout of `main`. Source inspection is pinned to that full SHA.[[catalog]][[repo]][[head]][[atlas]]

## Summary

GitHub Agentic Workflows (gh-aw) is a Go CLI extension and compiler that turns Markdown workflow definitions with YAML frontmatter into GitHub Actions workflows. Its memory features persist ordinary files across runs using GitHub Actions cache, git branches, or an experimental GitHub Drives preview. The agent reads and writes files through its normal tools; gh-aw supplies restoration, prompts, validation, and persistence steps. These are source and documentation observations, not measured memory quality results.[[readme]][[cache-doc]][[repo-doc]][[drive-doc]]

## Who and what

The official repository describes GitHub Agentic Workflows as an open-source GitHub CLI extension. The reviewed memory mechanisms are workflow features rather than a separate memory server or model: cache-memory and repo-memory are configured in workflow frontmatter, while Drive memory is explicitly feature-gated for repositories enrolled in a private preview.[[readme]][[cache-doc]][[repo-doc]][[drive-doc]]

## Architecture and data model

The three memory surfaces store user-authored files rather than imposing one fact schema. Cache-memory mounts a workflow-scoped directory, normally `/tmp/gh-aw/cache-memory/`; multiple cache IDs get separate directories. Repo-memory mounts a configured branch under `/tmp/gh-aw/repo-memory-{id}/`; branches are created as orphans by default or cloned shallowly. Drive memory mounts an enrolled GitHub Drive under `/tmp/gh-aw/drive-memory/`. Markdown, text, JSON/JSONL, and CSV are common supported formats, subject to configured extension/glob rules.[[cache-doc]][[repo-doc]][[drive-doc]]

The compiler generates setup and persistence jobs around the agent. Cache-memory ordinarily restores and saves Actions cache entries; when configured with threat detection, a separate publisher validates and saves the staged artifact. Repo-memory validates eligible changed files and commits/pushes them after the workflow, with merge handling for concurrent branch updates. Drive memory checks out the drive before execution and publishes validated changes afterward; with threat detection, publication is a separate job gated on detector acceptance and an unchanged drive checkout.[[cache-doc]][[repo-doc]][[drive-doc]][[cache-setup]][[repo-clone]][[cache-commit]]

## Write, update, delete, and retrieval

**Writes and updates.** The agent edits files in its mounted directory using its regular file tools. Cache-memory persists a snapshot in an Actions cache lineage and can be evicted; repo-memory commits file changes to a branch; Drive memory commits to the enrolled drive. Optional JSON/JSONL schemas and JavaScript validation can reject persistence. Repo-memory also supports file-count, file-size, patch-size, extension, and glob limits. Repo-memory concurrent saves preserve files not changed by the current run; JSONL can union rows, while same-line changes in other file types use the current run's version.[[cache-doc]][[repo-doc]][[drive-doc]]

**Updates and deletion.** Files can be overwritten or removed in the working directory; repo-memory's Git history preserves versioned prior states. The inspected guides do not describe a memory-specific correction protocol, semantic fact retraction, or tombstone model. Repo-memory persistence scopes eligible files but explicitly preserves branch files outside the configured scope, so omission from an upload is not deletion. Cache cleanup can remove old cache entries, but cache expiry/eviction is not a content-level erasure guarantee. Physical erasure across Git history, cache copies, backups, or preview service storage was not established.[[repo-doc]][[cache-doc]][[drive-doc]]

**Retrieval.** gh-aw does not expose a built-in ranked memory query API in the reviewed memory guides. It mounts the store as files and injects instructions and location into the agent prompt; retrieval is performed by the agent or by separately configured tools such as MCP servers. Cache restore may fall back across compatible keys and branch scopes. Repo-memory reads its configured branch. The reviewed Drive guide describes a mounted filesystem, not semantic retrieval. Recall quality and whether an agent reads the relevant file are not established by these storage mechanisms.[[cache-prompt]][[repo-prompt]][[repo-prompt-multi]][[cache-doc]][[repo-doc]][[drive-doc]]

## Scope isolation

Cache keys are workflow- and branch-scoped; runs on non-default branches can fall back to the default-branch cache, while pull-request writes remain isolated to the merge ref. The `scope: repo` option broadens compatible restore behavior within the branch namespace. Integrity-aware cache-memory adds separate `merged`, `approved`, `unapproved`, and `none` lineages and merges higher-integrity data down, but the docs explicitly say namespaces do not authenticate contents or prevent another writer from using the same namespace.[[cache-doc]]

Repo-memory branches and optional target repositories define storage boundaries; workflows sharing a branch can share its contents. GitHub repository permissions and optional app credentials govern access, but branch protection and trusted writers remain operational responsibilities. Drive names are repository-wide and branch-aware under the preview service; runs sharing repository, ref, and drive scope can exchange content across event types. The docs caution against sharing Drive scope where stronger producer isolation is required and say gh-aw does not verify server-side namespace enforcement. No adversarial cross-workflow or tenant-isolation test was run.[[repo-doc]][[drive-doc]]

## Provenance and evidence

Git history can show repo-memory file revisions, and cache-memory integrity branches separate data by the writer run's configured integrity level. Threat-detection gates and validators can prevent some candidate writes from being published. These mechanisms provide lineage or persistence controls, not proof that stored statements are true or that an authorized writer's content is safe. Cache contents are described as unsigned and unverified; restored memory is treated as untrusted data. The guides do not define per-claim source citations, evidence adjudication, correction confidence, or a provenance record for ordinary files.[[cache-doc]][[repo-doc]][[drive-doc]][[repo-prompt]][[cache-setup]]

## Efficiency and observability

The documentation characterizes cache-memory as faster and short-lived, repo-memory as slower and versioned, and identifies cache limits and repo-memory per-file/count/patch constraints. Cache storage is subject to a 10GB per-repository quota, LRU behavior, and eviction after seven days of inactivity; repo-memory retention is described as unlimited subject to repository limits. These statements are documented platform behavior, not measurements made here. Operational troubleshooting points users to workflow logs and persistence-job summaries. No retrieval latency, write-to-recall delay, token use, cost, or corpus storage efficiency was measured.[[cache-doc]][[repo-doc]][[metrics]][[status]]

## Metric-domain evidence

All project benchmark domains are **unmeasured in this review**. The metric definitions and fixture describe evaluation scope only. gh-aw, its tests, and benchmarks were not run for this task. See [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | File mounting and agent-directed retrieval are documented; no retrieval probes were scored. | Unmeasured |
| Correction accuracy and stale values | File overwrite and Git history are available; no correction workload was run. | Unmeasured |
| Deletion leakage | Files may be deleted from a working copy, but persistence-specific erasure across all copies is not established; no probes were run. | Unmeasured |
| Scope isolation | Cache branches, repo branches, target repositories, and Drive scopes are documented; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | No per-claim evidence contract was found in the inspected memory guides; no answers were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Storage and restore/publish paths are documented; no timings were collected. | Unmeasured |
| Tokens, cost and storage | Quotas and configured validation limits are documented; no resource measurements were collected. | Unmeasured |

## Limits and unknowns

This is a bounded review of the current README, cache-memory, repo-memory, and experimental Drive guides, plus cache/repository setup and commit scripts. It does not trace every compiler path, action, trigger, enterprise configuration, or external GitHub service behavior. File-backed state makes schema and retrieval design largely the responsibility of each workflow author; the reviewed guides do not prove that any particular workflow records durable, accurate, or useful facts.[[readme]][[cache-doc]][[repo-doc]][[drive-doc]]

The review did not run gh-aw, tests, or benchmarks. It cannot establish runtime correctness, recall quality, correction behavior, complete deletion, authorization isolation, performance, token usage, cost, or storage efficiency. Drive memory is a private-preview integration and should be understood within that explicit availability limitation.[[drive-doc]][[metrics]][[status]]

## Benchmark status

**Benchmark not run.** No gh-aw runtime, tests, or benchmark workload was executed for this review. No recall, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Contact

The official pinned SECURITY.md publishes the obfuscated address `opensource-security[@]github.com` for coordinated vulnerability disclosure. It is recorded as `opensource-security@github.com`, with the exact checked URL; no commit or profile metadata or third-party directory was used.[[security]]

## Sources

Upstream file citations are pinned to the verified full SHA. The Atlas entry is included solely as curated roster attribution, not assessment evidence. See the structured record [gh-aw.json](../data/system-reviews/gh-aw.json) and [curated roster](../data/memory-systems.json).
