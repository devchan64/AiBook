# P5-7.1 근거 검토 메모

## 절의 역할

- 사전학습을 LLM 공통 기반으로 설명한다.
- 파인튜닝, instruction tuning과의 차이를 초심자 수준에서 분리한다.

## 이번 절의 핵심 주장

- 사전학습은 대규모 텍스트에서 일반 언어 패턴과 표현을 먼저 배우는 단계다.
- 사전학습은 사실 저장과 같은 말이 아니다.
- 이후 파인튜닝과 지시 튜닝은 그 위에 얹히는 조정 단계다.

## 반영한 근거

- Radford et al., `Improving Language Understanding by Generative Pre-Training`
- Howard and Ruder, `Universal Language Model Fine-tuning for Text Classification`
- Brown et al., `Language Models are Few-Shot Learners`
- Jurafsky and Martin, `Speech and Language Processing`

## 집필 판단

- pretraining/fine-tuning/instruction tuning을 한 표로 분리했다.
- RLHF 세부는 아직 다루지 않았다.

## 제외한 내용

- 목적 함수 수식
- 분산학습 인프라
