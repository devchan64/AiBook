# P4-11.5 보충학습: solver와 regularization을 처음 읽는 법

> Section ID: `P4-11.5`
> Version: `v2026.07.26`

로지스틱 회귀를 라이브러리로 써 보면 곧 solver, penalty, `C` 같은 인자를 만나게 됩니다. 초심자는 이 지점에서 `갑자기 구현 세부로 넘어갔다`고 느끼기 쉽습니다. 하지만 이 설정들은 이론과 완전히 분리된 잡음이 아닙니다.

이 절의 중심 질문은 다음입니다.

왜 같은 로지스틱 회귀라도 solver와 regularization 설정을 함께 기록하고 비교해야 하는가?

## solver와 regularization을 처음 읽을 때 닫을 질문

이 절은 다음 질문에 답합니다.

- solver는 무엇을 하는가?
- regularization은 무엇을 조절하는가?
- penalty와 `C`는 어떤 방향으로 읽으면 되는가?

이 절은 solver와 regularization을 `같은 모델명 안에서도 결과 해석을 바꾸는 비교 조건`으로 먼저 닫고, 라이브러리 옵션 암기보다 계산 절차와 규제 방향을 읽는 데 집중합니다.

## solver와 regularization에서 남길 판단 기준

- solver를 `파라미터를 실제로 찾는 계산 절차`로 설명할 수 있습니다.
- regularization을 `학습 데이터에 너무 바짝 맞추지 않게 조절하는 장치`로 설명할 수 있습니다.
- L1, L2, Elastic-Net, `C`의 방향성을 초심자 수준에서 읽을 수 있습니다.
- 같은 모델명이라도 설정 차이가 결과 해석을 바꾼다는 점을 설명할 수 있습니다.

## 학습 배경

로지스틱 회귀는 보통 닫힌 해(closed-form solution)를 바로 적기보다, 반복 계산을 통해 좋은 파라미터를 찾는 쪽으로 구현됩니다. 그래서 어떤 데이터 크기인지, 희소 행렬(sparse matrix)인지, 어떤 규제항을 쓰는지에 따라 설정 선택이 중요해집니다.

