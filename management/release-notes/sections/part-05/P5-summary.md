# Section Release Note

- Section ID: `P5-summary`
- Source File: `docs/parts/part-05/summary.md`

### v2026.07.07-1

- 변경 이유: Part 마무리 페이지 후반 질문과 연결 문단에 영어 표면형 중심 용어 묶음이 남아 있어, 본문에서 맞춘 한국어 우선 병기 기준이 다시 약해지고 있었음.
- 본문 반영: 후반 점검 질문과 다음 Part 연결 문단의 Transformer, attention, optimizer, regularization, instruction tuning, RAG, agent 등을 한국어 우선 병기로 정리했다.
- 번역 동기화 메모: Korean-first terminology was reinforced across the latter half of the Part 5 summary page. / wording change only. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-2

- 변경 이유: Part 마무리 페이지가 다음 Part의 새 핵심 개념을 이름 중심으로 먼저 도입해 Part 경계를 흐리고 있었음.
- 본문 반영: `RAG`, `agent`, `GPT`, `BERT` 등 다음 Part의 개별 개념명을 일반적인 연결 표현으로 낮추어, Part 5 마무리가 현재 Part 요약과 다음 단계 방향만 남기도록 조정했다.
- 번역 동기화 메모: Summary-page bridge wording was generalized to avoid introducing next-part concepts prematurely. / wording change only. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.11

- 변경 이유: Part 5 커리큘럼 적합성 재점검에서 Part 마무리 페이지의 자기 확인 표지가 AGENTS의 `체크리스트` 규칙과 어긋나 있었다.
- 본문 반영: Part 마무리 페이지 하단의 `짧은 점검` 표지를 `체크리스트`로 통일해 Part 단위 자기 확인 구조를 현재 기준과 맞췄다.
- 추가 반영: 학습 밀도 검토 결과를 반영해, 후반부 구조 전환을 `순차 상태 -> 직접 참조 -> 병렬 블록 -> 생성 후보 선택`으로 다시 천천히 묶는 문단과 표를 보강했다.
- 번역 동기화 메모: Part-level self-check label was aligned to the shared `checklist` convention. / wording change only. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.11`

### v2026.07.11-2
- 변경 이유: Part 5 마무리 페이지에서 구조, 학습 절차, 구조 분기, 생성 연결을 한 번에 복습할 수 있는 도식이 필요했다.
- 본문 반영: `표현 변화 -> 손실과 역전파 -> 학습 안정화 -> 구조 분기 -> 생성 결과 선택` 흐름을 압축한 Mermaid 도식을 추가했다.
- 번역 동기화 메모: Keep the English Mermaid source aligned with the Korean public include target. / pending
- 번역 반영 상태: not-started
- 관련 자산: `docs/assets/part-05/part5-recap-flow-en.mmd`, `docs/assets/part-05/part5-recap-flow-ko.mmd`
- 원문 기준 버전: `v2026.07.11`
