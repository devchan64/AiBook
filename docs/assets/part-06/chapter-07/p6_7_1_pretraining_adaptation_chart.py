from collections import Counter, defaultdict
from csv import DictReader
from pathlib import Path
from typing import Iterable, Union
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

STAGE_BUNDLES = [
    ("general_only", ("general_text",)),
    ("with_domain", ("general_text", "customer_support")),
    ("with_instruction", ("general_text", "customer_support", "instruction_reply")),
]

LANG_TEXT = {
    "ko": {
        "data_file": "p6-7-pretraining-stage-sentences.csv",
        "focus_links": [
            {
                "key": "broad_language",
                "left": "내용을",
                "rights": ("확인", "정리", "요약", "설명"),
            },
            {
                "key": "domain_support",
                "left": "환불",
                "rights": ("문의", "요청", "상태", "처리"),
            },
            {
                "key": "instruction_style",
                "left": "단계별로",
                "rights": ("안내", "설명", "정리"),
            },
        ],
        "domain_start_tokens": {"환불", "배송", "계정", "교환"},
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "pretraining-adaptation-counts-ko.png",
        "xlabel": "",
        "ylabel": "다음 토큰 관측 횟수",
        "bundle_labels": {
            "general_only": "일반 말뭉치",
            "with_domain": "도메인 추가",
            "with_instruction": "지시형 응답 추가",
        },
        "link_labels": {
            "broad_language": "넓은 언어 연결\n내용을 -> 확인/정리/요약/설명",
            "domain_support": "도메인 연결\n환불 -> 문의/요청/상태/처리",
            "instruction_style": "요청 형식 연결\n단계별로 -> 안내/설명/정리",
        },
    },
    "en": {
        "data_file": "p6-7-pretraining-stage-sentences-en.csv",
        "focus_links": [
            {
                "key": "broad_language",
                "left": "content",
                "rights": ("check", "organize", "summarize", "explain"),
            },
            {
                "key": "domain_support",
                "left": "refund",
                "rights": ("inquiry", "request", "status", "process"),
            },
            {
                "key": "instruction_style",
                "left": "step_by_step",
                "rights": ("guide", "explain", "summarize"),
            },
        ],
        "domain_start_tokens": {"refund", "delivery", "account", "exchange"},
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "pretraining-adaptation-counts-en.png",
        "xlabel": "",
        "ylabel": "next-token count",
        "bundle_labels": {
            "general_only": "general text",
            "with_domain": "after domain data",
            "with_instruction": "after instruction replies",
        },
        "link_labels": {
            "broad_language": "broad language link\ncontent -> check/summarize/explain",
            "domain_support": "domain link\nrefund -> inquiry/request/status/process",
            "instruction_style": "instruction-style link\nstep-by-step -> guide/explain/summarize",
        },
    },
    "zh": {
        "data_file": "p6-7-pretraining-stage-sentences-zh.csv",
        "focus_links": [
            {
                "key": "broad_language",
                "left": "内容",
                "rights": ("确认", "整理", "摘要", "说明"),
            },
            {
                "key": "domain_support",
                "left": "退款",
                "rights": ("咨询", "请求", "状态", "处理"),
            },
            {
                "key": "instruction_style",
                "left": "逐步",
                "rights": ("引导", "说明", "整理"),
            },
        ],
        "domain_start_tokens": {"退款", "配送", "账号", "换货"},
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK",
            "PingFang SC",
            "Songti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "pretraining-adaptation-counts-zh.png",
        "xlabel": "",
        "ylabel": "下一个词元观测次数",
        "bundle_labels": {
            "general_only": "一般语料",
            "with_domain": "加入领域数据",
            "with_instruction": "加入指令型回应",
        },
        "link_labels": {
            "broad_language": "宽广语言连接\n内容 -> 确认/整理/摘要/说明",
            "domain_support": "领域连接\n退款 -> 咨询/请求/状态/处理",
            "instruction_style": "请求格式连接\n逐步 -> 引导/说明/整理",
        },
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


def load_rows(data_path: Path) -> list[dict[str, str]]:
    with data_path.open(newline="", encoding="utf-8") as f:
        return list(DictReader(f))


def build_bigram_counts(sentences: Iterable[str]) -> dict[str, Counter]:
    counts = defaultdict(Counter)
    for sentence in sentences:
        tokens = sentence.split()
        for left, right in zip(tokens, tokens[1:]):
            counts[left][right] += 1
    return counts


def rows_for_stages(rows: list[dict[str, str]], stages: tuple[str, ...]) -> list[dict[str, str]]:
    return [row for row in rows if row["stage"] in stages]


def link_count(counts: dict[str, Counter], left: str, rights: tuple[str, ...]) -> int:
    return sum(counts[left][right] for right in rights)


def collect_link_rows(
    rows: list[dict[str, str]],
    focus_links: list[dict[str, object]],
) -> list[dict[str, Union[int, str]]]:
    result = []
    for bundle_name, stages in STAGE_BUNDLES:
        bundle_rows = rows_for_stages(rows, stages)
        counts = build_bigram_counts(row["sentence"] for row in bundle_rows)
        for link in focus_links:
            result.append(
                {
                    "bundle": bundle_name,
                    "link": link["key"],
                    "count": link_count(counts, link["left"], link["rights"]),
                }
            )
    return result


def collect_stage_sizes(rows: list[dict[str, str]]) -> dict[str, int]:
    sizes = Counter(row["stage"] for row in rows)
    return {stage: sizes[stage] for stage in ("general_text", "customer_support", "instruction_reply")}


def collect_new_domain_links(
    rows: list[dict[str, str]],
    domain_start_tokens: set[str],
    limit: int = 6,
) -> list[tuple[str, int]]:
    general_counts = build_bigram_counts(
        row["sentence"] for row in rows if row["stage"] == "general_text"
    )
    domain_counts = build_bigram_counts(
        row["sentence"] for row in rows if row["stage"] == "customer_support"
    )
    new_links = []
    for left, right_counts in domain_counts.items():
        if left not in domain_start_tokens:
            continue
        for right, domain_count in right_counts.items():
            if general_counts[left][right] == 0:
                new_links.append((f"{left} -> {right}", domain_count))
    return sorted(new_links, key=lambda item: (-item[1], item[0]))[:limit]


def print_summary(rows: list[dict[str, str]], text: dict[str, object]) -> None:
    print("[stage_rows]")
    for stage, count in collect_stage_sizes(rows).items():
        print(f"{stage}: {count}")

    print("\n[focus_link_counts]")
    link_rows = collect_link_rows(rows, text["focus_links"])
    for link in text["focus_links"]:
        values = {
            row["bundle"]: row["count"]
            for row in link_rows
            if row["link"] == link["key"]
        }
        print(
            f"{link['key']}: "
            f"general_only={values['general_only']}, "
            f"with_domain={values['with_domain']}, "
            f"with_instruction={values['with_instruction']}"
        )

    print("\n[new_links_after_domain]")
    for link_name, count in collect_new_domain_links(rows, text["domain_start_tokens"]):
        print(f"{link_name}: {count}")


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(rows: list[dict[str, str]], text: dict[str, object]) -> None:
    configure_font(text)
    link_rows = collect_link_rows(rows, text["focus_links"])
    link_keys = [link["key"] for link in text["focus_links"]]
    bundle_keys = [bundle_name for bundle_name, _ in STAGE_BUNDLES]
    x_positions = list(range(len(link_keys)))
    bar_width = 0.24
    offsets = [-bar_width, 0, bar_width]
    colors = {
        "general_only": "#64748b",
        "with_domain": "#16a34a",
        "with_instruction": "#7c3aed",
    }

    values_by_bundle = {
        bundle_key: [
            next(
                row["count"]
                for row in link_rows
                if row["bundle"] == bundle_key and row["link"] == link_key
            )
            for link_key in link_keys
        ]
        for bundle_key in bundle_keys
    }

    fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    for offset, bundle_key in zip(offsets, bundle_keys):
        bars = ax.bar(
            [x + offset for x in x_positions],
            values_by_bundle[bundle_key],
            width=bar_width,
            color=colors[bundle_key],
            label=text["bundle_labels"][bundle_key],
        )
        for bar in bars:
            value = bar.get_height()
            ax.annotate(
                f"{value:g}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 5),
                ha="center",
                fontsize=8.5,
                color="#172033",
            )

    ax.set_xticks(x_positions)
    ax.set_xticklabels([text["link_labels"][link_key] for link_key in link_keys])
    if text["xlabel"]:
        ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, max(max(values) for values in values_by_bundle.values()) * 1.25)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        rows = load_rows(OUT_DIR / text["data_file"])
        print(f"[{text['outfile']}]")
        print_summary(rows, text)
        save_chart(rows, text)


if __name__ == "__main__":
    main()
