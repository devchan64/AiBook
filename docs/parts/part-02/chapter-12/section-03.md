# P2-12.3 학습용 데이터셋(dataset) 준비의 직관

> Section ID: `P2-12.3`
> Version: `v2026.09.15`

## 예측 시점과 입력 열

학습용 데이터셋은 모델이 사용할 입력과 맞혀야 할 정답을 묶은 데이터입니다. 같은 학생 표라도 시험 전에 합격 여부를 예측하는지, 시험 후에 점수로 합격 여부를 계산하는지에 따라 쓸 수 있는 열이 달라집니다.

| 열 | 시험 전 합격 예측에서의 역할 |
| --- | --- |
| `student_id` | 학생을 구분하는 식별자 |
| `region` | 예측 시점에 알려진 범주형 입력 후보 |
| `absences` | 예측 시점까지 집계한 결석 수 입력 후보 |
| `score` | 아직 치르지 않은 시험의 결과이므로 입력에서 제외 |
| `passed` | 맞혀야 할 정답 |

시험 전에는 최종 점수를 알 수 없습니다. 과거 기록에 점수가 있다고 해서 입력에 넣으면, 실제 예측 때 사용할 수 없는 정보를 학습에 제공하게 됩니다. 이를 데이터 누수(data leakage)라고 합니다. 최종 합격 여부가 점수 기준으로 정해진다면 점수를 이용한 합격 판정은 해당 기준을 적용하는 계산으로 처리할 수 있습니다.

## 입력 X와 정답 y

`X`는 입력 특징(feature)을 담은 표이고, `y`는 타깃(target), 즉 정답 묶음입니다. 다음 표에서 시험 전까지의 지역과 결석 수를 입력 후보로 고르고 합격 여부를 정답으로 분리합니다.

```python
import pandas as pd

df = pd.DataFrame(
    {
        "student_id": ["S001", "S002", "S003", "S004"],
        "region": ["Seoul", "Busan", "Seoul", "Busan"],
        "absences": [1, 5, 0, 2],
        "score": [82, 45, 90, 73],
        "passed": ["yes", "no", "yes", "yes"],
    }
)

X = df[["region", "absences"]]
y = df["passed"]

print(X)
print(y)
print(X.shape, y.shape)
```

`X`에는 네 학생의 지역과 결석 수가 들어 있고, `y`에는 `["yes", "no", "yes", "yes"]`가 들어 있습니다. 모양은 각각 `(4, 2)`와 `(4,)`입니다. 두 특징을 가진 학생 4명과 그 학생들의 정답 4개라는 뜻입니다. 행 순서가 달라져 다른 학생의 정답과 짝지어지지 않도록 `X`와 `y`를 함께 다뤄야 합니다.

```mermaid
--8<-- "assets/part-02/chapter-12/x-y-split-flow-ko.mmd"
```

`student_id`는 기록을 연결할 때 쓰는 식별자입니다. 번호 자체가 성취도를 설명한다고 볼 근거가 없다면 입력에서 제외합니다. `passed`를 입력에도 포함하면 정답을 그대로 읽을 수 있으므로 예측 능력을 평가할 수 없습니다.

## 학습·검증·테스트 분리

학습 데이터는 모델의 규칙을 배우는 데 사용합니다. 검증 데이터는 모델 종류나 설정을 비교하는 데 사용하고, 테스트 데이터는 선택이 끝난 모델을 마지막으로 평가하는 데 남겨 둡니다. 같은 데이터를 학습과 평가에 쓰면 이미 본 기록을 기억한 효과와 새로운 기록에 대한 예측 능력을 구분하기 어렵습니다.

```mermaid
--8<-- "assets/part-02/chapter-12/train-val-test-flow-ko.mmd"
```

서로 다른 학생의 독립적인 기록을 무작위로 나누는 예에서는 `train_test_split`을 사용할 수 있습니다. 한 학생의 반복 기록이나 시간 순서가 있는 데이터라면 학생별 묶음이나 시간 순서를 고려해야 합니다. 행을 무작위로 나누는 것만으로 모든 누수가 차단되지는 않습니다.

## 사례: 학생 36명을 27명과 9명으로 나누기

[`student-progress-samples.csv`](../../../assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview }의 학생 36명으로 시험 전 합격 예측용 데이터를 준비합니다. 여기서는 공부 시간·결석 수·퀴즈 수가 모두 예측 시점까지 얻은 기록이라고 가정합니다. 최종 점수 `score`와 정답 `passed`는 입력에서 제외합니다.

저장소 루트에서 실행하면 입력은 `(36, 3)`, 정답은 `(36,)`입니다. 행의 25%인 9명을 테스트용으로 떼고 27명을 학습용으로 남깁니다.

