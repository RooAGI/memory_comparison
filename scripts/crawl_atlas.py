#!/usr/bin/env python3
"""Refresh the memory systems comparison index from the Agent Memory Atlas.

Uses only Python's standard library. Atlas detail pages are the inventory
source; GitHub repository pages provide optional metadata. Missing evidence is
kept explicit in the output.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html
from html.parser import HTMLParser
import json
import re
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ATLAS_INDEX = "https://neoneye.github.io/agent-memory-atlas/a-z/"
ATLAS_REPOSITORY = "https://github.com/neoneye/agent-memory-atlas"
LOCAL_ATLAS = Path(__file__).resolve().parents[1] / "references" / "agent-memory-atlas"
ATLAS_HOST = "neoneye.github.io"
GITHUB_REPO = re.compile(r"^https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:/.*)?$")
ATLAS_DESCRIPTIVE_FIELDS = (
    "Memory unit",
    "Storage backend",
    "Retrieval strategy",
    "Write strategy",
    "Update/delete model",
    "Scoping model",
    "Agent integration",
    "Background processing",
    "Trust/provenance model",
    "Notable strengths",
    "Main risks",
)

BENCHMARK_METRICS = (
    {"name": "Answerable retrieval accuracy", "description": "Correct answerable cases divided by all answerable cases."},
    {"name": "Correction accuracy", "description": "Post-correction probes returning the current gold value divided by all post-correction answerable probes."},
    {"name": "Stale-value rate", "description": "Post-correction probes asserting a superseded value as current divided by eligible post-correction probes."},
    {"name": "Deletion leak rate", "description": "Post-deletion probes exposing protected deleted content divided by scheduled eligible probes."},
    {"name": "Scope isolation leak rate", "description": "Forbidden cross-scope returns divided by scheduled cross-scope probes."},
    {"name": "Evidence support precision", "description": "Cited factual claims supported by cited stored sources divided by cited factual claims."},
    {"name": "Citation coverage", "description": "Factual claims with a resolvable citation divided by all adjudicated factual claims."},
    {"name": "Retrieval latency", "description": "Per-operation latency distribution, reported as p50, p95, and p99."},
    {"name": "Write-to-recall delay", "description": "Time from acknowledged write to first scheduled correct recall, with censoring reported."},
    {"name": "Tokens", "description": "Input and output token usage reported separately with provider or tokenizer provenance."},
    {"name": "Cost", "description": "Measured charges for in-scope operations under a named provider price schedule and currency/date."},
    {"name": "Storage efficiency", "description": "Persistent bytes attributable to the benchmark corpus, with measurement boundary and bytes per accepted item where reliable."},
)

METRICS = (
    "Tombstone",
    "Trust state",
    "Bi-temporal",
    "Scope enforced",
    "Mutation audit",
    "Human review",
    "Negative evals",
)

CAPABILITY_KEYS = {
    "Tombstone": "tombstone",
    "Trust state": "trust_state",
    "Bi-temporal": "bitemporal",
    "Scope enforced": "scope_enforced",
    "Mutation audit": "audit_log",
    "Human review": "human_review",
    "Negative evals": "negative_eval",
}

METRIC_DOMAIN_MAPPING = {
    "recall": {
        "profile_fields": ["Memory unit", "Retrieval strategy", "Write strategy", "Background processing"],
        "capability_flags": ["Trust state", "Bi-temporal"],
        "benchmark_metrics": ["Answerable retrieval accuracy", "Write-to-recall delay"],
    },
    "correction": {
        "profile_fields": ["Update/delete model", "Trust/provenance model"],
        "capability_flags": ["Trust state", "Bi-temporal", "Mutation audit", "Human review"],
        "benchmark_metrics": ["Correction accuracy", "Stale-value rate"],
    },
    "deletion": {
        "profile_fields": ["Update/delete model", "Background processing"],
        "capability_flags": ["Tombstone", "Mutation audit"],
        "benchmark_metrics": ["Deletion leak rate"],
    },
    "scope": {
        "profile_fields": ["Scoping model", "Agent integration"],
        "capability_flags": ["Scope enforced"],
        "benchmark_metrics": ["Scope isolation leak rate"],
    },
    "evidence": {
        "profile_fields": ["Memory unit", "Trust/provenance model", "Agent integration"],
        "capability_flags": ["Trust state", "Human review", "Negative evals"],
        "benchmark_metrics": ["Evidence support precision", "Citation coverage"],
    },
    "efficiency": {
        "profile_fields": ["Storage backend", "Retrieval strategy", "Write strategy", "Background processing", "Agent integration"],
        "capability_flags": [],
        "benchmark_metrics": ["Retrieval latency", "Tokens", "Cost", "Storage efficiency"],
    },
}
USER_AGENT = "memory-comparison-indexer/1.0 (source-backed public metadata)"


def fetch(url: str, timeout: int = 25) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/json"})
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


class PageParser(HTMLParser):
    """Collect links, page text, and text grouped by article-like containers."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.text: list[str] = []
        self._anchor_depth = 0
        self._anchor_href = ""
        self._anchor_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            self._anchor_depth = 1
            self._anchor_href = dict(attrs).get("href") or ""
            self._anchor_text = []
        elif self._anchor_depth:
            self._anchor_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self._anchor_depth:
            self._anchor_depth -= 1
            if self._anchor_depth == 0:
                label = " ".join("".join(self._anchor_text).split())
                if self._anchor_href:
                    self.links.append((self._anchor_href, label))
                self._anchor_href = ""
                self._anchor_text = []

    def handle_data(self, data: str) -> None:
        clean = html.unescape(data).strip()
        if clean:
            self.text.append(clean)
        if self._anchor_depth:
            self._anchor_text.append(data)


