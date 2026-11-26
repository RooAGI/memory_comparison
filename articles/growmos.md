# growmos source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 277 / growmos / `growmos`  
**Listed repository locator:** [codician-team/growmos](https://github.com/codician-team/growmos)  
**Canonical upstream:** [codician-team/growmos](https://github.com/codician-team/growmos)  
**Default branch / reviewed head:** main / [510deb2dfee151fb79402b0a3274025f9c1c2c71](https://github.com/codician-team/growmos/commit/510deb2dfee151fb79402b0a3274025f9c1c2c71)  
**Review time:** 2026-11-25 22:10:11 UTC (2026-11-25 14:10:11 PST; America/Los_Angeles).

## Identity and review pin

The curated catalog lists ordinal 277 as growmos, slug `growmos`, with the explicit locator `https://github.com/codician-team/growmos`. The catalog’s pinned Atlas entry is included only for roster identity and locator attribution, not as assessment evidence. GitHub’s official repository page shows `main`; the official `main.atom` feed identifies full head `510deb2dfee151fb79402b0a3274025f9c1c2c71`, matching the catalog pin. The official commit tree API returned that same SHA.[[catalog]][[atlas]][[repo]][[head]][[tree]]

## Summary

Growmos is a Python command-line and MCP knowledge graph for repository documentation and agent sessions. It stores entities, aliases, relations, sources, and raw mentions in editable files under `.growmos/`. A staged pipeline delegates extraction and resolution judgments to an agent through task packets, while deterministic code validates and assembles the graph. Queries return a bounded graph neighborhood with edge identifiers and source labels for citation. This is an implementation review; it does not measure answer quality or runtime performance.[[readme]][[store]][[graph]][[schema]]

## Who and what

The official README describes Growmos as an open-source, tool-agnostic implementation built by Codician. It provides a CLI and zero-dependency MCP stdio server, with integration instructions for agent CLIs. Optional headless ingestion can call configured Anthropic or OpenAI-compatible APIs. No individual maintainer identity is asserted here.[[readme]]

## Architecture and data model

The `.growmos/` directory is the system’s working state. `sources.jsonl` tracks source references, content hashes, and processing status; `mentions.jsonl` retains raw extracted entity mentions append-only; `entities.jsonl` contains canonical typed nodes; `aliases.jsonl` maps names to nodes; and `relations.jsonl` holds directed predicates with source IDs and corroboration counts. `schema.json`, `config.json`, `state.json`, profiles, prompts, gold examples, and an append-only journal support the processing loop and evaluation. The format is deterministic JSON/JSONL intended to be hand-editable and committed with a repository.[[store]][[file-format]]

Extraction produces typed entity and relation candidates. The validator rejects malformed rows and drops relations whose endpoints were not included among extracted entities. Resolution is a structured judgment stage; missing names fall back to single-name clusters, and unmatched entities remain provisional instead of being discarded. Source changes are detected by content hash and put back into `pending` status for reprocessing. Profiles are summarized records keyed to their source set and can be marked stale when that set changes.[[schema]][[store]][[file-format]][[readme]]

## Write, update, delete, and retrieval

**Write.** `growmos remember` creates or finds an entity and stores a raw mention with its source reference. `growmos link` creates or finds endpoint entities and adds a directed relation; repeated assertions of the same relation add distinct source IDs. `growmos journal` appends a timestamped memo. Document ingestion follows `next` task packets and `apply` validation; the README also documents optional headless `ingest`. These paths distinguish agent-provided judgments from deterministic validation and storage.[[readme]][[store]][[schema]]

**Update and correction.** Re-registering a file source with a changed hash marks it pending so changed content can be extracted again. Entity resolution can repoint aliases, merge a provisional or duplicate entity into a canonical one, and rewrite its relation endpoints. The merge combines source lists and mention counts, but the inspected merge path does not retain a durable merge event or explicit correction history. Relation identity is derived from endpoints and normalized predicate; source corroboration is the number of distinct source documents, not a calibrated confidence score.[[store]][[file-format]]

**Delete.** The README’s documented command and MCP tool surfaces do not list a general fact-forget or delete operation, and no standalone delete method was found in the inspected store implementation. `merge` removes the folded entity after redirecting aliases and relations; `compact` prunes dangling relations and aliases and deduplicates raw mentions. These operations do not establish erasure of the original source documents, repository history, or external copies. Deletion behavior therefore remains a significant unknown beyond the inspected merge and compaction paths.[[readme]][[store]]

**Retrieval.** Query resolves seed entities from aliases and question tokens, traverses a k-hop neighborhood, serializes the induced subgraph, sorts edges by corroboration, and limits output (the inspected graph defaults to at most 400 nodes and 300 triples). Serialized edges include edge IDs and up to three source labels. The answer schema requires both `cited_edges` and `not_in_graph`; `check` compares a claimed relation with graph edges and can return related edge evidence when the exact claim is absent. These constraints support traceable answers but do not by themselves establish factual correctness or calibrated abstention.[[graph]][[schema]][[readme]]

## Scope isolation

Growmos keeps `.growmos/` under a repository root, and file sources are addressed by repository-relative paths. The inspected entity, alias, relation, and source schemas contain no user, tenant, or per-agent authorization scope. The project directory is therefore the visible data boundary; it is not a demonstrated security boundary. Shared access, committed graph contents, filesystem permissions, and multi-tenant isolation were not tested.[[store]][[file-format]][[readme]]

## Provenance and evidence

Relations carry source IDs; sources carry references and content hashes; and raw extracted mentions are retained append-only. Relation IDs identify a triple, while the `confidence` field counts distinct source documents that corroborate it. Query serialization returns edge IDs and source labels, and the answer shape requires edge citations. The model does not imply that source text supports every generated claim: the review stage writes a memo rather than attaching its verdict to the judged node, and source evidence support was not benchmarked.[[store]][[graph]][[schema]][[readme]]

## Efficiency and observability

Content hashes avoid reprocessing unchanged documents. Configuration caps the default extraction run at 50 documents, limits entities per document, and chunks long documents; graph traversal and serialization cap returned context. The deterministic graph implementation uses Python dictionaries and sets without a graph-library dependency. `status` and graph diagnostics expose node/edge counts, connected components, density, isolated nodes, provisional entities, pending sources, and stale profiles. Optional headless providers and unattended ingestion introduce model/API usage; no latency, tokens, cost, or storage measurements were collected.[[store]][[graph]][[readme]][[file-format]]

## Metric-domain evidence

All project benchmark domains are **unmeasured here**. Source paths and the repository’s own evaluation workflow are not results from this review. The [metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe project evaluation materials, not Growmos measurements.[[metrics]][[fixture]][[execution_status]]

| Domain | Source evidence | Measurement status |
|---|---|---|
| Answerable recall and abstention | Query serialization requires edge citations and a `not_in_graph` field; answer correctness and abstention were not scored. | Unmeasured |
| Correction accuracy and stale retrieval | Source hashes trigger reprocessing and merge rewrites graph references; correction sequences were not evaluated. | Unmeasured |
| Deletion leakage | No general delete path was identified in the inspected command/tool surface and store; no deletion probe was run. | Unmeasured |
| Scope isolation | State is repository-local with no principal field in inspected records; no cross-scope workload was run. | Unmeasured |
| Evidence support and citation coverage | Responses carry edge IDs and source labels; no claims were adjudicated against source text. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timed workload or probe schedule was run. | Unmeasured |
| Tokens and cost | Optional model providers are documented; usage and charges were not measured. | Unmeasured |
| Storage efficiency | JSONL persistence is inspectable; no corpus storage measurement was made. | Unmeasured |

## Limits and unknowns

This review inspected the current README, store, graph, schema, and file-format documentation at the verified full SHA. Growmos, its test suite, and benchmarks were not run. README statements about the project’s own graph, evaluation workflow, or token reduction are upstream claims, not measurements reproduced here.[[readme]][[store]][[graph]][[schema]][[file-format]]

Mutation and deletion semantics beyond entity merge and compaction were not established. No adversarial isolation test, source-grounding adjudication, retrieval-quality evaluation, provider-cost accounting, or persistent-storage measurement was performed. The data model records provenance references, but source support, authorization boundaries, and deletion completeness remain unverified.[[store]][[graph]][[schema]][[metrics]]

## Benchmark status

**Benchmark not run.** No Growmos runtime, tests, or benchmark workload was executed. No retrieval, correction, deletion, scope, evidence, latency, token, cost, or storage result is claimed. The [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status record](../results/initial-baselines-status.json) describe the evaluation protocol, not Growmos measurements.[[metrics]][[fixture]][[execution_status]]

## Contact

The official pinned [README](https://github.com/codician-team/growmos/blob/510deb2dfee151fb79402b0a3274025f9c1c2c71/README.md) and the [official project website](https://codician-team.github.io/growmos/) were checked for a published contact email; neither publishes one. The structured record stores `contact_email: null` and both exact checked URLs. No profile, commit metadata, Atlas description, or third-party directory was used.[[readme]][[site]]

## Sources

All upstream file citations are pinned to the verified full SHA. The Atlas source is included only for curated roster attribution, not system assessment. See the structured record [growmos.json](../data/system-reviews/growmos.json) and the [curated roster](../data/memory-systems.json).