```python
from pathlib import Path
from sklearn.model_selection import train_test_split

csv_path = Path("docs/assets/part-02/chapter-12/student-progress-samples.csv")
df = pd.read_csv(csv_path)

feature_columns = ["study_hours", "absences", "practice_quizzes"]
X = df[feature_columns]
y = df["passed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print("X shape:", X.shape)
print("y shape:", y.shape)
print("train/test shapes:", X_train.shape, X_test.shape, y_train.shape, y_test.shape)
```

```text
X shape: (36, 3)
y shape: (36,)
train/test shapes: (27, 3) (9, 3) (27,) (9,)
```

`test_size`를 `0.5`로 바꾸면 학습과 테스트가 각각 18명으로 나뉩니다. `random_state`를 바꾸면 선택한 학생이 달라질 수 있지만, 같은 비율에서는 행 수가 같습니다. 위 코드는 학습·테스트 분할 예시이며 검증 집합을 따로 만들지는 않습니다. 모델 설정을 비교하려면 학습 쪽에서 검증용 데이터를 추가로 나누거나 교차 검증을 사용합니다.

`stratify=y`는 합격·불합격 비율이 두 집합에 가능한 한 비슷하게 남도록 나눕니다. 정수 명수로 나누므로 비율이 완전히 같지는 않을 수 있습니다. 각 클래스의 기록이 너무 적거나 나눌 집합이 너무 작으면 층화 분할이 불가능합니다. 고정된 `random_state`는 같은 입력과 실행 조건에서 분할을 재현하기 위한 값이며, 한 번의 분할이 대표성을 보장하지는 않습니다.

## 입력·정답과 학생 중복 확인

분할 전부터 `X`와 `y`의 학생 순서는 같아야 합니다. `train_test_split`은 학생 ID를 찾아 잘못된 짝을 고쳐 주지 않으며, 함께 전달된 배열의 현재 행 대응을 유지해 나눕니다. 반환된 인덱스로 대응과 집합 간 중복을 확인할 수 있습니다.

```python
print(X_train.index.equals(y_train.index))
print(X_test.index.equals(y_test.index))
print(set(X_train.index).isdisjoint(X_test.index))

train_ids = set(df.loc[X_train.index, "student_id"])
test_ids = set(df.loc[X_test.index, "student_id"])
print(train_ids.isdisjoint(test_ids))
```

```text
True
True
True
True
```

앞 두 값은 입력과 정답의 라벨 순서가 같다는 뜻이고, 셋째는 행이 겹치지 않는다는 뜻입니다. 넷째는 학생 ID도 겹치지 않음을 확인합니다. 이 CSV에는 학생마다 한 행만 있지만, 한 학생의 반복 기록에서는 행이 달라도 학생이 겹칠 수 있습니다. 이때 새로운 학생에 대한 예측을 평가하려면 학생 단위로 분리해야 합니다.

## 검증용 학생 9명 남기기

27명의 학습 후보에서 9명을 다시 검증용으로 떼면 학습 18명·검증 9명·테스트 9명이 됩니다. 테스트 집합은 이 두 번째 분할에 사용하지 않습니다.

```python
X_fit, X_val, y_fit, y_val = train_test_split(
    X_train, y_train, test_size=9, random_state=42, stratify=y_train
)
print(len(X_fit), len(X_val), len(X_test))
```

```text
18 9 9
```

`test_size=9`는 9행, `test_size=0.25`는 전체의 25%를 뜻합니다. 이 세 집합으로 모델을 비교한다면 전처리 기준과 모델 학습에는 `X_fit`을 사용하고, 검증 결과로 설정을 고른 뒤 테스트를 마지막 평가에 사용합니다. 36명은 분할 절차를 확인하는 작은 예제이므로 안정적인 성능 추정 자료로 보지는 않습니다.

같은 분할과 중복 확인을 파일로 실행할 수 있습니다.

[p2_12_3_dataset_split_preview.py](../../../assets/part-02/chapter-12/p2_12_3_dataset_split_preview.py)

```bash
python docs/assets/part-02/chapter-12/p2_12_3_dataset_split_preview.py
```

## 학습 데이터에서 전처리 기준 계산

결측치를 평균으로 채우거나 값을 표준화할 때는 평균·표준편차 같은 기준을 데이터에서 계산합니다. 이 기준은 학습 데이터로만 정하고, 검증·테스트에는 같은 기준을 적용합니다. 테스트까지 합쳐 평균을 구하면 평가용 데이터의 정보가 학습에 섞입니다.

```mermaid
--8<-- "assets/part-02/chapter-12/no-leakage-preprocessing-flow-ko.mmd"
```

학습용 공부 시간이 `[2.0, 4.0, 결측치]`, 테스트용 시간이 `[10.0, 결측치]`라고 합시다. 학습에서 관측된 값의 평균은 3이므로 양쪽 결측치를 모두 3으로 채웁니다.

