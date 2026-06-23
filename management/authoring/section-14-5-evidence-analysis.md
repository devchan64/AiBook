# Section 14.5 근거 검토: 하네스(harness)와 평가 실행 환경

## 검토 목적

- 14.5의 중심 질문은 “모델, 도구, MCP, 에이전트 실행을 어떻게 기록하고 검증하고 반복 평가할 것인가?”입니다.
- 하네스(harness)를 특정 제품 이름이 아니라 실행을 감싸는 환경으로 일반화하는 것이 목적입니다.
- 사용자의 요청에 따라 하네스의 어원적 직관, 소프트웨어 테스트 하네스(test harness)에서의 등장, 에이전트 하네스(agent harness)로 확장되는 흐름을 함께 검토했습니다.
- 추가 논의에 따라 워크플로우(workflow), 파이프라인(pipeline), 운영(Ops) 관점과의 비교를 짧게 넣되, 하네스와 동일시하지 않도록 제한했습니다.
- 본문 재검토에서 도입부의 비교 설명을 `가까운 말들과 구분하기`로 분리하고, 책 작성 과정 자체를 하네스 예시로 드는 문단은 Section 도메인 밖으로 판단해 본문에서 제거했습니다.
- 14.6의 `AI 서비스가 현실에서 만나는 제약`과 15장의 보안 세부 쟁점을 침범하지 않도록 범위를 제한했습니다.

## 확인한 자료

| 자료 | 위치 | 반영 판단 |
| --- | --- | --- |
| Merriam-Webster, *Harness* | `.tmp/section-14-5-evidence/merriam-webster-harness.html` | 로컬 다운로드는 Cloudflare 차단 페이지였으나, 브라우저 확인으로 harness가 장비, 고정 장치, 기술을 활용한다는 동사 의미를 가진다는 점을 확인했습니다. 어원과 직관 설명의 보조 근거로 사용했습니다. |
| Online Etymology Dictionary, *Harness* | `.tmp/section-14-5-evidence/etymonline-harness.html` | harness가 장비, 무장, 말의 장구에서 출발하고, 동사로 준비시키다, 장비하다, 힘으로 쓰도록 제어하다는 의미로 확장된 흐름을 확인했습니다. |
| Sanderson Oliveira de Macedo, *What makes a harness a harness: necessary and sufficient conditions for an agent harness* | `.tmp/section-14-5-evidence/agent-harness-2606-10106.html`, `.tmp/section-14-5-evidence/agent-harness-2606-10106.pdf` | 2026년 arXiv 프리프린트입니다. agent harness라는 표현이 생성형 AI 소프트웨어 엔지니어링 문맥에서 널리 쓰이지만 제품, 평가 scaffold, framework, SDK, IDE plugin, orchestrator와 혼용된다는 점을 확인했습니다. 표준 합의가 아니라 최근 논의로 제한해 반영했습니다. |
| LangChain, *LangSmith Observability* | `.tmp/section-14-5-evidence/langsmith-observability.html` | LLM 애플리케이션을 개별 trace부터 production-wide metric까지 관찰하고, tracing을 앱에 붙이며, workflow 자동화와 online evaluation을 구성한다는 근거로 사용했습니다. |
| LangChain, *Evaluation concepts* | `.tmp/section-14-5-evidence/langsmith-evaluation-concepts.html` | LLM 출력의 비결정성 때문에 평가가 필요하며, LLM call, retrieval step, tool invocation, output formatting 같은 구성요소별 품질 기준을 세운다는 근거로 사용했습니다. offline evaluation, online evaluation, trace 기반 run, evaluator, feedback loop 설명을 확인했습니다. |
| Yang et al., *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering* | `.tmp/section-14-5-evidence/swe-agent-2405-15793.html` | LM agent가 디지털 환경에서 복잡한 작업을 수행하고, 파일 편집, 저장소 탐색, 테스트 실행을 위한 agent-computer interface가 성능에 영향을 준다는 사례 근거로 사용했습니다. |
| Wang et al., *OpenHands: An Open Platform for AI Software Developers as Generalist Agents* | `.tmp/section-14-5-evidence/openhands-2407-16741.html` | 에이전트가 코드 작성, CLI, 브라우징, 샌드박스 실행, 평가 벤치마크를 포함하는 플랫폼 안에서 동작한다는 사례 근거로 사용했습니다. |
| OpenAI, *Integrations and observability* | `.tmp/section-14-5-evidence/openai-agents-integrations-observability.html` | 에이전트 실행에서 trace가 모델 호출, 도구 호출, 핸드오프, 가드레일, custom span을 기록한다는 근거로 사용했습니다. |
| OpenAI, *Evaluate agent workflows* | `.tmp/section-14-5-evidence/openai-agent-evals.html` | 개별 trace 확인에서 데이터셋과 평가 실행으로 넘어가는 흐름, agent workflow 평가 개념의 근거로 사용했습니다. |
| OpenAI, *Working with evals* | `.tmp/section-14-5-evidence/openai-evals.html` | evals가 모델 출력 테스트와 개선에 쓰이며, 기준과 결과 보고를 포함한다는 근거로 사용했습니다. |
| OpenAI, *Agents SDK* | `.tmp/section-14-3-evidence/openai-agents-guide.html` | agent loop, state, observability, eval workflow로 이어지는 큰 지도 근거로 재사용했습니다. |

