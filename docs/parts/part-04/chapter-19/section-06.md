# P4-19.6 보충학습: policy gradient 첫 읽기

> Section ID: `P4-19.6`
> Version: `v2026.07.26`

_보조제목: likelihood ratio trick은 정책 확률 변화와 기대 보상을 어떻게 연결하는가_

P4-19.2에서 정책 기반 강화학습을 읽다 보면 곧 다음 이름이 붙습니다.

- [policy gradient theorem](../../../reference/concept-glossary-parts/09-jieut.md#policy-gradient-theorem)
- [likelihood ratio trick](../../../reference/concept-glossary-parts/01-giyeok.md#likelihood-ratio-trick)

이 절은 엄밀한 증명 전체를 끝까지 따라가기보다, 왜 정책 파라미터의 변화가 [기대 보상(expected reward)](../../../reference/concept-glossary-parts/01-giyeok.md#expected-reward) 변화와 연결되는가, 왜 [로그 확률(log-probability)](../../../reference/concept-glossary-parts/04-rieul.md#log-probability) 형태가 자주 나오는가를 처음 읽는 보충학습입니다.

## 보충학습: policy gradient와 likelihood ratio trick을 처음 읽는 법에서 닫을 질문

이 절은 다음 질문에 답합니다.

- [policy gradient](../../../reference/concept-glossary-parts/09-jieut.md#policy-gradient)는 왜 정책 확률을 직접 조정하는 식으로 읽히는가?
- likelihood ratio trick은 왜 로그 확률과 기대값 계산을 연결하는가?
- 이 수식 감각이 [REINFORCE](../../../reference/concept-glossary-parts/04-rieul.md#reinforce)와 [actor-critic](../../../reference/concept-glossary-parts/08-ieung.md#actor-critic) 해석에 어떻게 이어지는가?

이 절은 `정책 확률`, `기대 보상`, `로그 확률 기울기`라는 세 손잡이로 정책 기반 수식의 입문 감각을 잡는 데 집중합니다.

## 보충학습: policy gradient와 likelihood ratio trick을 처음 읽는 법에서 남길 판단 기준

- policy gradient를 `기대 보상을 늘리는 방향으로 정책 확률을 조정하는 기울기`로 설명할 수 있습니다.
- likelihood ratio trick을 `확률 분포 안쪽의 미분을 로그 확률 기울기로 바꾸어 계산을 읽기 쉽게 하는 장치`로 설명할 수 있습니다.
- REINFORCE와 actor-critic에서 왜 `log pi(a|s)` 같은 형태가 등장하는지 말할 수 있습니다.

## 왜 이 절이 필요한가

정책 기반 강화학습은 직관 문장으로는 이해하기 쉽지만, 수식을 만나면 갑자기 낯설어집니다.

- 왜 기대 보상을 미분하는데 로그가 나오지?
- 왜 행동 확률의 기울기가 보상과 곱해지지?

바로 여기서 likelihood ratio trick이 등장합니다.

즉, 이 절의 핵심은 `정책을 직접 조정한다`는 말이 수식에서는 어떻게 `로그 확률의 기울기`로 읽히는지 처음 연결하는 데 있습니다.

## policy gradient는 무엇을 미분하려는가

정책 기반 강화학습은 결국 다음 질문을 품고 있습니다.

`정책 파라미터를 조금 바꾸면, 장기 기대 보상이 더 커지는 방향은 어디인가?`

그래서 policy gradient는 아주 짧게 말하면:

`기대 보상을 늘리는 방향으로 정책 파라미터를 움직이기 위한 기울기`

입문적으로는 다음 정도만 붙잡으면 충분합니다.

| 읽는 질문 | policy gradient가 말하는 것 |
| --- | --- |
| 무엇을 바꾸는가 | 정책 파라미터 |
| 왜 바꾸는가 | 기대 보상을 더 크게 만들기 위해 |
| 어떤 신호를 쓰는가 | 보상이 좋았던 행동은 더 자주, 나빴던 행동은 덜 자주 나오게 하는 방향 |

즉, policy gradient는 `정책 분포를 직접 미세 조정하는 업데이트`로 읽는 편이 맞습니다.

## likelihood ratio trick은 왜 나오는가

기대값 안에 확률 분포가 들어 있으면 미분이 까다로워집니다. likelihood ratio trick은 이때 자주 쓰이는 변형입니다.

핵심 감각은 다음 한 문장입니다.

`확률 자체를 직접 미분하기보다, 로그 확률의 기울기로 바꾸면 기대값 안에서 읽기가 쉬워진다.`

아주 짧게 형태만 보면 다음처럼 읽습니다.

```text
grad p(x) = p(x) * grad log p(x)
```

이 식의 역할은 `확률 분포가 기대값 안에 있을 때, 그 미분을 샘플 기반 업데이트와 연결하기 쉽게 바꾸는 것`입니다.

즉, 로그가 나오는 이유는 장식이 아니라 계산 구조를 바꾸기 위해서입니다.

## 그래서 REINFORCE 식은 어떻게 읽으면 되는가

REINFORCE 직관은 보통 다음 형태로 읽을 수 있습니다.

`좋은 보상을 준 행동의 log-probability 기울기는 강화하고, 나쁜 보상을 준 행동의 기울기는 약화한다.`

입문적으로는 다음 비교가 가장 중요합니다.

| 보상이 좋았다 | 보상이 나빴다 |
| --- | --- |
| 그 행동이 다시 나올 확률을 높이는 방향으로 조정 | 그 행동이 덜 나오게 하는 방향으로 조정 |
| `log pi(a|s)` 기울기가 강화 신호로 쓰인다 | 같은 기울기가 반대 방향 신호로 작동할 수 있다 |

이때 likelihood ratio trick은 `왜 이런 업데이트가 log-probability 형태로 적히는가`를 설명해 주는 연결 다리입니다.

## actor-critic과는 어떻게 이어지나

P4-19.2에서 본 actor-critic은 정책을 직접 조정하되, critic이 평가 신호를 더 안정적으로 주는 구조입니다. 수식 감각으로 보면 다음처럼 읽을 수 있습니다.

- actor: 여전히 정책의 로그 확률 기울기를 따라 조정한다
- critic: 어떤 행동이 얼마나 좋았는지 평가 신호를 더 덜 흔들리게 준다

즉, actor-critic은 policy gradient를 버리는 것이 아니라, `그 기울기에 곱해지는 평가 신호를 더 안정적으로 만드는 방향`으로 읽을 수 있습니다.

## 사례 및 예시

### 사례 1. 좋은 광고 노출 비율은 더 자주, 나쁜 비율은 덜 자주 나오게 만들고 싶을 때

광고 노출 정책이 `할인 배너 70% / 추천 배너 30%` 같은 비율을 확률적으로 고른다고 해 보겠습니다. 사람이 먼저 쓰기 쉬운 기준은 보통 `이번에 잘된 배너 비율을 다음에도 더 많이 쓰자`는 직관입니다.

이 직관은 방향은 맞지만, 수식을 만나면 금방 흐려집니다. `왜 확률을 직접 고친다고 하지?`, `왜 log-probability가 나오지?`, `왜 같은 행동도 보상 부호에 따라 조정 방향이 달라지지?` 같은 질문이 바로 생기기 때문입니다. policy gradient와 likelihood ratio trick은 이 지점에서 `좋은 확률은 올리고, 나쁜 확률은 내리는` 직관을 수식 읽기로 이어 주는 역할을 합니다.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-6-mermaid-01-ko.mmd"
```

| 문제 장면 | 사람이 먼저 쓰기 쉬운 기준 | 곧 드러나는 한계 | 현재 절이 바꾸는 해석 |
| --- | --- | --- | --- |
| 추천 배너 비중이 장기 구매를 늘렸다 | 다음에도 그 비중을 더 자주 쓰자 | 확률을 어떤 계산으로 조정할지 설명이 부족하다 | 기대 보상을 늘리는 방향의 policy gradient로 읽는다 |
| 클릭은 높았지만 환불과 이탈이 늘었다 | 그 비율을 줄이자 | 왜 같은 행동이 반대 방향 신호를 받는지 수식이 낯설다 | 보상 부호에 따라 log-probability 기울기 해석이 달라진다 |
| 수식에 `log pi(a|s)`가 등장한다 | 어려운 수학 장식 같다 | 확률 미분과 샘플 기반 업데이트 연결이 안 보인다 | likelihood ratio trick으로 읽는다 |

이 사례의 확인 가능한 결과는 `좋은 비율은 더 자주, 나쁜 비율은 덜 자주`라는 문장을, `기대 보상`, `로그 확률 기울기`, `보상 부호`라는 세 손잡이로 다시 읽을 수 있게 되는가에 있습니다. 즉, 정책 기반 직관이 수식 때문에 사라지는 것이 아니라, 수식이 그 직관을 더 정밀하게 적는 도구라는 점을 확인해야 합니다.

## 연습 및 예제

이번 연습은 `좋은 보상 -> chosen action 확률 강화`, `나쁜 보상 -> chosen action 확률 약화`, `왜 log-probability가 같이 등장하는가`를 작은 숫자로 직접 보는 데 초점을 둡니다.

문제 상황:

- policy gradient와 likelihood ratio trick은 이름만 보면 추상적이지만, 실제로는 `선택한 행동 확률을 어떤 방향으로 밀 것인가`를 계산하기 위한 장치다

입력(input):

- 두 행동의 정책 점수(logit)
- 선택된 행동
- 같은 행동에 대한 양의 보상과 음의 보상

기대 출력(output):

- 업데이트 전 행동 확률
- 선택된 행동의 `grad log pi(a|s)`
- 보상 부호에 따라 달라지는 업데이트 후 행동 확률

확인할 개념:

- log-probability는 선택한 행동 확률을 업데이트 계산에 연결하는 읽기 장치다
- 보상 부호가 바뀌면 같은 행동에 대한 조정 방향도 바뀐다

```python
import numpy as np


def softmax(logits):
    shifted = logits - np.max(logits)
    exp_values = np.exp(shifted)
    return exp_values / exp_values.sum()


# 두 행동: 할인 배너 노출, 추천 배너 노출
logits = np.array([0.2, -0.2])
chosen_action = 0
learning_rate = 0.4

for reward in [2.0, -2.0]:
    probs_before = softmax(logits)
    grad_log_prob = -probs_before
    grad_log_prob[chosen_action] += 1.0
    logits_after = logits + learning_rate * reward * grad_log_prob
    probs_after = softmax(logits_after)

    print("reward=", reward)
    print("prob_before=", [round(float(v), 3) for v in probs_before])
    print("grad_log_prob=", [round(float(v), 3) for v in grad_log_prob])
    print("prob_after=", [round(float(v), 3) for v in probs_after])
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
reward= 2.0
prob_before= [0.599, 0.401]
grad_log_prob= [0.401, -0.401]
prob_after= [0.739, 0.261]
reward= -2.0
prob_before= [0.599, 0.401]
grad_log_prob= [0.401, -0.401]
prob_after= [0.44, 0.56]
```

이 예제에서 핵심은 숫자 부호 자체를 외우는 데 있지 않습니다.

1. `grad log pi(a|s)`는 선택한 행동 확률을 업데이트 계산과 연결해 주는 읽기 손잡이다.
2. 같은 행동이라도 보상이 양수이면 선택된 행동의 확률이 `0.599 -> 0.739`로 올라간다.
3. 보상이 음수이면 같은 기울기를 써도 선택된 행동의 확률이 `0.599 -> 0.44`로 내려간다.
4. likelihood ratio trick은 이런 연결을 `확률 미분` 대신 `로그 확률 기울기`로 읽기 쉽게 바꾸는 역할을 한다.

### 직접 판단해 보기

아래 관찰을 보고, 어느 해석이 더 안전한지 먼저 골라 봅니다.

| 관찰 | 성급한 결론 | 더 안전한 해석 |
| --- | --- | --- |
| `log pi(a|s)`가 음수로 나온다 | 정책이 틀렸다 | 확률이 1보다 작으면 로그는 음수일 수 있고, 중요한 것은 보상과 곱해진 조정 방향이다 |
| 같은 행동에 양의 보상과 음의 보상을 넣었더니 신호 부호가 바뀌었다 | 수식이 불안정하다 | 보상 부호에 따라 그 행동을 더 자주 혹은 덜 자주 나오게 하려는 해석이 달라진다 |
| 로그 확률이 등장한다 | 단지 수학 장식이다 | 기대값 안의 확률 미분을 샘플 기반 업데이트와 연결하기 쉽게 바꾼 장치다 |

이 표의 목적은 수식을 증명하는 데 있지 않습니다. `정책 확률을 어떻게 밀고 당기는가`, `왜 로그 확률이 그 연결에 필요한가`를 해석 중심으로 붙잡는 데 있습니다.

## 체크리스트

- policy gradient가 정책 파라미터를 기대 보상 증가 방향으로 움직이려는 기울기라는 점을 설명할 수 있는가
- likelihood ratio trick이 확률 미분을 로그 확률 기울기로 바꾸어 읽기 쉽게 만드는 장치라는 점을 설명할 수 있는가
- REINFORCE와 actor-critic 모두 이 로그 확률 기울기 감각 위에서 읽을 수 있다는 점을 설명할 수 있는가
- 양의 보상과 음의 보상이 chosen action 확률을 서로 다른 방향으로 조정하게 만든다는 점을 말할 수 있는가

## 출처와 참고 자료

- Ronald J. Williams, `Simple statistical gradient-following algorithms for connectionist reinforcement learning`, Machine Learning, 1992. REINFORCE 계열 알고리즘과 expected reinforcement의 gradient-following 관점을 확인할 때 참고했다. 확인 날짜: 2026-07-19. [https://doi.org/10.1007/BF00992696](https://doi.org/10.1007/BF00992696){: target="_blank" rel="noopener noreferrer" }
- Richard S. Sutton, David McAllester, Satinder Singh, Yishay Mansour, `Policy Gradient Methods for Reinforcement Learning with Function Approximation`, NeurIPS 1999. policy gradient theorem, approximate value/advantage function과 경험 기반 추정 연결을 확인할 때 참고했다. 확인 날짜: 2026-07-19. [https://papers.nips.cc/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html](https://papers.nips.cc/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Vijay R. Konda, John N. Tsitsiklis, `On Actor-Critic Algorithms`, SIAM Journal on Control and Optimization, 2003. actor-critic을 policy gradient 계열의 평가 신호 안정화 관점으로 연결할 때 참고했다. 확인 날짜: 2026-07-19. [https://doi.org/10.1137/S0363012901385691](https://doi.org/10.1137/S0363012901385691){: target="_blank" rel="noopener noreferrer" }
