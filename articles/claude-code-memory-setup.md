# claude-code-memory-setup — source review

**Review status:** Reviewed from code at the verified upstream head  
**Benchmark status:** Benchmark not run  
**Roster position:** Ordinal 123 — claude-code-memory-setup / `claude-code-memory-setup`  
**Listed repository:** [lucasrosati/claude-code-memory-setup](https://github.com/lucasrosati/claude-code-memory-setup)  
**Canonical upstream:** same repository; default branch `main`; reviewed head `4cd2e6bd4319fcb2e8d24c2407a864516e7c133a`  
**Review time:** 2026-11-25 08:04:10 UTC (2026-11-25 00:04:10 PST; America/Los_Angeles)

## Identity and scope

The local roster identifies this entry at ordinal 123, with the explicit listed repository above. Its pinned Atlas source is retained only as roster attribution for identity and locator context; Atlas descriptions and assessments are not evidence for this review.[[catalog](../data/memory-systems.json)] [[Atlas roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/claude-code-memory-setup.md)]

GitHub identifies the public repository and its default branch as `main`. The current main commit history and its official patch identify the reviewed full head SHA `4cd2e6bd4319fcb2e8d24c2407a864516e7c133a`; the patch records the commit date as 2026-10-20 21:15:44 -0700.[[repository](https://github.com/lucasrosati/claude-code-memory-setup)] [[reviewed head](https://github.com/lucasrosati/claude-code-memory-setup/commit/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a)]

The repository is a guide and set of scripts and command files for Claude Code with an Obsidian vault. It also describes Graphify as a separate code graph tool. It is not a hosted memory service, and this review does not inspect the external Obsidian or Graphify implementation.[[README](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/README.md)]

## Architecture and data model

**Code observation.** The repository combines free-form vault Markdown, a chat-export processor, slash-command instructions, and a SessionEnd hook. Imported chat notes receive YAML fields for title, tags, source, origin, created date, processed time, status, and type. Origin is inferred from path or content markers; tags are keyword matches; the created date comes from the source file's modification time. Session-end logs include a transcript-derived first prompt, file paths, command samples, and timestamps.[[importer](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/claude_to_obsidian.py)] [[auto-save hook](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/session_autosave.py)]

The guide recommends a central Obsidian vault with project folders, permanent notes, logs, chat imports, and graph output. The commands describe Markdown destinations for durable decisions, reusable insights, facts, and conventions. These are vault conventions and agent instructions rather than a validated record schema enforced by a memory service.[[README](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/README.md)] [[/save command](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/commands/save.md)]

## Write, update, delete, and retrieval

**Write — code observation.** The chat processor recursively scans Markdown exports, derives frontmatter and tags, optionally inserts wikilinks, and writes files under `chats/code` or `chats/web`. The SessionEnd hook parses the Claude transcript JSONL locally and writes a mechanical log after filtering sessions with fewer than two user messages. Separately, `/save` instructs the model to write a richer session log and conditionally consolidate durable knowledge.[[importer](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/claude_to_obsidian.py)] [[auto-save hook](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/session_autosave.py)] [[/save command](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/commands/save.md)]

**Update and correction — documented workflow.** The `/save` instructions tell the model to search for duplicates, update an equivalent note, and record corrections to outdated memory. This is a prompt-level procedure, not a transactional correction log or a source-enforced guarantee that a corrected fact will replace every old copy.[[/save command](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/commands/save.md)]

**Delete and overwrite — code observation.** The importer writes to a destination derived from origin and filename, so another import with the same destination can replace the existing Markdown file. Its optional `--move` flag removes the input export after processing. The README says not to delete vault notes without asking; the reviewed repository does not provide a general memory deletion API or establish physical erasure from backups and copies.[[importer](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/claude_to_obsidian.py)] [[README](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/README.md)]

**Retrieval — documented workflow.** The `/resume` procedure reads recent logs and project decisions; the guide also points the agent to vault notes and Graphify output, while Obsidian supplies its own search and graph view. The importer adds a wikilink on the first name match outside code blocks. The repository does not implement a ranked retrieval API, answerability check, or retrieval-quality evaluation.[[/save command](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/commands/save.md)] [[README](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/README.md)] [[importer](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/claude_to_obsidian.py)]

## Scope isolation

The importer separates imported chats by inferred origin (`code` or `web`). The auto-save hook places logs in a project folder selected from the working-directory basename when that folder exists in the vault; otherwise it uses a vault-wide logs directory. These are organizational and routing rules. No authenticated project/user boundary or cross-scope isolation guarantee was established by the inspected source.[[importer](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/claude_to_obsidian.py)] [[auto-save hook](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/session_autosave.py)] [[/save command](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/commands/save.md)]

## Provenance and evidence

Imported chat notes include source and origin labels, a file-derived creation date, and processing time. Auto-logs preserve selected transcript facts, including the first user prompt, touched paths, sampled commands, and timestamps. The reviewed code does not validate those facts against an external source or provide claim-level evidence citations for downstream answers.[[importer](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/claude_to_obsidian.py)] [[auto-save hook](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/session_autosave.py)]

## Efficiency and observability

**Code observation.** The importer can run in dry-run mode, limits wikilink insertion to one matching occurrence per vault note, and skips code spans and fences. The SessionEnd hook parses local JSONL without an LLM call, limits file/command samples, applies a minimum-message filter, and appends errors/status to a local log. These are implementation choices, not measured performance.[[importer](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/claude_to_obsidian.py)] [[auto-save hook](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/session_autosave.py)]

The README labels its historical token reduction figures author-reported and says the underlying source snapshot, prompts, tokenizer, and usage logs are not published; the figures therefore are not reproducible results for this review. No latency, token, cost, or storage measurements were collected.[[README](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/README.md)]

## Contact

The official pinned README was checked and does not publish a contact email. The record stores `contact_email: null` with that exact checked URL.[[README](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/README.md)]

## Metric-domain evidence

All project benchmark domains remain unmeasured: answerable retrieval and abstention; correction/staleness; deletion leakage; scope isolation; evidence support and citation coverage; latency and write-to-recall delay; tokens, cost, and storage efficiency. The project metric definitions and fixture describe evaluation plans, and the execution record is not evidence of system results.[[metric definitions](../METRICS.md)] [[benchmark fixture](../fixtures/memory-benchmark-v1.json)] [[execution status](../results/initial-baselines-status.json)]

## Limits and unknowns

This is a read-only source review at the verified current main head. No setup instructions, scripts, tests, or benchmark workload were run. Source inspection cannot establish successful installation, correct memory consolidation, recall quality, complete deletion, cross-project isolation, latency, cost, or end-to-end token savings. The vault’s access controls and behavior depend on the user's filesystem, Obsidian setup, and agent environment.

## Sources

- [Roster entry and ordinal](../data/memory-systems.json)
- [Atlas roster attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/claude-code-memory-setup.md)
- [Official repository and default branch](https://github.com/lucasrosati/claude-code-memory-setup)
- [Reviewed full head](https://github.com/lucasrosati/claude-code-memory-setup/commit/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a)
- [README.md](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/README.md)
- [scripts/claude_to_obsidian.py](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/claude_to_obsidian.py)
- [scripts/session_autosave.py](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/scripts/session_autosave.py)
- [commands/save.md](https://github.com/lucasrosati/claude-code-memory-setup/blob/4cd2e6bd4319fcb2e8d24c2407a864516e7c133a/commands/save.md)
- [Project metric definitions](../METRICS.md)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Benchmark execution status](../results/initial-baselines-status.json)

**Verification boundary:** no system runtime, tests, or benchmarks were run for this review.