## 하네스 용어 검토

- 사전과 어원 자료에서는 harness가 장비, 마구, 붙잡아 고정하는 장치, 힘을 활용하도록 제어하는 동작과 연결됩니다.
- 소프트웨어 테스트 문맥의 테스트 하네스(test harness)는 테스트 대상(system under test)을 입력, 설정, 스텁(stub), 드라이버(driver), 비교 기준으로 감싸 반복 실행 가능하게 만드는 장치로 이해할 수 있습니다.
- AI 에이전트 문맥의 하네스는 모델 자체가 아니라 모델, 도구, 프롬프트, 상태, 권한, 로그, 평가 기준을 실행 가능한 작업 흐름으로 묶는 주변 구조로 일반화할 수 있습니다.
- `agent harness`라는 표현은 아직 제품 전체, 평가 scaffold, framework, SDK, IDE plugin, orchestrator와 혼용될 수 있으므로, 본문에서는 `에이전트 실행을 감싸고 관찰, 검증, 평가하게 하는 실행 장치`라는 좁은 의미로 제한했습니다.
- 사용자의 “공감의 흐름” 요청은 “하네스가 왜 이 개념에 어울리는가”라는 직관적 연결로 해석했습니다. 본문에서는 “힘을 만드는 장치가 아니라 힘을 안전하게 쓰게 하는 연결 장치”라는 일반화 문구로 정리했습니다.
- 워크플로우(workflow)는 단계 흐름, 파이프라인(pipeline)은 반복 가능한 처리 흐름, 운영(Ops)은 안정적 반복과 관찰, 개선의 배경으로 구분했습니다. 하네스는 이 셋과 비교할 수 있지만, 실행을 감싸 기록하고 평가하게 하는 장치로 좁혔습니다.
- 프레임워크(framework)는 개발 구조와 API를 제공하는 더 넓은 개념으로 두고, 하네스는 그 안에 포함되거나 구현에 사용될 수 있지만 동일하지 않다고 구분했습니다.
- trace, log, eval을 에이전트 워크플로우에 묶는다는 해석은 OpenAI의 trace-grading workflow, LangSmith의 trace 기반 online evaluation, datasets와 eval runs, evaluator 설명과 연결됩니다.
- 다만 eval은 항상 실행 중에 실시간으로 작동한다고 단정하지 않았습니다. 실행 중 trace/log, 실행 후 또는 운영 중 evaluation이 개선 루프에 연결된다는 제한된 표현을 사용했습니다.
- trace/log/eval이 별도의 독립 도구 묶음으로 존재해야만 하네스가 된다고 설명하지 않았습니다. 에이전트와 에이전트를 연결하거나 검토 흐름을 붙이는 패턴도 실행을 제한, 기록, 검증하게 만들면 하네스 관점으로 볼 수 있습니다.
- 반대로 여러 에이전트를 연결한 모든 구조를 하네스라고 단정하지 않았습니다. 관찰 가능성, 실행 조건, 검증 기준, 실패 확인이 함께 있어야 하네스 관점이 성립한다고 제한했습니다.

