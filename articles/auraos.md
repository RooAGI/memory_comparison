# AuraOS source review

**Review status:** Reviewed from code  
**Benchmark status:** Benchmark not run  
**Roster ordinal / name / slug:** 78 / AuraOS / auraos  
**Listed repository locator:** [AdultSwimmer/AuraOS](https://github.com/AdultSwimmer/AuraOS)  
**Current canonical repository:** [AdultSwimmer/AuraOS](https://github.com/AdultSwimmer/AuraOS)  
**Default branch / reviewed head:** main / 8c96c48b5785b52ef4292110e41f0c254ec22a7d  
**Review time:** 2026-11-24 22:00:20 UTC (14:00:20 PST; America/Los_Angeles).

## Identity and review pin

The curated roster places AuraOS at ordinal 78 and lists the repository locator above. Its Atlas entry is retained for identity and attribution only; Atlas descriptions, marks, and layout were not used as assessment evidence. GitHub identifies `main` as the default branch. The official main commit feed reports full head `8c96c48b5785b52ef4292110e41f0c254ec22a7d`, matching the repository page’s latest commit prefix. This review is pinned to that head, not the older roster revision `81dffa9ba95334b3ded57f9237750372ab80815d`. [[curated roster](../data/memory-systems.json)] [[official repository](https://github.com/AdultSwimmer/AuraOS)] [[main commit feed](https://github.com/AdultSwimmer/AuraOS/commits/main.atom)] [[reviewed commit](https://github.com/AdultSwimmer/AuraOS/commit/8c96c48b5785b52ef4292110e41f0c254ec22a7d)]

## Summary

AuraOS is a small Flask chat application that combines a local text-file identity, a per-user text transcript, and the current message into a prompt sent to Ollama. The inspected route uses the full transcript for each request and appends both turns after a successful model response. The README describes the intended system as local-first and user-owned; the inspected server implementation instead creates and reads histories beneath its own project directory. This is a source review, not a runtime or benchmark result. [[README.md](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/README.md)] [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)]

## Who and what

The repository is published under the GitHub account AdultSwimmer. The README calls AuraOS an early prototype and describes it as a local-first personal AI continuity system. In the inspected implementation it is a Flask web application serving a static frontend, with Ollama as the model endpoint. The repository does not establish a maintainer’s personal identity in the sources reviewed. [[official repository](https://github.com/AdultSwimmer/AuraOS)] [[README.md](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/README.md)] [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)]

## Architecture and data model

**Code observation.** At startup, `server/main.py` resolves the repository root, creates a `histories/` directory, and loads all nonempty `.txt` and `.md` files in `core/` in sorted filename order. Their full contents are combined into one permanent identity string and held in `CORE_MEMORY`. The source comments and README describe this as identity included in each prompt. [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)] [[README.md](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/README.md)]

**Code observation.** A history is plain text at `histories/{user_id}.txt`. Each appended turn has an ISO-formatted UTC timestamp, an uppercased role label, the text, and blank-line separators. The file is read as a whole; no separate records, index, database, or retrieval ranking appear in this route. [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)]

**Documentation/code distinction.** The README describes a portable, user-held `HISTORY.txt` whose contents are not stored on the server. The reviewed server code instead creates a project-local `histories/` directory and accesses a file named from the request’s `user_id`. This bounded review does not establish whether another client or deployment path implements the user-held-file model. [[README.md](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/README.md)] [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)]

## Write, update, delete, and retrieval

**Write and retrieval.** The `POST /chat` route reads `message` and `user_id` from JSON, defaulting the latter to `default`, and rejects an empty message. It loads the selected history in full and builds a prompt containing the startup-loaded core identity, the entire history (or a no-history marker), and the current message. It posts this prompt to the configured Ollama generation endpoint with streaming disabled and a 120-second timeout. After a successful response, it appends the user message and Aura reply as separate timestamped turns. A failed model request returns an error before either turn is appended. [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)]

**Scope and isolation.** The file name is derived directly from request-supplied `user_id`; the inspected route shows no authentication, authorization, or identifier/path validation. The implementation therefore does not demonstrate that a caller may access only their own transcript. The shared core identity is loaded once for all requests. This is a code-level scope observation, not a tested exploit or deployment assessment. [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)]

