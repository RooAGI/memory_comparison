# Empirica

## Identity and review pin

- **Catalog position:** 218, “Empirica”; slug `empirica`.
- **Listed repository:** [EmpiricaAI/empirica](https://github.com/EmpiricaAI/empirica); the roster marks the locator explicit. The pinned Atlas entry is recorded only as curated identity and locator attribution.
- **Canonical upstream:** [EmpiricaAI/empirica](https://github.com/EmpiricaAI/empirica), default branch `main`. GitHub’s official repository API reports `main`; its commit API for `main` returned full head `227ca60336fef77cafe1fe9f706cfe9c83378133`.
- **Reviewed:** 2026-11-25 19:15:03 UTC (2026-11-25 11:15:03 PST; America/Los_Angeles).
- **Status:** Reviewed from code at the verified SHA. Benchmark not run.

The [catalog record](../data/memory-systems.json) supplies the ordinal, slug, listed repository locator, and roster attribution. The [pinned Atlas record](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/empirica.md) is cited for roster attribution only, not as assessment evidence.

## Summary

Empirica is a local-first Python CLI and library for recording and evaluating an agent’s work beliefs, evidence, and outcomes. Its artifact records are stored in a project SQLite database, Git notes provide a versioned history channel, and optional Qdrant collections provide semantic retrieval. The three stores serve different purposes and can diverge; this review does not establish runtime accuracy or performance.

## Who and what

The official [README](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/README.md) describes Empirica as epistemic infrastructure for measuring agent beliefs, gating actions, and retaining learning across sessions. It is an open source CLI/library with a harness integration; the README says the open-source project is MIT licensed. The README lists the project website, GitHub issues, and discussions as support channels. I checked that pinned README for a contact email; it publishes none.

## Architecture and data model

The pinned [architecture overview](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/ARCHITECTURE.md) describes three storage layers. SQLite is the queryable working record for sessions, transactions, goals, vectors, and typed artifacts. Git notes hold artifacts and checkpoints attached to commits for history and repository transport. Optional Qdrant collections hold vectors for semantic retrieval. The project explicitly notes that these layers are written at different times and may disagree; reconciliation is separate work.[[architecture](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/ARCHITECTURE.md)] [[storage guide](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/docs/architecture/CANONICAL_STORAGE.md)]

Artifacts are typed records such as findings, unknowns, assumptions, decisions, mistakes, dead ends, goals, lessons, and sources. SQLite rows carry project/session/goal relationships and optional evidence references or source associations; Git note stores attach per-artifact records to refs under `refs/notes/empirica/<type>/<id>`. The [lifecycle guide](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/docs/architecture/ARTIFACT_LIFECYCLE_AND_OUTCOME_FEEDBACK.md) documents typed state transitions and a source-outcome trail for cited sources.[[storage guide](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/docs/architecture/CANONICAL_STORAGE.md)] [[artifact repository](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/data/repositories/breadcrumbs.py)] [[lifecycle guide](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/docs/architecture/ARTIFACT_LIFECYCLE_AND_OUTCOME_FEEDBACK.md)]

## Write, update, delete, and retrieval

**Write.** CLI artifact-log commands and repository methods create typed SQLite artifacts, with project and session identifiers plus optional source/evidence references. The architecture guide describes matching per-type Git note stores. When embeddings are enabled, Qdrant receives derived representations for memory artifacts and other project knowledge; Qdrant is optional and its collections are created lazily.[[artifact repository](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/data/repositories/breadcrumbs.py)] [[storage guide](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/docs/architecture/CANONICAL_STORAGE.md)] [[Qdrant collections](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/core/qdrant/collections.py)]

**Update and resolve.** The lifecycle model closes findings with typed reasons such as stale, superseded, retracted, or mistyped; supersession can point to a named artifact. Unknowns can be answered, assumptions verified/falsified/expired, goals completed, and decisions assessed with outcomes. The helper for finding references requires an exact ID or an unambiguous prefix across artifact types. This is lifecycle state on retained records, not an in-place factual edit API.[[lifecycle guide](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/docs/architecture/ARTIFACT_LIFECYCLE_AND_OUTCOME_FEEDBACK.md)] [[resolution helpers](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/data/resolution_kind.py)]

**Delete and archival.** The canonical-storage guide describes note lifecycle operations that archive notes on delete and stamp resolution on active notes. The implementation moves an active Git note ref to an archive ref and removes it from the active namespace after the archive write succeeds; the archived note remains. This review found no guarantee that deleting/archiving a note physically erases its SQLite row, Qdrant representation, backups, or other copies. The lifecycle guide also records that bulk invalidation for dead ends and mistakes is SQLite-only and may reappear as valid after a from-notes rebuild.[[storage guide](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/docs/architecture/CANONICAL_STORAGE.md)] [[note lifecycle](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/core/canonical/empirica_git/note_lifecycle.py)] [[lifecycle guide](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/docs/architecture/ARTIFACT_LIFECYCLE_AND_OUTCOME_FEEDBACK.md)]

**Retrieval.** The default Qdrant `focused` search covers docs, memory, eidetic facts, and episodic entries; `intelligence` adds assumptions, decisions, and goals. Search is project-keyed and hides resolved memory items by default. Search returns empty results when Qdrant is unavailable; the architecture guide says retrieval degrades to keyword search when semantic search is unavailable. The `situation` bootstrap also reads active project goals from SQLite. These are implementation paths, not measured relevance or abstention results.[[Qdrant search](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/core/qdrant/memory.py)] [[Qdrant collections](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/core/qdrant/collections.py)] [[bootstrap situation](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/core/bootstrap/situation.py)]

## Scope isolation

SQLite artifact reads commonly predicate on `project_id`, and Qdrant names its semantic collections by project ID. The inspected code therefore provides project partitioning in its data access paths. This review found no evidence that those identifiers are an authorization boundary by themselves; deployment credentials, filesystem/database permissions, and any remote Qdrant access controls were not evaluated.[[artifact repository](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/data/repositories/breadcrumbs.py)] [[Qdrant collections](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/core/qdrant/collections.py)]

## Provenance and evidence

Artifact APIs accept evidence references and source identifiers; the lifecycle guide describes source-outcome events when cited artifacts are confirmed, invalidated, superseded, or retracted. It also says outcome bookkeeping is fail-open. Git notes anchor records to commits, which provides a history/transport mechanism. These structures support traceability, but they do not independently prove a claim’s truth or guarantee that every finding has a source citation.[[artifact repository](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/data/repositories/breadcrumbs.py)] [[lifecycle guide](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/docs/architecture/ARTIFACT_LIFECYCLE_AND_OUTCOME_FEEDBACK.md)] [[Git notes storage](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/core/canonical/git_notes_storage.py)]

## Efficiency and observability

SQLite supports structured project reads; Qdrant adds optional vector retrieval, with per-project collections created lazily. The code’s unavailable-Qdrant behavior and the documented keyword fallback provide a reduced retrieval mode, not a performance guarantee. The README and architecture describe grading self-assessments against external signals such as test results and commit activity, while noting that the belief inputs remain self-reported. No latency, throughput, write-to-recall delay, token, cost, storage, or retrieval-quality measurements were collected for this review.[[Qdrant collections](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/core/qdrant/collections.py)] [[Qdrant search](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/empirica/core/qdrant/memory.py)] [[architecture](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/ARCHITECTURE.md)] [[README](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/README.md)]

## Metric-domain evidence

- **Answerable retrieval and abstention:** semantic search and keyword fallback paths are present; answer accuracy and abstention were not measured.
- **Correction and stale values:** typed resolution and supersession are documented; correction accuracy and stale-value rate were not measured.
- **Deletion leakage:** Git note archival and vector resolution sync were inspected; complete deletion or residual leakage was not measured.
- **Scope isolation:** project identifiers partition inspected SQLite and Qdrant paths; no authorization boundary test was run.
- **Evidence support and citations:** evidence/source references and source-outcome bookkeeping exist; support precision and citation coverage were not measured.
- **Retrieval latency and write-to-recall delay:** not measured.
- **Tokens, cost, and storage efficiency:** not measured.

See the project's [metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and [benchmark fixture](../fixtures/memory-benchmark-v1.json). They define the comparison workload and do not report Empirica results.

## Contact

No contact email was found in the official pinned [README](https://github.com/EmpiricaAI/empirica/blob/227ca60336fef77cafe1fe9f706cfe9c83378133/README.md). Exact checked URL is recorded in [empirica.json](../data/system-reviews/empirica.json).

## Limits and unknowns

This is a source review at one verified upstream SHA. I did not run Empirica, its tests, or benchmarks. Source inspection cannot establish artifact retrieval quality, effective authorization across deployment boundaries, cross-store consistency under failure, physical erasure across replicas or backups, or operational latency/cost. The optional embeddings backend, harness, configuration, and deployment can change behavior and were not evaluated.

## Benchmark status

**Benchmark not run.** No Empirica runtime, tests, or benchmarks were run. See the [project metrics](../METRICS.md), [shared status](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and SHA-pinned upstream URLs are recorded in [empirica.json](../data/system-reviews/empirica.json). The [curated roster](../data/memory-systems.json) and [pinned Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/empirica.md) support identity and locator context only.
