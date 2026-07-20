# P4-13.1 SVM의 직관

> Section ID: `P4-13.1`
> Version: `v2026.07.19`

P4-11.2에서는 분류를 `경계(boundary)를 그어 공간을 나누는 일`로 보았습니다. P4-12에서는 `가까운 이웃을 보고 판단하는 방식`도 살펴보았습니다. 이제 같은 분류 문제를 다른 질문으로 다시 읽습니다.

경계를 그을 수 있다면, 그중 어떤 경계가 더 좋은 경계인가?

이 질문이 SVM(support vector machine)의 출발점입니다.

SVM은 class를 나누는 선을 찾되, 그 선이 양쪽 데이터로부터 가능한 한 여유 있게 떨어지도록 하려는 모델이다.

SVM은 단지 `분류선 하나`를 찾는 데서 멈추지 않고, `가장 안정적으로 보이는 분리선`을 찾으려는 시도입니다.

이 절은 `SVM(support vector machine)`, `margin`, `support vector`의 기본 뜻을 설명합니다. 뒤 절에서는 이 손잡이를 바탕으로 현재 맥락의 판단을 이어 가고, 경계의 안정성을 읽는 기본 감각은 이 절과 [개념사전](../../../reference/concept-glossary.md)을 기준으로 다시 연결합니다.

## 이 절의 범위

이 절은 `좋은 경계란 무엇인가`라는 질문을 SVM의 손잡이로 처음 붙잡는 절입니다. 여기서는 margin, support vector, soft margin 직관을 중심으로 `분리 가능`보다 `더 안정적으로 나누는 기준`을 먼저 읽습니다.

이 절은 다음 질문에 답합니다.

- SVM은 왜 단순한 경계선보다 `margin`을 더 중요하게 보는가?
- margin은 무엇이며, 왜 분류 안정성과 연결되는가?
- support vector는 무엇이고 왜 이름의 중심에 있는가?
- 데이터가 완벽히 나뉘지 않을 때는 어떤 생각이 추가되는가?
- SVM은 앞의 로지스틱 회귀, k-NN과 어떤 점이 다른가?

커널(kernel) 발상과 비선형 경계의 큰 그림은 P4-13.2에서 바로 이어서 다루고, `C`, `gamma` 같은 하이퍼파라미터를 읽는 기준과 검증 비용은 P4-9.1, P4-9.2에서 다시 연결합니다. 즉, 이번 절은 `좋은 경계란 무엇인가`를 margin과 support vector 관점으로 먼저 붙잡는 자리입니다.

## 이 절의 목표

- SVM을 `margin을 최대화하는 분류기`라는 직관으로 설명할 수 있습니다.
- 같은 데이터를 나누는 여러 경계 중에서 왜 어떤 경계가 더 낫다고 말할 수 있는지 설명할 수 있습니다.
- support vector가 `경계에서 가장 가까운 핵심 점들`이라는 점을 설명할 수 있습니다.
- 완벽한 분리가 어려울 때 margin과 오류 허용이 함께 등장한다는 점을 입문 수준에서 이해할 수 있습니다.
- 11장의 결정 경계, 12장의 거리와 스케일 논의가 왜 SVM으로 이어지는지 설명할 수 있습니다.

## 학습 배경

P4-11의 로지스틱 회귀는 `입력 공간을 나누는 경계`를 보여 주었습니다. 하지만 그 절만으로는 이런 질문이 남습니다.

- 나누기만 하면 충분한가?
- 경계가 class에 너무 바짝 붙어 있어도 괜찮은가?
- 경계 주변의 작은 흔들림에도 예측이 쉽게 바뀌면 어떻게 되는가?

SVM은 이 질문에 답하는 첫 번째 대표 사례입니다.

이 절은 `분류선` 자체보다 `좋은 분류선의 기준`을 배우는 데 더 가깝습니다.

## 주요 학습내용

### 왜 margin을 따로 보아야 하는가

