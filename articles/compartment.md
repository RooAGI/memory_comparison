# Compartment — source review

## Identity and review pin

- **Roster ordinal / name / slug:** 141 / Compartment / `compartment`
- **Listed repository locator:** https://github.com/MaxFreedomPollard/Compartment
- **Roster attribution:** `repository_status: explicit`; Atlas locator retained for identity only. [Curated roster](../data/memory-systems.json) · [Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/compartment.md)
- **Canonical upstream / default branch:** [MaxFreedomPollard/Compartment](https://github.com/MaxFreedomPollard/Compartment) / `main`
- **Reviewed head:** [98d4917181c04e5efa41e82ba455b25084edc99f](https://github.com/MaxFreedomPollard/Compartment/commit/98d4917181c04e5efa41e82ba455b25084edc99f)
- **Official main feed:** [main commit feed](https://github.com/MaxFreedomPollard/Compartment/commits/main.atom) reports this head at 2026-11-18 10:10:42 UTC.
- **Reviewed:** 2026-11-25 08:46:19 UTC (2026-11-25 00:46:19 PST; America/Los_Angeles)
- **Status:** Reviewed from code; benchmark not run

## Summary

Compartment is an offline, local memory vault for AI agents, exposed through an MCP server and CLI. It stores encrypted records and vectors in a sealed vault, with namespace permissions, hybrid retrieval, provenance, and an audit trail. This assessment is based on official documentation and source at the pinned upstream revision; no runtime or benchmark was run. [README](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/README.md) · [memory design](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/docs/MEMORY.md)

## Who and what

The official project describes a local vault that can be used by multiple agent clients through MCP, command-line tools, and desktop integrations. The server uses stdio transport. The repository's official support page lists **maxpollard790@gmail.com**. [README](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/README.md) · [MCP server](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/server.py) · [support page](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/support.md)

## Architecture and data model

The `Vault` coordinates the store, index, embedding, ACL, encryption, and audit code. Unlock decrypts the sealed payload into RAM, replays its journal, and rebuilds the vector index. The SQLite image is serialized inside the sealed `.vault` file; record text and vectors are encrypted at rest. [vault source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/vault.py) · [store source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/store.py)

A record includes encrypted text, a per-record key wrapped by the vault key, an embedding, namespace, tags, importance, quarantine flag, caller provenance, timestamps, source, discovery date, optional expiry, and pack metadata. Related tables store vector windows, FTS rows, explicit relations, audit records, and vault metadata. Relations can point to the memory they came from and carry validity windows. [store source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/store.py) · [memory guide](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/docs/MEMORY.md)

The bundled local ONNX embedder produces 384-dimensional vectors. The guide describes exact SIMD search below 20,000 records and HNSW above that threshold, alongside SQLite FTS5. Its model hash is recorded and checked when opening the vault. Those are implementation/documentation claims; this review did not measure their performance. [memory guide](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/docs/MEMORY.md) · [ranking source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/ranking.py)

## Write, update, delete, and retrieval

**Write.** Authored stores enforce one claim with a default 200-character limit. Capture and import routes preserve their input and skip that gate. The vault embeds, deduplicates, encrypts, journals, and audits new records. A required `source` and separate `discovered` date preserve how and when a fact became known. [README](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/README.md) · [memory guide](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/docs/MEMORY.md) · [vault source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/vault.py) · [store source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/store.py)

**Update and correction.** Records can be superseded by ID; the old item is excluded from retrieval but remains readable by ID with a replacement pointer. Similar opinions trigger an explicit decision to reaffirm, replace, or keep both. These mechanisms describe lifecycle behavior, not correction accuracy. [memory guide](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/docs/MEMORY.md) · [vault source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/vault.py)

**Delete and forgetting.** The CLI and MCP expose forgetting, including a shred option. Shredding destroys the wrapped record key; the store also removes full-text rows and vacuums freed pages. No delete or residual-data check was performed. [README](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/README.md) · [store source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/store.py)

**Retrieval.** Search combines semantic vector evidence, keyword matching, and optional graph expansion. Importance and memory-count recency priors are applied to matching evidence; namespace, tag, date, and starter-fact filters constrain results. The project describes a relative relevance threshold and an explicit `top_k` option. These source-visible paths do not measure answer quality. [memory guide](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/docs/MEMORY.md) · [ranking source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/ranking.py) · [README](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/README.md)

## Scope isolation

Namespace grants are configured per caller with `rw`, `ro`, or `none`; `packs/*` is read-only. The server accepts its caller name through `--caller`, and its source recommends a separate server instance and ACL configuration per host when real isolation is required. The caller label is declarative; this review did not verify host authentication or test cross-caller isolation. [ACL source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/acl.py) · [server source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/server.py)

## Provenance and evidence

Records include host, agent, and session provenance, source, and discovery date. Quarantined content is accompanied by an untrusted-data warning; recalled memories are marked as data rather than instructions. Audit rows carry caller, operation, detail, timestamp, and a chained hash; an anchor records the chain head and length to detect truncation. This supports traceability and tamper detection but does not guarantee generated answers cite or entail the underlying memory. [store source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/store.py) · [vault source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/vault.py) · [audit source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/audit.py) · [memory guide](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/docs/MEMORY.md)

## Efficiency and observability

The README and memory guide report figures such as roughly 12 ms hybrid recall and about 40 ms per store. These are upstream-reported measurements under stated project conditions, not measurements from this review. The project describes an offline design with local status, recent-memory, dashboard, and audit/verify views; this assessment collected no latency, cost, token, or storage data. [README](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/README.md) · [memory guide](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/docs/MEMORY.md) · [audit source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/audit.py)

## Metric-domain evidence

All benchmark domains remain **unmeasured** in this review: answerable recall and abstention; correction accuracy and staleness; deletion leakage; scope isolation; evidence support and citation coverage; latency; write-to-recall delay; tokens; cost; storage; and observability. Project definitions and fixtures describe the protocol, not system outcomes. [metric definitions](../METRICS.md) · [benchmark status](../results/initial-baselines-status.json) · [benchmark fixture](../fixtures/memory-benchmark-v1.json)

## Limits and unknowns

The review covered the main memory guide and selected current source modules, not every CLI/client path, cryptographic implementation, migration, pack operation, recovery case, or configuration. It cannot establish practical answer quality, abstention, correction correctness, complete erasure, deployment-specific isolation, or resource use. The authoring gate uses heuristic rules, approximate HNSW search is used above the exact-search threshold, and the MCP caller identifier is not independently authenticated by the server. [memory guide](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/docs/MEMORY.md) · [server source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/server.py) · [ACL source](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/src/compartment/acl.py)

## Benchmark status

**Not run.** No Compartment system, benchmark, or test was run. The project's metric definitions, initial-baseline status, and fixture are protocol material only. [metric definitions](../METRICS.md) · [benchmark status](../results/initial-baselines-status.json) · [benchmark fixture](../fixtures/memory-benchmark-v1.json)

## Contact

The official support page publishes **maxpollard790@gmail.com**. [Pinned official support page](https://github.com/MaxFreedomPollard/Compartment/blob/98d4917181c04e5efa41e82ba455b25084edc99f/support.md)
