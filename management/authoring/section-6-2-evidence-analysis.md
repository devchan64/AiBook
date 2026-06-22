# 6.2 근거 검토 메모

이 문서는 `docs/chapters/chapter-06/section-02.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- `uncertainty`, `probability`, `stochastic`을 같은 말처럼 쓰지 않도록 기준을 세웁니다.
- 사용자의 `불확정성`, `확률적 동작`, `확률이 반복되면 사고와 비슷해진다`는 직관을 표준 용어로 분해합니다.
- 6.3, Chapter 7, Part 5에서 확률 출력, 휴리스틱, LLM 생성 설정을 설명할 때 사용할 용어 기준을 만듭니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Poole & Mackworth, Chapter 9 `Reasoning with Uncertainty` | `.tmp/section-2-2-evidence/poole-mackworth-ch9-uncertainty.html`, `.tmp/section-2-2-evidence/poole-mackworth-ch9-s1-probability.html` | uncertainty, probability as calculus of belief, prior/posterior probability, evidence, random variable 설명 |
| Poole & Mackworth, Chapter 3 `State Spaces` | `.tmp/section-2-2-evidence/poole-mackworth-ch3-s2-state-spaces.html` | 상태가 완전히 관측되지 않거나 행동이 stochastic할 수 있다는 예시 |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | `.tmp/section-01-evidence/sep-ai.html` | 무지, 비결정성, 모호함 때문에 확률적 접근이 필요할 수 있고, probabilistic inference가 evidence에서 posterior probability를 계산한다는 설명 |
| Hüllermeier & Waegeman, `Aleatoric and Epistemic Uncertainty in Machine Learning` | `.tmp/section-6-2-evidence/hullermeier-waegeman-uncertainty-ml.pdf`, `.tmp/section-6-2-evidence/hullermeier-waegeman-uncertainty-ml-abstract.html` | ML에서 uncertainty가 중요한 방법론 요소이며, aleatoric/epistemic uncertainty 구분이 중요하다는 배경 |
| scikit-learn, `Probability calibration` | `.tmp/section-6-2-evidence/scikit-learn-probability-calibration.html` | 분류 모델의 확률 출력은 confidence처럼 읽힐 수 있지만, 잘 보정된 확률인지 확인해야 한다는 실무적 근거 |

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 불확실성은 확실히 알 수 없는 상태다 | Poole & Mackworth는 실제 에이전트가 전지적이지 않고, SEP는 모든 명제의 참·거짓을 알 수 없다고 설명함 | 유지 |
| 확률은 불확실성을 표현하고 갱신하는 숫자 언어다 | Poole & Mackworth는 probability를 belief의 calculus로 설명하고 prior/posterior 갱신을 다룸 | 유지. 수식은 생략 |
| 중간 확률값은 사실이 부분적으로 참이라는 뜻이 아니라 에이전트가 모른다는 상태를 반영한다 | Poole & Mackworth가 0과 1 사이의 확률을 agent의 ignorance로 설명함 | 유지 |
| evidence는 관측 정보이며 판단을 갱신한다 | Poole & Mackworth의 evidence, prior, posterior 설명 | 유지 |
| stochastic은 과정이나 행동에 확률적 변동이 포함된 성질이다 | Poole & Mackworth가 행동이 stochastic할 수 있음을 로봇 overshoot, 학생 학습 실패 예시로 설명함 | 유지 |
| random, stochastic, nondeterministic, probabilistic은 구분해야 한다 | SEP가 ignorance, non-determinism, vagueness를 구분해 언급하고, 본문은 학습용 용어 기준으로 정리함 | 유지. 엄밀한 형식 정의는 보류 |
| AI 일반 문맥에서는 `불확정성`보다 `불확실성(uncertainty)`을 우선 사용한다 | 물리학적 불확정성 원리와의 혼동 가능성을 피하기 위한 이 책의 용어 정책 | 유지. 외부 사전 정의로 단정하지 않음 |
| 불확실성에는 줄일 수 있는 모름과 반복해도 남는 변동이 있을 수 있다 | Hüllermeier & Waegeman이 aleatoric/epistemic uncertainty 구분의 중요성을 설명함 | 유지하되 6.2에서는 호기심 유도 수준으로 제한. 상세 설명은 6.3 또는 Part 3 이후로 보류 |
| 모델 확률 출력은 실제 빈도와 맞는지 calibration 관점으로 검토해야 한다 | scikit-learn probability calibration 문서는 predict_proba와 confidence level, calibration curve를 설명함 | 유지하되 수식과 calibration 방법론은 뒤 장으로 넘김 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 6.1 | 규칙만으로 처리하기 어려운 문제 조건 도입 |
| 6.2 | uncertainty, probability, stochastic 용어 구분 |
| 6.3 | AI에서 확률적 판단이 쓰이는 위치 |
| Chapter 7 | 휴리스틱과 탐색 공간 |
| Part 2 | 확률과 통계의 수학 기초 |
| Part 5 | LLM 생성 설정, sampling, temperature, top-p |

## 보수화한 표현

- `probability`를 빈도주의/베이지안 전체 논쟁으로 확장하지 않았습니다. Poole & Mackworth의 belief 갱신 관점을 입문용으로만 사용했습니다.
- `stochastic`을 “아무렇게나” 또는 “무질서”로 설명하지 않았습니다.
- `nondeterministic`을 확률 분포가 명시된 stochastic 과정과 같은 말로 단정하지 않았습니다.
- LLM이 같은 프롬프트에 다른 답을 낼 수 있다는 설명은 생성 설정과 샘플링 방식에 따라 달라질 수 있다는 수준으로 제한했습니다.
- `불확정성`은 특정 학문 분야 용어와 혼동될 수 있으므로 일반 AI 설명에서는 우선 사용하지 않는 정책으로 정리했습니다.
- aleatoric/epistemic uncertainty는 본문에서 용어 소개와 질문 수준으로만 배치했습니다. 6.2의 핵심 범위는 `uncertainty`, `probability`, `stochastic` 구분입니다.
- calibration은 “모델의 확률 숫자를 그대로 믿지 말자”는 호기심을 만들기 위해 사용했습니다. 분류 평가, calibration curve, temperature scaling은 뒤 장에서 다룹니다.

## 확인한 원문 위치

- `.tmp/section-2-2-evidence/poole-mackworth-ch9-s1-probability.html`
  - probability as calculus of belief: 123-153행 부근
  - 0과 1 사이 확률과 ignorance: 163-171행 부근
  - random variable: 179-205행 부근
  - evidence, prior, posterior: 376-418행 부근
- `.tmp/section-2-2-evidence/poole-mackworth-ch3-s2-state-spaces.html`
  - stochastic actions 예시: 316-332행 부근
- `.tmp/section-01-evidence/sep-ai.html`
  - ignorance, non-determinism, vagueness, random variables: 2120-2133행 부근
  - probabilistic inference: 2247-2256행 부근
- `.tmp/section-6-2-evidence/hullermeier-waegeman-uncertainty-ml-abstract.html`
  - uncertainty가 ML 방법론의 핵심 요소라는 설명: 29행, 40행, 177-178행 부근
  - aleatoric/epistemic uncertainty 구분의 중요성: 29행, 40행, 177-178행 부근
- `.tmp/section-6-2-evidence/scikit-learn-probability-calibration.html`
  - classification에서 class probability와 confidence 설명: 737-755행 부근
  - well calibrated classifier의 해석: 748-754행 부근
  - calibration curve와 predicted probability 비교: 770-788행 부근

## 남은 검토 사항

- 6.3에서 분류 확률, calibration, confidence, uncertainty estimation의 차이를 별도 근거로 다룹니다.
- Part 2에서 확률의 빈도주의, 베이지안 해석은 필요한 범위 안에서 더 엄밀히 분리합니다.
- Part 5에서 LLM sampling, temperature, top-p를 설명할 때 6.2의 stochastic 기준과 연결합니다.
