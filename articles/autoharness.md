# autoharness

## Identity and review pin

- **System:** autoharness
- **Curated position:** 83
- **Slug:** \`autoharness\`
- **Listed repository:** [tigerless-labs/autoharness](https://github.com/tigerless-labs/autoharness)
- **Default branch:** \`main\`
- **Reviewed head:** [\`6d85325ab5ef436d1d4d52ffa82e43ea0365d144\`](https://github.com/tigerless-labs/autoharness/commit/6d85325ab5ef436d1d4d52ffa82e43ea0365d144)
- **Reviewed:** 2026-11-24 23:12:22 UTC (15:12:22 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/autoharness.md), retained only for identity, listed locator, and source attribution.

The curated roster places autoharness at ordinal 83 with listed repository \`https://github.com/tigerless-labs/autoharness\`. The official GitHub repository identifies \`main\` as the default branch; the repository page's latest commit prefix and the newest entry in its main commit feed agree on full head \`6d85325ab5ef436d1d4d52ffa82e43ea0365d144\`. Reviewed repository file links below pin to that commit. The roster and Atlas source were used for identity and attribution only, not as assessment evidence.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/tigerless-labs/autoharness)] [[main commit feed](https://github.com/tigerless-labs/autoharness/commits/main.atom)] [[reviewed head](https://github.com/tigerless-labs/autoharness/commit/6d85325ab5ef436d1d4d52ffa82e43ea0365d144)]

## Summary

autoharness is a Claude Code plugin that learns and maintains native skill folders from work in a session. It captures bounded, redacted session evidence, asks a reflector to propose changes, and uses a deterministic promoter to validate and write them. It adds an index of its own skills to the host's recall surface and tracks use-related signals for lifecycle management. This is a pinned source review, not a runtime or benchmark evaluation.[[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)] [[capture](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/capture.py)] [[promoter](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/promoter.py)]

## Who and what

The repository says it is built by Tigerless Labs and presents autoharness as a Claude Code plugin and self-learning skill layer, not a hosted memory service. Its stored objects are plain native skill folders read by the host's skill mechanism. The official organization website also lists Tigerless Labs among its projects.[[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)] [[official Tigerless website](https://tigerless.ai/)]

## Architecture and data model

A memory unit is a directory containing a native \`SKILL.md\` and optional support files under locations such as \`scripts/\`, \`templates/\`, \`assets/\`, or \`references/\`. The sidecar stores operational metadata such as \`created_by: agent\`, use/view/patch counters, and a request-count anchor. The append-only \`.ledger.jsonl\` records actions, reasons, and evidence references. Accepted session evidence is redacted again and materialized as a content-addressed Markdown file under the skill's references directory.[[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)] [[sidecar](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/sidecar.py)] [[ledger](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/ledger.py)] [[promoter](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/promoter.py)]

The system has separate global and project filesystem layers. Configuration can redirect their roots, but a skill has no tenant or principal field; the ownership marker identifies the managed pool so the plugin avoids changing user-authored and installed skills. This is filesystem and host integration, not an authorization model.[[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)] [[sidecar](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/sidecar.py)] [[skill store](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/skill_store.py)] [[validation](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/validate.py)]

The hook pipeline captures transcript data and starts a reflector that compares the episode with existing skills. The reflector proposes structured intents through the \`stage_skill\` tool; the deterministic promoter validates and applies them. The MCP tool appends intent records and does not write the skill tree itself.[[capture](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/capture.py)] [[stage_skill contract](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/stage_skill/server.py)] [[promoter](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/promoter.py)]

## Write, update, delete, and retrieval

The default reflection cadence is 50 tool calls, configurable through environment settings. The Stop hook checks a disk-backed counter, resets it once the threshold is reached, and skips child sessions to avoid recursive reflection. A SessionEnd flush handles a positive tail, while \`/learn\` offers an on-demand route through the same proposal and validation path.[[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)] [[Stop trigger](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/on_stop.py)]

Capture starts at a byte watermark, clips oversized records and the overall window, redacts the result before passing it to a child, and does not write back to the host transcript. It can also form a bounded digest from earlier exchanges. The reflector proposes create, update, patch, support-file removal, whole-skill deletion, or a suggestion for a read-only owner, with a reason and evidence slice.[[capture](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/capture.py)] [[stage_skill tool](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/stage_skill/server.py)] [[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)]

The promoter shapes and validates the proposed change before writing. It lands referenced subfiles and a redacted evidence slice first, writes \`SKILL.md\` last using atomic replacement, adds the managed ownership marker for new skills, and appends a ledger record. The code describes the skill file as the visible commit point. Invalid intents are rejected before landing.[[promoter](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/promoter.py)] [[validation](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/validate.py)] [[ledger](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/ledger.py)]

For an update, the reflector can supply a replacement body; a patch replaces a uniquely matching old string with new text. Support files are constrained to approved subdirectories and validated against references in the skill body. A whole-skill delete moves the folder into an archive outside recall, preserving its ledger and evidence; the store exposes restore, so this is reversible retirement, not secure erasure.[[stage_skill contract](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/stage_skill/server.py)] [[promoter](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/promoter.py)] [[skill store](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/skill_store.py)] [[ledger](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/ledger.py)]

At session start, autoharness adds a byte-bounded index of managed skills grouped by category and layer. The host already injects full skill descriptions, so this compact map adds ownership/category information without replacing native recall. A maintenance pass evaluates use after probation and archives dormant skills; if a mature layer exceeds capacity, it archives the lowest usage rates. No source in the reviewed path shows an independent semantic search over skill bodies.[[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)] [[session-start index](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/on_session_start.py)] [[lifecycle](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/lifecycle.py)]

## Scope isolation

The project and global layers are separate directories, and configuration can disable global management or redirect roots. The promoter and lifecycle code check the managed ownership marker before modifying skills. The inspected data and retrieval path does not enforce access by user, agent, tenant, or project identity; which layer is visible depends on the host and filesystem environment. No isolation probes were run.[[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)] [[promoter](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/promoter.py)] [[sidecar](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/sidecar.py)] [[session-start index](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/on_session_start.py)]

## Provenance and evidence

Each accepted create or update records an action and reason in the per-skill ledger and points to a redacted session slice. The promoter computes the evidence filename from the slice's SHA-256, so the model does not choose the evidence path. The ledger is append-only and can be read after archival. This preserves provenance for why a skill was created or changed, but the system does not itself attach claim-level citations to answers returned by the host.[[promoter](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/promoter.py)] [[ledger](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/ledger.py)] [[capture](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/capture.py)]

## Source-visible efficiency and observability

**Code observations, not measurements.** Capture seeks from a byte offset rather than rereading the whole transcript, then applies record and total-window caps. Session counters are disk-backed constant-size read/modify/write values; managed-skill usage counters live in small sidecars. The session-start map has a byte budget. The design has no resident daemon: lifecycle decisions run at session start. These mechanisms bound some work and persistent state, but no latency was measured.[[capture](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/capture.py)] [[counters](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/counters.py)] [[sidecar](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/sidecar.py)] [[session-start index](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/on_session_start.py)] [[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)]

Operational traces include per-run accounts for proposed, landed, and rejected intents, a last-run summary, counters, and pre-merge snapshots. This makes learning and maintenance outcomes inspectable from files, but does not supply an adjudicated quality score. The README says the plugin has zero third-party Python dependencies and uses configurable child models for reflection and curation; token usage and provider charges were not found in the reviewed record format.[[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)] [[promoter](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/promoter.py)] [[ledger](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/ledger.py)]

## Metric-domain evidence

Every domain below is **unmeasured for this review**. The table records code-visible mechanisms and gaps, not performance results.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | The plugin injects a managed-skill index alongside native host recall and tracks later skill use; this review did not run answer or abstention probes. | Unmeasured |
| Correction accuracy and stale-value rate | Reflector update/patch intents carry reason and evidence, but no fact-level temporal scoring rule was found. | Unmeasured |
| Deletion leakage | Whole-skill retirement moves data out of recall but leaves an archived copy that can be restored. | Unmeasured |
| Scope isolation | Global/project storage layers and ownership checks are visible; principal or tenant access control was not found in the skill record path. | Unmeasured |
| Evidence support and citation coverage | A redacted source slice is linked to each accepted mutation; claim-level answer citations are not part of the interface. | Unmeasured |
| Retrieval latency and write-to-recall delay | Bounded capture, fixed-size counters, and index-size limits are visible; no timings or scheduled recall probes were collected. | Unmeasured |
| Tokens, cost, and persistent storage | Plain files, sidecars, ledgers, run records, and configurable child models are source-visible; no token, charge, or corpus-attributed byte counts were collected. | Unmeasured |

The [project metric definitions](../METRICS.md), [versioned benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json) define proposed measurement methods and report \`not_run\`; they do not supply autoharness results.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded source review of selected documentation and code at the pinned head. It does not establish whether reflection produces useful skills, whether the index surfaces the right skill for a query, whether updates preserve correctness, or how the system behaves with adversarial session content and concurrent host activity. Lifecycle use rate is an operational proxy: a view can reflect browsing or curation, and a load does not prove a skill helped. The documented host is Claude Code; parity with other agent runtimes was not established.[[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)] [[capture](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/capture.py)] [[sidecar](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/sidecar.py)] [[lifecycle](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/lifecycle.py)]

The archive is reversible and retains the stored skill material. This review does not establish complete deletion from backups or other copies. Directory separation also does not provide independent user or tenant authorization; exposure depends on host and filesystem permissions.[[skill store](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/skill_store.py)] [[promoter](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/promoter.py)] [[README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)]

## Contact-list follow-up

The official [Tigerless website](https://tigerless.ai/) lists \`info@tigerless.com\` in its contact section. I also checked the pinned [repository README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md) and the root [SECURITY.md path](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/SECURITY.md); the pinned revision has no SECURITY.md file. The JSON record stores the published email and website URL.

## Benchmark status

**Benchmark not run.** No autoharness runtime, benchmark workload, build, or tests were run for this review. Project metric definitions and fixture describe planned workloads, not autoharness measurements. See [metric definitions](../METRICS.md), the [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[status](../results/initial-baselines-status.json)]

## Sources

- [Curated roster entry](../data/memory-systems.json) — ordinal, slug, listed repository, and Atlas attribution only.
- [Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/autoharness.md) — roster source attribution only.
- [Official repository](https://github.com/tigerless-labs/autoharness) — canonical repository and default branch.
- [Official main branch feed](https://github.com/tigerless-labs/autoharness/commits/main.atom) — latest commit at review time.
- [Reviewed head](https://github.com/tigerless-labs/autoharness/commit/6d85325ab5ef436d1d4d52ffa82e43ea0365d144)
- [README](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/README.md)
- [Session capture](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/capture.py)
- [Reflection trigger](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/on_stop.py)
- [Session-start index](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/on_session_start.py)
- [stage_skill tool](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/stage_skill/server.py)
- [Promoter](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/promoter.py)
- [Skill store](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/skill_store.py)
- [Validation](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/validate.py)
- [Sidecar](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/sidecar.py)
- [Ledger](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/ledger.py)
- [Lifecycle](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/lifecycle.py)
- [Counters](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/lib/counters.py)
- [Usage hook](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/src/autoharness/hook/on_skill_call.py)
- [Official Tigerless website](https://tigerless.ai/) — contact email.
- [Checked SECURITY.md path](https://github.com/tigerless-labs/autoharness/blob/6d85325ab5ef436d1d4d52ffa82e43ea0365d144/SECURITY.md) — not present at the reviewed revision.
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only source review; no autoharness execution, benchmark, tests, or build.
