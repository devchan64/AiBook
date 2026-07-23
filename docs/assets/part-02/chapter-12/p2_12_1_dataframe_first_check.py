from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parent / "student-progress-samples.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print("shape:", df.shape)
    print("columns:", list(df.columns))
    print("index:", df.index)
    print("\ndtypes")
    print(df.dtypes)
    print("\nhead")
    print(df.head(3).to_string(index=False))


if __name__ == "__main__":
    main()
