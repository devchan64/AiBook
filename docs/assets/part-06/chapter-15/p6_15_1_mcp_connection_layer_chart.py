from __future__ import annotations

from pathlib import Path
import csv
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

OUT_DIR = Path(__file__).resolve().parent
TOOLS_CSV = OUT_DIR / "p6-15-1-mcp-tool-catalog.csv"
RESOURCES_CSV = OUT_DIR / "p6-15-1-mcp-resource-catalog.csv"
REQUESTS_CSV = OUT_DIR / "p6-15-1-mcp-connection-requests.csv"

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
        "outfile": "mcp-connection-layer-check-ko.png",
        "ylabel": "통과한 요청 수",
        "common_label": "공통 연결 계층",
        "mixed_label": "제각각 연결 계층",
        "labels": ["요청 완료", "연결 준비", "도구 해석", "자원 해석"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "mcp-connection-layer-check-en.png",
        "ylabel": "passed requests",
        "common_label": "common layer",
        "mixed_label": "mixed layer",
        "labels": ["request success", "connection ready", "tool resolved", "resource resolved"],
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK",
            "PingFang SC",
            "Heiti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "mcp-connection-layer-check-zh.png",
        "ylabel": "通过请求数",
        "common_label": "共享连接层",
        "mixed_label": "临时连接层",
        "labels": ["请求完成", "连接准备", "工具解析", "资源解析"],
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, str]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def split_pipe(value: str) -> list[str]:
    return [item for item in value.split("|") if item]


def load_inputs() -> tuple[list[dict[str, object]], list[dict[str, str]], list[dict[str, object]]]:
    with TOOLS_CSV.open(encoding="utf-8", newline="") as file:
        tools = list(csv.DictReader(file))
    for tool in tools:
        tool["input_schema"] = split_pipe(str(tool["input_schema"]))

    with RESOURCES_CSV.open(encoding="utf-8", newline="") as file:
        resources = list(csv.DictReader(file))

    requests = []
    with REQUESTS_CSV.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            row["required_inputs"] = split_pipe(row["required_inputs"])
            row["payload_keys"] = split_pipe(row["payload_keys"])
            row["requires_approval"] = row["requires_approval"].lower() == "true"
            requests.append(row)
    return tools, resources, requests


def evaluate_reports() -> tuple[dict[str, dict[str, int]], int]:
    tools, resources, requests = load_inputs()
    layers = sorted({str(tool["layer"]) for tool in tools})

    def find_tool(layer: str, tool_name: str) -> dict[str, object] | None:
        return next(
            (
                tool
                for tool in tools
                if tool["layer"] == layer and tool["exposed_name"] == tool_name
            ),
            None,
        )

    def find_resource(layer: str, resource_name: str) -> dict[str, str] | None:
        return next(
            (
                resource
                for resource in resources
                if resource["layer"] == layer and resource["exposed_name"] == resource_name
            ),
            None,
        )

    reports = []
    for layer in layers:
        for request in requests:
            tool = find_tool(layer, str(request["tool_needed"]))
            resource = find_resource(layer, str(request["resource_needed"]))
            tool_resolved = tool is not None
            resource_resolved = resource is not None
            connection_ready = False
            request_success = False

            if tool and resource:
                schema = tool["input_schema"]
                required_inputs = request["required_inputs"]
                payload_keys = request["payload_keys"]
                missing_schema = [field for field in required_inputs if field not in schema]
                missing_payload = [field for field in required_inputs if field not in payload_keys]
                connection_ready = (
                    bool(schema)
                    and not missing_schema
                    and bool(tool["returns"])
                    and bool(resource["resource_type"])
                )
                request_success = (
                    connection_ready
                    and not missing_payload
                    and not request["requires_approval"]
                )

            reports.append(
                {
                    "layer": layer,
                    "tool_resolved": tool_resolved,
                    "resource_resolved": resource_resolved,
                    "connection_ready": connection_ready,
                    "request_success": request_success,
                }
            )

    summary = {}
    for layer in layers:
        rows = [row for row in reports if row["layer"] == layer]
        summary[layer] = {
            "request_success_count": sum(row["request_success"] for row in rows),
            "connection_ready_count": sum(row["connection_ready"] for row in rows),
            "tool_resolved_count": sum(row["tool_resolved"] for row in rows),
            "resource_resolved_count": sum(row["resource_resolved"] for row in rows),
        }
    return summary, len(requests)


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    summary, request_count = evaluate_reports()
    labels = text["labels"]
    common_values = [
        summary["common_layer"]["request_success_count"],
        summary["common_layer"]["connection_ready_count"],
        summary["common_layer"]["tool_resolved_count"],
        summary["common_layer"]["resource_resolved_count"],
    ]
    mixed_values = [
        summary["mixed_layer"]["request_success_count"],
        summary["mixed_layer"]["connection_ready_count"],
        summary["mixed_layer"]["tool_resolved_count"],
        summary["mixed_layer"]["resource_resolved_count"],
    ]
    x_positions = list(range(len(labels)))
    bar_width = 0.34

    fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    common_bars = ax.bar(
        [x - bar_width / 2 for x in x_positions],
        common_values,
        width=bar_width,
        color="#2563eb",
        label=text["common_label"],
    )
    mixed_bars = ax.bar(
        [x + bar_width / 2 for x in x_positions],
        mixed_values,
        width=bar_width,
        color="#dc2626",
        label=text["mixed_label"],
    )

    for bars in (common_bars, mixed_bars):
        for bar in bars:
            value = bar.get_height()
            ax.annotate(
                f"{value:g}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 6),
                ha="center",
                fontsize=9,
                color="#172033",
            )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, request_count * 1.25)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
