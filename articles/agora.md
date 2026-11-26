# Agora

**Reviewed from code** at `main` revision `100810d9096896d5be1bf25dd0f546647c575bca`. Reviewed 2026-11-24 19:32:41 UTC (11:32:41 PST, America/Los_Angeles). **Benchmark not run.**

## Summary

Agora is a self-hosted agent collaboration platform. For hosted agent sessions, it stores the agent’s final-turn summary and uses it as a fallback context for a later wake when the native CLI session cannot be resumed. The summary is a compact, agent-authored text field; it is not a separately searchable memory store.

## Who and what

The official README presents Agora as a provider-agnostic agent collaboration platform. It includes a server, web and mobile clients, an MCP server, and a host process that wakes local agent CLIs. The reviewed memory behavior belongs to the hosted-session subsystem, rather than a standalone memory library or service. ([README](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/README.md?plain=1))

## Architecture and data model

A hosted session belongs to an agent bot in a channel and is stored in `agent_sessions`. The migration defines one `summary` text field and a `native_session_id`; it also ties the session to its server, channel, bot, and profile. The current summary is therefore attached to a session record, not represented as individually addressable facts. ([session schema](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/src/db/migrations/037_agent_sessions.sql?plain=1))

The host builds a wake prompt from the claimed session and inbox. It includes the prior summary only when there is no native session ID, labels it “untrusted,” and puts its lines in a quoted block. The documentation says the host resumes the agent’s own CLI session when possible; otherwise it starts fresh with the summary from the previous wake. ([host prompt](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/agora-host/src/prompt.ts?plain=1), [session guide](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/docs/agent-sessions.md?plain=1))

## Write, update, delete, and retrieval

On successful CLI completion, the host reports the parsed summary with the run’s native session ID and usage. The server stores the per-run summary on `agent_runs`, then updates the session summary with `COALESCE(new_summary, existing_summary)`: a non-null returned summary replaces the prior one, while a null summary leaves it in place. The claim path sends the stored summary back to the host for the next wake. ([host scheduler](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/agora-host/src/scheduler.ts?plain=1), [completion and claim](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/src/lib/agent-runs.ts?plain=1))

Adapters accept structured JSON summaries from supported CLI outputs; the ACP parser also falls back to the final text when it is not a JSON summary. Summary values are capped at 16,000 characters. The source shows parsing and storage, not whether the summary is complete or accurate. ([CLI adapters](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/agora-host/src/adapters.ts?plain=1), [ACP session parser](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/agora-host/src/acp/session.ts?plain=1))

There is no separate summary search or item-level edit API in the paths reviewed. A successful workspace checkpoint restore clears the native session ID and replaces the summary with a fixed instruction to read channel history. The `/clear` command similarly clears the native session ID and writes a fixed summary. The session table’s foreign keys cascade on server, channel, bot, or profile deletion; a standalone summary deletion operation was not found in this bounded inspection. ([workspace restore](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/src/routes/workspace-review.ts?plain=1), [session commands](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/src/lib/session-commands.ts?plain=1), [session schema](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/src/db/migrations/037_agent_sessions.sql?plain=1))

## Scope isolation

The session row identifies a bot, channel, profile, and server, and the claim is for one session. Documentation describes a channel session as one agent in one channel, with task-card and subtask sessions scoped to their own thread. The summary is read through that claimed session. These are source-visible scope boundaries; this review did not run cross-channel, cross-user, or cross-session isolation probes or audit every authorization and database policy. ([session schema](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/src/db/migrations/037_agent_sessions.sql?plain=1), [session guide](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/docs/agent-sessions.md?plain=1), [claim path](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/src/lib/agent-runs.ts?plain=1))

## Provenance and evidence

The summary comes from the agent’s final CLI response, which the host parses and sends to the server. The schema stores plain text without source-document IDs, quotations, claim-level citations, an evidence state, or an independently adjudicated provenance record. The wake prompt explicitly treats the stored summary as untrusted data. ([CLI adapters](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/agora-host/src/adapters.ts?plain=1), [host prompt](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/agora-host/src/prompt.ts?plain=1), [session schema](https://github.com/CaffeinatedSoftwareLLC/agora/blob/100810d9096896d5be1bf25dd0f546647c575bca/src/db/migrations/037_agent_sessions.sql?plain=1))

## Metric-domain evidence

These are **source observations**, not measured results:

- **Recall and abstention:** fallback retrieval inserts the single prior summary into a fresh-session prompt. No indexed query, answerability detector, or summary recall scoring was identified in the reviewed path.
- **Correction and staleness:** a returned non-null summary replaces the previous session summary; a null value preserves it. No correction history or stale-claim adjudication is stored in this summary field.
- **Deletion:** restore and `/clear` replace the summary with a fixed context instruction. Session ownership rows have cascading foreign keys. Deletion leakage, backups, and erasure behavior were not tested.
- **Scope:** session identifiers and channel/thread relationships are represented in code and schema. Isolation leak rate is unmeasured.
- **Evidence:** summaries have no citation or source-pointer field in the inspected schema. Evidence support and citation coverage are unmeasured.
- **Efficiency and observability:** the summary is bounded to 16,000 characters and stored in one text field; the host sends it only on the fresh-session path. Run token usage is recorded separately, but no summary-specific token, cost, storage, or retrieval-latency measurement was collected.

The project’s metric definitions are in [METRICS.md](../METRICS.md), with fixture [memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json) and status record [initial-baselines-status.json](../results/initial-baselines-status.json).

## Limits and unknowns

This review inspected the hosted-session summary flow at the pinned repository head, including session schema, claim/complete handling, host prompt construction, output parsing, and restore/clear paths. It did not inspect every adapter or all session authorization and deletion paths. The source cannot establish summary factual accuracy, coverage of prior work, whether CLI-native resume succeeds in practice, end-to-end recall quality, or effective isolation. No runtime, benchmark, or tests were run.

## Benchmark status

**Benchmark not run.** No Agora runtime or benchmark workload was executed. All metric domains remain unmeasured for this system. The project metric definitions and initial status record describe the evaluation protocol and status, not Agora results.

## Sources

Repository source citations are pinned to the reviewed full SHA. The curated roster entry is retained only for identity and attribution; its descriptions and marks were not used as assessment evidence. See the structured record [agora.json](../data/system-reviews/agora.json).
