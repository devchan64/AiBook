# P5-14.4 RNN 상태 전달과 Transformer 병렬 계산

> Section ID: `P5-14.4`
> Version: `v2026.07.31`

_보조제목: 순차 상태 전달과 토큰 관계 계산은 병렬 처리에서 어떻게 갈라지는가_

P5-14.1부터 P5-14.3까지는 Transformer 블록 안에서 표현을 갱신하는 계산의 역할을 보았습니다. 이제 그 계산이 한 시퀀스 안에서 어떤 순서로 실행되는지 RNN과 비교해야 합니다.

RNN은 왜 순차 상태 전달처럼 느껴지고, Transformer는 왜 토큰 관계 계산과 GPU 병렬 처리에 더 잘 맞는가?

비교 기준은 `Transformer가 더 최신이다` 같은 시간순 인상이 아닙니다. 핵심은 앞 step 상태를 차례로 넘기는 계산과, 한 층 안의 여러 토큰 관계를 큰 행렬 연산으로 묶기 쉬운 계산의 차이입니다.

비교 표를 만들 때도 모델 이름만 나란히 두지 말고 `depends_on_previous_step`, `relation_matrix`, `parallel_unit`, `batch_axis`를 함께 적어 봅니다. 그러면 RNN과 Transformer의 차이가 유행 순서가 아니라 계산 의존성과 병렬화 단위의 차이로 정리됩니다.

## 계산 흐름과 병렬 처리가 다루는 질문

- RNN은 왜 앞 step 상태를 뒤로 넘기는 구조로 읽히는가?
- Transformer는 왜 토큰 관계를 더 한꺼번에 계산하는 구조로 읽히는가?
- 이 차이는 왜 GPU 병렬 처리와 대규모 학습으로 이어지는가?

## RNN은 상태를 차례로 넘긴다

RNN 계열은 각 step가 이전 상태를 이어받아 다음 상태를 만듭니다. 따라서 계산 감각이 자연스럽게 다음처럼 보입니다.

- 첫 토큰을 보고 상태를 만듭니다.
- 그 상태를 가지고 두 번째 토큰을 봅니다.
- 다시 그 상태를 세 번째 토큰으로 넘깁니다.

`RNN은 앞에서 만든 상태를 뒤로 넘겨 가며 순차적으로 계산하는 구조다.`

이 구조는 순서가 중요한 데이터를 다루는 데 자연스럽지만, 병렬 처리 관점에서는 부담이 됩니다. 뒤 step이 앞 step 결과를 기다려야 하면, 계산 장비가 많아도 한 시퀀스 안의 step을 마음대로 동시에 처리하기 어렵습니다.

여기서 주의할 점은 `RNN은 텐서 계산이 아니다`가 아니라는 것입니다. RNN도 입력 벡터, hidden state, 가중치 행렬을 쓰는 텐서 계산입니다. 차이는 텐서 계산을 하느냐가 아니라, 한 시퀀스 안에서 앞 step의 hidden state가 다음 step 계산에 필요하다는 점입니다.

## Transformer는 관계를 한꺼번에 계산하는 쪽에 가깝다

Transformer의 self-attention은 각 토큰이 같은 시퀀스 안 다른 토큰을 함께 참고하게 만듭니다. 그래서 계산 감각은 상태를 한 줄로 넘기는 쪽보다, 토큰들 사이 관계를 큰 행렬 계산으로 함께 다루는 쪽에 가깝습니다.

`RNN은 순서대로 상태를 전달하고, Transformer는 토큰들 사이 관계를 더 한꺼번에 계산한다.`

행렬과 텐서는 먼저 이렇게 잡아도 됩니다. 한 문장 안에서 `토큰 1이 토큰 2를 얼마나 참고하는가`, `토큰 6이 토큰 1을 얼마나 참고하는가` 같은 관계 점수를 표처럼 놓으면 행렬입니다. 그런 관계 점수 표를 배치 안 여러 문장만큼 쌓아 두면 텐서입니다. 따라서 이 절의 구분은 `RNN은 숫자 묶음을 쓰지 않고 Transformer만 텐서를 쓴다`가 아니라, Transformer 쪽이 한 층의 관계 점수 표들을 큰 행렬·텐서 연산으로 묶기 쉽다는 뜻입니다.

