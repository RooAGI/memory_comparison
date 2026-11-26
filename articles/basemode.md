# basemode source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 87 / basemode / basemode  
**Listed repository locator:** [ChristopherKahler/base](https://github.com/ChristopherKahler/base)  
**Current canonical repository:** [ChristopherKahler/base](https://github.com/ChristopherKahler/base)  
**Default branch / reviewed head:** main / `a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae`  
**Review time:** 2026-11-24 23:21:21 UTC (15:21:21 PST; America/Los_Angeles).

## Identity and review pin

The curated order identifies basemode at ordinal 87 and lists the repository locator above, with Atlas attribution at catalog revision 19199a4fc249e89c0793be06f0b166b358089ba0. The roster was used only for identity, locator, and attribution. Atlas descriptions, marks, prose, and layout are not assessment evidence. Fresh `git ls-remote --symref` identified refs/heads/main as HEAD at a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae; a depth-one checkout resolved to the same SHA.[[curated roster](../data/memory-systems.json)] [[repository](https://github.com/ChristopherKahler/base)] [[reviewed commit](https://github.com/ChristopherKahler/base/commit/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae)]

## Summary

basemode is a local Rust CLI and Claude Code hook integration that stores project, decision, note, rule, document, and code-structure knowledge in an RDF graph. It injects selected graph context at session start, prompt submission, and before or after file tools. The findings below are source observations from the pinned code; this review did not run basemode.[[README.md](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/README.md)]

## Who and what

The official repository describes basemode as a single Rust binary that maps a workspace into a knowledge graph and integrates with Claude Code hooks. The repository is owned by ChristopherKahler on GitHub; the reviewed README does not state a separate maintainer identity. It is local CLI and hook software with an embedded dashboard and optional extensions, rather than a hosted memory service.[[repository](https://github.com/ChristopherKahler/base)] [[README.md](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/README.md)]

## Architecture and data model

**Code observation.** The README identifies Oxigraph as the embedded RDF store, SPARQL as its query and update interface, and N-Quads text files as persistence. Reads load graph files into an in-memory store. The merged read path combines the global graph under ~/.base-gbl/.base with the nearest workspace .base graph when present, so SPARQL queries can traverse those loaded tiers.[[README.md](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/README.md)] [[graph store](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/store.rs)]

Notes and decisions are typed RDF resources with text or name/rationale, status, creation time, and optional relations to domains, projects, or entities. Notes created by the learn path are written into the current workspace graph. Markdown and code extraction add entities and relations; source-file and line metadata can support tracing graph objects to files. The vocabulary also defines provenance and source-document fields for derived concepts.[[note operations](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/note.rs)] [[decision operations](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/decision.rs)] [[ontology](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/ontology/ops.ttl)] [[semantic extraction](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/semantic.rs)]

The integration has event-specific retrieval paths. Session start gathers signals and working-set context; prompt submission matches domain, rule, and decision context; pre-tool handling can add file or AST context; post-tool handling updates activity and can add section context; Stop refreshes touched code maps asynchronously. Output collectors fit blocks to configured session or prompt budgets before printing.[[session-start hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/session_start.rs)] [[prompt hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/user_prompt_submit.rs)] [[pre-tool hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/pre_tool_use.rs)] [[post-tool hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/post_tool_use.rs)] [[Stop hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/stop.rs)]

## Write, update, delete, and retrieval

**Write — code observation.** The learn command creates a note with a slug, note text, type, active status, timestamp, and optional domain/project/entity relations. Decision logging stores decision text and rationale and can link it to a domain. Knowledge writes use the graph mutation path; when sync capture is enabled, graph deltas can be recorded in the sync ledger.[[notes](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/note.rs)] [[decisions](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/decision.rs)] [[storage](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/store.rs)]

**Update and correction — code observation.** Note text can be replaced by slug. A new note or decision can supersede an earlier record. Supersession retains both records and writes forward and inverse edges with a superseded status label in one update. Serving reads exclude older records by the supersession edge; graph inspection retains the history. This is an explicit replacement chain, not general temporal validity or claim verification.[[notes](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/note.rs)] [[supersession](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/supersede.rs)]

**Delete — code observation and limit.** Note removal deletes all triples for that note from the current workspace graph. A stale-note purge can select notes by lastRead age; the official guide says preview is the default and applying deletion snapshots first. These paths do not establish deletion across copies, exports, backups, or external sync destinations. I did not inspect every entity type’s deletion behavior.[[notes](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/note.rs)] [[graph maintenance](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/graph.rs)] [[durability guide](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/docs/graph-durability.md)]

**Retrieval — code observation.** Explicit note recall searches by text substring or domain relation. Prompt and tool hooks load graph context and match rules, decisions, projects, and file structure to prompts or touched paths; signals are also emitted at session start. Prompt blocks are budget-fitted, and the match log records matched domains, served and cut rules or decisions, scores, and withholding reasons. README claims automatic context delivery; that is intended behavior, not a measured recall result.[[notes](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/note.rs)] [[session-start hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/session_start.rs)] [[prompt hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/user_prompt_submit.rs)] [[pre-tool hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/pre_tool_use.rs)] [[match log](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/emit/match_log.rs)]

## Metric-domain evidence

All domains below are **unmeasured in this review**. Code observations describe mechanisms; they do not establish retrieval outcomes or runtime performance.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

- **Answerable recall and abstention:** keyword/domain recall and contextual prompt matching are present. No adjudicated question set or abstention probes were run.[[notes](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/note.rs)] [[prompt hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/user_prompt_submit.rs)]
- **Correction and staleness:** supersession edges preserve replacement history and exclude old records from serving reads. No correction accuracy or stale-value measurement was run.[[supersession](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/supersede.rs)]
- **Deletion:** note removal and usage-based stale-note purge exist. No deletion-leak probe was run, and backup/export cleanup is not established.[[notes](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/note.rs)] [[graph maintenance](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/graph.rs)]
- **Scope isolation:** reads merge the global tier and current workspace tier. No tenant authorization review or cross-scope probe was run. The workspace scoping document is design context with planned requirements, not proof those requirements are implemented.[[storage](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/store.rs)] [[workspace document](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/docs/workspace-scoping.md)]
- **Evidence and citations:** graph relations and source-file metadata expose some structural provenance, but no claim-support or citation-coverage result was measured.[[ontology](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/ontology/ops.ttl)] [[semantic extraction](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/semantic.rs)]
- **Latency, write-to-recall delay, tokens, cost, and storage:** in-memory graph loads, output budgets, and match logging are visible in source. No runtime latency, token, cost, storage, or write-to-recall measurement was collected here.[[storage](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/store.rs)] [[prompt hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/user_prompt_submit.rs)] [[match log](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/emit/match_log.rs)]

## Limits and unknowns

This is a bounded read-only inspection at the verified main head. The system was not executed. This review does not establish answer quality, calibrated abstention, end-to-end deletion, deployed access controls, cross-user isolation, sync reliability, or runtime efficiency. Supersession is an explicit replacement mechanism; it does not verify that newer content is true. The workspace scoping document contains current-state observations and planned requirements, so implementation claims here rely on current code instead.[[README.md](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/README.md)] [[storage](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/store.rs)] [[supersession](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/supersede.rs)] [[workspace document](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/docs/workspace-scoping.md)]

## Benchmark status

**Benchmark not run.** No system execution, benchmark workload, or tests were run. Project metric definitions, fixture, and execution-status record describe the separate project protocol; they are not basemode measurements.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

## Contact-list follow-up

I checked the official pinned repository README for a published contact email. It contains no published contact email, so the JSON record stores null and the exact checked README URL. No commit metadata, personal profile email, or third-party source was used.[[official README](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/README.md)]

## Sources

- [Canonical public GitHub repository](https://github.com/ChristopherKahler/base)
- [Reviewed full main head](https://github.com/ChristopherKahler/base/commit/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae)
- [Official project README](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/README.md)
- [Graph storage, merged reads and writes](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/store.rs)
- [Notes: create, recall, update and remove](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/note.rs)
- [Decision write and search paths](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/decision.rs)
- [Supersession chains](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/supersede.rs)
- [Session-start hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/session_start.rs)
- [Prompt hook and budget fitting](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/user_prompt_submit.rs)
- [Pre-tool context hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/pre_tool_use.rs)
- [Post-tool hook](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/post_tool_use.rs)
- [Stop hook and code map refresh](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/hook/stop.rs)
- [Prompt and tool match log](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/emit/match_log.rs)
- [RDF ontology](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/ontology/ops.ttl)
- [Document-derived semantic graph writes](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/crud/semantic.rs)
- [Graph maintenance](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/src/graph.rs)
- [Graph durability and recovery guide](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/docs/graph-durability.md)
- [Workspace scoping design document](https://github.com/ChristopherKahler/base/blob/a37b9a8f88fb5676ff9ed3ddd9f124d4cd6aa8ae/docs/workspace-scoping.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and attribution](../data/memory-systems.json)
