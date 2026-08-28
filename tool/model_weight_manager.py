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
HUGGINGFACE_DOWNLOAD_ROOT = DOWNLOAD_ROOT / "huggingface"
DEFAULT_HUGGINGFACE_HUB = Path("/home/cbsim/.cache/huggingface/hub")
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

    verify_migrations = subcommands.add_parser("verify-migrations", help="Recalculate manifests for model directories moved into .tmp/download/.")
    verify_migrations.add_argument("--ref", action="append", help="Verify only this component ref; may be repeated.")

    relocate = subcommands.add_parser("relocate", help="Move one Hugging Face cache entry after a SHA-256 manifest comparison.")
    relocate.add_argument("--ref", required=True, help="CycloneDX component bom-ref with a Hugging Face distribution URL.")
    relocate.add_argument("--source-hub", type=Path, default=DEFAULT_HUGGINGFACE_HUB, help="Existing Hugging Face hub cache.")
    relocate.add_argument("--dry-run", action="store_true", help="Show the source, target, and file count without moving anything.")

    relocate_directory = subcommands.add_parser("relocate-directory", help="Move one registered non-Hugging Face cache directory after a SHA-256 manifest comparison.")
    relocate_directory.add_argument("--ref", required=True, help="CycloneDX component bom-ref.")
    relocate_directory.add_argument("--source", type=Path, required=True, help="Existing model cache directory to move.")
    relocate_directory.add_argument("--dry-run", action="store_true", help="Show the source, target, and file count without moving anything.")

    audit = subcommands.add_parser("audit-cache", help="Compare a Hugging Face cache with model repositories registered in the BOM.")
    audit.add_argument("--hub-root", type=Path, default=HUGGINGFACE_DOWNLOAD_ROOT / "hub", help="Hugging Face hub cache to inspect.")
    audit.add_argument("--unregistered-only", action="store_true", help="Show only cache entries absent from the BOM.")

    quarantine = subcommands.add_parser("quarantine", help="Move one unregistered cache entry to a recoverable quarantine after hash comparison.")
    quarantine.add_argument("--cache-name", required=True, help="Exact models--ORG--NAME cache directory name from audit-cache.")
    quarantine.add_argument("--hub-root", type=Path, default=HUGGINGFACE_DOWNLOAD_ROOT / "hub", help="Hugging Face hub cache containing the entry.")
    quarantine.add_argument("--dry-run", action="store_true", help="Show the planned quarantine move without moving anything.")
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


def huggingface_cache_directory(component: dict[str, Any], hub_root: Path) -> Path:
    source = distribution_url(component)
    if not source or urlparse(source).netloc != "huggingface.co":
        raise SystemExit("relocate supports only a component with a Hugging Face distribution URL.")
    parts = [part for part in urlparse(source).path.split("/") if part]
    if "resolve" in parts:
        parts = parts[: parts.index("resolve")]
    if len(parts) != 2:
        raise SystemExit(f"Cannot derive a Hugging Face repository from: {source}")
    return hub_root / f"models--{parts[0]}--{parts[1]}"


def file_manifest(directory: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(directory.rglob("*")):
        if path.is_file() and not path.is_symlink():
            records.append({"path": path.relative_to(directory).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    return records


def relocate(component: dict[str, Any], args: argparse.Namespace) -> int:
    source_hub = args.source_hub.resolve()
    source = huggingface_cache_directory(component, source_hub)
    target_hub = HUGGINGFACE_DOWNLOAD_ROOT / "hub"
    target = huggingface_cache_directory(component, target_hub)
    if not source.is_dir():
        raise SystemExit(f"Source cache entry not found: {source}")
    if target.exists():
        raise SystemExit(f"Target cache entry already exists: {target}; compare it before any manual reconciliation.")
    source_manifest = file_manifest(source)
    summary = {"component_ref": component["bom-ref"], "source": str(source), "target": str(target), "file_count": len(source_manifest), "bytes": sum(item["bytes"] for item in source_manifest)}
    if args.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))
    target_manifest = file_manifest(target)
    if target_manifest != source_manifest:
        raise SystemExit("Migration hash manifest mismatch; source was moved, so stop and inspect the target before using it.")
    record_directory = HUGGINGFACE_DOWNLOAD_ROOT / "migrations"
    record_directory.mkdir(parents=True, exist_ok=True)
    record_path = record_directory / f"{safe_component_directory(component['bom-ref']).name}.json"
    record = {**summary, "moved_at": dt.datetime.now(dt.timezone.utc).isoformat(), "manifest": target_manifest}
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({**summary, "status": "verified-moved", "record": str(record_path.relative_to(REPOSITORY_ROOT))}, ensure_ascii=False, indent=2))
    return 0


