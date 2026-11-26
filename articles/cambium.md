# Cambium

## Identity and review pin

- **Ordinal:** 110
- **Listed and canonical repository:** https://github.com/KimGLee/Cambium
- **Default branch:** main
- **Reviewed head:** [6ed60b8cbacf121fa11f6b0753746e4b6d9b7216](https://github.com/KimGLee/Cambium/commit/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216)
- **Reviewed:** 2026-11-25 01:20:35 UTC (2026-11-24 17:20:35 PST; America/Los_Angeles)
- **Status:** Reviewed from code; benchmark not run
- **Catalog attribution:** [ordinal 110 source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0) is retained only for identity.

## Summary

Cambium is a governance standard and reference toolset for LLM-maintained knowledge repositories. It provides policies, controlled mutation tools, evidence ledgers, recovery state, and agent-host interfaces. Adopters own the corpus and choose a profile; Cambium is not itself a knowledge base or RAG engine.[[official README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]

## Who and what

The official repository describes Cambium as a governance standard and reference toolset. Its layers include a normative kernel, adopter-selected profile, non-authoritative Cards, Read Sets, deterministic Tools, and adopter-owned `.cambium/` state. This checkout is intentionally uninstantiated and selects no adopter profile.[[README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]

## Architecture and data model

The adopter owns the corpus, profile decisions, task state, queues, deltas, receipts, and recovery evidence. The repository supplies schemas and writers for those records rather than shipping a default corpus.[[README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]

Read Sets declare canonical inputs for an already selected route or phase. Cards are short checklists; canonical material resolved through a paired Read Set owns the rule when a Card is insufficient or disputed. This is bounded context loading, not ranked semantic memory search.[[Read Set contract](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/execution/context_delivery/read_set_contract.py)]

The stable CLI contract and agent-interface policy compile into MCP and per-host projections. The typed runner invokes registered capabilities and stops at semantic boundaries; the README says it is not a scheduler.[[MCP implementation](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/platform/agent_interface/mcp_server.py)] [[README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]

## Write, update, delete, and retrieval

**Write/update — code observation.** Coverage Deltas pass through controlled writers. The delta path validates bound state and applies typed transitions; profile editing uses snapshot preconditions and validation. The README says not to hand-edit canonical state.[[delta writer](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/execution/task_runtime/apply_delta.py)] [[profile validation](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/governance/profile/check_profile.py)] [[README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]

**Delete/supersession — code observation.** The reviewed model emphasizes controlled lifecycle transitions and retained history. No general claim-deletion operation or end-to-end corpus erasure guarantee is established by these sources.[[delta writer](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/execution/task_runtime/apply_delta.py)] [[README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]

**Retrieval — code observation.** Cambium provides no retrieval engine. Read Sets bound canonical sources for a route; the tools do not rank memories or select routes autonomously.[[Read Set contract](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/execution/context_delivery/read_set_contract.py)] [[MCP implementation](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/platform/agent_interface/mcp_server.py)]

**Provenance and evidence — code observation.** Receipts record tool/check/target/result/sequence and queue identity and are append-only. The README distinguishes what a host was sent from proof of model-context placement or agent cognition. Local hashes detect drift but are not signatures or an external trust anchor.[[receipt writer](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/platform/common/receipts.py)] [[receipt schema](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/schemas/receipt.template.jsonl)] [[README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]

## Metric-domain evidence

All domains are **unmeasured**. These are source observations, not benchmark outcomes.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)] [[fixture](../fixtures/memory-benchmark-v1.json)]

- **Recall and abstention:** route-bound source declarations are visible; no answer-quality probes were run.[[Read Set](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/execution/context_delivery/read_set_contract.py)]
- **Correction and staleness:** controlled delta transitions exist; no correction workload was run.[[delta writer](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/execution/task_runtime/apply_delta.py)]
- **Deletion leakage:** no post-delete or corpus-erasure probe was measured.[[README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]
- **Scope isolation:** writer identity and batch checks are source-visible; no cross-adopter isolation workload was run.[[delta writer](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/execution/task_runtime/apply_delta.py)]
- **Evidence and citations:** receipt/proof mechanisms are documented; no claim-support adjudication was performed.[[receipt writer](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/platform/common/receipts.py)]
- **Efficiency and observability:** source-visible mechanisms exist, but no latency, token, cost, storage, or write-to-recall measurements were collected.[[README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]

## Limits and unknowns

The repository is uninstantiated: it selects no adopter profile and supplies no governed corpus. Profile fit, freshness, and ongoing corpus maintenance are not exercised. The README also lists scheduling, worker isolation, authenticated reviewer identity, and protected whole-workspace execution among capabilities not shipped yet.[[README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]

This is read-only source inspection at the verified `main` head. Cambium and its tests were not executed; source structure does not establish runtime behavior or host enforcement.[[reviewed commit](https://github.com/KimGLee/Cambium/commit/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216)]

## Benchmark status

**not_run.** Metric definitions, fixtures, and execution-status records describe evaluation protocol and status; they are not Cambium measurements. No system, benchmarks, or tests were run.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[status](../results/initial-baselines-status.json)]

## Sources

- [Official repository](https://github.com/KimGLee/Cambium)
- [Verified main head](https://github.com/KimGLee/Cambium/commit/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216)
- [Official README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)
- [Coverage Delta transaction](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/execution/task_runtime/apply_delta.py)
- [Profile validation and snapshot-bound editing](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/governance/profile/check_profile.py)
- [Read Set contract](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/execution/context_delivery/read_set_contract.py)
- [MCP interface implementation](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/platform/agent_interface/mcp_server.py)
- [Receipt creation and publication](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/platform/common/receipts.py)
- [Receipt schema](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/Tools/schemas/receipt.template.jsonl)
- [Metric definitions](../METRICS.md)
- [Benchmark execution status](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated identity and attribution entry](../data/memory-systems.json)
- [Atlas discovery attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cambium.md)

**Contact:** the official README was checked and no published contact email appears. The repository root listing contains no `SECURITY.md` or `SUPPORT.md`; no email was inferred.[[README](https://github.com/KimGLee/Cambium/blob/6ed60b8cbacf121fa11f6b0753746e4b6d9b7216/README.md)]
