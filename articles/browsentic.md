# Browsentic source review

## Identity and review pin

- **Curated ordinal:** 104
- **Listed name / slug:** Browsentic / `browsentic`
- **Listed repository locator:** https://github.com/imshaikot/browsentic
- **Canonical repository:** https://github.com/imshaikot/browsentic
- **Default branch:** `main`
- **Reviewed head:** [`9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632`](https://github.com/imshaikot/browsentic/commit/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632)
- **Reviewed at:** 2026-11-25 00:13:22 UTC (2026-11-24 16:13:22 PST; America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The curated roster establishes the ordinal, name, slug, listed repository, and Atlas attribution only. Its descriptions and capability marks were not assessment evidence.[[roster](../data/memory-systems.json)][[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/browsentic.md)] A fresh read-only remote check identified `refs/heads/main` as HEAD at the reviewed full SHA; a shallow checkout of `main` resolved to the same commit.[[repository](https://github.com/imshaikot/browsentic)][[head](https://github.com/imshaikot/browsentic/commit/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632)]

## Summary

Browsentic is a local browser-agent harness with several distinct forms of persistent context: a user profile, site-specific notes or generated maps, and user-recorded browsing workflows. The selected source shows file-backed site maps, an extension-local recording store, and a local profile file; these paths do not form one shared memory database.[[README](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/README.md)][[site map guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/site-maps.md)][[recording guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/recordings.md)]

## Who and what

The README describes Browsentic as a browser harness for local agent command-line tools, with an extension and a local Bridge. It supports using the user's logged-in browser and offers an optional MCP endpoint. The reviewed repository is an application and browser extension with context features, rather than a standalone memory service. The README identifies the project as built by Imshaik but provides no contact email; no additional maintainer identity is inferred.[[README](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/README.md)]

## Architecture and data model

**Code observation — user profile.** The profile is a JSON object with typed contact fields, up to 20 labeled details, and standing instructions capped at 4,000 characters. The daemon stores it as `profile.json` with mode 0600 under its local state directory; an empty profile removes the file. It is read fresh for side-panel and scheduled runs and added to the prompt, but is not supplied to site mapping or MCP-client runs.[[profile model](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/settings/profile.ts)][[profile storage](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/profile.ts)][[profile guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/profile.md)]

**Code observation — site notes and maps.** Skills are Markdown files loaded from bundled, user, and uploaded directories. Site-exploration skills carry domain metadata and authored/generated provenance. A generated map is staged as `SKILL.md`, `map.json`, `meta.json`, page notes, screenshots, and captured sitemap evidence. The report includes a summary, landmarks, pages, links, and quirks; the rendered Markdown marks it as machine generated and records a generation timestamp.[[skill loader and router](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/skills.ts)][[map staging](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/site-map-store.ts)][[map report contract](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/skills/site-map.ts)]

**Code observation — recordings.** The extension's `browser.storage.local` keeps a metadata index and separate recording bodies containing timestamped browsing events and, after analysis, a normalized workflow. Metadata includes host, start URL, capture choice, event/step counts, status, duration, and created/updated times. This is browser-extension storage, separate from the Bridge's files.[[recording store](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/bridge/recording-store.ts)][[recorded event model](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/recordings/events.ts)][[workflow model and validation](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/recordings/workflow.ts)]

## Write, update, delete, and retrieval

**Profile — code observation.** Saving normalizes and writes the whole profile; clearing its fields removes the file. Side-panel and scheduled runs receive profile and standing-instruction prompt sections. MCP clients, site-mapping runs, file analysis, and conversation titles do not.[[profile storage](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/profile.ts)][[profile guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/profile.md)][[prompt assembly](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/prompt.ts)]

**Site maps — code observation.** A user explicitly starts mapping. The mapper reads robots/sitemap documents and explores pages; report validation scrubs text, restricts paths to the mapped origin, deduplicates pages, and caps fields and list sizes. Generated output stays in a staging directory until the user activates it. Activation renames it into the uploaded-skill directory; replacement moves the old directory into staging. The user can discard staged work, delete an active site map, or let the staging sweep remove abandoned drafts after 24 hours. Hand-authored skills can also be uploaded and removed.[[site map guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/site-maps.md)][[site map reader](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/sitemap.ts)][[report validation](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/skills/site-map.ts)][[staging lifecycle](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/site-map-store.ts)][[skill deletion](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/skill-store.ts)]

**Recordings — code observation.** Recording begins only after the user's action, follows one tab, and stops on tab close or after 15 minutes. Captured form values default to placeholders; passwords, hidden fields, one-time codes, and card-like values are filtered. Analysis turns the trace into a bounded workflow. Replaying rechecks targets against the live page and retains the normal approval gate for consequential actions. The extension keeps at most 20 recordings, dropping the oldest body as entries exceed the cap; each can be renamed or removed. Profile editing and site-map deletion do not delete recordings because they occupy a separate store.[[recording guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/recordings.md)][[event capture limits and redaction](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/recordings/events.ts)][[recording store](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/bridge/recording-store.ts)][[workflow checks](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/recordings/workflow.ts)][[recording guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/recordings.md)]

**Retrieval and scope — code observation.** At run time, the active page's host selects matching site notes; the longest matching domain takes priority, and explicit `@name` can attach a note elsewhere. Authored notes precede generated notes. The prompt builder includes them only while the full prompt remains within its 64 KiB cap and logs/drops entries that do not fit. Recordings are listed in a separate prompt section capped at 4 KiB, with an explicit note when some were omitted; the agent can then read a selected recording. Profile data is applied across local side-panel and scheduled runs. These are local context-selection rules, not evidence of multi-tenant isolation.[[skill routing](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/skills.ts)][[prompt limits and overlays](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/prompt.ts)][[recording context assembly](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/service.ts)]

**Provenance and evidence — code observation.** Site maps store the mapping run ID, generation time, host/domain, robots and sitemap evidence, screenshots, page paths and report metadata. Recording events retain timestamps and page URLs; generated workflows add ordered steps, variables and caveats, but this review found no cryptographic lineage or adjudication linking each generated step back to an event. Profile values are user-entered data without source citations or a validity history.[[staging metadata and evidence](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/site-map-store.ts)][[map index evidence](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/sitemap.ts)][[recorded event model](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/recordings/events.ts)][[workflow model](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/recordings/workflow.ts)][[profile model](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/settings/profile.ts)]

**Source-visible efficiency and observability.** The sitemap fetcher bounds remote documents to 20, each document to 4 MiB, aggregate bytes to 16 MiB, URLs to 5,000 and retained paths to 200; requests have a 10-second timeout, at most two redirects, and are restricted to the pinned origin. Mapping defaults are 15 pages, 10 screenshots, and 10 minutes, with configured ceilings of 40 pages, 24 screenshots, and 30 minutes. Recording buffers flush every second or 20 events, with at most 2,000 events and a 15-minute duration. Prompt composition has 64 KiB overall and 4 KiB for recording summaries. Logs report map activation/discard/sweeps and prompt omissions. These are code-visible limits and logs, not measured throughput or latency.[[sitemap bounds](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/sitemap.ts)][[mapping configuration](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/config.ts)][[recording limits](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/recordings/events.ts)][[prompt limits](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/prompt.ts)][[staging logs](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/site-map-store.ts)]

## Metric-domain evidence

The source review identifies relevant implementation paths but does not produce performance or quality results. All metric domains remain unmeasured for Browsentic.

| Domain | Source observation | Measurement |
|---|---|---|
| Answerable recall and abstention | Host-selected notes, user profile, and recording lookup are visible. | No answerable or unanswerable probes run. |
| Correction accuracy and staleness | Users can edit profile fields and replace site maps; no fact-level validity history was inspected. | No correction adjudication run. |
| Deletion leakage | Profile clearing, map deletion, and recording removal each exist in separate stores. | No cross-store deletion or post-delete retrieval probes run. |
| Scope isolation | Domain matching and local profile distribution are source-visible. | No cross-browser, cross-agent, or cross-principal isolation probes run. |
| Evidence support and citation coverage | Maps retain evidence files; recordings retain events and workflow structure. | No generated-note or workflow evidence adjudication run. |
| Retrieval latency and write-to-recall delay | Prompt construction and bounded sitemap/recording paths are visible. | No runtime timings gathered. |
| Tokens and cost | Prompt byte limits and provider execution are visible. | No token or provider-cost measurements gathered. |
| Storage efficiency | Profile JSON, map directories, and browser local storage are source-visible. | No stored bytes-per-item measurement gathered. |

See the project's [metric definitions](../METRICS.md), [benchmark status record](../results/initial-baselines-status.json), and [fixture/protocol](../fixtures/memory-benchmark-v1.json). These define measurement domains and protocol; they are not Browsentic results.[[metrics](../METRICS.md)][[status](../results/initial-baselines-status.json)][[fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded code review of selected files at one verified revision. Browsentic, its workflows, and its tests were not run. It cannot establish the quality or freshness of generated maps, whether redaction catches every sensitive value, actual browser-storage retention behavior across browser versions, or operational latency and cost. The selected sources show local host/domain filtering and extension storage, not a general tenant authorization boundary. Profile, generated-map, and recording lifecycle paths are separate, so deletion in one does not establish deletion across all context stores.[[head](https://github.com/imshaikot/browsentic/commit/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632)][[profile guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/profile.md)][[site map guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/site-maps.md)][[recording guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/recordings.md)]

## Benchmark status

**Benchmark not run.** No Browsentic runtime, benchmark workload, or tests were run for this review. The project metric definitions and fixture describe protocol; the execution-status record reports `not_run` and contains no measured values.[[metrics](../METRICS.md)][[benchmark status](../results/initial-baselines-status.json)][[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Official repository and default branch](https://github.com/imshaikot/browsentic)
- [Reviewed full head commit](https://github.com/imshaikot/browsentic/commit/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632)
- [Official README](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/README.md)
- [Official SECURITY.md](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/SECURITY.md)
- [Site maps guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/site-maps.md)
- [Recordings guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/recordings.md)
- [Profile guide](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/docs/guide/features/profile.md)
- [Site-map store](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/site-map-store.ts)
- [Site-map report contract](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/skills/site-map.ts)
- [Sitemap fetcher](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/sitemap.ts)
- [Skill loader and domain router](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/skills.ts)
- [Skill add/delete operations](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/skill-store.ts)
- [Prompt assembly](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/prompt.ts)
- [Agent service recording context](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/agent/service.ts)
- [Profile schema](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/settings/profile.ts)
- [Profile persistence](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/daemon/profile.ts)
- [Recording storage](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/bridge/recording-store.ts)
- [Recorded event model](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/recordings/events.ts)
- [Recording workflow validation](https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/src/lib/recordings/workflow.ts)
- [Curated ordinal and identity](../data/memory-systems.json)
- [Atlas attribution source](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/browsentic.md)
- [Metric definitions](../METRICS.md)
- [Benchmark status record](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)

## Contact-list follow-up

The official pinned [README](<https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/README.md>) and [SECURITY.md](<https://github.com/imshaikot/browsentic/blob/9c0892a457e86cf2a5c3d1f4a8eea7eeb0900632/SECURITY.md>) were checked for a published contact email. The README lists GitHub issues and contributing guidance, while SECURITY.md directs vulnerability reports to GitHub security advisories; neither publishes an email. The JSON records `contact_email: null` and the pinned README as the checked contact source.

**Verification boundary:** no Browsentic runtime, benchmark, or tests were run.
