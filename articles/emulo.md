# Emulo

## Identity and review pin

- **Catalog position:** 220, “Emulo”; slug `emulo`.
- **Listed repository:** [ohad6k/emulo](https://github.com/ohad6k/emulo); roster status is explicit. The pinned Atlas entry is used only for roster identity and locator attribution.
- **Canonical upstream:** [ohad6k/emulo](https://github.com/ohad6k/emulo), default branch `main`. The official GitHub repository page and Git remote identify this repository; `git ls-remote --symref` reported `HEAD -> refs/heads/main` and full head `5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe`. A shallow checkout of `main` resolved to the same SHA.
- **Reviewed:** 2026-11-25 19:14:26 UTC (2026-11-25 11:14:26 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) supplies ordinal, name, slug, listed repository, and roster attribution. The pinned [Atlas entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/emulo.md) supports that attribution only; it is not assessment evidence.

## Summary

Emulo mines user-authored coding-agent session messages into dated, quote-backed personal instruction profiles. It has a local extractor/redactor, a manual chunk-and-agent path, and a plugin/bootstrap path that validates model-produced evidence reports and activates a versioned profile. Retrieval loads a whole work profile and optionally one domain profile; it is not relevance-ranked memory search. No quality or performance measurement was run for this review.

## Who and what

The official [README](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/README.md) describes Emulo as a local Python tool and agent integration for mining Claude Code, Codex, Copilot CLI, OpenCode, and Google Antigravity logs. The maintainer attribution in the README names Ohad Krispin. The project README presents two distinct paths: a command-line path that exports chunks for an agent to turn into a profile, and an agent plugin/bootstrap path that runs a staged workflow and activates a profile.

## Architecture and data model

The source is centered on a stdlib Python extractor in `emulo.py`, supported by skills, plugins, and a separate Autopilot package. The extractor selects recognized human-authored messages, filters injected context and pasted logs, redacts common secrets and personal information, deduplicates long repeated messages, and writes session/date-labeled text. Redaction is documented as best-effort, and the README recommends inspecting private output before sharing it.[[extractor](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/emulo.py)] [[profile flow](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/docs/PROFILE-FLOW.md)] [[security notes](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/SECURITY.md)]

The manual path writes a corpus, session-boundary chunks, stats, and `RUN_ME.md`; a coding agent authors `you.md`. The plugin/bootstrap path stores redacted segments, reports, reductions, runs, and active profile versions under `~/.emulo` (or `EMULO_HOME`). Its profile pack contains domain profiles, a quote appendix, card, and manifests. Activation stages a version directory and changes a current-version pointer after validation.[[readme](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/README.md)] [[extractor](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/emulo.py)]

## Write, update, delete, and retrieval

**Write.** The local extractor reads supported session formats, keeps recognized human turns, strips selected harness/injected content, redacts, and emits date-tagged session blocks. In the manual workflow the user hands these chunks to an agent, which writes the Markdown profile. In the plugin flow, preflight creates an explicit plan; the workflow expects approval before model work, worker reports are validated, and a reducer assembles a complete profile pack. README claims for the agent workflow are documented behavior; no mining run was performed here.[[extractor](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/emulo.py)] [[mine skill](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/skills/mine/SKILL.md)] [[readme](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/README.md)]

**Update and delete.** The profile is a set of Markdown files that can be reviewed and edited in the manual path; the install command copies or appends the selected profile for supported agent hosts. Plugin-managed active files are checked against their manifest, so direct edits are refused by the loaders; the documented route to change them is to mine again. The docs describe removing the manual `emulo-out/` folder or the complete local `~/.emulo` store. I found no per-rule delete API, no tombstone mechanism, and no remote deletion protocol for the local profile store. The user can remove the local files, but this review did not verify secure erasure or provider-side retention of text previously sent to a hosted model.[[profile flow](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/docs/PROFILE-FLOW.md)] [[extractor](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/emulo.py)]

**Retrieval.** The installed profile is instruction text, not a vector or keyword-indexed store. Native skills load the work profile and, for design, writing, or video tasks, the corresponding additional domain file. The MCP server exposes `load_emulo_profile` and returns the selected profile text; it reports a recovery instruction if there is no active profile. The docs say the standalone `RUN_ME.md` profile is not served through this MCP/plugin path until activated through the agent mining flow.[[readme](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/README.md)] [[extractor](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/emulo.py)]

**Scope isolation.** The documented store is local to one user home or configured `EMULO_HOME`; work, design, writing, and video are separate profile domains. I found no tenant, project, or session authorization boundary on profile reads. A configured directory and a domain selector are organization/layout choices, not an access-control proof. The user or host must secure local files and any agent context that receives the profile.[[profile flow](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/docs/PROFILE-FLOW.md)] [[extractor](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/emulo.py)]

**Provenance and evidence.** The mining flow associates short dated verbatim quotes with known session identifiers; the README describes checks for quote presence, distinct-session support, contradictions, and generic rules. The standalone `emulo verify` command checks whether quoted spans can be found in the mined corpus and flags quotes found in only one session. These mechanisms support traceability to captured user messages, not proof that an inferred rule is true or still current. The README says the manual `RUN_ME.md` path relies on agent instructions for profile quality and its verifier only checks quotes against the corpus.[[readme](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/README.md)] [[extractor](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/emulo.py)] [[profile flow](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/docs/PROFILE-FLOW.md)]

**Efficiency and observability.** The source uses content hashes for segments/reports and caches unchanged mining work; README says an identical plugin update plans zero additional Emulo mining passes. Its displayed selected-token counts and planned worker/reducer passes are planning values, not provider billing or measured cost. The local usage report counts selected message patterns and prints supporting messages. I found no basis here for latency, token billing, storage-efficiency, or operational telemetry claims; none was measured.[[readme](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/README.md)] [[extractor](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/emulo.py)] [[profile flow](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/docs/PROFILE-FLOW.md)]

## Metric-domain evidence

- **Answerable retrieval and abstention:** domain files can be loaded, but relevance ranking, answerability, and abstention were not measured.
- **Correction and stale values:** profile revision/remine is available in documentation; per-rule correction semantics and stale-value rates were not measured.
- **Deletion leakage:** local profile and cache removal is documented; no deletion probes or secure-erasure checks were run.
- **Scope isolation:** local path and domain organization are visible in source/docs; no cross-user or cross-project isolation workload was run.
- **Evidence support and citation coverage:** dated source-session quotes are part of the profile workflow; support quality and citation coverage were not measured.
- **Retrieval latency and write-to-recall delay:** not measured.
- **Tokens, cost, and storage efficiency:** no provider token, billing, or storage measurements were collected.

See the project's [metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and [benchmark fixture](../fixtures/memory-benchmark-v1.json). These comparison documents are not Emulo results.

## Contact

No contact email was found in the official pinned [README](https://github.com/ohad6k/emulo/blob/5b6745f0ecbb11027d5dfdc3c97778b0fbd273fe/README.md). The exact checked URL is recorded in [emulo.json](../data/system-reviews/emulo.json); no commit/profile metadata or third-party directory was used.

## Limits and unknowns

This is a source review at the verified `main` head. I did not run Emulo, its tests, or benchmarks. Source inspection cannot establish rule quality, retrieval usefulness, robustness to malformed or adversarial logs, hosted-model retention, tenant safety, file-removal guarantees, latency, actual provider cost, or scale. The README itself distinguishes changed model output from evidence of improved output and reports mixed profile comparisons; those are project-reported observations, not measurements made for this review.

## Benchmark status

**Benchmark not run.** No Emulo runtime, tests, or benchmarks were run. See the [project metrics](../METRICS.md), [shared status](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and SHA-pinned upstream links are recorded in [emulo.json](../data/system-reviews/emulo.json). The [curated roster](../data/memory-systems.json) and [pinned Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/emulo.md) support identity and locator context only.