두 class를 분리할 수 있는 직선은 하나만 있는 것이 아닐 수 있습니다. 같은 데이터를 놓고도 여러 개의 선이 그려질 수 있습니다.

문제는 이런 선들이 모두 똑같이 좋아 보이지 않는다는 점입니다.

- 어떤 선은 한쪽 점에 너무 바짝 붙어 있습니다.
- 어떤 선은 양쪽 점과 조금 더 떨어져 있습니다.
- 어떤 선은 작은 노이즈(noise)만 들어와도 class가 뒤집힐 것처럼 보입니다.

SVM은 바로 이 차이를 `margin`이라는 말로 잡습니다.

`margin은 경계선과 가장 가까운 데이터들 사이의 여유 폭이다.`

이 여유 폭이 크면, 경계가 데이터 사이에 더 안정적으로 놓여 있다고 읽을 수 있습니다.

다시 말해 SVM은 `선을 그릴 수 있는가`를 넘어서 `여러 경계 후보 중 어떤 경계가 더 안정적인가`를 묻습니다. 핵심은 분리 가능 여부가 아니라, 가장 가까운 점들과의 최소 간격을 기준으로 더 여유 있는 경계를 고른다는 데 있습니다.

같은 생각을 판단 순서로 다시 압축하면 다음과 같습니다.

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-01-ko.mmd"
```

이 도식의 핵심은 `margin을 따로 보는 일`이 부가 장식이 아니라는 점입니다. 먼저 같은 데이터를 나눌 수 있는 여러 경계를 후보로 두고, 그다음 각 경계에서 가장 가까운 점들을 비교해야 비로소 작은 흔들림에 취약한 경계와 여유를 남긴 경계를 구분할 수 있습니다. 경계가 한쪽 class에 너무 가까우면 새 사례가 조금만 움직여도 near-boundary review가 빠르게 늘고, 양쪽에 여유를 둔 경계는 같은 변화에도 즉시 뒤집힐 가능성이 상대적으로 줄어듭니다.

### 큰 margin은 왜 좋은가

큰 margin이 언제나 절대 정답이라고 말할 수는 없습니다. 하지만 교육적으로는 다음 이유 때문에 매우 중요한 기준이 됩니다.

1. 경계가 양쪽 class에 너무 붙지 않습니다.
2. 경계 근처의 작은 흔들림에 덜 민감해 보입니다.
3. 처음 보는 데이터에서도 조금 더 안정적인 일반화(generalization)를 기대할 수 있다는 직관을 줍니다.

이 세 번째 이유 때문에 SVM은 통계학습이론(statistical learning theory)과 자주 함께 언급됩니다. 이 책의 앞절에서 보았듯, 일반화는 `훈련 데이터를 잘 외우는 것`이 아니라 `새 데이터에도 타당한 판단을 유지하는 것`에 더 가깝습니다. SVM은 그 일반화 문제를 `margin`이라는 기하학적 언어로 읽게 해 줍니다.

`SVM은 경계를 맞히는 문제를, 여유 있는 경계를 찾는 문제로 다시 바꿔 읽는다.`

프로젝트 메모 형식으로 줄이면 다음처럼 적을 수 있습니다.

| 기록 항목 | 예 |
| --- | --- |
| 현재 후보 경계 | `linear SVM` |
| margin 근처 사례 | `거래 A`, `거래 B` |
| review 필요 여부 | `경계에 너무 가까워 검토` |
| 다음 질문 | `soft margin으로 완화하면 같은 사례가 유지되는가` |

이 표가 있으면 SVM 소개가 수식보다 `비교 후보 -> review 사례 -> 다음 질문` 구조로 먼저 읽힙니다. 같은 정확도나 비슷한 평균 점수가 보여도, 어떤 후보가 더 넓은 여유를 남기고 어떤 후보가 경계 근처 사례를 더 많이 남기는지는 따로 확인해야 합니다.

### support vector는 무엇인가

SVM이라는 이름에는 `support vector`가 들어 있습니다. 이 말이 중요한 이유는, 모든 점이 똑같은 정도로 경계를 결정하지 않기 때문입니다.

SVM의 직관에서 가장 중요한 점들은 보통 `경계에 가장 가까운 점들`입니다. 이 점들이 경계의 위치를 사실상 떠받치고 있다고 읽을 수 있습니다. 그래서 support vector라는 이름이 붙습니다.

- 멀리 떨어진 점들은 경계 결정에 덜 민감합니다.
- 경계에 가장 바짝 붙은 점들이 경계 위치를 더 강하게 좌우합니다.
- 그래서 SVM은 전체 데이터 중에서도 `가장 빡빡한 점들`을 특히 중요하게 봅니다.

간단히 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-02-ko.mmd"
```

