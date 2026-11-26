# Flowix source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 243 / Flowix / flowix  
**Listed repository locator:** [text2future/flowix](https://github.com/text2future/flowix)  
**Current canonical repository:** [text2future/flowix](https://github.com/text2future/flowix)  
**Default branch / reviewed head:** main / `2318ff8cf02ac21650d2501e8ae1ff167d1c1aac`  
**Review time:** 2026-11-25 23:41:08 UTC (15:41:08 PST; America/Los_Angeles).

## Identity and scope

The curated catalog places Flowix at ordinal 243, with slug `flowix`, explicit listed locator `https://github.com/text2future/flowix`, and an Agent Memory Atlas attribution. That catalog and its attribution are used only to identify the system and locator. The official repository page identifies `main`; its official commit feed reports the full head SHA recorded above. The source review is pinned to that head.[[roster](../data/memory-systems.json)] [[repository](https://github.com/text2future/flowix)] [[head](https://github.com/text2future/flowix/commits/main.atom)]

Flowix describes itself as a tool for exploring AI agent workspaces and presents notebooks, notes, files, and deliverables as an editable workspace for agent context. This review focuses on its Markdown note and collection memory surfaces and the local CLI/MCP bridge, rather than treating Flowix as a standalone fact-retrieval database.[[readme](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/README.en.md)] [[website](https://flowix.cc/)] [[mcp-doc](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/dsh-flowix-memory/README.md)]

## Who and what

The public project is maintained under the Text2Future GitHub organization. It is an open-source desktop/workspace application with a local CLI and an MCP bundle: the bundle starts `flowix-cli` over stdio and reads the configured local notebook data. Its documentation says the MCP tool can search, read, create, and edit Markdown memos and access declared collection artifacts. The reviewed repo does not describe this bundle as connecting to a remote Flowix memory service.[[repository](https://github.com/text2future/flowix)] [[mcp-doc](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/dsh-flowix-memory/README.md)]

## Architecture and data model

Notebook registry metadata is stored in a device-local SQLite database at the Flowix config directory's `db/local.db`. Each notebook is a separately configured directory. For note content, Markdown files are canonical; the per-notebook SQLite note index is a rebuildable projection and does not supply the note bytes. The projection holds path-addressed note metadata such as title, preview, timestamps, tags, todos, and agent labels. The README describes the workspace as including notes, folders, databases, and web deliverables.[[registry](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-core/src/memo_file/notebook_registry.rs)] [[index](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-core/src/memo_file/note_index.rs)] [[readme](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/README.en.md)]

The MCP bundle exposes a structured `memo` tool. Its action schema includes notebook discovery, note list/tags/show/search, create/edit/write/delete, collection list/describe/query/read and collection mutations, plus artifact operations. Collections expose typed fields and records and can contain note, media, or work-document domains. This gives agents a workspace interface to both prose and structured material; it does not itself impose a fact ontology or claim-level evidence schema.[[mcp-doc](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/dsh-flowix-memory/README.md)] [[schema](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/dsh-flowix-memory/memo-tool-schema.json)] [[collections](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/collection_store.rs)]

## Write, update, delete, and retrieval

**Write.** The note CLI/MCP path creates a Markdown note in a selected notebook and optional folder, with a title defaulting to “Untitled.” Note addresses can be notebook-relative or explicit `notebook-id::relative/path`; the path resolver rejects empty, absolute, dot, and parent-traversal paths and checks that the target is inside a configured notebook. Collection operations separately support typed collection creation and record/note additions.[[path-store](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/path_store.rs)] [[schema](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/dsh-flowix-memory/memo-tool-schema.json)] [[collections](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/collection_store.rs)]

**Update and conflict handling.** `edit` replaces a nonempty exact text span only when it occurs exactly once. Full-note `write` checks an optional expected SHA-256 body version and then saves against the current body; concurrent changes return a conflict instead of being silently overwritten. MCP instructions require `expectedVersion` for write and delete. The schema documents request IDs for create-like operations; collection-add deduplication is process-local, so retries after a server restart require checking for an existing note.[[path-store](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/path_store.rs)] [[mcp](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/mcp.rs)] [[schema](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/dsh-flowix-memory/memo-tool-schema.json)]

**Delete.** The note path checks the expected content version and calls the core checked-delete operation for the addressed note. This is a delete operation on the notebook file; the inspected path does not establish deletion from backups, external copies, or synchronized replicas. Collection deletion semantics were not assessed in this bounded note review.[[path-store](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/path_store.rs)]

**Retrieval.** Note search accepts query text and optional notebook and tag filters. When no notebook filter is supplied, the implementation selects every available configured notebook, reconciles each note index, then returns matching titles, snippets, paths, and notebook-qualified addresses. A caller can use `show` to retrieve the Markdown body. List/search pagination uses offsets and a snapshot token to detect changed results. Search behavior was inspected in source; retrieval quality was not measured.[[path-store](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/path_store.rs)] [[index](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-core/src/memo_file/note_index.rs)] [[mcp](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/mcp.rs)]

## Scope isolation, provenance, and evidence

Notebooks provide an organizational scope, and addresses bind note operations to a notebook. Search can be narrowed by a notebook ID/name, but omitting that filter intentionally searches across available notebooks. The MCP code explicitly says MCP access is not a filesystem sandbox and that hosts must restrict other entry points separately. Notebook separation and path validation therefore do not establish per-user or per-project authorization isolation; no leakage probes were run.[[path-store](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/path_store.rs)] [[mcp](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/mcp.rs)] [[registry](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-core/src/memo_file/notebook_registry.rs)]

The note projection exposes created/updated times, tags, todos, and agent labels, while Markdown remains the content source. The inspected MCP and note data model do not require claim-level citations, source passages, confidence, review state, or fact-correction history. Users can store such context in documents, but this review did not find a guarantee that a retrieved assertion is supported by retained evidence.[[index](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-core/src/memo_file/note_index.rs)] [[schema](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/dsh-flowix-memory/memo-tool-schema.json)]

## Efficiency and observability

The local design uses Markdown as canonical note storage and a rebuildable SQLite projection for indexed note access. Searches reconcile the projection before querying. The MCP interface supports bounded list/query results and snapshot-aware paging; collection add request IDs are deduplicated only within the server process. These are implementation observations, not measured speed or durability results. The inspected paths do not establish retrieval latency, storage overhead, token/cost accounting, or a memory-specific quality telemetry pipeline.[[index](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-core/src/memo_file/note_index.rs)] [[path-store](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/path_store.rs)] [[mcp](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/mcp.rs)]

## Project metric domains

All benchmark results are unmeasured for this review. No Flowix runtime, benchmark, or tests were run. The project metric definitions, fixture, and result-status record below define comparison protocol and status only; they are not Flowix measurements.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[record](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a bounded, read-only inspection of the current official README, product website, memory bundle/schema, note operations, notebook registry, and note index at the verified repository head. It does not establish end-to-end retrieval correctness, calibrated abstention, correction accuracy, physical erasure across copies, authorization isolation, latency, cost, storage efficiency, or production behavior. No system runtime, tests, or benchmark workload was run.[[readme](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/README.en.md)] [[mcp-doc](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/dsh-flowix-memory/README.md)] [[path-store](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/app/flowix-cli/src/path_store.rs)] [[metrics](../METRICS.md)]

## Contact

The official pinned README and official project website were checked for a published contact email. Neither page listed one. No address was inferred from commit metadata, profiles, or third-party directories.[[readme](https://github.com/text2future/flowix/blob/2318ff8cf02ac21650d2501e8ae1ff167d1c1aac/README.en.md)] [[website](https://flowix.cc/)]

## Benchmark status

**Benchmark not run.** No Flowix runtime, tests, or benchmark workload was run. Project metrics, fixture, and execution-status files describe protocol and status only, not Flowix results.[[metrics](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[record](../results/initial-baselines-status.json)]
