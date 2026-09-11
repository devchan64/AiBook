# Part 2 번역 검수 — 2026-09-08

## 범위와 판정

P2-2.2부터 P2-summary까지 한국어 61개 문서에 대응하는 영어·중국어 122개 파일을 동기화한다. 현재 33개 Section의 양 언어 수정과 구조·수식·코드 대조를 완료했다. 나머지는 이전 원문 기준이며 후속 수정 중이다. 전체 완료로 판정하지 않는다.

## 우선 수정 항목

1. **P2-12.3 입력·분할 예제 불일치**: 양 언어 157~165행에 최종 점수 `score`를 입력에 넣고 전체 표를 인코딩한 뒤 분할하는 이전 코드가 남아 있다. 한국어는 시험 전 예측 시점을 명시하고 수치 특징 3개·27명/9명 분할로 수정했다. 공용 스크립트와도 현재 번역 본문이 다르다.
2. **P2-12.2 동작 시간 해석 오류**: 양 언어 502행은 마지막 관측 시각을 `total_duration_seconds`로 부른다. 진행 비율이 0.40·0.50인 기록으로 전체 완료 시간을 알 수 없다. 한국어의 `last_recorded_seconds`, 시간순 정렬, 관측 범위 설명을 반영해야 한다.
3. **P2-13.1 A·B 설명 반전**: 양 언어 94행은 A가 평평하다고 설명하지만 120~121행 코드는 A가 오르내리고 B가 일정하다. 한국어에서 바로잡은 대응을 반영해야 한다.
4. **반복 진행 메타 잔존**: 한국어에서 삭제한 도입·학습 수준 표·진행 안내가 번역본에 남아 있다. 문구만 다듬기보다 현재 한국어 문단·표·사례 구조에 맞춰 재대조해야 한다.

## 파일별 구조 대조

라인 수는 누락 신호일 뿐 번역 충실도의 증명이 아니다. 원문에서 삭제한 문장이 번역본에 남아 길이가 길어도 통과로 판정하지 않는다.

