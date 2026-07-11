from __future__ import annotations

import base64
from pathlib import Path

# Keep both language variants together:
# `-en.svg` is the canonical source set for future translation reuse,
# and `-ko.svg` is the current public-facing asset set for Korean pages.

ASSET_DIR = Path(__file__).resolve().parent
HORSE_PHOTO = ASSET_DIR / "horse-field-photo.png"


def write(path: Path, content: str) -> None:
    path.write_text(content + "\n", encoding="utf-8")


def matrix_group(
    x: int,
    y: int,
    values: list[list[int]],
    cell: int,
    fill: str,
    stroke: str,
    text_class: str,
    stroke_width: float = 1.4,
) -> str:
    rows = len(values)
    cols = len(values[0])
    parts = [
        f'<g transform="translate({x} {y})">',
        f'<rect x="0" y="0" width="{cols * cell}" height="{rows * cell}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>',
    ]
    for c in range(1, cols):
        parts.append(
            f'<line x1="{c * cell}" y1="0" x2="{c * cell}" y2="{rows * cell}" stroke="{stroke}" stroke-width="1"/>'
        )
    for r in range(1, rows):
        parts.append(
            f'<line x1="0" y1="{r * cell}" x2="{cols * cell}" y2="{r * cell}" stroke="{stroke}" stroke-width="1"/>'
        )
    for r, row in enumerate(values):
        for c, value in enumerate(row):
            tx = c * cell + cell / 2
            ty = r * cell + cell * 0.72
            parts.append(f'<text class="{text_class}" x="{tx}" y="{ty}" text-anchor="middle">{value}</text>')
    parts.append("</g>")
    return "\n".join(parts)


