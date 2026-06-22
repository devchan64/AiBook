# 5.2 근거 분석: inference는 무엇을 실행하는가

이 문서는 `docs/chapters/chapter-05/section-02.md`의 근거 연결을 검토한 관리 메모입니다.

원문 확인 규칙에 따라 이미 내려받은 `.tmp/section-5-1-evidence/` 자료를 우선 사용했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 확인한 자료

| 자료 | 로컬 확인 | 본문 반영 역할 |
| --- | --- | --- |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-5-1-evidence/google-ml-glossary.html` | inference, prediction, weight, prompt 정의 확인 |
| scikit-learn, `Glossary of Common Terms and API Elements` | `.tmp/section-5-1-evidence/scikit-learn-glossary.html` | fitted, predict, NotFittedError, target space 설명 확인 |

## 핵심 근거 연결

| 본문 주장 | 근거 | 반영 판단 |
| --- | --- | --- |
| 전통적 머신러닝에서 inference는 학습된 모델을 라벨 없는 예시에 적용해 예측을 만드는 과정이다 | Google ML Glossary의 inference 항목 | 유지 |
| LLM에서 inference는 학습된 모델을 사용해 프롬프트에 대한 응답을 생성하는 과정이다 | Google ML Glossary의 inference 항목 | 유지. LLM 세부 디코딩은 뒤로 보냄 |
| training은 가중치를 정하고 inference는 학습된 가중치로 예측을 만든다 | Google ML Glossary의 weight 항목 | 유지 |
| prediction은 모델의 출력이며, 과제에 따라 클래스나 숫자가 될 수 있다 | Google ML Glossary의 prediction 항목 | 유지 |
| fitted 상태가 아닌 모델에서 predict를 호출하면 오류가 발생해야 한다 | scikit-learn glossary의 fitted, predict 항목 | 학습된 모델을 사용한다는 실무 API 관점의 보조 근거로 반영 |
| inference와 통계학의 inference는 의미가 다를 수 있다 | Google ML Glossary의 inference 항목은 statistics에서의 의미가 다르다고 명시함 | 5.3의 용어 혼동으로 넘기되 5.2에서 짧게 경계 표시 |
| 한국어 `추론`은 논리적 사고의 어감을 줄 수 있으므로 5.2에서는 `모델 실행`, `모델 적용`, `출력을 만드는 실행`으로 풀어 읽는 것이 안전하다 | Google ML Glossary의 inference 정의가 전통 ML에서는 trained model을 unlabeled examples에 applying해 predictions를 만드는 과정, LLM에서는 prompt에 대한 response를 generate하는 과정이라고 설명함 | 유지. 상세한 한국어 추론과의 비교는 5.3으로 넘김 |
| 한국어의 일반적 추론과 AI inference는 입력에서 결과를 낸다는 점은 비슷하지만, 사람의 의미 이해와 논리적 reasoning 전체를 뜻하지는 않는다 | Google ML Glossary의 inference 정의는 prediction/response generation 중심이며, statistics의 inference와도 의미가 다를 수 있다고 구분함 | 5.2에는 전환 문장만 남기고, 비교표와 상세 설명은 5.3으로 이동 |

## 섹션 구성 검토

| 검토 항목 | 판단 |
| --- | --- |
| 5.1과의 경계 | 훈련으로 내부 값이 바뀐다는 설명을 이어 받아, inference는 그 값을 사용하는 과정으로 제한 |
| 5.3과의 경계 | 한국어 `추론`, reasoning, statistical inference의 혼동은 길게 다루지 않고 다음 절로 넘김 |
| Chapter 10-13과의 경계 | LLM 토큰 생성, temperature, 프롬프트, 임베딩, RAG는 위치만 언급하고 세부 설명은 뒤로 보냄 |
| Chapter 14와의 경계 | 서비스 요청 처리 흐름은 모델 inference와 서비스 처리를 구분하는 수준만 설명 |
| Part 4와의 경계 | 순전파(forward pass)는 직관만 언급하고 행렬 계산, attention, 역전파와 옵티마이저는 다루지 않음 |

## 주의한 표현

- inference를 사람의 reasoning과 동일시하지 않았습니다.
- 한국어 독자에게 `inference=추론`만 제시하면 논리적 사고처럼 오해될 수 있어, `모델 실행`, `모델 적용`, `출력을 만드는 실행`이라는 짧은 풀이만 남겼습니다.
- 한국어의 일반적 `추론`과 AI inference의 비슷한 점과 다른 점은 5.3으로 자연스럽게 넘어가도록 전환 문장만 남겼습니다.
- LLM inference를 “생각하는 과정”이 아니라 학습된 모델과 프롬프트, 생성 설정을 사용해 응답을 만드는 실행으로 설명했습니다.
- 일반적인 inference에서는 모델 파라미터가 바뀌지 않는다고 쓰되, 온라인 학습과 지속 학습 같은 예외가 있음을 밝혔습니다.
- 모델 출력과 서비스 결정을 구분했습니다.
- `temperature`, `top-p`, `max tokens`는 모델 내부 파라미터가 아니라 생성 설정값으로 유지했습니다.

## 본문에 넣지 않은 내용

- 행렬 곱, activation, attention, KV cache, decoding 알고리즘은 LLM과 딥러닝 장에서 다룹니다.
- statistical inference와 reasoning의 용어 구분은 5.3에서 다룹니다.
- RAG, Tool use, 라우팅, 권한, 모니터링은 AI 서비스 아키텍처 장에서 다룹니다.
- 모델 serving 인프라, GPU 최적화, latency, batch inference는 서비스 운영 장에서 다룹니다.

## 검증 필요

- `inference`의 한국어 표현을 `추론`, `실행`, `모델 실행` 중 어떤 방식으로 병기할지 5.3에서 재검토합니다.
- LLM 장에서 `generation`, `decoding`, `sampling`의 용어 경계를 다시 정리해야 합니다.

## 출처

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary), 확인 날짜: 2026-06-22.
- scikit-learn developers, [Glossary of Common Terms and API Elements](https://scikit-learn.org/stable/glossary.html), 확인 날짜: 2026-06-22.
