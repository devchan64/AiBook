# 10.1 근거 검토: 분류, 예측, 생성의 차이

## 검토 목적

10.1은 생성형 AI 개론의 도입 절이다. 목적은 생성형 AI를 바로 설명하기 전에 분류(classification), 예측(prediction), 생성(generation)의 출력 차이를 정리하는 것이다.

이 절에서는 다음 경계를 둔다.

- 분류는 범주(class)를 고르는 작업으로 설명한다.
- 예측은 숫자, 범주, 상태, 다음 항목을 추정하는 넓은 표현으로 설명한다.
- 생성은 조건에 맞는 새 산출물(output artifact)을 만드는 작업으로 설명한다.
- 생성형 AI를 기존 머신러닝과 완전히 단절된 기술처럼 쓰지 않는다.
- 다음 토큰 예측, sampling, diffusion model, Transformer 세부 구조는 10.2와 뒤 LLM 장으로 넘긴다.

## 확인한 원문

원문 HTML과 PDF는 `.tmp/section-10-1-evidence/` 아래에 저장했다.

| 자료 | 파일 | 확인 내용 |
| --- | --- | --- |
| Google Machine Learning Crash Course, Classification | `google-classification.html` | classification은 여러 class 중 예제가 어디에 속하는지 예측하는 작업 |
| Google Machine Learning Crash Course, Linear regression | `google-linear-regression.html` | linear regression은 feature를 바탕으로 label 값을 예측하는 통계적 방법 |
| IBM, What is Machine Learning? | `ibm-machine-learning.html` | ML은 training data의 pattern을 학습해 new data에 대한 inference, decision, prediction을 수행 |
| IBM, What is Machine Learning? | `ibm-machine-learning.html` | regression은 continuous values 예측, classification은 discrete values 예측으로 구분 |
| IBM, What is Generative AI? | `ibm-generative-ai.html` | generative AI는 data의 patterns and relationships를 encoding하고 new content로 응답 |
| Feuerriegel et al., Generative AI | `feuerriegel-2023-generative-ai.pdf` | generative AI를 training data에서 text, images, audio 같은 meaningful content를 생성하는 computational techniques로 설명 |

주의: 현재 로컬 환경에는 `pdftotext`가 없어 Feuerriegel et al. PDF의 텍스트 추출은 수행하지 못했다. PDF 원문은 저장했고, arXiv 메타데이터와 웹 확인 결과를 보조 근거로 사용했다.

## 자료별 근거 판단

### Google, Classification

근거 위치:

- `google-classification.html` 3705행 부근: classification을 example이 어떤 class에 속하는지 예측하는 task로 설명한다.
- 같은 문단에서 binary classification과 multi-class classification을 구분한다.

본문 반영:

- 분류를 정해진 범주 후보 중 하나를 고르는 작업으로 설명했다.
- 스팸/정상, 고양이/개/새 예시를 자체 예시로 작성했다.

주의:

- classification도 prediction이라는 표현을 사용하므로, 본문에서는 "분류도 넓은 의미에서는 예측"이라고 명시했다.

### Google, Linear regression

근거 위치:

- `google-linear-regression.html` 3610행 부근: linear regression을 feature를 바탕으로 label value를 predict하는 statistical method로 설명한다.
- 3615행 부근: feature와 label의 관계를 equation으로 표현한다고 설명한다.

본문 반영:

- 회귀(regression)를 연속적인 값(continuous value)을 예측하는 작업으로 설명했다.
- 집 가격 예시는 IBM 자료의 예시와도 부합하지만, 본문에서는 일반적 자체 예시로 구성했다.

주의:

- 10.1은 회귀 알고리즘 설명 절이 아니므로 수식과 gradient descent 설명은 제외했다.

### IBM, What is Machine Learning?

근거 위치:

- `ibm-machine-learning.html` 2610행 부근: ML은 training data의 pattern을 학습하고 new data에 대한 inference를 만든다고 설명한다.
- 2822행 부근: supervised learning은 classification 또는 regression처럼 external ground truth와 관련된 작업에 적용된다고 설명한다.
- 2853행 부근: regression은 continuous values, classification은 discrete values를 예측한다고 구분한다.

본문 반영:

- 예측을 넓은 표현으로 두고, 분류와 회귀를 그 안의 대표 작업으로 정리했다.
- 생성형 AI도 data, model, learning, inference, probability, representation의 흐름과 완전히 끊어지지 않는다고 설명했다.

주의:

- IBM 문서의 rule-based AI 예시는 10.1 본문에는 사용하지 않았다. 해당 논의는 앞 장의 도메인에 속한다.

### IBM, What is Generative AI?

근거 위치:

- `ibm-generative-ai.html` 2625행 부근: generative AI는 data의 patterns and relationships를 encoding하고 user request에 relevant new content로 응답한다고 설명한다.
- 2697행 부근: foundation model과 text, image, video, sound, music generation을 언급한다.
- 2699행 부근: training 결과가 parameters와 encoded representations가 되어 prompts에 대응해 content를 generate할 수 있다고 설명한다.

본문 반영:

- 생성을 조건에 맞는 새 산출물(output artifact)을 만드는 작업으로 설명했다.
- 텍스트 요약, 이미지 생성, 코드 변환 예시를 자체 예시로 작성했다.

주의:

- "autonomously" 같은 표현은 입문자에게 과장된 인상을 줄 수 있으므로 본문에서는 사용하지 않았다.
- 생성형 AI의 품질, 위험, RAG 등은 뒤 절과 뒤 장으로 넘겼다.

### Feuerriegel et al., Generative AI

근거 위치:

- arXiv 초록: generative AI를 training data에서 text, images, audio 같은 seemingly new, meaningful content를 generate할 수 있는 computational techniques로 설명한다.

본문 반영:

- 생성형 AI를 의미 있는 새 콘텐츠를 생성하는 계산 기법으로 보는 설명의 보조 근거로 사용했다.

주의:

- PDF 텍스트 추출을 하지 못했으므로 본문에서는 직접 인용하지 않았다.
- 논문의 정보시스템 관점, 사회기술 시스템 논의는 10.1 범위를 넘어가므로 반영하지 않았다.

## 일반화 문구

10.1에서는 다음 문구가 안전하다.

> 분류는 범주를 고르고, 예측은 값이나 상태를 추정하고, 생성은 조건에 맞는 새 산출물을 만든다. 세 작업은 모두 모델의 출력이라는 점에서 연결되지만, 출력의 성격이 다르다.

생성형 AI의 위치는 다음처럼 설명한다.

> 생성형 AI는 기존 머신러닝과 완전히 끊어진 기술이 아니다. 다만 사용자가 체감하는 출력이 범주나 숫자 하나가 아니라 문장, 이미지, 코드, 오디오 같은 새 산출물로 확장되었기 때문에 사용 경험과 위험이 달라진다.

## 도메인 경계

10.1에서 다룬다:

- 분류, 예측, 생성의 출력 차이
- 같은 입력이 문제 정의에 따라 다른 작업이 되는 예시
- 생성형 AI가 기존 ML과 연결되지만 출력의 성격이 다르다는 관점

10.1에서 깊게 다루지 않는다:

- next-token prediction의 세부 구조
- sampling, temperature, top-k, top-p
- diffusion model의 작동 방식
- LLM의 tokenizer, embedding, Transformer 구조
- 생성 결과 평가 지표의 세부
