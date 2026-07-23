from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parent / "student-progress-samples.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    feature_columns = ["region", "study_hours", "absences", "practice_quizzes", "score"]
    target_column = "passed"

    X = df[feature_columns]
    y = df[target_column]
    X_encoded = pd.get_dummies(X, columns=["region"], dtype=int)

    test_index = df.sample(frac=0.25, random_state=42).index
    train_index = df.index.difference(test_index)

    X_train = X_encoded.loc[train_index]
    X_test = X_encoded.loc[test_index]
    y_train = y.loc[train_index]
    y_test = y.loc[test_index]

    print("X shape:", X.shape)
    print("y shape:", y.shape)
    print("encoded columns:", list(X_encoded.columns))
    print("train/test shapes:", X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    print("\ny_train value counts")
    print(y_train.value_counts())
    print("\ny_test value counts")
    print(y_test.value_counts())


if __name__ == "__main__":
    main()
