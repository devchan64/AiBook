# 한국어 개념사전 인덱스

이 파일은 한국어 표면형, 동의어 후보, 혼동 가능한 표현을 `docs/reference/concept-glossary-terms/`의 단어별 원고으로 연결하는 보조 인덱스다.

정의는 이 파일에 중복 작성하지 않는다. 대표 정의는 단어별 원고 파일과 해당 `중심 Section`을 기준으로 확인한다.

일반 사전적 의미와 원고 안의 의미가 분리되어 쓰이는 표현은 `비고`에 `표제 관리 제외 검토` 또는 `표제 통일 관리 검토`를 표시한다. 제외 검토 대상은 독립 표제어보다 대표 항목의 하위 설명이나 본문 문맥으로 돌릴 후보이고, 통일 관리 검토 대상은 일반화된 학술·기술 표현을 확인해 대표 표제어를 맞출 후보다. 세부 판정 근거는 `korean-general-expression-review.md`를 기준으로 본다.

| 인덱스 표기 | 대표 표제어 | 영어 기준 용어 | 중심 Section | 파일 slug | 앵커 | 검증 레퍼런스 | 비고 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 결정적 | 결정적 | deterministic | P1-3.1 | deterministic | deterministic | AIMA, SEP AI | 같은 조건에서 결과가 하나로 닫히는 성질 |
| 경로 | 경로 | route, path | P1-7.1 | route | route | Poole & Mackworth search as path | PATH 환경 변수와 구분되는 탐색·계획의 이동 흐름 |
| 계획 | 계획 | planning | P1-7.4 | planning | planning | Poole & Mackworth search, motion planning survey | 목표에 도달하기 위한 행동·경로 선택 과정 |
| 검색 | 검색 | retrieval | P1-13.3 | retrieval | retrieval | RAG paper | RAG에서 생성 입력에 넣을 외부 문서 후보를 찾아오는 단계 |
| 검색 인덱스 | 검색 인덱스 | search index | P1-13.4 | search-index | search-index | ANN, vector search context | 많은 벡터나 문서를 빠르게 찾기 위해 미리 만든 검색 구조 |
| 검색 질의 | 검색 질의 | search query | P4-12.1 | search-query | search-query | 단어별 원고 기준 | 검색과 k-NN에서 저장된 기준 사례와 비교할 새 입력 기준 |
| 그룹 분할 | 그룹 분할 | group split | P3-9.13 | group-split | group-split | scikit-learn grouped cross-validation, P3-9.13 source context | 같은 개체나 그룹이 학습 쪽과 검증·테스트 쪽에 동시에 섞이지 않도록 나누는 방식 |
| 기준 모델 | 기준 모델 | baseline model | P4-8.2 | baseline-model | baseline-model | P4-8.2 source context | 후보 모델이 넘어야 할 가장 단순한 비교용 모델이나 점수 기준 |
| 기준선 | 기준선 | baseline | P3-7.3 | baseline | baseline | BLS base period, NCI baseline context | 현재 값이나 모델 점수를 단독으로 읽지 않기 위해 두는 참조 기준 |
| 혼동 행렬 | 혼동 행렬 | confusion matrix | P4-6.1 | confusion-matrix | confusion-matrix | P4-6.1 source context | 실제 라벨과 예측 라벨의 조합으로 분류 오류 방향을 읽는 표 |
| 군집 | 군집 | cluster | P1-8.2 | cluster | cluster | P1-8.2 source context | 알고리즘이 찾은 묶음이며 지도학습 라벨과 구분 |
| k-평균 | k-평균 | k-means | P1-8.2 | k-means | k-means | P1-8.2 source context | k개의 중심점을 반복 갱신하는 군집화 알고리즘 |
| 강화학습 환경 | 강화학습 환경 | reinforcement learning environment | P1-8.3 | reinforcement-learning-environment | reinforcement-learning-environment | 단어별 원고 기준 | 강화학습 에이전트가 행동하고 상태 변화와 보상을 돌려받는 상호작용 대상 |
| 근사 검색 | 근사 검색 | approximate search | P1-13.4 | approximate-search | approximate-search | ANN context | 충분히 가까운 후보를 빠르게 찾는 검색 절충 |
| 근사 최근접 이웃 | 근사 최근접 이웃 | approximate nearest neighbor, ANN | P1-13.4 | ann-approximate-nearest-neighbor | ann-approximate-nearest-neighbor | vector search context | 정확한 최근접보다 빠른 후보 탐색을 우선하는 방식 |
| 규칙 기반 접근 | 규칙 기반 접근 | rule-based approach | P1-2.1 | rule-based-approach | rule-based-approach | SEP logic and AI, AIMA | 규칙 기반 시스템보다 넓은 접근 층위 |
| 궤적 | 궤적 | trajectory | P1-7.4 | trajectory | trajectory | motion planning survey | 시간·속도까지 포함한 실행 직전 움직임 계획 |
| 딥 강화학습 | 딥 강화학습 | deep reinforcement learning | P1-8.3 | deep-reinforcement-learning | deep-reinforcement-learning | P1-8.3 source context | 딥러닝을 함수 근사 도구로 쓰는 강화학습 접근 |
| 라벨이 있는 예시 | 라벨이 있는 예시 | labeled example | P1-8.1 | labeled-example | labeled-example | P1-8.1 source context | 입력과 정답 라벨이 함께 묶인 지도학습 사례 |
| 라벨 일관성 | 라벨 일관성 | label consistency | P3-9.6 | label-consistency | label-consistency | P3-9.6 source context | 같은 사건이나 비슷한 조건에 같은 의미의 라벨이 반복해서 붙는 정도 |
| 라벨 예측 | 라벨 예측 | label prediction | P3-9.1 | label-prediction | label-prediction | P3-9.1 source context | 안정된 목표 라벨을 맞히도록 문제를 올리는 더 강한 문제 설정 |
| 밀도 | 밀도 | density | P1-8.2 | density | density | P1-8.2 source context | 데이터 공간에서 사례들이 촘촘히 모인 정도 |
| 문맥 의존성 | 문맥 의존성 | context dependency | P1-10.2 | context-dependency | context-dependency | P1-10.2 source context | 현재 출력 후보가 앞선 입력과 생성 내용에 따라 달라지는 성질 |
| 메타데이터 | 메타데이터 | metadata | P1-13.4 | metadata | metadata | 단어별 원고 기준 | 문서·검색 맥락의 부가 정보로 관리; 일반 사전 의미와 구분 |
| 모션 플래닝 | 모션 플래닝 | motion planning | P1-7.4 | motion-planning | motion-planning | Motion Planning for Autonomous Driving survey | 실행 가능한 움직임 후보를 만들고 평가하는 계획 문제 |
| 모델링 과제 | 모델링 과제 | modeling task | P1-4.4 | modeling-task | modeling-task | Google ML Glossary task | 현실 목표를 입력·출력 계산 문제로 좁힌 형태 |
| 범주 | 범주 | category | P1-8.1 | category | category | P1-8.1 source context | 분류 문제에서 사례를 넣을 후보 그룹 |
| RLHF | RLHF | reinforcement learning from human feedback | P1-8.3 | rlhf-reinforcement-learning-from-human-feedback | rlhf-reinforcement-learning-from-human-feedback | P1-8.3 source context | 사람 피드백을 보상 신호처럼 쓰는 LLM 조정 접근 |
| 수작업 특징 | 수작업 특징 | hand-crafted features | P1-9.1 | hand-crafted-features | hand-crafted-features | face recognition survey, representation learning review | 사람이 미리 설계한 입력 단서 |
| 알고리즘 | 알고리즘 | algorithm | P4-3.1 | algorithm | algorithm | AIMA, P4-3.1 source context | 문제를 풀기 위해 정해진 순서대로 수행하는 절차 |
| 순차 모델링 | 순차 모델링 | sequence modeling | P1-9.3 | sequence-modeling | sequence-modeling | Seq2Seq, Attention, Transformer papers | 순서 있는 데이터의 관계와 생성을 다루는 문제 설정 |
| 손실 | 손실 | loss | P1-5.1 | loss | loss | Google ML Glossary loss | 학습 목표와 현재 출력의 차이를 나타내는 신호 |
| 순전파 | 순전파 | forward pass | P1-5.2 | forward-pass | forward-pass | P1-5.2 source context | 입력이 학습된 파라미터를 지나 출력으로 계산되는 방향 |
| 업무 성과 | 업무 성과 | business outcome | P1-4.4 | business-outcome | business-outcome | scikit-learn model evaluation context | 모델 점수 바깥의 실제 업무 결과 |
| 엡실론 그리디 정책 | 엡실론 그리디 정책 | epsilon-greedy policy | P1-8.3 | epsilon-greedy-policy | epsilon-greedy-policy | P1-8.3 source context | 대부분 활용하되 작은 확률로 탐험하는 정책 |
| 엔드투엔드 학습 | 엔드투엔드 학습 | end-to-end learning | P1-9.2 | end-to-end-learning | end-to-end-learning | object detection context | 입력에서 최종 출력까지 연결된 구조를 함께 학습하는 접근 |
| 언어 모델링 | 언어 모델링 | language modeling | P1-9.3 | language-modeling | language-modeling | Bengio neural probabilistic language model | 단어·토큰 순서의 확률을 다루는 LLM 직접 계보의 문제 설정 |
| 원천데이터 | 원천데이터 | source data | P3-1.1 | source-data | source-data | P3-1.1 source context | 분석이나 학습 문제로 다시 구성하기 전의 출발 기록 |
| 개입 피드백 | 개입 피드백 | intervention feedback | P3-8.7 | intervention-feedback | intervention-feedback | P3-8.7 source context | 검토 규칙이나 운영 조치가 후속 데이터와 라벨을 바꾸는 되먹임 구조 |
| 결측값 | 결측값 | missing value | P3-5.5 | missing-value | missing-value | P3-5.5 source context | 있어야 할 위치에 관측값이나 기록값이 비어 있는 상태 |
| 예측 계약 | 예측 계약 | prediction contract | P3-9.7 | prediction-contract | prediction-contract | P3-9.7 source context | 입력 정의, 결과 정의, 시점 가용성, 재현 가능성을 함께 닫는 예측 문제 약속 |
| 오류 누적 | 오류 누적 | error accumulation | P1-10.2 | error-accumulation | error-accumulation | P1-10.2 source context | 앞 단계 오류가 뒤 생성 조건으로 남아 결과를 흔드는 현상 |
| 오류 비용 | 오류 비용 | error cost | P3-9.12 | error-cost | error-cost | Google ML Glossary thresholding, P3-9.12 source context | 오류 종류별 실제 부담을 다르게 두고 임계값과 판단 방향을 읽는 기준 |
| 거짓 음성 | 거짓 음성 | false negative | P3-9.12 | false-negative | false-negative | Google ML Glossary false negative, P3-9.12 source context | 실제로는 양성인데 모델이나 규칙이 음성으로 판단해 놓친 사례 |
| 거짓 양성 | 거짓 양성 | false positive | P3-9.12 | false-positive | false-positive | Google ML Glossary false positive, P3-9.12 source context | 실제로는 음성인데 모델이나 규칙이 양성으로 판단해 잘못 올린 사례 |
| 응답 생성 | 응답 생성 | response generation | P1-5.2 | response-generation | response-generation | Google ML Glossary inference LLM context | LLM이 프롬프트를 바탕으로 자연어 응답을 만드는 실행 |
| 의사결정 | 의사결정 | decision | P1-6.3 | decision | decision | P1-6.3 source context | 모델 숫자와 비용·정책을 함께 보고 실제 행동을 정하는 단계 |
| 원-핫 표현 | 원-핫 표현 | one-hot representation | P1-11.1 | one-hot-representation | one-hot-representation | P1-11.1 source context | 항목 위치 한 칸만 1로 켜는 희소한 식별 표현 |
| 이미지 인식 | 이미지 인식 | image recognition | P1-9.1 | image-recognition | image-recognition | LeCun deep learning review, face recognition survey | 이미지에서 의미 있는 시각 범주를 예측하는 문제 |
| 자기회귀 모델 | 자기회귀 모델 | autoregressive model | P1-9.2 | autoregressive-model | autoregressive-model | language modeling and sequence generation context | 앞 값에 조건부로 다음 값을 순서대로 예측·생성하는 모델 |
| 자동 프롬프트 최적화 | 자동 프롬프트 최적화 | automatic prompt optimization | P6-10.3 | automatic-prompt-optimization | automatic-prompt-optimization | 단어별 원고 기준 | 프롬프트 후보 생성·평가·선택을 자동 탐색 문제로 다루는 접근 |
| 모델 점수 | 모델 점수 | model score | P1-5.2 | model-score | model-score | Google ML Glossary score context | 후보 출력 비교와 임계값 판단에 쓰이는 모델 출력 수치 |
| 순위화 | 순위화 | ranking | P1-13.2 | ranking | ranking | P1-13.2 source context | 여러 후보를 점수나 우선순위 기준으로 줄 세우는 문제 유형 |
| 점 예측 | 점 예측 | point prediction | P1-6.3 | point-prediction | point-prediction | P1-6.3 source context | 불확실성 범위 없이 하나의 대표 숫자만 제시하는 예측 |
| 조밀한 벡터 | 조밀한 벡터 | dense vector | P1-11.1 | dense-vector | dense-vector | P1-11.1 source context | 대부분의 차원이 실제 값을 가지는 임베딩식 벡터 표현 |
| 중심점 | 중심점 | centroid | P1-8.2 | centroid | centroid | P1-8.2 source context | 군집을 대표하는 평균 위치 |
| 주성분 분석 | 주성분 분석 | principal component analysis, PCA | P1-8.2 | principal-component-analysis-pca | principal-component-analysis-pca | P1-8.2 source context | 분산이 큰 방향을 찾는 차원 축소 방법 |
| 지연 보상 | 지연 보상 | delayed reward | P1-8.3 | delayed-reward | delayed-reward | P1-8.3 source context | 행동의 결과가 여러 단계 뒤 보상으로 드러나는 상황 |
| 정보 무결성 | 정보 무결성 | information integrity | P1-10.3 | information-integrity | information-integrity | NIST GenAI Profile | 정보가 사실과 맥락을 왜곡하지 않고 신뢰 가능한 상태 |
| 시간 순서 분할 | 시간 순서 분할 | time split | P3-9.13 | time-split | time-split | FPP3 time series cross-validation, P3-9.13 source context | 시간 순서가 중요한 문제에서 과거 구간과 이후 구간을 섞지 않고 평가하는 분할 방식 |
| 통계적 언어 모델 | 통계적 언어 모델 | statistical language model | P1-11.1 | statistical-language-model | statistical-language-model | P1-11.1 source context | 빈도와 조건부 확률로 다음 표현 가능성을 추정하는 언어 모델 |
| 통계적 추론 | 통계적 추론 | statistical inference | P1-5.3 | statistical-inference | statistical-inference | OpenStax Introductory Statistics | 표본에서 모집단과 불확실성을 다루는 통계 절차 |
| 마스크드 언어 모델 | 마스크드 언어 모델 | masked language model | P1-11.3 | masked-language-model | masked-language-model | P1-11.3 source context | 문장 일부를 가리고 주변 문맥으로 맞히는 사전학습 방식 |
| 문맥 내 학습 | 문맥 내 학습 | in-context learning | P1-12.1 | in-context-learning | in-context-learning | GPT-3 paper | 모델 가중치 업데이트 없이 현재 입력 문맥으로 출력 행동이 달라지는 현상 |
| 맥락 | 맥락 | context | P1-12.1 | context | context | prompt engineering context | 작업에 필요한 배경·자료·앞선 결정을 제공하는 입력 요소 |
| 벡터 검색 | 벡터 검색 | vector search | P1-13.4 | vector-search | vector-search | vector search implementation context | 임베딩 벡터 공간에서 가까운 후보를 찾는 검색 방식 |
| 벡터 데이터베이스 | 벡터 데이터베이스 | vector database | P6-12.1 | vector-database | vector-database | vector database context | 벡터 저장, 인덱스, 메타데이터, 필터링을 함께 다루는 시스템 |
| 프록시 라벨 | 프록시 라벨 | proxy label | P1-8.1 | proxy-label | proxy-label | P1-8.1 source context | 직접 목표를 대신하는 대리 라벨 |
| 프롬프트 | 프롬프트 | prompt | P1-12.1 | prompt | prompt | OpenAI prompt engineering, GPT-3 paper | 현재 응답 조건을 담은 입력 전체 |
| 프롬프트 구조화 | 프롬프트 구조화 | prompt structuring | P1-12.2 | prompt-structuring | prompt-structuring | prompt engineering context | 입력 안의 역할을 나눠 쓰는 방식 |
| 프롬프트의 한계 | 프롬프트의 한계 | limit of prompting | P1-12.3 | limit-of-prompting | limit-of-prompting | P1-12.3 source context | 입력을 잘 써도 자동으로 해결되지 않는 문제 |
| 사전학습 LLM | 사전학습 LLM | pretrained LLM | P1-11.3 | pretrained-llm | pretrained-llm | P1-11.3 source context | 대규모 일반 학습을 먼저 마친 대규모 언어 모델 |
| 사실성 | 사실성 | factuality | P1-12.3 | factuality | factuality | NIST GenAI Profile | 문장이 실제 사실과 맞는지 보는 기준 |
| 유사도 검색 | 유사도 검색 | similarity search | P1-13.2 | similarity-search | similarity-search | information retrieval context | 질문 벡터와 가까운 문서 벡터 후보를 찾는 과정 |
| 재현율 | 재현율 | recall | P1-13.4 | recall | recall | IR evaluation context | 찾아야 할 관련 후보 중 실제로 찾아낸 비율 |
| 정밀도 | 정밀도 | precision | P1-13.4 | precision | precision | IR evaluation context | 가져온 후보 중 실제로 관련 있는 후보의 비율 |
| 정확 검색 | 정확 검색 | exact search | P1-13.4 | exact-search | exact-search | vector search context | 가장 가까운 후보를 정확히 찾기 위해 충분히 비교하는 방식 |
| 정보 검색 | 정보 검색 | information retrieval | P1-13.3 | information-retrieval | information-retrieval | IR textbook, RAG context | 질문에 맞는 문서·문단·근거 후보를 찾아오는 문제 |
| 회귀 | 회귀 | regression | P1-8.1 | regression | regression | P1-8.1 source context | 입력을 바탕으로 연속적인 수치 값이나 점수를 예측하는 모델링 과제 |
| 학습 | 학습 | learning | P1-5.1 | learning | learning | Deep Learning Book, Mitchell definition | 경험 이후 과제 성능이 개선되는 넓은 개념 |
| 학습 기반 접근 | 학습 기반 접근 | learning-based approach | P4-1.2 | learning-based-approach | learning-based-approach | P4-1.2 source context | 사례 데이터에서 입력과 출력의 관계를 맞추어 판단 기준을 만드는 접근 |
| 학습된 표현 | 학습된 표현 | learned representation | P1-9.1 | learned-representation | learned-representation | representation learning review | 모델이 과제에 맞게 데이터에서 배운 내부 표현 |
| 표현 학습 | 표현 학습 | representation learning | P1-3.3 | representation-learning | representation-learning | representation learning review | 모델이 과제에 유용한 내부 표현을 데이터에서 함께 배우는 접근 |
| 합성곱 신경망 | 합성곱 신경망 | CNN, convolutional neural network | P1-9.1 | cnn-convolutional-neural-network | cnn-convolutional-neural-network | LeCun deep learning review | 이미지의 지역 패턴을 계층적으로 다루는 신경망 구조 |
| 알렉스넷 | 알렉스넷 | AlexNet | P1-9.1 | alexnet | alexnet | AlexNet paper | 대규모 이미지 인식에서 딥러닝 확산을 각인시킨 전환점 사례 |
| 객체 검출 | 객체 검출 | object detection | P1-9.2 | object-detection | object-detection | object detection context | 이미지 안의 물체 범주와 위치를 함께 예측하는 문제 |
| 음성 생성 | 음성 생성 | speech generation | P1-9.2 | speech-generation | speech-generation | sequence generation context | 시간 순서의 오디오 신호를 만드는 생성 문제 |
| 텍스트 음성 변환 | 텍스트 음성 변환 | TTS, text-to-speech | P1-9.2 | tts-text-to-speech | tts-text-to-speech | Deep Voice paper | 텍스트 입력을 음성 출력으로 바꾸는 응용 문제 |
| 위험 | 위험 | risk | P1-10.3 | risk | risk | NIST GenAI Profile | 생성 결과나 AI 사용이 피해로 이어질 가능성 |
| 확률적 예측 | 확률적 예측 | probabilistic prediction | P1-6.3 | probabilistic-prediction | probabilistic-prediction | Google ML Glossary probabilistic regression model | 가능한 결과의 범위나 가능성을 함께 표현하는 예측 |
| 확률적 선택 | 확률적 선택 | probabilistic choice | P1-10.2 | probabilistic-choice | probabilistic-choice | P1-10.2 source context | 후보 분포에서 실제 출력 하나를 선택하는 과정 |
| 키워드 검색 | 키워드 검색 | keyword search | P1-13.2 | keyword-search | keyword-search | information retrieval context | 단어나 구문 일치를 기준으로 후보를 찾는 검색 방식 |
| 평가 설계 | 평가 설계 | evaluation design | P3-9.13 | evaluation-design | evaluation-design | P3-9.13 source context | 문제 구조에 맞는 데이터 분할, 지표, 비교 조건을 정하는 평가 기준 설계 |
| 논리적 추론 | 논리적 추론 | reasoning | P1-5.3 | reasoning | reasoning | P1-5.3 source context | 모델 실행과 구분해야 하는 논리적 사고 과정 |
| 근거성 | 근거 | evidence | P1-12.3 | evidence | evidence | P1-12.3 source context | 주장을 뒷받침하는 출처나 확인 근거가 있는지 보는 기준 |
| 평가 데이터 | 평가 데이터 | evaluation data | P4-4.1 | evaluation-data | evaluation-data | P4-4.1 source context | 모델 학습에 직접 쓰지 않고 학습된 모델의 동작을 확인하기 위해 따로 남겨 둔 데이터 |
| 재현성 | 재현성 | reproducibility | P2-7.5 | reproducibility | reproducibility | reproducible workflow context | 무엇을 바꿨고 결과가 어땠는지 다시 확인할 수 있는 성질 |
| RAG | 검색 증강 생성 | retrieval-augmented generation | P1-13.3 | retrieval-augmented-generation-rag | retrieval-augmented-generation-rag | RAG paper | 검색한 외부 자료를 생성 입력에 붙이는 구조 |
| AI 앱 | AI 앱 | AI application | P1-14.1 | ai-application | ai-application | P1-14.1 source context | 일반 앱이 아니라 모델·도구·데이터를 묶어 사용자가 만나는 AI 서비스 표면 |
| 외부 도구 | 외부 도구 | external tool | P1-14.1 | external-tool | external-tool | P1-14.1 source context | 모델이나 AI 앱이 연결해 쓰는 모델 밖 실행 기능 |
| 오케스트레이션 | 오케스트레이션 | orchestration | P1-14.1 | orchestration | orchestration | P1-14.1 source context | 모델, 데이터, 도구, 앱을 순서와 조건으로 연결하는 제어 층 |
| 도구 사용 | 도구 사용 | tool use | P1-14.2 | tool-use | tool-use | P1-14.2 source context | 외부 시스템 기능을 호출해 조회·실행·상태 변경을 일으키는 구조 |
| 외부 시스템 | 외부 시스템 | external system | P1-14.2 | external-system | external-system | P1-14.2 source context | 도구 사용으로 연결되는 바깥 서비스·파일·데이터베이스·API |
| 권한 | 권한 | permission | P7-6.2 | permission | permission | P1-14.2 source context | 실행 가능한 범위와 접근 한계를 미리 정한 통제 장치 |
| AI 에이전트 | AI 에이전트 | AI agent | P1-14.3 | ai-agent | ai-agent | P1-14.3 source context | 목표, 상태, 관찰, 행동을 이어 가며 작업을 수행하는 AI 시스템 문맥의 실행 구조 |
| 상태 표현 | 상태 표현 | state | P1-7.1 | state | state | P1-14.3 source context | 다음 행동 판단에 쓰는 현재 상황 정보의 요약 표현 |
| 에이전트 행동 | 에이전트 행동 | action | P1-8.3 | action | action | P1-14.3 source context | AI 에이전트나 강화학습 에이전트가 상태를 바꾸기 위해 선택하는 실행 단위 |
| 관찰 결과 | 관찰 결과 | observation | P1-14.3 | observation | observation | P1-14.3 source context | 행동 뒤 돌아와 다음 판단에 쓰는 새 정보나 결과 |
| MCP | 모델 컨텍스트 프로토콜 | Model Context Protocol | P1-14.4 | model-context-protocol-mcp | model-context-protocol-mcp | MCP specification context | AI 앱과 외부 도구·리소스·프롬프트 연결을 표준화하려는 프로토콜 |
| 외부 리소스 | 외부 리소스 | external resource | P1-14.4 | external-resource | external-resource | P1-14.4 source context | 모델이나 앱이 읽는 외부 맥락 데이터 |
| 신뢰 경계 | 신뢰 경계 | trust boundary | P1-14.4 | trust-boundary | trust-boundary | P1-14.4 source context | 믿을 수 있는 영역과 검증해야 하는 영역을 나누는 경계 |
| 소프트웨어 회귀 | 소프트웨어 회귀 | software regression | P1-14.5 | software-regression | software-regression | P1-14.5 source context | 변경 뒤 이전에는 되던 기능이나 품질이 나빠지는 현상 |
| 가드레일 | 가드레일 | guardrail | P1-14.5 | guardrail | guardrail | P1-14.5 source context | 허용 범위를 벗어난 입력·출력·실행을 막는 제한과 점검 장치 |
| 서비스 운영 | 서비스 운영 | service operation | P1-14.6 | service-operation | service-operation | P1-14.6 source context | AI 서비스를 반복 사용 속에서 비용·오류·속도·품질까지 관리하는 일 |
| AI 윤리 | AI 윤리 | AI ethics | P1-15.1 | ai-ethics | ai-ethics | NIST AI RMF, OECD AI Principles | AI 시스템의 사회적 위험과 책임 구조를 다루는 기준 |
| 편향 | 편향 | bias | P1-15.1 | bias | bias | NIST AI RMF, fairness context | 특정 사람·집단·상황에 반복적으로 불리한 결과가 몰리는 문제 |
| 안전성 | 안전성 | safety | P1-15.1 | safety | safety | NIST AI RMF | AI 결과나 자동화가 실제 피해로 이어지지 않게 제한하는 조건 |
| 책임 | 책임 | accountability | P1-15.1 | accountability | accountability | OECD AI Principles, NIST AI RMF | 문제 발생 시 누가 검토·설명·수정할지 남기는 원칙 |
| 투명성 | 투명성 | transparency | P1-15.1 | transparency | transparency | OECD AI Principles, NIST AI RMF | AI 사용 여부, 목적, 한계, 근거를 알 수 있게 드러내는 성질 |
| 인간 감독 | 인간 감독 | human oversight | P1-15.1 | human-oversight | human-oversight | AI governance context | 사람이 실제로 멈추고 수정하고 다시 판단할 수 있는 구조 |
| 저작권 | 저작권 | copyright | P1-15.2 | copyright | copyright | Korean Copyright Act | 창작적 표현의 복제·배포·수정 조건을 다루는 권리 |
| 인용 | 인용 | quotation | P1-15.2 | quotation | quotation | Korean Copyright Act Article 28 context | 필요한 범위의 외부 표현 일부를 출처와 함께 쓰는 방식 |
| 저작권의 표현 | 저작권의 표현 | protected expression | P1-15.2 | protected-expression | protected-expression | copyright expression/idea distinction | 아이디어·사실과 구분되는 구체적 창작 표현 |
| 출처 표시 | 출처 표시 | attribution | P1-15.2 | attribution | attribution | Korean Copyright Act Article 37 context | 외부 자료의 저자·기관·제목·URL·확인 날짜를 남기는 일 |
| 라이선스 | 라이선스 | license | P1-15.2 | license | license | copyright licensing context | 자료 사용 조건과 허락 범위를 정한 규칙 |
| 사실 | 사실 | fact | P1-10.3 | fact | fact | information integrity context | 참거짓을 확인할 수 있는 현실 주장 |
| 학습 데이터 | 학습 데이터 | training data | P1-15.2 | training-data | training-data | P1-15.2, P2-15.2 source context | 모델이 패턴이나 규칙을 배우는 데 직접 사용하는 데이터 |
| 권리자 | 권리자 | rightsholder | P1-15.2 | rightsholder | rightsholder | copyright rightsholder context | 저작물이나 자료의 이용 권리를 가진 사람이나 기관 |
| 공정 이용 | 공정 이용 | fair use | P1-15.2 | fair-use | fair-use | U.S. Copyright Office AI reports | 저작물의 제한적 이용 가능성을 여러 요소로 보는 법적 개념 |
| 변형적 이용 | 변형적 이용 | transformative use | P1-15.2 | transformative-use | transformative-use | fair use context | 원저작물을 새로운 목적이나 성격으로 바꾸어 쓰는 이용 주장 |
| 텍스트·데이터 마이닝 | 텍스트·데이터 마이닝 | text and data mining | P1-15.2 | text-and-data-mining | text-and-data-mining | TDM policy context | 많은 텍스트나 데이터를 분석해 패턴을 찾는 처리 방식 |
| 시장 대체 | 시장 대체 | market substitution | P1-15.2 | market-substitution | market-substitution | copyright market effect context | 이용이나 출력이 원저작물의 수요를 대신할 수 있는 위험 |
| 보안 | 보안 | security | P1-15.3 | security | security | OWASP LLM Top 10 | 입력, 출력, 권한, 도구, 데이터 경로를 악용에서 보호하는 조건 |
| 개인정보 | 개인정보 | privacy | P1-15.3 | privacy | privacy | privacy/security context | 개인을 식별하거나 추적할 수 있는 정보와 보호 요구 |
| 프롬프트 인젝션 | 프롬프트 인젝션 | prompt injection | P1-15.3 | prompt-injection | prompt-injection | OWASP LLM Top 10 | 입력이나 외부 문서의 숨은 지시가 AI 행동을 바꾸는 공격 |
| 최소 권한 | 최소 권한 | least privilege | P1-15.3 | least-privilege | least-privilege | security principle context | 필요한 범위까지만 접근 권한을 여는 보안 원칙 |
| 민감 정보 | 민감 정보 | sensitive information | P1-15.3 | sensitive-information | sensitive-information | privacy/security context | 노출되면 개인·조직·보안에 피해를 줄 수 있는 정보 |
| 인증 정보 | 인증 정보 | credential | P1-15.3 | credential | credential | security credential context | 비밀번호, API 키, 토큰처럼 접근 권한으로 이어지는 증명 수단 |
| 비밀 정보 | 비밀 정보 | confidential information | P1-15.3 | confidential-information | confidential-information | security/confidentiality context | 외부 노출 시 조직·고객·운영에 피해를 줄 수 있는 내부 정보 |
| 과도한 권한 | 과도한 권한 | excessive agency | P1-15.3 | excessive-agency | excessive-agency | OWASP LLM agentic risk context | 현재 작업 목적보다 실행 권한과 자율성이 너무 넓은 상태 |
| 실행 범위 | 실행 범위 | scope | P1-15.3 | scope | scope | P1-16.3 source context | 현재 요청이나 자동화가 영향을 줄 수 있는 대상과 경계 |
| 시나리오 | 시나리오 | scenario | P1-17.1 | scenario | scenario | forecast scenario context | 확정 예측이 아니라 가능한 전개 경로를 조건별로 나누는 틀 |
| 지표 | 지표 | indicator | P1-17.1 | indicator | indicator | AI Index indicator context | 변화 방향을 보여 주는 수치나 관찰 신호 |
| 해석 경계 | 해석 경계 | interpretation boundary | P3-8.2 | interpretation-boundary | interpretation-boundary | P3-1.2 source context | 데이터나 비교 결과를 어디까지 말할 수 있는지 정하는 설명의 한계선 |
| 표본 | 표본 | sample | P2-5.3 | statistical-sample | statistical-sample | P2-5.3 source context | 모집단에서 실제로 관측한 일부 데이터 |
| 사실 주장 | 사실 주장 | factual claim | P1-17.3 | factual-claim | factual-claim | source verification context | 외부 자료와 근거로 확인되어야 하는 문장 |
| 예측 | 예측 | prediction | P1-10.1 | prediction | prediction | ML prediction/forecast distinction | 입력이나 현재 정보에서 다음 값·상태·사건을 추정하는 일 |
| 계산 언어 | 계산 언어 | calculation language | P2-1.1 | calculation-language | calculation-language | P2-1.1 source context | 데이터와 모델 계산 구조를 읽기 위한 수학적 표현 체계 |
| 압축 표기 | 압축 표기 | notation | P2-1.1 | notation | notation | P2-1.1 source context | 반복 계산과 관계를 짧은 기호 체계로 줄여 쓰는 방식 |
| 프로그램 코드 | 프로그램 코드 | program code | P2-1.2 | code | code | P2-1.2 source context | 컴퓨터가 실행할 계산 절차를 프로그래밍 언어로 적은 구조 |
| 변수 | 변수 | variable | P2-2.1 | variable | variable | P2-2.1 source context | 값을 가리키기 위해 붙인 이름 |
| 함수 | 함수 | function | P2-2.1 | function | function | P2-2.1 source context | 입력을 받아 출력으로 바꾸는 관계나 계산 단위 |
| 식 | 식 | expression | P2-2.1 | expression | expression | P2-2.1 source context | 값, 변수, 연산, 함수 호출을 조합한 계산 조각 |
| 극한 | 극한 | limit | P2-2.3 | limit | limit | P2-2.3 source context | 입력이 어떤 값에 가까워질 때 함수값의 경향을 보는 표기 |
| 변화율 | 변화율 | rate of change | P2-4.2 | rate-of-change | rate-of-change | P2-2.3 source context | 입력 변화량에 비해 출력이 얼마나 변하는지 보는 비율 |
| 로그 | 수학 로그 | logarithm | P2-2.4 | logarithm | logarithm | P2-2.4 source context | 지수 함수를 거꾸로 읽고 곱셈 관계를 더하기 관계로 바꾸는 함수 |
| 지수 함수 | 지수 함수 | exponential function | P2-2.4 | exponential-function | exponential-function | P2-2.4 source context | 입력이 지수 자리에 들어가 같은 비율의 변화를 표현하는 함수 |
| 로그 손실 | 로그 손실 | log loss | P2-2.4 | log-loss | log-loss | P2-2.4 source context | 정답 확률이 낮을수록 더 큰 벌점을 주는 손실 |
| 시그모이드 | 시그모이드 | sigmoid | P2-2.4 | sigmoid | sigmoid | P2-2.4 source context | 실수 점수를 0과 1 사이 값으로 바꾸는 S자 함수 |
| 소프트맥스 | 소프트맥스 | softmax | P2-2.4 | softmax | softmax | P2-2.4 source context | 여러 점수를 비교 가능한 비율 값으로 정규화하는 함수 |
| 선형대수 | 선형대수 | linear algebra | P2-3.1 | linear-algebra | linear-algebra | P2-3.1 source context | 스칼라·벡터·행렬과 그 계산을 다루는 기본 수학 언어 |
| 스칼라 | 스칼라 | scalar | P2-3.1 | scalar | scalar | P2-3.1 source context | 숫자 하나로 표현되는 값 |
| 벡터 | 벡터 | vector | P2-3.1 | vector | vector | P2-3.1 source context | 순서가 있는 여러 값을 한 묶음으로 담은 표현 |
| 행렬 | 행렬 | matrix | P2-3.1 | matrix | matrix | P2-3.1 source context | 행과 열 구조로 배열한 2차원 숫자 표현 |
| 벡터 공간 | 벡터 공간 | vector space | P2-3.2 | vector-space | vector-space | P2-3.2 source context | 벡터들이 놓이고 서로 비교되는 표현 공간 |
| 차원 | 차원 | dimension | P2-3.2 | dimension | dimension | P2-3.2 source context | 벡터가 가진 값의 개수 또는 좌표 축의 수 |
| 위상 | 위상 | topology | P2-3.2 | topology | topology | P2-3.2 source context | 공간의 가까움·연결·연속성 구조를 보는 추상 관점 |
| 매니폴드 | 매니폴드 | manifold | P2-3.2 | manifold | manifold | P2-3.2 source context | 데이터 표현들이 이루는 더 낮거나 부드러운 공간 구조 |
| 행렬 곱 | 행렬 곱 | matrix multiplication | P2-3.3 | matrix-multiplication | matrix-multiplication | P2-3.3 source context | 행과 열을 조합해 새 값을 만드는 계산 |
| 가중합 | 가중합 | weighted sum | P2-3.3 | weighted-sum | weighted-sum | P2-3.3 source context | 입력값마다 가중치를 곱한 뒤 더해 하나의 값을 만드는 계산 |
| 선형 변환 | 선형 변환 | linear transformation | P2-3.3 | linear-transformation | linear-transformation | P2-3.3 source context | 행렬 곱으로 벡터를 다른 표현 공간으로 옮기는 계산 |
| 거리 | 거리 | distance | P2-3.4 | distance | distance | P2-3.4 source context | 두 벡터가 표현 공간에서 얼마나 떨어져 있는지 보는 기준 |
| 유사도 | 유사도 | similarity | P2-3.4 | similarity | similarity | P2-3.4 source context | 두 벡터나 표현이 얼마나 닮았는지 보는 비교 기준 |
| 코사인 유사도 | 코사인 유사도 | cosine similarity | P2-3.4 | cosine-similarity | cosine-similarity | P2-3.4 source context | 두 벡터의 방향 유사성을 보는 기준 |
| 미분 | 미분 | derivative | P2-4.3 | derivative | derivative | P2-4.3 source context | 입력을 아주 조금 바꿨을 때 출력이 얼마나 변하는지 나타내는 순간 변화율 |
| 편미분 | 편미분 | partial derivative | P2-4.3 | partial-derivative | partial-derivative | P2-4.3 source context | 여러 입력 중 하나만 바꿨다고 보고 계산한 변화율 |
| 그래디언트 | 그래디언트 | gradient | P2-4.3 | gradient | gradient | P2-4.3 source context | 여러 편미분을 순서 있게 모은 변화율 벡터 |
| 벡터해석 | 벡터해석 | vector calculus | P2-4.5 | vector-calculus | vector-calculus | P2-4.5 source context | 벡터·공간·함수·변화율을 함께 다루는 수학 체계 |
| 역방향 패스 | 역방향 패스 | backward pass | P2-4.5 | backward-pass | backward-pass | P2-4.5 source context | 손실에서 거꾸로 각 계산 단계의 그래디언트를 계산하는 실행 방향 |
| 합성함수 | 합성함수 | composite function | P2-4.6 | composite-function | composite-function | P2-4.6 source context | 한 함수의 출력이 다음 함수의 입력으로 이어지는 함수 구조 |
| 연쇄 법칙 | 연쇄 법칙 | chain rule | P2-4.6 | chain-rule | chain-rule | P2-4.6 source context | 합성함수에서 단계별 변화율을 이어 읽는 미분 규칙 |
| 확률 | 확률 | probability | P2-5.1 | probability | probability | P2-5.1 source context | 불확실성을 0과 1 사이의 숫자로 표현하는 언어 |
| 불확실성 | 불확실성 | uncertainty | P1-6.2 | uncertainty | uncertainty | P2-5.1 source context | 현재 정보만으로 하나의 결과를 확정할 수 없는 상태 |
| 사건 | 사건 | event | P2-5.1 | event | event | P2-5.1 source context | 관심 있는 결과들을 묶은 집합 |
| 표본공간 | 표본공간 | sample space | P2-5.1 | sample-space | sample-space | P2-5.1 source context | 가능한 모든 결과를 모아 둔 전체 집합 |
| 베이즈 규칙 | 베이즈 규칙 | Bayes' rule | P2-5.1 | bayes-rule | bayes-rule | P2-5.1 source context | 새 증거로 가능성 판단을 갱신하는 확률 규칙 |
| 분포 | 분포 | distribution | P2-5.2 | distribution | distribution | P2-5.2 source context | 값들이 어디에 몰리고 얼마나 퍼져 있는지 보여 주는 전체 모양 |
| 데이터 분포 | 데이터 분포 | data distribution | P2-5.2 | data-distribution | data-distribution | P2-5.2 source context | 실제로 관측한 데이터 값들이 놓인 모양 |
| 데이터 모델링 | 데이터 모델링 | data modeling | P3-1.1 | data-modeling | data-modeling | P3-1.1 source context | 원천데이터를 질문에 답할 수 있는 샘플, 특징, 비교, 출력 구조로 다시 설계하는 과정 |
| 데이터과학 | 데이터과학 | data science | P3-1.1 | data-science | data-science | P3-1.1 source context | 데이터를 수집, 정리, 표현, 모델링, 해석해 질문과 의사결정에 연결하는 넓은 흐름 |
| 확률분포 | 확률분포 | probability distribution | P2-5.2 | probability-distribution | probability-distribution | P2-5.2 source context | 가능한 값이나 결과에 확률을 배정한 수학적 표현 |
| 평균 | 평균 | mean | P2-5.2 | mean | mean | P2-5.2 source context | 여러 값을 더한 뒤 개수로 나눈 대표 중심값 |
| 분산 | 분산 | variance | P2-5.2 | variance | variance | P2-5.2 source context | 값들이 평균 주변에서 얼마나 퍼져 있는지 나타내는 값 |
| 모집단 | 모집단 | population | P2-5.3 | population | population | P2-5.3 source context | 알고 싶어 하는 전체 대상 |
| 추정 | 추정 | estimation | P2-5.3 | estimation | estimation | P2-5.3 source context | 표본으로 모집단의 값이나 성질을 짐작하는 일 |
| 오차 | 오차 | error | P2-5.3 | error | error | P2-5.3 source context | 추정값이나 예측값과 실제 값 사이의 차이 |
| 표본 편향 | 표본 편향 | sampling bias | P2-5.3 | sampling-bias | sampling-bias | P2-5.3 source context | 표본이 모집단을 잘 대표하지 못하고 특정 방향으로 치우친 상태 |
| 선택적 라벨 | 선택적 라벨 | selective labels | P3-8.6 | selective-labels | selective-labels | KDD 2017 selective labels problem | 검토나 기존 의사결정 경로를 통과한 일부 사례에만 결과 라벨이 남아 있는 상태 |
| 테스트 데이터 | 테스트 데이터 | test data | P2-5.3 | test-data | test-data | P2-5.3 source context | 학습에 직접 쓰지 않고 모델 성능 확인을 위해 따로 둔 데이터 |
| 이상값 | 이상값 | outlier | P2-13.1 | outlier | outlier | P2-5.4 source context | 전체 값 흐름에서 유난히 멀리 떨어져 보이는 값 |
| 표준편차 | 표준편차 | standard deviation | P2-5.5 | standard-deviation | standard-deviation | P2-5.5 source context | 분산의 제곱근으로 퍼짐을 원래 단위에 가깝게 읽는 값 |
| 공분산 | 공분산 | covariance | P2-5.5 | covariance | covariance | P2-5.5 source context | 두 값이 함께 움직이는 방향을 보는 값 |
| 상관계수 | 상관계수 | correlation coefficient | P2-5.5 | correlation-coefficient | correlation-coefficient | P2-5.5 source context | 두 값의 함께 움직임을 비교하기 쉬운 눈금으로 나타낸 값 |
| 신뢰구간 | 신뢰구간 | confidence interval | P2-5.5 | confidence-interval | confidence-interval | P2-5.5 source context | 추정값을 어느 범위 안에서 함께 읽어야 하는지 보여 주는 방식 |
| 가설검정 | 가설검정 | hypothesis testing | P2-5.5 | hypothesis-testing | hypothesis-testing | P2-5.5 source context | 관측된 차이가 표본 우연만으로 설명될 수 있는지 따져 보는 절차 |
| 최적화 | 최적화 | optimization | P2-6.1 | optimization | optimization | P2-6.1 source context | 기준과 제약을 고려해 여러 후보 중 더 나은 값을 찾는 문제 |
| 롱 컨텍스트 | 롱 컨텍스트 | long-context | P6-4.5 | long-context | long-context | long-context design context | 긴 입력에서 중요한 정보를 유지하고 활용하는 설계 문제 |
| 문맥 창 | 문맥 창 | context window | P6-4.2 | context-window | context-window | P6-4.2 source context | 모델이 한 번의 입력-출력 계산 동안 함께 참고할 수 있는 최대 토큰 범위 |
| 멀티헤드 어텐션 | 멀티헤드 어텐션 | multi-head attention | P5-13.3 | multi-head-attention | multi-head-attention | Transformer context | 여러 attention head로 토큰 관계를 나누어 읽은 뒤 결과를 합치는 구조 |
| 위치 인코딩 | 위치 인코딩 | positional encoding | P1-11.3 | positional-encoding | positional-encoding | Transformer context | 토큰 의미 벡터와 별도로 공급하는 시퀀스 위치 정보 |
| 셀프 어텐션 | 셀프 어텐션 | self-attention | P5-13.2 | self-attention | self-attention | Transformer context | 같은 시퀀스 안의 토큰 관계를 계산해 각 토큰 표현을 갱신하는 attention 방식 |
| 다음 토큰 예측 | 다음 토큰 예측 | next-token prediction | P1-10.2 | next-token-prediction | next-token-prediction | LLM generation context | 현재 문맥에서 다음 토큰 후보를 계산하고 한 토큰씩 생성을 이어 가는 방식 |
| 샘플링 | 샘플링 | sampling | P5-15.3 | sampling | sampling | P5-15.3 source context | 후보 분포에서 실제 출력 조각 하나를 선택하는 절차 |
| Transformer | 트랜스포머 | Transformer | P1-11.3 | transformer | transformer | Attention Is All You Need | attention 기반으로 시퀀스 위치 관계를 비교하는 신경망 구조 계열 |
| 파라미터 | 파라미터 | parameter | P1-4.3 | parameter | parameter | P2-6.1 source context | 학습 과정에서 조정되는 모델 내부 값 |
| 손실 함수 | 손실 함수 | loss function | P2-6.2 | loss-function | loss-function | P2-6.2 source context | 예측의 틀림을 학습에 쓸 수 있는 숫자로 바꾸는 함수 |
| 목적 함수 | 목적 함수 | objective function | P2-6.2 | objective-function | objective-function | P2-6.2 source context | 학습이나 최적화가 실제로 줄이거나 키우려는 전체 기준 |
| 평균 제곱 오차 | 평균 제곱 오차 | mean squared error, MSE | P2-6.2 | mean-squared-error-mse | mean-squared-error-mse | P2-6.2 source context | 실제값과 예측값의 차이를 제곱한 뒤 여러 샘플에 대해 평균낸 값 |
| 평가 지표 | 평가 지표 | metric | P4-6.1 | metric | metric | P2-6.2 source context | 모델 결과를 사람이 해석하고 비교하기 위해 쓰는 성능 기준 |
| 검증 데이터 | 검증 데이터 | validation data | P2-6.2 | validation-data | validation-data | P2-6.2 source context | 학습 중 모델 설정을 확인하고 조정하는 데 쓰는 데이터 |
| 교차검증 | 교차검증 | cross-validation | P4-4.2 | cross-validation | cross-validation | scikit-learn Cross-validation, P4-4.2 source context | 주어진 데이터를 여러 번 나누어 서로 다른 검증 구간에서 모델이나 설정을 반복 평가하는 방법 |
| 경사하강법 | 경사하강법 | gradient descent | P2-6.3 | gradient-descent | gradient-descent | P2-6.3 source context | 손실을 낮추기 위해 파라미터를 조금씩 바꾸는 반복 최적화 방법 |
| 실행 환경 | 실행 환경 | runtime | P2-7.1 | runtime | runtime | Python runtime context | 코드가 실제로 실행되는 자리와 연결된 프로그램·패키지·설정 묶음 |
| 의존성 | 의존성 | dependency | P2-7.5 | dependency | dependency | Python Packaging User Guide | 코드 실행에 필요한 외부 패키지나 환경 조건 |
| 자료구조 | 자료구조 | data structure | P2-9.1 | data-structure | data-structure | P2-9.1 source context | 데이터를 조직하는 모양과 자주 수행할 연산을 함께 보는 기준 |
| 배열 | 배열 | array | P2-9.2 | array | array | P2-9.2 source context | 위치와 축을 기준으로 값을 읽는 구조 |
| 트리 | 트리 | tree | P2-9.2 | tree | tree | P2-9.2 source context | 부모와 자식의 계층 관계로 항목을 조직하는 구조 |
| 그래프 | 그래프 | graph | P2-9.3 | graph | graph | P2-9.3 source context | 대상을 노드로 두고 관계를 엣지로 연결한 구조 |
| 노트북, 계산 문서 | 노트북 | notebook | P2-10.1 | notebook | notebook | Jupyter docs, P2-10.1 source context | 코드, 설명, 출력이 함께 들어 있는 계산 문서 |
| 출력 | 출력 | output | P1-4.2 | output | output | 단어별 원고 기준 | 모델링에서 문제를 어떤 결과 형태로 풀지 드러내는 결과 설계 |
| 숨은 상태 | 숨은 상태 | hidden state | P1-11.2 | hidden-state | hidden-state | P1-11.2 source context | 순환 신경망에서 앞 입력 정보를 누적해 다음 계산으로 넘기는 내부 상태 |
| 브로드캐스팅 | 브로드캐스팅 | broadcasting | P2-11.3 | broadcasting | broadcasting | P2-11.3 source context | 작은 값이나 배열을 큰 배열의 shape에 맞춰 적용하는 계산 규칙 |
| 벡터화 | 벡터화 | vectorization | P2-11.3 | vectorization | vectorization | P2-11.3 source context | 반복 계산을 배열 연산 하나로 표현하는 방식 |
| 변수변환 | 변수변환 | variable transformation | P3-6.1 | variable-transformation | variable-transformation | P3-6.1 source context | 같은 구조나 값을 비교하기 쉬운 다른 표현으로 바꾸는 과정 |
| 토큰 | 토큰 | token | P6-2.1 | token | token | P6-2.1 source context | 모델이 텍스트를 처리하기 위해 나누는 기본 계산 단위 |
| 토큰화 | 토큰화 | tokenization | P6-2.2 | tokenization | tokenization | P3-6.2 source context | 원문이나 구간 구조를 모델이 읽을 수 있는 짧은 token 시퀀스로 바꾸는 과정 |
| 어휘 사전 | 어휘 사전 | vocabulary | P6-2.2 | vocabulary | vocabulary | P6-2.2 source context | tokenizer가 만들 수 있는 token 조각과 ID를 모아 둔 계산용 목록 |
| 청크 | 청크 | chunk | P1-13.1 | chunk | chunk | P1-13.1 source context | 긴 문서를 검색과 비교에 쓰기 좋은 작은 텍스트 단위로 나눈 묶음 |
| DataFrame | DataFrame | DataFrame | P2-12.1 | dataframe | dataframe | P2-12.1 source context | 행과 열 라벨이 붙은 2차원 표 형식 데이터 구조 |
| 데이터셋 | 데이터셋 | dataset | P2-12.3 | dataset | dataset | P2-12.3 source context | 학습이나 평가를 위해 정리한 샘플과 변수의 묶음 |
| 타깃 | 타깃 | target | P1-8.1 | target | target | P2-12.3 source context | 모델이 맞혀야 하는 정답 열 또는 목표 값 |
| 모델 출력 구조 | 모델 출력 구조 | model output structure | P3-2.2 | output-structure | output-structure | P3-1.1 source context | 계산 결과를 어떤 형식의 문제 결과로 내보낼지 정한 설계상의 결과 틀 |
| 실제 목표 | 실제 목표 | actual target | P3-9.9 | actual-target | actual-target | P3-9.9 source context | 정말 알고 싶고 최종적으로 줄이거나 맞히고 싶은 결과 |
| 대리 타깃 | 대리 타깃 | proxy target | P3-9.9 | proxy-target | proxy-target | Google ML Glossary proxy labels, P3-9.9 source context | 실제 목표를 바로 볼 수 없을 때 임시 목표처럼 사용하는 대체 열 |
| 확률 추정값 | 확률 추정값 | probability estimate | P1-7.3 | probability-estimate | probability-estimate | P1-7.3 source context | 확률처럼 읽고 싶은 모델 수치 출력이며 보정 여부를 따로 확인해야 하는 값 |
| 임계값 | 임계값 | threshold | P1-7.3 | threshold | threshold | P3-2.2 source context | 출력 숫자나 비교값을 실제 행동으로 바꿀 때 쓰는 절단 기준 |
| 정책 | 정책 | policy | P1-8.3 | policy | policy | P1-14.3 source context | 현재 상태나 관측에서 어떤 행동을 고를지 정하는 기준 또는 함수 |
| 검증 | 검증 | validation | P4-4.2 | validation | validation | P2-12.3 source context | 설정과 선택을 비교 점검하기 위한 중간 평가 데이터 또는 절차 |
| 데이터 누수 | 데이터 누수 | data leakage | P2-12.3 | data-leakage | data-leakage | P2-12.3 source context | 예측 시점에 알 수 없는 정보가 학습 과정에 미리 섞이는 문제 |
| 비교 가능성 | 비교 가능성 | comparability | P3-2.3 | comparability | comparability | P3-2.3 source context | 둘 이상의 값이나 샘플을 같은 기준 위에서 해석해도 되는 정도 |
| 전처리 | 전처리 | preprocessing | P4-7.2 | preprocessing | preprocessing | P2-12.3 source context | 모델에 넣기 전에 입력 표현을 계산 가능한 형태로 준비하는 과정 |
| 그래프(plot) | 그래프 | plot | P2-13.1 | plot | plot | P2-13.1 source context | 숫자나 표 데이터를 시각적 모양으로 바꾸어 보여 주는 그림 |
| 시각화 | 시각화 | visualization | P2-13.1 | visualization | visualization | P2-13.1 source context | 숫자나 표 데이터를 눈으로 비교 가능한 모양으로 바꾸어 확인하는 과정 |
| 손실 곡선 | 손실 곡선 | loss curve | P2-13.2 | loss-curve | loss-curve | P2-13.2 source context | 학습 반복에 따라 손실이 어떻게 변하는지 보여 주는 선 그래프 |
| 정확도 | 정확도 | accuracy | P2-13.3 | accuracy | accuracy | P2-13.3 source context | 전체 예측 중 맞춘 비율을 나타내는 성능 지표 |
| 버전 관리 | 버전 관리 | version control | P2-14.1 | version-control | version-control | P2-14.1 source context | 시간에 따라 바뀐 파일 상태와 이유를 다시 찾게 해 주는 기록 방식 |
| 문서 재현성 | 문서 재현성 | document reproducibility | P2-14.2 | document-reproducibility | document-reproducibility | P2-14.2 source context | 원고, 코드, 이미지, 설정을 맞춰 같은 문서 결과를 다시 만들 수 있는 성질 |
| 대조 학습 | 대조 학습 | contrastive learning | P6-3.3 | contrastive-learning | contrastive-learning | SimCLR, SBERT context | 가까워져야 할 쌍과 멀어져야 할 쌍으로 표현 공간 배치를 배우는 접근 |
