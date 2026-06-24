# Section P2-3.5 근거 검토: 선형대수를 NumPy로 확인하기

## 검토 목적

- P2-3.5의 중심 질문은 “P2-3.1부터 P2-3.3까지 본 선형대수 개념을 NumPy 코드로 어떻게 확인할 수 있는가?”입니다.
- 이 절은 NumPy 문법 전체가 아니라, 벡터, 행렬, shape, 위치별 곱, 행렬 곱을 작은 코드로 확인하는 데 집중합니다.

## 확인한 자료

P2-1.1에서 내려받아 확인한 NumPy 관련 자료를 재사용했습니다. 원문 PDF는 `.tmp/section-p2-1-1-evidence/` 아래에 있습니다. NumPy 공식 문서는 온라인 문서 기준으로 확인했습니다. Colab 사용 안내는 P2-3.4로 분리했습니다.

| 자료 | 저장 위치 | 반영 판단 |
| --- | --- | --- |
| NumPy Developers, *NumPy documentation* | 온라인 문서 | NumPy가 배열 계산을 제공하는 표준적 파이썬 라이브러리라는 배경 근거로 사용했습니다. |
| NumPy Developers, *NumPy quickstart* | 온라인 문서 | 배열 생성, shape, 기본 연산의 문서적 배경으로 사용했습니다. |
| Harris et al., *Array Programming with NumPy* | `.tmp/section-p2-1-1-evidence/harris-2020-array-programming-numpy.pdf` | NumPy와 배열 프로그래밍의 과학 계산 맥락을 설명하는 근거로 사용했습니다. |

## 본문 반영 기준

- NumPy 배열(array)을 벡터와 행렬의 코드 표현으로 설명했습니다.
- `.shape` 확인을 수식과 코드 사이를 연결하는 핵심 습관으로 배치했습니다.
- 벡터 덧셈(vector addition), 스칼라배(scalar multiplication), 위치별 곱(element-wise multiplication), 행렬 곱(matrix multiplication)을 작은 예제로 제한했습니다.
- NumPy의 `*`와 `@`를 명확히 구분했습니다.
- 여러 샘플을 행렬로 묶어 같은 가중치 행렬을 적용하는 배치(batch) 계산을 P2-3.3과 연결했습니다.
- shape 오류는 실제 오류 메시지 분석보다 “왜 모양이 맞지 않는가”를 이해하는 방향으로 설명했습니다.
- 본문 예제를 내려받아 실행할 수 있도록 `docs/assets/part-02/chapter-03/p2_3_5_numpy_linear_algebra.py`를 추가했습니다.

## Section 경계 검토

- P2-3.5는 NumPy 실습 입문입니다.
- NumPy 설치, 패키지 관리, 가상환경 운영은 상세히 다루지 않고 최소 안내만 넣었습니다.
- Colab 사용 안내와 `%pip` 설명은 P2-3.4로 분리했습니다.
- 브로드캐스팅(broadcasting), dtype, 성능 최적화, GPU 계산은 다루지 않았습니다.
- 확률, 미분, 최적화, 신경망 구현은 후속 장으로 넘겼습니다.
- 행렬 곱의 수학적 직관은 P2-3.3에서 이미 설명했으므로 이 절에서는 코드 확인에 집중했습니다.

## 용어 검토

- `NumPy`, `파이썬(Python)`, `배열(array)`, `shape`, `벡터 덧셈(vector addition)`, `스칼라배(scalar multiplication)`, `위치별 곱(element-wise multiplication)`, `행렬 곱(matrix multiplication)`, `가중치 행렬(weight matrix)`, `샘플(sample)`, `배치(batch)`, `브로드캐스팅(broadcasting)`을 한영 병기했습니다.

## 검증 메모

- 현재 로컬 `.venv`에 NumPy 2.0.2를 설치했습니다.
- 본문 예제의 산술은 P2-3.3에서 사용한 작은 행렬 계산과 일치하며, `p2_3_5_numpy_linear_algebra.py`를 실행해 결과를 확인했습니다.
- MkDocs 렌더링 빌드에서 코드 블록과 수식이 깨지지 않는지 확인합니다.

## 주의한 오해

- NumPy의 `*`를 행렬 곱으로 설명하지 않았습니다.
- `@`를 모든 상황에서 AI 모델 계산 전체와 동일시하지 않았습니다.
- shape이 맞으면 의미도 항상 맞는다고 단정하지 않았습니다. shape은 계산 가능 여부를 알려 주지만, 데이터 의미 검토는 별도임을 전제로 했습니다.

## 참고 자료

- NumPy Developers, [NumPy documentation](https://numpy.org/doc/), 확인 날짜: 2026-06-24.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html), 확인 날짜: 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256), Nature, 2020, 확인 날짜: 2026-06-24.
