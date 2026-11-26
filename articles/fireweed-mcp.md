# Fireweed MCP source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Curated ordinal / name / slug:** 239 / Fireweed MCP / fireweed-mcp  
**Listed repository locator:** [Starksood/fireweed-mcp](https://github.com/Starksood/fireweed-mcp)  
**Canonical upstream:** [Starksood/fireweed-mcp](https://github.com/Starksood/fireweed-mcp)  
**Default branch / reviewed head:** main / [b37747b0c8f2ed7f1b6b05309a6fb660a82d8605](https://github.com/Starksood/fireweed-mcp/commit/b37747b0c8f2ed7f1b6b05309a6fb660a82d8605)  
**Review time:** 2026-11-25 20:29:44 UTC (2026-11-25 12:29:44 PST; America/Los_Angeles).

## Identity and review pin

The curated roster lists Fireweed MCP at ordinal 239, slug fireweed-mcp, with the explicit locator https://github.com/Starksood/fireweed-mcp. Its Atlas entry is recorded only as curated identity and locator attribution. The official GitHub repository identifies the canonical repository and default branch `main`; GitHub’s current repository and commit APIs, fresh `git ls-remote`, and a shallow checkout agree on full head b37747b0c8f2ed7f1b6b05309a6fb660a82d8605. This review is pinned to that revision.[[catalog]][[atlas]][[repo]][[head]]

## Summary

Fireweed MCP is a local MCP memory server that admits a proposed claim only after deterministic checks compare it with quoted evidence. It returns grounded claim records with byte-range receipts and can abstain with a typed reason. The README describes the write gate as the stronger part and retrieval on unseen phrasings as a major weakness.[[readme]][[server]][[receipts]]

## Who and what

The public repository presents a stdlib-only MCP server using JSON-RPC over stdin and stdout. The server itself does not call a model; an optional companion extractor proposes claim/evidence pairs, which still pass through the same checks. The official README publishes sanyamsood2@gmail.com for commercial-use inquiries; the structured record stores that exact official URL.[[readme]][[server]]

## Architecture and data model

The server defaults to a local store under `~/.fireweed/mcp/`, overridable with `FIREWEED_MCP_STORE`. It keeps a JSON substrate snapshot, source documents, a SQLite event ledger, and keys in a separate directory. The snapshot is an open, versioned JSON format with a standard-library reference reader. The graph contains claims, entities, and typed relations.[[server]][[spec]][[readme]]

A node records claim and normalized text, entity references, domains and facets, predicate and temporal fields, provenance, reinforcement, and lifecycle status. Relations represent supersession, support, contradiction, causality, and other links. The format retains superseded claims while treating erasure as a separate operation. Its spec warns that emitted entity types are currently unreliable.[[graph]][[spec]]

The ingest pipeline converts proposals into create, modify, dispute, or no-op mutations after a deterministic firewall decision. The server attaches and seals a SQLite ledger, commits mutation events with WAL and synchronous FULL, and rewrites the JSON snapshot after mutation. Ledger events are hash-chained and can reconstruct graph state from a checkpoint and later events.[[pipeline]][[server]][[sqlite-ledger]][[ledger]]

## Write, update, delete, and retrieval

**Write.** The MCP `remember` tool requires a claim and evidence text. The gate checks subject grounding, relation order, numerals, and whether the claim asserts more than the evidence. Refusals are typed. Supplying the full source document lets the server create a receipt that binds the quoted evidence to a SHA-256 hash and exact UTF-8 byte range. Source origin and validation fields are caller-declared, not verified.[[server]][[firewall]][[receipts]][[provenance]]

**Update.** There is no general in-place update tool in the MCP surface. The ingest resolver may choose a modification: the pipeline marks the older node superseded, stamps its validity end and replacement ID, adds a supersedes relation, and creates a new node. A conflicting proposal can instead leave both claims disputed and readable. Superseded records remain in the snapshot as history.[[server]][[pipeline]][[graph]][[spec]]

**Delete.** The `forget` tool computes a subject’s connected claim/entity closure, appends an ERASE event, destroys the subject content key when the keyring is attached, and redacts matching source passages. Merkle receipts for unaffected passages can remain verifiable. It runs probes and issues a certificate only when erasure passes; the certificate states what it covers and does not attest to copies outside the active substrate and ledger.[[server]][[erasure]][[crypto]][[readme]]

**Retrieval.** The read path uses deterministic graph retrieval with lexical similarity/query coverage, entity match, and reinforcement in ranking, with optional graph and significance expansions. A read gate checks a requested predicate and subject scope before returning up to five displayed matches with receipts, or a typed abstention and suggested remedy. The optional semantic encoder is off by default; the README reports that enabling it substantially harms absent-answer refusals.[[retrieval]][[read-gate]][[server]][[readme]]

The MCP tools also include source registration, read review, evidence tracing, receipt verification, export, and memory statistics. Read auditing is off by default; when enabled, it records salted query fingerprints unless the operator separately opts into query text. The ledger’s tenant label is fixed to `mcp` in this server setup and does not establish user authentication or tenant authorization.[[server]][[audit]][[sqlite-ledger]]

## Scope isolation

The read gate can scope a question that names one subject. The official README says multi-subject questions still match against the whole store. The repository is organized as a local substrate, not a demonstrated multi-user service; no cross-tenant authorization boundary or isolation workload was verified in this review.[[read-gate]][[readme]][[server]]

## Provenance and evidence

A receipt proves that the stored evidence quote occupies the recorded byte range in a source with the recorded hash, and verification can detect source changes. The system computes the source hash and byte length. It records source origin, origin kind, supplier, validator, and ingest clock from caller input, so those assertions are not independently attested. The claim-to-evidence gate supports faithful storage but does not prove source authenticity or truth.[[receipts]][[provenance]][[firewall]][[spec]]

## Efficiency and observability

The local JSON snapshot is rewritten after mutations, while SQLite uses WAL and synchronous FULL commits for the event ledger. Graph indexes support entity-linked retrieval; the read path caps displayed matches. These are implementation properties, not measured latency or throughput. `memory_stats` reports counts and whether semantic matching is available. Optional read auditing records decision metadata and a salted fingerprint by default; failed best-effort audit writes do not fail retrieval.[[server]][[graph]][[sqlite-ledger]][[audit]]

The server itself uses no model. The optional extractor and semantic encoder are separate resource paths, so their token, compute, and storage costs are not represented by this source inspection. No efficiency measurements were collected.[[readme]][[metrics]][[status]]

## Metric-domain evidence

All project benchmark domains remain unmeasured for this review. The README reports 4.8% refusal for familiar tuned phrasings and 99.2% for unseen phrasings, reports 96.1% refusal accuracy on absent-answer traps, and says an earlier 98.4% recall claim was withdrawn. The README states that its evaluation corpus and method are private; these are upstream-reported figures and were not independently reproduced.[[readme]]

| Domain | Source evidence | Measurement status |
| --- | --- | --- |
| Answerable recall and abstention | The README reports retrieval/abstention figures; source review did not score answerable cases. | Unmeasured here |
| Correction and stale values | Supersession and disputed-state paths exist; no correction probes were run. | Unmeasured |
| Deletion leakage | The code implements closure erasure and probes; no deletion workload or backup audit was run. | Unmeasured |
| Scope isolation | Single-subject scope is described; multi-subject scope is a documented limitation. | Unmeasured |
| Evidence support and citation coverage | A deterministic claim-to-quote gate and byte receipts exist; no answer-level citations were adjudicated. | Unmeasured |
| Retrieval latency and write-to-recall delay | No timings were collected. | Unmeasured |
| Tokens, cost, and storage | No resource workload was measured. | Unmeasured |

See the [project metric definitions](../METRICS.md), [benchmark fixture](../fixtures/memory-benchmark-v1.json), and [execution status](../results/initial-baselines-status.json); these define the project protocol and run status, not Fireweed measurements.[[metrics]][[fixture]][[status]]

## Limits and unknowns

This is a bounded inspection of the official README, the current server, graph, pipeline, retrieval, provenance, ledger and erasure modules, and the open-format specification at the verified SHA. The write checks establish a relation between a proposal and cited text; they do not establish that the source is authentic or that a real-world claim is true. The README’s evaluation corpus is not public, and its reported scores were not reproduced.[[readme]][[firewall]][[provenance]][[repo]]

The source code describes safeguards around keys, erasure certificates, and source redaction, but this review did not test restore behavior, concurrent use, host backups, filesystem permissions, or adversarial access. Default HMAC certificates are shared-secret checksums rather than third-party signatures; Ed25519 is optional. Key separation does not protect against an attacker who controls the whole home directory. The open snapshot reader improves portability, while the project’s own spec separates that open format from the adjudication engine.[[server]][[crypto]][[erasure]][[spec]]

## Benchmark status

**Benchmark not run.** No Fireweed runtime, tests, or benchmark workload was executed. No project metric value is claimed. The README’s reported figures remain upstream-reported; the local [benchmark fixture](../fixtures/memory-benchmark-v1.json), [metric definitions](../METRICS.md), and [execution status record](../results/initial-baselines-status.json) are not results for Fireweed.[[fixture]][[metrics]][[status]][[readme]]

## Contact

The official pinned README publishes sanyamsood2@gmail.com for commercial-use inquiries. The structured review records that address and the exact checked source URL; no commit/profile metadata or third-party directory was used.[[readme]]

## Sources

All upstream file citations are pinned to the reviewed full SHA. The Atlas citation is used solely for curated roster attribution. See the structured record [fireweed-mcp.json](../data/system-reviews/fireweed-mcp.json) and [curated roster](../data/memory-systems.json).
