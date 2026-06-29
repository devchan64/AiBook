# P4-13.2 self-attention으로 이어지는 흐름

P4-13.1에서는 attention을 `현재 계산에 중요한 위치를 더 크게 참고하는 방식`으로 설명했습니다. 이제 다음 질문이 바로 이어집니다.

그렇다면 입력과 출력이 따로 있는 번역 상황만이 아니라, 입력 안의 각 위치가 서로를 직접 참고하게 만들면 무엇이 달라지는가?

이 질문에 대한 핵심 답이 self-attention입니다.

self-attention은 시퀀스 안의 각 토큰이 같은 시퀀스의 다른 토큰들을 서로 참고하며, 현재 표현을 다시 계산하는 방식이다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- self-attention은 attention과 무엇이 다른가?
- 왜 `자기 시퀀스 안에서 서로 참조한다`는 발상이 중요한가?
- self-attention은 RNN과 어떤 점에서 계산 관점이 다른가?
- 왜 Transformer의 핵심으로 이어지는가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- query, key, value의 공식 유도
- multi-head attention의 구현 세부
- positional encoding의 수식 상세

Transformer 전체 구성은 P4-14.1, P4-14.2에서 이어서 다루고, context window와 실제 LLM 사용 제약은 Part 5의 P5-3.1, P5-3.2에서 다시 연결합니다. query, key, value의 공식 유도와 multi-head attention 세부 구현은 이 책의 현재 본편 범위 밖에 둡니다.

## 이 절의 목표

- self-attention을 `시퀀스 내부 토큰들 사이의 상호 참조`로 설명할 수 있습니다.
- self-attention이 RNN식 순차 전달과 다른 계산 감각을 준다는 점을 말할 수 있습니다.
- self-attention이 병렬 처리와 긴 문맥 문제에 어떤 장점을 주는지 말할 수 있습니다.
- 작은 Python 예제로 토큰 간 중요도 참조 직관을 확인할 수 있습니다.

## attention과 self-attention은 무엇이 다른가

attention은 넓게 보면 `현재 계산이 어떤 위치를 더 강하게 참고할지 정하는 방식`입니다. self-attention은 그 참조 대상이 같은 시퀀스 내부라는 점이 핵심입니다.

예를 들어 문장 안에서:

- 각 단어는 다른 단어들을 참고할 수 있고
- 현재 단어 표현은 전체 문장 안의 관련 토큰 정보를 다시 모아 계산할 수 있습니다

즉, self-attention은 `문장 바깥 정보를 가져오는 것`이 아니라, `문장 내부 관계를 다시 읽는 방식`입니다.

## 왜 이것이 중요한가

RNN은 보통 앞에서 뒤로, 혹은 양방향이라 해도 시간 흐름을 따라 상태를 전달하는 감각이 강합니다. self-attention은 이와 다르게, 현재 토큰이 필요할 때 멀리 떨어진 토큰도 비교적 직접 참고할 수 있게 합니다.

다음처럼 이해하면 충분합니다.

`RNN은 기억을 이어서 전달하는 방식에 가깝고, self-attention은 필요한 단어를 다시 찾아보는 방식에 가깝다.`

즉, 오래전 정보가 희미해지는 문제에 대해, self-attention은 더 직접적인 참조 경로를 만듭니다.

이 차이는 다음 표로 더 짧게 잡을 수 있습니다.

| 관점 | RNN 계열 | self-attention |
| --- | --- | --- |
| 기본 감각 | 상태를 다음 step으로 넘긴다 | 모든 토큰 사이 관련도를 다시 계산한다 |
| 먼 정보 접근 | 여러 step을 거쳐 전달된다 | 더 직접 참고할 수 있다 |
| 계산 느낌 | 순차 전달 | 관계 계산 |

## 문장 안에서 어떤 일이 일어나나

예를 들어 문장:

`The animal didn't cross the road because it was tired.`

에서 `it`이 무엇을 가리키는지 이해하려면, 문장 안 다른 단어와의 관계를 봐야 합니다. self-attention은 이런 관계를 설명하는 입문적 직관에 매우 잘 맞습니다.

각 토큰은:

- 자기 자신만 보는 것이 아니라
- 다른 토큰과의 관련도를 계산하고
- 더 중요한 토큰 정보를 더 많이 반영해
- 새로운 표현을 만듭니다

즉, self-attention은 토큰 표현을 문맥적으로 다시 쓰는 방식입니다.

## 왜 Transformer의 핵심이 되었나