이 차이는 짧은 흐름도로 다시 보면 다음처럼 정리됩니다. RNN식 흐름은 앞 상태를 기다리는 계산이고, Transformer식 흐름은 같은 층의 관계 점수를 표와 텐서로 묶는 계산입니다.

```mermaid
--8<-- "assets/part-05/chapter-14/parallel-computation-flow-ko.mmd"
```

이 도식에서 중요한 점은 두 흐름 모두 숫자 묶음을 계산한다는 것입니다. 갈림점은 `텐서를 쓰는가`가 아니라, 시퀀스 안 계산을 앞 step 상태에 묶는가, 같은 층의 관계 점수 묶음으로 조직하는가입니다.

| 관점 | RNN 계열 | Transformer |
| --- | --- | --- |
| 계산 흐름 | 앞 step 결과가 다음 step에 필요하다 | 토큰 관계를 더 한꺼번에 계산한다 |
| 정보 이동 감각 | 상태를 이어 전달한다 | 필요한 위치를 다시 비교한다 |
| 병렬 처리 | 순차 의존성이 병목이 되기 쉽다 | 큰 행렬 연산으로 묶기 쉽다 |
| 규모 확장 | 긴 시퀀스가 많아질수록 순차 부담이 커진다 | 배치와 텐서 계산으로 규모를 키우기 쉽다 |

GPU는 비슷한 계산을 많이 동시에 처리할 때 강합니다. Part 5 앞쪽에서 본 배치(batch)와 텐서(tensor) 계산도 같은 감각입니다. Transformer의 self-attention과 feed-forward는 큰 행렬 연산으로 묶기 쉬워 이런 계산 자원과 잘 맞았습니다.

병렬 처리 설명에서 중요한 관찰값은 `속도가 빨라졌다`가 아니라, 어떤 계산이 기다려야 하고 어떤 계산은 함께 묶을 수 있는가입니다.

다만 이 병렬화 감각은 주로 학습 때 한 층 안의 토큰 관계 계산을 말합니다. 실제 생성 단계에서는 아직 나오지 않은 다음 토큰을 미리 알 수 없으므로, 다음 토큰을 차례로 만드는 순서 제약이 남습니다. 그래서 이 절에서는 `Transformer는 모든 상황에서 순서가 없다`가 아니라 `학습 중 한 층의 관계 계산을 더 크게 묶기 쉽다`로 읽어야 합니다.

| 관찰할 질문 | RNN식 흐름에서 생기는 부담 | Transformer식 흐름에서 보이는 장점 |
| --- | --- | --- |
| 다음 토큰 계산이 앞 step 완료를 기다리는가 | 순차 의존성이 병목이 되기 쉽다 | 한 층 안의 여러 토큰 관계를 함께 계산하기 쉽다 |
| 같은 종류의 곱셈이 많이 반복되는가 | step 단위 반복으로 쪼개져 보이기 쉽다 | 큰 행렬 연산으로 묶어 GPU에 올리기 쉽다 |
| 많은 문장을 한꺼번에 학습할 수 있는가 | 문장 안 순서 의존성이 누적된다 | 대규모 배치와 텐서 계산으로 조직하기 쉽다 |

`Transformer는 토큰 간 관계를 병렬 행렬 연산으로 바꾸기 쉬워서, 대규모 GPU 학습과 잘 맞았다.`

## RNN 상태 전달과 Transformer 병렬 계산: 확인할 판단 기준

이 사례에서는 RNN의 순차 상태 전달과 Transformer의 토큰 관계 계산을 비교하고, 그 차이가 GPU 병렬 처리와 대규모 학습에 왜 유리했는지 설명해야 합니다. Python 예제는 속도 측정이 아니라 순차 trace, 관계 score 행렬, 배치 score 텐서 shape를 비교하는 데 집중해야 하며, 같은 판단을 반복하는 연습은 늘리지 않습니다.

### 사례. 작업 허가 문장과 대량 학습 배치

작업 허가 문장을 줄 단위로 나누어 보겠습니다.

