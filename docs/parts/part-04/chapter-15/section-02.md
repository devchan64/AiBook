# P4-15.2 특징 중요도(feature importance)

> Section ID: `P4-15.2`
> Version: `v2026.07.12`

P4-15.1에서는 랜덤포레스트(random forest)가 왜 여러 트리를 모아 더 안정적인 예측을 만들 수 있는지 보았습니다. 그러면 바로 다음 질문이 생깁니다.

이 숲은 무엇을 중요하게 보고 판단했는가?

이 질문이 특징 중요도(feature importance)의 출발점입니다.

특징 중요도는 모델이 어떤 특징을 더 자주, 더 크게 활용했는지 요약한 숫자이지만, 그 숫자를 곧바로 원인이나 진실의 순위라고 읽으면 위험하다.

특징 중요도는 유용한 요약이지만, 해석의 함정도 함께 가진 도구입니다.

이 절은 랜덤포레스트의 기본 정의를 다시 길게 반복하지 않습니다. `여러 트리의 합의로 흔들림을 줄인다`는 핵심 직관은 P4-15.1과 [개념사전](../../../reference/concept-glossary.md)을 기준으로 다시 연결하고, 여기서는 그 숲이 무엇을 중요하게 보았는지 해석하는 문제에만 집중합니다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 랜덤포레스트에서 특징 중요도는 어떻게 만들어지는가?
- `feature_importances_`는 무엇을 뜻하는가?
- impurity-based importance와 permutation importance는 어떻게 다른가?
- 왜 중요한 숫자처럼 보여도 오해를 만들 수 있는가?
- PDP(partial dependence plot), SHAP는 중요도와 무엇이 다른 해석 질문을 던지는가?
- 왜 중요도 해석을 바로 인과 추론(causal inference)으로 넘기면 안 되는가?
- 상관 특성이 매우 강한 실제 데이터에서는 어떤 보수적 해석 전략이 필요한가?

이 절은 다음 내용은 깊게 다루지 않습니다.

- PDP, SHAP의 구현 라이브러리별 세부 옵션
- 인과 추론의 식별 가정과 추정 절차 전체
- 대규모 상관 구조 해소를 위한 전체 파이프라인 설계

이 절은 중요도 해석의 바깥 경계만 남기는 데서 끝내지 않고, `숫자 요약만으로 부족할 때 무엇을 더 봐야 하는가`, `왜 원인 해석과 구분해야 하는가`, `상관이 강할 때 어떻게 더 보수적으로 읽어야 하는가`까지는 현재 절 안에서 함께 잡아 둡니다.

| 항목 | 이 절에서의 처리 |
| --- | --- |
| PDP(partial dependence plot), SHAP | 이 절 후반에서 중요도와 무엇이 다른 질문을 던지는지까지는 직접 회수합니다. 다만 구현 옵션 전체를 길게 풀지는 않습니다. |
| 인과 추론(causal inference) 관점의 중요도 해석 | 이 절 후반에서 `모델 사용량`과 `원인 효과`를 왜 구분해야 하는지까지는 직접 회수합니다. 다만 식별 가정과 추정 절차 전체를 길게 풀지는 않습니다. |
| 상관 특성이 매우 강한 실제 대규모 데이터셋의 해석 전략 | 이 절 후반에서 해석 전략의 최소 순서까지는 직접 회수합니다. 다만 대규모 운영 파이프라인 전체를 길게 전개하지는 않습니다. |

이 절은 입문적으로 `숫자를 읽는 태도`를 세우는 데 초점을 둡니다.

## 이 절의 목표

- 특징 중요도를 `모델 내부 사용량의 요약`으로 설명할 수 있습니다.
- impurity-based importance(MDI)와 permutation importance를 구분할 수 있습니다.
- 특징 중요도가 곧 인과관계(causality)나 진짜 원인 순위를 뜻하지 않는다는 점을 설명할 수 있습니다.
- 상관 특성(multicollinear or correlated features)과 high-cardinality feature가 왜 해석을 왜곡할 수 있는지 말할 수 있습니다.

## 학습 배경

랜덤포레스트를 배우고 나면 독자는 이런 기대를 갖기 쉽습니다.

- 숲이 잘 맞춘다.
- 숲 안에는 많은 트리가 있다.
- 그러면 이 모델은 무엇이 중요한지도 잘 말해 줄 것 같다.

이 기대는 절반만 맞습니다.

| 기대 | 실제로는 |
| --- | --- |
| 중요도 숫자가 크면 원인이다 | 모델이 많이 썼다는 뜻에 더 가깝다 |
| 중요도 숫자가 낮으면 쓸모없는 특징이다 | 다른 특징과 겹치거나 대체되었을 수 있다 |
| 중요도는 항상 공정한 순위다 | 계산 방식에 따라 편향이 생길 수 있다 |

