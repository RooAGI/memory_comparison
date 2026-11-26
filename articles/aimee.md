# Aimee source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 44 / aimee / aimee  
**Listed repository locator:** [RakuenSoftware/aimee](https://github.com/RakuenSoftware/aimee)  
**Current canonical repository:** [RakuenSoftware/aimee](https://github.com/RakuenSoftware/aimee)  
**Default branch / reviewed head:** testing / 56d9b0fa7880b7398aa7ca48f2b65b845192a6bf  
**Review time:** 2026-11-24 19:59:19 UTC (11:59:19 PST; America/Los_Angeles).

## Identity and scope

The curated roster places **aimee** at ordinal 44, lists the repository above, and attributes discovery to an Atlas report at revision `19199a4fc249e89c0793be06f0b166b358089ba0`. I used that entry only for identity, locator, and attribution; its descriptions, marks, and layout were not assessment evidence. A fresh read of the official Git remote identified `testing` as the symbolic HEAD/default branch. Its full head was `56d9b0fa7880b7398aa7ca48f2b65b845192a6bf`, matching the reviewed checkout.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/RakuenSoftware/aimee)] [[reviewed head](https://github.com/RakuenSoftware/aimee/commit/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf)]

Aimee is a self-hosted runtime with personal memory on Server and optional shared memory on KB. The key limit for this review is that current memory storage, retrieval, and lifecycle are provided by a separately maintained private implementation shipped as a binary bundle. The public repository exposes the SDK, transport, and host checks, but not that implementation's datastore or retrieval policy.[[README.md](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/README.md)] [[memory module docs](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/modules/memory.md)] [[memory boundary](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/MEMORY.md)]

## Architecture and data model

The active public architecture has a generic Go memory client over a module bus. Authenticated Server and KB hosts dispatch to the implementation selected during deployment. Without a provisioned implementation, the public adapter does not attach or provide a local datastore; readiness reports missing memory and calls fail unavailable. The repository assigns storage, ontology, retrieval policy, and maintenance to the private bundle.[[module documentation](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/modules/memory.md)] [[unavailable adapter](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/modules/memory/adapter/unavailable.go)] [[module descriptor](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/src/modules/memory/module.yaml)]

The public record contract carries an integer ID, scope, tier, kind, key, content, confidence, optional metadata, validity bounds, sensitivity, authorship, utility horizon, and a version. A version identifies schema, owner, record, and revision; it is a mutation precondition, not proof that a row is eligible to serve. These interface fields are not the complete private persisted schema.[[Store and record types](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/store.go)] [[record version](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/version.go)]

## Write, update, delete, and retrieval

**Write.** The generic Store contract provides `Put` by kind/key; IDs are assigned by the canonical source. The client borrows an already admitted bus caller and does not attach principal identity or supply a local policy fallback. Actual write admission and storage behavior remain inside the installed implementation.[[Store contract](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/store.go)] [[memory client](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/client.go)]

**Update and correction.** Basic upsert is separate from conditional mutation in an extended API. The version tuple provides an owner/record/revision precondition. Docs describe retained revisions, but implementation conflict handling is not visible in this repository.[[Store contract](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/store.go)] [[record version](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/version.go)] [[knowledge docs](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/KNOWLEDGE.md)]

**Delete and retirement.** The Store has scoped `Delete`. The module docs state that the legacy `memory.delete` name means retained retirement: invalidation makes a record unavailable for current use but does not physically delete its payload or earlier revisions. This contract does not establish erasure from backups or exports.[[Store contract](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/store.go)] [[retention and deletion contract](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/modules/memory.md)]

**Retrieval.** Scoped `Get` and `Search` are available; an empty query lists eligible records in the requested scope. Optional candidate selection is bounded and explicitly not a completeness guarantee for semantic search. Its contract requires selected canonical revisions to be revalidated. The private implementation determines ranking, eligibility, and retrieval quality.[[Store and candidate contracts](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/store.go)] [[provider dispatch fence](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/src/wire_fence.c)] [[module docs](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/modules/memory.md)]

## Scope isolation and provenance

The SDK recognizes `user`, `global`, `workspace`, and `project` scopes and canonicalizes values, but explicitly does not grant access or choose defaults. Placement and caller admission remain host decisions. Docs separate personal Server memory from explicitly selected shared KB memory; a failed private lookup does not switch stores.[[scope contract](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/scope.go)] [[knowledge docs](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/KNOWLEDGE.md)] [[security model](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/SECURITY.md)]

The client uses an admitted caller rather than accepting identity as a record argument. Version tuples bind revisions to an owner and row; the record also exposes authorship and metadata. Host-side context release and source revalidation constrain what reaches provider dispatch. These mechanisms support traceability but do not establish private provenance completeness or whether evidence supports a generated answer.[[memory client](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/client.go)] [[record and version](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/store.go)] [[ingress context](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/src/server/ingress_preinject.c)] [[dispatch fence](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/src/wire_fence.c)]

## Source-visible efficiency and observability

**Code observations.** The generic client defaults to a five-second module-call deadline (shortened by the caller context), rejects over-limit wire bodies, and distinguishes unavailable, unauthorized, and attempted-error embedding results. Candidate limits and derived-store cleanup contracts make some capacity and cleanup boundaries explicit. These are SDK/host properties, not private retrieval latency or throughput measurements.[[memory client](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/client.go)] [[wire and result types](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/types.go)] [[Store limits](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/store.go)]

**Operational observations.** Docs describe `missing_module: memory` readiness, provisioning and supervisor logs, and a bus probe for an attached implementation. These diagnostics distinguish attachment and setup from memory quality.[[module documentation](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/modules/memory.md)]

## Metric-domain evidence

All outcomes below are **unmeasured for this review**. Interfaces, lifecycle docs, and host guards do not establish workload performance or quality.[[metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

| Domain | Source observation | Status |
| --- | --- | --- |
| Answerable recall and abstention | Scoped search and candidate-selection contracts exist; ranking and eligibility policy are private. | Unmeasured |
| Correction accuracy and stale values | Record versions and mutation preconditions are exposed; accuracy and stale-value rates were not measured. | Unmeasured |
| Deletion leakage | Delete is documented as retained retirement, not physical erasure; no leakage workload was run. | Unmeasured |
| Scope isolation | Scope canonicalization and host caller admission are defined; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Version and authorship fields plus source revalidation exist; claim support was not adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | SDK deadlines and bounded candidates are visible; end-to-end distributions were not collected. | Unmeasured |
| Tokens, cost, and storage efficiency | No token, cost, or storage-efficiency results were collected for this system. | Unmeasured |

## Limits and unknowns

This review inspected the current public README, memory module and boundary docs, generic Go record/store/scope/version/client types, unavailable adapter, and host provider-dispatch source. It did not inspect the private bundle, execute Aimee, or run tests or benchmarks. It cannot establish the active ranking policy, complete database schema, write-admission internals, retrieval quality, deletion across backups/replicas/exports, or measured efficiency. Unknown means this bounded public-source review could not verify the behavior, not that it is necessarily absent.[[README.md](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/README.md)] [[module docs](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/modules/memory.md)] [[memory client](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/client.go)]

## Contact-list follow-up

The official pinned README publishes `jbailes@gmail.com` for discussing other terms. The reviewed repository root has no separate `SECURITY.md` or `SUPPORT.md`; no address was inferred from commit or profile metadata.[[README contact](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/README.md)]

## Benchmark status

**Benchmark not run.** No Aimee system, benchmark workload, or test suite was run. This article records source observations only. The project metric definitions, fixture, and execution-status record are protocol references, not Aimee results.[[metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical repository and default branch](https://github.com/RakuenSoftware/aimee)
- [Reviewed default-ref commit](https://github.com/RakuenSoftware/aimee/commit/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf)
- [README.md](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/README.md)
- [docs/modules/memory.md](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/modules/memory.md)
- [docs/MEMORY.md](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/MEMORY.md)
- [docs/KNOWLEDGE.md](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/KNOWLEDGE.md)
- [server-go/memory/store.go](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/store.go)
- [server-go/memory/types.go](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/types.go)
- [server-go/memory/scope.go](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/scope.go)
- [server-go/memory/version.go](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/version.go)
- [server-go/memory/client.go](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/memory/client.go)
- [server-go/modules/memory/adapter/unavailable.go](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/server-go/modules/memory/adapter/unavailable.go)
- [src/modules/memory/module.yaml](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/src/modules/memory/module.yaml)
- [src/server/ingress_preinject.c](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/src/server/ingress_preinject.c)
- [src/wire_fence.c](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/src/wire_fence.c)
- [docs/SECURITY.md](https://github.com/RakuenSoftware/aimee/blob/56d9b0fa7880b7398aa7ca48f2b65b845192a6bf/docs/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status record](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and attribution](../data/memory-systems.json)
- [Roster attribution source (identity only)](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/aimee.md)

**Verification boundary:** no Aimee system, tests, or benchmarks were run.
