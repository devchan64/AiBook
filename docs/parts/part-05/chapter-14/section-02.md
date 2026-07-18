# P5-14.2 병렬 처리와 긴 문맥

Section ID: `P5-14.2`
Version: `v2026.07.17`

P5-14.1에서는 트랜스포머(Transformer)를 셀프 어텐션(self-attention), feed-forward, residual connection, layer normalization의 조합으로 설명했습니다. 이제 다음 질문이 남습니다.

왜 트랜스포머는 RNN보다 병렬 처리에 더 잘 맞고, 긴 문맥(long context) 문제에서도 더 강한 전환점처럼 보였는가?

트랜스포머는 토큰을 순서대로만 상태 전달하지 않고 서로의 관계를 한 번에 계산하는 구조에 더 가까워, 병렬 처리와 긴 문맥 참조에서 큰 장점을 드러냈다.

계산 감각의 기준선을 다시 짧게 잡아야 할 때는 개념사전의 [트랜스포머(Transformer)](../../../reference/concept-glossary.md#transformer), [셀프 어텐션(self-attention)](../../../reference/concept-glossary.md#self-attention), [병렬 처리(parallel processing)](../../../reference/concept-glossary.md#parallel-processing) 항목을 함께 다시 보는 편이 좋습니다.

## 이 절의 범위

- RNN과 트랜스포머의 계산 흐름은 왜 다르게 느껴지는가?
- 병렬 처리 관점에서 트랜스포머가 왜 유리했는가?
- 긴 문맥을 다룰 때 self-attention은 어떤 직관적 장점을 주는가?
- 이 차이가 왜 대규모 생성 모델 시대로 연결되는가?

이 절에서 먼저 닫아야 하는 핵심은 `Transformer는 더 좋은 이름의 모델이 아니라, 순차 전달을 관계 계산으로 바꿔 GPU 병렬 처리와 긴 문맥 재참조를 동시에 밀어 올린 구조`라는 점입니다.

KV cache, sparse attention, long-context를 처음 읽는 법은 P6-3.3 보충학습에서 다시 설명합니다. 즉, 여기서는 `순차 상태 전달`보다 `토큰 관계를 한꺼번에 계산하는 구조`가 왜 병렬 처리와 먼 문맥 재참조에 유리했는가를 먼저 닫습니다.

여기서 끝내야 하는 설명도 하나입니다. `Transformer가 빠르다`는 인상만 남기는 것이 아니라, 왜 `순차 상태 전달`보다 `토큰 관계를 한꺼번에 계산하는 구조`가 병렬 처리와 먼 문맥 재참조에 유리했는지를 현재 절 안에서 이해해야 합니다. residual, normalization 같은 블록 내부 부품 설명은 앞 절 범위로 두고, 여기서는 계산 감각 차이에 집중합니다.

이 절에서는 `RNN 대 Transformer`를 수학적으로 완전히 비교하기보다, 큰 구조 차이를 먼저 이해합니다.

## 이 절의 목표

- RNN과 Transformer의 계산 흐름 차이를 설명할 수 있습니다.
- Transformer가 왜 병렬 처리와 더 잘 맞는지 말할 수 있습니다.
- 긴 문맥 참조에서 self-attention의 장점을 직관적으로 설명할 수 있습니다.
- 이 차이가 왜 대규모 생성 모델 학습과 이어지는지 연결할 수 있습니다.

## 이 절을 읽는 순서

이 절은 RNN의 순차 전달과 Transformer의 관계 계산을 대비한 뒤, 그 차이가 병렬 처리와 긴 문맥 문제에 어떻게 이어지는지 설명합니다.

1. 먼저 RNN의 순차 전달과 Transformer의 관계 계산을 나란히 놓고 봅니다.
2. 그 다음 왜 이 차이가 GPU 병렬 처리와 연결되는지 읽습니다.
3. 이어서 긴 문맥에서 먼 위치를 다시 참고하는 감각 차이를 확인합니다.
4. 마지막에 왜 이 구조 차이가 현대 생성 모델의 기반이 되었는지 정리합니다.

## Transformer는 왜 다르게 보이나

Transformer의 self-attention은 각 토큰이 같은 시퀀스 안 다른 토큰들을 함께 참고하게 만듭니다. 이 구조는 토큰 간 관련도를 더 행렬적인 계산으로 다루기 쉽습니다.

즉:

- 꼭 한 토큰씩 순서대로만 상태를 넘기지 않아도 되고
- 토큰들 사이 관계를 한 번에 계산하는 감각이 더 강합니다

`RNN은 순서대로 상태를 전달하고, Transformer는 토큰들 사이의 관계를 더 한꺼번에 계산한다.`

P5-14.1이 `Transformer 블록 안에 무엇이 들어 있나`를 설명하는 절이었다면, 이 절은 `그 블록 구조가 실제 계산 방식과 학습 규모에서 무엇을 바꾸었나`를 설명하는 절입니다.

## RNN은 왜 순차적 느낌이 강한가

RNN 계열은 각 step가 이전 상태를 이어받아 다음 상태를 만드는 구조였습니다. 따라서 계산 감각이 자연스럽게 다음처럼 보입니다.

- 첫 토큰을 보고 상태를 만듭니다
- 그 상태를 가지고 두 번째 토큰을 봅니다
- 다시 그 상태를 세 번째 토큰으로 넘깁니다

즉, 토큰을 차례대로 밀어 가는 흐름에 가깝습니다.

핵심은 RNN이 앞에서 만든 상태를 뒤로 넘기며 계산을 이어 가는 구조라는 점입니다.

`RNN은 앞에서 만든 상태를 뒤로 넘겨 가며 순차적으로 계산하는 구조다.`

## 왜 이것이 병렬 처리에 유리했나

Part 5에서 이미 본 것처럼 GPU는 비슷한 계산을 많이 동시에 처리할 때 강합니다. Transformer의 self-attention과 큰 행렬 연산은 이런 구조와 잘 맞습니다.

즉, Transformer는:

- 토큰 간 관련도 계산을 텐서 연산으로 묶기 쉽고
- 배치(batch) 단위로도 잘 확장되며
- 대규모 병렬 학습에 잘 맞는 방향을 보여 주었습니다

핵심은 Transformer가 토큰 간 관계 계산을 병렬 행렬 연산으로 재구성해, 대규모 GPU 학습과 잘 맞게 만들었다는 점입니다.

`Transformer는 토큰 간 관계를 병렬 행렬 연산으로 바꾸기 쉬워서, 대규모 GPU 학습과 잘 맞았다.`

여기서 독자가 꼭 잡아야 할 핵심은 `Transformer가 더 똑똑한 규칙을 하나 더 붙였다`가 아니라, `계산 자체를 GPU가 잘하는 형태로 재구성했다`는 점입니다. 즉, 이 절의 질문은 `블록 안에 무슨 부품이 있나`가 아니라 `그 블록을 반복할 때 계산 흐름이 왜 달라졌나`입니다.

이 차이를 입문용으로 더 짧게 보면 다음과 같습니다.

| 관점 | RNN 계열 | Transformer |
| --- | --- | --- |
| 계산 흐름 | 앞 step 결과가 다음 step에 필요하다 | 토큰 관계를 더 한꺼번에 계산한다 |
| GPU와의 궁합 | 순차 의존성이 강하다 | 큰 행렬 연산으로 묶기 쉽다 |
| 먼 문맥 참조 | 상태 전달에 크게 의존한다 | 필요한 위치를 더 직접 본다 |

## 긴 문맥에서는 왜 유리했나

RNN에서는 아주 먼 정보가 현재까지 오려면 상태를 여러 step 거쳐 전달해야 합니다. 반면 self-attention에서는 현재 토큰이 멀리 떨어진 토큰도 더 직접 참고할 수 있습니다.

즉, 긴 문맥에서의 장점은 먼 위치 정보를 중간 상태에만 의존하지 않고 현재 위치에서 더 직접 다시 참고할 수 있다는 점입니다.

- 먼 위치 정보를 중간 상태에만 희미하게 보관하지 않아도 되고
- 현재 위치가 필요할 때 관련 위치를 더 직접 참고할 수 있습니다

이 때문에 긴 문맥을 읽는 문제에서 Transformer는 강한 전환점을 만들었습니다.

즉, 이 절에서 읽어야 할 변화는 `먼 정보를 오래 기억해야 한다`에서 `먼 정보를 지금 다시 찾아올 수 있다`로 계산 감각이 옮겨 갔다는 점입니다.

## 이를 아주 단순하게 그리면

```mermaid
--8<-- "assets/part-05/chapter-14/long-context-direct-reference-ko.mmd"
```

이 도식은 RNN식 순차 전달과, self-attention이 주는 더 직접적인 참조 감각을 함께 상징합니다.

같은 긴 문맥 요청 하나를 두 계산 경로로만 다시 비교하면 다음처럼 볼 수 있습니다.

```mermaid
--8<-- "assets/part-05/chapter-14/sequential-vs-direct-baseline-ko.mmd"
```

이 비교 도식에서 먼저 붙잡아야 할 점은 다음과 같습니다.

- 순차 전달 쪽은 앞 규칙을 중간 상태에 계속 실어 나르며 마지막 요청까지 가져가야 합니다.
- 직접 참조 쪽은 현재 요청 위치가 필요한 앞 규칙과 상태 줄을 다시 바로 끌어옵니다.
- 그래서 차이는 `먼 단서를 다시 본다`는 결과만이 아니라, `그 단서에 도달하는 계산 경로` 자체가 다르다는 데 있습니다.

## 사례 및 예시

아래 도식은 이 절의 세 사례를 `순차 전달 중심 읽기`와 `직접 참조 중심 읽기`의 차이로 다시 묶은 것입니다.

```mermaid
--8<-- "assets/part-05/chapter-14/long-context-task-flow-ko.mmd"
```

이 도식은 과업이 달라도 문제의 핵심이 비슷하다는 점을 보여 줍니다. 모두 `먼 앞쪽 단서를 현재 위치에서 다시 끌어와야 한다`는 문제를 갖고 있고, Transformer는 그 문제를 더 직접 참조하는 방식으로 다룹니다.

같은 문제를 두 감각으로 나눠 보면 차이가 더 직접 보입니다. 여기서는 `무엇을 다시 참고하는가`뿐 아니라, `지금 위치가 그 단서를 다시 읽을 때 계산을 한 줄씩 밀어 가는가, 아니면 여러 위치 관계를 한꺼번에 다루는가`도 같이 봐야 합니다.

| 같은 장면 | 순차 전달 중심으로 먼저 읽을 때 생기기 쉬운 일 | 직접 참조 중심으로 읽을 때 먼저 기대하는 일 |
| --- | --- | --- |
| 긴 작업 허가 질의응답 | 앞부분 금지 조건과 예외 조항이 뒤 질문으로 갈수록 흐려질 수 있다 | 현재 답변 위치가 앞 단서를 다시 확인해 안전 판단을 바로잡는다 |
| 긴 교대 인수인계 위험 판단 | 초반 경보와 중간 점검 근거를 잃고 마지막 상태 보고에만 기대기 쉽다 | 현재 판단 위치가 필요한 앞 로그와 중간 점검 근거를 다시 끌어온다 |
| 긴 설정 파일 검토 | 현재 줄 근처 정보만 보다가 먼 앞 정의와 제한 규칙을 놓치기 쉽다 | 현재 위치가 앞쪽 정의와 제약을 다시 참조해 설정 일관성을 유지한다 |

### 대표 사례. 긴 작업 허가 질의응답

긴 작업 허가 문서를 읽은 뒤 마지막 줄에서 `지금 라인 3 재기동을 승인해도 되는가?`를 다시 묻는 상황을 떠올려 보겠습니다. 앞부분에는 `압력 해소가 확인되기 전에는 재기동을 시작하지 않는다`, `인터록 해제 전에는 밸브를 열지 않는다` 같은 조건이 이미 나와 있지만, 질문 시점에서는 마지막 몇 줄만 다시 보고 답하고 싶어지기 쉽습니다. 순차 전달 구조라면 이런 조건을 앞에서 뒤로 계속 들고 와야 하므로, 문서가 길어질수록 핵심 금지 조건이 약해질 수 있습니다. 반면 Transformer 계열은 현재 질문 위치가 문서 앞의 금지 조건과 예외 조항을 다시 직접 참고할 수 있어, `지금 답해야 하는 위치`와 `앞 규칙 위치`를 더 자연스럽게 연결합니다. 이때 병렬 계산 감각도 같이 중요합니다. 각 토큰 관계를 큰 행렬 연산으로 함께 다루기 때문에, 질문 위치가 앞 조건 하나씩을 순서대로 더듬어 가기보다 여러 관련 위치를 한꺼번에 계산 안으로 끌어들이기 쉽습니다.
그래서 이 사례에서 확인해야 할 결과는 현재 답변 위치가 바로 앞 문장만 따라가지 않고, 앞쪽 금지 조건과 예외 조항을 실제로 다시 참고해 재기동 허가를 더 안전하게 판단하는가입니다.

같은 관점은 긴 교대 인수인계 위험 판단이나 긴 설정 파일 검토에도 그대로 이어집니다. 다만 이 절에서 붙잡을 핵심은 도메인 이름이 아니라, `현재 위치가 먼 앞 단서를 직접 다시 참고하고 그 비교를 병렬 관계 계산으로 함께 다루는가`입니다.

| 사람이 먼저 보기 쉬운 기준 | 병렬 처리·직접 재참조 관점으로 다시 읽는 기준 |
| --- | --- |
| 앞에서 읽은 정보는 상태에만 남겨 두면 충분하다고 느끼기 쉽다 | 중간 문맥이 길어질수록 상태 하나만으로는 약해질 수 있으므로 현재 위치가 필요한 앞 단서를 다시 찾아와야 한다 |
| Transformer가 빠르다는 말만 들으면 그냥 새 모델이 더 좋다고 느끼기 쉽다 | 핵심은 계산을 `순차 전달`에서 `관계 계산`으로 바꿔 GPU 병렬 처리와 긴 문맥 재참조를 함께 밀어 올렸다는 점이다 |
| 긴 문맥 문제는 메모리 크기만 늘리면 해결된다고 느끼기 쉽다 | 실제로는 먼 단서를 현재 위치에서 다시 집어오는 구조가 있어야 해석 안정성이 올라간다 |

세 사례를 읽은 뒤에는 다음 세 줄로 다시 말할 수 있으면 충분합니다. `먼 단서를 상태에만 남기면 중간에 흐려질 수 있다. 현재 위치가 필요한 앞 단서를 다시 참조하면 해석이 더 안정된다. Transformer는 이 재참조를 병렬 계산과 함께 밀어 올린 구조다.`

즉, 이 절의 마무리는 `나중에 long context를 다시 본다`가 아닙니다. 현재 절 안에서 이미 `먼 앞 단서를 상태에만 남겨 두는 방식`과 `현재 위치가 그 단서를 다시 직접 참조하는 방식`의 차이를 독자가 말할 수 있어야 하고, 다음 Part는 그 구조가 생성 모델 본문에서 어떻게 쓰이는지로만 이어지면 충분합니다.

여기서 한 번 멈추고, `언제 블록 내부 부품 설명보다 병렬 처리와 긴 문맥 계산 감각을 먼저 떠올려야 하는가`를 짧게 고정해 두면 Part 5 후반 구조 전환이 더 분명해집니다.

| 먼저 떠올릴 질문 | 병렬 처리·긴 문맥 관점이 먼저 필요한 이유 | 뒤 Part에서 이어질 것 |
| --- | --- | --- |
| 왜 Transformer가 GPU 시대 대규모 학습과 강하게 연결되는가 | 토큰 관계 계산을 큰 행렬 연산으로 묶어 병렬 처리하기 쉽기 때문 | 생성 모델 규모 확장과 추론 비용 |
| 왜 먼 앞 단서를 다시 읽는 감각이 중요해졌는가 | 순차 상태 전달보다 현재 위치가 필요한 단서를 직접 재참조하는 쪽이 긴 문맥에서 더 자연스럽기 때문 | long context 운용, KV cache, 문맥 관리 |
| 왜 RNN 대비가 단순 구형/신형 비교가 아닌가 | 계산 흐름 자체가 `상태 전달`에서 `관계 계산`으로 바뀌었기 때문 | 이후 LLM 구조와 학습 파이프라인 이해 |

## 연습 및 예제

이번 예제의 목표는 긴 입력에서 `앞 규칙을 순차 상태 하나에 압축해 들고 가는 방식`과 `현재 질문이 필요한 앞 문장을 다시 직접 참고하는 방식`이 어떻게 다르게 보이는지 확인하는 것입니다.

예제를 읽기 전에, 이번 절에서 실제로 먼저 확인해야 할 최소 포인트를 고정하면 다음과 같습니다.

| 확인 포인트 | 예제에서 바로 볼 값 | 왜 중요한가 |
| --- | --- | --- |
| 순차 상태가 어디서 약해지는가 | `history`, `final_state`, `sequential_support` | 앞 단서를 상태 하나로 넘길 때 중간 로그가 길어지면 핵심 규칙이 얼마나 빨리 흐려지는지 보여 준다 |
| 직접 참조가 무엇을 다시 집어오는가 | `top_matches` | 현재 요청이 필요한 앞 문장을 다시 고르는 구조가 어떤 줄을 근거로 삼는지 눈으로 확인하게 한다 |
| 두 구조가 최종 판단에서 어떻게 갈라지는가 | `sequential_decision`과 `direct_decision` | `상태 전달`과 `직접 재참조`가 같은 문맥에서도 다른 결론으로 이어질 수 있음을 드러낸다 |

입력:

- 앞쪽 규칙 문장, 중간 운영 로그, 마지막 운영 요청이 섞인 긴 문맥
- 규칙 단서를 점점 잊어 가는 단순 sequential 상태
- 마지막 질문이 관련 문장을 다시 찾는 direct reference 점수

출력:

- 각 줄을 읽을 때 갱신되는 sequential 상태
- 마지막 요청 시점의 핵심 단서 최소값
- 마지막 요청이 어떤 앞 문장을 다시 참고했는지
- 두 방식이 내리는 최종 판단

문제 상황:

- 긴 문맥 처리에서는 순차 상태만으로 충분한지, 아니면 앞 단서를 직접 다시 찾는 구조가 필요한지 비교해 볼 필요가 있다

확인할 개념:

- Transformer식 직접 참조는 먼 위치 단서를 다시 읽는 데 강점을 보일 수 있다
- 순차 상태와 직접 참조 판단을 나란히 보면 구조 차이가 더 명확해진다

코드를 보기 전에, 순차 상태와 직접 재참조가 어디서 먼저 갈라질지 예상해 보면 좋습니다.

| 비교 포인트 | 순차 상태에서 먼저 예상할 결과 | 직접 재참조에서 먼저 예상할 결과 |
| --- | --- | --- |
| `sequential_support` / `direct_decision` | 중간 로그를 거치며 규칙 단서가 점차 약해질 수 있다 | 마지막 요청 시점에 필요한 규칙 줄과 대상 줄을 다시 집어올 수 있다 |
| `history` / `top_matches` | 앞 규칙이 뒤로 갈수록 흐릿해지는 과정이 보일 것이다 | 요청과 직접 맞닿는 줄이 상위 근거로 다시 떠오를 것이다 |
| 최종 판단 | `uncertain`처럼 흐려질 수 있다 | `block_restart`처럼 규칙을 더 직접 유지할 수 있다 |

이 예제에서 독자가 실제로 봐야 하는 차이도 여기서 끝나지 않습니다. 같은 요청을 받았을 때 순차 상태 쪽은 `규칙을 충분히 확신하지 못해 보류 또는 재확인`으로 기울 수 있고, 직접 재참조 쪽은 `앞 규칙과 대상 정보를 다시 묶어 즉시 차단`으로 기울 수 있어야 합니다. 즉, 계산 차이는 결국 `무슨 다음 조치를 택하게 만드는가`까지 이어져야 합니다.

입력(input):

위에 정리한 문맥 줄 목록 `context`를 사용합니다.

```python
context = [
    "Rule: unstable pressure state must not be restarted.",
    "Log: sensor calibration completed for line 3.",
    "Log: packaging material restocked this morning.",
    "State: pressure has not fully returned to safe range.",
    "Log: operator schedule updated for tomorrow.",
    "Request: restart line 3 now.",
]

def sequential_reader(lines, decay=0.55):
    state = {"pressure_risk": 0.0, "restart": 0.0, "block": 0.0}
    history = []
    for idx, line in enumerate(lines, start=1):
        lowered = line.lower()
        for key in state:
            state[key] *= decay
        if "pressure" in lowered or "unstable" in lowered:
            state["pressure_risk"] += 1.0
        if "restart" in lowered:
            state["restart"] += 1.0
        if "must not" in lowered:
            state["block"] += 1.0
        snapshot = {key: round(value, 3) for key, value in state.items()}
        history.append((idx, line, snapshot))
    support = round(min(state.values()), 3)
    decision = "block_restart" if support >= 0.8 else "uncertain"
    return history, {key: round(value, 3) for key, value in state.items()}, support, decision

def direct_reference_reader(lines):
    request = lines[-1].lower()
    keywords = {"restart", "pressure", "unstable", "must", "not"}
    scored = []
    for idx, line in enumerate(lines[:-1], start=1):
        words = set(line.lower().replace(".", "").replace(":", "").split())
        score = len(words & keywords)
        scored.append((score, idx, line))
    top_matches = sorted(scored, reverse=True)[:2]
    matched_lines = [line.lower() for _, _, line in top_matches]
    decision = (
        "block_restart"
        if any("must not be restarted" in line for line in matched_lines)
        and any("pressure" in line or "unstable" in line for line in matched_lines)
        and "restart" in request
        else "allow"
    )
    return top_matches, decision

history, final_state, sequential_support, sequential_decision = sequential_reader(context)
top_matches, direct_decision = direct_reference_reader(context)

print("[sequential reader]")
for idx, line, snapshot in history:
    print(f"{idx}. {line}")
    print("   state =", snapshot)
print("final_state =", final_state)
print("sequential_support =", sequential_support)
print("sequential_decision =", sequential_decision)
print()

print("[direct reference reader]")
for score, idx, line in top_matches:
    print(f"matched line {idx} (score={score}): {line}")
print("direct_decision =", direct_decision)
```

출력에서는 sequential_support가 얼마나 약해졌는지와 direct_decision이 어떻게 유지되는지부터 보면 됩니다.

```text
[sequential reader]
1. Rule: unstable pressure state must not be restarted.
   state = {'pressure_risk': 1.0, 'restart': 1.0, 'block': 1.0}
2. Log: sensor calibration completed for line 3.
   state = {'pressure_risk': 0.55, 'restart': 0.55, 'block': 0.55}
3. Log: packaging material restocked this morning.
   state = {'pressure_risk': 0.303, 'restart': 0.303, 'block': 0.303}
4. State: pressure has not fully returned to safe range.
   state = {'pressure_risk': 1.166, 'restart': 0.166, 'block': 0.166}
5. Log: operator schedule updated for tomorrow.
   state = {'pressure_risk': 0.642, 'restart': 0.092, 'block': 0.092}
6. Request: restart line 3 now.
   state = {'pressure_risk': 0.353, 'restart': 1.05, 'block': 0.05}
final_state = {'pressure_risk': 0.353, 'restart': 1.05, 'block': 0.05}
sequential_support = 0.05
sequential_decision = uncertain

[direct reference reader]
matched line 1 (score=4): Rule: unstable pressure state must not be restarted.
matched line 4 (score=2): State: pressure has not fully returned to safe range.
direct_decision = block_restart
```

첫 번째 산출물은 순차 상태가 문맥을 지나며 어떻게 약해지는지입니다. `block` 축은 규칙 줄에서 강하게 시작하지만 중간 로그를 지나 마지막 요청 시점에는 `0.05`만 남습니다.

![순차 상태 약화](/AiBook/assets/part-05/chapter-14/sequential-state-decay-ko.png)

두 번째 산출물은 직접 재참조 방식이 마지막 요청 시점에 어떤 줄을 다시 끌어오는지입니다. 규칙 줄과 압력 상태 줄이 높은 근거로 다시 떠오르므로, 이 예제에서 읽어야 할 변화는 단순히 두 결정 이름이 다르다는 사실이 아니라, 앞 단서가 `상태 안에서 약해지는가`와 `현재 요청에서 다시 호출되는가`의 차이입니다.

![직접 재참조 점수](/AiBook/assets/part-05/chapter-14/direct-reference-match-scores-ko.png)

| 먼저 볼 출력 | 이 출력이 뜻하는 것 | 바꿔 보면 달라지는 것 |
| --- | --- | --- |
| `sequential_support`와 `direct_decision`의 차이 | 상태 압축만으로는 앞 규칙이 약해지고, 직접 재참조는 필요한 줄을 다시 끌어온다는 뜻 | `decay`와 중간 로그 수를 바꾸면 순차 압축의 약화 정도가 더 직접 드러납니다 |

| 운영 판단 기준 | 순차 상태 출력만 보면 쉬운 판단 | 직접 재참조 출력을 읽고 바뀌는 판단 |
| --- | --- | --- |
| 압력 미복귀 상태의 재기동 요청 처리 | `uncertain`이므로 마지막 요청만 보고 재기동을 진행하거나, 규칙 문서를 다시 수동 재검색해야 할 수 있다 | 규칙 줄과 상태 줄이 다시 떠오르므로 `재기동 차단`을 바로 우선 조치로 잡을 수 있다 |
| 로그가 길어졌을 때의 대응 | 중간 로그가 많아질수록 앞 규칙이 희미해져 `왜 막아야 하는가` 근거가 흐려질 수 있다 | 요청 시점마다 필요한 앞 문장을 다시 끌어오므로, 로그가 길어져도 차단 근거를 현재 판단에 다시 붙일 수 있다 |

- 먼저 `sequential_support = 0.05`와 `direct_decision = block_restart`를 같이 봐야 합니다. 앞 규칙을 상태에만 눌러 담은 쪽은 마지막 요청 시점에 금지 근거가 거의 사라졌고, 필요한 줄을 다시 참조한 쪽은 같은 요청을 바로 차단하기 때문입니다.
- sequential 방식에서는 앞 규칙이 중간 로그를 지나는 동안 점차 약해져, 마지막 요청 시점에는 `압력 위험`, `재기동`, `금지` 세 단서를 동시에 강하게 유지하지 못합니다
- `sequential_support`는 마지막 요청 시점에 세 핵심 단서 중 가장 약한 축이 얼마나 남았는지를 보여 주며, 여기서는 `block` 축이 거의 사라졌음을 확인할 수 있습니다
- direct reference 방식에서는 마지막 요청이 관련된 앞 규칙과 대상 정보가 있는 줄을 다시 바로 찾습니다
- 긴 문맥에서 중요한 것은 `앞 문장을 한 번 읽고 버티는가`보다 `현재 위치에서 필요한 앞 문장을 다시 끌어올 수 있는가`라는 점입니다

이 결과를 운영 현장 판단으로 바꾸면, sequential 쪽은 `출고 금지 규칙을 끝까지 붙잡지 못해 사람이 다시 문서를 뒤져야 하는 상태`에 가깝고, direct reference 쪽은 `현재 요청 처리 시점에 바로 금지 근거를 호출해 차단 결정을 내리는 상태`에 가깝습니다. 이 절에서 읽어야 할 구조 차이는 바로 이런 `근거 호출 방식의 차이`입니다.

이 출력은 단순 비교로 끝내기보다, 바로 어떤 값을 바꿔 보며 구조 차이를 더 확인할지로 이어지면 좋습니다.

| 먼저 보인 출력 신호 | 지금 바로 해 볼 변화 | 아직 이 예제만으로 서두르지 않을 결론 |
| --- | --- | --- |
| `sequential_support`가 빠르게 작아진다 | `decay`를 더 낮추거나 중간 로그 줄 수를 늘려 순차 압축이 얼마나 더 흔들리는지 본다 | 모든 순차 모델이 항상 실패한다고 단정하지 않는다 |
| `top_matches`가 규칙 줄과 대상 줄을 다시 집어온다 | 규칙 문장을 더 멀리 보내거나 요청 표현을 바꿔도 필요한 줄을 다시 찾는지 본다 | 직접 재참조가 곧 완전한 이해를 보장한다고 단정하지 않는다 |
| `sequential_decision`과 `direct_decision`이 갈라진다 | 규칙 단서 수를 줄이거나 늘려 어떤 조건에서 두 구조 판단이 다시 가까워지는지 본다 | 이 간단한 비교 예제 하나로 실제 long-context 최적화 성능 전체를 결론내리지 않는다 |

이 예제는 RNN과 Transformer 전체를 구현한 것은 아니지만, 긴 문맥에서 `상태에 압축해 유지하는 감각`과 `필요한 앞 위치를 다시 참조하는 감각` 차이를 실제로 실험해 볼 수 있습니다. `decay` 값을 바꾸거나 중간 로그 줄 수를 늘려 보면 순차 압축이 왜 더 어려워지는지도 직접 확인할 수 있습니다.

## 이 예제를 긴 문맥 재참조 관점으로 다시 보면

앞의 간단한 비교 코드는 Transformer 전체를 구현한 것은 아니지만, 비교 기준은 분명합니다.

- sequential 쪽은 `앞 규칙을 상태 하나에 압축해 오래 버틸 수 있는가`를 보여 줍니다.
- direct reference 쪽은 `현재 요청이 필요할 때 앞 규칙과 대상 정보를 다시 집어 올 수 있는가`를 보여 줍니다.
- 그래서 최종적으로 갈리는 것도 `기억이 좋으냐` 같은 인상이 아니라, `현재 판단 시점에 금지 근거를 다시 호출해 즉시 차단할 수 있느냐`입니다.

즉, 긴 문맥 문제를 `기억 유지`로만 보면 순차 상태의 한계가 먼저 보이고, `필요한 앞 위치 재참조`로 보면 Transformer 계열의 장점이 더 직접적으로 보입니다. 이 감각이 있어야 뒤에서 긴 문맥 제약을 읽을 때도 `무조건 더 오래 기억한다`가 아니라 `필요한 문맥을 다시 창 안으로 가져와 읽는다`는 관점으로 자연스럽게 이해할 수 있습니다.

Transformer가 attention 중심 구조와 병렬 계산의 장점을 결합하면서, 자연어 처리의 기본 계산 구조가 크게 바뀌었습니다. 이후 대규모 사전학습(pretraining), 긴 문맥 처리, 다양한 생성 모델 확장은 모두 이 구조적 전환과 깊게 연결됩니다.

- 왜 Transformer가 단순한 또 하나의 순차 모델이 아니었는지
- 왜 GPU 시대와 맞물려 대규모 언어 모델이 가능해졌는지
- 왜 긴 문맥과 대규모 학습의 기준이 함께 바뀌었는지

를 한 절에서 묶어 주기 때문입니다.

## 체크리스트

- 왜 트랜스포머가 RNN보다 병렬 처리에 더 잘 맞는지 설명할 수 있는가?
- 긴 문맥(long context) 참조에서 셀프 어텐션의 장점을 말할 수 있는가?
- Transformer는 토큰을 순차 상태로만 전달하지 않고, 관계를 더 병렬적으로 계산한다는 점을 설명할 수 있는가?
- 이 구조가 GPU 병렬 처리와 잘 맞는다는 점을 말할 수 있는가?
- self-attention은 먼 위치를 더 직접 참조하는 감각을 준다는 점을 설명할 수 있는가?
- Transformer의 강점을 `더 성능이 좋다`가 아니라 `계산 흐름을 GPU 친화적 관계 계산으로 바꿨다`는 말로 설명할 수 있는가?
- 긴 문맥 문제를 `오래 기억한다`보다 `필요한 앞 단서를 현재 위치가 다시 본다`는 감각으로 설명할 수 있는가?
- 이후 LLM 장을 읽을 때도 먼저 `구조가 무엇을 계산 가능하게 만들었는가`를 떠올릴 준비가 되어 있는가?

## 출처와 참고 자료

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-06-29.
- Colin Raffel et al., `Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer`, JMLR, 2020, 확인 날짜: 2026-06-29.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
