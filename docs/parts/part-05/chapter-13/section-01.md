# P5-13.1 어텐션(Attention)의 직관

> Section ID: `P5-13.1`
> Version: `v2026.07.19`

P5-12.2에서는 장기 의존성(long-term dependency) 때문에 순차 모델이 오래전 정보를 충분히 유지하기 어려울 수 있다는 점을 보았습니다. 여기서 다음 질문이 생깁니다.

현재 위치가 필요한 과거 정보를 더 직접적으로 참고하게 만들 수는 없는가?

이 질문에 대한 대표적 답이 어텐션(Attention)입니다.

어텐션은 현재 계산에 정말 중요한 위치나 토큰(token)에 더 큰 비중을 두어, 필요한 정보를 더 직접적으로 참고하게 만드는 방식입니다.

attention의 기본 문제의식을 다시 짧게 잡아야 할 때는 개념사전의 [어텐션(Attention)](../../../reference/concept-glossary.md#attention) 항목을 기준으로 다시 읽습니다.

## 이 절의 범위

- 어텐션은 어떤 문제를 해결하려는가?
- `필요한 위치를 더 강하게 본다`는 말은 무엇을 뜻하는가?
- attention은 RNN 계열과 어떻게 연결되는가?
- 왜 attention이 큰 전환점처럼 느껴졌는가?

이 절에서 먼저 닫아야 하는 핵심은 `오래 기억하려고만 애쓰기보다, 지금 필요한 위치를 다시 찾아보는 방식이 필요했다`는 점입니다.

self-attention과 Transformer 연결은 다음 절과 다음 장에서 이어서 다룹니다. query, key, value와 multi-head attention의 입문적 설명은 보충학습 P5-13.3에서 회수합니다.

## 이 절의 목표

- attention을 `중요한 위치를 더 직접적으로 참고하는 방식`으로 설명할 수 있습니다.
- 장기 의존성 문제와 attention의 연결을 말할 수 있습니다.
- 초기 encoder-decoder와 운영 문서 변환 장면에서 왜 attention이 중요했는지 설명할 수 있습니다.
- 실행 가능한 Python 예제로 가중 평균 형태의 attention 직관을 확인할 수 있습니다.

## attention은 왜 등장했나

기본 RNN이나 encoder-decoder 구조에서는 긴 입력 전체를 하나의 압축된 상태(state)에 담으려는 경향이 있었습니다. 입력이 짧을 때는 버틸 수 있어도, 길이가 늘어나면 지금 꼭 필요한 단서가 그 압축된 상태 안에서 흐려지기 쉬웠습니다.

attention은 이 문제를 다르게 봅니다.

`현재 출력을 만들 때, 입력 전체 중 어디를 더 참고해야 하는지를 직접 계산하자.`

즉, 오래전 정보를 무조건 상태 안에만 눌러 담아 두는 대신, 필요할 때 다시 꺼내 보려는 발상입니다. 이 절에서 attention을 읽는 핵심은 `더 오래 기억하게 만들기`보다 `지금 필요한 위치를 다시 찾게 만들기`에 있습니다.

## `더 강하게 본다`는 말은 무엇인가

attention의 핵심은 현재 과업과 더 관련 있는 위치에 더 큰 가중치를 두고 정보를 다시 모으는 데 있습니다. 중요한 것은 모든 위치를 미리 똑같이 취급하지 않는다는 점입니다.

- 현재 위치에서
- 과거 입력이나 다른 위치들을 훑어보고
- 그중 더 중요한 위치에 더 큰 점수를 주고
- 그 점수를 바탕으로 정보를 모읍니다

즉, 모든 위치를 똑같이 보는 것이 아니라, `현재 과업과 더 관련 있는 위치를 더 크게 참고하는 방식`입니다. 그래서 같은 입력을 두고도 현재 질문이 달라지면, 다시 크게 봐야 할 위치도 함께 달라질 수 있습니다.

이 흐름을 아주 짧게 표로 보면 다음과 같습니다.

| 단계 | 지금 일어나는 일 |
| --- | --- |
| 1 | 현재 위치가 다른 위치들을 훑는다 |
| 2 | 관련 있는 위치에 더 큰 점수를 준다 |
| 3 | 그 점수를 반영해 문맥 정보를 모은다 |

아래 짧은 문장 예시는 현재 문장이 뒤 문장에서 이유 단서를 더 크게 참고하는 장면으로 `훑기 -> 점수 주기 -> 문맥 모으기`를 보여 줍니다.

```text
재기동은 연기되었다. 이유는 압력 불안정이었다.
```

만약 지금 모델이 `이유는 무엇인가?`에 답하려 한다면, 모든 단어를 같은 비중으로 보는 것이 아니라 `압력`, `불안정`, `이유` 같은 위치에 더 큰 비중을 둘 것입니다. 즉, attention에서 `더 강하게 본다`는 말은 `현재 질문과 더 직접 연결된 위치가 계산에 더 크게 반영된다`는 뜻입니다.

## 직접 참조 예시로 보면 왜 직관적인가

attention은 역사적으로 sequence-to-sequence 번역(sequence-to-sequence translation) 맥락에서 큰 힘을 얻었지만, 독자 입장에서는 `현재 문구를 만들 때 입력 어디를 다시 봐야 하는가`라는 작업 지시 변환 장면으로 읽는 편이 더 직접적입니다.

예를 들어 영문 운전 절차를 한국어 작업 지침으로 바꿀 때 현재 출력 문구가 어떤 단어를 만들고 있을 때:

- 입력 문장 전체 중 어떤 단어가 지금 가장 관련 있는지
- 그 위치를 더 강하게 참고할 수 있습니다

즉, 출력 단어 하나를 만들 때마다 입력 전체를 훑되, 필요한 위치에 더 무게를 두는 방식입니다.

`attention은 지금 작성하는 작업 지침 문구에 맞는 입력 위치를 찾아 더 많이 참고하게 하는 장치다.`

## attention은 장기 의존성 문제에 어떻게 답하나

장기 의존성 문제는 오래전 정보가 현재까지 약해지거나 사라질 수 있다는 것이었습니다. attention은 이 문제에 대해 다음처럼 답합니다.

- 굳이 오래전 정보를 상태 안에 희미하게만 남겨 두지 말고
- 현재 step에서 과거 위치 전체를 다시 훑어보며
- 중요한 곳을 직접 선택해서 참고하자

즉, attention은 `기억을 더 오래 보존하는 것`보다, `필요한 정보를 더 잘 찾아오는 것`에 가까운 발상입니다.

P5-12.2를 `상태가 멀리 갈수록 정보가 희미해질 수 있다`는 절로 읽었다면, 이 절은 그 문제를 `그러면 지금 필요한 위치를 다시 보자`로 뒤집는 절입니다.

이 전환만 따로 아주 짧게 압축하면 다음 흐름으로 읽을 수 있습니다.

```mermaid
--8<-- "assets/part-05/chapter-13/attention-direct-reference-bridge-ko.mmd"
```

이 도식의 핵심은 `오래 들고 가는 것`에서 `필요할 때 다시 찾는 것`으로 손잡이가 바뀐다는 점입니다.

## 이를 아주 단순하게 그리면

```mermaid
--8<-- "assets/part-05/chapter-13/attention-focus-flow-ko.mmd"
```

이 도식은 attention을 `필요한 위치 탐색 -> 가중치 부여 -> 집중된 문맥 형성`으로 압축합니다.

같은 입력 문장이라도 현재 질문이 바뀌면 다시 봐야 할 위치가 어떻게 달라지는지 한 번 더 짧게 고정하면 다음처럼 볼 수 있습니다.

```mermaid
--8<-- "assets/part-05/chapter-13/attention-question-shift-ko.mmd"
```

이 비교 도식에서 먼저 붙잡아야 할 점은 다음과 같습니다.

- 입력 문장은 같아도 `무엇을 묻는가`가 바뀌면 높은 비중을 받는 위치도 함께 바뀝니다.
- 그래서 attention의 핵심은 `중요한 문장을 미리 하나 정해 두는 것`이 아니라, 현재 질문에 따라 다시 참조 위치를 고르는 데 있습니다.
- 이 감각이 잡혀야 다음 절의 self-attention에서 `토큰마다 다시 보는 위치가 달라진다`는 설명으로 더 자연스럽게 넘어갈 수 있습니다.

## attention을 `요약`으로 오해하면 어디서 어긋나나

attention을 처음 접하면 `중요한 부분만 남기는 요약 장치`처럼 느끼기 쉽습니다. 하지만 여기서는 조금 더 정확하게 구분하는 편이 좋습니다.

- attention은 현재 계산에서 더 중요한 위치에 더 큰 비중을 둡니다
- 그래서 전체 문맥이 `중요한 부분이 더 강조된 상태`로 다시 읽힐 수 있습니다
- 하지만 attention 자체가 입력 길이를 줄이거나 내용을 따로 압축 저장하는 것은 아닙니다

즉, attention의 핵심은 `문맥을 줄이는 것`보다 `문맥 안에서 무엇을 더 크게 참고할 것인가`에 있습니다.

이 차이를 한 문장으로 줄이면 다음과 같습니다.

`attention은 문맥을 짧게 요약하는 장치라기보다, 현재 계산에서 중요한 위치를 더 크게 읽게 만드는 장치다.`

## 왜 큰 전환점처럼 보였나

attention은 단순히 성능을 조금 올린 보조 기법이 아니라, sequence modeling의 관점을 바꾸는 효과가 있었습니다.

이전에는:

- 긴 문장을 압축 상태에 넣는 방식이 중심이었다면

attention 이후에는:

- 입력 전체를 두고 필요한 위치를 선택적으로 참고하는 방식이 더 강조되었습니다

이 변화는 이후 self-attention과 Transformer로 이어지며, RNN 중심 흐름에서 큰 전환을 만들어 냈습니다. 현재 절에서 독자가 붙잡아야 하는 것도 바로 이 지점입니다. `정보를 오래 들고 갈까`에서 `필요한 위치를 다시 볼까`로 질문 자체가 바뀌었다는 점입니다.

## 사례 및 예시

### 대표 사례. 운전 절차 변환 문서

영문 운전 절차 문서를 한국어 작업 지침으로 바꾼다고 생각해 보겠습니다. 사람은 처음에는 왼쪽에서 오른쪽으로 차례로 읽으며 바로 옮기면 된다고 느끼기 쉽습니다. 하지만 실제로는 지금 만들고 있는 한국어 지침 문구가 입력 문장 전체 중 어느 위치와 가장 직접 연결되는지 다시 확인해야 할 때가 많습니다. 예를 들어 문장 앞쪽의 주체와 뒤쪽의 안전 조건 관계를 놓치면, 문장은 문법상 맞아 보여도 누가 무엇을 먼저 해야 하는지가 어색해질 수 있습니다. 사람이 절차 문서를 옮길 때도 보통 현재 쓰는 단어에 맞는 입력 위치를 다시 눈으로 찾아봅니다. attention은 바로 이 `지금 출력할 문구에 가장 관련 있는 입력 위치를 더 강하게 본다`는 직관과 잘 맞고, 긴 문장에서 멀리 떨어진 핵심 단어를 놓치는 문제를 줄이는 방향으로 이해할 수 있습니다.
그래서 이 사례에서 확인해야 할 결과는 현재 번역 문구가 가까운 단어만 따라가지 않고, 앞 주체와 뒤 안전 조건을 실제로 다시 함께 참조해 조건부 작업 지침으로 닫히는가입니다.

같은 관점은 장애 메모 요약이나 매뉴얼 질의응답에도 그대로 이어집니다. 다만 이 절에서 붙잡을 핵심은 도메인 이름이 아니라, `현재 질문이나 출력 목표가 바뀌면 다시 크게 참고할 위치도 함께 바뀌는가`입니다.

세 사례를 같이 놓고 보면 attention을 `중요한 부분을 대충 요약하는 장치`보다 `현재 질문이나 출력 목표에 따라 다시 참고할 위치를 바꾸는 구조`로 읽어야 하는 이유가 더 분명해집니다.

| 사람이 먼저 보기 쉬운 기준 | attention 관점으로 다시 읽는 기준 |
| --- | --- |
| 문장 전체를 한 번 읽어 둔 인상만으로도 현재 질문에 답할 수 있다고 느낀다 | 현재 질문이나 출력 목표가 바뀌면 다시 봐야 할 위치도 함께 바뀐다 |
| 중요한 문장은 처음부터 고정되어 있다고 본다 | 같은 문서라도 `무엇을 묻는가`에 따라 높은 비중을 받는 위치가 달라진다 |
| attention을 단순한 요약 장치처럼 이해하기 쉽다 | 핵심은 길이를 줄이는 것이 아니라 현재 과업에 맞게 참조 비중을 다시 나누는 데 있다 |

## 연습 및 예제

이번 예제의 목표는 여러 위치 중 중요한 곳에 더 큰 비중을 주고 가중 평균을 만드는 attention 직관을 확인하는 것입니다. 단순 숫자 평균이 아니라, `질문`과 `문장 후보`가 있을 때 어디를 더 보게 되는지를 작은 질의응답 장면으로 바꿔 보겠습니다.

문제 상황:

- 모든 입력 위치를 똑같이 평균내면 현재 질문과 직접 관련된 정보가 흐려질 수 있다

입력:

- 질문 두 개
- 세 개의 문장 후보 값
- 질문마다 달라지는 후보 관련도 점수

출력:

- 모든 후보를 똑같이 평균낸 baseline 문맥값
- 질문마다 달라지는 정규화된 비중
- 질문마다 달라지는 문맥값
- 어떤 후보가 가장 크게 반영되는지에 대한 요약

확인할 개념:

- attention은 모든 후보를 같은 비중으로 보는 대신 현재 질문에 더 관련된 위치를 더 크게 본다
- baseline 평균과 attention 가중 평균을 비교해야 왜 중요한 위치 선택이 필요한지 보인다
- 같은 후보 묶음도 질문이 달라지면 비중이 다시 나뉜다
- 질의응답 장면으로 바꾸면 attention이 `어디를 더 볼 것인가`의 문제라는 점이 분명해진다

코드를 보기 전에, 같은 후보를 두고 질문만 바꾸면 어디에 weight가 몰릴지 먼저 예상해 보면 좋습니다.

| 질문 | baseline에서 생기기 쉬운 오해 | attention에서 먼저 예상할 변화 |
| --- | --- | --- |
| `압력 해소 유지 시간은?` | 모든 후보가 비슷하게 섞여도 된다고 느끼기 쉽다 | `pressure_hold_time` 쪽 weight가 가장 커져야 한다 |
| `냉각수 유량 기준은?` | 같은 후보 집합이면 앞 질문과 비슷한 문맥이 나올 것이라고 느끼기 쉽다 | `coolant_flow_limit` 쪽 weight가 가장 커져야 한다 |
| 두 질문 모두 | 평균값 하나면 충분하다고 느끼기 쉽다 | 질문이 바뀌면 같은 후보라도 context가 달라져야 한다 |

입력(input):

위에 정리한 질문과 문장별 점수 후보를 사용합니다.

```python
# 같은 후보 문장 묶음에서 질문이 바뀔 때 baseline 평균과 attention 가중 평균이 어떻게 다른 context를 만드는지 비교하는 예제입니다.
import math

question = "압력 해소 유지 시간은?"
flow_question = "냉각수 유량 기준은?"
sentences = {
    "pressure_hold_time": 3.0,
    "coolant_flow_limit": 12.0,
    "high_temp_exception": 5.0,
}
scores_for_pressure = {
    "pressure_hold_time": 2.5,
    "coolant_flow_limit": 0.9,
    "high_temp_exception": 0.3,
}
scores_for_flow = {
    "pressure_hold_time": 0.8,
    "coolant_flow_limit": 2.4,
    "high_temp_exception": 0.4,
}

ordered_names = list(sentences.keys())
values = [sentences[name] for name in ordered_names]

uniform_weight = 1 / len(values)
baseline_context = sum(uniform_weight * v for v in values)

def run_attention(question, score_table):
    raw_scores = [score_table[name] for name in ordered_names]
    exp_scores = [math.exp(s) for s in raw_scores]
    total = sum(exp_scores)
    weights = [s / total for s in exp_scores]
    context = sum(w * v for w, v in zip(weights, values))

    print("question =", question)
    print("baseline_uniform_context =", round(baseline_context, 3))
    for name, weight in zip(ordered_names, weights):
        print(name, "weight =", round(weight, 3), "value =", sentences[name])
    print("weights =", [round(w, 3) for w in weights])
    print("context =", round(context, 3))
    print("shift_from_baseline =", round(context - baseline_context, 3))
    print()

run_attention(question, scores_for_pressure)
run_attention(flow_question, scores_for_flow)
```

출력에서는 질문 관련 후보에 weight가 얼마나 몰렸는지부터 보면 됩니다.

```text
question = 압력 해소 유지 시간은?
baseline_uniform_context = 6.667
pressure_hold_time weight = 0.762 value = 3.0
coolant_flow_limit weight = 0.154 value = 12.0
high_temp_exception weight = 0.084 value = 5.0
weights = [0.762, 0.154, 0.084]
context = 4.553
shift_from_baseline = -2.114

question = 냉각수 유량 기준은?
baseline_uniform_context = 6.667
pressure_hold_time weight = 0.151 value = 3.0
coolant_flow_limit weight = 0.748 value = 12.0
high_temp_exception weight = 0.101 value = 5.0
weights = [0.151, 0.748, 0.101]
context = 9.933
shift_from_baseline = 3.266
```

- baseline처럼 모든 후보를 똑같이 평균내면 문맥값은 `6.667`이 되어, 질문과 직접 관련 없는 `coolant_flow_limit`, `high_temp_exception` 값도 같은 비중으로 섞입니다
- `pressure_hold_time` 문장이 가장 큰 weight를 받습니다
- 그래서 최종 context는 압력 해소 유지 시간 문장의 영향을 가장 크게 받습니다
- `shift_from_baseline`이 음수라는 점은 질문과 직접 관련된 후보에 더 큰 비중이 실리면서, 문맥 표현이 `압력 해소 유지 시간` 쪽으로 더 끌려갔다는 뜻입니다
- 냉각수 유량 질문으로 바꾸면 같은 후보 집합이어도 `coolant_flow_limit`가 가장 큰 weight를 받으며 context도 유량 기준 쪽으로 올라갑니다
- 즉, attention은 모든 위치를 똑같이 평균내지 않고, 현재 질문과 더 관련 있는 위치를 더 크게 반영합니다

이 예제에서 먼저 볼 산출물은 질문별 attention 비중입니다. 압력 해소 유지 시간 질문에서는 `pressure_hold_time`의 비중이 가장 크고, 냉각수 유량 기준 질문에서는 `coolant_flow_limit`의 비중이 가장 큽니다.

![압력 해소 유지 시간 질문의 attention 비중](../../../assets/part-05/chapter-13/attention-pressure-question-weights-ko.png)

![냉각수 유량 기준 질문의 attention 비중](../../../assets/part-05/chapter-13/attention-flow-question-weights-ko.png)

두 번째로 볼 산출물은 문맥값입니다. baseline 평균은 두 질문을 구분하지 못해 `6.667`에 머물지만, attention context는 질문에 따라 `4.553`과 `9.933`으로 달라집니다.

![질문별 attention context와 baseline 평균 비교](../../../assets/part-05/chapter-13/attention-context-comparison-ko.png)

출력 숫자를 읽을 때도 `같은 후보 집합`과 `질문에 따라 달라지는 weight`를 분리해서 봐야 합니다.

| 비교 | 출력에서 먼저 보이는 것 | 평균만 보면 남기 쉬운 해석 | attention까지 보면 바뀌는 해석 |
| --- | --- | --- | --- |
| `baseline_uniform_context` | 두 질문 모두 baseline은 `6.667`로 같습니다. | 같은 후보 집합이면 문맥도 거의 같아야 할 것처럼 보입니다. | baseline은 질문을 반영하지 못해, 현재 필요한 위치가 바뀌어도 같은 평균값에 머뭅니다. |
| `pressure_hold_time` 질문 | `pressure_hold_time` weight가 `0.762`로 가장 큽니다. | 숫자 `3.0`이 작아서 문맥값이 단순히 내려간 것처럼 보일 수 있습니다. | 질문이 유지 시간에 맞춰져 있으므로, attention은 유지 시간 후보를 더 크게 참고하도록 비중을 다시 나눕니다. |
| `냉각수 유량 기준은?` 질문 | `coolant_flow_limit` weight가 `0.748`로 가장 큽니다. | 같은 후보인데 이번엔 숫자 큰 쪽이 우연히 선택된 것처럼 보일 수 있습니다. | 질문이 바뀌자 같은 후보 집합도 참조 비중이 다시 배분되어, 유량 기준 쪽 문맥이 더 크게 형성됩니다. |

## 이 예제를 질문-후보 비교 관점으로 다시 보면

앞의 숫자는 실제 단어 임베딩 전체를 계산한 것은 아니지만, 직관은 분명합니다.

- baseline 평균은 `문장들이 그냥 같이 있었다`는 사실만 반영합니다.
- attention 가중 평균은 `지금 질문이 무엇이냐`를 기준으로, 후보들 사이 비중을 다시 나눕니다.
- 그래서 질문이 `압력 해소 유지 시간`에서 `냉각수 유량 기준`으로 바뀌면 같은 후보 묶음이어도 가장 크게 참고하는 위치가 달라집니다.

즉, attention은 단순히 정보를 더 많이 모으는 방식이 아니라, `현재 질문에 맞게 어떤 정보를 더 크게 섞을지 다시 정하는 방식`입니다.

attention은 sequence-to-sequence 번역 연구에서 큰 영향력을 얻었고, 이후 self-attention과 Transformer로 이어지면서 현대 딥러닝의 핵심 문맥 참조 방식으로 자리 잡았습니다. 이 절에서 독자가 남겨야 할 결론은 간단합니다. attention은 `정보를 오래 들고 가는 구조`보다 `지금 필요한 위치를 다시 크게 보는 구조`에 더 가깝습니다. 다음 절 P5-13.2에서는 이 직접 참조 발상이 같은 시퀀스 안 토큰들이 서로를 다시 읽는 구조로 어떻게 이어지는지를 설명합니다.

## 체크리스트

- 어텐션(Attention)이 `필요한 위치를 다시 참고하는 방식`이라는 점을 설명할 수 있는가?
- 장기 의존성 문제와 어텐션의 연결을 말할 수 있는가?
- attention은 현재 계산에 중요한 위치를 더 크게 참고하는 방식이라는 점을 설명할 수 있는가?
- 이는 장기 의존성 문제에 대한 더 직접적인 응답이라는 점을 말할 수 있는가?
- attention을 `기억을 더 오래 남기는 방법`이 아니라 `지금 필요한 위치를 더 크게 다시 보는 방법`으로 설명할 수 있는가?
- baseline 평균과 가중 평균의 차이를 현재 질문 기준으로 설명할 수 있는가?
- 상태를 오래 보존하는 설명만으로는 왜 성능이 막히는지 부족할 때, attention의 직접 참조 관점을 먼저 떠올릴 수 있는가?
- 다음 절의 self-attention을 읽을 때도 먼저 `현재 토큰이 같은 시퀀스 안 어디를 다시 봐야 하는가`를 떠올릴 준비가 되어 있는가?

## 출처와 참고 자료

- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, `Neural Machine Translation by Jointly Learning to Align and Translate`, ICLR 2015, 확인 날짜: 2026-07-19. [https://arxiv.org/abs/1409.0473](https://arxiv.org/abs/1409.0473){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Kyunghyun Cho et al., `Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation`, arXiv, 2014, 확인 날짜: 2026-07-19. [https://arxiv.org/abs/1406.1078](https://arxiv.org/abs/1406.1078){: target="_blank" rel="noopener noreferrer" }
