# P4-15.1 생성 모델은 무엇을 배우는가 근거 메모

## Section 역할

- Part 4 Module 5 Chapter 15의 첫 번째 절입니다.
- 분류 중심 설명에서 생성 중심 설명으로 이동하는 Part 4 마무리 절입니다.
- Part 5 생성형 AI, LLM의 개념적 입구 역할을 합니다.

## 핵심 주장

1. 생성 모델은 데이터 패턴과 그럴듯한 다음 출력 또는 새 샘플을 학습하려는 모델로 설명할 수 있다.
2. 분류 모델은 범주 선택을, 생성 모델은 출력 자체 생성을 중심에 둔다.
3. 생성 문제는 여러 그럴듯한 답을 허용하므로 확률적 출력과 자주 연결된다.
4. 이 관점은 텍스트 생성과 이미지 생성을 같은 큰 틀에서 묶어 준다.

## 근거 출처

### 1) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - generative models overview and distribution perspective

### 2) VAE paper

- 문서: `Auto-Encoding Variational Bayes`
- 저자: Diederik P. Kingma, Max Welling
- 매체: ICLR 2014
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - representative generative modeling line

### 3) GAN paper

- 문서: `Generative Adversarial Nets`
- 저자: Ian J. Goodfellow et al.
- 매체: NeurIPS 2014
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - representative generative modeling line

## 집필 판단

- diffusion까지 한 절에 다 넣지 않고, 생성 모델의 공통 관점만 정리했습니다.
- `distribution을 배운다`는 표현을 초심자용 통계적 감각으로 풀어 설명했습니다.
- 다음 절 sampling 설명을 위해 확률적 출력 맥락을 미리 깔아 두었습니다.

## 제외한 내용

- diffusion details
- exact likelihood derivations
- mode collapse / latent variable deep details
