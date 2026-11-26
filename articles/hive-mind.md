# HiveMind (projectmentor) source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 303 / HiveMind (projectmentor) / `hive-mind`  
**Listed repository locator:** [projectmentor/hive-mind](https://github.com/projectmentor/hive-mind)  
**Canonical upstream:** [projectmentor/hive-mind](https://github.com/projectmentor/hive-mind)  
**Default branch / reviewed head:** main / [296dc41b15126280d40b9cfdb18aca5f2286f3f5](https://github.com/projectmentor/hive-mind/commit/296dc41b15126280d40b9cfdb18aca5f2286f3f5)  
**Review time:** 2026-11-25 23:18:05 UTC (2026-11-25 15:18:05 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists HiveMind (projectmentor) at ordinal 303, slug `hive-mind`, with the explicit locator `https://github.com/projectmentor/hive-mind`. Its pinned Agent Memory Atlas entry is retained only as roster attribution and is not assessment evidence. The official GitHub repository API identifies `projectmentor/hive-mind` and default branch `main`; the official commits/main API reports current full head `296dc41b15126280d40b9cfdb18aca5f2286f3f5`. The README, internals and implementation files cited below were inspected at that commit. The review timestamp records when the repository state was checked.[[catalog]][[atlas]][[repo]][[head]]

## Summary

HiveMind is a self-hosted, peer-to-peer memory system for AI agents. Each device stores the full shared hive in an append-only signed journal; a rebuildable SQLite/FTS5 index supports local search. Devices exchange journal deltas over a Tailscale network. Confidence is derived from independent corroboration and owner governance, rather than being set by a writer.[[readme]][[internals]]

## Who and what

The official README describes HiveMind as shared memory for agents across devices, without a central service. The reviewed repository provides the `hv` CLI, an installer and sync daemon, plus integrations for Claude Code, Hermes and MCP. The README identifies ProjectMentor and Certified Project Management, LLC as the project/copyright holder; it calls the software alpha and says the agent contract changes between minor versions.[[readme]]

## Architecture and data model

The source of truth is a daily JSONL journal. Entries carry a device identity, per-device sequence, type, timestamp, payload, previous-entry hash and (for signed entries) public key and Ed25519 signature. Journal references use stable `(node_id, seq)` identity rather than local database row IDs. The journal is append-only; entries are not edited in place.[[internals]][[journal]]

Each device derives a local SQLite `store.db` from that journal. The WAL-mode database includes FTS5-backed facts plus decisions, ideas, entities, links and a journal identity index. It is a projection rather than authoritative storage and can be rebuilt with `hv doctor rebuild`. Projections calculate confidence, contested state, learned importance and utility from journal events and governance.[[internals]][[journal]]

The sync daemon exchanges missing journal entries using Merkle chunk hashes (100 entries per chunk); matching roots avoid transferring the corpus again. The README describes a default five-minute sync interval and on-demand sync. There is no leader or broker: each device holds a complete local hive and works offline between syncs.[[readme]][[internals]]

## Write, update, delete, and retrieval

**Write.** The documented CLI writes facts with `hv remember`, decisions with `hv decide`, hypotheses with `hv propose`, and named entities with `hv entity`. Agent integrations can call the same command/API surface. Journal writes are append-first; SQLite is then projected from the journal. Identical fact text is corroborating evidence for an existing fact rather than a new independent assertion. Decisions can name the stable references that informed them; facts can be linked as supporting, contradicting, resolving or outcome evidence.[[cli]][[internals]][[journal]][[links]]

**Correction and deletion.** There is no in-place edit or physical delete for journal facts. `hv retract` appends a retraction as negative evidence; the owner can issue an owner-signed forget that sets that exact content to the forget floor, hiding it from ordinary search. `hive-mind unforget` is an owner-only counter-action. The text remains in the append-only journal, and the README describes old lines as staying in the hive. Thus owner forget is a query/projection control, not erasure of historical bytes. Decision correction uses a superseding decision/link; whether a supersedes link takes effect depends on authority. A non-owner link can be recorded as evidence without hiding or replacing its target.[[readme]][[cli]][[internals]][[links]]

**Retrieval.** The documented search path uses local SQLite FTS5, not a vector or embedding index. `hv search` searches facts, decisions and ideas, supports tags, confidence/status and ranking choices, and returns stable references. Fact confidence is decayed at read time; importance and utility can also be ranked with their configured time decay. The CLI documentation identifies `hv search` as the normal retrieval command; dashboard search reuses the same projections and is read-only.[[cli]][[internals]][[read-api]]

## Scope isolation

The basic data boundary is the hive: all its devices share the same corpus, and the README says each device keeps the full hive. The reviewed fact schema does not provide a project, user or tenant scope on each fact. Tags are search filters and can help organize project material, but they are not an authorization boundary. A device that has synced can read the hive; admission determines whether its writes count toward confidence, and owner governance controls membership. The design is suitable for a deliberately shared group, not for separating mutually unauthorized projects or users inside one hive.[[readme]][[internals]][[cli]]

The sync daemon binds to the Tailscale address, and sync reads are authenticated as admitted devices under the documented protocol. That network/membership boundary does not create per-record access control. No runtime isolation or hostile-peer test was performed for this review.[[readme]][[internals]]

## Provenance and evidence

Signed journal entries bind events to device keys; per-node sequence and hash chains make the journal auditable and allow deterministic replay. The human-readable source label adds app/context/instance information but is self-declared; cryptographic device identity is what authenticates the writer. The owner-signed governance journal defines admission and confidence parameters so devices derive the same projection.[[readme]][[internals]][[journal]]

Fact confidence comes from distinct `(device, app, instance)` identities, with same-device discounts, an admission gate after owner setup, and a cap when corroborators belong to one principal. Repeating a writer's own assertion cannot raise trust. Contested facts remain visible rather than being silently filtered. Generic links represent support, contradiction, resolution, supersession, informed-by and outcome relationships. Hard supersession/resolution requires owner authority at that journal position or authorship of the target; otherwise the link remains weigh-only evidence. This is provenance and governance evidence, not a guarantee that the underlying statement is true.[[internals]][[links]]

The system can preserve the source event and stable identity for a fact, but this review found no requirement that every fact include a quoted external source passage or that downstream natural-language answers emit citations. Evidence support and citation quality therefore remain unestablished.[[internals]][[cli]]

## Efficiency and observability

The implementation uses SQLite WAL/FTS5, caches successful signature verification within a bounded process-local LRU, and syncs only missing Merkle chunks. These choices reduce repeated full transfer and support local reads. The internals documentation says projections still scan the whole journal and reports an upstream timing example on one approximately 860-entry hive; those are source/documentation observations, not independently reproduced results for this review. Journal growth and projection cost at larger scales are unknown here.[[internals]][[journal]]

Operators can inspect status, peers, statistics and health with the CLI; the README describes a read-only local dashboard for corpus, peers, health and telemetry. The read API reuses the CLI projections. These are observability surfaces, not performance measurements. No latency, write-to-recall delay, token use, cost or storage benchmark was collected.[[readme]][[read-api]][[metrics]]

## Metric-domain evidence

All benchmark domains are **unmeasured** for this review. The project definitions, synthetic fixture and shared execution-status file define a protocol and current project status; they are not HiveMind results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Local FTS search and minimum-confidence filters are implemented; no fixture questions were run or scored. | Unmeasured |
| Correction accuracy and stale values | Retractions, owner forgets and authorized decision supersession are documented; no correction probes were run. | Unmeasured |
| Deletion leakage | Owner forget affects the projection; journal bytes persist. No post-forget leak probes or storage audit were run. | Unmeasured |
| Scope isolation | Membership is hive-wide; no per-project isolation probes were run. | Unmeasured |
| Evidence support and citation coverage | Signed provenance and relation links exist; no answer claims or citations were adjudicated. | Unmeasured |
| Retrieval latency | No timed retrieval operations were collected. | Unmeasured |
| Write-to-recall delay | No scheduled post-write recall probes were collected. | Unmeasured |
| Tokens and cost | No model/token or provider billing observations were collected. | Unmeasured |
| Storage efficiency | Journal and derived SQLite store are documented; no byte boundary or corpus storage size was measured. | Unmeasured |

## Limits and unknowns

This is a bounded source review of the official README, CLI reference, internals documentation and selected current implementation at the verified SHA. HiveMind, its tests and benchmarks were not run. Source inspection establishes documented and implemented paths, not real-world recall quality, correctness under concurrency, end-user behavior or security against every deployment threat.[[readme]][[cli]][[internals]]

The journal grows append-only. Owner forget hides matching content in the derived view but does not remove journal history; copies already held by peers, exports or backups were not assessed. Whole-hive membership and shared read scope make project-level separation an operator-level concern. The README labels the system alpha, and its contract may change between minor versions. Scale and rebuild time beyond the documentation's cited example remain unknown.[[readme]][[internals]][[cli]]

The reviewed README and internals explain how provenance and confidence are derived, but they do not establish factual truth, answer citation support, or independently verified trustworthiness of the writer's source claims. Peer-to-peer convergence, scope isolation, forget behavior and decision outcomes were not dynamically exercised.[[readme]][[internals]]

## Benchmark status

**Benchmark not run.** HiveMind, tests and benchmark workloads were not run. No retrieval, correction, deletion, isolation, evidence, latency, token, cost or storage result is claimed. The [project metric definitions](../METRICS.md), [synthetic benchmark fixture](../fixtures/memory-benchmark-v1.json) and [execution status](../results/initial-baselines-status.json) are project-owned protocol/status documents, not HiveMind measurement results.[[metrics]][[fixture]][[status]]

## Contact

The official README at the reviewed commit publishes `hello@projectmentor.org`. The structured record stores the address and the exact pinned README URL. No commit/profile metadata, third-party directory or inferred address was used.[[readme]]

## Sources

The catalog identity and Atlas attribution are listed only for curated roster context; Atlas is not assessment evidence. All upstream source links below are pinned to the full reviewed SHA. See the structured record [hive-mind.json](../data/system-reviews/hive-mind.json), the [curated roster](../data/memory-systems.json), [project metrics](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json) and [execution status](../results/initial-baselines-status.json).

## Citation source map

[[catalog]] ../data/memory-systems.json
[[atlas]] https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/hive-mind.md
[[repo]] https://api.github.com/repos/projectmentor/hive-mind
[[head]] https://api.github.com/repos/projectmentor/hive-mind/commits/main
[[readme]] https://github.com/projectmentor/hive-mind/blob/296dc41b15126280d40b9cfdb18aca5f2286f3f5/README.md
[[internals]] https://github.com/projectmentor/hive-mind/blob/296dc41b15126280d40b9cfdb18aca5f2286f3f5/docs/INTERNALS.md
[[cli]] https://github.com/projectmentor/hive-mind/blob/296dc41b15126280d40b9cfdb18aca5f2286f3f5/docs/CLI_REFERENCE.md
[[journal]] https://github.com/projectmentor/hive-mind/blob/296dc41b15126280d40b9cfdb18aca5f2286f3f5/hivemind/parts/02_store_journal.py
[[links]] https://github.com/projectmentor/hive-mind/blob/296dc41b15126280d40b9cfdb18aca5f2286f3f5/hivemind/parts/06_links_forget.py
[[read-api]] https://github.com/projectmentor/hive-mind/blob/296dc41b15126280d40b9cfdb18aca5f2286f3f5/hivemind/parts/08_read_api.py
[[metrics]] ../METRICS.md
[[fixture]] ../fixtures/memory-benchmark-v1.json
[[status]] ../results/initial-baselines-status.json
