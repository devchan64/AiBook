# P5-14.1 트랜스포머(Transformer)의 기본 구성

Section ID: `P5-14.1`
Version: `v2026.07.12`

P5-13.2에서는 셀프 어텐션(self-attention)이 같은 시퀀스 내부 토큰들이 서로를 직접 참고하는 방식이며, 트랜스포머(Transformer)의 핵심 발상으로 이어진다고 설명했습니다. 여기서 다음 질문이 생깁니다.

그렇다면 트랜스포머는 셀프 어텐션 하나만 있는 구조인가, 아니면 그 주변에 어떤 기본 구성 요소들이 함께 있는가?

트랜스포머는 셀프 어텐션(self-attention)으로 문맥 관계를 읽고, 피드포워드 네트워크(feed-forward network)로 각 위치 표현을 다시 가공하며, 잔차 연결(residual connection)과 레이어 정규화(layer normalization)로 그 계산 블록을 무너지지 않게 이어 가는 구조로 이해할 수 있다.

블록 부품 이름이 다시 섞일 때는 개념사전의 [트랜스포머(Transformer)](../../../reference/concept-glossary.md#transformer), [피드포워드 네트워크(feed-forward network)](../../../reference/concept-glossary.md#feed-forward-network), [잔차 연결(residual connection)](../../../reference/concept-glossary.md#residual-connection), [레이어 정규화(layer normalization)](../../../reference/concept-glossary.md#layer-normalization) 항목을 함께 다시 보는 편이 좋습니다.

## 이 절의 범위

- 트랜스포머의 핵심 블록은 무엇으로 이루어지는가?
- 셀프 어텐션(self-attention), 피드포워드 네트워크(feed-forward network), 잔차 연결(residual connection), 레이어 정규화(layer normalization)는 각각 어떤 역할을 하나?
- 왜 이 구조가 RNN 이후 큰 전환점처럼 보였는가?
- encoder/decoder 세부 이전에 어떤 큰 지도를 먼저 잡아야 하는가?

이 절에서 먼저 붙잡아야 할 핵심은 `트랜스포머는 셀프 어텐션이라는 한 아이디어가 아니라, 문맥 읽기와 표현 가공, 블록 유지 장치를 한 묶음으로 가진 구조`라는 점입니다. 지금 장의 손잡이는 `필요한 위치를 어떻게 참고할까`에서 `그 참조 계산을 어떤 블록 구성으로 안정적으로 반복할까`로 옮겨 갑니다. 따라서 여기서는 optimizer나 regularization 같은 학습 절차보다, Transformer 블록 안에서 각 부품이 어떻게 역할을 나누는가를 먼저 읽습니다.

| 지금 이 절에서 읽는 것 | 아직 다음 절로 넘기는 것 |
| --- | --- |
| 셀프 어텐션, 피드포워드, 잔차 연결, 정규화가 한 블록 안에서 어떻게 역할을 나누는가 | 그 블록이 병렬 처리, 긴 문맥 비용, 계산 규모에서 무엇을 바꾸는가 |
| 블록 내부의 관계 읽기와 표현 가공 | 대규모 학습 절차와 long-context 최적화 |

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- multi-head attention의 수식 전개
- positional encoding의 상세 수학
- encoder-only, decoder-only, encoder-decoder 계열의 세부 아키텍처 분화

multi-head attention과 query, key, value의 입문적 설명은 보충학습 P5-13.3에서 회수합니다. 대신 병렬 처리와 긴 문맥의 장점은 P5-14.2에서 이어서 다루고, encoder-only, decoder-only, encoder-decoder의 세부 분화는 P6-3.1에서 LLM 관점으로 다시 비교합니다. 더 깊은 세부 아키텍처 분화와 수식 전개는 이 책의 현재 본편 범위 밖에 둡니다.

여기서는 Transformer 논문 전체를 따라가기보다, 블록 수준에서 무엇이 결합되어 있는지 먼저 잡습니다.

## 이 절의 목표

- Transformer를 self-attention 하나가 아니라 여러 핵심 부품의 조합으로 설명할 수 있습니다.
- 각 부품이 문맥 읽기, 표현 가공, 학습 안정화 중 어떤 역할을 하는지 말할 수 있습니다.
- 이후 다른 모델 계열을 볼 때도 Transformer의 기본 블록을 떠올릴 수 있습니다.
- 실행 가능한 Python 예제로 토큰 표현이 여러 단계를 거쳐 바뀌는 흐름을 직관적으로 확인할 수 있습니다.

## 이 절을 읽는 순서

1. 먼저 P5-13.2에서 본 self-attention이 Transformer 안에서 어느 자리에 놓이는지 확인합니다.
2. 그 다음 self-attention, feed-forward, residual, layer normalization의 역할을 나눠 읽습니다.
3. 이어서 이 부품들이 왜 하나의 반복 블록으로 묶였는지 봅니다.
4. 마지막에 왜 이 블록 구조가 이후 생성 모델의 기본 단위가 되었는지 정리합니다.

## Transformer를 아주 큰 그림으로 보면

먼저 다음 네 요소만 확실히 잡아도 충분합니다.

1. self-attention
2. feed-forward network
3. residual connection
4. layer normalization

이 네 가지를 간단히 말하면:

- self-attention: 서로 어떤 토큰을 참고할지 정한다
- feed-forward: 각 위치 표현을 더 가공한다
- residual connection: 원래 정보 흐름을 함께 남긴다
- layer normalization: 값의 스케일을 다루며 학습을 안정화한다

즉, Transformer는 `문맥 관계를 읽고 -> 표현을 가공하고 -> 정보 흐름을 안정적으로 유지하는 블록`의 반복 구조입니다.

역할 분담은 다음 표처럼 정리할 수 있습니다.

| 구성 요소 | 먼저 잡아야 할 역할 |
| --- | --- |
| self-attention | 다른 토큰과의 관계를 읽는다 |
| feed-forward | 각 위치 표현을 다시 가공한다 |
| residual connection | 원래 정보 흐름을 함께 남긴다 |
| layer normalization | 값 범위를 정리해 학습을 덜 흔들리게 한다 |

여기서 가장 자주 섞어 읽는 두 질문을 바로 갈라 두면 다음 절과의 경계가 더 선명해집니다.

| 지금 이 절에서 답하는 질문 | 아직 다음 절로 넘기는 질문 |
| --- | --- |
| `한 블록 안에서 attention, feed-forward, residual, normalization이 어떻게 역할을 나누는가` | `그 블록을 많이 반복할 때 왜 GPU 병렬 처리와 긴 문맥 계산에서 유리해지는가` |
| `표현이 어떤 순서로 읽히고 가공되는가` | `계산량, 처리 속도, 긴 문맥 비용이 어떻게 달라지는가` |

같은 토큰 표현 하나를 따라가며 보면, 각 부품의 역할 차이가 더 직접 보입니다.

| 같은 장면 | 먼저 봐야 할 부품 | 그 부품이 바로 하는 일 |
| --- | --- | --- |
| 현재 토큰이 문장 안 어디를 더 참고할지 정할 때 | self-attention | 다른 위치와의 관계를 읽어 필요한 문맥을 모은다 |
| 모아 온 문맥이 섞인 현재 표현을 더 다듬을 때 | feed-forward | 현재 위치 표현을 한 번 더 가공해 특징을 풍부하게 만든다 |
| 새 계산이 원래 입력 흐름을 너무 덮어쓰지 않게 할 때 | residual connection | 이전 표현을 함께 남겨 정보 흐름을 이어 준다 |
| 다음 계산으로 넘기기 전에 값 범위를 정리할 때 | layer normalization | 표현 크기와 분포를 정리해 계산을 덜 흔들리게 한다 |

P5-13.2를 `토큰들이 서로를 참고하는 계산`의 절로 읽었다면, 이 절은 그 계산이 실제 모델 안에서 `어떤 보조 부품들과 함께 한 블록을 이루는가`를 보여 주는 절입니다.

여기서 독자가 특히 붙잡아야 할 것은 `부품이 따로따로 흩어져 있는 구조`가 아니라는 점입니다. Transformer는 보통 다음 질문 순서로 한 블록을 읽으면 가장 이해가 쉽습니다.

1. 지금 토큰이 다른 토큰 중 어디를 더 참고할까?
2. 그렇게 모인 문맥을 현재 위치 표현에 어떻게 다시 반영할까?
3. 그 표현을 각 위치에서 한 번 더 가공할까?
4. 이 과정에서 원래 정보와 안정성을 어떻게 유지할까?

즉, Transformer 블록은 `관계 읽기 -> 위치별 가공 -> 안정적 전달`의 묶음으로 읽는 편이 더 자연스럽습니다.

## self-attention은 무엇을 담당하나

P5-13장에서 본 것처럼 self-attention은 각 토큰이 다른 토큰들을 서로 참고해 문맥적 표현을 다시 계산하는 역할을 합니다.

`self-attention은 지금 이 토큰을 이해하기 위해 문장 안의 어디를 더 봐야 하는지 정하는 장치다.`

핵심은 `관계 읽기`입니다.

## feed-forward network는 왜 필요한가

self-attention만으로는 토큰 간 관계를 읽을 수 있지만, 각 위치 표현을 더 비선형적으로 가공하는 과정도 필요합니다. 여기서 feed-forward network가 등장합니다.

핵심은 attention이 문맥 관계를 섞은 뒤, feed-forward가 각 위치 표현을 그 자리에서 더 비선형적으로 가공한다는 점입니다.

`attention이 다른 토큰과의 관계를 반영해 문맥을 섞는다면, feed-forward는 각 위치의 표현을 더 풍부하게 다시 가공하는 작은 MLP처럼 볼 수 있다.`

이 차이는 한 토큰만 놓고 봐도 읽을 수 있습니다. self-attention 단계는 `이 토큰이 다른 토큰에게서 무엇을 받아올까?`를, feed-forward 단계는 `받아온 문맥이 섞인 현재 표현을 이 위치에서 어떻게 다시 다듬을까?`를 묻습니다. 즉, attention은 `바깥과의 관계`, feed-forward는 `현재 위치 안에서의 가공`에 더 가깝습니다.

## residual connection은 왜 필요한가

딥러닝에서 층이 깊어질수록 정보가 지나치게 바뀌거나 학습이 불안정해질 수 있습니다. residual connection은 이전 표현을 다음 단계로 함께 흘려 보내는 장치로 볼 수 있습니다.

핵심은 완전히 새 계산만 믿지 않고, 원래 입력 표현도 함께 남겨 다음 단계로 보내 학습을 덜 흔들리게 하는 데 있습니다.

`완전히 새 계산만 믿지 말고, 원래 입력 표현도 함께 남겨 다음 단계로 보내는 안전장치`

residual connection은 정보 손실을 줄이고 학습을 더 안정적으로 만듭니다.

## layer normalization은 왜 등장하나

여러 층과 큰 행렬 연산을 반복하면 값의 스케일과 분포가 학습 안정성에 영향을 줄 수 있습니다. layer normalization은 각 위치 표현을 더 다루기 쉬운 범위로 정리해 학습을 돕는 장치입니다.

핵심은 표현값의 크기와 분포를 정리해, 다음 계산이 더 안정적으로 이어지게 만드는 데 있습니다.

`layer normalization은 표현값의 크기와 분포를 정리해, 다음 계산이 덜 흔들리도록 돕는 장치다.`

즉, Transformer는 `강한 attention`만이 아니라, `깊은 학습을 견디게 하는 안정화 장치들`도 함께 갖추고 있습니다.

## 이를 아주 단순하게 그리면

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-block-flow-ko.mmd"
```

이 도식은 Transformer 블록 하나를 입문 수준에서 압축한 것입니다.

이 흐름을 한 줄씩 다시 읽으면 다음과 같습니다.

- `self-attention`: 다른 토큰과의 관계를 반영한다
- `add + norm`: 원래 정보 흐름을 너무 잃지 않게 정리한다
- `feed-forward`: 각 위치 표현을 한 번 더 가공한다
- `add + norm`: 다시 안정적으로 다음 블록으로 넘긴다

즉, Transformer 블록은 `문맥을 섞고 끝나는 구조`가 아니라, `문맥을 섞은 뒤 그 표현을 다시 다듬고 안정적으로 전달하는 구조`입니다.

## 왜 이 구성이 중요했나

Transformer가 큰 전환점처럼 보인 이유는 단순히 새로운 층 하나를 추가했기 때문이 아닙니다. 이 절 범위에서 먼저 봐야 할 핵심은 다음 부품들이 `반복 가능한 한 블록`으로 결합되었다는 점입니다.

- attention 중심의 문맥 참조
- 위치별 표현을 다시 가공하는 feed-forward
- 원래 흐름과 값 범위를 유지하는 residual, normalization

즉, Transformer는 `sequence modeling의 핵심 계산 방식`을 새 블록 단위로 다시 묶은 아키텍처였습니다.

여기서 한 번 멈추고, `언제 attention 개념 자체보다 Transformer 블록 구성 관점부터 먼저 읽어야 하는가`를 짧게 고정해 두면 다음 절의 병렬 처리 설명으로 넘어갈 때 기준선이 덜 흔들립니다.

| 먼저 떠올릴 질문 | Transformer 기본 구성 관점이 먼저 필요한 이유 | 바로 다음 절에서 이어질 것 |
| --- | --- | --- |
| self-attention만으로 왜 모델이 끝나지 않는가 | 문맥 읽기 외에도 위치별 가공과 안정적 전달 장치가 함께 있어야 반복 블록이 성립하기 때문 | 이 블록을 반복할 때 계산 감각이 왜 달라지는가 |
| residual과 layer normalization은 왜 같이 언급되는가 | 강한 문맥 계산만이 아니라 깊은 블록 반복을 견디게 하는 안정화 축이 필요하기 때문 | 병렬 학습과 규모 확장에서 블록 반복이 어떤 의미를 갖는가 |
| feed-forward는 attention과 무엇이 다른가 | 관계 읽기와 위치별 가공을 분리해서 봐야 블록 내부 역할이 섞이지 않기 때문 | 긴 문맥과 GPU 계산에서 블록 전체가 어떻게 작동하는가 |

## 사례 및 예시

사례에 들어가기 전에, 이 절에서 같은 Transformer 블록이 과업마다 어떻게 다르게 읽히는지만 먼저 짧게 고정하면 뒤 설명이 덜 길게 느껴집니다.

| 상황 | 먼저 봐야 할 관계 문제 | Transformer 블록이 도와주는 방식 |
| --- | --- | --- |
| 다국어 작업 지시 번역 | 문장 뒤 안전 조건이 앞쪽 조치 해석을 바꿀 수 있다 | 문장 전체 위치 관계를 함께 반영해 앞뒤 안전 조건을 다시 묶는다 |
| 장애 보고서 요약 | 핵심 근거가 여러 문단과 로그에 흩어져 있다 | 떨어진 단서들을 함께 참고하며 표현을 갱신한다 |
| 운영 스크립트/LLM | 멀리 떨어진 변수명, 제약, 예외 조건을 끝까지 맞춰야 한다 | 앞쪽 제약과 현재 위치를 반복적으로 연결한다 |

아래 도식은 같은 Transformer 블록이 서로 다른 과업에서 어떻게 읽히는지를 아주 거칠게 묶어 보여 줍니다.

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-task-flow-ko.mmd"
```

이 도식에서 봐야 할 점은 과업이 달라도 블록 자체가 바뀌는 것이 아니라, `문맥 관계를 읽고 표현을 다시 가공하는 같은 기본 구조`가 작업 지시 번역, 장애 보고서 요약, 운영 스크립트 생성에 공통으로 쓰인다는 점입니다.

### 사례 1. 다국어 작업 지시 번역

긴 작업 지시 문장을 다른 언어로 옮긴다고 해 보겠습니다. 예를 들어 `재기동을 시작하되, 압력 해소가 확인되지 않았으면 밸브를 열지 않는다` 같은 문장은 앞쪽의 `재기동을 시작하되`만 빨리 읽으면 곧바로 작업 허가처럼 느껴질 수 있습니다. 하지만 실제 번역에서는 뒤쪽의 안전 조건 `압력 해소가 확인되지 않았으면`이 앞 조치의 해석 범위를 바꿉니다. 예전 순차 구조에서는 이런 먼 조건을 끝까지 안정적으로 끌고 가는 일이 특히 어려웠습니다. 여기서 바뀌는 점은 `앞에서 뒤로 밀어 가며 읽는 방식`에서 `문장 전체 관계를 함께 반영하며 읽는 방식`으로 기준이 이동한다는 것입니다. Transformer 블록은 각 위치가 문장 전체 다른 위치를 함께 참조하며 표현을 다시 만들 수 있게 해, 앞 조치와 뒤 안전 조건의 관계를 한 번에 더 넓게 반영합니다. 그래서 긴 작업 지시 번역에서 뒤늦게 금지 조건을 다시 붙여야 하던 부담을 줄이는 데 중요한 전환점이 되었습니다.

### 사례 2. 장애 보고서 요약

긴 장애 보고서를 요약한다고 해 봅시다. 사람이 급하게 요약할 때는 제목, 첫 문단, 마지막 결론 같은 일부 위치에 더 크게 기대기 쉽습니다. 하지만 실제 핵심 원인은 중간 로그 발췌나 앞뒤에 흩어진 조건 문장에 숨어 있을 수 있습니다. 예를 들어 마지막 결론이 `배포 롤백 후 복구`라고 적혀 있어도, 그 결론이 유효한 이유는 앞쪽의 `압력 변동이 배포 직후 시작되었다`는 로그와 중간의 `수동 밸브 점검에서는 이상이 없었다`는 문장에 들어 있을 수 있습니다. 여기서 바뀌는 점은 `눈에 띄는 위치 몇 군데만 붙잡는 읽기`에서 `흩어진 관련 문장을 반복적으로 묶는 읽기`로 기준이 이동한다는 것입니다. Transformer 블록은 문서 전체 여러 위치를 함께 참고하며 각 위치 표현을 반복적으로 갱신할 수 있어서, 멀리 떨어진 관련 문장을 더 쉽게 같은 장애 요약 판단 안에 묶습니다.

### 사례 3. 운영 스크립트 생성과 LLM

운영 스크립트 생성에서 함수 시작부의 `line_id`, `pressure_ok`, `interlock_released` 같은 조건과 아래쪽 재기동 로직이 멀리 떨어져 있는 장면을 떠올려 볼 수 있습니다. 사람은 바로 앞 몇 줄만 보며 이어 써도 될 것처럼 느끼기 쉽지만, 그렇게 쓰면 위에서 쓴 변수 이름과 아래에서 참조하는 이름이 어긋나거나, `pressure_ok`가 `False`일 때는 재기동을 막아야 한다는 앞 제약을 뒤쪽에서 잊기 쉽습니다. 예를 들어 함수 초반에 `interlock_released`를 확인했는데, 뒤쪽 재기동 함수 호출에서는 그 조건을 빼먹으면 스크립트가 현장 규칙과 어긋납니다. 긴 자연어 생성도 마찬가지로, 앞에서 세운 제약과 뒤 문장에서 이어질 설명이 멀리 떨어져 연결됩니다. 여기서 바뀌는 점은 `바로 앞 토큰만 따라 쓰는 방식`에서 `먼 앞쪽 제약과 현재 위치를 함께 묶는 방식`으로 기준이 이동한다는 것입니다. Transformer 블록은 이런 멀리 떨어진 토큰 관계를 반복적으로 반영하며 각 위치의 표현을 갱신합니다.

세 사례에서 공통으로 확인해야 할 결과는 먼 위치의 단서를 현재 표현 안에 함께 반영할 수 있다는 점입니다. 작업 지시 번역에서는 뒤쪽 안전 조건이 앞 조치 해석까지 이어지는지, 장애 보고서 요약에서는 흩어진 로그와 조건 문장이 결론과 함께 묶이는지, 운영 스크립트와 자연어 생성에서는 변수명과 차단 조건 같은 앞 제약이 끝까지 유지되는지를 보면 충분합니다.

| 사람이 먼저 보기 쉬운 기준 | Transformer 블록 관점으로 다시 읽는 기준 |
| --- | --- |
| attention만 있으면 Transformer 설명은 끝난다고 느끼기 쉽다 | 관계를 읽은 뒤 표현을 다시 가공하고, 원래 정보와 안정성을 유지하는 부품까지 함께 봐야 블록이 닫힌다 |
| 문맥을 한 번 섞으면 바로 최종 판단이 나온다고 본다 | `문맥 읽기 -> 위치별 가공 -> residual -> normalization`이 차례로 이어져야 현재 표현 변화가 해석된다 |
| 과업이 달라도 모델 구조가 크게 달라질 것이라고 느끼기 쉽다 | 작업 지시 번역, 장애 요약, 운영 스크립트 생성이 달라도 같은 블록이 `무엇을 다시 묶는가`만 바꿔 반복된다고 보는 편이 정확하다 |

같은 세 사례를 블록 부품별 책임으로 다시 나눠 보면, 왜 `attention 하나`로 절 설명을 닫으면 부족한지도 더 직접 보입니다.

| 사례 | self-attention이 먼저 맡는 일 | feed-forward가 이어서 맡는 일 | residual + normalization이 지키는 것 |
| --- | --- | --- | --- |
| 다국어 작업 지시 번역 | 앞 조치와 뒤 안전 조건을 다시 연결한다 | 현재 위치 표현을 `허가 문장`이 아니라 `조건부 허가 문장`으로 더 분명히 가공한다 | 조건을 다시 반영한 표현이 다음 토큰 생성까지 안정적으로 이어지게 한다 |
| 장애 보고서 요약 | 앞쪽 로그, 중간 점검, 마지막 결론을 함께 참고한다 | 현재 문장을 `잡음`이 아니라 `원인 근거` 또는 `복구 근거`로 더 선명하게 다듬는다 | 한 번 섞인 근거 표현이 다음 블록에서도 무너지지 않게 유지한다 |
| 운영 스크립트 생성 | 앞쪽 변수명, 인터록 조건, 금지 제약을 현재 줄과 연결한다 | 현재 위치 표현을 `일반 함수 호출`이 아니라 `조건이 붙은 재기동 로직`으로 가공한다 | 앞 제약을 잊지 않은 표현이 긴 코드 흐름 끝까지 안정적으로 남게 한다 |

## 연습 및 예제

이번 예제의 목표는 Transformer 블록을 구성하는 두 핵심 단계, 즉 `문맥을 섞는 단계`와 `각 위치 표현을 다시 가공하는 단계`를 실제 운영 문장 장면에 얹어 보는 것입니다.

코드를 읽기 전에 아래 네 값부터 순서대로 보면 이 절의 구조 축이 덜 흩어집니다.

| 먼저 볼 값 | 왜 먼저 보아야 하는가 |
| --- | --- |
| `contextual tokens` | self-attention이 장애 대응 로그의 여러 단서를 먼저 어떻게 섞는지 바로 보이기 때문에 |
| `feed-forward output` | attention으로 섞인 표현이 각 위치에서 다시 어떻게 가공되는지 이어서 볼 수 있어서 |
| `after residual` | 새 계산 결과만 쓰지 않고 원래 입력 표현도 함께 남긴다는 점을 확인할 수 있어서 |
| `after simple layer norm` | 다음 블록으로 넘기기 전에 값 범위를 다시 정리하는 감각을 마지막에 붙잡을 수 있어서 |

입력:

- 세 개 토큰의 초기 표현
- 두 가지 운영 장면별 attention 가중치
- feed-forward 가중치

출력:

- attention 적용 전후의 토큰 표현
- feed-forward 적용 후 표현
- residual을 더한 뒤의 표현
- 간단한 layer normalization 뒤 표현
- `rollback confirmed` 장면과 `rollback not confirmed` 장면에서 조치 토큰 표현이 어떻게 달라지는지

문제 상황:

- 장애 대응 운영에서는 `장애 증상`, `배포 단서`, `조치 확인`이 멀리 떨어져 적혀 있어도 함께 읽어야 하므로, Transformer 블록이 이런 장면에서 어떤 식으로 표현을 갱신하는지 단계별로 볼 필요가 있다

확인할 개념:

- Transformer 블록은 attention과 feed-forward가 한 묶음으로 반복된다
- residual과 normalization까지 봐야 표현이 어떻게 안정적으로 갱신되는지 이해할 수 있다
- 운영 문장 장면에서 `조치 확인 단서가 들어오면 action token 표현이 어떻게 달라지는가`를 보면 블록 내부 역할 분담이 더 선명해진다

코드를 보기 전에, 두 운영 장면에서 어떤 단계가 먼저 달라질지 예상해 보면 좋습니다.

| 비교 포인트 | `rollback confirmed`에서 먼저 예상할 변화 | `rollback not confirmed`에서 먼저 예상할 변화 |
| --- | --- | --- |
| `contextual tokens` | action token이 조치 확인 단서를 더 강하게 섞을 것 | action token이 증상/배포 단서 쪽을 더 많이 유지할 것 |
| `feed-forward output` | 섞인 조치 문맥이 각 위치 표현에 더 반영될 것 | 확인 부족 문맥이 남아 action 표현이 덜 회복 쪽으로 갈 것 |
| `action token after residual` | recovery 축이 더 크게 남을 것 | 증상/원인 축이 상대적으로 더 남을 것 |

입력(input):

`symptom`, `deploy clue`, `action status` 세 토큰을 쓰고, `rollback confirmed` 장면과 `rollback not confirmed` 장면을 비교합니다.

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
    delta_from_input = ff_output - tokens
    residual_added = ff_output + tokens
    normalized = np.vstack([simple_layer_norm(row) for row in residual_added])

    print(f"[{name}]")
    print("contextual tokens =")
    print(np.round(contextual, 3))
    print("feed-forward output =")
    print(np.round(ff_output, 3))
    print("change from input =")
    print(np.round(delta_from_input, 3))
    print("after residual =")
    print(np.round(residual_added, 3))
    print("after simple layer norm =")
    print(np.round(normalized, 3))
    print("action token after residual =", np.round(residual_added[2], 3))
    print("---")
```

출력에서는 두 장면 모두 `action token after residual`을 먼저 비교한 뒤, 그 차이가 `contextual tokens` 단계에서 이미 어떻게 만들어졌는지 거슬러 올라가 보면 됩니다.

```text
[rollback_confirmed]
contextual tokens =
[[0.87 0.37]
 [0.69 0.59]
 [0.52 0.77]]
feed-forward output =
[[1.031 0.718]
 [0.877 0.866]
 [0.726 0.978]]
change from input =
[[ 0.031  0.518]
 [ 0.077  0.366]
 [ 0.426 -0.022]]
after residual =
[[2.031 0.918]
 [1.677 1.366]
 [1.026 1.978]]
after simple layer norm =
[[ 1. -1.]
 [ 1. -1.]
 [-1.  1.]]
action token after residual = [1.026 1.978]
---
[rollback_not_confirmed]
contextual tokens =
[[0.87 0.37]
 [0.76 0.51]
 [0.76 0.51]]
feed-forward output =
[[1.031 0.718]
 [0.938 0.814]
 [0.938 0.814]]
change from input =
[[ 0.031  0.518]
 [ 0.138  0.314]
 [ 0.638 -0.186]]
after residual =
[[2.031 0.918]
 [1.738 1.314]
 [1.238 1.814]]
after simple layer norm =
[[ 1. -1.]
 [ 1. -1.]
 [-1.  1.]]
action token after residual = [1.238 1.814]
---
```

| 비교 포인트 | rollback confirmed | rollback not confirmed | 왜 중요한가 |
| --- | --- | --- | --- |
| action token이 참고한 문맥 | 조치 확인 토큰이 자기 자신과 원인 단서를 더 강하게 유지한다 | 조치 확인이 약해져 증상/배포 단서 쪽 비중이 상대적으로 커진다 | 같은 블록이어도 운영 장면에 따라 `어느 단서를 더 묶는가`가 달라지기 때문이다 |
| action token after residual | `[1.026, 1.978]` | `[1.238, 1.814]` | 조치 확정 여부가 현재 위치 표현을 실제로 다른 방향으로 움직인다는 점이 드러나기 때문이다 |
| 해석 방식 | `조치가 확인되었으니 복구 상태를 더 강하게 반영한다` | `아직 확인이 약하니 경보와 배포 단서를 더 의심한다` | Transformer 블록이 운영 문장을 읽을 때도 단순 순차가 아니라 관계 재반영으로 작동함을 보여 준다 |

| 블록 단계 | 이 단계만 따로 보면 생기기 쉬운 오해 | 블록 전체로 읽을 때 바로잡아야 할 점 |
| --- | --- | --- |
| self-attention (`contextual tokens`) | 문맥만 한 번 섞었으니 이미 최종 판단이 끝났다고 느끼기 쉽다 | 이 단계는 `무엇을 다시 참고할까`를 정하는 자리이고, 아직 현재 위치 표현 가공과 안정적 전달은 남아 있다 |
| feed-forward (`feed-forward output`) | 숫자만 다시 변형했으니 부차적 후처리처럼 느끼기 쉽다 | 실제로는 attention으로 모아 온 문맥을 각 위치 표현 안에서 다시 다듬어, 같은 문맥이라도 위치별 해석을 갈라 준다 |
| residual (`after residual`) | 그냥 이전 값을 더하는 덧셈처럼 보이기 쉽다 | 새 계산만 믿지 않고 원래 입력 표현을 함께 남겨, 조치 토큰이 원래 갖고 있던 복구 상태 정보가 사라지지 않게 한다 |
| layer normalization (`after simple layer norm`) | 숫자 크기만 정리하는 부차적 단계로 느끼기 쉽다 | 다음 블록으로 넘길 표현 범위를 다시 맞춰, 블록 반복이 깊어져도 계산이 덜 흔들리게 한다 |

- attention 단계에서는 각 토큰이 다른 토큰 정보를 받아 원래 표현이 바뀝니다.
- feed-forward 단계에서는 문맥이 섞인 표현을 위치별로 다시 변형합니다.
- `after residual`은 새 계산 결과만 쓰지 않고 원래 토큰 표현을 함께 남긴다는 점을 보여 줍니다.
- `after simple layer norm`은 각 위치 표현이 다음 단계로 넘어가기 전에 값 범위가 다시 정리될 수 있음을 보여 줍니다.
- 운영 문장 장면에서는 `rollback confirmed` 같은 멀리 있는 단서가 action token 표현에 실제로 반영되는지가 핵심입니다.

즉, `rollback confirmed`와 `rollback not confirmed`를 갈라 놓는 것은 attention 단계에서 시작되지만, 그 차이를 실제 블록 출력으로 안정적으로 넘겨 주는 것은 feed-forward, residual, normalization까지 포함한 전체 조합입니다. Transformer를 `attention이 센 모델` 정도로만 읽으면 바로 이 조합 책임이 빠집니다.

즉, 이 예제는 같은 장애 대응 로그라도 `rollback confirmed` 문장이 들어오느냐에 따라 현재 조치 표현이 달라질 수 있음을 보여 줍니다. Transformer 블록이 중요한 이유는 단순히 토큰을 섞어서가 아니라, 이런 `운영 판단에 필요한 먼 단서`를 현재 표현 안에 다시 반영하도록 만들기 때문입니다.

| 먼저 보인 출력 신호 | 지금 바로 해 볼 변화 | 아직 이 예제만으로 서두르지 않을 결론 |
| --- | --- | --- |
| `action token after residual`이 장면마다 달라진다 | 조치 확인 토큰의 attention 비중을 더 키우거나 줄여 보고 운영 판단 표현이 어떻게 달라지는지 비교한다 | attention 수치 하나만으로 실제 운영 우선순위 전체가 결정된다고 단정하지 않는다 |
| `contextual tokens`가 장면마다 다르게 섞인다 | 증상 토큰과 배포 단서 토큰 비중을 바꿔 어떤 문맥이 action token에 더 크게 들어오는지 본다 | 숫자 변화가 크다고 해서 항상 더 좋은 표현 학습이라고 단정하지 않는다 |
| `after simple layer norm`이 비슷한 범위로 정리된다 | 특정 축 값을 과하게 키워 normalization 전후 차이가 얼마나 커지는지 본다 | 이 축약 normalization 비교만으로 실제 layer normalization 구현 세부를 모두 대체하지 않는다 |

실제 Transformer는 잔차 연결(residual connection), layer normalization, multi-head attention을 함께 쓰지만, 큰 흐름은 이런 블록 반복으로 읽는 것이 좋습니다.

## 이 예제를 블록 조합 관점으로 다시 보면

앞의 숫자는 Transformer 전체를 구현한 것은 아니지만, 각 부품의 역할 차이는 분명하게 드러납니다.

- `contextual tokens`는 self-attention이 다른 위치 정보를 먼저 섞는 단계입니다.
- `feed-forward output`은 섞인 표현을 각 위치에서 한 번 더 가공한 결과입니다.
- `after residual`은 새 계산만 믿지 않고 원래 표현도 함께 들고 가는 안전장치 역할을 보여 줍니다.
- `after simple layer norm`은 다음 블록으로 넘기기 전에 값 범위를 다시 정리하는 감각을 줍니다.

즉, Transformer 블록은 `attention 하나`가 아니라, `문맥 섞기 + 위치별 가공 + 원래 정보 보존 + 안정화`가 한 묶음으로 반복되는 구조입니다. 이 감각이 잡혀야 다음 절 P5-14.2에서 병렬 처리와 긴 문맥을 설명할 때도, 왜 이 블록이 대규모로 반복되기 쉬웠는지 더 자연스럽게 읽을 수 있습니다.

Transformer는 attention이 보조 장치에서 핵심 블록으로 승격된 사례입니다. 그리고 이 블록 설계는 이후 다양한 대규모 언어·멀티모달 모델에서 공통 기본 단위처럼 재사용되었습니다.

## 체크리스트

- 트랜스포머(Transformer) 블록을 셀프 어텐션, feed-forward, residual connection, layer normalization으로 설명할 수 있는가?
- 트랜스포머가 한 아이디어가 아니라 부품 묶음 구조라는 점을 말할 수 있는가?
- Transformer를 읽을 때 self-attention이 문맥 관계를 모으고, feed-forward가 표현을 가공하며, residual과 normalization이 깊은 계산을 안정화하는 블록 조합으로 구분할 수 있는가?
- Transformer를 `attention이 있는 모델` 정도로만 말하지 않고, `관계 읽기, 위치별 가공, 안정적 전달을 반복하는 블록 구조`로 설명할 수 있는가?
- self-attention과 feed-forward의 역할 차이를 `바깥과의 관계 읽기`와 `현재 위치 표현 가공`으로 나눠 말할 수 있는가?
- residual과 normalization이 깊은 학습을 안정화하는 역할을 한다는 점을 설명할 수 있는가?
- attention 일반론만으로는 Transformer를 설명하기 부족할 때, 블록 구성 관점을 먼저 떠올릴 수 있는가?
- 다음 절의 병렬 처리 설명을 읽을 때도 먼저 `이 블록을 많이 반복하면 계산 흐름이 왜 달라지는가`를 떠올릴 준비가 되어 있는가?

## 출처와 참고 자료

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-06-29.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Jay Alammar, `The Illustrated Transformer`, 확인 날짜: 2026-06-29. [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/){: target="_blank" rel="noopener noreferrer" }
