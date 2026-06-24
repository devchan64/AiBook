# P2-5.1 근거 분석: 확률은 불확실성을 어떻게 숫자로 표현하는가

## Section 목적

P2-5.1은 확률 계산의 엄밀한 절이 아니라, AI 학습자가 확률을 “불확실성을 숫자로 표현하는 언어”로 다시 읽도록 돕는 입문 절이다.

중심 질문:

```text
확률은 왜 AI 문서에서 반복해서 등장하며, 초심자는 무엇을 먼저 구분해야 하는가?
```

## 확인한 근거

### OpenStax, Introductory Statistics, 3.1 Terminology

- URL: https://openstax.org/books/introductory-statistics/pages/3-1-terminology
- 로컬 파일: `.tmp/section-p2-5-1-evidence/openstax-intro-stats-3-1-terminology.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 확률(probability), 실험(experiment), 결과(outcome), 표본공간(sample space), 사건(event)의 입문 용어를 확인했다.
- 확률이 0과 1 사이의 숫자로 표현된다는 설명, 공정한 동전과 주사위 예시, 장기 상대빈도(long-term relative frequency) 관점을 확인했다.
- 동일 가능성(equally likely outcomes)을 전제로 단순 확률을 계산하는 방식과, 현실에서는 결과가 동일 가능하지 않을 수 있다는 주의점을 확인했다.

반영 판단:

- 본문에는 용어 정의와 주사위 예시만 입문 수준으로 재서술했다.
- 원문 예시와 문장을 길게 옮기지 않았다.
- OpenStax 페이지에는 LLM 학습 사용 제한 문구가 있으므로, 본문에는 직접 인용을 넣지 않고 출처 확인과 개념 검토 용도로만 사용했다.

### Goodfellow, Bengio, Courville, Deep Learning, Chapter 3

- URL: https://www.deeplearningbook.org/contents/prob.html
- 로컬 파일: `.tmp/section-p2-5-1-evidence/deep-learning-book-ch3-probability.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 확률론이 불확실한 명제를 표현하고 정량화하는 수학적 틀이라는 설명을 확인했다.
- 머신러닝이 불확실한 양과 확률적(stochastic) 양을 다룬다는 설명을 확인했다.
- 불확실성의 원천으로 시스템 자체의 확률성, 불완전한 관측, 불완전한 모델링을 제시하는 흐름을 확인했다.
- 확률을 장기 빈도와 믿음의 정도로 해석하는 관점이 모두 AI 문맥에서 중요하다는 점을 확인했다.

반영 판단:

- 본문에서는 “불확실성은 숫자가 아니라 모르는 상태이고, 확률은 그것을 숫자로 표현하는 언어”라는 안전한 재서술로 반영했다.
- 빈도주의와 베이지안 관점을 본격 설명하지 않고, `장기 빈도(long-run frequency)`와 `믿음의 정도(degree of belief)`를 구분하는 수준으로만 소개했다.
- 베이즈 규칙은 계산으로 들어가지 않고, `prior belief`, `evidence`, `posterior belief`의 믿음 갱신 흐름만 보충했다.
- 확률분포 종류와 정보이론은 Section 경계를 넘기 때문에 제외했다.

## 표현 정리

본문에 사용한 안전한 표현:

```text
확률은 정답이 아니라 현재 정보와 모델을 기준으로 불확실성을 표현하는 숫자 언어다.
```

피한 표현:

```text
AI는 확률만으로 사고한다.
확률이 높으면 그것이 정답이다.
확률적이라는 말은 무작위라는 말과 같다.
```

이 표현들은 AI의 계산 구조를 지나치게 단순화하거나, 확률(probability), 무작위(random), 확률적(stochastic), 비결정적(nondeterministic)을 혼동하게 만들 수 있으므로 피했다.

## 자체 제작 차트

이 절에는 설명용 SVG 차트 3개와 Mermaid 도식 1개를 자체 제작해 추가했다. 외부 도표를 복제하지 않았고, `management/authoring/chart-guidelines.md`의 기준에 따라 차트 내부의 보이는 문구는 영어를 사용하고 한국어 설명은 본문에서 보조했다.

| 형식 | 목적 |
| --- | --- |
| SVG: `docs/assets/part-02/chapter-05/probability-uncertainty-scale.svg` | 불확실성을 0과 1 사이의 확률 숫자로 표현한다는 직관을 보여 준다. |
| SVG: `docs/assets/part-02/chapter-05/sample-space-event-outcome.svg` | 주사위 예시로 표본공간, 사건, 결과의 포함 관계를 보여 준다. |
| Mermaid: `section-01.md` 본문 | 베이즈 규칙을 공식이 아니라 사전 믿음, 증거, 사후 믿음의 갱신 흐름으로 보여 준다. |
| SVG: `docs/assets/part-02/chapter-05/probability-score-decision-threshold.svg` | AI 모델의 확률 점수와 서비스 운영 결정 기준이 분리된다는 점을 보여 준다. |

## Section 경계

이 절에서 다룬 내용:

- 불확실성(uncertainty)을 모르는 상태로 설명
- 확률(probability)을 0과 1 사이의 숫자 언어로 설명
- 결과(outcome), 사건(event), 표본공간(sample space)의 입문 구분
- 공정한 주사위 예시
- 장기 빈도(long-run frequency)와 믿음의 정도(degree of belief)의 최소 구분
- 베이즈 규칙(Bayes' rule)의 이름과 믿음 갱신 직관
- AI 모델 출력 확률과 운영 결정의 구분
- probability, uncertainty, stochastic의 구분

이 절에서 다루지 않은 내용:

- 조건부확률 계산
- 베이즈 규칙의 공식 계산
- 분포의 종류와 평균, 분산
- 통계적 추정과 표본 오차
- 모델 보정(calibration)
- 생성형 AI의 샘플링 절차

이 내용은 P2-5.2, P2-5.3, 이후 머신러닝과 LLM 파트에서 다루는 것이 적절하다.
