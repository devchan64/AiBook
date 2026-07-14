from pathlib import Path
import os
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


OUT_DIR = Path(__file__).resolve().parent
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

LANG_TEXT = {
    "ko": {
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "regression_out": "output-activation-regression-distance-ko.svg",
        "binary_out": "output-activation-binary-threshold-ko.svg",
        "multiclass_out": "output-activation-multiclass-gap-ko.svg",
        "regression_xlabel": "에너지 사용량(kWh)",
        "regression_actual": "실제값 12.4",
        "regression_predicted": "예측값 12.7",
        "regression_error": "오차 0.3 kWh",
        "regression_band": "허용 오차 범위",
        "regression_title": "회귀 출력은 정답과의 거리로 읽는다",
        "regression_desc": "실제 에너지 사용량 12.4kWh와 예측값 12.7kWh 사이의 거리를 표시해 회귀 출력이 확률이 아니라 연속값 오차로 읽힌다는 점을 보여 주는 그래프.",
        "binary_xlabel": "sigmoid 출력 점수",
        "binary_y": "경보",
        "binary_low": "기록만",
        "binary_mid": "현장 확인",
        "binary_high": "자동 정지",
        "binary_threshold_mid": "0.60",
        "binary_threshold_high": "0.90",
        "binary_title": "이진 분류 출력은 threshold 구간으로 읽는다",
        "binary_desc": "sigmoid 출력 점수 0.30, 0.65, 0.91이 기록, 현장 확인, 자동 정지 구간으로 나뉘는 모습을 보여 주는 그래프.",
        "multiclass_ylabel": "softmax 출력",
        "multiclass_classes": ["정상", "스크래치", "오염"],
        "multiclass_gap": "1등-2등 차이 0.04",
        "multiclass_title": "다중 분류 출력은 후보 간 점수 차이로 읽는다",
        "multiclass_desc": "정상 0.38, 스크래치 0.34, 오염 0.28의 softmax 출력 막대를 비교해 1등 후보와 2등 후보의 차이가 작을 때 재검토가 필요할 수 있음을 보여 주는 그래프.",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "regression_out": "output-activation-regression-distance-en.svg",
        "binary_out": "output-activation-binary-threshold-en.svg",
        "multiclass_out": "output-activation-multiclass-gap-en.svg",
        "regression_xlabel": "energy use (kWh)",
        "regression_actual": "actual 12.4",
        "regression_predicted": "prediction 12.7",
        "regression_error": "error 0.3 kWh",
        "regression_band": "allowed error band",
        "regression_title": "Regression output is read as distance from the target",
        "regression_desc": "A chart showing the distance between actual energy use of 12.4 kWh and a prediction of 12.7 kWh, emphasizing that regression output is read as continuous-value error rather than probability.",
        "binary_xlabel": "sigmoid output score",
        "binary_y": "alarm",
        "binary_low": "record only",
        "binary_mid": "field check",
        "binary_high": "auto stop",
        "binary_threshold_mid": "0.60",
        "binary_threshold_high": "0.90",
        "binary_title": "Binary classification output is read by threshold bands",
        "binary_desc": "A chart showing sigmoid output scores 0.30, 0.65, and 0.91 being separated into record-only, field-check, and auto-stop bands.",
        "multiclass_ylabel": "softmax output",
        "multiclass_classes": ["normal", "scratch", "contamination"],
        "multiclass_gap": "top gap 0.04",
        "multiclass_title": "Multiclass output is read through score gaps between candidates",
        "multiclass_desc": "A bar chart comparing softmax outputs normal 0.38, scratch 0.34, and contamination 0.28 to show why a narrow top gap may require review.",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, object]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def inject_accessibility(svg_path: Path, title: str, desc: str) -> None:
    tree = ET.parse(svg_path)
    root = tree.getroot()
    root.set("role", "img")
    root.set("aria-labelledby", "title desc")

    for tag in ["title", "desc"]:
        existing = root.find(f"{{{SVG_NS}}}{tag}")
        if existing is not None:
            root.remove(existing)

    title_el = ET.Element(f"{{{SVG_NS}}}title", {"id": "title"})
    title_el.text = title
    desc_el = ET.Element(f"{{{SVG_NS}}}desc", {"id": "desc"})
    desc_el.text = desc
    root.insert(0, desc_el)
    root.insert(0, title_el)
    tree.write(svg_path, encoding="utf-8", xml_declaration=False)


def style_axes(ax) -> None:
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_regression_distance_chart(text: dict[str, object]) -> None:
    configure_font(text)
    actual = 12.4
    predicted = 12.7
    tolerance = 0.5

    fig, ax = plt.subplots(figsize=(6.2, 2.6), dpi=160)
    fig.patch.set_facecolor("white")
    style_axes(ax)
    ax.set_xlim(11.7, 13.3)
    ax.set_ylim(-0.4, 0.4)
    ax.set_yticks([])
    ax.set_xticks([11.8, 12.0, 12.4, 12.7, 13.0, 13.2])
    ax.set_xlabel(text["regression_xlabel"])
    ax.axvspan(actual - tolerance, actual + tolerance, color="#dbeafe", alpha=0.75, label=text["regression_band"])
    ax.hlines(0, actual, predicted, color="#f97316", linewidth=4)
    ax.scatter([actual], [0], s=70, color="#2563eb", zorder=4)
    ax.scatter([predicted], [0], s=70, color="#dc2626", zorder=4)
    ax.annotate(text["regression_actual"], (actual, 0), xytext=(-16, 20), textcoords="offset points", ha="right", fontsize=9)
    ax.annotate(text["regression_predicted"], (predicted, 0), xytext=(12, 20), textcoords="offset points", ha="left", fontsize=9)
    ax.annotate(text["regression_error"], ((actual + predicted) / 2, 0), xytext=(0, -28), textcoords="offset points", ha="center", fontsize=9, color="#9a3412")
    ax.legend(frameon=False, loc="upper left", fontsize=8.5)

    out = OUT_DIR / text["regression_out"]
    fig.tight_layout(pad=0.8)
    fig.savefig(out, format="svg")
    plt.close(fig)
    inject_accessibility(out, text["regression_title"], text["regression_desc"])


def save_binary_threshold_chart(text: dict[str, object]) -> None:
    configure_font(text)
    scores = [0.30, 0.65, 0.91]
    y_positions = [0, 0, 0]

    fig, ax = plt.subplots(figsize=(6.2, 2.8), dpi=160)
    fig.patch.set_facecolor("white")
    style_axes(ax)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.55, 0.55)
    ax.set_yticks([])
    ax.set_xticks([0, 0.3, 0.6, 0.9, 1.0])
    ax.set_xlabel(text["binary_xlabel"])
    ax.axvspan(0, 0.6, color="#dcfce7", alpha=0.8)
    ax.axvspan(0.6, 0.9, color="#fef3c7", alpha=0.9)
    ax.axvspan(0.9, 1.0, color="#fee2e2", alpha=0.95)
    ax.axvline(0.6, color="#92400e", linewidth=1.2, linestyle=(0, (4, 4)))
    ax.axvline(0.9, color="#991b1b", linewidth=1.2, linestyle=(0, (4, 4)))
    ax.text(0.30, 0.36, text["binary_low"], ha="center", fontsize=9, color="#166534")
    ax.text(0.75, 0.36, text["binary_mid"], ha="center", fontsize=9, color="#92400e")
    ax.text(0.95, 0.36, text["binary_high"], ha="center", fontsize=9, color="#991b1b")
    ax.text(0.6, -0.42, text["binary_threshold_mid"], ha="center", fontsize=8.5, color="#92400e")
    ax.text(0.9, -0.42, text["binary_threshold_high"], ha="center", fontsize=8.5, color="#991b1b")
    ax.scatter(scores, y_positions, s=80, color=["#16a34a", "#f59e0b", "#dc2626"], zorder=4)
    for score in scores:
        ax.annotate(f"{score:.2f}", (score, 0), xytext=(0, -24), textcoords="offset points", ha="center", fontsize=9)

    out = OUT_DIR / text["binary_out"]
    fig.tight_layout(pad=0.8)
    fig.savefig(out, format="svg")
    plt.close(fig)
    inject_accessibility(out, text["binary_title"], text["binary_desc"])


