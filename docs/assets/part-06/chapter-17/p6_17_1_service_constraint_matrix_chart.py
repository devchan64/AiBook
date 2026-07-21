from pathlib import Path
import os

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap

OUT_DIR = Path(__file__).resolve().parent

SERVICES = [
    {"name": "fast", "quality": 0.78, "latency_ms": 900, "cost": 1, "requests_per_minute": 120},
    {"name": "balanced", "quality": 0.84, "latency_ms": 1700, "cost": 2, "requests_per_minute": 90},
    {"name": "rich", "quality": 0.89, "latency_ms": 3200, "cost": 4, "requests_per_minute": 40},
    {"name": "cheap_but_weak", "quality": 0.65, "latency_ms": 700, "cost": 1, "requests_per_minute": 150},
    {"name": "accurate_but_capped", "quality": 0.87, "latency_ms": 1500, "cost": 2, "requests_per_minute": 45},
]

CONSTRAINTS = {
    "max_latency_ms": 2000,
    "max_cost": 3,
    "min_quality": 0.75,
    "required_requests_per_minute": 80,
}

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
        "outfile": "service-constraint-matrix-ko.png",
        "checks": ["품질\nq>=0.75", "지연\nms<=2000", "비용\ncost<=3", "처리량\nrpm>=80"],
        "pass": "통과",
        "fail": "탈락",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "service-constraint-matrix-en.png",
        "checks": ["quality\nq>=0.75", "latency\nms<=2000", "cost\ncost<=3", "throughput\nrpm>=80"],
        "pass": "pass",
        "fail": "fail",
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


def evaluate(service: dict[str, object]) -> list[bool]:
    return [
        service["quality"] >= CONSTRAINTS["min_quality"],
        service["latency_ms"] <= CONSTRAINTS["max_latency_ms"],
        service["cost"] <= CONSTRAINTS["max_cost"],
        service["requests_per_minute"] >= CONSTRAINTS["required_requests_per_minute"],
    ]


def annotation_values(service: dict[str, object]) -> list[str]:
    return [
        f'{service["quality"]:.2f}',
        f'{service["latency_ms"]}ms',
        f'{service["cost"]}',
        f'{service["requests_per_minute"]}rpm',
    ]


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    matrix = [[1 if ok else 0 for ok in evaluate(service)] for service in SERVICES]
    annotations = [annotation_values(service) for service in SERVICES]
    service_names = [service["name"] for service in SERVICES]
    cmap = ListedColormap(["#dc2626", "#0f766e"])

    fig, ax = plt.subplots(figsize=(8.9, 4.2), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.imshow(matrix, cmap=cmap, vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(range(len(text["checks"])))
    ax.set_xticklabels(text["checks"])
    ax.set_yticks(range(len(service_names)))
    ax.set_yticklabels(service_names)
    ax.tick_params(axis="x", labelsize=9, pad=8)
    ax.tick_params(axis="y", labelsize=8.7)

    ax.set_xticks([index - 0.5 for index in range(1, len(text["checks"]))], minor=True)
    ax.set_yticks([index - 0.5 for index in range(1, len(service_names))], minor=True)
    ax.grid(which="minor", color="white", linewidth=2.2)
    ax.tick_params(which="minor", bottom=False, left=False)

    for row_index, row in enumerate(matrix):
        for col_index, ok in enumerate(row):
            status = text["pass"] if ok else text["fail"]
            ax.text(
                col_index,
                row_index,
                f"{status}\n{annotations[row_index][col_index]}",
                ha="center",
                va="center",
                color="white",
                fontsize=8,
                fontweight="bold",
            )

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
