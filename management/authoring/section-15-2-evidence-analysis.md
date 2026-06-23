# 15.2 근거 검토: 저작권과 학습 데이터

## 목적

15.2는 AI 윤리 논의에서 저작권(copyright)과 학습 데이터(training data) 논쟁으로 넘어가는 절이다. 법률 자문이 아니라, 책 작성자가 자료를 사용할 때 검토해야 할 기준을 정리하는 것이 목적이다.

## Section 경계

- 15.1은 편향(bias), 안전성(safety), 책임(accountability)을 다룬다.
- 15.2는 저작권, 인용, 학습 데이터, 생성 결과의 유사성 위험을 다룬다.
- 15.3은 보안(security), 개인정보(privacy), 비밀 정보 유출을 다룬다.
- 15.2에서는 개인정보나 보안 로그 문제를 깊게 다루지 않는다.

## 확인한 자료

| 자료 | 성격 | 반영 방식 |
| --- | --- | --- |
| 국가법령정보센터, 저작권법 | 한국 법령 공식 출처 | 제2조 저작물 정의, 제28조 인용, 제35조의5 공정한 이용, 제37조 출처 명시를 요지 수준으로 반영 |
| U.S. Copyright Office, Copyright and Artificial Intelligence | 미국 저작권청 공식 AI 저작권 페이지 | AI 저작권 쟁점이 보고서 형태로 검토되고 있음을 반영 |
| U.S. Copyright Office, Part 3: Generative AI Training | 미국 저작권청 보고서 사전 공개본 | 생성형 AI 학습 데이터가 별도 쟁점으로 검토됨을 반영 |
| Associated Press, NYT v. OpenAI/Microsoft 보도 | 주요 언론 보도 | 소송에서 제기된 주장과 논쟁의 구조를 사례로만 반영 |
| Lee, Cooper, Grimmelmann, Generative-AI Supply Chain | 학술 논문 | 생성형 AI를 공급망 단계로 나누어 저작권 쟁점을 보자는 관점 반영 |
| Daniel M. German, Copyright related risks in ML/AI systems | 학술 논문 | ML/AI 시스템 생애주기에서 여러 이해관계자에게 저작권 위험이 생긴다는 관점 참고 |

## 내려받은 원문

원문 확인용 파일은 `.tmp/section-15-2-evidence/` 아래에 저장했다. `.tmp/`는 커밋하지 않는다.

- `usco-ai.html`
- `usco-part-3-generative-ai-training.pdf`
- `korea-copyright-law.html`
- `korea-copyright-law-21336-20260511.pdf`
- `ap-nyt-openai-lawsuit.html`
- `generative-ai-supply-chain.pdf`
- `copyright-risks-ml-ai.pdf`

## 법령 PDF 확인

사용자가 제공한 `저작권법(법률)(제21336호)(20260511).pdf`를 확인했다. 원문에서 확인한 핵심은 다음과 같다.

- 제2조는 저작물을 인간의 사상 또는 감정을 표현한 창작물로 정의한다.
- 제28조는 공표된 저작물을 보도, 비평, 교육, 연구 등을 위해 정당한 범위와 공정한 관행에 맞게 인용할 수 있다고 정한다.
- 제35조의5는 일반적인 이용 방법과 충돌하지 않고 저작자의 정당한 이익을 부당하게 해치지 않는 경우의 공정한 이용을 다루며, 이용 목적과 성격, 저작물의 종류와 용도, 이용 분량과 중요성, 현재 또는 잠재 시장과 가치에 미치는 영향을 고려하도록 한다.
- 제37조는 이 관에 따라 저작물을 이용하는 경우 출처 명시를 요구하며, 이용 상황에 따라 합리적인 방법으로 출처를 명시하도록 한다.

## 본문 반영 기준

- 한국 독자를 위한 책이므로 한국 저작권법을 우선 기준으로 삼았다.
- 미국 저작권청 자료는 국제 논의의 참고점이며, 한국 법률 판단을 대체하지 않는다고 명시했다.
- AP 보도는 NYT 측 주장과 소송 맥락을 보여 주는 사례로만 사용했다.
- 소송 결과가 확정된 것처럼 표현하지 않았다.
- “출처 표시만 하면 된다”는 오해를 피하기 위해 출처 표시, 이용 허락, 라이선스, 인용 요건을 분리했다.
- 법령 PDF 확인 후 제37조 출처 명시를 본문에 별도로 보강했다.
- 학습 데이터 논쟁은 단정하지 않고 권리자 관점과 AI 개발자 관점의 쟁점을 나누어 설명했다.

## 용어 처리

- 저작권(copyright)
- 저작물(work)
- 표현(expression)
- 아이디어(idea)
- 사실(fact)
- 라이선스(license)
- 출처 표시(attribution)
- 이용 허락(permission)
- 인용(quotation)
- 학습 데이터(training data)
- 권리자(rightsholder)
- 공정 이용(fair use)
- 텍스트·데이터 마이닝(text and data mining, TDM)
- 변형적 이용(transformative use)
- 시장 대체(market substitution)
- 실질적 유사성(substantial similarity)

## 검증 필요

- 한국의 생성형 AI 학습 데이터 관련 판례와 제도 논의는 계속 변할 수 있다.
- 한국저작권위원회 또는 문화체육관광부의 최신 생성형 AI 저작권 안내서가 확인되면 보완한다.
- 미국, EU, 일본의 TDM 예외와 fair use 논의는 후속 절이나 Part 5/6의 실무 적용 문서에서 더 자세히 다룰 수 있다.
- 특정 소송의 최신 절차 진행 상황은 본문 반영 전에 다시 확인해야 한다.

## 작성 판단

이 절은 저작권법을 자세히 설명하는 장이 아니라, AI 책을 작성하면서 필요한 안전한 사고 틀을 제공하는 절이다. 따라서 법률 조문을 길게 인용하지 않고, 자료 사용 원칙과 검토 질문을 중심으로 구성했다.
