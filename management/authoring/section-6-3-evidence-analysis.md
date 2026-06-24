# 6.3 근거 검토 메모

이 문서는 `docs/parts/part-01/chapter-06/section-03.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- 6.2에서 정리한 불확실성(uncertainty), 확률(probability), 확률적 과정(stochastic)을 실제 AI 작업 유형에 연결합니다.
- 사용자의 “확률이 반복되면 인간의 사고와 비슷해진다”는 직관을 그대로 주장하지 않고, 분류, 예측, 생성, 의사결정에서 확률이 쓰이는 위치로 보수화합니다.
- `확률 출력 = 정답` 또는 `temperature = 학습된 모델 파라미터` 같은 오해를 줄입니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-2-1-labeling-evidence/google-ml-glossary.html` | classification threshold, probabilistic regression model, softmax, temperature 용어 확인 |
| scikit-learn, `Probability calibration` | `.tmp/section-6-2-evidence/scikit-learn-probability-calibration.html` | 분류에서 class probability를 얻고 싶을 때가 많지만, 모델에 따라 확률 추정이 나쁠 수 있고 calibration이 필요하다는 설명 |
| Poole & Mackworth, `Artificial Intelligence: Foundations of Computational Agents` | `.tmp/section-2-2-evidence/poole-mackworth-ch9-s1-probability.html` 등 | 확률을 불확실한 상황에서 믿음을 표현하고 갱신하는 관점으로 이해하는 배경 |

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 분류(classification)에서는 후보 라벨의 확률 추정값(probability estimate)을 사용할 수 있다 | scikit-learn은 classification에서 class label뿐 아니라 해당 label의 probability가 필요할 수 있다고 설명함. Google glossary는 softmax가 multi-class classification에서 클래스별 확률을 계산한다고 설명함 | 유지 |
| 확률 출력은 정답이 아니라 현재 모델 기준의 그럴듯함으로 읽어야 한다 | scikit-learn은 일부 모델이 class probability를 poor estimate로 줄 수 있다고 설명하고 calibration 필요성을 제시함 | 유지 |
| 임계값(threshold)은 자동 처리와 사람 검토를 나누는 기준으로 설명할 수 있다 | Google glossary의 classification threshold, post-processing 예시와 연결됨 | 유지. 공정성 세부 논의는 제외 |
| 보정(calibration)은 `0.80` 출력이 실제 빈도와 얼마나 맞는지 묻는 문제다 | scikit-learn은 well-calibrated classifier의 `predict_proba`를 confidence level로 해석할 수 있으며, 0.8 부근 샘플 중 약 80%가 positive class여야 한다고 설명함 | 유지 |
| 예측(regression, forecasting)에서는 값 하나뿐 아니라 불확실성(uncertainty)을 함께 볼 수 있다 | Google glossary의 probabilistic regression model은 prediction과 uncertainty를 함께 생성한다고 설명함 | 유지 |
| 생성(generation)에서는 여러 후보 중 선택하는 문제가 있고 temperature가 출력 변동성과 연결된다 | Google glossary는 temperature를 model output의 randomness 정도를 제어하는 hyperparameter로 설명함 | 유지. decoding 상세는 Part 5로 이월 |
| 확률은 최종 결정이 아니라 판단 재료다 | classification threshold, calibration, uncertainty 설명을 서비스 판단으로 일반화한 문구 | 유지. 정책과 책임 판단은 뒤의 AI 서비스/윤리 장에서 확장 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 6.1 | 규칙만으로 닫히지 않는 문제 조건 도입 |
| 6.2 | uncertainty, probability, stochastic 용어 구분 |
| 6.3 | 확률적 관점이 쓰이는 작업 위치 소개 |
| Part 2 | 확률, 조건부 확률, 베이즈 규칙, 확률 분포의 수학 기초 |
| Part 3 | 분류 모델, 회귀 모델, 평가 지표, calibration의 실제 방법 |
| Part 5 | LLM 생성, sampling, temperature, top-p 상세 |
| Part 6 또는 윤리 장 | 자동화된 의사결정의 정책, 위험, 책임 |

## 보수화한 표현

- “현대 AI는 확률이 반복되면 인간의 사고와 비슷해진다”는 표현은 본문 주장으로 사용하지 않았습니다.
- “AI가 확률적으로 동작한다”는 표현은 분류, 예측, 생성, 의사결정의 구체적 위치로 나누어 설명했습니다.
- `softmax` 수식과 `temperature scaling`은 다루지 않았습니다. 이 절은 호기심과 위치 감각을 만드는 절입니다.
- `temperature`는 모델 실행 설정으로 설명하고, 학습된 모델 파라미터(parameter)와 구분했습니다.
- `0.70` 같은 점수는 작업, 데이터, 모델, 보정, 임계값 안에서 읽어야 한다고 제한했습니다.

## 확인한 원문 위치

- `.tmp/section-6-2-evidence/scikit-learn-probability-calibration.html`
  - classification에서 class probability와 confidence 설명: 737-755행 부근
  - well calibrated classifier의 해석: 748-754행 부근
  - calibration curve와 predicted probability 비교: 770-788행 부근
- `.tmp/section-2-1-labeling-evidence/google-ml-glossary.html`
  - classification threshold, post-processing 예시: 12515-12560행 부근
  - probabilistic regression model: 12852-12862행 부근
  - softmax와 multi-class classification probability: 15190-15270행 부근
  - temperature: 15895-15910행 부근

## 남은 검토 사항

- Part 3에서 calibration, reliability diagram, Brier score, log loss를 본격적으로 다룰지 결정합니다.
- Part 5에서 `temperature`, `top-p`, `sampling`, `deterministic decoding`을 6.2와 6.3의 용어 기준에 맞춰 다시 정리합니다.
- 자동화된 의사결정의 책임과 위험은 AI 윤리, 보안, 서비스 아키텍처 장에서 별도 근거를 확보합니다.
