# P5-14.8 보충학습: 값의 기준선을 맞추는 정규화

> Section ID: `P5-14.8`
> Version: `v2026.07.31`

_보조제목: layer normalization은 한 위치 표현 안의 평균과 퍼짐을 어떻게 다시 맞추는가_

P5-14.2에서는 Transformer 블록 안에서 layer normalization이 값 범위를 정리한다고 보았습니다. 그런데 `정규화(normalization)`라는 말은 입력 전처리, 배치 정규화(batch normalization), 정규화(regularization)와 쉽게 섞입니다.

Transformer 블록에서 layer normalization은 의미를 새로 고르는 장치가 아니라, 한 위치 표현 안의 값들이 다음 계산으로 넘어가기 쉬운 기준선에 놓이도록 평균과 퍼짐을 다시 맞추는 장치입니다.

용어가 다시 흩어질 때는 개념사전의 [레이어 정규화(layer normalization)](../../../reference/concept-glossary-parts/12-tieut.md#transformer) 항목과 P5-14.2의 네 부품 역할 분담을 함께 다시 보면 좋습니다.

## 값의 기준선이 흔들린다는 뜻

Transformer 블록 안의 표현은 하나의 숫자가 아니라 여러 축을 가진 벡터입니다. 어떤 축은 `재기동`이라는 조치 의미를 담고, 어떤 축은 `보류`, `위험`, `조건` 같은 문맥 단서를 담는다고 생각할 수 있습니다.

self-attention과 feed-forward network가 표현을 바꾸고, residual connection이 원래 표현까지 더하면 값의 크기와 퍼짐이 계속 달라질 수 있습니다. 어떤 블록에서는 일부 축이 너무 커지고, 다른 블록에서는 값들이 너무 좁게 모일 수 있습니다. 이 상태가 계속되면 다음 attention이나 feed-forward는 매번 다른 기준선에서 입력을 받게 됩니다.

입문 단계에서는 다음처럼 읽으면 충분합니다.

| 흔들린 상태 | 왜 문제가 되는가 |
| --- | --- |
| 어떤 표현 축이 지나치게 크다 | 다음 계산이 그 축에 과하게 끌릴 수 있다 |
| 값들이 너무 좁게 모여 있다 | 축 사이 차이가 약해져 구분이 흐려질 수 있다 |
| 블록마다 값 범위가 크게 달라진다 | 다음 부품이 비슷한 기준으로 계산을 이어가기 어렵다 |

layer normalization은 이 문제를 `어떤 의미가 중요한가`로 풀지 않습니다. 한 위치 표현 안의 값 범위를 다시 정리해, 다음 계산이 다루기 쉬운 입력 상태를 만듭니다.

## 한 위치 안에서 평균과 퍼짐을 맞춘다

layer normalization의 핵심은 `한 위치 표현 안에서` 값을 정리한다는 점입니다. 즉 문장 전체 토큰을 한꺼번에 섞어 의미를 고르는 것이 아니라, 현재 위치의 표현 벡터 안에 있는 여러 숫자 축을 기준으로 평균과 퍼짐을 맞춥니다.

```mermaid
--8<-- "assets/part-05/chapter-14/layer-normalization-value-scale-ko.mmd"
```

이 도식에서 앞 표현은 이미 attention, feed-forward, residual connection을 지나 값 범위가 흔들린 상태입니다. layer normalization은 그 값을 한 위치 안에서 다시 정리하고, 다음 계산이 시작할 수 있는 기준선으로 넘깁니다.

여기서 중요한 경계는 다음과 같습니다.

| 질문 | 더 직접 맡는 부품 |
| --- | --- |
| 어떤 다른 토큰을 참고할까 | self-attention |
| 문맥이 섞인 현재 표현을 어떻게 바꿀까 | feed-forward network |
| 원래 표현이 새 계산에 덮이지 않게 할까 | residual connection |
| 다음 계산이 다루기 쉬운 값 범위인가 | layer normalization |

layer normalization은 이 네 번째 질문에 답합니다. 따라서 `값을 정리한다`는 말은 `의미를 지운다`나 `중요한 의미만 남긴다`가 아니라, 다음 계산이 같은 종류의 입력을 더 안정적으로 다룰 수 있게 기준선을 맞춘다는 뜻입니다.

## batch normalization과 무엇이 다른가

초심자에게 가장 자주 생기는 혼동은 layer normalization과 batch normalization을 같은 것으로 읽는 것입니다. 둘 다 normalization이라는 이름을 쓰지만, 무엇을 기준으로 통계를 잡는지가 다릅니다.

| 구분 | 기준으로 보는 것 | Transformer 문맥에서 읽는 감각 |
| --- | --- | --- |
| batch normalization | 여러 샘플이 들어 있는 배치의 통계 | 배치 구성과 학습/평가 모드 차이를 함께 고려해야 한다 |
| layer normalization | 한 샘플, 한 위치 표현 안의 여러 값 | 현재 위치 표현을 다음 계산 기준선에 맞춘다 |

Part 5의 앞쪽에서 배치 정규화를 볼 때는 여러 샘플이 함께 들어오는 학습 배치가 중요했습니다. 반면 Transformer의 layer normalization은 한 위치 표현 안의 값들을 기준으로 정리한다고 읽는 편이 입문 단계에서는 더 직접적입니다.

이 차이는 실제 사용 맥락에서도 중요합니다. 언어 모델은 문장 길이, 배치 구성, 생성 시점이 다양하게 바뀔 수 있습니다. 이때 layer normalization은 현재 위치 표현 자체를 기준으로 값을 정리하므로, Transformer 블록 안에서 반복적으로 쓰기 좋은 안정화 장치가 됩니다.

## residual connection 뒤에서 왜 자주 보이는가

Transformer 설명에서 residual connection과 layer normalization은 자주 붙어 나옵니다. 그러나 두 장치가 같은 일을 해서 붙는 것은 아닙니다.

residual connection은 원래 입력 표현과 새 계산 결과를 함께 남깁니다. 이 더하기는 정보 흐름을 보존하는 데 도움이 되지만, 값의 크기와 퍼짐은 더 흔들릴 수 있습니다. layer normalization은 그렇게 합쳐진 표현을 다음 계산이 다루기 쉬운 범위로 다시 맞춥니다.

| 단계 | 중심 질문 | 결과 |
| --- | --- | --- |
| 새 계산 | 현재 표현을 어떻게 바꿀까 | 문맥이 반영된 새 표현이 생긴다 |
| residual connection | 원래 표현을 함께 남길까 | 원래 축과 새 표현이 함께 남는다 |
| layer normalization | 다음 계산이 다루기 쉬운 범위인가 | 값 기준선이 정리된다 |

따라서 `residual + normalization`을 한 덩어리로 외우면 부족합니다. residual connection은 정보 흐름의 문제를 다루고, layer normalization은 값 범위의 문제를 다룹니다.

## 값의 기준선을 맞추는 정규화: 확인할 판단 기준

이 사례를 읽을 때는 다음 두 가지를 먼저 확인한다.

- layer normalization이 의미 선택이 아니라 값 기준선 정리라는 점을 보충해야 합니다. Python 예제는 평균·표준편차와 다음 계산 점수의 전후 차이를 보여 주는 데 한정하고, P5-14.2의 역할 분담을 반복하는 연습은 늘리지 않습니다.
- 이어지는 사례에서 입력, 비교 기준, 출력, 한계가 제목의 판단 기준과 어떻게 연결되는지 확인한다.

### 사례. 작업 허가 문장에서 값 기준선이 흔들리는 경우

`압력 미해소 상태에서는 재기동을 보류한다`에서 `재기동` 위치를 보겠습니다. attention은 `압력 미해소`와 `보류`를 함께 참고하게 만들고, feed-forward는 현재 표현을 `조건부 차단 조치` 쪽으로 가공합니다. residual connection은 여기에 원래 `재기동` 조치 축을 함께 남깁니다.

이제 뒤 블록으로 넘길 표현에는 여러 단서가 함께 들어 있습니다. `재기동`, `압력 미해소`, `보류`, `위험`, `조건` 같은 축이 서로 다른 크기로 남을 수 있습니다. 일부 축이 너무 커지면 뒤 계산은 그 축에 과하게 끌릴 수 있고, 값들이 너무 작거나 좁게 모이면 단서 차이를 충분히 읽지 못할 수 있습니다.

layer normalization은 이때 `재기동이 중요한가, 보류가 중요한가`를 새로 판단하지 않습니다. 이미 만들어진 현재 위치 표현의 값 범위를 정리해, 다음 블록이 비슷한 기준선에서 다시 관계 읽기와 표현 가공을 시작하게 합니다.

| 표현 안에 함께 남은 단서 | layer normalization이 직접 하는 일 | 직접 하지 않는 일 |
| --- | --- | --- |
| `재기동`, `보류`, `위험` 축의 값 크기가 제각각이다 | 평균과 퍼짐을 맞춰 다음 계산 기준선을 정리한다 | 어떤 단서가 법적으로 더 중요한지 판단한다 |
| residual로 원래 조치 축과 새 위험 축이 함께 남았다 | 합쳐진 표현의 값 범위를 안정화한다 | 원래 조치 축을 보존하는 경로를 새로 만든다 |
| 다음 attention이 이 위치를 다시 사용할 예정이다 | 다음 계산이 다루기 쉬운 입력 상태로 만든다 | 어떤 토큰을 다시 볼지 고른다 |

이 사례에서 확인해야 할 결과는 layer normalization이 의미 판단자가 아니라 계산 기준선 정리자라는 점입니다.

### 예시. 값 범위 흔들림을 실험으로 넘기기

두 표현이 모두 `재기동은 보류해야 한다`는 방향을 담고 있다고 해도, 값 범위가 크게 다르면 다음 계산이 받는 입력 감각은 달라질 수 있습니다. 예를 들어 한 축만 지나치게 크거나, 모든 값이 너무 좁게 모이거나, 블록마다 값 범위가 크게 바뀌면 다음 attention과 feed-forward는 매번 다른 기준선에서 입력을 받습니다.

이 차이는 말로만 보면 쉽게 흐려집니다. 그래서 다음 예제에서는 `risk_axis_spike`, `too_narrow`, `mixed_after_residual` 세 표현을 직접 넣고, normalization 전후의 평균, 퍼짐, 다음 계산 점수가 어떻게 달라지는지 확인합니다. 여기서 먼저 잡아야 할 기준은 `표현 의미`와 `값 스케일`이 같은 문제가 아니라는 점입니다.

## 연습 및 예제

### 예제. layer normalization 전후의 기준선 확인하기

이 예제는 layer normalization의 수식을 외우기 위한 코드가 아닙니다. 한 위치 표현 안의 값 범위가 흔들릴 때, 평균과 퍼짐을 맞춘 뒤 다음 계산이 받는 입력 감각이 어떻게 달라지는지 확인하는 실험입니다.

| 조작할 값 | 관찰할 출력 | 확인할 질문 |
| --- | --- | --- |
| `risk_axis_spike`의 큰 값 | `raw mean/std`, `norm mean/std` | 한 축이 지나치게 클 때 기준선이 어떻게 정리되는가 |
| `too_narrow`의 값 차이 | `normalized values` | 너무 좁게 모인 값도 다시 비교 가능한 퍼짐을 갖는가 |
| `probe` | `next score before/after` | 다음 계산 점수가 원래 값 스케일에 얼마나 끌렸는가 |

```python
# layer normalization 전후의 평균, 표준편차, 다음 계산 점수를 비교해 한 위치 표현의 값 기준선이 어떻게 정리되는지 확인하는 예제입니다.
import numpy as np

representations = {
    "risk_axis_spike": np.array([0.6, 8.0, 0.4, 0.5]),
    "too_narrow": np.array([0.48, 0.51, 0.49, 0.50]),
    "mixed_after_residual": np.array([2.0, 4.5, 1.0, 3.5]),
}

probe = np.array([0.2, 1.0, 0.3, 0.7])

def layer_norm(x, eps=1e-6):
    return (x - x.mean()) / (x.std() + eps)

for name, values in representations.items():
    normalized = layer_norm(values)
    raw_score = float(values @ probe)
    normalized_score = float(normalized @ probe)

    print(f"[{name}]")
    print("raw mean/std =", round(values.mean(), 3), round(values.std(), 3))
    print("norm mean/std =", round(normalized.mean(), 3), round(normalized.std(), 3))
    print("next score before/after =", round(raw_score, 3), round(normalized_score, 3))
    print("normalized values =", np.round(normalized, 3).tolist())
    print("---")
```

출력 예시는 다음처럼 읽습니다.

```text
[risk_axis_spike]
raw mean/std = 2.375 3.248
norm mean/std = -0.0 1.0
next score before/after = 8.59 1.036
normalized values = [-0.546, 1.732, -0.608, -0.577]
---
[too_narrow]
raw mean/std = 0.495 0.011
norm mean/std = 0.0 1.0
next score before/after = 1.103 1.252
normalized values = [-1.342, 1.342, -0.447, 0.447]
---
[mixed_after_residual]
raw mean/std = 2.75 1.346
norm mean/std = 0.0 1.0
next score before/after = 7.65 1.188
normalized values = [-0.557, 1.3, -1.3, 0.557]
```

앞 두 축만 2D 좌표로 투영하면, 정규화 전후의 위치 이동을 다음처럼 볼 수 있습니다. 이 그림은 4차원 표현 전체를 완전히 보여 주는 그래프가 아니라, 값 스케일이 정리되면 같은 표현도 다음 계산이 받는 좌표 감각이 달라진다는 점을 보조로 확인하는 그림입니다.

![layer normalization 전후 벡터 이동](/AiBook/assets/part-05/chapter-14/layer-normalization-vector-shift-ko.png)

첫 번째 경우는 위험 축 하나가 지나치게 큰 표현입니다. layer normalization 뒤에는 평균이 거의 0, 표준편차가 1에 가까워져 다음 계산이 원래 값 크기에 과하게 끌리는 정도가 줄어듭니다. 두 번째 경우는 값들이 너무 좁게 모인 표현입니다. 원래 값 차이는 작지만 표준편차도 작기 때문에, 평균을 빼고 표준편차로 나누면 축 사이의 상대적 차이가 다시 읽히는 범위로 펼쳐집니다.

해설: 이 예제에서 중요한 것은 normalized value 하나하나를 정답처럼 외우는 것이 아닙니다. layer normalization은 의미를 새로 고르지 않고, 한 위치 표현 안의 값 기준선을 다음 계산이 다루기 쉬운 상태로 맞춥니다. 그래서 `next score before/after`의 변화는 의미 판단이 바뀌었다는 뜻이 아니라, 같은 probe가 더 정리된 입력 기준에서 계산된다는 뜻입니다.

### 연습. 값 범위 문제를 말로 진단하기

아래 상황에서 layer normalization이 왜 필요한지 한 문장으로 써 보십시오.

| 상황 | 가능한 답 | 해설 |
| --- | --- | --- |
| residual 이후 특정 축 값만 지나치게 커졌다 | 다음 계산이 한 축에 과하게 끌리지 않도록 값 기준선을 정리해야 한다 | 값 크기 불균형을 줄이는 관점입니다. |
| 여러 블록을 지나며 표현값 범위가 계속 달라진다 | 반복 블록이 비슷한 입력 기준에서 계산을 이어 가도록 값 범위를 맞춰야 한다 | 깊은 반복 안정화 관점입니다. |
| 한 위치 표현 안의 값들이 너무 좁게 모였다 | 축 사이 차이가 다음 계산에서 읽히도록 퍼짐을 다시 맞춰야 한다 | 너무 큰 값뿐 아니라 너무 좁은 값도 문제로 볼 수 있습니다. |

해설: 이 연습은 수식을 계산하는 문제가 아닙니다. layer normalization이 `정답을 고르는 단계`가 아니라 `다음 계산이 표현을 읽을 수 있게 만드는 조건 정리`라는 점을 말로 확인하는 연습입니다.

## 체크리스트

- layer normalization을 한 위치 표현 안의 값 평균과 퍼짐을 맞추는 장치로 설명할 수 있는가?
- layer normalization과 batch normalization의 기준 차이를 말할 수 있는가?
- residual connection과 layer normalization의 차이를 `정보 흐름 보존`과 `값 기준선 정리`로 구분할 수 있는가?
- layer normalization이 의미 선택이나 토큰 관계 선택을 직접 맡지 않는다는 점을 설명할 수 있는가?

## 출처와 참고 자료

- Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton, `Layer Normalization`, arXiv, 2016, 확인 날짜: 2026-07-19. [https://arxiv.org/abs/1607.06450](https://arxiv.org/abs/1607.06450){: target="_blank" rel="noopener noreferrer" }
- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