def parse_html(document: str) -> PageParser:
    parser = PageParser()
    parser.feed(document)
    return parser


def canonical_repo(url: str) -> tuple[str, str] | None:
    match = GITHUB_REPO.match(url.rstrip("/"))
    if not match:
        return None
    owner, name = match.groups()
    if name.lower() in {"tree", "blob", "issues", "pull", "discussions", "wiki", "actions"}:
        return None
    return owner, name.removesuffix(".git")


def report_links(page: PageParser, base_url: str) -> list[tuple[str, str]]:
    found = []
    for href, label in page.links:
        absolute = urljoin(base_url, href).split("#", 1)[0]
        parsed = urlparse(absolute)
        if parsed.netloc == ATLAS_HOST and "/systems/" in parsed.path:
            slug = parsed.path.rstrip("/").rsplit("/", 1)[-1]
            if slug and slug not in {"systems", "a-z"}:
                found.append((slug, absolute))
    return list(dict.fromkeys(found))


def github_links(page: PageParser, base_url: str) -> list[str]:
    found = []
    for href, _ in page.links:
        absolute = urljoin(base_url, href)
        if canonical_repo(absolute):
            found.append(absolute.rstrip("/"))
    return list(dict.fromkeys(found))


class RubricTableParser(HTMLParser):
    """Read rubric labels and marks from structured HTML table rows only."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None
        self.blocks: list[str] = []
        self._block_stack: list[tuple[str, list[str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"div", "li", "p"}:
            self._block_stack.append((tag, []))
        if tag == "tr":
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"td", "th"} and self._cell is not None:
            self._row.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None
            self._cell = None
        if self._block_stack and self._block_stack[-1][0] == tag:
            _, parts = self._block_stack.pop()
            text = " ".join("".join(parts).split())
            if text and len(text) <= 120:
                self.blocks.append(text)

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)
        for _, parts in self._block_stack:
            parts.append(data)


def _rubric_state(mark: str) -> str | None:
    normalized = " ".join(mark.split()).casefold()
    if normalized in {"✓", "✔", "✅", "yes", "true", "present", "supported"}:
        return "positive"
    if normalized in {"—", "–", "-", "✗", "✘", "×", "no", "false", "absent", "not supported"}:
        return "negative"
    return None


def evidence_metrics(document: str, source_url: str) -> dict[str, dict[str, object]]:
    parser = RubricTableParser()
    parser.feed(document)
    result = {
        metric: {
            "value": None,
            "status": "unavailable",
            "source_url": source_url,
            "evidence": None,
        }
        for metric in METRICS
    }
    labels = {metric.casefold(): metric for metric in METRICS}
    for row_number, row in enumerate(parser.rows, start=1):
        for index, cell in enumerate(row):
            metric = labels.get(cell.casefold())
            if not metric:
                continue
            for mark in row[:index] + row[index + 1:]:
                state = _rubric_state(mark)
                if state:
                    result[metric] = {
                        "value": state == "positive",
                        "status": state,
                        "source_url": source_url,
                        "evidence": {
                            "row": row_number,
                            "excerpt": " | ".join(row),
                        },
                    }
                    break
            if result[metric]["status"] != "unavailable":
                break
    for block in parser.blocks:
        for metric in METRICS:
            if result[metric]["status"] != "unavailable":
                continue
            if not re.search(r"(?<![\w])" + re.escape(metric) + r"(?![\w])", block, re.IGNORECASE):
                continue
            remainder = re.sub(r"(?<![\w])" + re.escape(metric) + r"(?![\w])", "", block, count=1, flags=re.IGNORECASE)
            remainder = remainder.strip(" :|·")
            state = _rubric_state(remainder)
            if state:
                result[metric] = {
                    "value": state == "positive",
                    "status": state,
                    "source_url": source_url,
                    "evidence": {"element": block},
                }
    return result


def get_repo_metadata(repo_url: str) -> dict[str, object]:
    repo = canonical_repo(repo_url)
    if not repo:
        return {"status": "unavailable", "reason": "No canonical GitHub repository URL"}
    owner, name = repo
    api_url = f"https://api.github.com/repos/{owner}/{name}"
    try:
        payload = json.loads(fetch(api_url, timeout=20))
        license_data = payload.get("license") or {}
        return {
            "status": "available",
            "description": payload.get("description"),
            "stars": payload.get("stargazers_count"),
            "forks": payload.get("forks_count"),
            "language": payload.get("language"),
            "license": license_data.get("spdx_id"),
            "default_branch": payload.get("default_branch"),
            "updated_at": payload.get("updated_at"),
            "metadata_source_url": api_url,
        }
    except (HTTPError, URLError, TimeoutError, ValueError, OSError) as exc:
        return {"status": "unavailable", "reason": f"GitHub metadata request failed: {exc}"}


def crawl_one(item: tuple[str, str]) -> dict[str, object]:
    slug, detail_url = item
    record: dict[str, object] = {
        "slug": slug,
        "name": slug.replace("-", " ").replace("_", " ").title(),
        "atlas_url": detail_url,
        "source_url": detail_url,
        "repository_url": None,
        "repository_status": "unavailable",
        "atlas_summary": None,
        "atlas_descriptions": {},
        "capability_evidence": evidence_metrics("", detail_url),
        "repository_metadata": {"status": "unavailable", "reason": "Repository URL not found in atlas report"},
    }
    try:
        document = fetch(detail_url)
        page = parse_html(document)
        text = " ".join(page.text)
        record["atlas_summary"] = text[:500] if text else None
        record["capability_evidence"] = evidence_metrics(document, detail_url)
        repos = github_links(page, detail_url)
        if repos:
            record["repository_url"] = repos[0]
            record["repository_status"] = "linked"
            record["repository_metadata"] = get_repo_metadata(repos[0])
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        record["crawl_error"] = str(exc)
    return record


def _frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(r"^" + re.escape(key) + r":\s*(.*?)\s*$", frontmatter, re.MULTILINE)
    if not match:
        return None
    value = match.group(1)
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except ValueError:
            return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value or None


def _frontmatter_section(frontmatter: str, section: str) -> dict[str, str]:
    match = re.search(r"^" + re.escape(section) + r":\s*\n((?:[ \t]+[^\n]*\n?)*)", frontmatter, re.MULTILINE)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"\s+([a-z_]+):\s*(.*?)\s*$", line)
        if not item:
            continue
        key, raw = item.groups()
        try:
            value = json.loads(raw) if raw.startswith('"') else raw
        except ValueError:
            value = raw[1:-1] if len(raw) >= 2 and raw[0] == raw[-1] == '"' else raw
        values[key] = value
    return values


def _local_report(path: Path, checkout: Path, revision: str) -> dict[str, object]:
    document = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", document, re.DOTALL)
    frontmatter = match.group(1) if match else ""
    slug = path.stem
    title = _frontmatter_value(frontmatter, "title") or slug
    repo_url = _frontmatter_value(frontmatter, "source_url")
    pinned_revision = _frontmatter_value(frontmatter, "revision")
    atlas_url = f"https://neoneye.github.io/agent-memory-atlas/systems/{slug}/"
    report_source_url = f"{ATLAS_REPOSITORY}/blob/{revision}/content/systems/{path.name}"
    matrix = _frontmatter_section(frontmatter, "matrix")
    descriptive_keys = {
        "memory_unit": "Memory unit", "storage": "Storage backend",
        "retrieval": "Retrieval strategy", "write": "Write strategy",
        "update_delete": "Update/delete model", "scoping": "Scoping model",
        "integration": "Agent integration", "background": "Background processing",
        "trust": "Trust/provenance model", "strengths": "Notable strengths",
        "risks": "Main risks",
    }
    descriptions = {
        label: {
            "value": matrix.get(key),
            "status": "available" if matrix.get(key) else "unknown",
            "source_url": report_source_url,
            "evidence": {"frontmatter": f"matrix.{key}", "revision": pinned_revision},
        }
        for key, label in descriptive_keys.items()
    }
    listed = _frontmatter_value(frontmatter, "capabilities")
    declared = set((listed or "").split(", ")) if listed is not None else None
    details = _frontmatter_section(frontmatter, "capability_evidence")
    capabilities: dict[str, object] = {}
    for label, key in CAPABILITY_KEYS.items():
        if declared is None or not pinned_revision:
            status, value = "unknown", None
            evidence = {"basis": "Report capability declaration or analyzed revision is missing"}
        elif key in declared:
            status, value = "positive", True
            evidence = {"frontmatter": f"capability_evidence.{key}" if key in details else "capabilities",
                        "excerpt": details.get(key), "revision": pinned_revision}
        else:
            status, value = "negative", False
            evidence = {"frontmatter": "capabilities", "excerpt": f"Atlas report does not mark {label} present at its pinned revision; dash means not found, not impossible.", "revision": pinned_revision}
        capabilities[label] = {"value": value, "status": status, "source_url": report_source_url, "evidence": evidence}
    return {
        "name": title,
        "slug": slug,
        "atlas_url": atlas_url,
        "source_url": report_source_url,
        "repository_url": repo_url,
        "repository_status": "explicit" if repo_url else "unavailable",
        "revision": pinned_revision,
        "revision_status": "pinned" if pinned_revision else "unavailable",
        "revision_url": _frontmatter_value(frontmatter, "revision_url"),
        "analyzed_at": _frontmatter_value(frontmatter, "analyzed_at"),
        "atlas_descriptions": descriptions,
        "capability_evidence": capabilities,
        "profile_metric_mapping": METRIC_DOMAIN_MAPPING,
        "project_benchmark_results": {"status": "not_measured", "note": "Profile descriptions and Atlas capability evidence are not benchmark results."},
    }


def crawl_local(checkout: Path) -> dict[str, object]:
    checkout = checkout.resolve()
    reports_dir = checkout / "content" / "systems"
    if not reports_dir.is_dir():
        raise RuntimeError(f"No content/systems directory in local Atlas checkout: {checkout}")
    try:
        revision = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, OSError):
        revision = "unknown"
    paths = sorted(reports_dir.glob("*.md"), key=lambda p: p.name.casefold())
    records = [_local_report(path, checkout, revision) for path in paths]
    records.sort(key=lambda row: str(row["name"]).casefold())
    return {
        "schema_version": 3,
        "source_url": ATLAS_REPOSITORY,
        "source_revision": revision,
        "source_revision_status": "pinned" if revision != "unknown" else "unknown",
        "source_path": str(checkout),
        "fetched_at": None,
        "system_count": len(records),
        "report_count": len(paths),
        "atlas_published_report_count": 852,
        "atlas_count_note": "Published A–Z page states 852 reports; local checkout report count is measured from content/systems/*.md.",
        "atlas_descriptive_fields": list(ATLAS_DESCRIPTIVE_FIELDS),
        "capability_definitions": {"source": "Agent Memory Atlas report evidence", "fields": list(METRICS), "interpretation": "Unavailable in this offline inventory; feature marks have not been extracted from report evidence."},
        "benchmark_metrics": list(BENCHMARK_METRICS),
        "metric_domain_mapping": METRIC_DOMAIN_MAPPING,
        "profile_interpretation": "Atlas fields describe designs; capability states are reviewer claims at each report revision. Neither feature presence nor descriptive fields are benchmark performance.",
        "systems": records,
    }


def crawl(source_url: str, workers: int = 8) -> dict[str, object]:
    source_path = Path(source_url).expanduser()
    if source_path.is_dir():
        return crawl_local(source_path)
    index_document = fetch(source_url)
    index_page = parse_html(index_document)
    items = report_links(index_page, source_url)
    if not items:
        raise RuntimeError(f"No atlas system report links found at {source_url}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        records = list(pool.map(crawl_one, items))
    records.sort(key=lambda row: str(row["name"]).casefold())
    return {
        "schema_version": 1,
        "source_url": source_url,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "system_count": len(records),
        "atlas_descriptive_fields": list(ATLAS_DESCRIPTIVE_FIELDS),
        "capability_definitions": {
            "source": "Agent Memory Atlas report evidence",
            "fields": list(METRICS),
            "interpretation": "Positive and negative values require an explicit mark paired with an exact rubric label in a structured table row or compact structured rubric element. Unavailable means no such mark was found; prose mentions are ignored. These are not benchmark scores.",
        },
        "benchmark_metrics": list(BENCHMARK_METRICS),
        "metric_domain_mapping": METRIC_DOMAIN_MAPPING,
        "profile_interpretation": "Atlas fields describe designs; capability states are reviewer claims at each report revision. Neither feature presence nor descriptive fields are benchmark performance.",
        "systems": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(LOCAL_ATLAS) if LOCAL_ATLAS.is_dir() else ATLAS_INDEX, help="Atlas checkout directory or A–Z index URL")
    parser.add_argument("--output", default="data/memory-systems.json", help="Output JSON path")
    parser.add_argument("--workers", type=int, default=8, help="Concurrent atlas and GitHub requests (online source only)")
    parser.add_argument("--check", action="store_true", help="Crawl and report counts without writing")
    args = parser.parse_args()
    try:
        result = crawl(args.source, max(1, min(args.workers, 16)))
    except Exception as exc:
        print(f"crawl failed: {exc}", file=sys.stderr)
        return 1
    print(f"Discovered {result['system_count']} atlas reports from {result['source_url']}")
    repos = sum(bool(row["repository_url"]) for row in result["systems"])
    print(f"Found {repos} linked GitHub repositories")
    if args.check:
        return 0
    with open(args.output, "w", encoding="utf-8") as output:
        json.dump(result, output, ensure_ascii=False, indent=2)
        output.write("\n")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
