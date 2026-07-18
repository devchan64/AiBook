# Section Release Note

- Section ID: `BOOK-toc`
- Source File: `docs/book/table-of-contents.md`

### v2026.07.18

- 변경 이유: Part 7이 프로젝트 유형을 나열하는 카탈로그처럼 읽혀, 앞 Part에서 다듬은 `문제 정의 -> baseline -> 구조 선택 -> 실행 -> 평가 -> 운영 회고` 중심축이 공개 목차에서 드러나지 않았다.
- 본문 반영: 한국어 독자용 목차의 Part 7 소개 문단을 `작은 프로젝트로 다시 실행해 보는 구간`으로 다시 쓰고, 설명의 중심을 새 이론 소개가 아니라 `입력 단위 정의`, `baseline 설정`, `구조 선택`, `코드와 도식 확인`으로 옮겼다.
- 본문 반영: Part 7의 모듈과 장 구조를 `데이터/전통 ML/이미지/텍스트/RAG/agent/배포` 나열형에서 `프로젝트 문제 정의와 기준선 -> 구조 선택이 드러나는 모델 프로젝트 -> LLM 서비스 프로젝트 -> 배포와 운영 회고` 흐름으로 재배치했다.
- 본문 반영: Part 7 각 Section 설명도 프로젝트 유형 소개 대신 `비교표와 오류 사례 읽기`, `입력 구조와 모델 구조 선택`, `검색-근거-답변 검증`, `계획-도구 호출-승인 흐름`, `배포 점검과 운영 회고`처럼 실습 판단 장면이 먼저 보이도록 갱신했다.
- 추가 보강: 같은 날짜 재수정에서 Part 7 소개 문단과 각 Section 설명을 더 풀어 써, 무엇을 실행하고 무엇을 비교하며 무엇을 해석하는 실습인지가 공개 목차만 읽어도 보이도록 분량과 구체성을 보강했다.
- 추가 보강: 장난감 예제로 읽힐 수 있는 표현을 걷어 내고, 실제 데이터 준비, 비교표, 실패 사례, 로그, 운영 기록까지 다루는 프로젝트 강도가 드러나도록 Part 7 문구를 다시 조정했다.
- 추가 보강: Part 6 Chapter 3의 과밀한 보충학습을 `P6-3.3 위치 표현과 multi-head attention`, `P6-3.4 KV cache, sparse attention, long-context`의 두 Section으로 나누고, 공개 목차 설명도 각각의 학습 역할이 드러나도록 다시 썼다.
- 추가 보강: 같은 날짜 재수정에서 `P6-3.4`도 다시 `KV cache`, `P6-3.5 sparse attention과 long-context`로 분리해, 공개 목차만 읽어도 `반복 생성 재사용`과 `장문맥 계산/유지`가 다른 질문이라는 점이 보이도록 정리했다.
- 본문 메타데이터 반영: 한국어 독자용 목차 본문의 `Version`을 `v2026.07.18`로 갱신했다.
- 번역 동기화 메모: 같은 날짜 재수정에서 영어판과 중국어 간체판 독자용 목차도 `P6-3.3/P6-3.4/P6-3.5` 분리 구조와 Part 7의 practice-centered 공개 목차 개편을 함께 반영했다. 중국어 간체판 초반 개념사전 링크도 현재 상대 경로 기준으로 바로잡았다.
- 번역 반영 상태: 영어판 및 중국어 간체 목차 반영
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.18`

### v2026.07.08

- 변경 이유: Part 4 Chapter 7에서 전처리 입문 보충학습을 먼저 두고 특징 선택·차원 축소 구분 보충학습을 뒤로 미루는 재배치가 필요해졌다.
- 본문 반영: 한국어 독자용 목차의 `P4-7.3`을 `결측치, 스케일, 인코딩을 어떤 입력 문제로 구분하는가`로 갱신하고, 기존 `필터, 래퍼, 차원 축소` 보충학습을 `P4-7.4`로 뒤에 추가했다. 영어판 독자용 목차도 같은 구조로 맞췄다.
- 변경 이유: Part 2 수학 축에서 로그·지수, 벡터 비교 기준, 연쇄 법칙이 빠져 있으면 초심자가 뒤 Part의 핵심 계산 언어를 읽기 전에 빈칸이 생긴다는 판단이 추가되었다.
- 본문 반영: Part 2 목차에 `P2-2.4`, `P2-3.6`, `P2-4.6` 더미 Section을 추가하고, 각 항목이 뒤 Part의 어떤 계산 이해를 미리 떠받치는지 한 줄 설명으로 정리했다.
- 추가 정리: Chapter 3의 이해 순서와 번호 체계를 다시 맞추기 위해 `P2-3.4`, `P2-3.5`, `P2-3.6`의 목차 순서를 `벡터 비교 -> 실행 환경 -> NumPy 실습`으로 재배치했다.

### v2026.07.09

- 변경 이유: Part 2의 보충학습 재방문 경로가 독자용 목차에서 일부 누락되어 있었고, 실제 본문과 목차의 정합성을 다시 맞출 필요가 있었다.
- 본문 반영: Part 2 목차에 `P2-7.9`와 `P2-11.4`를 추가해 로컬 Python 환경 점검과 NumPy `shape`/원본 공유 보충학습이 독자용 목차에서도 직접 보이도록 정리했다.
- 변경 이유: Part 4 Chapter 11의 기존 `P4-11.3`이 log-odds, MLE, 다중 클래스, solver와 regularization을 한 항목에 함께 담아 초심자 기준 중심 질문이 흐려졌고, 보충학습을 더 잘게 분리하는 재배치가 필요해졌다.
- 본문 반영: 한국어 독자용 목차의 Chapter 11 설명을 `P4-11.3 log-odds와 MLE`, `P4-11.4 다중 클래스(multinomial)`, `P4-11.5 solver와 regularization`의 세 갈래 보충학습으로 갱신했다.
- 변경 이유: Part 4 Chapter 15에서 Extra Trees 비교를 본편 밖으로 둘 수 없다는 판단이 생겼고, 랜덤포레스트를 배운 직후 다시 찾아갈 보충학습 경로를 목차에 드러낼 필요가 있었다.
- 본문 반영: 한국어 독자용 목차에 `P4-15.4 보충학습: Extra Trees와 랜덤포레스트를 처음 비교하는 법`을 추가해 split 무작위화, bootstrap 기본값, OOB 가능 조건 비교가 독자용 목차에서도 직접 보이도록 정리했다.
- 번역 동기화 메모: 향후 다른 언어 목차에서도 Part 2 보충학습 누락 없이 같은 구조를 유지하고, Part 4 Chapter 11 보충학습도 `P4-11.3`, `P4-11.4`, `P4-11.5`의 세 갈래 구조를 유지해야 한다.
- 번역 반영 상태: 향후 반영 필요
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.09`

