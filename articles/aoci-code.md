# AOCI-CODE

## Identity and review pin

**Name:** AOCI-CODE  
**Repository:** [aoci-spec/aoci-code](https://github.com/aoci-spec/aoci-code)  
**Default branch:** `main`  
**Reviewed head:** [d28c856699fec9724b7824ac8cec421f4de0cc00](https://github.com/aoci-spec/aoci-code/commit/d28c856699fec9724b7824ac8cec421f4de0cc00)  
**Reviewed:** 2026-11-24 13:06:38 PST (America/Los_Angeles) / 21:06:38 UTC  
**Status:** Reviewed from code. Benchmark not run.  
**Roster:** Curated ordinal 61, slug `aoci-code`; the roster locator and Atlas source attribution are recorded for identity only. Atlas assessment descriptions and marks were not used.

## Summary

AOCI-CODE is a local Go CLI and stdio MCP server that helps a coding agent maintain a Git-versioned, plain-text map of a repository. Its current Cognition Volumes workflow serves selected index contents, validates model-authored updates against repository state, and publishes formal index changes through guarded transactions; this review did not measure runtime quality or performance. [[README](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/README.md)] [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)]

## Who and what

The public repository belongs to the aoci-spec GitHub organization. AOCI-CODE is a local Go CLI and stdio MCP server used with a coding agent; the README assigns semantic entry authoring to the host model and deterministic validation and governed writes to the program. It is a developer tool, not a hosted memory service. [[Repository](https://github.com/aoci-spec/aoci-code)] [[README](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/README.md)]

## Architecture and data model

The current Cognition Volumes layout separates repository identity and layout (Root, `aoci.txt`), authoring rules (Meta, `aoci.meta.txt`), code-file entries (Code, `aoci.code.txt`), and optional database-table entries (Database, `aoci.database.txt`). Compact entries record Function, Relations, API, constraints, and tags. A repository-local Baseline binds formal assets and managed objects to source state; Git versions the text assets. [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)] [[README](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/README.md)]

Fresh initialization uses Volumes; existing Legacy indices remain readable with a retired authoring path in the current release. Root and Meta participate in scope dependencies, while Code and Database are separately selectable object collections. The Overview implementation assembles the requested object bytes into a scope delivery and checks that the result is coherent before treating it as reliable. [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)] [[Overview handler](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_read_volumes.go)]

The system's semantic map is authored by the coding agent from source. AOCI-CODE provides deterministic inventory, parsing, validation, source binding, and publication. The README positions the index as a complement to reading actual source and tests, not as a parser that infers business meaning. [[README](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/README.md)]

## Write, update, delete, and retrieval

**Write and update.** The host follows the machine-issued Maintain batch, reads its source targets, and submits authored Entries through the update interface. The batch writer validates and plans all targets against in-memory index text before writing. On success it uses a lock, compare-and-swap, and atomic file publication; if a target fails validation, the formal index is left unchanged. Candidate identity and source digests bind the write to the state Maintain issued. [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)] [[Atomic batch writer](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_write_batch.go)]

**Correction.** Replacing an Entry is a governed index update. Source bindings and transaction safety do not establish that the authored meaning is correct or that an agent will consistently prefer a corrected entry. The current docs also state that general Root/Meta editing and some Volume lifecycle operations are unavailable. [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)] [[Atomic batch writer](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_write_batch.go)]

**Removal.** The inspected removal surface is for orphan index Entries and ownership repair under guarded commit/recovery. It removes an index record after the source object is absent; it does not delete the source file. This is not a general forget operation for arbitrary current objects. [[Removal implementation](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_remove.go)] [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)]

**Retrieval.** Overview delivers a selected scope as a complete body or a sequence of chunks, with continuation tied to the host session and scope identity. The documented default is 7,000 tokens per chunk, configurable from 4,000 to 24,000. A compact check-only result is not a full index delivery. [[Overview handler](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_read_volumes.go)] [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)]

Search applies keyword and tag filters to local index entries, limits displayed results, and reports object references in Volume mode. This is retrieval from the map; it does not demonstrate answer correctness or evidence use. [[Search handler](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_read_search.go)]

