# Agentic GraphRAG source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 18 / Agentic GraphRAG / agentic-graphrag  
**Listed repository locator:** [ontogr/agentic-graphrag](https://github.com/ontogr/agentic-graphrag)  
**Current canonical repository:** [ontogr/agentic-graphrag](https://github.com/ontogr/agentic-graphrag)  
**Default branch / reviewed head:** main / ab33b3a6dd85aaf579d8ae90a15b64e072980fdd  
**Review time:** 2026-11-24 18:45:37 UTC (10:45:37 PST; America/Los_Angeles).

## Identity and scope

The curated roster lists Agentic GraphRAG at ordinal 18, gives the repository locator above, and attributes the entry to the Agent Memory Atlas catalog source revision `19199a4fc249e89c0793be06f0b166b358089ba0`. The roster was used for identity and attribution only; Atlas descriptions, marks, and layout were not assessment evidence. The official repository page identifies `main` as the default branch. Its latest commit patch identifies the full reviewed head as `ab33b3a6dd85aaf579d8ae90a15b64e072980fdd`.[[curated roster](../data/memory-systems.json)] [[GitHub repository](https://github.com/ontogr/agentic-graphrag)] [[reviewed main head patch](https://github.com/ontogr/agentic-graphrag/commit/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd.patch)]

Agentic GraphRAG is a Python framework for building a graph that connects ingested enterprise documents with task histories and agent decisions. The README describes the same evidence and history tools for Python callers, a built-in agent, and an MCP server, with Neo4j or FalkorDB graph stores and optional external vector stores. Product documentation is treated as documentation; code observations below are tied to the reviewed revision.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)]

## Architecture and data model

**Documentation observation.** Ingestion preserves document structure: documents contain nested sections, chunks, tables, and figures, with hierarchy and neighboring-chunk links. A configured schema/ontology drives typed entity and relation extraction, graph labels and relationships, indexing, and retrieval. Low-confidence or out-of-schema extraction candidates retain links to source passages and stay out of search pending review.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)]

**Documentation and code observation.** The graph also stores task records with ordered events and named steps, and decisions with conclusions, rationale, assumptions, open questions, and typed supports to document passages, task events, or earlier decisions. The inspected `DecisionTraces` implementation binds those operations to a configured project and author. Document support records version-specific evidence; decision reviews and supersession preserve earlier history.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)] [[agrag/decisions.py](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/agrag/decisions.py)]

## Write, update, delete, and retrieval

**Write.** The README documents `Graph.add` as the document-ingestion entry point. Its pipeline loads source formats, retains structure while chunking, extracts schema-constrained entities and relations, resolves entity matches, and writes graph and vector data. The hybrid extraction mode uses local GLiNER output and sends only less-certain chunks for LLM review, subject to a configured budget. These are documented design paths, not measurements.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)]

**Update, deletion, and correction.** The README says a new document version preserves older evidence text and flags decisions that depend on changed or removed sources for review; reviewers can reaffirm, replace, or reject decisions, retaining prior versions. The latest reviewed code additionally records text-bearing sources that a decision consulted without citing, and flags a decision if such a source changes. Reaffirmation clears the read-only consulted references. This inspection does not establish physical erasure across every store, backup, embedding, trace, or downstream export.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)] [[agrag/decisions.py](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/agrag/decisions.py)] [[reviewed head patch](https://github.com/ontogr/agentic-graphrag/commit/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd.patch)]

**Retrieval.** The documented interfaces include lexical, semantic, and hybrid passage search, optional reranking, schema-bounded entity and relationship search, theme search over community reports, and navigation around a matched passage. Fetch returns exact stored text with status and document version; only fetched passages can be cited. The README describes explicit incomplete/failed search statuses, distinguishing a genuinely empty result from a partial result. These interfaces do not establish answerable recall, calibrated abstention, or citation correctness under a workload.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)]

## Scope isolation and provenance

**Scope isolation.** Evidence search and fetch are restricted to a configured document scope; an evidence identifier outside scope is described as unavailable. The README says the local MCP server starts read-only and exposes only configured documents, with writes enabled only by changing settings. Decision history is project-scoped. Document scope and project identity are configuration boundaries; this source review does not establish tenant authentication or isolation for every deployment path, and the documented project-scoped decision search is distinct from document-scoped evidence reads.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)] [[agrag/decisions.py](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/agrag/decisions.py)]

**Provenance and evidence.** Passage records retain source location and version identity. An evidence ID continues to resolve to the text originally cited after an edit, marked as superseded; citation checking rejects unread, malformed, or out-of-scope IDs. Decisions retain typed supports, and changes to supporting sources can trigger review. These mechanisms record traceability and review state; they do not by themselves prove that a cited passage entails a generated claim.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)] [[agrag/decisions.py](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/agrag/decisions.py)]

## Source-visible efficiency and observability

**Source and documentation observations.** The documented resolution pipeline uses exact, name, fuzzy, embedding, cluster, and LLM checks in order, sending only unresolved pairs to the LLM. Local GLiNER extraction is available, with LLM review limited by a configured budget. OpenTelemetry instrumentation is opt-in: when a tracer is supplied, documented spans cover loading, chunking, extraction, resolution, storage, search, and model calls, including attempts, token counts, and failure trace/span IDs. Traces may contain full prompts, questions, or evidence, so destination and retention settings matter. None of these source-visible design choices is a benchmark result.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)]

## Project metric domains

All benchmark domains are **unmeasured** for Agentic GraphRAG. The reviewed sources expose evidence retrieval and citation checks, version updates and review, configured scope, graph/vector storage, and optional trace instrumentation. No workload was run to measure answerable recall or abstention, correction or stale-value accuracy, deletion leakage, cross-scope leakage, evidence support or citation coverage, latency, write-to-recall delay, tokens, cost, or storage efficiency. Project metrics, fixture, and status record define the separate protocol; they are not system results.[[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded review of the official README, the decision-trace implementation, and the latest commit patch at the verified SHA. The system, its tests, and benchmarks were not run. The selected sources do not establish physical deletion completeness across all persistence and observability backends, deployed tenant authorization, answer quality, or runtime cost and performance. Unknown here means not established by this inspection, not that a feature is absent.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)] [[agrag/decisions.py](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/agrag/decisions.py)] [[reviewed head patch](https://github.com/ontogr/agentic-graphrag/commit/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd.patch)]

## Contact-list follow-up

The official README and repository security policy were checked for a published contact email. Neither publishes an address. The security policy directs reporters to GitHub Security Advisories or maintainer profiles; I did not consult personal profiles or infer an email. The JSON record stores `contact_email: null` and the exact checked security-policy URL.[[README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)] [[SECURITY.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/SECURITY.md)]

## Benchmark status

**Benchmark not run.** No system execution, test suite, or benchmark workload was run. Source and documentation observations are not measured results. See the project metric definitions, benchmark status record, and fixture for the separate measurement protocol.[[project metric definitions](../METRICS.md)] [[benchmark status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical GitHub repository](https://github.com/ontogr/agentic-graphrag)
- [Reviewed full main head patch](https://github.com/ontogr/agentic-graphrag/commit/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd.patch)
- [README.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/README.md)
- [agrag/decisions.py](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/agrag/decisions.py)
- [SECURITY.md](https://github.com/ontogr/agentic-graphrag/blob/ab33b3a6dd85aaf579d8ae90a15b64e072980fdd/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status record](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and source attribution](../data/memory-systems.json)

**Verification boundary:** no Agentic GraphRAG system, tests, or benchmarks were run.