이 도식은 support vector가 왜 특별한지 보여 줍니다. 전체 학습 점이 모두 같은 무게로 경계를 정하는 것이 아니라, 경계에서 멀리 떨어진 점들은 경계를 덜 흔들고, 가장 가까운 일부 점들이 실제로는 분리선 위치를 더 강하게 떠받친다는 뜻입니다.

실무적으로는 support vector를 다음처럼 읽을 수도 있습니다.

- 모든 고객 기록이 같은 중요도를 갖는 것은 아닙니다.
- 모든 시험 답안이 같은 정도로 경계 기준을 흔드는 것도 아닙니다.
- 실제로는 `애매한 경계 근처 사례`가 모델 기준을 더 많이 바꿉니다.

이 감각은 뒤의 모델 해석과 오류 분석에도 중요합니다. 어떤 모델이든 `경계에서 애매한 사례`를 확인하는 습관이 생기면, 단순 정확도 숫자보다 더 많은 것을 읽을 수 있습니다.

### Python 예제로 `어떤 경계가 더 큰 margin을 가지는가` 보기

이번 예제는 SVM 학습기를 직접 구현하는 것이 아닙니다. 대신 같은 두 class를 나누는 여러 `세로 경계 후보`를 두고, 어느 경계가 더 큰 margin을 가지는지 직접 계산해 봅니다.

- 문제 상황: 두 class가 x축의 왼쪽과 오른쪽에 나뉘어 있다.
- 입력(input): 2차원 점
- 정답(label): negative / positive
- 확인할 개념:
  - 경계를 만들 수 있는 후보는 여러 개일 수 있다.
  - SVM의 관심은 그중 `가장 작은 여유 폭(minimum gap)`이 큰 경계를 찾는 데 있다.
  - 경계에서 가장 가까운 점들이 support vector처럼 읽힌다.

```python
# SVM에서 여러 경계 후보의 margin과 support vector처럼 작동하는 가까운 점을 비교하는 예제입니다.
negative = [(1.0, 2.0), (2.0, 3.0), (3.0, 2.5)]
positive = [(5.0, 2.2), (6.0, 3.2), (7.0, 2.8)]

candidates = [3.4, 4.0, 4.6]

for boundary_x in candidates:
    neg_min = min(boundary_x - x for x, _ in negative)
    pos_min = min(x - boundary_x for x, _ in positive)
    margin = min(neg_min, pos_min)

    support_neg = [p for p in negative if abs((boundary_x - p[0]) - neg_min) < 1e-9]
    support_pos = [p for p in positive if abs((p[0] - boundary_x) - pos_min) < 1e-9]

    print("boundary x =", boundary_x)
    print("  negative-side nearest distance =", round(neg_min, 3))
    print("  positive-side nearest distance =", round(pos_min, 3))
    print("  margin =", round(margin, 3))
    print("  support-like points =", support_neg + support_pos)
    print()
```

실행 결과 예시는 다음과 같습니다.