| 줄 | 문서 내용 | 마지막 판단과의 관계 |
| --- | --- | --- |
| 1 | `압력 해소 전에는 라인 3을 재기동하지 않는다.` | 금지 규칙 |
| 2 | `센서 보정은 오전에 완료되었다.` | 중간 운영 로그 |
| 3 | `포장재 보충 작업은 별도 승인되었다.` | 중간 운영 로그 |
| 4 | `현재 압력은 아직 안전 범위로 돌아오지 않았다.` | 현재 상태 |
| 5 | `근무 교대 기록은 갱신되었다.` | 중간 운영 로그 |
| 6 | `지금 라인 3 재기동을 승인해도 되는가?` | 마지막 질문 |

사람이 먼저 쓰기 쉬운 기준은 `문서가 순서대로 쓰였으니 앞에서 뒤로 읽으면 된다`입니다. 하지만 계산 흐름 관점에서는 더 구체적으로 물어야 합니다. 1번 줄의 금지 규칙과 4번 줄의 현재 상태를 6번 줄의 질문과 비교할 때, 계산은 앞 step 결과를 기다리는가, 아니면 같은 층의 여러 관계 계산으로 묶을 수 있는가?

RNN식 상태 전달 감각에서는 앞 단서가 다음 줄 상태로 계속 압축되어 넘어갑니다. 6번 질문을 처리하려면 1번에서 만든 상태가 2번, 3번, 4번, 5번 계산을 거쳐 도착해야 합니다. 따라서 같은 문장 안에서도 뒤 step은 앞 step 계산이 끝나기를 기다리는 구조가 됩니다.

Transformer식 관계 계산 감각에서는 6번 질문 위치와 1번 규칙, 4번 상태 사이의 관계를 같은 층의 attention 계산 안에서 구성할 수 있습니다. 이때 P5-14.4에서 보는 핵심은 `먼 앞 단서를 얼마나 잘 기억하는가`가 아니라, 위치 쌍의 비교를 큰 행렬 연산으로 조직하기 쉽다는 점입니다. 먼 단서가 마지막 판단에서 어떻게 다시 호출되는지는 P5-14.5의 긴 문맥 문제로 넘깁니다.

| 비교 장면 | RNN식 상태 전달로 읽을 때 | Transformer식 관계 계산으로 읽을 때 |
| --- | --- | --- |
| 6번 질문과 1번 금지 규칙 비교 | 2~5번 step을 지나 6번 상태로 전달되어야 한다 | 6번 위치와 1번 위치의 관계 점수로 함께 계산될 수 있다 |
| 6번 질문과 4번 현재 압력 상태 비교 | 5번 step을 거쳐 6번 상태로 전달되어야 한다 | 6번 위치와 4번 위치의 관계 점수로 함께 계산될 수 있다 |
| 배치 안 여러 문장의 위치 관계 비교 | 문장 안 step 의존성이 반복된다 | 문장별 관계 score를 텐서 형태로 함께 조직하기 쉽다 |

이 사례에서 확인해야 할 결과는 `Transformer가 새 모델이라 더 좋다`가 아닙니다. 같은 마지막 질문을 두고도 RNN식 설명은 `앞 step 상태가 끝나야 뒤 step이 시작되는가`를 묻고, Transformer식 설명은 `여러 위치 관계를 같은 층의 행렬 계산으로 묶을 수 있는가`를 묻습니다. 병렬 처리 설명의 핵심은 모델 이름이 아니라 `기다려야 하는 계산이 무엇이고, 함께 묶을 수 있는 계산이 무엇인가`입니다.

## 연습 및 예제

### 예제. 순차 trace와 관계 score 행렬 비교하기

이 예제는 실제 Transformer 구현이 아니라, P5-14.4의 중심 질문을 작은 출력으로 확인하는 실험입니다. 실행 시간 비교가 아니라 `순차 trace는 step 순서로 쌓이고`, `관계 score는 행렬 shape로 한꺼번에 조직된다`는 차이를 봅니다.

| 조작할 값 | 관찰할 출력 | 확인할 질문 |
| --- | --- | --- |
| `line_features`의 줄 순서 | `recurrent trace` | 앞 step 상태가 뒤 step으로 순서대로 전달되는가 |
| `relation_kernel` | `request row`, `top related lines` | 현재 질문이 어떤 앞 줄과 관계 score를 크게 갖는가 |
| `batch`에 넣은 문장 개수 | `score tensor shape` | 여러 문장의 관계 score가 하나의 텐서 계산으로 묶이는가 |

