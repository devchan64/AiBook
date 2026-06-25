# P2-12.2 근거 검토: 선택, 필터링, 집계

확인 날짜: 2026-06-25

## 사용한 주요 자료

| 자료 | 확인 내용 | 반영 위치 |
| --- | --- | --- |
| pandas Developers, `Indexing and selecting data` | `.loc`는 라벨 기반, `.iloc`는 정수 위치 기반 선택으로 설명한다. 불리언 인덱싱(Boolean indexing) 예제도 제공한다. | 열 선택, 행 선택, `loc/iloc`, 조건 필터 설명 |
| pandas Developers, `Group by: split-apply-combine` | `groupby`를 split-apply-combine 흐름으로 설명하고, 그룹별 집계 예를 제공한다. | `groupby` 입문 설명, 범주별 평균 예 |
| pandas Developers, `10 minutes to pandas` | 열 선택, 슬라이싱, 불리언 필터, 집계와 같은 기본 조작 예를 제공한다. | 초심자용 예제 구성과 범위 조절 |

## 작성 판단

- 12.1이 DataFrame 구조 소개였으므로 12.2는 `표를 어떻게 좁혀 읽는가`에 범위를 제한했다.
- `Series`를 별도 장으로 빼지 않고, 한 열 선택의 자연스러운 결과로만 소개했다.
- `loc`와 `iloc`의 차이는 라벨과 위치 구분까지만 남기고, 슬라이스의 모든 변형은 다루지 않았다.
- 집계는 `mean`, `max`, `count` 정도의 기본 요약으로 제한했다.
- `groupby`는 split-apply-combine의 엄밀한 구조보다 “같은 범주끼리 묶고 나서 요약한다”는 흐름으로 단순화했다.
- `merge`, `join`, `pivot`, 결측치 처리는 12.3 이후 범위로 넘겼다.

## 본문에 반영한 안전한 설명

- 한 열 선택은 보통 `Series`, 여러 열 선택은 `DataFrame` 결과로 읽을 수 있다고 설명했다.
- `loc`는 라벨, `iloc`는 위치를 기준으로 고른다고 설명했다.
- 조건 필터는 각 행에 대해 `True/False`를 만든 뒤 `True`인 행만 남기는 방식으로 설명했다.
- 집계는 많은 행을 더 작은 요약값으로 바꾸는 과정으로 설명했다.
- `groupby`는 같은 값을 가진 행을 먼저 묶고, 각 묶음에 집계를 적용하는 방식으로 설명했다.

## 제외한 내용

- 다중 조건 슬라이싱의 세부 규칙
- `query`
- `assign`
- `sort_values`
- `value_counts`
- `agg`와 `transform`의 차이
- 다중 키 `groupby`
- `pivot_table`

이 내용은 뒤 절에서 데이터 준비와 함께 필요한 만큼 확장한다.