def layer_stack(
    x: int,
    y: int,
    width: int,
    height: int,
    offsets: list[tuple[int, int]],
    fill: str,
    stroke: str,
    accent_svg: str,
) -> str:
    parts = [f'<g transform="translate({x} {y})">']
    for dx, dy in offsets:
        parts.append(
            f'<rect x="{dx}" y="{dy}" width="{width}" height="{height}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        )
    parts.append(accent_svg)
    parts.append("</g>")
    return "\n".join(parts)


def channel_panel(
    x: int,
    title: str,
    subtitle: str,
    filter_label: str,
    partial_map_label: str,
    patch_fill: str,
    patch_stroke: str,
    patch_values: list[list[int]],
    filter_values: list[list[int]],
    result_values: list[list[int]],
) -> str:
    parts = [
        f'<g transform="translate({x} 386)">',
        '<rect class="panel" x="0" y="0" width="238" height="248"/>',
        f'<text class="panel-title" x="119" y="32" text-anchor="middle">{title}</text>',
        f'<text class="label" x="119" y="56" text-anchor="middle">{subtitle}</text>',
        matrix_group(28, 82, patch_values, 22, patch_fill, patch_stroke, "cell-text"),
        '<g transform="translate(132 84)">',
        f'<text class="label" x="36" y="-12" text-anchor="middle">{filter_label}</text>',
        matrix_group(0, 0, filter_values, 22, "#f0fdf4", "#84cc16", "small-text"),
        "</g>",
        '<line x1="170" y1="150" x2="170" y2="182" stroke="#64748b" stroke-width="2.5" marker-end="url(#arrow)"/>',
        '<g transform="translate(90 206)">',
        f'<text class="label" x="28" y="-14" text-anchor="middle">{partial_map_label}</text>',
        matrix_group(0, 0, result_values, 24, "#ffffff", "#94a3b8", "small-text", 1.2),
        "</g>",
        "</g>",
    ]
    return "\n".join(parts)


def generate_channel_feature_map(lang: str = "en") -> str:
    red_patch = [
        [2, 1, 0, 1],
        [3, 2, 1, 0],
        [1, 2, 3, 1],
        [0, 1, 2, 2],
    ]
    green_patch = [
        [0, 2, 1, 1],
        [1, 3, 2, 0],
        [2, 1, 0, 1],
        [1, 0, 2, 3],
    ]
    blue_patch = [
        [1, 2, 0, 1],
        [0, 1, 2, 2],
        [1, 0, 1, 3],
        [2, 1, 0, 2],
    ]
    red_filter = [
        [1, -1, 0],
        [0, 2, -1],
        [1, 0, 1],
    ]
    green_filter = [
        [0, 1, 1],
        [-1, 1, 0],
        [1, 1, -1],
    ]
    blue_filter = [
        [1, 1, 0],
        [0, -1, 1],
        [1, 0, 1],
    ]
    red_result = [[3, 1], [2, 4]]
    green_result = [[1, 2], [3, 2]]
    blue_result = [[2, 0], [1, 2]]
    final_result = [[6, 3], [6, 8]]

    labels = {
        "en": {
            "title": "One filter reads RGB together, then makes one map",
            "subtitle": "One patch, three channels, one final feature map.",
            "input_title": "Input image with 3 channels",
            "input_subtitle": "the same local patch is separated into red, green, and blue values",
            "red_title": "Red channel",
            "red_subtitle": "patch and filter slice",
            "green_title": "Green channel",
            "green_subtitle": "same filter, green values",
            "blue_title": "Blue channel",
            "blue_subtitle": "same filter, blue values",
            "filter": "filter",
            "partial_map": "partial map",
            "final_map": "Final feature map",
            "svg_title": "One CNN filter spans all input channels and produces one feature map",
            "svg_desc": "A simplified three-channel image patch is separated into red, green, and blue grids. Each channel uses its own filter slice, then the three partial responses are added into one feature map.",
        },
        "ko": {
            "title": "하나의 필터가 RGB를 함께 읽고 하나의 맵을 만든다",
            "subtitle": "하나의 패치, 세 채널, 하나의 최종 특징 맵.",
            "input_title": "3개 채널을 가진 입력 이미지",
            "input_subtitle": "같은 지역 패치를 빨강, 초록, 파랑 값으로 나누어 본다",
            "red_title": "빨강 채널",
            "red_subtitle": "패치와 필터 조각",
            "green_title": "초록 채널",
            "green_subtitle": "같은 필터, 초록 값",
            "blue_title": "파랑 채널",
            "blue_subtitle": "같은 필터, 파랑 값",
            "filter": "필터",
            "partial_map": "부분 맵",
            "final_map": "최종 특징 맵",
            "svg_title": "하나의 CNN 필터가 모든 입력 채널을 함께 읽고 하나의 특징 맵을 만든다",
            "svg_desc": "단순화한 세 채널 이미지 패치를 빨강, 초록, 파랑 격자로 나눈다. 각 채널은 자기 필터 조각과 반응하고, 세 부분 반응을 더해 하나의 특징 맵을 만든다.",
        },
    }[lang]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 820" role="img" aria-labelledby="title desc">
  <title id="title">{labels["svg_title"]}</title>
  <desc id="desc">{labels["svg_desc"]}</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
    </marker>
    <style>
      .title {{ font: 700 24px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #111827; }}
      .subtitle {{ font: 400 16px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #475569; }}
      .panel {{ fill: #f8fafc; stroke: #cbd5e1; stroke-width: 1.4; rx: 16; }}
      .panel-title {{ font: 700 18px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #1f2937; }}
      .label {{ font: 600 13px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #334155; }}
      .cell-text {{ font: 700 18px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill: #0f172a; }}
      .small-text {{ font: 700 16px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill: #0f172a; }}
      .plus {{ font: 700 42px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #475569; }}
    </style>
  </defs>

  <rect width="920" height="820" fill="#ffffff"/>
  <text class="title" x="30" y="42">{labels["title"]}</text>
  <text class="subtitle" x="30" y="70">{labels["subtitle"]}</text>

  <rect x="36" y="102" width="848" height="250" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <text class="panel-title" x="460" y="140" text-anchor="middle">{labels["input_title"]}</text>
  <text class="label" x="460" y="166" text-anchor="middle">{labels["input_subtitle"]}</text>

  <g transform="translate(382 186)">
    <g opacity="0.92">
      <rect x="0" y="0" width="128" height="128" fill="#fee2e2" stroke="#ef4444" stroke-width="1.4"/>
      <line x1="32" y1="0" x2="32" y2="128" stroke="#ef4444" stroke-width="1"/>
      <line x1="64" y1="0" x2="64" y2="128" stroke="#ef4444" stroke-width="1"/>
      <line x1="96" y1="0" x2="96" y2="128" stroke="#ef4444" stroke-width="1"/>
      <line x1="0" y1="32" x2="128" y2="32" stroke="#ef4444" stroke-width="1"/>
      <line x1="0" y1="64" x2="128" y2="64" stroke="#ef4444" stroke-width="1"/>
      <line x1="0" y1="96" x2="128" y2="96" stroke="#ef4444" stroke-width="1"/>
    </g>
    <g transform="translate(14 14)" opacity="0.92">
      <rect x="0" y="0" width="128" height="128" fill="#dcfce7" stroke="#22c55e" stroke-width="1.4"/>
      <line x1="32" y1="0" x2="32" y2="128" stroke="#22c55e" stroke-width="1"/>
      <line x1="64" y1="0" x2="64" y2="128" stroke="#22c55e" stroke-width="1"/>
      <line x1="96" y1="0" x2="96" y2="128" stroke="#22c55e" stroke-width="1"/>
      <line x1="0" y1="32" x2="128" y2="32" stroke="#22c55e" stroke-width="1"/>
      <line x1="0" y1="64" x2="128" y2="64" stroke="#22c55e" stroke-width="1"/>
      <line x1="0" y1="96" x2="128" y2="96" stroke="#22c55e" stroke-width="1"/>
    </g>
    <g transform="translate(28 28)" opacity="0.92">
      <rect x="0" y="0" width="128" height="128" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.4"/>
      <line x1="32" y1="0" x2="32" y2="128" stroke="#7c3aed" stroke-width="1"/>
      <line x1="64" y1="0" x2="64" y2="128" stroke="#7c3aed" stroke-width="1"/>
      <line x1="96" y1="0" x2="96" y2="128" stroke="#7c3aed" stroke-width="1"/>
      <line x1="0" y1="32" x2="128" y2="32" stroke="#7c3aed" stroke-width="1"/>
      <line x1="0" y1="64" x2="128" y2="64" stroke="#7c3aed" stroke-width="1"/>
      <line x1="0" y1="96" x2="128" y2="96" stroke="#7c3aed" stroke-width="1"/>
    </g>
  </g>

  <line x1="426" y1="338" x2="188" y2="376" stroke="#64748b" stroke-width="2.8" marker-end="url(#arrow)"/>
  <line x1="474" y1="338" x2="474" y2="376" stroke="#64748b" stroke-width="2.8" marker-end="url(#arrow)"/>
  <line x1="522" y1="338" x2="650" y2="376" stroke="#64748b" stroke-width="2.8" marker-end="url(#arrow)"/>

  {channel_panel(52, labels["red_title"], labels["red_subtitle"], labels["filter"], labels["partial_map"], "#fee2e2", "#ef4444", red_patch, red_filter, red_result)}
  {channel_panel(340, labels["green_title"], labels["green_subtitle"], labels["filter"], labels["partial_map"], "#dcfce7", "#22c55e", green_patch, green_filter, green_result)}
  {channel_panel(628, labels["blue_title"], labels["blue_subtitle"], labels["filter"], labels["partial_map"], "#ede9fe", "#7c3aed", blue_patch, blue_filter, blue_result)}

  <line x1="170" y1="642" x2="430" y2="728" stroke="#64748b" stroke-width="2.8" marker-end="url(#arrow)"/>
  <line x1="458" y1="642" x2="458" y2="700" stroke="#64748b" stroke-width="2.8" marker-end="url(#arrow)"/>
  <line x1="746" y1="642" x2="486" y2="728" stroke="#64748b" stroke-width="2.8" marker-end="url(#arrow)"/>

  <rect x="324" y="776" width="268" height="32" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <text class="panel-title" x="458" y="798" text-anchor="middle">{labels["final_map"]}</text>
  {matrix_group(432, 704, final_result, 26, "#ffffff", "#2563eb", "cell-text", 1.5)}
</svg>"""


def generate_horse_receptive_field_flow(lang: str = "en") -> str:
    horse_data = base64.b64encode(HORSE_PHOTO.read_bytes()).decode("ascii")
    labels = {
        "en": {
            "svg_title": "CNN layers expand receptive field over the same horse photo",
            "svg_desc": "The same horse photo is reused in three panels. Early convolution reacts to small local regions, deeper layers cover a larger body part, and later layers can gather object-level evidence from a wider area.",
            "title": "CNN receptive field grows over the same photo",
            "subtitle": "The input image stays fixed. Deeper layers can combine a wider region.",
            "stage1": "1. Early conv",
            "stage1_sub": "small field -> edge / texture",
            "stage1_note": "small local response",
            "between1a": "wider",
            "between1b": "context",
            "stage2": "2. Part layer",
            "stage2_sub": "larger field -> head + neck",
            "stage2_note": "part-sized response",
            "between2a": "more",
            "between2b": "evidence",
            "stage3": "3. Object layer",
            "stage3_sub": "part maps -> horse cue",
            "stage3_note": "object-level evidence",
        },
        "ko": {
            "svg_title": "CNN 층이 같은 말 사진 위에서 수용장을 넓혀 간다",
            "svg_desc": "같은 말 사진을 세 패널에 다시 쓴다. 초기 합성곱은 작은 지역 단서에 반응하고, 더 깊은 층은 더 큰 몸체 부분을 덮으며, 뒤쪽 층은 더 넓은 영역에서 객체 수준 단서를 모은다.",
            "title": "CNN 수용장은 같은 사진 위에서 점점 넓어진다",
            "subtitle": "입력 이미지는 그대로이고, 깊은 층일수록 더 넓은 영역을 함께 본다.",
            "stage1": "1. 초기 합성곱",
            "stage1_sub": "작은 범위 -> 경계 / 질감",
            "stage1_note": "작은 지역 반응",
            "between1a": "더 넓은",
            "between1b": "문맥",
            "stage2": "2. 부분 층",
            "stage2_sub": "더 큰 범위 -> 머리 + 목",
            "stage2_note": "부분 크기 반응",
            "between2a": "더 많은",
            "between2b": "단서",
            "stage3": "3. 객체 층",
            "stage3_sub": "부분 맵 -> 말 단서",
            "stage3_note": "객체 수준 단서",
        },
    }[lang]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 420" role="img" aria-labelledby="title desc">
  <title id="title">{labels["svg_title"]}</title>
  <desc id="desc">{labels["svg_desc"]}</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
    </marker>
    <clipPath id="localClip">
      <rect x="40" y="170" width="240" height="200" rx="16"/>
    </clipPath>
    <clipPath id="partClip">
      <rect x="340" y="170" width="240" height="200" rx="16"/>
    </clipPath>
    <clipPath id="objectClip">
      <rect x="640" y="170" width="240" height="200" rx="16"/>
    </clipPath>
    <style>
      .title {{ font: 700 24px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #111827; }}
      .subtitle {{ font: 400 16px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #475569; }}
      .stage-title {{ font: 700 17px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #1f2937; }}
      .label {{ font: 600 14px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #334155; }}
      .note {{ font: 600 16px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #334155; }}
    </style>
  </defs>

  <rect width="920" height="420" fill="#ffffff"/>
  <text class="title" x="30" y="42">{labels["title"]}</text>
  <text class="subtitle" x="30" y="70">{labels["subtitle"]}</text>

  <text class="stage-title" x="40" y="130">{labels["stage1"]}</text>
  <text class="label" x="40" y="152">{labels["stage1_sub"]}</text>
  <rect x="40" y="170" width="240" height="200" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g clip-path="url(#localClip)">
    <image href="data:image/png;base64,{horse_data}" x="-110" y="24" width="540" height="360"/>
  </g>
  <rect x="136" y="236" width="44" height="52" rx="8" fill="none" stroke="#2563eb" stroke-width="4"/>
  <rect x="60" y="382" width="200" height="24" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.8"/>
  <text class="label" x="160" y="398" text-anchor="middle" fill="#2563eb">{labels["stage1_note"]}</text>

  <line x1="286" y1="270" x2="334" y2="270" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>
  <rect x="280" y="214" width="60" height="34" rx="8" fill="#ffffff"/>
  <text class="label" x="310" y="228" text-anchor="middle">
      <tspan x="310" dy="0">{labels["between1a"]}</tspan>
      <tspan x="310" dy="12">{labels["between1b"]}</tspan>
  </text>

  <text class="stage-title" x="340" y="130">{labels["stage2"]}</text>
  <text class="label" x="340" y="152">{labels["stage2_sub"]}</text>
  <rect x="340" y="170" width="240" height="200" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g clip-path="url(#partClip)">
    <image href="data:image/png;base64,{horse_data}" x="184" y="40" width="480" height="320"/>
  </g>
  <rect x="388" y="204" width="116" height="104" rx="10" fill="none" stroke="#16a34a" stroke-width="5"/>
  <rect x="360" y="382" width="200" height="24" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.8"/>
  <text class="label" x="460" y="398" text-anchor="middle" fill="#16a34a">{labels["stage2_note"]}</text>

  <line x1="586" y1="270" x2="634" y2="270" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>
  <rect x="580" y="214" width="60" height="34" rx="8" fill="#ffffff"/>
  <text class="label" x="610" y="228" text-anchor="middle">
      <tspan x="610" dy="0">{labels["between2a"]}</tspan>
      <tspan x="610" dy="12">{labels["between2b"]}</tspan>
  </text>

  <text class="stage-title" x="640" y="130">{labels["stage3"]}</text>
  <text class="label" x="640" y="152">{labels["stage3_sub"]}</text>
  <rect x="640" y="170" width="240" height="200" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g clip-path="url(#objectClip)">
    <image href="data:image/png;base64,{horse_data}" x="640" y="190" width="240" height="160"/>
  </g>
  <rect x="706" y="226" width="118" height="92" rx="10" fill="none" stroke="#ea580c" stroke-width="5"/>
  <rect x="660" y="382" width="200" height="24" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="1.8"/>
  <text class="label" x="760" y="398" text-anchor="middle" fill="#ea580c">{labels["stage3_note"]}</text>
</svg>"""

def generate_feature_map_hierarchy(lang: str = "en") -> str:
    labels = {
        "en": {
            "svg_title": "CNN feature maps combine local responses into larger patterns",
            "svg_desc": "An early feature map reacts to local edges and textures. A deeper part map becomes strong when nearby responses align. A later object map becomes stronger when several part cues appear together.",
            "title": "Feature maps: local response -> part cue -> object cue",
            "subtitle": "Deeper layers combine earlier activations into larger patterns.",
            "card1": "1. Early feature map",
            "card1_sub": "edge or texture response",
            "card1_note": "local patches fire first",
            "combine": "combine",
            "card2": "2. Deeper part map",
            "card2_sub": "part pattern response",
            "card2_note": "part cue becomes stable",
            "gather": "gather",
            "card3": "3. Later object map",
            "card3_sub": "object-level response",
            "card3_note": "object cue can emerge",
            "summary": "Local maps combine into part maps, then object cues.",
        },
        "ko": {
            "svg_title": "CNN 특징 맵은 지역 반응을 더 큰 패턴으로 합친다",
            "svg_desc": "초기 특징 맵은 지역 경계와 질감에 반응한다. 더 깊은 부분 맵은 가까운 반응이 함께 맞을 때 강해지고, 뒤쪽 객체 맵은 여러 부분 단서가 모일 때 더 강해진다.",
            "title": "특징 맵: 지역 반응 -> 부분 단서 -> 객체 단서",
            "subtitle": "깊은 층은 앞선 활성값을 더 큰 패턴으로 합친다.",
            "card1": "1. 초기 특징 맵",
            "card1_sub": "경계 또는 질감 반응",
            "card1_note": "지역 패치가 먼저 반응",
            "combine": "합치기",
            "card2": "2. 더 깊은 부분 맵",
            "card2_sub": "부분 패턴 반응",
            "card2_note": "부분 단서가 안정화됨",
            "gather": "모으기",
            "card3": "3. 뒤쪽 객체 맵",
            "card3_sub": "객체 수준 반응",
            "card3_note": "객체 단서가 나타날 수 있음",
            "summary": "지역 맵이 부분 맵으로, 다시 객체 단서로 합쳐진다.",
        },
    }[lang]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 430" role="img" aria-labelledby="title desc">
  <title id="title">{labels["svg_title"]}</title>
  <desc id="desc">{labels["svg_desc"]}</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
    </marker>
    <style>
      .title {{ font: 700 24px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #111827; }}
      .subtitle {{ font: 400 16px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #475569; }}
      .card-title {{ font: 700 18px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #1f2937; }}
      .label {{ font: 600 14px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #334155; }}
      .note {{ font: 600 16px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #334155; }}
    </style>
  </defs>

  <rect width="920" height="430" fill="#ffffff"/>
  <text class="title" x="30" y="42">{labels["title"]}</text>
  <text class="subtitle" x="30" y="70">{labels["subtitle"]}</text>

  <rect x="40" y="110" width="240" height="240" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <text class="card-title" x="62" y="140">{labels["card1"]}</text>
  <text class="label" x="62" y="162">{labels["card1_sub"]}</text>
  <rect x="86" y="194" width="48" height="48" fill="#dbeafe" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="134" y="194" width="48" height="48" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="182" y="194" width="48" height="48" fill="#dbeafe" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="86" y="242" width="48" height="48" fill="#93c5fd" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="134" y="242" width="48" height="48" fill="#dbeafe" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="182" y="242" width="48" height="48" fill="#60a5fa" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="76" y="310" width="168" height="24" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.6"/>
  <text class="label" x="160" y="326" text-anchor="middle" fill="#2563eb">{labels["card1_note"]}</text>

  <line x1="286" y1="230" x2="334" y2="230" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>
  <text class="label" x="310" y="208" text-anchor="middle">{labels["combine"]}</text>

  <rect x="340" y="110" width="240" height="240" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <text class="card-title" x="362" y="140">{labels["card2"]}</text>
  <text class="label" x="362" y="162">{labels["card2_sub"]}</text>
  <rect x="386" y="194" width="48" height="48" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="434" y="194" width="48" height="48" fill="#86efac" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="482" y="194" width="48" height="48" fill="#4ade80" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="386" y="242" width="48" height="48" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="434" y="242" width="48" height="48" fill="#bbf7d0" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="482" y="242" width="48" height="48" fill="#86efac" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="376" y="310" width="168" height="24" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.6"/>
  <text class="label" x="460" y="326" text-anchor="middle" fill="#16a34a">{labels["card2_note"]}</text>

  <line x1="586" y1="230" x2="634" y2="230" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>
  <text class="label" x="610" y="208" text-anchor="middle">{labels["gather"]}</text>

  <rect x="640" y="110" width="240" height="240" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <text class="card-title" x="662" y="140">{labels["card3"]}</text>
  <text class="label" x="662" y="162">{labels["card3_sub"]}</text>
  <rect x="700" y="194" width="64" height="64" fill="#fed7aa" stroke="#ea580c" stroke-width="1.2"/>
  <rect x="764" y="194" width="64" height="64" fill="#fb923c" stroke="#ea580c" stroke-width="1.2"/>
  <rect x="732" y="258" width="64" height="32" fill="#fdba74" stroke="#ea580c" stroke-width="1.2"/>
  <rect x="676" y="310" width="168" height="24" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="1.6"/>
  <text class="label" x="760" y="326" text-anchor="middle" fill="#ea580c">{labels["card3_note"]}</text>

  <rect x="180" y="376" width="560" height="24" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
  <text class="note" x="460" y="393" text-anchor="middle">{labels["summary"]}</text>
</svg>"""


def main() -> None:
    write(ASSET_DIR / "cnn-channel-feature-map-en.svg", generate_channel_feature_map("en"))
    write(ASSET_DIR / "cnn-channel-feature-map-ko.svg", generate_channel_feature_map("ko"))
    write(ASSET_DIR / "cnn-hierarchical-vision-flow-en.svg", generate_horse_receptive_field_flow("en"))
    write(ASSET_DIR / "cnn-hierarchical-vision-flow-ko.svg", generate_horse_receptive_field_flow("ko"))
    write(ASSET_DIR / "cnn-feature-map-hierarchy-en.svg", generate_feature_map_hierarchy("en"))
    write(ASSET_DIR / "cnn-feature-map-hierarchy-ko.svg", generate_feature_map_hierarchy("ko"))


if __name__ == "__main__":
    main()
