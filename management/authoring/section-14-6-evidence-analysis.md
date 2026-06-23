# Section 14.6 근거 검토: AI 서비스가 현실에서 만나는 제약

## 검토 목적

- 14.6의 제목을 `비용, 지연 시간, 운영 고려`에서 `AI 서비스가 현실에서 만나는 제약`으로 재구성했습니다.
- 비용(cost), 지연 시간(latency), 운영(operation)을 제목의 병렬 항목으로 나열하면 실무 운영 방법론이나 비용 최적화 절로 좁게 읽힐 수 있습니다.
- Part 1의 개론 흐름에서는 `서비스 제약(service constraints)`이라는 상위 관점으로 묶고, 비용과 지연 시간은 그 안의 핵심 요소로 설명하는 편이 안전하다고 판단했습니다.

## 확인 자료

| 자료 | 확인한 내용 | 본문 반영 |
| --- | --- | --- |
| OpenAI, Latency optimization | 스트리밍, 청킹, 지연 시간 최적화가 사용자 경험과 실제 처리 시간에 영향을 준다는 설명 | 지연 시간은 모델 실행만이 아니라 사용자 대기 시간 전체라는 설명에 반영 |
| OpenAI, Cost optimization | 비용과 지연 시간이 연결되어 있고, 토큰과 요청 수를 줄이면 비용과 처리 시간이 줄어드는 경향이 있다는 설명 | 비용을 토큰, 요청 수, 모델 선택, 배치, 캐싱과 연결 |
| OpenAI, Prompt caching | 반복되는 입력 접두부(prefix)를 캐싱하면 비용과 지연 시간을 줄일 수 있으나 입력 구조가 중요함 | 캐싱을 만능 해법이 아니라 반복 입력에서 유리한 선택지로 설명 |
| OpenAI, Batch API | 비동기 요청 묶음, 별도 처리 한도, 즉시 응답이 필요하지 않은 작업에 적합하다는 설명 | 실시간 작업과 배치 작업의 차이 설명에 반영 |
| OpenAI, Rate limits | 조직, 프로젝트, 모델 단위 제한, 남은 요청/토큰 헤더, 재시도와 지수 백오프 권장, 실패 요청도 제한에 포함될 수 있음 | 제한을 설계 조건으로 보고 재시도 정책을 설명 |
| OpenAI, Production best practices | 모델 모니터링, 데이터와 모델 관리, 재학습, 배포 자동화 등 운영 단계 고려사항 | 운영을 반복 사용을 위한 관찰과 조정 조건으로 제한해 반영 |
| OpenAI, Deployment checklist | 운영 전 확인해야 할 보안, 안정성, 오류 처리, 모니터링 성격의 체크리스트 | 작은 서비스에서도 기준을 먼저 정해야 한다는 설명의 배경으로 사용 |

원문 HTML은 `.tmp/section-14-6-evidence/` 아래에 내려받아 확인했습니다. `.tmp/`는 임시 근거 확인 공간이므로 커밋하지 않습니다.

## 본문 반영 기준

- 가격표, 모델별 단가, 특정 모델 추천은 제외했습니다. 가격과 제품 스펙은 변동 가능성이 높고, 이 절의 중심 질문이 아닙니다.
- 비용(cost)을 토큰(token) 수만으로 단순화하지 않고, 모델 선택(model choice), 입력/출력 길이, 호출 횟수, 도구 호출(tool call), 재시도(retry), 평가 실행(eval run)까지 포함했습니다.
- 지연 시간(latency)을 모델 실행(inference)만으로 설명하지 않고, 검색(retrieval), 도구 호출(tool call), 네트워크(network), 후처리(post-processing)까지 포함했습니다.
- 레이트 리밋(rate limit), 사용량 제한(usage limit)은 장애가 아니라 설계 조건으로 설명했습니다.
- 스트리밍(streaming), 캐싱(caching), 배치(batch)는 특정 벤더 기능이라기보다 서비스 제약을 다루는 선택지로 설명했습니다.

## Section 경계 검토

- 14.1의 서비스 구성요소, 14.2의 RAG와 도구 사용, 14.3의 에이전트, 14.4의 MCP, 14.5의 하네스 설명을 반복하지 않았습니다.
- 14.6은 이 구성들이 실제 서비스에서 만나는 제약으로 넘어가는 연결 절로 작성했습니다.
- 보안(security), 개인정보(privacy), 저작권(copyright)은 15장 영역이므로 자세히 다루지 않았습니다.
- DevOps, MLOps, LLMOps 방법론 설명으로 확장하지 않았습니다. 운영(operation)은 반복 사용을 위한 관찰과 조정 조건으로 제한했습니다.

## 용어 검토

- `서비스 제약(service constraints)`, `비용(cost)`, `지연 시간(latency)`, `처리량(throughput)`, `사용량 제한(usage limit)`, `레이트 리밋(rate limit)`, `재시도(retry)`, `지수 백오프(exponential backoff)`, `지터(jitter)`, `배치(batch)`, `캐싱(caching)`, `프롬프트 캐싱(prompt caching)`, `스트리밍(streaming)`, `모니터링(monitoring)`, `토큰(token)`, `도구 호출(tool call)`, `모델 실행(inference)`을 한영 병기했습니다.
- `운영(operation)`은 제목의 중심어로 두지 않고, 본문에서 좁은 의미로 제한했습니다.

## 주의한 오해

- 비용은 토큰 수만으로 결정된다고 쓰지 않았습니다.
- 지연 시간은 모델 속도만으로 결정된다고 쓰지 않았습니다.
- 캐싱과 배치는 항상 좋은 해법이라고 쓰지 않았습니다.
- 레이트 리밋 오류는 무한 재시도로 해결하면 된다고 쓰지 않았습니다.
- 운영은 특정 도구나 DevOps 방법론과 같다고 쓰지 않았습니다.

## 참고 자료

- OpenAI, [Latency optimization](https://developers.openai.com/api/docs/guides/latency-optimization), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Cost optimization](https://developers.openai.com/api/docs/guides/cost-optimization), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Batch API](https://developers.openai.com/api/docs/guides/batch), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Rate limits](https://developers.openai.com/api/docs/guides/rate-limits), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Deployment checklist](https://developers.openai.com/api/docs/guides/deployment-checklist), OpenAI API Docs, 확인 날짜: 2026-06-23.
