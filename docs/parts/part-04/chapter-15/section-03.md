# P4-15.3 OOB(out-of-bag)와 랜덤포레스트 점검

> Section ID: `P4-15.3`
> Version: `v2026.07.31`

P4-15.1에서는 [랜덤포레스트(random forest)](../../../reference/concept-glossary-parts/04-rieul.md#random-forest)가 왜 여러 트리를 모아 더 안정적인 예측을 만들 수 있는지 보았습니다. P4-15.2에서는 그 숲이 무엇을 중요하게 보았는지, 즉 [특징 중요도(feature importance)](../../../reference/concept-glossary-parts/04-rieul.md#random-forest)를 조심해서 읽는 법을 보았습니다.

그러면 이제 남는 질문은 이것입니다.

이 숲이 정말 괜찮게 학습되고 있는지는 어떻게 점검할 수 있을까?

랜덤포레스트에서는 이 질문에 대해 먼저 만나는 손잡이 중 하나가 [OOB(out-of-bag)](../../../reference/concept-glossary-parts/08-ieung.md#oob-score)입니다.

OOB는 [bootstrap](../../../reference/concept-glossary-parts/06-bieup.md#bootstrap)에 뽑히지 않은 샘플을 이용해, 랜덤포레스트가 학습 중에 스스로를 거칠게 점검하는 내부 검증 방식이다.

즉, OOB는 `새로운 모델`이 아니라, 랜덤포레스트를 읽고 점검하는 방법입니다.

이 절도 랜덤포레스트의 기본 구조를 다시 길게 설명하지 않습니다. 핵심 직관은 P4-15.1과 [랜덤포레스트(random forest)](../../../reference/concept-glossary-parts/04-rieul.md#random-forest) 항목을 기준으로 다시 연결하고, 여기서는 bootstrap과 OOB가 점검 장치로 어떻게 이어지는지에만 집중합니다.

## OOB(out-of-bag)와 랜덤포레스트 점검에서 닫을 질문

이 절은 다음 질문에 답합니다.

- [OOB(out-of-bag)](../../../reference/concept-glossary-parts/08-ieung.md#oob-score)는 왜 생기는가?
- [bootstrap](../../../reference/concept-glossary-parts/06-bieup.md#bootstrap)과 OOB는 어떤 관계인가?
- [`oob_score=True`](../../../reference/concept-glossary-parts/08-ieung.md#oob-score)는 무엇을 뜻하는가?
- OOB 점수는 train accuracy, validation score, test score와 어떻게 다른가?
- OOB를 어디까지 믿고, 어디서 멈춰야 하는가?

OOB의 바깥 경계는 아래 정도만 잡아 두면 충분합니다.

| 항목 | 현재 본편에서의 회수 상태 |
| --- | --- |
| [교차검증(cross-validation)](../../../reference/concept-glossary-parts/01-giyeok.md#cross-validation)의 모든 변형 | 교차검증의 기본 역할은 P4-9.1, P4-9.3에서 다시 연결하지만, 모든 변형을 이 절에서 대신 설명하지는 않습니다. |
| [확률 보정(calibration)](../../../reference/concept-glossary-parts/14-hieut.md#probability-calibration)과 [threshold](../../../reference/concept-glossary-parts/08-ieung.md#threshold) 조정 | threshold와 calibration의 기본 감각은 P4-6.4, threshold 정책은 P4-11.1에서 다시 이어지지만, OOB 절에서 그 세부를 함께 전개하지는 않습니다. |
| 그래디언트 부스팅의 OOB 성격 차이 | 부스팅의 점검 감각은 P4-16.1, P4-16.2에서 validation과 early stopping 쪽으로 다시 이어지지만, OOB와의 세부 대비를 이 절에서 길게 다루지는 않습니다. |

즉, 이 절은 OOB를 `랜덤포레스트의 내부 점검판`으로 고정하는 데 집중하고, 더 넓은 평가 절차와 점수 운영 정책은 후속 절에서 질문별로 나누어 다시 읽는 편이 가장 자연스럽습니다.

## OOB(out-of-bag)와 랜덤포레스트 점검에서 남길 판단 기준

- OOB를 `bootstrap에 빠진 샘플을 이용한 내부 일반화 추정`으로 설명할 수 있습니다.
- 왜 `bootstrap=True`일 때만 OOB가 가능한지 말할 수 있습니다.
- OOB 점수와 test score를 같은 것으로 단정하면 왜 위험한지 설명할 수 있습니다.
- 랜덤포레스트 실험에서 `train / OOB / test`를 함께 읽는 기본 태도를 가질 수 있습니다.

## 왜 이 절이 필요한가

랜덤포레스트를 처음 쓰면 보통 이런 흐름을 겪습니다.

1. 일단 학습이 잘 된다.
2. train accuracy가 높게 나온다.
3. 그러면 모델이 좋은 것처럼 느껴진다.

하지만 이 흐름에는 큰 빈칸이 있습니다.

`훈련에 잘 맞는 것`과 `처음 보는 데이터에도 잘 맞는 것`은 다를 수 있습니다.

랜덤포레스트는 bootstrap을 쓰기 때문에, 학습 과정 안에서 `이번 트리가 보지 않은 샘플`이 생깁니다. OOB는 바로 이 틈을 활용합니다.

즉, 15.3은 `숲이 낸 점수 하나를 믿는 법`이 아니라 `숲의 상태를 여러 점수로 점검하는 법`을 배우는 절입니다.

## OOB는 왜 생기는가

scikit-learn 사용자 가이드는 random forest에서 각 트리가 bootstrap sample, 즉 복원추출(with replacement)한 샘플로 만들어진다고 설명합니다. 이렇게 복원추출을 하면 어떤 샘플은 한 트리에 여러 번 들어가고, 어떤 샘플은 그 트리 학습에서 아예 빠집니다.

그 빠진 샘플이 바로 out-of-bag sample입니다.

다음처럼 읽습니다.

- 한 트리는 전체 훈련 데이터를 다 보지 않는다.
- 그래서 `그 트리가 보지 않은 훈련 샘플`이 생긴다.
- 그 샘플로 그 트리를 부분적으로 점검할 수 있다.

즉, OOB는 bootstrap이 만든 부산물이고, 랜덤포레스트는 그 부산물을 점검 자원으로 다시 사용합니다.

## bootstrap과 OOB의 관계

한 장면으로 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-3-mermaid-01-ko.mmd"
```

이 그림에서 중요한 점은 OOB가 `별도의 추가 데이터셋`이 아니라는 것입니다. 여전히 훈련 세트 안의 샘플이지만, 특정 트리 입장에서는 `보지 않은 샘플`이었다는 점이 중요합니다.

## `oob_score=True`는 무엇을 뜻하는가

scikit-learn API 문서는 `oob_score`를 `out-of-bag samples를 사용해 generalization score를 추정할지`를 정하는 옵션으로 설명합니다. 그리고 이 기능은 `bootstrap=True`일 때만 사용할 수 있다고 설명합니다.

- `bootstrap=True`: 각 트리가 복원추출 샘플로 학습된다.
- `oob_score=True`: 빠진 샘플을 모아 내부 점검 점수를 계산한다.

즉, OOB는 bootstrap이 없으면 성립하지 않습니다. 모든 트리가 항상 전체 데이터를 다 본다면, `보지 않은 샘플`이라는 개념 자체가 사라지기 때문입니다.

## OOB는 어떤 점수인가

API 문서는 `oob_score_`를 training dataset에 대한 out-of-bag estimate로 얻은 score라고 설명합니다.

여기서 독자가 조심해야 할 점은 두 가지입니다.

1. OOB는 훈련 데이터 바깥의 완전한 새 데이터 점수가 아니다.
2. 그렇다고 단순한 train accuracy도 아니다.

즉, OOB는 둘 사이에 놓인 `내부 일반화 추정치`입니다.

| 점수 | 무엇을 기준으로 하나 |
| --- | --- |
| train accuracy | 학습에 직접 사용된 데이터에 얼마나 잘 맞았는가 |
| OOB score | 각 샘플을 보지 않은 트리들의 예측으로 얼마나 맞았는가 |
| test score | 완전히 따로 떼어 둔 데이터에 얼마나 맞았는가 |

그래서 OOB는 train score보다 현실적일 수 있지만, test score를 완전히 대체한다고 단정하면 위험합니다.

이 차이를 숫자 장면으로 짧게 압축하면 다음처럼 읽을 수 있습니다.

| 점수 패턴 | 먼저 떠올릴 해석 | 바로 이어질 질문 |
| --- | --- | --- |
| train만 매우 높다 | 훈련에 과하게 맞았을 수 있다 | OOB와 test도 같이 높은가? |
| train은 높고 OOB/test는 비슷하게 따라온다 | 숲이 내부 점검과 별도 검증에서 비교적 안정적일 수 있다 | 남는 오류 사례는 어떤 유형인가? |
| train, OOB, test가 모두 낮다 | 숲 자체보다 입력 표현이나 데이터 품질이 병목일 수 있다 | 특징(feature) 표현을 다시 봐야 하는가? |

즉, OOB 절의 핵심은 `점수 하나`보다 `점수 조합`입니다.

## OOB를 왜 편리하다고 느끼는가

scikit-learn 문서와 예제 설명은 OOB error가 random forest를 학습시키는 동안 검증 추정을 함께 얻을 수 있게 해 준다고 설명합니다.

이 장점은 실험 초반 점검에서 매우 실용적입니다.

- 작은 실험을 빠르게 반복할 수 있습니다.
- train score만 보는 실수를 줄일 수 있습니다.
- 트리 수(../../../reference/concept-glossary-parts/14-hieut.md#hyperparameter))를 늘릴 때 상태가 어떻게 바뀌는지 빨리 점검할 수 있습니다.

즉, OOB는 `정식 평가의 종착점`이라기보다 `빠른 내부 점검판`에 가깝습니다.

## 그렇다면 OOB만 보면 충분한가

여기서 반드시 한 번 멈춰야 합니다.

`아니다. 보통은 OOB만으로 끝내지 않는다.`

이유는 간단합니다.

- OOB는 bootstrap 구조에 의존한 내부 추정입니다.
- 실제 배포 상황의 새 데이터와 완전히 같은 조건은 아닙니다.
- 데이터가 작거나, 클래스 불균형이 있거나, 평가 기준이 민감하면 따로 떼어 둔 validation/test 점수가 여전히 중요합니다.

OOB의 역할은 다음 기준으로 구분됩니다.

| 상황 | OOB의 역할 |
| --- | --- |
| 빠른 실험 초반 | 매우 유용한 내부 점검 |
| 하이퍼파라미터 대략 탐색 | 참고 지표로 유용 |
| 최종 성능 보고 | test/validation과 함께 봐야 함 |
| 배포 전 최종 판단 | OOB 하나로 끝내지 않음 |

### 언제 OOB를 특히 유용하게 쓸 수 있는가

OOB는 모든 평가를 대체하지는 않지만, 랜덤포레스트 실험 초반에는 매우 실용적인 내부 점검판이 됩니다.

| 현재 상황 | OOB가 특히 유용한 이유 | 같이 확인할 것 |
| --- | --- | --- |
| 빠르게 여러 숲 설정을 비교하고 싶다 | bootstrap 안에서 내부 점검 점수를 같이 얻을 수 있기 때문 | test를 마지막 확인용으로 남기는지 |
| train 점수가 너무 높아 불안하다 | train보다 덜 낙관적인 내부 추정치를 볼 수 있기 때문 | OOB와 test 간격 |
| `n_estimators`를 늘릴지 고민 중이다 | 트리 수 변화에 따라 내부 안정성을 빨리 볼 수 있기 때문 | 계산 비용 대비 개선 폭 |
| validation 세트를 크게 쓰기 어려운 작은 실험이다 | 별도 분할 없이 추가 점검 신호를 얻을 수 있기 때문 | OOB를 최종 보고 점수로 착각하지 않는지 |
| bootstrap 기반 숲이 제대로 작동하는지 보고 싶다 | 보지 않은 샘플 예측을 통해 내부 상태를 점검할 수 있기 때문 | `bootstrap=True` 설정 여부 |

이 표의 핵심은 OOB를 `최종 진실`이 아니라 `빠른 내부 상태 점검판`으로 올바르게 위치시키는 데 있습니다.

## train / OOB / test를 함께 읽는 이유

랜덤포레스트 점검에서는 세 숫자를 같이 놓고 보는 습관이 중요합니다.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-3-mermaid-02-ko.mmd"
```

예를 들어:

- train은 매우 높고 OOB와 test가 많이 낮으면: [과적합(overfitting)](../../../reference/concept-glossary-parts/01-giyeok.md#overfitting)을 의심할 수 있습니다.
- train, OOB, test가 모두 비슷하게 낮으면: 표현력 부족이나 데이터 한계를 의심할 수 있습니다.
- train은 높고 OOB와 test가 비슷하게 따라오면: 비교적 안정적인 상태로 읽을 수 있습니다.

이 절의 핵심은 특정 숫자 하나보다 `숫자 사이의 간격`입니다.

## Python 예제로 OOB 점수 보기

이번 예제는 유방암(breast cancer) 분류 데이터에서 train / OOB / test를 같이 출력해 보는 작은 실습입니다.

- 문제 상황: 랜덤포레스트가 학습에 잘 맞는지, 내부 점검과 별도 test에서도 비슷하게 가는지 본다.
- 입력(input): 30개 연속형 특징
- 정답(label): 악성/양성 class
- 확인할 개념:
  - OOB는 `oob_score_`로 읽는다
  - OOB는 train과 test 사이에서 내부 점검 역할을 한다
  - 세 점수의 간격을 같이 본다
- 조작해 볼 값:
  - `n_estimators`를 100, 300, 600으로 바꿔 OOB와 test 간격이 안정되는지 본다.
  - `random_state`를 바꿔도 train/OOB/test 패턴이 유지되는지 본다.

```python
# 유방암 분류에서 train, OOB, test 점수를 함께 출력해 간격을 읽는 예제입니다.
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    bootstrap=True,
    oob_score=True,
    random_state=42
)
model.fit(X_train, y_train)

print("train accuracy:", round(model.score(X_train, y_train), 3))
print("oob score     :", round(model.oob_score_, 3))
print("test accuracy :", round(model.score(X_test, y_test), 3))
print("n_estimators  :", model.n_estimators)
```

실행 결과 예시는 다음과 비슷하게 나올 수 있습니다. 실제 값은 데이터 분할, 라이브러리 버전, 난수 설정에 따라 조금 달라질 수 있습니다.

```text
train accuracy: 1.0
oob score     : 0.96
test accuracy : 0.947
n_estimators  : 300
```

이 결과를 읽는 순서는 다음과 같습니다.

1. train accuracy가 1.0이므로, 숲은 훈련 세트를 매우 잘 설명했다.
2. 그러나 train만 보면 너무 낙관적일 수 있다.
3. OOB 0.96과 test 0.947이 크게 벌어지지 않으므로, 이 실험에서는 숲이 완전히 허상만 학습한 것은 아니라는 신호를 준다.

물론 이것만으로 모델이 충분히 좋다고 확정할 수는 없습니다. 하지만 `train 1.0`이라는 숫자를 바로 믿지 않게 해 주는 점에서 OOB는 매우 유용합니다.

## Python 예제로 트리 수가 늘 때 OOB가 어떻게 보이는지 보기

이번 예제는 `n_estimators`를 바꾸며 OOB와 test가 어떻게 움직이는지 보는 실습입니다.

문제 상황:

- 랜덤포레스트에서 트리 수를 늘릴 때 OOB 점수와 test 점수가 어떻게 변하는지 함께 보는 연습이 필요하다

입력(input):

- 유방암 데이터셋 `X`, `y`
- 여러 `n_trees`

기대 출력(output):

- 트리 수별 OOB score
- 트리 수별 test score

확인할 개념:

- 트리 수가 늘면 보통 OOB가 어느 정도 안정되는 방향을 볼 수 있다
- 무조건 트리를 많이 늘린다고 모든 문제가 해결되지는 않는다

조작해 볼 값:

- `[10, 50, 100, 300]` 목록에 600을 추가해 개선 폭과 계산 비용을 같이 본다.
- `max_depth`를 제한한 경우와 제한하지 않은 경우의 train/OOB/test 간격을 비교한다.

```python
# n_estimators를 바꾸며 OOB 점수와 test 점수가 어떻게 움직이는지 비교하는 예제입니다.
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for n_trees in [10, 50, 100, 300]:
    model = RandomForestClassifier(
        n_estimators=n_trees,
        bootstrap=True,
        oob_score=True,
        random_state=42
    )
    model.fit(X_train, y_train)

    print(
        f"trees={n_trees:3d} | "
        f"oob={model.oob_score_:.3f} | "
        f"test={model.score(X_test, y_test):.3f}"
    )
```

실행 결과 예시는 다음과 비슷하게 나올 수 있습니다. 실제 값은 데이터 분할, 라이브러리 버전, 난수 설정에 따라 조금 달라질 수 있습니다.

```text
trees= 10 | oob=0.942 | test=0.947
trees= 50 | oob=0.957 | test=0.947
trees=100 | oob=0.960 | test=0.947
trees=300 | oob=0.960 | test=0.947
```

이 예제에서 독자가 읽어야 할 것은:

- 트리 수가 너무 적을 때는 OOB가 다소 흔들릴 수 있습니다.
- 어느 정도 이후에는 OOB가 안정되는 모습이 보일 수 있습니다.
- 하지만 test 점수가 같은 수준에 머물 수 있으므로, `트리를 계속 늘리면 성능이 계속 오른다`고 읽으면 안 됩니다.

즉, OOB는 `언제쯤 숲이 대체로 안정되는가`를 보는 데 도움을 줄 수 있지만, 그 자체가 성능 보증서는 아닙니다.

이때 OOB를 점수 하나로만 두지 말고, 어떤 비교 기준과 어떤 남는 사례를 함께 적을지 바로 정리해 둡니다. 같은 OOB나 test 점수처럼 보여도 반복해서 남는 오류 유형이 다를 수 있으므로, 점수 패턴과 사례 패턴을 함께 읽습니다.

| 같이 남길 항목 | 이번 절에서 적는 내용 | 왜 필요한가 |
| --- | --- | --- |
| 내부 비교 기준 | train / OOB / test 간격 | 훈련 적합과 일반화 추정이 얼마나 벌어지는지 보기 위해 |
| 남는 review 사례 | OOB와 test에서 반복해서 틀리는 샘플 | 숲을 더 키울지, 특징 표현을 다시 볼지 가르기 위해 |
| 다음 검증 질문 | 트리 수, 깊이, 특징 표현 중 어디를 먼저 바꿀지 | 점수 해석을 다음 실험 순서로 넘기기 위해 |

## OOB를 해석할 때 자주 생기는 오해

특히 자주 생기는 오해는 다음과 같습니다.

| 오해 | 더 안전한 해석 |
| --- | --- |
| OOB가 높으니 배포해도 된다 | OOB는 내부 점검일 뿐, 최종 검증은 따로 필요하다 |
| OOB가 test와 비슷하니 항상 같다 | 이번 실험에서 비슷했을 뿐이다 |
| OOB가 있으면 validation split은 필요 없다 | 상황에 따라 여전히 필요하다 |
| OOB가 낮으면 랜덤포레스트는 쓸모없다 | 데이터 품질, 특징 표현, 하이퍼파라미터를 함께 봐야 한다 |

중요한 것은 `OOB를 과소평가하지도, 과대평가하지도 않는 태도`입니다.

### OOB와 test가 엇갈리면 무엇을 먼저 의심해야 하나

초심자는 OOB와 test가 비슷하게 나와야만 정상이라고 생각하기 쉽습니다. 하지만 두 값이 조금 다르게 나오는 것 자체는 이상한 일이 아닙니다. 더 중요한 것은 `왜 다르게 보이는가`를 성급히 단정하지 않는 것입니다.

| 보인 장면 | 먼저 의심할 것 | 이유 |
| --- | --- | --- |
| OOB는 괜찮은데 test가 더 낮다 | hold-out 분할 차이, 데이터 대표성 차이 | OOB는 내부 추정이고 test는 완전히 따로 떼어 둔 샘플이기 때문입니다. |
| OOB는 낮은데 test는 조금 더 높다 | bootstrap 기반 내부 추정의 흔들림, 작은 데이터 크기 | 특정 실험에서는 OOB가 더 보수적으로 보일 수도 있기 때문입니다. |
| 둘 다 흔들린다 | 데이터 수 부족, 클래스 불균형, 특징 표현 약함 | 숲의 구조보다 데이터 상태가 먼저 문제일 수 있기 때문입니다. |

여기서 중요한 것은 `어느 쪽이 진짜인가`를 즉시 고르는 일이 아닙니다. 같은 조건에서 실험을 반복했을 때 패턴이 유지되는지, 남는 오류 사례가 비슷한지, 데이터 분할이 대표성을 크게 잃지 않았는지를 같이 보는 일입니다.

## OOB와 랜덤포레스트 점검: 확인할 판단 기준

이 사례 절은 다음 질문으로 중심축을 확인한다.

- 오픈체크리스트의 중심축 문장인 "OOB 점검이 추가 검증 기준이라는 점을 보여 주어야 합니다."를 본문 사례에서 어느 대목으로 확인할 수 있는가?
- 표, 코드, 도식, 체크리스트 중 어떤 장치가 이 판단을 다시 검토하게 만드는가?

### 사례 1. 훈련 점수는 완벽한데 정말 괜찮은 숲인지 빨리 점검하고 싶을 때

사기 거래 탐지 팀이 랜덤포레스트를 학습했더니 train accuracy가 거의 완벽하게 나옵니다. 사람이 먼저 보던 기준은 `짧은 시간 내 반복 결제`, `이상한 지역`, `심야 거래` 같은 신호였습니다.

이 높은 훈련 점수만 보면 모델이 충분히 좋아졌다고 느낄 수 있습니다. 하지만 팀은 이미 결정트리에서 `훈련에 잘 맞는다`와 `새 데이터에도 잘 맞는다`가 다를 수 있다는 점을 배웠습니다. 랜덤포레스트에서는 bootstrap 때문에 각 트리가 보지 않은 샘플이 생기므로, 그 틈을 이용해 OOB 점수로 내부 점검을 합니다.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-3-mermaid-03-ko.mmd"
```

이 장면에서 OOB는 `최종 성능 점수`가 아니라 `내부 일반화 추정치`로 읽어야 합니다. train 점수는 높지만 OOB와 test가 함께 낮다면 여전히 과적합이나 데이터 표현 문제를 의심해야 하고, train과 OOB, test가 큰 차이 없이 따라오면 비교적 안정적인 숲으로 읽습니다. 즉, 중요한 것은 숫자 하나가 아니라 숫자 사이의 간격입니다.

확인 가능한 결과는 train / OOB / test를 나란히 볼 때 드러납니다. OOB가 train보다 훨씬 낮다면 낙관적 해석을 멈추게 해 주고, OOB와 test가 비슷하게 움직인다면 숲의 상태를 빠르게 점검하는 유용한 손잡이가 됩니다.

이 사례를 메모 형식으로 더 짧게 남기면 다음처럼 적을 수 있습니다.

| 관찰한 점수 패턴 | 바로 붙일 해석 | 남겨 둘 review 사례 | 다음 질문 |
| --- | --- | --- | --- |
| train은 매우 높고 OOB/test가 더 낮다 | 숲이 훈련 데이터에는 과하게 맞고 있을 수 있다 | 반복 오류가 나는 거래 유형, 희귀 패턴, 클래스 불균형 사례 | 트리 깊이와 특징 표현을 먼저 줄이거나 다시 설계할까 |
| train, OOB, test가 비슷하게 따라온다 | 현재 숲은 내부 점검과 별도 검증에서 비교적 안정적이다 | 여전히 남는 오탐/미탐 사례 | threshold나 중요도 해석으로 넘어가도 될까 |

### 사례 2. OOB는 좋아 보이는데 test가 기대보다 더 낮을 때

품질 검사 팀이 불량 탐지용 랜덤포레스트를 학습했더니 train은 높고 OOB도 꽤 좋아 보였다고 하겠습니다. 그래서 `이 정도면 충분한 것 아닌가?`라고 느끼기 쉽습니다. 그런데 별도로 떼어 둔 test에서는 기대보다 점수가 더 낮게 나올 수 있습니다.

이 장면에서 사람이 먼저 내리기 쉬운 판단은 `OOB가 틀렸다` 또는 `test가 우연히 나빴다`입니다. 하지만 더 안전한 해석은 둘 다 바로 폐기하지 않고, `내부 추정과 별도 검증이 왜 벌어졌는가`를 먼저 묻는 것입니다. 특정 기간 데이터가 test에 더 많이 몰렸는지, 희귀 불량 유형이 hold-out 쪽에 더 들어갔는지, 현재 특징 표현이 일부 패턴을 놓치는지부터 다시 봐야 합니다.

즉, OOB와 test가 엇갈릴 때의 핵심은 `둘 중 하나를 즉시 정답으로 고르는 일`이 아니라, `어떤 데이터 장면에서 차이가 커졌는가`를 찾아 다음 실험의 순서를 정하는 데 있습니다. 이때는 숲을 더 키우는 것보다 데이터 분할, 반복 오류 사례, 특징 표현을 먼저 다시 보는 편이 더 안전할 수 있습니다.

## 실무에서 어떻게 쓰는가

실무 흐름으로 바꾸면 OOB는 보통 다음처럼 읽을 수 있습니다.

1. baseline 모델로 랜덤포레스트를 빠르게 학습한다.
2. train score와 OOB score를 함께 본다.
3. 너무 낙관적인 train score만 보고 멈추지 않는다.
4. 필요하면 validation/test로 다시 확인한다.
5. 그 다음에야 특징 중요도나 threshold 같은 해석/조정을 본다.

즉, OOB는 `점검 순서`를 바로잡아 주는 장치입니다.

이 절의 결과도 같은 회고 구조로 곧바로 정리할 수 있습니다.

| Part 4에서 남길 질문 | Part 6 회고 문서 언어 |
| --- | --- |
| train / OOB / test는 각각 얼마였는가? | 사실(fact) |
| 숫자 사이 간격이 과적합, 안정, 표현 부족 중 무엇을 시사하는가? | 해석(interpretation) |
| 다음 실험에서 트리 수, 특징, validation 구성을 어디부터 다시 볼 것인가? | 다음 질문(next question) |

예를 들어 train만 높고 OOB가 낮으면 지금 숲이 훈련 데이터에만 낙관적으로 맞고 있을 수 있습니다. 이때는 트리 깊이, 특징 표현, validation 분리를 다시 점검해야 합니다. 반대로 `OOB와 test가 함께 낮으면 숲 자체보다 입력 표현이나 데이터 품질을 다시 봐야 한다.` 이런 판단까지 붙어야 OOB가 점수 설명을 넘어 다음 실험 순서를 정하는 기준이 됩니다.

이 절에서는 여기서 한 번 더 멈춰, `지금 당장 무엇을 바꿀 것인가`와 `아직 나중으로 미룰 판단은 무엇인가`를 같이 구분해 둡니다.

| 먼저 보인 신호 | 지금 바로 읽어야 할 뜻 | 바로 이어질 다음 조치 | 아직 이 단계에서 서두르지 않을 판단 |
| --- | --- | --- | --- |
| train만 높고 OOB/test가 낮다 | 숲이 훈련 데이터에는 너무 잘 맞고 있을 수 있다 | 트리 깊이, 최소 샘플 수, 특징 표현, validation 분리를 먼저 다시 본다 | threshold나 서비스 정책을 먼저 만지지 않는다 |
| train, OOB, test가 모두 함께 낮다 | 숲 자체보다 입력 표현이나 데이터 품질이 더 큰 병목일 수 있다 | 특징 설계, 누락 변수, 데이터 품질, baseline 대비 개선폭을 다시 본다 | 트리 수만 계속 늘리며 해결하려고 하지 않는다 |
| OOB와 test가 비슷하게 따라온다 | 현재 숲은 내부 점검과 별도 test에서 비슷한 상태다 | 이때부터 특징 중요도, threshold, 후속 앙상블 비교로 넘어간다 | OOB 하나만 보고 최종 배포 판단을 끝내지 않는다 |

즉, OOB 절의 핵심은 `점수가 얼마인가`보다 `이 점수 패턴이면 다음 실험에서 무엇을 바꾸고, 무엇은 아직 미뤄야 하는가`를 바로 말할 수 있게 되는 데 있습니다.

### OOB를 본 뒤 최소한 같이 남길 실험 메모

OOB는 숫자 하나만 적고 지나가면 금방 의미가 흐려집니다. 최소한 다음 네 줄은 같이 남기는 편이 좋습니다.

| 항목 | 적는 예 |
| --- | --- |
| observed scores | `train=1.00, OOB=0.96, test=0.947` |
| first interpretation | `train 대비 OOB/test 간격은 있지만 완전히 붕괴한 상태는 아니다` |
| review cases | `희귀 불량 유형과 반복 오탐 사례를 다시 본다` |
| next action | `트리 수를 더 늘리기보다 특징 표현과 validation 분리를 먼저 재검토한다` |

이 메모가 있으면 OOB 절이 단순 점수 소개를 넘어, 다음 조정 순서를 남기는 실험 기록으로 바뀝니다.

이 절의 다음 장면은 그래디언트 부스팅(gradient boosting)입니다. 랜덤포레스트가 `여러 트리를 병렬적으로 모아 흔들림을 줄이는 방식`이었다면, 바로 다음 P4-16의 부스팅은 `이전 오류를 다음 트리가 순차적으로 보정하는 방식`으로 넘어갑니다.

## 체크리스트

- OOB를 test score와 같은 것으로 읽고 있지 않은가?
- `bootstrap=True`일 때만 OOB가 가능하다는 점을 설명할 수 있는가?
- train / OOB / test 세 숫자의 간격을 함께 보고 있는가?
- OOB가 bootstrap에 빠진 샘플을 활용한 내부 점검 방식이고, `oob_score=True`는 bootstrap 기반 랜덤포레스트에서만 의미가 있다는 점을 설명할 수 있는가
- OOB는 train score보다 현실적일 수 있지만 test score를 완전히 대체하지는 않는다는 점을 설명할 수 있는가
- 랜덤포레스트 점검에서는 `train / OOB / test`를 함께 읽어야 한다는 점을 설명할 수 있는가

## 출처와 참고 자료

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, 확인 날짜: 2026-07-26. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `RandomForestClassifier`, scikit-learn API Reference, 확인 날짜: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
