# Bolt PCHIE source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 96 / Bolt PCHIE / `bolt-pchie`  
**Listed repository locator:** [wetwaferworks/bolt-pch-ie](https://github.com/wetwaferworks/bolt-pch-ie)  
**Catalog source attribution:** [Atlas report at pinned revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/bolt-pchie.md)  
**Canonical repository / default branch:** [wetwaferworks/bolt-pch-ie](https://github.com/wetwaferworks/bolt-pch-ie) / `main`  
**Reviewed head:** [7227c059cb62c204b72475ff73316a136efc2161](https://github.com/wetwaferworks/bolt-pch-ie/commit/7227c059cb62c204b72475ff73316a136efc2161)  
**Review time:** 2026-11-24 23:48:33 UTC (15:48:33 PST; America/Los_Angeles). The official repository page shows `main`; the official main Atom feed reports the full head above and was checked against `git ls-remote --symref`.  
**Published contact:** No email was found in the official [README at the reviewed revision](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/README.md) or [SECURITY.md](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/SECURITY.md). SECURITY.md asks reporters to contact the maintainer privately but publishes no address; the JSON stores null and the checked README URL.

## Identity and review pin

The curated roster identifies position 96 as Bolt PCHIE, slug `bolt-pchie`, with listed locator `https://github.com/wetwaferworks/bolt-pch-ie`. Its pinned Atlas URL is recorded for identity/source attribution only; Atlas descriptions, marks, and layout were not used as assessment evidence.[[roster](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/bolt-pchie.md)]

The official repository page identifies the canonical public repository and shows `main` as the default branch. Its main-branch Atom feed reports head `7227c059cb62c204b72475ff73316a136efc2161`; a fresh read-only `git ls-remote --symref` independently confirmed `main` as HEAD at the same full SHA. Assessment links below pin the reviewed upstream source to that revision.[[repository](https://github.com/wetwaferworks/bolt-pch-ie)] [[main history](https://github.com/wetwaferworks/bolt-pch-ie/commits/main.atom)] [[head commit](https://github.com/wetwaferworks/bolt-pch-ie/commit/7227c059cb62c204b72475ff73316a136efc2161)]

## Summary

Bolt PCHIE is a deterministic robotics research harness whose Little Nemo agent can record episodic maze runs and optionally use earlier outcomes to adjust search. The reviewed memory consists of a bounded run-receipt ring and a separate opt-in plan store. Its integrity machinery detects inconsistency against a local chain; it does not make local files tamper-proof.[[README](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/README.md)] [[ledger](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlLedger.h)] [[plan store](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/PlanMemory.h)] [[security notes](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/SECURITY.md)]

## Who and what

The README describes PCHIE as an open-source, on-device inference test bed that runs Little Nemo in simulated LithoKraft mazes. It credits Jaydee Wetwork / Wet Wafer Works with architecture and direction. Memory is integrated C++ harness code rather than a standalone hosted memory service.[[README](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/README.md)]

## Architecture and data model

### Episodic receipts

NEML uses a fixed 4,128-byte file: a 32-byte header and sixteen 256-byte receipt slots. Each receipt records run counters, maze identity and metadata, and up to six key events. Writes rotate through the ring, retaining the latest sixteen runs. The derived `nemo_priors.txt` summarizes counts and event-derived priors.[[ledger](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlLedger.h)] [[store](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlStore.h)]

Storage defaults to the operating system's user-data directory, can be redirected with configuration, and is kept outside the repository. The optional chat-note store has its own sixteen-slot ring. The chat write-back hook is off by default and the source labels it unapproved.[[store](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlStore.h)]

### Query-before-plan memory

The separate QBP store persists JSONL plan rows. Its key hashes task ID, observation tokens, belief digest, weights hash, and domain version. A row contains an action-ID plan fragment, a run provenance hash, truth state, and hash-chain link. The memory flag is opt-in and the default minimum truth is SimVerified.[[plan store](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/PlanMemory.h)] [[flags](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/RlFlags.h)]

The episodic query loads one checked snapshot, filters receipts by an eight-byte maze hash derived from canonical starting-maze bytes, and can further filter by seed, event type, or cell. That key separates maze environments in the lookup; it is not a user or tenant identity.[[query](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlQuery.h)]

## Write, update, delete, and retrieval

**Writes.** At run teardown, the recorder writes a receipt. Although it captures every fired event during the run, a stored receipt keeps only the first five non-exit events plus the first ExitFound event, or the first six events if there was no exit. A save appends a journal record and then atomically rewrites the ring file under an operating-system lock.[[ledger](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlLedger.h)] [[store](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlStore.h)] [[journal](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlJournal.h)]

**Integrity and provenance.** The journal chains each record by SHA-256 and records the expected resulting file state. Load replays and compares the chain and saved bytes, refusing broken or torn state rather than clearing it. The chain is unkeyed: someone with write access to the directory can rebuild the files. A run that reads episodic memory can include the snapshot digest in its own provenance.[[journal](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlJournal.h)] [[query](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlQuery.h)]

**Retrieval and scope.** A maze-memory prior reduces the search prior for directions that previously led into a dead end and renormalizes the weights deterministically. QBP returns a plan only for an exact situation key and accepted truth state. A hit is still checked for action legality and the PCH gate; it only shifts root prior mass and does not directly commit an action. The inspected QBP key contains no principal ID.[[query](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlQuery.h)] [[plan store](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/PlanMemory.h)] [[integration](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/MazeL1.h)] [[reasoning guide](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/docs/guide/reasoning-layers.md)]

**Update and delete.** The reviewed interfaces expose no general update or delete operation. Episodic history expires by ring overwrite, while its journal remains append-only. QBP exposes append-between-runs only, without a correction or row-removal method. In the inspected implementation, lookup stops at the first matching situation row, so a later Refuted duplicate does not retire an earlier matching row.[[ledger](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlLedger.h)] [[journal](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlJournal.h)] [[plan store](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/PlanMemory.h)]

## Metric-domain evidence

These are source observations, not measurements from this review. The repository's metric definitions, fixture and execution-status record describe the evaluation protocol, not Bolt PCHIE results.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

| Domain | Evidence available in source | Review measurement |
|---|---|---|
| Answerable recall and abstention | Exact maze-key and situation-hash lookup; QBP truth filter | Unmeasured |
| Correction and stale values | No inspected correction/update API | Unmeasured |
| Deletion leakage | Bounded ring overwrite; append-only journal | Unmeasured |
| Scope isolation | Maze key and task/context hash; no principal boundary in inspected key | Unmeasured |
| Evidence and citations | Plan rows bind run provenance hash and chain integrity; no semantic evidence adjudication | Unmeasured |
| Latency and write-to-recall delay | Episodic search is bounded by 16 receipts; QBP JSONL loads into an unbounded row vector | Unmeasured |
| Tokens, cost and storage | Fixed ring and default 384-token memory block cap | Unmeasured |
| Source-visible efficiency and observability | Hit/miss/rejection counters, QBP logs, snapshot digest, save errors and journal checks | Code-visible only; runtime unmeasured |

## Limits and unknowns

The fixed receipt ring bounds episodic retention and can omit later events from a run. The plan JSONL has no row-count cap in the inspected code, and both stores lack targeted erasure. Hash chaining detects changes relative to the chain on disk but does not authenticate it against a writer able to replace both files. These are source limits, not adversarial-test results.[[ledger](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlLedger.h)] [[plan store](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/PlanMemory.h)] [[journal](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlJournal.h)]

This review covered memory-specific source and selected integration/docs at the verified head. It did not establish real deployment isolation, runtime error rates, end-to-end memory quality, or full diagnostic coverage. The reasoning guide says memory hits remain proposals, and the inspected MazeL1 header says the between-run QBP writer is not wired in this pass.[[reasoning guide](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/docs/guide/reasoning-layers.md)] [[integration](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/MazeL1.h)]

## Benchmark status

**Benchmark not run.** I did not execute PCHIE, tests or benchmark workloads; this review produced no measurements. The repository's Results guide separately reports a historical 13 November QBP comparison with seeded hits and an unchanged walk, plus source-reported model-forward counts. Those are upstream-reported provisional results, not measurements from this review.[[upstream results](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/docs/guide/results.md)] [[project metrics](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [README.md](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/README.md)
- [SECURITY.md](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/SECURITY.md)
- [docs/guide/reasoning-layers.md](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/docs/guide/reasoning-layers.md)
- [docs/guide/limitations-and-threat-model.md](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/docs/guide/limitations-and-threat-model.md)
- [include/pchie/neml/NemlLedger.h](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlLedger.h)
- [include/pchie/neml/NemlQuery.h](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlQuery.h)
- [include/pchie/neml/NemlStore.h](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlStore.h)
- [include/pchie/neml/NemlJournal.h](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/neml/NemlJournal.h)
- [include/pchie/rl/PlanMemory.h](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/PlanMemory.h)
- [include/pchie/rl/RlFlags.h](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/RlFlags.h)
- [include/pchie/rl/MazeL1.h](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/include/pchie/rl/MazeL1.h)
- [docs/guide/results.md](https://github.com/wetwaferworks/bolt-pch-ie/blob/7227c059cb62c204b72475ff73316a136efc2161/docs/guide/results.md)
- [METRICS.md](../METRICS.md)
- [fixtures/memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json)
- [results/initial-baselines-status.json](../results/initial-baselines-status.json)
- [data/memory-systems.json](../data/memory-systems.json)
