# Cortana — upstream unavailable

**Review status:** Not reviewed — upstream unavailable  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 156 — Cortana / `cortana`  
**Listed repository:** [adea-ai/cortana](https://github.com/adea-ai/cortana)  
**Catalog revision (unverified as current):** `f26a1ac2b01bc903a86b0198d375c8e146ecbbde`  
**Review time:** 2026-11-25 09:24:13 UTC (2026-11-25 01:24:13 PST; America/Los_Angeles)

## Identity and blocker

The curated catalog identifies ordinal 156 as Cortana, slug `cortana`, with the explicit listed locator above. The pinned Atlas entry is retained only as roster attribution; Atlas descriptions are not assessment evidence.[[catalog](../data/memory-systems.json)] [[Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/cortana.md)]

At review time, the official [repository page](https://github.com/adea-ai/cortana), the catalog-pinned [commit](https://github.com/adea-ai/cortana/commit/f26a1ac2b01bc903a86b0198d375c8e146ecbbde), [README](https://github.com/adea-ai/cortana/blob/f26a1ac2b01bc903a86b0198d375c8e146ecbbde/README.md), and [SECURITY.md](https://github.com/adea-ai/cortana/blob/f26a1ac2b01bc903a86b0198d375c8e146ecbbde/SECURITY.md) all rendered GitHub “Page not found.” The official [repository API endpoint](https://api.github.com/repos/adea-ai/cortana) returned “API rate limit exceeded.” Consequently I could not verify the canonical current upstream, default branch, current full head SHA, source contents, or project contact. The catalog’s older revision is preserved as unverified locator metadata, not presented as the reviewed current head.[[repository page check](https://github.com/adea-ai/cortana)] [[API response](https://api.github.com/repos/adea-ai/cortana)] [[catalog-pinned commit check](https://github.com/adea-ai/cortana/commit/f26a1ac2b01bc903a86b0198d375c8e146ecbbde)]

## Architecture and data model

Not assessed. The upstream repository and pinned source pages were unavailable, and Atlas discovery descriptions are not used as implementation evidence.[[repository page check](https://github.com/adea-ai/cortana)] [[catalog-pinned commit check](https://github.com/adea-ai/cortana/commit/f26a1ac2b01bc903a86b0198d375c8e146ecbbde)]

## Write, update, delete, retrieval, and scope

Not assessed. No current upstream documentation or implementation was accessible, so write/update/delete and retrieval behavior, including isolation boundaries, remain unknown.[[repository page check](https://github.com/adea-ai/cortana)] [[pinned README check](https://github.com/adea-ai/cortana/blob/f26a1ac2b01bc903a86b0198d375c8e146ecbbde/README.md)]

## Provenance, efficiency, and observability

Not assessed because the official source repository and documentation could not be inspected. No provenance, evidence, cost, storage, latency, or observability behavior is asserted.[[repository page check](https://github.com/adea-ai/cortana)]

## Metric-domain evidence

All metric domains are unmeasured. No runtime, tests, benchmarks, or source-based implementation review was performed.[[metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

- **Answerable recall and abstention — unmeasured.** No source was accessible and no workload was run.[[metric definitions](../METRICS.md)]
- **Correction accuracy and stale retrieval — unmeasured.** No source was accessible and no workload was run.[[metric definitions](../METRICS.md)]
- **Deletion leakage — unmeasured.** No source was accessible and no workload was run.[[metric definitions](../METRICS.md)]
- **Scope isolation — unmeasured.** No source was accessible and no workload was run.[[metric definitions](../METRICS.md)]
- **Evidence support and citation coverage — unmeasured.** No source was accessible and no workload was run.[[metric definitions](../METRICS.md)]
- **Retrieval latency and write-to-recall delay — unmeasured.** No timing workload was run.[[metric definitions](../METRICS.md)]
- **Tokens, cost, and storage efficiency — unmeasured.** No accounting or storage workload was run.[[metric definitions](../METRICS.md)]

## Limits and unknowns

The exact blocker is that official GitHub returned “Page not found” for the listed repository and the catalog-pinned commit, README, and SECURITY.md, while the official API returned a rate-limit response. This does not establish whether the project was deleted, renamed, private, or temporarily unavailable. Current branch, head SHA, architecture, operations, isolation, provenance, performance, and contact are unknown.[[repository page check](https://github.com/adea-ai/cortana)] [[API response](https://api.github.com/repos/adea-ai/cortana)] [[pinned README check](https://github.com/adea-ai/cortana/blob/f26a1ac2b01bc903a86b0198d375c8e146ecbbde/README.md)] [[pinned security check](https://github.com/adea-ai/cortana/blob/f26a1ac2b01bc903a86b0198d375c8e146ecbbde/SECURITY.md)]

## Contact

No contact email was verified. The only checked official contact locations were the catalog-pinned README and SECURITY.md URLs, both of which returned Page not found; the record stores `contact_email: null` and those exact URLs.[[pinned README check](https://github.com/adea-ai/cortana/blob/f26a1ac2b01bc903a86b0198d375c8e146ecbbde/README.md)] [[pinned security check](https://github.com/adea-ai/cortana/blob/f26a1ac2b01bc903a86b0198d375c8e146ecbbde/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No system runtime, tests, or benchmarks were run. See the [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).
