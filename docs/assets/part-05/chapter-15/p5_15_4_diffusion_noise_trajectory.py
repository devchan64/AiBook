"""Generate language-specific SVGs from a forward-diffusion mixture."""

from pathlib import Path
import math
import random


OUT_DIR = Path(__file__).parent
LABELS = {
    "ko": ("원본", "초기 노이즈", "중간 노이즈", "강한 노이즈"),
    "en": ("Original", "Light noise", "Medium noise", "Heavy noise"),
    "zh": ("原始状态", "轻度噪声", "中度噪声", "强噪声"),
}
ALPHA_BARS = (1.0, 0.78, 0.38, 0.06)


def cell_color(base: int, noise: float, alpha_bar: float) -> str:
    signal = (base - 128) / 128
    mixed = math.sqrt(alpha_bar) * signal + math.sqrt(1 - alpha_bar) * noise
    value = round((max(-1, min(1, mixed)) + 1) * 127.5)
    return f"rgb({value},{value},{value})"


def build_svg(language: str) -> str:
    random_source = random.Random(15)
    base = [(row * 29 + col * 43 + 48) % 210 + 20 for row in range(6) for col in range(6)]
    noise = [random_source.gauss(0, 1) for _ in base]
    cards = []
    for index, (label, alpha_bar) in enumerate(zip(LABELS[language], ALPHA_BARS)):
        x_offset = 20 + index * 190
        cells = []
        for cell_index, base_value in enumerate(base):
            row, col = divmod(cell_index, 6)
            cells.append(
                f'<rect x="{x_offset + col * 22}" y="55" width="21" height="21" '
                f'fill="{cell_color(base_value, noise[cell_index], alpha_bar)}"/>'
            )
            cells[-1] = cells[-1].replace(' y="55"', f' y="{55 + row * 22}"')
        cards.append(
            f'<g><rect x="{x_offset - 8}" y="25" width="150" height="185" rx="8" fill="#f8fafc" stroke="#94a3b8"/>'
            f'<text x="{x_offset + 67}" y="45" text-anchor="middle" font-size="14">{label}</text>{"".join(cells)}</g>'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="780" height="240" viewBox="0 0 780 240" role="img">'
        '<title>Diffusion noise trajectory</title><desc>A synthetic six by six grid shown with increasing noise.</desc>'
        '<rect width="780" height="240" fill="white"/>'
        + "".join(cards)
        + '</svg>'
    )


for language in LABELS:
    (OUT_DIR / f"diffusion-noise-trajectory-{language}.svg").write_text(build_svg(language), encoding="utf-8")
