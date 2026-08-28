#!/usr/bin/env python3
"""Download and verify manuscript model weights recorded in the AI/ML-BOM.

Model files are always written beneath ``.tmp/download/`` and are never added
to Git. The tool reads CycloneDX component references from
``model-inventory/model-weights.cdx.json`` and records the resolved URL,
revision, byte length, and SHA-256 next to every downloaded artifact.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote, urlparse
from urllib.request import Request, urlopen


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOM = REPOSITORY_ROOT / "model-inventory" / "model-weights.cdx.json"
DOWNLOAD_ROOT = REPOSITORY_ROOT / ".tmp" / "download"
USER_AGENT = "AiBookModelWeightManager/1.0 (+local manuscript asset maintenance)"
RECORD_NAME = "download-record.json"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bom", type=Path, default=DEFAULT_BOM, help="CycloneDX AI/ML-BOM path.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    listing = subcommands.add_parser("list", help="List registered model-weight components.")
    listing.add_argument("--review-required", action="store_true", help="Show only components awaiting license review.")

    fetch = subcommands.add_parser("fetch", help="Download one registered weight and write its SHA-256 record.")
    fetch.add_argument("--ref", required=True, help="CycloneDX component bom-ref.")
    fetch.add_argument("--url", help="Explicit direct artifact URL; required when the BOM has no single selector.")
    fetch.add_argument("--selector", help="Override the BOM file selector for this download.")
    fetch.add_argument("--revision", help="Immutable revision for a Hugging Face selector; defaults to main only when not recorded.")
    fetch.add_argument("--filename", help="Output file name inside the component directory.")
    fetch.add_argument("--force", action="store_true", help="Replace an existing target file.")
    fetch.add_argument("--dry-run", action="store_true", help="Show the planned URL and output path without downloading.")
    fetch.add_argument("--timeout", type=int, default=60, help="HTTP timeout in seconds.")

    verify = subcommands.add_parser("verify", help="Recalculate SHA-256 for recorded downloads.")
    verify.add_argument("--ref", action="append", help="Verify only this component ref; may be repeated.")
    return parser.parse_args(argv)


def load_bom(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise SystemExit(f"BOM not found: {path}") from error
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid BOM JSON: {path}: {error}") from error
    if data.get("bomFormat") != "CycloneDX":
        raise SystemExit(f"Not a CycloneDX BOM: {path}")
    return data


def properties(component: dict[str, Any]) -> dict[str, str]:
    return {
        item["name"]: item["value"]
        for item in component.get("properties", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str) and isinstance(item.get("value"), str)
    }


def component_by_ref(bom: dict[str, Any], ref: str) -> dict[str, Any]:
    for component in bom.get("components", []):
        if component.get("bom-ref") == ref:
            return component
    raise SystemExit(f"Unknown component ref: {ref}")


def distribution_url(component: dict[str, Any]) -> str | None:
    for reference in component.get("externalReferences", []):
        if reference.get("type") == "distribution" and isinstance(reference.get("url"), str):
            return reference["url"]
    return None


def safe_component_directory(ref: str) -> Path:
    slug = re.sub(r"[^0-9A-Za-z._-]+", "-", ref).strip(".-")
    directory = (DOWNLOAD_ROOT / slug).resolve()
    try:
        directory.relative_to(DOWNLOAD_ROOT.resolve())
    except ValueError as error:
        raise SystemExit(f"Unsafe component ref: {ref}") from error
    return directory


def selector_from_component(component: dict[str, Any], override: str | None) -> str | None:
    if override:
        return override
    selector = properties(component).get("aibook:download-selector")
    if selector and ";" not in selector and " or " not in selector:
        return selector
    return None


def observed_revision(component: dict[str, Any], override: str | None) -> str:
    if override:
        return override
    value = properties(component).get("aibook:observed-revision", "")
    match = re.match(r"^[0-9a-f]{7,64}", value)
    return match.group(0) if match else "main"


def direct_url(component: dict[str, Any], args: argparse.Namespace) -> tuple[str, str | None, str | None]:
    if args.url:
        return args.url, args.selector, args.revision
    source = distribution_url(component)
    selector = selector_from_component(component, args.selector)
    if not source:
        raise SystemExit("This component has no distribution URL; pass --url after recording the source in the BOM.")
    parsed = urlparse(source)
    path_parts = [part for part in parsed.path.split("/") if part]
    if parsed.netloc == "huggingface.co" and "resolve" in path_parts:
        resolve_index = path_parts.index("resolve")
        recorded_revision = path_parts[resolve_index + 1] if len(path_parts) > resolve_index + 1 else None
        return source, selector, args.revision or recorded_revision
    if parsed.netloc == "huggingface.co" and len(path_parts) == 2:
        if not selector:
            raise SystemExit("This Hugging Face repository has no single file selector; pass --selector or --url.")
        revision = observed_revision(component, args.revision)
        return f"https://huggingface.co/{path_parts[0]}/{path_parts[1]}/resolve/{quote(revision, safe='')}/{quote(selector, safe='/')}", selector, revision
    if selector:
        raise SystemExit("A selector can be resolved automatically only for a Hugging Face repository URL; pass --url.")
    return source, None, args.revision


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def target_name(url: str, requested_name: str | None) -> str:
    if requested_name:
        if Path(requested_name).name != requested_name:
            raise SystemExit("--filename must be a file name, not a path.")
        return requested_name
    name = unquote(Path(urlparse(url).path).name)
    return name if name and name not in {"main", "resolve"} else "artifact.bin"


def write_record(directory: Path, record: dict[str, Any]) -> None:
    path = directory / RECORD_NAME
    existing: list[dict[str, Any]] = []
    if path.exists():
        previous = json.loads(path.read_text(encoding="utf-8"))
        existing = previous.get("downloads", []) if isinstance(previous, dict) else []
    existing = [item for item in existing if item.get("filename") != record["filename"]]
    existing.append(record)
    path.write_text(json.dumps({"schema": "aibook-model-download-record-v1", "downloads": existing}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch(component: dict[str, Any], args: argparse.Namespace) -> int:
    url, selector, revision = direct_url(component, args)
    directory = safe_component_directory(component["bom-ref"])
    name = args.filename or (Path(selector).name if selector else target_name(url, None))
    target = directory / name
    if args.dry_run:
        print(json.dumps({"url": url, "output": str(target.relative_to(REPOSITORY_ROOT)), "selector": selector, "revision": revision}, ensure_ascii=False))
        return 0
    if target.exists() and not args.force:
        raise SystemExit(f"Target already exists: {target}. Use --force after comparing the existing SHA-256.")
    directory.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".part")
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=args.timeout) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output, length=1024 * 1024)
            content_type = response.headers.get_content_type()
            final_url = response.url
    except Exception as error:  # urllib exposes several transport-specific exception classes
        temporary.unlink(missing_ok=True)
        raise SystemExit(f"Download failed: {error}") from error
    temporary.replace(target)
    record = {
        "component_ref": component["bom-ref"],
        "filename": target.name,
        "source_url": distribution_url(component),
        "resolved_url": final_url,
        "selector": selector,
        "revision": revision,
        "downloaded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
        "content_type": content_type,
    }
    write_record(directory, record)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def verify(bom: dict[str, Any], requested_refs: list[str] | None) -> int:
    refs = requested_refs or [component.get("bom-ref") for component in bom.get("components", []) if component.get("bom-ref")]
    failures = 0
    checked = 0
    for ref in refs:
        directory = safe_component_directory(ref)
        record_path = directory / RECORD_NAME
        if not record_path.exists():
            continue
        for record in json.loads(record_path.read_text(encoding="utf-8")).get("downloads", []):
            checked += 1
            target = directory / record["filename"]
            actual = sha256(target) if target.is_file() else None
            status = "ok" if actual == record.get("sha256") else "mismatch"
            print(json.dumps({"component_ref": ref, "file": str(target.relative_to(REPOSITORY_ROOT)), "status": status, "sha256": actual}, ensure_ascii=False))
            failures += status != "ok"
    if not checked:
        print("No download records found beneath .tmp/download/.", file=sys.stderr)
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    bom = load_bom(args.bom)
    if args.command == "list":
        for component in bom.get("components", []):
            props = properties(component)
            if args.review_required and props.get("aibook:license-review") != "review-required":
                continue
            print("\t".join((component.get("bom-ref", ""), component.get("name", ""), distribution_url(component) or "source-url-required", props.get("aibook:download-selector", ""))))
        return 0
    if args.command == "fetch":
        return fetch(component_by_ref(bom, args.ref), args)
    return verify(bom, args.ref)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