그래서 15.2는 `중요도 숫자를 믿는 법`이 아니라 `중요도 숫자를 과신하지 않는 법`을 배우는 절입니다.

여기서도 기록 구조를 같이 고정해 둡니다. 특징 중요도 절은 단순히 숫자를 정렬하는 절이 아니라, `어떤 중요도 관찰이 나왔는가`, `무엇은 아직 해석 경계 안에 있는가`, `다음 데이터 보강 질문은 무엇인가`를 남기는 절이기 때문입니다. 같은 중요도 순위처럼 보여도 어떤 특징 조합이 서로 역할을 대신하는지, 어떤 중요도 차이가 실제 성능 패턴 차이로 이어지는지는 따로 확인해야 합니다.

| 같이 남길 기록 | 왜 필요한가 |
| --- | --- |
| 관찰된 중요도 순위 | 모델이 어떤 특징을 더 많이 썼는지 보기 위해서입니다. |
| 해석 경계 문장 | 중요도 숫자를 원인 순위로 단정하지 않기 위해서입니다. |
| review 대상 특징 | 상관 특성이나 high-cardinality 열을 다시 보기 위해서입니다. |
| 다음 질문 | 어떤 특징을 더 수집하거나 어떤 비교 실험을 더 할지 정하기 위해서입니다. |

### 언제 중요도 숫자를 특히 조심해서 읽어야 하는가

특징 중요도는 편리하지만, 특정 데이터 구조에서는 해석을 쉽게 과신하게 만듭니다.

| 보이는 장면 | 먼저 조심할 이유 | 같이 확인할 것 |
| --- | --- | --- |
| 값 종류가 매우 많은 열이 상위에 뜬다 | high-cardinality 편향일 수 있기 때문 | permutation importance 비교 |
| 비슷한 뜻의 특징이 여러 개 있다 | 서로 정보를 대신해 importance가 갈라질 수 있기 때문 | 상관 특성 묶음 확인 |
| 중요도 차이가 작지만 순위는 갈린다 | 순위 차이를 진실 순위로 과장하기 쉽기 때문 | 실제 성능 변화와 함께 보기 |
| importance는 높지만 설명이 어색하다 | 모델 내부 사용과 현실 원인은 다를 수 있기 때문 | 도메인 의미와 사례 검토 |
| importance가 낮아 보이는 특징을 지우고 싶다 | 다른 특징과 함께 있을 때 역할을 했을 수 있기 때문 | 제거 전후 비교 실험 |

이 표의 목적은 중요도 숫자를 버리게 하는 것이 아니라, `언제 이 숫자가 특히 오해를 부르기 쉬운가`를 먼저 보게 하는 데 있습니다.

## 주요 학습내용

### 특징 중요도는 어떤 생각에서 나오나

scikit-learn 사용자 가이드는 트리에서 상위에 있는 decision node가 더 많은 샘플의 예측에 기여하고, split으로 impurity를 얼마나 줄였는지를 합쳐 상대적 중요도를 추정할 수 있다고 설명합니다. 이 아이디어를 여러 randomized tree에 대해 평균낸 것이 mean decrease in impurity, 즉 MDI입니다.

특징 중요도는 어떤 특징이 분기 개선에 얼마나 자주, 얼마나 크게 기여했는지를 요약한 값입니다.

`어떤 특징이 자주, 그리고 큰 분기 개선을 만들었다면 그 특징을 더 중요하게 본다.`

이 설명만 보면 매우 자연스러워 보입니다. 실제로도 빠르고 편리합니다. 하지만 여기에는 중요한 단서가 붙습니다.

`이 값은 모델이 학습 데이터 안에서 분기에 사용한 흔적을 요약한 것이다.`

중요도는 `모델 내부의 사용 기록`에 가깝지, 세상에서의 진짜 중요도나 원인의 크기를 바로 뜻하지는 않습니다.

### MDI(mean decrease in impurity)는 무엇인가

scikit-learn 문서는 tree ensemble의 특징 중요도를 impurity-based feature importance로 설명하고, 이를 여러 tree에 평균낸 것이 MDI라고 설명합니다.

MDI는 다음 순서로 계산됩니다.

1. 트리의 각 분기에서 impurity가 얼마나 줄었는지 본다.
2. 그 분기를 만든 feature에 그 감소량을 배정한다.
3. 트리 전체에서 합친다.
4. 숲 전체에서 평균낸다.
5. 1이 되도록 정규화(normalize)한다.

