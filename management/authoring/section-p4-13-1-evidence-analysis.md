# P4-13.1 Attention의 직관 근거 메모

## Section 역할

- Part 4 Module 4 Chapter 13의 첫 번째 절입니다.
- 장기 의존성 문제 다음에, 중요한 위치를 더 직접적으로 참고하는 attention 발상을 도입합니다.
- self-attention과 Transformer 절의 입구 역할을 합니다.

## 핵심 주장

1. attention은 현재 계산에 중요한 위치를 더 크게 참고하는 방식으로 설명할 수 있다.
2. 이는 긴 문맥을 하나의 압축 상태에만 담으려는 방식보다 더 직접적인 참조를 제공한다.
3. 번역, 요약, 질의응답 맥락에서 attention 직관을 설명하기 좋다.
4. attention은 self-attention과 Transformer로 이어지는 핵심 전환 개념이다.

## 근거 출처

### 1) Bahdanau et al. 2015

- 문서: `Neural Machine Translation by Jointly Learning to Align and Translate`
- 저자: Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio
- 매체: ICLR 2015
- 확인 날짜: 2026-06-29

### 2) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

### 3) Cho et al. 2014

- 문서: `Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation`
- 저자: Kyunghyun Cho et al.
- 매체: arXiv, 2014
- 확인 날짜: 2026-06-29

## 제외한 내용

- multi-head details
- scaled dot-product formulas
- implementation code with real models