```python
# RNN식 순차 trace와 Transformer식 관계 score 행렬을 비교해 step 순서 누적과 병렬 관계 계산의 차이를 확인하는 예제입니다.
import numpy as np

line_features = np.array([
    [0.0, 1.0, 1.0, 0.0, 0.0],  # rule: pressure + block
    [0.0, 0.0, 0.0, 1.0, 0.0],  # log
    [0.0, 0.0, 0.0, 1.0, 0.0],  # log
    [0.0, 1.0, 0.0, 0.0, 0.0],  # state: pressure
    [0.0, 0.0, 0.0, 1.0, 0.0],  # log
    [1.0, 0.0, 0.0, 0.0, 1.0],  # request: restart + question
])

line_names = [
    "rule",
    "sensor_log",
    "packing_log",
    "pressure_state",
    "shift_log",
    "request",
]

relation_kernel = np.array([
    [1.0, 1.0, 1.0, 0.0, 1.0],
    [0.0, 1.0, 0.3, 0.0, 0.0],
    [0.0, 0.5, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.2, 0.0],
    [1.0, 0.5, 0.5, 0.0, 1.0],
])

state = np.zeros(5)
recurrent_trace = []
for step, (name, features) in enumerate(zip(line_names, line_features), start=1):
    state = 0.55 * state + features
    recurrent_trace.append((step, name, np.round(state, 3)))

relation_scores = line_features @ relation_kernel @ line_features.T
request_scores = relation_scores[-1]
related_to_request = [
    (score, name)
    for score, name in zip(request_scores, line_names)
    if name != "request"
]
ranked = sorted(related_to_request, reverse=True)

batch = np.stack([
    line_features,
    line_features[[0, 2, 4, 3, 1, 5]],
    line_features[[1, 2, 0, 3, 4, 5]],
])
batch_scores = batch @ relation_kernel @ np.transpose(batch, (0, 2, 1))

print("[recurrent trace]")
for step, name, snapshot in recurrent_trace:
    print(f"step {step}: {name:14s} state={snapshot}")

print("
[relation score matrix]")
print("shape =", relation_scores.shape)
print("request row =", np.round(request_scores, 1).tolist())
print("top related lines =", [(name, float(score)) for score, name in ranked[:3]])

print("
[batched relation scores]")
print("batch shape =", batch.shape)
print("score tensor shape =", batch_scores.shape)
```

출력 예시는 다음처럼 읽습니다.

```text
[recurrent trace]
step 1: rule           state=[0. 1. 1. 0. 0.]
step 2: sensor_log     state=[0.   0.55 0.55 1.   0.  ]
...
step 6: request        state=[1.    0.353 0.05  0.808 1.   ]

[relation score matrix]
shape = (6, 6)
request row = [3.0, 0.0, 0.0, 1.5, 0.0, 4.0]
top related lines = [('rule', 3.0), ('pressure_state', 1.5), ('shift_log', 0.0)]

[batched relation scores]
batch shape = (3, 6, 5)
score tensor shape = (3, 6, 6)
```

첫 번째 출력은 RNN식 상태 감각을 보여 줍니다. 6번 request 상태는 1번부터 5번까지의 갱신을 차례로 지난 뒤에야 만들어집니다. 두 번째 출력은 관계 계산 감각을 보여 줍니다. 6개 위치 사이의 관계 score가 `(6, 6)` 행렬로 한 번에 놓이고, request 행에서는 자기 자신을 제외하면 rule과 pressure_state가 크게 잡힙니다. 세 번째 출력의 `(3, 6, 6)`은 문장 3개를 배치로 묶으면 각 문장의 위치 관계 행렬도 텐서 형태로 함께 조직될 수 있음을 보여 줍니다.

