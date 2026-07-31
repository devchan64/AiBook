# P5-14.6 보충학습: 위치별 표현 가공

> Section ID: `P5-14.6`
> Version: `v2026.07.31`

_보조제목: feed-forward network는 attention 뒤에서 각 위치 표현을 어떻게 다시 가공하는가_

P5-14.2에서는 Transformer 블록 안에서 feed-forward network가 self-attention과 다른 일을 맡는다고 보았습니다. 그런데 `attention이 이미 문맥을 섞었는데 왜 또 feed-forward가 필요한가?`라는 질문이 남습니다.

Transformer 블록에서 feed-forward network는 새로 참고할 토큰을 고르는 장치가 아니라, attention으로 문맥이 섞인 각 위치 표현을 다시 가공하는 장치입니다.

용어가 다시 흩어질 때는 개념사전의 [피드포워드 네트워크(feed-forward network)](../../../reference/concept-glossary-parts/12-tieut.md#transformer) 항목과 P5-14.2의 네 부품 역할 분담을 함께 다시 보면 좋습니다.

## attention 뒤에 왜 한 번 더 가공하는가

self-attention은 현재 위치가 다른 위치에서 어떤 정보를 가져올지 정합니다. 하지만 `무엇을 참고했는가`와 `그 참고 결과를 현재 위치의 다음 표현으로 어떻게 바꿀 것인가`는 같은 질문이 아닙니다.

예를 들어 `압력 미해소 상태에서는 재기동을 보류한다`에서 `재기동` 위치가 `압력 미해소`와 `보류`를 attention으로 함께 보았다고 해 보겠습니다. 이때 attention은 관계를 섞어 주지만, 그 결과를 `단순 조치`, `조건부 조치`, `차단 대상 조치` 가운데 어느 방향으로 더 선명하게 가공할지는 별도의 변환이 필요합니다. Transformer 블록에서 그 역할을 맡는 쪽이 feed-forward network입니다.

짧게 나누면 다음과 같습니다.

| 질문 | 더 직접 맡는 부품 | 이유 |
| --- | --- | --- |
| 현재 위치가 어떤 다른 위치를 참고해야 하는가 | self-attention | 토큰 사이 관계를 읽기 때문입니다. |
| 참고한 문맥이 섞인 현재 표현을 어떻게 바꿀까 | feed-forward network | 같은 위치 안의 표현을 다시 비선형적으로 가공하기 때문입니다. |

## 같은 FFN을 여러 위치에 적용한다는 뜻

Transformer의 feed-forward network는 보통 각 위치에 같은 가중치를 적용합니다. 여기서 `같다`는 말은 모든 위치가 같은 출력이 된다는 뜻이 아닙니다. 입력 표현이 위치마다 다르면, 같은 변환을 지나도 출력은 달라집니다.

```mermaid
--8<-- "assets/part-05/chapter-14/feed-forward-position-update-ko.mmd"
```

이 도식에서 점선은 같은 가중치가 여러 위치에 공유된다는 뜻이고, 실선은 각 위치 표현이 자기 위치 안에서 따로 가공된다는 뜻입니다. 따라서 feed-forward network는 순서를 따라 상태를 넘기는 장치도 아니고, 새로 참고할 위치를 고르는 장치도 아닙니다. 이미 문맥이 섞인 각 위치 표현을 같은 규칙으로 다시 변환하는 장치입니다.

같은 FFN을 쓴다고 해서 모든 토큰을 같은 의미로 만드는 것이 아닙니다. `서로 다른 입력 표현을 같은 가공 기준으로 통과시킨다`고 읽어야 합니다.

## 비선형 가공이 필요한 이유

feed-forward network를 단순한 숫자 후처리로 읽으면 Transformer 블록의 절반이 사라집니다. attention이 문맥을 섞은 뒤에도 표현은 아직 여러 단서가 한데 들어온 상태입니다. feed-forward network는 그 섞인 표현을 현재 위치의 다음 표현으로 더 분리하고 압축합니다.

| attention 뒤 표현에 남은 상태 | feed-forward가 돕는 일 |
| --- | --- |
| 여러 단서가 섞여 있지만 아직 현재 위치 의미가 흐릿하다 | 현재 위치 안에서 의미 축을 더 선명하게 가공한다 |
| 단순 선형 결합만으로는 조건, 부정, 예외 같은 차이가 약하게 남을 수 있다 | 비선형 변환으로 단서 조합의 차이를 더 잘 드러낸다 |
| 각 위치가 서로 다른 문맥을 섞어 받았다 | 같은 FFN을 적용하되 위치마다 다른 출력 표현을 만든다 |

여기서 `비선형`이라는 말은 당장 수식을 외우라는 뜻이 아닙니다. 입문 단계에서는 `단순히 더하고 평균낸 표현을, 다음 블록이 쓸 수 있는 더 구분된 표현으로 바꾸는 과정`으로 읽으면 충분합니다. 아래 예제의 `relu`도 이 감각만 보면 됩니다. 선형 계산으로 나온 값 중 0보다 작은 축을 접어 두면, 같은 입력 변화라도 출력 방향이 단순한 더하기와 다르게 꺾일 수 있습니다.

## 위치별 표현 가공: 확인할 판단 기준

이 사례에서는 feed-forward network가 attention 뒤에서 위치별 표현 가공을 맡는다는 점을 보충해야 합니다. Python 예제는 같은 FFN 가중치를 여러 위치에 공유 적용해도 입력 표현 차이에 따라 hidden/output이 달라지는 점을 보여 주는지 확인한다.

### 사례. 작업 허가 문장에서 조치 표현을 가공하는 경우

작업 허가 문장에서 `재기동`이라는 단어만 보면 사람은 먼저 `라인을 다시 켠다`는 행동을 떠올립니다. 하지만 문장 안에 `압력 미해소`와 `보류`가 함께 있으면, 현재 위치의 표현은 단순 행동명이 아니라 `조건이 붙어 차단되어야 하는 조치` 쪽으로 바뀌어야 합니다.

self-attention은 `재기동`이 `압력 미해소`와 `보류`를 함께 보게 만듭니다. feed-forward network는 그 섞인 표현을 현재 위치 안에서 다시 가공해, `재기동` 표현이 단순 실행 요청이 아니라 조건부 차단 조치에 가깝게 남도록 돕습니다.

| 사람이 먼저 보기 쉬운 표현 | attention 뒤에 섞인 문맥 | feed-forward 뒤에 더 선명해져야 하는 표현 |
| --- | --- | --- |
| `재기동`은 실행 행동이다 | `압력 미해소`, `보류`가 함께 섞인다 | `조건이 붙은 차단 대상 조치` |
| `승인`은 허용 신호다 | `검증 미완료`, `예외 없음`이 함께 섞인다 | `아직 확정 승인 아님` |
| `배포`는 작업 진행이다 | `rollback not confirmed`, `증상 지속`이 함께 섞인다 | `복구 확인 전 진행 위험` |

이 사례에서 확인해야 할 결과는 feed-forward network가 새로운 근거 위치를 찾는 것이 아니라, 이미 attention으로 들어온 근거를 현재 위치 표현 안에서 더 구분된 의미로 가공한다는 점입니다.

## 연습 및 예제

### 예제. 같은 FFN을 지나도 위치마다 출력이 달라지는지 확인하기

이 예제는 실제 Transformer 구현이 아니라, feed-forward network의 위치별 가공 감각을 확인하는 작은 실험입니다. attention 뒤에 이미 문맥이 섞인 세 위치 표현이 있고, 같은 FFN 가중치를 각 위치에 똑같이 적용한다고 가정합니다.

| 조작할 값 | 관찰할 출력 | 확인할 질문 |
| --- | --- | --- |
| `positions`의 각 행 | `hidden`, `output` | 같은 FFN을 지나도 위치별 출력이 달라지는가 |
| `restart` 위치의 입력값 | `restart before/after` | 현재 위치 표현이 바뀌면 같은 FFN도 다른 방향으로 가공하는가 |
| `changed[1]`만 바꾸기 | `other positions unchanged` | 한 위치의 FFN 계산이 다른 위치를 새로 참고하지 않는가 |

```python
# 같은 feed-forward network를 위치별 표현에 공유 적용해도 각 위치의 hidden과 output이 어떻게 다르게 가공되는지 확인하는 예제입니다.
import numpy as np

output_axes = ["action_axis", "block_axis"]

positions = np.array([
    [0.2, 0.1, 0.9, 0.1],  # pressure_state: condition signal high
    [0.8, 0.2, 0.2, 0.1],  # restart: action signal high
    [0.3, 0.9, 0.2, 0.7],  # hold: block/negation signal high
])

position_names = ["pressure_state", "restart", "hold"]

w1 = np.array([
    [1.0, -0.2, 0.8],
    [0.3, 1.2, -0.6],
    [0.8, 0.1, 0.5],
    [-0.4, 0.7, 1.0],
])
b1 = np.array([-0.2, -0.1, 0.0])
w2 = np.array([
    [0.9, 0.2],
    [-0.3, 1.0],
    [0.4, 0.8],
])

def relu(x):
    return np.maximum(x, 0.0)

def ffn(x):
    hidden = relu(x @ w1 + b1)
    output = hidden @ w2
    return hidden, output

hidden, output = ffn(positions)

print("[same FFN, different positions]")
print("output axes =", output_axes)
for name, before, h, after in zip(position_names, positions, hidden, output):
    print(f"{name:15s} input={np.round(before, 2)} hidden={np.round(h, 2)} output={np.round(after, 2)}")

changed = positions.copy()
changed[1] += np.array([0.0, 0.5, 0.0, 0.4])
_, changed_output = ffn(changed)

print("
[change only restart position]")
print("restart before/after =", np.round(output[1], 2), "->", np.round(changed_output[1], 2))
print("other positions unchanged =", np.allclose(output[[0, 2]], changed_output[[0, 2]]))
```

출력 예시는 다음처럼 읽습니다.

```text
[same FFN, different positions]
output axes = ['action_axis', 'block_axis']
pressure_state  input=[0.2 0.1 0.9 0.1] hidden=[0.71 0.14 0.65] output=[0.86 0.8 ]
restart         input=[0.8 0.2 0.2 0.1] hidden=[0.78 0.07 0.72] output=[0.97 0.8 ]
hold            input=[0.3 0.9 0.2 0.7] hidden=[0.25 1.43 0.5 ] output=[-0.    1.88]

[change only restart position]
restart before/after = [0.97 0.8 ] -> [0.74 1.76]
other positions unchanged = True
```

첫 번째 출력은 같은 FFN을 적용해도 위치마다 입력 표현이 다르면 hidden과 output이 달라진다는 점을 보여 줍니다. 여기서 `output`의 첫 번째 값은 `action_axis`, 두 번째 값은 `block_axis`로 읽습니다. 예를 들어 `hold` 위치는 `block_axis`가 더 크게 남고, `restart` 위치에 보류 단서를 더 섞으면 두 번째 출력에서 `block_axis`가 `0.8`에서 `1.76`으로 커집니다. 두 번째 출력은 `restart` 위치의 입력만 바꾸면 그 위치의 출력만 바뀌고, 다른 위치 출력은 그대로 남는다는 점도 보여 줍니다.

해설: 이 예제에서 읽어야 할 결과는 feed-forward network가 새 토큰을 고르는 장치가 아니라는 점입니다. 다른 위치를 참고하는 일은 이미 attention 단계에서 일어났고, FFN은 각 위치에 들어온 표현을 같은 가공 기준으로 통과시킵니다. 그래서 같은 FFN이 공유되어도 위치마다 출력이 달라질 수 있습니다.

### 연습. 현재 위치 표현을 말로 바꾸기

아래 장면에서 attention 뒤에 문맥이 섞였다고 가정하고, feed-forward 뒤에 현재 위치 표현이 어느 방향으로 가공되어야 할지 말로 써 보십시오.

| 현재 위치 | attention으로 함께 섞인 단서 | feed-forward 뒤 표현 방향 | 해설 |
| --- | --- | --- | --- |
| `재기동` | `압력 미해소`, `보류` | 조건부 차단 조치 | 행동 자체보다 안전 조건 때문에 막혀야 하는 조치로 읽어야 합니다. |
| `승인` | `검증 미완료`, `예외 없음` | 확정 승인 전 보류 상태 | 승인 단어만 보지 않고 미완료 조건을 현재 표현 안에 반영해야 합니다. |
| `배포` | `rollback not confirmed`, `증상 지속` | 복구 확인 전 위험 작업 | 배포가 단순 진행이 아니라 위험을 남긴 작업으로 가공되어야 합니다. |

해설: 좋은 답은 멋진 용어가 아니라 `현재 위치 표현이 어떤 방향으로 바뀌어야 하는가`를 말로 분명히 쓰는 것입니다. 먼저 현재 위치의 단어만 따로 보면 어떤 기본 의미가 떠오르는지 적습니다. 그다음 attention 뒤에 어떤 단서가 함께 들어왔는지 붙입니다. 마지막으로 그 단서들이 들어왔기 때문에 현재 위치 표현이 어떤 쪽으로 더 선명해져야 하는지 씁니다.

예를 들어 `재기동`만 보면 기본 의미는 `라인을 다시 켜는 실행 행동`입니다. 그런데 attention 뒤에는 `압력 미해소`와 `보류`라는 단서가 함께 들어와 있습니다. 그러면 feed-forward 뒤의 표현 방향은 단순 실행 행동이 아니라 `안전 조건 때문에 막혀야 하는 조치`가 됩니다. 즉 답은 `재기동은 실행 행동처럼 보이지만, 압력이 아직 해소되지 않았고 보류 단서가 함께 있으므로, 현재 위치 표현은 조건부 차단 조치 쪽으로 가공되어야 한다`처럼 쓸 수 있습니다.

이렇게 쓰면 P5-14.2의 표현 이동 예제에서 `feed-forward output`을 단순 중간 숫자로 읽지 않게 됩니다. 출력 숫자는 이름표가 없는 계산 찌꺼기가 아니라, 현재 위치 표현이 어떤 의미 방향으로 더 정리되었는지를 보여 주는 흔적으로 읽어야 합니다.

## 체크리스트

- feed-forward network를 attention 뒤의 단순 후처리가 아니라 위치별 표현 가공으로 설명할 수 있는가?
- 같은 FFN을 여러 위치에 적용해도 입력 표현이 다르면 출력 표현이 달라진다는 점을 설명할 수 있는가?
- self-attention의 `관계 읽기`와 feed-forward network의 `위치 안 변환`을 구분할 수 있는가?

## 출처와 참고 자료

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
