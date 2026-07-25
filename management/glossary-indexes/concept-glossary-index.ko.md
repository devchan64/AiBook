# 한국어 개념사전 인덱스

이 파일은 한국어 표면형, 동의어 후보, 혼동 가능한 표현을 `docs/reference/concept-glossary-terms/`의 단어별 원고으로 연결하는 보조 인덱스다.

정의는 이 파일에 중복 작성하지 않는다. 대표 정의는 단어별 원고 파일과 해당 `중심 Section`을 기준으로 확인한다.

| 인덱스 표기 | 대표 표제어 | 영어 기준 용어 | 중심 Section | 파일 slug | 앵커 | 검증 레퍼런스 | 비고 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 결정적 | 결정적 | deterministic | P1-3.1 | deterministic | deterministic | AIMA, SEP AI | 같은 조건에서 결과가 하나로 닫히는 성질 |
| 경로 | 경로 | route, path | P1-7.1 | route | route | Poole & Mackworth search as path | PATH 환경 변수와 구분되는 탐색·계획의 이동 흐름 |
| 계획 | 계획 | planning | P1-7.4 | planning | planning | Poole & Mackworth search, motion planning survey | 목표에 도달하기 위한 행동·경로 선택 과정 |
| 검색 | 검색 | retrieval | P1-13.3 | retrieval | retrieval | RAG paper | RAG에서 생성 입력에 넣을 외부 문서 후보를 찾아오는 단계 |
| 검색 인덱스 | 검색 인덱스 | search index | P1-13.4 | search-index | search-index | HNSW, FAISS context | 많은 벡터나 문서를 빠르게 찾기 위해 미리 만든 검색 구조 |
| 글로벌 플래너 | 글로벌 플래너 | global planner | P1-7.4 | global-planner | global-planner | autonomous driving planning context | 목적지까지의 큰 경로 흐름을 정하는 계획 층위 |
| 기대 출력 | 기대 출력 | expected output | P1-8.1 | expected-output | expected-output | P1-8.1 source context | 지도학습에서 입력에 대해 기대하는 정답 또는 목표 출력 |
| 군집 | 군집 | cluster | P1-8.2 | cluster | cluster | P1-8.2 source context | 알고리즘이 찾은 묶음이며 지도학습 라벨과 구분 |
| k-평균 | k-평균 | k-means | P1-8.2 | k-means | k-means | P1-8.2 source context | k개의 중심점을 반복 갱신하는 군집화 알고리즘 |
| 근사 검색 | 근사 검색 | approximate search | P1-13.4 | approximate-search | approximate-search | HNSW, ANN context | 충분히 가까운 후보를 빠르게 찾는 검색 절충 |
| 근사 최근접 이웃 | 근사 최근접 이웃 | approximate nearest neighbor, ANN | P1-13.4 | ann-approximate-nearest-neighbor | ann-approximate-nearest-neighbor | HNSW, FAISS context | 정확한 최근접보다 빠른 후보 탐색을 우선하는 방식 |
| 규칙 기반 접근 | 규칙 기반 접근 | rule-based approach | P1-2.1 | rule-based-approach | rule-based-approach | SEP logic and AI, AIMA | 규칙 기반 시스템보다 넓은 접근 층위 |
| 궤적 | 궤적 | trajectory | P1-7.4 | trajectory | trajectory | motion planning survey | 시간·속도까지 포함한 실행 직전 움직임 계획 |
| 누적 효과 | 누적 효과 | accumulation effect | P1-10.2 | accumulation-effect | accumulation-effect | P1-10.2 source context | 앞선 출력 선택이 뒤 생성 조건으로 계속 남는 현상 |
| 딥 강화학습 | 딥 강화학습 | deep reinforcement learning | P1-8.3 | deep-reinforcement-learning | deep-reinforcement-learning | P1-8.3 source context | 딥러닝을 함수 근사 도구로 쓰는 강화학습 접근 |
| 라벨이 있는 예시 | 라벨이 있는 예시 | labeled example | P1-8.1 | labeled-example | labeled-example | P1-8.1 source context | 입력과 정답 라벨이 함께 묶인 지도학습 사례 |
| 로컬 플래너 | 로컬 플래너 | local planner | P1-7.4 | local-planner | local-planner | autonomous driving planning context | 현재 상황에 맞는 짧은 궤적을 고르는 계획 층위 |
| 밀도 | 밀도 | density | P1-8.2 | density | density | P1-8.2 source context | 데이터 공간에서 사례들이 촘촘히 모인 정도 |
| 문맥 의존성 | 문맥 의존성 | context dependency | P1-10.2 | context-dependency | context-dependency | P1-10.2 source context | 현재 출력 후보가 앞선 입력과 생성 내용에 따라 달라지는 성질 |
| 모션 플래닝 | 모션 플래닝 | motion planning | P1-7.4 | motion-planning | motion-planning | Motion Planning for Autonomous Driving survey | 실행 가능한 움직임 후보를 만들고 평가하는 계획 문제 |
| 모델링 과제 | 모델링 과제 | modeling task | P1-4.4 | modeling-task | modeling-task | Google ML Glossary task | 현실 목표를 입력·출력 계산 문제로 좁힌 형태 |
| 바운딩 박스 | 바운딩 박스 | bounding box | P1-9.2 | bounding-box | bounding-box | YOLO paper | 객체 검출에서 물체 위치를 사각형으로 나타내는 출력 표현 |
| 범주 | 범주 | category | P1-8.1 | category | category | P1-8.1 source context | 분류 문제에서 사례를 넣을 후보 그룹 |
| RLHF | RLHF | reinforcement learning from human feedback | P1-8.3 | rlhf-reinforcement-learning-from-human-feedback | rlhf-reinforcement-learning-from-human-feedback | P1-8.3 source context | 사람 피드백을 보상 신호처럼 쓰는 LLM 조정 접근 |
| 수작업 특징 | 수작업 특징 | hand-crafted features | P1-9.1 | hand-crafted-features | hand-crafted-features | face recognition survey, representation learning review | 사람이 미리 설계한 입력 단서 |
| 순차 모델링 | 순차 모델링 | sequence modeling | P1-9.3 | sequence-modeling | sequence-modeling | Seq2Seq, Attention, Transformer papers | 순서 있는 데이터의 관계와 생성을 다루는 문제 설정 |
| 산출물 | 출력 산출물 | output artifact | P1-10.1 | output-artifact | output-artifact | P1-10.1 source context | 생성형 AI가 만들어 사람이 검토·재사용하는 결과물 |
| 생성 설정값 | 생성 설정값 | generation setting | P1-4.3 | generation-setting | generation-setting | Google ML Glossary temperature | 생성 시점의 출력 선택 조절값 |
| 서비스 | 서비스 | service | P1-4.1 | service | service | P1-4.1 source context | 사용자가 실제로 만나는 제공 형태와 운영 구조 |
| 사람 검토 | 사람 검토 | human review | P1-6.3 | human-review | human-review | P1-6.3 source context | 자동 처리하기 애매하거나 위험한 사례를 사람이 확인하는 절차 |
| 손실 | 손실 | loss | P1-5.1 | loss | loss | Google ML Glossary loss | 학습 목표와 현재 출력의 차이를 나타내는 신호 |
| 신뢰 수준 | 신뢰 수준 | confidence level | P1-6.2 | confidence-level | confidence-level | scikit-learn probability calibration | 보정된 확률 출력을 어느 정도 믿을 수 있는지 읽는 수준 |
| 순전파 | 순전파 | forward pass | P1-5.2 | forward-pass | forward-pass | P1-5.2 source context | 입력이 학습된 파라미터를 지나 출력으로 계산되는 방향 |
| 업무 성과 | 업무 성과 | business outcome | P1-4.4 | business-outcome | business-outcome | scikit-learn model evaluation context | 모델 점수 바깥의 실제 업무 결과 |
| 엡실론 그리디 정책 | 엡실론 그리디 정책 | epsilon-greedy policy | P1-8.3 | epsilon-greedy-policy | epsilon-greedy-policy | P1-8.3 source context | 대부분 활용하되 작은 확률로 탐험하는 정책 |
| 엔드투엔드 학습 | 엔드투엔드 학습 | end-to-end learning | P1-9.2 | end-to-end-learning | end-to-end-learning | YOLO paper | 입력에서 최종 출력까지 연결된 구조를 함께 학습하는 접근 |
| 언어 모델링 | 언어 모델링 | language modeling | P1-9.3 | language-modeling | language-modeling | Bengio neural probabilistic language model | 단어·토큰 순서의 확률을 다루는 LLM 직접 계보의 문제 설정 |
| 원시 오디오 파형 | 원시 오디오 파형 | raw audio waveform | P1-9.2 | raw-audio-waveform | raw-audio-waveform | WaveNet paper | 시간 순서로 기록된 오디오 신호 값 자체에 가까운 표현 |
| 오류 누적 | 오류 누적 | error accumulation | P1-10.2 | error-accumulation | error-accumulation | P1-10.2 source context | 앞 단계 오류가 뒤 생성 조건으로 남아 결과를 흔드는 현상 |
| 응답 생성 | 응답 생성 | response generation | P1-5.2 | response-generation | response-generation | Google ML Glossary inference LLM context | LLM이 프롬프트를 바탕으로 자연어 응답을 만드는 실행 |
| 의사결정 | 의사결정 | decision | P1-6.3 | decision | decision | P1-6.3 source context | 모델 숫자와 비용·정책을 함께 보고 실제 행동을 정하는 단계 |
| 영향 | 영향 | impact | P1-1.1 | impact | impact | OECD AI system definition | 출력이 사람 판단·환경 변화에 닿는 결과 |
| 원-핫 표현 | 원-핫 표현 | one-hot representation | P1-11.1 | one-hot-representation | one-hot-representation | P1-11.1 source context | 항목 위치 한 칸만 1로 켜는 희소한 식별 표현 |
| 이미지 인식 | 이미지 인식 | image recognition | P1-9.1 | image-recognition | image-recognition | LeCun deep learning review, face recognition survey | 이미지에서 의미 있는 시각 범주를 예측하는 문제 |
| 자기회귀 모델 | 자기회귀 모델 | autoregressive model | P1-9.2 | autoregressive-model | autoregressive-model | WaveNet paper, language modeling context | 앞 값에 조건부로 다음 값을 순서대로 예측·생성하는 모델 |
| 자연스러움 | 자연스러움 | naturalness | P1-10.3 | naturalness | naturalness | P1-10.3 source context | 생성 문장이 매끄럽고 그럴듯해 보이는 성질 |
| 점수 | 점수 | score | P1-5.2 | score | score | Google ML Glossary score context | 후보 출력 비교에 쓰이는 모델 수치 |
| 점 예측 | 점 예측 | point prediction | P1-6.3 | point-prediction | point-prediction | P1-6.3 source context | 불확실성 범위 없이 하나의 대표 숫자만 제시하는 예측 |
| 조밀한 벡터 | 조밀한 벡터 | dense vector | P1-11.1 | dense-vector | dense-vector | P1-11.1 source context | 대부분의 차원이 실제 값을 가지는 임베딩식 벡터 표현 |
| 주변 근거 | 주변 근거 | surrounding evidence | P1-9.3 | surrounding-evidence | surrounding-evidence | P1-9.3 source context | 직접 조상은 아니지만 딥러닝 확산의 배경이 되는 사례 |
| 중심점 | 중심점 | centroid | P1-8.2 | centroid | centroid | P1-8.2 source context | 군집을 대표하는 평균 위치 |
| 주성분 분석 | 주성분 분석 | principal component analysis, PCA | P1-8.2 | principal-component-analysis-pca | principal-component-analysis-pca | P1-8.2 source context | 분산이 큰 방향을 찾는 차원 축소 방법 |
| 지연 보상 | 지연 보상 | delayed reward | P1-8.3 | delayed-reward | delayed-reward | P1-8.3 source context | 행동의 결과가 여러 단계 뒤 보상으로 드러나는 상황 |
| 지역 패턴 | 지역 패턴 | local pattern | P1-9.1 | local-pattern | local-pattern | CNN context | 이미지의 작은 영역에서 반복적으로 나타나는 시각 단서 |
| 직접 계보 | 직접 계보 | direct lineage | P1-9.3 | direct-lineage | direct-lineage | P1-9.3 source context | 현재 기술 핵심 구조로 직접 이어지는 연구 흐름 |
| 정보 무결성 | 정보 무결성 | information integrity | P1-10.3 | information-integrity | information-integrity | NIST GenAI Profile | 정보가 사실과 맥락을 왜곡하지 않고 신뢰 가능한 상태 |
| 조건 | 조건 | condition | P1-10.2 | condition | condition | P1-10.2 source context | 출력을 만들 때 참고하는 입력·지시·맥락·제약 |
| 통계적 언어 모델 | 통계적 언어 모델 | statistical language model | P1-11.1 | statistical-language-model | statistical-language-model | P1-11.1 source context | 빈도와 조건부 확률로 다음 표현 가능성을 추정하는 언어 모델 |
| 통계적 추론 | 통계적 추론 | statistical inference | P1-5.3 | statistical-inference | statistical-inference | OpenStax Introductory Statistics | 표본에서 모집단과 불확실성을 다루는 통계 절차 |
| 마스크드 언어 모델 | 마스크드 언어 모델 | masked language model | P1-11.3 | masked-language-model | masked-language-model | P1-11.3 source context | 문장 일부를 가리고 주변 문맥으로 맞히는 사전학습 방식 |
| 문맥 벡터 | 문맥 벡터 | context vector | P1-11.2 | context-vector | context-vector | P1-11.2 source context | attention에서 입력 표현을 가중합해 만든 현재 단계의 문맥 표현 |
| 문맥 내 학습 | 문맥 내 학습 | in-context learning | P1-12.1 | in-context-learning | in-context-learning | GPT-3 paper | 모델 가중치 업데이트 없이 현재 입력 문맥으로 출력 행동이 달라지는 현상 |
| 맥락 | 맥락 | context | P1-12.1 | context | context | prompt engineering context | 작업에 필요한 배경·자료·앞선 결정을 제공하는 입력 요소 |
| 문서 벡터 | 문서 벡터 | document vector | P1-13.2 | document-vector | document-vector | P1-13.2 source context | 문서나 문서 조각을 검색 비교용 임베딩으로 바꾼 표현 |
| 벡터 검색 | 벡터 검색 | vector search | P1-13.4 | vector-search | vector-search | vector search implementation context | 임베딩 벡터 공간에서 가까운 후보를 찾는 검색 방식 |
| 벡터 데이터베이스 | 벡터 데이터베이스 | vector database | P6-12.1 | vector-database | vector-database | vector database context | 벡터 저장, 인덱스, 메타데이터, 필터링을 함께 다루는 시스템 |
| 프록시 라벨 | 프록시 라벨 | proxy label | P1-8.1 | proxy-label | proxy-label | P1-8.1 source context | 직접 목표를 대신하는 대리 라벨 |
| 픽셀 | 픽셀 | pixel | P1-9.1 | pixel | pixel | P1-9.1 source context | 디지털 이미지를 이루는 가장 작은 위치 단위 |
| 프롬프트 | 프롬프트 | prompt | P1-12.1 | prompt | prompt | OpenAI prompt engineering, GPT-3 paper | 현재 응답 조건을 담은 입력 전체 |
| 프롬프트 구조화 | 프롬프트 구조화 | prompt structuring | P1-12.2 | prompt-structuring | prompt-structuring | prompt engineering context | 입력 안의 역할을 나눠 쓰는 방식 |
| 프롬프트 예시 | 프롬프트 예시 | prompt example, task demonstration | P1-12.2 | prompt-example | prompt-example | GPT-3 paper | 현재 입력 안에서 원하는 패턴이나 판단 기준을 보여 주는 예시 |
| 프롬프트의 한계 | 프롬프트의 한계 | limit of prompting | P1-12.3 | limit-of-prompting | limit-of-prompting | P1-12.3 source context | 입력을 잘 써도 자동으로 해결되지 않는 문제 |
| 사전학습 LLM | 사전학습 LLM | pretrained LLM | P1-11.3 | pretrained-llm | pretrained-llm | P1-11.3 source context | 대규모 일반 학습을 먼저 마친 대규모 언어 모델 |
| 스킵그램 | 스킵그램 | Skip-gram | P1-11.1 | skip-gram | skip-gram | P1-11.1 source context | 중심 단어로 주변 단어를 예측하며 단어 벡터를 배우는 word2vec 방식 |
| 사실성 | 사실성 | factuality | P1-12.3 | factuality | factuality | NIST GenAI Profile | 문장이 실제 사실과 맞는지 보는 기준 |
| 최신성 | 최신성 | recency | P1-12.3 | recency | recency | P1-12.3 source context | 정보가 지금 시점에도 유효한지 보는 기준 |
| 상위 k개 | 상위 k개 | top-k | P1-13.2 | top-k | top-k | vector retrieval context | 가까운 후보 k개를 가져오는 검색 결과 선택 방식 |
| 유사도 검색 | 유사도 검색 | similarity search | P1-13.2 | similarity-search | similarity-search | information retrieval context | 질문 벡터와 가까운 문서 벡터 후보를 찾는 과정 |
| 재현율 | 재현율 | recall | P1-13.4 | recall | recall | IR evaluation context | 찾아야 할 관련 후보 중 실제로 찾아낸 비율 |
| 정밀도 | 정밀도 | precision | P1-13.4 | precision | precision | IR evaluation context | 가져온 후보 중 실제로 관련 있는 후보의 비율 |
| 정확 검색 | 정확 검색 | exact search | P1-13.4 | exact-search | exact-search | vector search context | 가장 가까운 후보를 정확히 찾기 위해 충분히 비교하는 방식 |
| 전체 비교 | 전체 비교 | brute-force search | P1-13.4 | brute-force-search | brute-force-search | vector search context | 모든 벡터를 매번 직접 비교하는 기준선 검색 |
| 정보 검색 | 정보 검색 | information retrieval | P1-13.3 | information-retrieval | information-retrieval | IR textbook, RAG context | 질문에 맞는 문서·문단·근거 후보를 찾아오는 문제 |
| 질문 벡터 | 질문 벡터 | query vector | P1-13.2 | query-vector | query-vector | P1-13.2 source context | 검색 요청을 임베딩으로 바꾼 기준 벡터 |
| 학습 | 학습 | learning | P1-5.1 | learning | learning | Deep Learning Book, Mitchell definition | 경험 이후 과제 성능이 개선되는 넓은 개념 |
| 학습된 표현 | 학습된 표현 | learned representation | P1-9.1 | learned-representation | learned-representation | representation learning review | 모델이 과제에 맞게 데이터에서 배운 내부 표현 |
| 합성곱 신경망 | 합성곱 신경망 | CNN, convolutional neural network | P1-9.1 | cnn-convolutional-neural-network | cnn-convolutional-neural-network | LeCun deep learning review | 이미지의 지역 패턴을 계층적으로 다루는 신경망 구조 |
| 알렉스넷 | 알렉스넷 | AlexNet | P1-9.1 | alexnet | alexnet | AlexNet paper | 대규모 이미지 인식에서 딥러닝 확산을 각인시킨 전환점 사례 |
| 객체 검출 | 객체 검출 | object detection | P1-9.2 | object-detection | object-detection | YOLO paper | 이미지 안의 물체 범주와 위치를 함께 예측하는 문제 |
| 욜로 | 욜로 | YOLO | P1-9.2 | yolo | yolo | YOLO paper | 객체 검출을 단일 신경망 예측 문제로 재구성한 사례 |
| 웨이브넷 | 웨이브넷 | WaveNet | P1-9.2 | wavenet | wavenet | WaveNet paper | 원시 오디오 파형을 순차 생성한 모델 사례 |
| 음성 생성 | 음성 생성 | speech generation | P1-9.2 | speech-generation | speech-generation | WaveNet paper | 시간 순서의 오디오 신호를 만드는 생성 문제 |
| 텍스트 음성 변환 | 텍스트 음성 변환 | TTS, text-to-speech | P1-9.2 | tts-text-to-speech | tts-text-to-speech | Deep Voice paper | 텍스트 입력을 음성 출력으로 바꾸는 응용 문제 |
| 후처리 | 후처리 | postprocessing | P1-5.2 | postprocessing | postprocessing | P1-5.2 source context | 모델 출력을 서비스 결정이나 표시 결과로 바꾸는 단계 |
| 위험 | 위험 | risk | P1-10.3 | risk | risk | NIST GenAI Profile | 생성 결과나 AI 사용이 피해로 이어질 가능성 |
| 확률적 예측 | 확률적 예측 | probabilistic prediction | P1-6.3 | probabilistic-prediction | probabilistic-prediction | Google ML Glossary probabilistic regression model | 가능한 결과의 범위나 가능성을 함께 표현하는 예측 |
| 확률적 선택 | 확률적 선택 | probabilistic choice | P1-10.2 | probabilistic-choice | probabilistic-choice | P1-10.2 source context | 후보 분포에서 실제 출력 하나를 선택하는 과정 |
| 키워드 검색 | 키워드 검색 | keyword search | P1-13.2 | keyword-search | keyword-search | information retrieval context | 단어나 구문 일치를 기준으로 후보를 찾는 검색 방식 |
| 웨이포인트 | 웨이포인트 | waypoint | P1-7.4 | waypoint | waypoint | autonomous driving planning context | 큰 경로나 참조선을 표현하는 기준점 열 |
| 입력 조건 | 입력 조건 | input condition | P1-12.1 | input-condition | input-condition | P1-12.1 source context | 현재 실행에서 프롬프트로 제공한 작업 조건 |
| 출력 정의 | 출력 정의 | output definition | P1-4.4 | output-definition | output-definition | P1-4.4 source context | 모델이 내야 하는 결과 형식과 의미 |
| 출력 형식 | 출력 형식 | output format | P1-12.1 | output-format | output-format | OpenAI prompt engineering | 결과를 표, 목록, JSON, 문단 등 어떤 모양으로 받을지 정하는 조건 |
| reasoning | reasoning | reasoning | P1-5.3 | reasoning | reasoning | P1-5.3 source context | 모델 실행과 구분해야 하는 논리적 사고 과정 |
| CBOW | 연속 bag-of-words | continuous bag-of-words | P1-11.1 | cbow-continuous-bag-of-words | cbow-continuous-bag-of-words | P1-11.1 source context | 주변 단어로 중심 단어를 예측하며 단어 벡터를 배우는 word2vec 방식 |
| 어텐션 가중치 | 어텐션 가중치 | attention weight | P1-11.2 | attention-weight | attention-weight | P1-11.2 source context | 모델 파라미터 weight와 구분되는 현재 문맥의 참고 비중 |
| 지시 | 지시 | instruction | P1-12.1 | instruction | instruction | InstructGPT, prompt engineering context | 모델에게 수행할 작업을 알려 주는 요청 요소 |
| 제약 | 제약 | constraint | P1-12.1 | constraint | constraint | P1-12.1 source context | 길이, 범위, 금지 조건처럼 결과 범위를 좁히는 조건 |
| 근거성 | 근거 | evidence | P1-12.3 | evidence | evidence | P1-12.3 source context | 주장을 뒷받침하는 출처나 확인 근거가 있는지 보는 기준 |
| 평가 | 평가 | evaluation | P6-16.1 | evaluation | evaluation | InstructGPT, evaluation context | 출력이 목적과 기준에 맞는지 확인하는 절차 |
| 재현성 | 재현성 | reproducibility | P2-7.5 | reproducibility | reproducibility | reproducible workflow context | 무엇을 바꿨고 결과가 어땠는지 다시 확인할 수 있는 성질 |
| 일관성 | 일관성 | consistency | P1-12.3 | consistency | consistency | P1-12.3 source context | 여러 입력과 반복 결과에서 기준이 유지되는 정도 |
| RAG | 검색 증강 생성 | retrieval-augmented generation | P1-13.3 | retrieval-augmented-generation-rag | retrieval-augmented-generation-rag | RAG paper | 검색한 외부 자료를 생성 입력에 붙이는 구조 |
| HNSW | HNSW | hierarchical navigable small world | P1-13.4 | hnsw-hierarchical-navigable-small-world | hnsw-hierarchical-navigable-small-world | HNSW paper | 그래프 기반 ANN의 대표적인 벡터 검색 인덱스 방법 |
| 앱 | 앱 | application | P1-14.1 | application | application | P1-14.1 source context | 모델, 데이터, 도구를 묶어 사용자가 만나는 기능 형태 |
| 도구 | 도구 | tool | P1-14.1 | tool | tool | P1-14.1 source context | 모델 밖의 기능을 조회하거나 실행하는 연결 수단 |
| 오케스트레이션 | 오케스트레이션 | orchestration | P1-14.1 | orchestration | orchestration | P1-14.1 source context | 모델, 데이터, 도구, 앱을 순서와 조건으로 연결하는 제어 층 |
| 도구 사용 | 도구 사용 | tool use | P1-14.2 | tool-use | tool-use | P1-14.2 source context | 외부 시스템 기능을 호출해 조회·실행·상태 변경을 일으키는 구조 |
| 도구 호출 | 도구 호출 | tool call | P1-14.2 | tool-call | tool-call | P1-14.2 source context | 어떤 도구를 어떤 인자로 실행할지 만든 요청 |
| 외부 시스템 | 외부 시스템 | external system | P1-14.2 | external-system | external-system | P1-14.2 source context | 도구 호출로 연결되는 바깥 서비스·파일·데이터베이스·API |
| 권한 | 권한 | permission | P7-6.2 | permission | permission | P1-14.2 source context | 실행 가능한 범위와 접근 한계를 미리 정한 통제 장치 |
| 승인 | 승인 | approval | P1-14.2 | approval | approval | P1-14.2 source context | 실행 전 지금 이 행동을 실제로 허용할지 확인하는 절차 |
| 에이전트 | 에이전트 | agent | P1-14.3 | agent | agent | P1-14.3 source context | 목표, 상태, 관찰, 행동을 이어 가며 작업을 수행하는 실행 구조 |
| 목표 | 목표 | goal | P1-14.3 | goal | goal | P1-14.3 source context | 에이전트가 도달하려는 작업 상태 |
| 상태 | 상태 | state | P1-7.1 | state | state | P1-14.3 source context | 다음 행동 판단에 쓰이는 현재 정보와 조건의 묶음 |
| 행동 | 행동 | action | P1-8.3 | action | action | P1-14.3 source context | 에이전트가 상태를 바꾸기 위해 선택하는 실행 단위 |
| 관찰 | 관찰 | observation | P1-14.3 | observation | observation | P1-14.3 source context | 행동 뒤 돌아온 결과나 환경에서 새로 확인한 정보 |
| 종료 조건 | 종료 조건 | stop condition | P1-14.3 | stop-condition | stop-condition | P1-14.3 source context | 작업을 계속할지 멈출지 정하는 기준 |
| MCP | 모델 컨텍스트 프로토콜 | Model Context Protocol | P1-14.4 | model-context-protocol-mcp | model-context-protocol-mcp | MCP specification context | AI 앱과 외부 도구·리소스·프롬프트 연결을 표준화하려는 프로토콜 |
| 프로토콜 | 프로토콜 | protocol | P1-14.4 | protocol | protocol | P1-14.4 source context | 시스템끼리 요청과 응답 형식을 맞추는 통신 규칙 |
| 호스트 | 호스트 | host | P1-14.4 | host | host | P1-14.4 source context | MCP 연결을 품은 사용자 쪽 AI 앱 또는 실행 주체 |
| 클라이언트 | 클라이언트 | client | P1-14.4 | client | client | P1-14.4 source context | 서버에 요청을 보내는 연결 주체 |
| 서버 | 서버 | server | P1-14.4 | server | server | P1-14.4 source context | 요청을 받아 도구, 데이터, 기능을 제공하는 쪽 |
| 리소스 | 리소스 | resource | P1-14.4 | resource | resource | P1-14.4 source context | 모델이나 앱이 읽을 수 있도록 제공되는 외부 맥락 데이터 |
| 발견 | 발견 | discovery | P1-14.4 | discovery | discovery | P1-14.4 source context | 연결 대상이 제공하는 도구와 리소스를 알아내는 단계 |
| 신뢰 경계 | 신뢰 경계 | trust boundary | P1-14.4 | trust-boundary | trust-boundary | P1-14.4 source context | 믿을 수 있는 영역과 검증해야 하는 영역을 나누는 경계 |
| 하네스 | 하네스 | harness | P1-14.5 | harness | harness | P1-14.5 source context | 실행을 감싸고 기록·평가·재실행을 가능하게 하는 틀 |
| 추적 | 추적 | trace | P1-14.5 | trace | trace | P1-14.5 source context | 한 요청이 거친 단계와 연결 관계를 따라 남기는 기록 |
| 실행 로그 | 로그 | log | P7-6.2 | log | log | P1-14.5 source context | 실행 과정에서 나중에 확인할 수 있도록 남기는 기록 |
| 그레이더 | 그레이더 | grader | P1-14.5 | grader | grader | P1-14.5 source context | 출력이나 실행 결과를 기준에 따라 판정하는 평가 장치 |
| 평가 실행 | 평가 실행 | eval run | P1-14.5 | eval-run | eval-run | P1-14.5 source context | 정해 둔 입력 세트와 평가 기준으로 한 번 돌린 평가 단위 |
| 소프트웨어 회귀 | 소프트웨어 회귀 | software regression | P1-14.5 | software-regression | software-regression | P1-14.5 source context | 변경 뒤 이전에는 되던 기능이나 품질이 나빠지는 현상 |
| 가드레일 | 가드레일 | guardrail | P1-14.5 | guardrail | guardrail | P1-14.5 source context | 허용 범위를 벗어난 입력·출력·실행을 막는 제한과 점검 장치 |
| 서비스 제약 | 서비스 제약 | service constraints | P1-14.6 | service-constraints | service-constraints | P1-14.6 source context | 비용, 지연 시간, 처리량, 호출 한도 같은 운영 제한 조건 |
| 비용 | 비용 | cost | P1-14.6 | cost | cost | P1-14.6 source context | 모델 호출과 서비스 운영에 드는 자원·요금 부담 |
| 지연 시간 | 지연 시간 | latency | P1-14.6 | latency | latency | P1-14.6 source context | 요청 후 결과가 돌아오기까지 걸리는 시간 |
| 처리량 | 처리량 | throughput | P1-14.6 | throughput | throughput | P1-14.6 source context | 단위 시간 동안 처리할 수 있는 요청·토큰·작업의 양 |
| 레이트 리밋 | 레이트 리밋 | rate limit | P1-14.6 | rate-limit | rate-limit | P1-14.6 source context | 짧은 시간 안에 허용되는 요청 수나 토큰 수 제한 |
| 사용량 제한 | 사용량 제한 | usage limit | P1-14.6 | usage-limit | usage-limit | P1-14.6 source context | 기간이나 계정 범위의 총 요청·토큰·비용 한도 |
| 재시도 | 재시도 | retry | P1-14.6 | retry | retry | P1-14.6 source context | 실패한 요청을 조건에 따라 다시 실행하는 정책 |
| 배치 | 배치 | batch | P1-14.6 | batch | batch | P1-14.6 source context | 여러 요청이나 작업을 묶어 처리하는 방식 |
| 캐싱 | 캐싱 | caching | P1-14.6 | caching | caching | P1-14.6 source context | 반복 계산이나 요청 결과를 저장해 재사용하는 방식 |
| 운영 | 운영 | operation | P1-14.6 | service-operation | service-operation | P1-14.6 source context | 서비스를 반복 사용 속에서 비용·오류·속도·품질까지 관리하는 일 |
| 스트리밍 | 스트리밍 | streaming | P1-14.6 | streaming | streaming | P1-14.6 source context | 전체 결과 완성 전 생성 조각을 순서대로 전달하는 방식 |
| 프롬프트 캐싱 | 프롬프트 캐싱 | prompt caching | P1-14.6 | prompt-caching | prompt-caching | P1-14.6 source context | 반복되는 프롬프트 입력 처리를 저장해 재사용하는 최적화 |
| 지수 백오프 | 지수 백오프 | exponential backoff | P1-14.6 | exponential-backoff | exponential-backoff | P1-14.6 source context | 재시도 대기 시간을 점점 크게 늘리는 전략 |
| 지터 | 지터 | jitter | P1-14.6 | jitter | jitter | P1-14.6 source context | 재시도 시점을 분산시키기 위해 대기 시간에 더하는 무작위 흔들림 |
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
| 아이디어 | 아이디어 | idea | P1-15.2 | idea | idea | copyright idea/expression distinction | 구체적 표현으로 고정되기 전의 주제·발상·원리 |
| 사실 | 사실 | fact | P1-10.3 | fact | fact | information integrity context | 참거짓을 확인할 수 있는 현실 주장 |
| 학습 데이터 | 학습 데이터 | training data | P1-15.2 | training-data | training-data | generative AI training data context | 모델이 패턴을 배우는 데 사용되는 데이터 |
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
| 마스킹 | 마스킹 | masking | P1-15.3 | masking | masking | security logging context | 민감 정보 일부를 가리거나 대체해 노출 위험을 줄이는 처리 |
| 개인 학습 | 개인 학습 | personal learning | P1-16.1 | personal-learning | personal-learning | P1-16.1 source context | 잊은 개념을 질문과 근거로 다시 회복하는 학습 과정 |
| 복습 | 복습 | relearning | P1-16.1 | relearning | relearning | P1-16.1 source context | 예전에 배운 내용을 현재 기준으로 다시 재구성하는 과정 |
| 문서화 | 문서화 | documentation | P1-16.1 | documentation | documentation | P1-16.1 source context | 학습 내용과 판단 과정을 구조화된 글과 기록으로 남기는 일 |
| 근거 확인 | 근거 확인 | evidence review | P1-16.1 | evidence-review | evidence-review | P1-16.1 source context | AI 초안이나 검색 결과가 실제 주장을 뒷받침하는지 대조하는 절차 |
| 작업 가설 | 작업 가설 | working hypothesis | P1-16.1 | working-hypothesis | working-hypothesis | P1-16.1 source context | 검증 전 직관을 사실과 구분해 임시 설명으로 보존하는 문장 |
| 질문 구조화 | 질문 구조화 | question structuring | P1-16.1 | question-structuring | question-structuring | P1-16.1 source context | 막연한 기억이나 문제의식을 순서와 범위가 있는 질문으로 나누는 과정 |
| 업무 자동화 | 업무 자동화 | work automation | P1-16.2 | work-automation | work-automation | P1-16.2 source context | 업무 흐름 일부 단계를 AI나 스크립트에 맡기는 적용 방식 |
| 요약 | 요약 | summary | P1-16.2 | summary | summary | P1-16.2 source context | 긴 자료의 핵심 내용을 짧은 형태로 줄여 보여 주는 작업 |
| 검토 | 검토 | review | P1-10.3 | review | review | P1-16.2 source context | AI 결과의 근거, 표현, 범위, 책임 조건을 사람이 다시 확인하는 절차 |
| 생산성 | 생산성 | productivity | P1-16.2 | productivity | productivity | P1-16.2 source context | 생성 속도뿐 아니라 검토·실패·운영 비용까지 포함한 효율 기준 |
| 근거 후보 | 근거 후보 | evidence candidate | P1-16.2 | evidence-candidate | evidence-candidate | P1-16.2 source context | 검색이나 RAG가 찾아낸 검증 전 자료 후보 |
| 검토 비용 | 검토 비용 | review cost | P1-16.2 | review-cost | review-cost | P1-16.2 source context | AI 결과를 실제 사용 가능 상태로 만들기 위한 확인·수정·승인 비용 |
| 프로젝트 | 프로젝트 | project | P1-16.3 | project | project | P1-16.3 source context | 질문이나 목표를 산출물로 검증하는 작업 단위 |
| 실행 범위 | 실행 범위 | scope | P1-15.3 | scope | scope | P1-16.3 source context | 현재 요청이나 자동화가 영향을 줄 수 있는 대상과 경계 |
| 성공 기준 | 성공 기준 | success criteria | P1-16.3 | success-criteria | success-criteria | P1-16.3 source context | 프로젝트 결과를 성공으로 볼 조건을 미리 적은 판단 기준 |
| 기록 | 기록 | record | P1-16.3 | record | record | P1-16.3 source context | 시도, 결과, 실패, 수정 과정을 다시 확인할 수 있게 남긴 자료 |
| 실패 유형 | 실패 유형 | failure type | P1-16.3 | failure-type | failure-type | P1-16.3 source context | 반복되는 실패를 구조에 따라 묶은 분류 틀 |
| 요구사항 | 요구사항 | requirement | P1-16.3 | requirement | requirement | P1-16.3 source context | 프로젝트나 시스템이 반드시 만족해야 하는 기능·품질·제약 조건 |
| 전망 | 미래 전망 | forecast | P1-17.1 | forecast | forecast | Stanford HAI AI Index, WEF Future of Jobs | 미래 변화 가능성을 근거와 조건 위에서 말하는 문장이나 자료 |
| 시나리오 | 시나리오 | scenario | P1-17.1 | scenario | scenario | forecast scenario context | 확정 예측이 아니라 가능한 전개 경로를 조건별로 나누는 틀 |
| 지표 | 지표 | indicator | P1-17.1 | indicator | indicator | AI Index indicator context | 변화 방향을 보여 주는 수치나 관찰 신호 |
| 이해관계 | 이해관계 | stake | P1-17.1 | stake | stake | source evaluation context | 말하는 주체가 얻게 되거나 잃게 되는 이익과 입장 |
| 정책 제안 | 정책 제안 | policy proposal | P1-17.1 | policy-proposal | policy-proposal | policy context | 제도나 규칙을 어떻게 바꾸어야 한다고 제시하는 주장 |
| 기업 발표 | 기업 발표 | company announcement | P1-17.1 | company-announcement | company-announcement | company source context | 기업이 제품·투자·사업 방향을 공개적으로 알리는 자료 |
| 뉴스 | 뉴스 | news | P1-17.2 | news | news | news source reading context | 사건과 당사자를 빠르게 전하는 기사 |
| 칼럼 | 칼럼 | opinion column | P1-17.2 | opinion-column | opinion-column | opinion source context | 필자나 매체의 관점과 해석을 드러내는 글 |
| 보고서 | 보고서 | report | P1-17.2 | report | report | research/report methodology context | 지표, 방법론, 조사 범위, 표본, 한계를 포함해 정리한 자료 |
| 정책 문서 | 정책 문서 | policy document | P1-17.2 | policy-document | policy-document | policy document context | 제도 방향, 의무, 권고, 적용 범위를 밝히는 문서 |
| 사실 사건 | 사실 사건 | fact event | P1-17.2 | fact-event | fact-event | source reading context | 발표, 소송, 발간처럼 날짜와 당사자로 확인할 수 있는 현실 사건 |
| 해석 | 해석 | interpretation | P1-17.2 | interpretation | interpretation | source reading context | 사건이나 자료에 사람이 의미를 붙인 설명 |
| 방법론 | 방법론 | methodology | P1-17.2 | methodology | methodology | report methodology context | 자료를 어떻게 모으고 측정하고 분석했는지 설명하는 절차 |
| 표본 | 표본 | sample | P2-5.3 | statistical-sample | statistical-sample | P2-5.3 source context | 모집단에서 실제로 관측한 일부 데이터 |
| 보고서 한계 | 보고서 한계 | report limit | P1-17.2 | report-limit | report-limit | report limitation context | 보고서의 범위, 표본, 방법, 기간, 해석 가능성의 제한 |
| 사실 주장 | 사실 주장 | factual claim | P1-17.3 | factual-claim | factual-claim | source verification context | 외부 자료와 근거로 확인되어야 하는 문장 |
| 예측 | 예측 | prediction | P1-10.1 | prediction | prediction | ML prediction/forecast distinction | 입력이나 현재 정보에서 다음 값·상태·사건을 추정하는 일 |
| 계산 언어 | 계산 언어 | calculation language | P2-1.1 | calculation-language | calculation-language | P2-1.1 source context | 데이터와 모델 계산 구조를 읽기 위한 수학적 표현 체계 |
| 압축 표기 | 압축 표기 | notation | P2-1.1 | notation | notation | P2-1.1 source context | 반복 계산과 관계를 짧은 기호 체계로 줄여 쓰는 방식 |
| 수식 | 수식 | formula | P2-1.2 | formula | formula | P2-1.2 source context | 계산 관계나 절차를 기호와 숫자로 압축해 적은 표현 |
| 코드 | 코드 | code | P2-1.2 | code | code | P2-1.2 source context | 컴퓨터가 실행할 계산 절차를 프로그래밍 언어로 적은 구조 |
| shape | shape | shape | P2-3.1 | shape | shape | P2-1.2 source context | 배열이나 텐서의 차원과 축별 크기를 보여 주는 모양 정보 |
| 변수 | 변수 | variable | P2-2.1 | variable | variable | P2-2.1 source context | 값을 가리키기 위해 붙인 이름 |
| 함수 | 함수 | function | P2-2.1 | function | function | P2-2.1 source context | 입력을 받아 출력으로 바꾸는 관계나 계산 단위 |
| 식 | 식 | expression | P2-2.1 | expression | expression | P2-2.1 source context | 값, 변수, 연산, 함수 호출을 조합한 계산 조각 |
| 시그마 | 시그마 | sigma | P2-2.2 | sigma | sigma | P2-2.2 source context | 반복 덧셈을 압축해 적는 합 기호 |
| 반복 인덱스 | 반복 인덱스 | summation index | P2-2.2 | summation-index | summation-index | P2-2.2 source context | 시그마 표기에서 반복 위치를 나타내는 이름 |
| 항 | 항 | term | P2-2.2 | summation-term | summation-term | P2-2.2 source context | 시그마에서 반복할 때마다 더해지는 계산 조각 |
| 극한 | 극한 | limit | P2-2.3 | limit | limit | P2-2.3 source context | 입력이 어떤 값에 가까워질 때 함수값의 경향을 보는 표기 |
| 대입 | 대입 | substitution | P2-2.3 | substitution | substitution | P2-2.3 source context | 변수 자리에 특정 값을 넣어 계산해 보는 절차 |
| 가까워짐 | 가까워짐 | approach | P2-2.3 | limit-approach | limit-approach | P2-2.3 source context | 극한에서 값이 목표 지점으로 다가가는 움직임 |
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
| 벡터 위치 | 벡터 위치 | vector position | P2-3.2 | vector-position | vector-position | P2-3.2 source context | 벡터 공간에서 좌표나 점처럼 읽는 표현의 자리 |
| 차원 | 차원 | dimension | P2-3.2 | dimension | dimension | P2-3.2 source context | 벡터가 가진 값의 개수 또는 좌표 축의 수 |
| 위상 | 위상 | topology | P2-3.2 | topology | topology | P2-3.2 source context | 공간의 가까움·연결·연속성 구조를 보는 추상 관점 |
| 매니폴드 | 매니폴드 | manifold | P2-3.2 | manifold | manifold | P2-3.2 source context | 데이터 표현들이 이루는 더 낮거나 부드러운 공간 구조 |
| 벡터 덧셈 | 벡터 덧셈 | vector addition | P2-3.2 | vector-addition | vector-addition | P2-3.2 source context | 같은 위치 성분끼리 더해 새 벡터를 만드는 계산 |
| 스칼라배 | 스칼라배 | scalar multiplication | P2-3.2 | scalar-multiplication | scalar-multiplication | P2-3.2 source context | 벡터 각 성분에 같은 스칼라를 곱하는 계산 |
| 선형 결합 | 선형 결합 | linear combination | P2-3.2 | linear-combination | linear-combination | P2-3.2 source context | 스칼라배와 벡터 덧셈을 묶어 새 표현을 만드는 계산 |
| 행렬 곱 | 행렬 곱 | matrix multiplication | P2-3.3 | matrix-multiplication | matrix-multiplication | P2-3.3 source context | 행과 열을 조합해 새 값을 만드는 계산 |
| 위치별 곱 | 위치별 곱 | element-wise multiplication | P2-3.3 | element-wise-multiplication | element-wise-multiplication | P2-3.3 source context | 같은 shape의 같은 위치 값끼리 곱하는 계산 |
| 가중합 | 가중합 | weighted sum | P2-3.3 | weighted-sum | weighted-sum | P2-3.3 source context | 입력값마다 가중치를 곱한 뒤 더해 하나의 값을 만드는 계산 |
| 가중치 행렬 | 가중치 행렬 | weight matrix | P2-3.3 | weight-matrix | weight-matrix | P2-3.3 source context | 여러 가중합을 한꺼번에 계산하도록 가중치를 행렬로 묶은 구조 |
| 선형 변환 | 선형 변환 | linear transformation | P2-3.3 | linear-transformation | linear-transformation | P2-3.3 source context | 행렬 곱으로 벡터를 다른 표현 공간으로 옮기는 계산 |
| 내적 | 내적 | dot product | P2-3.4 | dot-product | dot-product | P2-3.4 source context | 같은 위치 성분을 곱해 더한 하나의 요약값 |
| 노름 | 길이 | norm | P2-3.4 | norm | norm | P2-3.4 source context | 벡터의 길이나 크기를 하나의 숫자로 요약한 값 |
| 거리 | 거리 | distance | P2-3.4 | distance | distance | P2-3.4 source context | 두 벡터가 표현 공간에서 얼마나 떨어져 있는지 보는 기준 |
| 유사도 | 유사도 | similarity | P2-3.4 | similarity | similarity | P2-3.4 source context | 두 벡터나 표현이 얼마나 닮았는지 보는 비교 기준 |
| 코사인 유사도 | 코사인 유사도 | cosine similarity | P2-3.4 | cosine-similarity | cosine-similarity | P2-3.4 source context | 두 벡터의 방향 유사성을 보는 기준 |
| 콜랩 | Colab | Colab | P2-10.2 | colab | colab | P2-3.5 source context | 브라우저에서 노트북을 실행하는 Google 호스팅형 Jupyter 환경 |
| 로컬 PC | 로컬 PC | local PC | P2-3.5 | local-pc | local-pc | P2-3.5 source context | 독자 자신의 컴퓨터에서 Python과 터미널로 코드를 실행하는 자리 |
| 코드 셀 | 코드 셀 | code cell | P2-10.1 | code-cell | code-cell | P2-3.5 source context | 노트북에서 실제 코드를 입력하고 실행하는 셀 |
| 매직 명령 | 매직 명령 | magic command | P2-3.5 | magic-command | magic-command | P2-3.5 source context | Jupyter/Colab 코드 셀에서 쓰는 특수 환경 명령 |
| import 문 | import 문 | import statement | P2-3.5 | import-statement | import-statement | P2-3.5 source context | 설치된 모듈이나 패키지를 Python 코드에서 불러오는 문장 |
| 넘파이 | NumPy | NumPy | P2-3.6 | numpy | numpy | P2-3.6 source context | Python에서 숫자 배열과 벡터·행렬 계산을 다루는 라이브러리 |
| 변화 비교 | 변화 비교 | change comparison | P2-4.1 | change-comparison | change-comparison | P2-4.1 source context | 입력 변화와 출력 변화가 어떻게 함께 움직이는지 보는 질문 |
| 접선 | 접선 | tangent line | P2-4.1 | tangent-line | tangent-line | P2-4.1 source context | 곡선의 한 지점 근처 변화 방향을 보여 주는 직선 |
| 기울기 | 기울기 | slope | P2-4.2 | slope | slope | P2-4.2 source context | 입력 변화에 대한 출력 변화를 그래프 위에서 읽는 값 |
| 곡선 | 곡선 | curve | P2-4.2 | curve | curve | P2-4.2 source context | 위치에 따라 변화율이 달라질 수 있는 선 |
| 평균 변화율 | 평균 변화율 | average rate of change | P2-4.2 | average-rate-of-change | average-rate-of-change | P2-4.2 source context | 두 지점 사이 구간 전체의 변화 비율 |
| 순간 변화율 | 순간 변화율 | instantaneous rate of change | P2-4.2 | instantaneous-rate-of-change | instantaneous-rate-of-change | P2-4.2 source context | 특정 지점 바로 근처의 변화율 |
| 미분 | 미분 | derivative | P2-4.3 | derivative | derivative | P2-4.3 source context | 입력을 아주 조금 바꿨을 때 출력이 얼마나 변하는지 나타내는 순간 변화율 |
| 미분계수 | 미분계수 | derivative at a point | P2-4.3 | derivative-at-a-point | derivative-at-a-point | P2-4.3 source context | 특정 지점에서 읽은 순간 변화율 값 |
| 도함수 | 도함수 | derivative function | P2-4.3 | derivative-function | derivative-function | P2-4.3 source context | 각 입력 위치의 미분계수를 알려 주는 함수 |
| 편미분 | 편미분 | partial derivative | P2-4.3 | partial-derivative | partial-derivative | P2-4.3 source context | 여러 입력 중 하나만 바꿨다고 보고 계산한 변화율 |
| 그래디언트 | 그래디언트 | gradient | P2-4.3 | gradient | gradient | P2-4.3 source context | 여러 편미분을 순서 있게 모은 변화율 벡터 |
| 나블라 | 나블라 | nabla | P2-4.3 | nabla | nabla | P2-4.3 source context | 그래디언트를 적을 때 쓰는 ∇ 기호의 이름 |
| 조정 방향 | 조정 방향 | update direction | P2-4.4 | update-direction | update-direction | P2-4.4 source context | 손실을 줄이기 위해 파라미터를 움직일 방향 정보 |
| 방향도함수 | 방향도함수 | directional derivative | P2-4.5 | directional-derivative | directional-derivative | P2-4.5 source context | 특정 방향으로 조금 움직였을 때 함수값이 얼마나 변하는지 보는 변화율 |
| 벡터해석 | 벡터해석 | vector calculus | P2-4.5 | vector-calculus | vector-calculus | P2-4.5 source context | 벡터·공간·함수·변화율을 함께 다루는 수학 체계 |
| 일변수 함수 | 일변수 함수 | single-variable function | P2-4.5 | single-variable-function | single-variable-function | P2-4.5 source context | 입력 변수가 하나인 함수 |
| 다변수 함수 | 다변수 함수 | multivariable function | P2-4.5 | multivariable-function | multivariable-function | P2-4.5 source context | 입력 변수가 두 개 이상인 함수 |
| 스칼라장 | 스칼라장 | scalar field | P2-4.5 | scalar-field | scalar-field | P2-4.5 source context | 공간의 각 위치마다 하나의 스칼라 값을 대응시키는 표현 |
| 벡터장 | 벡터장 | vector field | P2-4.5 | vector-field | vector-field | P2-4.5 source context | 공간의 각 위치마다 하나의 벡터를 대응시키는 표현 |
| 역방향 패스 | 역방향 패스 | backward pass | P2-4.5 | backward-pass | backward-pass | P2-4.5 source context | 손실에서 거꾸로 각 계산 단계의 그래디언트를 계산하는 실행 방향 |
| 합성함수 | 합성함수 | composite function | P2-4.6 | composite-function | composite-function | P2-4.6 source context | 한 함수의 출력이 다음 함수의 입력으로 이어지는 함수 구조 |
| 연쇄 법칙 | 연쇄 법칙 | chain rule | P2-4.6 | chain-rule | chain-rule | P2-4.6 source context | 합성함수에서 단계별 변화율을 이어 읽는 미분 규칙 |
| 확률 | 확률 | probability | P2-5.1 | probability | probability | P2-5.1 source context | 불확실성을 0과 1 사이의 숫자로 표현하는 언어 |
| 불확실성 | 불확실성 | uncertainty | P1-6.2 | uncertainty | uncertainty | P2-5.1 source context | 현재 정보만으로 하나의 결과를 확정할 수 없는 상태 |
| 결과 | 결과 | outcome | P2-5.1 | outcome | outcome | P2-5.1 source context | 한 번의 시행에서 나올 수 있는 개별 결과 |
| 사건 | 사건 | event | P2-5.1 | event | event | P2-5.1 source context | 관심 있는 결과들을 묶은 집합 |
| 표본공간 | 표본공간 | sample space | P2-5.1 | sample-space | sample-space | P2-5.1 source context | 가능한 모든 결과를 모아 둔 전체 집합 |
| 장기 빈도 | 장기 빈도 | long-run frequency | P2-5.1 | long-run-frequency | long-run-frequency | P2-5.1 source context | 반복 실험에서 어떤 결과가 나타나는 비율로 확률을 읽는 관점 |
| 믿음의 정도 | 믿음의 정도 | degree of belief | P2-5.1 | degree-of-belief | degree-of-belief | P2-5.1 source context | 현재 정보로 어떤 일이 얼마나 그럴듯한지 표현하는 확률 해석 |
| 베이즈 규칙 | 베이즈 규칙 | Bayes' rule | P2-5.1 | bayes-rule | bayes-rule | P2-5.1 source context | 새 증거로 가능성 판단을 갱신하는 확률 규칙 |
| 사전 믿음 | 사전 믿음 | prior belief | P2-5.1 | prior-belief | prior-belief | P2-5.1 source context | 새 관측을 보기 전에 가진 가능성 판단 |
| 사후 믿음 | 사후 믿음 | posterior belief | P2-5.1 | posterior-belief | posterior-belief | P2-5.1 source context | 새 증거를 반영한 뒤 갱신된 가능성 판단 |
| 분포 | 분포 | distribution | P2-5.2 | distribution | distribution | P2-5.2 source context | 값들이 어디에 몰리고 얼마나 퍼져 있는지 보여 주는 전체 모양 |
| 데이터 분포 | 데이터 분포 | data distribution | P2-5.2 | data-distribution | data-distribution | P2-5.2 source context | 실제로 관측한 데이터 값들이 놓인 모양 |
| 확률분포 | 확률분포 | probability distribution | P2-5.2 | probability-distribution | probability-distribution | P2-5.2 source context | 가능한 값이나 결과에 확률을 배정한 수학적 표현 |
| 중심 | 중심 | center | P2-5.2 | center | center | P2-5.2 source context | 여러 값이 대체로 모여 있는 대표 자리 |
| 평균 | 평균 | mean | P2-5.2 | mean | mean | P2-5.2 source context | 여러 값을 더한 뒤 개수로 나눈 대표 중심값 |
| 분산 | 분산 | variance | P2-5.2 | variance | variance | P2-5.2 source context | 값들이 평균 주변에서 얼마나 퍼져 있는지 나타내는 값 |
| 퍼짐 | 퍼짐 | spread | P2-5.2 | spread | spread | P2-5.2 source context | 값들이 중심 주변에서 얼마나 넓게 흩어져 있는지 보는 관점 |
| 모집단 | 모집단 | population | P2-5.3 | population | population | P2-5.3 source context | 알고 싶어 하는 전체 대상 |
| 추정 | 추정 | estimation | P2-5.3 | estimation | estimation | P2-5.3 source context | 표본으로 모집단의 값이나 성질을 짐작하는 일 |
| 통계량 | 통계량 | statistic | P2-5.3 | statistic | statistic | P2-5.3 source context | 표본에서 계산한 값 |
| 실제 값 | 실제 값 | true value | P2-5.3 | true-value | true-value | P2-5.3 source context | 추정하려는 대상의 실제 값 |
| 오차 | 오차 | error | P2-5.3 | error | error | P2-5.3 source context | 추정값이나 예측값과 실제 값 사이의 차이 |
| 표본추출 변동 | 표본추출 변동 | sampling variation | P2-5.3 | sampling-variation | sampling-variation | P2-5.3 source context | 표본을 다시 뽑을 때 추정값이 조금씩 달라지는 현상 |
| 표본 편향 | 표본 편향 | sampling bias | P2-5.3 | sampling-bias | sampling-bias | P2-5.3 source context | 표본이 모집단을 잘 대표하지 못하고 특정 방향으로 치우친 상태 |
| 테스트 데이터 | 테스트 데이터 | test data | P2-5.3 | test-data | test-data | P2-5.3 source context | 학습에 직접 쓰지 않고 모델 성능 확인을 위해 따로 둔 데이터 |
| 중위값 | 중위값 | median | P2-5.4 | median | median | P2-5.4 source context | 값을 크기순으로 정렬했을 때 가운데에 놓이는 값 |
| 이상값 | 이상값 | outlier | P2-13.1 | outlier | outlier | P2-5.4 source context | 전체 값 흐름에서 유난히 멀리 떨어져 보이는 값 |
| 표본 평균 | 표본 평균 | sample mean | P2-5.4 | sample-mean | sample-mean | P2-5.4 source context | 표본에 들어 있는 값들의 평균 |
| 모집단 분산 | 모집단 분산 | population variance | P2-5.4 | population-variance | population-variance | P2-5.4 source context | 가진 데이터 묶음을 모집단 전체로 보고 계산하는 분산 |
| 표본 분산 | 표본 분산 | sample variance | P2-5.4 | sample-variance | sample-variance | P2-5.4 source context | 표본으로 모집단의 퍼짐을 추정한다고 보고 계산하는 분산 |
| 표준편차 | 표준편차 | standard deviation | P2-5.5 | standard-deviation | standard-deviation | P2-5.5 source context | 분산의 제곱근으로 퍼짐을 원래 단위에 가깝게 읽는 값 |
| 공분산 | 공분산 | covariance | P2-5.5 | covariance | covariance | P2-5.5 source context | 두 값이 함께 움직이는 방향을 보는 값 |
| 상관계수 | 상관계수 | correlation coefficient | P2-5.5 | correlation-coefficient | correlation-coefficient | P2-5.5 source context | 두 값의 함께 움직임을 비교하기 쉬운 눈금으로 나타낸 값 |
| 표준오차 | 표준오차 | standard error | P2-5.5 | standard-error | standard-error | P2-5.5 source context | 표본 평균 같은 추정값이 얼마나 흔들릴 수 있는지 보여 주는 값 |
| 신뢰구간 | 신뢰구간 | confidence interval | P2-5.5 | confidence-interval | confidence-interval | P2-5.5 source context | 추정값을 어느 범위 안에서 함께 읽어야 하는지 보여 주는 방식 |
| 가설검정 | 가설검정 | hypothesis testing | P2-5.5 | hypothesis-testing | hypothesis-testing | P2-5.5 source context | 관측된 차이가 표본 우연만으로 설명될 수 있는지 따져 보는 절차 |