```text
boundary x = 3.4
  negative-side nearest distance = 0.4
  positive-side nearest distance = 1.6
  margin = 0.4
  support-like points = [(3.0, 2.5), (5.0, 2.2)]

boundary x = 4.0
  negative-side nearest distance = 1.0
  positive-side nearest distance = 1.0
  margin = 1.0
  support-like points = [(3.0, 2.5), (5.0, 2.2)]

boundary x = 4.6
  negative-side nearest distance = 1.6
  positive-side nearest distance = 0.4
  margin = 0.4
  support-like points = [(3.0, 2.5), (5.0, 2.2)]
```

이 출력에서 읽어야 할 핵심은 다음입니다.

- 세 경계 모두 두 class를 나누기는 합니다.
- 하지만 `x = 4.0`일 때 가장 작은 여유 폭이 가장 큽니다.
- 경계에 가장 가까운 `(3.0, 2.5)`와 `(5.0, 2.2)`가 support vector처럼 작동합니다.

SVM은 `나눌 수 있는가`에서 멈추지 않고 `얼마나 여유 있게 나누는가`를 추가로 묻습니다.

## 세부 학습내용

### 데이터가 완벽히 나뉘지 않으면 어떻게 되는가

현실 데이터는 항상 이렇게 깔끔하지 않습니다. 어떤 점은 반대 class 쪽 가까이에 섞여 들어올 수 있습니다. 그러면 완벽한 분리선(perfect separating line)을 만들기 어렵습니다.

이때 SVM 직관은 이렇게 바뀝니다.

- 모든 점을 완벽하게 분리하는 것만 고집하지 않는다.
- 일부 오류나 침범을 허용하더라도,
- 전체적으로 더 타당한 margin을 찾으려 한다.

이 생각이 뒤에서 `soft margin`과 하이퍼파라미터 `C`로 이어집니다. 지금 절에서는 다음 문장을 기준으로 잡으면 됩니다.

`현실의 SVM은 완벽한 분리만이 아니라, 여유와 오류 허용 사이의 균형도 함께 다룬다.`

