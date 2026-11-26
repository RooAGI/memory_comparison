# Aukora Kernel source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 75 / Aukora Kernel / aukora-kernel  
**Listed repository locator:** [aumara-xyz/aukora-kernel](https://github.com/aumara-xyz/aukora-kernel)  
**Current canonical repository:** [aumara-xyz/aukora-kernel](https://github.com/aumara-xyz/aukora-kernel)  
**Default branch / reviewed head:** main / b441edc4d17de778d30ae955f46408edae39bffe  
**Review time:** 2026-11-24 22:00:06 UTC (14:00:06 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog places Aukora Kernel at ordinal 75 with the listed repository locator above. I recorded its linked Atlas page only as catalog attribution; its descriptions, marks, and layout were not used as assessment evidence. The official repository page shows main as the default branch and latest commit prefix b441edc; the official [main commit feed](https://github.com/aumara-xyz/aukora-kernel/commits/main.atom) reports the full head b441edc4d17de778d30ae955f46408edae39bffe (feed updated 2026-07-15T22:00:13Z). [[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/aumara-xyz/aukora-kernel)] [[main branch feed](https://github.com/aumara-xyz/aukora-kernel/commits/main.atom)] [[reviewed full head](https://github.com/aumara-xyz/aukora-kernel/commit/b441edc4d17de778d30ae955f46408edae39bffe)]

## Summary

Aukora Kernel is an authority and receipt framework for agent actions, not a standalone memory database. At the reviewed head, memory code appears in the wider Symbiote reference application: a local IDE JSONL store and a separate Convex memory path. The portable @aukora/kernel package has no filesystem, network, or persistence capability. This review covers the memory paths visible in the repository and keeps their source observations separate from any measured behavior. [official README](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/README.md) [Convex reference README](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/README.md)

## Who and what

The GitHub repository is owned by the aumara-xyz organization; the official README presents the project as an authorization-and-receipt kernel with a broader PROVEN-LAB reference application. It describes memory as one component in that broader stack. The memory implementation discussed below belongs to the host/reference layers, rather than the portable verifier/reducer package. [official repository](https://github.com/aumara-xyz/aukora-kernel) [official README](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/README.md)

## Architecture and data model

The README separates packages/kernel, a portable deterministic verifier/reducer, from convex, a broader reference app with persistence and custody demonstrations. Its package boundary excludes Convex, filesystems, networks, ambient time, signing, and live execution. The repository also contains an IDE-facing Symbiote memory implementation, so Aukora memory is not one interchangeable backend. [official README](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/README.md) [local IDE memory](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/memory.ts) [Convex reference README](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/README.md)

The local IDE path stores JSONL entries under $HOME/.aukora-symbiote by default, with environment overrides for the memory and receipt files. Each entry carries a version, actor, chain key, sequence, remember/forget operation, tier, content hash, timestamp, previous hash, plaintext (nullable), and active/tombstoned status. The separate receipt record includes the gate-argument hash and content hash, not plaintext. [memory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/memory.ts) [chain.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/chain.ts)

The Convex path uses an aukora_memory row with owner root, writer principal, delegation ID, receipt and memory hashes, node, visibility, key, value, and optional embedding. The inspected schema and memory module expose owner/key and owner indexes, plus search and vector indexes. This path is part of the reference application, not the portable package contract. [aumlokMemory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts) [Convex schema](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/schema.ts) [Convex reference README](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/README.md)

## Write, update, delete, and retrieval

**Write.** In the local IDE module, remember calls the shared memory permission gate with the proposed content as the diff, then hashes the content and appends a receipt before writing the row. Both receipt append and store write call fsync; errors return a fail-closed pause result. The module says the gate also blocks while AUMLOK is locked and rejects apparent secrets. [memory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/memory.ts)

The Convex aumlokMemoryWrite mutation requires the memory.write action and local-write ring, consumes a delegation-manifest use, issues a one-shot grant, checks intent/token authorization, writes a receipt binding the manifest and memory hash, then inserts the row in the same Convex mutation. The implementation uses an optimistic concurrency count on manifest uses so concurrent reuse of the same use sequence conflicts. [aumlokMemory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts)

**Update.** I found no ordinary in-place value-update API in the reviewed local memory module or Convex memory write surface. The Convex write path inserts a row; the local API exposes remember and forget. Whether uninspected callers provide a higher-level correction workflow remains unknown. [memory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/memory.ts) [aumlokMemory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts)

**Delete and erasure.** Local forget is authority-gated, clears the matching entry's plaintext, marks it tombstoned, retains its hash-chain position, and appends a forget receipt. Convex aumlokMemoryErase uses the owner's active root key and a dedicated signed erase request; it scrubs the serving value to an empty string, preserves a countable row stub and original hashes, and adds an erasure receipt. The source explicitly limits this claim: underlying Convex document versions and SQLite pages can persist for their retention/vacuum periods, and unsalted commitments can still reveal a guessed value. [memory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/memory.ts) [aumlokMemory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts)

**Retrieval.** Local recall reads active remember entries for the selected chain key, orders them by sequence, and applies an optional tail limit; corrupt JSONL is surfaced as corrupt with no facts. Convex point recall is owner/key addressed and checks content against its memory hash and receipt evidence before returning it. The code requires proof of possession by the owner root or the still-authorized delegated writer, and returns no content for an unrelated principal. [memory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/memory.ts) [aumlokMemory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts)

The Convex module also contains owner-only full-text and vector search candidates that return keys, then leave content reads to the integrity-checked recall path. Both are explicitly described in source as benchmark candidates not called by any lane at this revision; they should not be presented as the active recall route. [aumlokMemory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts)

**Scope isolation.** Local memory uses a default auma-ide chain key, and recall filters by the supplied/default key. The store is a shared local file, and the inspected local recall API has no principal check; a chain key is a filter rather than proof of caller identity. In Convex, writes bind a resource to the manifest owner root; recall accepts the owner or the manifest's delegated writer while that manifest remains valid. Search is owner-root-only. The Convex module is registered as internal-only, and its README says calls require the self-hosted admin key; the application-level authorization properties should not be generalized to an arbitrary deployment. [memory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/memory.ts) [aumlokMemory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts) [Convex reference README](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/README.md)

**Provenance and evidence.** The local receipt chain binds actor, chain key, sequence, operation, content hash, previous hash, timestamp, and a hash of the gate arguments. verifyChain recomputes links and cross-checks the independent receipt file, but the source explicitly says this local layer is not a signature: an attacker able to rewrite both files consistently is outside that check. In Convex, write receipts bind the manifest, owner, subject, fingerprint, use sequence, memory hash, and node; the row stores receipt and content-binding hashes. Reads re-derive the content binding, and erase retains a receipt-backed stub. Neither mechanism proves that remembered content is true; the root README describes receipts as evidence of reported state, not truth. [memory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/memory.ts) [chain.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/chain.ts) [aumlokMemory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts) [official README](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/README.md)

**Source-visible efficiency and observability.** The local path loads and parses the JSONL store to select a chain, sorts entries for sequence order, and rewrites the complete entry file on mutation; the receipt log is append-only. The Convex path has owner/key and search indexes; search over-fetches a bounded multiple and vector search caps its candidate pool. Verification returns chain length or checked/flagged/quarantined/deleted/erased counts and reasons. These are code-visible work bounds and diagnostic outputs, not latency, throughput, token, cost, or storage measurements. [memory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/memory.ts) [aumlokMemory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts) [Convex schema](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/schema.ts)

## Metric-domain evidence

Every metric domain is unmeasured for this review. Source-visible hash checks, scope predicates, indexes, query limits, and diagnostics are implementation evidence only. No runtime or benchmark probes were run for recall/abstention, correction/staleness, deletion leakage, scope isolation, evidence support/citation coverage, latency, write-to-recall delay, token/cost, or storage efficiency. The project metric definitions, fixture, and execution-status record describe the review protocol; they are not Aukora results. [[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This review inspected the root README and security policy, local IDE memory and chain code, Convex memory/schema, and the Convex subproject README at the verified repository head. It did not run the system, tests, or benchmark workloads. The repository describes itself as a PROVEN-LAB/research engineering artifact and explicitly says it is not a production deployment. The separate boot-recall module says it has no current importer; its pure region transform is the tested part, but tests were not run here. Actual caller wiring, production authorization, deployment state, and erasure across storage snapshots/backups remain unverified. The local JSONL chain is hash-chained and receipt-backed, not signed; the Convex path's indexed search candidates are not wired into an active lane according to their source comments. [official README](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/README.md) [SECURITY.md](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/SECURITY.md) [bootRecall.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/runtime/bootRecall.ts) [aumlokMemory.ts](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts)

## Contact-list follow-up

The official pinned [SECURITY.md](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/SECURITY.md) publishes **auma@aumara.xyz** for private vulnerability reports. The repository README was also checked; it did not publish a contact email. No profile or third-party email sources were used.

## Benchmark status

**Benchmark not run.** I did not run Aukora, tests, or benchmarks. The project metric definitions, fixture, and the not_run execution-status record are linked here only to define what would be measured; they are not measured Aukora results. [[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Official repository](https://github.com/aumara-xyz/aukora-kernel)
- [Official main branch commit feed](https://github.com/aumara-xyz/aukora-kernel/commits/main.atom)
- [Reviewed full head commit](https://github.com/aumara-xyz/aukora-kernel/commit/b441edc4d17de778d30ae955f46408edae39bffe)
- [README.md](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/README.md)
- [Symbiote local IDE memory](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/memory.ts)
- [Local memory hash-chain primitives](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/chain.ts)
- [Convex memory and authorization implementation](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/aumlokMemory.ts)
- [Convex schema](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/schema.ts)
- [Convex reference README](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/convex/README.md)
- [Boot recall integration source](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/apps/symbiote/memory/runtime/bootRecall.ts)
- [Security policy and published contact](https://github.com/aumara-xyz/aukora-kernel/blob/b441edc4d17de778d30ae955f46408edae39bffe/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and attribution](../data/memory-systems.json)
- [Atlas roster attribution source, identity only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/aukora-kernel.md)

**Verification boundary:** no Aukora runtime, benchmark workload, or tests were run.

---
