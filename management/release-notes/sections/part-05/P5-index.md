# Section Release Note

- Section ID: `P5-index`
- Source File: `docs/parts/part-05/index.md`

### v2026.07.20
- 저작권 검토: Part 5 index 순차 검토 범위에서 Part 5 학습 경로, 주요 구조 축, 범위 안내, 후반부 구조 전환 표, 완료 기준, 체크리스트, 출처와 참고 자료 문단을 확인했다. 본문은 Part 5 내부 내용을 안내하는 자체 개요로 판단했다.
- 출처 사용 점검: 본문에 외부 URL, 외부 도표·표·코드·데이터 재사용, 직접 인용은 확인하지 않았다. 하단 출처 문단도 외부 자료 직접 인용이 없다고 명시되어 있어 저작권 검토 결과와 일치한다.
- 관련 자산: `docs/assets/part-05/part5-learning-map-ko.mmd`는 Part 5 학습 순서를 요약한 한국어 자체 Mermaid 도식으로 판단했다.
- 본문 반영: 한국어 원문 `Version`을 `v2026.07.20`으로 갱신했다.
- 번역 동기화 메모: 영어·중국어 간체 번역본의 Version, Part 5 6개 축 구조, 개념사전 상대 링크, `손실 -> gradient -> 역전파/자동미분 -> 계산 확장 -> 구조 분기 -> 생성과 샘플링` 흐름을 원문 기준 `v2026.07.20`까지 동기화했다.
- 번역 반영 상태: 영문/중문 번역 반영 완료
- 원문 기준 버전: `v2026.07.20`

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

### v2026.07.16
- 변경 이유: Part 5 목차 개편에서 초중반 흐름을 `출력/손실/역전파`가 아니라 `출력과 손실 -> 손실에서 gradient로 -> 학습 루프와 안정화 -> 계산 확장 -> 표현 학습과 구조 분기`로 다시 잡을 필요가 생겼다.
- 본문 반영: Part 5 개요의 학습 순서, 학습 절차 설명, 완료 기준을 `손실에서 gradient로`, `역전파와 자동미분`, `계산 확장`, `표현 학습과 구조 분기` 중심으로 갱신했다.
- 번역 동기화 메모: Future translations should update the Part 5 overview around the new loss-to-gradient and computation-scaling sequence. English and Simplified Chinese overview pages are not yet updated.
- 번역 반영 상태: 향후 번역 반영 필요
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.16`

### v2026.07.16-2
- 변경 이유: Part 5 공개 목차가 6개 모듈 축으로 재정렬되면서 Part 시작 페이지의 학습 순서도 같은 구조를 보여 주어야 했다.
- 본문 반영: Part 5 개요의 초반 학습 순서를 `신경망의 기본 계산 구조 -> 출력과 손실 신호 -> 학습 루프와 안정화 -> 계산 확장 -> 표현 학습과 구조 분기 -> 생성 모델과 샘플링` 흐름으로 압축했다.
- 번역 동기화 메모: Future translations should align the Part 5 overview with the six-module restructuring. English and Simplified Chinese overview pages are not yet updated.
- 번역 반영 상태: 향후 반영 필요
- 관련 자산: 없음
- 원문 기준 버전: `v2026.07.16`

### v2026.07.17
- 본문 반영: Part 5 시작 페이지의 `설명하는 범위와 설명하지 않을 범위`에서 생략 항목 목록을 걷어내고, 이 Part가 실제로 회수하는 `구조 -> 손실과 gradient -> 학습 안정화 -> 계산 확장 -> 구조 분기 -> 생성과 샘플링` 축이 먼저 보이도록 다시 정리했다.
- 추가 반영: 시작 페이지 범위 안내가 개별 장과 같은 handoff 원칙을 따르도록, Section들에서 실제로 닫히는 학습 흐름 중심 문장으로 바꿨다.
- 번역 동기화 메모: Future translations should preserve the Part 5 overview as a map of the actual recovery axes rather than a list of omitted advanced topics.
