# Agent Mesh source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster name / slug:** Agent Mesh / `agent-mesh`  
**Listed repository locator:** [cbalgeman/agent-mesh](https://github.com/cbalgeman/agent-mesh)  
**Default branch / reviewed head:** `main` / `5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd`  
**Review time:** 2026-11-24 18:27:33 UTC (10:27:33 PST; America/Los_Angeles). GitHub repository metadata reported `main` as the default branch; the `commits/main` API returned the full head SHA shown here.

## Identity and scope

The curated catalog entry at position 12 identifies the system as Agent Mesh, slug `agent-mesh`, and lists `https://github.com/cbalgeman/agent-mesh`. That catalog record is used here only for identity and locator attribution. Its descriptive fields, capability marks, and presentation were not used as assessment evidence. ([project roster](../data/memory-systems.json); [catalog attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agent-mesh.md))

Agent Mesh is a pre-1.0, local-first coordination tool for durable project requests, decisions, backlog items, handoffs, and results. It is not a general-purpose memory database: ordinary conversations are not automatically copied, and records are explicitly promoted into the project history. GitHub repository metadata identifies cbalgeman as the public repository owner; this review did not establish a broader maintainer roster. ([README.md](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/README.md); [repository metadata](https://github.com/cbalgeman/agent-mesh))

## Architecture and data model

**Code observation.** The canonical source is an append-only `.agent-mesh/events.jsonl` log. Event envelopes include identifiers and sequence numbers, the prior event hash, and optional actor-instance attribution. The hashing helper serializes canonical JSON and hashes the exact newline-terminated event bytes with SHA-256. The README says longer bodies may be stored in content-hash-addressed files; SQLite and optional Markdown views are derived projections that can be rebuilt from the event history. ([README.md](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/README.md); [events.py](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/events.py); [hashing.py](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/hashing.py); [rebuild.py](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/store/rebuild.py))

The inspected SQLite module configures WAL mode, a busy timeout, foreign keys, and a projection schema for messages, decisions, backlog, dispatch, assurance, and agent-instance records. README documentation identifies the CLI and local browser Workbench as supported write surfaces, with `agent-q` for bounded reads. The event chain is described as tamper-evident, not encryption or proof of cryptographic identity. ([sqlite.py](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/store/sqlite.py); [README.md](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/README.md))

## Write, update, delete, and retrieval

**Code observation.** Durable writes append schema-versioned events through the event protocol, which validates event envelopes and provenance. The README describes the user-facing record families (requests/responses, human feedback, backlog work, decisions, and dispatch/review evidence) and states that records are promoted deliberately rather than copied from ordinary chat. ([events.py](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/events.py); [README.md](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/README.md))

**Correction and deletion.** Current privacy documentation says supported corrections are domain-native appended events that preserve the prior canonical bytes. It explicitly says Agent Mesh does not currently provide an emergency history-rewrite command, retrieval tombstones, automatic retention, or a privacy-reviewed export command. The separate privacy-lifecycle document is a future contract and explicitly says it does not implement those commands. A filtered view or correction therefore must not be described as deletion or erasure. ([privacy.md](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/docs/privacy.md); [privacy-lifecycle.md](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/docs/privacy-lifecycle.md))

**Retrieval.** `agent-q context bootstrap` is documented as a bounded, mutation-free retrieval of a verified canonical snapshot plus fixed-target project contract files and freshness metadata. Decision meaning is retrieved separately through `agent-q decisions preflight`, with cited records resolved through `agent-q refs resolve`. The documented contract distinguishes retrieval completeness from harness delivery verification: a self-reported capability does not prove that an installed lifecycle event ran. ([context-delivery-contract.md](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/docs/context-delivery-contract.md); [context_delivery.py](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/context_delivery.py))

## Scope isolation and provenance

**Code observation.** State is project-local under the configured repository, with multiple project registrations available on the local machine. The README explicitly says memory is project-scoped and that the store does not provide multi-tenant access control inside one project. Thus project path boundaries are visible in the design, but they are not evidence of a tenant authorization boundary or verified cross-project security isolation. ([README.md](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/README.md); [agent_instances.py](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/agent_instances.py))

Source provenance is represented on supported event payloads using structured source context references. Validation requires each reference to name a channel and at least one source locator, and ties source references to body-authority and body-fidelity metadata. Selection metadata can record mode, confidence, selector, and whether review is required. These are source-visible provenance fields; the review did not establish end-to-end support for every claim in an agent-generated answer. ([provenance.py](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/provenance.py))

## Efficiency and observability

**Code observation.** Context bootstrap has explicit bounds in code: 64 MiB and 50,000 events for the source snapshot, a 256 KiB output ceiling, and a 10-second overall command budget. The verified read-model cache is process-local and bounded by configured entry and serialized-byte limits; a cold open captures and verifies the full event log before replay, while reuse requires the cached source to remain unchanged. These are implementation limits and controls, not performance results. ([context_delivery.py](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/context_delivery.py); [read_model.py](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/store/read_model.py))

No retrieval-latency histogram, token/cost instrumentation, storage measurement, or write-to-recall timing was established in the inspected paths. No system or benchmark workload was executed.

## Project metric domains

All domains remain **unmeasured** for Agent Mesh: answerable retrieval and abstention; correction accuracy and stale-value rate; deletion leakage; scope-isolation leakage; evidence support and citation coverage; retrieval latency; write-to-recall delay; token use; cost; and storage efficiency. The project metric definitions and fixture specify measurement protocols; they are not Agent Mesh measurements. The current execution status record does not provide a measured Agent Mesh result. ([METRICS.md](../METRICS.md); [benchmark fixture](../fixtures/memory-benchmark-v1.json); [baseline execution status](../results/initial-baselines-status.json))

## Limits and unknowns

This is a bounded source review at the pinned repository head, based on selected code and documentation paths. It does not establish runtime correctness, answer quality, abstention behavior, authorization enforcement, deletion completeness, successful harness lifecycle delivery, or production reliability. The privacy-lifecycle contract describes proposed behavior, not implemented capability. Unknown means unverified in this review, not that the behavior is impossible.

## Sources

- [Current upstream repository at reviewed commit](https://github.com/cbalgeman/agent-mesh/tree/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd)
- [README.md — project overview and storage model](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/README.md)
- [src/agent_mesh/core/events.py — event protocol](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/events.py)
- [src/agent_mesh/core/hashing.py — canonical event hashing](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/hashing.py)
- [src/agent_mesh/store/rebuild.py — deterministic projections](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/store/rebuild.py)
- [src/agent_mesh/store/sqlite.py — SQLite read model](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/store/sqlite.py)
- [src/agent_mesh/core/provenance.py — source provenance validation](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/provenance.py)
- [src/agent_mesh/core/agent_instances.py — project-local agent identities](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/agent_instances.py)
- [src/agent_mesh/core/context_delivery.py — bounded bootstrap implementation](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/core/context_delivery.py)
- [src/agent_mesh/store/read_model.py — verified read model/cache](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/src/agent_mesh/store/read_model.py)
- [docs/context-delivery-contract.md — retrieval/delivery contract](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/docs/context-delivery-contract.md)
- [docs/privacy.md — current privacy capabilities](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/docs/privacy.md)
- [docs/privacy-lifecycle.md — future lifecycle contract](https://github.com/cbalgeman/agent-mesh/blob/5eac85ba6ab4bde08f0f8ac96ccb5d86bb1813fd/docs/privacy-lifecycle.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project baseline execution status](../results/initial-baselines-status.json)
- [Catalog identity and locator attribution only](../data/memory-systems.json)
