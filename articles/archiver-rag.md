# Archiver RAG

## Identity and review pin

- **System:** Archiver RAG
- **Curated position:** 65
- **Slug:** `archiver-rag`
- **Listed repository:** [FernandoJRR/archiver-rag](https://github.com/FernandoJRR/archiver-rag)
- **Default branch:** `main`
- **Reviewed head:** [`72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e`](https://github.com/FernandoJRR/archiver-rag/commit/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e)
- **Reviewed:** 2026-11-24 21:16:57 UTC (13:16:57 PST; America/Los_Angeles)
- **Review status:** Reviewed from code
- **Benchmark status:** Benchmark not run
- **Roster attribution:** [curated Atlas source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/archiver-rag.md), retained only for identity, listed locator, and source attribution.

The curated roster places Archiver RAG at ordinal 65 with slug `archiver-rag` and listed repository `https://github.com/FernandoJRR/archiver-rag`. GitHub identifies the canonical public repository and `main` as its default branch. The official main commit feed's newest entry is full SHA `72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e`, matching the repository page's latest commit prefix. All reviewed repository file links below pin to that SHA.[[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/FernandoJRR/archiver-rag)] [[official main feed](https://github.com/FernandoJRR/archiver-rag/commits/main.atom)] [[reviewed head](https://github.com/FernandoJRR/archiver-rag/commit/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1)]

## Summary

Archiver RAG is a local, agent-accessible memory layer built around an Obsidian vault of Markdown notes. A file watcher indexes note chunks into a persistent Chroma vector collection; an MCP server exposes search, note creation, graph, health, and organization tools. This review describes source-visible behavior at the pinned revision, not runtime quality or benchmark performance.[[README](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/README.md)] [[MCP server](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/mcp/server.py)]

## Who and what

The repository is maintained under the GitHub account FernandoJRR; the README presents Archiver RAG as a beta, self-hosted Python application, not a hosted service or general-purpose memory library. It stores notes in the user's Obsidian vault and supports MCP-compatible clients over stdio or HTTP. Its README says the system keeps only information that a person or agent elects to write down, rather than silently capturing every conversation.[[README](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/README.md)]

## Architecture and data model

**Code and documentation observations.** Markdown files in one configured vault are the readable source of record; the persistent Chroma collection is a derived search index. Ingest accepts indexable Markdown, parses frontmatter, derives title/type/tags and wikilinks, and records source path, folder, type, tags, links, incoming-link count, title, and integer modification time on each indexed chunk. It removes the managed Related section from the text that is chunked, then prepends a contextual prefix containing the note title, folder, up to eight tags, and up to eight outgoing links.[[ingest](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/ingest.py)] [[chunker](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/chunker.py)]

The chunker splits on whitespace into 500-word windows with 50-word overlap. Each chunk is embedded with the local sentence-transformers model all-MiniLM-L6-v2. The database wrapper lazily opens a persistent Chroma collection named obsidian_vault using cosine distance, and checks the Chroma SQLite file's modification time and size so long-lived processes can reconnect after another process changes the index.[[chunker](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/chunker.py)] [[embedder](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/embedder.py)] [[Chroma wrapper](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/db.py)]

Wikilinks form the explicit graph edges between note files. The graph linker builds each note's managed Related section from semantic neighbors, prunes links to missing notes, and can trim related links to a score margin. Folder descriptions and frontmatter type support optional semantic placement. Automatic placement, folder description refresh, and inbox routing are configuration-controlled and off by default; auto-linking and indexing are on after setup.[[linker](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/graph/linker.py)] [[README](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/README.md)]

## Write, update, delete, and retrieval

**Writes and updates.** The MCP log_note tool and CLI create a Markdown file under a type-named folder. The filename is a slug of the title; if it already exists, a numeric suffix is selected rather than replacing the existing note. Frontmatter contains the type and current date, with optional tags and related-note names. The watcher ingests new or edited Markdown by deleting old Chroma chunks for that source path and inserting freshly identified chunk rows. Editing a note in Obsidian is therefore the correction path; the code does not expose a separate semantic update or version-history API. Sync compares integer file modification times with indexed metadata, so same-second edits are a possible blind spot in the source-visible freshness rule.[[note writer and deletion](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/vault/notes.py)] [[ingest and sync](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/ingest.py)] [[watcher](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/watcher.py)]

**Deletion.** The CLI delete operation moves notes into the vault's recoverable .trash directory, removes inbound links from managed Related sections, and prunes chunks for files no longer in the vault. The watcher also handles notes moved out of the indexable vault area. This is soft deletion: the source note remains in .trash and may be recoverable. The reviewed paths do not establish secure erasure from backups, snapshots, or other copies.[[note writer and deletion](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/vault/notes.py)] [[ingest and prune](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/ingest.py)] [[watcher](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/watcher.py)]

**Retrieval.** search_vault embeds the query and asks Chroma for the requested number of nearest chunks (three by default). A frontmatter type filter is applied in the database; tag filtering happens after retrieval and fetches three times as many candidates when tags are supplied. Candidates below the configured semantic floor (0.35 by default, on the code's 1 - distance/2 score) are discarded. Reranking adds up to 0.10 for a direct incoming or outgoing wikilink to a context note and up to 0.10 for incoming-link hub status; the response includes chunk text, source path, type, tags, title, and score components. The MCP tool returns retrieved notes; it does not itself generate a natural-language answer or attach claim-level citations.[[search](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/search.py)] [[reranker](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/graph/rerank.py)] [[MCP server](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/mcp/server.py)]

## Scope isolation

The configured vault is the data boundary. Search filters can restrict frontmatter type and tags, but these are caller-selected retrieval filters, not principal or tenant authorization. The reviewed search path does not apply a per-user, per-agent, or per-project access predicate. The HTTP MCP transport has no built-in authentication or TLS; the README and security policy warn that any client able to reach it can read the vault and call mutating tools. It defaults to loopback, and the project recommends putting an authentication/TLS proxy, SSH tunnel, or private VPN in front when remote access is needed.[[search](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/search.py)] [[README](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/README.md)] [[security policy](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/SECURITY.md)]

## Provenance and evidence

Frontmatter date, type, tags, note path, title, and body text provide human-readable context, and indexed chunks retain their source path. The inspected schema does not attach an author identity, source document or conversation ID, confidence, trust state, evidence links, or mutation history to a note. Notes written by an agent and notes written by a person share the same representation. Search returns the matching text and file path, which lets a caller inspect the note, but this review found no claim-level evidence or citation mechanism in the MCP result contract.[[note writer](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/vault/notes.py)] [[ingest](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/ingest.py)] [[MCP server](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/mcp/server.py)]

## Source-visible efficiency and observability

**Code observations, not measurements.** Index writes replace all chunks for a changed note. Full index and sync walk Markdown files, and orphan pruning fetches indexed metadata to compare source paths against disk. Query cost includes query embedding, Chroma candidate retrieval, and building wikilink maps for graph reranking. The implementation exposes index chunk/note counts, missing/stale/orphaned source counts, watcher heartbeat, activity counters, and service logs; these support health diagnosis but are not latency or cost measurements.[[ingest](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/ingest.py)] [[reranker](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/graph/rerank.py)] [[index statistics](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/index_stats.py)] [[README](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/README.md)]

The upstream README reports about five seconds for the first search on a warm disk and about 70 ms for later calls, but gives no reproducible workload or environment detail in that statement. These are upstream documentation claims, not measurements from this review. The install depends on PyTorch and the embedding model; the README estimates an install around 1.4 GB and an initial model download around 90 MB. No token accounting or per-query cost reporting was found.[[README](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/README.md)] [[embedder](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/embedder.py)]

## Metric-domain evidence

All domains below are **unmeasured for this review**. The table records source-visible mechanisms or gaps only.

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable retrieval and abstention | Semantic threshold, vector candidates, and graph reranking define a retrieval path; no answer-quality or abstention probe was run. | Unmeasured |
| Correction accuracy and staleness | Manual Markdown edits are reindexed; no semantic correction history is stored. | Unmeasured |
| Deletion leakage | CLI trashing and index pruning remove active search entries but retain recoverable note files. | Unmeasured |
| Scope isolation | One configured vault with type/tag filters; no principal or tenant filtering in reviewed search. | Unmeasured |
| Evidence support and citation coverage | Search exposes source chunk and path; no claim-level citation contract was found. | Unmeasured |
| Retrieval latency and write-to-recall delay | Lazy model load, query embedding, index updates, and watcher processing are visible in source; no timings were collected. | Unmeasured |
| Tokens, cost, and storage | Local embedding/model dependencies and persistent Chroma storage are visible; no token, cost, or corpus-attributed byte measurements were collected. | Unmeasured |

The [project metric definitions](../METRICS.md), [versioned benchmark fixture](../fixtures/memory-benchmark-v1.json), and [initial execution status](../results/initial-baselines-status.json) define proposed workloads and reporting. Their planned cases are not results for Archiver RAG.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded read-only inspection of selected documentation and code at the reviewed commit. It does not establish recall quality, threshold calibration, watcher reliability under real editor workloads, same-second edit behavior, complete deletion, actual scope isolation, or performance. The project describes Archiver RAG as beta and says tools/config may change before 1.0. It documents Linux/macOS support and no Windows support. The HTTP server does not authenticate callers; deployments exposed beyond loopback need an external access-control layer. The current note/index format is Markdown-specific; broader document ingestion appears in the README as a roadmap item, not an inspected capability.[[README](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/README.md)] [[security policy](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/SECURITY.md)] [[watcher](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/watcher.py)]

## Contact-list follow-up

I checked the official pinned [README](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/README.md) and [SECURITY.md](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/SECURITY.md). They describe public issue and private vulnerability-report routes but publish no contact email. The JSON record therefore stores `contact.email: null` and records the checked source URLs.

## Benchmark status

**Benchmark not run.** No Archiver RAG runtime, benchmark workload, build, or tests were run for this review. Source structure and upstream README timing claims are not benchmark results from this review. See [project metric definitions](../METRICS.md), the [versioned fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json).[[metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Sources

- [Curated roster entry](../data/memory-systems.json) — ordinal, slug, listed locator, and Atlas attribution only.
- [Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/archiver-rag.md) — identity/locator attribution only.
- [Official repository](https://github.com/FernandoJRR/archiver-rag) — canonical public repository and default branch.
- [Official main branch feed](https://github.com/FernandoJRR/archiver-rag/commits/main.atom) — current full head at review time.
- [Reviewed head](https://github.com/FernandoJRR/archiver-rag/commit/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e)
- [README](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/README.md)
- [Ingest and synchronization](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/ingest.py)
- [Search](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/search.py)
- [Graph reranker](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/graph/rerank.py)
- [Persistent Chroma wrapper](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/db.py)
- [Chunker](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/chunker.py)
- [Embedder](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/embedder.py)
- [File watcher](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/watcher.py)
- [MCP tools](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/mcp/server.py)
- [Note writer and deletion](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/vault/notes.py)
- [Index statistics](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/archiver_rag/core/index_stats.py)
- [Security policy](https://github.com/FernandoJRR/archiver-rag/blob/72e6d82bb4d5ec2e978f109d5e8ffba13ba33e1e/SECURITY.md)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** read-only source review; no Archiver RAG execution, benchmark, build, or tests.