이를 개념적으로 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-03-ko.mmd"
```

### SVM은 어떤 문제를 다루는가

SVM은 scikit-learn 공식 문서에서도 분류(classification), 회귀(regression), 이상치 탐지(outlier detection)에 쓰이는 지도학습(supervised learning) 방법군으로 소개됩니다. 하지만 이 절에서는 먼저 이진 분류(binary classification)만 다룹니다.

예를 들면 다음과 같습니다.

| 업무 상황 | 예측하려는 값 |
| --- | --- |
| 정상 거래 / 사기 거래 | 0 / 1 |
| 불합격 / 합격 | 0 / 1 |
| 비이탈 / 이탈 | 0 / 1 |

이때 SVM의 관심은 단순히 `예측을 맞힌다`에만 있지 않습니다. `맞히는 선이 얼마나 여유 있게 놓였는가`도 함께 봅니다.

실무 감각으로 다시 읽으면 다음과 같습니다.

| 장면 | SVM이 특히 신경 쓰는 질문 |
| --- | --- |
| 사기 거래 탐지 | 정상 거래와 사기 거래의 경계가 너무 촘촘해 작은 흔들림에도 뒤집히지 않는가? |
| 채용 서류 분류 | 합격/보류 경계가 특정 사례에 과하게 끌려가지 않는가? |
| 설비 이상 탐지 | 정상과 이상 상태가 구분되더라도 경계가 너무 빡빡해 경보가 불안정하지 않은가? |

SVM은 단지 `누가 어느 class인가`보다 `그 기준이 얼마나 불안정한가`를 함께 의식하게 만드는 모델입니다.

### 로지스틱 회귀, k-NN과는 무엇이 다른가

앞 절의 모델들과 SVM을 나란히 놓으면 차이가 더 선명해집니다.

| 모델 | 중심 질문 |
| --- | --- |
| 로지스틱 회귀 | 어떤 선형 점수와 threshold로 class를 나눌까? |
| k-NN | 이 점 주변의 가까운 사례들은 어떤 class인가? |
| SVM | 두 class를 나누되, 가장 여유 있는 경계는 무엇인가? |

이 비교는 매우 중요합니다. 세 모델 모두 분류(classification)를 하지만, `무엇을 좋은 판단 기준으로 보는가`가 다릅니다.

- 로지스틱 회귀는 점수와 확률처럼 읽히는 출력을 잘 보여 줍니다.
- k-NN은 주변 사례를 근거로 삼는 판단을 보여 줍니다.
- SVM은 경계와 margin 중심의 판단을 보여 줍니다.

따라서 SVM을 읽을 때는 `예측값`만 보지 말고, `경계가 얼마나 빡빡한가`, `어떤 점들이 경계를 떠받치는가`도 함께 봐야 합니다.

### 언제 SVM을 먼저 후보로 올리면 좋은가

SVM은 분류 문제의 모든 기본 해답은 아니지만, `경계의 안정성` 자체가 중요한 문제에서는 좋은 후보가 됩니다.

| 현재 문제 상태 | SVM을 먼저 올릴 이유 | 먼저 확인할 점 |
| --- | --- | --- |
| 분류 경계가 너무 빡빡해 보인다 | margin이 큰 경계를 우선 찾기 때문 | 경계 근처 사례가 많은지 |
| 작은 흔들림에도 class가 자주 바뀐다 | 안정적인 분리선을 찾는 발상이 필요하기 때문 | support vector처럼 보이는 점이 어디인지 |
| 선형 경계 후보는 있지만 여유 폭이 의심된다 | 같은 분리라도 더 좋은 경계를 비교할 수 있기 때문 | baseline이나 로지스틱 회귀와 무엇이 다른지 |
| 경계 근처 사례를 review 대상으로 관리하고 싶다 | margin 근처 사례를 따로 기록하기 좋기 때문 | 어떤 사례를 검토 대상으로 남길지 |
| 나중에 비선형 경계 후보까지 확장할 가능성이 있다 | 선형 SVM에서 kernel SVM으로 자연스럽게 이어지기 때문 | 현재는 선형으로 충분한지 |

이 표의 핵심은 SVM을 `또 하나의 분류기`가 아니라, `좋은 경계의 기준을 더 강하게 묻는 후보`로 위치시키는 데 있습니다.

이 절은 앞 모델들과 무엇이 다르게 중요해지는지를 다음처럼 잡습니다.

| 모델 | 먼저 붙잡는 질문 | 지금 절에서 더 강하게 보는 기준 |
| --- | --- | --- |
| 로지스틱 회귀 | 어떤 점수와 threshold로 class를 가를까? | 확률처럼 읽히는 출력과 선형 경계 |
| k-NN | 주변의 어떤 사례를 참고할까? | 지역 이웃과 거리 기준 |
| SVM | 여러 경계 중 어떤 경계가 더 안정적인가? | margin과 support vector |

SVM은 `경계를 그릴 수 있는가`를 넘어서 `그 경계가 얼마나 여유 있고 안정적인가`를 중심 질문으로 바꿉니다. 이 기준이 잡혀야 뒤의 soft margin, kernel, `C` 같은 설명도 새 옵션 목록이 아니라 `좋은 경계의 기준을 조정하는 장치`로 읽힙니다.

여기에 한 가지를 더 붙이면 SVM 절이 지금까지 정리한 비교 기록 구조와 직접 이어집니다. SVM을 후보로 올릴 때는 `margin이 크다`는 말만 남기는 것이 아니라, `어떤 사례가 margin 근처에 남아 있는가`, `baseline이나 다른 후보보다 무엇이 더 안정적으로 보이는가`, `다음에 무엇을 더 조정할 것인가`를 함께 적어 둡니다. 이때 margin 근처 사례는 우선 검토 우선순위를 올리는 신호로 읽고, 그 사례가 왜 거기에 남았는지 원인 설명까지 자동으로 끝난 것으로 보지는 않습니다.

| 같이 남길 기록 | 왜 필요한가 |
| --- | --- |
| baseline과 SVM 비교 | 단순 기준보다 margin 관점이 실제로 무엇을 바꾸는지 보기 위해서입니다. |
| margin 근처 사례 | review 대상으로 남겨야 할 애매한 사례를 찾기 위해서입니다. |
| support vector처럼 읽히는 점 | 어떤 점이 경계를 가장 많이 흔드는지 다시 보기 위해서입니다. |
| 다음 실험 질문 | `C`를 볼지, 커널 후보를 올릴지, 특징을 더 볼지 정하기 위해서입니다. |

## 연습 및 예제

### Python 예제로 `완벽 분리`가 깨지면 무엇이 달라지는가 보기

이번 예제는 앞 예제에 경계 근처의 `애매한 negative 점` 하나를 더 넣습니다.

문제 상황:

- 원래는 잘 분리되던 두 class 사이에 경계 근처 예외 사례가 하나 들어온다

입력(input):

- negative 점 목록
- positive 점 목록
- 여러 후보 경계 `boundary_x`

기대 출력(output):

- 각 경계에서의 음성 쪽 최근접 거리
- 양성 쪽 최근접 거리
- margin 값

확인할 개념:

- 어떤 경계는 더 이상 완벽한 분리를 만들지 못한다
- 완벽한 분리가 어려워지면 `margin이 큰가`만이 아니라 `어느 정도의 침범을 허용할 것인가`도 같이 생각해야 한다

```python
# SVM에서 여러 경계 후보의 margin과 support vector처럼 작동하는 가까운 점을 비교하는 예제입니다.
negative = [(1.0, 2.0), (2.0, 3.0), (3.0, 2.5), (4.7, 2.4)]
positive = [(5.0, 2.2), (6.0, 3.2), (7.0, 2.8)]