값을 바꿔 볼 때는 먼저 `line_features`의 줄 순서를 바꿔 `recurrent trace`의 도착 상태가 달라지는지 봅니다. 그다음 `relation_kernel`에서 pressure나 block 관련 가중치를 낮추면 `top related lines` 순위가 어떻게 바뀌는지 확인합니다. 마지막으로 `batch`에 같은 형식의 문장을 하나 더 추가하면 `score tensor shape`의 첫 번째 숫자가 문장 개수만큼 늘어나는지 볼 수 있습니다.

해설: 이 예제에서 읽어야 할 결과는 `어느 쪽이 실제로 몇 배 빠른가`가 아닙니다. P5-14.4의 핵심은 순차 상태 전달은 step trace로 읽히고, Transformer식 관계 계산은 위치 관계 행렬과 배치 텐서로 읽힌다는 점입니다. 그래서 병렬 처리 설명은 하드웨어 자랑이 아니라 계산 구조의 차이로 닫혀야 합니다.

### 연습. 기다리는 계산과 묶는 계산 표시하기

아래 장면을 보고, 먼저 `기다림`과 `묶음`을 표시해 보십시오.

| 장면 | 표시 | 해설 |
| --- | --- | --- |
| 문장 안 3번째 토큰 계산이 2번째 토큰의 hidden state를 받아야 한다 | 기다림 | 앞 step 결과가 뒤 step에 필요하므로 순차 의존성이 생깁니다. |
| 한 문장 안 모든 토큰 쌍의 attention score를 같은 층에서 계산한다 | 묶음 | 여러 토큰 관계 점수를 행렬 연산으로 구성하기 쉽습니다. |
| 배치 안 여러 문장의 feed-forward 계산을 같은 가중치로 각 위치에 적용한다 | 묶음 | 같은 종류의 위치별 계산을 텐서 연산으로 함께 처리하기 좋습니다. |
| 생성 중 아직 나오지 않은 다음 토큰을 미리 알고 계산해야 한다 | 기다림 | 생성 실행 단계에는 순서 제약이 남습니다. 학습 시 병렬화 감각과 구분해야 합니다. |
| 문서의 앞 규칙을 상태 하나에 압축해 마지막까지 들고 간다 | 기다림에 가까움 | 앞 단서가 여러 step을 지나야 하므로 순차 전달 부담이 커집니다. |

해설: 이 연습은 실제 GPU 커널을 구현하는 문제가 아닙니다. P5-14.4에서 필요한 학습은 `상태를 넘기는 계산`, `관계를 다시 계산하는 흐름`, `한꺼번에 묶을 수 있는 계산`을 구분하는 것입니다.

`기다림`으로 표시한 장면은 뒤 계산이 앞 계산의 결과를 받아야 시작되는 경우입니다. 3번째 토큰이 2번째 hidden state를 기다리거나, 앞 규칙이 여러 step을 지나 마지막 상태까지 전달되어야 하는 장면이 여기에 속합니다. 이런 구조에서는 같은 문장 안의 step을 마음대로 동시에 처리하기 어렵습니다.

`묶음`으로 표시한 장면은 같은 종류의 계산을 표나 텐서 형태로 함께 놓을 수 있는 경우입니다. 한 문장 안 모든 토큰 쌍의 attention score를 행렬로 만들거나, 배치 안 여러 문장의 feed-forward 계산을 같은 가중치로 적용하는 장면이 여기에 속합니다. GPU 병렬 처리는 바로 이런 반복 계산 묶음과 잘 맞습니다.

따라서 이 연습의 결론은 `Transformer가 무조건 빠르다`가 아닙니다. 학습 중 한 층의 관계 계산은 큰 행렬·텐서 연산으로 조직하기 쉽고, RNN식 순차 상태 전달은 앞 step 결과를 기다리는 축이 강하다는 점입니다. 이 구분이 있어야 Transformer의 병렬 처리 장점을 단순 속도 인상이 아니라 계산 구조 변화로 설명할 수 있습니다.

## 체크리스트

- RNN을 순차 상태 전달 구조로 설명할 수 있는가?
- Transformer를 토큰 관계 계산 구조로 설명할 수 있는가?
- Transformer가 병렬 처리에 잘 맞는 이유를 큰 행렬 연산 관점으로 설명할 수 있는가?
- RNN의 순차 의존성과 Transformer의 관계 계산을 병렬 처리 관점에서 비교할 수 있는가?

## 출처와 참고 자료

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
