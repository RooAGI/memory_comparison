# System article template

Use this schema for one source reviewed system article. Keep source observations and benchmark observations in separate sections.

## Required article fields

- **Identity and review pin:** system name, repository URL, default branch, full commit SHA, review timestamp with timezone, and review status.
- **Summary:** a short, plain language description.
- **Who and what:** project owner/maintainer identity only when confirmed in upstream sources; explain whether this is a library, service, or framework.
- **Architecture and data model:** describe modules and stored objects with links to concrete files and symbols.
- **Write, update, delete, and retrieval:** describe the documented/code-inspected APIs and their limits. Say when an operation was not found or was not inspected.
- **Metric-domain evidence:** address answerable recall, abstention, correction/staleness, deletion, scope isolation, evidence/citations, latency, write-to-recall delay, tokens/cost, and storage. Label code evidence as code observations and runtime evidence as measured results.
- **Limits and unknowns:** state what the inspection or available evidence cannot establish.
- **Benchmark status:** link the project's metric definitions and result record. Do not put source claims in benchmark results.
- **Sources:** link upstream files at the full reviewed SHA and project-owned metric/result documents.

## Status vocabulary

Use **Reviewed from code** for source inspection tied to a verified repository SHA. Use **Benchmark not run** when no versioned measured result exists. Use **Measured** only for a versioned, adjudicated result record. Never turn planned fixture counts, documentation statements, source structure, or Atlas discovery metadata into measurements or project findings.

## Article data

The browser route reads `data/system-articles.json`. Each article supplies `slug`, `name`, `repository`, `branch`, `revision`, `reviewed_at`, `review_timezone`, `source_status`, `benchmark_status`, `summary`, `who_what`, section arrays, metric rows, limits, and sources. Each fact paragraph names one or more source IDs, and the source IDs resolve to URLs in the article's `sources` array.
