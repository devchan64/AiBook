# P4-10.2 깊은 층의 표현 근거 메모

## Section 역할

- Part 4 Module 3 Chapter 10의 두 번째 절입니다.
- 표현 학습이 층을 거치며 어떻게 더 추상적인 표현으로 이어진다고 설명하는지 정리합니다.
- 다음 Chapter 11 CNN으로 넘어가기 위한 계층적 표현 직관을 만듭니다.

## 핵심 주장

1. 깊은 층 표현은 낮은 수준 패턴에서 높은 수준 표현으로 이동하는 경향으로 설명할 수 있다.
2. 여러 층을 쌓는 이유는 파라미터 수 증가뿐 아니라 표현 수준의 변화와도 연결된다.
3. 이미지, 음성, 텍스트 모두에서 계층적 표현 직관이 자주 유효하다.
4. 이 설명은 엄밀한 보편 법칙이 아니라 교육적 기본 지도라는 점을 함께 명시해야 한다.

## 근거 출처

### 1) Bengio et al. 2013

- 문서: `Representation Learning: A Review and New Perspectives`
- 저자: Yoshua Bengio, Aaron Courville, Pascal Vincent
- 매체: IEEE TPAMI, 2013
- 확인 날짜: 2026-06-29

### 2) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

### 3) Erhan et al. 2010

- 문서: `Why Does Unsupervised Pre-training Help Deep Learning?`
- 저자: Dumitru Erhan et al.
- 매체: JMLR, 2010
- 확인 날짜: 2026-06-29

## 제외한 내용

- feature visualization techniques
- mechanistic interpretability details
- self-supervised modern representation analysis
