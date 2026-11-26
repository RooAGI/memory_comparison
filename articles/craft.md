# craft

## Identity and review pin

- Catalog ordinal: 169
- System: craft
- Slug: `craft`
- Listed and canonical repository: https://github.com/drobins25/craft
- Catalog revision: `7006381d0b01990e5d3fc3d3b9d97cf9a5e545a0`
- Catalog revision exists in the listed repository; official GitHub commit API returned that exact SHA.
- Default branch: `main`
- Current `main` head reviewed: [c9c16fa53c214577b5aca7770b1875f53c80a101](https://github.com/drobins25/craft/commit/c9c16fa53c214577b5aca7770b1875f53c80a101)
- Review timestamp: 2026-11-25T22:17:56Z (UTC; 2026-11-25 14:17:56 PST; America/Los_Angeles)
- Identity status: **Verified**
- Review scope: repository identity, branch and revision, and correction of prior source links and identity claims. This is not a fresh implementation assessment.
- Benchmark status: **Benchmark not run**

### Resolution of the prior identity discrepancy

The catalog lists `https://github.com/drobins25/craft` and pins revision `7006381d0b01990e5d3fc3d3b9d97cf9a5e545a0`. Fresh official GitHub repository metadata reports that same repository as public, non-fork, with default branch `main`; its description identifies Craft as a Claude Code plugin. The listed URL does not redirect to `neo4j-labs/create-context-graph`. The previous review's API lookups used that unrelated destination, which caused its false missing-commit result. GitHub's official commit endpoint now confirms that the catalog-pinned SHA exists in `drobins25/craft`. The pinned Atlas roster entry names the same upstream locator and revision; it is used here only for roster/locator attribution, not as assessment evidence. ([repository metadata](https://api.github.com/repos/drobins25/craft), [pinned commit lookup](https://api.github.com/repos/drobins25/craft/commits/7006381d0b01990e5d3fc3d3b9d97cf9a5e545a0), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/craft.md))

The current `main` head was independently read from GitHub's commits API and its full commit page. The README cited below is pinned to that same full head SHA. ([current main head](https://api.github.com/repos/drobins25/craft/commits/main), [head commit page](https://github.com/drobins25/craft/commit/c9c16fa53c214577b5aca7770b1875f53c80a101), [README at reviewed head](https://github.com/drobins25/craft/blob/c9c16fa53c214577b5aca7770b1875f53c80a101/README.md))

## Assessment status

The repository identity and revision discrepancy are resolved. The prior “upstream identity not verified” blocker and claims that the pinned SHA was absent are withdrawn because they came from links aimed at the wrong repository. This link-focused re-review did not inspect implementation files or redo the system assessment, so architecture, storage behavior, retrieval, updates/deletion, scope enforcement, provenance, and operational properties remain **not assessed here**. The README at the verified head describes Craft as a Claude Code plugin and presents its product and workflow overview; that documentation is not treated as implementation verification. ([README at reviewed head](https://github.com/drobins25/craft/blob/c9c16fa53c214577b5aca7770b1875f53c80a101/README.md))

## Metric-domain evidence

All benchmark domains remain **unmeasured**. No system, tests, or benchmark workloads were run. ([metric definitions](../METRICS.md), [project result status](../results/initial-baselines-status.json), [fixture, not run](../fixtures/memory-benchmark-v1.json))

| Domain | Status | Evidence |
|---|---|---|
| Answerable retrieval and abstention | Unmeasured | No measurements were made in this link-focused re-review. |
| Correction accuracy and stale-value rate | Unmeasured | No measurements were made in this link-focused re-review. |
| Deletion leakage | Unmeasured | No measurements were made in this link-focused re-review. |
| Scope isolation | Unmeasured | No measurements were made in this link-focused re-review. |
| Evidence support and citation coverage | Unmeasured | No measurements were made in this link-focused re-review. |
| Retrieval latency | Unmeasured | No runtime measurements were made. |
| Write-to-recall delay | Unmeasured | No timed probes were run. |
| Tokens and cost | Unmeasured | No runtime measurements were made. |
| Storage efficiency | Unmeasured | No storage measurements were made. |

## Limits

This review verifies the listed repository, its default branch, current head, and the existence of the catalog-pinned revision using official GitHub sources. It corrects the prior mis-targeted Neo4j citations and the claims based on them. The pinned Atlas entry is only roster/locator attribution. No implementation behavior or benchmark result is claimed from Atlas or from this link-focused re-review. A separate source assessment would be needed to evaluate implementation behavior. ([repository metadata](https://api.github.com/repos/drobins25/craft), [current main head](https://api.github.com/repos/drobins25/craft/commits/main), [pinned commit lookup](https://api.github.com/repos/drobins25/craft/commits/7006381d0b01990e5d3fc3d3b9d97cf9a5e545a0), [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/craft.md))

## Benchmark status

**Benchmark not run.** The Craft system, its tests, and benchmark workloads were not run. The fixture is a workload specification only; the shared execution-status record contains no Craft measurement. ([metric definitions](../METRICS.md), [fixture](../fixtures/memory-benchmark-v1.json), [status record](../results/initial-baselines-status.json))

## Sources

- [Catalog identity, locator, and pinned revision](../data/memory-systems.json)
- [Atlas roster entry, locator attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/craft.md)
- [Official GitHub repository metadata](https://api.github.com/repos/drobins25/craft)
- [Official current main commit endpoint](https://api.github.com/repos/drobins25/craft/commits/main)
- [Official current main head commit page](https://github.com/drobins25/craft/commit/c9c16fa53c214577b5aca7770b1875f53c80a101)
- [Official API lookup for catalog-pinned revision](https://api.github.com/repos/drobins25/craft/commits/7006381d0b01990e5d3fc3d3b9d97cf9a5e545a0)
- [README at verified current destination head](https://github.com/drobins25/craft/blob/c9c16fa53c214577b5aca7770b1875f53c80a101/README.md)
- [Project metric definitions](../METRICS.md)
- [Project fixture, not run](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution-status record](../results/initial-baselines-status.json)