self-attention이 중요한 이유는 단순히 `더 똑똑해 보여서`가 아닙니다. 계산 구조 자체를 바꾸기 때문입니다.

특히 독자 기준에서 중요한 차이는 다음 두 가지입니다.

1. 먼 위치를 더 직접 참고할 수 있습니다
2. 순차적으로만 상태를 전달하지 않아도 되어 병렬 계산과 잘 맞습니다

즉, self-attention은 장기 의존성 문제와 병렬 처리 요구를 동시에 더 잘 만족시키는 방향으로 보였습니다. 이것이 Transformer의 핵심이 된 이유 중 하나입니다.

## 이를 아주 단순하게 그리면

```mermaid
flowchart LR
  A["token 1"]
  B["token 2"]
  C["token 3"]
  D["token 4"]

  A --- B
  A --- C
  A --- D
  B --- C
  B --- D
  C --- D
```

이 도식은 각 토큰이 다른 토큰들을 서로 참고할 수 있다는 직관을 압축합니다. 실제 구현은 더 정교하지만, 입문 단계에서는 이 연결 감각이 가장 중요합니다.

## self-attention은 왜 병렬 처리와 잘 맞나

RNN은 시점 순서대로 상태를 넘기므로, 계산 흐름이 순차적이라는 감각이 강합니다. self-attention은 각 토큰의 관련도 계산을 더 행렬적인 방식으로 다루기 쉬워, GPU 병렬 처리와 잘 맞습니다.

다음처럼 기억하면 충분합니다.

`self-attention은 토큰들을 순서대로만 밀어내기보다, 한 번에 서로의 관계를 계산하는 방향에 더 가깝다.`

이 점은 Part 4의 GPU/배치/텐서 계산과도 자연스럽게 연결됩니다.

## 사례로 보기

### 사례 1. 문장 안 지시어 해석

고객 문의 문장에 `상품은 반품했지만 박스는 버리지 않았습니다. 그것이 문제인가요?` 같은 표현이 있다고 해 보겠습니다. 사람이 대충 읽을 때는 보통 `그것` 바로 근처 단어만 먼저 보고 뜻을 짐작하기 쉽습니다. 하지만 실제로는 `그것`이 박스를 가리키는지, 반품 사실을 가리키는지에 따라 답변 내용이 달라질 수 있습니다. 가까운 단어만 따라가면 이런 참조 관계를 놓치기 쉽습니다. self-attention은 현재 토큰이 문장 안 다른 위치를 다시 참고해 `무엇을 가리키는가`를 더 직접 계산한다는 직관을 줍니다. 이 사례는 self-attention이 단순히 옆 단어를 보는 것이 아니라, 문장 안 관계를 다시 읽는 방식임을 보여 줍니다.

### 사례 2. 문서 요약

긴 회의록을 요약할 때를 생각해 보겠습니다. 사람은 요약을 빨리 만들려 하면 보통 마지막 결론 문단이나 굵은 제목만 먼저 보고 핵심을 정리하려고 합니다. 하지만 실제로는 문서 앞부분의 전제 조건과 뒷부분의 최종 결정이 함께 있어야 정확한 요약이 됩니다. 앞뒤를 따로 읽으면 `무엇을 하기로 했는가`는 남아도 `왜 그렇게 했는가`나 `어떤 예외가 붙었는가`를 놓치기 쉽습니다. 예를 들어 마지막에 `배포를 연기한다`고 적혀 있어도, 중간의 장애 위험 설명과 앞부분의 고객 공지 조건을 함께 봐야 제대로 요약할 수 있습니다. self-attention은 현재 요약 표현을 만들 때 문서 앞뒤의 관련 표현을 함께 다시 참고하는 전역 참조(global reference) 직관과 잘 맞습니다. 그래서 이 사례는 긴 문서에서 멀리 떨어진 단서들을 한 문맥 안에서 다시 모아 읽는 필요를 보여 줍니다.

### 사례 3. 코드 이해

