# P5-1.2 근거 검토 메모

## 절의 역할

- 토큰화(tokenization)가 실제 비용, 문맥 길이, 검색, 생성에 영향을 준다는 점을 설명한다.
- 임베딩과 RAG 설명으로 이어지는 실무 감각을 만든다.

## 이번 절의 핵심 주장

- 토큰화는 원문을 모델 계산 단위로 바꾸는 절차다.
- 같은 의미의 텍스트도 표기 방식에 따라 토큰 수가 달라질 수 있다.
- 토큰화는 비용, context window, 검색 청크, 생성 해석에 영향을 준다.

## 반영한 근거

- Jurafsky and Martin, `Speech and Language Processing`
  - 텍스트 단위화의 일반 배경 설명 근거로 사용.
- Sennrich et al., `Neural Machine Translation of Rare Words with Subword Units`
  - subword 단위가 널리 쓰이게 된 역사적 전환의 근거로 사용.
- OpenAI API Docs
  - 실제 서비스에서 토큰 수가 길이와 비용에 연결된다는 실무 근거로 사용.

## 집필 판단

- 알고리즘 세부보다 사용자 경험과 서비스 설계 영향에 초점을 맞췄다.
- 한국어 사용자가 토큰 경계를 더 낯설게 느낄 수 있다는 점을 일반화 문구로 설명했다.

## 제외한 내용

- tokenizer vocabulary 학습 절차
- 멀티모달 토큰 설계
- 특정 모델별 tokenizer 비교표

이는 이후 필요할 때 별도 절에서 다룬다.