이를 짧게 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-2-mermaid-01-ko.mmd"
```

이 구조 덕분에 `feature_importances_`는 계산이 빠르고, 랜덤포레스트를 학습한 뒤 바로 볼 수 있다.

### 왜 상위 분기가 더 크게 작용하는가

scikit-learn 문서는 트리의 상위 분기에서 사용된 feature가 더 많은 입력 샘플의 최종 예측에 영향을 준다고 설명합니다. 그래서 같은 impurity 감소라도, 더 많은 샘플 흐름을 바꾼 분기가 중요도에 더 크게 반영될 수 있습니다.

이 감각을 짧게 바꾸면 다음과 같습니다.

`트리 초반의 질문은 더 많은 사람을 나누고, 뒤쪽의 질문은 더 적은 사람만 나눈다. 그래서 초반 분기 feature가 전체 중요도에서 더 크게 보일 수 있다.`

### `feature_importances_`는 어떻게 읽어야 하나

API 문서는 `feature_importances_`를 impurity-based feature importances라고 설명합니다. 값은 양수이고 합은 1.0입니다.

먼저는 다음처럼 읽습니다.

| 숫자 모습 | 뜻 |
| --- | --- |
| 값이 크다 | 모델이 그 feature를 상대적으로 더 많이 활용했다 |
| 값이 작다 | 모델이 그 feature를 상대적으로 덜 활용했다 |
| 합이 1이다 | 절대 점수보다 상대 비중으로 읽어야 한다 |

여기서 중요한 것은 `상대 비중`이라는 점입니다.

예를 들어 중요도가:

- `visits = 0.45`
- `late_payment = 0.35`
- `support_calls = 0.20`

라면, 모델 내부 분기 기준에서는 `visits`가 가장 큰 역할을 했다고 읽을 수 있습니다. 하지만 이것이 곧 `방문 수가 가장 강한 원인이다`라는 뜻은 아닙니다.

### permutation importance는 왜 따로 필요한가

scikit-learn 문서는 impurity-based feature importance의 대안으로 permutation importance를 제시합니다. permutation importance는 특정 feature 값을 무작위로 섞었을 때 성능이 얼마나 나빠지는지를 봅니다.

MDI가 `모델 내부 사용 기록`이라면, permutation importance는 `그 feature를 망가뜨렸을 때 실제 예측 성능이 얼마나 흔들리는가`에 더 가깝습니다.

두 방식을 비교하면 다음과 같습니다.

| 방식 | 핵심 질문 |
| --- | --- |
| MDI | 이 feature가 분기에서 얼마나 많이, 얼마나 크게 쓰였는가? |
| permutation importance | 이 feature를 섞어 버리면 모델 성능이 얼마나 떨어지는가? |

이 차이는 매우 중요합니다. 하나는 `모델 안에서의 사용 흔적`이고, 다른 하나는 `성능 의존도 검사`에 가깝기 때문입니다.

### permutation importance를 흐름으로 보기

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-2-mermaid-02-ko.mmd"
```

이 흐름은 매우 중요합니다. 왜냐하면 중요도를 `숫자 속성`이 아니라 `성능 변화 실험`으로 다시 읽게 하기 때문입니다.

## 세부 학습내용

### 왜 impurity-based importance는 조심해야 하나

scikit-learn 사용자 가이드는 impurity-based feature importances에 두 가지 주요 문제가 있다고 경고합니다.

1. 학습 데이터에서 계산된 통계에 의존하므로, hold-out 데이터에서 일반화 성능의 중요도를 반드시 반영하지는 않는다.
2. unique value가 많은 high-cardinality feature를 선호할 수 있다.

다음처럼 바꾸어 말할 수 있습니다.

`MDI는 빠르고 편하지만, 훈련 데이터 안에서 분기를 잘게 만들기 쉬운 feature를 과대평가할 수 있다.`

예를 들어 고객 ID처럼 값 종류가 매우 많은 열이 있다면, 실제로는 일반화에 도움이 적어도 훈련 데이터 안에서는 분기를 잘게 나누기 쉬워 중요도가 커 보일 수 있습니다.

### 상관 특성이 있으면 왜 헷갈리는가

scikit-learn 예제는 multicollinear or correlated features에서는 permutation importance가 기대와 다르게 보일 수 있음을 보여 줍니다. 서로 비슷한 정보를 가진 feature가 여러 개 있으면, 하나를 섞어도 다른 feature가 대신 역할을 할 수 있기 때문입니다.

이 상황에서는 다음 오해가 생깁니다.

- test accuracy는 높다
- 그런데 어떤 feature의 permutation importance는 낮다
- 그러면 그 feature는 중요하지 않은가?

항상 그렇지는 않습니다.

`중요하지 않다`가 아니라 `다른 correlated feature가 대신 정보를 제공하고 있다`일 수 있습니다.

따라서 중요도 해석은 feature 하나만 보는 일이 아니라, feature들 사이의 관계를 함께 읽는 일입니다.

이 장면을 아주 작은 표로 다시 쓰면 다음과 같습니다.

