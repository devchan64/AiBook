# P5-14.3 토큰 표현은 Transformer 블록 안에서 어떻게 이동하는가

> Section ID: `P5-14.3`
> Version: `v2026.07.19`

P5-14.2에서는 Transformer 블록의 부품별 역할을 나누어 보았습니다. 이제 같은 흐름을 현재 표현 하나가 실제로 어떻게 지나가는지로 다시 좁혀 봅니다.

Transformer 블록 안에서 현재 토큰 표현은 어떤 단계로 바뀌는가?

초점은 부품 이름 나열보다 `입력 표현 -> 문맥이 섞인 표현 -> 위치별로 가공된 표현 -> 원래 정보가 더해진 표현 -> 정리된 표현`이라는 갱신 흐름입니다.

## 표현 갱신이 다루는 질문

- self-attention 뒤의 표현은 입력 표현과 무엇이 달라지는가?
- feed-forward는 그 표현을 어떻게 다시 바꾸는가?
- residual과 normalization을 거치면 왜 다음 블록으로 넘길 수 있는 표현이 되는가?

## 표현 이동을 단계로 보면

같은 현재 표현 하나를 따라가면 Transformer 블록은 다음처럼 읽을 수 있습니다.

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-representation-update-ko.mmd"
```

이 도식에서 먼저 볼 것은 계산식이 아니라 의미 변화입니다.

| 단계 | 표현에 생기는 변화 |
| --- | --- |
| 입력 표현 | 아직 현재 토큰 자체의 출발 표현에 가깝다 |
| self-attention 이후 | 다른 토큰에서 가져온 문맥이 섞인다 |
| feed-forward 이후 | 현재 위치에서 그 문맥이 다시 가공된다 |
| residual 이후 | 새 계산과 원래 표현이 함께 남는다 |
| normalization 이후 | 다음 블록으로 넘기기 쉬운 범위로 정리된다 |

## 사례 및 예시

### 사례. 조치 확인 단서가 action token 표현을 바꾸는 경우

장애 대응 로그에서 `증상`, `배포 단서`, `조치 상태`가 따로 등장한다고 해 보겠습니다. 현재 관심 위치가 `조치 상태`라면, 그 표현은 단순히 자기 자신만 보고 정해지지 않습니다. rollback이 확인되었는지, 배포 단서가 원인처럼 보이는지, 증상이 아직 남았는지에 따라 현재 조치 표현이 달라집니다.

사람이 먼저 쓰기 쉬운 기준은 `조치 상태 토큰 자체가 무엇을 말하는가`입니다. 하지만 Transformer 블록 관점에서는 그 토큰이 attention으로 어떤 문맥을 섞었고, feed-forward와 residual을 지나 어떤 방향의 표현으로 남았는지가 더 중요합니다.

| 장면 | 현재 표현이 향해야 하는 쪽 | 왜 그런가 |
| --- | --- | --- |
| rollback confirmed | 복구 상태가 더 강한 조치 표현 | 조치 확인 단서가 action token에 강하게 섞이기 때문 |
| rollback not confirmed | 증상/원인 단서가 더 남은 조치 표현 | 조치 확인이 약해져 원인 의심 축이 더 남기 때문 |

| 너무 빠른 판단 | 표현 갱신 관점의 판단 | 확인할 결과 |
| --- | --- | --- |
| action token은 원래 `조치 상태`를 뜻하므로 두 장면에서 비슷하게 남는다 | attention으로 섞이는 단서가 달라지면 같은 action token도 다른 방향으로 이동한다 | `rollback confirmed`와 `rollback not confirmed`의 action token 출력이 서로 달라진다 |

이 사례에서 확인해야 할 결과는 Transformer 블록이 토큰을 한 번 섞고 끝나는 것이 아니라, 현재 위치 표현을 단계적으로 이동시킨다는 점입니다.

## 연습 및 예제

### 예제. action token 표현 이동 따라가기

이번 예제의 목표는 `문맥을 섞는 단계`와 `각 위치 표현을 다시 가공하는 단계`를 실제 운영 문장 장면에 얹어 보는 것입니다.

코드를 읽을 때는 전체 행렬을 한꺼번에 외우려 하지 말고, action token이 다른 단서를 얼마나 참고하는지만 먼저 보십시오.

| 조작할 값 | 관찰할 출력 | 확인할 질문 |
| --- | --- | --- |
| action token 행의 attention 비중 | `contextual tokens`의 action token 행 | 조치 토큰이 자기 자신, 증상, 배포 단서 중 무엇을 더 섞는가 |
| 같은 비중이 feed-forward를 지난 뒤 | `feed-forward output` | 섞인 문맥이 현재 위치 표현 안에서 어떻게 다시 가공되는가 |
| residual 이후 action token | `action token after residual` | 원래 조치 축이 남은 상태에서 최종 블록 출력 방향이 어떻게 달라지는가 |

```python
import numpy as np

