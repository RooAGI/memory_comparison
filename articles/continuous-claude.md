# Continuous Claude — source review

## Identity and review pin

- **Roster ordinal / name / slug:** 152 / Continuous Claude / `continuous-claude`
- **Listed repository locator:** https://github.com/parcadei/Continuous-Claude-v3
- **Roster attribution:** `repository_status: explicit`; Atlas is retained for identity/locator attribution only. [Curated roster](../data/memory-systems.json) · [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/continuous-claude.md)
- **Canonical upstream / default branch:** [parcadei/Continuous-Claude-v3](https://github.com/parcadei/Continuous-Claude-v3) / `main`
- **Reviewed head:** [d07ff4b06b62f43771bc0c927d0211b734d6149e](https://github.com/parcadei/Continuous-Claude-v3/commit/d07ff4b06b62f43771bc0c927d0211b734d6149e)
- **Verification:** GitHub’s official repository page identifies `main` as the default branch and shows the head; its official main commits Atom feed reports the same full SHA.
- **Reviewed:** 2026-11-25 09:12:48 UTC (2026-11-25 01:12:48 PST; America/Los_Angeles)
- **Status:** Reviewed from current pinned upstream source and documentation. Benchmark not run.

## Summary

Continuous Claude is a Claude Code environment combining session continuity, hook-driven context injection, agent workflows, code analysis, and a cross-session learning store. Its README describes PostgreSQL with pgvector for learning records and a background daemon that extracts learnings from session reasoning, then surfaces matches through a prompt hook.[README](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/README.md) The code also includes a SQLite/PostgreSQL backend factory, but at this reviewed head the factory’s default SQLite service import points to a file that is absent from the repository; the default write path therefore appears unavailable unless PostgreSQL is selected.[factory](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/db/memory_factory.py) · [SQLite implementation path checked](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/db/memory_service.py)

## Architecture and data model

The project is broader than a memory database: Claude Code hooks load continuity ledgers and handoffs, monitor work, and trigger context recall; skills and agents coordinate tasks; TLDR provides layered code analysis. The README describes memory as a PostgreSQL + pgvector subsystem with a session table, file-claim coordination, archival learnings, and handoffs.[README](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/README.md)

The PostgreSQL schema stores archival records with UUID, session ID, optional agent ID, content, JSONB metadata, a 1024-dimensional embedding, and creation time. It indexes session and agent scope, creation time, and full-text content. Handoffs are a separate record type with session/span/transcript references, outcome fields, content, and embeddings.[schema](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/docker/init-schema.sql) The learning writer supports seven typed categories and optional context, tags, and confidence metadata; it embeds content and skips a record when its nearest vector result meets a fixed 0.85 similarity threshold.[store](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/store_learning.py)

## Write, update, delete, and retrieval

**Write.** The README describes a daemon polling stale sessions, starting headless Claude to extract learning from thinking blocks, and persisting the results for later recall.[README](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/README.md) The daemon source documents a 60-second poll, a five-minute stale threshold, and a concurrency cap of two extractions; it logs to a local file.[daemon](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/memory_daemon.py) There is also an explicit learning-store command.[store](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/store_learning.py)

**Backend availability.** The factory defaults to SQLite unless an environment variable selects PostgreSQL, and imports `memory_service.py` for SQLite. That file is absent at the reviewed head (GitHub returned 404 for the pinned path), while the factory and PostgreSQL service are present. Thus source inspection indicates that a fresh configuration using the documented default backend cannot create its memory service; PostgreSQL is the available implementation inspected here.[factory](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/db/memory_factory.py) · [SQLite path check](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/db/memory_service.py) · [PostgreSQL service](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/db/memory_service_pg.py)

**Update and deletion.** The inspected writer performs similarity-based deduplication, not an explicit correction or supersession protocol. The learning recall command exposes search; the reviewed writer and recall paths do not show a user-facing forget operation or a deletion audit. Core memory has a set operation that replaces a key’s prior value, but that is distinct from archival learning correction.[store](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/store_learning.py) · [recall](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/recall_learnings.py) · [PostgreSQL service](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/db/memory_service_pg.py)

**Retrieval.** The README describes automatic prompt-time memory matches and a hybrid text/vector search command. The standalone recall script’s PostgreSQL text query filters to session-learning records but, in the inspected query, does not constrain results by session or project. Retrieval can therefore cross those boundaries; the schema’s session key alone does not isolate this query.[README](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/README.md) · [recall](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/recall_learnings.py) · [schema](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/docker/init-schema.sql)

## Scope isolation

Archival rows carry session and optional agent IDs, and the PostgreSQL service uses those fields for core-memory operations and recent-context selection. However, the inspected explicit recall query is global across all session-learning rows, with no project/session predicate. The repository also describes handoffs and project context separately. This is not evidence of tenant isolation, and the cross-project recall path needs deployment-specific care.[schema](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/docker/init-schema.sql) · [PostgreSQL service](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/db/memory_service_pg.py) · [recall](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/recall_learnings.py)

## Provenance and evidence

Learning rows preserve a session identifier and metadata; the schema does not define a dedicated source-transcript pointer or evidence span for each learning. Handoff records do have optional JSONL path and span identifiers, but they are a separate table. Confidence and category metadata can describe a learning, but the inspected recall path does not use confidence to withhold results. These fields therefore provide trace context, not verified support for a recalled claim.[store](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/store_learning.py) · [schema](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/docker/init-schema.sql) · [recall](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/recall_learnings.py)

## Efficiency and observability

Background extraction avoids placing all mining work in the active prompt path, while the README describes hybrid search and automatic context injection. The daemon uses periodic polling and caps simultaneous extraction processes; its code writes a local log. The repository advertises token reduction for its separate TLDR code-analysis subsystem, not a measured memory benchmark. No latency, indexing delay, token, cost, storage, or daemon reliability measurements were collected in this review.[README](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/README.md) · [daemon](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/opc/scripts/core/memory_daemon.py)

## Limitations and unknowns

This is a source review, not a runtime audit. The missing SQLite implementation makes the default backend path a concrete source-level concern; the PostgreSQL path still depends on external setup and services. The inspected recall query lacks session/project filtering, and the reviewed entry points do not establish archival correction, forgetting, or source-level evidence validation. I did not inspect every hook, service configuration, database migration, or deployment topology. Effective data isolation, successful daemon extraction, and practical search quality remain unknown.

## Contact

The official pinned [README](https://github.com/parcadei/Continuous-Claude-v3/blob/d07ff4b06b62f43771bc0c927d0211b734d6149e/README.md) was checked for a published contact email; none was found. No email was inferred from commit or profile metadata.

## Benchmark status

**Not run.** No Continuous Claude runtime, benchmark, or test was run for this review. See [project metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and the [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured evidence IDs and pinned URLs are recorded in [continuous-claude.json](../data/system-reviews/continuous-claude.json). The [Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/continuous-claude.md) supports identity and listed-locator attribution only.