for boundary_x in [4.0, 4.8, 5.2]:
    neg_min = min(boundary_x - x for x, _ in negative)
    pos_min = min(x - boundary_x for x, _ in positive)
    margin = min(neg_min, pos_min)

    print("boundary x =", boundary_x)
    print("  negative-side nearest distance =", round(neg_min, 3))
    print("  positive-side nearest distance =", round(pos_min, 3))
    print("  margin =", round(margin, 3))
    print("  perfectly separates? =", neg_min > 0 and pos_min > 0)
    print()
```

실행 결과 예시는 다음과 같습니다.

```text
boundary x = 4.0
  negative-side nearest distance = -0.7
  positive-side nearest distance = 1.0
  margin = -0.7
  perfectly separates? = False

boundary x = 4.8
  negative-side nearest distance = 0.1
  positive-side nearest distance = 0.2
  margin = 0.1
  perfectly separates? = True

boundary x = 5.2
  negative-side nearest distance = 0.5
  positive-side nearest distance = -0.2
  margin = -0.2
  perfectly separates? = False
```

이 출력에서 읽을 점은 분명합니다.

- 경계 근처의 예외 점 하나만 들어와도 일부 경계는 더 이상 완벽히 분리되지 않습니다.
- 겨우 분리가 되더라도 margin이 매우 작아질 수 있습니다.
- 그래서 현실의 SVM은 `완벽 분리만 고집하지 않고`, `margin과 오류 허용을 함께 조정`하는 방향으로 넘어갑니다.

### 값 하나 더 바꿔 보기: 예외 점이 경계에 더 가까워지면 무엇이 유지되고 무엇이 달라지는가

이번에는 애매한 negative 점을 `(4.7, 2.4)`에서 `(4.9, 2.4)`로 더 오른쪽으로 옮겨 봅니다.

```python
# SVM에서 여러 경계 후보의 margin과 support vector처럼 작동하는 가까운 점을 비교하는 예제입니다.
negative = [(1.0, 2.0), (2.0, 3.0), (3.0, 2.5), (4.9, 2.4)]
positive = [(5.0, 2.2), (6.0, 3.2), (7.0, 2.8)]