```python
train_hours = pd.Series([2.0, 4.0, None])
test_hours = pd.Series([10.0, None])

fill_value = train_hours.mean()
print(train_hours.fillna(fill_value).tolist())
print(test_hours.fillna(fill_value).tolist())
```

```text
[2.0, 4.0, 3.0]
[10.0, 3.0]
```

전체 관측값으로 평균을 구하면 `(2 + 4 + 10) / 3`, 약 5.33이 되어 학습용 결측치에도 테스트 정보가 반영됩니다. 테스트의 10을 100으로 바꿔도 학습에서 정한 채움 값은 3으로 유지되어야 합니다.

scikit-learn에서는 기준을 배우는 동작을 `fit`, 배운 기준을 적용하는 동작을 `transform`으로 구분합니다. 테스트 데이터에는 전처리의 `fit`이나 `fit_transform`을 호출하지 않습니다.

## 범주를 숫자 열로 표현하기

지역처럼 문자열로 된 범주는 모델에 따라 숫자 표현으로 바꿔야 합니다. `get_dummies`는 지역마다 지시 열을 만들고, 해당 지역이면 1, 아니면 0을 넣습니다. 다음 작은 표에서는 Busan·Seoul 두 열이 생깁니다.

```python
regions = pd.DataFrame({"region": ["Seoul", "Busan", "Seoul"]})
encoded = pd.get_dummies(regions, columns=["region"], dtype=int)
print(encoded)
```

```text
   region_Busan  region_Seoul
0             0             1
1             1             0
2             0             1
```

이 코드는 범주 표현만 보여 주는 독립 예제입니다. 학습·테스트를 각각 `get_dummies`에 넣으면 포함된 지역에 따라 열이 달라질 수 있습니다. 실제 학습에서는 학습 데이터로 범주와 열 구성을 정하고, 테스트에는 같은 구성을 적용하며 새로운 범주를 처리할 방법도 정해야 합니다.

## 결측치와 타입 확인

CSV의 열별 결측치 수와 타입을 확인하면, 채워야 할 값이나 숫자로 변환할 열이 있는지 알 수 있습니다. 다음 코드에서 학생 CSV의 결측치 수는 모든 열이 0입니다. 이는 값이 빠져 있지 않다는 뜻이며, 기록 시점이나 정답의 정확성까지 보장하지는 않습니다.

```python
print(df.isna().sum())
print(df.dtypes)
```

문자열 `"unknown"`이 들어 있는 숫자 열은 `isna()`만으로 미입력을 찾을 수 없습니다. 다음 코드는 숫자로 해석할 수 없는 값을 결측치로 바꿉니다.

```python
hours_text = pd.Series(["8.0", "unknown", "6.5"])
hours = pd.to_numeric(hours_text, errors="coerce")
print(hours.isna().tolist())
print(hours.dropna().tolist())
```

```text
[False, True, False]
[8.0, 6.5]
```

`errors="coerce"`는 잘못된 문자열의 의미를 판단하지 않고 결측치로 바꿉니다. 변환 후 결측치 수가 늘었다면 원래 표기와 입력 오류를 확인하고 처리 기준을 정합니다. 숫자로 읽힌 값도 음수 공부 시간처럼 허용 범위 밖일 수 있습니다.

## 체크리스트

- 예측 시점과 정답을 한 문장으로 정할 수 있는가?
- 최종 점수를 시험 전 입력에서 제외하는 이유를 설명할 수 있는가?
- 입력 `X`와 정답 `y`의 행을 같은 학생끼리 맞출 수 있는가?
- 학습·검증·테스트 데이터의 역할을 구분할 수 있는가?
- 테스트 값을 바꿔도 학습에서 구한 전처리 기준은 유지되어야 하는 이유를 설명할 수 있는가?
- 범주 인코딩에서 학습과 테스트의 열 구성을 맞춰야 하는 이유를 설명할 수 있는가?
- 분할 후 행 중복과 학생 중복을 구분하고, 검증 데이터를 학습 후보에서 따로 나눌 수 있는가?

## 출처와 참고 자료

- pandas Developers, [pandas.get_dummies](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 확인 날짜: 2026-07-20. 범주형 변수를 dummy/indicator 변수로 바꾸는 예시 확인에 사용했다.
- scikit-learn Developers, [Glossary](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, 확인 날짜: 2026-07-20. 1d/2d array, array-like, estimator 입력 관례와 `X`, `y` 용어 배경 확인에 사용했다.
- scikit-learn Developers, [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, 확인 날짜: 2026-09-15. 배열과 행렬을 train/test subset으로 나누는 API와 `test_size`, `random_state` 예시 확인에 사용했다.
- scikit-learn Developers, [Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, 확인 날짜: 2026-09-15. train/test 분리 전후의 전처리 순서와 data leakage 주의 설명 확인에 사용했다.
- pandas Developers, [pandas.to_numeric](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 확인 날짜: 2026-09-15. errors="coerce"의 수치 변환 실패 처리.
