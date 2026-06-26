# P3-7.1 특징 선택(feature selection) - 근거 검토 메모

## 검토 목적

- 특징 선택을 `어떤 입력을 모델에 줄 것인가를 고르는 일`로 초심자 수준에서 설명한다.
- 특징 선택이 성능 숫자뿐 아니라 누수(leakage), 계산 비용, 안정성과 연결된다는 점을 보수적으로 정리한다.
- 알고리즘 세부보다 실무 휴리스틱을 먼저 설명하되, 공식 자료와 어긋나지 않게 쓴다.

## 핵심 근거

1. scikit-learn, `1.13. Feature selection`
   - URL: https://scikit-learn.org/stable/modules/feature_selection.html
   - 확인 날짜: 2026-06-26
   - 반영 포인트:
     - 특징 선택 모듈은 정확도 개선 또는 고차원 데이터에서 성능 향상에 사용될 수 있다.
     - low variance 제거, univariate selection, recursive feature elimination, model-based selection 같은 대표 범주가 있다.
   - 주의:
     - 공식 문서는 방법 분류와 API를 자세히 설명하지만, 이 절은 입문 절이므로 수식과 API 상세는 생략한다.

2. scikit-learn, `12.2. Data leakage during pre-processing`
   - URL: https://scikit-learn.org/stable/common_pitfalls.html
   - 확인 날짜: 2026-06-26
   - 반영 포인트:
     - 특징 선택은 전처리의 한 종류처럼 다뤄질 수 있으며, 훈련 데이터만 사용해야 한다.
     - 테스트 데이터를 특징 선택에 포함하면 성능이 낙관적으로 부풀려진다.
     - 파이프라인(pipeline)으로 훈련/평가 경계를 지키는 것이 권장된다.
   - 주의:
     - 이 절에서는 pipeline 구현보다 `예측 시점에 쓸 수 없는 정보는 빼야 한다`는 직관을 우선 설명한다.

3. Guyon, Elisseeff, `An Introduction to Variable and Feature Selection`
   - URL: https://jmlr.org/papers/v3/guyon03a.html
   - PDF: https://jmlr.org/papers/volume3/guyon03a/guyon03a.pdf
   - 확인 날짜: 2026-06-26
   - 반영 포인트:
     - variable과 feature를 구분할 수 있다. raw input variable과 constructed feature의 차이를 본문에서 초심자 수준으로 일반화한다.
     - 특징 선택의 목적은 예측 성능 향상, 더 빠르고 비용이 적은 예측기, 데이터 생성 과정에 대한 이해 향상으로 정리할 수 있다.
     - 관련성(relevance)과 예측기 구축에서의 유용성(usefulness)은 구분될 수 있다.
   - 주의:
     - 본문에서는 논문의 세부 알고리즘 분류(filter, wrapper, embedded)를 깊게 전개하지 않는다.

## 본문 일반화 원칙

- `특징 선택은 많이 넣는 일이 아니라 정당하게 쓸 수 있는 입력을 고르는 일`이라는 문장으로 요약한다.
- 특징을 `현실 정보를 입력 변수로 표현한 단위`로 설명하고, 특징 선택을 `입력 공간을 설계하는 일`로 일반화한다.
- 신호(signal), 잡음(noise), 중복(redundancy) 관점으로 좋은 특징의 조건을 초심자 수준에서 설명한다.
- 학술 용어로는 variable, feature, relevance, usefulness의 차이를 짧게 짚되, 본문은 정의 암기보다 설명 흐름을 우선한다.
- 식별자, 사후 정보, 상수 칼럼, 운영에서 불안정한 칼럼은 초심자 점검표로 제시한다.
- low variance, univariate selection, RFE 같은 이름은 소개하되, 알고리즘 장처럼 깊게 들어가지 않는다.

## 도메인 경계

- 이 절은 특징 선택 자체를 다룬다.
- 결측치 처리, 스케일 조정, 범주형 인코딩은 P3-7.2 전처리 절로 넘긴다.
- 모델 중요도 해석, feature importance의 세부 의미는 Part 3 후반 알고리즘 절이나 트리/앙상블 절과 연결할 수 있으나, 여기서 깊게 다루지 않는다.
