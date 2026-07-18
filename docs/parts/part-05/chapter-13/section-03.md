# P5-13.3 보충학습: 쿼리-키-값(query-key-value, QKV)과 멀티헤드 어텐션(multi-head attention)

Section ID: `P5-13.3`
Version: `v2026.07.18`

P5-13.1과 P5-13.2에서는 어텐션(Attention)과 셀프 어텐션(self-attention)의 직관을 먼저 잡았습니다. 그런데 여기까지 읽으면 자연스럽게 다음 질문이 생깁니다.

그렇다면 어텐션이 실제 계산에서는 쿼리(query), 키(key), 값(value)으로 왜 설명되며, 멀티헤드 어텐션(multi-head attention)은 왜 따로 이름이 붙는가?

용어가 다시 흩어져 보일 때는 개념사전의 [쿼리-키-값(query-key-value, QKV)](../../../reference/concept-glossary.md#-query-key-value-qkv)과 [멀티헤드 어텐션(multi-head attention)](../../../reference/concept-glossary.md#multi-head-attention) 항목을 함께 다시 봅니다.

## 이 보충학습의 범위

- 쿼리(query), 키(key), 값(value)은 무엇을 뜻하나?
- 왜 셀프 어텐션 계산을 이 세 이름으로 나누어 설명하나?
- 멀티헤드 어텐션은 무엇을 여러 번 본다는 뜻인가?
- 트랜스포머를 읽을 때 이 개념을 어느 정도까지 이해하면 충분한가?

이 보충학습에서는 `왜 이런 이름을 쓰는가`, `한 head와 여러 head의 차이를 어떻게 직관적으로 읽는가`를 붙잡는 데 집중합니다. 이 보충학습의 핵심은 `새 수식을 더 외우는가`가 아니라, 이미 잡은 attention 직관을 `QKV`와 `multi-head`라는 반복 이름으로 다시 읽게 만드는 데 있습니다.

## 이 보충학습의 목표

- query, key, value를 입문 수준에서 설명할 수 있습니다.
- self-attention을 `질문하고, 맞는 위치를 찾고, 그 정보를 가져오는 계산`으로 읽을 수 있습니다.
- multi-head attention을 `관계를 한 종류로만 보지 않고 여러 관점으로 나누어 본다`는 뜻으로 설명할 수 있습니다.
- Transformer 절을 다시 읽을 때 QKV와 multi-head가 어디에 놓이는지 떠올릴 수 있습니다.

## 먼저 아주 짧은 비유로 보면

query, key, value는 다음처럼 비유할 수 있습니다.

| 이름 | 입문용 직관 |
| --- | --- |
| query | 지금 무엇을 찾고 싶은가 |
| key | 각 위치가 어떤 정보인지 붙어 있는 표지 |
| value | 실제로 가져올 내용 |

도서관 비유로 다시 쓰면 다음과 같습니다.

- query: `나는 지금 역사 책을 찾고 싶다`
- key: `각 책 카드에는 역사, 과학, 소설 같은 표지가 붙어 있다`
- value: `실제로 읽어 가져갈 책 내용`

즉, attention은 `지금 필요한 질문(query)`에 맞춰 `어울리는 표지(key)`를 가진 위치를 찾고, 거기서 `실제 내용(value)`을 더 많이 가져오는 계산입니다.

운영 메모 문맥으로 바로 바꿔 읽으면 더 분명해집니다.

| 같은 운영 메모 장면 | query처럼 읽는 것 | key처럼 읽는 것 | value처럼 읽는 것 |
| --- | --- | --- | --- |
| `정지 해제는 요청되었다. 그러나 압력 복귀는 아직 완료되지 않았다.` | 현재 표현이 `무엇이 아직 미완료인가`를 다시 확인하려는 질문 | `정지 해제`, `압력 복귀`, `완료되지 않았다`처럼 각 위치가 어떤 종류 정보인지 드러내는 표지 | 현재 표현에 실제로 다시 섞여 들어와야 하는 `정지 요청`과 `복귀 미완료`의 의미 내용 |
| 교대 인수인계 요약 | 지금 요약 표현이 `최종 결정인가, 근거인가, 조건인가`를 가르는 질문 | 각 문장이 `결론`, `이상 징후`, `안전 조건` 가운데 무엇에 가까운지 보여 주는 표지 | 최종 요약에 실제로 남겨야 하는 결정, 근거, 조건의 내용 |
| 정비 코드 읽기 | 현재 줄이 `이 값이 어디서 왔는가`를 다시 묻는 질문 | 변수 정의, 조건문, 함수 호출이 어떤 역할인지 보여 주는 표지 | 현재 줄 해석에 실제로 다시 섞여 들어와야 하는 정의-사용 관계와 호출 맥락 |

즉, QKV를 굳이 따로 부르는 이유는 `지금 무엇을 찾는가`, `각 위치가 어떤 종류 정보인가`, `실제로 무엇을 가져와 표현을 바꿀 것인가`를 분리해 읽기 위해서입니다. 이 절은 이 역할 이름이 왜 필요한지 붙잡는 자리이지, 행렬 차원과 구현 최적화를 다루는 자리가 아닙니다.

## self-attention 안에서는 무엇이 달라지나

P5-13.2에서는 self-attention을 `같은 시퀀스 안 토큰들이 서로를 참고해 표현을 다시 계산하는 방식`이라고 설명했습니다. 여기서 QKV를 붙이면 같은 말을 조금 더 계산 친화적으로 다시 쓰게 됩니다.

- 현재 토큰은 `나는 지금 무엇이 필요한가`라는 query를 냅니다.
- 모든 토큰은 `나는 어떤 정보인가`라는 key를 가집니다.
- 모든 토큰은 `내가 실제로 줄 수 있는 내용은 무엇인가`라는 value를 가집니다.

즉, 현재 토큰은 자기 query와 다른 토큰들의 key를 비교해 `누구를 더 참고할지`를 정하고, 그다음 그 토큰들의 value를 가중 평균해 새 표현을 만듭니다.

이 흐름을 아주 단순하게 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-13/qkv-flow-ko.mmd"
```

이 도식은 다음 순서의 계산을 압축합니다.

1. 현재 토큰이 질문을 던집니다.
2. 그 질문이 어떤 토큰 표지와 더 잘 맞는지 비교합니다.
3. 잘 맞는 위치에 더 큰 비중을 줍니다.
4. 그 위치들의 실제 내용(value)을 더 많이 섞어 새 표현을 만듭니다.

## 왜 굳이 key와 value를 나누나

입문 독자는 여기서 `어차피 토큰 하나인데 왜 key와 value를 따로 부르지?`라는 질문이 자연스럽습니다.

핵심은 `찾는 기준`과 `가져올 내용`의 역할이 다를 수 있기 때문입니다.

예를 들어 교대 인수인계 기록에서 `이번 교대의 최종 결정`을 찾는다고 해 보겠습니다.

- `결정`, `승인`, `보류` 같은 단어는 지금 찾는 기준에 가까운 표지 역할을 합니다.
- 실제로 모델이 가져와야 하는 것은 그 문장 전체가 담고 있는 의미 표현입니다.

즉, key는 `이 위치를 얼마나 참고할지 정하는 데 쓰이는 표지`에 가깝고, value는 `정말 섞어 와서 새 표현을 만들 내용`에 가깝습니다.

이 구분을 한 문장으로 줄이면 다음과 같습니다.

`key는 어디를 볼지 정하는 데 더 가깝고, value는 실제로 무엇을 가져올지에 더 가깝다.`

## 작은 문장으로 다시 보면

```text
정지 해제는 요청되었다. 그러나 압력 복귀는 아직 완료되지 않았다.
```

만약 현재 토큰이 `그러나` 뒤 문맥을 이해하려 한다면, query는 `무엇이 지금 대비를 이루는가`를 찾는 질문처럼 작동할 수 있습니다. 이때 `정지 해제 요청`과 `압력 복귀 미완료`라는 두 표현이 각각 다른 key를 내고, 현재 query와 더 잘 맞는 위치가 더 큰 비중을 받습니다. 그리고 그 위치의 value가 더 많이 섞여 현재 표현이 업데이트됩니다.

즉, self-attention에서 토큰 하나는 `문장 전체를 다시 훑으며 지금 내 해석에 필요한 단서를 골라 섞는 방식`입니다.

## multi-head attention은 무엇을 여러 번 본다는 뜻인가

이제 다음 질문이 생깁니다.

한 번의 attention이면 충분한데, 왜 `multi-head`가 필요한가?

핵심은 한 종류의 관계만 보지 않고, 서로 다른 관점으로 토큰 관계를 나누어 읽는다는 점입니다.

`한 종류의 관계만 보지 말고, 서로 다른 관점으로 여러 번 관계를 읽어 보자.`

예를 들어 문장에서는 같은 토큰이라도 여러 관계가 함께 중요할 수 있습니다.

- 어떤 head는 주어-동사 관계를 더 잘 볼 수 있습니다.
- 어떤 head는 수식 대상이나 지시어 관계를 더 잘 볼 수 있습니다.
- 어떤 head는 가까운 토큰 결합을, 다른 head는 더 먼 토큰 연결을 더 잘 볼 수 있습니다.

즉, multi-head attention은 `하나의 정답 관계만 보는 대신, 여러 종류의 관련성을 나누어 읽는 장치`입니다.

아래 표는 같은 장면에서 single-head와 multi-head가 남기는 관계 정보의 차이를 바로 비교합니다.

| 같은 장면 | single-head처럼 한 번만 읽을 때 먼저 남는 것 | multi-head처럼 여러 관점으로 읽을 때 먼저 남는 것 |
| --- | --- | --- |
| 절차 문서 변환 | 가장 눈에 띄는 한 관계만 남고 수식 범위나 예외 조건이 약해질 수 있다 | 주체-행동, 수식 범위, 대비 관계를 나눠 함께 볼 수 있다 |
| 교대 인수인계 요약 | 결론 한 줄은 남아도 근거나 조건이 함께 약해질 수 있다 | 결론, 근거, 조건을 서로 다른 관련성으로 나눠 보존하기 쉽다 |
| 정비 코드 이해 | 변수명 반복 같은 한 종류 신호에 치우치기 쉽다 | 정의-사용, 조건-결과, 호출 흐름을 다른 관점으로 함께 읽기 쉽다 |

## 도식으로 보면

```mermaid
--8<-- "assets/part-05/chapter-13/multihead-flow-ko.mmd"
```

이 도식에서 핵심은 `입력이 여러 개로 쪼개진다`가 아니라, `같은 입력을 여러 관점으로 읽은 결과를 다시 합친다`는 점입니다.

같은 판단 문장을 single-head와 multi-head 감각으로 더 짧게 병치하면 다음처럼 볼 수 있습니다.

```mermaid
--8<-- "assets/part-05/chapter-13/single-vs-multihead-baseline-ko.mmd"
```

이 비교 도식에서 먼저 붙잡아야 할 점은 다음과 같습니다.

- single-head는 `결정`, `근거`, `조건`을 하나의 절충 문맥으로 접기 쉽습니다.
- multi-head는 같은 입력을 보더라도 `결정 쪽 관계`, `조건 쪽 관계`처럼 다른 관련성 패턴을 나눠 남길 수 있습니다.
- 이 감각이 잡혀야 멀티헤드를 `attention을 여러 번 반복한다`가 아니라 `관계 종류를 분리해 유지한다`는 구조로 읽게 됩니다.

## 사례 및 예시

이 절의 사례는 `먼 위치를 다시 본다` 자체보다, `무슨 종류의 관계를 따로 들고 가야 하는가`를 먼저 봐야 합니다. 즉, 같은 문장을 읽더라도 `결정`, `근거`, `조건`, `정의-사용` 같은 관계를 하나의 평균 문맥으로 접을지, 서로 다른 관점으로 나눠 들고 갈지를 구분해서 읽어야 합니다.

### 대표 사례. 절차 문서 변환

긴 절차 문서를 작업 지침으로 바꿀 때 사람은 보통 단어 뜻 하나만 맞추면 된다고 느끼기 쉽습니다. 하지만 실제로는 주체-행동 관계, 수식 범위, 부정 표현, 예외 조건이 동시에 중요할 수 있습니다. 예를 들어 한 표현이 `무엇을 꾸미는가`와 `어디에 대비되는가`를 동시에 봐야 제대로 지침이 만들어지는 장면이 있습니다. 이때 한 번의 attention만으로 모든 관계를 한 종류로만 읽으면 중요한 차이가 섞일 수 있습니다. multi-head attention은 서로 다른 관계를 나누어 읽는다는 직관을 주므로, 절차 문서에서 여러 문법 단서를 함께 반영하는 장면을 설명하기 좋습니다.
그래서 이 사례에서 확인해야 할 결과는 현재 지침 문구가 한 관계만 따라가지 않고, 주체-행동 관계와 예외 조건 범위를 서로 다른 관점으로 함께 남겨 실제 작업 순서를 덜 왜곡하는가입니다.

같은 관점은 교대 판단 문장 정리나 정비 코드 읽기에도 그대로 이어집니다. 다만 이 절에서 붙잡을 핵심은 도메인 이름이 아니라, `한 문맥으로 절충되기 쉬운 관계를 여러 head가 서로 다른 관점으로 나누어 유지하는가`입니다.

```mermaid
--8<-- "assets/part-05/chapter-13/multihead-decision-condition-case-flow-ko.mmd"
```

이 도식은 같은 판단 문장이 single-head에서는 절충되고 multi-head에서는 결정·근거·조건 관계로 다시 나뉘는 차이를 압축해 보여 줍니다.

| 사람이 먼저 보기 쉬운 기준 | single-head 관점으로 다시 읽는 기준 | multi-head 관점으로 다시 읽는 기준 |
| --- | --- | --- |
| 절차 문서는 핵심 단어 몇 개만 맞으면 된다고 느끼기 쉽다 | 가장 강한 한 관계가 남고 수식 범위나 예외 조건은 한 문맥 안에 절충될 수 있다 | 주체-행동, 수식 범위, 대비 관계를 다른 head가 나눠 읽어 함께 유지할 수 있다 |
| 교대 판단 문장은 결론 단어만 잡으면 충분하다고 느끼기 쉽다 | 결론 중심 신호 하나가 평균적 문맥을 끌고 가며 근거나 조건은 약해질 수 있다 | 결론, 근거, 조건을 서로 다른 관련성 패턴으로 나눠 더 오래 보존할 수 있다 |
| 코드는 변수명만 이어지면 읽힌다고 느끼기 쉽다 | 정의-사용, 조건-결과, 호출 흐름이 하나의 절충 표현에 섞일 수 있다 | 서로 다른 head가 다른 연결 패턴을 나눠 읽어 한 종류 신호에만 치우치지 않게 한다 |

세 사례에서 공통으로 확인해야 할 결과는 관계를 한 줄로만 읽지 않고 여러 관점으로 나누어 본다는 점입니다. 절차 문서 변환에서는 주체-행동 관계와 예외 조건이 함께 유지되는지, 교대 판단 문장에서는 결론과 근거와 조건이 함께 남는지, 코드에서는 정의-사용과 조건-결과 관계가 함께 이어지는지를 보면 충분합니다.

이 사례들에서 최종적으로 확인해야 할 결과도 분명합니다. multi-head의 차이는 `attention을 여러 번 돈다`는 데 있지 않고, single-head에서는 한 문맥으로 절충되기 쉬운 여러 관계를 서로 다른 head에 나누어 더 오래 유지한다는 데 있습니다.

## 연습 및 예제

이번 예제의 목표는 같은 토큰열을 보더라도 head마다 서로 다른 관계를 읽고, 그 차이가 head 가중치 변화에 따라 얼마나 커지거나 줄어드는지 직접 실험해 보는 것입니다.

이번에는 추상 토큰 대신 짧은 운전 보고서 조각을 간단한 벡터로 놓고 읽어 보겠습니다. `정지 결정`, `압력 이상 근거`, `복귀 조건` 세 조각이 있을 때, single-head는 이 셋을 하나의 절충 문맥으로 접기 쉽고, multi-head는 `결정 쪽`, `조건 쪽` 같은 관점을 나눠 유지할 수 있는지를 보는 것이 핵심입니다.

입력:

- 세 개의 토큰 표현
- 세 가지 head 가중치 시나리오
- 비교 기준으로 쓸 single-head 가중치

출력:

- 각 시나리오의 single-head 문맥
- 각 시나리오의 head 1, head 2 문맥
- single-head 대비 head별 차이
- 두 head가 얼마나 다른 관계를 읽었는지 보여 주는 분리 정도

문제 상황:

- multi-head attention은 말로만 들으면 추상적이므로, `head를 얼마나 다르게 두었을 때 관계 분리가 실제로 커지는가`를 직접 비교해 볼 필요가 있다

확인할 개념:

- 서로 다른 head는 같은 토큰열에서도 다른 관계를 강조할 수 있다
- head 가중치가 비슷하면 multi-head도 절충에 가까워지고, 멀어지면 관계 분리가 더 커진다
- 여러 head 결과를 합치면 single-head보다 더 풍부한 표현을 만들 수 있다

입력(input):

위에 정리한 세 개의 보고서 조각 표현과 세 가지 head 가중치 시나리오를 사용합니다.

코드를 보기 전에 먼저 각 시나리오가 어떤 관계 분리 정도를 남길지 예상해 보면, `절충된 한 문맥`과 `나뉜 여러 관계`의 차이가 더 잘 보입니다.

| 비교 항목 | 먼저 예상해 볼 출력 | 예상 이유 |
| --- | --- | --- |
| `balanced_heads` | `head1_context`와 `head2_context` 차이가 비교적 작을 가능성이 큼 | 두 head 모두 `정지 결정`, `압력 이상 근거`, `복귀 조건`을 비슷한 비율로 섞기 때문입니다. |
| `decision_vs_condition_split` | `head1_context`와 `head2_context` 차이가 가장 크게 벌어질 가능성이 큼 | 한 head는 결정 쪽을, 다른 head는 조건 쪽을 강하게 밀어 single-head에서 접히는 차이를 크게 다시 벌립니다. |
| `condition_heavy_both_heads` | 두 head가 모두 뒤쪽으로 기울어 single-head와 큰 차이가 적을 가능성이 큼 | 두 head가 서로 다른 관점이라기보다 같은 조건 쪽 관계를 함께 강조하기 때문입니다. |
| `head_separation` | `decision_vs_condition_split`이 가장 클 가능성이 큼 | 서로 다른 head가 실제로 다른 종류의 관계를 읽을 때 분리 정도가 커집니다. |

이 표의 목적은 정확한 벡터 값을 미리 계산하는 데 있지 않습니다. multi-head가 단순 반복이 아니라, head를 어떻게 설계하느냐에 따라 `관계 분리`가 커지기도 하고 다시 절충에 가까워지기도 한다는 점을 코드 전에 붙잡는 데 있습니다.

```python
import numpy as np

tokens = np.array([
    [1.0, 0.0],   # 정지 결정
    [0.0, 2.0],   # 압력 이상 근거
    [3.0, 1.0],   # 복귀 조건
])

single_head_weights = np.array([0.4, 0.3, 0.3])

scenarios = {
    "balanced_heads": {
        "head1": np.array([0.45, 0.30, 0.25]),
        "head2": np.array([0.30, 0.30, 0.40]),
    },
    "decision_vs_condition_split": {
        "head1": np.array([0.70, 0.20, 0.10]),
        "head2": np.array([0.10, 0.30, 0.60]),
    },
    "condition_heavy_both_heads": {
        "head1": np.array([0.20, 0.25, 0.55]),
        "head2": np.array([0.15, 0.20, 0.65]),
    },
}


def summarize_scenario(name, head1_weights, head2_weights):
    single_head_context = single_head_weights @ tokens
    head1_context = head1_weights @ tokens
    head2_context = head2_weights @ tokens
    combined = np.concatenate([head1_context, head2_context])
    difference_from_single = combined - np.concatenate(
        [single_head_context, single_head_context]
    )
    head_separation = np.linalg.norm(head1_context - head2_context)

    print(f"[{name}]")
    print("single_head_context =", np.round(single_head_context, 3).tolist())
    print("head1_context       =", np.round(head1_context, 3).tolist())
    print("head2_context       =", np.round(head2_context, 3).tolist())
    print("difference_from_single =", np.round(difference_from_single, 3).tolist())
    print("head_separation =", round(float(head_separation), 3))
    print()


print("tokens =")
print(tokens)
print()

for scenario_name, heads in scenarios.items():
    summarize_scenario(scenario_name, heads["head1"], heads["head2"])
```

출력에서는 각 시나리오의 `head_separation`과 `difference_from_single`이 어떻게 달라지는지부터 보면 됩니다.

```text
tokens =
[[1. 0.]
 [0. 2.]
 [3. 1.]]

[balanced_heads]
single_head_context = [1.3, 0.9]
head1_context       = [1.2, 0.85]
head2_context       = [1.5, 1.0]
difference_from_single = [-0.1, -0.05, 0.2, 0.1]
head_separation = 0.335

[decision_vs_condition_split]
single_head_context = [1.3, 0.9]
head1_context       = [1.0, 0.5]
head2_context       = [1.9, 1.2]
difference_from_single = [-0.3, -0.4, 0.6, 0.3]
head_separation = 1.14

[condition_heavy_both_heads]
single_head_context = [1.3, 0.9]
head1_context       = [1.85, 1.05]
head2_context       = [2.1, 1.05]
difference_from_single = [0.55, 0.15, 0.8, 0.15]
head_separation = 0.25
```

이 예제에서 먼저 볼 산출물은 시나리오별 `head_separation`입니다. `decision_vs_condition_split`은 두 head가 결정 쪽과 조건 쪽으로 실제로 갈라지므로 분리 정도가 가장 크고, `condition_heavy_both_heads`는 head가 둘이어도 같은 조건 쪽을 함께 보므로 분리 정도가 작습니다.

![시나리오별 헤드 분리 정도](../../../assets/part-05/chapter-13/qkv-head-separation-ko.png)

두 번째 산출물은 single-head 문맥과 head 1, head 2 문맥이 좌표 위에서 어디로 갈라지는지입니다. 회색 점은 같은 single-head 기준이고, 파란 삼각형과 주황 사각형 사이의 거리가 커질수록 두 head가 서로 다른 관계를 더 분리해서 읽는다고 볼 수 있습니다.

![싱글 헤드와 두 헤드의 문맥 위치](../../../assets/part-05/chapter-13/qkv-head-context-space-ko.png)

| 먼저 볼 출력 | 이 출력이 뜻하는 것 | 바꿔 보면 달라지는 것 |
| --- | --- | --- |
| `head_separation`이 크다 | 두 head가 실제로 다른 관계를 읽고 있다는 뜻 | head 가중치를 더 비슷하게 만들면 분리 정도가 줄고, 더 다르게 만들면 커집니다 |
| `difference_from_single`이 양쪽으로 벌어진다 | single-head에서 평균내며 접힌 차이가 multi-head에서 다시 나뉜다는 뜻 | single-head 기준 가중치를 바꾸면 어떤 차이가 `절충 결과`에 이미 흡수되는지 비교할 수 있습니다 |
| 두 head가 모두 같은 방향으로 커진다 | head 수가 둘이어도 실제로는 같은 관계를 중복해서 보고 있을 수 있다는 뜻 | `condition_heavy_both_heads`처럼 두 head를 같은 쪽으로 몰면 multi-head의 분리 이점이 줄어듭니다 |

| 읽기 기준 | single-head 출력만 보면 쉬운 판단 | 시나리오 비교까지 보고 바뀌는 판단 |
| --- | --- | --- |
| 운전 보고서 요약 | `정지 결정`, `압력 이상`, `복귀 조건`이 한 덩어리 평균으로만 남아, 무엇이 결론이고 무엇이 조건인지 약해질 수 있다 | `decision_vs_condition_split`처럼 head를 갈라 두면 결론과 조건을 다른 문맥으로 오래 들고 갈 수 있다 |
| 절차 문서 해석 | head가 여러 개면 무조건 관계가 다양해질 것처럼 느끼기 쉽다 | `condition_heavy_both_heads`를 보면 head가 둘이어도 같은 조건만 함께 강조하면 관계 분리는 크지 않을 수 있다 |
| 실험 설계 | multi-head는 값 하나만 보면 이해했다고 느끼기 쉽다 | `balanced_heads`, `decision_vs_condition_split`, `condition_heavy_both_heads`를 나란히 봐야 `head를 어떻게 다르게 두는가`가 핵심이라는 점이 보인다 |

즉, single-head가 여러 관계를 하나의 절충 표현으로 접는다면, multi-head는 서로 다른 관계 읽기 결과를 나란히 유지해 단일 평균에서 사라질 차이를 더 오래 들고 갑니다. 다만 그 효과는 `head 수 자체`보다 `head들이 실제로 얼마나 다른 관계를 읽는가`에 더 크게 좌우됩니다.

이 숫자를 운영 보고서 읽기로 바꾸면, `balanced_heads`는 아직 절충에 가까운 요약이고, `decision_vs_condition_split`은 `결정 쪽 문맥`과 `조건 쪽 문맥`을 분리해 유지하는 읽기에 가깝습니다. 반대로 `condition_heavy_both_heads`는 head가 둘이어도 둘 다 조건 쪽으로 몰려, multi-head의 장점이 줄어든 장면으로 읽을 수 있습니다. 중요한 것은 벡터 값 자체보다, 서로 다른 head가 `어떤 종류 판단을 따로 남겨 두는가`입니다.

실제 multi-head attention은 이후 선형 변환까지 포함해 더 정교하게 결합되지만, 입문 단계에서는 `서로 다른 관계 읽기 결과를 나란히 유지한다`는 감각과 `head를 어떻게 나누느냐가 중요하다`는 감각까지 잡으면 충분합니다.

이 예제는 한 번 실행하고 끝내기보다, 아래 세 가지 조작을 직접 해 보면서 `관계 분리`가 언제 커지고 언제 줄어드는지 확인하는 편이 좋습니다.

| 지금 바로 바꿔 볼 값 | 관찰할 출력 | 해석할 질문 |
| --- | --- | --- |
| `head1`, `head2` 가중치를 더 비슷하게 바꾸기 | `head_separation` | 서로 다른 head가 사실상 같은 관계를 읽게 되면 multi-head의 장점이 얼마나 줄어드는가 |
| `single_head_weights`를 `head1` 쪽이나 `head2` 쪽으로 더 기울이기 | `difference_from_single` | single-head가 이미 특정 관계를 강하게 반영하면 multi-head와 차이가 얼마나 줄어드는가 |
| `tokens`에서 `복귀 조건` 값을 더 크게 또는 더 작게 바꾸기 | `head2_context`, `head_separation` | 토큰 자체의 의미 강도가 바뀌면 어떤 head가 그 변화를 더 민감하게 끌어오는가 |

앞의 숫자는 실제 대규모 multi-head attention 전체를 구현한 것은 아니지만, single-head가 여러 관계를 한 번에 평균내며 하나의 절충된 문맥으로 남기는 반면 multi-head는 서로 다른 관계 읽기 결과를 나란히 유지한 뒤 함께 쓴다는 비교 기준과, head 설계가 그 차이를 키우거나 줄인다는 실험 기준은 충분히 드러납니다. 즉, multi-head attention은 단순히 `attention을 여러 번 반복한다`는 뜻이 아니라, `서로 다른 종류의 관련성 패턴을 동시에 잃지 않게 들고 갈 수 있도록 head를 나누는 구조`에 더 가깝습니다.

이 절에서 독자가 최종적으로 붙잡아야 하는 것도 같습니다. QKV는 `무엇을 찾는가`, `어떤 표지와 맞는가`, `무엇을 실제로 가져오는가`를 나눠 읽게 하는 이름이고, multi-head는 그렇게 찾은 관계를 한 번에 평균내지 않고 `결정`, `근거`, `조건`처럼 다른 관점으로 더 오래 유지하게 하는 구조입니다.

## Part 5 흐름에서 왜 중요한가

이 보충학습은 attention 절과 Transformer 절 사이에 끼어 있는 세부 구현 메모가 아닙니다. 오히려 본편에서 이미 잡은 직관을 `왜 이런 이름과 구조가 붙는가`로 연결해 주는 회수 위치입니다. attention과 self-attention의 핵심 직관은 이미 본문에서 닫았지만, QKV와 multi-head라는 이름이 Transformer 본문에서 반복 등장하므로, 이 절은 수식 메모가 아니라 `이름을 다시 읽어 주는 입문 회수 위치`로 남겨 두는 편이 더 적절합니다. 다음 장 P5-14.1에서는 이 이름들이 Transformer 블록 안에서 어디에 놓이는지를 이어서 설명합니다.

## 체크리스트

- 쿼리-키-값(QKV)이 어텐션 계산을 설명하는 이름이라는 점을 설명할 수 있는가?
- 멀티헤드 어텐션이 왜 여러 관점의 참조 계산으로 읽히는지 말할 수 있는가?
- query, key, value를 `질문`, `표지`, `가져올 내용`의 역할 차이로 설명할 수 있는가?
- multi-head attention은 한 종류의 관계만 보지 않고 여러 관점의 관련성을 함께 읽는 방식이라는 점을 말할 수 있는가?
- single-head와 multi-head의 차이를 `절충된 하나의 관계`와 `여러 관계 관점의 동시 유지`로 나눠 말할 수 있는가?
- attention 직관만으로는 query, key, value 이름이 갑자기 튀어 보일 때, QKV 회수 관점을 먼저 떠올릴 수 있는가?
- head를 왜 여러 개 두는지 설명해야 할 때, single-head 절충과 multi-head 다관점 유지 차이를 다시 볼 수 있는가?
- 다음 Transformer 절을 읽을 때도 먼저 `이 이름들이 왜 블록 안 핵심 부품으로 반복되는가`를 떠올릴 준비가 되어 있는가?

## 출처와 참고 자료

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-06-30.
- Jay Alammar, `The Illustrated Transformer`, 확인 날짜: 2026-06-30. [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-30. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
