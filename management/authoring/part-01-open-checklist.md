# Part 1 미반영 체크리스트

이 문서는 Part 1 관련 섹션 메모에 남아 있던 `추가 보강 필요`, `남은 검토 사항`만 모아 둔 작업 체크리스트입니다.
이미 본문에 반영된 설명과 집필 판단은 개별 섹션 메모에서 계속 반복하지 않고, 실제 후속 작업만 여기서 관리합니다.

## 체크리스트

- [ ] `AI` 정의의 다국어 사전 비교를 더 보강할 필요가 있으면 한국어권과 일본어권 공개 사전 근거를 추가 확인한다.
- [x] 생성형 AI와 LLM의 관계는 Part 5의 교과서성 NLP 자료와 논문 계보 기준으로 다시 정리한다.
- [ ] `추천과 순위화`, `제어와 행동`, 검색 서비스, 자율주행 예시는 해당 본편 Section을 확장할 때 별도 근거를 다시 확보한다.
- [ ] 기호 기반 AI 대표 사례(Logic Theorist, GPS, MYCIN, DENDRAL)와 현대 규칙 기반 시스템 사례의 공식 근거를 보강한다.
- [x] `추론` 용어를 다시 손볼 때는 사전 정의, `reasoning`, `inference` 구분, LLM 맥락의 표현을 함께 점검한다.
- [x] Chapter 6과 7 연결에서 `uncertainty`, `probability`, `stochastic`, `randomness`, `nondeterminism`의 경계를 더 명확히 정리한다.
- [x] 6.3이나 Part 3에서 `calibration`, `confidence`, `uncertainty estimation` 차이를 별도 근거로 정리할지 결정한다.
- [ ] Part 2에서 빈도주의/베이지안 해석을 어디까지 복구할지 결정하고, 필요하면 연결 문장을 추가한다.
- [x] Chapter 7에서 휴리스틱과 확률 모델을 다시 한 번 분리하고, Part 5의 토큰 확률·프롬프트 휴리스틱 설명과도 용어를 맞춘다.
- [ ] Part 2에서 조합 폭발(combinatorial explosion)이나 지수적 증가(exponential growth)를 보충할지 결정한다.
- [ ] 경로 계획 예시를 Part 6 프로젝트까지 끌고 갈 경우 route, path, trajectory, control 계층을 별도 그림으로 정리한다.
- [x] Part 3의 지도/비지도/강화학습 설명이 8.1, 8.2, 8.3의 라벨·보상 구분을 분명히 이어받는지 점검한다.
- [x] Part 4와 Part 5를 다시 손볼 때 CNN, GPU, WaveNet, LLM 계보 설명이 9.1, 9.2의 경계와 충돌하지 않는지 확인한다.

## 이관한 기존 메모

- `section-01-evidence-analysis.md`
- `section-02-evidence-analysis.md`
- `section-03-evidence-analysis.md`
- `section-2-1-evidence-analysis.md`
- `section-5-3-evidence-analysis.md`
- `section-6-1-evidence-analysis.md`
- `section-6-2-evidence-analysis.md`
- `section-6-3-evidence-analysis.md`
- `section-7-1-evidence-analysis.md`
- `section-7-2-evidence-analysis.md`
- `section-7-3-evidence-analysis.md`
- `section-7-4-evidence-analysis.md`
- `section-8-1-evidence-analysis.md`
- `section-8-2-evidence-analysis.md`
- `section-8-3-evidence-analysis.md`
- `section-9-1-evidence-analysis.md`
- `section-9-2-evidence-analysis.md`

## 현재 결정

