# AnythingLLM source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 59 / AnythingLLM / `anything-llm`  
**Listed repository locator:** [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm)  
**Catalog source attribution:** [Agent Memory Atlas report at catalog revision 19199a4fc249e89c0793be06f0b166b358089ba0](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/anything-llm.md)  
**Canonical repository:** [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm)  
**Default branch / reviewed head:** master / [b01447009150507ae0cfd1304e3492fcaf2a92d8](https://github.com/Mintplex-Labs/anything-llm/commit/b01447009150507ae0cfd1304e3492fcaf2a92d8)  
**Review time:** 2026-11-24 20:56:14 UTC (12:56:14 PST; America/Los_Angeles). GitHub's repository page identifies `master`; its official master Atom feed names the head above.  
**Published contact:** No published contact email was found in the checked official [repository README at the reviewed revision](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/README.md); the JSON record stores null with that exact checked URL.

## Identity and review pin

The curated roster places AnythingLLM at ordinal 59, slug `anything-llm`, and lists `https://github.com/Mintplex-Labs/anything-llm`. It attributes the entry to the Atlas report pinned at `19199a4fc249e89c0793be06f0b166b358089ba0`. The roster is used only to establish identity, the listed locator, and attribution. Atlas descriptions, marks, report prose, and layout are not assessment evidence. [[curated roster entry](../data/memory-systems.json)] [[catalog attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/anything-llm.md)]

GitHub identifies the public canonical repository as `Mintplex-Labs/anything-llm` and shows `master` as its default branch. The official `master.atom` feed reports head `b01447009150507ae0cfd1304e3492fcaf2a92d8`; the repository page's latest commit abbreviation agrees. Code and documentation links below are pinned to that full SHA. [[repository page](https://github.com/Mintplex-Labs/anything-llm)] [[master history feed](https://github.com/Mintplex-Labs/anything-llm/commits/master.atom)] [[reviewed commit](https://github.com/Mintplex-Labs/anything-llm/commit/b01447009150507ae0cfd1304e3492fcaf2a92d8)]

## Summary

AnythingLLM is a self-hostable, multi-user AI application with workspace document retrieval, agents, and a first-party memory feature. The reviewed memory path stores short user or workspace facts in the application's relational database and appends a bounded selection to the chat system prompt. The code exposes scoped reads and writes; retrieval quality, deletion leakage, and performance were not measured. [[README](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/README.md)] [[memory model](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/models/memory.js)] [[memory prompt integration](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/utils/memories/index.js)]

## Who and what

The public repository is maintained under the Mintplex-Labs GitHub organization. Its README describes AnythingLLM as an all-in-one AI application, with local and hosted model support, document chat, agents, multi-user features, and automatic and user-managed memories. This review covers the first-party relational-memory model and prompt-injection helper, not every document/vector-store or agent memory mechanism in the wider application. [[repository](https://github.com/Mintplex-Labs/anything-llm)] [[README](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/README.md)]

## Architecture and data model

The repository describes a monorepo with a React frontend, Node/Express server, and a separate document collector. The reviewed memory model uses Prisma and stores records with an integer ID, nullable user and workspace IDs, a `workspace` or `global` scope, text content, last-used time, and created/updated timestamps. The model defines limits of 20 workspace memories and five global memories; global records are keyed to a user and have no workspace ID. [[README](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/README.md)] [[memory model](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/models/memory.js)]

The injection helper checks the system memory setting, then fetches that user's global records and records for the current workspace concurrently. It includes all selected global rows and up to five workspace rows. When there are more than five workspace candidates, it reranks them against the current prompt and up to the last three user turns; a reranker error falls back to the newest five. The selected text is formatted as a Markdown list under “Things I Remember About You” and appended to the system prompt. [[memory prompt integration](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/utils/memories/index.js)]

## Write, update, delete, and retrieval

**Write.** The model validates integer identifiers, accepted scope names, and non-empty content. Its create path counts rows for the specified scope, rejects a write when the corresponding 20-row workspace or five-row global limit is reached, then creates a Prisma row. These are source-visible rules, not a concurrency or runtime measurement. [[memory model](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/models/memory.js)]

**Update.** The reviewed model includes single-record content updates and a transactional batch path. In the batch path, LLM-provided update IDs are treated as untrusted: update predicates include the current user and either the current workspace scope or that user's global scope. Existing content is overwritten and `updatedAt` is refreshed. This is mutable state; the inspected model does not establish an append-only revision history or effective-time history. [[memory model](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/models/memory.js)]

**Delete.** The reviewed source surface establishes memory records and reads/writes, but the available code excerpt did not let me verify the exact delete implementation or its behavior across storage copies. Hard-erasure semantics and post-delete recall are therefore unknown in this review; no deletion probe was run. [[memory model](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/models/memory.js)]

**Retrieval.** Prompt-time retrieval is scope-filtered and newest-first at the database query. The helper reranks only the workspace candidates when that set exceeds five and a prompt or recent history is present; reranker failures fall back to the first five newest rows. Global records are all included, up to the model's five-record write cap. The helper catches failures, logs the error, and returns an empty memory section. These mechanics describe source behavior only; they do not establish answer quality or the efficacy of reranking. [[memory model](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/models/memory.js)] [[memory prompt integration](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/utils/memories/index.js)]

**Scope isolation.** Both reviewed read queries constrain user ID; the workspace query also constrains workspace ID and `scope = workspace`, while global retrieval constrains `scope = global`. The batch update path similarly constrains mutations to the current user and allowed current-workspace/global scope. This is code evidence for those query predicates, not a runtime isolation guarantee across all application endpoints or deployment configurations. [[memory model](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/models/memory.js)]

**Provenance and evidence.** The reviewed memory row contains text and ownership/scope/timestamp fields, but no source-chat pointer, source passage, confidence, or evidence citation field. The prompt helper injects memory text without a memory ID or source citation. The inspected path therefore does not itself preserve claim-level supporting evidence. Other application surfaces may maintain provenance separately; they were not assessed here. [[memory model](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/models/memory.js)] [[memory prompt integration](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/utils/memories/index.js)]

## Metric-domain evidence

All project benchmark domains are **unmeasured** for this review. The following are implementation observations, not measured results. The project metric definitions and shared execution record are linked for protocol context only. [[metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[benchmark execution status](../results/initial-baselines-status.json)]

- **Answerable retrieval and abstention:** code selects prompt memories and falls back to an empty section on errors; no answerable or unanswerable questions were run.
- **Correction accuracy and stale-value rate:** the model permits overwriting content, but no correction workload or stale-answer adjudication was performed.
- **Deletion leakage:** delete behavior was not established from the inspected excerpt and no post-delete probe was run.
- **Scope-isolation leakage:** user/workspace predicates are visible in read and batch-update code, but no cross-scope probes were run.
- **Evidence support and citation coverage:** the inspected memory row and prompt format expose no source citations; no generated claims were evaluated.
- **Retrieval latency and write-to-recall delay:** no timed retrieval samples or scheduled write-to-recall probes were collected.
- **Tokens, cost, and storage:** prompt injection adds selected record text, but no token, provider cost, database size, or per-item storage measurement was collected.

## Limits and unknowns

This is a bounded review of the current canonical repository at the pinned SHA, focused on `server/models/memory.js` and `server/utils/memories/index.js`. It does not establish behavior of every memory API route, automatic extraction worker, deployment option, or external vector-backed agent tool. The exact delete/erasure path was not verified. Source predicates do not prove adversarial isolation. No runtime behavior, answer quality, reliability, latency, cost, token use, or storage efficiency was measured. [[README](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/README.md)] [[memory model](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/models/memory.js)] [[memory prompt integration](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/utils/memories/index.js)]

## Benchmark status

**Benchmark not run.** No AnythingLLM instance, benchmark workload, or tests were run. The project metrics, fixture, and execution-status record describe the comparison protocol and shared run state; they are not AnythingLLM results. [[metric definitions](../METRICS.md)] [[fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Contact-list follow-up

I checked only the official repository README for a published contact email. The checked README at the reviewed revision did not publish a contact email, so the JSON record stores null and the exact README URL. I did not use commit metadata, personal profile emails, third-party directories, or infer an address. [[checked official README](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/README.md)]

## Sources

- [Canonical repository and default branch](https://github.com/Mintplex-Labs/anything-llm)
- [Current master branch history feed](https://github.com/Mintplex-Labs/anything-llm/commits/master.atom)
- [Verified reviewed head](https://github.com/Mintplex-Labs/anything-llm/commit/b01447009150507ae0cfd1304e3492fcaf2a92d8)
- [README.md](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/README.md)
- [server/models/memory.js](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/models/memory.js)
- [server/utils/memories/index.js](https://github.com/Mintplex-Labs/anything-llm/blob/b01447009150507ae0cfd1304e3492fcaf2a92d8/server/utils/memories/index.js)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Curated roster identity and source attribution](../data/memory-systems.json)

**Verification boundary:** source observations above are tied to the pinned SHA; benchmark status is not_run; no system, benchmark, or tests were run.
