# P5-14.5 긴 문맥에서 순차 상태와 직접 재참조는 어떻게 갈라지는가

> Section ID: `P5-14.5`
> Version: `v2026.07.31`

P5-14.4에서는 RNN의 순차 상태 전달과 Transformer의 관계 계산이 병렬 처리 관점에서 어떻게 다른지 보았습니다. P5-14.5의 관찰값은 GPU 효율이 아니라 긴 문맥(long context)에서 마지막 판단이 앞 단서를 어떤 방식으로 다시 근거로 붙이는가입니다.

긴 문맥에서 중요한 것은 오래 기억하는 것인가, 필요한 앞 위치를 다시 참고하는 것인가?

비교 대상은 Transformer 전체 구현이 아니라, 긴 문맥에서 `앞 규칙을 상태 하나에 압축해 들고 가는 방식`과 `현재 질문이 필요한 앞 문장을 다시 찾는 방식`입니다. 병렬 처리의 계산 효율은 P5-14.4에서 닫고, 여기서는 먼 단서가 최종 판단에 다시 붙는 경로만 봅니다.

긴 문맥 예제를 읽을 때는 `early_rule`, `current_request`, `distractor_context`, `reference_path`, `final_decision_basis`를 나누어 적습니다. 이 필드가 있어야 단순히 앞 내용을 오래 기억했는지보다, 마지막 판단이 어떤 앞 단서를 다시 근거로 삼았는지가 드러납니다.

## 긴 문맥 재참조와 실험이 다루는 질문

- 긴 문맥에서 순차 상태 전달은 왜 약해질 수 있는가?
- self-attention은 왜 먼 앞 위치를 더 직접 참고하는 감각을 주는가?
- 순차 상태 방식과 직접 재참조 방식은 같은 긴 문맥에서도 최종 판단을 어떻게 다르게 만들 수 있는가?

## 순차 전달과 직접 재참조를 비교하면

RNN에서는 먼 정보가 현재까지 오려면 상태를 여러 step 거쳐 전달해야 합니다. 반면 self-attention에서는 앞 단서를 상태 하나에만 압축해 지나오지 않고, 현재 위치와 앞 위치 사이의 관계 점수를 다시 계산할 수 있습니다. 그래서 멀리 떨어진 단서도 현재 판단 위치에서 더 직접 참고되는 것처럼 읽힙니다.

여기서 관계 점수는 마지막 요청 위치가 앞 단서들과 다시 비교해 얻는 관련도입니다. 마지막 요청 위치는 앞의 규칙 줄, 현재 상태 줄, 무관한 로그 줄을 모두 같은 방식으로 다시 비교합니다. 그중 현재 요청과 강하게 맞물리는 줄은 판단 근거로 다시 떠오르고, 관계가 약한 줄은 뒤로 밀립니다.

예를 들어 마지막 질문이 `지금 라인 3을 재기동해도 되는가?`라면, 질문 위치는 앞쪽의 `재기동하지 않는다` 규칙과 `압력이 안전 범위로 돌아오지 않았다` 상태를 다시 비교해야 합니다. 이 비교가 되면 긴 문맥 앞부분의 단서가 단순히 오래 기억된 것이 아니라, 마지막 판단 시점에 다시 근거로 붙습니다.

먼저 전체 개념 경로를 보면 다음과 같습니다. 앞 단서는 순차 상태 안에서 압축되어 이동할 수도 있고, 현재 질문 위치에서 다시 비교될 수도 있습니다.

```mermaid
--8<-- "assets/part-05/chapter-14/long-context-direct-reference-ko.mmd"
```

이제 같은 요청 하나를 두 계산 경로로만 나누어 보면 다음처럼 볼 수 있습니다. 이 도식은 긴 문맥 전체 구조보다, 마지막 요청이 어떤 근거 경로로 판단에 도착하는지를 비교합니다.

```mermaid
--8<-- "assets/part-05/chapter-14/sequential-vs-direct-baseline-ko.mmd"
```

| 관점 | 순차 상태 전달 | 직접 재참조 |
| --- | --- | --- |
| 앞 단서 이동 | 중간 상태를 거쳐 전달됨 | 현재 위치가 필요한 앞 위치를 다시 봄 |
| 긴 문맥 위험 | 중간 정보가 길어질수록 단서가 약해질 수 있음 | 관련 앞 위치를 다시 끌어올 가능성이 커짐 |
| 마지막 판단 | 상태 안에 남은 단서 강도에 의존 | 현재 요청과 앞 근거의 관계 계산에 의존 |

긴 문맥 문제를 `기억력`으로만 읽으면 모델이 앞 내용을 오래 붙잡고 있느냐만 보게 됩니다. 하지만 Transformer 구조에서 더 중요한 감각은 현재 위치가 필요한 앞 위치를 다시 참고할 수 있느냐입니다.

## 긴 문맥에서 순차 상태와 직접 재참조는 어떻게 갈라지는가: 확인할 판단 기준

이 사례를 읽을 때는 다음 두 가지를 먼저 확인한다.