[regularization](../../../reference/concept-glossary-parts/09-jieut.md#regularization)은 `학습 데이터에 너무 바짝 맞추지 않게 조절하는 장치`로 먼저 읽으면 됩니다. 같은 로지스틱 회귀라도 데이터가 적거나 특징이 많으면, 계수가 불안정하게 커지거나 특정 특징에 과하게 기대는 문제가 생길 수 있습니다. 이때 regularization이 계수를 더 보수적으로 잡게 도와줍니다.

## 주요 학습내용

### solver는 학습을 실제로 계산하는 절차다

먼저 solver는 `이 모델의 파라미터를 실제로 어떻게 찾을 것인가`와 연결됩니다.

간단히 표로 정리하면 다음과 같습니다.

| 설정 | 지금 절에서 먼저 이해할 뜻 | 뒤에서 더 깊게 볼 질문 |
| --- | --- | --- |
| solver | 파라미터를 실제로 찾는 계산 절차 | 데이터 크기와 희소성에 따라 무엇이 유리한가 |
| penalty | 계수를 얼마나 보수적으로 잡을지 정하는 규제 방식 | L1, L2가 어떤 차이를 만드는가 |
| `C` | 규제 강도의 반대 방향 조절값 | 과적합과 과소적합 사이를 어떻게 읽는가 |

즉, solver는 `라이브러리의 사소한 옵션`이 아니라, MLE나 log loss로 세운 학습 목적을 실제 계산으로 구현하는 손잡이입니다.

아래 표는 `2026-07-26`에 확인한 scikit-learn stable 문서 기준의 구현 설명입니다. solver 지원 범위와 기본값은 라이브러리 버전에 따라 달라질 수 있으므로, 실제 실습이나 프로젝트에서는 사용 중인 버전 문서를 다시 확인해야 합니다.

| solver | 다중 클래스(multinomial) | penalty / regularization | 먼저 읽을 특징 |
| --- | --- | --- | --- |
| `lbfgs` | 지원 | L2 또는 규제 없음 | 기본값으로 넓게 무난한 편 |
| `liblinear` | 직접적인 multinomial은 미지원 | L1, L2 | 작은 데이터와 이진 분류에서 자주 언급 |
| `newton-cg` | 지원 | L2 또는 규제 없음 | 2차 정보 기반 최적화 계열 |
| `newton-cholesky` | 지원 | L2 또는 규제 없음 | `n_samples`가 매우 크고 one-hot 특징이 많을 때 후보 |
| `sag` | 지원 | L2 또는 규제 없음 | 큰 데이터에서 빠른 편, 스케일 민감 |
| `saga` | 지원 | L1, L2, Elastic-Net | 희소 입력과 Elastic-Net까지 다루기 쉬움 |

이 표를 읽을 때 먼저 잡아야 할 판단은 다음 정도입니다.

- `multinomial을 직접 쓰려는가`를 먼저 봅니다.
- `L1`이나 `Elastic-Net`이 필요한가를 봅니다.
- 데이터가 크고 특징도 많다면 큰 데이터에서 유리한 계열을 먼저 떠올립니다.
- 기본 출발점이 필요하면 `lbfgs`가 무난한 첫 후보가 됩니다.

### regularization은 계수를 더 보수적으로 잡게 하는 장치다

regularization 쪽도 최소한 다음 감각은 눈에 보여야 합니다.

| 설정 | 수식에서 보는 모습 | 입문적으로 읽을 뜻 |
| --- | --- | --- |
| L2 | \(\lambda \sum_j w_j^2\) | 계수를 전반적으로 작게 눌러 과도한 흔들림을 줄임 |
| L1 | \(\lambda \sum_j |w_j|\) | 일부 계수를 0 쪽으로 강하게 밀어 희소성을 만들 수 있음 |
| Elastic-Net | \(\lambda_1 \sum_j |w_j| + \lambda_2 \sum_j w_j^2\) | L1과 L2의 성격을 섞음 |
| `C` | 규제 강도의 역수 | `C`가 작을수록 규제가 더 강해짐 |

이 수식들을 해석 문장으로 바로 바꾸면 다음과 같습니다.

- L2는 `큰 계수를 전체적으로 덜 선호한다`는 뜻이라, 경계가 특정 특징 하나에 과하게 끌리는 일을 줄이는 쪽으로 읽을 수 있습니다.
- L1은 `덜 중요한 특징의 계수를 0으로 밀 수 있다`는 뜻이라, 특징 선택 효과와 더 직접 연결됩니다.
- Elastic-Net은 `전반적으로 줄이되 일부는 0으로 만들고 싶다`는 절충으로 읽을 수 있습니다.
- `C`는 scikit-learn에서 자주 보는 조절 손잡이인데, `작을수록 규제가 더 강하다`는 방향을 꼭 기억해야 합니다.

### solver와 regularization은 구현 옵션이 아니라 비교 조건이다

P4-8에서 baseline을 비교할 때 `같은 분할, 같은 지표, 같은 실패 사례` 위에 올려놓아야 비교가 된다고 보았습니다. solver와 regularization도 비슷하게 읽어야 합니다.

- solver를 바꾸면 계산 과정과 수렴 특성이 달라질 수 있습니다.
- regularization 강도를 바꾸면 계수 크기와 경계의 보수성이 달라질 수 있습니다.

즉, `같은 로지스틱 회귀`라고 말해도 실제 비교에서는 어떤 solver와 어떤 규제를 썼는지 기록해야 합니다. 그래야 성능 차이가 `모델 구조 때문인지`, `설정 차이 때문인지`를 구분할 수 있습니다.

## 사례 및 예시

사례를 읽기 전에 이번 절의 비교 프레임을 먼저 한 표로 잡으면 다음과 같습니다.

| 장면 | 사람이 먼저 쓰기 쉬운 기준 | 그 기준의 한계 | solver / regularization이 바꾸는 점 | 확인할 결과 |
| --- | --- | --- | --- | --- |
| 설정 선택 | 기본값만 쓰면 된다고 본다 | 데이터 구조와 설정 차이를 놓친다 | 계산 절차와 규제 강도를 비교 조건으로 읽게 한다 | 같은 모델명이라도 결과 해석이 달라질 수 있음 |
| 계수 해석 | 큰 계수도 그대로 받아들인다 | 데이터 부족이나 특징 과다의 흔들림을 놓친다 | regularization으로 더 보수적인 계수 해석을 하게 한다 | 경계와 계수의 안정성이 달라질 수 있음 |

### 사례 1. 희소한 텍스트 분류와 정형 표 데이터는 왜 같은 설정으로 읽기 어려운가

단어 수가 많은 스팸 분류에서는 특징 수가 많고 희소한 입력이 흔합니다. 반면 고객 이탈 예측처럼 정형 표 데이터에서는 특징 수가 비교적 적고 해석 가능성이 중요할 수 있습니다. 이때 solver와 regularization은 같은 값으로 고정되는 보편 상수가 아니라, 데이터 구조와 운영 목적에 따라 다시 읽어야 하는 손잡이가 됩니다.

### 사례 2. 성능 차이가 모델 차이인지 설정 차이인지 어떻게 구분하는가

실험 A와 실험 B가 둘 다 로지스틱 회귀인데, 한쪽은 `lbfgs + L2`, 다른 쪽은 `saga + Elastic-Net`을 썼다면 결과 차이를 단순히 `로지스틱 회귀가 좋아졌다`고 읽으면 안 됩니다. 이 경우에는 모델명보다 설정 차이가 더 큰 원인일 수 있습니다.

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-5-mermaid-01-ko.mmd"
```

## 연습 및 예제

### Python 예제로 설정 비교 기록을 남기는 방식 보기

아래 예제는 실제 학습보다 `비교 기록을 어떻게 남겨야 하는가`를 보여 주는 장난감 코드입니다.

조작해 볼 값:

- `C`를 `0.1`, `1.0`, `10.0`으로 바꾸며 regularization 강도 방향을 기록할 수 있습니다.
- `penalty`를 `l1`로 바꿀 때는 `solver`도 `saga`처럼 지원되는 조합인지 함께 확인해야 합니다.

```python
# solver와 regularization 설정이 로지스틱 회귀 학습 조건을 어떻게 바꾸는지 확인하는 예제입니다.
from sklearn.linear_model import LogisticRegression

configs = [
    {
        "name": "baseline_lr",
        "solver": "lbfgs",
        "penalty": "l2",
        "C": 1.0,
    },
    {
        "name": "sparse_candidate",
        "solver": "saga",
        "penalty": "elasticnet",
        "l1_ratio": 0.5,
        "C": 0.5,
    },
]

models = []
for cfg in configs:
    kwargs = {
        "solver": cfg["solver"],
        "penalty": cfg["penalty"],
        "C": cfg["C"],
        "max_iter": 1000,
    }
    if "l1_ratio" in cfg:
        kwargs["l1_ratio"] = cfg["l1_ratio"]
    models.append((cfg["name"], LogisticRegression(**kwargs)))

for name, model in models:
    print(name, "->", model)
```

이 예제에서 중요한 것은 모델을 바로 실행하는 것보다, `같은 로지스틱 회귀라도 어떤 설정 조합을 비교했는지 분리해서 기록한다`는 점입니다.

실행 결과 예시는 다음과 같습니다.

```text
baseline_lr -> LogisticRegression(max_iter=1000)
sparse_candidate -> LogisticRegression(C=0.5, l1_ratio=0.5, max_iter=1000,
                                       penalty='elasticnet', solver='saga')
```

## 출처와 참고 자료

- scikit-learn, `LogisticRegression` API documentation, [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-26
- scikit-learn, linear models user guide, [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-26
