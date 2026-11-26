# EAN AgentOS — upstream unavailable

**Review status:** Not reviewed — upstream could not be verified  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 205 — EAN AgentOS / `ean-agentos`  
**Listed repository:** [eanai-ro/ean-agentos](https://github.com/eanai-ro/ean-agentos)  
**Catalog revision (not verified as current):** `0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6`  
**Review time:** 2026-11-25 11:50:42 UTC (2026-11-25 03:50:42 PST; America/Los_Angeles)

## Identity and blocker

The curated catalog identifies ordinal 205 as EAN AgentOS, slug `ean-agentos`, with the explicit listed repository locator above. The pinned Atlas entry is retained only for roster identity and locator attribution; its descriptions are not assessment evidence. ([catalog entry](../data/memory-systems.json)) ([Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/ean-agentos.md))

At review time, the official [repository page](https://github.com/eanai-ro/ean-agentos), catalog-pinned [commit](https://github.com/eanai-ro/ean-agentos/commit/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6), [README](https://github.com/eanai-ro/ean-agentos/blob/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6/README.md), and [SECURITY.md](https://github.com/eanai-ro/ean-agentos/blob/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6/SECURITY.md) rendered GitHub “Page not found.” The official [repository API](https://api.github.com/repos/eanai-ro/ean-agentos) returned HTTP 404 with “Not Found.” A read-only `git ls-remote --symref` attempt could not obtain refs: Git reported that it could not read a GitHub username because the device was not configured. These checks do not establish whether the repository was removed, renamed, private, or temporarily inaccessible.

The catalog pin is preserved as roster metadata only. I could not verify a canonical current upstream, default branch, or current full head SHA, and could not inspect source or documentation. No implementation assessment is claimed. ([repository check](https://github.com/eanai-ro/ean-agentos)) ([API response](https://api.github.com/repos/eanai-ro/ean-agentos)) ([pinned commit check](https://github.com/eanai-ro/ean-agentos/commit/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6))

## Architecture and data model

Not assessed. No official current source or documentation could be inspected. Atlas roster descriptions are excluded from implementation evidence. ([repository check](https://github.com/eanai-ro/ean-agentos)) ([pinned README check](https://github.com/eanai-ro/ean-agentos/blob/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6/README.md))

## Write, update, delete, retrieval, and scope

Not assessed. Write, update, deletion, retrieval, and scope-isolation behavior remain unknown because no upstream implementation or documentation was accessible. ([repository check](https://github.com/eanai-ro/ean-agentos)) ([pinned README check](https://github.com/eanai-ro/ean-agentos/blob/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6/README.md))

## Provenance, efficiency, and observability

Not assessed. No source evidence was available for provenance, evidence handling, efficiency, or observability. ([repository check](https://github.com/eanai-ro/ean-agentos)) ([pinned README check](https://github.com/eanai-ro/ean-agentos/blob/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6/README.md))

## Metric-domain evidence

All benchmark domains are unmeasured. No EAN AgentOS runtime, tests, or benchmarks were run, and no implementation review was possible. ([metric definitions](../METRICS.md)) ([benchmark status](../results/initial-baselines-status.json)) ([benchmark fixture](../fixtures/memory-benchmark-v1.json))

- **Answerable recall and abstention — unmeasured.** Upstream source was unavailable; no workload was run.
- **Correction accuracy and stale retrieval — unmeasured.** Upstream source was unavailable; no workload was run.
- **Deletion leakage — unmeasured.** Upstream source was unavailable; no workload was run.
- **Scope isolation — unmeasured.** Upstream source was unavailable; no workload was run.
- **Evidence support and citation coverage — unmeasured.** Upstream source was unavailable; no workload was run.
- **Retrieval latency and write-to-recall delay — unmeasured.** No timed workload was run.
- **Tokens and cost — unmeasured.** No usage or cost workload was run.
- **Storage efficiency — unmeasured.** No storage workload was run.

## Limits and unknowns

This task is blocked at upstream verification. The listed repository, catalog-pinned commit, README, and SECURITY.md returned GitHub “Page not found”; the repository API returned 404; and `git ls-remote` could not read a username in the configured device environment. This evidence does not determine whether the project was removed, renamed, private, or temporarily inaccessible. Current canonical repository, default branch, head SHA, architecture, write/update/delete/retrieval behavior, scope isolation, provenance, efficiency, observability, and official contact remain unknown. ([repository page](https://github.com/eanai-ro/ean-agentos)) ([API response](https://api.github.com/repos/eanai-ro/ean-agentos)) ([pinned commit](https://github.com/eanai-ro/ean-agentos/commit/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6)) ([pinned README](https://github.com/eanai-ro/ean-agentos/blob/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6/README.md)) ([pinned security policy](https://github.com/eanai-ro/ean-agentos/blob/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6/SECURITY.md))

## Contact

No contact email could be verified. The official repository, pinned README, and pinned SECURITY.md were checked but were unavailable; `contact_email` is null and the checked URLs are recorded. No profile, commit metadata, or third-party directory was used. ([repository page](https://github.com/eanai-ro/ean-agentos)) ([pinned README](https://github.com/eanai-ro/ean-agentos/blob/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6/README.md)) ([pinned security policy](https://github.com/eanai-ro/ean-agentos/blob/0c5e0ecfdb971f8b38c9ffc0848ef9e33fec6da6/SECURITY.md))

## Benchmark status

**Benchmark not run.** No system runtime, tests, or benchmarks were run. See the [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).
