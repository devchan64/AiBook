# P5-6.1 근거 검토 메모

## 절의 역할

- GPT 계열을 decoder 중심 Transformer 흐름으로 위치시킨다.
- BERT 계열과 GPT 계열의 차이를 구조와 생성 과업 기준으로 설명한다.

## 이번 절의 핵심 주장

- GPT 계열은 이전 토큰을 바탕으로 다음 토큰을 예측하는 생성 흐름이다.
- GPT 계열은 decoder 중심 Transformer로 읽는 편이 안전하다.
- 이 구조가 자동완성, 요약, 코드 생성 같은 사용자 경험으로 이어진다.

## 반영한 근거

- Radford et al., `Improving Language Understanding by Generative Pre-Training`
- Radford et al., `Language Models are Unsupervised Multitask Learners`
- Brown et al., `Language Models are Few-Shot Learners`
- Jurafsky and Martin, `Speech and Language Processing`

## 집필 판단

- 버전 연표보다 구조와 사용자 경험 연결을 우선했다.
- 다음 토큰 예측의 반복이라는 감각을 간단한 Python 예제로 보여 주었다.

## 제외한 내용

- GPT 버전별 세부 차이
- RLHF
- 최신 상용 모델 비교