for boundary_x in [4.8, 4.95]:
    neg_min = min(boundary_x - x for x, _ in negative)
    pos_min = min(x - boundary_x for x, _ in positive)
    margin = min(neg_min, pos_min)

    print("boundary x =", boundary_x)
    print("  negative-side nearest distance =", round(neg_min, 3))
    print("  positive-side nearest distance =", round(pos_min, 3))
    print("  margin =", round(margin, 3))
    print("  perfectly separates? =", neg_min > 0 and pos_min > 0)
    print()
```

실행 결과 예시는 다음과 같습니다.

```text
boundary x = 4.8
  negative-side nearest distance = -0.1
  positive-side nearest distance = 0.2
  margin = -0.1
  perfectly separates? = False

boundary x = 4.95
  negative-side nearest distance = 0.05
  positive-side nearest distance = 0.05
  margin = 0.05
  perfectly separates? = True
```

### 무엇이 유지되고 무엇이 달라지는가

- 유지된 점: 여전히 질문은 `class를 나눌 수 있는가`보다 `얼마나 여유 있게 나눌 수 있는가`에 있습니다.
- 바뀐 점: 예외 점이 경계에 더 가까워지자, 원래 가능해 보이던 경계도 더 쉽게 분리 실패로 바뀌거나 아주 작은 margin만 남깁니다.
- 먼저 남길 판단: 같은 분리 성공 여부라도 margin이 `0.2`일 때와 `0.05`일 때의 안정성은 전혀 다릅니다.

이 비교를 통해 SVM은 `정답을 맞히는 분류기`가 아니라 `경계 품질을 비교하는 모델`로 읽힙니다. 중요한 것은 분류 결과 하나를 보는 것이 아니라, 어떤 사례가 경계를 얼마나 빡빡하게 만들고 일반화 위험을 키우는지 읽는 일입니다. 예외 점을 조금씩 움직여 보는 반복 실습이 있어야 margin이 숫자 정의를 넘어 `흔들림에 대한 감각`으로 연결됩니다.

| 공통 기록 언어 | 이번 연습에서 바로 남길 내용 |
| --- | --- |
| 보인 구조 | 경계 근처 예외 점을 조금만 움직여도 분리 가능 여부와 margin 크기가 함께 크게 흔들렸다 |
| 해석 경계 | 한 장난감 예제에서 margin이 작아졌다고 해서 실제 모든 데이터에서 같은 경계가 항상 나쁘다고 단정할 수는 없다 |
| 다음 질문 | soft margin과 `C`를 쓰면 이 침범을 어디까지 허용할지, 다른 분류기와 비교하면 무엇이 더 먼저 보이는지 다시 볼 것인가 |

## 사례 및 예시

이 절의 직관은 추상적으로만 남기면 쉽게 흐려집니다. 그래서 업무 장면으로 다시 읽어 볼 필요가 있습니다.

### 사례 1. 사기 거래 탐지

- 너무 작은 margin:
  - 정상 거래와 사기 거래 경계가 너무 촘촘합니다.
  - 소액 결제, 해외 접속, 시간대 같은 특징이 조금만 흔들려도 class가 바뀔 수 있습니다.
- 더 큰 margin:
  - 경계가 양쪽 class에서 조금 더 떨어져 있습니다.
  - 애매한 거래는 남더라도, 기준선 자체는 덜 예민하게 흔들립니다.

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-04-ko.mmd"
```

### 사례 2. 채용 서류 분류

- 너무 작은 margin:
  - 특정 몇 명의 특이한 지원서가 경계를 과도하게 끌어당깁니다.
  - 점수 체계가 바뀌거나 새로운 배경을 가진 지원자가 들어오면 결과가 쉽게 흔들릴 수 있습니다.