긴 함수 안에서 위쪽에 `discount_rate`가 정의되고, 아래쪽 여러 조건문과 최종 반환식에서 다시 쓰인다고 해 보겠습니다. 사람이 코드를 읽을 때도 보통 현재 줄 주변만 먼저 보다가 계산식이 헷갈리면 위로 다시 올라가 변수 정의를 확인합니다. 그런데 순차적으로만 읽는 감각으로는 중간에 예외 처리와 다른 변수들이 많이 끼어들 때, 처음 정의가 어떤 역할을 했는지 흐려지기 쉽습니다. 예를 들어 마지막 반환식에서 할인값이 왜 음수가 아닌지 이해하려면, 위쪽의 초기화와 중간 조건문 두세 곳을 함께 다시 봐야 할 수 있습니다. self-attention은 현재 토큰이 멀리 떨어진 변수 정의, 함수 호출, 조건 분기와의 관계를 더 직접 참고한다는 설명에 잘 맞습니다. 이 사례는 코드 이해에서도 self-attention이 `멀리 있는 중요한 줄을 다시 찾아보는 계산 감각`을 준다는 점을 보여 줍니다.

세 사례를 한 줄로 묶으면 다음과 같습니다.

| 상황 | self-attention이 잘 맞는 이유 |
| --- | --- |
| 대명사 해석 | 문장 안 관련 단어를 다시 찾아볼 수 있어서 |
| 문서 요약 | 앞뒤 핵심 표현을 함께 참조할 수 있어서 |
| 코드 이해 | 멀리 떨어진 정의와 사용 관계를 더 직접 볼 수 있어서 |

## 작은 Python 예제로 보기

이번 예제의 목표는 토큰 하나가 다른 토큰들의 정보를 가중 평균으로 다시 모아 새 표현을 만든다는 self-attention 직관을 확인하는 것입니다.

입력:

- 세 개의 토큰 값
- 현재 토큰이 각 토큰을 얼마나 참고할지에 대한 점수

출력:

- 정규화된 비중
- 새로 모인 표현

```python
import math

tokens = [1.0, 4.0, 8.0]
scores_for_current_token = [0.5, 2.0, 1.0]

exp_scores = [math.exp(s) for s in scores_for_current_token]
total = sum(exp_scores)
weights = [s / total for s in exp_scores]
new_representation = sum(w * t for w, t in zip(weights, tokens))

print("weights =", [round(w, 3) for w in weights])
print("new_representation =", round(new_representation, 3))
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
weights = [0.14, 0.629, 0.231]
new_representation = 4.501
```

이 결과에서 읽어야 할 핵심은 다음입니다.

- 현재 토큰 표현은 자기 자신만으로 결정되지 않고
- 다른 토큰들의 값도 함께 참고하며
- 더 중요한 토큰일수록 더 큰 비중을 갖습니다

즉, self-attention은 `문맥을 보고 표현을 다시 계산하는 방식`입니다.

## 역사와 커리큘럼 관점

self-attention은 attention이 번역 분야의 보조 메커니즘에 머무르지 않고, sequence modeling의 중심 계산 방식으로 이동하는 전환을 보여 줍니다. 그리고 이 흐름이 바로 Transformer의 핵심입니다.

커리큘럼 관점에서 이 절은 매우 중요합니다.

- attention을 단순한 보조 장치로 끝내지 않고
- 왜 self-attention이 구조 자체를 바꾸는 발상이었는지 설명하며
- Part 5의 LLM 설명에 직접 연결되기 때문입니다

즉, self-attention은 Part 4와 Part 5를 잇는 가장 중요한 개념 다리 중 하나입니다.

## 다음 절과의 연결

여기까지 오면 다음 질문이 남습니다.

- self-attention만으로 모델이 완성되는가?
- Transformer는 attention 외에 어떤 구성 요소를 함께 사용하며, 왜 RNN과 달랐는가?

이 질문은 바로 P4-14.1 Transformer의 기본 구성으로 이어집니다.

## 이 절에서 기억할 관점

- self-attention은 같은 시퀀스 안의 토큰들이 서로를 참고해 표현을 다시 계산하는 방식입니다.
- 이는 RNN식 순차 상태 전달과 다른 계산 감각을 제공합니다.
- self-attention은 먼 위치 참조와 병렬 계산에 유리한 방향을 보여 줍니다.
- Transformer는 이 self-attention을 핵심 계산 장치로 삼습니다.

## 체크리스트

- self-attention을 입문 수준에서 설명할 수 있는가?
- attention과 self-attention의 차이를 말할 수 있는가?
- self-attention이 RNN보다 어떤 계산 감각 차이를 주는지 설명할 수 있는가?
- 다음 절의 Transformer 구성으로 왜 자연스럽게 이어지는지 말할 수 있는가?

## 출처와 참고 자료

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-06-29.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, `Neural Machine Translation by Jointly Learning to Align and Translate`, ICLR 2015, 확인 날짜: 2026-06-29.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
