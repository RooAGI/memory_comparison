# EvoX Genesis source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 232 / EvoX Genesis / `evox-genesis`  
**Listed repository locator:** [EMI-Group/genesis](https://github.com/EMI-Group/genesis)  
**Canonical upstream:** [EMI-Group/genesis](https://github.com/EMI-Group/genesis)  
**Default branch / reviewed head:** main / [56569e9f323dd50b3e05266a937c18cf43c95ef2](https://github.com/EMI-Group/genesis/commit/56569e9f323dd50b3e05266a937c18cf43c95ef2)  
**Review time:** 2026-11-25 20:08:57 UTC (2026-11-25 12:08:57 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists EvoX Genesis at ordinal 232, slug `evox-genesis`, with the explicit locator `https://github.com/EMI-Group/genesis`. The catalog’s pinned Atlas source is retained as roster attribution only; it was not used as assessment evidence.[[catalog]][[atlas]]

GitHub’s official repository API identifies `EMI-Group/genesis` and default branch `main`; its official current `main` commit endpoint returned full head `56569e9f323dd50b3e05266a937c18cf43c95ef2`. The repository page and commit page were checked against that identity and pin.[[repo]][[head]]

## Summary

EvoX Genesis is an open-source agent system for long-running software development. Its memory-relevant design makes project context part of the repository: agents receive Markdown context associated with their assigned repository path, alongside the current task objective. Git versions candidate changes, while SQLite stores application runtime and task data. This is a source-based review of those documented and inspected paths, not a measurement of the running product.[[readme]][[context_node]][[context_builder]]

## Who and what

The README describes Genesis as developed by the EvoX Group at The Hong Kong Polytechnic University. It is a full software-development system with a desktop application, headless server, dashboard, and local MCP endpoint, rather than a standalone personal-memory database.[[readme]]

The README says managers decompose and delegate development objectives, executors work in isolated Git worktrees, and people review candidate diffs. It describes `CONTEXT.md` files as local contracts that define context, responsibility, and scope for a repository path.[[readme]]

## Architecture and data model

The project-context model is a hierarchy of repository paths. `ContextNode` represents a normalized relative path and repository identity; the inspected context builder asks it to assemble the context for an agent’s assigned node. Context is rendered from `CONTEXT.md` files along the repository-root-to-node chain, and the current code also has a global VCT context stage. Stages are rendered as text for the agent prompt, rather than as individually ranked memory records.[[context_node]][[context_builder]]

This is primarily a file-and-Git model for durable project knowledge. The repository documents Git as the record of software versions and SQLite as storage for runtime/task data. A separate per-agent archive table records task and agent IDs, parent/depth, context path, objective/result, base/final commits, branch and archive refs, repository identity, usage/settings, and timestamps.[[readme]][[archive_schema]]

The reviewed code bounds each rendered context stage by a configured byte limit and logs a warning when truncating it. Context-node hierarchy resolves VCT paths in one batched read; an unavailable or unmounted VCT degrades those paths to nil while retaining the nodes.[[context_node]]

## Write, update, delete, and retrieval

**Write and update.** The documented durable project-memory workflow is to edit repository-local `CONTEXT.md` files as ordinary project changes. Those edits travel with Git changes and candidate versions, and the README describes human review of diffs before accepted results carry forward. This review did not identify a separate memory-record write or patch API in the inspected sources.[[readme]][[context_node]]

**Retrieval.** The inspected core path selects context from the agent’s assigned repository path and renders the applicable ancestor files, plus the global context stage when available. It is explicit and structural: this path does not show vector search, semantic ranking, or an answerability/abstention decision over stored memories. I did not establish a separate cross-history recall path from the inspected current sources.[[context_node]][[context_builder]]

**Delete.** The checked sources document repository context files and Git-based project changes, but do not establish a memory-specific delete operation, per-memory tombstone, or deletion propagation protocol. Removing context as a repository change is possible in the file model; deletion leakage behavior was not tested or established by this review. The separately inspected task-archive API deletes archive rows by task ID, which is task-history cleanup rather than a memory deletion protocol.[[readme]][[context_node]][[archive_ops]]

**Scope isolation.** Context is tied to a repository and directory path. The assembled in-repository stages follow the root-to-node chain, so sibling paths do not enter this context string. The global VCT context is an additional shared stage; the inspected code does not establish access-control guarantees for it.[[context_node]]

**Provenance and evidence.** Git provides version history for project changes, and task archives preserve task/agent identity and commit/ref metadata. These records can identify which task and version produced a change, but the inspected model does not attach a source citation, trust state, or confidence to each statement in a `CONTEXT.md` file. Task provenance should not be read as proof that a memory claim is true.[[readme]][[archive_schema]]

## Metric-domain evidence

| Domain | Source-based evidence | Runtime result |
|---|---|---|
| Answerable retrieval and abstention | Context is assembled from path-scoped files; no scoring or abstention policy was established in the inspected path. | Unmeasured |
| Correction and stale values | Context files can be edited as repository changes; correction accuracy and stale-value handling were not evaluated. | Unmeasured |
| Deletion leakage | No memory-specific tombstone or delete protocol was established from inspected sources. | Unmeasured |
| Scope isolation | Root-to-node context assembly excludes sibling stages; global VCT access controls were not established. | Unmeasured |
| Evidence support and citation coverage | Task/commit provenance exists, but per-claim evidence links were not established. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timing or delay workload was run. | Unmeasured |
| Tokens, cost, and storage | Context stages have a configured byte cap; token, cost, and storage efficiency were not measured. | Unmeasured |

The project metric definitions, benchmark fixture, and shared execution-status record define evaluation material; they are not Genesis results.[[metrics]][[fixture]][[status]]

## Efficiency, observability, and limits

The inspected path uses explicit files and a hierarchy rather than a ranked retrieval index. Its context byte cap bounds each rendered stage, while the number of applicable stages grows with hierarchy depth. No end-to-end prompt-token, retrieval-latency, or storage measurement was collected.[[context_node]][[metrics]]

One visible failure mode is in `ContextBuilder.build_dynamic_context`: if context assembly returns an error, it falls back to a string containing the current path. The caller therefore receives a reduced context without an explicit error in that returned string. Truncation has a warning log; the reviewed code does not establish broader retrieval-quality observability.[[context_builder]][[context_node]]

This review covers public documentation and selected current upstream source paths, not a running Genesis instance. It cannot establish answer quality, context freshness, user/project authorization, global-context permissions, the behavior of uninspected recall tools, correctness after deletion, or actual performance. No runtime, benchmark, or tests were run.[[readme]][[context_node]][[context_builder]]

## Benchmark status

**Benchmark not run.** The fixture and metric files are evaluation definitions only; no measured Genesis result is recorded here. See the project [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).[[metrics]][[fixture]][[status]]

## Sources

Upstream file citations below are pinned to the reviewed full SHA. The [structured review record](../data/system-reviews/evox-genesis.json) contains the same source registry, and the [curated roster](../data/memory-systems.json) provides catalog identity.
