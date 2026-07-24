# Part 6 영문·중국어 간체 번역 준비 노트

작성일: 2026-07-24

이 문서는 Part 6 한국어 원문을 영어와 중국어 간체로 옮기기 전에 확인해야 할 대상, 순서, 자산 상태를 정리한다. 실제 번역 기준은 `management/guidelines/english-translation-guidelines.md`와 `management/guidelines/chinese-translation-guidelines.md`를 따른다.

## 현재 상태

- 기준 브랜치: `dev`
- 기준 원문 위치: `docs/parts/part-06/`
- 기준 릴리즈노트 위치: `management/release-notes/sections/part-06/`
- Part 시작/마무리 번역 파일은 이미 있으나, 한국어 원문 최신 버전과 맞지 않는다.
  - `docs/parts/part-06/index.md`: `v2026.07.24`
  - `docs/parts/part-06/index.en.md`: `v2026.07.21`
  - `docs/parts/part-06/index.zh.md`: `v2026.07.21`
  - `docs/parts/part-06/summary.md`: `v2026.07.24`
  - `docs/parts/part-06/summary.en.md`: `v2026.07.21`
  - `docs/parts/part-06/summary.zh.md`: `v2026.07.21`
- Section 본문 번역 파일은 아직 없다.
  - 한국어 Section: 54개
  - 영어 Section 파일: 0개
  - 중국어 간체 Section 파일: 0개
- Part 6 자산은 `-ko`, `-en` 쌍이 많이 준비되어 있다.
  - `docs/assets/part-06/`의 `*-ko.*`: 243개
  - `docs/assets/part-06/`의 `*-en.*`: 242개
  - `docs/assets/part-06/`의 `*-zh.*`: 0개

## 작업 원칙

- 영어 파일은 한국어 원문과 같은 폴더에 `section-XX.en.md`로 둔다.
- 중국어 간체 파일은 한국어 원문과 같은 폴더에 `section-XX.zh.md`로 둔다.
- 각 번역본의 `Section ID`와 `Version`은 대응 한국어 원문과 같은 값을 쓴다.
- 번역본을 만들 때 별도 릴리즈노트 파일을 만들지 않는다. 기존 공통 릴리즈노트에 `번역 동기화 메모`, `번역 반영 상태`, `원문 기준 버전`을 갱신한다.
- 한국어 원문에 없는 주장, 사례, 판단 기준을 번역본에서 임의로 추가하지 않는다.
- 번역 검수 때 한국어 원문과 번역본의 빈 줄 제외 라인 수 차이가 5% 이상이면 누락·과축약 여부를 먼저 확인한다.
- 영어 본문은 기존 `-en` Mermaid/PNG 자산을 우선 사용한다.
- 중국어 간체 본문은 `-zh` 자산이 아직 없으므로 다음 중 하나로 처리한다.
  - 본문 이해에 꼭 필요한 도식은 `-zh` 자산을 새로 만든다.
  - 공용 영문 자산으로도 학습 흐름이 유지되면 본문에서 영어 라벨을 풀어 설명한다.
  - 한국어 라벨 자산을 중국어 본문에 그대로 연결하지 않는다.

## 우선순위

1. `P6-index`, `P6-summary`의 영어·중국어 간체 파일을 한국어 `v2026.07.24`에 맞춰 먼저 갱신한다.
2. Module 1부터 순서대로 Section 번역 파일을 만든다. Part 6은 생성형 AI 산출물에서 시작하는 구조로 개편되었으므로, 앞쪽 Module의 용어와 연결 문장이 뒤쪽 번역 기준이 된다.
3. 자산 의존이 큰 Section은 번역 전에 도식 상태를 먼저 확인한다.
   - Chapter 2-4: 토큰, 임베딩, Transformer, attention 관련 Mermaid/PNG
   - Chapter 10-12: 프롬프트, RAG, 벡터 DB 관련 Mermaid/PNG
   - Chapter 13-17: 도구, 함수 호출, 에이전트, MCP, 하네스, 평가, 운영 관련 Mermaid/PNG
4. 각 Section 번역 후 공통 릴리즈노트에 번역 반영 상태를 바로 남긴다.

## 번역 대상 목록

