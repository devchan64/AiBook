"""Generate initial gateway reports for manuscript translation quality.

The script compares Korean source Markdown files with localized manuscript
files such as ``section-01.en.md`` or ``section-01.zh.md``. It combines
deterministic checks from the repository translation guidelines with an
optional sliding-window Ollama review to decide whether each file needs
additional translation or focused human review before it proceeds.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


SUPPORTED_LOCALES = {"en": "English", "zh": "Simplified Chinese"}
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:14b")
DEFAULT_REPORT_DIR = Path("management/authoring/translation-quality")
METADATA_RE = re.compile(r"^\s*(Section ID|Version)\s*:\s*(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")


@dataclasses.dataclass(frozen=True)
class FilePair:
    source: Path
    target: Path
    locale: str


@dataclasses.dataclass(frozen=True)
class DeterministicChecks:
    source_nonblank_lines: int
    target_nonblank_lines: int
    line_delta_percent: float
    source_metadata: dict[str, str]
    target_metadata: dict[str, str]
    metadata_mismatches: list[str]
    source_heading_count: int
    target_heading_count: int
    heading_count_delta: int
    source_link_count: int
    target_link_count: int
    link_count_delta: int
    source_code_fence_count: int
    target_code_fence_count: int
    code_fence_delta: int
    warnings: list[str]


@dataclasses.dataclass(frozen=True)
class LlmReview:
    score: int | None
    status: str
    summary: str
    issues: list[str]
    suggestions: list[str]
    raw: str


@dataclasses.dataclass(frozen=True)
class Segment:
    index: int
    title: str
    source_text: str
    target_text: str
    source_context: str
    target_context: str


@dataclasses.dataclass(frozen=True)
class SegmentReview:
    index: int
    title: str
    score: int | None
    status: str
    summary: str
    issues: list[str]
    suggestions: list[str]
    raw: str


@dataclasses.dataclass(frozen=True)
class PairReport:
    pair: FilePair
    checks: DeterministicChecks
    llm_review: LlmReview | None
    segment_reviews: list[SegmentReview]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an Ollama-backed initial gateway report for translated manuscripts.",
    )
    parser.add_argument(
        "--locale",
        required=True,
        choices=sorted(SUPPORTED_LOCALES),
        help="Target locale suffix to inspect. Supported: en, zh.",
    )
    parser.add_argument(
        "--root",
        default="docs/parts",
        type=Path,
        help="Directory to scan for manuscript Markdown files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Markdown report path. Defaults to management/authoring/translation-quality/.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Ollama model name. Can also be set with OLLAMA_MODEL.",
    )
    parser.add_argument(
        "--ollama-host",
        default=os.environ.get("OLLAMA_HOST"),
        help="Optional Ollama host URL. Can also be set with OLLAMA_HOST.",
    )
    parser.add_argument(
        "--skip-llm",
        action="store_true",
        help="Skip Ollama review and run deterministic checks only.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=12000,
        help="Maximum characters per source or target text sent to Ollama for full-file review.",
    )
    parser.add_argument(
        "--segment-max-chars",
        type=int,
        default=5000,
        help="Maximum characters per source or target segment sent to Ollama.",
    )
    parser.add_argument(
        "--context-lines",
        type=int,
        default=2,
        help="Neighboring lines added around each segment for sliding-context review.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit the number of translated files reviewed.",
    )
    parser.add_argument(
        "--include-missing",
        action="store_true",
        help="Also report Korean source files without a target translation.",
    )
    parser.add_argument(
        "--fail-on-review",
        action="store_true",
        help="Exit with code 3 when any file needs additional translation or review.",
    )
    return parser.parse_args(argv)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def nonblank_line_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def extract_metadata(text: str) -> dict[str, str]:
    return {match.group(1): match.group(2) for match in METADATA_RE.finditer(text)}


def count_code_fences(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip().startswith("```"))


def deterministic_checks(source_text: str, target_text: str) -> DeterministicChecks:
    source_lines = nonblank_line_count(source_text)
    target_lines = nonblank_line_count(target_text)
    line_delta_percent = 0.0
    if source_lines:
        line_delta_percent = abs(target_lines - source_lines) / source_lines * 100

    source_metadata = extract_metadata(source_text)
    target_metadata = extract_metadata(target_text)
    metadata_mismatches: list[str] = []
    for key in ("Section ID", "Version"):
        if source_metadata.get(key) != target_metadata.get(key):
            metadata_mismatches.append(
                f"{key}: source={source_metadata.get(key, '<missing>')} "
                f"target={target_metadata.get(key, '<missing>')}"
            )

    source_headings = HEADING_RE.findall(source_text)
    target_headings = HEADING_RE.findall(target_text)
    source_links = LINK_RE.findall(source_text)
    target_links = LINK_RE.findall(target_text)
    source_fences = count_code_fences(source_text)
    target_fences = count_code_fences(target_text)

    warnings: list[str] = []
    if line_delta_percent >= 5:
        warnings.append(
            f"Nonblank line delta is {line_delta_percent:.1f}%, above the 5% guideline signal."
        )
    if metadata_mismatches:
        warnings.append("Section metadata does not match the Korean source.")
    if len(source_headings) != len(target_headings):
        warnings.append("Heading count differs from the Korean source.")
    if source_fences != target_fences:
        warnings.append("Code fence count differs from the Korean source.")

    return DeterministicChecks(
        source_nonblank_lines=source_lines,
        target_nonblank_lines=target_lines,
        line_delta_percent=line_delta_percent,
        source_metadata=source_metadata,
        target_metadata=target_metadata,
        metadata_mismatches=metadata_mismatches,
        source_heading_count=len(source_headings),
        target_heading_count=len(target_headings),
        heading_count_delta=len(target_headings) - len(source_headings),
        source_link_count=len(source_links),
        target_link_count=len(target_links),
        link_count_delta=len(target_links) - len(source_links),
        source_code_fence_count=source_fences,
        target_code_fence_count=target_fences,
        code_fence_delta=target_fences - source_fences,
        warnings=warnings,
    )


def is_localized_markdown(path: Path) -> bool:
    return any(path.name.endswith(f".{locale}.md") for locale in SUPPORTED_LOCALES)


def source_for_target(target: Path, locale: str) -> Path:
    suffix = f".{locale}.md"
    if not target.name.endswith(suffix):
        raise ValueError(f"Not a .{locale}.md file: {target}")
    return target.with_name(target.name[: -len(suffix)] + ".md")


def target_for_source(source: Path, locale: str) -> Path:
    return source.with_name(source.stem + f".{locale}.md")


def discover_pairs(root: Path, locale: str, include_missing: bool) -> list[FilePair]:
    translated_targets = sorted(root.rglob(f"*.{locale}.md"))
    pairs = [
        FilePair(source=source_for_target(target, locale), target=target, locale=locale)
        for target in translated_targets
    ]

    if include_missing:
        known_sources = {pair.source for pair in pairs}
        for source in sorted(root.rglob("*.md")):
            if is_localized_markdown(source) or source in known_sources:
                continue
            target = target_for_source(source, locale)
            if not target.exists():
                pairs.append(FilePair(source=source, target=target, locale=locale))

    return sorted(pairs, key=lambda pair: str(pair.target))


def truncate_for_prompt(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    head = max_chars // 2
    tail = max_chars - head
    return (
        text[:head]
        + "\n\n[... middle omitted for prompt length ...]\n\n"
        + text[-tail:]
    )


def split_markdown_sections(text: str) -> list[tuple[str, str]]:
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        return [("문서 전체", text)]

    sections: list[tuple[str, str]] = []
    if matches[0].start() > 0 and text[: matches[0].start()].strip():
        sections.append(("문서 앞부분", text[: matches[0].start()].strip()))

    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(2).strip(), text[start:end].strip()))

    return sections


def neighbor_context(sections: list[tuple[str, str]], index: int, context_lines: int) -> str:
    context_parts: list[str] = []
    if index > 0:
        previous_lines = sections[index - 1][1].splitlines()
        context_parts.append("\n".join(previous_lines[-context_lines:]))
    if index + 1 < len(sections):
        next_lines = sections[index + 1][1].splitlines()
        context_parts.append("\n".join(next_lines[:context_lines]))
    return "\n\n".join(part for part in context_parts if part.strip())


def split_heading_segments(source_text: str, target_text: str, context_lines: int) -> list[Segment]:
    source_sections = split_markdown_sections(source_text)
    target_sections = split_markdown_sections(target_text)
    count = min(len(source_sections), len(target_sections))
    segments: list[Segment] = []
    for index in range(count):
        source_title, source_body = source_sections[index]
        _target_title, target_body = target_sections[index]
        segments.append(
            Segment(
                index=index + 1,
                title=source_title,
                source_text=source_body,
                target_text=target_body,
                source_context=neighbor_context(source_sections, index, context_lines),
                target_context=neighbor_context(target_sections, index, context_lines),
            )
        )
    return segments


def build_llm_prompt(
    pair: FilePair,
    source_text: str,
    target_text: str,
    checks: DeterministicChecks,
    max_chars: int,
) -> str:
    target_language = SUPPORTED_LOCALES[pair.locale]
    source_excerpt = truncate_for_prompt(source_text, max_chars)
    target_excerpt = truncate_for_prompt(target_text, max_chars)

    return f"""You are reviewing a translated Markdown manuscript for AiBook.

