# P3-8.2 기준 모델(baseline) - 근거 검토 메모

## 검토 목적

- baseline을 초심자 기준에서 `비교의 출발점`으로 설명한다.
- 복잡한 모델을 먼저 고르는 흐름보다, 단순 기준을 먼저 세우는 흐름이 왜 안전한지 정리한다.
- 분류와 회귀의 대표 baseline을 dummy 계열 도구와 연결한다.

## 핵심 근거

1. scikit-learn, `DummyClassifier`
   - URL: https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html
   - 확인 날짜: 2026-06-26
   - 반영 포인트:
     - 입력 특징을 무시하는 단순 분류기다.
     - 더 복잡한 분류기와 비교하기 위한 simple baseline으로 설명된다.

2. scikit-learn, `DummyRegressor`
   - URL: https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html
   - 확인 날짜: 2026-06-26
   - 반영 포인트:
     - 평균, 중앙값, 상수 같은 단순 규칙으로 예측한다.
     - 다른 회귀기와 비교하기 위한 simple baseline으로 설명된다.

3. Sebastian Raschka, `Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning`
   - URL: https://arxiv.org/abs/1811.12808
   - 확인 날짜: 2026-06-26
   - 반영 포인트:
     - 평가와 모델 선택, 알고리즘 비교는 분리된 문제다.
     - 비교 절차를 세우지 않으면 점수 해석이 흔들릴 수 있다.

## 본문 일반화 원칙

- baseline을 `낮은 성능 모델`보다 `성능을 읽기 위한 기준선`으로 설명한다.
- 분류의 다수 클래스 예측, 회귀의 평균/중앙값 예측을 대표 예시로 든다.
- dummy 계열은 서비스용 모델이 아니라 비교용 교육 도구로 소개한다.
- baseline은 모델 선택 뒤, 튜닝 전의 절이라는 커리큘럼 위치를 드러낸다.

## 도메인 경계

- 이 절은 baseline의 역할과 입문적 예시를 다룬다.
- 통계 검정, 벤치마크 설계, 리더보드 비교는 다루지 않는다.
- 하이퍼파라미터 조정은 P3-9로 넘긴다.
- 개별 알고리즘이 baseline을 넘는 방식은 P3-10 이후 절에서 구체화한다.
