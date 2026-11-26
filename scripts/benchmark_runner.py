#!/usr/bin/env python3
"""Run versioned memory benchmark fixtures through a system adapter.

Adapters are imported as Python modules and expose ADAPTER_VERSION, capabilities(),
reset(case_id, *, config), write(operation, *, config), retrieve(operation, *, config),
correct(operation, *, config), delete(operation, *, config), set_scope(operation, *, config),
and extract_evidence(operation, retrieval, *, config). See BENCHMARK_ADAPTER.md.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import platform
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HARNESS_VERSION = "1.0.0"
CAPABILITY_NAMES = ("reset", "write", "retrieve", "correct", "delete", "scope", "evidence")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_revision() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True
        ).stdout.strip() or None
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def validate_fixture(fixture: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(fixture, dict):
        return ["fixture root must be an object"]
    for key in ("fixture_version", "fixture_id", "cases", "workload_record"):
        if key not in fixture:
            errors.append(f"missing fixture field: {key}")
    cases = fixture.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty array")
        return errors
    case_ids: set[str] = set()
    op_ids: set[str] = set()
    for case_index, case in enumerate(cases):
        if not isinstance(case, dict) or not isinstance(case.get("case_id"), str):
            errors.append(f"case {case_index} must have a string case_id")
            continue
        case_id = case["case_id"]
        if case_id in case_ids:
            errors.append(f"duplicate case_id: {case_id}")
        case_ids.add(case_id)
        operations = case.get("operations")
        if not isinstance(operations, list) or not operations:
            errors.append(f"{case_id}: operations must be a non-empty array")
            continue
        for operation_index, operation in enumerate(operations):
            label = f"{case_id} operation {operation_index}"
            if not isinstance(operation, dict):
                errors.append(f"{label} must be an object")
                continue
            op_id, op_type = operation.get("op_id"), operation.get("type")
            if not isinstance(op_id, str):
                errors.append(f"{label}: op_id must be a string")
            elif op_id in op_ids:
                errors.append(f"duplicate op_id: {op_id}")
            else:
                op_ids.add(op_id)
            if op_type not in ("write", "query", "correction", "delete"):
                errors.append(f"{label}: unsupported fixture operation type {op_type!r}")
            if op_type == "query" and not isinstance(operation.get("expected"), dict):
                errors.append(f"{label}: query requires expected scoring metadata")
    return errors


def nearest_rank(values: list[float], percentile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    rank = max(1, int((percentile * len(ordered)) + 0.999999999))
    return ordered[rank - 1]


def normalize_result(
    run_id: str, case_id: str, operation: dict[str, Any], status: str, started_at: str,
    latency_ms: float | None, *, raw: Any = None, evidence: Any = None, reason: str | None = None
) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    usage = raw.get("usage") if isinstance(raw.get("usage"), dict) else {}
    ids = raw.get("returned_source_ids", [])
    citations = raw.get("citations", [])
    return {
        "run_id": run_id,
        "case_id": case_id,
        "op_id": operation["op_id"],
        "turn": operation["turn"],
        "operation_type": operation["type"],
        "execution_status": status,
        "result_state": None,
        "started_at": started_at,
        "latency_ms": latency_ms,
        "request": operation,
        "response": raw.get("response"),
        "response_hash_sha256": raw.get("response_hash_sha256"),
        "returned_source_ids": ids if isinstance(ids, list) else [],
        "citations": citations if isinstance(citations, list) else [],
        "evidence": evidence,
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "tokenizer_or_usage_source": usage.get("tokenizer_or_usage_source"),
        "cost_usd": usage.get("cost_usd"),
        "price_schedule": usage.get("price_schedule"),
        "persistent_storage_bytes": raw.get("persistent_storage_bytes"),
        "storage_boundary": raw.get("storage_boundary"),
        "write_ack_at": raw.get("write_ack_at"),
        "probe_at": raw.get("probe_at"),
        "write_to_recall_delay_ms": raw.get("write_to_recall_delay_ms"),
        "failure_or_unavailable_reason": reason or raw.get("failure_or_unavailable_reason"),
    }


def run(fixture: dict[str, Any], fixture_path: Path, config: dict[str, Any],
        adapter: Any, dataset_version: str, repeat_index: int) -> dict[str, Any]:
    capabilities = adapter.capabilities(config)
    if not isinstance(capabilities, dict):
        raise ValueError("adapter.capabilities(config) must return a capability mapping")
    for name in CAPABILITY_NAMES:
        if not isinstance(capabilities.get(name), bool):
            raise ValueError(f"adapter capability {name!r} must be true or false")

    run_id = str(uuid.uuid4())
    started_at = utc_now()
    records: list[dict[str, Any]] = []
    case_summaries: list[dict[str, Any]] = []
    for case in fixture["cases"]:
        case_id = case["case_id"]
        case_start = len(records)
        if not capabilities["reset"]:
            for operation in case["operations"]:
                records.append(normalize_result(
                    run_id, case_id, operation, "not_run", utc_now(), None,
                    reason="adapter reports reset capability unsupported; case isolation unavailable",
                ))
            case_summaries.append({"case_id": case_id, "execution_status": "not_run"})
            continue
        try:
            adapter.reset(case_id, config=config)
        except NotImplementedError as exc:
            for operation in case["operations"]:
                records.append(normalize_result(
                    run_id, case_id, operation, "not_run", utc_now(), None,
                    reason=f"reset unsupported: {exc}",
                ))
            case_summaries.append({"case_id": case_id, "execution_status": "not_run"})
            continue
        except Exception as exc:
            for operation in case["operations"]:
                records.append(normalize_result(
                    run_id, case_id, operation, "not_run", utc_now(), None,
                    reason=f"reset failed: {type(exc).__name__}: {exc}",
                ))
            case_summaries.append({"case_id": case_id, "execution_status": "failed"})
            continue

        for operation in case["operations"]:
            op_type = operation["type"]
            capability = {
                "write": "write", "query": "retrieve", "correction": "correct", "delete": "delete"
            }[op_type]
            if not capabilities[capability]:
                records.append(normalize_result(
                    run_id, case_id, operation, "unsupported", utc_now(), None,
                    reason=f"adapter reports {capability} capability unsupported",
                ))
                continue
            if op_type == "query" and not capabilities["scope"]:
                records.append(normalize_result(
                    run_id, case_id, operation, "unsupported", utc_now(), None,
                    reason="adapter reports scope capability unsupported; caller scope cannot be enforced",
                ))
                continue

            op_started_at = utc_now()
            before = time.perf_counter()
            raw: Any = None
            evidence: Any = None
            status = "completed"
            reason = None
            try:
                if op_type == "write":
                    raw = adapter.write(operation, config=config)
                elif op_type == "correction":
                    raw = adapter.correct(operation, config=config)
                elif op_type == "delete":
                    raw = adapter.delete(operation, config=config)
                else:
                    # Gold labels are harness-only; never pass expected answers to the adapter.
                    adapter_operation = {key: value for key, value in operation.items() if key != "expected"}
                    adapter.set_scope(adapter_operation, config=config)
                    raw = adapter.retrieve(adapter_operation, config=config)
                    if capabilities["evidence"]:
                        evidence = adapter.extract_evidence(adapter_operation, raw, config=config)
                    else:
                        evidence = {"status": "unsupported", "reason": "adapter reports evidence capability unsupported"}
                if raw is None:
                    raw = {}
                if not isinstance(raw, dict):
                    raise TypeError("operation adapter methods must return a JSON-compatible object mapping")
                if isinstance(evidence, dict) and evidence.get("status") == "unsupported":
                    reason = evidence.get("reason")
            except NotImplementedError as exc:
                status, reason = "unsupported", str(exc) or f"{capability} unsupported"
            except Exception as exc:
                status, reason = "failed", f"{type(exc).__name__}: {exc}"
            latency_ms = (time.perf_counter() - before) * 1000.0
            records.append(normalize_result(
                run_id, case_id, operation, status, op_started_at, latency_ms,
                raw=raw, evidence=evidence, reason=reason,
            ))

        case_records = records[case_start:]
        case_summaries.append({
            "case_id": case_id,
            "execution_status": ("failed" if any(row["execution_status"] == "failed" for row in case_records)
                                 else "unsupported" if any(row["execution_status"] == "unsupported" for row in case_records)
                                 else "completed"),
        })

    latencies = [
        row["latency_ms"] for row in records
        if row["operation_type"] == "query" and row["latency_ms"] is not None
    ]
    token_rows = [row for row in records if row["input_tokens"] is not None or row["output_tokens"] is not None]
    costs = [row["cost_usd"] for row in records if isinstance(row["cost_usd"], (int, float))]
    storage_values = [row["persistent_storage_bytes"] for row in records
                      if isinstance(row["persistent_storage_bytes"], int)]
    return {
        "result_schema_version": "1.0.0",
        "data_kind": "measured_benchmark_result",
        "run": {
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": utc_now(),
            "fixture_id": fixture["fixture_id"],
            "fixture_version": fixture["fixture_version"],
            "dataset_version": dataset_version,
            "fixture_sha256": sha256_file(fixture_path),
            "harness_version": HARNESS_VERSION,
            "harness_commit": git_revision(),
            "python_version": platform.python_version(),
            "repeat_index": repeat_index,
            "system": config["system"],
            "model": config["model"],
            "prompt": config["prompt"],
            "retrieval_settings": config["retrieval_settings"],
            "adapter": {"module": config["adapter_module"],
                        "version": str(getattr(adapter, "ADAPTER_VERSION", "unversioned")),
                        "capabilities": capabilities},
            "operation_order": [row["op_id"] for row in records],
        },
        "summary": {
            "operation_count": len(records),
            "execution_status_counts": {status: sum(row["execution_status"] == status for row in records)
                                         for status in ("completed", "unsupported", "failed", "not_run")},
            "case_summaries": case_summaries,
            "retrieval_latency_ms": {
                "n": len(latencies),
                "p50": nearest_rank(latencies, 0.50),
                "p95": nearest_rank(latencies, 0.95),
                "p99": nearest_rank(latencies, 0.99),
                "failures_and_timeouts": sum(row["execution_status"] == "failed" for row in records
                                             if row["operation_type"] == "query"),
            },
            "tokens": {
                "input_total": sum(row["input_tokens"] for row in token_rows
                                   if isinstance(row["input_tokens"], int)),
                "output_total": sum(row["output_tokens"] for row in token_rows
                                    if isinstance(row["output_tokens"], int)),
                "operations_with_usage": len(token_rows),
            },
            "cost": {"total_usd": sum(costs) if len(costs) == len(records) else None,
                     "operations_with_cost": len(costs),
                     "price_schedule": config.get("price_schedule", "unavailable")},
            "storage": {"latest_observed_bytes": storage_values[-1] if storage_values else None,
                        "boundary": config.get("storage_boundary", "unavailable")},
        },
        "operations": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=Path("fixtures/memory-benchmark-v1.json"))
    parser.add_argument("--dataset-version", help="version/hash label for the fixture dataset (defaults to fixture version)")
    parser.add_argument("--config", type=Path, help="JSON file pinning adapter, model, prompt, and retrieval settings")
    parser.add_argument("--adapter", help="Python module implementing BENCHMARK_ADAPTER.md")
    parser.add_argument("--output", type=Path, help="new JSON result path, separate from Atlas catalog data")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--check", action="store_true", help="parse and structurally validate fixture; do not execute")
    args = parser.parse_args()

    try:
        fixture = load_json(args.fixture)
        errors = validate_fixture(fixture)
        if errors:
            raise ValueError("\n".join(errors))
        if args.check:
            print(json.dumps({
                "status": "valid",
                "fixture_id": fixture["fixture_id"],
                "fixture_version": fixture["fixture_version"],
                "cases": len(fixture["cases"]),
                "operations": sum(len(case["operations"]) for case in fixture["cases"]),
                "sha256": sha256_file(args.fixture),
            }, indent=2))
            return 0
        if not args.config or not args.output:
            parser.error("--config and --output are required unless --check is used")
        config = load_json(args.config)
        required = ("model", "prompt", "retrieval_settings", "system")
        missing = [key for key in required if key not in config]
        if missing:
            raise ValueError(f"config missing required pinned fields: {', '.join(missing)}")
        module_name = args.adapter or config.get("adapter_module")
        if not module_name:
            raise ValueError("adapter module must be set with --adapter or config.adapter_module")
        config["adapter_module"] = module_name
        if not isinstance(config["model"], dict) or not isinstance(config["prompt"], dict):
            raise ValueError("model and prompt settings must be JSON objects with explicit version fields")
        if not config["model"].get("version") or not config["prompt"].get("version"):
            raise ValueError("model.version and prompt.version are required")
        if not isinstance(config["retrieval_settings"], dict):
            raise ValueError("retrieval_settings must be a JSON object")
        if not isinstance(config["system"], dict) or not config["system"].get("name"):
            raise ValueError("system.name is required")
        if not config["system"].get("commit_or_version") or not isinstance(config["system"].get("config"), dict):
            raise ValueError("system.commit_or_version and system.config object are required")
        if args.repeat < 1:
            raise ValueError("--repeat must be at least 1")
        adapter = importlib.import_module(module_name)
        dataset_version = args.dataset_version or fixture["fixture_version"]
        for repeat_index in range(1, args.repeat + 1):
            result = run(fixture, args.fixture, config, adapter, dataset_version, repeat_index)
            output_path = args.output if args.repeat == 1 else args.output.with_name(
                f"{args.output.stem}-repeat-{repeat_index}{args.output.suffix}"
            )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("x", encoding="utf-8") as stream:
                json.dump(result, stream, indent=2, ensure_ascii=False)
                stream.write("\n")
            print(json.dumps({"status": "written", "path": str(output_path),
                              "run_id": result["run"]["run_id"],
                              "operations": result["summary"]["operation_count"]}))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, ImportError) as exc:
        print(f"benchmark runner: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
