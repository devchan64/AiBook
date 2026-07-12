# P5-12.2 장기 의존성(long-term dependency)

Section ID: `P5-12.2`
Version: `v2026.07.12`

P5-12.1에서는 RNN, LSTM, GRU가 순차 데이터(sequence data)를 다루기 위해 등장한 구조라고 설명했습니다. 여기서 바로 다음 질문이 생깁니다.

왜 순차 모델은 오래전 정보를 끝까지 유지하기 어려웠고, 그것이 왜 큰 문제였는가?

이 질문에 답하는 개념이 장기 의존성(long-term dependency)입니다.

장기 의존성은 현재 판단에 오래전 정보가 중요한데도, 모델이 그 정보를 충분히 오래 유지하거나 전달하지 못하는 문제를 뜻한다.

이후 attention 장을 읽다가 거리 문제의 출발점을 다시 확인해야 할 때는 개념사전의 [장기 의존성(long-term dependency)](../../../reference/concept-glossary.md#long-term-dependency) 항목으로 돌아갑니다.

## 이 절의 범위

- 장기 의존성은 무엇을 뜻하는가?
- 왜 기본 RNN에서는 오래전 정보가 약해지기 쉬운가?
- 이 문제가 실제 문장, 음성, 시계열에서 어떻게 드러나는가?
- LSTM, GRU, 그리고 나중의 attention이 왜 이 문제와 연결되는가?

이 절에서 먼저 닫아야 하는 핵심은 `순차 상태를 넘기는 구조만으로는 먼 앞 단서를 현재 판단까지 안정적으로 들고 오기 어렵다`는 점입니다.

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- vanishing gradient 수식의 엄밀한 전개
- BPTT(backpropagation through time)의 상세 유도
- attention 메커니즘의 구현 세부

attention 자체는 다음 장에서 이어서 다루고, Transformer로의 확장은 그다음 장에서 다시 다룹니다. vanishing gradient 수식과 BPTT의 상세 유도는 이 책의 현재 본편 범위 밖에 둡니다.

지금 읽는 층위는 `상태 보존 한계 층위`입니다. 앞 절의 RNN, LSTM, GRU가 `순차 상태를 어떻게 넘기고 관리할까`를 다뤘다면, 여기서는 그 상태 보존 방식이 어디에서 흔들리기 시작하는지 읽습니다. 바로 다음의 attention 절에서는 이 한계를 `필요한 위치를 다시 찾아보는 방식`으로 어떻게 뒤집는지 질문이 더 커집니다.

여기서는 장기 의존성을 Part 5 본류의 `상태 보존 한계 손잡이`로 먼저 잡고, 그 다음에 attention이 어떤 구조 전환을 가져오는지 같이 보는 편이 흐름이 덜 끊깁니다.

| 지금 단계의 손잡이 | 바로 다음에 이어질 질문 | 뒤에서 본격적으로 다시 읽는 위치 |
| --- | --- | --- |
| RNN / LSTM / GRU | 순차 상태를 어떻게 넘기고 더 잘 관리할 수 있는가? | P5-12.1 |
| 장기 의존성 | 그 상태 보존이 왜 먼 단서 앞에서 흔들리기 쉬운가? | P5-12.2 |
| attention | 필요한 위치를 현재 시점에서 다시 직접 참고할 수 있는가? | P5-13.1 |

앞뒤 장의 최소 차이는 다음 표처럼 다시 고정할 수 있습니다.

| 바로 앞 장 | 지금 장 | 바로 다음에 더 붙는 장 |
| --- | --- | --- |
| RNN 계열: 상태를 어떻게 이어받고 조절할까 | 장기 의존성: 그 상태 보존이 어디에서 약해지는가 | attention: 필요한 위치를 다시 찾아보는 방식으로 무엇이 바뀌는가 |
| 상태 전달 구조 | 상태 보존의 한계 | 직접 참조 구조 |

즉, 지금 장의 핵심은 `상태를 어떻게 관리할까`에서 `그 상태 관리가 왜 먼 단서 앞에서 흔들리는가`로 손잡이가 바뀐다는 점입니다.

## 이 절의 목표

- 장기 의존성을 `오래전 정보가 필요한데 잘 유지되지 않는 문제`로 설명할 수 있습니다.
- 기본 RNN이 긴 문맥을 다루기 어려운 이유를 입문 수준에서 말할 수 있습니다.
- LSTM과 GRU가 왜 등장했는지 더 분명히 연결할 수 있습니다.
- attention이 왜 자연스러운 다음 주제가 되는지 설명할 수 있습니다.

## 이 절을 읽는 순서

1. 장기 의존성이 무엇을 뜻하는지 먼저 정의합니다.
2. 왜 기본 RNN에서 오래전 정보가 약해지기 쉬운지 봅니다.
3. 이 문제가 단순 성능 저하가 아니라 문맥 해석 방식의 문제라는 점을 봅니다.
4. LSTM과 GRU가 왜 나왔는지 다시 연결합니다.
5. 마지막에 왜 attention이 자연스러운 다음 주제가 되는지 정리합니다.

## 장기 의존성은 무엇을 뜻하나

순차 데이터에서는 현재 위치의 의미가 훨씬 앞에 있던 정보에 달려 있을 수 있습니다.

예를 들어 문장에서:

- 주어가 앞에 나오고
- 동사가 한참 뒤에 나오며
- 부정 표현이 뒤 의미를 바꿀 수도 있습니다

이때 현재 단어를 해석하려면, 오래전 단서를 기억하고 있어야 할 수 있습니다.

핵심은 현재 판단이 가까운 정보만으로는 부족하고, 한참 앞의 단서까지 이어서 참조해야 한다는 점입니다.

`가까운 정보만으로는 부족하고, 한참 앞의 정보까지 이어서 봐야 하는 상황이 장기 의존성 문제를 만든다.`

즉, 장기 의존성은 `이전 정보가 있으면 좋다` 정도의 문제가 아니라, `오래전 정보가 없으면 현재 판단 자체가 흔들리는가`를 묻는 문제입니다.

## 왜 기본 RNN은 오래전 정보를 놓치기 쉬운가

RNN은 각 step에서 이전 상태를 이어받지만, 그 상태는 계속 새 입력과 섞이며 갱신됩니다. 시점이 길어질수록 오래전 정보는 점점 희미해질 수 있습니다.

다음 비유로 읽으면 더 분명합니다.

- 메모를 계속 새로 덧쓰는 작은 칠판이 있다고 생각해 봅니다
- 짧은 정보는 남기기 쉽지만
- 오래전 중요한 문장을 계속 보존하기는 어렵습니다

즉, RNN의 핵심 아이디어는 좋지만, 긴 시퀀스에서는 `무엇을 오래 남길지`를 정교하게 관리하기 어렵다는 한계가 있었습니다.

이 절에서 중요한 것은 수식을 먼저 외우는 일이 아니라, `상태를 계속 갱신하다 보면 오래전 정보가 뒤로 갈수록 희미해질 수 있다`는 감각을 잡는 것입니다.

## 왜 이것이 단순한 성능 문제가 아닌가

장기 의존성은 단순히 `조금 덜 정확하다` 정도의 문제가 아니라, 순차 구조를 해석하는 방식 자체를 바꿉니다.

왜냐하면:

- 어떤 문제는 가까운 정보만 보면 충분하지만
- 어떤 문제는 오래전 정보가 핵심 단서이기 때문입니다

즉, 장기 의존성 문제는 모델이 `얼마나 멀리까지 문맥을 유지할 수 있는가`에 대한 질문입니다.

독자는 여기서 `가까운 단서`와 `먼 단서`를 나눠 보면 이해가 빨라집니다.

| 단서 유형 | 예 |
| --- | --- |
| 가까운 단서 | 바로 앞 단어, 직전 몇 초의 센서 변화 |
| 먼 단서 | 문장 맨 앞 주어, 오래전 시제 정보, 훨씬 앞쪽 이상 징후 |

장기 의존성은 주로 두 번째 유형이 중요할 때 드러납니다.

## 그래서 LSTM과 GRU는 무엇을 하려 했나

P5-12.1에서 본 것처럼 LSTM과 GRU는 기본 RNN보다 더 잘 기억을 관리하려는 구조입니다.

핵심은 어떤 정보는 남기고 어떤 정보는 버리며, 현재 입력을 얼마나 반영할지를 더 세밀하게 조절한다는 점입니다.

- 어떤 정보는 남기고
- 어떤 정보는 버리고
- 현재 입력을 얼마나 반영할지

를 더 세밀하게 조절해, 장기 의존성을 더 잘 다루려는 시도입니다.

즉, LSTM과 GRU는 `오래 기억하고 싶은 정보를 더 오래 살아남게 하려는 구조`라고 볼 수 있습니다.

이 설명은 바로 앞 절과도 이어집니다. P5-12.1에서 RNN을 `상태를 넘기는 구조`로 봤다면, 여기서는 LSTM과 GRU를 `그 상태를 더 잘 보존하게 만든 구조`로 읽으면 됩니다.

## 그런데 왜 attention이 다시 등장했나

LSTM과 GRU는 장기 의존성 문제를 완화했지만, 여전히 순차 상태를 차례대로 전달하는 구조의 한계가 남아 있었습니다. 바로 이 지점에서 attention이 중요해집니다.

이 전환은 sequence-to-sequence(seq2seq) 번역이나 encoder-decoder 구조를 떠올리면 더 분명해집니다. 입력 문장을 읽는 encoder가 긴 입력의 핵심을 하나의 상태나 소수의 상태에 압축해 decoder로 넘기면, 문장이 짧을 때는 버틸 수 있어도 길어질수록 `지금 출력하는 단어와 직접 관련 있는 앞 위치`를 끝까지 보존하기가 어려워집니다. 즉, 문제는 단순히 `더 오래 기억하자`에만 있지 않고, `출력 시점마다 어떤 입력 위치를 다시 참고해야 하나`를 따로 다루지 못한다는 데에도 있었습니다.

attention의 핵심 직관은 다음과 같이 연결할 수 있습니다.

`굳이 오래전 정보를 상태에만 희미하게 담아 두지 말고, 현재 위치가 필요할 때 과거의 중요한 위치를 더 직접적으로 참고하자.`

즉, attention은 장기 의존성 문제에 대한 더 직접적인 응답처럼 읽을 수 있습니다.

이 전환을 순차 전달과 직접 참조의 대비로 아주 짧게 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-12/state-vs-direct-reference-flow-ko.mmd"
```

이 도식에서 먼저 확인할 결과는, 순차 상태 전달은 앞 단서가 많은 중간 step을 거쳐야 하지만, direct reference 계열은 필요한 시점에 그 단서를 다시 바로 끌어올 수 있다는 점입니다.

이 seq2seq 전환을 가장 짧게 붙들면 다음과 같습니다.

| 구조 감각 | 입력 정보를 다루는 기본 방식 | 길어질수록 먼저 드러나는 부담 |
| --- | --- | --- |
| basic RNN | 상태를 한 step씩 계속 넘긴다 | 오래전 단서가 뒤로 갈수록 흐려질 수 있다 |
| encoder-decoder | 입력 전체를 압축한 상태를 decoder가 이어받는다 | 긴 입력의 세부 단서를 출력 시점마다 다시 꺼내기 어렵다 |
| attention | 출력 시점마다 관련 있는 입력 위치를 다시 본다 | 어떤 위치를 얼마나 참고할지 계산해야 한다 |

이 점이 다음 절로 넘어갈 때 가장 중요합니다. basic RNN, LSTM, GRU는 모두 `상태를 이어서 기억한다`는 계열 안에 있지만, attention은 `필요한 위치를 다시 본다`는 쪽으로 발상을 바꿉니다.

이 연결을 더 짧게 정리하면 다음과 같습니다.

| 구조 | 오래전 정보를 다루는 기본 감각 |
| --- | --- |
| basic RNN | 상태를 계속 넘기며 유지하려 한다 |
| LSTM / GRU | 무엇을 남길지 더 잘 조절한다 |
| attention | 필요한 위치를 더 직접 다시 참고한다 |

이 전환을 한계와 다음 발상이라는 흐름으로 다시 정리하면 다음과 같습니다.

| 단계 | 먼저 드러난 한계 | 바로 다음에 바뀌는 발상 |
| --- | --- | --- |
| basic RNN | 상태를 넘기지만 오래전 단서가 쉽게 희미해질 수 있다 | 기억을 더 잘 관리하는 구조가 필요하다 |
| LSTM / GRU | 기억 관리는 나아지지만 여전히 순차 전달 부담이 남는다 | 필요한 위치를 현재 시점에 다시 직접 참고하자 |
| attention | 상태 보존보다 직접 참조가 더 중요해진다 | 뒤 장에서 self-attention과 Transformer로 확장된다 |

## 사례 및 예시

### 사례 1. 긴 문장 해석

고객센터 문서에 `환불은 가능하지만 배송비는 제외된다`라는 문장이 앞부분에 있고, 뒤쪽 FAQ에서 `최종 환불 금액은?`을 다시 묻는 상황을 생각해 보겠습니다. 사람이 문서를 대충 읽을 때는 보통 질문 바로 근처 문장만 다시 보고 `환불 가능`만 기억한 채 답을 정리하기 쉽습니다. 그런데 실제로는 앞쪽의 `배송비는 제외` 조건이 핵심이라, 그 문장을 놓치면 환불 금액을 과하게 안내하는 오답이 나올 수 있습니다. basic RNN은 긴 문장을 따라가며 이런 앞쪽 조건을 상태 안에 계속 보존해야 하므로, 뒤로 갈수록 중요한 단서가 흐려질 수 있습니다. attention 관점에서는 현재 답을 만들 때 앞부분의 `배송비는 제외` 위치를 더 직접 참고할 수 있어, 오래전 단서를 다시 끌어오기 쉬워집니다.

### 사례 2. 번역

긴 번역 문장에서 주어가 앞에 있고 동사가 한참 뒤에 나오면, 중간에 수식어가 많이 끼어들 수 있습니다. 사람이 손으로 번역할 때도 보통은 `지금 보고 있는 단어 주변`을 먼저 읽다가, 주어와 동사의 연결이 멀어지면 문장 앞을 다시 확인하게 됩니다. 예를 들어 문장 초반의 인물 주어가 뒤쪽 동사의 시제와 수를 결정하는데, 중간 설명이 길어지면 그 연결이 쉽게 흐려질 수 있습니다. 순차 상태에만 의존하면 모델은 이 `앞으로 다시 돌아가 확인하는 행동`을 직접 하기가 어렵고, 앞의 핵심 단서를 뒤 시점까지 안정적으로 유지하지 못할 수 있습니다. attention은 현재 번역 중인 위치가 문장 앞의 중요한 단어를 다시 바라보게 만들어, 멀리 떨어진 대응 관계를 더 직접 다루는 데 도움을 줍니다.

### 사례 3. 시계열 이상 탐지

설비 센서 데이터에서 평소에는 안정적이던 값이 한참 뒤에 급격히 흔들렸는데, 그 원인이 초반 설정 단계의 작은 이상 신호에 있을 수 있습니다. 사람이 단순 규칙으로 보려 하면 보통 `최근 10초 평균`이나 `현재 임계치 초과 여부`처럼 가까운 구간만 먼저 확인합니다. 하지만 실제 고장은 초반의 작은 흔들림과 뒤쪽의 큰 이상이 이어진 결과일 수 있어, 최근 값만 보면 원인을 놓치기 쉽습니다. 예를 들어 초반의 작은 진동 증가가 한동안 누적되다가 뒤늦게 큰 온도 상승으로 이어졌다면, 마지막 구간만 봐서는 왜 고장이 났는지 설명하기 어렵습니다. 상태가 여러 step을 지나며 희석되면 모델도 초반 신호를 뒤 판단에 약하게 반영할 수 있습니다. 이때 필요한 시점끼리 더 직접 연결해 보는 관점은, 왜 장기 의존성과 attention 문제가 함께 언급되는지를 더 분명하게 보여 줍니다.

세 사례에서 공통으로 확인해야 할 결과는 먼 단서를 끝까지 그대로 들고 가기보다, 필요한 앞 위치를 다시 더 직접 참고할 수 있어야 한다는 점입니다. 긴 문장 해석에서는 예외 조건을 놓치지 않는지, 번역에서는 앞 주어와 시제 단서가 끝까지 유지되는지, 시계열 이상 탐지에서는 초반 이상 신호와 마지막 경보가 실제로 함께 읽히는지를 보면 충분합니다.

| 사례 | 초반에 꼭 남아 있어야 하는 단서 | 중간 간격이 길어질수록 생기는 문제 | 이 절에서 확인할 결과 |
| --- | --- | --- | --- |
| 긴 문장 해석 | `배송비는 제외` 같은 앞 조건 | 뒤 질문 시점에는 핵심 예외 조건이 흐려질 수 있다 | 최종 답변이 앞 조건까지 함께 반영하는가 |
| 번역 | 문장 앞 주어, 시제, 수 일치 단서 | 중간 수식어가 길어질수록 앞뒤 대응이 약해질 수 있다 | 문장 끝에서도 앞 단서가 유지되는가 |
| 시계열 이상 탐지 | 초반의 작은 진동 증가나 설정 이상 | 최근 값만 남고 초기 이상 징후가 희미해질 수 있다 | 마지막 경보가 초반 이상 신호까지 반영하는가 |

## 이를 아주 단순하게 그리면

```mermaid
--8<-- "assets/part-05/chapter-12/long-term-dependency-flow-ko.mmd"
```

이 도식에서 확인해야 할 결과는 오래전 입력의 중요한 단서가 상태 갱신을 거치며 현재 결정 단계에 도달할수록 점점 약해질 수 있다는 점입니다.

## 연습 및 예제

이번 예제의 목표는 `초반 규칙`과 `마지막 질문` 사이의 간격이 길어질수록, 순차 상태가 앞 단서를 얼마나 빨리 잃는지 직접 확인하는 것입니다. 동시에 같은 문맥을 `직접 다시 찾는 방식`과 비교해 장기 의존성 문제가 왜 생기는지도 봅니다.

입력:

- 문서 맨 앞의 핵심 규칙 한 줄
- 길이가 다른 중간 설명 구간
- 문서 끝의 같은 질문 한 줄

출력:

- 간격 길이별 최종 상태값
- 상태 기반 판정 결과
- 질문 시점에서의 상태 기반 핵심 단서 최소값
- 앞 규칙을 다시 찾는 direct reference 판정 결과
- 질문과 규칙 줄 사이의 direct match score

문제 상황:

- 긴 문맥에서는 앞에서 본 규칙이 뒤 질문 시점까지 얼마나 남는지 순차 상태만으로는 약해질 수 있다

확인할 개념:

- 순차 상태는 시간이 길어질수록 앞 단서를 약하게 남길 수 있다
- 직접 참조와 상태 기반 판단을 비교하면 장기 의존성 문제가 더 직관적으로 보인다

입력(input):

위에 정리한 규칙 문장, 질문 문장, 문서 줄 목록을 사용합니다.

```python
rule = "Rule: shipping fee is excluded from refunds."
question = "Question: what is the final refund amount?"

def sequential_state(document, decay=0.72):
    state = {"refund": 0.0, "exclude": 0.0, "fee": 0.0}
    for line in document:
        lowered = line.lower()
        for key in state:
            state[key] *= decay
        if "refund" in lowered:
            state["refund"] += 1.0
        if "exclude" in lowered or "excluded" in lowered:
            state["exclude"] += 1.0
        if "fee" in lowered:
            state["fee"] += 1.0
    support = round(min(state.values()), 3)
    decision = "keeps exclusion" if support >= 0.45 else "loses exclusion"
    return {key: round(value, 3) for key, value in state.items()}, support, decision

def direct_reference(document):
    matches = []
    for idx, line in enumerate(document[:-1], start=1):
        lowered = line.lower()
        score = 0
        for keyword in ["refund", "excluded", "fee"]:
            if keyword in lowered:
                score += 1
        matches.append((score, idx, line))
    best = max(matches)
    decision = "keeps exclusion" if best[0] == 3 else "loses exclusion"
    return best, decision

for gap in [1, 3, 6]:
    filler = [f"Detail line {i}: general customer guidance only." for i in range(1, gap + 1)]
    document = [rule] + filler + [question]
    state_snapshot, state_support, state_decision = sequential_state(document)
    best_match, direct_decision = direct_reference(document)
    print(f"[gap={gap}]")
    print("document_length =", len(document))
    print("state_snapshot =", state_snapshot)
    print("state_support =", state_support)
    print("state_decision =", state_decision)
    print("direct_match_score =", best_match[0])
    print("best_direct_match =", best_match[2])
    print("direct_decision =", direct_decision)
    print()
```

출력에서는 gap이 커질수록 state_support가 약해지고 direct_match_score는 유지되는지부터 보면 됩니다.

```text
[gap=1]
document_length = 3
state_snapshot = {'refund': 1.518, 'exclude': 0.518, 'fee': 0.518}
state_support = 0.518
state_decision = keeps exclusion
direct_match_score = 3
best_direct_match = Rule: shipping fee is excluded from refunds.
direct_decision = keeps exclusion

[gap=3]
document_length = 5
state_snapshot = {'refund': 1.269, 'exclude': 0.269, 'fee': 0.269}
state_support = 0.269
state_decision = loses exclusion
direct_match_score = 3
best_direct_match = Rule: shipping fee is excluded from refunds.
direct_decision = keeps exclusion

[gap=6]
document_length = 8
state_snapshot = {'refund': 1.1, 'exclude': 0.1, 'fee': 0.1}
state_support = 0.1
state_decision = loses exclusion
direct_match_score = 3
best_direct_match = Rule: shipping fee is excluded from refunds.
direct_decision = keeps exclusion
```

- 같은 규칙과 같은 질문이라도, 둘 사이의 간격이 길어질수록 순차 상태 안의 `exclude`, `fee` 단서가 빠르게 약해집니다
- `state_support`는 질문 시점에서 핵심 단서가 얼마나 남아 있는지를 보여 주며, gap이 길어질수록 빠르게 줄어듭니다
- 상태 기반 방식은 중간 설명 줄이 늘어나면 앞의 핵심 예외 조건을 잃기 쉬워집니다
- 직접 다시 찾는 방식은 간격이 길어져도 같은 규칙 줄을 다시 집어 올 수 있고, 여기서는 `direct_match_score`가 계속 3으로 유지됩니다

## 이 예제를 attention 직관으로 다시 보면

이 장난감 코드는 attention 자체를 구현한 것은 아닙니다. 하지만 읽어야 할 연결은 분명합니다.

- 순차 상태 쪽은 `앞 단서를 상태 안에 계속 남겨 둘 수 있는가`가 핵심입니다.
- direct reference 쪽은 `현재 질문이 필요할 때 앞 단서를 다시 집어 올 수 있는가`가 핵심입니다.

즉, 장기 의존성 문제를 오래전 단서의 `보존` 문제로 보면 RNN/LSTM/GRU 쪽과 연결되고, 필요한 단서의 `재참조` 문제로 보면 attention 쪽과 연결됩니다. 이 구분이 잡혀야 다음 절 P5-13.1에서 attention을 `가중치 계산 공식`이 아니라 `필요한 위치를 직접 다시 보는 발상`으로 자연스럽게 읽을 수 있습니다.

장기 의존성 문제는 순차 모델링 역사에서 매우 중요한 전환점입니다. 왜냐하면 이 문제를 이해해야:

- 왜 basic RNN만으로는 부족했는지
- 왜 LSTM과 GRU가 강한 영향력을 가졌는지
- 왜 결국 attention과 Transformer가 큰 전환을 만들었는지

를 하나의 흐름으로 설명할 수 있기 때문입니다.

바로 앞의 P5-12.1에서 `순차 상태를 이어받는 구조`를 보았다면, 이제는 그 구조가 어디서 막히는지를 이해해야 합니다. 단순히 구조 이름을 외우는 대신, `무엇이 문제였기 때문에 다음 구조가 나왔는가`를 보여 주어야 attention과 Transformer가 왜 필요했는지 더 자연스럽게 읽을 수 있습니다.

여기서 한 번 멈추고, `언제 순차 상태 구조 설명만으로는 부족하고 장기 의존성 문제를 따로 꺼내야 하는가`를 짧게 고정해 두면 다음 attention 절로 넘어갈 때 전환 이유가 더 분명해집니다.

| 먼저 떠올릴 질문 | 장기 의존성 관점이 먼저 필요한 이유 | 바로 다음 절에서 이어질 것 |
| --- | --- | --- |
| 왜 중요한 앞 단서가 뒤 판단까지 그대로 남지 않는가 | 상태를 계속 갱신하는 구조에서는 먼 단서가 희미해질 수 있기 때문 | 필요한 위치를 현재 시점에 다시 직접 보는 attention |
| 왜 LSTM과 GRU가 있어도 문제가 완전히 끝나지 않았는가 | 기억 관리는 나아져도 여전히 순차 전달 부담과 거리 문제가 남기 때문 | 직접 참조 구조로의 발상 전환 |
| 왜 attention이 단순 성능 개선이 아니라 구조 전환처럼 읽히는가 | `상태에 오래 담아 둔다`에서 `필요할 때 다시 본다`로 질문 자체가 바뀌기 때문 | self-attention과 Transformer 확장 |

## 체크리스트

- 장기 의존성(long-term dependency)이 어떤 문제를 뜻하는지 설명할 수 있는가?
- 오래전 정보를 유지하기 어려운 점이 왜 attention으로 이어지는지 말할 수 있는가?
- 장기 의존성은 오래전 정보가 중요한데도 충분히 유지되지 않는 문제라는 점을 설명할 수 있는가?
- 기본 RNN에서는 시간이 길어질수록 오래전 단서가 약해지기 쉽다는 점을 말할 수 있는가?
- LSTM과 GRU는 이 문제를 더 잘 다루려는 구조라는 점을 설명할 수 있는가?
- 장기 의존성을 `기억이 조금 약해진다` 정도가 아니라 `오래전 단서가 없으면 현재 판단 자체가 흔들리는가`의 문제로 설명할 수 있는가?
- 상태 보존과 직접 참조를 서로 다른 발상으로 나눠 말할 수 있는가?
- 다음 장의 attention을 읽을 때도 먼저 `어떤 앞 위치를 다시 봐야 하는가`를 떠올릴 준비가 되어 있는가?

## 출처와 참고 자료

- Sepp Hochreiter, Jürgen Schmidhuber, `Long Short-Term Memory`, Neural Computation, 1997, 확인 날짜: 2026-06-29.
- Yoshua Bengio, Patrice Simard, Paolo Frasconi, `Learning Long-Term Dependencies with Gradient Descent is Difficult`, IEEE Transactions on Neural Networks, 1994, 확인 날짜: 2026-06-29.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