- 긴 문맥 문제를 단순 기억력보다 현재 위치가 필요한 앞 단서를 직접 다시 참고하는 문제로 읽게 하고, 순차 상태 방식과 직접 재참조 방식이 최종 판단을 다르게 만들 수 있음을 실험과 해설로 보여 주어야 합니다. Python 예제는 Transformer 구현이 아니라 `sequential_support`와 `direct_decision`의 관찰 차이를 닫는 용도로 유지하는지 확인한다.
- 이어지는 사례에서 입력, 비교 기준, 출력, 한계가 제목의 판단 기준과 어떻게 연결되는지 확인한다.

### 사례. 압력 미복귀 상태의 재기동 요청

긴 작업 허가 질의응답을 보겠습니다.

| 후보 단서 | 마지막 판단과의 관계 | 직접 재참조 관점 |
| --- | --- | --- |
| `압력 해소 전에는 라인 3을 재기동하지 않는다` | 재기동 차단 규칙 | 반드시 다시 불러와야 하는 앞 단서 |
| `현재 압력은 아직 안전 범위로 돌아오지 않았다` | 규칙이 현재도 적용되는 상태 | 반드시 다시 불러와야 하는 앞 단서 |
| `센서 보정은 오전에 완료되었다` | 안전 범위 복귀를 뜻하지 않음 | 혼동될 수 있는 약한 단서 |
| `근무 교대 기록은 갱신되었다` | 재기동 안전 판단과 직접 관계 약함 | 판단 중심에서 밀어낼 단서 |
| `지금 라인 3 재기동을 승인해도 되는가?` | 현재 질문 | 앞 규칙과 상태를 다시 붙여야 하는 위치 |

사람이 먼저 쓰기 쉬운 기준은 `문서를 많이 읽었으니 앞 내용을 기억해야 한다`입니다. 하지만 이 사례에서 확인해야 할 결과는 `많이 기억했는가`가 아닙니다. 마지막 판단 시점에 금지 규칙과 현재 압력 상태를 다시 근거로 붙였는가입니다.

순차 상태 방식은 앞 규칙을 하나의 상태에 압축해 끝까지 가져가려 합니다. 중간 로그가 많아지면 금지 규칙 축이 약해질 수 있습니다. 직접 재참조 방식은 마지막 요청 시점에 규칙 줄과 압력 상태 줄을 다시 찾아옵니다.

상태 하나에 압축한다는 말은 앞 단서가 사라진다는 뜻이 아닙니다. 다만 새 줄을 읽을 때마다 상태 안에는 센서 보정, 포장재 보충, 근무 교대 같은 다른 정보도 계속 섞입니다. 마지막 요청에 도착했을 때 금지 규칙이 별도 근거로 선명하게 남아 있지 않으면, 모델은 `재기동 금지`보다 최근 로그나 승인 단어에 더 흔들릴 수 있습니다.

이 사례의 판단 문장은 다음처럼 닫혀야 합니다.

| 방식 | 판단 문장 |
| --- | --- |
| 순차 상태만 약하게 남은 경우 | 앞 금지 규칙이 마지막 요청까지 충분히 남지 않아 판단이 불확실해질 수 있다 |
| 직접 재참조가 필요한 단서를 찾은 경우 | 마지막 요청이 금지 규칙과 현재 압력 상태를 다시 근거로 붙여 재기동 차단 쪽으로 판단한다 |

## 연습 및 예제

### 연습. 필요한 앞 단서와 방해 단서 나누기

아래 후보 단서를 `필요`, `약함`, `방해에 가까움`으로 나누어 보십시오.

| 후보 단서 | 분류 | 해설 |
| --- | --- | --- |
| `압력 해소 전에는 라인 3을 재기동하지 않는다` | 필요 | 마지막 재기동 승인 질문을 직접 막는 규칙입니다. |
| `현재 압력은 아직 안전 범위로 돌아오지 않았다` | 필요 | 금지 규칙이 현재도 적용되는지 확인합니다. |
| `센서 보정은 오전에 완료되었다` | 약함 | 센서 보정은 압력 안전 범위 복귀와 같지 않습니다. |
| `포장재 보충 작업은 별도 승인되었다` | 방해에 가까움 | 승인이라는 단어가 있어도 라인 3 재기동 승인과 직접 관계가 약합니다. |

해설: 긴 문맥 문제의 학습 포인트는 `많이 읽었다`가 아니라 `마지막 판단에 필요한 근거를 다시 붙였다`입니다. 필요한 단서만 고르는 것이 아니라, 직접 관계가 약한 단서를 판단 중심에서 밀어내야 합니다.

### 예제. sequential reader와 direct reference reader 비교

이 예제는 Transformer 구현이 아니라, 긴 문맥 판단에서 두 참조 방식이 어떤 관찰값을 남기는지 비교하는 실험입니다. `direct_reference_reader`는 실제 attention 계산이 아니라 키워드 점수로 앞 줄을 다시 정렬하는 축약 모델입니다. 여기서 확인할 것은 정해진 답을 맞히는지 여부가 아니라 `상태 안에서 약해지는 단서`와 `현재 요청에서 다시 위로 올라오는 단서`의 출력 차이입니다.