| feature | 실제 뜻 |
| --- | --- |
| `monthly_spend` | 최근 한 달 소비 금액 |
| `yearly_spend_div_12` | 최근 1년 소비 금액을 12로 나눈 값 |

이 둘은 거의 같은 방향의 정보를 담을 수 있습니다. 이때 모델은 둘 중 하나를 더 자주 쓰고, 다른 하나는 덜 쓸 수 있습니다. 하지만 덜 쓰인 쪽이 완전히 쓸모없다는 뜻은 아닙니다. `둘이 비슷한 정보를 나눠 들고 있어서 importance가 갈라졌을 가능성`을 먼저 떠올려야 합니다.

같은 장면은 permutation importance에서도 헷갈릴 수 있습니다. `monthly_spend`를 섞어도 `yearly_spend_div_12`가 남아 있으면 성능 하락이 생각보다 작을 수 있기 때문입니다. 그러면 permutation importance까지 낮게 나와 `둘 다 별로 안 중요한가?`라는 오해가 생길 수 있습니다. 하지만 실제로는 `둘 중 어느 하나가 남아 있기 때문에 모델이 덜 무너진 것`일 수 있습니다.

즉, 상관 특성이 강할 때는 `숫자가 낮다 -> 중요하지 않다`가 아니라 `숫자가 낮아 보여도 다른 feature가 대신 설명하고 있는가`를 먼저 점검해야 합니다.

## PDP와 SHAP는 중요도와 무엇이 다른가

특징 중요도는 `모델이 무엇을 많이 썼는가`를 요약합니다. 하지만 독자는 곧 다음 질문도 하게 됩니다.

- 그 특징 값이 커지면 예측은 어느 방향으로 움직이는가?
- 개별 샘플에서는 어떤 특징이 예측을 밀어 올렸는가?

바로 여기서 PDP(partial dependence plot)와 SHAP가 같이 언급됩니다.

| 도구 | 먼저 답하려는 질문 |
| --- | --- |
| feature importance | 모델이 무엇을 많이 썼는가 |
| PDP | 한 특징 값을 바꾸면 예측이 평균적으로 어떻게 움직이는가 |
| SHAP | 이 샘플의 예측에 각 특징이 어떻게 기여했는가 |

즉, 중요도는 `사용량 요약`, PDP는 `평균적 방향`, SHAP는 `개별 예측 기여 분해`에 더 가깝습니다.

이 차이를 짧게 읽으면 다음과 같습니다.

| 지금 보고 싶은 것 | 더 먼저 떠올릴 도구 |
| --- | --- |
| 전체 모델이 무엇을 많이 쓰는가 | feature importance |
| 특정 특징이 커질수록 예측이 오르는가 내려가는가 | PDP |
| 이 사례 한 건에서 무엇이 예측을 밀어 올렸는가 | SHAP |

따라서 중요도 숫자만으로 `어느 방향으로 영향을 주는가`까지 말하려 하면 정보가 부족합니다. 예를 들어 importance는 높지만, 값이 커질수록 예측이 올라가는지 내려가는지는 importance 하나만으로는 알 수 없습니다. 이 방향성 질문은 PDP 같은 도구가 더 직접 답합니다.

마찬가지로 importance가 높다고 해도, 개별 샘플 A와 B에서 같은 특징이 같은 방식으로 작동한다고 단정할 수는 없습니다. 그 개별 기여를 더 잘 보려는 질문에서 SHAP가 등장합니다.

즉, PDP와 SHAP는 중요도를 대체하는 이름이 아니라, `중요도 숫자만으로는 닫히지 않는 다른 해석 질문`을 붙잡는 도구들로 읽는 편이 맞습니다.

## 중요도와 인과 추론은 왜 다른가

중요도 숫자를 보다 보면 독자는 쉽게 다음 문장으로 점프합니다.

`이 특징이 중요하니, 이것이 결과의 원인이다.`

하지만 이 점프는 안전하지 않습니다.

| 중요도 해석이 말해 주는 것 | 인과 해석이 묻는 것 |
| --- | --- |
| 모델이 어떤 특징을 예측에 많이 활용했는가 | 그 특징을 실제로 바꾸면 결과가 달라지는가 |
| 데이터 안의 통계적 관계 | 개입(intervention)과 원인 효과 |

예를 들어 `recent_visits` 중요도가 높게 나왔다고 해 봅시다. 이것은 모델이 예측할 때 최근 방문 수를 많이 사용했다는 뜻입니다. 하지만 그것만으로 `방문 수를 늘리면 반응률이 반드시 올라간다`고 말할 수는 없습니다. 실제로는:

- 방문 수가 원인일 수도 있고
- 이미 관심이 높은 고객이라 방문 수와 반응률이 같이 높았을 수도 있으며
- 다른 숨은 요인이 둘을 함께 움직였을 수도 있습니다

