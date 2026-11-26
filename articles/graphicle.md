# Graphicle source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 270 / Graphicle / `graphicle`  
**Listed repository locator:** [Graphicle-AI/graphicle](https://github.com/Graphicle-AI/graphicle)  
**Canonical upstream:** [Graphicle-AI/graphicle](https://github.com/Graphicle-AI/graphicle)  
**Default branch / reviewed head:** main / [b0bb41407d1ffe863221181112656c28c483046c](https://github.com/Graphicle-AI/graphicle/commit/b0bb41407d1ffe863221181112656c28c483046c)  
**Review time:** 2026-11-25 21:30:39 UTC (2026-11-25 13:30:39 PST; America/Los_Angeles).

## Identity and review pin

The catalog lists Graphicle at ordinal 270 with slug `graphicle`, an explicit repository locator, and a pinned Agent Memory Atlas attribution. The catalog and Atlas record were used only for roster identity, locator, and attribution. GitHub's official repository page identifies `main` as the default branch; the official current-commit API identifies full head `b0bb41407d1ffe863221181112656c28c483046c` and commit time 2026-11-21T12:14:08Z. All implementation and documentation observations below are pinned to that head.[[roster]][[atlas]][[repo]][[head]]

## Summary

Graphicle is a local Rust application combining a code graph, project documents and captured agent sessions, reviewed memory, an MCP server, CLI, and browser app. Agent memory proposals remain drafts until an authorized review; retrieval returns cited source evidence and reviewed memories. This review describes source behavior and does not measure runtime quality.[[readme]][[mcp]]

## Who and what

The upstream README describes Graphicle as a Rust port of Graphify with memory for coding agents. It is a local program and integrated toolset rather than a hosted memory service in the inspected sources. The official project page publishes `info@karlexai.com`; I did not use commit or profile metadata to identify a contact.[[readme]][[repo]][[website]]

## Architecture and data model

Graphicle combines a parsed code graph with versioned project sources, connector documents, captured sessions, and reviewed memory. The README describes a local data folder, CLI, browser app, and MCP server, with SQLite as its default store. The MCP guide separates a full project server from a graph-only server and describes optional HTTP and workspace modes.[[readme]][[mcp]]

Memory rows are scoped to a repository and revisioned in a journal. Structured recall metadata carries an identity name, aliases, semantic scopes, state, validity interval, and optional supersession target. Those semantic scopes filter memory selection inside an authorized repository; they do not themselves grant repository or source access.[[memory]][[recall]][[structured]]

## Write, update, delete, and retrieval

**Write.** With learning enabled, agents propose drafts containing exact source quotes; the proposal path checks citations against the current authorized source set. A draft is not served by recall until an approver reviews it. Member-authored notes use a separate approval-authorized operation.[[mcp]][[memory]]

**Update and correction.** Writes carry expected revisions and append a revision record. A structured replacement requires an accessible current reviewed memory, an expected revision, matching scopes, active state, and a valid effective time; the operation closes the old validity interval where the replacement begins.[[memory]][[structured]]

**Delete and forgetting.** The deletion implementation handles connector documents, whole connectors, and projects. It removes controlled derived artifacts, checks for residue, and records hash-chained receipts. The source explicitly excludes prior backups, provider retention of requests already sent, and copies exported before deletion; residual content is reported.[[deletion]]

**Retrieval.** The memory selector defaults to exact whole-word matching against declared names and aliases. An explicit lexical mode ranks positive term overlap with inverse-document-frequency weighting; both modes apply scope, state, and valid-time eligibility before truncating to the requested limit. The integrated recall path can combine code, documents, sessions, and reviewed memories into source-cited context within a caller-set token budget, without a model call inside the MCP tool.[[recall]][[mcp]][[readme]]

## Scope isolation

Memory and source reads are associated with a repository and authorized credential. A project connection keeps recall and source reads within that project, while graph tools may target another project the key can access. Workspace connections can search across authorized projects, defaulting to at most eight; a local server uses the saved key, which can be the owner's credential. Therefore, deployment access configuration determines the effective boundary, and code presence alone is not a measured isolation guarantee.[[mcp]][[memory]][[metrics]]

## Provenance and evidence

Citation quotes are required to occur in the current authorized source set. The store records source hashes and dependency links; source file reads check SHA-256, and dependent memories can become stale when their evidence changes. Recall can return original evidence alongside selected memory, but the response says semantic entailment has not been verified. Quote membership and provenance metadata should not be read as proof that a paraphrased claim is supported.[[memory]][[structured]][[mcp]]

## Efficiency and observability

The memory selector has an explicit record cap, query limit, and validated name/scope bounds. Recall can apply a token budget and skips repeated excerpts when requested. Retrieval packets include selection and evidence data, temporal inputs, and counts of withheld stale or unreviewed memories; queued job status and model usage are available through a status tool. These source-described mechanisms are not performance measurements. No latency, write-to-recall, token, cost, or storage samples were collected.[[recall]][[mcp]][[structured]][[metrics]]

## Metric-domain evidence

Every project benchmark domain remains **unmeasured** for this review. The project's [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the workload and record `not_run`; they are not Graphicle outcomes.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Identity/lexical selectors and cited recall packets are present; no responses were scored. | Unmeasured |
| Correction and stale values | Revision checks and effective-time supersession are present; no correction probes were run. | Unmeasured |
| Deletion leakage | Controlled deletion and receipts are present; no post-deletion probes were run. | Unmeasured |
| Scope isolation | Project and credential access controls are documented; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Exact source quote checks are present; semantic entailment is explicitly not verified, and no claims were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No runtime timing samples were collected. | Unmeasured |
| Tokens, cost, and storage | Context budgets and a local store are documented; no resource measurements were collected. | Unmeasured |

## Limits and unknowns

The memory selector finds declared identities or lexical overlaps; inspected source does not make it an entailment verifier. The MCP guide describes materially different project and workspace access boundaries, and warns in effect that workspace exposure follows the credential's allowed projects. Runtime isolation, practical recall quality, and exact external deletion behavior were not tested here.[[recall]][[structured]][[mcp]][[deletion]]

The deletion contract expressly excludes earlier backups, provider retention, and prior exports. The official README reports results for identified pre-release builds and configurations; those claims are not measured results for the reviewed main head. This review did not run Graphicle, its tests, or benchmarks.[[deletion]][[readme]][[status]]

## Benchmark status

**Benchmark not run.** No Graphicle executable, test suite, or benchmark workload was run. The official README's pre-release comparisons are attributed upstream claims and do not establish results for the reviewed commit. See [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) for evaluation definitions and project status; none is a Graphicle result record.[[readme]][[metrics]][[fixture]][[status]]

## Contact

The official Graphicle project website publishes `info@karlexai.com`. The pinned README and SECURITY.md were also checked. No email was inferred from commit/profile metadata or a third-party directory.[[website]][[readme]][[security]]

## Sources

Upstream file links are pinned to `b0bb41407d1ffe863221181112656c28c483046c`. The Atlas link is retained only for curated roster attribution, not as assessment evidence. See the structured [Graphicle review record](../data/system-reviews/graphicle.json) and [curated catalog](../data/memory-systems.json).
