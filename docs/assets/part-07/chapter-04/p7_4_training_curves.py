from __future__ import annotations

import csv
import os
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

OUT_DIR = Path(__file__).resolve().parent
DATASET_PATH = OUT_DIR / "p7-4-support-routing-dataset.csv"
LOG_PATH = OUT_DIR / "p7-4-training-log.csv"
SVG_PATH = OUT_DIR / "p7-4-learning-curves-ko.svg"
KOREAN_FONT_PATH = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")


def choose_font() -> str:
    system_fonts = [Path(path) for path in font_manager.findSystemFonts()]
    candidates = [KOREAN_FONT_PATH] + [
        path
        for path in system_fonts
        if "NotoSansCJK" in path.name or "Nanum" in path.name
    ]
    for candidate in candidates:
        if candidate.exists():
            font_manager.fontManager.addfont(str(candidate))
            return font_manager.FontProperties(fname=str(candidate)).get_name()
    raise RuntimeError("한글 차트에는 Noto Sans CJK 또는 Nanum 계열 폰트가 필요합니다.")


def configure_font() -> None:
    plt.rcParams["font.family"] = choose_font()
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
    cleaned_lines = [line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()]
    svg_path.write_text("\n".join(cleaned_lines) + "\n", encoding="utf-8")


def load_dataset() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows = list(csv.DictReader(DATASET_PATH.open(encoding="utf-8")))
    for row in rows:
        row["label"] = int(row["label"])
    train_rows = [row for row in rows if row["split"] == "train"]
    test_rows = [row for row in rows if row["split"] == "test"]
    return train_rows, test_rows


def tokenize(text: str) -> list[str]:
    return text.split()


def build_matrix(
    rows: list[dict[str, object]], token_to_index: dict[str, int]
) -> tuple[np.ndarray, np.ndarray]:
    X = np.zeros((len(rows), len(token_to_index)), dtype=float)
    y = np.zeros(len(rows), dtype=int)
    for i, row in enumerate(rows):
        y[i] = int(row["label"])
        for token in tokenize(str(row["text"])):
            if token in token_to_index:
                X[i, token_to_index[token]] += 1.0
    return X, y


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp_shifted = np.exp(shifted)
    return exp_shifted / exp_shifted.sum(axis=1, keepdims=True)


def loss_and_accuracy(
    X: np.ndarray, y: np.ndarray, W: np.ndarray, b: np.ndarray
) -> tuple[float, float]:
    probs = softmax(X @ W + b)
    loss = float(-np.log(probs[np.arange(len(y)), y] + 1e-12).mean())
    accuracy = float((probs.argmax(axis=1) == y).mean())
    return loss, accuracy


def run_training() -> list[dict[str, float]]:
    train_rows, test_rows = load_dataset()
    vocab = sorted({token for row in train_rows for token in tokenize(str(row["text"]))})
    token_to_index = {token: index for index, token in enumerate(vocab)}

    X_train, y_train = build_matrix(train_rows, token_to_index)
    X_test, y_test = build_matrix(test_rows, token_to_index)

    num_classes = 2
    W = np.zeros((len(vocab), num_classes), dtype=float)
    b = np.zeros(num_classes, dtype=float)
    Y_train = np.zeros((len(y_train), num_classes), dtype=float)
    Y_train[np.arange(len(y_train)), y_train] = 1.0

    baseline_class = int(np.bincount(y_train).argmax())
    baseline_accuracy = float((np.full_like(y_test, baseline_class) == y_test).mean())

    learning_rate = 0.35
    logs: list[dict[str, float]] = []
    for epoch in range(1, 13):
        probs = softmax(X_train @ W + b)
        grad_W = X_train.T @ (probs - Y_train) / len(X_train)
        grad_b = (probs - Y_train).mean(axis=0)
        W -= learning_rate * grad_W
        b -= learning_rate * grad_b

        train_loss, train_accuracy = loss_and_accuracy(X_train, y_train, W, b)
        eval_loss, eval_accuracy = loss_and_accuracy(X_test, y_test, W, b)
        logs.append(
            {
                "epoch": epoch,
                "train_loss": round(train_loss, 3),
                "eval_loss": round(eval_loss, 3),
                "train_accuracy": round(train_accuracy, 3),
                "eval_accuracy": round(eval_accuracy, 3),
                "baseline_accuracy": round(baseline_accuracy, 3),
            }
        )

    return logs


def write_log_csv(logs: list[dict[str, float]]) -> None:
    with LOG_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "epoch",
                "train_loss",
                "eval_loss",
                "train_accuracy",
                "eval_accuracy",
                "baseline_accuracy",
            ],
        )
        writer.writeheader()
        writer.writerows(logs)


def draw_chart(logs: list[dict[str, float]]) -> None:
    configure_font()
    epochs = [int(row["epoch"]) for row in logs]
    train_loss = [row["train_loss"] for row in logs]
    eval_loss = [row["eval_loss"] for row in logs]
    eval_accuracy = [row["eval_accuracy"] for row in logs]
    baseline_accuracy = [row["baseline_accuracy"] for row in logs]

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.5), constrained_layout=True)

    ax_loss, ax_acc = axes
    ax_loss.plot(epochs, train_loss, marker="o", linewidth=2.2, color="#0f766e", label="학습 손실")
    ax_loss.plot(epochs, eval_loss, marker="o", linewidth=2.2, color="#ea580c", label="평가 손실")
    ax_loss.set_title("손실 곡선")
    ax_loss.set_xlabel("epoch")
    ax_loss.set_ylabel("loss")
    ax_loss.set_xticks(epochs)
    ax_loss.grid(alpha=0.22)
    ax_loss.legend(frameon=False, loc="upper right")

    ax_acc.plot(epochs, eval_accuracy, marker="o", linewidth=2.2, color="#2563eb", label="평가 정확도")
    ax_acc.plot(
        epochs,
        baseline_accuracy,
        linestyle="--",
        linewidth=1.8,
        color="#64748b",
        label="기준선 정확도",
    )
    ax_acc.set_title("정확도와 기준선 비교")
    ax_acc.set_xlabel("epoch")
    ax_acc.set_ylabel("accuracy")
    ax_acc.set_xticks(epochs)
    ax_acc.set_ylim(0.68, 0.9)
    ax_acc.grid(alpha=0.22)
    ax_acc.legend(frameon=False, loc="lower right")
    ax_acc.annotate(
        "정확도는 0.857에서 유지되지만\n손실은 계속 감소",
        xy=(8, eval_accuracy[7]),
        xytext=(5.1, 0.885),
        arrowprops={"arrowstyle": "->", "color": "#1f2937", "linewidth": 1.2},
        fontsize=10,
    )

    fig.suptitle(
        "고객 문의 라우팅 분류 학습 로그\n평가 정확도 0.857 유지 · 평가 손실 0.624 → 0.404",
        fontsize=14,
        fontweight="bold",
    )
    fig.savefig(SVG_PATH, format="svg", dpi=160, bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(
        SVG_PATH,
        "고객 문의 라우팅 분류 학습 로그",
        "왼쪽에는 epoch에 따라 학습 손실과 평가 손실이 함께 내려가는 선 그래프, 오른쪽에는 평가 정확도가 0.857에 머문 채 기준선 0.714보다 위에서 유지되는 선 그래프가 있다.",
    )


def main() -> None:
    logs = run_training()
    write_log_csv(logs)
    draw_chart(logs)


if __name__ == "__main__":
    main()
