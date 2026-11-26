# Benchmark adapter contract

The reusable runner in `scripts/benchmark_runner.py` executes fixture events in order. An adapter is a Python module placed on `PYTHONPATH` and named by `--adapter` or the run config's `adapter_module`. Implement the functions below. The runner passes fixture operation mappings to adapter methods and gives every call the frozen JSON config as a keyword argument. For query operations it removes the `expected` gold-label field before calling scope, retrieval, or evidence methods, so expected answers never reach the system.

```python
ADAPTER_VERSION = "1.0.0"

def capabilities(config) -> dict[str, bool]:
    # All keys are required: reset, write, retrieve, correct, delete, scope, evidence.
    ...

def reset(case_id: str, *, config) -> None: ...
def write(operation: dict, *, config) -> dict: ...
def retrieve(operation: dict, *, config) -> dict: ...
def correct(operation: dict, *, config) -> dict: ...
def delete(operation: dict, *, config) -> dict: ...
def set_scope(operation: dict, *, config) -> None: ...
def extract_evidence(operation: dict, retrieval: dict, *, config) -> object: ...
```

Every capability must be explicitly reported as `true` or `false`. False capabilities are recorded as `unsupported` per operation with a reason; a false reset capability makes case operations `not_run` because clean case isolation cannot be claimed. A method may raise `NotImplementedError` to report an operation as unsupported. Other adapter exceptions are recorded as execution failures and do not stop later fixture events. Each operation has an `execution_status` (completed, unsupported, failed, or not_run) and a null `result_state`; the runner does not adjudicate gold answers or call execution a pass. An adjudicator may later set result_state to supported, unsupported, unknown, or not_run under the fixture definitions. The runner never invents a success for missing output.

For query events the runner calls `set_scope` with the query operation (including its principal and `allowed_scopes`), then calls `retrieve` with the exact query text. If scope enforcement is unsupported, that query is marked unsupported and retrieval is skipped. Evidence extraction is a separate adapter operation, invoked after retrieval when supported. Return evidence in a JSON-serializable form; an object such as `{"status":"unsupported","reason":"..." }` explicitly reports unsupported evidence extraction while retaining the raw answer.

Return a JSON-compatible mapping from write, retrieve, correction, and delete methods. Query mappings use this shape; write-like methods may use the acknowledgment, usage, and storage fields that apply:

```json
{
  "response": "raw answer text, preserved exactly",
  "response_hash_sha256": null,
  "returned_source_ids": ["source-id"],
  "citations": ["source-id"],
  "usage": {
    "input_tokens": 12,
    "output_tokens": 8,
    "tokenizer_or_usage_source": "provider-reported",
    "cost_usd": 0.0001,
    "price_schedule": "provider price sheet, YYYY-MM-DD"
  },
  "write_ack_at": null,
  "probe_at": "RFC3339 UTC timestamp",
  "write_to_recall_delay_ms": null,
  "persistent_storage_bytes": null,
  "storage_boundary": "unavailable",
  "failure_or_unavailable_reason": null
}
```

Use null for unobserved values, never zero as a placeholder. Supply raw answer text when policy permits, otherwise supply a stable SHA-256 hash and document redaction in the adapter/config. Token totals are provider-reported or name the tokenizer and version. Costs are measured in USD under an identified price schedule. Storage measurements name their boundary. Evidence results should include the retrieved passages/IDs or a stable reference that lets the result be audited.

## Run configuration and outputs

Pass a JSON config with explicit, versioned settings. At minimum:

```json
{
  "adapter_module": "my_memory_adapter",
  "system": {"name": "Example", "commit_or_version": "git SHA or release", "config": {}},
  "dataset_version": "fixture/dataset version label",
  "model": {"provider": "provider", "name": "model-name", "version": "model-version"},
  "prompt": {"version": "prompt-set-version", "templates": {}},
  "retrieval_settings": {"top_k": 5},
  "price_schedule": "provider price sheet, YYYY-MM-DD",
  "storage_boundary": "stores and indexes included; logical or physical"
}
```

Run `python3 scripts/benchmark_runner.py --check` for fixture parse/structure validation without executing a system. To execute, provide `--config`, `--adapter` (or `adapter_module`), and a fresh `--output` path. The runner refuses to overwrite an existing result. Results use schema version 1.0.0 and `data_kind: measured_benchmark_result`, and include fixture hash/version, harness and adapter versions, system commit/config, model/prompt/retrieval settings, operation order, per-operation raw responses/evidence/timing/token/cost observations, unavailable reasons, execution statuses, and summaries. They leave scoring state null for later adjudication. Store result JSON separately from `data/memory-systems.json`; that catalog holds Atlas descriptions and feature-review evidence, not benchmark outcomes.
