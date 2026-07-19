from math import exp
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

OUT_DIR = Path(__file__).resolve().parent

CONTEXTS = {
    "formal_notice": {
        "features": {
            "formal_tone": 1.0,
            "casual_tone": 0.0,
            "notice_style": 1.0,
            "meeting_context": 0.8,
            "past_tense": 0.0,
        },
    },
    "casual_team_chat": {
        "features": {
            "formal_tone": 0.0,
            "casual_tone": 1.0,
            "notice_style": 0.0,
            "meeting_context": 0.4,
            "past_tense": 0.0,
        },
    },
}

EXPERIMENTS = [
    {"name": "formal_notice", "context": "formal_notice", "changes": {}},
    {
        "name": "formal_notice_weaker_notice_style",
        "context": "formal_notice",
        "changes": {"notice_style": 0.2},
    },
    {"name": "casual_team_chat", "context": "casual_team_chat", "changes": {}},
    {
        "name": "casual_team_chat_more_formal",
        "context": "casual_team_chat",
        "changes": {"formal_tone": 0.5, "casual_tone": 0.4},
    },
]

CANDIDATES = {
    "합니다": {
        "base": 0.2,
        "weights": {
            "formal_tone": 1.2,
            "casual_tone": -0.8,
            "notice_style": 0.9,
            "meeting_context": 0.2,
            "past_tense": -0.6,
        },
    },
    "이다": {
        "base": 0.3,
        "weights": {
            "formal_tone": -0.3,
            "casual_tone": 0.7,
            "notice_style": -0.2,
            "meeting_context": 0.1,
            "past_tense": -0.5,
        },
    },
    "되었습니다": {
        "base": 0.1,
        "weights": {
            "formal_tone": 0.8,
            "casual_tone": -0.4,
            "notice_style": 0.4,
            "meeting_context": -0.1,
            "past_tense": 1.3,
        },
    },
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
        "outfile": "context-candidate-distribution-ko.png",
        "experiment_labels": ["공지", "공지\n약화", "팀 메모", "팀 메모\n공손 단서"],
        "probability_ylabel": "후보 확률",
        "margin_ylabel": "1, 2위 점수 차이",
        "margin_label": "top_2_margin",
        "candidate_labels": {
            "합니다": "합니다",
            "이다": "이다",
            "되었습니다": "되었습니다",
        },
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "context-candidate-distribution-en.png",
        "experiment_labels": ["notice", "notice\nweaker", "team memo", "team memo\nmore formal"],
        "probability_ylabel": "candidate probability",
        "margin_ylabel": "top-2 score margin",
        "margin_label": "top_2_margin",
        "candidate_labels": {
            "합니다": "formal ending",
            "이다": "plain ending",
            "되었습니다": "past formal",
        },
    },
}

COLORS = {
    "합니다": "#0f766e",
    "이다": "#2563eb",
    "되었습니다": "#b45309",
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


def apply_changes(features: dict[str, float], changes: dict[str, float]) -> dict[str, float]:
    updated = features.copy()
    updated.update(changes)
    return updated


def score_candidates(feature_values: dict[str, float]) -> list[dict[str, float | str]]:
    scored = []
    for token, config in CANDIDATES.items():
        total = config["base"]
        for feature_name, feature_value in feature_values.items():
            total += feature_value * config["weights"][feature_name]
        scored.append({"token": token, "score": round(total, 2)})

    exp_scores = [exp(item["score"]) for item in scored]
    total_exp_score = sum(exp_scores)
    for item, exp_score in zip(scored, exp_scores):
        item["probability"] = round(exp_score / total_exp_score, 3)
    return sorted(scored, key=lambda item: item["score"], reverse=True)


def summarize_experiments() -> list[dict[str, object]]:
    rows = []
    for experiment in EXPERIMENTS:
        context = CONTEXTS[experiment["context"]]
        features = apply_changes(context["features"], experiment["changes"])
        ranking = score_candidates(features)
        rows.append(
            {
                "name": experiment["name"],
                "ranking": ranking,
                "margin": round(ranking[0]["score"] - ranking[1]["score"], 2),
            }
        )
    return rows


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    rows = summarize_experiments()
    labels = text["experiment_labels"]
    x_positions = list(range(len(rows)))
    candidate_names = list(CANDIDATES)
    width = 0.22

    fig, (prob_ax, margin_ax) = plt.subplots(
        2,
        1,
        figsize=(7.2, 5.4),
        dpi=180,
        gridspec_kw={"height_ratios": [2.1, 1.0], "hspace": 0.34},
    )
    fig.patch.set_facecolor("white")

    for axis in (prob_ax, margin_ax):
        axis.set_facecolor("white")
        style_axis(axis)

    for offset, candidate in enumerate(candidate_names):
        values = []
        for row in rows:
            probability_by_token = {item["token"]: item["probability"] for item in row["ranking"]}
            values.append(probability_by_token[candidate])
        positions = [x + (offset - 1) * width for x in x_positions]
        bars = prob_ax.bar(
            positions,
            values,
            width=width,
            color=COLORS[candidate],
            label=text["candidate_labels"][candidate],
        )
        for bar, value in zip(bars, values):
            prob_ax.annotate(
                f"{value:.3f}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 5),
                ha="center",
                fontsize=7.4,
                color="#172033",
            )

    prob_ax.set_xticks(x_positions, labels)
    prob_ax.set_ylabel(text["probability_ylabel"])
    prob_ax.set_ylim(0, 0.82)
    prob_ax.legend(loc="upper right", ncol=3, frameon=False, fontsize=8.2)

    margins = [row["margin"] for row in rows]
    margin_bars = margin_ax.bar(x_positions, margins, color="#475569", width=0.48, label=text["margin_label"])
    for bar, value in zip(margin_bars, margins):
        margin_ax.annotate(
            f"{value:.2f}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 5),
            ha="center",
            fontsize=8,
            color="#172033",
        )
    margin_ax.set_xticks(x_positions, labels)
    margin_ax.set_ylabel(text["margin_ylabel"])
    margin_ax.set_ylim(0, max(margins) * 1.25)

    fig.subplots_adjust(left=0.11, right=0.98, top=0.96, bottom=0.11, hspace=0.42)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