### v2026.07.11

- 변경 이유: Part 5 외부 커리큘럼 비교에서 `초기화(initialization)`, `수치 안정성(numerical stability)`, `batch normalization`을 한 자리에서 회수하는 초심자용 보강 위치가 필요해졌다.
- 본문 반영: 독자용 목차의 Part 5 Chapter 6에 `P5-6.3 보충학습: 초기화(initialization), 수치 안정성(numerical stability), 배치 정규화(batch normalization)를 처음 묶어 읽는 법`을 추가했다.
- 번역 동기화 메모: Part 5 Chapter 6 gained a new supplemental stabilization section and other language TOCs should preserve the same Section ID and placement. / pending
- 번역 반영 상태: 향후 반영 필요
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.11`

### v2026.07.12

- 변경 이유: 중국어 독자용 목차 초반 설명에서 영어판 개념사전 절대 경로가 남아 있었고, `这个 Part` 표현도 현재 중국어 목차군의 `这一 Part` 기준과 어긋나 있었다.
- 본문 반영: 중국어 독자용 목차의 개념사전 링크를 상대 경로 `../reference/concept-glossary.md`로 정리하고, 초반 안내 문단의 `这个 Part`를 `这一 Part`로 통일했다.
- 추가 반영: 중국어 독자용 목차에 Part 2, Part 3, Part 4에 이어 Part 5, Part 6, Part 7 전체 구간도 새로 번역해 추가했다.
- 본문 메타데이터 반영: 중국어 독자용 목차 본문의 `Version`을 `v2026.07.12`로 갱신했다.
- 추가 반영: 영어 독자용 목차에서 누락되어 있던 `P2-2.4`, `P2-4.6`, `P2-7.9`, `P2-11.4`, `P3-7.5`, `P4-8.3`, `P4-11.3~P4-11.5`, `P4-12.3`, `P4-15.4`, `P4-16.3`, `P4-17.3~P4-17.4`, `P4-19.5~P4-19.6`, `P5-6.3`를 같은 위치에 보강하고 `Version`을 `v2026.07.12`로 갱신했다.
- 추가 반영: Part 6 Chapter 1을 `토큰과 토큰화` 8절 구조로 다시 재편하고, 독자용 목차도 `왜 토큰이 필요한가 -> 토큰은 무엇인가 -> 토큰은 어떻게 사용하나 -> 토큰화는 무엇인가 -> 토큰화는 무엇을 바꾸는가 -> 대표 토크나이저 계열 -> 종류 차이는 언제 드러나는가 -> 토큰 관점은 어디에 활용되는가` 흐름으로 다시 정리했다.
- 번역 동기화 메모: English and Simplified Chinese reader-facing TOCs now reflect the current Korean source structure through Part 7, including the newer supplemental sections added in Parts 2, 3, 4, and 5. / 2026-07-12
- 번역 반영 상태: 영어판 보강 및 중국어 간체 추가 수정 반영
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.12`

