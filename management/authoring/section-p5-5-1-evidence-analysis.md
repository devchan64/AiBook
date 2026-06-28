# P5-5.1 근거 검토 메모

## 절의 역할

- BERT 계열을 encoder 중심 Transformer 흐름으로 위치시킨다.
- GPT 계열과의 차이를 `생성/이해`라는 단순 구호가 아니라 구조와 용도 차이로 설명한다.

## 이번 절의 핵심 주장

- BERT 계열은 입력 전체 문맥을 반영한 표현을 만드는 encoder 중심 구조다.
- 생성보다 분류, 검색, 임베딩 계열 과업과 더 잘 맞는다.
- GPT 계열과의 차이는 우열보다 구조와 과업 차이로 읽어야 한다.

## 반영한 근거

- Devlin et al., `BERT`
- Peters et al., `Deep contextualized word representations`
- Jurafsky and Martin, `Speech and Language Processing`

## 집필 판단

- `이해 모델` 같은 표현은 유지하되, 사람식 이해로 오해되지 않게 보정 문구를 함께 넣었다.
- 실무 연결을 위해 검색, 임베딩, 분류 예시를 함께 배치했다.

## 제외한 내용

- RoBERTa, ALBERT, DistilBERT 등의 상세 비교
- MLM 수식
