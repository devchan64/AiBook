# Section 13.4 근거 검토: 벡터 검색 구현의 직관

## 검토 목적

- 13.4의 중심 질문은 “벡터가 아주 많아지면 가까운 후보를 어떻게 빨리 찾는가?”입니다.
- 13.2가 유사도 검색의 개념, 13.3이 RAG 연결 흐름을 다뤘으므로, 13.4는 인덱스와 근사 검색의 구현 직관만 다뤘습니다.

## 확인한 자료

원문 PDF와 arXiv HTML 메타데이터를 `.tmp/section-13-4-evidence/` 아래에 내려받았습니다.

| 자료 | 위치 | 반영 판단 |
| --- | --- | --- |
| Malkov and Yashunin, *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs*, 2016 | `.tmp/section-13-4-evidence/malkov-2016-hnsw.pdf`, `.html` | HNSW를 그래프 기반 approximate K-nearest neighbor search의 대표 사례로 설명하는 근거로 사용했습니다. |
| Johnson, Douze, Jegou, *Billion-scale similarity search with GPUs*, 2017 | `.tmp/section-13-4-evidence/johnson-2017-billion-scale-similarity-search.pdf`, `.html` | 대규모 similarity search가 고차원 feature와 specific indexing structures를 요구한다는 근거와 brute-force, approximate, compressed-domain search 구분의 배경으로 사용했습니다. |

## 본문 반영 기준

- 전체 비교(brute-force search)는 개념적으로만 설명했습니다.
- 인덱스(index)는 검색을 빠르게 하기 위한 사전 준비 구조로 설명했습니다.
- 근사 최근접 이웃(approximate nearest neighbor, ANN)은 속도와 검색 품질 사이의 절충으로 설명했습니다.
- 그래프(graph) 기반 검색은 노드(node)와 간선(edge)으로 가까운 벡터 사이의 연결을 만들고, 그 연결을 따라 후보를 좁히는 직관으로 설명했습니다.
- HNSW(hierarchical navigable small world)는 대표 예로만 소개하고, 구현 파라미터나 알고리즘 세부는 다루지 않았습니다.

## Section 경계 검토

- 13.4는 벡터 검색 구현의 직관에 집중합니다.
- 13.1의 임베딩 생성, 13.2의 유사도 계산, 13.3의 RAG 입력 구성은 반복하지 않았습니다.
- Part 2의 그래프 자료구조 설명을 선행 지식으로 요구하지 않고, 후속 보강 위치로만 연결했습니다.
- 14장의 서비스 아키텍처, 권한 관리, 운영 모니터링은 상세히 설명하지 않았습니다.

## 용어 검토

- `전체 비교(brute-force search)`, `인덱스(index)`, `근사 최근접 이웃(approximate nearest neighbor, ANN)`, `그래프(graph)`, `노드(node)`, `간선(edge)`, `HNSW(hierarchical navigable small world)`, `벡터 데이터베이스(vector database)`, `메타데이터(metadata)`, `필터링(filtering)`, `지연 시간(latency)`, `재현율(recall)`, `정밀도(precision)`, `비용(cost)`을 한영 병기했습니다.
- `근사`를 “대충 찾기”가 아니라 속도와 품질의 절충으로 설명했습니다.
- `벡터 데이터베이스`를 검색 알고리즘 하나로 축소하지 않고 저장, 인덱스, 메타데이터, 필터링, 업데이트를 함께 다루는 시스템으로 설명했습니다.

## 주의한 오해

- HNSW를 벡터 검색의 유일한 방법으로 설명하지 않았습니다.
- 그래프 기반 검색을 일반 그래프 이론 전체로 확장하지 않았습니다.
- ANN이 항상 정확한 최근접 이웃을 보장한다고 설명하지 않았습니다.
- 벡터 데이터베이스를 사용하면 RAG 품질 문제가 자동으로 해결된다고 설명하지 않았습니다.
- recall, precision을 평가 지표 장 전체로 확장하지 않고 입문 수준의 직관으로 제한했습니다.

## 참고 자료

- Yu. A. Malkov, D. A. Yashunin, [Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs](https://arxiv.org/abs/1603.09320), arXiv, 2016, 확인 날짜: 2026-06-23.
- Jeff Johnson, Matthijs Douze, Herve Jegou, [Billion-scale similarity search with GPUs](https://arxiv.org/abs/1702.08734), arXiv, 2017, 확인 날짜: 2026-06-23.