- 더 큰 margin:
  - 경계가 한두 사례에 덜 끌립니다.
  - 기준이 더 일반적이고 설명 가능한 방향으로 유지될 가능성이 높습니다.

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-05-ko.mmd"
```

`SVM의 margin 직관은 모델이 만든 경계가 현장에서 얼마나 예민하게 흔들릴지를 묻는 질문과 연결된다.`

### 학술적 배경과 역사

SVM은 통계학습이론과 일반화 논의에서 매우 중요한 위치를 차지하는 방법입니다. 앞서 P4-5.2에서 보았듯, 일반화는 훈련 데이터만 잘 맞히는 문제를 넘어서 `새 데이터에서도 타당한 판단을 유지하는가`라는 질문과 연결됩니다.

이 절에서 학술적 배경과 역사는 본론을 대체하는 설명이 아니라, 왜 `margin을 기준으로 좋은 경계를 따로 묻는가`를 짧게 붙잡아 주는 보조 맥락으로만 사용합니다.

역사적으로는 1990년대 Cortes와 Vapnik의 논문 *Support-Vector Networks*가 이 흐름을 대표합니다. 이 절에서 중요한 것은 세부 증명보다 다음 변화입니다.

1. 분류는 경계를 찾는 문제로 읽을 수 있다.
2. 경계는 하나가 아니라 여러 개일 수 있다.
3. 그러므로 `어떤 경계가 더 좋은가`라는 기준이 필요하다.
4. SVM은 그 기준을 margin 최대화라는 언어로 제시했다.

이 때문에 SVM은 단순한 알고리즘 이름이 아니라, `일반화를 기하학적으로 설명하려는 대표 사례`로도 자주 소개됩니다.

이 절의 핵심은 SVM 이름을 외우는 일이 아니라, 좋은 경계를 어떤 기준으로 읽을지 고정하는 데 있습니다.

같은 흐름을 한 번에 다시 묶으면 다음과 같습니다.

```mermaid
--8<-- "assets/part-04/chapter-13/p4-13-1-mermaid-06-ko.mmd"
```

| 같이 봐야 할 것 | 이 절에서 먼저 읽는 질문 | 바로 다음에 이어질 곳 |
| --- | --- | --- |
| margin과 support vector | 여러 경계 중 무엇이 더 여유 있고 안정적인가 | P4-13.2 kernel과 비선형 경계 |
| soft margin과 오류 허용 | 완벽한 분리보다 어떤 균형을 택해야 하는가 | P4-9 하이퍼파라미터, `C` 해석 |
| 앞 모델과의 비교 | 로지스틱 회귀와 k-NN이 못 보여 준 어떤 기준이 추가되는가 | 뒤 분류 알고리즘 비교와 일반화 해석 |

## 체크리스트

- SVM을 class를 나누는 경계 중에서도 `더 큰 margin`을 갖는 경계를 찾으려는 모델로 설명할 수 있는가?
- margin을 경계와 가장 가까운 데이터들 사이의 여유 폭으로 읽을 수 있는가?
- support vector처럼 경계를 실제로 떠받치는 사례가 무엇인지 다시 볼 수 있는가?
- 현실 데이터에서는 완벽한 분리보다 `여유`와 `오류 허용`의 균형이 중요하다는 점을 이해했는가?
- 지금 문제에서 단지 나누는 것보다 경계의 여유와 안정성이 더 중요한가?
- 작은 점수 차이보다 margin 근처 사례의 성격을 함께 확인하고 있는가?
- 로지스틱 회귀나 k-NN과 비교해 SVM의 질문이 `무엇이 더 좋은 경계인가`라는 점을 설명할 수 있는가?

## 출처와 참고 자료

- scikit-learn, *Support Vector Machines*, scikit-learn User Guide, 확인 날짜: 2026-06-27. <https://scikit-learn.org/stable/modules/svm.html>{: target="_blank" rel="noopener noreferrer" }
- C. Cortes and V. Vapnik, *Support-Vector Networks*, Machine Learning, 1995, 확인 날짜: 2026-07-19. [https://doi.org/10.1007/BF00994018](https://doi.org/10.1007/BF00994018){: target="_blank" rel="noopener noreferrer" }