| 조작할 값 | 관찰할 출력 | 확인할 질문 |
| --- | --- | --- |
| `decay` | `sequential_support`, `final_state` | 앞 규칙이 순차 상태 안에서 얼마나 빨리 약해지는가 |
| 중간 `Log:` 줄 개수 | `block` 축의 마지막 값 | 관련 없는 중간 문장이 늘어날수록 순차 상태가 더 흔들리는가 |
| 마지막 `Request:` 문장 | 상위 matched line, score | 현재 요청과 어떤 앞 줄의 단어 축이 더 강하게 겹치는가 |

```python
# 긴 문맥에서 순차 상태가 약해지는 과정과 direct reference가 앞 규칙을 다시 찾는 과정을 비교하는 예제입니다.
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
    return history, {key: round(value, 3) for key, value in state.items()}, support

def direct_reference_reader(lines):
    request = lines[-1].lower()
    keywords = set(request.replace(".", "").replace(":", "").split())
    keywords |= {"pressure", "unstable", "must", "not"}
    scored = []
    for idx, line in enumerate(lines[:-1], start=1):
        words = set(line.lower().replace(".", "").replace(":", "").split())
        score = len(words & keywords)
        scored.append((score, idx, line))
    top_matches = sorted(scored, reverse=True)[:2]
    return top_matches

history, final_state, sequential_support = sequential_reader(context)
top_matches = direct_reference_reader(context)

print("[sequential reader]")
for idx, line, snapshot in history:
    print(f"{idx}. {line}")
    print("   state =", snapshot)
print("final_state =", final_state)
print("sequential_support =", sequential_support)
print()

print("[direct reference reader]")
for score, idx, line in top_matches:
    print(f"matched line {idx} (score={score}): {line}")
```

출력 예시는 다음처럼 읽습니다.

```text
final_state = {'pressure_risk': 0.353, 'restart': 1.05, 'block': 0.05}
sequential_support = 0.05

matched line 1 (score=4): Rule: unstable pressure state must not be restarted.
matched line 4 (score=2): State: pressure has not fully returned to safe range.
```

첫 번째 산출물은 순차 상태가 문맥을 지나며 어떻게 약해지는지입니다. `block` 축은 규칙 줄에서 강하게 시작하지만 중간 로그를 지나 마지막 요청 시점에는 `0.05`만 남습니다.

![순차 상태 약화](/AiBook/assets/part-05/chapter-14/sequential-state-decay-ko.png)

두 번째 산출물은 직접 재참조 방식이 마지막 요청 시점에 어떤 줄을 다시 끌어오는지입니다. 이 코드는 `재기동을 차단하라`는 정답을 판정하지 않습니다. 대신 마지막 요청 문장의 단어 축과 앞 줄의 단어 축을 비교해, 규칙 줄과 압력 상태 줄이 상위 근거로 다시 떠오르는지 보여 줍니다. 이 예제에서 읽어야 할 변화는 결정 이름이 아니라, 앞 단서가 `상태 안에서 약해지는가`와 `현재 요청에서 다시 위로 올라오는가`의 차이입니다.

![직접 재참조 점수](/AiBook/assets/part-05/chapter-14/direct-reference-match-scores-ko.png)

### 연습. 값을 바꿔 차이 확인하기

| 바꿔 볼 값 | 예상되는 출력 변화 | 해설 |
| --- | --- | --- |
| `decay`를 `0.55`에서 `0.8`로 높인다 | `sequential_support`가 커질 수 있다 | 순차 상태가 앞 단서를 더 오래 유지하므로, 규칙 줄에서 생긴 `block` 축이 마지막 요청까지 덜 약해집니다. |
| 중간 로그를 3줄 더 추가한다 | 순차 상태 쪽이 더 흔들리기 쉽다 | 중간 줄이 늘수록 상태 안의 앞 단서는 계속 감쇠하지만, 직접 재참조는 키워드가 맞는 앞 줄을 다시 찾을 수 있으면 판단을 유지할 수 있습니다. |
| 마지막 요청에서 `restart`라는 단어를 뺀다 | 상위 matched line의 순위가 달라질 수 있다 | 현재 요청에 앞 규칙과 연결될 핵심 단어가 빠지면, 직접 재참조 쪽에서도 어떤 앞 단서가 강하게 떠오르는지 달라집니다. |

해설: 이 연습은 직접 재참조가 언제나 정답을 보장한다고 말하려는 것이 아닙니다. 핵심은 긴 문맥에서 앞 단서가 `상태 안에서 약해지는가`, 아니면 `현재 요청과의 비교에서 다시 위로 올라오는가`를 출력 변화로 구분하는 것입니다.

## 체크리스트

- 긴 문맥 문제를 순차 상태 전달과 직접 재참조의 차이로 설명할 수 있는가?
- self-attention이 먼 위치를 더 직접 참고하는 감각을 준다는 점을 말할 수 있는가?
- `sequential_support`와 상위 matched line의 차이를 설명할 수 있는가?
- 긴 문맥에서 최종 판단이 근거 호출 방식에 따라 달라질 수 있음을 말할 수 있는가?

## 출처와 참고 자료

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
