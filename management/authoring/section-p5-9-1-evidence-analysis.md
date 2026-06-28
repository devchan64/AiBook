# P5-9.1 근거 검토 메모

## 절의 역할

- 파인튜닝을 사전학습 이후의 목적 적응 단계로 설명한다.
- 프롬프트, RAG, 파인튜닝의 선택지를 초심자 수준에서 구분한다.

## 이번 절의 핵심 주장

- 파인튜닝은 사전학습된 모델을 특정 과업/도메인에 맞게 추가 조정하는 과정이다.
- 프롬프트는 입력을 바꾸고, 파인튜닝은 모델 내부 가중치 조정을 포함한다.
- 최신성/외부 근거 문제는 RAG가 더 적합한 경우가 많다.

## 반영한 근거

- Howard and Ruder, `Universal Language Model Fine-tuning for Text Classification`
- Houlsby et al., `Parameter-Efficient Transfer Learning for NLP`
- Brown et al., `Language Models are Few-Shot Learners`

## 집필 판단

- 파인튜닝을 만능 해결책처럼 쓰지 않았다.
- 실무 의사결정 질문으로 RAG와 구분했다.

## 제외한 내용

- optimizer 세부
- full fine-tuning 구현 절차
