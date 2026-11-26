# Cloud Alter Ego — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 131 — Cloud Alter Ego / `cloud-alter-ego`  
**Listed repository:** [SebastiaanBoon/cloud-alter-ego](https://github.com/SebastiaanBoon/cloud-alter-ego)  
**Canonical upstream:** same repository; default branch `main`; reviewed head [3f8b3bb4bfe243dacef2903e27a3f569638b622f](https://github.com/SebastiaanBoon/cloud-alter-ego/commit/3f8b3bb4bfe243dacef2903e27a3f569638b622f)  
**Review time:** 2026-11-25 08:21:07 UTC (2026-11-25 00:21:07 PST; America/Los_Angeles)

## Identity and scope

The catalog places Cloud Alter Ego at ordinal 131, gives slug `cloud-alter-ego`, and lists the explicit repository locator above. The pinned Atlas entry is retained only to attribute this curated roster identity and locator; it is not assessment evidence.[[roster](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cloud-alter-ego.md)]

GitHub’s official repository page identifies `main` as the default branch. The official main commit feed reports full head `3f8b3bb4bfe243dacef2903e27a3f569638b622f`, updated 2026-11-19T20:13:52Z; the repository page shows the corresponding abbreviated head.[[repository](https://github.com/SebastiaanBoon/cloud-alter-ego)] [[main commit feed](https://github.com/SebastiaanBoon/cloud-alter-ego/commits/main.atom)] [[reviewed head](https://github.com/SebastiaanBoon/cloud-alter-ego/commit/3f8b3bb4bfe243dacef2903e27a3f569638b622f)]

The reviewed system is the self-managed Git repository and Python hooks for Claude Code and Codex. The README describes a separate remote MCP connector as another product route; its hosted service is outside this review.[[README](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/README.md)] [[workflow](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/WORKFLOW.md)]

## Architecture and data model

The memory is a directory tree rather than a database or embedding index. Shared profile and working rules live in `identity.md` and `preferences.md`; `clients/` and `projects/` contain context READMEs, monthly journal Markdown and saved sessions. Optional `skills/` and `techniques/` hold reference material. Git is documented as the source of truth across clones.[[README](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/README.md)] [[workflow](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/WORKFLOW.md)]

SessionStart attempts to repair and pull repository state, resolves the session context, then injects the full `preferences.md` with instructions to read the active context README and newest journal. Claude Code hooks capture prompt and answer events; Codex uses a notify callback. SessionEnd saves a transcript. The documented core is plain Python with no third-party dependencies.[[session hook](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/session_start.py)] [[workflow](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/WORKFLOW.md)] [[README](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/README.md)]

Context pointers are per-session files under `.current-context.d` when a session ID is known, with a gitignored `.current-context` device default and `clients/_unsorted` fallback. Monthly journals are append-oriented text. Saved Claude transcripts have JSONL and readable Markdown forms; known secret patterns are redacted before journal or transcript content is saved.[[context CLI](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/note.py)] [[session save](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/save_session.py)] [[redaction](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/redact.py)] [[journal merge rule](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/.gitattributes)]

## Write, update, delete, and retrieval

**Write.** UserPromptSubmit and Stop hooks extract and shorten the latest user question and assistant answer, append them to the active context journal, and start Git synchronization. The agent is also instructed to add one meaningful summary line per turn with `note.py`. SessionEnd stores the transcript and commits changes. These are source-visible behaviors, not runtime results.[[workflow](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/WORKFLOW.md)] [[auto journal](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/auto_journal.py)] [[context CLI](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/note.py)] [[session save](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/save_session.py)]

**Update or correction.** `note.py` appends new lines; working rules, profile, READMEs and other context files can be edited as ordinary files. I found no structured fact-replacement, supersession or correction API in the inspected local repository paths. Journals are intended to be append-only and Git history retains earlier content.[[context CLI](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/note.py)] [[workflow](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/WORKFLOW.md)] [[README](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/README.md)] [[journal merge rule](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/.gitattributes)]

**Delete.** I found no dedicated forget/delete command in the inspected CLI and hooks. Files can be edited or removed manually, but Git history and other clones retain prior versions unless separately cleaned. SessionEnd removes the previous saved file for the same session before writing its newer, fuller transcript; this is session-save replacement, not a general memory deletion contract.[[context CLI](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/note.py)] [[session save](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/save_session.py)] [[README](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/README.md)]

**Retrieval.** There is no automatic semantic or keyword search engine in the inspected local core. SessionStart injects preferences and asks the agent to open the current context README and newest journal; further recall is agent-directed file reading. Full transcripts are archived in `sessions/` but are not described as automatically searched at startup.[[workflow](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/WORKFLOW.md)] [[session hook](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/session_start.py)] [[README](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/README.md)]

## Scope isolation

Context files are organized under client/project folders, and each session can select a folder. If a session has no pointer, selection falls back to a device-wide default or `_unsorted`. The repository may hold multiple clients and projects; instructions tell the agent which files to read, but I found no access-control or enforced read filter separating folders. This is an organizational convention, not a verified security boundary.[[context CLI](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/note.py)] [[session hook](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/session_start.py)] [[workflow](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/WORKFLOW.md)] [[working rules](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/preferences.md)]

## Provenance and evidence

Journal entries carry local timestamps and context paths; saved transcripts preserve conversation events and tool-use/result markers, while Git records repository history. Automatic journal lines are shortened, whereas saved transcripts preserve more content after redaction. The inspected format does not provide claim-level source citations or guarantee that a later answer is supported by recalled lines.[[auto journal](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/auto_journal.py)] [[context CLI](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/note.py)] [[session save](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/save_session.py)] [[redaction](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/redact.py)]

## Efficiency and observability

Hooks avoid model calls for mechanical question/answer capture, while one agent-written summary line adds token use. Journal lines are truncated; local appends and synchronization use a lock plus retry behavior. Journal files use Git's union merge. Sync health/status and error logs are present, and SessionStart warns when injected context is too long. These are implementation features; no efficiency or reliability measurements were collected.[[workflow](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/WORKFLOW.md)] [[auto journal](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/auto_journal.py)] [[session hook](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/session_start.py)] [[journal merge rule](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/.gitattributes)]

Concurrency behavior differs by file type. The repository documents union merges for journal Markdown; other files use ordinary Git merging and can conflict when devices edit the same lines. Session IDs provide distinct active-context pointers for parallel sessions on one device, but this does not enforce access isolation.[[README](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/README.md)] [[workflow](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/WORKFLOW.md)] [[journal merge rule](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/.gitattributes)]

## Contact

The official pinned README and SECURITY.md were checked for a contact email; neither publishes one. SECURITY.md directs vulnerability reports through GitHub private vulnerability reporting. The structured record stores `contact_email: null` and the exact checked URLs.[[README](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/README.md)] [[security policy](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/SECURITY.md)]

## Metric-domain evidence

All domains remain unmeasured: answerable recall and abstention; correction and staleness; deletion leakage; scope isolation; evidence support and citation coverage; retrieval latency; write-to-recall delay; token use and cost; and storage efficiency. The project definitions and synthetic fixture describe planned measurements, not Cloud Alter Ego results. Benchmark status is `not_run`.[[metric definitions](../METRICS.md)] [[planned fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This bounded review inspected the official README, workflow guide, session and journaling hooks, context CLI, redaction helper and journal merge rule at one verified revision. It did not trace every optional tool, installer mutation, platform-specific behavior or error path.

No runtime, tests or benchmark workload were run. Retrieval quality, abstention, sync reliability, write-to-recall delay, token use, cost, storage growth, deletion completeness and isolation remain unknown. Redaction covers known patterns only; the README warns it does not catch every secret. Automatically pushed journals and transcripts can therefore retain sensitive material. Per-session context markers are conventions rather than authenticated principals, and Git history, device clones and remote copies mean removing a current file does not establish complete erasure.[[README](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/README.md)] [[redaction](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/redact.py)] [[context CLI](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/note.py)] [[metric definitions](../METRICS.md)]

The structured [system review](../data/system-reviews/cloud-alter-ego.json) records source IDs, pinned links, contact status and benchmark status.

## Sources

- [Catalog roster entry and ordinal](../data/memory-systems.json)
- [Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cloud-alter-ego.md)
- [Official repository and default branch](https://github.com/SebastiaanBoon/cloud-alter-ego)
- [Official main branch commit feed](https://github.com/SebastiaanBoon/cloud-alter-ego/commits/main.atom)
- [Reviewed full head](https://github.com/SebastiaanBoon/cloud-alter-ego/commit/3f8b3bb4bfe243dacef2903e27a3f569638b622f)
- [README.md](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/README.md)
- [WORKFLOW.md](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/WORKFLOW.md)
- [tools/session_start.py](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/session_start.py)
- [tools/auto_journal.py](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/auto_journal.py)
- [tools/save_session.py](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/save_session.py)
- [tools/note.py](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/note.py)
- [tools/redact.py](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/tools/redact.py)
- [.gitattributes](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/.gitattributes)
- [SECURITY.md](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/SECURITY.md)
- [preferences.md](https://github.com/SebastiaanBoon/cloud-alter-ego/blob/3f8b3bb4bfe243dacef2903e27a3f569638b622f/preferences.md)
- [Project metric definitions](../METRICS.md)
- [Planned benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** runtime behavior, tests, benchmarks and measured metrics were not executed for this review.
