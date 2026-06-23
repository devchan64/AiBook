# 10.3 근거 검토: 생성 결과의 품질과 위험

## 검토 목적

10.3은 생성형 AI 결과를 어떻게 검토해야 하는지 다루는 절이다. 목적은 자연스러운 출력과 믿을 수 있는 출력을 구분하고, 환각, 근거 누락, 안전, 저작권, 개인정보, 보안 위험을 개론 수준에서 연결하는 것이다.

이 절에서는 다음 경계를 둔다.

- 환각(hallucination)은 NIST의 confabulation 설명과 연결한다.
- 저작권은 법률 결론을 내리지 않고, 권리 검토 필요성만 소개한다.
- 보안은 OWASP Top 10 for LLM Applications 2025의 존재와 대표 위험만 언급한다.
- 한국 저작권법, 보안 설계, 개인정보 처리 기준은 Chapter 15로 넘긴다.
- 이 책의 작성 절차와 연결해 AI 초안은 사람 검토 대상임을 강조한다.

## 확인한 원문

원문은 `.tmp/section-10-3-evidence/` 아래에 저장했다.

| 자료 | 파일 | 확인 내용 |
| --- | --- | --- |
| NIST AI 600-1 | `nist-ai-600-1-genai-profile.pdf`, `nist-ai-600-1-genai-profile.txt` | GAI 위험 범주, confabulation, information integrity, information security, intellectual property |
| OWASP Top 10 for LLM Applications 2025 | `owasp-top-10-llm-2025.pdf` | `curl` 저장은 no-access HTML로 저장됨. 브라우저 도구로 PDF 내용과 항목 목차 확인 |
| U.S. Copyright Office, Part 2 Copyrightability | `usco-ai-copyrightability-part-2.pdf`, `usco-ai-copyrightability-part-2.txt` | human authorship 요구, AI-only output의 저작권 보호 한계 |
| IBM, AI hallucinations | `ibm-ai-hallucinations.html` | hallucination의 일반적 설명과 실제 위험 예시 |
| AP, Philly sheriff AI-generated bogus news | `ap-ai-generated-bogus-news.html` | AI 생성 뉴스형 글, 사실 확인 누락, 정보 무결성 위험 사례 |
| AP, UK fake AI-generated legal cases | `ap-uk-fake-ai-cases.html` | 존재하지 않는 AI 생성 판례 인용, 고위험 영역에서의 검토 책임 사례 |
| AP, New Jersey deceptive AI-generated media law | `ap-new-jersey-deepfake-law.html` | 기만적 AI 생성 미디어와 딥페이크에 대한 법적 대응 사례 |

주의: OWASP PDF는 브라우저 도구에서는 열렸지만 `curl` 저장은 접근 차단 페이지로 저장되었다. 따라서 본문에서는 OWASP를 보안 위험 분류의 보조 근거로만 사용했다.

## 자료별 근거 판단

### NIST AI 600-1, Generative AI Profile

근거 위치:

- 추출 텍스트 222-223행: Confabulation을 confidently stated but erroneous or false content로 설명하고 hallucinations/fabrications라고도 부른다.
- 303-316행: GAI systems가 prompts에 대해 erroneous or false content를 생성하고, 통계적 분포 근사와 관련해 사실적으로 부정확하거나 내부적으로 일관되지 않은 출력을 만들 수 있다고 설명한다.
- 242-243행, 449-464행: Information Integrity를 사실/의견/허구 구분, 불확실성 표시, misinformation/disinformation과 연결한다.
- 361행 이후와 449행 이후: Data privacy, information security, intellectual property 등 위험 범주를 제시한다.
- 516-521행: 저작권 있는 자료를 포함한 training data와 memorization 출력이 copyright risk와 연결될 수 있음을 설명한다.

본문 반영:

- 환각을 `그럴듯한 오류`, `근거 없는 생성`, `confabulation`으로 설명했다.
- 생성형 AI 위험을 사실성, 정보 무결성, 개인정보, 보안, 저작권, 과신으로 나눴다.
- NIST의 위험 범주는 개론용으로 압축해 반영했다.

주의:

- NIST의 CBRN, 환경 영향, 사회적 영향 등 전체 위험 분류는 10.3 범위를 넘으므로 일부만 반영했다.
- 고위험 사용 맥락은 15장에서 더 자세히 다룬다.

### OWASP Top 10 for LLM Applications 2025

근거 위치:

- 브라우저 확인 내용: 2025 버전 목차에 Prompt Injection, Sensitive Information Disclosure, Supply Chain, Data and Model Poisoning, Improper Output Handling, Excessive Agency, System Prompt Leakage, Vector and Embedding Weaknesses, Misinformation 등이 포함된다.
- 공개 페이지는 2024-11-17 자료로 표시된다.

본문 반영:

- LLM 애플리케이션 보안 위험 예시로 prompt injection, sensitive information disclosure, improper output handling, excessive agency를 언급했다.

주의:

