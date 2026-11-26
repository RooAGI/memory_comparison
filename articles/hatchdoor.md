# Hatchdoor source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 283 / Hatchdoor / `hatchdoor`  
**Listed repository locator:** [BatterWorks/Hatchdoor](https://github.com/BatterWorks/Hatchdoor)  
**Canonical upstream:** [BatterWorks/Hatchdoor](https://github.com/BatterWorks/Hatchdoor)  
**Default branch / reviewed head:** main / [7268fdab2024bf04e2dff7cd8febb17ec97e1092](https://github.com/BatterWorks/Hatchdoor/commit/7268fdab2024bf04e2dff7cd8febb17ec97e1092)  
**Review time:** 2026-11-25 22:31:33 UTC (2026-11-25 14:31:33 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists Hatchdoor at ordinal 283, slug `hatchdoor`, with the explicit locator `https://github.com/BatterWorks/Hatchdoor`. Its pinned Atlas entry is included only as roster attribution and locator context; it is not assessment evidence. The official GitHub repository page identifies `main` as the default branch. GitHub's official `commits/main` API returned the full current head `7268fdab2024bf04e2dff7cd8febb17ec97e1092`, which is the revision reviewed here.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Hatchdoor is a self-hosted server for Markdown and Obsidian-style vaults. It serves a browser UI and an MCP endpoint over shared note operations, and maintains a disposable SQLite read model for browsing, links, metadata, keyword search, and semantic search. Markdown on disk remains canonical.[[readme]][[module-map]][[snapshots]]

## Who and what

The official project presents Hatchdoor as a self-hosted vault server with web and MCP interfaces. The repository is published under BatterWorks. The README explicitly describes the deployment as single trusted user: it is not a hosted sync service or multi-user collaboration platform.[[readme]]

## Architecture and data model

The repository describes one Rust server combining HTTP handlers, MCP tools, and the browser application over shared Vault read and mutation cores. A registry gives each Vault an identity, source folder, settings, and optional Git configuration. Markdown files in that folder are authoritative; the SQLite cache is generated and is intended to be rebuildable from those files.[[readme]][[module-map]][[vault]][[snapshots]]

The cache publishes a Vault-qualified snapshot of note structure, links, tags, metadata, and searchable chunks. Semantic search adds locally generated vectors. Snapshot status tracks participation, freshness, and whether vectors are available as separate properties; structural browsing can be available before embedding finishes. Exact note reads continue to use the Markdown source rather than treating cached bodies as canonical.[[snapshots]][[search]][[read-core]]

## Write, update, delete, and retrieval

The shared mutation core resolves a Vault ID, checks lifecycle and write capability, serializes the operation with that Vault's mutation lock, builds a pre-write index for path and layer checks, then runs filesystem work off the async runtime. The exposed primitives include create, append, edit, update, frontmatter update, section replacement, move/rename, archive, note deletion, tag changes, and attachment operations. Note writes use an expected content hash to reject stale edits. Where the filesystem supports atomic compare-and-swap, the write can use that stronger commit path; on filesystems without it, a weaker check-then-rename path remains writable and can race an outside editor. An intent log supports recovery of interrupted multi-file writes.[[mutation-core]][[vault]][[readme]]

Delete actions move the note and its folder assets into `.hatchdoor-trash`, which the indexer excludes; archive moves notes below the configured archive prefix. These are recoverable moves, not proof of physical erasure. The reviewed sources do not establish secure deletion of copies outside the active vault or its Git history.[[readme]][[vault]]

Retrieval includes exact reads, note outlines and selected sections, structural browsing, keyword search, and semantic search. Search requests name a Vault scope and a search mode; the code has distinct keyword and semantic paths rather than a single fused mode. Search results include the Vault, note and chunk identifiers, note path, heading path, text, score, layer, links, and note metadata. The inspected search implementation bounds ranked candidates and applies a per-note result cap. No retrieval quality or timing was measured here.[[read-core]][[search]][[snapshots]]

## Scope isolation

The read core accepts either one canonical Vault ID or the literal `all`. It resolves requested Vaults before reading, excludes disabled/nonparticipating snapshots, and the search queries also constrain rows to the selected Vault IDs. Writes require one Vault; collection-wide scope is not a mutation target.[[read-core]][[search]][[mutation-core]][[module-map]]

Vault scope is a query boundary, not a per-user authorization boundary. The README says whoever can reach the trusted private deployment can see every served Vault; the MCP endpoint uses one shared bearer token and has no account-to-Vault permission mapping. The task did not run cross-Vault or cross-surface isolation probes.[[readme]][[security]]

## Provenance and evidence

Markdown is the primary record, with note paths, frontmatter, file hashes, and links available as context. Optional Git integration can commit writes and add a `Hatchdoor-Origin` trailer for web or MCP origin; MCP client names are labels supplied by the client, not verified identities. Unrecorded changed paths can be labeled unknown. The reviewed sources do not show a fact-level verification state or a mechanism that adjudicates whether a retrieved note supports an answer. These mechanisms preserve content and operational origin, not truth guarantees.[[readme]][[git-origin]][[snapshots]]

## Efficiency and observability

The disposable SQLite read model avoids rebuilding note structure for every query. Search omits bodies and frontmatter properties when those values are unnecessary, uses bounded candidate windows, and limits repeated chunks from one note. Local embedding models are selected during setup; the README says vault content is not sent to a remote embedding service. Index turns publish structural rows before vectors and expose readiness/progress and per-Vault status. Request tracing and optional usage reports are documented; usage reporting is off unless enabled and is described as deployment-configuration telemetry.[[snapshots]][[search]][[readme]][[module-map]][[security]]

## Metric-domain evidence

All benchmark domains are unmeasured in this review. The source mechanisms below are not benchmark results.[[metrics]][[fixture]][[status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Keyword/semantic retrieval and exact reads exist; answer correctness and abstention were not evaluated. | Unmeasured |
| Correction and staleness | Hash-checked updates and stale/fresh snapshot states are implemented; correction accuracy and stale-answer rate were not measured. | Unmeasured |
| Deletion leakage | Delete moves notes into excluded trash; no post-delete retrieval, external-copy, or Git-history probe was run. | Unmeasured |
| Scope isolation | Vault-qualified scopes and SQL filters exist; no isolation workload was run, and scope is not account authorization. | Unmeasured |
| Evidence support and citations | Note paths, links, metadata, and optional Git origin are exposed; answer support and citation precision were not adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | Bounded search and indexing progress are implemented; no timings were collected. | Unmeasured |
| Tokens and cost | Compact results and local embedding options are documented; no token or cost workload was run. | Unmeasured |
| Storage efficiency | SQLite is a derived cache over Markdown, but no size or rebuild-cost comparison was run. | Unmeasured |

## Limits and unknowns

This review covers the pinned README, architecture map, shared mutation/read cores, snapshot storage, scoped search, Git origin message code, and security policy. It did not inspect every HTTP/MCP adapter, all individual mutation helpers, model implementation details, or all cache migration paths. No Hatchdoor runtime, tests, benchmarks, or isolation probes were run. Consequently, retrieval quality, operational performance, end-to-end freshness delay, actual erasure across backups/remotes, and answer-level evidence quality remain unknown.[[readme]][[module-map]][[mutation-core]][[vault]][[read-core]][[search]][[snapshots]][[git-origin]][[security]]

The project documents a single trusted operator model. A bearer token and caller-provided MCP client label should not be read as distinct user identities or per-Vault permissions. Local Git history and remote synchronization also make trash moves distinct from deletion across all copies.[[readme]][[security]][[git-origin]]

## Benchmark status

**Benchmark not run.** No Hatchdoor runtime, tests, or benchmark workload was run. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. See the project [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json); these are evaluation materials, not Hatchdoor results.[[metrics]][[fixture]][[status]]

## Contact

The official pinned README and `SECURITY.md` were checked. Neither publishes a contact email; `contact_email` is null in the structured record. No commit/profile metadata or third-party directory was used.[[readme]][[security]]

## Sources

Repository implementation citations are pinned to the verified full SHA. The Atlas link records curated roster attribution only, not assessment evidence. See the structured [review record](../data/system-reviews/hatchdoor.json) and [curated catalog](../data/memory-systems.json).
