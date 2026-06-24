# Section P2-3.2 근거 검토: 벡터 공간과 위치의 직관

## 검토 목적

- P2-3.2의 중심 질문은 “벡터 공간(vector space)을 AI 입문자가 어느 수준으로 이해하면 되는가?”입니다.
- 이 절은 벡터 공간의 엄밀한 공리보다, 벡터가 같은 공간 안의 위치처럼 비교될 수 있다는 직관을 설명합니다.

## 확인한 자료

P2-1.1에서 내려받아 확인한 자료를 재사용했고, 표현 학습과 단어 벡터 표현에 대한 arXiv 자료를 추가로 내려받아 확인했습니다. 원문 HTML/PDF는 `.tmp/section-p2-1-1-evidence/`와 `.tmp/section-p2-3-evidence/` 아래에 있습니다.

| 자료 | 저장 위치 | 반영 판단 |
| --- | --- | --- |
| Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* | `.tmp/section-p2-1-1-evidence/mml-book-home.html` | 머신러닝 수학 기초에서 선형대수와 벡터 공간이 중요하게 배치된다는 배경 근거로 사용했습니다. |
| Goodfellow, Bengio, Courville, *Deep Learning* | `.tmp/section-p2-1-1-evidence/deeplearningbook-home.html` | 표현 학습과 벡터 표현을 읽기 위한 선형대수 배경 근거로 사용했습니다. |
| Harris et al., *Array Programming with NumPy* | `.tmp/section-p2-1-1-evidence/harris-2020-array-programming-numpy.pdf` | 배열과 차원, shape의 코드적 감각을 연결하는 배경 근거로 사용했습니다. |
| Bengio, Courville, Vincent, *Representation Learning: A Review and New Perspectives* | `.tmp/section-p2-3-evidence/bengio-2013-representation-learning-review.html`, `.tmp/section-p2-3-evidence/bengio-2013-representation-learning-review.pdf` | 데이터 표현과 표현 학습, 기하학적 연결을 설명하는 근거로 사용했습니다. |
| Mikolov, Chen, Corrado, Dean, *Efficient Estimation of Word Representations in Vector Space* | `.tmp/section-p2-3-evidence/mikolov-2013-word-representations-vector-space.html`, `.tmp/section-p2-3-evidence/mikolov-2013-word-representations-vector-space.pdf` | 단어를 연속 벡터 표현으로 학습하고 유사도 과제로 평가한 사례 근거로 사용했습니다. |

## 본문 반영 기준

- 벡터 공간(vector space)을 “벡터들이 같은 규칙으로 놓이고 비교되는 계산 가능한 자리”로 설명했습니다.
- P2-3.1의 스칼라, 벡터, 행렬 흐름이 벡터 공간의 위치 비교로 이어진다는 연결 문단을 추가했습니다.
- 벡터를 좌표처럼 읽는 직관을 사용하되, 엄밀한 수학 정의와 동일시하지 않았습니다.
- 차원(dimension)은 입문 단계에서 벡터가 가진 값의 개수 또는 좌표 축의 수로 설명했습니다.
- 벡터 공간의 최소 수학 규칙으로 벡터 덧셈(vector addition), 스칼라배(scalar multiplication), 선형 결합(linear combination)을 가볍게 소개했습니다.
- 가까운 벡터가 비슷함의 후보가 될 수 있지만 정답은 아니며 검증이 필요하다고 설명했습니다.
- 위치(position), 거리(distance), 위상(topology)을 같은 말로 섞지 않도록 구분하는 문단을 추가했습니다.
- Bengio et al.과 Mikolov et al.을 표현 학습과 단어 벡터 표현의 학술 근거로 추가했습니다.
- 임베딩(embedding), 유사도 검색(similarity search), RAG, 추천(recommendation), 클러스터링(clustering)으로 다시 등장하는 위치를 안내했습니다.

## Section 경계 검토

- P2-3.2는 벡터 공간과 위치의 직관만 다룹니다.
- 거리(distance), 내적(inner product), 코사인 유사도(cosine similarity)의 계산은 후속 수학/검색 절로 넘겼습니다.
- 행렬 곱(matrix multiplication)과 선형 변환(linear transformation)은 P2-3.3으로 넘겼습니다.
- 벡터 공간의 공리 전체는 다루지 않고, 덧셈과 스칼라배가 가능한 계산 구조라는 수준으로 제한했습니다.
- NumPy로 벡터 공간을 계산하거나 시각화하는 실습은 P2-3.4와 P2-13.x로 넘겼습니다.
- 임베딩과 RAG의 서비스 구조는 Part 1에서 다룬 내용을 다시 확장하지 않고, 수학 직관의 연결점으로만 언급했습니다.
- 위상(topology)은 용어 혼동 방지를 위한 짧은 구분으로만 설명하고, 위상수학의 정의나 정리는 다루지 않았습니다.

## 용어 검토

- `벡터(vector)`, `벡터 공간(vector space)`, `차원(dimension)`, `좌표(coordinate)`, `위치(position)`, `거리(distance)`, `위상(topology)`, `매니폴드(manifold)`, `연속성(continuity)`, `벡터 덧셈(vector addition)`, `스칼라배(scalar multiplication)`, `선형 결합(linear combination)`, `공리(axiom)`, `임베딩(embedding)`, `특징(feature)`, `유사도(similarity)`, `검색(search)`, `유사도 검색(similarity search)`, `RAG(retrieval-augmented generation)`, `추천(recommendation)`, `분류(classification)`, `클러스터링(clustering)`, `표현(representation)`을 한영 병기했습니다.

## 주의한 오해

- 벡터 공간을 단순히 “그림 위의 점”으로만 단정하지 않았습니다. 2차원 그림은 직관이고, 실제 AI 벡터는 고차원일 수 있음을 명시했습니다.
- 가까운 벡터가 항상 의미적으로 유사하다고 단정하지 않았습니다.
- 임베딩의 각 차원이 사람이 붙인 명확한 의미를 갖는다고 단정하지 않았습니다.
- 위상(topology)을 위치(position)나 거리(distance)와 같은 뜻으로 설명하지 않았습니다.
- 벡터 공간의 공리, 기저, 선형 독립 같은 엄밀한 선형대수 주제는 이 절에서 제외했습니다.

## 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/), Cambridge University Press, 2020, 확인 날짜: 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/), MIT Press, 2016, 확인 날짜: 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256), Nature, 2020, 확인 날짜: 2026-06-24.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538), arXiv, 2012, 확인 날짜: 2026-06-24.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781), arXiv, 2013, 확인 날짜: 2026-06-24.