def save_multiclass_gap_chart(text: dict[str, object]) -> None:
    configure_font(text)
    classes = text["multiclass_classes"]
    values = [0.38, 0.34, 0.28]
    colors = ["#2563eb", "#f97316", "#64748b"]

    fig, ax = plt.subplots(figsize=(5.8, 3.5), dpi=160)
    fig.patch.set_facecolor("white")
    style_axes(ax)
    bars = ax.bar(classes, values, color=colors, width=0.58)
    ax.set_ylim(0, 0.5)
    ax.set_ylabel(text["multiclass_ylabel"])
    ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.015, f"{value:.2f}", ha="center", fontsize=9)
    ax.hlines([values[0], values[1]], xmin=0.1, xmax=0.65, color="#9a3412", linewidth=1.0, linestyle=(0, (3, 3)))
    ax.annotate(
        "",
        xy=(0.65, values[1]),
        xytext=(0.65, values[0]),
        arrowprops={"arrowstyle": "<->", "color": "#9a3412", "linewidth": 1.2},
    )
    ax.text(0.78, (values[0] + values[1]) / 2, text["multiclass_gap"], va="center", fontsize=9, color="#9a3412")

    out = OUT_DIR / text["multiclass_out"]
    fig.tight_layout(pad=0.8)
    fig.savefig(out, format="svg")
    plt.close(fig)
    inject_accessibility(out, text["multiclass_title"], text["multiclass_desc"])


def main() -> None:
    for text in LANG_TEXT.values():
        save_regression_distance_chart(text)
        save_binary_threshold_chart(text)
        save_multiclass_gap_chart(text)


if __name__ == "__main__":
    main()
