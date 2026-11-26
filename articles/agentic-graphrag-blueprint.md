# Agentic GraphRAG Blueprint source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 19 / Agentic GraphRAG Blueprint / agentic-graphrag-blueprint  
**Listed repository locator:** [sebastianbrzustowicz/Agentic-GraphRAG-Blueprint](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint)  
**Current canonical repository:** [sebastianbrzustowicz/Agentic-GraphRAG-Blueprint](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint)  
**Default branch / reviewed head:** main / `e33f5f690e3b22efbf4f89d5c273a575699dd6ec`  
**Review time:** 2026-11-24 18:46:32 UTC (10:46:32 PST; America/Los_Angeles).

## Identity and scope

The curated roster places Agentic GraphRAG Blueprint at ordinal 19, lists the repository locator above, and attributes the entry to Agent Memory Atlas catalog revision `19199a4fc249e89c0793be06f0b166b358089ba0`. The official GitHub repository page identifies `main` as the default branch and shows the latest commit; the commit page verifies the full reviewed head SHA recorded above. The roster is used only for identity and attribution. Atlas descriptions, marks, prose, and layout are not assessment evidence.[[curated roster](../data/memory-systems.json)] [[repository](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint)] [[reviewed commit](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/commit/e33f5f690e3b22efbf4f89d5c273a575699dd6ec)]

The project describes itself as a reference architecture and runnable prototype for document question answering with graph and vector retrieval. It combines a FastAPI backend and React frontend, with Azure infrastructure defined in Terraform. Its README identifies Sebastian Brzustowicz as the author and publishes the contact email recorded in the JSON review record.[[README.md](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/README.md)] [[backend/app.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/app.py)]

## Architecture and data model

**Code observation.** The API module creates one NetworkX graph store and one persistent Chroma vector store when the backend process loads. The graph adapter stores a directed multigraph; graph and vector interfaces are abstracted so alternative stores can be supplied. The vector adapter embeds documents using the configured OpenAI-compatible embedding endpoint and writes them into the `graphrag` collection with cosine distance.[[backend/app.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/app.py)] [[graph-store interface](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/storage/base.py)] [[graph adapter](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/storage/graph_store.py)] [[vector adapter](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/storage/vector_store.py)]

Ingestion splits documents into sentence-oriented chunks, asks an LLM for entity and relation JSON, merges entities by canonical names, constructs a graph, detects communities with Leiden, and creates text reports for communities. The vector store indexes chunks, entities, and reports under kind metadata. It persists graph data as a pickle and tracks file/report state in a JSON state file. The README and code describe skipping unchanged files using content hashes and regenerating reports for affected communities; these are implementation design observations, not measured savings.[[ingestion](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/ingestion.py)] [[README.md](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/README.md)] [[configuration](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/config.py)]

## Write, update, delete, and retrieval

**Write and update — code observation.** The API accepts uploaded files into its configured data directory and starts ingestion in a background thread. The ingestion logic uses file state and content hashes to identify changes, extracts graph data from changed chunks, updates vector records, and saves graph/state snapshots. A force-reset configuration is available for a full rebuild. The inspected API does not expose per-memory CRUD operations; the primary write unit is an ingested file/corpus.[[backend/app.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/app.py)] [[ingestion](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/ingestion.py)] [[configuration](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/config.py)]

**Delete — code observation and limit.** The vector adapter supports deleting IDs, and ingestion removes stale community-report IDs. The inspected API does not provide a user-facing delete-document operation or demonstrate full cleanup of graph nodes, source chunks, persisted state, backups, and derived data when a source file is removed. Deletion completeness is therefore unknown from this review.[[vector adapter](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/storage/vector_store.py)] [[ingestion](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/ingestion.py)]

**Retrieval.** Local search obtains vector matches for entity and chunk kinds, expands a graph neighborhood around entity hits, puts graph context and source-labeled chunks into the LLM prompt, and returns an answer and subgraph. Global search retrieves community reports, maps them to question-relevant summaries, reduces those summaries to an answer, and returns report-associated graph nodes. The default prompt asks local search to state when provided context is insufficient; this is a prompt instruction, not measured abstention behavior. The API response shape does not include a list of claim-level citations or source-chunk identifiers.[[search](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/search.py)] [[prompts](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/prompts.json)] [[backend/app.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/app.py)]

## Scope isolation and provenance

