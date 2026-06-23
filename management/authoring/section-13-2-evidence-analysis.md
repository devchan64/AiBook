# Section 13.2 근거 검토: 유사도 검색의 직관

## 검토 목적

- 13.2의 중심 질문은 “가까운 벡터를 찾는다는 것은 무엇이며, 왜 그것이 정답 보장이 아닌가?”입니다.
- 13.1에서 텍스트를 벡터로 표현하는 직관을 다뤘으므로, 13.2는 벡터 사이의 가까움을 이용해 후보를 찾는 검색 단계로 작성했습니다.

## 확인한 자료

11.1에서 내려받아 확인한 자료를 재사용했습니다. 원문 PDF와 추출 텍스트는 `.tmp/section-11-1-evidence/` 아래에 있습니다.

| 자료 | 위치 | 반영 판단 |
| --- | --- | --- |
| Bengio et al., *A Neural Probabilistic Language Model*, 2003 | `.tmp/section-11-1-evidence/bengio-2003-neural-probabilistic-language-model.pdf`, `.txt` | distributed feature vector가 단어 사이의 similarity를 표현하고 information retrieval과 연결될 수 있다는 배경 근거로 사용했습니다. |
| Mikolov et al., *Efficient Estimation of Word Representations in Vector Space*, 2013 | `.tmp/section-11-1-evidence/mikolov-2013-efficient-estimation-word-representations.pdf`, `.txt` | vector space에서 cosine distance로 closest word를 찾는 사례와 information retrieval 응용 가능성 언급의 근거로 사용했습니다. |
| Mikolov et al., *Distributed Representations of Words and Phrases and their Compositionality*, 2013 | `.tmp/section-11-1-evidence/mikolov-2013-distributed-representations-phrases.pdf`, `.txt` | nearest representation, nearest neighbours, cosine distance를 사용하는 벡터 공간 검색 직관의 근거로 사용했습니다. |

## 본문 반영 기준

- 유사도 검색(similarity search)을 질문 벡터(query vector)와 가까운 문서 벡터(document vector)를 찾는 과정으로 설명했습니다.
- 유사도(similarity)와 거리(distance)는 비교 기준이라는 직관까지만 설명했습니다.
- 코사인 유사도(cosine similarity)는 수식 없이 방향의 비슷함으로 설명했습니다.
- 상위 k개(top-k)는 가까운 후보 여러 개를 가져오는 방식으로 설명했습니다.
- 검색 결과는 정답이 아니라 후보(candidate)임을 반복해서 명시했습니다.

## Section 경계 검토

- 13.2는 유사도 검색의 직관과 한계에 집중합니다.
- 13.1의 임베딩 생성 직관은 반복하지 않았습니다.
- 13.3의 RAG(retrieval-augmented generation) 구조는 예고만 했습니다.
- 벡터 데이터베이스(vector database), 인덱스(index), 근사 최근접 이웃(approximate nearest neighbor, ANN)은 구현 세부로 보고 자세히 다루지 않았습니다.
- 그래프(graph) 자료구조는 벡터 검색 구현에서 다시 등장할 수 있는 배경으로만 언급하고, 13.2의 중심 설명에는 넣지 않았습니다.
- 14장의 도구 사용(tool use), 에이전트(agent), 하네스(harness) 구조를 설명하지 않았습니다.

## 용어 검토

- `유사도 검색(similarity search)`, `유사도(similarity)`, `거리(distance)`, `최근접 이웃(nearest neighbor)`, `질문 벡터(query vector)`, `문서 벡터(document vector)`, `후보(candidate)`, `코사인 유사도(cosine similarity)`, `상위 k개(top-k)`, `조각(chunk)`, `메타데이터(metadata)`, `키워드 검색(keyword search)`을 한영 병기했습니다.
- `코사인 유사도(cosine similarity)`는 방향의 비슷함이라는 직관을 설명했습니다.
- `정답`이라는 표현은 피하고, 검색 결과를 후보로 제한했습니다.

## 주의한 오해

- 가까운 벡터가 정답이나 근거 품질을 보장한다고 설명하지 않았습니다.
- 유사도 검색을 사실 검증 장치로 설명하지 않았습니다.
- 상위 k개(top-k)를 크게 하면 항상 좋아진다고 설명하지 않았습니다.
- RAG를 만능 해결책처럼 예고하지 않았습니다.
- 수식 중심의 선형대수 설명으로 확장하지 않았습니다.

## 참고 자료

- Yoshua Bengio, Rejean Ducharme, Pascal Vincent, Christian Jauvin, [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html), Journal of Machine Learning Research, 2003, 확인 날짜: 2026-06-23.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781), arXiv, 2013, 확인 날짜: 2026-06-23.
- Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, Jeffrey Dean, [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546), arXiv, 2013, 확인 날짜: 2026-06-23.