Evaluate whether the target manuscript preserves the Korean source's learning role,
scope, conceptual sequence, examples, cautions, metadata, links, tables, and code blocks.
Do not rewrite the full manuscript. Report actionable issues only.

Repository translation quality rules to apply:
- The target should answer the same central question as the Korean source.
- Section ID and Version should match the Korean source.
- The target should not add unsupported new claims, examples, or scope.
- A nonblank line-count delta of 5% or more is a signal to check for omission,
  over-compression, or formatting-driven exceptions.
- Terms such as inference, reasoning, prediction, generation, model, parameter,
  level, and layer should remain contextually distinct.
- Internal links should prefer the same-language target when available.
- Glossary direct links should not be overused.

Return strict JSON with these keys:
{{
  "score": 1,
  "status": "pass|review|fail",
  "summary": "one or two Korean sentences",
  "issues": ["Korean bullet item", "..."],
  "suggestions": ["Korean bullet item", "..."]
}}

Score meaning:
5 = publishable after light proofreading
4 = mostly good, minor fixes
3 = usable but needs focused review
2 = substantial omissions or meaning shifts
1 = not reliable

Target language: {target_language}
Source file: {pair.source}
Target file: {pair.target}
Deterministic check summary:
- Source nonblank lines: {checks.source_nonblank_lines}
- Target nonblank lines: {checks.target_nonblank_lines}
- Line delta percent: {checks.line_delta_percent:.1f}
- Metadata mismatches: {checks.metadata_mismatches or "none"}
- Heading count delta: {checks.heading_count_delta}
- Link count delta: {checks.link_count_delta}
- Code fence delta: {checks.code_fence_delta}

