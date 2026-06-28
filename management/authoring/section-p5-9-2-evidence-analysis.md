# P5-9.2 근거 검토 메모

## 절의 역할

- PEFT(parameter-efficient fine-tuning)의 필요성을 설명한다.
- LoRA를 큰 기반 모델 위 작은 조정분 학습으로 소개한다.

## 이번 절의 핵심 주장

- 전체 파인튜닝은 비용이 크다.
- LoRA는 작은 추가 조정 파라미터를 통해 효율적으로 목적 적응을 시도한다.
- LoRA는 비용을 줄여 주지만 품질 검증을 대신하지는 않는다.

## 반영한 근거

- Houlsby et al., `Parameter-Efficient Transfer Learning for NLP`
- Hu et al., `LoRA: Low-Rank Adaptation of Large Language Models`

## 집필 판단

- low-rank 수식은 제외하고 목적과 구조 직관만 남겼다.
- adapter 계열 전체 비교는 뒤로 미뤘다.

## 제외한 내용

- 저랭크 수식
- 메모리 계산 세부