- Chapter 6과 7의 용어 경계는 별도 보충학습을 추가하지 않고 현재 본문에서 닫습니다.
- `uncertainty`, `probability`, `stochastic`, `randomness`, `nondeterminism`은 Chapter 6에서 기본 구분을 세우고, 휴리스틱과 확률 모델의 차이는 Chapter 7에서 다시 분리하는 현재 구조를 유지합니다.
- Part 5의 생성 확률과 프롬프트 휴리스틱도 `모델 내부 확률`, `운영 임계값`, `사람이 정한 입력 전략`을 분리해 읽는 현재 용어 경계와 맞는 것으로 봅니다.
- `calibration`, `confidence`, `uncertainty estimation`은 Part 1에서 모두 세부 이론으로 확장하지 않습니다. Part 1에서는 Chapter 6과 7에서 `확률처럼 보이는 점수`, `보정(calibration)`, `운영 임계값(threshold)`의 자리만 먼저 잡고, ROC/PR/log loss/calibration/reliability diagram/Brier score의 첫 해설은 P3-6.4 보충학습으로, threshold와 calibration의 서비스 판단 연결은 P3-15.3으로 회수하는 현재 구조를 유지합니다.
- Chapter 9의 직접 계보/주변 근거 구분도 현재 본문으로 닫습니다.
- CNN, GPU, YOLO, WaveNet은 Part 1에서 `딥러닝 확산의 주변 근거`로 유지하고, Part 4의 CNN/Transformer, Part 5의 GPT/BERT/LLM 본류 설명은 `직접 계보` 쪽에 두는 현재 구조가 서로 충돌하지 않는 것으로 봅니다.
- 생성형 AI는 `무엇을 생성하는가`를 기준으로 묶는 더 넓은 범주로 두고, LLM은 그 안의 언어 모델 계열로 둡니다. Part 5에서는 이 경계를 `토큰 -> Transformer -> GPT` 본류와 `LLM 발전사`, `BERT 계열 비교` 배경 축으로 다시 읽는 현재 구조를 유지합니다.
- `추론`은 Part 1에서 먼저 `inference = 모델 실행`, `reasoning = 사고 과정`, `prediction = 모델 출력`, `generation = 생성`, `statistical inference = 통계적 추론`으로 나눠 둡니다. Part 5에서는 next-token prediction, reasoning처럼 보이는 생성 텍스트, 평가 문맥에서 이 경계를 그대로 다시 사용합니다.

## 이번 반영

- Part 1 index와 summary에 Chapter 6, 7이 `불확실성/확률/확률적 과정`과 `휴리스틱/확률 모델` 경계를 Part 1 안에서 먼저 닫는다는 판단을 명시했습니다.
- 체크리스트에서 Chapter 6의 확률 관련 용어 경계 정리 항목과 Chapter 7의 휴리스틱/확률 모델 분리 항목을 완료 처리했습니다.
- Part 1 index와 summary에 9장이 `직접 계보`와 `주변 근거`를 나눠 Part 4, Part 5와 충돌하지 않게 읽는다는 판단을 덧붙였습니다.
- 체크리스트에서 `CNN, GPU, WaveNet, LLM 계보 설명이 9.1, 9.2 경계와 충돌하지 않는지 확인` 항목을 완료 처리했습니다.
- Part 1 index와 summary에 생성형 AI는 더 넓은 범주이고 LLM은 그 안의 언어 모델 계열이라는 경계를 명시했습니다.
- 체크리스트에서 생성형 AI와 LLM 관계를 Part 5의 GPT/BERT/LLM 계보 기준으로 다시 정리하는 항목을 완료 처리했습니다.
- Part 1 index와 summary에 `추론` 관련 최소 기억점을 추가해 inference, reasoning, prediction, generation, statistical inference를 먼저 나눠 읽게 했습니다.
- 체크리스트에서 `추론` 용어를 Part 1의 모델 실행 문맥과 Part 5의 생성/평가 문맥까지 포함해 다시 점검하는 항목을 완료 처리했습니다.
- Part 1 index와 summary에 `calibration`, `confidence`, `uncertainty estimation`의 세부 설명은 Part 3 평가 장과 보충학습에서 회수한다는 범위 결정을 반영했습니다.
- 체크리스트에서 `calibration`, `confidence`, `uncertainty estimation` 차이를 어디서 정리할지 결정하는 항목을 완료 처리했습니다.
