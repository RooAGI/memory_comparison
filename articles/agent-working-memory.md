# AgentWorkingMemory

## Identity and review pin

- **Curated ordinal:** 32 in `data/memory-systems.json`
- **Listed name / slug:** AgentWorkingMemory / `agent-working-memory`
- **Listed repository locator:** https://github.com/CompleteIdeas/agent-working-memory
- **Canonical repository:** https://github.com/CompleteIdeas/agent-working-memory
- **Default branch:** `master`
- **Reviewed head:** [`e1c8705849f7f72ee8106c440d796337d17d1518`](https://github.com/CompleteIdeas/agent-working-memory/commit/e1c8705849f7f72ee8106c440d796337d17d1518)
- **Reviewed at:** 2026-11-24 19:26:22 UTC (11:26:22 PST, America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The roster’s Atlas source is [its pinned AgentWorkingMemory entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/agent-working-memory.md). It supplies the ordinal, name, listed repository locator, and attribution only. Atlas descriptions, marks, and layout are not assessment evidence.

## Summary

AgentWorkingMemory (AWM) is a local-first memory application for AI agents. It writes selectively to an engram store, retrieves through a multi-stage lexical, vector, graph, and reranking pipeline, and can supersede or retract memories. This is a source review at one verified commit; it does not measure behavior or performance.

## Who and what

The official [repository README](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/README.md) describes AWM as a local agent-memory system distributed as a Node.js package, with MCP, HTTP, CLI, and Claude Code integrations. The [architecture guide](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/docs/architecture.md) describes its engine and storage layers. The repository identifies Complete Ideas and Robert Winter in source copyright notices; this review makes no claim about an individual’s maintainer role.

## Architecture and data model

The [architecture guide](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/docs/architecture.md) describes MCP and HTTP entry points over shared cognitive engines and SQLite/FTS5 storage. The MCP entry point registers memory, checkpoint, task, feedback, retraction, and compression tools in-process; a hook sidecar supports checkpoints and scheduled consolidation. The guide says the MCP and HTTP entry points are not designed to run simultaneously against one database.

An engram is the stored memory unit. The documented schema includes an ID and agent ID, concept, content, tags, type/class, salience, confidence, access state, embedding, and lifecycle stage. It also includes optional task fields, validity dates, question text, slots, and provenance-related fields such as origin class and writer session. Associations link engrams with Hebbian, causal, temporal, and other edge types; episodes group related memories. SQLite is the default backend, with PGlite and Postgres alternatives described in the guide.

See the pinned [architecture documentation](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/docs/architecture.md), [MCP interface](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/mcp.ts), and [SQLite store](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/storage/sqlite.ts).

## Write, update, delete, and retrieval

- **Write:** `memory_write` routes through the shared [write pipeline](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/core/write-pipeline.ts). It redacts configured sensitive patterns, evaluates salience and novelty, then creates, reinforces an exact-concept match, or supersedes a prior memory under correction/supersession rules. New low-salience writes can be discarded or staged; session-scoped notes have separate gates. Embedding and connection work can happen asynchronously. These are implementation observations, not evidence that a memory is correct or will later be found.
- **Update/correction:** `memory_supersede` creates a replacement engram and marks the earlier item superseded; retrieval down-ranks superseded items. `memory_retract` marks a memory retracted, can create a correction engram and invalidation edge, and reduces confidence in a bounded set of connected memories. The [retraction engine](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/engine/retraction.ts) describes this as soft invalidation. The inspected MCP surface documents no general hard-delete tool, so permanent erasure behavior is not established here.
- **Retrieval:** The [activation engine](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/engine/activation.ts) embeds the query, retrieves lexical and vector candidates, computes text, confidence, decay and association signals, traverses graph links, reranks a bounded pool with a local cross-encoder, applies validity/supersession and agreement rules, then returns a limited result. Some abstention behavior is opt-in. The database FTS index and slim cache support candidate selection.
- **Maintenance:** The architecture guide describes a consolidation cycle that strengthens or decays associations, synthesizes patterns, fades content, archives or prunes memories, and sweeps staging. These background operations are distinct from an explicit caller update.

## Scope isolation

Engrams and association queries carry an `agent_id`; the MCP server chooses an agent identity from configuration or derives one from the project directory. This provides per-agent pools in the reviewed path. Session-scoped reads are separately tagged. Shared backends and team coordination are also documented, so the presence of an agent key alone does not prove a deployment’s authorization boundary or isolation under every API path. Those properties were not runtime-tested.

## Provenance and evidence

The schema has fields including `origin_class`, `writer_session`, and `recipe_id`, plus references and source-related tags on some flows. The [write pipeline](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/core/write-pipeline.ts) accepts caller-supplied memory content and metadata, and applies configured redaction before storage. These fields preserve some origin context; the inspection did not find a required, validated evidence chain tying every recalled claim to an authoritative source. Citation correctness and provenance completeness are therefore unknown.

## Source-visible efficiency and observability

The retrieval code runs lexical and vector retrieval in parallel, keeps a bounded rerank pool (at least 32 candidates at default limit), and uses local ONNX embedding and reranking models. SQLite uses FTS5, WAL, a configurable page cache and mmap; the store also has a slim in-memory cache. Cross-encoder reranking and model loading are visible cost centers. The [SQLite store](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/storage/sqlite.ts) and [activation engine](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/engine/activation.ts) expose these implementation choices, not independently measured results.

The documented schema includes activation events with context, result count, top score, and latency, retrieval feedback, and staging decisions; the MCP entry point also initializes structured logging and a loop-lag monitor. These are source-visible observability hooks. No metric values were collected for this review.

## Metric-domain evidence

Every domain below is **unmeasured in this task**. The source mechanisms do not establish retrieval quality, correctness, or costs. Project metric definitions live in [METRICS.md](../METRICS.md); the [baseline status record](../results/initial-baselines-status.json) and [planned fixture](../fixtures/memory-benchmark-v1.json) are not results for AWM.

| Domain | Source observation | Measurement status |
|---|---|---|
| Answerable recall and abstention | Multi-stage candidate retrieval and agreement/optional calibrated gates are present. | Unmeasured |
| Correction accuracy and stale values | Supersession, validity windows, and retraction paths exist. | Unmeasured |
| Deletion leakage | Retraction is a soft invalidation path; hard-delete coverage was not established. | Unmeasured |
| Scope isolation | Agent and session identifiers are used in memory flows. | Unmeasured |
| Evidence support and citation coverage | Origin/reference fields exist, without a verified required evidence chain. | Unmeasured |
| Latency and write-to-recall delay | Parallel candidate legs, model scoring, and event latency fields are visible in source. | Unmeasured |
| Tokens, cost, and storage | Local models, SQLite settings, and token/context helpers are present; workload costs were not collected. | Unmeasured |

## Limits and unknowns

This is a bounded inspection of selected current documentation and code at one verified repository head. It did not establish runtime correctness, retrieval quality, deletion completeness, authorization, production reliability, or measured resource use. The README and docs contain their own benchmark claims, but none are treated here as measurements from this review.

The reviewed system has several storage backends and many configurable paths. Backend parity, all route-level scope checks, lifecycle edge cases, and the practical impact of maintenance jobs were not exhaustively audited. No published contact email appeared in the checked official repository README; the JSON record stores `contact.email: null` and that exact checked source URL.

## Benchmark status

**Benchmark not run.** No AWM runtime, benchmark, or tests were run for this task. Source observations above are not benchmark results. The [structured review](../data/system-reviews/agent-working-memory.json) records the source contract; the [project metric definitions](../METRICS.md), [execution-status record](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json) are separate.

## Sources

- [Canonical upstream repository](https://github.com/CompleteIdeas/agent-working-memory)
- [Reviewed head commit](https://github.com/CompleteIdeas/agent-working-memory/commit/e1c8705849f7f72ee8106c440d796337d17d1518)
- [Official README at reviewed revision](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/README.md)
- [Architecture guide at reviewed revision](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/docs/architecture.md)
- [MCP interface](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/mcp.ts)
- [Shared write pipeline](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/core/write-pipeline.ts)
- [Activation engine](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/engine/activation.ts)
- [Retraction engine](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/engine/retraction.ts)
- [SQLite store](https://github.com/CompleteIdeas/agent-working-memory/blob/e1c8705849f7f72ee8106c440d796337d17d1518/src/storage/sqlite.ts)
- [Project metric definitions](../METRICS.md)
- [Benchmark execution-status record](../results/initial-baselines-status.json)
- [Planned benchmark fixture](../fixtures/memory-benchmark-v1.json)