**Scope and isolation.** Selectable scopes are repository-level (all/project/meta/code/database), with Root and Meta dependencies as defined by the layout. The reviewed scope model has no user or tenant identity. It should be read as local repository organization; cross-principal authorization was not established by source inspection. [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)] [[Overview handler](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_read_volumes.go)] [[README](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/README.md)]

**Provenance and evidence.** An Entry names its object and relations; write batches bind candidates to the machine-issued identity and current source digest. Database entries use a separate accepted schema-evidence path. These mechanisms establish structural and source-version bindings, not that the Entry's prose is true, that every claim retains a source passage, or that generated answers cite the evidence. [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)] [[Atomic batch writer](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_write_batch.go)]

## Metric-domain evidence

Every domain below is **unmeasured**. Implementation details are source observations; no benchmark run or runtime measurement was performed. The project metric definitions specify how a future run should be scored. [[METRICS.md](../METRICS.md)] [[Execution status](../results/initial-baselines-status.json)] [[Fixture](../fixtures/memory-benchmark-v1.json)]

| Domain | Source observations | Measurement status |
|---|---|---|
| Answerable recall and abstention | Overview and Search deliver authored index content; no response outcomes were adjudicated. | Unmeasured |
| Correction accuracy and stale values | Governed update and source binding are present; no post-correction probes were run. | Unmeasured |
| Deletion leakage | Guarded orphan removal is present; no post-removal probes or copy-erasure audit were run. | Unmeasured |
| Scope isolation | Repository and Volume scope selection is visible; no forbidden-scope probes were run. | Unmeasured |
| Evidence support and citation coverage | Object references, source digests, and database evidence bindings are visible; generated claims were not scored. | Unmeasured |
| Latency and write-to-recall delay | Search can log operation duration when the Ledger is enabled; no timings were collected. | Unmeasured |
| Tokens and cost | Overview chunk configuration is visible; no provider usage or cost was collected. | Unmeasured |
| Storage efficiency | Files and Baseline are inspectable; no bytes were measured. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of selected docs and current handlers at one verified `main` commit. It does not establish runtime correctness, answer quality, reliability, security, or performance. Model-authored semantic entries can be structurally valid while incomplete or wrong, and no end-to-end host session was evaluated. [[README](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/README.md)] [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)]

Source-digest binding verifies which source bytes a candidate was prepared against; it is not semantic evidence for every sentence in an entry. Repository/Volume scopes do not prove tenant authorization, and local deployment protections depend on the host and filesystem. Database collection, where configured, is a separate schema-metadata path. [[Cognition Volumes](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)] [[Security policy](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/SECURITY.md)]

The README publishes rough scale and first-index-time examples, but they are project statements, not measurements from this review. Legacy migration, every host integration, database behavior, and all transaction recovery cases were not exhaustively inspected. [[README](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/README.md)]

## Benchmark status

**Benchmark not run.** The shared execution-status record is `not_run`; fixture operation counts are planned inputs, not measured denominators. No AOCI-CODE runtime, benchmark workload, or tests were executed. No metric values are reported. [[METRICS.md](../METRICS.md)] [[Execution status](../results/initial-baselines-status.json)] [[Fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Canonical repository](https://github.com/aoci-spec/aoci-code)
- [Full reviewed main head](https://github.com/aoci-spec/aoci-code/commit/d28c856699fec9724b7824ac8cec421f4de0cc00)
- [README at reviewed SHA](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/README.md)
- [Cognition Volumes documentation at reviewed SHA](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/docs/cognition-volumes.md)
- [Volume Overview handler at reviewed SHA](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_read_volumes.go)
- [Search handler at reviewed SHA](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_read_search.go)
- [Atomic batch writer at reviewed SHA](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_write_batch.go)
- [Removal path at reviewed SHA](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/internal/mcptools/tools_remove.go)
- [Security policy at reviewed SHA](https://github.com/aoci-spec/aoci-code/blob/d28c856699fec9724b7824ac8cec421f4de0cc00/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution status](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster identity and attribution](../data/memory-systems.json)