### v2026.07.13

- 변경 이유: Part 5 Chapter 3에서 대표 활성화 함수 비교가 `sigmoid`, `tanh`, `ReLU`, `수식 비교` 네 Section으로 분리되면서 독자용 목차도 기존 3절 구조와 어긋났다.
- 본문 반영: 한국어 독자용 목차의 P5-3 항목을 `P5-3.2 sigmoid`, `P5-3.3 tanh`, `P5-3.4 ReLU`, `P5-3.5 대표 활성화 함수 수식 비교`, `P5-3.6 출력층(output layer)과 활성화의 선택`으로 갱신했다.
- 추가 반영: 영어판과 중국어 간체판 독자용 목차도 같은 Section ID와 순서로 맞추고, 세 파일의 `Version`을 `v2026.07.13`으로 갱신했다.
- 번역 동기화 메모: Korean, English, and Simplified Chinese reader-facing TOCs now reflect the expanded P5-3 section structure. Future translations should keep P5-3.2 through P5-3.6 aligned.
- 번역 반영 상태: 영어판 및 중국어 간체 목차 반영
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.13`

### v2026.07.14

- 변경 이유: P5-6.3의 안정화 정리와 실제 큰 스케일 누적 실험을 한 절에 함께 두면 보충학습 Section이 과밀해져, 실제 Python 실험을 별도 Section으로 분리할 필요가 생겼다.
- 본문 반영: 한국어, 영어, 중국어 간체 독자용 목차에 `P5-6.4 보충학습: 큰 초기화 스케일이 깊은 층에서 값을 어떻게 키우는가` 항목을 추가하고 세 목차의 `Version`을 `v2026.07.14`로 갱신했다.
- 번역 동기화 메모: Reader-facing TOCs now include P5-6.4 as the practice section that follows the P5-6.3 stabilization overview. Future translations should keep P5-6.3 as the concept map and P5-6.4 as the concrete deep-scale experiment.
- 번역 반영 상태: 영어판 및 중국어 간체 목차 반영
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.14`

### v2026.07.16

- 변경 이유: P5-7.1에서 본편 범위 밖으로만 남아 있던 `adaptive optimization의 이론적 수렴 분석`을 보충학습으로 회수하면서 독자용 목차도 새 Section을 노출해야 했다.
- 본문 반영: 한국어 독자용 목차의 Part 5 Chapter 7에 `P5-7.3 보충학습: adaptive optimization의 수렴 분석을 처음 읽는 법`을 추가하고 `Version`을 `v2026.07.16`으로 갱신했다.
- 번역 동기화 메모: Korean reader-facing TOC now includes P5-7.3 as a supplemental section for adaptive optimization convergence analysis. Future English and Simplified Chinese TOCs should add the same Section ID when translated.
- 번역 반영 상태: 향후 번역 반영 필요
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.16`

### v2026.07.16-2

- 변경 이유: Part 5 큰 폭 개편에서 초중반 목차 축을 `출력, 손실, 역전파` 중심에서 `출력과 gradient 신호`, `손실에서 gradient로`, `계산 그래프와 자동미분` 중심으로 재정렬할 필요가 있었다.
- 본문 반영: 한국어 독자용 목차의 Part 5 Module 2, Chapter P5-5, P5-5.1, P5-5.2, Chapter P5-8 표기를 새 구성에 맞춰 갱신했다.
- 번역 동기화 메모: Korean reader-facing TOC now reflects the Part 5 restructuring around loss-to-gradient conversion and computation graph plus automatic differentiation. Future English and Simplified Chinese TOCs should mirror this structure when translated.
- 번역 반영 상태: 향후 번역 반영 필요
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.16`