| 번역 파일 | 원문 라인 | 번역 라인 | 원문 H2 | 번역 H2 | 판정 |
| --- | ---: | ---: | ---: | ---: | --- |
| `docs/parts/part-02/chapter-02/section-02.en.md` | 201 | 201 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-02/section-02.zh.md` | 201 | 201 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-02/section-03.en.md` | 152 | 152 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-02/section-03.zh.md` | 152 | 152 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-02/section-04.en.md` | 110 | 110 | 7 | 7 | 동기화 완료 |
| `docs/parts/part-02/chapter-02/section-04.zh.md` | 110 | 110 | 7 | 7 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-01.en.md` | 200 | 200 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-01.zh.md` | 200 | 200 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-02.en.md` | 133 | 133 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-02.zh.md` | 133 | 133 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-03.en.md` | 197 | 197 | 9 | 9 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-03.zh.md` | 197 | 197 | 9 | 9 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-04.en.md` | 89 | 89 | 7 | 7 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-04.zh.md` | 89 | 89 | 7 | 7 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-05.en.md` | 85 | 85 | 8 | 8 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-05.zh.md` | 85 | 85 | 8 | 8 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-06.en.md` | 260 | 260 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-03/section-06.zh.md` | 260 | 260 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-01.en.md` | 37 | 37 | 6 | 6 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-01.zh.md` | 37 | 37 | 6 | 6 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-02.en.md` | 150 | 150 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-02.zh.md` | 150 | 150 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-03.en.md` | 146 | 146 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-03.zh.md` | 146 | 146 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-04.en.md` | 104 | 104 | 11 | 11 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-04.zh.md` | 104 | 104 | 11 | 11 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-05.en.md` | 128 | 128 | 13 | 13 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-05.zh.md` | 128 | 128 | 13 | 13 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-06.en.md` | 50 | 50 | 6 | 6 | 동기화 완료 |
| `docs/parts/part-02/chapter-04/section-06.zh.md` | 50 | 50 | 6 | 6 | 동기화 완료 |
| `docs/parts/part-02/chapter-05/section-01.en.md` | 118 | 118 | 13 | 13 | 동기화 완료 |
| `docs/parts/part-02/chapter-05/section-01.zh.md` | 118 | 118 | 13 | 13 | 동기화 완료 |
| `docs/parts/part-02/chapter-05/section-02.en.md` | 106 | 106 | 11 | 11 | 동기화 완료 |
| `docs/parts/part-02/chapter-05/section-02.zh.md` | 106 | 106 | 11 | 11 | 동기화 완료 |
| `docs/parts/part-02/chapter-05/section-03.en.md` | 111 | 111 | 13 | 13 | 동기화 완료 |
| `docs/parts/part-02/chapter-05/section-03.zh.md` | 111 | 111 | 13 | 13 | 동기화 완료 |
| `docs/parts/part-02/chapter-05/section-04.en.md` | 178 | 178 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-05/section-04.zh.md` | 178 | 178 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-05/section-05.en.md` | 72 | 72 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-05/section-05.zh.md` | 72 | 72 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-06/section-01.en.md` | 105 | 105 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-06/section-01.zh.md` | 105 | 105 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-06/section-02.en.md` | 121 | 121 | 11 | 11 | 동기화 완료 |
| `docs/parts/part-02/chapter-06/section-02.zh.md` | 121 | 121 | 11 | 11 | 동기화 완료 |
| `docs/parts/part-02/chapter-06/section-03.en.md` | 112 | 112 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-06/section-03.zh.md` | 112 | 112 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-01.en.md` | 121 | 121 | 11 | 11 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-01.zh.md` | 121 | 121 | 11 | 11 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-02.en.md` | 166 | 166 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-02.zh.md` | 166 | 166 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-03.en.md` | 126 | 126 | 11 | 11 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-03.zh.md` | 126 | 126 | 11 | 11 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-04.en.md` | 123 | 125 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-04.zh.md` | 123 | 125 | 12 | 12 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-05.en.md` | 174 | 174 | 13 | 13 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-05.zh.md` | 174 | 174 | 13 | 13 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-06.en.md` | 224 | 224 | 14 | 14 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-06.zh.md` | 224 | 224 | 14 | 14 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-07.en.md` | 146 | 146 | 14 | 14 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-07.zh.md` | 146 | 146 | 14 | 14 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-08.en.md` | 97 | 97 | 9 | 9 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-08.zh.md` | 97 | 97 | 9 | 9 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-09.en.md` | 82 | 82 | 9 | 9 | 동기화 완료 |
| `docs/parts/part-02/chapter-07/section-09.zh.md` | 82 | 82 | 9 | 9 | 동기화 완료 |
| `docs/parts/part-02/chapter-08/section-01.en.md` | 139 | 139 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-08/section-01.zh.md` | 139 | 139 | 10 | 10 | 동기화 완료 |
| `docs/parts/part-02/chapter-08/section-02.en.md` | 248 | 393 | 10 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-02.zh.md` | 248 | 393 | 10 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-03.en.md` | 184 | 284 | 10 | 11 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-03.zh.md` | 184 | 284 | 10 | 11 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-04.en.md` | 230 | 521 | 11 | 11 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-04.zh.md` | 230 | 522 | 11 | 11 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-05.en.md` | 244 | 363 | 6 | 8 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-05.zh.md` | 244 | 364 | 6 | 8 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-06.en.md` | 167 | 389 | 9 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-06.zh.md` | 167 | 389 | 9 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-07.en.md` | 108 | 177 | 7 | 8 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-08/section-07.zh.md` | 108 | 177 | 7 | 8 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-09/section-01.en.md` | 132 | 273 | 8 | 12 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-09/section-01.zh.md` | 132 | 273 | 8 | 12 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-09/section-02.en.md` | 205 | 344 | 8 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-09/section-02.zh.md` | 205 | 344 | 8 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-09/section-03.en.md` | 171 | 237 | 11 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-09/section-03.zh.md` | 171 | 237 | 11 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-09/section-04.en.md` | 159 | 437 | 11 | 11 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-09/section-04.zh.md` | 159 | 437 | 11 | 11 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-10/section-01.en.md` | 104 | 219 | 7 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-10/section-01.zh.md` | 104 | 219 | 7 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-10/section-02.en.md` | 126 | 176 | 11 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-10/section-02.zh.md` | 126 | 176 | 11 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-10/section-03.en.md` | 134 | 239 | 13 | 16 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-10/section-03.zh.md` | 134 | 239 | 13 | 16 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-11/section-01.en.md` | 201 | 295 | 9 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-11/section-01.zh.md` | 201 | 295 | 9 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-11/section-02.en.md` | 246 | 317 | 11 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-11/section-02.zh.md` | 246 | 317 | 11 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-11/section-03.en.md` | 166 | 242 | 10 | 12 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-11/section-03.zh.md` | 166 | 242 | 10 | 12 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-11/section-04.en.md` | 107 | 195 | 7 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-11/section-04.zh.md` | 107 | 195 | 7 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-12/section-01.en.md` | 135 | 371 | 8 | 12 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-12/section-01.zh.md` | 135 | 371 | 8 | 12 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-12/section-02.en.md` | 231 | 436 | 10 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-12/section-02.zh.md` | 231 | 436 | 10 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-12/section-03.en.md` | 119 | 267 | 9 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-12/section-03.zh.md` | 119 | 267 | 9 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-13/section-01.en.md` | 142 | 232 | 11 | 12 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-13/section-01.zh.md` | 142 | 232 | 11 | 12 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-13/section-02.en.md` | 115 | 202 | 8 | 12 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-13/section-02.zh.md` | 115 | 202 | 8 | 12 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-13/section-03.en.md` | 99 | 162 | 8 | 11 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-13/section-03.zh.md` | 99 | 162 | 8 | 11 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-14/section-01.en.md` | 107 | 136 | 11 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-14/section-01.zh.md` | 107 | 136 | 11 | 14 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-14/section-02.en.md` | 71 | 131 | 8 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-14/section-02.zh.md` | 71 | 131 | 8 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-15/section-01.en.md` | 106 | 187 | 9 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-15/section-01.zh.md` | 106 | 187 | 9 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-15/section-02.en.md` | 71 | 145 | 8 | 10 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/chapter-15/section-02.zh.md` | 71 | 145 | 8 | 10 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/summary.en.md` | 79 | 165 | 7 | 13 | 이전 버전, 동기화 필요 |
| `docs/parts/part-02/summary.zh.md` | 79 | 165 | 7 | 13 | 이전 버전, 동기화 필요 |
