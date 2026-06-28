# P5-6.2 근거 검토 메모

## 절의 역할

- GPT 계열 생성 구조가 어떻게 대화형 LLM 사용자 경험으로 바뀌었는지 설명한다.
- instruction tuning, safety, interface, tool layer를 나중 절과 연결할 준비를 한다.

## 이번 절의 핵심 주장

- 대화형 LLM은 단순 자동완성 모델 위에 지시 따르기, 안전 조정, 인터페이스 층이 더해진 경험이다.
- 사용자가 만나는 챗봇 경험은 모델 구조 하나만으로 설명되지 않는다.

## 반영한 근거

- Radford et al., `Language Models are Unsupervised Multitask Learners`
- Brown et al., `Language Models are Few-Shot Learners`
- OpenAI API Docs의 chat/prompt 사용 구조

## 집필 판단

- RLHF 세부 설명은 뒤 장으로 넘기고, 여기서는 사용자 경험 전환을 중심에 두었다.
- agent, tool use, MCP와 혼동되지 않도록 시스템 층을 따로 설명했다.

## 제외한 내용

- RLHF 알고리즘 세부
- product UX 비교
