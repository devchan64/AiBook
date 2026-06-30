from __future__ import annotations

import base64
from pathlib import Path


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
        '<text class="label" x="36" y="-12" text-anchor="middle">filter</text>',
        matrix_group(0, 0, filter_values, 22, "#f0fdf4", "#84cc16", "small-text"),
        "</g>",
        '<line x1="170" y1="150" x2="170" y2="182" stroke="#64748b" stroke-width="2.5" marker-end="url(#arrow)"/>',
        '<g transform="translate(90 206)">',
        '<text class="label" x="28" y="-14" text-anchor="middle">partial map</text>',
        matrix_group(0, 0, result_values, 24, "#ffffff", "#94a3b8", "small-text", 1.2),
        "</g>",
        "</g>",
    ]
    return "\n".join(parts)


def generate_channel_feature_map() -> str:
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

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 820" role="img" aria-labelledby="title desc">
  <title id="title">One CNN filter spans all input channels and produces one feature map</title>
  <desc id="desc">A simplified three-channel image patch is separated into red, green, and blue grids. Each channel uses its own filter slice, then the three partial responses are added into one feature map.</desc>
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
  <text class="title" x="30" y="42">One filter reads RGB together, then makes one map</text>
  <text class="subtitle" x="30" y="70">One patch, three channels, one final feature map.</text>

  <rect x="36" y="102" width="848" height="250" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <text class="panel-title" x="460" y="140" text-anchor="middle">Input image with 3 channels</text>
  <text class="label" x="460" y="166" text-anchor="middle">the same local patch is separated into red, green, and blue values</text>

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

  {channel_panel(52, "Red channel", "patch and filter slice", "#fee2e2", "#ef4444", red_patch, red_filter, red_result)}
  {channel_panel(340, "Green channel", "same filter, green values", "#dcfce7", "#22c55e", green_patch, green_filter, green_result)}
  {channel_panel(628, "Blue channel", "same filter, blue values", "#ede9fe", "#7c3aed", blue_patch, blue_filter, blue_result)}

  <line x1="170" y1="642" x2="430" y2="728" stroke="#64748b" stroke-width="2.8" marker-end="url(#arrow)"/>
  <line x1="458" y1="642" x2="458" y2="700" stroke="#64748b" stroke-width="2.8" marker-end="url(#arrow)"/>
  <line x1="746" y1="642" x2="486" y2="728" stroke="#64748b" stroke-width="2.8" marker-end="url(#arrow)"/>

  <rect x="324" y="776" width="268" height="32" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <text class="panel-title" x="458" y="798" text-anchor="middle">Final feature map</text>
  {matrix_group(432, 704, final_result, 26, "#ffffff", "#2563eb", "cell-text", 1.5)}
</svg>"""


def generate_horse_receptive_field_flow() -> str:
    horse_data = base64.b64encode(HORSE_PHOTO.read_bytes()).decode("ascii")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 420" role="img" aria-labelledby="title desc">
  <title id="title">CNN layers expand receptive field over the same horse photo</title>
  <desc id="desc">The same horse photo is reused in three panels. Early convolution reacts to small local regions, deeper layers cover a larger body part, and later layers can gather object-level evidence from a wider area.</desc>
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
  <text class="title" x="30" y="42">CNN receptive field grows over the same photo</text>
  <text class="subtitle" x="30" y="70">The input image stays fixed. Deeper layers can combine a wider region.</text>

  <text class="stage-title" x="40" y="130">1. Early conv</text>
  <text class="label" x="40" y="152">small field -> edge / texture</text>
  <rect x="40" y="170" width="240" height="200" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g clip-path="url(#localClip)">
    <image href="data:image/png;base64,{horse_data}" x="-110" y="24" width="540" height="360"/>
  </g>
  <rect x="136" y="236" width="44" height="52" rx="8" fill="none" stroke="#2563eb" stroke-width="4"/>
  <rect x="60" y="382" width="200" height="24" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.8"/>
  <text class="label" x="160" y="398" text-anchor="middle" fill="#2563eb">small local response</text>

  <line x1="286" y1="270" x2="334" y2="270" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>
  <rect x="280" y="214" width="60" height="34" rx="8" fill="#ffffff"/>
  <text class="label" x="310" y="228" text-anchor="middle">
    <tspan x="310" dy="0">wider</tspan>
    <tspan x="310" dy="12">context</tspan>
  </text>

  <text class="stage-title" x="340" y="130">2. Part layer</text>
  <text class="label" x="340" y="152">larger field -> head + neck</text>
  <rect x="340" y="170" width="240" height="200" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g clip-path="url(#partClip)">
    <image href="data:image/png;base64,{horse_data}" x="184" y="40" width="480" height="320"/>
  </g>
  <rect x="388" y="204" width="116" height="104" rx="10" fill="none" stroke="#16a34a" stroke-width="5"/>
  <rect x="360" y="382" width="200" height="24" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.8"/>
  <text class="label" x="460" y="398" text-anchor="middle" fill="#16a34a">part-sized response</text>

  <line x1="586" y1="270" x2="634" y2="270" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>
  <rect x="580" y="214" width="60" height="34" rx="8" fill="#ffffff"/>
  <text class="label" x="610" y="228" text-anchor="middle">
    <tspan x="610" dy="0">more</tspan>
    <tspan x="610" dy="12">evidence</tspan>
  </text>

  <text class="stage-title" x="640" y="130">3. Object layer</text>
  <text class="label" x="640" y="152">part maps -> horse cue</text>
  <rect x="640" y="170" width="240" height="200" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g clip-path="url(#objectClip)">
    <image href="data:image/png;base64,{horse_data}" x="640" y="190" width="240" height="160"/>
  </g>
  <rect x="706" y="226" width="118" height="92" rx="10" fill="none" stroke="#ea580c" stroke-width="5"/>
  <rect x="660" y="382" width="200" height="24" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="1.8"/>
  <text class="label" x="760" y="398" text-anchor="middle" fill="#ea580c">object-level evidence</text>
</svg>"""

