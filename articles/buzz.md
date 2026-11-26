# Buzz source review

## Identity and review pin

- **Curated ordinal:** 105
- **Listed name / slug:** Buzz / `buzz`
- **Listed repository locator:** https://github.com/block/buzz
- **Canonical repository:** https://github.com/block/buzz
- **Default branch:** `main`
- **Reviewed head:** [`61c070d5915e11ef8f24b32d6f4f217132294320`](https://github.com/block/buzz/commit/61c070d5915e11ef8f24b32d6f4f217132294320)
- **Reviewed at:** 2026-11-25 00:35:23 UTC (2026-11-24 16:35:23 PST; America/Los_Angeles)
- **Status:** Reviewed from code
- **Benchmark status:** Benchmark not run

The curated roster establishes this ordinal, name, slug, listed repository, and Atlas attribution. Atlas descriptions and capability marks were not used as assessment evidence.[[roster](../data/memory-systems.json)][[Atlas attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/buzz.md)] The official repository page identifies `main` as the default branch and current commit prefix `61c070d`; its main feed identifies full head `61c070d5915e11ef8f24b32d6f4f217132294320` (updated 2026-11-25T00:33:09Z), independently confirmed with read-only `git ls-remote --symref`.[[repository](https://github.com/block/buzz)][[main feed](https://github.com/block/buzz/commits/main.atom)][[head](https://github.com/block/buzz/commit/61c070d5915e11ef8f24b32d6f4f217132294320)]

## Summary

Buzz is a self-hostable collaboration workspace built around a Nostr relay and signed event log. The memory-specific slice is the optional NIP-AE agent engram protocol: encrypted profile and memory records addressed to an agent-owner pair, surfaced through a CLI and injected core profile for ACP sessions. The inspected code and protocol describe implementation behavior; no runtime or benchmark was run.[[readme](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/README.md)][[nip-ae](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/docs/nips/NIP-AE.md)][[engram](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-core/src/engram.rs)]

## Who and what

The official README identifies Buzz as built by Block, Inc. and describes the repository as the relay and mobile client; it points to a separate repository for the desktop app. This review is about the agent memory feature in this large workspace application, not a standalone memory service.[[readme](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/README.md)]

## Architecture and data model

**Code and protocol observations.** NIP-AE defines kind 30174 addressable Nostr events. A `core` body holds a free-form agent profile; `mem/…` records hold one slug and a UTF-8 value (or null tombstone). The body is JSON, encrypted with NIP-44 v2 using the conversation key shared by the agent and owner. The event is signed by the agent key and carries public `d` and owner `p` tags; the slug itself is hidden in an HMAC-derived `d` tag.[[nip-ae](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/docs/nips/NIP-AE.md)][[engram](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-core/src/engram.rs)]

The core crate implements slug validation, HMAC addressing, NIP-44 encryption/decryption, event validation, and head selection as pure primitives; it does not itself perform relay or filesystem I/O. The `buzz mem` CLI supplies the relay transport and credentials. ACP has a separate fetcher for the `core` record at new-session creation.[[engram](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-core/src/engram.rs)][[mem-cli](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-cli/src/commands/mem.rs)][[acp-fetch](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-acp/src/engram_fetch.rs)]

## Write, update, delete, and retrieval

**Writes and updates — code/protocol observations.** CLI commands include `mem set`, `mem patch`, `mem get`, `mem hash`, `mem ls`, and `mem rm`. Writes select the current head, use a strictly increasing event timestamp, encrypt and sign a replacement event, and ask the relay whether it accepted the event; a dominated/duplicate event is surfaced as a conflict. Patch applies a unified diff against the current value using a SHA-256 compare-and-swap guard. The protocol describes post-publish head verification as recommended and best effort, not a global transaction across relays.[[mem-cli](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-cli/src/commands/mem.rs)][[nip-ae](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/docs/nips/NIP-AE.md)]

`mem rm` publishes an in-band null-value tombstone for a memory slug; the reserved `core` record cannot be removed through this command. NIP-09 deletion requests are optional and relay policy determines whether they remove prior events, so a tombstone does not establish erasure from archival relays. A later write may restore the slug.[[mem-cli](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-cli/src/commands/mem.rs)][[nip-ae](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/docs/nips/NIP-AE.md)]

**Retrieval — code/protocol observations.** CLI reads can run from the agent side or owner side. `mem ls` queries configured relays and selects the greatest valid head per slug; `get` and `hash` address a named slug. NIP-AE permits wiki links such as `[[mem/project]]`; core is the session bootstrap surface and can point to additional memories. Listing is best effort because Nostr has no protocol-level pagination and relays may cap results.[[mem-cli](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-cli/src/commands/mem.rs)][[nip-ae](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/docs/nips/NIP-AE.md)]

At ACP session creation, the fetcher queries at most 16 candidate core events. A valid decrypted core becomes a `<core-memory>` prompt section. A confirmed empty result produces an onboarding nudge; transport, parse, or unreadable-candidate errors are logged and inject no section, avoiding treating relay failure as absent memory. Session creation is not blocked by that fetch.[[acp-fetch](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-acp/src/engram_fetch.rs)]

## Scope isolation

The protocol addresses each memory by the agent-owner public-key pair. The `d` tag is an HMAC of the shared conversation key and slug, while relay authorization additionally checks filters that could match agent engrams: the authenticated reader must be the author or the addressed owner. The relay code documents an exception for explicit event-ID filters, which it treats as authorized when the caller already knows the event ID. These are protocol and code observations, not an isolation test result.[[nip-ae](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/docs/nips/NIP-AE.md)][[relay-request](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-relay/src/handlers/req.rs)]

## Provenance and evidence

NIP-44 encryption and event signatures establish confidentiality and which agent key authored an event; they do not establish that remembered content is true or how it was learned. The protocol suggests optional inline `source` and `added` metadata in profile/value text, but calls it the agent's own claim rather than verified attestation. Structured provenance and trust fields are outside this protocol version.[[nip-ae](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/docs/nips/NIP-AE.md)][[engram](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-core/src/engram.rs)]

## Source-visible efficiency and observability

The core rejects serialized bodies above the NIP-44 plaintext limit of 65,535 bytes and slugs over 255 bytes. The CLI validates candidate events and ignores malformed array entries during listing rather than allowing one malformed event to abort the whole list. ACP bounds its core query to 16 candidates and distinguishes errors from confirmed absence. These source-level bounds and logs are not measured throughput or latency.[[engram](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-core/src/engram.rs)][[mem-cli](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-cli/src/commands/mem.rs)][[acp-fetch](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-acp/src/engram_fetch.rs)]

## Metric-domain evidence

The source inspection identifies behaviors and evaluation paths, but this review produced no measured results. Each metric domain remains unmeasured.

| Domain | Source observation | Measurement |
| --- | --- | --- |
| Answerable recall and abstention | Named reads, listing, core injection, and confirmed-absence handling are source-visible. | No answerability probes run. |
| Correction accuracy and staleness | Patch uses a content hash guard and writes a replacement head. | No correction or stale-value adjudication run. |
| Deletion leakage | Memory tombstones exist; relay-level historical deletion depends on optional NIP-09 requests and relay behavior. | No post-delete or archival-relay probes run. |
| Scope isolation | Agent-owner addressing and relay read authorization are implemented. | No cross-owner or unauthorized-read workload run. |
| Evidence support and citation coverage | Event signatures identify an author; optional textual source metadata is not an attestation. | No evidence-support adjudication run. |
| Retrieval latency and write-to-recall delay | Relay query, decryption, head selection, and post-write verification paths are visible. | No runtime timings gathered. |
| Tokens and cost | ACP injects core text at session creation and has an explicit query candidate cap. | No token or provider-cost measurements gathered. |
| Storage efficiency | Encrypted, replaceable relay events store current heads; relay retention policies may differ. | No bytes-per-memory or relay-storage measurements gathered. |

See the project [metric definitions](../METRICS.md), [benchmark status record](../results/initial-baselines-status.json), and [fixture/protocol](../fixtures/memory-benchmark-v1.json). They define evaluation domains and status, not Buzz results.[[metrics](../METRICS.md)][[status](../results/initial-baselines-status.json)][[fixture](../fixtures/memory-benchmark-v1.json)]

## Limits and unknowns

This is a bounded review of NIP-AE and selected implementation paths at one verified commit. Buzz was not run. The review does not establish real relay interoperability, relay retention or deletion policy, listing completeness under relay caps, concurrent-writer convergence across partitions, confidentiality metadata leakage, or memory quality. The overall workspace has many other agent and event features that were not assessed. No benchmark or test results are claimed.[[head](https://github.com/block/buzz/commit/61c070d5915e11ef8f24b32d6f4f217132294320)][[nip-ae](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/docs/nips/NIP-AE.md)][[mem-cli](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-cli/src/commands/mem.rs)]

## Benchmark status

**Benchmark not run.** No Buzz runtime, benchmark workload, or tests were run for this review. Project metric definitions, the fixture, and execution-status record are protocol/status artifacts, not Buzz measurements.[[metrics](../METRICS.md)][[status](../results/initial-baselines-status.json)][[fixture](../fixtures/memory-benchmark-v1.json)]

## Sources

- [Official repository and default branch](https://github.com/block/buzz)
- [Official main commit feed](https://github.com/block/buzz/commits/main.atom)
- [Reviewed full head commit](https://github.com/block/buzz/commit/61c070d5915e11ef8f24b32d6f4f217132294320)
- [Official README](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/README.md)
- [NIP-AE agent engram specification](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/docs/nips/NIP-AE.md)
- [Engram primitives](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-core/src/engram.rs)
- [Memory CLI](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-cli/src/commands/mem.rs)
- [ACP core fetch](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-acp/src/engram_fetch.rs)
- [Relay read handler](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/crates/buzz-relay/src/handlers/req.rs)
- [Official security policy](https://github.com/block/buzz/blob/61c070d5915e11ef8f24b32d6f4f217132294320/SECURITY.md)
- [Curated ordinal and identity](../data/memory-systems.json)
- [Atlas attribution only](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/buzz.md)
- [Metric definitions](../METRICS.md)
- [Benchmark status record](../results/initial-baselines-status.json)
- [Benchmark fixture](../fixtures/memory-benchmark-v1.json)

## Contact-list follow-up

The official pinned README and SECURITY.md were checked. The README publishes no contact email; SECURITY.md publishes `buzz@block.xyz` for use when GitHub private vulnerability reporting is unavailable. The JSON records that email and the exact pinned SECURITY.md URL; it does not treat the address as a general support contact.

**Verification boundary:** no Buzz runtime, benchmarks, or tests were run.
