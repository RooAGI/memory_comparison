# Engram Cognitive source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 224 / Engram Cognitive / engram-cognitive  
**Listed repository locator:** [TAIPANBOX/engram](https://github.com/TAIPANBOX/engram)  
**Catalog source attribution:** [Agent Memory Atlas report at catalog revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/engram-cognitive.md)  
**Current canonical repository:** [TAIPANBOX/engram](https://github.com/TAIPANBOX/engram)  
**Default branch / reviewed head:** main / [08ee3bf5a9e50cf067f50221a8ac77c9adfa539e](https://github.com/TAIPANBOX/engram/commit/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e)  
**Review time:** 2026-11-25 19:24:05 UTC (11:24:05 PST; America/Los_Angeles). GitHub identifies main as the default branch; the official main Atom feed identifies the full head SHA.  
**Published contact:** No email was found in the pinned official README or SECURITY.md, or on the official [Engram website](https://it-rat.com/services/engram.html). The JSON stores a null email and the exact pinned SECURITY.md URL checked. The policy directs vulnerability reports to GitHub private security advisories.

## Identity and scope

The curated roster places **Engram Cognitive** at ordinal 224, slug `engram-cognitive`, and lists `https://github.com/TAIPANBOX/engram`. Its Atlas attribution is the pinned report at revision `19199a4fc249e89c0793be06f0b166b358089ba0`. The roster is used only for identity and locator context; Atlas descriptions, marks, and prose are not assessment evidence. [[Roster entry](../data/memory-systems.json)] [[Catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/engram-cognitive.md)]

GitHub identifies `TAIPANBOX/engram` as the canonical repository and `main` as its default branch. The official main-branch Atom feed identifies head `08ee3bf5a9e50cf067f50221a8ac77c9adfa539e`. Upstream file links below are pinned to that revision. [[Repository](https://github.com/TAIPANBOX/engram)] [[Main history feed](https://github.com/TAIPANBOX/engram/commits/main.atom)] [[Reviewed head](https://github.com/TAIPANBOX/engram/commit/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e)]

Engram is a local-first Python library that stores agent memory in an embeddable SQLite file. The reviewed README documents episodic observations, semantic facts, graph relationships, a CLI and optional MCP/framework integrations. [[README](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/README.md)] [[API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)]

## Architecture and data model

**Code and documentation observations.** The store separates raw episodic observations from semantic subject-predicate-object facts, entities, graph edges, reflection runs, and access records. Episodes can carry timestamps, actors, tags, salience, emotional value, agent scope, provenance, and quarantine state. Facts retain validity and recorded-time fields, confidence, source derivations, and trust metadata. [[Data flow](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/DATA_FLOW.md)] [[Schema](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/schema.py)] [[API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)]

The local embedder writes vectors to sqlite-vec, while FTS5 provides keyword search. The vector schema makes agent identity a partition key and timestamps index metadata, allowing scope and `as_of` constraints to be applied within the KNN scan. The store configures SQLite WAL and serializes access to its shared connection. [[Schema](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/schema.py)] [[Store](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/store.py)] [[Core](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/core.py)]

WorkingMemory is a bounded LRU scratchpad that can spill evicted values into episodic memory. Reflection is a separate slower path: an optional LLM adapter extracts facts, and reflection can build graph edges, detect contradictions, and apply importance decay. [[README](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/README.md)] [[Data flow](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/DATA_FLOW.md)] [[Reflection](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/reflection.py)]

## Write, update, delete, and retrieval

**Write.** `observe()` records an episode, computes a local embedding, and updates the text index without an LLM call. `observe_many()` batches embedding and insertion in one transaction. In the library API, provenance defaults to external; older rows without the provenance field are returned as unknown. [[API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)] [[Core](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/core.py)] [[Schema](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/schema.py)]

**Update and correction.** `assert_fact()` writes a semantic fact directly; `reflect()` and `reflect_async()` extract facts from episodes using the configured LLM adapter. Superseded facts are closed with temporal metadata rather than overwritten. `refute_fact()` closes a fact and marks dependent facts as undermined while retaining their history. These source paths do not establish measured correction accuracy. [[API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)] [[Reflection](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/reflection.py)] [[Store](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/store.py)]

**Delete and compression.** The public API includes forgetting episodes, facts, and entities with connected records. Compression can write summaries and remove source episodes. A source review cannot establish erasure from backups, exported copies, or external systems. [[API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)] [[Core](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/core.py)] [[Store](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/store.py)]

**Retrieval.** Recall supports cosine vector search, hybrid BM25 plus cosine ranking, and graph spreading activation. It accepts time and agent filters, supports explicit cross-agent recall, and logs access for importance reinforcement. The existence of these paths says nothing by itself about answer quality or latency. [[API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)] [[Retrieval](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/retrieval.py)] [[Graph](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/graph.py)]

## Scope isolation, provenance, and evidence

The library defaults to unscoped recall when no `agent_id` is supplied; callers need to pass the intended scope. MCP binds a server to its configured agent identity, refuses calls naming a different agent, sets provenance itself, and can quarantine subsequent writes after untrusted content is read. MCP runs over stdio and intentionally does not expose reflection. [[API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)] [[MCP server](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/mcp_server.py)]

Recall and `why()` return provenance and quarantine metadata. Facts can link to source episodes, and optional Agent Passport NDJSON events record writes, forgets, reflections, and contradictions. These features improve traceability but do not prove that a generated answer claim is supported by the linked observation. [[README](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/README.md)] [[Events](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/events.py)] [[API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)]

## Efficiency and observability

Source-visible design includes local embeddings, FTS/vector hybrid search, batched writes, buffered access logging, and WAL-backed SQLite. Optional event output is off by default. The inspected project docs publish performance figures from earlier named runs; this review did not reproduce them or collect runtime traces, latency, token, cost, or storage measurements. [[Data flow](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/DATA_FLOW.md)] [[API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)] [[Events](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/events.py)]

## Metric-domain evidence

All metric domains below are **unmeasured in this review**. The project metric definitions and shared execution record are linked for context; fixture cases are planned workload, not results. [[Metrics](../METRICS.md)] [[Execution status](../results/initial-baselines-status.json)] [[Fixture](../fixtures/memory-benchmark-v1.json)]

| Domain | Review evidence |
|---|---|
| Answerable retrieval and abstention | Retrieval modes are present; no probes were run. [[Retrieval](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/retrieval.py)] |
| Correction and stale values | Temporal supersession and refutation paths are present; no correction workload was run. [[Reflection](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/reflection.py)] |
| Deletion leakage | Forget APIs exist; no post-delete probes were run. [[API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)] |
| Scope isolation | Indexed agent filtering and MCP server identity checks exist; no cross-agent workload was run. [[Schema](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/schema.py)] [[MCP server](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/mcp_server.py)] |
| Evidence support and citation coverage | Provenance and source links exist; no answers were scored against evidence. [[Events](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/events.py)] |
| Latency and write-to-recall delay | No workload was timed in this review. [[Metrics](../METRICS.md)] |
| Tokens, cost, and storage efficiency | No accounting or storage measurements were collected. [[Metrics](../METRICS.md)] |

## Limits and unknowns

- This is a bounded read-only review of the pinned README, data-flow and API documentation, and selected core, store, retrieval, reflection, schema, graph, event, and MCP code.
- Agent filters and MCP identity checks are code-level mechanisms; deployment configuration and cross-agent leakage were not tested.
- Reflection and compression can call an external LLM adapter. Their outputs and costs depend on configuration and provider behavior.
- Complete physical erasure from backups or exported copies is not established by the inspected APIs.
- No Engram runtime, tests, or benchmark workloads were run. Runtime correctness, retrieval quality, deletion leakage, isolation leakage, and performance remain unknown here.

## Contact check

The official pinned README and [SECURITY.md](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/SECURITY.md) and the official project website were checked for a published contact email. No email was found. The security policy directs vulnerability reports to [GitHub private security advisories](https://github.com/TAIPANBOX/engram/security/advisories/new). No commit/profile metadata or third-party directory was used.

## Benchmark status

**Benchmark not run.** No Engram runtime, tests, or benchmark workload was executed for this review. Source observations and prior project documentation are not measurements produced by this review. See the project [[metric definitions](../METRICS.md)], [[execution-status record](../results/initial-baselines-status.json)], and [[benchmark fixture](../fixtures/memory-benchmark-v1.json)].

## Sources

- [Current canonical repository](https://github.com/TAIPANBOX/engram)
- [Reviewed main branch head](https://github.com/TAIPANBOX/engram/commit/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e)
- [README](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/README.md)
- [Data flow and database architecture](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/DATA_FLOW.md)
- [API reference](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/docs/api-reference.md)
- [Core API](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/core.py)
- [SQLite store](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/store.py)
- [Retrieval](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/retrieval.py)
- [Reflection](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/reflection.py)
- [Graph retrieval](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/graph.py)
- [SQLite schema](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/schema.py)
- [Agent Passport events](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/events.py)
- [MCP server](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/engram/mcp_server.py)
- [Security policy](https://github.com/TAIPANBOX/engram/blob/08ee3bf5a9e50cf067f50221a8ac77c9adfa539e/SECURITY.md)
- [Official project website](https://it-rat.com/services/engram.html)
- [Curated roster entry](../data/memory-systems.json)
- [Project metrics](../METRICS.md)
- [Benchmark execution status](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)

**Verification boundary:** no Engram runtime, tests, or benchmarks were run.
