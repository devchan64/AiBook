from pathlib import Path
import csv
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
CSV_PATH = OUT_DIR / "rnn-sequence-events.csv"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

SENSOR_ALPHA = 0.6
SENSOR_THRESHOLD = 68


def choose_font() -> str:
    candidates = [
        "Noto Sans CJK KR",
        "NanumGothic",
        "Arial Unicode MS",
        "Songti SC",
        "Heiti TC",
        "Apple SD Gothic Neo",
        "AppleGothic",
        "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def read_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return sorted(rows, key=lambda row: (row["sequence_id"], int(row["step"])))


def group_sensor_values(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    groups: dict[str, list[float]] = {}
    for row in rows:
        if row["kind"] != "sensor":
            continue
        groups.setdefault(row["sequence_id"], []).append(float(row["sensor_value"]))
    return groups


def sensor_states(values: list[float], alpha: float = SENSOR_ALPHA) -> list[float]:
    state = 0.0
    states = []
    for value in values:
        state = alpha * state + (1 - alpha) * value
        states.append(state)
    return states


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


LANG_LABELS = {
    "ko": {
        "ylabel": "누적 상태",
        "threshold": "threshold 68",
        "file": "rnn-sequence-csv-state-trace-ko.svg",
        "title": "CSV 시퀀스별 누적 상태 변화",
        "desc": "CSV에 담긴 여러 센서 시퀀스가 모두 마지막 값 80으로 끝나더라도 직전 흐름에 따라 누적 상태가 서로 다르고, 일부만 threshold 68을 넘는다는 점을 보여 주는 그래프.",
    },
    "en": {
        "ylabel": "accumulated state",
        "threshold": "threshold 68",
        "file": "rnn-sequence-csv-state-trace-en.svg",
        "title": "Accumulated state by CSV sequence",
        "desc": "A chart showing that several sensor sequences in the CSV all end at the final value 80, but their accumulated states differ according to the preceding flow and only some exceed threshold 68.",
    },
    "zh": {
        "ylabel": "累积状态",
        "threshold": "threshold 68",
        "file": "rnn-sequence-csv-state-trace-zh.svg",
        "title": "按 CSV 序列比较的累积状态变化",
        "desc": "这张图显示：CSV 中的多个传感器序列虽然最后都以 80 结束，但会因为前面的流向不同而留下不同的累积状态，只有一部分会超过 threshold 68。",
    },
}


def save_state_trace_chart(groups: dict[str, list[float]], labels_for_lang: dict[str, str]) -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False

    selected = [
        "sensor_gradual_rise",
        "sensor_temporary_spike",
        "sensor_late_rise",
        "sensor_stable_high",
        "sensor_recovered_then_rise",
    ]
    colors = {
        "sensor_gradual_rise": "#2563eb",
        "sensor_temporary_spike": "#dc2626",
        "sensor_late_rise": "#059669",
        "sensor_stable_high": "#f59e0b",
        "sensor_recovered_then_rise": "#7c3aed",
    }
    labels = {
        "sensor_gradual_rise": "gradual_rise",
        "sensor_temporary_spike": "temporary_spike",
        "sensor_late_rise": "late_rise",
        "sensor_stable_high": "stable_high",
        "sensor_recovered_then_rise": "recovered_then_rise",
    }

    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f8fafc")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for name in selected:
        values = groups[name]
        steps = list(range(1, len(values) + 1))
        ax.plot(steps, sensor_states(values), marker="o", linewidth=2.4, markersize=4.8, color=colors[name], label=labels[name])

    ax.axhline(SENSOR_THRESHOLD, color="#475569", linewidth=1.2, linestyle=(0, (5, 4)))
    ax.text(1.05, SENSOR_THRESHOLD + 1.2, labels_for_lang["threshold"], fontsize=8.5, color="#334155")
    ax.set_xlabel("step")
    ax.set_ylabel(labels_for_lang["ylabel"])
    ax.set_xticks(range(1, 7))
    ax.set_ylim(20, 75)
    ax.legend(frameon=False, loc="lower right", fontsize=8.0)

    fig.tight_layout(pad=0.9)
    out_path = OUT_DIR / labels_for_lang["file"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(
        out_path,
        labels_for_lang["title"],
        labels_for_lang["desc"],
    )


def main() -> None:
    rows = read_rows()
    groups = group_sensor_values(rows)
    for labels_for_lang in LANG_LABELS.values():
        save_state_trace_chart(groups, labels_for_lang)


if __name__ == "__main__":
    main()