def relocate_directory(component: dict[str, Any], args: argparse.Namespace) -> int:
    """Move a non-Hugging Face cache into its registered component directory."""
    source = args.source.resolve()
    target = safe_component_directory(component["bom-ref"])
    if not source.is_dir():
        raise SystemExit(f"Source model directory not found: {source}")
    if target.exists():
        raise SystemExit(f"Target model directory already exists: {target}; compare it before any manual reconciliation.")
    source_manifest = file_manifest(source)
    summary = {
        "component_ref": component["bom-ref"],
        "source": str(source),
        "target": str(target),
        "file_count": len(source_manifest),
        "bytes": sum(item["bytes"] for item in source_manifest),
    }
    if args.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))
    target_manifest = file_manifest(target)
    if target_manifest != source_manifest:
        raise SystemExit("Migration hash manifest mismatch; source was moved, so stop and inspect the target before using it.")
    record_directory = DOWNLOAD_ROOT / "migrations"
    record_directory.mkdir(parents=True, exist_ok=True)
    record_path = record_directory / f"{safe_component_directory(component['bom-ref']).name}.json"
    record = {**summary, "moved_at": dt.datetime.now(dt.timezone.utc).isoformat(), "manifest": target_manifest}
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({**summary, "status": "verified-moved", "record": str(record_path.relative_to(REPOSITORY_ROOT))}, ensure_ascii=False, indent=2))
    return 0


