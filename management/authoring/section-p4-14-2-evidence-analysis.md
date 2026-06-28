# P4-14.2 병렬 처리와 긴 문맥 근거 메모

## Section 역할

- Part 4 Module 4 Chapter 14의 두 번째 절입니다.
- Transformer가 RNN과 왜 다른 전환점이었는지 계산 구조 관점에서 설명합니다.
- Part 5 LLM 확산의 계산적 배경을 준비합니다.

## 핵심 주장

1. Transformer는 순차 상태 전달보다 토큰 간 관계를 병렬적으로 계산하는 구조에 더 가깝다.
2. 이 구조는 GPU 병렬 처리와 잘 맞는다.
3. self-attention은 긴 문맥 참조에서 더 직접적인 장점을 제공한다.
4. 이 차이가 LLM과 대규모 사전학습 확산의 핵심 기반 중 하나였다.

## 근거 출처

### 1) Attention Is All You Need

- 문서: `Attention Is All You Need`
- 저자: Ashish Vaswani et al.
- 매체: NeurIPS 2017
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - self-attention replacing recurrence for sequence transduction

### 2) T5 paper

- 문서: `Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer`
- 저자: Colin Raffel et al.
- 매체: JMLR, 2020
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - Transformer scalability and text-to-text framing

### 3) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - sequence modeling and long dependency background

## 집필 판단

- complexity 수치 비교보다 초심자에게 필요한 구조 감각을 우선했습니다.
- 긴 문맥과 GPU 병렬 처리를 같은 절 안에서 묶어, LLM 전환 배경이 드러나도록 했습니다.
- code example은 sequential accumulation vs direct reference intuition 수준으로 제한했습니다.

## 제외한 내용

- KV cache
- sparse attention variants
- scaling law discussion
