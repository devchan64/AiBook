# 3.3 근거 분석: 규칙 기반 접근(rule-based approach)과 표현 학습(representation learning)

이 문서는 `docs/chapters/chapter-03/section-03.md`의 근거 연결을 검토한 관리 메모입니다.

원문 확인 규칙에 따라 이미 내려받은 자료와 새로 내려받은 자료를 사용했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 확인한 자료

| 자료 | 로컬 확인 | 본문 반영 역할 |
| --- | --- | --- |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | `.tmp/section-01-evidence/sep-ai.html` | feature vector representation, 특징 표현 함수, 딥러닝의 계층적 추상화 설명 근거 |
| Bengio, Courville, Vincent, `Representation Learning: A Review and New Perspectives` | `.tmp/section-3-3-evidence-bengio-representation-learning.html` | 머신러닝 성능이 데이터 표현에 의존하고, 표현이 데이터의 설명 요인을 드러내거나 숨길 수 있다는 설명 근거 |
| George A. Miller, `The Magical Number Seven, Plus or Minus Two` | `.tmp/section-3-2-evidence/miller-magical-number-seven.html` | 청킹(chunking), 재부호화(recoding), 익숙한 단위로 입력을 묶어 처리한다는 학습용 비유의 근거 |

## 핵심 근거 연결

| 본문 주장 | 근거 | 반영 판단 |
| --- | --- | --- |
| 명시적 규칙은 사람이 읽고 수정할 수 있는 외부 기준으로 설명할 수 있다 | 3.1의 규칙 기반 시스템 설명과 연결. 새 외부 근거를 추가하지 않고 기존 장의 정의를 재사용 | 유지 |
| 특징은 입력을 모델이 쓰기 쉬운 형태로 바꾸는 값으로 설명할 수 있다 | SEP AI 항목은 입력을 feature vector representation으로 변환하고, 해당 표현이 불필요한 정보를 버리고 과제에 유용한 정보를 남기려 한다고 설명함 | 유지 |
| 특징 표현이 좋으면 학습 문제가 더 쉬워질 수 있다 | SEP AI 항목은 도메인 전문가가 제공한 feature representation이 과제 난이도의 일부를 떠안을 수 있다고 설명함 | 유지 |
| 딥러닝은 여러 층을 통해 점점 추상적인 표현을 만들 수 있다 | SEP AI 항목은 얼굴 이미지 예시에서 낮은 층이 edge, 다음 층이 얼굴 특징, 더 높은 층이 특징 묶음에 반응할 수 있다고 설명함 | 유지하되 딥러닝 상세는 후속 파트로 보냄 |
| 머신러닝 알고리즘의 성공은 데이터 표현에 크게 의존한다 | Bengio et al. 리뷰의 초록은 성공이 데이터 표현에 의존하고, 표현이 설명 요인을 더 드러내거나 숨길 수 있다고 설명함 | 유지 |
| 사람의 빠른 판단은 입력을 의미 단위로 묶어 처리한다는 비유로 설명할 수 있다 | Miller는 입력을 익숙한 units or chunks로 조직하고, 더 큰 chunk로 재부호화하면 기억 가능한 정보량이 늘 수 있다고 설명함 | `컨텍스트 압축`을 표준 신경과학 용어로 쓰지 않고 표현 학습을 이해하는 보조 비유로만 사용 |
| 학습된 표현은 사람이 바로 읽을 수 있는 규칙 목록과 다르다 | 표현 학습과 규칙 기반 시스템의 성격 차이를 본문에서 일반화 | 유지하되 “모델이 규칙을 스스로 작성한다”처럼 단정하지 않음 |
| 규칙과 모델은 경쟁만 하는 관계가 아니라 역할 분담할 수 있다 | 3.1과 3.2의 결론을 연결한 저자적 일반화 | 유지. 특정 제품 구조처럼 단정하지 않음 |

## 주의한 표현

- 3.3은 규칙 기반 시스템의 역사나 전문가 시스템 사례를 다시 설명하지 않습니다. 이는 3.1과 2.1의 범위입니다.
- 3.3은 3.2의 학습 데이터, 라벨, 학습, 추론 구조를 반복하지 않습니다. 이 절의 중심은 입력이 모델 내부에서 표현으로 바뀌는 위치와 의미입니다.
- 3.3은 모델 학습 알고리즘, 손실 함수, 역전파, 신경망 구조를 자세히 설명하지 않습니다. 이는 Part 3과 Part 4로 넘깁니다.
- `표현(representation)`은 사람이 읽을 수 있는 의미 단위로 항상 분해된다고 단정하지 않습니다. 본문의 고객 문의 표는 학습용 단순화입니다.
- `컨텍스트 압축`은 본문에서 표준 용어로 정의하지 않습니다. 사용자의 직관을 일반화한 학습용 비유이며, 청킹과 재부호화 근거를 연결해 “입력을 표현으로 다시 묶는 관점”으로만 설명합니다.
- SEP의 얼굴 이미지 계층 예시는 딥러닝의 계층적 표현을 설명하는 근거로만 사용합니다. 신경망이 사람의 뇌처럼 이해한다는 주장으로 쓰지 않습니다.
- Bengio et al. 자료는 표현 학습의 중요성을 뒷받침하지만, 3.3에서는 비지도 표현 학습이나 manifold learning 세부 내용으로 확장하지 않습니다.
- 규칙 기반 접근과 표현 학습을 “옛 방식과 새 방식”의 단순 대체 관계로 쓰지 않습니다. 실제 시스템에서는 둘이 함께 쓰일 수 있음을 남깁니다.

## 본문에 넣지 않은 내용

- CNN, RNN, Transformer 같은 구체 모델 구조는 Part 4와 Part 5에서 다룹니다.
- 임베딩(embedding), 벡터 검색(vector search), RAG는 Part 5에서 다룹니다.
- 설명 가능 AI(XAI), feature attribution, SHAP, LIME 같은 기법은 후속 평가와 해석 가능성 절에서 다룹니다.
- 표현 학습의 수학적 목적 함수, manifold, density estimation은 현재 Section의 범위를 벗어나므로 다루지 않습니다.

## 검증 필요

- `표현`, `특징`, `임베딩`, `파라미터`, `활성값`의 한국어 용어 구분은 이후 용어표에서 다시 확인합니다.
- 설명 가능성 관련 절을 작성할 때는 XAI 공식/논문 근거를 별도로 수집해야 합니다.

## 출처

- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/), 2018-07-12, 확인 날짜: 2026-06-22.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538), arXiv, 2012-06-24, 확인 날짜: 2026-06-22.
- George A. Miller, [The Magical Number Seven, Plus or Minus Two: Some Limits on our Capacity for Processing Information](http://psychclassics.yorku.ca/Miller/), Psychological Review, 1956, 확인 날짜: 2026-06-22.
