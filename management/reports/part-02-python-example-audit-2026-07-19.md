# Part 2 Python 예제 점검 리포트

- 작성일: 2026-07-19
- 점검 범위: `docs/parts/part-02/` 한국어 본문 Section 63개, `docs/assets/part-02/` Python 자산 7개
- 기준 문서: `management/guidelines/python-example-guidelines.md`, `management/guidelines/manuscript-writing-workflow.md`, `management/guidelines/section-metadata-guidelines.md`

## 점검 목적

Part 2의 Python 예제가 초심자에게 실제로 실행해 볼 만한 학습 활동인지, 또는 이미 정해진 답을 코드가 단순 출력하거나 집계만 하는 형태인지 확인했다. 특히 검색 결과, 추천 후보, 후보 점수처럼 이미 라벨이나 점수가 고정된 목록을 두고 코드가 기준 이상 항목만 고르는 예시는 실험형 코드로 보기 어렵기 때문에 별도 위험 항목으로 점검했다.

Part 2는 수학·통계·Python·NumPy·데이터 준비의 기초를 복구하는 파트이므로, 모든 코드가 모델 실험일 필요는 없다. 문법, 자료구조, 배열 shape, 인덱싱, 브로드캐스팅, 파일 저장처럼 도구 자체를 설명하는 코드는 `설명형 예제`로 유지할 수 있다. 다만 AI 판단이나 검색 성능을 실험하는 것처럼 보이는 코드는 입력을 바꿔 결과가 달라지거나, 코드 대신 표와 해석으로 처리되어야 한다.

## 수량 점검

| 항목 | 결과 |
| --- | ---: |
| 한국어 본문 Section 수 | 63 |
| Python 코드 블록이 있는 Section 수 | 39 |
| 수정 후 Python 코드 블록 수 | 306 |
| Part 2 Python 자산 수 | 7 |

Python 코드 블록 수는 P2-9.3에서 후보 점수 필터링 코드 1개를 제거한 뒤의 값이다.

## 판정 요약

| 판정 | 범위 | 처리 |
| --- | --- | --- |
| 설명형 유지 | Chapter 7, Chapter 8의 실행 환경, 변수, 조건문, 반복문, 함수, 리스트·딕셔너리 예제 | Python 자체를 배우는 구간이므로 짧은 출력 확인 코드를 유지 |
| 실험형 유지 | P2-5.4, P2-11.1, P2-11.2, P2-11.3, P2-12.1, P2-12.2, P2-12.3, P2-13.1, P2-13.2, P2-13.3 | 데이터, shape, 열 선택, 시각화 결과를 바꿔 확인할 수 있어 유지 |
| 표 대체 | P2-9.3의 검색 후보 유사도 기준 필터링 코드 | 이미 계산된 후보 점수를 코드가 기준으로 걸러 출력하는 형태라 표와 해석 문장으로 대체 |
| 자산 보정 | P2-5.2 분포·평균·분산 차트 생성 스크립트 | Linux 검증 환경에서 한글/CJK 글리프 경고가 나지 않도록 Noto Sans CJK 폰트 후보 추가 |

## 수정 내역

### P2-9.3 검색 후보 점수 예시

`docs/parts/part-02/chapter-09/section-03.md`의 후보 점수 예시는 `doc_a`, `doc_b`, `doc_c`에 유사도 점수가 이미 들어 있고, Python 코드는 `0.7` 이상인 항목만 출력했다. 이 코드는 검색 시스템을 구현하거나 점수 계산을 실험하는 예제가 아니라, 이미 만들어진 점수표를 필터링하는 코드였다.

따라서 해당 코드 블록을 제거하고, 후보 문서·점수·기준선 비교·해석을 보여 주는 Markdown 표로 대체했다. 본문도 `Python 실험`이 아니라 `이미 계산된 관계 점수를 기준선과 비교해 해석하는 예시`라고 명확히 정리했다.

릴리즈노트는 `management/release-notes/sections/part-02/P2-9.3.md`의 `v2026.07.19`에 반영했다.

### P2-5.2 차트 자산 스크립트

`docs/assets/part-02/chapter-05/p2_5_2_distribution_mean_variance.py` 실행 중 DejaVu Sans에 한글·중국어 글리프가 없어 경고가 발생했다. 검증 환경에는 Noto CJK 폰트가 설치되어 있었지만, 스크립트 후보 목록에 없어서 사용되지 못했다.

한국어 후보에 `Noto Sans CJK KR`, 중국어 후보에 `Noto Sans CJK SC`를 추가하고 PNG를 재생성했다. 재실행 결과 글리프 경고 없이 종료됐다.

릴리즈노트는 `management/release-notes/sections/part-02/P2-5.2.md`의 `v2026.07.19`에 반영했다.

## 자산 스크립트 실행 결과

| 파일 | 결과 | 비고 |
| --- | --- | --- |
| `docs/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py` | 성공 | 벡터·행렬 shape와 행렬곱 출력 확인 |
| `docs/assets/part-02/chapter-05/p2_5_2_distribution_mean_variance.py` | 성공 | 폰트 후보 보강 후 경고 없이 PNG 재생성 |
| `docs/assets/part-02/chapter-05/p2_5_4_small_statistics.py` | 성공 | 평균·중앙값·분산·샘플 평균 출력 확인 |
| `docs/assets/part-02/chapter-11/p2_11_1_numpy_arrays.py` | 성공 | 배열 shape, 행렬곱, 리스트/배열 차이 출력 확인 |
| `docs/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py` | 성공 | 인덱싱, 슬라이싱, 축별 집계 출력 확인 |
| `docs/assets/part-02/chapter-11/p2_11_3_broadcast_vectorization.py` | 성공 | 브로드캐스팅 성공/실패와 벡터화 결과 출력 확인 |
| `docs/assets/part-02/chapter-13/p2_13_3_compare_and_save.py` | 성공 | 학습 곡선 비교 PNG 생성 확인 |

## 검증 명령

```bash
find docs/parts/part-02 -name 'section-[0-9][0-9].md' | sort | wc -l
rg -n '^```python' docs/parts/part-02 -g 'section-[0-9][0-9].md' | cut -d: -f1 | sort -u | wc -l
rg -n '^```python' docs/parts/part-02 -g 'section-[0-9][0-9].md' | wc -l
find docs/assets/part-02 -name '*.py' | sort
.venv/bin/python docs/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py
.venv/bin/python docs/assets/part-02/chapter-05/p2_5_2_distribution_mean_variance.py
.venv/bin/python docs/assets/part-02/chapter-05/p2_5_4_small_statistics.py
.venv/bin/python docs/assets/part-02/chapter-11/p2_11_1_numpy_arrays.py
.venv/bin/python docs/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py
.venv/bin/python docs/assets/part-02/chapter-11/p2_11_3_broadcast_vectorization.py
.venv/bin/python docs/assets/part-02/chapter-13/p2_13_3_compare_and_save.py
```

## 남은 위험

Part 2에는 Python 자체를 가르치는 설명형 코드가 많다. 이 코드는 고정 출력이 있어도 문법과 자료구조 확인이 목적이므로 현재 기준에서는 유지하는 것이 맞다. 다만 향후 목표가 `설명형 코드 최소화`로 바뀐다면 Chapter 7, Chapter 8의 짧은 문법 예제 일부는 본문 설명이나 표로 더 줄일 수 있다.

이번 점검 기준에서 즉시 수정이 필요했던 항목은 P2-9.3의 후보 점수 필터링 코드 1건이었다. 실행 검증 중 발견된 P2-5.2 차트 폰트 문제도 함께 보정했다.
