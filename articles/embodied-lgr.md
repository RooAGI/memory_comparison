# EmbodiedLGR — upstream unavailable

**Review status:** Not reviewed — listed upstream unavailable  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 215 / EmbodiedLGR / `embodied-lgr`  
**Listed repository locator:** [paolorv/lgr-agent](https://github.com/paolorv/lgr-agent)  
**Catalog revision (unverified as current):** `3593e6a459e5099704b4e5577e4d4339dd2bf8dc`  
**Review time:** 2026-11-26 00:33:41 UTC (2026-11-25 16:33:41 PST; America/Los_Angeles)

## Identity and attribution

The catalog resolves ordinal 215 to **EmbodiedLGR**, slug `embodied-lgr`, with the explicit listed locator above and an Atlas roster attribution pinned to revision `19199a4fc249e89c0793be06f0b166b358089ba0`. The catalog entry and Atlas page are used only for name, slug, ordinal, listed locator, and attribution. Atlas descriptions and capability evidence are not assessment evidence.[[catalog](../data/memory-systems.json)] [[atlas](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/embodied-lgr.md)]

## Exact blocker

On 2026-11-26 at 00:33 UTC, the official [listed GitHub repository page](https://github.com/paolorv/lgr-agent) rendered “Page not found.” The official [GitHub repository API](https://api.github.com/repos/paolorv/lgr-agent) returned JSON with `message: Not Found` and `status: 404`. The catalog-pinned [commit](https://github.com/paolorv/lgr-agent/commit/3593e6a459e5099704b4e5577e4d4339dd2bf8dc) and pinned [README](https://github.com/paolorv/lgr-agent/blob/3593e6a459e5099704b4e5577e4d4339dd2bf8dc/README.md) also rendered “Page not found.” Therefore I could not verify a canonical current upstream, default branch, full current head SHA, or current source contents. The catalog revision is preserved only as unverified locator metadata, not as a current review pin.[[repo](https://github.com/paolorv/lgr-agent)] [[api](https://api.github.com/repos/paolorv/lgr-agent)] [[catalog_revision](https://github.com/paolorv/lgr-agent/commit/3593e6a459e5099704b4e5577e4d4339dd2bf8dc)] [[readme](https://github.com/paolorv/lgr-agent/blob/3593e6a459e5099704b4e5577e4d4339dd2bf8dc/README.md)]

The official GitHub repository search for `lgr-agent` returned three repositories, including `insygna-research/census-paolorv-lgr-agent`, whose description refers to semantic-spatial memory for robotics. The search result does not establish that this separate repository is the canonical upstream or a continuation of the listed locator, so it was not used as review evidence.[[search](https://api.github.com/search/repositories?q=lgr-agent)]

## Architecture, operations, and evidence

Not assessed. No source or documentation from a verifiable canonical upstream was accessible. Architecture and data model; write, update, delete, and retrieval behavior; scope isolation; provenance and evidence handling; efficiency and observability; limitations; and runtime behavior all remain unknown. Atlas discovery descriptions were excluded from assessment evidence.[[repo]][[api]][[readme]]

## Metric-domain evidence

All domains are unmeasured. No system runtime, tests, or benchmarks were run.

- **Answerable retrieval and abstention — unmeasured.** No current upstream source was accessible and no workload was run.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)]
- **Correction accuracy and stale retrieval — unmeasured.** No source review or correction workload was possible.[[metrics]]
- **Deletion leakage — unmeasured.** No source review or deletion workload was possible.[[metrics]]
- **Scope isolation — unmeasured.** No source review or cross-scope workload was possible.[[metrics]]
- **Evidence support and citation coverage — unmeasured.** No source review or output adjudication was possible.[[metrics]]
- **Retrieval latency and write-to-recall delay — unmeasured.** No runtime timing samples were collected.[[metrics]]
- **Tokens, cost, and storage efficiency — unmeasured.** No usage or storage measurements were collected.[[metrics]]

## Limits and unknowns

The exact blocker is that official GitHub rendered “Page not found” for the listed repository, the catalog-pinned commit, and the pinned README; the repository API returned a 404 Not Found response. These observations do not establish whether the project was deleted, renamed, made private, or is temporarily unavailable. Canonical upstream identity, branch, current head, implementation behavior, scope boundaries, provenance, limitations, observability, and efficiency remain unverified. No implementation assessment is asserted.[[repo]][[api]][[catalog_revision]][[readme]]

## Contact

No contact email could be verified. I checked the official repository page and catalog-pinned README URL; both were unavailable. The record stores `contact_email: null` and the exact checked README URL. No address was inferred or taken from commit/profile metadata or third-party directories.[[repo]][[readme]]

## Benchmark status

**Benchmark not run.** No system runtime, tests, or benchmarks were run. See [metric definitions](../METRICS.md), the [benchmark fixture](../fixtures/memory-benchmark-v1.json), and the [execution status record](../results/initial-baselines-status.json) [[result](../results/initial-baselines-status.json)].
