# fx source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 249 / fx / `fx`  
**Listed repository locator:** [vercel-labs/fx](https://github.com/vercel-labs/fx)  
**Canonical upstream:** [vercel-labs/fx](https://github.com/vercel-labs/fx)  
**Default branch / reviewed head:** main / [75fb0649d45ce552a749a50d60c36c14358973db](https://github.com/vercel-labs/fx/commit/75fb0649d45ce552a749a50d60c36c14358973db)  
**Review time:** 2026-11-25 20:45:45 UTC (2026-11-25 12:45:45 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists fx at ordinal 249, slug `fx`, with the explicit repository locator `https://github.com/vercel-labs/fx`. Its pinned Agent Memory Atlas entry is recorded only as roster attribution; Atlas descriptions and capability marks were not used as assessment evidence. The official GitHub repository page shows the default branch as main. GitHub's official main commit feed identifies the full current head SHA; the inspection is pinned to that commit.[[catalog]][[atlas]][[repo]][[head]]

## Summary

The current fx repository describes a native Zig coding agent. Its persistent memory is primarily resumable conversation history: fx records sessions locally, compacts older turns to fit the model context, and leaves the originals available for later lookup. The inspected source does not establish a separate store of durable user facts. This is a source review only; no runtime quality or efficiency was measured.[[readme]][[session-log]][[compactor]]

## Who and what

The upstream README describes fx as a small, open, embeddable coding agent distributed as one native binary written in Zig. It supports terminal, script, editor, and library use. The curated entry's Atlas attribution is retained only to identify the roster record; no Atlas profile claims inform this assessment.[[readme]][[catalog]][[atlas]]

## Architecture and data model

The README says fx saves conversations under `~/.fx/sessions/` and resumes them with `fx -c`. When context fills, older turns are compacted, while their full text stays on disk for the agent to look up later. This provides continuity for past conversations; it is not described as a user-managed set of independent facts.[[readme]]

The inspected session store uses per-session directories. The event log source names `events.jsonl`, a `session.json` manifest, permissions data, and a recovery checkpoint. Conversation events carry sequence numbers and are replayed into session history. Session identifiers are validated before being used as directory names, and the implementation declares private file and directory permissions.[[session-log]][[session-store]][[layout]]

The store supports session discovery, loading, read-only inspection, resuming, and forking. Session state includes workspace metadata and conversation history. Separately, the built-in context provider assembles project instruction files and other prompt context for the agent.[[session-store]][[context]]

The compactor selects an older history window, keeps recent turns intact, asks a model for a summary, and saves a checkpoint. It also saves records for turns, tool calls, and earlier compactions so the agent can search older material. The checkpoint replaces earlier turns in the active model context; the raw conversation remains in the session archive.[[compactor]][[session-log]]

## Write, update, delete, and retrieval

**Write and update.** fx writes session events as conversations and tool activity occur. Compaction adds a summary checkpoint; it does not edit the archived conversation into corrected facts. I did not find a supported per-fact create or update API in the inspected sources.[[readme]][[session-log]][[compactor]]

**Delete.** The session store source inspected here covers discovery, loading, resume, and fork. I did not identify a reviewed session-delete or per-record correction operation, so deletion semantics for stored sessions and memory facts remain unknown.[[session-store]]

**Retrieval.** Users can resume a session, and the compactor exposes phrase search over saved turns, tool calls, earlier compactions, and conversation archives. This is lexical lookup over archived conversation, not semantic retrieval over a separate fact database. This review did not run a recall query or assess whether search finds relevant evidence.[[readme]][[session-store]][[compactor]]

## Scope isolation

Sessions live in the user's local fx profile and include workspace metadata for project-oriented continuation. The inspected source validates session IDs and organizes each session separately, but this review did not establish a hard tenant boundary or test isolation across workspaces or users. The README's project continuation behavior is not a security guarantee.[[readme]][[session-store]][[layout]]

## Provenance and evidence

The session archive preserves an ordered conversation and tool activity, so past statements can be associated with the session and surrounding execution. The compactor's lint stage checks summary notes and references against saved turns and tool calls and marks content it cannot confirm. These are provenance aids for conversation recall, not a general model of truth or source citations attached to every fact.[[session-log]][[compactor]]

## Efficiency and observability

Compaction is intended to keep the active conversation within the model context while retaining raw history for later lookup. The README describes compaction and session files, and the compactor reports progress and records bounded trace events. These mechanisms do not establish retrieval latency, summary quality, token savings, storage efficiency, or reliability; no measurements were collected.[[readme]][[compactor]][[session-log]]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for fx in this review. Source code and documentation are not benchmark results. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the project's evaluation materials, not fx measurements.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Session resume and phrase lookup are available; no answer quality or abstention was scored. | Unmeasured |
| Correction and stale values | Session transcripts and compaction checkpoints preserve history; no fact correction workflow was assessed. | Unmeasured |
| Deletion leakage | No deletion path or post-delete probe was assessed. | Unmeasured |
| Scope isolation | Workspace metadata and local session storage are present; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Conversation/tool context and summary checks exist; no generated evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timing samples were collected. | Unmeasured |
| Tokens, cost, and storage | Compaction is a context-bounding design; token, cost, and storage use were not measured. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the current README, session event/store/layout code, compaction pipeline, and context builder. It did not inspect every command or all cleanup paths, and it did not run fx, tests, or benchmarks. The source review cannot show whether compaction retains useful details, whether phrase search returns the best historical evidence, or how the system behaves under storage failure or concurrent access.[[readme]][[session-log]][[session-store]][[compactor]][[context]]

The saved conversation can contain prompts and tool context. Local permission bits are declared in source, but encryption, backup, recovery from corruption, and removal from external copies were not tested.[[session-log]][[session-store]]

## Benchmark status

**Benchmark not run.** No fx runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the project protocol and shared status, not fx results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README was checked for a published contact email and none was present. The structured record stores `contact_email: null` and the checked URL. No address was inferred from commit/profile metadata or obtained from a third-party directory.[[readme]]

## Sources

Repository file citations are pinned to the verified full SHA, except the repository identity page, current-head Atom feed, and Atlas roster attribution. The Atlas source supports curated identity/locator attribution only. See the structured record [fx.json](../data/system-reviews/fx.json) and the [curated roster](../data/memory-systems.json).
