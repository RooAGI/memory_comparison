# CLIO source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 129 / CLIO / clio  
**Listed repository locator:** [SyntheticAutonomicMind/CLIO](https://github.com/SyntheticAutonomicMind/CLIO) (explicit)  
**Catalog source attribution:** [Atlas report at catalog revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/clio.md); used for roster identity and locator attribution only  
**Current canonical repository:** [SyntheticAutonomicMind/CLIO](https://github.com/SyntheticAutonomicMind/CLIO)  
**Default branch / reviewed head:** main / [4babd7be9dc15acc894d4089ff4eb840ad3e10cf](https://github.com/SyntheticAutonomicMind/CLIO/commit/4babd7be9dc15acc894d4089ff4eb840ad3e10cf)  
**Review time:** 2026-11-25 08:17:43 UTC (2026-11-25 00:17:43 PST; America/Los_Angeles). GitHub's official main feed reports this head at 2026-11-17T23:53:30Z; the repository page identifies `main` as the default branch.  
**Published contact:** No email was found in the official pinned [SECURITY.md](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/SECURITY.md), which was checked. Its reference to the maintainer's GitHub profile was not used. The JSON records null and this exact checked URL.

## Identity and scope

The catalog places CLIO at ordinal 129, slug `clio`, and lists `https://github.com/SyntheticAutonomicMind/CLIO` with explicit locator status. It attributes the roster entry to the pinned Atlas report linked above. Atlas was used only for identity and locator attribution; this assessment is based on official upstream documentation and source. [[roster entry](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/clio.md)]

GitHub identifies the public canonical repository and default branch `main`. The official main feed gives full head `4babd7be9dc15acc894d4089ff4eb840ad3e10cf` and update time 2026-11-17T23:53:30Z. The repository page shows the same head prefix and default branch. Upstream source and documentation links below pin the full reviewed SHA. [[repository](https://github.com/SyntheticAutonomicMind/CLIO)] [[main branch history](https://github.com/SyntheticAutonomicMind/CLIO/commits/main.atom)] [[reviewed head](https://github.com/SyntheticAutonomicMind/CLIO/commit/4babd7be9dc15acc894d4089ff4eb840ad3e10cf)]

CLIO is a Perl terminal agent and agent harness. Its memory features are local project and session state integrated into the agent context and tool surface, rather than a standalone hosted memory service. The README describes multi-provider model support; memory data is kept under the local CLIO project data directory. [[official README](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/README.md)] [[memory architecture guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)]

## Architecture and data model

The memory guide describes three related forms of state: short-term memory (STM), a sliding active message window; YaRN, a durable thread archive with compressed summaries for context recovery; and long-term memory (LTM), a project knowledge base. Session-level key/value notes and cross-session transcript recall are additional operations. The memory guide names `ShortTerm.pm`, `YaRN.pm`, and `LongTerm.pm`; the current source implements the LTM store and memory tool separately. [[memory architecture guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)] [[LTM implementation](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Memory/LongTerm.pm)] [[memory tool](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Tools/MemoryOperations.pm)]

LTM is a JSON structure with categories for discoveries, problem-solution pairs, code patterns, workflows, failures, and context rules, plus metadata. Entries may carry confidence, timestamps, examples or application counts, and trust/corroboration fields. The guide places the file at `~/.clio/projects/<uuid>/ltm.json`; PathResolver obtains a project UUID from `.clio/project_uuid` and resolves project data paths. The memory tool also exposes session key/value storage under the same project data area and session transcript search. [[memory architecture guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)] [[LTM implementation](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Memory/LongTerm.pm)] [[memory tool](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Tools/MemoryOperations.pm)] [[project path resolver](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Util/PathResolver.pm)]

## Write, update, delete, and retrieval

**Write.** LTM entries are added through explicit memory operations such as `add_discovery`, `add_solution`, and `add_pattern`; the implementation documentation says agents record significant findings rather than relying on heuristic automatic capture. LTM persistence uses atomic temporary-file writes followed by rename, and the in-memory store marks itself dirty for saves. Session notes have separate key/value store operations. [[memory architecture guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)] [[LTM implementation](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Memory/LongTerm.pm)] [[memory tool](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Tools/MemoryOperations.pm)]

**Update and correction.** `update_ltm` finds matching entries and replaces their text. Rewriting an entry resets it to unverified and clears corroboration sources/count, so prior trust does not automatically transfer to changed content. Re-import or correction behavior for arbitrary session transcripts is not established by the selected sources. [[memory architecture guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)] [[LTM implementation](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Memory/LongTerm.pm)] [[memory tool](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Tools/MemoryOperations.pm)]

**Delete and maintenance.** Session memory has a delete-by-key operation. The reviewed LTM tool surface exposes pruning but no direct delete-by-entry operation; prune removes old or low-confidence entries subject to tier-specific retention. The guide describes unverified entries aging out sooner than trusted entries. I did not establish a complete erasure path for LTM or session transcript history from backups or other copies. [[memory architecture guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)] [[LTM implementation](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Memory/LongTerm.pm)] [[memory tool](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Tools/MemoryOperations.pm)]

**Retrieval.** ContextBuilder scores LTM entries against the current user input, active task, and unresolved state using lexical keyword overlap. The documented defaults select entries above a relevance threshold, cap injection at five, and apply a minimum confidence floor; entries are rendered into dynamic context rather than dumped wholesale into a static system prompt. `recall_sessions` searches past session transcripts and returns scored excerpts; session key/value memory has retrieve, search, and list operations. These are source-visible behaviors, not measured recall results. [[memory architecture guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)] [[context builder](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Core/ContextBuilder.pm)] [[memory tool](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Tools/MemoryOperations.pm)]

## Scope isolation, provenance, and evidence

Project data is addressed by a UUID stored in the project's `.clio/project_uuid`, with LTM and memory paths resolved beneath the project data directory. The path resolver treats the launch directory as the project root and documents explicit project boundaries. This gives a project-scoped storage design, but this review did not run cross-project or adversarial isolation tests. [[memory architecture guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)] [[project path resolver](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Util/PathResolver.pm)]

The LTM trust tier distinguishes single-source unverified entries from entries corroborated by distinct `agent:session` identities; corroboration records those identities, and explicit promotion is also documented. The current runtime path constrains supplied source identities against the active runtime identity. This is provenance about who corroborated a memory, not a source citation for each factual claim. No claim-to-evidence ledger or answer citation guarantee was identified in the inspected paths. [[memory architecture guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)] [[LTM implementation](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Memory/LongTerm.pm)] [[memory tool](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Tools/MemoryOperations.pm)]

## Efficiency and observability

The design keeps memory local in JSON files and session state, uses atomic writes for persistent stores, scores a bounded number of LTM entries, and exposes LTM statistics. ContextBuilder uses token estimates and a bounded selection policy to manage prompt content. The guide describes this as a way to limit injected context and preserve session continuity; this review collected no latency, token, cost, or storage measurements. [[memory architecture guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)] [[LTM implementation](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Memory/LongTerm.pm)] [[context builder](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Core/ContextBuilder.pm)]

## Metric-domain evidence

| Domain | Review status | Evidence |
|---|---|---|
| Answerable recall and abstention | Unmeasured | LTM scoring and transcript search are implemented; no answerability or abstention probes were run. [[context builder](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Core/ContextBuilder.pm)] |
| Correction accuracy and staleness | Unmeasured | LTM text update resets trust; no correction or stale-memory probe was run. [[LTM implementation](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Memory/LongTerm.pm)] |
| Deletion leakage | Unmeasured | Session key deletion and LTM pruning are exposed; no deletion leakage or residual-copy audit was run. [[memory tool](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Tools/MemoryOperations.pm)] |
| Scope isolation | Unmeasured | Project UUID path resolution is implemented; no cross-project isolation probe was run. [[project path resolver](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Util/PathResolver.pm)] |
| Evidence support and citation coverage | Unmeasured | Corroboration identity is recorded, but answer-level evidence support was not adjudicated. [[LTM implementation](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Memory/LongTerm.pm)] |
| Retrieval latency | Unmeasured | No retrieval timing workload was run. [[metric definitions](../METRICS.md)] |
| Write-to-recall delay | Unmeasured | No timed write-and-recall workload was run. [[metric definitions](../METRICS.md)] |
| Tokens and cost | Unmeasured | No token or cost measurement was collected. [[metric definitions](../METRICS.md)] |
| Storage efficiency | Unmeasured | No database, JSON, or session storage size measurement was collected. [[metric definitions](../METRICS.md)] |

**Benchmark status:** not run. Project metric definitions and the benchmark-status record are contextual links, not CLIO results; the fixture is a planned workload and was not executed. [[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

- This is a bounded inspection of the official README, memory guide, LTM store, memory tool, context builder, and project path resolver at one verified SHA. It did not cover every memory integration, migration, failure mode, or session storage implementation.
- No CLIO runtime, tests, or benchmark workload was run. Runtime reliability, recall quality, correction quality, deletion completeness, project isolation under edge cases, and all metric values remain unknown.
- The documentation describes trust promotion, pruning, and recovery behavior; this review did not verify those claims with executions.
- The reviewed memory operations expose session key deletion and LTM pruning, but no direct LTM item deletion operation was found in the inspected tool contract. Complete erasure from backups or every persisted copy remains unknown.
- Corroboration tracks distinct agent/session identity, but does not establish the factual correctness of the memory or provide citations supporting generated answers.

## Sources

- [Official README at reviewed revision](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/README.md)
- [Memory architecture guide at reviewed revision](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/docs/MEMORY.md)
- [LTM implementation at reviewed revision](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Memory/LongTerm.pm)
- [Memory operations tool at reviewed revision](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Tools/MemoryOperations.pm)
- [ContextBuilder at reviewed revision](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Core/ContextBuilder.pm)
- [Project PathResolver at reviewed revision](https://github.com/SyntheticAutonomicMind/CLIO/blob/4babd7be9dc15acc894d4089ff4eb840ad3e10cf/lib/CLIO/Util/PathResolver.pm)
- [Curated roster entry](../data/memory-systems.json)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution-status record](../results/initial-baselines-status.json)
- [Benchmark fixture (planned workload)](../fixtures/memory-benchmark-v1.json)
