# P5-2.1 근거 검토 메모

## 절의 역할

- 토큰 다음 단계로서 임베딩을 정의한다.
- 토큰 ID와 벡터 표현의 차이를 초심자에게 설명한다.

## 이번 절의 핵심 주장

- 임베딩은 토큰이나 문장을 계산 가능한 벡터 표현으로 바꾸는 방식이다.
- 토큰 ID는 번호이고, 임베딩은 계산용 수치 표현이다.
- 임베딩은 LLM 내부 계산과 검색 서비스 양쪽의 기반이다.

## 반영한 근거

- Bengio et al., `A Neural Probabilistic Language Model`
  - 분산 표현과 신경 언어 모델의 초기 흐름 설명 근거로 사용.
- Mikolov et al., word2vec 관련 논문
  - 비슷한 문맥과 벡터 표현의 직관을 설명하는 역사적 근거로 사용.
- Jurafsky and Martin, `Speech and Language Processing`
  - NLP 교육 관점에서 임베딩 개념을 일반화하는 근거로 사용.

## 집필 판단

- 이 절에서는 수학 공식보다 직관과 실무 연결을 우선했다.
- `toy embedding` 예제를 넣어 ID와 벡터 표현의 차이를 직접 보이도록 했다.

## 제외한 내용

- sentence embedding 구조 비교
- contrastive objective 세부 설명
- 벡터 차원 선택 기준