| 순서 | Section ID | 한국어 원문 | Version | 영어 파일 | 중국어 간체 파일 | 상태 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | P6-index | `docs/parts/part-06/index.md` | `v2026.07.24` | 있음, 최신 | 있음, 업데이트 필요 | 영문 완료 |
| 1 | P6-1.1 | `docs/parts/part-06/chapter-01/section-01.md` | `v2026.07.23` | 있음, 최신 | 없음 | 영문 완료 |
| 2 | P6-1.2 | `docs/parts/part-06/chapter-01/section-02.md` | `v2026.07.23` | 있음, 최신 | 없음 | 영문 완료 |
| 3 | P6-1.3 | `docs/parts/part-06/chapter-01/section-03.md` | `v2026.07.22` | 있음, 최신 | 없음 | 영문 완료 |
| 4 | P6-2.1 | `docs/parts/part-06/chapter-02/section-01.md` | `v2026.07.23` | 있음, 최신 | 없음 | 영문 완료 |
| 5 | P6-2.2 | `docs/parts/part-06/chapter-02/section-02.md` | `v2026.07.23` | 있음, 최신 | 없음 | 영문 완료 |
| 6 | P6-2.3 | `docs/parts/part-06/chapter-02/section-03.md` | `v2026.07.24` | 있음, 최신 | 없음 | 영문 완료 |
| 7 | P6-2.4 | `docs/parts/part-06/chapter-02/section-04.md` | `v2026.07.23` | 있음, 최신 | 없음 | 영문 완료 |
| 8 | P6-2.5 | `docs/parts/part-06/chapter-02/section-05.md` | `v2026.07.24` | 있음, 최신 | 없음 | 영문 완료 |
| 9 | P6-3.1 | `docs/parts/part-06/chapter-03/section-01.md` | `v2026.07.24` | 있음, 최신 | 없음 | 영문 완료 |
| 10 | P6-3.2 | `docs/parts/part-06/chapter-03/section-02.md` | `v2026.07.24` | 있음, 최신 | 없음 | 영문 완료 |
| 11 | P6-3.3 | `docs/parts/part-06/chapter-03/section-03.md` | `v2026.07.23` | 있음, 최신 | 없음 | 영문 완료 |
| 12 | P6-3.4 | `docs/parts/part-06/chapter-03/section-04.md` | `v2026.07.24` | 있음, 최신 | 없음 | 영문 완료 |
| 13 | P6-4.1 | `docs/parts/part-06/chapter-04/section-01.md` | `v2026.07.23` | 있음, 최신 | 없음 | 영문 완료 |
| 14 | P6-4.2 | `docs/parts/part-06/chapter-04/section-02.md` | `v2026.07.24` | 있음, 최신 | 없음 | 영문 완료 |
| 15 | P6-4.3 | `docs/parts/part-06/chapter-04/section-03.md` | `v2026.07.23` | 있음, 최신 | 없음 | 영문 완료 |
| 16 | P6-4.4 | `docs/parts/part-06/chapter-04/section-04.md` | `v2026.07.23` | 있음, 최신 | 없음 | 영문 완료 |
| 17 | P6-4.5 | `docs/parts/part-06/chapter-04/section-05.md` | `v2026.07.23` | 있음, 최신 | 없음 | 영문 완료 |
| 18 | P6-5.1 | `docs/parts/part-06/chapter-05/section-01.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 19 | P6-5.2 | `docs/parts/part-06/chapter-05/section-02.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 20 | P6-6.1 | `docs/parts/part-06/chapter-06/section-01.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 21 | P6-6.2 | `docs/parts/part-06/chapter-06/section-02.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 22 | P6-7.1 | `docs/parts/part-06/chapter-07/section-01.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 23 | P6-7.2 | `docs/parts/part-06/chapter-07/section-02.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 24 | P6-8.1 | `docs/parts/part-06/chapter-08/section-01.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 25 | P6-8.2 | `docs/parts/part-06/chapter-08/section-02.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 26 | P6-9.1 | `docs/parts/part-06/chapter-09/section-01.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 27 | P6-9.2 | `docs/parts/part-06/chapter-09/section-02.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 28 | P6-9.3 | `docs/parts/part-06/chapter-09/section-03.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 29 | P6-9.4 | `docs/parts/part-06/chapter-09/section-04.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 30 | P6-9.5 | `docs/parts/part-06/chapter-09/section-05.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 31 | P6-10.1 | `docs/parts/part-06/chapter-10/section-01.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 32 | P6-10.2 | `docs/parts/part-06/chapter-10/section-02.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 33 | P6-10.3 | `docs/parts/part-06/chapter-10/section-03.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 34 | P6-10.4 | `docs/parts/part-06/chapter-10/section-04.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 35 | P6-11.1 | `docs/parts/part-06/chapter-11/section-01.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 36 | P6-11.2 | `docs/parts/part-06/chapter-11/section-02.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 37 | P6-12.1 | `docs/parts/part-06/chapter-12/section-01.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 38 | P6-12.2 | `docs/parts/part-06/chapter-12/section-02.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 39 | P6-13.1 | `docs/parts/part-06/chapter-13/section-01.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 40 | P6-13.2 | `docs/parts/part-06/chapter-13/section-02.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 41 | P6-14.1 | `docs/parts/part-06/chapter-14/section-01.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 42 | P6-14.2 | `docs/parts/part-06/chapter-14/section-02.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 43 | P6-15.1 | `docs/parts/part-06/chapter-15/section-01.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 44 | P6-15.2 | `docs/parts/part-06/chapter-15/section-02.md` | `v2026.07.23` | 있음 | 최신 | 영문 완료 |
| 45 | P6-16.1 | `docs/parts/part-06/chapter-16/section-01.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 46 | P6-16.2 | `docs/parts/part-06/chapter-16/section-02.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 47 | P6-17.1 | `docs/parts/part-06/chapter-17/section-01.md` | `v2026.07.24` | 있음 | 최신 | 영문 완료 |
| 48 | P6-17.2 | `docs/parts/part-06/chapter-17/section-02.md` | `v2026.07.24` | 없음 | 없음 | 신규 번역 |
| 49 | P6-18.1 | `docs/parts/part-06/chapter-18/section-01.md` | `v2026.07.23` | 없음 | 없음 | 신규 번역 |
| 50 | P6-18.2 | `docs/parts/part-06/chapter-18/section-02.md` | `v2026.07.23` | 없음 | 없음 | 신규 번역 |
| 51 | P6-19.1 | `docs/parts/part-06/chapter-19/section-01.md` | `v2026.07.24` | 없음 | 없음 | 신규 번역 |
| 52 | P6-19.2 | `docs/parts/part-06/chapter-19/section-02.md` | `v2026.07.24` | 없음 | 없음 | 신규 번역 |
| 53 | P6-20.1 | `docs/parts/part-06/chapter-20/section-01.md` | `v2026.07.23` | 없음 | 없음 | 신규 번역 |
| 54 | P6-20.2 | `docs/parts/part-06/chapter-20/section-02.md` | `v2026.07.24` | 없음 | 없음 | 신규 번역 |
| 55 | P6-summary | `docs/parts/part-06/summary.md` | `v2026.07.24` | 있음, 최신 | 있음, 업데이트 필요 | 영문 완료 |