tokens = np.array([
    [1.0, 0.2],   # symptom token: urgency high
    [0.8, 0.5],   # deploy clue token: cause evidence medium
    [0.3, 1.0],   # action token: recovery status important
])

attention_cases = {
    "rollback_confirmed": np.array([
        [0.6, 0.3, 0.1],
        [0.2, 0.5, 0.3],
        [0.1, 0.3, 0.6],
    ]),
    "rollback_not_confirmed": np.array([
        [0.6, 0.3, 0.1],
        [0.3, 0.5, 0.2],
        [0.3, 0.5, 0.2],
    ]),
}

ff_weights = np.array([
    [1.1, 0.4],
    [0.2, 1.0],
])

def simple_layer_norm(row):
    mean = np.mean(row)
    std = np.std(row)
    return (row - mean) / (std + 1e-6)

for name, attention_weights in attention_cases.items():
    contextual = attention_weights @ tokens
    ff_output = contextual @ ff_weights
    residual_added = ff_output + tokens
    normalized = np.vstack([simple_layer_norm(row) for row in residual_added])

    print(f"[{name}]")
    print("contextual tokens =")
    print(np.round(contextual, 3))
    print("feed-forward output =")
    print(np.round(ff_output, 3))
    print("after residual =")
    print(np.round(residual_added, 3))
    print("after simple layer norm =")
    print(np.round(normalized, 3))
    print("action token after residual =", np.round(residual_added[2], 3))
    print("---")
```

출력 예시는 다음처럼 읽을 수 있습니다.

```text
[rollback_confirmed]
action token after residual = [1.026 1.978]
---
[rollback_not_confirmed]
action token after residual = [1.238 1.814]
---
```

해설: 두 장면은 같은 입력 토큰에서 시작하지만 attention 가중치가 달라지면서 action token 표현도 다르게 이동합니다. `rollback_confirmed`에서는 복구 상태 축이 더 크게 남고, `rollback_not_confirmed`에서는 증상/원인 축이 상대적으로 더 남습니다. 이 차이는 attention 단계에서 시작되지만 feed-forward와 residual을 거치며 블록 출력으로 남습니다.

![조치 토큰의 단계별 표현 이동](../../../assets/part-05/chapter-14/transformer-block-action-stage-trace-ko.png)

### 연습. action token 행을 바꿔 보기

아래 세 변화는 같은 코드에서 `attention_cases`의 action token 행만 바꾸면 확인할 수 있습니다.

| 바꿔 볼 값 | 예상되는 변화 | 해설 |
| --- | --- | --- |
| `rollback_confirmed`의 action token 행을 `[0.05, 0.15, 0.8]`로 바꾼다 | 복구 상태 축이 더 강하게 남는다 | action token이 자기 자신의 조치 상태를 더 많이 유지하기 때문입니다. |
| `rollback_not_confirmed`의 action token 행을 `[0.45, 0.45, 0.1]`로 바꾼다 | 증상/배포 단서 축이 더 강하게 남는다 | 조치 확인보다 원인 단서 쪽 문맥이 더 많이 섞이기 때문입니다. |
| 두 장면의 action token 행을 같게 만든다 | 두 장면의 action token 출력 차이가 줄어든다 | 현재 절의 핵심은 같은 입력이라도 attention으로 섞는 문맥이 달라지면 표현 이동이 달라진다는 점입니다. |

해설: 이 연습에서 중요한 것은 어느 숫자가 정답인지가 아닙니다. action token이 어떤 문맥을 더 많이 섞는지 바꾸면, 그 차이가 feed-forward와 residual을 지나 블록 출력으로 남는다는 흐름을 확인하는 것입니다.

## 체크리스트

- Transformer 블록을 표현 이동의 흐름으로 설명할 수 있는가?
- `contextual tokens`, `feed-forward output`, `after residual`이 각각 무엇을 보여 주는지 말할 수 있는가?
- 같은 입력이라도 attention 가중치가 달라지면 현재 표현이 달라질 수 있음을 설명할 수 있는가?

## 출처와 참고 자료

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