**Scope observation.** The inspected API initializes a single graph and vector collection for the process; query requests carry query text and a local/global mode, with no user, tenant, project, or document-scope field. The FastAPI setup enables wildcard CORS and the inspected API module shows no authentication middleware. The README describes Entra ID on the frontend for its deployment, but that does not establish backend data-layer tenant isolation. Treat deployment authorization and cross-user isolation as unverified.[[backend/app.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/app.py)] [[search](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/search.py)] [[README.md](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/README.md)]

**Evidence and provenance.** Source chunks carry source metadata into vector search hits and local prompt context; the frontend can visualize returned graph subgraphs. The API returns the answer and subgraph, but the inspected response contract does not return claim-to-source links. Community reports summarize graph members and relations, with report metadata retaining an entity list. This provides inspectable context paths, not proof that generated claims are supported by cited source passages.[[search](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/search.py)] [[ingestion](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/ingestion.py)] [[README.md](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/README.md)]

## Source-visible efficiency and observability

**Code observation.** Configuration exposes chunk size and overlap, embedding batch size, extraction batch size, top-k limits, graph radius, and LLM concurrency. Ingestion uses threaded work for file processing and community report generation; embeddings and API calls have retry paths with exponential delays. The README describes incremental hash checks and regeneration limited to affected communities. These are visible controls and intended work-saving mechanisms, not throughput, latency, or cost measurements.[[configuration](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/config.py)] [[ingestion](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/ingestion.py)] [[vector adapter](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/storage/vector_store.py)]

The API emits Python logs for uploads and ingestion failures and exposes health, ingestion progress, and aggregate node/edge/document counts. Progress state includes file counts and an error/result field. The inspected code does not establish distributed tracing, token/cost accounting, or a persistent latency histogram.[[backend/app.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/app.py)] [[progress state](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/progress.py)]

## Project metric domains

All benchmark domains are **unmeasured** for this system. The inspected sources show answer generation and a prompt instruction to report insufficient context, but no answerable-recall or abstention evaluation; there are no correction/staleness operations or results; deletion completeness and scope isolation have not been tested; the API does not return claim-level citations for support adjudication; and no runtime latency, write-to-recall delay, token/cost, or storage-efficiency measurements were collected. Project metric definitions and fixture define evaluation protocols, not Agentic GraphRAG Blueprint results.[[project metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded read-only inspection of the current repository page, selected official documentation, and backend files at the verified SHA. The system was not executed. The reviewed evidence does not establish production availability, deployed authentication boundaries, entity-resolution quality, answer grounding, complete source-file deletion, behavior under concurrent ingestion/query load, or performance and cost at any corpus size. Unknown means unverified in this review.[[backend/app.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/app.py)] [[ingestion](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/ingestion.py)] [[search](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/search.py)]

## Contact-list follow-up

The official pinned README names the author and publishes `Se.Brzustowicz@gmail.com`; the JSON record stores that value and the exact pinned README source URL. No profile, third-party directory, or commit metadata was used.[[README.md](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/README.md)]

## Benchmark status

**Benchmark not run.** No system execution, test suite, or benchmark workload was run. Code observations and product documentation are not measured results. See the project metric definitions, execution status, and fixture for the separate measurement protocol.[[project metric definitions](../METRICS.md)] [[benchmark execution status](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical GitHub repository](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint)
- [Reviewed full main head commit](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/commit/e33f5f690e3b22efbf4f89d5c273a575699dd6ec)
- [README.md](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/README.md)
- [CONTRIBUTING.md](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/CONTRIBUTING.md)
- [backend/app.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/app.py)
- [backend/src/config.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/config.py)
- [backend/src/ingestion.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/ingestion.py)
- [backend/src/progress.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/progress.py)
- [backend/src/search.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/search.py)
- [backend/src/storage/base.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/storage/base.py)
- [backend/src/storage/graph_store.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/storage/graph_store.py)
- [backend/src/storage/vector_store.py](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/src/storage/vector_store.py)
- [backend/prompts.json](https://github.com/sebastianbrzustowicz/Agentic-GraphRAG-Blueprint/blob/e33f5f690e3b22efbf4f89d5c273a575699dd6ec/backend/prompts.json)
- [Project metric definitions](../METRICS.md)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and source attribution](../data/memory-systems.json)

**Verification boundary:** no Agentic GraphRAG Blueprint system, tests, or benchmarks were run.