**Update and delete.** No history correction, update, or delete endpoint was found in the inspected server module. The transcript is an append-only sequence through this route; operators could edit local files outside the API, but the reviewed sources do not describe a managed correction or deletion contract, nor cleanup of backups or derived copies. [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)] [[README.md](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/README.md)]

## Metric-domain evidence

**Code observations, not measurements.** Retrieval is a full-file read followed by prompt concatenation. The inspected code shows no search, ranking, token-budget truncation, summarization, or history cutoff. Writes append two text blocks after a successful model call. These structures imply that history input and prompt size can grow with transcript length, but no latency, throughput, token, or storage measurement was made. [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)]

The transcript records timestamp and role, which preserve basic turn-level origin and ordering. The route adds no source citations, evidence links, confidence, fact-level provenance, or correction history. The `/health` route exposes status, configured model name, and whether core text loaded; startup prints the model and core character count. No retrieval-quality telemetry or durable operation audit is visible in the inspected module. [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)]

| Domain | Source-visible evidence | Review measurement |
|---|---|---|
| Answerable recall and abstention | Whole transcript is placed in the prompt; no retrieval evaluation or abstention mechanism is shown in the inspected route | Unmeasured |
| Correction and stale values | The route appends turns and exposes no correction/supersession operation | Unmeasured |
| Deletion leakage | No API deletion path or cross-copy cleanup was found in the inspected module | Unmeasured |
| Scope isolation | A request field selects the history path; the route shows no caller authentication or ownership check | Unmeasured |
| Evidence support and citations | Timestamp and role are stored; source support or citation checking is not shown | Unmeasured |
| Latency and write-to-recall delay | A 120-second model-call timeout is configured; no timing workload was run | Unmeasured |
| Tokens, cost, and storage | Full core and transcript strings enter the prompt; no token/cost/storage measurement was made | Unmeasured |

The project’s metric definitions and benchmark status record describe the comparison protocol, not AuraOS results. [[metric definitions](../METRICS.md)] [[benchmark status record](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This review inspected the current README and the 131-line `server/main.py` implementation. It did not inspect every frontend, launcher, or experimental file, execute the service, or verify how deployed environments handle identity, history portability, concurrency, or backups. The source inspection does not establish actual recall quality, safe multi-user isolation, deletion completeness, response latency, token use, or operating cost. [[README.md](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/README.md)] [[server/main.py](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)]

## Benchmark status

**Benchmark not run.** No AuraOS runtime, benchmark workload, or tests were run for this review. The shared fixture, metric definitions, and execution-status record are protocol artifacts, not measurements. [[metric definitions](../METRICS.md)] [[benchmark status record](../results/initial-baselines-status.json)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Current canonical repository](https://github.com/AdultSwimmer/AuraOS)
- [Current main commits feed](https://github.com/AdultSwimmer/AuraOS/commits/main.atom)
- [Reviewed full head commit](https://github.com/AdultSwimmer/AuraOS/commit/8c96c48b5785b52ef4292110e41f0c254ec22a7d)
- [README.md at reviewed head](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/README.md)
- [server/main.py at reviewed head](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/server/main.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark status record](../results/initial-baselines-status.json)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Curated roster locator and source attribution](../data/memory-systems.json)

## Contact-list follow-up

The official pinned README was checked for a published contact email and does not publish one. The official pinned `SECURITY.md` URL returned “File not found.” The record therefore stores `contact_email: null` and both checked source URLs. [[README.md](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/README.md)] [[SECURITY.md](https://github.com/AdultSwimmer/AuraOS/blob/8c96c48b5785b52ef4292110e41f0c254ec22a7d/SECURITY.md)]