즉, 중요도는 예측 모델 안의 설명 도구이고, 인과 추론은 `무엇을 바꾸면 결과가 바뀌는가`를 더 엄격하게 묻는 다른 층위의 문제입니다.

이 절에서 독자가 꼭 남겨야 할 경계는 다음과 같습니다.

| 숫자를 본 뒤 바로 쓰기 쉬운 문장 | 더 안전한 문장 |
| --- | --- |
| `이 feature가 원인이다` | `이 모델은 이 feature를 예측에 많이 사용했다` |
| `이 feature를 바꾸면 결과가 바뀐다` | `결과를 바꾸는지는 별도의 인과 검토가 필요하다` |

따라서 중요도 해석은 `원인 가설 후보`를 만드는 데는 도움이 될 수 있어도, 그 자체가 원인 증명은 아닙니다.

## 상관 특성이 매우 강한 실제 데이터에서는 어떻게 읽는가

실제 대규모 데이터셋에서는 비슷한 뜻의 특징이 몇 개가 아니라 수십 개씩 함께 들어 있는 경우가 많습니다. 이때는 `한 열의 importance`만 보며 결론을 내리면 거의 항상 과신으로 이어지기 쉽습니다.

보수적 해석 전략은 다음 순서로 잡는 편이 좋습니다.

| 순서 | 먼저 할 일 | 이유 |
| --- | --- | --- |
| 1 | 비슷한 뜻의 특징을 묶음으로 본다 | importance가 여러 열에 갈라질 수 있기 때문입니다. |
| 2 | MDI와 permutation importance를 같이 본다 | 내부 사용량과 성능 의존도를 분리해서 보기 위해서입니다. |
| 3 | 제거 전후 비교 실험을 한다 | 정말 대체 가능한지 확인하기 위해서입니다. |
| 4 | 개별 열보다 특징 묶음 수준으로 메모를 남긴다 | 대규모 데이터에서는 역할이 한 열에 고정되지 않기 때문입니다. |

예를 들어 다음처럼 읽는 편이 더 안전합니다.

| 위험한 읽기 | 더 안전한 읽기 |
| --- | --- |
| `열 A 중요도가 낮으니 지운다` | `열 A는 같은 묶음의 다른 특징이 대신 설명하는지 먼저 본다` |
| `열 B가 1등이니 가장 중요한 비즈니스 원인이다` | `열 B가 속한 특징 묶음이 모델에서 크게 사용되었다` |
| `permutation drop이 작으니 필요 없다` | `대체 특징이 남아 있어 drop이 작을 수 있다` |

즉, 상관 특성이 매우 강한 데이터에서는 `개별 열 순위표`보다 `비슷한 특징 묶음`, `제거 전후 비교`, `중요도 방식 간 대조`가 더 중요합니다. 이 절의 목표도 바로 거기에 있습니다. 숫자 하나를 더 세게 믿는 것이 아니라, 숫자를 더 보수적으로 읽는 기준을 남기는 일입니다.

### 중요도 숫자를 보고 바로 무엇을 해야 하나

중요도 해석에서 초심자가 가장 자주 막히는 지점은 여기입니다. `그래서 숫자를 봤는데, 다음 행동은 무엇인가?`

이 절에서는 다음 다섯 줄을 최소 순서로 붙잡으면 됩니다.

| 순서 | 먼저 할 질문 | 왜 필요한가 |
| --- | --- | --- |
| 1 | 상위 feature가 무엇인가? | 모델이 어디를 주로 봤는지 확인하기 위해서입니다. |
| 2 | 이 값이 MDI인가, permutation인가? | 같은 importance라도 뜻이 다르기 때문입니다. |
| 3 | high-cardinality 열이나 상관 특성이 있는가? | 숫자 왜곡 가능성을 먼저 점검해야 하기 때문입니다. |
| 4 | 숫자 해석이 도메인 의미와 맞는가? | 모델 내부 사용과 현실 설명이 다를 수 있기 때문입니다. |
| 5 | 삭제나 정책 변경 전 비교 실험이 있는가? | importance만 보고 바로 결론 내리면 위험하기 때문입니다. |

이 순서의 목적은 일을 복잡하게 만드는 것이 아닙니다. 특징 중요도를 `점수표`가 아니라 `점검표`로 다시 읽게 만드는 데 있습니다.

### 중요도가 높거나 낮을 때 바로 내리기 쉬운 잘못된 결론

importance 숫자는 크고 작음이 분명해서, 독자가 곧바로 행동 결론까지 점프하기 쉽습니다. 하지만 안전한 해석은 다음처럼 한 단계를 더 거칩니다.