Korean source Markdown:
```markdown
{source_excerpt}
```

Translated Markdown:
```markdown
{target_excerpt}
```
"""


def build_segment_prompt(pair: FilePair, segment: Segment, max_chars: int) -> str:
    target_language = SUPPORTED_LOCALES[pair.locale]
    source_segment = truncate_for_prompt(segment.source_text, max_chars)
    target_segment = truncate_for_prompt(segment.target_text, max_chars)
    source_context = truncate_for_prompt(segment.source_context, max_chars // 3)
    target_context = truncate_for_prompt(segment.target_context, max_chars // 3)

    return f"""You are running a sliding-window gateway review for one translated Markdown segment.

Use the neighboring context only to understand continuity. Judge the target segment itself.
Detect omissions, over-compression, meaning shifts, unsupported additions, broken examples,
term drift, and link or formatting problems. Do not rewrite the full segment.

Return strict JSON with these keys:
{{
  "score": 1,
  "status": "pass|review|fail",
  "summary": "one Korean sentence",
  "issues": ["Korean bullet item", "..."],
  "suggestions": ["Korean bullet item", "..."]
}}

Status meaning:
- pass: no additional translation signal in this segment
- review: human review is needed before accepting this segment
- fail: additional translation is likely required

Target language: {target_language}
Source file: {pair.source}
Target file: {pair.target}
Segment index: {segment.index}
Segment title: {segment.title}

Korean neighboring context:
```markdown
{source_context}
```

Translated neighboring context:
```markdown
{target_context}
```

Korean segment:
```markdown
{source_segment}
```

