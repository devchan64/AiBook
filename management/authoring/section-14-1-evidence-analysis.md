# Section 14.1 근거 검토: 모델, 앱, 데이터, 도구

## 검토 목적

- 14.1의 중심 질문은 “AI 서비스를 모델 하나가 아니라 어떤 구성요소들의 조합으로 볼 것인가?”입니다.
- 13장이 임베딩, 검색, RAG를 다뤘으므로, 14.1은 실제 서비스 구조로 넘어가기 위한 구성요소 지도를 제공합니다.

## 확인한 자료

원문 HTML과 PDF를 `.tmp/section-14-1-evidence/` 아래에 내려받았습니다.

| 자료 | 위치 | 반영 판단 |
| --- | --- | --- |
| OpenAI, *Text generation* | `.tmp/section-14-1-evidence/openai-text-generation.html` | 모델 입력과 출력, 텍스트 생성 API가 앱에서 호출되는 구성요소라는 배경 근거로 사용했습니다. |
| OpenAI, *Function calling* | `.tmp/section-14-1-evidence/openai-function-calling.html` | 도구 호출이 외부 데이터와 시스템에 연결되는 방식이라는 배경 근거로 사용했습니다. |
| NIST, *Artificial Intelligence Risk Management Framework (AI RMF 1.0)* | `.tmp/section-14-1-evidence/nist-ai-rmf-1-0.pdf`, `.html` | AI 제품, 서비스, 시스템을 모델 하나가 아니라 설계, 개발, 사용, 평가, 위험 관리 맥락에서 봐야 한다는 넓은 관점의 근거로 사용했습니다. |

## 본문 반영 기준

- AI 서비스를 모델(model), 앱(application), 데이터(data), 도구(tool), 흐름(orchestration)의 조합으로 설명했습니다.
- 모델은 생성과 판단을 담당하지만 서비스 전체와 동일시하지 않았습니다.
- 앱은 사용자 경험, 입력 구성, 출력 표시, 오류 처리의 역할로 설명했습니다.
- 데이터는 근거 자료(evidence data), 상태 데이터(state data), 입력 데이터(input data), 로그 데이터(log data)로 구분했습니다.
- 도구는 모델 밖의 시스템을 실제로 실행하는 연결 수단으로 설명했습니다.

## Section 경계 검토

- 14.1은 구성요소의 지도에 집중합니다.
- 14.2의 RAG와 도구 사용(tool use)의 구체적 비교는 예고만 했습니다.
- 14.3의 에이전트(agent), 14.4의 MCP(Model Context Protocol), 14.5의 하네스(harness), 14.6의 운영 고려는 자세히 설명하지 않았습니다.
- 보안, 저작권, 개인정보 문제는 15장 도메인으로 넘기고, 14.1에서는 권한과 검토 필요성만 짧게 언급했습니다.

## 용어 검토

- `모델(model)`, `앱(application)`, `데이터(data)`, `도구(tool)`, `입력(input)`, `출력(output)`, `맥락(context)`, `흐름 조정(orchestration)`, `근거 자료(evidence data)`, `상태 데이터(state data)`, `입력 데이터(input data)`, `로그 데이터(log data)`, `도구 사용(tool use)`을 한영 병기했습니다.
- `application`은 한국어 문맥에서 `앱`으로 쓰되 처음에는 영어를 병기했습니다.
- `tool`은 단순 UI 버튼이 아니라 외부 시스템과 연결되는 실행 수단으로 제한했습니다.

## 주의한 오해

- AI 서비스를 모델 하나로 축소하지 않았습니다.
- 모델이 직접 API 호출이나 파일 변경을 실행한다고 설명하지 않았습니다.
- 앱을 단순 화면으로만 설명하지 않고 입력 구성과 결과 표시를 포함했습니다.
- 데이터가 많을수록 항상 좋다고 설명하지 않았습니다.
- 도구 사용을 에이전트 구조 전체와 혼동하지 않았습니다.

## 참고 자료

- OpenAI, [Text generation](https://developers.openai.com/api/docs/guides/text), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Function calling](https://developers.openai.com/api/docs/guides/function-calling), OpenAI API Docs, 확인 날짜: 2026-06-23.
- NIST, [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf), 2023, 확인 날짜: 2026-06-23.
