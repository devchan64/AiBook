# P4-9.2 배치(batch)와 텐서(tensor) 계산

P4-9.1에서는 딥러닝이 왜 GPU와 병렬 처리(parallel processing)에 잘 맞는지 보았습니다. 여기서 바로 다음 질문이 생깁니다.

그렇다면 GPU가 잘 처리하는 딥러닝 계산은 실제로 어떤 모양의 데이터 묶음으로 주어지는가?

이 질문에 답할 때 반복해서 등장하는 표현이 배치(batch)와 텐서(tensor)입니다.

배치(batch)는 여러 샘플을 한꺼번에 계산하기 위한 묶음이고, 텐서(tensor)는 그런 묶음을 포함해 딥러닝이 다루는 다차원 숫자 배열의 일반 이름이다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 배치(batch)는 왜 필요한가?
- 텐서(tensor)는 벡터와 행렬에서 어떻게 확장되는가?
- 배치 단위 계산은 병렬 처리와 어떤 관계가 있는가?
- 입력 shape를 읽는 감각은 왜 중요한가?

이 절은 다음 내용은 깊게 다루지 않습니다.

- 메모리 레이아웃과 stride의 내부 구현
- 프레임워크별 tensor class 세부 차이
- 분산 배치 처리(distributed batching)의 시스템 상세

이 절의 목적은 텐서 수학의 엄밀한 정의보다, `딥러닝 계산이 어떤 데이터 모양으로 흐르는가`를 설명하는 것입니다.

## 이 절의 목표

- 배치를 `여러 샘플을 한 번에 처리하는 계산 단위`로 설명할 수 있습니다.
- 텐서를 `벡터와 행렬을 포함하는 다차원 배열`로 설명할 수 있습니다.
- shape를 읽는 습관이 왜 딥러닝 실습에 중요한지 말할 수 있습니다.
- 작은 Python 예제로 batch와 tensor shape 감각을 확인할 수 있습니다.

## 배치는 왜 필요한가

딥러닝에서는 같은 모델을 많은 샘플에 반복 적용합니다. 한 샘플씩 순서대로 처리할 수도 있지만, 그러면 병렬 처리의 이점을 충분히 살리기 어렵습니다.

배치(batch)는 여러 샘플을 묶어서 한 번에 계산하는 방식입니다.

예를 들어:

- 이미지 1장만 처리하는 대신 32장을 같이 처리하고
- 문장 1개만 넣는 대신 여러 문장을 같이 넣으며
- 표 데이터도 여러 행(row)을 한 번에 모델에 전달합니다

다음처럼 이해하면 충분합니다.

`배치는 모델이 같은 연산을 여러 샘플에 반복해야 할 때, 그 반복을 한 덩어리로 묶어 계산하게 해 준다.`

## 배치를 쓰면 무엇이 좋아지나

배치를 쓰는 이유는 단순히 편의 때문만이 아닙니다.

- GPU의 병렬 계산을 더 잘 활용할 수 있고
- 샘플 하나씩 처리할 때보다 계산 효율이 좋아질 수 있으며
- gradient도 여러 샘플의 정보를 한 번에 반영하게 됩니다

물론 배치가 너무 크면 메모리를 많이 쓰거나, 학습 dynamics가 달라질 수도 있습니다. 하지만 입문 단계에서는 먼저 `병렬 계산의 기본 단위`로 이해하면 충분합니다.

## 텐서는 무엇인가

Part 2에서 스칼라(scalar), 벡터(vector), 행렬(matrix)를 보았습니다. 텐서는 이 흐름의 자연스러운 확장입니다.

다음 표로 설명하면 충분합니다.

| 이름 | 예시 | 차원 수 |
| --- | --- | --- |
| 스칼라(scalar) | `3.14` | 0차원 |
| 벡터(vector) | `[1, 2, 3]` | 1차원 |
| 행렬(matrix) | `[[1, 2], [3, 4]]` | 2차원 |
| 텐서(tensor) | 배치가 붙은 이미지/문장 배열 | 3차원 이상도 포함 |

즉, 텐서는 특별한 마법 개념이라기보다 `다차원 숫자 배열`을 넓게 부르는 이름입니다.

다음처럼 기억하면 좋습니다.

`딥러닝에서는 입력, 중간 표현, 출력이 모두 텐서로 흐른다고 보면 된다.`

## 이미지, 문장, 표 데이터는 어떤 텐서로 보이나

딥러닝에서는 데이터 종류가 달라도 결국 텐서 모양으로 정리됩니다.

예를 들어:

- 표 데이터: `(batch_size, feature_count)`
- 흑백 이미지: `(batch_size, height, width)`
- 컬러 이미지: `(batch_size, channel, height, width)` 또는 프레임워크에 따라 채널 위치가 다를 수 있음
- 문장 임베딩: `(batch_size, sequence_length, embedding_dim)`

즉, 텐서는 데이터 도메인을 넘어 공통 계산 언어 역할을 합니다.

## shape를 읽는 감각이 왜 중요한가

실습에서 가장 자주 만나는 오류 중 하나는 shape를 잘못 이해하는 것입니다.

예를 들어:

- 배치 차원을 빼먹거나
- 행과 열을 뒤집거나
- 채널 위치를 헷갈리거나
- 라벨 shape와 출력 shape가 맞지 않으면

모델이 아예 실행되지 않거나, 실행은 되지만 엉뚱한 계산을 할 수 있습니다.

다음 습관이 중요합니다.

`딥러닝 실습에서는 값 자체만 보지 말고, 항상 shape를 함께 본다.`

## 배치 계산과 병렬 처리의 연결

P4-9.1에서 본 GPU의 강점은 비슷한 연산을 많이 동시에 처리하는 데 있었습니다. 배치는 바로 그 구조를 딥러닝 계산에 맞게 제공하는 방식입니다.