| 지금 보인 숫자 | 바로 떠오르기 쉬운 결론 | 더 안전한 해석 |
| --- | --- | --- |
| importance가 높다 | 가장 중요한 원인이다 | 모델이 이 feature를 많이 사용했다 |
| importance가 낮다 | 지워도 된다 | 다른 feature에 가려졌을 수 있다 |
| permutation drop이 작다 | 성능에 필요 없다 | 대체 feature가 남아 있을 수 있다 |
| MDI가 매우 크다 | 이 feature 하나면 충분하다 | 훈련 데이터 분기 편향 가능성을 봐야 한다 |

이 표를 익혀 두면 중요도 숫자를 본 뒤의 첫 반응이 조금 더 느려집니다. 그 느려짐이 바로 해석 품질을 지키는 장치입니다.

## 사례 및 예시

### 사례 1. 중요도 숫자가 높다고 바로 원인이라고 말하면 왜 위험할까

마케팅 팀이 랜덤포레스트로 고객 반응을 예측한 뒤, 어떤 특징이 중요했는지 보고 싶어 합니다. 사람이 먼저 보던 기준은 `최근 방문 수`, `할인 메시지 반응`, `구매 금액`, `회원 등급` 같은 신호였습니다.

모델을 학습하고 `feature_importances_`를 보니 `recent_visits`와 `discount_clicks`가 높게 나옵니다. 이때 팀은 곧바로 `방문 수가 가장 큰 원인이다`라고 말하고 싶어질 수 있습니다. 하지만 그 숫자는 먼저 `모델이 분기에서 얼마나 많이 활용했는가`의 요약이지, 현실 세계의 인과 순위를 바로 보여 주는 값은 아닙니다.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-2-mermaid-03-ko.mmd"
```

이 장면에서 특징 중요도는 `설명 출발점`으로 읽습니다. MDI는 모델 내부 사용 흔적을 요약하고, permutation importance는 그 특징을 섞었을 때 실제 성능이 얼마나 흔들리는지를 봅니다. 또 비슷한 뜻의 특징이 여러 개 있으면 하나는 높고 다른 하나는 낮게 보여도, 실제로는 정보를 서로 대신하고 있을 수 있습니다.

확인 가능한 결과는 MDI와 permutation importance를 나란히 보고, high-cardinality 열이나 상관된 특징이 있는지 함께 검토할 때 드러납니다. 중요도 숫자 하나만 보고 정책을 바꾸기보다, 어떤 열이 모델 내부에서 많이 쓰였고 어떤 열이 성능을 실제로 흔드는지 분리해서 읽어야 합니다.

### 사례 2. 중요도는 낮아 보이는데 왜 바로 지우면 안 될까

구독 해지 예측 모델을 만든 팀이 있다고 하겠습니다. feature에는 `monthly_spend`, `yearly_spend_div_12`, `recent_visits`, `late_payment_count`가 함께 들어 있습니다. importance를 보니 `monthly_spend`는 중간 이상인데 `yearly_spend_div_12`는 거의 바닥에 가깝습니다.

이때 사람이 먼저 내리기 쉬운 판단은 `yearly_spend_div_12는 필요 없네. 지우자.`입니다. 하지만 이 둘이 거의 같은 뜻의 정보를 담고 있다면, 낮은 importance는 `쓸모없음`보다 `다른 feature가 이미 비슷한 설명을 대신함`에 더 가까울 수 있습니다.

이 장면에서 중요한 것은 `importance 숫자`보다 `지우기 전후 비교`입니다. 낮게 나온 feature를 지운 뒤 성능과 해석이 어떻게 달라지는지 같이 봐야 합니다. 성능 변화가 거의 없으면 정말 중복이 심한 것일 수 있고, 반대로 특정 사례 설명이 무너지거나 permutation 결과가 달라지면 그 feature가 보조 역할을 하고 있었을 수 있습니다.

즉, 중요도가 낮다고 해서 곧바로 `버릴 feature`로 읽기보다, 먼저 `정보가 겹친 것인가`, `특정 사례에서만 역할을 했는가`, `제거 전후 결과가 어떻게 달라지는가`를 묻는 편이 더 안전합니다.

### 실무에서 어떻게 읽으면 좋은가

특징 중요도는 다음처럼 쓰는 편이 보수적입니다.

| 좋은 사용법 | 위험한 사용법 |
| --- | --- |
| 모델이 주로 어떤 신호를 보는지 점검 | 중요도 순위를 원인 순위로 단정 |
| 이상한 열이 상위에 올라왔는지 확인 | 숫자가 낮은 feature를 즉시 삭제 |
| permutation 결과와 함께 교차 확인 | 훈련 데이터 기반 MDI 하나만 보고 결론 |
| 상관 관계와 데이터 의미를 함께 검토 | 숫자만 보고 정책 변경 |

결국 중요도는 `설명 도구의 시작점`이지 `최종 판결문`이 아닙니다.

프로젝트 메모 형식으로 줄이면 다음처럼 적을 수 있습니다.

| 기록 항목 | 예 |
| --- | --- |
| observed importance | `petal length = 0.444` |
| safe interpretation | `이 모델이 이 특징을 자주 활용했다` |
| review_needed | `상관된 특징이 있어 과신 금지` |
| next_question | `permutation importance도 함께 볼 것인가` |

이 표가 있으면 특징 중요도 절이 `관찰된 중요도 -> 해석 경계 -> 다음 질문` 구조로 읽힙니다. 결국 중요한 것은 숫자 순서 자체보다 `이 중요도 관찰이 어떤 실패 패턴 설명에는 도움이 되고, 어디부터는 아직 과신하면 안 되는가`를 함께 적는 일입니다.

### importance를 본 뒤 남기는 최소 해석 메모

실무에서는 중요도 표만 저장하고 끝내기 쉽습니다. 하지만 그 상태로는 나중에 다시 봤을 때 `왜 이 숫자를 믿었는가`, `어디서 멈췄는가`가 남지 않습니다.

최소한 다음 네 줄은 같이 적는 편이 좋습니다.

| 항목 | 적는 예 |
| --- | --- |
| observed importance | `recent_visits가 가장 높게 나왔다` |
| interpretation boundary | `이 값은 모델 사용 흔적이지 원인 순위는 아니다` |
| review target | `discount_clicks와 recent_visits의 상관 관계 확인 필요` |
| next action | `permutation importance와 제거 전후 비교 실험 추가` |

이 메모가 있으면 중요도 절이 단순 설명에서 끝나지 않고, 다음 실험으로 이어지는 학습 기록이 됩니다.

## 연습 및 예제

### Python 예제로 MDI 보기

이번 예제는 랜덤포레스트를 학습한 뒤 `feature_importances_`를 직접 읽어 보는 가장 작은 실습입니다.

- 문제 상황: iris 데이터에서 어떤 특징이 더 중요하게 쓰였는지 본다.
- 입력(input): iris의 4개 feature
- 정답(label): 품종 class
- 확인할 개념:
  - 중요도는 상대 비중이다
  - 값의 합은 1에 가깝다

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

iris = load_iris()
X, y = iris.data, iris.target
feature_names = iris.feature_names

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

print("test accuracy:", round(model.score(X_test, y_test), 3))
print("feature importances:")

for name, score in zip(feature_names, model.feature_importances_):
    print(f"  {name:20} {score:.3f}")

print("sum:", round(model.feature_importances_.sum(), 3))
```

