# Section Release Note

- Section ID: `REFERENCE-concept-glossary`
- Source File: `docs/reference/concept-glossary.md`

### v2026.07.16

- 변경 이유: Part 5 개편을 파일 경로와 Section ID까지 반영하면서 개념사전의 중심 Section과 등장 Section도 새 위치에 맞춰야 했다.
- 본문 반영: `배치(batch)`, `배치 정규화(batch normalization)`, `수치 안정성(numerical stability)`, `초기화(initialization)`, `평가 모드(evaluation mode)`, `학습 모드(training mode)` 관련 Section 참조를 새 P5-6/P5-8 구조에 맞게 갱신했다.
- 번역 반영 상태: 향후 번역 반영 필요

### v2026.07.10

- 변경 이유: `P3-2.1` 등에서 `#glossary-dataset`으로 직접 링크를 거는데, `데이터셋(dataset)` 표제어에는 명시적 앵커가 없어 링크 안정성이 heading slug에 의존하고 있었다.
- 본문 반영: `데이터셋(dataset)` 표제어 앞에 `<a id="glossary-dataset"></a>`를 추가해, 개념사전 직접 링크가 다른 핵심 표제어와 같은 방식으로 안정적으로 동작하도록 맞췄다.
- 번역 반영 상태: 향후 번역 반영 필요

### v2026.07.08

- 변경 이유: Part 4 Chapter 7 재배치 이후 특징 선택 관련 보충학습의 등장 Section 번호가 바뀌어 개념사전 참조 위치를 다시 맞출 필요가 있었다.
- 본문 반영: `특징 선택(feature selection)` 항목과 `차원 축소(dimensionality reduction)` 항목의 등장 Section 목록에 `P4-7.4`를 반영해, 필터·래퍼·차원 축소 구분 보충학습의 새 번호 체계를 맞췄다.

### v2026.07.11

- 변경 이유: Part 5에 학습 안정화 보충학습 `P5-6.3`이 추가되면서, 해당 절의 핵심 용어인 `배치 정규화(batch normalization)`, `수치 안정성(numerical stability)`, `초기화(initialization)`를 개념사전에서도 바로 다시 찾을 수 있어야 했다.
- 본문 반영: 개념사전에 `배치 정규화(batch normalization)`, `수치 안정성(numerical stability)`, `초기화(initialization)` 항목을 추가하고 중심 Section을 `P5-6.3`으로 연결했다.
- 번역 반영 상태: 향후 번역 반영 필요