def generate_feature_map_hierarchy() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 430" role="img" aria-labelledby="title desc">
  <title id="title">CNN feature maps combine local responses into larger patterns</title>
  <desc id="desc">An early feature map reacts to local edges and textures. A deeper part map becomes strong when nearby responses align. A later object map becomes stronger when several part cues appear together.</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
    </marker>
    <style>
      .title { font: 700 24px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #111827; }
      .subtitle { font: 400 16px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #475569; }
      .card-title { font: 700 18px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #1f2937; }
      .label { font: 600 14px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #334155; }
      .note { font: 600 16px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #334155; }
    </style>
  </defs>

  <rect width="920" height="430" fill="#ffffff"/>
  <text class="title" x="30" y="42">Feature maps: local response -> part cue -> object cue</text>
  <text class="subtitle" x="30" y="70">Deeper layers combine earlier activations into larger patterns.</text>

  <rect x="40" y="110" width="240" height="240" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <text class="card-title" x="62" y="140">1. Early feature map</text>
  <text class="label" x="62" y="162">edge or texture response</text>
  <rect x="86" y="194" width="48" height="48" fill="#dbeafe" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="134" y="194" width="48" height="48" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="182" y="194" width="48" height="48" fill="#dbeafe" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="86" y="242" width="48" height="48" fill="#93c5fd" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="134" y="242" width="48" height="48" fill="#dbeafe" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="182" y="242" width="48" height="48" fill="#60a5fa" stroke="#2563eb" stroke-width="1.2"/>
  <rect x="76" y="310" width="168" height="24" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.6"/>
  <text class="label" x="160" y="326" text-anchor="middle" fill="#2563eb">local patches fire first</text>

  <line x1="286" y1="230" x2="334" y2="230" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>
  <text class="label" x="310" y="208" text-anchor="middle">combine</text>

  <rect x="340" y="110" width="240" height="240" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <text class="card-title" x="362" y="140">2. Deeper part map</text>
  <text class="label" x="362" y="162">part pattern response</text>
  <rect x="386" y="194" width="48" height="48" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="434" y="194" width="48" height="48" fill="#86efac" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="482" y="194" width="48" height="48" fill="#4ade80" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="386" y="242" width="48" height="48" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="434" y="242" width="48" height="48" fill="#bbf7d0" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="482" y="242" width="48" height="48" fill="#86efac" stroke="#16a34a" stroke-width="1.2"/>
  <rect x="376" y="310" width="168" height="24" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.6"/>
  <text class="label" x="460" y="326" text-anchor="middle" fill="#16a34a">part cue becomes stable</text>

  <line x1="586" y1="230" x2="634" y2="230" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>
  <text class="label" x="610" y="208" text-anchor="middle">gather</text>

  <rect x="640" y="110" width="240" height="240" rx="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <text class="card-title" x="662" y="140">3. Later object map</text>
  <text class="label" x="662" y="162">object-level response</text>
  <rect x="700" y="194" width="64" height="64" fill="#fed7aa" stroke="#ea580c" stroke-width="1.2"/>
  <rect x="764" y="194" width="64" height="64" fill="#fb923c" stroke="#ea580c" stroke-width="1.2"/>
  <rect x="732" y="258" width="64" height="32" fill="#fdba74" stroke="#ea580c" stroke-width="1.2"/>
  <rect x="676" y="310" width="168" height="24" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="1.6"/>
  <text class="label" x="760" y="326" text-anchor="middle" fill="#ea580c">object cue can emerge</text>

  <rect x="180" y="376" width="560" height="24" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
  <text class="note" x="460" y="393" text-anchor="middle">Local maps combine into part maps, then object cues.</text>
</svg>"""


def main() -> None:
    write(ASSET_DIR / "cnn-channel-feature-map.svg", generate_channel_feature_map())
    write(ASSET_DIR / "cnn-hierarchical-vision-flow.svg", generate_horse_receptive_field_flow())
    write(ASSET_DIR / "cnn-feature-map-hierarchy.svg", generate_feature_map_hierarchy())


if __name__ == "__main__":
    main()
