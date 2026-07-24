"""Download evidence sources into .tmp for manuscript verification.

The collector accepts explicit URLs, a URL list file, or external links found
in a Markdown manuscript. It stores fetched originals and a small metadata
index under ``.tmp/evidence/`` so the files stay outside git.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import html
import json
import mimetypes
import re
import sys
import time
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


DEFAULT_OUTPUT_ROOT = Path(".tmp/evidence")
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_USER_AGENT = "AiBookEvidenceCollector/1.0 (+local manuscript verification)"
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
URL_RE = re.compile(r"https?://[^\s<>)\"']+")
TITLE_RE = re.compile(
    r"<title[^>]*>(?P<title>.*?)</title>",
    flags=re.IGNORECASE | re.DOTALL,
)
SAFE_NAME_RE = re.compile(r"[^0-9A-Za-z가-힣._-]+")
EXTENSIONS_BY_CONTENT_TYPE = {
    "application/pdf": ".pdf",
    "text/html": ".html",
    "application/xhtml+xml": ".html",
    "text/plain": ".txt",
    "text/markdown": ".md",
    "application/json": ".json",
}


@dataclasses.dataclass(frozen=True)
class EvidenceSource:
    url: str
    origin: str


@dataclasses.dataclass(frozen=True)
class FetchResult:
    source: EvidenceSource
    status: str
    output_path: Path | None
    metadata_path: Path
    title: str | None
    content_type: str | None
    bytes_written: int
    error: str | None


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download related evidence sources into .tmp/evidence/.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="Manuscript Markdown page whose linked external evidence should be downloaded.",
    )
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        help="Evidence URL to download. Can be repeated.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Text, Markdown, or JSON file containing URLs.",
    )
    parser.add_argument(
        "--label",
        help="Run label used for the .tmp/evidence/<label>/ directory.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Output root. Defaults to .tmp/evidence/.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.5,
        help="Delay between downloads in seconds.",
    )
    parser.add_argument(
        "--user-agent",
        default=DEFAULT_USER_AGENT,
        help="HTTP User-Agent header.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing downloaded files in the run directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only list URLs and planned paths without downloading.",
    )
    return parser.parse_args(argv)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def unique_sources(sources: Iterable[EvidenceSource]) -> list[EvidenceSource]:
    seen: set[str] = set()
    unique: list[EvidenceSource] = []
    for source in sources:
        normalized = source.url.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        unique.append(EvidenceSource(url=normalized, origin=source.origin))
    return unique


def extract_urls_from_markdown(path: Path) -> list[EvidenceSource]:
    text = read_text(path)
    sources: list[EvidenceSource] = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        url = match.group(1).strip()
        if is_external_url(url):
            sources.append(EvidenceSource(url=url, origin=f"markdown:{path}"))
    for match in URL_RE.finditer(text):
        sources.append(EvidenceSource(url=match.group(0), origin=f"raw-url:{path}"))
    return sources


def extract_urls_from_text(path: Path) -> list[EvidenceSource]:
    text = read_text(path)
    return [
        EvidenceSource(url=match.group(0), origin=f"input:{path}")
        for match in URL_RE.finditer(text)
    ]


def extract_urls_from_json(path: Path) -> list[EvidenceSource]:
    data = json.loads(read_text(path))
    urls: list[str] = []
    collect_urls_from_json_value(data, urls)
    return [EvidenceSource(url=url, origin=f"input:{path}") for url in urls]


def collect_urls_from_json_value(value, urls: list[str]) -> None:
    if isinstance(value, str):
        urls.extend(match.group(0) for match in URL_RE.finditer(value))
    elif isinstance(value, list):
        for item in value:
            collect_urls_from_json_value(item, urls)
    elif isinstance(value, dict):
        for item in value.values():
            collect_urls_from_json_value(item, urls)


def is_external_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def collect_sources(args: argparse.Namespace) -> list[EvidenceSource]:
    sources = [EvidenceSource(url=url, origin="cli") for url in args.url]
    if args.target:
        sources.extend(extract_urls_from_markdown(args.target))
    if args.input:
        if args.input.suffix.lower() == ".json":
            sources.extend(extract_urls_from_json(args.input))
        else:
            sources.extend(extract_urls_from_text(args.input))

    return unique_sources(source for source in sources if is_external_url(source.url))


def slugify(value: str) -> str:
    value = value.strip() or "evidence"
    value = SAFE_NAME_RE.sub("-", value)
    value = value.strip("-._")
    return value[:80] or "evidence"


def default_label(args: argparse.Namespace) -> str:
    if args.label:
        return slugify(args.label)
    if args.target:
        return slugify(args.target.with_suffix("").as_posix())
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"manual-{stamp}"


def filename_for_url(url: str, content_type: str | None, ordinal: int) -> str:
    parsed = urlparse(url)
    path_name = Path(parsed.path).name
    stem = slugify(Path(path_name).stem or parsed.netloc or "source")
    extension = Path(path_name).suffix
    if not extension:
        extension = extension_for_content_type(content_type)
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
    return f"{ordinal:03d}-{stem}-{digest}{extension}"


def extension_for_content_type(content_type: str | None) -> str:
    if not content_type:
        return ".bin"
    base_content_type = content_type.split(";", 1)[0].strip().lower()
    if base_content_type in EXTENSIONS_BY_CONTENT_TYPE:
        return EXTENSIONS_BY_CONTENT_TYPE[base_content_type]
    return mimetypes.guess_extension(base_content_type) or ".bin"


def decode_title(payload: bytes, content_type: str | None) -> str | None:
    if not content_type or "html" not in content_type.lower():
        return None
    sample = payload[:200_000].decode("utf-8", errors="replace")
    match = TITLE_RE.search(sample)
    if not match:
        return None
    return " ".join(html.unescape(match.group("title")).split())


def fetch_source(
    source: EvidenceSource,
    output_dir: Path,
    ordinal: int,
    timeout: int,
    user_agent: str,
    overwrite: bool,
    dry_run: bool,
) -> FetchResult:
    metadata_path = output_dir / f"{ordinal:03d}-metadata.json"
    if dry_run:
        metadata = base_metadata(source=source, status="planned", error=None)
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        return FetchResult(
            source=source,
            status="planned",
            output_path=None,
            metadata_path=metadata_path,
            title=None,
            content_type=None,
            bytes_written=0,
            error=None,
        )

    request = Request(source.url, headers={"User-Agent": user_agent})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = response.read()
            content_type = response.headers.get("Content-Type")
            filename = filename_for_url(source.url, content_type, ordinal)
            output_path = output_dir / filename
            if output_path.exists() and not overwrite:
                status = "skipped-existing"
                bytes_written = output_path.stat().st_size
            else:
                output_path.write_bytes(payload)
                status = "downloaded"
                bytes_written = len(payload)

            title = decode_title(payload, content_type)
            metadata = base_metadata(source=source, status=status, error=None)
            metadata.update(
                {
                    "http_status": getattr(response, "status", None),
                    "content_type": content_type,
                    "title": title,
                    "output_path": output_path.as_posix(),
                    "bytes_written": bytes_written,
                    "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                }
            )
            metadata_path.write_text(
                json.dumps(metadata, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            return FetchResult(
                source=source,
                status=status,
                output_path=output_path,
                metadata_path=metadata_path,
                title=title,
                content_type=content_type,
                bytes_written=bytes_written,
                error=None,
            )
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        metadata = base_metadata(source=source, status="failed", error=str(exc))
        metadata["retrieved_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        metadata_path.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return FetchResult(
            source=source,
            status="failed",
            output_path=None,
            metadata_path=metadata_path,
            title=None,
            content_type=None,
            bytes_written=0,
            error=str(exc),
        )


def base_metadata(source: EvidenceSource, status: str, error: str | None) -> dict[str, object]:
    return {
        "url": source.url,
        "origin": source.origin,
        "status": status,
        "error": error,
    }


def write_index(output_dir: Path, results: list[FetchResult], dry_run: bool) -> Path:
    index_path = output_dir / "index.md"
    lines = [
        "# Evidence Collection",
        "",
        f"- Generated at: {dt.datetime.now().astimezone().isoformat()}",
        f"- Mode: {'dry-run' if dry_run else 'download'}",
        f"- Source count: {len(results)}",
        "",
        "| Status | URL | Title | File | Metadata |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        file_path = result.output_path.as_posix() if result.output_path else "-"
        title = result.title or "-"
        lines.append(
            "| {status} | {url} | {title} | `{file}` | `{metadata}` |".format(
                status=result.status,
                url=result.source.url,
                title=title.replace("|", "\\|"),
                file=file_path,
                metadata=result.metadata_path.as_posix(),
            )
        )
    lines.append("")
    index_path.write_text("\n".join(lines), encoding="utf-8")
    return index_path


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    sources = collect_sources(args)
    if not sources:
        print("No external evidence URLs found.", file=sys.stderr)
        return 1

    output_dir = args.output_root / default_label(args)
    output_dir.mkdir(parents=True, exist_ok=True)

    results: list[FetchResult] = []
    for ordinal, source in enumerate(sources, start=1):
        print(f"[{ordinal}/{len(sources)}] {source.url}", file=sys.stderr)
        results.append(
            fetch_source(
                source=source,
                output_dir=output_dir,
                ordinal=ordinal,
                timeout=args.timeout,
                user_agent=args.user_agent,
                overwrite=args.overwrite,
                dry_run=args.dry_run,
            )
        )
        if ordinal < len(sources) and args.sleep > 0 and not args.dry_run:
            time.sleep(args.sleep)

    index_path = write_index(output_dir=output_dir, results=results, dry_run=args.dry_run)
    failed_count = sum(1 for result in results if result.status == "failed")
    print(f"Wrote evidence index: {index_path}")
    if failed_count:
        print(f"Failed downloads: {failed_count}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