실행 결과 예시는 다음과 같습니다.

```text
test accuracy: 0.911
feature importances:
  sepal length (cm)    0.098
  sepal width (cm)     0.028
  petal length (cm)    0.444
  petal width (cm)     0.430
sum: 1.0
```

이 예제에서 읽어야 할 것은:

1. 중요도는 상대 비중으로 나온다.
2. petal length와 petal width가 이 모델에서 더 많이 쓰였다.
3. 이것은 `이 모델의 분기 사용 흔적`이지, 곧바로 인과 설명은 아니다.

### Python 예제로 permutation importance와 나란히 보기

이번에는 같은 모델에 대해 permutation importance를 같이 봅니다.

문제 상황:

- 특징 중요도는 하나의 숫자만 보면 고정된 사실처럼 보이지만 계산 방식이 달라지면 결과도 달라질 수 있다

입력(input):

- iris 데이터셋
- 학습된 랜덤포레스트 모델

기대 출력(output):

- MDI 기반 중요도
- permutation importance 결과

확인할 개념:

- MDI와 permutation importance는 같은 값을 내놓지 않는다
- 두 숫자가 다르면 계산 방식이 다른 것임을 먼저 떠올려야 한다

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance

iris = load_iris()
X, y = iris.data, iris.target
feature_names = iris.feature_names

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

baseline_accuracy = model.score(X_test, y_test)

perm = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=20,
    random_state=42
)

print("baseline accuracy:", round(baseline_accuracy, 3))
print("feature".ljust(20), "MDI".rjust(8), "perm_mean".rjust(12))
for i, name in enumerate(feature_names):
    mdi = model.feature_importances_[i]
    pmean = perm.importances_mean[i]
    print(f"{name:20} {mdi:8.3f} {pmean:12.3f}")