즉:

- 모델은 같은 가중치를 유지한 채
- 배치 안의 여러 샘플에 대해
- 같은 forward와 backward 패턴을 반복합니다

이 반복이 batch dimension으로 묶이면서 병렬 계산과 자연스럽게 연결됩니다.

이를 아주 단순하게 그리면 다음과 같습니다.

```mermaid
flowchart LR
  A["sample 1"]
  B["sample 2"]
  C["sample 3"]
  D["batch tensor"]
  E["same model computation"]
  F["batch outputs"]

  A --> D
  B --> D
  C --> D
  D --> E --> F
```

## 사례로 보기

### 사례 1. 표 데이터 분류

고객 데이터가 100개 있고 각 고객마다 feature가 20개라면, 한 번의 배치 입력은 예를 들어 `(32, 20)` 같은 텐서로 볼 수 있습니다.

즉:

- 32는 이번 step에서 같이 처리하는 샘플 수
- 20은 한 샘플당 feature 수

를 뜻합니다.

### 사례 2. 이미지 분류

컬러 이미지 32장을 한 번에 넣는다면 `(32, 3, 224, 224)` 같은 shape가 등장할 수 있습니다. 여기서 중요한 것은 숫자를 외우는 것이 아니라, `배치`, `채널`, `높이`, `너비`가 축(axis)으로 나뉘어 있다는 점입니다.

### 사례 3. 문장 모델

문장 데이터를 다룰 때는 `(batch_size, sequence_length, embedding_dim)` 같은 shape가 자주 나옵니다. 즉, 텐서는 데이터 종류가 달라도 같은 계산 언어를 제공합니다.

## 작은 Python 예제로 보기

이번 예제의 목표는 배치와 텐서 shape를 숫자로 직접 확인하는 것입니다.

입력:

- 표 데이터 형태의 작은 배치
- 이미지 비슷한 3차원 데이터 묶음

출력:

- 각 배열의 shape
- 배치 첫 샘플과 두 번째 샘플

```python
import numpy as np

# tabular batch: 3 samples, 4 features
batch_table = np.array([
    [1.0, 0.2, 3.1, 0.0],
    [0.5, 1.4, 2.8, 1.0],
    [1.2, 0.1, 3.3, 0.0],
])

# image-like tensor: 2 samples, 2x2 grayscale images
batch_images = np.array([
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]],
])

print("batch_table shape =", batch_table.shape)
print("first tabular sample =", batch_table[0])
print("batch_images shape =", batch_images.shape)
print("first image =")
print(batch_images[0])
print("second image =")
print(batch_images[1])
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
batch_table shape = (3, 4)
first tabular sample = [1.  0.2 3.1 0. ]
batch_images shape = (2, 2, 2)
first image =
[[1 2]
 [3 4]]
second image =
[[5 6]
 [7 8]]
```

이 결과에서 읽어야 할 핵심은 다음입니다.

- `(3, 4)`는 3개 샘플과 4개 feature를 뜻합니다
- `(2, 2, 2)`는 2개 샘플이 있고, 각 샘플이 2x2 배열임을 뜻합니다
- 배치 차원은 같은 연산을 여러 샘플에 동시에 적용하기 위한 축입니다

## 역사와 커리큘럼 관점

배치와 텐서라는 표현은 단순한 라이브러리 문법이 아니라, 딥러닝이 대규모 병렬 수치 계산 체계로 정착하면서 함께 일반화된 표현입니다. GPU 기반 학습이 확산되면서, 데이터를 `샘플 하나`보다 `묶음 단위 tensor`로 보는 감각이 사실상 표준이 되었습니다.

커리큘럼 관점에서도 이 절은 중요합니다.

- Part 2의 선형대수와 NumPy 배열
- Part 3의 입력 행렬과 feature table
- Part 4의 GPU 병렬 처리

가 여기서 하나의 shape 언어로 합쳐지기 때문입니다.

즉, 텐서는 새로운 어려운 개념이라기보다, 앞에서 배운 배열 사고를 딥러닝 규모로 확장한 결과라고 보는 편이 좋습니다.

## 다음 절과의 연결

여기까지 오면 다음 질문이 남습니다.

- 이렇게 많은 텐서 계산을 거치며, 신경망은 결국 무엇을 배우는가?
- 사람이 직접 특징(feature)을 쓰지 않아도, 모델이 내부 표현(representation)을 배운다는 말은 무슨 뜻인가?

이 질문은 바로 P4-10.1 표현 학습(representation learning)으로 이어집니다.

## 이 절에서 기억할 관점

- 배치는 여러 샘플을 한꺼번에 처리하는 계산 단위입니다.
- 텐서는 딥러닝이 다루는 다차원 숫자 배열의 일반 이름입니다.
- shape를 읽는 습관은 딥러닝 실습에서 매우 중요합니다.
- 배치와 텐서는 GPU 병렬 처리와 직접 연결되는 계산 표현입니다.

## 체크리스트

- 배치와 텐서를 각각 한 문장으로 설명할 수 있는가?
- 표 데이터, 이미지, 문장이 서로 다른 shape를 갖는다는 점을 설명할 수 있는가?
- shape를 확인하는 습관이 왜 중요한지 말할 수 있는가?
- 다음 절의 표현 학습으로 왜 자연스럽게 넘어가는지 연결할 수 있는가?

## 출처와 참고 자료

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Aurélien Géron, `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow`, 3rd ed., O'Reilly, 2022, 확인 날짜: 2026-06-29.
- NumPy Developers, `ndarray`, NumPy Documentation, 확인 날짜: 2026-06-29. [https://numpy.org/doc/stable/reference/arrays.ndarray.html](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }
