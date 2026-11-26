# Backboard Desktop source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 86 / Backboard Desktop / backboard-desktop  
**Listed repository locator:** [Backboard-io/Backboard-Desktop](https://github.com/Backboard-io/Backboard-Desktop)  
**Current canonical repository:** [Backboard-io/Backboard-Desktop](https://github.com/Backboard-io/Backboard-Desktop)  
**Default branch / reviewed head:** stable / 7e05905a32a587f0b17ce7507ca3528b67d22a9c  
**Review time:** 2026-11-24 23:24:13 UTC (15:24:13 PST; America/Los_Angeles).

## Identity and review pin

The curated roster places Backboard Desktop at ordinal 86 with slug `backboard-desktop`, the listed repository locator, and a pinned Atlas attribution source. I used the roster only to establish identity, locator, and attribution; its descriptions and marks were not assessment evidence. The official GitHub repository page displays the `stable` branch, and its recent-commits feed identifies full head `7e05905a32a587f0b17ce7507ca3528b67d22a9c`. This review is pinned to that revision.[[curated roster](../data/memory-systems.json)] [[repository](https://github.com/Backboard-io/Backboard-Desktop)] [[stable head](https://github.com/Backboard-io/Backboard-Desktop/commit/7e05905a32a587f0b17ce7507ca3528b67d22a9c)] [[stable commit feed](https://github.com/Backboard-io/Backboard-Desktop/commits/stable.atom)]

## Summary

Backboard Desktop is an open-source desktop agent IDE. Its README advertises memory across chats, while the inspected current CLI source shows durable, per-session conversation and request logs. In the bounded code inspected here I found no semantic memory store, profile-wide recall path, or memory mutation API; the relationship between the product claim and these session logs remains unverified.[[README](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/README.md)] [[session store](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/SessionStore.ts)] [[session runtime](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/Session.ts)]

## Who and what

The repository presents Backboard Desktop as a free MIT-licensed desktop workspace built on Code - OSS. It runs a TypeScript/Bun CLI agent process beside the IDE and describes support for coding agents, multiple sessions, browser/computer use, skills, MCP, and memory. The README names Erin Tomorri and Nihal Kodukula among contributors. This is an application and agent runtime, not a standalone memory service.[[README](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/README.md)]

## Architecture and data model

The CLI runtime keeps a `Session` projection in memory: a Backboard thread ID, assistant ID, ordered messages, todos, status, token usage, and context-window values. Messages are typed as user text, assistant text/tool calls, or tool results; the session can hydrate from a supplied thread and transcript. These objects describe conversation state rather than extracted long-term memory facts.[[runtime session](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/Session.ts)] [[message types](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/Message.ts)]

`SessionStore` creates a directory under `<baseDir>/.backboard/sessions/<sessionId>/`. It names client and server JSONL logs, metadata, worker state, checkpoints, and a pending-undo pointer; content-addressed checkpoint objects are shared beside session directories. Metadata records session ID, creation time, cwd, model, and profile. The sessions architecture doc describes sessions as groups of chats sharing workspace context and a pluggable provider model for local or remote agent hosts.[[session store](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/SessionStore.ts)] [[paths](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/config/paths.ts)] [[sessions architecture](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/src/vs/sessions/SESSIONS.md)]

## Write, update, delete, and retrieval

**Writes and provenance.** The client event log subscribes to every event on the runtime bus and appends timestamped, sequenced JSONL records tagged with session ID and source. The server event log records request/response endpoint, method, status, body, and latency; it redacts API key, authorization, and session-token headers before writing. These are event-trace provenance fields, not source citations for remembered claims.[[client event log](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/ClientEventLog.ts)] [[server event log](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/ServerEventLog.ts)]

**Ordering and durability.** The JSONL writer serializes queued appends, preserves enqueue order, and exposes `flush()` for callers that need to wait for writes. It checks whether an existing file ends with a newline before appending. The session lifecycle initializes a new session directory, can activate/resume a session directory, and acquires a file lease to coordinate access.[[JSONL writer](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/JsonlWriter.ts)] [[session lifecycle](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/SessionLifecycle.ts)]

**Update, removal, and recall.** The inspected session object supports hydration and reset; reset clears the in-memory transcript and usage, while lifecycle resume activates a session directory. I found no semantic-memory edit, delete-by-item, or query API in these inspected files. Durable logs and transcript hydration support session continuity/diagnostics, but this review did not establish a search or recall mechanism for remembered facts across chats.[[runtime session](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/Session.ts)] [[session lifecycle](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/SessionLifecycle.ts)] [[session store](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/SessionStore.ts)]

## Scope isolation and provenance

The CLI path builder places each session under the supplied base directory, and session metadata includes cwd and profile. The inspected session records do not expose a tenant or principal authorization model. Separate directories are a storage boundary visible in code, not evidence of cross-user isolation or enforcement in every integration.[[paths](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/config/paths.ts)] [[session store](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/SessionStore.ts)]

Client records carry timestamp, session ID, sequence, event type, and payload. Server records carry timestamp, session ID, sequence, endpoint, method, status/body, and latency; selected sensitive headers are redacted. The inspected logs do not attach citations or external evidence to memory claims, and the full event/request bodies can still contain conversation content.[[client event log](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/ClientEventLog.ts)] [[server event log](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/ServerEventLog.ts)]

## Source-visible efficiency and observability

The inspected persistence path uses append-only local JSONL files and serialized writes. Client logs observe the event bus; server logs store request and response latency fields; the JSON event stream also emits a full client trace to stdout for debugging and automation. These mechanisms make traces inspectable but do not establish their runtime overhead, retention, or semantic-memory performance.[[JSONL writer](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/JsonlWriter.ts)] [[client event log](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/ClientEventLog.ts)] [[server event log](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/ServerEventLog.ts)] [[JSON event stream](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/JsonEventStream.ts)]

## Project metric domains

The following are code observations only; all runtime metric domains are unmeasured. Session transcripts and event traces are not treated as semantic-memory benchmark results.[[project metric definitions](../METRICS.md)] [[benchmark status record](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This bounded inspection covered the README, sessions architecture documentation, CLI session model and message types, session path/store/lifecycle code, JSONL persistence, and client/server event tracing at the reviewed SHA. It did not inspect or execute the complete desktop app, every provider, hosted Backboard services, or all code that may implement the README's cross-chat memory claim. The exact write and retrieval behavior of that advertised memory feature, its retention/deletion controls, scope isolation, source evidence, and runtime costs therefore remain unknown.[[README](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/README.md)] [[sessions architecture](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/src/vs/sessions/SESSIONS.md)] [[session store](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/SessionStore.ts)]

## Contact-list follow-up

The official repository README lists no contact email. The official Backboard organization website's contact page publishes `hello@backboard.io`; I record it with that exact URL. No commit metadata, personal profile email, or third-party email listing was used.[[README](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/README.md)] [[official contact page](https://backboard.io/company/contact)]

## Benchmark status

**Benchmark not run.** I did not execute Backboard Desktop, any system workload, tests, or benchmarks. This record reports source observations only. Project metric definitions, status, and fixture are review protocol artifacts, not measurements of Backboard Desktop.[[project metric definitions](../METRICS.md)] [[benchmark status record](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Official repository and branch](https://github.com/Backboard-io/Backboard-Desktop)
- [Reviewed full stable head](https://github.com/Backboard-io/Backboard-Desktop/commit/7e05905a32a587f0b17ce7507ca3528b67d22a9c)
- [README.md](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/README.md)
- [Sessions architecture](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/src/vs/sessions/SESSIONS.md)
- [SessionStore](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/SessionStore.ts)
- [Session paths](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/config/paths.ts)
- [Session lifecycle](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/SessionLifecycle.ts)
- [Session and message model](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/Session.ts)
- [Message types](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/Message.ts)
- [Client event log](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/ClientEventLog.ts)
- [Server event log](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/ServerEventLog.ts)
- [JSONL writer](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/JsonlWriter.ts)
- [JSON event stream](https://github.com/Backboard-io/Backboard-Desktop/blob/7e05905a32a587f0b17ce7507ca3528b67d22a9c/backboard/cli-ts/src/core/session/JsonEventStream.ts)
- [Project metric definitions](../METRICS.md)
- [Benchmark status record](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster identity and source attribution](../data/memory-systems.json)

**Verification boundary:** bounded source inspection only; no system, tests, or benchmarks were run.
