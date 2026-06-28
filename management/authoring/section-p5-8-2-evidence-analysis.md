# P5-8.2 근거 검토 메모

## 절의 역할

- 생성 과정을 확률 분포와 선택 규칙의 반복으로 설명한다.
- greedy, sampling, temperature를 초심자 수준에서 구분한다.

## 이번 절의 핵심 주장

- 생성은 확률 후보에서 다음 토큰을 반복 선택하는 과정이다.
- greedy와 sampling은 선택 규칙이 다르다.
- temperature는 일반적으로 생성 시 선택 성향을 바꾸는 설정값이다.

## 반영한 근거

- Brown et al., `Language Models are Few-Shot Learners`
- OpenAI API Docs의 생성 설정 설명
- Anthropic Docs의 sampling/temperature 설명

## 집필 판단

- temperature를 모델 학습 파라미터와 혼동하지 않도록 설명했다.
- API 제품 설정을 일반 개념으로 과도하게 확대하지 않도록 `일반적으로`라는 단서를 유지했다.

## 제외한 내용

- beam search
- top-k/top-p 수식 세부
