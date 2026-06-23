# Section 15.1 근거 검토: 편향, 안전성, 책임

## 검토 목적

- 15.1은 Chapter 15 `AI 윤리, 저작권, 보안`의 첫 절입니다.
- 이 절은 저작권과 학습 데이터(15.2), 보안과 개인정보(15.3)를 침범하지 않고, AI 결과가 사회적으로 영향을 줄 때 생기는 편향(bias), 안전성(safety), 책임(accountability)을 개론 수준에서 다룹니다.
- 사용자의 요청에 따라 뉴스, 칼럼, 탐사보도는 주요 현실 사례 근거로 사용하고, NIST/OECD/UNESCO 자료는 개념 기준과 용어 정리의 근거로 사용했습니다.

## 확인 자료

| 자료 | 성격 | 확인한 내용 | 본문 반영 |
| --- | --- | --- | --- |
| NIST AI RMF 1.0 | 공식 프레임워크 | AI 위험은 개인, 집단, 조직, 사회, 환경에 영향을 줄 수 있고 AI는 사회기술적(socio-technical) 성격을 가진다고 설명 | AI 윤리를 기술 바깥의 장식이 아니라 기술 사용 조건의 일부로 설명 |
| NIST AI RMF 웹페이지 | 공식 안내 | AI RMF는 AI 제품, 서비스, 시스템의 설계, 개발, 사용, 평가에서 신뢰성 고려를 통합하려는 자발적 프레임워크 | 신뢰할 수 있는 AI의 속성 정리에 사용 |
| OECD AI Principles | 국제 원칙 | 인권과 민주적 가치, 투명성과 설명가능성, 견고성·보안·안전, 책임성을 제시 | 책임, 투명성, 안전성 설명의 기준으로 사용 |
| UNESCO Recommendation on the Ethics of AI | 국제 윤리 권고 | 인권, 기본적 자유, 인간 존엄, 공정성, 비차별, 안전, 책임을 포함하는 윤리 기준 | AI 윤리를 사회적 영향과 권리 문제로 연결하는 배경으로 사용 |
| ProPublica, Machine Bias | 탐사보도 | COMPAS 재범 위험 점수 사례에서 집단별 오류와 공정성 논쟁이 발생했음을 보도. 개발사 반론도 함께 존재 | 편향 사례로 사용하되, 단일 기사로 결론을 단정하지 않음 |
| Associated Press, Detroit facial recognition arrest | 뉴스 | 얼굴인식 기술이 관련된 오인 체포 사례와 이후 사용 기준 논쟁을 보도 | 안전성, 인간 검토, 고위험 사용 맥락 사례로 사용 |

원문 HTML/PDF는 `.tmp/section-15-1-evidence/` 아래에 내려받아 확인했습니다. `.tmp/`는 임시 근거 확인 공간이므로 커밋하지 않습니다.

## 본문 반영 기준

- 뉴스와 탐사보도는 실제 문제가 사회적으로 어떻게 드러나는지 보여 주는 사례로 사용했습니다.
- 공식 문서와 국제 원칙은 용어와 개념의 기준으로 사용했습니다.
- ProPublica의 COMPAS 보도는 개발사 반론이 있었음을 함께 적어, “기사 하나로 모든 결론이 끝났다”는 식의 단정을 피했습니다.
- AP 얼굴인식 사례는 얼굴인식 기술 전체의 금지/허용 결론이 아니라, 고위험 분야에서 AI 결과를 증거처럼 사용할 때 필요한 검증과 인간 감독 문제로 제한했습니다.

## Section 경계 검토

- 15.1은 편향(bias), 안전성(safety), 책임(accountability), 투명성(transparency), 인간 감독(human oversight)을 다룹니다.
- 저작권(copyright), 학습 데이터(training data), 한국 출판물 인용 기준은 15.2로 넘겼습니다.
- 보안(security), 개인정보(privacy), 로그에 남는 민감 정보 문제는 15.3으로 넘겼습니다.
- 법률적 책임 판단을 단정하지 않고, 입문 수준의 실무적 책임 질문으로 제한했습니다.

## 용어 검토

- `AI 윤리(AI ethics)`, `편향(bias)`, `안전성(safety)`, `책임(accountability)`, `투명성(transparency)`, `설명가능성(explainability)`, `해석가능성(interpretability)`, `인간 감독(human oversight)`, `고위험(high-risk)`, `사회기술적(socio-technical)`, `대리 지표(proxy)`, `위험 점수(risk score)`를 한영 병기했습니다.
- `책임(accountability)`은 법률적 책임 확정이 아니라 설명, 검토, 수정, 중단 가능성을 포함하는 실무적 책임으로 제한했습니다.

## 주의한 오해

- 편향은 개발자의 악의에서만 생긴다고 쓰지 않았습니다.
- 전체 정확도가 높으면 공정하다고 쓰지 않았습니다.
- AI 안전성을 단순히 모델 출력 필터링으로만 설명하지 않았습니다.
- “AI가 했다”는 말로 책임이 사라진다고 쓰지 않았습니다.
- 투명성을 모델 내부 전면 공개와 동일시하지 않았습니다.
- 인간 감독을 형식적 승인 절차로 충분하다고 쓰지 않았습니다.
- 뉴스 사례를 모든 AI 시스템에 그대로 일반화하지 않았습니다.

## 참고 자료

- NIST, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework), National Institute of Standards and Technology, 확인 날짜: 2026-06-23.
- NIST, [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf), NIST AI 100-1, 2023, 확인 날짜: 2026-06-23.
- OECD.AI, [OECD AI Principles overview](https://oecd.ai/en/ai-principles), OECD AI Policy Observatory, 확인 날짜: 2026-06-23.
- UNESCO, [Recommendation on the Ethics of Artificial Intelligence](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics), UNESCO, 확인 날짜: 2026-06-23.
- Julia Angwin, Jeff Larson, Surya Mattu, Lauren Kirchner, [Machine Bias](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing), ProPublica, 2016-05-23, 확인 날짜: 2026-06-23.
- Ed White, [Judge dismisses lawsuit against Detroit police in wrongful arrest case](https://apnews.com/article/detroit-facial-recognition-arrest-821d260e932a4582a6a912dd61fde157), Associated Press, 2025-09-17, 확인 날짜: 2026-06-23.
