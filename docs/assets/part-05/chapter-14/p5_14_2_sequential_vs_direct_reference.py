from pathlib import Path
import os


REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


OUT_DIR = Path(__file__).resolve().parent

CONTEXT = {
    "ko": ["규칙", "보정 로그", "자재 로그", "압력 상태", "일정 로그", "요청"],
    "en": ["Rule", "Calibration", "Restock", "Pressure state", "Schedule", "Request"],
    "zh": ["规则", "校准日志", "补货日志", "压力状态", "排班日志", "请求"],
}

CONTEXT_LINES = [
    "Rule: unstable pressure state must not be restarted.",
    "Log: sensor calibration completed for line 3.",
    "Log: packaging material restocked this morning.",
    "State: pressure has not fully returned to safe range.",
    "Log: operator schedule updated for tomorrow.",
    "Request: restart line 3 now.",
]

LINE_GROUP = {
    1: "rule",
    2: "other",
    3: "other",
    4: "pressure_state",
    5: "other",
}

DIRECT_LABELS = {
    "ko": {
        "rule": "규칙 줄",
        "pressure_state": "압력 상태 줄",
        "other": "기타 로그",
    },
    "en": {
        "rule": "Rule line",
        "pressure_state": "Pressure state",
        "other": "Other logs",
    },
    "zh": {
        "rule": "规则行",
        "pressure_state": "压力状态行",
        "other": "其他日志",
    },
}


def configure_fonts():
    candidates = [
        "Noto Sans CJK SC",
        "Noto Sans CJK JP",
        "Microsoft YaHei",
        "PingFang SC",
        "AppleGothic",
        "Noto Sans CJK KR",
        "Noto Sans KR",
        "Malgun Gothic",
        "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False


def sequential_reader(lines: list[str], decay: float = 0.55) -> list[dict[str, float]]:
    state = {"pressure_risk": 0.0, "restart": 0.0, "block": 0.0}
    history = []
    for line in lines:
        lowered = line.lower()
        for key in state:
            state[key] *= decay
        if "pressure" in lowered or "unstable" in lowered:
            state["pressure_risk"] += 1.0
        if "restart" in lowered:
            state["restart"] += 1.0
        if "must not" in lowered:
            state["block"] += 1.0
        history.append({key: round(value, 3) for key, value in state.items()})
    return history


def direct_reference_scores(lines: list[str]) -> dict[str, int]:
    keywords = {"restart", "pressure", "unstable", "must", "not"}
    group_scores = {"rule": 0, "pressure_state": 0, "other": 0}
    for idx, line in enumerate(lines[:-1], start=1):
        words = set(line.lower().replace(".", "").replace(":", "").split())
        score = len(words & keywords)
        group = LINE_GROUP[idx]
        group_scores[group] = max(group_scores[group], score)
    return group_scores


def state_history_by_key() -> dict[str, list[float]]:
    history = sequential_reader(CONTEXT_LINES)
    return {key: [snapshot[key] for snapshot in history] for key in history[0]}


def localized_direct_matches(locale: str) -> dict[str, int]:
    scores = direct_reference_scores(CONTEXT_LINES)
    labels = DIRECT_LABELS[locale]
    return {
        labels["rule"]: scores["rule"],
        labels["pressure_state"]: scores["pressure_state"],
        labels["other"]: scores["other"],
    }


def draw_state_decay(locale: str):
    locale_text = {
        "ko": {
            "x_label": "문맥 진행 위치",
            "y_label": "상태 강도",
            "final_note": "마지막 요청에서 금지 근거는 0.05만 남음",
            "labels": {
                "pressure_risk": "압력 위험",
                "restart": "재기동 요청",
                "block": "금지 근거",
            },
            "suffix": "ko",
        },
        "en": {
            "x_label": "Context position",
            "y_label": "State strength",
            "final_note": "At the final request, block clue remains only 0.05",
            "labels": {
                "pressure_risk": "pressure risk",
                "restart": "restart",
                "block": "block clue",
            },
            "suffix": "en",
        },
        "zh": {
            "x_label": "上下文推进位置",
            "y_label": "状态强度",
            "final_note": "到最后请求时，阻断线索只剩 0.05",
            "labels": {
                "pressure_risk": "压力风险",
                "restart": "重启请求",
                "block": "阻断线索",
            },
            "suffix": "zh",
        },
    }[locale]

    context_labels = CONTEXT[locale]
    x = list(range(1, len(context_labels) + 1))
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    state_history = state_history_by_key()

    colors = {
        "pressure_risk": "#d97706",
        "restart": "#2563eb",
        "block": "#dc2626",
    }
    labels = {
        "pressure_risk": locale_text["labels"]["pressure_risk"],
        "restart": locale_text["labels"]["restart"],
        "block": locale_text["labels"]["block"],
    }
    for key, values in state_history.items():
        ax.plot(
            x,
            values,
            marker="o",
            linewidth=2.8,
            color=colors[key],
            label=labels[key],
        )
    ax.axvline(6, color="#111827", linestyle="--", linewidth=1.1, alpha=0.55)
    ax.annotate(
        locale_text["final_note"],
        xy=(6, state_history["block"][-1]),
        xytext=(3.55, 1.2),
        arrowprops={"arrowstyle": "->", "color": "#111827", "lw": 1.2},
        fontsize=9.5,
        color="#111827",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(context_labels, rotation=18, ha="right")
    ax.set_xlabel(locale_text["x_label"])
    ax.set_ylabel(locale_text["y_label"])
    ax.set_ylim(0, 1.35)
    ax.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax.legend(loc="upper right", frameon=False, fontsize=8.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / f"sequential-state-decay-{locale_text['suffix']}.png", dpi=160)
    plt.close(fig)


def draw_direct_reference(locale: str):
    bar_label = {
        "ko": "키워드 일치 점수",
        "en": "Keyword match score",
        "zh": "关键词匹配分数",
    }[locale]
    direct_matches = localized_direct_matches(locale)
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    bar_names = list(direct_matches.keys())
    bar_values = list(direct_matches.values())
    bar_colors = ["#dc2626", "#d97706", "#9ca3af"]
    ax.bar(bar_names, bar_values, color=bar_colors, width=0.58)
    ax.set_ylabel(bar_label)
    ax.set_ylim(0, 4.6)
    ax.grid(True, axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(bar_values):
        ax.text(idx, value + 0.12, str(value), ha="center", va="bottom", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / f"direct-reference-match-scores-{locale}.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    configure_fonts()
    for locale in ["ko", "en", "zh"]:
        draw_state_decay(locale)
        draw_direct_reference(locale)
