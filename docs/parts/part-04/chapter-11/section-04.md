# P4-11.4 보충학습: 다중 클래스(multinomial) 로지스틱 회귀를 읽는 법

> Section ID: `P4-11.4`
> Version: `v2026.07.19`

P4-11.3에서 본 log-odds와 MLE는 기본적으로 `둘 중 하나를 고르는 이진 분류(binary classification)`를 기준으로 설명했습니다. 하지만 현실의 분류 문제는 셋 이상 중 하나를 고르는 경우도 많습니다.

이 절의 중심 질문은 다음입니다.

이진 분류에서 익힌 `점수 -> 확률 -> class 선택` 감각은 여러 클래스 문제에서도 어떻게 이어지는가?

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 다중 클래스(multinomial) 문제에서는 무엇이 유지되는가?
- softmax는 왜 등장하는가?
- one-vs-rest와 multinomial은 어떤 차이로 읽으면 되는가?

이 절은 다중 클래스 로지스틱 회귀를 `점수 -> 확률 분포 -> class 선택` 구조가 여러 클래스에도 이어지는 확장으로 먼저 닫고, threshold 감각이 argmax 감각으로 어떻게 옮겨가는지를 붙잡는 데 집중합니다.

대신 이번 절에서 바로 더 좁혀 볼 질문도 분명합니다. solver와 regularization의 구현 관점은 P4-11.5에서 이어서 다룹니다.

## 이 절의 목표

- 다중 클래스에서도 `입력 -> 점수 -> 확률 비교 -> class 선택` 구조가 유지된다는 점을 설명할 수 있습니다.
- softmax를 `클래스별 점수를 확률 분포로 바꾸는 함수`라고 읽을 수 있습니다.
- one-vs-rest와 multinomial의 차이를 입문 수준에서 설명할 수 있습니다.

## 학습 배경

P4-11.1에서 로지스틱 회귀를 처음 볼 때는 보통 `class 1 확률` 하나를 보고 threshold와 비교했습니다. 하지만 뉴스 분류, 고객 문의 분류, 이미지 분류처럼 현실의 많은 문제는 둘 중 하나가 아니라 여러 클래스 중 하나를 고르는 문제입니다.

예를 들면 다음과 같습니다.

| 문제 | 클래스 예 |
| --- | --- |
| 뉴스 분류 | 정치 / 경제 / 스포츠 |
| 고객 문의 분류 | 환불 / 배송 / 계정 |
| 이미지 분류 | 고양이 / 강아지 / 새 |

이때 독자가 먼저 잡아야 할 것은 `완전히 다른 모델이 시작된다`가 아니라 `이진 분류에서 익힌 읽기 틀이 넓어진다`는 점입니다.

## 주요 학습내용

### 다중 클래스에서도 점수와 확률 비교 구조는 유지된다

다중 클래스에서는 각 클래스 \(k\)마다 점수 \(z_k\)를 만든다고 생각할 수 있습니다.

\[
z_k = w_k^\top x + b_k
\]

그리고 이 점수들을 확률 분포로 바꾸기 위해 보통 softmax를 씁니다.

\[
P(y = k \mid x) = \frac{e^{z_k}}{\sum_{j=1}^{K} e^{z_j}}
\]

이 식이 말하는 핵심은 단순합니다.

- 분자는 `현재 클래스 k의 점수`
- 분모는 `모든 클래스 점수의 합`
- 따라서 한 클래스 확률은 항상 `전체 클래스들 사이의 상대 비교`로 정해집니다.

즉, 다중 클래스 로지스틱 회귀의 최소 수식 구조는 `클래스마다 점수를 만들고`, `그 점수들을 함께 정규화해 확률 분포로 바꾼다`는 두 줄입니다.

### 이진 분류의 threshold 감각은 다중 클래스에서 argmax 감각으로 옮겨간다

이진 분류에서는 `0.5를 넘는가`가 핵심 감각이었다면, 다중 클래스에서는 보통 `어느 클래스 확률이 가장 큰가`가 핵심 감각이 됩니다.

- 이진 분류: `class 1 확률` 하나를 보고 threshold와 비교
- 다중 클래스: `클래스별 확률들`을 보고 가장 큰 값을 선택

이 변화는 P4-11.1과 직접 연결됩니다. 초심자는 여기서 `확률을 여러 개 내면 더 복잡한 완전히 다른 모델인가`라고 오해하기 쉽지만, 핵심 구조는 여전히 `입력 -> 점수 -> 확률 비교 -> class 선택`입니다.

### one-vs-rest와 multinomial은 비교 방식이 다르다

입문 단계에서는 one-vs-rest와 multinomial의 차이를 다음 정도로 잡으면 충분합니다.

- one-vs-rest: 각 클래스를 `이 클래스냐 아니냐`로 따로 본 뒤 비교합니다.
- multinomial: 클래스들을 한 번에 놓고 상대 비교하는 구조로 봅니다.

아주 작은 문의 분류 장면으로 바꾸면 차이가 더 쉽게 읽힙니다.