```

실행 결과 예시는 다음과 같습니다.

```text
baseline accuracy: 0.911
feature                   MDI    perm_mean
sepal length (cm)       0.098        0.011
sepal width (cm)        0.028        0.000
petal length (cm)       0.444        0.222
petal width (cm)        0.430        0.189
```

이 결과가 뜻하는 바는 다음과 같습니다.

- 두 방식은 순위가 비슷할 수도 있고 다를 수도 있습니다.
- 같은 feature라도 `분기에서 많이 쓰였는가`와 `섞었을 때 성능이 얼마나 떨어지는가`는 다른 질문입니다.
- 따라서 하나의 중요도 숫자만 보고 해석을 끝내면 위험합니다.

### 직접 판단해 보기

아래 관찰을 보고, 어느 해석이 더 안전한지 먼저 스스로 골라 봅니다.

| 관찰 | 성급한 결론 | 더 안전한 해석 |
| --- | --- | --- |
| `petal length`의 MDI가 가장 크다 | 가장 강한 원인이다 | 이 모델이 분기에서 가장 많이 활용한 특징이다 |
| `sepal width`의 permutation 값이 0에 가깝다 | 완전히 쓸모없는 특징이다 | 다른 특징이 비슷한 정보를 대신하고 있는지 더 봐야 한다 |
| MDI와 permutation 값이 다르다 | 둘 중 하나가 틀렸다 | 두 값이 서로 다른 질문에 답하고 있다 |

이 표의 목적은 정답 맞히기가 아닙니다. 중요도 숫자를 본 뒤 `바로 결론`으로 뛰지 않고, `이 숫자가 어떤 질문의 답인가`를 한 번 더 확인하는 습관을 만드는 데 있습니다.

### high-cardinality feature를 조심해야 하는 이유

트리 계열은 unique value가 많은 feature에 쉽게 반응할 수 있습니다. 이런 feature는 훈련 데이터 안에서 분기를 더 세밀하게 만들 기회를 많이 주기 때문입니다.

예를 들어:

- 고객 ID
- 주문 번호
- 타임스탬프 원본

같은 열은 실제 업무 의미보다 `분기 후보가 너무 많다`는 이유로 중요해 보일 수 있습니다.

따라서 중요도를 볼 때는 항상 묻습니다.

`이 열은 정말 의미 있는 변수인가, 아니면 그냥 값을 잘게 나누기 쉬운 열인가?`

### 상관 특성(correlated features)을 조심해야 하는 이유

예를 들어 `monthly_spend`와 `yearly_spend / 12`처럼 거의 같은 뜻의 열이 둘 다 들어 있다면, 모델은 둘 중 하나를 주로 쓰고 다른 하나는 덜 쓸 수 있습니다.

그 결과:

- 한쪽 중요도는 높고
- 다른 쪽 중요도는 낮게

보일 수 있습니다.

하지만 이것이 낮은 쪽이 쓸모없다는 뜻은 아닙니다. 단지 정보가 겹쳐서 대체되었을 수 있습니다.

이 때문에 중요도 해석은 늘 다음 질문과 함께 가야 합니다.

- 비슷한 뜻의 feature가 여러 개 있는가?
- 숫자가 큰 feature가 정말 독립적으로 중요한가?
- 숫자가 낮은 feature가 다른 feature에 가려진 것은 아닌가?

## 이 절에서 기억할 관점

- 특징 중요도는 모델이 무엇을 봤는지 요약하는 도구입니다.
- MDI는 분기 사용과 impurity 감소를 평균낸 내부 요약입니다.
- permutation importance는 feature를 섞었을 때 성능이 얼마나 떨어지는지 보는 외부 점검입니다.
- 중요도 숫자는 곧바로 인과관계나 원인 순위를 뜻하지 않습니다.
- high-cardinality feature와 correlated feature는 해석을 왜곡할 수 있습니다.

## 체크리스트

- importance를 원인 순위처럼 읽고 있지 않은가?
- MDI와 permutation importance가 서로 다른 질문에 답한다는 점을 구분하고 있는가?
- 상관 특성이나 high-cardinality 열이 있는지 먼저 점검하고 있는가?

## 언제 이 관점을 먼저 떠올려야 하는가

- 중요도 숫자 하나만 보고 원인 순위를 말하고 싶어질 때, importance는 설명 출발점이라는 관점을 먼저 떠올립니다.
- MDI와 permutation importance 결과가 다를 때, 두 값이 서로 다른 질문에 답한다는 점을 다시 확인합니다.
- high-cardinality 열이나 상관 특성이 섞여 있을 때, 중요도 해석이 쉽게 왜곡될 수 있다는 경계를 먼저 꺼냅니다.

## 출처와 참고 자료

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, 확인 날짜: 2026-06-27. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `RandomForestClassifier`, scikit-learn API Reference, 확인 날짜: 2026-06-27. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Permutation feature importance`, scikit-learn User Guide, 확인 날짜: 2026-06-27. [https://scikit-learn.org/stable/modules/permutation_importance.html](https://scikit-learn.org/stable/modules/permutation_importance.html){: target="_blank" rel="noopener noreferrer" }
- Gilles Louppe, *Understanding Random Forests: From Theory to Practice*, PhD Thesis, University of Liege, 2014. [https://arxiv.org/abs/1407.7502](https://arxiv.org/abs/1407.7502){: target="_blank" rel="noopener noreferrer" }
