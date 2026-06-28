# P5-5.2 근거 검토 메모

## 절의 역할

- 이해 중심 태스크를 하나의 묶음으로 설명한다.
- BERT 계열의 실무 용도를 분류, 문장쌍 판단, 검색, 임베딩으로 정리한다.

## 이번 절의 핵심 주장

- 이해 중심 태스크는 라벨, 관련도, 점수, 표현을 출력하는 작업 흐름이다.
- 분류, 검색, 문장쌍 비교, 임베딩은 하나의 encoder 활용 흐름으로 묶을 수 있다.
- 이 대비가 GPT 계열 설명으로 자연스럽게 이어진다.

## 반영한 근거

- Devlin et al., `BERT`
- Jurafsky and Martin, `Speech and Language Processing`
- Peters et al., `Deep contextualized word representations`

## 집필 판단

- 세부 벤치마크보다 업무 예시 중심으로 일반화했다.
- cross-encoder / bi-encoder 세부는 아직 넣지 않았다.

## 제외한 내용

- GLUE 세부 점수표
- dense retrieval 구현 세부
