# 7.4 근거 검토 메모

이 문서는 `docs/parts/part-01/chapter-07/section-04.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- Chapter 7의 일반 원리인 탐색(search), 휴리스틱(heuristic), 계층화(layering)를 자율주행 경로 계획 사례에 연결합니다.
- 사용자의 질문인 웨이포인트, 글로벌 플래너, 로컬 플래너를 도메인 용어 나열이 아니라 일반화된 표현의 역사와 구조로 정리합니다.
- 자율주행 구현 세부를 과도하게 설명하지 않고, `큰 경로`와 `짧은 궤적`의 구분을 입문 수준에서 설명합니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Poole & Mackworth, `3.1 Problem Solving as Search` | `.tmp/section-7-4-poole-search.html` | 길찾기와 경로 문제를 그래프 위의 path finding으로 추상화하는 고전적 설명 |
| DARPA, `Route Network Definition File (RNDF) and Mission Data File (MDF) Formats` | `.tmp/section-7-4-rndf-mdf.pdf` 메타데이터와 파일 제목 수준 확인 | Urban Challenge 시기에 도로 네트워크와 미션 경로를 구조적 파일 형식으로 다뤘다는 역사적 배경 |
| Teng et al., `Motion Planning for Autonomous Driving: The State of the Art and Future Perspectives` | `.tmp/section-7-4-motion-planning-survey.html` | 자율주행에서 motion planning, pipeline planning, tracking controller가 핵심이라는 최근 정리 |
| Jiang et al., `A Dynamic Motion Planning Framework for Autonomous Driving in Urban Environments` | `.tmp/section-7-4-dynamic-motion-planning.html` | road centerline 기반 참조선, candidate trajectories 생성과 평가, trajectory tracking, control 연결 설명 |

## 확인한 원문 위치

- `.tmp/section-7-4-poole-search.html`
  - graph 위 start node에서 goal node까지 path를 찾는 추상화: `p1`, `p2`
  - computer maps path finding 예시와 best route 기준: `Example 3.1`
  - humans find satisficing solutions and heuristic knowledge guides search: `p5`, `p6`
- `.tmp/section-7-4-motion-planning-survey.html`
  - `motion planners`와 `tracking controllers`가 intelligent vehicle의 essential prerequisites라는 추상 설명: meta description, citation abstract
  - `pipeline planning`과 `end-to-end planning` 구분: meta description, citation abstract
- `.tmp/section-7-4-dynamic-motion-planning.html`
  - `Given road centerline`으로 시작하는 참조선 기반 설명: meta description, citation abstract
  - `candidate trajectory sets are generated and evaluated` 설명: meta description, citation abstract
  - `trajectory tracking`과 steering/acceleration control로의 변환 설명: meta description, citation abstract
- `.tmp/section-7-4-rndf-mdf.pdf`
  - `pdfinfo` 결과에서 제목이 `DARPA Grand Challenge 2005`로 노출되어 archive capture의 정확성에 불확실성이 있음
  - URL 자체는 RNDF/MDF format 문서를 가리키므로, 본문에서는 `Urban Challenge 시기의 구조적 경로 표현`이라는 제한적 역사 배경으로만 사용

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 길찾기 문제는 그래프 위의 경로 탐색으로 추상화할 수 있다 | Poole & Mackworth 3.1 | 유지 |
| 실제 차량 시스템에서는 큰 경로 계획과 즉시 움직임 계획을 같은 층위에서 다루기 어렵다 | Poole의 추상 path finding과 자율주행 motion planning survey, dynamic planning framework를 연결한 일반화 | 유지. `많은 시스템`, `보통` 같은 완화 표현 사용 |
| 웨이포인트는 큰 경로를 기준점들의 열로 다루게 해 주는 표현이다 | RNDF/MDF의 역사적 배경과 일반적인 path representation 관행을 바탕으로 한 보수적 일반화 | 유지. 특정 파일 형식 세부 정의는 쓰지 않음 |
| 글로벌 플래너는 큰 길의 흐름을 정하고, 로컬 플래너는 짧은 궤적 후보를 생성·평가한다 | dynamic planning framework의 road centerline, candidate trajectories, tracking 설명과 최근 survey의 motion planner 정리를 바탕으로 한 입문 수준 요약 | 유지 |
| 로컬 플래너의 핵심은 예측 자체보다 candidate trajectories 생성과 선택에 있다 | dynamic planning framework의 abstract에 명시된 generated and evaluated trajectory sets | 유지 |
| prediction과 planning은 많은 시스템에서 구분될 수 있다 | 일반적인 자율주행 스택의 보수적 요약 | 유지. 별도 prediction survey 근거가 없으므로 `많은 시스템에서`로 제한 |
| path/route와 trajectory는 같은 말이 아니다 | Poole의 route/path와 motion planning 논문의 trajectory를 비교한 개념 일반화 | 유지 |
| 자율주행 경로 계획은 탐색 공간을 층위화해 다루는 사례다 | Chapter 7 전체의 개념과 자율주행 계획 문헌 연결 | 유지 |

## 보수화한 표현

- `모든 자율주행 시스템은 글로벌 플래너와 로컬 플래너를 가진다`고 쓰지 않았습니다. 구현은 다양하므로 `많은 시스템`, `보통`, `입문 단계에서는`으로 제한했습니다.
- RNDF/MDF 문서는 archive capture 상태가 완전히 깨끗하지 않아, 차선 수, zone, checkpoint 같은 세부 포맷 설명은 본문에서 제외했습니다.
- `웨이포인트를 따라간다`는 표현은 독자가 익숙해 보여도, 본문에서는 `웨이포인트나 기준선을 참고해 실제 궤적을 만든다`로 보수화했습니다.
- prediction 모듈은 별도 근거가 충분하지 않아 자세히 전개하지 않았고, planning에 입력을 주는 경우가 많다는 수준으로만 적었습니다.
- behavior planner라는 표현은 업계에서 널리 쓰이지만, 이번 절의 중심 질문이 아니므로 표제 수준으로 올리지 않았습니다.
- 강화학습, end-to-end driving, HD map 제작은 범위 밖으로 두었습니다.

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 7.1 | 탐색 공간과 계산 한계 |
| 7.2 | 휴리스틱이 탐색에서 무엇을 줄이는가 |
| 7.3 | 휴리스틱과 확률 모델의 차이 |
| 7.4 | 자율주행 사례로 보는 경로 표현, 층위 분리, 후보 궤적 선택 |
| Part 2 P2-9 | 그래프(graph) 자료구조와 관계 표현 |
| Part 3 P3-2.3 | 강화학습을 자율주행 전체와 혼동하지 않도록 별도 구분 |

## 남은 검토 사항

- RNDF/MDF 원문을 더 안정적으로 추출할 수 있으면 waypoint와 route network 표현을 더 정확히 보강할 수 있습니다.
- 이후 Part 6 프로젝트에서 로봇, 내비게이션, 자율주행 예시를 추가할 경우, route, path, trajectory, control의 계층을 별도 그림으로 정리할 수 있습니다.