### v2026.07.16-3

- 변경 이유: 큰폭 개편안의 모듈 경계가 아직 공개 목차에 충분히 반영되지 않아, 활성화 함수가 출력/손실 축에 섞이고 GPU/배치와 표현 학습이 같은 모듈에 묶이는 문제가 남아 있었다.
- 본문 반영: 한국어 독자용 목차의 Part 5를 `신경망의 기본 계산 구조`, `출력과 손실 신호`, `학습 루프와 안정화`, `계산 확장`, `표현 학습과 구조 분기`, `생성 모델과 샘플링`의 6개 모듈 축으로 재정렬했다.
- 번역 동기화 메모: Korean reader-facing TOC now uses the six-module Part 5 restructuring. Future English and Simplified Chinese TOCs should mirror this module boundary when translated.
- 번역 반영 상태: 향후 반영 필요
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.16`

### v2026.07.16-4

- 변경 이유: Part 5 개편을 파일 경로와 Section ID까지 반영하면서 P5-6/P5-8의 공개 목차 순서를 다시 맞춰야 했다.
- 본문 반영: 한국어 독자용 목차에서 Chapter P5-6을 `학습 루프와 모델 실행`으로 바꾸고, `P5-6.1 학습 루프`, `P5-6.2 learning/inference`, `P5-6.3 training/evaluation mode` 순서로 정리했다. 기존 안정화 보충학습은 `P5-8.3`, 큰 초기화 스케일 실험은 `P5-8.4`로 Chapter P5-8 아래에 배치했다.
- 번역 동기화 메모: Korean reader-facing TOC now reflects the path-level P5-6/P5-8 restructuring. Future English and Simplified Chinese TOCs should follow the new Section IDs.
- 번역 반영 상태: 향후 반영 필요
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.16`

### v2026.07.17

- 변경 이유: Part 5 Chapter 7을 `본편 3절 + 보충학습 5절` 구조로 확장하면서, 독자용 목차도 새 보충학습 재방문 경로를 바로 보여 줄 필요가 생겼다.
- 본문 반영: 한국어 독자용 목차의 Part 5 Chapter 7에 `P5-7.5 momentum, AdaGrad, RMSProp, Adam`, `P5-7.6 learning rate scheduler, warmup, decay`, `P5-7.7 optimizer state와 parameter-wise update`, `P5-7.8 gradient clipping과 불안정한 update`를 추가하고 `Version`을 `v2026.07.17`로 갱신했다.
- 본문 반영: P5-7.4의 표제를 `adaptive optimization의 수렴 보장과 주장 구분`으로 갱신해, 독자용 목차와 배포 내비게이션에서도 이 절이 `읽는 법` 안내가 아니라 주장 구분 기준을 주는 보충학습으로 보이게 정리했다.
- 변경 이유: Part 5 Module 3의 중심이 `학습 루프와 안정화`인데, 기존 Chapter 8 제목 `학습 안정화와 일반화 제약`은 regularization과 stabilization을 병렬 축처럼 읽히게 만들어 흐름이 갈렸다.
- 본문 반영: 한국어 독자용 목차의 Part 5 Chapter 8 제목을 `학습 루프를 안정적으로 만드는 제어 장치`로 바꾸고, P5-8.1~P5-8.4 설명도 `목적 함수 제어 -> 구조 수준 제어 -> 계산 안정화 -> 숫자 확인` 흐름이 보이도록 다시 정리했다.
- 본문 반영: Chapter 8 각 Section 제목도 `기법 이름`과 `질문형 보충학습`이 섞이지 않도록, 모두 `무엇을 제어하는가`가 먼저 보이는 역할형 제목으로 다시 맞췄다.
- 번역 동기화 메모: Korean reader-facing TOC now reflects the expanded Chapter 7 supplementary-learning structure. Future English and Simplified Chinese TOCs should preserve the same Section IDs and order when translated.
- 번역 동기화 메모: Future English and Simplified Chinese TOCs should also replace the old Chapter 8 framing with the new learning-loop-control wording when those translations are updated.
- 번역 반영 상태: 향후 반영 필요
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.17`
