# Section 13.1 근거 검토: 텍스트를 벡터로 표현한다는 것

## 검토 목적

- 13.1의 중심 질문은 “텍스트를 벡터로 표현한다는 것은 무엇인가?”입니다.
- 11.1에서 임베딩의 역사적 흐름을 이미 다뤘으므로, 13.1은 프롬프트 이후 서비스 흐름에서 임베딩이 검색과 비교로 이어지는 직관을 설명하는 절로 작성했습니다.

## 확인한 자료

11.1에서 내려받아 확인한 자료를 재사용했습니다. 원문 PDF와 추출 텍스트는 `.tmp/section-11-1-evidence/` 아래에 있습니다.

| 자료 | 위치 | 반영 판단 |
| --- | --- | --- |
| Jurafsky & Martin, *Speech and Language Processing*, Chapter 6 | `.tmp/section-11-1-evidence/jurafsky-martin-slp3-ch06-vector-semantics.pdf`, `.txt` | token embedding, embedding matrix, static embedding, contextual embedding, pooling 설명의 근거로 사용했습니다. |
| Bengio et al., *A Neural Probabilistic Language Model*, 2003 | `.tmp/section-11-1-evidence/bengio-2003-neural-probabilistic-language-model.pdf`, `.txt` | 단어의 distributed representation과 유사 단어 일반화의 역사적 배경 근거로 사용했습니다. |
| Mikolov et al., *Efficient Estimation of Word Representations in Vector Space*, 2013 | `.tmp/section-11-1-evidence/mikolov-2013-efficient-estimation-word-representations.pdf`, `.txt` | vector space, syntactic/semantic similarity, cosine distance, information retrieval 응용 가능성 언급의 근거로 사용했습니다. |
| Mikolov et al., *Distributed Representations of Words and Phrases and their Compositionality*, 2013 | `.tmp/section-11-1-evidence/mikolov-2013-distributed-representations-phrases.pdf`, `.txt` | distributed vector representation과 nearest neighbour 예시의 배경 근거로 사용했습니다. |

## 본문 반영 기준

- 임베딩(embedding)을 텍스트를 벡터 표현(vector representation)으로 바꾸는 방법으로 설명했습니다.
- 벡터(vector)는 사람이 직접 해석해야 하는 좌표가 아니라 모델과 검색 시스템이 계산하는 표현으로 설명했습니다.
- 벡터 공간(vector space)은 텍스트 비교를 가능하게 하는 공간이라는 직관까지만 설명했습니다.
- 선형대수(linear algebra)나 확률(probability) 계산을 13.1의 선행 조건으로 두지 않고, 벡터와 거리의 직관만 요구했습니다.
- 유사도(similarity), 거리(distance), cosine similarity의 계산 방식은 13.2로 넘겼습니다.
- RAG(retrieval-augmented generation)의 전체 구조는 13.3으로 넘겼습니다.

## Section 경계 검토

- 13.1은 “벡터로 표현한다”는 직관에 집중합니다.
- 13.2는 벡터 사이의 가까움을 계산하고 검색하는 절입니다.
- 13.3은 검색 결과를 LLM 입력으로 연결하는 RAG 흐름을 다룹니다.
- 11.1의 word2vec, CBOW, Skip-gram 역사 설명을 반복하지 않았습니다.
- 14장의 도구 사용(tool use), 에이전트(agent), 하네스(harness) 구조를 설명하지 않았습니다.

## 용어 검토

- `텍스트(text)`, `벡터(vector)`, `임베딩(embedding)`, `벡터 표현(vector representation)`, `벡터 공간(vector space)`, `학습된 표현(learned representation)`, `단어(word)`, `토큰(token)`, `문장(sentence)`, `문단(paragraph)`, `문서(document)`, `조각(chunk)`, `유사도 검색(similarity search)`을 한영 병기했습니다.
- `의미`라는 표현은 조심해서 사용했습니다. 임베딩을 의미 자체로 단정하지 않고, 모델이 학습한 기준에 따른 수치 표현으로 설명했습니다.
- `가깝다`는 표현은 계산 가능한 벡터 공간에서의 가까움이며, 실제 의미 동일성을 보장하지 않는다는 주의점을 남겼습니다.

## 주의한 오해

- 임베딩을 문장의 진짜 의미를 완벽히 저장한 값으로 설명하지 않았습니다.
- 임베딩을 최신 사실이나 근거 검증 장치로 설명하지 않았습니다.
- 문서 임베딩과 RAG를 만능 검색 해결책처럼 설명하지 않았습니다.
- 유사도 계산과 벡터 데이터베이스 구조를 13.1에서 자세히 설명하지 않았습니다.
- 13.1을 선형대수나 확률 이론 설명으로 확장하지 않았습니다.

## 참고 자료

- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, Chapter 6: Neural Networks and Neural Language Models](https://web.stanford.edu/~jurafsky/slp3/6.pdf), draft of 2026-01-06, 확인 날짜: 2026-06-23.
- Yoshua Bengio, Rejean Ducharme, Pascal Vincent, Christian Jauvin, [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html), Journal of Machine Learning Research, 2003, 확인 날짜: 2026-06-23.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781), arXiv, 2013, 확인 날짜: 2026-06-23.
- Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, Jeffrey Dean, [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546), arXiv, 2013, 확인 날짜: 2026-06-23.
