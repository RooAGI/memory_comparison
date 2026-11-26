# HomeBody source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 307 / HomeBody / `homebody`  
**Listed repository locator:** [Stanford-TML/homebody](https://github.com/Stanford-TML/homebody)  
**Canonical upstream:** [Stanford-TML/homebody](https://github.com/Stanford-TML/homebody)  
**Default branch / reviewed head:** main / [d7eb20834024f0fdbf2b8357fb55e8bbd01610cf](https://github.com/Stanford-TML/homebody/commit/d7eb20834024f0fdbf2b8357fb55e8bbd01610cf)  
**Review time:** 2026-11-25 23:29:46 UTC (2026-11-25 15:29:46 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists HomeBody at ordinal 307, slug `homebody`, with the explicit repository locator `https://github.com/Stanford-TML/homebody`. Its pinned Agent Memory Atlas entry is retained only as roster attribution, not assessment evidence. The official repository page identifies `main`; its official `main.atom` commit feed reports full current head `d7eb20834024f0fdbf2b8357fb55e8bbd01610cf` and timestamp 2026-11-18T01:37:00Z. The reviewed README, source files, and skill handlers are pinned to that SHA. The review timestamp records the time of inspection.[[catalog]][[atlas]][[repo]][[head]]

## Summary

HomeBody is a humanoid robotics system whose persistent memory is a named collection of map-localized photographs. It stores a short description alongside RGB, optional calibrated depth, camera metadata, pose, and map/frame identity. Recall ranks stored views by spatial proximity and heading; it does not search description text.[[readme]][[memory-store]][[remember]][[recall]]

## Who and what

The official README and project site describe a Stanford-led research system combining a vision-language model with reusable humanoid skills, simulation and real-robot backends, and a spatial photo memory. The memory code is a local Python library used by the `remember` and `recall` skills; this review covers that memory path, not a hosted memory service.[[readme]][[website]][[memory-store]][[remember]][[recall]]

## Architecture and data model

`NamedMemory` opens one named directory containing an atomic `memory.json` state file and content-addressed image/depth assets. State records include UUID, description, map pose `[x, y, yaw]`, timestamp, frame ID, image and optional depth references, camera data, and the required map binding. Asset references carry a SHA-256 digest and byte size; asset paths are restricted to digest-named PNG or NPY files. The state tracks records and removal events separately.[[memory-store]]

A `MapBinding` records scene ID/hash, frame ID, navigation hash, and optionally a geometry hash. Opening a store requires an explicit binding, rejects a symlinked memory directory, and validates its state. Recall checks that current navigation still matches the bound map/frame before allowing the operation. This is a deployment/map consistency boundary, not an account or user authorization system.[[memory-store]][[binding]][[recall]]

## Write, update, delete, and retrieval

**Write.** The passive `remember` skill observes the current frame and calls `NamedMemory.remember(frame, content)`. The store validates and encodes the photo and optional depth, writes assets by content digest, appends a new record, and atomically replaces the state file under a process/thread lock. The skill prompt asks for a short view description and warns that the observation does not certify future presence. A general update or deduplication flow was not found in the inspected skill/store path; remembering again creates another observation.[[remember]][[memory-store]]

**Update and removal.** The `recall` skill accepts `op: "remove"` as well as retrieval. Removal runs the same spatial query, then appends a removal entry for every returned hit to the state; active-record reads exclude removed IDs. The store retains the record and removal history in the state file. The reviewed code does not establish secure erasure of old state-file copies, backups, or assets no longer referenced by records.[[recall]][[memory-store]]

**Retrieval.** Recall requires a finite three-coordinate map pose, accepts (k) from 1 through 8, and ranks active photographs using planar distance plus a configurable yaw penalty. If the nearest score exceeds the configured radius, it returns a valid absent result; a missing pose also returns absent because text search is unavailable. Hits are marked historical and include pose, time, frame, description, image/depth/camera references, and map binding. The prompt explicitly says to verify current evidence before assuming an object remains present or reachable.[[recall]][[memory-store]]

## Scope isolation

Each named store is a local directory and records are bound to a scene and navigation frame. These checks prevent using a store with a different map/frame identity, but they do not provide per-user, tenant, agent, or process authorization. The reviewed code checks the named directory and lock against symlinks and uses local file locks; it does not establish isolation between mutually untrusted callers.[[memory-store]][[binding]]

## Provenance and evidence

A memory hit carries the recorded description, timestamp, pose, frame ID, map binding, camera metadata, and asset digest references. `load_image` verifies the returned hit belongs to the current binding, remains active, and retains the same image reference, then loads pixels from the digest-validated asset path. This supports tracing a recalled view back to a stored image and spatial context. The reviewed model does not provide claim-level evidence spans, source attribution for text, confidence/trust state, or an audit of edits to record content; descriptions remain caller-provided labels.[[memory-store]][[binding]][[remember]][[recall]]

## Efficiency and observability

The implementation stores photos and optional depth as separate content-addressed files and keeps metadata in one JSON state document. Recall sorts the active records in memory and therefore scans the active record set; no vector index, text index, or background consolidation path was found in the reviewed memory module. File and directory fsyncs, atomic replacement, and an exclusive file lock are used for state writes. No query latency, write-to-recall delay, token use, API cost, or storage workload was measured.[[memory-store]]

## Metric-domain evidence

All benchmark domains are **unmeasured** for HomeBody. The project metric definitions, fixture, and shared execution status describe evaluation materials and project-wide execution state; they are not HomeBody results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Spatial nearest-view retrieval and an absent result are implemented; no recall probes were scored. | Unmeasured |
| Correction and stale values | New observations append records; no correction sequence or stale-value workload was evaluated. | Unmeasured |
| Deletion leakage | Spatial removal records deactivation; no post-removal, backup, or asset-erasure probe was run. | Unmeasured |
| Scope isolation | Scene/map/frame binding is checked; no cross-store or adversarial isolation workload was run. | Unmeasured |
| Evidence support and citations | Hits include photo and spatial metadata; no evidence-support or citation adjudication was performed. | Unmeasured |
| Latency and write-to-recall delay | No runtime timings or delayed-recall probes were collected. | Unmeasured |
| Tokens, cost, and storage | File-backed images, optional depth, and JSON metadata are present; no usage or storage measurements were collected. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of the official README, project page, and selected memory implementation at the verified head. HomeBody, its tests, and benchmarks were not run. Source inspection establishes available code paths, not that remembered views are useful, that spatial ranking finds the correct object, or that the robot can safely act on a recalled view.[[readme]][[website]][[memory-store]][[metrics]]

Memory is a spatial photo archive rather than semantic text memory: descriptions are returned with matches but the recall path requires a map pose and has no text-search operation. The source review did not establish behavior under large stores, map changes beyond the binding checks, concurrent independent clients, crash recovery across every asset/state boundary, or storage cleanup for orphaned assets.[[memory-store]][[binding]][[recall]]

The removal operation deactivates spatial query hits while preserving removal records. Physical erasure across backups, copied stores, or unreferenced content-addressed assets was not established. The memory directory is named and map-bound, but deployment identity and access control are outside the inspected implementation.[[memory-store]][[binding]]

## Benchmark status

**Benchmark not run.** HomeBody, tests, and benchmark workloads were not run. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) are project documents, not HomeBody measurement results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and the official project website were checked for a published contact email; neither page displayed one. The structured record stores `contact_email: null` and both exact checked URLs. No address was inferred from commit or profile metadata or a third-party directory.[[readme]][[website]]

## Sources

The catalog identity and Atlas attribution are recorded for curated roster context only; Atlas is not assessment evidence. Upstream implementation links use the full reviewed SHA. See the structured record [homebody.json](../data/system-reviews/homebody.json) and [curated roster](../data/memory-systems.json).