## 본문 반영 기준

- 하네스의 어원적 직관은 장식적 비유가 아니라, 왜 AI 실행 구조를 `감싸는 장치`로 이해할 수 있는지 설명하는 도입 근거로만 사용했습니다.
- 테스트 하네스(test harness)를 소프트웨어 테스트에서 온 용례로 소개하되, 특정 테스트 프레임워크나 구현 방식은 설명하지 않았습니다.
- agent harness 관련 최근 논문은 2026년 프리프린트이므로, 합의된 표준 정의처럼 단정하지 않고 용례가 넓고 느슨하다는 주의점의 근거로 사용했습니다.
- DevOps, MLOps, LLMOps는 독자가 이미 가진 운영 감각과 연결하기 위한 비교 배경으로만 사용했습니다. 하네스를 하나의 Ops 방법론, 제품군, 도구 묶음으로 이해하지 않도록 본문에 제한 문장을 추가했습니다. 별도의 학술 정의나 운영 방법론 설명은 14.6 이후의 영역으로 넘겼습니다.
- LangSmith 문서는 특정 제품 문서이므로, 제품 사용법이 아니라 관찰 가능성(observability), trace 기반 run, offline/online evaluation, evaluator, feedback loop가 실제 LLM 앱 운영 문맥에서 함께 다뤄진다는 근거로 제한했습니다.
- SWE-agent와 OpenHands는 `agent harness`라는 용어의 직접 정의 근거가 아니라, 에이전트 실행 환경이 파일, 명령, 테스트, 샌드박스, 평가 벤치마크와 결합된다는 사례 근거로 제한했습니다.
- multi-agent나 agent-to-agent 연결은 하네스의 한 구현 패턴이 될 수 있지만, 하네스와 동일한 개념으로 다루지 않았습니다.
- 하네스(harness)를 `모델과 도구 실행을 감싸고 기록, 검증, 평가할 수 있게 하는 실행 환경`으로 일반화했습니다.
- trace는 요청 하나의 실행 흐름을 단계별로 보는 기록으로 설명했습니다.
- log는 사후 설명, 재현성, 책임 추적을 위한 기록으로 설명했습니다.
- evaluation은 데이터셋(dataset), 기대 결과(expected output), 그레이더(grader), 평가 실행(eval run), 보고서(report)의 조합으로 설명했습니다.
- OpenAI 문서는 특정 플랫폼 문서이므로, 구현 기능 소개가 아니라 일반적인 관찰 가능성(observability)과 반복 평가의 근거로 제한해 사용했습니다.

## Section 경계 검토

- 14.5는 하네스, trace, log, evaluation, grader의 개념에 집중합니다.
- 하네스의 어원과 테스트 하네스에서 온 흐름은 개념 이해를 위한 도입으로만 다루었습니다.
- 에이전트 하네스의 엄밀한 정의 논쟁은 깊게 들어가지 않았습니다.
- 워크플로우, 파이프라인, Ops 비교는 하네스의 위치를 잡기 위한 짧은 구분으로만 넣었습니다.
- 프레임워크 비교도 하네스의 위치를 잡기 위한 구분으로만 넣었고, 에이전트 프레임워크 설명으로 확장하지 않았습니다.
- trace/log/eval을 워크플로우 일부로 묶는다는 설명은 14.5의 관찰과 평가 범위 안에서만 다루었습니다.
- 특정 SDK 코드, 대시보드 사용법, API 파라미터, 평가 자동화 구현은 다루지 않았습니다.
- 14.6의 비용(cost), 지연 시간(latency), 운영(operation)은 예고만 하고 자세히 다루지 않았습니다.
- 15장의 보안(security), 개인정보(privacy)는 로그 설계의 주의점 수준으로만 언급했습니다.
- Part 5의 LLM 평가 장에서는 더 깊은 평가 방법을 다룰 수 있으므로, 여기서는 서비스 구조 관점의 입문 설명으로 제한했습니다.

