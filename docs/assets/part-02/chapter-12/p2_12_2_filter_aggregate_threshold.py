from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parent / "student-progress-samples.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    # Change these two values to see which rows and summaries move.
    pass_threshold = 75
    focus_region = "Busan"

    selected = df.loc[
        (df["score"] >= pass_threshold) & (df["region"] == focus_region),
        ["student_id", "region", "score", "passed"],
    ]

    summary = (
        df.assign(over_threshold=df["score"] >= pass_threshold)
        .groupby("region")
        .agg(
            sample_count=("student_id", "count"),
            mean_score=("score", "mean"),
            over_threshold_count=("over_threshold", "sum"),
            mean_absences=("absences", "mean"),
        )
        .round(2)
        .sort_values("mean_score", ascending=False)
    )

    print("selected rows")
    print(selected.to_string(index=False))
    print("\nregion summary")
    print(summary)


if __name__ == "__main__":
    main()