Translated segment:
```markdown
{target_segment}
```
"""


def parse_llm_json(raw: str) -> dict[str, Any]:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def normalize_review(data: dict[str, Any], raw: str) -> LlmReview:
    score = data.get("score")
    if not isinstance(score, int) or score < 1 or score > 5:
        score = None

    status = data.get("status")
    if status not in {"pass", "review", "fail"}:
        status = "review"

    summary = data.get("summary")
    if not isinstance(summary, str):
        summary = ""

    issues = data.get("issues")
    if not isinstance(issues, list):
        issues = []
    issues = [str(item) for item in issues]

    suggestions = data.get("suggestions")
    if not isinstance(suggestions, list):
        suggestions = []
    suggestions = [str(item) for item in suggestions]

    return LlmReview(
        score=score,
        status=status,
        summary=summary,
        issues=issues,
        suggestions=suggestions,
        raw=raw,
    )


def normalize_segment_review(segment: Segment, data: dict[str, Any], raw: str) -> SegmentReview:
    review = normalize_review(data, raw)
    return SegmentReview(
        index=segment.index,
        title=segment.title,
        score=review.score,
        status=review.status,
        summary=review.summary,
        issues=review.issues,
        suggestions=review.suggestions,
        raw=review.raw,
    )


def run_ollama_review(
    pair: FilePair,
    source_text: str,
    target_text: str,
    checks: DeterministicChecks,
    model: str,
    host: str | None,
    max_chars: int,
) -> LlmReview:
    try:
        import ollama
    except ImportError as exc:
        raise RuntimeError(
            "The ollama Python package is not installed. Install requirements.txt "
            "or rerun with --skip-llm."
        ) from exc

    client = ollama.Client(host=host) if host else ollama.Client()
    prompt = build_llm_prompt(pair, source_text, target_text, checks, max_chars)
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"temperature": 0.1},
    )
    raw = response["message"]["content"]
    try:
        return normalize_review(parse_llm_json(raw), raw)
    except json.JSONDecodeError:
        return LlmReview(
            score=None,
            status="review",
            summary="Ollama 응답을 JSON으로 해석하지 못했습니다.",
            issues=["원문 응답을 확인해야 합니다."],
            suggestions=["같은 명령을 다시 실행하거나 다른 모델을 지정하세요."],
            raw=raw,
        )


def run_segment_review(
    client: Any,
    pair: FilePair,
    segment: Segment,
    model: str,
    max_chars: int,
) -> SegmentReview:
    prompt = build_segment_prompt(pair, segment, max_chars)
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"temperature": 0.1},
    )
    raw = response["message"]["content"]
    try:
        return normalize_segment_review(segment, parse_llm_json(raw), raw)
    except json.JSONDecodeError:
        return SegmentReview(
            index=segment.index,
            title=segment.title,
            score=None,
            status="review",
            summary="Ollama 구간 응답을 JSON으로 해석하지 못했습니다.",
            issues=["원문 응답을 확인해야 합니다."],
            suggestions=["같은 명령을 다시 실행하거나 다른 모델을 지정하세요."],
            raw=raw,
        )


def run_segment_reviews(
    pair: FilePair,
    source_text: str,
    target_text: str,
    model: str,
    host: str | None,
    segment_max_chars: int,
    context_lines: int,
) -> list[SegmentReview]:
    try:
        import ollama
    except ImportError as exc:
        raise RuntimeError(
            "The ollama Python package is not installed. Install requirements.txt "
            "or rerun with --skip-llm."
        ) from exc

    client = ollama.Client(host=host) if host else ollama.Client()
    segments = split_heading_segments(source_text, target_text, context_lines)
    return [
        run_segment_review(
            client=client,
            pair=pair,
            segment=segment,
            model=model,
            max_chars=segment_max_chars,
        )
        for segment in segments
    ]


def make_missing_report(pair: FilePair) -> PairReport:
    checks = DeterministicChecks(
        source_nonblank_lines=0,
        target_nonblank_lines=0,
        line_delta_percent=0.0,
        source_metadata={},
        target_metadata={},
        metadata_mismatches=["Target translation file is missing."],
        source_heading_count=0,
        target_heading_count=0,
        heading_count_delta=0,
        source_link_count=0,
        target_link_count=0,
        link_count_delta=0,
        source_code_fence_count=0,
        target_code_fence_count=0,
        code_fence_delta=0,
        warnings=["Target translation file is missing."],
    )
    review = LlmReview(
        score=None,
        status="fail",
        summary="번역 파일이 없습니다.",
        issues=["대응 번역 파일이 없어 품질 검수를 수행할 수 없습니다."],
        suggestions=[f"`{pair.target}` 파일을 만든 뒤 다시 실행하세요."],
        raw="",
    )
    return PairReport(pair=pair, checks=checks, llm_review=review, segment_reviews=[])


def make_report(
    pair: FilePair,
    model: str,
    host: str | None,
    skip_llm: bool,
    max_chars: int,
    segment_max_chars: int,
    context_lines: int,
) -> PairReport:
    if not pair.target.exists():
        return make_missing_report(pair)
    if not pair.source.exists():
        raise FileNotFoundError(f"Missing Korean source for {pair.target}: {pair.source}")

    source_text = read_text(pair.source)
    target_text = read_text(pair.target)
    checks = deterministic_checks(source_text, target_text)
    llm_review = None
    segment_reviews: list[SegmentReview] = []
    if not skip_llm:
        segment_reviews = run_segment_reviews(
            pair=pair,
            source_text=source_text,
            target_text=target_text,
            model=model,
            host=host,
            segment_max_chars=segment_max_chars,
            context_lines=context_lines,
        )
        llm_review = run_ollama_review(
            pair=pair,
            source_text=source_text,
            target_text=target_text,
            checks=checks,
            model=model,
            host=host,
            max_chars=max_chars,
        )

    return PairReport(
        pair=pair,
        checks=checks,
        llm_review=llm_review,
        segment_reviews=segment_reviews,
    )


def status_for_report(report: PairReport) -> str:
    if report.llm_review:
        return report.llm_review.status
    if report.checks.warnings:
        return "review"
    return "pass"


def needs_additional_translation(report: PairReport) -> bool:
    if any(review.status in {"review", "fail"} for review in report.segment_reviews):
        return True
    if report.llm_review and report.llm_review.status in {"review", "fail"}:
        return True
    return bool(report.checks.warnings)


def gateway_decision_for_report(report: PairReport) -> str:
    if any(review.status == "fail" for review in report.segment_reviews):
        return "추가 번역 필요"
    if report.llm_review and report.llm_review.status == "fail":
        return "추가 번역 필요"
    if any(review.status == "review" for review in report.segment_reviews):
        return "번역 검수 필요"
    if report.llm_review and report.llm_review.status == "review":
        return "번역 검수 필요"
    if report.checks.warnings:
        return "기계 점검 확인 필요"
    return "통과"


def score_for_report(report: PairReport) -> str:
    segment_scores = [
        review.score for review in report.segment_reviews if review.score is not None
    ]
    if segment_scores:
        return str(min(segment_scores))
    if report.llm_review and report.llm_review.score is not None:
        return str(report.llm_review.score)
    return "-"


def markdown_list(items: list[str]) -> str:
    if not items:
        return "- 없음\n"
    return "".join(f"- {item}\n" for item in items)


def render_markdown(reports: list[PairReport], locale: str, model: str, skip_llm: bool) -> str:
    now = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    status_counts: dict[str, int] = {"pass": 0, "review": 0, "fail": 0}
    for report in reports:
        status_counts[status_for_report(report)] = status_counts.get(status_for_report(report), 0) + 1
    blocked_count = sum(1 for report in reports if needs_additional_translation(report))
    passed_count = len(reports) - blocked_count
    gate_result = "통과" if blocked_count == 0 else "추가 번역 또는 검수 필요"

    lines = [
        f"# 번역 게이트웨이 리포트: {locale}",
        "",
        f"- 생성 시각: {now}",
        f"- 대상 언어: {SUPPORTED_LOCALES[locale]} (`{locale}`)",
        f"- Ollama 모델: {'사용 안 함' if skip_llm else model}",
        f"- 분석 방식: {'기계 점검만 수행' if skip_llm else '제목 구간 기반 슬라이딩 검수 + 전체 파일 검수'}",
        f"- 파일 수: {len(reports)}",
        f"- 게이트 판정: {gate_result}",
        f"- 통과 파일 수: {passed_count}",
        f"- 추가 번역 또는 검수 필요 파일 수: {blocked_count}",
        f"- 상태 요약: pass {status_counts.get('pass', 0)}, review {status_counts.get('review', 0)}, fail {status_counts.get('fail', 0)}",
        "",
        "이 리포트는 최종 편집 승인서가 아니라, 추가 번역이 필요한 산출물을 초기에 걸러내기 위한 게이트웨이 점검 결과다.",
        "",
        "## 파일별 요약",
        "",
        "| 게이트 판정 | 상태 | 점수 | 원문 | 번역본 | 줄 수 차이 | 경고 수 |",
        "| --- | --- | --- | --- | --- | ---: | ---: |",
    ]

    for report in reports:
        checks = report.checks
        flagged_segment_count = sum(
            1 for review in report.segment_reviews if review.status in {"review", "fail"}
        )
        lines.append(
            "| {decision} | {status} | {score} | `{source}` | `{target}` | {delta:.1f}% | {warnings} |".format(
                decision=gateway_decision_for_report(report),
                status=status_for_report(report),
                score=score_for_report(report),
                source=report.pair.source,
                target=report.pair.target,
                delta=checks.line_delta_percent,
                warnings=len(checks.warnings) + flagged_segment_count,
            )
        )

    lines.extend(["", "## 상세", ""])
    for report in reports:
        checks = report.checks
        review = report.llm_review
        lines.extend(
            [
                f"### `{report.pair.target}`",
                "",
                f"- 원문: `{report.pair.source}`",
                f"- 게이트 판정: `{gateway_decision_for_report(report)}`",
                f"- 상태: `{status_for_report(report)}`",
                f"- 점수: `{score_for_report(report)}`",
                f"- 빈 줄 제외 라인 수: 원문 {checks.source_nonblank_lines}, 번역본 {checks.target_nonblank_lines}, 차이 {checks.line_delta_percent:.1f}%",
                f"- 제목 수 차이: {checks.heading_count_delta}",
                f"- 링크 수 차이: {checks.link_count_delta}",
                f"- 코드 펜스 수 차이: {checks.code_fence_delta}",
                "",
                "기계 점검 경고:",
                "",
                markdown_list(checks.warnings),
            ]
        )
        if checks.metadata_mismatches:
            lines.extend(["메타데이터 불일치:", "", markdown_list(checks.metadata_mismatches)])
        if review:
            lines.extend(
                [
                    "Ollama 요약:",
                    "",
                    review.summary or "-",
                    "",
                    "주요 이슈:",
                    "",
                    markdown_list(review.issues),
                    "수정 제안:",
                    "",
                    markdown_list(review.suggestions),
                ]
            )
        if report.segment_reviews:
            flagged_segments = [
                segment
                for segment in report.segment_reviews
                if segment.status in {"review", "fail"}
            ]
            lines.extend(["구간별 슬라이딩 검수:", ""])
            if not flagged_segments:
                lines.append("- 추가 번역 신호가 있는 구간 없음\n")
            for segment in flagged_segments:
                lines.extend(
                    [
                        f"#### 구간 {segment.index}. {segment.title}",
                        "",
                        f"- 상태: `{segment.status}`",
                        f"- 점수: `{segment.score if segment.score is not None else '-'}`",
                        f"- 요약: {segment.summary or '-'}",
                        "",
                        "이슈:",
                        "",
                        markdown_list(segment.issues),
                        "수정 제안:",
                        "",
                        markdown_list(segment.suggestions),
                    ]
                )
        lines.append("")

    return "\n".join(lines)


def default_output_path(locale: str) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return DEFAULT_REPORT_DIR / f"translation-quality-{locale}-{stamp}.md"


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.root
    if not root.exists():
        print(f"Root directory does not exist: {root}", file=sys.stderr)
        return 2

    pairs = discover_pairs(root=root, locale=args.locale, include_missing=args.include_missing)
    if args.limit is not None:
        pairs = pairs[: args.limit]
    if not pairs:
        print(f"No .{args.locale}.md translation files found under {root}", file=sys.stderr)
        return 1

    reports: list[PairReport] = []
    for index, pair in enumerate(pairs, start=1):
        print(f"[{index}/{len(pairs)}] reviewing {pair.target}", file=sys.stderr)
        reports.append(
            make_report(
                pair=pair,
                model=args.model,
                host=args.ollama_host,
                skip_llm=args.skip_llm,
                max_chars=args.max_chars,
                segment_max_chars=args.segment_max_chars,
                context_lines=args.context_lines,
            )
        )

    output = args.output or default_output_path(args.locale)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_markdown(reports, locale=args.locale, model=args.model, skip_llm=args.skip_llm),
        encoding="utf-8",
    )
    print(f"Wrote report: {output}")
    if args.fail_on_review and any(needs_additional_translation(report) for report in reports):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
