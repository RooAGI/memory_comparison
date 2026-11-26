# distill-kura source review

**Review status:** Reviewed from code  
**Benchmark status:** Not run  
**Roster ordinal / name / slug:** 192 / distill-kura / `distill-kura`  
**Listed repository locator:** `https://github.com/lna-lab/distill-kura` (explicit)  
**Catalog attribution:** [Pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/distill-kura.md), used only for identity and locator attribution  
**Canonical repository / default branch:** [lna-lab/distill-kura](https://github.com/lna-lab/distill-kura) / `master`  
**Reviewed head:** [`3a02c04e5155cd66d49cfd95d11b09239499c97d`](https://github.com/lna-lab/distill-kura/commit/3a02c04e5155cd66d49cfd95d11b09239499c97d); official master history agrees  
**Review time:** 2026-11-25 11:13:14 UTC (2026-11-25 03:13:14 PST; America/Los_Angeles)  
**Published contact:** No email found in the [official README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md).

## Identity and scope

The catalog places distill-kura at ordinal 192, uses slug `distill-kura`, and lists the explicit repository locator above. The pinned Atlas report is retained only for roster attribution; the assessment below is based on official upstream documentation and source at the reviewed revision.[[catalog entry](../data/memory-systems.json)] [[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/distill-kura.md)]

GitHub identifies `master` as the default branch. Its official master Atom feed reports full head `3a02c04e5155cd66d49cfd95d11b09239499c97d`, updated 2026-09-30T10:40:08Z. The repository and commit pages corroborate the upstream identity and reviewed revision.[[repository](https://github.com/lna-lab/distill-kura)] [[master history](https://github.com/lna-lab/distill-kura/commits/master.atom)] [[reviewed head](https://github.com/lna-lab/distill-kura/commit/3a02c04e5155cd66d49cfd95d11b09239499c97d)]

## Summary

distill-kura is a local-first, file-based long-term memory package for agents. It stores one Markdown file per memory and a recognition-oriented index, gates transcript distillation with deterministic evidence checks, and retrieves relevant memories through a direct-match fast path or model-assisted selection followed by link walking.[[README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md)] [[store](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/store.py)] [[recall](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/recall.py)]

The project describes a Python library, CLI, HTTP service, MCP bridge, and DeepSeek Harness plugin. Its README says it uses the Python standard library and does not require embeddings or a vector database. The README also publishes example and project-specific measured figures; this review did not reproduce them, and they are not benchmark results for this project.[[README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md)]

## Who and what

The reviewed repository presents distill-kura as an agent memory system implemented as a Python package, with several host integration routes. The repository's code and documentation were inspected; no maintainer identity is asserted here beyond the repository namespace.[[README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md)] [[repository](https://github.com/lna-lab/distill-kura)]

## Architecture and data model

A store is a directory containing `MEMORY.md`, one Markdown file per memory, optional long-form notes, and an `_still/` work area for drafts, watermarks, read logs, write-ahead records, and revision state. Memory files use frontmatter for a name/description/type and optional tags and curation annotations; their prose body carries a fact and its rationale or application guidance. The index contains one recognition trigger per memory and can link related slugs.[[store](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/store.py)] [[README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md)]

The distillation pipeline separates journal intake, candidate generation, deterministic evidence checks, novelty handling, composition, draft staging, and later draft review. A draft is not yet a canonical memory: the scribe re-reads it and chooses to pour, fix, or toss it. Evidence manifests and signed envelopes support validation before a draft is written into the store.[[pipeline](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/pipeline.py)] [[gate](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/gate.py)]

The design has no vector database or embedding store. Recall's direct-match fast path can answer without a thinker call; otherwise the configured thinker selects relevant index entries by meaning, then the store walks their links and returns bounded context.[[README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md)] [[recall](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/recall.py)]

## Write, update, delete, and retrieval

**Write.** Journal adapters classify input segments as USER, TOOL, ACT, or SELF. Candidate quotes must occur in the corresponding raw material; echoes already present in the store are suppressed. A SELF-only candidate must be marked as a judgement, and unsupported numbers or attribution are rejected by deterministic checks. Later model-written prose is checked again for unsupported numbers, human attribution, broken memory links, and invented quotations.[[pipeline](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/pipeline.py)] [[gate](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/gate.py)]

Accepted candidates are composed into signed drafts. The later pour step re-reads each draft without its earlier context and decides whether to pour, fix, or toss it. Failed work is kept pending for retry instead of being treated as a successful empty batch. A separate direct-write policy controls whether host tools and CLI calls can write or annotate memories.[[pipeline](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/pipeline.py)] [[trust](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/docs/TRUST.md)] [[README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md)]

**Update and correction.** Annotation merges tags and curation text into an existing memory. A dedicated retirement operation can mark an old memory as superseded and name a successor. It requires a verified evidence manifest with one USER-class quote that names the old memory, states a replacement/retirement construction, and names the successor. The old memory remains in the store; retirement is not erasure.[[store](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/store.py)] [[transition verifier](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/transition.py)] [[trust](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/docs/TRUST.md)]

**Delete.** The inspected API and documentation do not define a general memory deletion or secure-erasure operation. Retirement changes the index face but leaves the old Markdown memory present. The checked sources do not establish how deletion propagates through backups, filesystem history, or hosted model retention.[[store](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/store.py)] [[README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md)] [[trust](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/docs/TRUST.md)]

**Retrieval.** A deterministic fast path tries direct recognition and returns only gated hits. Otherwise the thinker receives the full recognition index and names relevant slugs by meaning; the store then follows memory links. Per-memory and whole-context character limits bound the returned context. If the thinker is unavailable, recall falls back to word overlap and labels that degraded path. An explicit empty selection from the thinker is preserved as no match rather than replaced with word-overlap guesses.[[recall](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/recall.py)]

## Scope isolation

Each store is a separate directory, and a mode or host configuration selects the store before a conversation. The trust guide describes directory and mode separation as routing rather than authorization: the HTTP service has no authentication. It recommends separating users/processes and their filesystem permissions, warns about shared journal roots and shared model endpoints, and notes that hardlinks can expose content even when symlinks are excluded.[[trust](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/docs/TRUST.md)] [[README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md)]

## Provenance and evidence

The evidence gate establishes that candidate quotes occur in classified source material, suppresses store echoes, and restricts the kind of claim allowed by each evidence class. A manifest records evidence references, and the transition verifier requires direct human wording for a supersession and its successor.[[gate](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/gate.py)] [[pipeline](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/pipeline.py)] [[transition verifier](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/transition.py)]

This demonstrates traceability to source text and its assigned class, not that the source is true or complete. Correctness also depends on journal adapters classifying material properly. The trust guide says the adjacent local gate key and manifest boundary protects against tool-level mutation, not a principal with filesystem access.[[gate](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/gate.py)] [[pipeline](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/pipeline.py)] [[trust](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/docs/TRUST.md)]

## Efficiency and observability

The design avoids embedding generation and vector lookup infrastructure. Direct recognition can avoid a model call, while semantic selection sends the index to a model. These are source-visible design properties, not measurements made for this review.[[README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md)] [[recall](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/recall.py)]

Recall responses expose the method used, fastpath verdict and time, picked/walked/included memories, budget drops, estimated token count, and elapsed time. The README and store doctor describe distillation logs/metrics and health checks for links, manifests, index state, revision/WAL, curation, fastpath, and capacity. These provide inspection surfaces; no latency, token, cost, or storage samples were collected here.[[recall](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/recall.py)] [[store](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/store.py)] [[README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md)]

## Metric-domain evidence

| Domain | Review status | Evidence |
|---|---|---|
| Answerable retrieval accuracy and abstention | Unmeasured | Recall implements a fast path, meaning selection, and no-pick behavior; no project probes were run.[[recall](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/recall.py)] |
| Correction accuracy and stale-value rate | Unmeasured | A proven retirement transition exists; no correction probes were run.[[transition verifier](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/transition.py)] |
| Deletion leakage | Unmeasured | No general deletion route was established; no post-delete probes were run.[[store](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/store.py)] |
| Scope isolation leak rate | Unmeasured | Directory and mode boundaries are documented with limits; no cross-scope probes were run.[[trust](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/docs/TRUST.md)] |
| Evidence support precision and citation coverage | Unmeasured | The gate verifies quote occurrence and class rules; no claim adjudication was run.[[gate](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/gate.py)] |
| Retrieval latency | Unmeasured | Timing fields exist, but no timing samples were collected.[[recall](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/recall.py)] |
| Write-to-recall delay | Unmeasured | No acknowledged writes or scheduled recall probes were run.[[pipeline](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/pipeline.py)] |
| Tokens and cost | Unmeasured | Estimated context tokens are reported by source; provider usage and cost were not collected.[[recall](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/recall.py)] |
| Storage efficiency | Unmeasured | Doctor reports bytes and token estimates; no benchmark corpus footprint was measured.[[store](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/store.py)] |

These are the project's measurement domains, not distill-kura results. See [metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and the [planned fixture](../fixtures/memory-benchmark-v1.json).

## Contact

The official pinned [README](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/README.md) was checked for contact information and publishes no email. The JSON record stores `contact_email: null` and the exact checked URL. No commit/profile metadata or third-party directory was used.

## Limitations and unknowns

- The deterministic gate checks whether a quote appears in a source classified by the adapter; it cannot establish whether that source is truthful, complete, or correctly classified.[[gate](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/gate.py)] [[pipeline](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/distill/pipeline.py)]
- The meaning tier depends on the configured thinker, while degraded word overlap and the fast path serve different query shapes. The source review does not establish retrieval accuracy on an external workload.[[recall](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/recall.py)]
- Mode/store routing does not provide access control. An unauthenticated HTTP listener, shared models or journals, filesystem access, and hardlinks can cross intended boundaries.[[trust](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/docs/TRUST.md)]
- Retirement preserves old memory content. The reviewed sources do not establish hard deletion, backup erasure, or hosted-model retention behavior.[[store](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/distill_kura/store.py)] [[trust](https://github.com/lna-lab/distill-kura/blob/3a02c04e5155cd66d49cfd95d11b09239499c97d/docs/TRUST.md)]
- No distill-kura runtime, tests, or benchmark workloads were run. All project metric domains remain unmeasured.[[metric definitions](../METRICS.md)] [[execution status](../results/initial-baselines-status.json)]

## Benchmark status

**Benchmark not run.** No distill-kura runtime, tests, or benchmark workloads were executed. This source assessment is not a measured result. See [project metric definitions](../METRICS.md), [shared execution status](../results/initial-baselines-status.json), and [planned fixture](../fixtures/memory-benchmark-v1.json).

## Sources

Structured source IDs and pinned upstream URLs are in [distill-kura.json](../data/system-reviews/distill-kura.json). The [pinned Atlas roster entry](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/distill-kura.md) is included for curated identity and locator attribution only.
