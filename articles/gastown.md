# Gas Town

**Review status:** Reviewed from code and official documentation at `main` [`94cc82289d2ead275a62e1db4ef1d4ada4a1f98e`](https://github.com/gastownhall/gastown/commit/94cc82289d2ead275a62e1db4ef1d4ada4a1f98e). Review time: 2026-11-25 20:49:38 UTC (12:49:38 PST; America/Los_Angeles).

## Summary

Gas Town is a multi-agent workspace manager. Its memory feature stores typed text values through Beads key-value commands and injects the full set into agent context at prime time.[readme][remember][prime] It does not implement relevance-ranked retrieval in the inspected path.[prime][memories]

## Who and what

The official README describes Gas Town as a multi-agent workspace manager with persistent work tracking backed by Beads.[readme] Ordinal 251 resolves to Gas Town, slug `gastown`, and listed locator `https://github.com/gastownhall/gastown`; the pinned Atlas entry is retained only for roster identity and locator attribution, not as assessment evidence.[catalog][atlas]

## Architecture and data model

The memory interface consists of `gt remember`, `gt memories`, `gt forget`, and memory injection during `gt prime`.[remember][memories][forget][prime] The commands delegate storage to Beads KV through `bd kv set`, `bd kv list --json`, and `bd kv clear`; Gas Town does not define a separate memory database or record schema in these paths.[remember][memories][forget]

Keys use `memory.<type>.<slug>`, with feedback, project, user, reference, and general categories. Values are plain strings; the inspected path adds no per-value source, author, timestamp, confidence, or lifecycle status.[remember] Legacy untyped keys are read as general memories.[remember]

Gas Town documentation describes Beads as persistent work tracking and Dolt as its data plane. This review did not inspect Beads' own storage implementation, so the exact physical layout and transaction behavior for memory KV values are not established here.[readme][security]

GitHub identifies `main` as the default branch. The official commits feed lists [`94cc82289d2ead275a62e1db4ef1d4ada4a1f98e`](https://github.com/gastownhall/gastown/commit/94cc82289d2ead275a62e1db4ef1d4ada4a1f98e) as the current head; the official Git remote and shallow checkout resolved to the same full SHA.[repo][head][commit]

## Write, update, delete, and retrieval

`gt remember` accepts nonempty text, an optional type, and an optional key. Without an explicit key it derives a slug from up to the first five words; different values with the same opening words can therefore collide. A write to an existing type/key replaces the stored value through `bd kv set`.[remember]

`gt memories` lists the Beads KV map, optionally filtering by type or a case-insensitive substring of the key, value, or type. Results are sorted by type priority and key; this is substring lookup, not semantic ranking.[memories]

At prime time, Gas Town lists all Beads KV entries in the selected work directory, filters to `memory.` keys, sorts and groups them, then prints every memory by category. Feedback and user context appear before project, reference, and general entries. The inspected path has no relevance selection or explicit count/token cap.[prime]

`gt forget` resolves typed or legacy keys and removes a match with `bd kv clear`. The inspected Gas Town code does not add a tombstone, preserve prior text, or expose a memory-specific mutation history.[forget]

## Scope, provenance, efficiency, and observability

The role guidance recommends storing user feedback, project context, user preferences, and references, while avoiding information recoverable from code or documentation.[mayor] Those are instructions to agents; the stored string format does not enforce provenance, evidence, or trust labels.[remember]

Prime invokes Beads using a resolved directory for the work directory. The memory key has no tenant, project, agent, or user field, so effective isolation depends on Beads routing and workspace setup; the reviewed code does not independently establish caller-level authorization or cross-rig isolation.[prime][security]

The README describes structured OTLP logs and metrics for agent operations, including Beads calls and durations.[readme] The inspected memory path defines no separate memory telemetry contract. If the KV listing fails, memory injection returns silently.[prime]

Each prime loads the full set of memory KV values and sorts them for output; no relevance index or memory-specific size bound is present in the inspected code.[prime] This implies work proportional to the listed data and context size, but latency, token use, cost, and storage efficiency were not measured.[prime][metrics][status]

## Metric-domain evidence

- Answerable retrieval and abstention — unmeasured; prime injects all memories and the list command offers substring filtering. No answerability probe was run.[prime][memories][metrics][status]
- Correction accuracy and stale-value rate — unmeasured; a same-key write overwrites, but no correction workload was evaluated.[remember][metrics][status]
- Deletion leakage — unmeasured; forget calls KV clear, but no residual-data probe was run.[forget][metrics][status]
- Scope isolation — unmeasured; no cross-workspace or cross-agent isolation test was run.[prime][metrics][status]
- Evidence support precision and citation coverage — unmeasured; values are unstructured strings and no claim-support evaluation was run.[remember][metrics][status]
- Retrieval latency and write-to-recall delay — unmeasured; no timing probe was run.[prime][metrics][status]
- Token use and cost — unmeasured; no context-size or model-cost data was collected.[prime][metrics][status]
- Storage efficiency — unmeasured; no memory-attributed storage measurement was collected.[remember][metrics][status]

Project benchmark status is [`not_run`](../data/system-reviews/gastown.json); see [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json). These files define the project workload/status; no benchmark was executed.[metrics][fixture][status]

## Limits and unknowns

- This is a bounded review of Gas Town's memory commands and prime-time injection at one verified main SHA; it did not inspect Beads internals.
- The review cannot establish the physical KV storage layout, transaction and retention behavior, or backup guarantees from Gas Town sources alone.
- Effective memory scope depends on workspace-to-Beads routing; cross-workspace authorization and isolation were not tested.
- The inspected injection path has no visible size bound; practical context growth and prime failure behavior were not measured.
- The stored text format has no enforced provenance, evidence, or trust-state fields.
- No Gas Town runtime, benchmarks, or tests were run.

## Sources

- [Official repository](https://github.com/gastownhall/gastown), [main feed](https://github.com/gastownhall/gastown/commits/main.atom), and [verified head](https://github.com/gastownhall/gastown/commit/94cc82289d2ead275a62e1db4ef1d4ada4a1f98e).
- [README](https://github.com/gastownhall/gastown/blob/94cc82289d2ead275a62e1db4ef1d4ada4a1f98e/README.md), [memory write](https://github.com/gastownhall/gastown/blob/94cc82289d2ead275a62e1db4ef1d4ada4a1f98e/internal/cmd/remember.go), [list/search](https://github.com/gastownhall/gastown/blob/94cc82289d2ead275a62e1db4ef1d4ada4a1f98e/internal/cmd/memories.go), [delete](https://github.com/gastownhall/gastown/blob/94cc82289d2ead275a62e1db4ef1d4ada4a1f98e/internal/cmd/forget.go), and [prime injection](https://github.com/gastownhall/gastown/blob/94cc82289d2ead275a62e1db4ef1d4ada4a1f98e/internal/cmd/prime.go).
- [Role memory guidance](https://github.com/gastownhall/gastown/blob/94cc82289d2ead275a62e1db4ef1d4ada4a1f98e/internal/templates/roles/mayor.md.tmpl) and [security policy](https://github.com/gastownhall/gastown/blob/94cc82289d2ead275a62e1db4ef1d4ada4a1f98e/SECURITY.md).
- [Roster identity and locator](../data/memory-systems.json); Atlas attribution is not assessment evidence.
- [Metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).