def registered_huggingface_cache_names(bom: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for component in bom.get("components", []):
        source = distribution_url(component)
        if not source or urlparse(source).netloc != "huggingface.co":
            continue
        parts = [part for part in urlparse(source).path.split("/") if part]
        if "resolve" in parts:
            parts = parts[: parts.index("resolve")]
        if len(parts) == 2:
            names.add(f"models--{parts[0]}--{parts[1]}")
    return names


def directory_size(directory: Path) -> int:
    return sum(path.stat().st_size for path in directory.rglob("*") if path.is_file() and not path.is_symlink())


def audit_cache(bom: dict[str, Any], args: argparse.Namespace) -> int:
    hub_root = args.hub_root.resolve()
    if not hub_root.is_dir():
        raise SystemExit(f"Hub cache not found: {hub_root}")
    registered = registered_huggingface_cache_names(bom)
    rows = []
    for directory in sorted(hub_root.glob("models--*")):
        status = "registered" if directory.name in registered else "unregistered-candidate"
        if args.unregistered_only and status != "unregistered-candidate":
            continue
        rows.append({"cache_name": directory.name, "status": status, "bytes": directory_size(directory)})
    print(json.dumps({"hub_root": str(hub_root), "entries": rows, "registered_count": sum(row["status"] == "registered" for row in rows), "unregistered_count": sum(row["status"] == "unregistered-candidate" for row in rows)}, ensure_ascii=False, indent=2))
    return 0


def quarantine_cache(bom: dict[str, Any], args: argparse.Namespace) -> int:
    if Path(args.cache_name).name != args.cache_name or not args.cache_name.startswith("models--"):
        raise SystemExit("--cache-name must be one exact models--ORG--NAME directory name.")
    if args.cache_name in registered_huggingface_cache_names(bom):
        raise SystemExit("Registered model: remove or retire its BOM component before quarantining it.")
    source = args.hub_root.resolve() / args.cache_name
    if not source.is_dir():
        raise SystemExit(f"Cache entry not found: {source}")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = HUGGINGFACE_DOWNLOAD_ROOT / "quarantine" / stamp / args.cache_name
    manifest = file_manifest(source)
    summary = {"cache_name": args.cache_name, "source": str(source), "target": str(target), "file_count": len(manifest), "bytes": sum(item["bytes"] for item in manifest)}
    if args.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))
    if file_manifest(target) != manifest:
        raise SystemExit("Quarantine hash manifest mismatch; stop and inspect the target before deleting anything.")
    record = {**summary, "quarantined_at": dt.datetime.now(dt.timezone.utc).isoformat(), "manifest": manifest}
    (target.parent / f"{args.cache_name}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({**summary, "status": "verified-quarantined"}, ensure_ascii=False, indent=2))
    return 0


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
        requested_path = Path(requested_name)
        if requested_path.is_absolute() or ".." in requested_path.parts:
            raise SystemExit("--filename must be a safe relative path beneath the component directory.")
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
    try:
        target.resolve().relative_to(directory.resolve())
    except ValueError as error:
        raise SystemExit("--filename must remain beneath the component directory.") from error
    if args.dry_run:
        print(json.dumps({"url": url, "output": str(target.relative_to(REPOSITORY_ROOT)), "selector": selector, "revision": revision}, ensure_ascii=False))
        return 0
    if target.exists() and not args.force:
        raise SystemExit(f"Target already exists: {target}. Use --force after comparing the existing SHA-256.")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".part")
    resumed_bytes = temporary.stat().st_size if temporary.exists() else 0
    headers = {"User-Agent": USER_AGENT}
    if resumed_bytes:
        headers["Range"] = f"bytes={resumed_bytes}-"
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=args.timeout) as response:
            can_append = resumed_bytes and getattr(response, "status", None) == 206
            with temporary.open("ab" if can_append else "wb") as output:
                shutil.copyfileobj(response, output, length=1024 * 1024)
            content_type = response.headers.get_content_type()
            final_url = response.url
    except Exception as error:  # urllib exposes several transport-specific exception classes
        raise SystemExit(f"Download failed (partial file retained for resume): {error}") from error
    temporary.replace(target)
    record = {
        "component_ref": component["bom-ref"],
        "filename": str(target.relative_to(directory)),
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


def verify_migrations(requested_refs: list[str] | None) -> int:
    """Compare every recorded moved-directory manifest to the current files."""
    records = sorted((HUGGINGFACE_DOWNLOAD_ROOT / "migrations").glob("*.json"))
    records.extend(sorted((DOWNLOAD_ROOT / "migrations").glob("*.json")))
    checked = 0
    failures = 0
    for record_path in records:
        record = json.loads(record_path.read_text(encoding="utf-8"))
        ref = record.get("component_ref")
        if requested_refs and ref not in requested_refs:
            continue
        target = Path(record["target"])
        actual = file_manifest(target) if target.is_dir() else None
        status = "ok" if actual == record.get("manifest") else "mismatch"
        print(json.dumps({"component_ref": ref, "target": str(target), "status": status, "file_count": len(actual or [])}, ensure_ascii=False))
        checked += 1
        failures += status != "ok"
    if not checked:
        print("No migration records found beneath .tmp/download/.", file=sys.stderr)
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
    if args.command == "verify-migrations":
        return verify_migrations(args.ref)
    if args.command == "relocate":
        return relocate(component_by_ref(bom, args.ref), args)
    if args.command == "relocate-directory":
        return relocate_directory(component_by_ref(bom, args.ref), args)
    if args.command == "audit-cache":
        return audit_cache(bom, args)
    if args.command == "quarantine":
        return quarantine_cache(bom, args)
    return verify(bom, args.ref)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
