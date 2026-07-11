# Section Release Note

- Section ID: `BOOK-toc`
- Source File: `docs/book/table-of-contents.md`

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