- OWASP 항목을 상세 설명하지 않는다.
- 보안 설계와 완화책은 Chapter 15 또는 서비스 아키텍처 장으로 넘긴다.

### U.S. Copyright Office, Copyright and Artificial Intelligence Part 2

근거 위치:

- 추출 텍스트 213-218행 부근: human authorship이 저작권 보호의 핵심 요건이고, AI-generated material이 있으면 human author contribution을 설명해야 한다는 취지.
- 추출 텍스트 1027-1031행 부근: human-authored and AI-generated material의 selection, coordination, arrangement와 AI-generated elements standing alone의 구분.

본문 반영:

- AI가 전적으로 생성한 콘텐츠와 인간의 창작적 기여가 있는 AI 보조 산출물을 구분해야 한다고 설명했다.
- 한국어 공개 문서인 이 책에서는 대한민국 저작권법 관점 검토가 별도로 필요하다고 명시했다.

주의:

- 미국 저작권청 기준을 한국 법률 결론처럼 쓰지 않는다.
- 한국 출판물과 교육 자료 사용 기준은 AGENTS.md와 Chapter 15에서 별도 검토한다.

### IBM, AI hallucinations

근거 위치:

- HTML meta description: AI hallucinations를 LLM이 nonexistent patterns or objects를 인식해 nonsensical or inaccurate outputs를 만드는 현상으로 설명한다.
- 768행 부근: generative AI가 요청에 적절히 답하기를 기대하지만, 때로는 training data에 기반하지 않거나 식별 가능한 패턴을 따르지 않는 출력을 만들 수 있다고 설명한다.
- 882행 부근: healthcare나 emergency news 같은 실사용 맥락에서 hallucination의 위험을 언급한다.

본문 반영:

- 환각이 실제 사용 맥락에서 위험해질 수 있다는 보조 근거로 사용했다.

주의:

- IBM의 비유 표현은 본문에 직접 인용하지 않았다.
- 환각 정의의 핵심 근거는 NIST를 우선했다.

### Associated Press 보도 사례

근거 위치:

- `ap-ai-generated-bogus-news.html` 16415-16416행 부근: 선거 캠페인 사이트에 게시된 30개 이상의 긍정적 “뉴스” 글이 ChatGPT로 생성되었고, 지역 언론사가 원문을 확인하지 못한 뒤 삭제되었다고 보도한다.
- `ap-ai-generated-bogus-news.html` 16941행 부근: 업무 이메일, 웹사이트 문구, 문서 작성에 생성형 AI를 사용할 때 정확성 검토와 사실 확인을 우선하지 않으면 문제가 생길 수 있다고 설명한다.
- `ap-uk-fake-ai-cases.html` 16550-16551행 부근: 영국 법정 절차에서 AI가 생성한 가짜 판례가 인용되었고, 판사는 정확성 확인 없이 제출된 허위 정보가 사법 신뢰에 영향을 줄 수 있다고 경고했다.
- `ap-uk-fake-ai-cases.html` 16570행, 17405행 부근: 한 사건에서는 존재하지 않는 판례 18건, 다른 사건에서는 가짜 판례 5건이 언급되었다.
- `ap-new-jersey-deepfake-law.html` 16523-16524행 부근: 뉴저지에서 기만적 AI 생성 미디어 제작과 배포가 범죄 및 민사소송 대상이 되었고, 여러 주가 선거 관련 생성형 AI 미디어에 대응하고 있다고 보도한다.

본문 반영:

- 언론 보도는 개념 정의의 근거가 아니라 실제 사용 맥락의 보조 사례로 분리했다.
- 가짜 뉴스형 문장, 가짜 판례, 딥페이크 규제 사례를 정보 무결성, 사실성, 안전, 권리 문제와 연결했다.

주의:

- AP 보도 사례를 생성형 AI 위험의 전체 통계처럼 일반화하지 않는다.
- 개념 기준은 NIST, OWASP, 저작권청 자료에 두고, 언론 보도는 독자의 현실 감각을 보강하는 사례로만 사용한다.

## 일반화 문구

10.3에서는 다음 문구가 안전하다.

> 자연스러움은 품질의 일부일 뿐이고, 사실성, 근거, 안전성, 저작권, 개인정보, 사용 맥락을 따로 검토해야 한다.

이 책의 작성 원칙과 연결할 문구는 다음이 적절하다.

> AI는 빠르게 초안을 만들 수 있지만, 책의 신뢰성은 초안 생성 속도가 아니라 검토 과정에서 나온다.

## 도메인 경계

10.3에서 다룬다:

- 자연스러운 출력과 정확한 출력의 차이
- 환각/confabulation
- 근거 누락
- 생성 결과의 안전, 개인정보, 저작권, 보안 위험을 개론 수준으로 분류
- 이 책의 AI 초안 검토 절차

10.3에서 깊게 다루지 않는다:

- 한국 저작권법 세부 판단
- 프롬프트 인젝션 완화 설계
- 개인정보 처리 기준
- AI governance 체계
- RAG, tool use, model card, system card 상세