| 읽는 방식 | 같은 문의를 어떻게 보나 |
| --- | --- |
| one-vs-rest | `환불 문의인가?`, `배송 문의인가?`, `계정 문의인가?`를 각각 따로 묻고 나중에 비교합니다. |
| multinomial | `환불 / 배송 / 계정`을 한 번에 놓고 어느 쪽이 가장 그럴듯한지 바로 비교합니다. |

세부 행렬 수식과 softmax 전개까지 현재 절에서 길게 밀어붙일 필요는 없습니다. 중요한 것은 `이진 분류에서 익힌 점수와 확률 비교 감각이 여러 클래스에도 이어진다`는 연결입니다.

우도 쪽 모양도 이진 분류와 같은 생각으로 확장됩니다. 정답 클래스가 one-hot 벡터처럼 주어졌다고 생각하면, 다중 클래스의 로그우도는 보통 다음과 같은 합 형태로 읽습니다.

\[
\log L = \sum_{i=1}^{n}\sum_{k=1}^{K} y_{ik} \log P(y=k \mid x_i)
\]

여기서 \(y_{ik}\)는 `샘플 i의 실제 정답이 클래스 k이면 1, 아니면 0`을 뜻합니다. 이 식도 결국 `실제 정답 클래스에 높은 확률을 준 쪽을 더 좋게 본다`는 생각을 다중 클래스 버전으로 적은 것입니다.

## 사례 및 예시

사례를 읽기 전에 이번 절의 비교 프레임을 먼저 한 표로 잡으면 다음과 같습니다.

| 장면 | 사람이 먼저 쓰기 쉬운 기준 | 그 기준의 한계 | 다중 클래스 로지스틱 회귀가 바꾸는 점 | 확인할 결과 |
| --- | --- | --- | --- | --- |
| 여러 클래스 분류 | 0.5 기준을 그대로 떠올린다 | 여러 클래스 비교 문제를 잘못 읽는다 | softmax와 argmax 관점으로 상대 비교하게 한다 | 가장 큰 확률의 클래스를 선택 |
| 구현 선택 | 각 클래스를 따로 떼어 본다 | 클래스 간 상대 비교를 놓친다 | multinomial 구조로 한 번에 경쟁하게 읽는다 | 클래스 전체 분포를 함께 봄 |

### 사례 1. 다중 클래스에서는 0.5보다 상대 비교가 중요하다

고객 문의 분류에서 세 클래스가 `환불`, `배송`, `계정`이라고 해 보겠습니다. 어떤 문의에 대해 확률이 `[0.41, 0.39, 0.20]`으로 나왔다면, 0.5를 넘는 값은 없습니다. 하지만 모델은 여전히 `환불`을 가장 그럴듯하게 보고 있습니다.

이 장면은 다중 클래스에서 `0.5를 넘는가`보다 `무엇이 가장 큰가`가 더 중요해진다는 점을 보여 줍니다.

### 사례 2. 같은 입력도 one-vs-rest와 multinomial은 읽는 방식이 다르다

문의 내용에 `환불`, `결제 취소`, `계정 잠금` 같은 표현이 함께 섞여 있으면, one-vs-rest는 각 클래스를 따로 점검한 뒤 비교합니다. 반면 multinomial은 클래스 전체를 한 번에 놓고 상대 확률을 정합니다. 초심자 입장에서는 후자가 `한 번의 비교 구조`로 읽히기 쉬울 때가 많습니다.

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-4-mermaid-01-ko.mmd"
```

## 연습 및 예제

### Python 예제로 다중 클래스 확률표 읽기

아래 예제는 다중 클래스에서 `0.5를 넘는가`보다 `가장 큰 확률이 무엇인가`를 읽는 기본 감각을 보여 줍니다.

| 입력 묶음 | 뜻 |
| --- | --- |
| `class_names` | 클래스 이름 목록 |
| `multi_proba` | 클래스별 확률 분포 예시 |

```python
import numpy as np

class_names = ["refund", "shipping", "account"]
multi_proba = np.array([
    [0.41, 0.39, 0.20],
    [0.18, 0.63, 0.19],
    [0.22, 0.28, 0.50],
])

print("multiclass predictions")
for row in multi_proba:
    best_idx = int(np.argmax(row))
    print(
        "  probs =",
        np.round(row, 2),
        "->",
        class_names[best_idx],
    )
```

실행 결과 예시는 다음과 같습니다.

```text
multiclass predictions
  probs = [0.41 0.39 0.2 ] -> refund
  probs = [0.18 0.63 0.19] -> shipping
  probs = [0.22 0.28 0.5 ] -> account
```

이 출력은 다음처럼 읽으면 됩니다.

- 첫 번째 행은 0.5를 넘는 값이 없어도 가장 큰 확률인 `refund`를 고릅니다.
- 다중 클래스에서는 `확률 하나 vs threshold`보다 `확률 분포 전체의 상대 비교`가 중요합니다.
- 즉, 기본 감각은 threshold보다 argmax 쪽으로 이동합니다.

## 출처와 참고 자료

- C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006. 확인 날짜: 2026-07-19. [https://link.springer.com/book/9780387310732](https://link.springer.com/book/9780387310732){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, linear models user guide, [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-09
- scikit-learn, `LogisticRegression` API documentation, [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-09
