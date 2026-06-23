# Section 13.3 근거 검토: RAG로 이어지는 흐름

## 검토 목적

- 13.3의 중심 질문은 “검색된 문서 후보를 LLM 답변에 어떻게 연결하는가?”입니다.
- 13.1은 임베딩, 13.2는 유사도 검색을 다뤘으므로, 13.3은 검색 결과를 입력 맥락으로 보강해 생성에 연결하는 흐름만 다뤘습니다.

## 확인한 자료

원문 PDF와 arXiv HTML 메타데이터를 `.tmp/section-13-3-evidence/` 아래에 내려받았습니다. 로컬 환경에 `pdftotext`, `pypdf`, `pdfplumber`가 없어 PDF 텍스트 전체 추출은 하지 못했습니다. 대신 arXiv HTML의 제목, 저자, 초록, 메타데이터를 확인하고 PDF 파일을 함께 보관했습니다.

| 자료 | 위치 | 반영 판단 |
| --- | --- | --- |
| Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, 2020 | `.tmp/section-13-3-evidence/lewis-2020-retrieval-augmented-generation.pdf`, `.html` | RAG를 pre-trained parametric memory와 dense vector index 기반 non-parametric memory를 결합한 generation 구조로 설명하는 핵심 근거로 사용했습니다. |
| Karpukhin et al., *Dense Passage Retrieval for Open-Domain Question Answering*, 2020 | `.tmp/section-13-3-evidence/karpukhin-2020-dense-passage-retrieval.pdf`, `.html` | open-domain QA에서 passage retrieval이 candidate contexts를 고르는 단계라는 근거로 사용했습니다. |
| Guu et al., *REALM: Retrieval-Augmented Language Model Pre-Training*, 2020 | `.tmp/section-13-3-evidence/guu-2020-realm.pdf`, `.html` | 언어 모델의 implicit knowledge와 외부 문서 검색을 결합해 modularity와 interpretability를 얻으려는 흐름의 근거로 사용했습니다. |

## 본문 반영 기준

- RAG(retrieval-augmented generation)를 “검색한 뒤 생성한다”는 입문용 흐름으로 설명했습니다.
- 검색(retrieval), 보강(augmentation), 생성(generation)을 분리해 설명했습니다.
- parametric memory와 non-parametric memory는 학술 용어이므로 한영 병기하고, 입문자용으로 “모델 내부 지식”과 “외부 검색 자료”로 풀어 설명했습니다.
- RAG가 최신성(recency), 근거성(evidence), 출처 추적(provenance)에 도움을 줄 수 있지만 자동 보장은 아니라고 정리했습니다.
- RAG를 프롬프트(prompt)의 대체물이 아니라 프롬프트 맥락(context)을 준비하는 구조로 설명했습니다.

## Section 경계 검토

- 13.3은 RAG의 개념 흐름과 한계에 집중합니다.
- 13.1의 임베딩 설명과 13.2의 유사도 검색 설명을 반복하지 않고 연결만 했습니다.
- 벡터 데이터베이스(vector database), 인덱스(index), 근사 최근접 이웃(approximate nearest neighbor, ANN), 그래프(graph) 기반 구현은 13.4로 넘겼습니다.
- 14장의 AI 서비스 아키텍처, 도구 사용(tool use), 에이전트(agent), 하네스(harness)는 예고만 하고 설명하지 않았습니다.

## 용어 검토

- `RAG(retrieval-augmented generation)`, `검색(retrieval)`, `보강(augmentation)`, `생성(generation)`, `맥락(context)`, `모델 내부 지식(parametric memory)`, `외부 검색 자료(non-parametric memory)`, `최신성(recency)`, `근거성(evidence)`, `출처 추적(provenance)`, `파이프라인(pipeline)`, `조각 나누기(chunking)`를 한영 병기했습니다.
- `RAG`는 사실 검증 장치가 아니라 검색 후보를 입력 맥락에 연결하는 구조로 제한했습니다.
- `출처 표시`와 `정확성 보장`을 같은 것으로 설명하지 않았습니다.

## 주의한 오해

- RAG를 쓰면 환각이 사라진다고 설명하지 않았습니다.
- 검색 결과를 정답 또는 검증 완료 자료로 설명하지 않았습니다.
- 모델 내부 지식을 “없다”고 설명하지 않았고, 외부 검색 자료와의 역할 차이로 설명했습니다.
- RAG를 프롬프트 엔지니어링의 반대 개념으로 설명하지 않았습니다.
- 구현 세부와 서비스 운영 문제를 13.3에서 과도하게 확장하지 않았습니다.

## 참고 자료

- Patrick Lewis et al., [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401), arXiv, 2020, 확인 날짜: 2026-06-23.
- Vladimir Karpukhin et al., [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906), arXiv, 2020, 확인 날짜: 2026-06-23.
- Kelvin Guu et al., [REALM: Retrieval-Augmented Language Model Pre-Training](https://arxiv.org/abs/2002.08909), arXiv, 2020, 확인 날짜: 2026-06-23.