## 용어 검토

- `하네스(harness)`, `테스트 하네스(test harness)`, `에이전트 하네스(agent harness)`, `테스트 대상(system under test)`, `스텁(stub)`, `드라이버(driver)`, `워크플로우(workflow)`, `파이프라인(pipeline)`, `운영(Ops)`, `프레임워크(framework)`, `추적(trace)`, `로그(log)`, `평가(evaluation)`, `그레이더(grader)`, `데이터셋(dataset)`, `평가 실행(eval run)`, `회귀(regression)`, `재현성(reproducibility)`, `관찰 가능성(observability)`, `가드레일(guardrail)`, `핸드오프(handoff)`, `커스텀 스팬(custom span)`을 한영 병기했습니다.
- `추론`이라는 한국어 표현은 사용하지 않고, 실행 관찰과 평가 중심으로 용어를 정리했습니다.
- `evaluation`을 단순 감상이나 사용자의 느낌으로 설명하지 않고, 반복 가능한 비교와 기준으로 설명했습니다.

## 주의한 오해

- 하네스가 모델 자체라고 설명하지 않았습니다.
- 하네스의 어원을 근거로 AI 시스템의 모든 실행 구조를 하네스라고 부르지는 않았습니다.
- 에이전트 하네스(agent harness)를 합의된 표준 용어로 단정하지 않았습니다.
- 하네스와 DevOps, MLOps, LLMOps를 같은 개념으로 설명하지 않았습니다.
- 하네스와 프레임워크를 같은 개념으로 설명하지 않았습니다.
- 하네스를 특정 DevOps 도구처럼 이해하게 만드는 문장을 피했습니다.
- 하네스를 trace/log/eval 도구 묶음으로만 이해하게 만드는 문장을 피했습니다.
- 여러 에이전트를 연결하면 곧 하네스가 된다는 식의 단정을 피했습니다.
- eval이 항상 실시간 워크플로우 내부에서 실행된다고 설명하지 않았습니다.
- 하네스가 정답을 자동 보장한다고 설명하지 않았습니다.
- trace와 log를 같은 말로 뭉개지 않고, trace는 실행 흐름, log는 사후 기록으로 구분했습니다.
- 그레이더가 사람의 판단을 완전히 대체한다고 설명하지 않았습니다.
- 평가 기준과 데이터셋 대표성은 사람이 설계해야 한다는 점을 남겼습니다.

## 참고 자료

- Merriam-Webster, [Harness](https://www.merriam-webster.com/dictionary/harness), Merriam-Webster Dictionary, 확인 날짜: 2026-06-23.
- Online Etymology Dictionary, [Harness](https://www.etymonline.com/word/harness), 확인 날짜: 2026-06-23.
- Sanderson Oliveira de Macedo, [What makes a harness a harness: necessary and sufficient conditions for an agent harness](https://arxiv.org/abs/2606.10106), arXiv preprint, 2026, 확인 날짜: 2026-06-23.
- LangChain, [LangSmith Observability](https://docs.langchain.com/langsmith/observability), Docs by LangChain, 확인 날짜: 2026-06-23.
- LangChain, [Evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts), Docs by LangChain, 확인 날짜: 2026-06-23.
- John Yang et al., [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793), arXiv, 2024, 확인 날짜: 2026-06-23.
- Xingyao Wang et al., [OpenHands: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/abs/2407.16741), arXiv, 2024, 확인 날짜: 2026-06-23.
- OpenAI, [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Working with evals](https://developers.openai.com/api/docs/guides/evals), OpenAI API Docs, 확인 날짜: 2026-06-23.
