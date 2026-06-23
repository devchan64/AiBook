# 15.3 근거 검토: 보안과 개인정보

## 목적

15.3은 AI 서비스의 입력, 출력, 도구 권한, 로그가 보안(security)과 개인정보(privacy) 위험으로 이어질 수 있음을 설명한다.

## 근거

- OWASP Top 10 for Large Language Model Applications: 프롬프트 인젝션, 민감 정보 노출, 과도한 에이전시, 플러그인 설계 위험을 본문에 반영했다.
- NIST AI RMF 및 Generative AI Profile: AI 위험을 서비스 설계와 운영에서 관리해야 한다는 기준으로 사용했다.

## 반영 판단

- 개인정보보호 법률 세부 조항은 이 절에서 자세히 설명하지 않았다.
- 보안 실무 세부 구현은 Part 5/6 또는 프로젝트 문서로 넘긴다.
- 핵심은 “AI 입력은 데이터 이동이며, 에이전트 권한은 최소화해야 한다”는 입문 관점이다.

## 내려받은 원문

- `.tmp/sections-15-3-to-17-3-evidence/owasp-llm-top10.html`
- `.tmp/sections-15-3-to-17-3-evidence/nist-ai-rmf.html`