## Module별 번역 주의점

| Module | Section 범위 | 번역 시 고정할 축 |
| --- | --- | --- |
| Module 1 | P6-1.1-P6-1.3 | 생성형 AI 출력은 정답 표시가 아니라 검토해야 할 산출물이라는 출발점 |
| Module 2 | P6-2.1-P6-2.5 | 토큰, token ID, 토큰화, 비용, 청크, 토크나이저 계열의 층위 구분 |
| Module 3 | P6-3.1-P6-3.4 | 임베딩은 정답이 아니라 가까운 후보와 검색 후보를 만드는 표현이라는 점 |
| Module 4 | P6-4.1-P6-4.5 | Transformer, attention, KV cache, 긴 문맥을 다음 후보 생성 구조로 읽는 흐름 |
| Module 5 | P6-5.1-P6-12.2 | 프롬프트로 조정할 문제와 RAG·벡터 DB로 넘길 문제의 경계 |
| Module 6 | P6-13.1-P6-15.2 | tool use, function calling, agent, MCP, harness의 실행 층위 구분 |
| Module 7 | P6-16.1-P6-18.2 | 자연스러운 답변과 서비스 가능한 결과의 평가·운영·기록 차이 |
| Module 8 | P6-19.1-P6-20.2 | LLM 발전사와 BERT 계열은 GPT 중심 본류를 보정하는 배경 지도 |

## 번역 시작 전 체크

- [x] `P6-index.en.md`, `P6-summary.en.md`를 `v2026.07.24` 기준으로 업데이트한다.
- [ ] `P6-index.zh.md`, `P6-summary.zh.md`를 `v2026.07.24` 기준으로 업데이트한다.
- [ ] Section별 신규 번역 파일을 만들 때 제목, `Section ID`, `Version`을 원문과 먼저 맞춘다.
- [ ] 영어판에서 내부 링크가 있으면 대응 `*.en.md`가 실제 존재하는지 확인한다.
- [ ] 중국어 간체판에서 내부 링크가 있으면 대응 `*.zh.md`가 실제 존재하는지 확인한다.
- [ ] 도식 링크는 영어판은 `-en`, 중국어 간체판은 가능한 `-zh` 또는 본문 해설 대체 기준으로 처리한다.
- [ ] 각 Section 번역 후 공통 릴리즈노트에 번역 반영 상태를 기록한다.
- [ ] 번역 배치가 끝난 뒤 `.venv/bin/python -m mkdocs build`로 한 번에 확인한다.
