# P2-11.3 근거 검토: 브로드캐스팅과 벡터화

확인 날짜: 2026-06-25

## 사용한 주요 자료

| 자료 | 확인 내용 | 반영 위치 |
| --- | --- | --- |
| NumPy Developers, `Broadcasting` | broadcasting은 서로 다른 shape을 가진 배열을 산술 연산에서 어떻게 다루는지 설명하는 용어이며, 작은 배열이 큰 배열과 호환되는 shape처럼 취급된다고 설명한다. 또한 broadcasting이 배열 연산을 vectorize하는 수단을 제공하고, Python 대신 C 수준에서 반복이 일어나도록 돕는다고 설명한다. 단, 특정 경우 메모리 사용이 비효율적일 수 있음을 경고한다. | broadcasting 정의, scalar broadcasting, `(4, 3) + (3,)`, vectorization 설명, 주의점 |
| NumPy Developers, `NumPy quickstart` | 배열의 산술 연산이 elementwise로 적용되고, ufunc와 broadcasting rules가 서로 다른 shape을 다루는 데 사용된다고 설명한다. | element-wise 계산, shape 확인 습관 |
| NumPy Developers, `NumPy: the absolute basics for beginners` | broadcasting이 배열 사이의 연산을 허용하는 메커니즘이며, 배열과 스칼라 계산의 예를 제공한다. | 초심자용 scalar broadcasting 설명 |

## 작성 판단

- P2-11.1은 배열 생성과 shape 확인, P2-11.2는 인덱싱·슬라이싱·axis를 다루었으므로 P2-11.3은 배열 전체에 계산을 적용하는 방식으로 범위를 제한했다.
- broadcasting을 “자동 복사”로 단정하지 않고, 계산 규칙상 작은 배열이 큰 배열에 맞춰 적용된다고 설명했다.
- vectorization을 “반복이 사라진다”로 표현하지 않고, Python 반복문을 배열 연산으로 표현하는 방식이라고 정리했다.
- `(4, 3) + (3,)`은 가능하지만 `(4, 3) + (4,)`은 실패할 수 있는 예를 넣어 shape 확인의 필요성을 강조했다.
- 특징별 평균 제거 예제는 P2-11.2의 `axis=0`과 자연스럽게 연결되도록 구성했다.
- 도식 `broadcast-scalar-array.svg`, `broadcast-row-vector.svg`, `vectorization-loop-array.svg`는 자체 제작했다. NumPy 공식 도식을 복제하지 않았다.

## 본문에 반영한 안전한 설명

- 브로드캐스팅은 작은 값이나 작은 배열을 큰 배열의 shape에 맞춰 계산하게 해 주는 규칙으로 설명했다.
- 스칼라와 배열의 계산은 각 위치에 같은 값을 적용하는 element-wise 계산으로 설명했다.
- `(4, 3)` 배열과 `(3,)` 배열의 계산은 길이 3 벡터가 각 행에 적용되는 예로 설명했다.
- shape이 맞지 않으면 `ValueError`가 날 수 있음을 예제로 보였다.
- 벡터화는 반복 계산을 배열 연산으로 표현하는 방식이며, 내부적으로 반복 자체가 완전히 사라지는 것은 아니라고 설명했다.
- broadcasting은 편리하지만 복잡한 경우 해석 난이도와 메모리 사용 문제가 생길 수 있다고 설명했다.

## 제외한 내용

- `np.newaxis`
- `reshape`를 이용한 고급 broadcasting 제어
- stride와 memory view
- broadcasting 성능 벤치마크
- ufunc 내부 구현
- GPU tensor operation
- 3차원 이상 배열의 복잡한 broadcasting

이 내용은 이후 작은 모델 계산이나 딥러닝 프레임워크를 다룰 때 필요한 만큼 다시 다룬다.
