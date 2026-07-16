# Section Release Note

- Section ID: `P5-index`
- Source File: `docs/parts/part-05/index.md`

### v2026.07.12
- 본문 반영: 집필 순서만 예고하는 `다음 ... 연결` 계열 표지를 제거했다. 본문 메타데이터 버전도 함께 갱신했다.
- 번역 동기화 메모: 영어판과 중국어 간체판에 같은 메타 표지 제거, 현재 checklist 구조, Part 5 시작 페이지의 최신 설명 흐름을 반영했다. 추가로 중국어 공개 본문이 `part5-learning-map-zh.mmd`를 직접 참조하도록 자산 운영을 현재 차트 가이드라인에 맞췄다. / reflected in English and Simplified Chinese on 2026-07-12, with the Simplified Chinese page now referencing its own `-zh` Mermaid asset

### v2026.07.07-1
- 본문 반영: 후반 표와 문단의 CNN, RNN, Attention, Transformer, gradient, optimizer, decoding 등을 한국어 우선 병기 중심으로 정리했다.
- 번역 동기화 메모: Korean-first terminology was reinforced across the latter half of the Part 5 overview page. / wording change only. / pending

### v2026.07.07-2
- 본문 반영: `instruction tuning`, `RAG`, `tool use`, `agent`, `Attention`, `Transformer`, `decoding` 등을 한국어 우선 병기로 정리하고, 다음 Part 연결 문단의 용어 묶음도 같은 기준으로 맞췄다.
- 번역 동기화 메모: Korean-first terminology was reinforced again in the Part 5 overview bridge sections. / wording change only. / pending

### v2026.07.11
- 본문 반영: Part 시작 페이지 하단의 `짧은 점검` 표지를 `체크리스트`로 통일해 Part 단위 자기 확인 구조를 현재 기준과 맞췄다.
- 추가 반영: 학습 밀도 검토 결과를 반영해, 후반부 구조 전환을 `순차 상태 -> 직접 참조 -> 병렬 블록 -> 생성 후보 선택`으로 다시 묶는 짧은 문단과 표를 추가했다.
- 번역 동기화 메모: Part-level self-check label was aligned to the shared `checklist` convention. / wording change only. / pending

### v2026.07.11-2
- 본문 반영: `신경망 기초 -> 학습과 확장 -> 구조 분기 -> 생성` 흐름을 압축한 Mermaid 도식을 추가했다.
- 번역 동기화 메모: Keep the English Mermaid source aligned with the Korean public include target. / pending

### v2026.07.12-diagram
- 번역 동기화 메모: The Korean learning-map asset now localizes the remaining attention/Transformer labels while preserving the same chapter-flow structure. Future translations should keep language-specific labels on their own asset files.

### v2026.07.12-zh-link
- 번역 반영: `index.zh.md`의 개념사전 복귀 링크를 상대경로 `concept-glossary.md`에서 언어 전환이 명시된 영어 개념사전 절대경로 `/AiBook/en/reference/concept-glossary/`로 바꿨다.
