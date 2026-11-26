# Attune AI source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 74 / Attune AI / attune-ai  
**Listed repository locator:** [Smart-AI-Memory/attune-ai](https://github.com/Smart-AI-Memory/attune-ai)  
**Current canonical repository:** [Smart-AI-Memory/attune-ai](https://github.com/Smart-AI-Memory/attune-ai)  
**Default branch / reviewed head:** main / d076f7d31bccef75915ff988a949f6e2069d6c7d  
**Review time:** 2026-11-24 21:48:26 UTC (13:48:26 PST; America/Los_Angeles).

## Identity and review pin

The curated roster places Attune AI at ordinal 74, gives the listed locator above, and attributes the entry to the Agent Memory Atlas catalog source. That roster was used only for identity and source attribution; Atlas descriptions, marks, and layout were not used as assessment evidence. The official repository page identifies main as the default branch. The official commits/main Atom feed reports full head d076f7d31bccef75915ff988a949f6e2069d6c7d, updated 2026-11-20T21:54:17Z; the repository page shows the same latest commit prefix.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/Smart-AI-Memory/attune-ai)] [[main commit feed](https://github.com/Smart-AI-Memory/attune-ai/commits/main.atom)] [[reviewed commit](https://github.com/Smart-AI-Memory/attune-ai/commit/d076f7d31bccef75915ff988a949f6e2069d6c7d)]

## Summary

Attune AI combines cross-session findings, curated project lessons, and prompt-triggered lesson recall. The inspected design favors a small, expiring raw stash and human-gated promotion, with local files as the no-infrastructure tier and an optional Redis Agent Memory Server backend. This review describes selected current source and documentation, not measured system behavior.[[README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)] [[session_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/session_stash.py)] [[file_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/file_stash.py)]

## Who and what

The repository identifies Smart AI Memory, LLC and says the project was built by Patrick Roebuck. Attune AI is an open source developer workflow package and Claude Code plugin with CLI and MCP surfaces; the repository README describes its cross-session memory as one part of a larger workflow hub.[[README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)]

## Architecture and data model

**Code observation.** The session stash models a finding with UUID, originating session, working-directory path, UTC timestamp, type, text, tags, and a TTL. Types are decision, pattern, bug, reference, and note; the entry constructor rejects blank text and truncates content above 500 characters. Backend resolution uses an injectable searchable-memory protocol and registered backend entry points; a connected upgrade such as AMS can be preferred over the local file fallback.[[session_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/session_stash.py)]

**Code observation.** The zero-infrastructure backend stores findings as JSONL at ~/.attune/session_stash/findings.jsonl and key/value data in a sibling kv.json. It loads records from the file and prunes expired records lazily during access. The implementation defines a 30-day default TTL and a three-day recency half-life.[[file_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/file_stash.py)]

**Documentation observation.** The README describes a separate curated tier of git-tracked Markdown lessons reached through a review-gated stash-to-curated promotion flow, plus lessons retrieved at prompt or tool-call time. The inspected lesson manager uses project-local .attune/lessons.md and a global ~/.attune/lessons.md fallback, and can sync the project lesson section into .claude/CLAUDE.md. These are distinct storage and delivery paths, not one unified record model.[[README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)] [[lessons.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/lessons.py)]

## Write, update, delete, and retrieval

**Write.** The README says a Stop hook extracts decisions, bugs, and references from a session and writes them to the stash. The session model bounds each raw entry to 500 characters and carries a 30-day TTL; its module documents a PII/secrets gate before writes. The no-Redis backend appends JSONL records, while the optional backend is resolved through the searchable-memory protocol. The actual hook and complete gate implementation were not part of this bounded inspection.[[README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)] [[session_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/session_stash.py)] [[file_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/file_stash.py)]

**Recall.** SessionStart recall is query-less and asks for recent entries; the session API describes same-working-directory entries as preferred, not as a hard filter. File-tier retrieval tokenizes text for keyword overlap and combines that signal with recency. The README separately describes on-demand topic recall and a prompt/tool-triggered lesson index, but their complete runtime wiring was not inspected here.[[session_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/session_stash.py)] [[file_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/file_stash.py)] [[README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)]

**Update and delete.** Raw findings can be forgotten by ID; the session API also resolves an ID prefix only when it matches exactly one of the recent records. The file tier lazily expires old JSONL records and provides key/value deletion. The README describes promotion as review-gated and curated lessons as editable Markdown, but this inspection did not establish a general fact-correction, supersession, or comprehensive deletion path across all backends, copies, and derived indexes.[[session_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/session_stash.py)] [[file_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/file_stash.py)] [[README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)]

**Other memory surface inspected.** The long-term pattern operations expose access-filtered listing and deletion by pattern ID, and successful deletion writes an audit event. The review did not inspect the concrete pattern storage backends or every mutation route, so it does not claim that all Attune memory tiers share this same access or audit behavior.[[long_term_operations.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/long_term_operations.py)]

## Metric-domain evidence

**Code and documentation observations.** The local file path provides a simple JSONL scan, keyword overlap, recency weighting, a soft current-directory preference, lazy TTL pruning, atomic key/value writes, and a writability probe. File backend stats expose the tier name, finding count, base directory, and TTL. The README also describes opt-in usage telemetry, local workflow cost/token/timing records, and bounded prompt-time lesson retrieval. These show implementation hooks and design choices; this review did not measure their performance or quality.[[file_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/file_stash.py)] [[session_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/session_stash.py)] [[README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)]

The README reports upstream dogfood results of 67× fewer tokens for trap-moment lessons, P@3 of 96% on a frozen 800+ lesson benchmark, and a SessionStart timing comparison. These are README-reported results with the README's stated setup; they are not measurements from this review and were not independently reproduced.[[README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)]

| Domain | Evidence available in inspected sources | Review measurement |
|---|---|---|
| Answerable recall and abstention | Keyword/recency recall and documented semantic backend option; no reviewed adjudicated output set | Unmeasured |
| Correction and stale values | Raw-entry forgetting and Markdown lesson editing; no end-to-end correction protocol inspected | Unmeasured |
| Deletion leakage | Expiry, raw-entry forgetting, key deletion, and pattern deletion surface are visible; cross-tier deletion completeness is unknown | Unmeasured |
| Scope isolation | Working directory influences recall ordering; it is a soft preference in the session API | Unmeasured |
| Evidence support and citations | Provenance envelope records tier/source/author and flags instruction-shaped text; no claim-entailment adjudication | Unmeasured |
| Latency and write-to-recall delay | Recency and local scan are source-visible; no timed workload run | Unmeasured |
| Tokens, cost, and storage | Backend statistics expose count/path/TTL; README describes bounded lesson context and upstream token figures | Unmeasured |

Project metric definitions and the shared status record describe the comparison protocol, but do not contain Attune AI execution results.[[metric definitions](../METRICS.md)] [[benchmark status record](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This bounded review inspected the official README, session entry/backend and local file-tier code, lesson manager, provenance renderer, and pattern list/delete operations. It did not inspect the entire package, hook code, all backend implementations, or run the system. Accordingly, semantic backend behavior, complete scope enforcement, physical deletion across replicas/indexes/backups, and measured recall, latency, cost, and storage remain unknown.[[README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)] [[session_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/session_stash.py)] [[file_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/file_stash.py)]

The provenance helper frames recalled content as source-attributed untrusted evidence, labels curated versus machine-extracted authorship, and scans for instruction-shaped patterns. Its own code calls delimiter framing a weak defense and says the scanner flags but does not block; those mechanisms do not establish immunity to prompt injection or that evidence supports an answer.[[provenance.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/provenance.py)]

## Benchmark status

**Benchmark not run.** No Attune AI execution, benchmark workload, or tests were run for this review. The project fixture, metric definitions, and shared status record are protocol artifacts; the reported upstream README figures remain separately labeled source claims.[[metric definitions](../METRICS.md)] [[benchmark status record](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)]

## Sources

- [Current canonical repository](https://github.com/Smart-AI-Memory/attune-ai)
- [Current main commits feed](https://github.com/Smart-AI-Memory/attune-ai/commits/main.atom)
- [Reviewed full head commit](https://github.com/Smart-AI-Memory/attune-ai/commit/d076f7d31bccef75915ff988a949f6e2069d6c7d)
- [README.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/README.md)
- [session_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/session_stash.py)
- [file_stash.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/file_stash.py)
- [long_term_operations.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/long_term_operations.py)
- [provenance.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/provenance.py)
- [lessons.py](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/src/attune/memory/lessons.py)
- [SECURITY.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status record](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and source attribution](../data/memory-systems.json)

## Contact-list follow-up

The official pinned SECURITY.md publishes security@smartaimemory.com for vulnerability reports and patrick.roebuck@smartaimemory.com in its security-update/contact section. The record uses the published security contact and links to that exact checked repository document.[[SECURITY.md](https://github.com/Smart-AI-Memory/attune-ai/blob/d076f7d31bccef75915ff988a949f6e2069d6c7d/SECURITY.md)]
