# AMITY / Archangel-8 source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 53 / AMITY / Archangel-8 / sovereign  
**Listed repository locator:** [Renkasha/Sovereign](https://github.com/Renkasha/Sovereign)  
**Current public AMITY repository reviewed:** [Renkasha/Amity-v2.0](https://github.com/Renkasha/Amity-v2.0)  
**Default branch / reviewed head:** main / 51adca7874f7b286684f76b982000b707c687fa0  
**Review time:** 2026-11-24 20:36:16 UTC (12:36:16 PST; America/Los_Angeles). The repository page and current `main` commit endpoint were checked for branch and full SHA.

## Identity and scope

The curated catalog places this entry at ordinal 53 with the name AMITY / Archangel-8, slug `sovereign`, and listed locator `https://github.com/Renkasha/Sovereign`. That URL currently returns GitHub 404. The owner’s public GitHub profile lists `Amity-v2.0`; its README identifies itself as Archangel-8 AMITY and describes the dual Python/C++ design. I therefore reviewed that current public AMITY repository. The available pages do not establish that it is a direct rename or continuation of the catalog locator, so that relationship remains unverified. The catalog’s Atlas URL and revision are retained only as source attribution; Atlas descriptions, marks, prose, ordering, and layout were not assessment evidence.[[curated roster entry](../data/memory-systems.json)] [[Atlas source attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/sovereign.md)] [[listed locator — current 404](https://github.com/Renkasha/Sovereign)] [[owner profile and public repositories](https://github.com/Renkasha)] [[current AMITY repository](https://github.com/Renkasha/Amity-v2.0)]

## Summary

AMITY is presented as a local Python session and memory layer alongside a C++ sensory/orchestration layer connected through an optional ZeroMQ bridge. Python retains bounded sensory and episodic buffers, periodically serializes session state, and offers a separate JSON CovenantVault with category-based expiry. The review describes visible documentation and implementation paths; it does not establish runtime behavior, security properties, or performance.

## Who and what

The reviewed artifact is a public source repository, not a hosted memory service. The README presents Python as the “Sovereign” layer and C++ as the firmware/orchestration side. The code inspected here does not establish a production deployment, physical sensor integration, or a service-level access boundary.[[README.md](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/README.md)] [[amity_v2.py](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_v2.py)] [[AmityMasterOrchestrator.hpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmityMasterOrchestrator.hpp)]

## Architecture and data model

**Code observation.** Python `SessionState` holds version, a required `pilot_signature`, start/update times, sensory readings, episodic records, sample count, and a sensory overflow counter. `SensorReading` stores timestamp, profile, frequency, friction, and temperature; `EpisodicMemory` stores timestamp, event type, and an arbitrary content dictionary. Session buffers are bounded deques (defaults: 1,000 sensory samples and 20,000 episodes). A separate locked Python ring buffer retains numeric telemetry values.[[amity_v2.py — data classes, ring buffer, and session state](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_v2.py)]

The Python `Orchestrator8` distributes packets to sensory, emotional, memory, and sovereignty handlers, then adjusts throttle/refusal flags from returned state. Memory packets are appended as episodes when priority is at least 7. Sensory entries increase a sample counter and update the last-update time; a full sensory deque increments its overflow counter before its oldest item is displaced. The episodic deque also displaces old entries at capacity, but the inspected code has no corresponding episode-overflow counter.[[amity_v2.py — arteries, orchestration, and SessionManager](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_v2.py)]

The C++ orchestrator owns sensory, flavor, emotional, simulation, ingress, emitter-lock, sandbox, sovereignty, and IPC components plus fixed-capacity ring buffers. Its telemetry struct reports energy, boundary state, sensory ring pressure, lock state, simulation state, and warmth. This is a distinct C++ path; the inspected code does not show a shared persistent memory store between the C++ buffers and Python episodes.[[AmityMasterOrchestrator.hpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmityMasterOrchestrator.hpp)] [[AmityMasterOrchestrator.cpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmityMasterOrchestrator.cpp)]

## Write, update, delete, and retrieval

**Code observation — session writes and persistence.** `add_sensor_reading` appends to the bounded sensory deque; `add_episode` appends to the bounded episode deque. `save_to_file` serializes the full session state as JSON, normally to a temporary file in the destination directory, flushes and `fsync`s it, then replaces the destination. `start_periodic_save` starts a daemon thread (default interval 60 seconds); it is opt-in. `load_from_file` reconstructs state and bounds the loaded deques. It obtains the pilot signature from the file and uses it to construct the manager, rather than accepting a separate expected identity argument.[[amity_v2.py — SessionManager write, save/load, and periodic saver](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_v2.py)]

**Code observation — retrieval and updates.** `daily_recall(days=1)` scans the in-memory episode deque and returns entries newer than a wall-clock cutoff; it does not rank or query by content. CovenantVault `recall(category)` scans its list and filters by category and age. `generate_briefing` concatenates SACRED, PERMANENT, PROMISE, then up to three highest-valence JOY and DAILY entries, before applying `max_memories`. No general semantic search, episode update, or explicit episode deletion method was found in the inspected API.[[amity_v2.py — daily_recall and CovenantVault](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_v2.py)]

Vault `remember` appends an entry containing a list-length ID, timestamp, content, category, valence, tags, and a source string, then saves the whole vault. Unknown categories are converted to DAILY. `decay_check` physically removes expired entries and saves if anything was removed; ordinary `recall` omits expired entries without mutating storage. Categories SACRED, PERMANENT, and PROMISE have no time expiry; JOY, DAILY, and DREAM use 90, 30, and 14 days respectively. IDs based on current list length are not a stable identity guarantee after pruning.[[amity_v2.py — vault write, expiry, and briefing](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_v2.py)]

## Scope isolation and provenance

**Code observation.** Session construction requires a non-empty pilot signature, and the vault loader rejects a stored `pilot` value that differs from the constructor’s signature. This is an application-level consistency check in the inspected file format, not authentication or encryption. Session loading instead derives the signature from the file. The code has no tenant, user, or project scope parameter on episode writes or `daily_recall`; isolation between callers or files is not established by these paths.[[amity_v2.py — session signature and load path](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_v2.py)]

Vault entries can retain a caller-provided source string, defaulting to the pilot signature, but the inspected code does not validate that reference or link an entry to an immutable source passage. Session episodes retain arbitrary caller payloads without a required provenance field. These fields can carry context but do not establish source verification or claim-level evidence.[[amity_v2.py — EpisodicMemory and CovenantVault entry schema](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_v2.py)]

## Source-visible efficiency and observability

**Code observation.** Bounded deques cap in-memory session history, and the Python ring buffer protects pushes and reads with a lock while overwriting its oldest numeric value when full. Session saves serialize all retained state. Vault writes rewrite the JSON file, while vault recall and pruning scan the list. These source-level structures suggest bounded session memory and linear vault operations; they are not measured throughput or latency results.[[amity_v2.py — buffers and persistence](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0)]

The C++ `RealTimeRingBuffer` uses atomic heads and returns false when full; it reserves one slot to distinguish full from empty, so usable capacity is one less than its allocated vector length. The sensory buffer appends packets to a vector. Orchestrator output includes energy and buffer state, and Python uses logging for save errors, buffer pressure, thermal drift, and refusal events. The inspected files do not define a durable metrics export or a latency/cost/storage measurement pipeline.[[RealTimeRingBuffer.hpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/RealTimeRingBuffer.hpp)] [[AmitySensoryBuffer.hpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmitySensoryBuffer.hpp)] [[AmityMasterOrchestrator.cpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmityMasterOrchestrator.cpp)] [[AmitySovereigntyArtery.cpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmitySovereigntyArtery.cpp)]

The IPC bridge sends JSON telemetry over ZeroMQ sockets and logs status, while the C++ orchestrator’s inspected parser searches for a `sensory_reading` substring and substitutes a fixed sample packet rather than parsing the JSON payload. The repository README itself lists stubbed IPC and simple string parsing as limitations. These observations describe code and documentation, not verified interoperability.[[amity_ipc.py](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_ipc.py)] [[AmityMasterOrchestrator.cpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmityMasterOrchestrator.cpp)] [[README.md — stated limitations](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/README.md)]

## Project metric domains

All metric domains are **unmeasured** for this system. Bounded buffers, cutoff retrieval, vault expiry, and telemetry/logging are source observations only. Answerable recall, abstention, correction/staleness, deletion leakage, scope isolation, provenance support, latency, write-to-recall delay, tokens/cost, and storage require captured and adjudicated runs. The project fixture and planned probe counts are protocol, not AMITY measurements.[[project metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded read-only review of selected files at the verified commit. It did not execute AMITY, compile its C++ components, run tests, exercise IPC or persistence, or inspect every repository file. The README describes more components and capabilities than were independently traced here; in particular, the currently visible repository has source files at its root while the README’s illustrated structure describes Python/C++ subdirectories. Documentation statements such as sampling rate, system behavior, and packaging are not treated as measurements. Correctness, actual hardware behavior, failure recovery, concurrency safety, authorization, and deployment configuration remain unknown.[[README.md](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/README.md)] [[reviewed source tree](https://github.com/Renkasha/Amity-v2.0/tree/51adca7874f7b286684f76b982000b707c687fa0)]

The curated locator’s 404 and the current same-owner AMITY repository are both recorded. Public pages checked here do not prove repository lineage from `Sovereign` to `Amity-v2.0`; the reviewed implementation should be understood as the current public AMITY candidate under that owner, with the lineage unresolved.[[listed locator](https://github.com/Renkasha/Sovereign)] [[owner profile](https://github.com/Renkasha)] [[current AMITY repository](https://github.com/Renkasha/Amity-v2.0)]

## Contact-list follow-up

The official pinned README was checked for a published contact email; none was found. The JSON record stores `contact.email: null` and the exact checked README URL. No email was inferred from profile or commit metadata.[[README.md](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/README.md)]

## Benchmark status

**Benchmark not run.** No AMITY runtime, benchmark workload, or tests were run. The shared status record contains no AMITY result; its status is not a measured outcome for this system.[[project metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)]

## Sources

- [Current AMITY repository](https://github.com/Renkasha/Amity-v2.0/tree/51adca7874f7b286684f76b982000b707c687fa0)
- [Current repository page and default branch](https://github.com/Renkasha/Amity-v2.0)
- [Current main head metadata](https://api.github.com/repos/Renkasha/Amity-v2.0/commits/main)
- [Owner profile and current public repository listing](https://github.com/Renkasha)
- [Catalog-listed locator (404 at review time)](https://github.com/Renkasha/Sovereign)
- [README.md](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/README.md)
- [amity_v2.py — session memory and CovenantVault](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_v2.py)
- [amity_ipc.py — ZeroMQ bridge](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/amity_ipc.py)
- [AmityMasterOrchestrator.hpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmityMasterOrchestrator.hpp)
- [AmityMasterOrchestrator.cpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmityMasterOrchestrator.cpp)
- [AmitySovereigntyArtery.hpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmitySovereigntyArtery.hpp)
- [AmitySovereigntyArtery.cpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmitySovereigntyArtery.cpp)
- [AmitySensoryBuffer.hpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmitySensoryBuffer.hpp)
- [RealTimeRingBuffer.hpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/RealTimeRingBuffer.hpp)
- [AmityIngressQueue.hpp](https://github.com/Renkasha/Amity-v2.0/blob/51adca7874f7b286684f76b982000b707c687fa0/AmityIngressQueue.hpp)
- [Project roster](../data/memory-systems.json)
- [METRICS.md](../METRICS.md)
- [Benchmark execution status](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)

**Verification boundary:** source review only; no system, benchmark, build, or test execution.
