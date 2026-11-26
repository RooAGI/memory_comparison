# Friday source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 247 / Friday / `friday`  
**Listed repository locator:** [friday-memory/friday](https://github.com/friday-memory/friday)  
**Canonical upstream:** [friday-memory/friday](https://github.com/friday-memory/friday)  
**Default branch / reviewed head:** main / [fad2a61c38eb77058e4ecb71a558fd579e671dce](https://github.com/friday-memory/friday/commit/fad2a61c38eb77058e4ecb71a558fd579e671dce)  
**Review time:** 2026-11-25 20:43:27 UTC (2026-11-25 12:43:27 PST; America/Los_Angeles).

## Identity and review pin

The catalog places Friday at ordinal 247, slug `friday`, with the explicit locator `https://github.com/friday-memory/friday`. Its pinned Agent Memory Atlas entry is retained as roster attribution only; Atlas descriptions and assessments are not evidence in this review. The official Git remote reported `refs/heads/main` at the full SHA above, and a shallow checkout of that branch resolved to the same SHA. GitHub REST API requests returned HTTP 403; branch and checkout verification therefore rely on official Git transport and the checked-out upstream source. The timestamp records when the review pin was checked.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Friday is a Python memory service for coding agents with MCP and HTTP interfaces. The primary Compose gateway combines a JSON facts ledger, Mem0-backed episodic memory/search, Neo4j graph extraction, and background decay/consolidation. The repository also contains an opt-in serverless gateway using project-keyed SQLite/libSQL records and FTS5. The code review describes those paths separately; it does not establish runtime quality, deployment safety, or performance.[[readme]][[gateway]][[serverless]][[storage]]

## Who and what

The repository describes Friday as an open-source, self-hosted persistent memory layer. This is a service and SDK/MCP integration rather than a standalone embedding or database library. The official security policy publishes `itskie7910@gmail.com` for vulnerability reports; this is recorded as the project contact source, not inferred maintainer identity.[[readme]][[security]]

## Architecture and data model

In the Compose gateway, `POST /add` sends episodic text to Mem0 using the fixed user ID `friday_user` and metadata for `source` and `project`. When a DeepSeek key is configured, a FastAPI background task extracts up to ten named entities and fifteen relations from a truncated text input and upserts them into Neo4j. Facts are stored separately in a JSON file with content-derived IDs, project, lifecycle status, energy, supersession and timestamps. Cognitive state and dream-cycle outputs form additional state/consolidation paths.[[gateway]][[autograph]][[readme]]

The README presents four layers and names ChromaDB, but the inspected Compose search code calls the Mem0 client API and contains no direct Chroma client in that route. Treat ChromaDB as README-described architecture, not a verified independent runtime store in this review. The serverless candidate is a separate design: a normalized record envelope `(kind, project, id, data)` in SQLite/libSQL, covering facts, memories, entities, edges, blueprints and state; FTS5 indexes memory content, source and project. SQLite writes use transactions, while its schema and operations differ from the Compose JSON/Mem0/Neo4j path.[[readme]][[gateway]][[records]][[storage]][[serverless]]

## Write, update, delete, and retrieval

**Writes and updates.** Compose `add_memory` stores source/project metadata with Mem0 and queues best-effort graph extraction when configured; a Mem0 error is included in the response rather than necessarily failing the whole request. `add_fact` deduplicates exact active content within a project and can supersede an explicit fact ID or same-key facts when text uses a colon/equal prefix. Serverless `/add` writes transactionally to SQLite/libSQL and deduplicates exact content within a project. Its `/update` changes content/source; `/supersede` links an old memory to a replacement.[[gateway]][[mcp]][[serverless]][[storage]]

**Delete and correction.** Compose memory delete/update call Mem0 after checking a retrievable record's project when supported. If that ownership lookup raises an ordinary exception, the helper logs a warning and continues, so the source does not establish fail-closed ownership checks under lookup failure. Fact revoke marks a fact superseded/revoked; the facts endpoint also supports hard removal. The serverless store supports transactional memory delete, update, and supersession, plus fact revoke or hard delete. These endpoints and storage variants should not be assumed to share identical lifecycle or audit behavior.[[gateway]][[facts]][[serverless]][[storage]]

**Retrieval.** Compose `/search` calls Mem0 with a fixed user and a project metadata filter, then applies a defensive filter while permitting legacy unscoped records. `/facts` returns active facts and can include global facts with a project read. MCP `get_context` composes facts and recent memories. Serverless search tokenizes query words into an FTS5 OR query, filters by project and excludes superseded memories; its context route returns active facts plus up to 50 newest memories. The README also advertises graph blast-radius retrieval, but the inspected query has no effective project predicate and contains a suspicious empty `toLower()` expression; correctness was not executed or claimed here.[[gateway]][[mcp]][[facts]][[storage]][[serverless]]

## Scope isolation

Project labels are passed through memory and fact APIs. Compose search applies project metadata filtering, while the defensive post-filter permits legacy unscoped memories. Its facts read route accepts an optional project and includes `global` facts. The memory mutation ownership helper allows legacy/unlabelled records for compatibility and continues if Mem0 retrieval is unavailable or errors; the graph extraction source includes project on project nodes, but entity identity is name-based and the graph search route shown does not filter by project. These are source-level boundaries and gaps, not a tested cross-tenant exploit claim.[[gateway]][[facts]][[autograph]]

The opt-in serverless gateway requires a nonempty project on routes and its storage queries include that project key, including FTS retrieval. This stronger code-level partition is specific to that backend. The Compose gateway has a shared default API secret and permissive CORS configuration in source; actual exposure depends on deployment settings and was not tested.[[serverless]][[storage]][[gateway]][[security]]

## Provenance and evidence

Memory records can carry a caller-provided source label such as agent, user, system, blueprint, or dream-cycle; the serverless records preserve source data, IDs, and timestamps. Facts record content, project, timestamps, lifecycle and energy fields, but the inspected fact write path does not attach external supporting citations or verify truth. Graph relations are generated from an LLM extraction prompt and stored as edges without source-memory identifiers in the inspected upsert path. These fields support origin/context tracking but do not independently establish claim accuracy or answer citation coverage.[[gateway]][[autograph]][[records]][[facts]][[serverless]]

## Efficiency and observability

Compose health reports availability for Neo4j, Mem0 configuration, and fact count; the gateway uses Python logging and records health timestamps. Background graph extraction is non-blocking and catches failures as warnings. The serverless variant uses SQLite transactions and a project-scoped FTS5 index; its health endpoint reports storage availability. The README publishes latency/token figures and a DeepEval table, but this review did not verify a versioned adjudicated result record or reproduce those claims. No latency, write-to-recall delay, token, cost, or storage measurements were collected.[[gateway]][[autograph]][[serverless]][[storage]][[readme]][[metrics]][[fixture]][[status]]

## Metric-domain evidence

All benchmark domains are **unmeasured** for Friday in this review. Code observations below describe mechanisms only. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) define the project evaluation protocol and shared status; they are not Friday measurements.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Mem0 semantic search and FTS5 keyword search paths exist; no answer scoring or abstention evaluation was run. | Unmeasured |
| Correction and stale values | Fact supersession/revocation and serverless memory supersession exist; no correction sequence was assessed. | Unmeasured |
| Deletion leakage | Compose Mem0 delete and JSON fact hard-delete/revoke paths exist; no post-delete probe or replica audit was run. | Unmeasured |
| Scope isolation | Project filters exist, with legacy unscoped allowance and unfiltered graph paths in Compose; no isolation workload was run. | Unmeasured |
| Evidence support and citation coverage | Source labels/timestamps and generated graph edges exist; no generated answer evidence was adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | README advertises figures; no runtime timing was collected or independently reproduced. | Unmeasured |
| Tokens, cost, and storage | No workload token, cloud charge, or persisted-storage measurements were collected. | Unmeasured |

## Limits and unknowns

This is a selected inspection of the pinned README, security policy, Compose gateway, MCP tools, graph extraction, fact lifecycle, serverless routes, and SQLite schema/store. It did not run Friday, tests, or benchmarks. It does not establish actual Mem0/Chroma backend topology, behavior under dependency outages, the quality of generated entity relationships, graph query correctness, deployment authentication, concurrency behavior in Compose's JSON facts file, or deletion from backups and external replicas.[[readme]][[gateway]][[autograph]][[facts]][[serverless]][[storage]]

The repository's README claims and benchmark table are documentation observations only. The project review did not reproduce its scenarios or verify adjudication artifacts. Source presence cannot establish useful agent selection, accurate answers, calibrated abstention, or the privacy guarantees of a deployed instance.[[readme]][[metrics]][[status]]

## Benchmark status

**Benchmark not run.** Friday, its tests, and benchmark workload were not executed. No recall, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. Consult the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) for project-owned protocol and status material, not Friday results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned [SECURITY.md](https://github.com/friday-memory/friday/blob/fad2a61c38eb77058e4ecb71a558fd579e671dce/SECURITY.md) publishes `itskie7910@gmail.com` as the vulnerability-report contact. No commit/profile metadata, third-party directory, or inferred address was used.[[security]]

## Sources

Repository source links are pinned to the verified full SHA. The repository page and head patch are official upstream identity/pin evidence; the Atlas link is included only for curated roster attribution. See the structured record [friday.json](../data/system-reviews/friday.json) and [curated roster](../data/memory-systems.json).
