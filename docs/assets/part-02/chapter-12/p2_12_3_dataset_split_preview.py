from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


DATA_PATH = Path(__file__).resolve().parent / "student-progress-samples.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    feature_columns = ["study_hours", "absences", "practice_quizzes"]
    X = df[feature_columns]
    y = df["passed"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    print("X shape:", X.shape)
    print("y shape:", y.shape)
    print("train/test shapes:", X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    print("\ny_train value counts")
    print(y_train.value_counts())
    print("\ny_test value counts")
    print(y_test.value_counts())


if __name__ == "__main__":
    main()
